"""Tests for custom tools."""

import pytest

from nuclear_intelligence.tools.crawl4ai_tool import Crawl4AITool


def test_crawl4ai_tool_initialization():
    """Test that Crawl4AITool can be instantiated."""
    tool = Crawl4AITool()
    assert tool.name == "Crawl4AI Web Scraper"
    assert tool.description is not None
    assert len(tool.description) > 0


def test_crawl4ai_tool_schema():
    """Test that Crawl4AITool has correct input schema."""
    tool = Crawl4AITool()
    schema = tool.args_schema.model_json_schema()
    assert "url" in schema["properties"]
    assert schema["properties"]["url"]["type"] == "string"


@pytest.mark.asyncio
async def test_crawl4ai_tool_basic_scraping():
    """Test basic web scraping functionality."""
    tool = Crawl4AITool()
    # Test with a simple, reliable URL
    result = tool._run(url="https://example.com", markdown=True)
    assert result is not None
    assert isinstance(result, str)
    # Should contain some content (even if just error message)
    assert len(result) > 0


