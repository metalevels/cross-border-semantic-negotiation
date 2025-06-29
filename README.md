# 🌍 Cross-Border Semantic Negotiation

AI-Powered Schema Alignment for EU Digital Identity Systems with Real-Time Step-by-Step Visualization

## 🚀 Latest Updates

### Enhanced Demo with Step-by-Step Visualization
We've added a comprehensive enhanced demo that provides **real-time visualization** of the semantic negotiation process, showing users exactly how AI models match mismatching schemas step-by-step.

## 🎯 Features

### 🔍 Real-Time Processing Visualization
- **Step 1: Schema Analysis** - Structural pattern analysis with field counting
- **Step 2: Claude AI Semantic Analysis** - Semantic relationship discovery with explanations
- **Step 3: Mistral AI Alignment Decisions** - Confidence refinement and mapping optimization
- **Step 4: Transformation Code Generation** - Executable Python code generation
- **Step 5: Compliance Validation** - GDPR/eIDAS regulatory compliance checking

### 🧠 AI-Powered Semantic Matching
- **Claude AI Integration**: Advanced semantic similarity analysis
- **Mistral AI Integration**: Intelligent alignment decision making
- **OntoAligner Compatibility**: Based on state-of-the-art ontology alignment research
- **Cross-linguistic Support**: Handles multiple EU languages and naming conventions

### 🔒 Compliance & Security
- **GDPR Compliance**: Data protection and privacy validation
- **eIDAS Compliance**: Cross-border digital identity standards
- **Sensitive Data Detection**: Automatic identification of sensitive fields
- **Encryption Recommendations**: Security best practices

## 🛠️ Quick Start

### Option 1: Enhanced Demo (Recommended)
```bash
# Clone the repository
git clone https://github.com/metalevels/cross-border-semantic-negotiation.git
cd cross-border-semantic-negotiation

# Run the setup script
chmod +x run.sh
./run.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-server.txt
python src/enhanced_demo.py
```

### Option 2: Production Server
```bash
# For production deployment
python src/server.py
```

### Option 3: Advanced Server
```bash
# For advanced features and detailed logging
python src/enhanced_server.py
```

## 🌐 Access the Demo

Once running, open your browser to:
- **http://localhost:8000** - Enhanced demo with step-by-step visualization
- **WebSocket Support** - Real-time updates during processing

## 📋 Supported EU Digital Identity Systems

| Country | System | Schema Fields |
|---------|--------|---------------|
| 🇮🇹 Italy | SPID | `nome`, `cognome`, `codice_fiscale`, `data_nascita`, `luogo_nascita` |
| 🇩🇪 Germany | eID | `firstName`, `lastName`, `taxId`, `birthDate`, `birthPlace` |
| 🇫🇷 France | FranceConnect | `givenName`, `familyName`, `fiscalNumber`, `dateOfBirth` |
| 🇪🇸 Spain | Cl@ve | `nombre`, `apellidos`, `nif`, `fechaNacimiento` |

## 🔧 Technical Architecture

### Backend Components
- **FastAPI Server**: High-performance async web framework
- **WebSocket Communication**: Real-time bidirectional communication
- **Mock AI Services**: Claude and Mistral AI simulation for demonstration
- **Semantic Analysis Engine**: Advanced field mapping algorithms
- **Compliance Validator**: GDPR/eIDAS compliance checking

### Frontend Features
- **Responsive Design**: Modern CSS Grid layout with gradients
- **Real-time Updates**: Live step-by-step processing visualization
- **Interactive Configuration**: Easy country and schema selection
- **Code Generation Display**: Shows actual executable transformation code
- **Confidence Scoring**: Visual confidence bars and percentage displays

## 📊 Example Output

### Field Mappings
```
nome (Italian) → firstName (German) - 89.2% confidence
codice_fiscale (Italian) → taxId (German) - 91.7% confidence
data_nascita (Italian) → birthDate (German) - 87.4% confidence
```

### Generated Transformation Code
```python
def transform_cross_border_data(source_data):
    """Auto-generated transformation function"""
    transformed_data = {}
    
    # High confidence mapping (89.2%)
    transformed_data['firstName'] = source_data.get('nome')
    
    # High confidence mapping (91.7%)
    transformed_data['taxId'] = source_data.get('codice_fiscale')
    
    return transformed_data
```

## 🔬 Research Foundation

This project builds upon:
- **OntoAligner**: State-of-the-art ontology alignment toolkit
- **RAG (Retrieval-Augmented Generation)**: Using Mistral-7B + BERT
- **Cross-border eIDAS Standards**: EU digital identity interoperability
- **GDPR Compliance**: European data protection regulations

## 📁 Project Structure

```
cross-border-semantic-negotiation/
├── src/
│   ├── enhanced_demo.py          # 🌟 Main enhanced demo with visualization
│   ├── server.py                 # Production-ready server
│   ├── enhanced_server.py        # Advanced server implementation
│   └── cross_border_implementation.py  # Core logic
├── demo/
│   └── cross_border_demo.html    # Original static demo
├── requirements-server.txt       # Server dependencies
├── run.sh                       # Quick setup script
└── README.md                    # This file
```

## 🚀 Development

### Adding New Countries
1. Add country schema to the semantic mappings in the AI services
2. Update the frontend country selection dropdown
3. Add country-specific compliance rules

### Extending AI Integration
- Replace mock services with real Claude/Mistral API calls
- Add additional AI models for specialized tasks
- Implement caching for improved performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OntoAligner Team**: For the foundational ontology alignment research
- **EU eIDAS Initiative**: For cross-border digital identity standards
- **FastAPI Community**: For the excellent web framework
- **Claude & Mistral AI**: For advanced language model capabilities

---

**🌟 Star this repository if you find it useful!**

For questions or support, please open an issue on GitHub.