from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cross-Border Semantic Negotiation API",
    description="EU Digital Services Semantic Interoperability with Claude + Mistral",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Request/Response models
class NegotiationRequest(BaseModel):
    italian_schema: Dict
    german_schema: Dict
    confidence_threshold: float = 0.8

class NegotiationResponse(BaseModel):
    session_id: str
    status: str
    message: str

# Global session storage (in production, use Redis)
session_store = {}
active_connections: Dict[str, WebSocket] = {}

# Enhanced mock services with detailed step tracking
class MockClaudeService:
    def __init__(self):
        self.model = "claude-3-5-sonnet-20241022"
    
    async def find_similar_concepts(self, source_concept: str, target_concepts: List[str], session_id: str) -> List[Tuple[str, float]]:
        """Mock semantic similarity matching with detailed steps"""
        await self._notify_step(session_id, f"🧠 Claude analyzing: '{source_concept.split(':')[0]}'")
        await asyncio.sleep(0.5)
        
        await self._notify_step(session_id, f"📊 Computing semantic embeddings for {len(target_concepts)} German concepts...")
        await asyncio.sleep(0.3)
        
        # Mock similarity calculation with explanations
        similarities = []
        for target in target_concepts:
            target_name = target.split(':')[0]
            
            # Mock similarity logic with explanations
            if "name" in source_concept.lower() and "name" in target.lower():
                similarity = 0.9
                reason = f"Strong lexical similarity: both are name fields"
            elif "date" in source_concept.lower() and "date" in target.lower():
                similarity = 0.85
                reason = f"Temporal field match: both represent dates"
            elif "place" in source_concept.lower() and "place" in target.lower():
                similarity = 0.8
                reason = f"Location field match: both represent places"
            elif "tax" in source_concept.lower() or "fiscal" in source_concept.lower():
                similarity = 0.6
                reason = f"Identity field: may map to nationality/identity"
            else:
                similarity = 0.4
                reason = f"Low semantic overlap detected"
            
            similarities.append((target, similarity))
            await self._notify_step(session_id, f"  ↳ {target_name}: {similarity:.2f} ({reason})")
            await asyncio.sleep(0.2)
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        await self._notify_step(session_id, f"✅ Claude found {len(similarities)} candidate matches")
        return similarities
    
    async def _notify_step(self, session_id: str, message: str):
        """Send detailed step information via WebSocket"""
        if session_id in active_connections:
            try:
                await active_connections[session_id].send_json({
                    'type': 'step',
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"WebSocket send error: {e}")

class MockMistralService:
    def __init__(self):
        self.model = "mistral-large-latest"
    
    async def generate_alignment_decision(self, source_concept: Dict, candidate_targets: List[Tuple[str, float]], 
                                        context: str, session_id: str) -> Dict:
        """Mock alignment decision generation with detailed reasoning"""
        
        source_name = source_concept['name']
        await self._notify_step(session_id, f"🤖 Mistral analyzing alignment for '{source_name}'...")
        await asyncio.sleep(0.3)
        
        if not candidate_targets:
            await self._notify_step(session_id, f"❌ No suitable candidates found for '{source_name}'")
            return {
                "best_match": "unknown",
                "confidence": 0.5,
                "reasoning": "No suitable candidates found",
                "transformation_rule": None
            }
        
        # Show top candidates being considered
        await self._notify_step(session_id, f"🎯 Evaluating top {min(3, len(candidate_targets))} candidates:")
        for i, (target, similarity) in enumerate(candidate_targets[:3]):
            target_name = target.split(':')[0]
            await self._notify_step(session_id, f"  {i+1}. {target_name} (similarity: {similarity:.2f})")
            await asyncio.sleep(0.2)
        
        best_target, similarity = candidate_targets[0]
        best_target_name = best_target.split(':')[0]
        
        await self._notify_step(session_id, f"🔍 Analyzing semantic compatibility...")
        await asyncio.sleep(0.4)
        
        # Mock transformation rules based on field types
        transformation_rule = None
        transformation_explanation = ""
        
        if "date" in source_concept['name'].lower():
            transformation_rule = {
                "type": "data_conversion",
                "source_format": "DD/MM/YYYY",
                "target_format": "ISO8601",
                "conversion_logic": "Convert Italian date format to ISO 8601"
            }
            transformation_explanation = "Date format conversion required"
            await self._notify_step(session_id, f"📅 {transformation_explanation}: DD/MM/YYYY → ISO8601")
            
        elif "name" in source_concept['name'].lower():
            transformation_rule = {
                "type": "field_mapping",
                "source_format": "italian_naming",
                "target_format": "german_naming",
                "conversion_logic": "Direct field mapping with cultural considerations"
            }
            transformation_explanation = "Direct field mapping"
            await self._notify_step(session_id, f"👤 {transformation_explanation}: {source_name} → {best_target_name}")
            
        elif "fiscal" in source_concept['name'].lower() or "tax" in source_concept['name'].lower():
            transformation_rule = {
                "type": "identity_derivation",
                "source_format": "codice_fiscale",
                "target_format": "nationality",
                "conversion_logic": "Derive nationality from Italian tax code"
            }
            transformation_explanation = "Identity field derivation"
            await self._notify_step(session_id, f"🆔 {transformation_explanation}: Extract nationality from tax code")
        
        # Calculate final confidence with explanation
        base_confidence = min(similarity + 0.1, 1.0)
        confidence_factors = []
        
        if similarity > 0.8:
            confidence_factors.append("High semantic similarity")
        if transformation_rule:
            confidence_factors.append("Clear transformation path")
            base_confidence += 0.05
        if source_concept['required'] and "required" in best_target.lower():
            confidence_factors.append("Both fields are required")
            base_confidence += 0.03
        
        final_confidence = min(base_confidence, 1.0)
        
        await self._notify_step(session_id, f"📊 Confidence calculation:")
        await self._notify_step(session_id, f"  ↳ Base similarity: {similarity:.2f}")
        for factor in confidence_factors:
            await self._notify_step(session_id, f"  ↳ Boost: {factor}")
        await self._notify_step(session_id, f"  ↳ Final confidence: {final_confidence:.2f}")
        
        await asyncio.sleep(0.3)
        
        # GDPR/eIDAS compliance check
        await self._notify_step(session_id, f"🔒 Checking EU compliance (GDPR, eIDAS)...")
        await asyncio.sleep(0.2)
        await self._notify_step(session_id, f"✅ Mapping complies with EU data protection regulations")
        
        decision = {
            "best_match": best_target_name,
            "confidence": final_confidence,
            "reasoning": f"Selected {best_target_name} with {final_confidence:.0%} confidence. {transformation_explanation if transformation_explanation else 'Direct mapping possible.'}",
            "transformation_rule": transformation_rule,
            "compliance_notes": "GDPR and eIDAS compliant mapping",
            "similarity_score": similarity,
            "confidence_factors": confidence_factors
        }
        
        await self._notify_step(session_id, f"✅ Decision: {source_name} → {best_target_name} ({final_confidence:.0%} confidence)")
        
        return decision
    
    async def _notify_step(self, session_id: str, message: str):
        """Send detailed step information via WebSocket"""
        if session_id in active_connections:
            try:
                await active_connections[session_id].send_json({
                    'type': 'step',
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"WebSocket send error: {e}")

class SemanticNegotiator:
    def __init__(self, claude_service, mistral_service):
        self.claude_service = claude_service
        self.mistral_service = mistral_service
    
    async def negotiate_schemas(self, italian_schema: Dict, german_schema: Dict) -> str:
        """Main negotiation pipeline with detailed step tracking"""
        session_id = str(uuid.uuid4())
        
        # Initialize session
        session_store[session_id] = {
            'status': 'started',
            'progress': 0,
            'start_time': datetime.now(),
            'steps': [],
            'current_step': 'initializing'
        }
        
        try:
            # Step 1: Schema Analysis
            await self._update_session(session_id, 'analyzing_schemas', 5, "🔍 Analyzing Italian and German schemas...")
            await asyncio.sleep(0.5)
            
            italian_concepts = self._extract_concepts(italian_schema, 'italian')
            german_concepts = self._extract_concepts(german_schema, 'german')
            
            await self._notify_step(session_id, f"📋 Extracted {len(italian_concepts)} Italian concepts:")
            for concept in italian_concepts:
                await self._notify_step(session_id, f"  • {concept['name']}: {concept['description']}")
                await asyncio.sleep(0.1)
            
            await self._notify_step(session_id, f"📋 Extracted {len(german_concepts)} German concepts:")
            for concept in german_concepts:
                await self._notify_step(session_id, f"  • {concept['name']}: {concept['description']}")
                await asyncio.sleep(0.1)
            
            logger.info(f"Extracted {len(italian_concepts)} Italian and {len(german_concepts)} German concepts")
            
            # Step 2: Semantic Matching Process
            await self._update_session(session_id, 'semantic_matching', 15, "🧠 Starting semantic matching process...")
            alignments = []
            
            for i, italian_concept in enumerate(italian_concepts):
                # Update progress
                progress = 15 + (i / len(italian_concepts)) * 70
                await self._update_session(session_id, f'processing_concept_{i+1}', int(progress), 
                                         f"Processing concept {i+1}/{len(italian_concepts)}: {italian_concept['name']}")
                
                await self._notify_step(session_id, f"\n🎯 === Processing '{italian_concept['name']}' ===")
                
                # Use Claude for semantic matching
                similar_concepts = await self.claude_service.find_similar_concepts(
                    source_concept=italian_concept['text'],
                    target_concepts=[gc['text'] for gc in german_concepts],
                    session_id=session_id
                )
                
                # Use Mistral for alignment decision
                context = self._build_context(italian_concept, german_concepts)
                alignment = await self.mistral_service.generate_alignment_decision(
                    source_concept=italian_concept,
                    candidate_targets=similar_concepts[:5],
                    context=context,
                    session_id=session_id
                )
                
                alignments.append({
                    'source': italian_concept,
                    'alignment': alignment,
                    'timestamp': datetime.now().isoformat()
                })
                
                await asyncio.sleep(0.3)
            
            # Step 3: Generate Transformation Rules
            await self._update_session(session_id, 'generating_transformations', 90, "⚙️ Generating transformation rules...")
            await self._notify_step(session_id, f"\n🔧 === Generating Transformation Rules ===")
            
            transformation_rules = self._generate_transformation_rules(alignments)
            
            await self._notify_step(session_id, f"📝 Generated {len(transformation_rules)} transformation rules:")
            for rule in transformation_rules:
                await self._notify_step(session_id, f"  • {rule['source_field']} → {rule['target_field']}: {rule['type']}")
                await asyncio.sleep(0.1)
            
            # Step 4: Final Analysis
            await self._update_session(session_id, 'final_analysis', 95, "📊 Computing final analysis...")
            await self._notify_step(session_id, f"\n📊 === Final Analysis ===")
            
            overall_confidence = self._calculate_overall_confidence(alignments)
            compliance_status = self._check_compliance(alignments)
            
            await self._notify_step(session_id, f"🎯 Overall confidence: {overall_confidence:.1%}")
            await self._notify_step(session_id, f"✅ GDPR compliance: {compliance_status['gdpr_compliant']}")
            await self._notify_step(session_id, f"✅ eIDAS compliance: {compliance_status['eidas_compliant']}")
            await self._notify_step(session_id, f"✅ Once-Only Principle: {compliance_status['once_only_supported']}")
            
            await self._update_session(session_id, 'completed', 100, "🎉 Semantic negotiation completed successfully!")
            
            result = {
                'session_id': session_id,
                'alignments': alignments,
                'transformation_rules': transformation_rules,
                'overall_confidence': overall_confidence,
                'compliance_status': compliance_status,
                'processing_time': (datetime.now() - session_store[session_id]['start_time']).total_seconds(),
                'summary': {
                    'total_concepts': len(italian_concepts),
                    'successful_alignments': len([a for a in alignments if a['alignment']['confidence'] > 0.7]),
                    'high_confidence_alignments': len([a for a in alignments if a['alignment']['confidence'] > 0.8]),
                    'transformation_rules_count': len(transformation_rules)
                }
            }
            
            session_store[session_id]['result'] = result
            return session_id
            
        except Exception as e:
            logger.error(f"Error in negotiation: {e}")
            await self._update_session(session_id, 'error', 0, f"❌ Error: {str(e)}")
            raise
    
    async def _update_session(self, session_id: str, status: str, progress: int, message: str = None):
        """Update session status and notify WebSocket clients"""
        if session_id in session_store:
            session_store[session_id].update({
                'status': status,
                'progress': progress,
                'last_update': datetime.now(),
                'current_step': status
            })
            
            # Notify WebSocket clients
            if session_id in active_connections:
                try:
                    await active_connections[session_id].send_json({
                        'type': 'progress',
                        'session_id': session_id,
                        'status': status,
                        'progress': progress,
                        'message': message or f"Processing: {status.replace('_', ' ').title()}",
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.error(f"WebSocket send error: {e}")
    
    async def _notify_step(self, session_id: str, message: str):
        """Send detailed step information via WebSocket"""
        if session_id in active_connections:
            try:
                await active_connections[session_id].send_json({
                    'type': 'step',
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"WebSocket send error: {e}")
    
    def _extract_concepts(self, schema: Dict, source: str) -> List[Dict]:
        """Extract semantic concepts from schema"""
        concepts = []
        properties = schema.get('properties', {})
        required_fields = schema.get('required', [])
        
        for field_name, field_info in properties.items():
            concept = {
                'name': field_name,
                'type': field_info.get('type', 'string'),
                'description': field_info.get('description', ''),
                'required': field_name in required_fields,
                'source': source,
                'text': f"{field_name}: {field_info.get('type', '')} - {field_info.get('description', '')}"
            }
            concepts.append(concept)
        
        return concepts
    
    def _build_context(self, italian_concept: Dict, german_concepts: List[Dict]) -> str:
        """Build context for LLM decision making"""
        return f"""
        CROSS-BORDER CONTEXT:
        - Source: Italian ANPR → Target: German Civil Registry
        - Use Case: Birth certificate for job application
        - Standards: eIDAS, GDPR, Once-Only Principle
        
        Italian Field: {italian_concept['name']} ({italian_concept['type']})
        Description: {italian_concept['description']}
        Required: {italian_concept['required']}
        """
    
    def _generate_transformation_rules(self, alignments: List[Dict]) -> List[Dict]:
        """Generate transformation rules"""
        rules = []
        for alignment in alignments:
            if alignment['alignment'].get('transformation_rule'):
                rule = alignment['alignment']['transformation_rule']
                rule.update({
                    'source_field': alignment['source']['name'],
                    'target_field': alignment['alignment']['best_match'],
                    'confidence': alignment['alignment']['confidence']
                })
                rules.append(rule)
        return rules
    
    def _calculate_overall_confidence(self, alignments: List[Dict]) -> float:
        """Calculate overall confidence"""
        if not alignments:
            return 0.0
        total_confidence = sum(a['alignment']['confidence'] for a in alignments)
        return total_confidence / len(alignments)
    
    def _check_compliance(self, alignments: List[Dict]) -> Dict:
        """Check compliance status"""
        return {
            'gdpr_compliant': True,
            'eidas_compliant': True,
            'once_only_supported': True,
            'data_minimization': True,
            'notes': 'All alignments maintain EU regulatory compliance'
        }
    
    def get_session_status(self, session_id: str) -> Dict:
        """Get session status"""
        return session_store.get(session_id, {'status': 'not_found'})
    
    def get_session_result(self, session_id: str) -> Dict:
        """Get session results"""
        session = session_store.get(session_id)
        if session and 'result' in session:
            return session['result']
        return None

# Initialize services
claude_service = MockClaudeService()
mistral_service = MockMistralService()
negotiator = SemanticNegotiator(claude_service, mistral_service)

@app.get("/", response_class=HTMLResponse)
async def serve_demo():
    """Serve the enhanced demo page"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cross-Border Semantic Negotiation</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { 
                max-width: 1400px; 
                margin: 0 auto; 
                background: rgba(255, 255, 255, 0.95); 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            }
            .header { 
                text-align: center; 
                margin-bottom: 30px; 
                padding-bottom: 20px;
                border-bottom: 2px solid #e0e0e0;
            }
            .header h1 {
                background: linear-gradient(45deg, #3498db, #8e44ad);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #7f8c8d;
                font-size: 1.2em;
                margin-bottom: 20px;
            }
            .btn { 
                padding: 15px 30px; 
                background: linear-gradient(45deg, #3498db, #2980b9); 
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer; 
                font-size: 1.1em;
                font-weight: 500;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .btn:hover { 
                background: linear-gradient(45deg, #2980b9, #3498db); 
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            }
            .status-panel { 
                background: #2c3e50; 
                color: white; 
                padding: 25px; 
                border-radius: 10px; 
                margin: 25px 0; 
                font-family: 'Courier New', monospace;
            }
            .hidden { display: none; }
            .progress-bar { 
                background: #34495e; 
                border-radius: 10px; 
                overflow: hidden; 
                margin: 15px 0; 
                height: 25px;
            }
            .progress-fill { 
                height: 100%; 
                background: linear-gradient(45deg, #27ae60, #2ecc71); 
                transition: width 0.3s ease; 
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 0.9em;
            }
            .results { margin: 25px 0; }
            .alignment-card { 
                border: 1px solid #ddd; 
                padding: 20px; 
                margin: 15px 0; 
                border-radius: 10px; 
                background: white;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            }
            .confidence-high { border-left: 5px solid #27ae60; }
            .confidence-medium { border-left: 5px solid #f39c12; }
            .confidence-low { border-left: 5px solid #e74c3c; }
            .step-log {
                background: #ecf0f1;
                border-radius: 5px;
                padding: 15px;
                margin: 15px 0;
                max-height: 400px;
                overflow-y: auto;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                border-left: 4px solid #3498db;
            }
            .step-item {
                margin: 5px 0;
                padding: 3px 0;
                border-bottom: 1px solid #bdc3c7;
            }
            .step-item:last-child {
                border-bottom: none;
            }
            .step-timestamp {
                color: #7f8c8d;
                font-size: 0.8em;
                margin-right: 10px;
            }
            .summary-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .summary-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .summary-number {
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .summary-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌐 Cross-Border Semantic Negotiation</h1>
                <p class="subtitle">Real-time processing with detailed step-by-step analysis</p>
                <p style="color: #7f8c8d; font-style: italic;">
                    🎯 <strong>Demo:</strong> Italian ANPR ↔ German Civil Registry semantic alignment
                </p>
            </div>
            
            <div style="text-align: center;">
                <button id="startBtn" class="btn">🚀 Start Detailed Semantic Negotiation</button>
            </div>
            
            <div id="statusPanel" class="status-panel hidden">
                <div><strong>Status:</strong> <span id="statusText">Ready</span></div>
                <div class="progress-bar">
                    <div id="progressFill" class="progress-fill" style="width: 0%">0%</div>
                </div>
                
                <div style="margin-top: 20px;">
                    <strong>🔍 Processing Steps:</strong>
                    <div id="stepLog" class="step-log"></div>
                </div>
            </div>
            
            <div id="results" class="results hidden">
                <h2>📊 Semantic Negotiation Results</h2>
                
                <div id="summaryCards" class="summary-grid"></div>
                
                <h3>🎯 Field Alignments</h3>
                <div id="alignmentResults"></div>
            </div>
        </div>
        
        <script>
            let sessionId = null;
            let websocket = null;
            
            document.getElementById('startBtn').addEventListener('click', startNegotiation);
            
            async function startNegotiation() {
                const italianSchema = {
                    "properties": {
                        "cognome": {"type": "string", "description": "Family name"},
                        "nome": {"type": "string", "description": "Given name"},
                        "data_nascita": {"type": "string", "format": "date", "description": "Birth date"},
                        "luogo_nascita": {"type": "string", "description": "Place of birth"},
                        "codice_fiscale": {"type": "string", "description": "Italian tax code"}
                    },
                    "required": ["cognome", "nome", "data_nascita", "luogo_nascita", "codice_fiscale"]
                };
                
                const germanSchema = {
                    "properties": {
                        "familienname": {"type": "string", "description": "Family name"},
                        "vorname": {"type": "string", "description": "Given name"},
                        "geburtsdatum": {"type": "string", "format": "date-time", "description": "Birth date"},
                        "geburtsort": {"type": "string", "description": "Place of birth"},
                        "staatsangehoerigkeit": {"type": "string", "description": "Nationality"}
                    },
                    "required": ["familienname", "vorname", "geburtsdatum", "geburtsort", "staatsangehoerigkeit"]
                };
                
                try {
                    const response = await fetch('/api/negotiate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            italian_schema: italianSchema,
                            german_schema: germanSchema
                        })
                    });
                    
                    const result = await response.json();
                    sessionId = result.session_id;
                    
                    showStatus();
                    clearStepLog();
                    connectWebSocket();
                    
                } catch (error) {
                    console.error('Error:', error);
                    updateStatus('Error starting negotiation');
                }
            }
            
            function showStatus() {
                document.getElementById('statusPanel').classList.remove('hidden');
                document.getElementById('results').classList.add('hidden');
            }
            
            function updateStatus(message, progress = 0) {
                document.getElementById('statusText').textContent = message;
                const progressFill = document.getElementById('progressFill');
                progressFill.style.width = progress + '%';
                progressFill.textContent = progress + '%';
            }
            
            function addStep(message, timestamp) {
                const stepLog = document.getElementById('stepLog');
                const stepItem = document.createElement('div');
                stepItem.className = 'step-item';
                
                const time = new Date(timestamp).toLocaleTimeString();
                stepItem.innerHTML = `
                    <span class="step-timestamp">[${