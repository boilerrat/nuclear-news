"""Crawl4AI tool for web scraping and content extraction.

This tool provides enhanced web scraping capabilities using Crawl4AI,
which generates clean markdown output optimized for RAG pipelines.
"""

import logging
from typing import Optional

from crawl4ai import AsyncWebCrawler
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Crawl4AIInput(BaseModel):
    """Input schema for Crawl4AI tool."""

    url: str = Field(
        ...,
        description="The URL of the webpage to scrape and extract content from",
    )
    markdown: bool = Field(
        default=True,
        description="Whether to return content as markdown (default: True)",
    )
    remove_links: bool = Field(
        default=False,
        description="Whether to remove links from the extracted content",
    )


class Crawl4AITool(BaseTool):
    """Tool for scraping web content using Crawl4AI.

    Crawl4AI provides advanced web scraping capabilities with clean markdown
    output, making it ideal for extracting content from technical publications,
    regulatory documents, and industry websites for analysis.

    Attributes:
        name: Tool name identifier
        description: Detailed description of tool capabilities
        args_schema: Pydantic model defining input parameters
    """

    name: str = "Crawl4AI Web Scraper"
    description: str = (
        "Scrapes and extracts content from web pages using Crawl4AI. "
        "Returns clean markdown-formatted content optimized for analysis. "
        "Use this tool when you need to extract detailed content from a specific URL, "
        "such as journal articles, regulatory documents, or technical reports. "
        "The tool handles JavaScript rendering, extracts main content while filtering "
        "navigation and ads, and provides structured markdown output."
    )
    args_schema: type[BaseModel] = Crawl4AIInput

    def _run(
        self,
        url: str,
        markdown: bool = True,
        remove_links: bool = False,
    ) -> str:
        """Execute web scraping using Crawl4AI.

        Args:
            url: The URL to scrape
            markdown: Whether to return markdown format (default: True)
            remove_links: Whether to remove links from output (default: False)

        Returns:
            Extracted content as markdown string, or error message if scraping fails

        Raises:
            Exception: If scraping fails critically
        """
        try:
            import asyncio

            async def scrape():
                async with AsyncWebCrawler(verbose=False) as crawler:
                    result = await crawler.arun(
                        url=url,
                        bypass_cache=True,
                    )

                    if result.success:
                        content = result.markdown if markdown else result.cleaned_html
                        if remove_links:
                            # Simple link removal from markdown
                            import re

                            content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)
                        return content
                    else:
                        error_msg = f"Failed to scrape {url}: {result.error_message}"
                        logger.error(error_msg)
                        return error_msg

            return asyncio.run(scrape())

        except Exception as e:
            error_msg = f"Error scraping {url}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg


