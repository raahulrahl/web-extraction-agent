<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Web Content Extraction Agent</h1>
<h3 align="center">AI-Powered Web Scraping and Structured Data Extraction</h3>

<p align="center">
  <strong>Transforms unstructured web content into organized, structured data using Firecrawl and Exa search. Extracts comprehensive information from web pages and presents it in structured Pydantic models for easy processing and analysis.</strong><br/>
  Automate web research, content aggregation, competitive intelligence, and data extraction with AI-powered precision.
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/web-extraction-agent/actions/workflows/build-and-push.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/web-extraction-agent/build-and-push.yml?branch=main" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/Paraschamoli/web-extraction-agent">
    <img src="https://img.shields.io/github/license/Paraschamoli/web-extraction-agent" alt="License">
  </a>
  <a href="https://img.shields.io/badge/python-3.12-blue">
    <img src="https://img.shields.io/badge/python-3.12-blue" alt="Python 3.12">
  </a>
</p>

---

## 🎯 What is Web Extraction Agent?

An AI-powered agent that automatically fetches, parses, and extracts structured information from web pages. It combines Firecrawl's advanced web scraping with Exa's intelligent search to transform unstructured HTML content into organized, structured data using Pydantic models.

### Key Features
*   **🕸️ Advanced Web Scraping** - Optional Firecrawl integration for JavaScript-rendered content
*   **🌐 Intelligent Content Extraction** - Exa search for reliable web content retrieval
*   **🏗️ Structured Data Output** - Pydantic models for consistent, validated output
*   **🔍 Comprehensive Extraction** - Titles, descriptions, content sections, links, metadata
*   **🧠 Conversation Memory** - Mem0 integration for context-aware extraction
*   **⚡ Hybrid Approach** - Combines multiple extraction methods for reliability
*   **🎯 Targeted Extraction** - Specialized handling for e-commerce, articles, documentation

### Built-in Tools
*   **FirecrawlTools** - Advanced web scraping with JavaScript support
*   **ExaTools** - Intelligent web search and content extraction
*   **Mem0Tools** - Conversation memory for context-aware extraction
*   **Pydantic Models** - Structured output validation and serialization

### Extraction Process
1.  **URL Analysis** - Parse and validate target web pages
2.  **Content Retrieval** - Fetch content using Firecrawl (optional) and Exa
3.  **Intelligent Parsing** - Identify and extract relevant content sections
4.  **Structured Organization** - Organize into PageInformation schema
5.  **Validation & Output** - Validate against Pydantic models and return JSON

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. **It takes 2 minutes and unlocks the full potential of your agent.**

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/web-extraction-agent.git
cd web-extraction-agent

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# OPENROUTER_API_KEY=sk-...      # Required: For OpenRouter LLM
# EXA_API_KEY=sk-...             # Required: For Exa web content extraction
# FIRECRAWL_API_KEY=sk-...       # Optional: For Firecrawl advanced scraping
# MEM0_API_KEY=sk-...            # Optional: For conversation memory
# MODEL_NAME=openai/gpt-4o       # Optional: Model ID for OpenRouter
# ENABLE_FIRECRAWL=true          # Optional: Enable/disable Firecrawl
```

### 3. Run Locally

```bash
# Start the web extraction agent
python -m web_extraction_agent

# Or using uv
uv run python -m web_extraction_agent
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3773
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```env
# Required APIs
OPENROUTER_API_KEY=sk-...           # Required for LLM calls
EXA_API_KEY=sk-...                  # Required for web content extraction

# Optional features
FIRECRAWL_API_KEY=sk-...            # Optional: Advanced web scraping
MEM0_API_KEY=sk-...                 # Optional: Conversation memory
MODEL_NAME=openai/gpt-4o            # Model ID for OpenRouter
ENABLE_FIRECRAWL=true               # Enable/disable Firecrawl
```

### Port Configuration
Default port: `3773` (can be changed in `agent_config.json`)

---

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Extract all information from https://www.example.com"
      }
    ]
  }'
```

### Sample Web Extraction Queries
*   "Extract all information from https://www.example.com"
*   "Scrape product details from https://store.example.com/product"
*   "Extract article content from https://news.example.com/article"
*   "Get company information from https://www.company.com/about"
*   "Analyze webpage structure from https://docs.example.com"
*   "Extract contact information from https://business.example.com/contact"
*   "Scrape pricing table from https://pricing.example.com"
*   "Extract metadata from https://blog.example.com/post"
*   "Get all links from https://resources.example.com"
*   "Analyze e-commerce product page from https://shop.example.com/item"

### Expected Response Format

```json
{
  "url": "https://www.example.com",
  "title": "Example Website",
  "description": "Example website description...",
  "features": ["Feature 1", "Feature 2"],
  "content_sections": [
    {
      "heading": "Welcome Section",
      "content": "Welcome to our website..."
    },
    {
      "heading": "About Us",
      "content": "Our company was founded in..."
    }
  ],
  "links": {
    "About Us": "https://www.example.com/about",
    "Contact": "https://www.example.com/contact",
    "Services": "https://www.example.com/services"
  },
  "contact_info": {
    "email": "info@example.com",
    "phone": "+1-234-567-8900",
    "address": "123 Example Street, City, Country"
  },
  "metadata": {
    "language": "en",
    "charset": "UTF-8",
    "viewport": "width=device-width, initial-scale=1.0"
  }
}
```

---

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t web-extraction-agent .

# Run container
docker run -d \
  -p 3773:3773 \
  -e OPENROUTER_API_KEY=your_openrouter_key \
  -e EXA_API_KEY=your_exa_key \
  -e FIRECRAWL_API_KEY=your_firecrawl_key \
  -e MEM0_API_KEY=your_mem0_key \
  -e MODEL_NAME=openai/gpt-4o \
  -e ENABLE_FIRECRAWL=true \
  --name web-extraction-agent \
  web-extraction-agent

# Check logs
docker logs -f web-extraction-agent
```

### Docker Compose (Recommended)

`docker-compose.yml`:

```yaml
version: '3.8'
services:
  web-extraction-agent:
    build: .
    ports:
      - "3773:3773"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - EXA_API_KEY=${EXA_API_KEY}
      - FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}
      - MEM0_API_KEY=${MEM0_API_KEY}
      - MODEL_NAME=${MODEL_NAME:-openai/gpt-4o}
      - ENABLE_FIRECRAWL=${ENABLE_FIRECRAWL:-true}
    restart: unless-stopped
```

### Run with Compose

```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
web-extraction-agent/
├── web_extraction_agent/
│   ├── skills/
│   │   └── web-extraction/
│   │       ├── skill.yaml          # Skill configuration
│   │       └── __init__.py
│   ├── __init__.py
│   ├── main.py                     # Agent entry point
│   └── agent_config.json           # Agent configuration
├── agent_config.json               # Bindu agent configuration
├── pyproject.toml                  # Python dependencies
├── Dockerfile                      # Multi-stage Docker build
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This documentation
├── .env.example                    # Environment template
└── tests/                          # Test suite
```

---

## 🔌 API Reference

### Health Check

```bash
GET http://localhost:3773/health
```

**Response:**
```json
{"status": "healthy", "agent": "Web Extraction Agent"}
```

### Chat Endpoint

```bash
POST http://localhost:3773/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your web extraction query here"}
  ]
}
```

---

## 🧪 Testing

### Local Testing

```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with coverage
pytest --cov=web_extraction_agent tests/
```

### Integration Test

```bash
# Start agent
python -m web_extraction_agent &

# Test API endpoint
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Extract info from https://www.example.com"}]}'
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
| :--- | :--- |
| "EXA_API_KEY required" | Get your key from exa.ai - Required for web content extraction |
| "OPENROUTER_API_KEY required" | Get your key from openrouter.ai |
| "Firecrawl not working" | Set `ENABLE_FIRECRAWL=false` or get a key from getfirecrawl.com |
| "Port 3773 already in use" | Change port in `agent_config.json` or kill the process: `lsof -ti:3773 | xargs kill -9` |
| "JSON parsing error" | Ensure agent output matches PageInformation schema |
| "Website blocking requests" | Enable Firecrawl for JavaScript rendering and proxy support |

---

## 📊 Dependencies

### Core Packages
*   **bindu** - Agent deployment framework
*   **agno** - AI agent framework
*   **firecrawl-py** - Advanced web scraping
*   **exa-py** - Web search and content extraction
*   **pydantic** - Structured data validation
*   **python-dotenv** - Environment management
*   **mem0ai** - Memory operations

### Development Packages
*   **pytest** - Testing framework
*   **ruff** - Code formatting/linting
*   **pre-commit** - Git hooks

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository.
2.  Create a feature branch: `git checkout -b feature/improvement`.
3.  Make your changes following the code style.
4.  Add tests for new functionality.
5.  Commit with descriptive messages.
6.  Push to your fork.
7.  Open a Pull Request.

### Code Style
*   Follow PEP 8 conventions.
*   Use type hints where possible.
*   Add docstrings for public functions.
*   Keep functions focused and small.

---

## 📄 License
MIT License - see LICENSE file for details.

---

## 🙏 Credits & Acknowledgments
*   **Developer:** Paras Chamoli
*   **Framework:** Bindu - Agent deployment platform
*   **Agent Framework:** Agno - AI agent toolkit
*   **Web Scraping:** Firecrawl - Advanced scraping API
*   **Search Engine:** Exa - Web search and extraction
*   **Memory System:** Mem0 - Conversation memory API
*   **Validation:** Pydantic - Data validation library

---

## 🔗 Useful Links
*   🌐 [Bindu Directory](https://bindus.directory)
*   📚 [Bindu Docs](https://docs.getbindu.com)
*   🐙 [GitHub](https://github.com/ParasChamoli/web-extraction-agent)
*   🕸️ [Firecrawl](https://getfirecrawl.com)
*   🌐 [Exa Search](https://exa.ai)
*   💬 [Bindu Community](https://discord.gg/bindu)

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Transforming unstructured web content into actionable structured data</em>
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/web-extraction-agent/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/ParasChamoli/web-extraction-agent/issues">🐛 Report Issues</a>
</p>

<p align="center">
  <em>Note: This agent extracts publicly available web content for legitimate purposes. Always respect website terms of service, robots.txt files, and rate limits. Use responsibly and in compliance with applicable laws and regulations.</em>
</p>
