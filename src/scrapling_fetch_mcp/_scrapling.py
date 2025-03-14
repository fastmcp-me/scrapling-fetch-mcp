from typing import Any

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
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


class UrlFetchResponse(BaseModel):
    content: str
    metadata: "UrlFetchResponse.Metadata" = Field(
        default_factory=lambda: UrlFetchResponse.Metadata(),
        description="Metadata about the content retrieval",
    )

    class Metadata(BaseModel):
        total_length: int = 0
        retrieved_length: int = 0
        is_truncated: bool = False
        start_index: int = 0
        percent_retrieved: float = 100.0


async def browse_url(request: UrlFetchRequest) -> Any:
    if request.mode == "basic":
        return await AsyncFetcher.get(request.url, stealthy_headers=True)
    elif request.mode == "stealth":
        return await StealthyFetcher.async_fetch(
            request.url, headless=True, network_idle=True
        )
    elif request.mode == "max-stealth":
        return await StealthyFetcher.async_fetch(
            request.url,
            headless=True,
            block_webrtc=True,
            network_idle=True,
            disable_resources=False,
            block_images=False,
        )
    else:
        raise ValueError(f"Unknown mode: {request.mode}")


def _extract_content(page, request) -> str:
    is_markdown = request.format == "markdown"
    return _html_to_markdown(page.html_content) if is_markdown else page.html_content


def _html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    body_elm = soup.find("body")
    return _CustomMarkdownify().convert_soup(body_elm if body_elm else soup)


async def fetch_url(request: UrlFetchRequest) -> UrlFetchResponse:
    page = await browse_url(request)
    full_content = _extract_content(page, request)
    total_length = len(full_content)
    truncated_content = full_content[
        request.start_index : request.start_index + request.max_length
    ]
    is_truncated = total_length > (request.start_index + request.max_length)
    return UrlFetchResponse(
        content=truncated_content,
        metadata=UrlFetchResponse.Metadata(
            total_length=total_length,
            retrieved_length=len(truncated_content),
            is_truncated=is_truncated,
            start_index=request.start_index,
            percent_retrieved=round((len(truncated_content) / total_length) * 100, 2)
            if total_length > 0
            else 100,
        ),
    )
