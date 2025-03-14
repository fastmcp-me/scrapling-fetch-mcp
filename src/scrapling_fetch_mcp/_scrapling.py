from pydantic import BaseModel, Field
from readabilipy import simple_tree_from_html_string
from scrapling.defaults import AsyncFetcher, StealthyFetcher

from scrapling_fetch_mcp._markdownify import _CustomMarkdownify


class UrlFetchRequest(BaseModel):
    url: str = Field(..., description="URL to fetch")
    mode: str = Field(
        "basic", description="Fetching mode (basic, stealth, or max-stealth)"
    )
    format: str = Field("markdown", description="Output format (html or markdown)")
    max_length: int = Field(
        5000,
        description="Maximum number of characters to return.",
        gt=0,
        lt=1000000,
        title="Max Length",
    )
    start_index: int = Field(
        0,
        description="On return output starting at this character index, useful if a previous fetch was truncated and more context is required.",
        ge=0,
        title="Start Index",
    )


async def fetch_url(request: UrlFetchRequest) -> str:
    if request.mode == "basic":
        page = await AsyncFetcher.get(request.url, stealthy_headers=True)
    elif request.mode == "stealth":
        page = await StealthyFetcher.async_fetch(
            request.url, headless=True, network_idle=True
        )
    elif request.mode == "max-stealth":
        page = await StealthyFetcher.async_fetch(
            request.url,
            headless=True,
            block_webrtc=True,
            network_idle=True,
            disable_resources=False,
            block_images=False,
        )
    else:
        raise ValueError(f"Unknown mode: {request.mode}")
    content = _extract_content(page, request)
    return content[request.start_index : request.start_index + request.max_length]


def _extract_content(page, request) -> str:
    is_markdown = request.format == "markdown"
    return _html_to_markdown(page.html_content) if is_markdown else page.html_content


def _html_to_markdown(html: str, **kwargs) -> str:
    tree = simple_tree_from_html_string(html)
    return _CustomMarkdownify().convert_soup(tree)
