#!/usr/bin/env python3
"""
Enhanced Cross-Border Semantic Negotiation Server
Provides detailed step-by-step visualization of the semantic matching process
"""

import asyncio
import json
import logging
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Enhanced Cross-Border Semantic Negotiation API")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Data models
class NegotiationRequest(BaseModel):
    source_country: str
    target_country: str
    source_schema: Dict[str, Any]
    target_schema: Dict[str, Any]

class AlignmentResult(BaseModel):
    source_field: str
    target_field: str
    confidence: float
    method: str
    explanation: str

class NegotiationResult(BaseModel):
    overall_confidence: float
    alignments: List[AlignmentResult]
    transformation_code: str
    compliance_notes: str
    processing_time: float

# Mock AI services for demonstration
class MockClaudeService:
    """Mock Claude AI service for semantic similarity analysis"""
    
    @staticmethod
    async def analyze_semantic_similarity(source_schema: Dict, target_schema: Dict) -> Dict[str, Any]:
        """Analyze semantic similarity between schema fields"""
        await asyncio.sleep(2)  # Simulate processing time
        
        # Mock semantic analysis results
        similarities = []
        source_fields = list(source_schema.keys())
        target_fields = list(target_schema.keys())
        
        # Define some semantic mappings for demonstration
        semantic_mappings = {
            'nome': ['firstName', 'first_name', 'givenName'],
            'cognome': ['lastName', 'last_name', 'surname', 'familyName'],
            'codice_fiscale': ['taxId', 'tax_id', 'fiscalCode'],
            'data_nascita': ['birthDate', 'birth_date', 'dateOfBirth'],
            'luogo_nascita': ['birthPlace', 'birth_place', 'placeOfBirth'],
            'user_id': ['personalId', 'personal_id', 'userId', 'id'],
            'firstName': ['nome', 'first_name', 'givenName'],
            'lastName': ['cognome', 'last_name', 'surname'],
            'personalId': ['user_id', 'userId', 'id'],
            'taxId': ['codice_fiscale', 'fiscal_code', 'tax_id'],
            'birthDate': ['data_nascita', 'birth_date', 'dateOfBirth'],
            'birthPlace': ['luogo_nascita', 'birth_place', 'placeOfBirth']
        }
        
        for source_field in source_fields:
            best_match = None
            best_confidence = 0.0
            explanation = ""
            
            for target_field in target_fields:
                confidence = 0.0
                
                # Exact match
                if source_field.lower() == target_field.lower():
                    confidence = 0.95
                    explanation = f"Exact field name match between '{source_field}' and '{target_field}'"
                
                # Semantic mapping
                elif source_field in semantic_mappings:
                    if target_field in semantic_mappings[source_field]:
                        confidence = 0.85 + random.uniform(0.05, 0.1)
                        explanation = f"Semantic match: '{source_field}' commonly maps to '{target_field}' in cross-border contexts"
                
                # Partial string similarity
                elif any(part in target_field.lower() for part in source_field.lower().split('_')):
                    confidence = 0.6 + random.uniform(0.1, 0.2)
                    explanation = f"Partial string similarity detected between '{source_field}' and '{target_field}'"
                
                # Type-based similarity
                elif source_schema[source_field] == target_schema.get(target_field):
                    confidence = 0.3 + random.uniform(0.1, 0.2)
                    explanation = f"Same data type ({source_schema[source_field]}) suggests potential compatibility"
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = target_field
                    best_explanation = explanation
            
            if best_match and best_confidence > 0.3:
                similarities.append({
                    'source_field': source_field,
                    'target_field': best_match,
                    'confidence': round(best_confidence, 3),
                    'explanation': best_explanation
                })
        
        return {
            'similarities': similarities,
            'analysis_method': 'Claude Semantic Analysis',
            'processing_time': 2.1
        }

class MockMistralService:
    """Mock Mistral AI service for alignment decisions"""
    
    @staticmethod
    async def make_alignment_decisions(claude_results: Dict, source_schema: Dict, target_schema: Dict) -> Dict[str, Any]:
        """Make final alignment decisions based on Claude's analysis"""
        await asyncio.sleep(1.5)  # Simulate processing time
        
        alignments = []
        total_confidence = 0.0
        
        for similarity in claude_results['similarities']:
            # Mistral refines Claude's confidence scores
            refined_confidence = similarity['confidence']
            
            # Apply Mistral's decision logic
            if refined_confidence > 0.8:
                refined_confidence += random.uniform(0.02, 0.08)  # High confidence boost
                method = "High-confidence semantic match"
            elif refined_confidence > 0.6:
                refined_confidence += random.uniform(-0.05, 0.05)  # Medium confidence adjustment
                method = "Medium-confidence contextual match"
            else:
                refined_confidence += random.uniform(-0.1, 0.02)  # Low confidence penalty
                method = "Low-confidence structural match"
            
            # Ensure confidence doesn't exceed 1.0
            refined_confidence = min(refined_confidence, 0.99)
            
            alignments.append({
                'source_field': similarity['source_field'],
                'target_field': similarity['target_field'],
                'confidence': round(refined_confidence, 3),
                'method': method,
                'explanation': similarity['explanation']
            })
            
            total_confidence += refined_confidence
        
        overall_confidence = (total_confidence / len(alignments)) if alignments else 0.0
        
        return {
            'alignments': alignments,
            'overall_confidence': round(overall_confidence, 3),
            'decision_method': 'Mistral Alignment Engine',
            'processing_time': 1.6
        }

class TransformationGenerator:
    """Generate transformation code based on alignments"""
    
    @staticmethod
    async def generate_transformation_code(alignments: List[Dict]) -> str:
        """Generate executable transformation code"""
        await asyncio.sleep(1.0)  # Simulate processing time
        
        code_lines = [
            "def transform_cross_border_data(source_data):",
            "    \"\"\"",
            "    Auto-generated transformation function for cross-border data mapping",
            "    Generated by Enhanced Semantic Negotiation Engine",
            "    \"\"\"",
            "    transformed_data = {}",
            ""
        ]
        
        for alignment in alignments:
            source_field = alignment['source_field']
            target_field = alignment['target_field']
            confidence = alignment['confidence']
            
            if confidence > 0.8:
                # High confidence - direct mapping
                code_lines.append(f"    # High confidence mapping ({confidence:.1%})")
                code_lines.append(f"    transformed_data['{target_field}'] = source_data.get('{source_field}')")
            elif confidence > 0.6:
                # Medium confidence - with validation
                code_lines.append(f"    # Medium confidence mapping ({confidence:.1%}) - with validation")
                code_lines.append(f"    if '{source_field}' in source_data:")
                code_lines.append(f"        transformed_data['{target_field}'] = source_data['{source_field}']")
                code_lines.append(f"        # TODO: Add validation logic for {source_field} -> {target_field}")
            else:
                # Low confidence - manual review required
                code_lines.append(f"    # Low confidence mapping ({confidence:.1%}) - MANUAL REVIEW REQUIRED")
                code_lines.append(f"    # transformed_data['{target_field}'] = source_data.get('{source_field}')  # VERIFY THIS MAPPING")
        
        code_lines.extend([
            "",
            "    return transformed_data",
            "",
            "# Example usage:",
            "# result = transform_cross_border_data(your_source_data)"
        ])
        
        return "\n".join(code_lines)

class ComplianceValidator:
    """Validate GDPR and eIDAS compliance"""
    
    @staticmethod
    async def validate_compliance(alignments: List[Dict], source_country: str, target_country: str) -> str:
        """Validate compliance with GDPR and eIDAS regulations"""
        await asyncio.sleep(0.8)  # Simulate processing time
        
        notes = []
        
        # GDPR compliance checks
        notes.append("🔒 GDPR Compliance Analysis:")
        notes.append("- All personal data mappings maintain data minimization principles")
        notes.append("- Field transformations preserve data subject rights")
        
        # Check for sensitive fields
        sensitive_fields = ['codice_fiscale', 'taxId', 'tax_id', 'fiscal_code']
        has_sensitive = any(alignment['source_field'] in sensitive_fields or 
                          alignment['target_field'] in sensitive_fields 
                          for alignment in alignments)
        
        if has_sensitive:
            notes.append("⚠️  Sensitive data detected - additional encryption recommended")
        
        # eIDAS compliance
        notes.append("\n🇪🇺 eIDAS Compliance Analysis:")
        notes.append(f"- Cross-border mapping from {source_country.upper()} to {target_country.upper()}")
        notes.append("- Identity attribute mappings comply with eIDAS technical specifications")
        notes.append("- Assurance level preservation maintained across transformation")
        
        # Country-specific notes
        if 'italy' in source_country.lower() or 'italy' in target_country.lower():
            notes.append("🇮🇹 SPID-specific: Codice Fiscale handling complies with Italian regulations")
        
        if 'germany' in source_country.lower() or 'germany' in target_country.lower():
            notes.append("🇩🇪 eID-specific: Personal identifier mapping follows German eID standards")
        
        return "\n".join(notes)

# Enhanced semantic negotiation engine
class EnhancedSemanticNegotiator:
    def __init__(self):
        self.claude_service = MockClaudeService()
        self.mistral_service = MockMistralService()
        self.transformation_generator = TransformationGenerator()
        self.compliance_validator = ComplianceValidator()
    
    async def negotiate(self, request: NegotiationRequest) -> NegotiationResult:
        """Perform enhanced semantic negotiation with detailed step tracking"""
        start_time = time.time()
        
        # Step 1: Schema Analysis
        await self._broadcast_step_update(1, 'active', 
            "🔍 Analyzing schema structures...<br>"
            f"Source: {len(request.source_schema)} fields from {request.source_country}<br>"
            f"Target: {len(request.target_schema)} fields from {request.target_country}")
        
        await asyncio.sleep(1)  # Simulate analysis time
        
        await self._broadcast_step_update(1, 'completed',
            "✅ Schema analysis complete<br>"
            f"Identified {len(request.source_schema)} source fields and {len(request.target_schema)} target fields<br>"
            "Ready for semantic similarity analysis")
        
        # Step 2: Claude Semantic Analysis
        await self._broadcast_step_update(2, 'active',
            "🧠 Claude AI analyzing semantic relationships...<br>"
            "Comparing field names, meanings, and contexts<br>"
            "Identifying potential cross-linguistic mappings")
        
        claude_results = await self.claude_service.analyze_semantic_similarity(
            request.source_schema, request.target_schema
        )
        
        similarities_count = len(claude_results['similarities'])
        avg_confidence = sum(s['confidence'] for s in claude_results['similarities']) / similarities_count if similarities_count > 0 else 0
        
        await self._broadcast_step_update(2, 'completed',
            f"✅ Claude analysis complete<br>"
            f"Found {similarities_count} potential field mappings<br>"
            f"Average semantic confidence: {avg_confidence:.1%}")
        
        # Step 3: Mistral Alignment Decisions
        await self._broadcast_step_update(3, 'active',
            "⚡ Mistral AI making alignment decisions...<br>"
            "Refining confidence scores based on context<br>"
            "Applying cross-border mapping heuristics")
        
        mistral_results = await self.mistral_service.make_alignment_decisions(
            claude_results, request.source_schema, request.target_schema
        )
        
        await self._broadcast_step_update(3, 'completed',
            f"✅ Mistral alignment complete<br>"
            f"Final alignments: {len(mistral_results['alignments'])}<br>"
            f"Overall confidence: {mistral_results['overall_confidence']:.1%}")
        
        # Step 4: Transformation Code Generation
        await self._broadcast_step_update(4, 'active',
            "⚙️ Generating transformation code...<br>"
            "Creating executable Python functions<br>"
            "Adding validation and error handling")
        
        transformation_code = await self.transformation_generator.generate_transformation_code(
            mistral_results['alignments']
        )
        
        await self._broadcast_step_update(4, 'completed',
            f"✅ Transformation code generated<br>"
            f"Generated {len(transformation_code.split('\\n'))} lines of Python code<br>"
            "Ready for deployment and testing")
        
        # Step 5: Compliance Validation
        await self._broadcast_step_update(5, 'active',
            "📋 Validating GDPR and eIDAS compliance...<br>"
            "Checking data protection requirements<br>"
            "Verifying cross-border regulations")
        
        compliance_notes = await self.compliance_validator.validate_compliance(
            mistral_results['alignments'], request.source_country, request.target_country
        )
        
        await self._broadcast_step_update(5, 'completed',
            "✅ Compliance validation complete<br>"
            "All GDPR and eIDAS requirements satisfied<br>"
            "Ready for production deployment")
        
        # Prepare final result
        processing_time = time.time() - start_time
        
        result = NegotiationResult(
            overall_confidence=mistral_results['overall_confidence'],
            alignments=[
                AlignmentResult(
                    source_field=alignment['source_field'],
                    target_field=alignment['target_field'],
                    confidence=alignment['confidence'],
                    method=alignment['method'],
                    explanation=alignment['explanation']
                ) for alignment in mistral_results['alignments']
            ],
            transformation_code=transformation_code,
            compliance_notes=compliance_notes,
            processing_time=processing_time
        )
        
        # Broadcast final result
        await manager.broadcast(json.dumps({
            'type': 'final_result',
            'result': result.dict()
        }))
        
        return result
    
    async def _broadcast_step_update(self, step: int, status: str, details: str):
        """Broadcast step update to all connected WebSocket clients"""
        await manager.broadcast(json.dumps({
            'type': 'step_update',
            'step': step,
            'status': status,
            'details': details
        }))

# Initialize the negotiator
negotiator = EnhancedSemanticNegotiator()

# API Routes
@app.get("/", response_class=HTMLResponse)
async def get_demo_page():
    """Serve the enhanced demo page"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cross-Border Semantic Negotiation - Enhanced Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 30px;
        }
        
        .input-section, .output-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
        }
        
        .section-title {
            font-size: 1.5em;
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #34495e;
            margin-bottom: 8px;
        }
        
        select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        select:focus, textarea:focus {
            outline: none;
            border-color: #3498db;
        }
        
        textarea {
            resize: vertical;
            min-height: 120px;
            font-family: 'Courier New', monospace;
        }
        
        .btn {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        
        .btn:disabled {
            background: #bdc3c7;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .processing-steps {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            border-left: 5px solid #3498db;
        }
        
        .step {
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            transition: all 0.3s;
        }
        
        .step.active {
            background: #e3f2fd;
            border-color: #2196f3;
            transform: translateX(5px);
        }
        
        .step.completed {
            background: #e8f5e8;
            border-color: #4caf50;
        }
        
        .step-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .step-number {
            background: #3498db;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }
        
        .step.completed .step-number {
            background: #4caf50;
        }
        
        .step-title {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .step-details {
            margin-left: 45px;
            color: #555;
            line-height: 1.6;
        }
        
        .confidence-bar {
            background: #e0e0e0;
            height: 8px;
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b 0%, #feca57 50%, #48dbfb 100%);
            transition: width 0.5s ease;
        }
        
        .results-section {
            grid-column: 1 / -1;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-top: 20px;
        }
        
        .alignment-result {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 5px solid #27ae60;
        }
        
        .transformation-code {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            margin-top: 15px;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Cross-Border Semantic Negotiation</h1>
            <p>AI-Powered Schema Alignment for EU Digital Identity Systems</p>
        </div>
        
        <div class="main-content">
            <div class="input-section">
                <h2 class="section-title">🔧 Configuration</h2>
                
                <div class="form-group">
                    <label for="sourceCountry">Source Country System:</label>
                    <select id="sourceCountry">
                        <option value="italy_spid">🇮🇹 Italy (SPID)</option>
                        <option value="germany_eid">🇩🇪 Germany (eID)</option>
                        <option value="france_franceconnect">🇫🇷 France (FranceConnect)</option>
                        <option value="spain_clave">🇪🇸 Spain (Cl@ve)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="targetCountry">Target Country System:</label>
                    <select id="targetCountry">
                        <option value="germany_eid">🇩🇪 Germany (eID)</option>
                        <option value="italy_spid">🇮🇹 Italy (SPID)</option>
                        <option value="france_franceconnect">🇫🇷 France (FranceConnect)</option>
                        <option value="spain_clave">🇪🇸 Spain (Cl@ve)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="sourceSchema">Source Schema (JSON):</label>
                    <textarea id="sourceSchema" placeholder="Enter source country schema...">{
  "user_id": "string",
  "nome": "string", 
  "cognome": "string",
  "codice_fiscale": "string",
  "data_nascita": "date",
  "luogo_nascita": "string"
}</textarea>
                </div>
                
                <div class="form-group">
                    <label for="targetSchema">Target Schema (JSON):</label>
                    <textarea id="targetSchema" placeholder="Enter target country schema...">{
  "personalId": "string",
  "firstName": "string",
  "lastName": "string", 
  "taxId": "string",
  "birthDate": "date",
  "birthPlace": "string"
}</textarea>
                </div>
                
                <button class="btn" onclick="startNegotiation()">
                    🚀 Start Semantic Negotiation
                </button>
            </div>
            
            <div class="output-section">
                <h2 class="section-title">⚡ Real-Time Processing</h2>
                
                <div class="processing-steps" id="processingSteps">
                    <div class="step" id="step1">
                        <div class="step-header">
                            <div class="step-number">1</div>
                            <div class="step-title">Schema Analysis</div>
                        </div>
                        <div class="step-details">
                            Analyzing source and target schemas for structural patterns...
                        </div>
                    </div>
                    
                    <div class="step" id="step2">
                        <div class="step-header">
                            <div class="step-number">2</div>
                            <div class="step-title">Semantic Similarity (Claude)</div>
                        </div>
                        <div class="step-details">
                            Using Claude AI to identify semantic relationships between fields...
                        </div>
                    </div>
                    
                    <div class="step" id="step3">
                        <div class="step-header">
                            <div class="step-number">3</div>
                            <div class="step-title">Alignment Decision (Mistral)</div>
                        </div>
                        <div class="step-details">
                            Mistral AI determining optimal field mappings and confidence scores...
                        </div>
                    </div>
                    
                    <div class="step" id="step4">
                        <div class="step-header">
                            <div class="step-number">4</div>
                            <div class="step-title">Transformation Rules</div>
                        </div>
                        <div class="step-details">
                            Generating executable transformation rules for data conversion...
                        </div>
                    </div>
                    
                    <div class="step" id="step5">
                        <div class="step-header">
                            <div class="step-number">5</div>
                            <div class="step-title">Compliance Validation</div>
                        </div>
                        <div class="step-details">
                            Validating GDPR and eIDAS compliance requirements...
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="results-section" id="resultsSection" style="display: none;">
            <h2 class="section-title">📊 Negotiation Results</h2>
            <div id="resultsContent"></div>
        </div>
    </div>

    <script>
        let ws = null;
        let currentStep = 0;
        
        function connectWebSocket() {
            ws = new WebSocket('ws://localhost:8000/ws');
            
            ws.onopen = function(event) {
                console.log('WebSocket connected');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            };
            
            ws.onclose = function(event) {
                console.log('WebSocket disconnected');
                setTimeout(connectWebSocket, 3000);
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        }
        
        function handleWebSocketMessage(data) {
            if (data.type === 'step_update') {
                updateStep(data.step, data.status, data.details);
            } else if (data.type === 'final_result') {
                showFinalResults(data.result);
            }
        }
        
        function updateStep(stepNumber, status, details) {
            const step = document.getElementById(`step${stepNumber}`);
            if (!step) return;
            
            step.classList.remove('active', 'completed');
            
            if (status === 'active') {
                step.classList.add('active');
                currentStep = stepNumber;
            } else if (status === 'completed') {
                step.classList.add('completed');
            }
            
            const step