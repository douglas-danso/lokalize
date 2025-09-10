# 🌍 Lokalize - AI Fashion Localization with Cultural Context

> **Hackathon Project**: AI-powered fashion marketing localization that goes beyond translation to provide deep cultural context and sensitivity.

## 🚀 Quick Start (2-minute setup)

### Option 1: Docker (Recommended for Hackathon)
```bash
# Clone and run
git clone <your-repo>
cd lokalize
docker build -t lokalize .
docker run lokalize
```

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run demo
python quickstart.py
```

## 🎯 What This Does

**Problem**: Fashion brands lose millions due to cultural missteps in international marketing.

**Solution**: AI system that provides culturally-aware fashion marketing advice using:
- 🌐 **Web scraping** of cultural fashion content (LangChain WebLoader)
- 🧠 **Knowledge base** powered by AWS Bedrock
- 🎨 **Cultural localization** advice beyond simple translation

## 🏗️ Architecture

```
Web Sources → LangChain WebLoader → Document Chunks → AWS Bedrock KB → RAG Query Engine
     ↓
Cultural Fashion Content (Saudi Arabia focus)
     ↓
AI-Generated Localization Advice
```

## 📊 Demo Capabilities

### 1. Web Scraping
- Scrapes Saudi Arabian fashion cultural content
- Uses LangChain WebBaseLoader + BeautifulSoup
- Automatically chunks content for optimal RAG performance

### 2. Knowledge Base
- AWS Bedrock Knowledge Base integration
- Stores and indexes cultural fashion insights
- Hybrid search (semantic + keyword)

### 3. Cultural Queries
- "How should luxury handbag brands adapt marketing for Saudi Arabia?"
- "What colors should be avoided in conservative markets?"
- "How to market modest fashion collections effectively?"

## 🛠️ Technical Stack

- **LangChain**: Document loading and text splitting
- **AWS Bedrock**: Knowledge Base + Claude 3 Sonnet
- **Python 3.11**: Core implementation
- **Docker**: Containerized deployment
- **boto3**: AWS SDK integration

## 📋 Files Structure

```
lokalize/
├── src/lokalize/
│   ├── rag/
│   │   ├── web_scraper.py      # LangChain web scraping
│   │   ├── query_engine.py     # AWS Bedrock integration
│   │   └── __init__.py         # RAG orchestrator
│   └── cultural/
│       └── models.py           # Cultural data models
├── quickstart.py               # Demo script
├── Dockerfile                  # Container setup
├── pyproject.toml             # Dependencies
└── README.md                  # This file
```

## 🚀 Hackathon Demo Script

```python
# Run the complete demo
python quickstart.py

# What you'll see:
# 1. Web scraping of Saudi fashion cultural content
# 2. Knowledge base document preparation
# 3. Sample localization queries with AI responses
```

## 🔧 AWS Setup (For Production)

### 0. Install Dependencies
```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

### 1. Create Bedrock Knowledge Base
```bash
# Using AWS CLI
aws bedrock-agent create-knowledge-base \
    --name "fashion-cultural-kb" \
    --description "Fashion cultural localization knowledge base"
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your AWS credentials and Knowledge Base ID
```

### 3. Upload Documents
```python
from src.lokalize.rag import setup_demo_knowledge_base

# Get scraped documents
docs = setup_demo_knowledge_base()

# Upload to Bedrock Knowledge Base (manual step for hackathon)
```

## 📈 Sample Outputs

### Query: "Luxury handbag marketing for Saudi Arabia"

**AI Response:**
```
🇸🇦 Cultural Localization Advice:

1. CULTURAL CONSIDERATIONS:
   - Emphasize modesty and elegance over flashy displays
   - Use family-oriented messaging (gifts for daughters, wives)
   - Highlight quality and craftsmanship

2. VISUAL GUIDELINES:
   - Modest styling in photography
   - Include local cultural elements
   - Appropriate contexts (family settings)

3. MESSAGING STRATEGY:
   - "Timeless elegance" vs "bold statements"
   - Emphasize heritage alongside luxury
   - Respectful Arabic language elements
```

## 🎨 Cultural Regions Supported

- 🇸🇦 **Saudi Arabia** (Primary focus)
- 🌍 **Expandable** to other MENA regions
- 🔄 **Scalable** architecture for global markets

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Test individual components
python src/lokalize/rag/web_scraper.py
python src/lokalize/rag/query_engine.py
```

## 🚧 Hackathon Limitations & Next Steps

### Current (Hackathon Scope)
- ✅ Web scraping pipeline
- ✅ AWS Bedrock integration
- ✅ Saudi Arabia cultural content
- ✅ Mock localization responses

### Production Roadmap
- 🔄 Real-time Knowledge Base updates
- 🌍 Multi-region cultural databases
- 🎨 Visual content analysis
- 📊 Marketing campaign effectiveness tracking
- 🔌 API for brand integration

## 🏆 Hackathon Pitch

**"Lokalize prevents the next $billions in cultural marketing disasters by providing AI-powered fashion localization that understands not just language, but cultural values, religious sensitivities, and local preferences."**

### Business Impact
- 💰 Prevent costly cultural missteps
- 🎯 Increase campaign effectiveness 
- 🌍 Accelerate global market entry
- 🤝 Build authentic cultural connections

## 📞 Team

Built for AWS + AI Hackathon 2024
- Focus: Cultural AI for fashion marketing
- Tech: LangChain + AWS Bedrock RAG
- Goal: Prevent cultural marketing failures

---

*Ready to demo in 2 minutes with `python quickstart.py`!* 🚀
