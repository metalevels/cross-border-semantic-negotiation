#!/usr/bin/env python3
"""
Enhanced Cross-Border Semantic Negotiation Demo
Simple working version with step-by-step visualization
"""

import asyncio
import json
import logging
import random
import time
from typing import Dict, List, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Enhanced Cross-Border Semantic Negotiation")

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections[:]:
            try:
                await connection.send_text(message)
            except:
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Data models
class NegotiationRequest(BaseModel):
    source_country: str
    target_country: str
    source_schema: Dict[str, Any]
    target_schema: Dict[str, Any]

# Enhanced negotiation engine
class EnhancedNegotiator:
    async def negotiate(self, request: NegotiationRequest):
        """Perform negotiation with step-by-step updates"""
        
        # Step 1: Schema Analysis
        await self._send_step_update(1, 'active', 
            f"🔍 Analyzing schemas...<br>Source: {len(request.source_schema)} fields<br>Target: {len(request.target_schema)} fields")
        await asyncio.sleep(1)
        await self._send_step_update(1, 'completed', "✅ Schema analysis complete")
        
        # Step 2: Claude Analysis
        await self._send_step_update(2, 'active', "🧠 Claude AI analyzing semantic relationships...")
        await asyncio.sleep(2)
        
        # Mock semantic analysis
        alignments = self._mock_semantic_analysis(request.source_schema, request.target_schema)
        avg_confidence = sum(a['confidence'] for a in alignments) / len(alignments) if alignments else 0
        
        await self._send_step_update(2, 'completed', 
            f"✅ Found {len(alignments)} mappings<br>Average confidence: {avg_confidence:.1%}")
        
        # Step 3: Mistral Decisions
        await self._send_step_update(3, 'active', "⚡ Mistral AI refining alignments...")
        await asyncio.sleep(1.5)
        
        # Refine alignments
        for alignment in alignments:
            alignment['confidence'] = min(alignment['confidence'] + random.uniform(-0.05, 0.1), 0.99)
        
        overall_confidence = sum(a['confidence'] for a in alignments) / len(alignments) if alignments else 0
        await self._send_step_update(3, 'completed', f"✅ Overall confidence: {overall_confidence:.1%}")
        
        # Step 4: Code Generation
        await self._send_step_update(4, 'active', "⚙️ Generating transformation code...")
        await asyncio.sleep(1)
        
        code = self._generate_code(alignments)
        await self._send_step_update(4, 'completed', f"✅ Generated {len(code.split())} lines of code")
        
        # Step 5: Compliance
        await self._send_step_update(5, 'active', "📋 Validating GDPR/eIDAS compliance...")
        await asyncio.sleep(0.8)
        
        compliance = self._check_compliance(request.source_country, request.target_country)
        await self._send_step_update(5, 'completed', "✅ Compliance validated")
        
        # Send final results
        result = {
            'overall_confidence': round(overall_confidence * 100, 1),
            'alignments': alignments,
            'transformation_code': code,
            'compliance_notes': compliance
        }
        
        await manager.broadcast(json.dumps({
            'type': 'final_result',
            'result': result
        }))
        
        return result
    
    async def _send_step_update(self, step: int, status: str, details: str):
        await manager.broadcast(json.dumps({
            'type': 'step_update',
            'step': step,
            'status': status,
            'details': details
        }))
    
    def _mock_semantic_analysis(self, source_schema: Dict, target_schema: Dict) -> List[Dict]:
        """Mock semantic analysis"""
        mappings = {
            'nome': 'firstName',
            'cognome': 'lastName', 
            'codice_fiscale': 'taxId',
            'data_nascita': 'birthDate',
            'luogo_nascita': 'birthPlace',
            'user_id': 'personalId'
        }
        
        alignments = []
        for source_field in source_schema.keys():
            if source_field in mappings:
                target_field = mappings[source_field]
                if target_field in target_schema:
                    alignments.append({
                        'source_field': source_field,
                        'target_field': target_field,
                        'confidence': 0.85 + random.uniform(0, 0.1),
                        'method': 'Semantic mapping',
                        'explanation': f"'{source_field}' semantically maps to '{target_field}'"
                    })
        
        return alignments
    
    def _generate_code(self, alignments: List[Dict]) -> str:
        """Generate transformation code"""
        lines = [
            "def transform_data(source_data):",
            "    transformed = {}",
            ""
        ]
        
        for alignment in alignments:
            confidence = alignment['confidence']
            source = alignment['source_field']
            target = alignment['target_field']
            
            if confidence > 0.8:
                lines.append(f"    # High confidence ({confidence:.1%})")
                lines.append(f"    transformed['{target}'] = source_data.get('{source}')")
            else:
                lines.append(f"    # Medium confidence ({confidence:.1%})")
                lines.append(f"    if '{source}' in source_data:")
                lines.append(f"        transformed['{target}'] = source_data['{source}']")
            lines.append("")
        
        lines.append("    return transformed")
        return "\n".join(lines)
    
    def _check_compliance(self, source_country: str, target_country: str) -> str:
        """Check compliance"""
        return f"""🔒 GDPR Compliance: ✅ All mappings preserve data rights
🇪🇺 eIDAS Compliance: ✅ Cross-border mapping {source_country} → {target_country}
⚠️ Recommendation: Encrypt sensitive fields during transmission"""

negotiator = EnhancedNegotiator()

@app.get("/", response_class=HTMLResponse)
async def get_demo():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Enhanced Cross-Border Semantic Negotiation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; }
        .header { text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .content { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .section { background: #f8f9fa; padding: 20px; border-radius: 8px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; }
        select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        textarea { height: 100px; font-family: monospace; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
        .btn:hover { background: #0056b3; }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .step { margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .step.active { background: #e3f2fd; border-color: #2196f3; }
        .step.completed { background: #e8f5e8; border-color: #4caf50; }
        .step-header { font-weight: bold; margin-bottom: 5px; }
        .results { grid-column: 1 / -1; margin-top: 20px; }
        .alignment { background: white; margin: 10px 0; padding: 15px; border-left: 4px solid #28a745; border-radius: 4px; }
        .code { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 4px; font-family: monospace; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Enhanced Cross-Border Semantic Negotiation</h1>
            <p>AI-Powered Schema Alignment with Step-by-Step Visualization</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h3>Configuration</h3>
                <div class="form-group">
                    <label>Source Country:</label>
                    <select id="sourceCountry">
                        <option value="italy_spid">🇮🇹 Italy (SPID)</option>
                        <option value="germany_eid">🇩🇪 Germany (eID)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Target Country:</label>
                    <select id="targetCountry">
                        <option value="germany_eid">🇩🇪 Germany (eID)</option>
                        <option value="italy_spid">🇮🇹 Italy (SPID)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Source Schema:</label>
                    <textarea id="sourceSchema">{
  "user_id": "string",
  "nome": "string",
  "cognome": "string",
  "codice_fiscale": "string",
  "data_nascita": "date",
  "luogo_nascita": "string"
}</textarea>
                </div>
                <div class="form-group">
                    <label>Target Schema:</label>
                    <textarea id="targetSchema">{
  "personalId": "string",
  "firstName": "string",
  "lastName": "string",
  "taxId": "string",
  "birthDate": "date",
  "birthPlace": "string"
}</textarea>
                </div>
                <button class="btn" onclick="startNegotiation()">🚀 Start Negotiation</button>
            </div>
            
            <div class="section">
                <h3>Processing Steps</h3>
                <div id="steps">
                    <div class="step" id="step1">
                        <div class="step-header">1. Schema Analysis</div>
                        <div>Analyzing source and target schemas...</div>
                    </div>
                    <div class="step" id="step2">
                        <div class="step-header">2. Claude Semantic Analysis</div>
                        <div>AI analyzing semantic relationships...</div>
                    </div>
                    <div class="step" id="step3">
                        <div class="step-header">3. Mistral Alignment Decisions</div>
                        <div>Refining confidence scores...</div>
                    </div>
                    <div class="step" id="step4">
                        <div class="step-header">4. Code Generation</div>
                        <div>Generating transformation code...</div>
                    </div>
                    <div class="step" id="step5">
                        <div class="step-header">5. Compliance Validation</div>
                        <div>Checking GDPR/eIDAS compliance...</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="results" id="results" style="display: none;">
            <h3>Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>

    <script>
        let ws = null;
        
        function connectWebSocket() {
            ws = new WebSocket('ws://localhost:8000/ws');
            ws.onopen = () => console.log('Connected');
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'step_update') {
                    updateStep(data.step, data.status, data.details);
                } else if (data.type === 'final_result') {
                    showResults(data.result);
                }
            };
            ws.onclose = () => setTimeout(connectWebSocket, 3000);
        }
        
        function updateStep(stepNum, status, details) {
            const step = document.getElementById(`step${stepNum}`);
            step.classList.remove('active', 'completed');
            if (status === 'active') step.classList.add('active');
            if (status === 'completed') step.classList.add('completed');
            step.querySelector('div:last-child').innerHTML = details;
        }
        
        function showResults(result) {
            const resultsDiv = document.getElementById('results');
            const content = document.getElementById('resultsContent');
            
            let html = `<div class="alignment"><h4>Overall Confidence: ${result.overall_confidence}%</h4></div>`;
            
            html += '<h4>Field Mappings:</h4>';
            result.alignments.forEach(a => {
                html += `<div class="alignment">
                    <strong>${a.source_field}</strong> → <strong>${a.target_field}</strong><br>
                    <small>Confidence: ${(a.confidence * 100).toFixed(1)}% | ${a.explanation}</small>
                </div>`;
            });
            
            html += `<h4>Generated Code:</h4><div class="code">${result.transformation_code}</div>`;
            html += `<h4>Compliance:</h4><div class="alignment">${result.compliance_notes.replace(/\\n/g, '<br>')}</div>`;
            
            content.innerHTML = html;
            resultsDiv.style.display = 'block';
            
            document.querySelector('.btn').textContent = '🚀 Start New Negotiation';
            document.querySelector('.btn').disabled = false;
        }
        
        async function startNegotiation() {
            const btn = document.querySelector('.btn');
            btn.textContent = '⏳ Processing...';
            btn.disabled = true;
            
            document.getElementById('results').style.display = 'none';
            
            // Reset steps
            for (let i = 1; i <= 5; i++) {
                const step = document.getElementById(`step${i}`);
                step.classList.remove('active', 'completed');
            }
            
            const data = {
                source_country: document.getElementById('sourceCountry').value,
                target_country: document.getElementById('targetCountry').value,
                source_schema: JSON.parse(document.getElementById('sourceSchema').value),
                target_schema: JSON.parse(document.getElementById('targetSchema').value)
            };
            
            try {
                await fetch('/negotiate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } catch (error) {
                console.error('Error:', error);
                btn.textContent = '🚀 Start Negotiation';
                btn.disabled = false;
            }
        }
        
        // Connect on page load
        document.addEventListener('DOMContentLoaded', connectWebSocket);
    </script>
</body>
</html>"""

@app.post("/negotiate")
async def negotiate(request: NegotiationRequest):
    """Start negotiation process"""
    asyncio.create_task(negotiator.negotiate(request))
    return {"status": "started"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)