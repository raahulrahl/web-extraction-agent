# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""web-extraction-agent - A Bindu Agent for web content extraction and structuring."""

import argparse
import asyncio
import json
import os
from pathlib import Path
from textwrap import dedent
from typing import Any, Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.exa import ExaTools
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.mem0 import Mem0Tools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich.pretty import pprint

# Load environment variables from .env file
load_dotenv()

# Global instances
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


class APIKeyError(ValueError):
    """API key is missing."""


class ContentSection(BaseModel):
    """Represents a section of content from the webpage."""

    heading: Optional[str] = Field(None, description="Section heading")
    content: str = Field(..., description="Section content text")


class PageInformation(BaseModel):
    """Structured representation of a webpage."""

    url: str = Field(..., description="URL of the page")
    title: str = Field(..., description="Title of the page")
    description: Optional[str] = Field(
        None, description="Meta description or summary of the page"
    )
    features: Optional[list[str]] = Field(None, description="Key feature list")
    content_sections: Optional[list[ContentSection]] = Field(
        None, description="Main content sections of the page"
    )
    links: Optional[dict[str, str]] = Field(
        None, description="Important links found on the page with description"
    )
    contact_info: Optional[dict[str, str]] = Field(
        None, description="Contact information if available"
    )
    metadata: Optional[dict[str, str]] = Field(
        None, description="Important metadata from the page"
    )


def load_config() -> dict:
    """Load agent configuration from project root."""
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error reading {config_path}: {e}")
                continue

    # Default configuration
    return {
        "name": "web-extraction-agent",
        "description": "AI agent that transforms unstructured web content into organized, structured data using Firecrawl and Exa search",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {
                "key": "OPENROUTER_API_KEY",
                "description": "OpenRouter API key for LLM calls (required)",
                "required": True,
            },
            {
                "key": "MODEL_NAME",
                "description": "Model ID for OpenRouter (default: openai/gpt-4o)",
                "required": False,
            },
            {
                "key": "MEM0_API_KEY",
                "description": "Mem0 API key for conversation memory",
                "required": False,
            },
            {
                "key": "EXA_API_KEY",
                "description": "Exa API key for web search and content extraction (required)",
                "required": True,
            },
            {
                "key": "FIRECRAWL_API_KEY",
                "description": "Firecrawl API key for advanced web scraping (optional)",
                "required": False,
            },
            {
                "key": "ENABLE_FIRECRAWL",
                "description": "Enable Firecrawl web scraping (default: true)",
                "required": False,
            },
        ],
    }


def _get_api_keys() -> tuple[str | None, str | None, str | None, str | None, str]:
    """Get API keys and configuration from environment."""
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    mem0_api_key = os.getenv("MEM0_API_KEY")
    exa_api_key = os.getenv("EXA_API_KEY")
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")
    return openrouter_api_key, mem0_api_key, exa_api_key, firecrawl_api_key, model_name


def _create_llm_model(openrouter_api_key: str, model_name: str) -> OpenRouter:
    """Create and return the OpenRouter model."""
    if not openrouter_api_key:
        error_msg = (
            "OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.\n"
            "Get an API key from: https://openrouter.ai/keys"
        )
        raise APIKeyError(error_msg)

    return OpenRouter(
        id=model_name,
        api_key=openrouter_api_key,
        cache_response=True,
        supports_native_structured_outputs=True,
    )


def _setup_tools(
    mem0_api_key: str | None,
    exa_api_key: str,
    firecrawl_api_key: str | None,
) -> list:
    """Set up all tools for the web extraction agent."""
    tools = []

    # ExaTools is required for web content extraction
    if not exa_api_key:
        error_msg = (
            "Exa API key is required. Set EXA_API_KEY environment variable.\n"
            "Get an API key from: https://exa.ai"
        )
        raise APIKeyError(error_msg)

    try:
        exa_tools = ExaTools(api_key=exa_api_key)
        tools.append(exa_tools)
        print("🌐 Exa search enabled for web content extraction")
    except Exception as e:
        print(f"❌ Failed to initialize ExaTools: {e}")
        raise

    # Firecrawl is optional for advanced web scraping
    enable_firecrawl = os.getenv("ENABLE_FIRECRAWL", "true").lower() in ("true", "1", "yes")
    if enable_firecrawl and firecrawl_api_key:
        try:
            firecrawl_tools = FirecrawlTools(
                api_key=firecrawl_api_key,
                enable_scrape=True,
                enable_crawl=True,
            )
            tools.append(firecrawl_tools)
            print("🕸️ Firecrawl enabled for advanced web scraping")
        except Exception as e:
            print(f"⚠️  Firecrawl initialization issue: {e}")
            print("⚠️  Continuing without Firecrawl (Exa will be used for extraction)")
    else:
        print("ℹ️  Firecrawl disabled or no API key provided")

    # Mem0 is optional for conversation memory
    if mem0_api_key:
        try:
            mem0_tools = Mem0Tools(api_key=mem0_api_key)
            tools.append(mem0_tools)
            print("🧠 Mem0 memory system enabled for conversation context")
        except Exception as e:
            print(f"⚠️  Mem0 initialization issue: {e}")

    return tools


async def initialize_agent() -> None:
    """Initialize the web extraction agent."""
    global agent

    openrouter_api_key, mem0_api_key, exa_api_key, firecrawl_api_key, model_name = _get_api_keys()

    # Validate required API keys
    if not openrouter_api_key:
        error_msg = (
            "OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.\n"
            "Get an API key from: https://openrouter.ai/keys"
        )
        raise APIKeyError(error_msg)

    if not exa_api_key:
        error_msg = (
            "Exa API key is required for web content extraction. Set EXA_API_KEY environment variable.\n"
            "Get an API key from: https://exa.ai"
        )
        raise APIKeyError(error_msg)

    model = _create_llm_model(openrouter_api_key, model_name)
    tools = _setup_tools(mem0_api_key, exa_api_key, firecrawl_api_key)

    # Create the web extraction agent
    agent = Agent(
        name="Web Extraction Assistant",
        model=model,
        tools=tools,
        description=dedent("""\
            You are a professional web researcher and content extractor with expertise in
            transforming unstructured web content into organized, structured data.
            
            You combine web scraping capabilities with intelligent analysis to extract
            comprehensive information from web pages and present it in a structured format.
            
            IMPORTANT: You must output your responses in a structured JSON format that matches
            the PageInformation schema. Your output should be valid JSON that can be parsed
            into the PageInformation model.
        """),
        instructions=dedent("""\
            WEB EXTRACTION PROCESS:

            1. CONTENT RETRIEVAL 🔍
               - Use available tools to fetch and analyze web content
               - Prioritize Firecrawl for advanced scraping when available
               - Use Exa search for reliable content extraction
               - Handle JavaScript-rendered content appropriately

            2. CONTENT ANALYSIS 📋
               - Accurately capture page title, description, and key features
               - Identify and extract main content sections with their headings
               - Find important links to related pages or resources
               - Locate contact information if available
               - Extract relevant metadata that provides context about the site

            3. STRUCTURED EXTRACTION 🏗️
               - Organize content into the PageInformation schema
               - Create ContentSection objects for logical content grouping
               - Categorize links by type and relevance
               - Normalize contact information formats
               - Include comprehensive metadata

            4. QUALITY ASSURANCE ✅
               - Be thorough but concise in extraction
               - Prioritize the most important information for extensive pages
               - Verify extracted information matches source content
               - Handle missing or optional fields gracefully
               - Maintain consistent output format

            5. OUTPUT FORMAT REQUIREMENTS ✨
               - Output MUST be valid JSON that matches PageInformation schema
               - Use this exact structure:
                 {
                   "url": "string",
                   "title": "string",
                   "description": "string or null",
                   "features": ["string1", "string2"] or null,
                   "content_sections": [
                     {
                       "heading": "string or null",
                       "content": "string"
                     }
                   ] or null,
                   "links": {"link_name": "url"} or null,
                   "contact_info": {"type": "value"} or null,
                   "metadata": {"key": "value"} or null
                 }
               - Do not include any markdown formatting or additional text
               - Output only the JSON object

            SPECIAL CONSIDERATIONS:
            - For e-commerce sites: Extract product details, prices, specifications
            - For news/articles: Extract author, date, main points, citations
            - For company sites: Extract services, team, contact information
            - For documentation: Extract code examples, API endpoints, tutorials
        """),
        structured_outputs=True,
        add_datetime_to_context=True,
        markdown=False,  # Disable markdown to ensure clean JSON output
    )

    print(f"✅ Web Extraction agent initialized using {model_name}")
    print("🌐 Exa search enabled for web content extraction")
    if firecrawl_api_key and os.getenv("ENABLE_FIRECRAWL", "true").lower() in ("true", "1", "yes"):
        print("🕸️ Firecrawl enabled for advanced web scraping")
    if mem0_api_key:
        print("🧠 Memory system enabled for conversation context")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent

    if not agent:
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    return await agent.arun(messages)


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Web Extraction Agent...")
            await initialize_agent()
            _initialized = True

    return await run_agent(messages)


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Web Extraction Agent resources...")


def _setup_environment_variables(args: argparse.Namespace) -> None:
    """Set environment variables from command line arguments."""
    if args.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_api_key
    if args.mem0_api_key:
        os.environ["MEM0_API_KEY"] = args.mem0_api_key
    if args.exa_api_key:
        os.environ["EXA_API_KEY"] = args.exa_api_key
    if args.firecrawl_api_key:
        os.environ["FIRECRAWL_API_KEY"] = args.firecrawl_api_key
    if args.model:
        os.environ["MODEL_NAME"] = args.model
    if args.enable_firecrawl is not None:
        os.environ["ENABLE_FIRECRAWL"] = str(args.enable_firecrawl)


def _display_configuration_info() -> None:
    """Display configuration information to the user."""
    print("=" * 60)
    print("🕸️ WEB EXTRACTION AGENT")
    print("=" * 60)
    print("📄 Purpose: Transform web content into structured data")
    print("🔧 Powered by: Firecrawl scraping + Exa search + Pydantic structuring")

    config_info = []
    if os.getenv("OPENROUTER_API_KEY"):
        model = os.getenv("MODEL_NAME", "openai/gpt-4o")
        config_info.append(f"🤖 Model: {model}")
    if os.getenv("EXA_API_KEY"):
        config_info.append("🌐 Exa: Web content extraction")
    if os.getenv("FIRECRAWL_API_KEY") and os.getenv("ENABLE_FIRECRAWL", "true").lower() in ("true", "1", "yes"):
        config_info.append("🕸️ Firecrawl: Advanced scraping")
    if os.getenv("MEM0_API_KEY"):
        config_info.append("🧠 Memory: Conversation context")

    for info in config_info:
        print(info)

    print("=" * 60)
    print("Example queries:")
    print("• 'Extract all information from https://www.example.com'")
    print("• 'Scrape product details from https://store.example.com/product'")
    print("• 'Extract article content from https://news.example.com/article'")
    print("• 'Get company information from https://www.company.com/about'")
    print("=" * 60)


def main() -> None:
    """Run the main entry point for the Web Extraction Agent."""
    parser = argparse.ArgumentParser(
        description="Web Extraction Agent - Transform web content into structured data"
    )
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--mem0-api-key",
        type=str,
        default=os.getenv("MEM0_API_KEY"),
        help="Mem0 API key for conversation memory (optional)",
    )
    parser.add_argument(
        "--exa-api-key",
        type=str,
        default=os.getenv("EXA_API_KEY"),
        help="Exa API key for web content extraction (required)",
    )
    parser.add_argument(
        "--firecrawl-api-key",
        type=str,
        default=os.getenv("FIRECRAWL_API_KEY"),
        help="Firecrawl API key for advanced scraping (optional)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-4o"),
        help="Model ID for OpenRouter (env: MODEL_NAME)",
    )
    parser.add_argument(
        "--enable-firecrawl",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=os.getenv("ENABLE_FIRECRAWL", "true"),
        help="Enable Firecrawl web scraping (default: true)",
    )

    args = parser.parse_args()

    _setup_environment_variables(args)
    _display_configuration_info()

    config = load_config()

    try:
        print("\n🚀 Starting Web Extraction Agent server...")
        print(f"🌐 Access at: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Web Extraction Agent stopped")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
        import traceback

        traceback.print_exc()
        import sys

        sys.exit(1)
    finally:
        asyncio.run(cleanup())


if __name__ == "__main__":
    main()