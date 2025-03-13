from typing import Optional

from pydantic import BaseModel, Field
from scrapling.defaults import AsyncFetcher, StealthyFetcher


class QuickBrowsingRequest(BaseModel):
    url: str = Field(..., description="URL to browse")
    browser_type: str = Field(
        "basic",
        description="Browser type for scraping (basic or stealth). Defaults to basic for efficiency; consider stealth for sites with bot detection.",
    )
    selector: Optional[str] = Field(
        None, description="CSS selector to extract specific content"
    )
    format: str = Field("text", description="Output format (text or html)")
    auto_match: bool = Field(
        False,
        description="Use Scrapling's auto-matching to find elements after website changes",
    )
    auto_save: bool = Field(
        False, description="Save element information for future auto-matching"
    )
    network_idle: bool = Field(
        True, description="Wait for network to be idle before scraping"
    )
    headless: bool = Field(True, description="Run browser in headless mode")
    disable_resources: bool = Field(
        False, description="Disable loading of non-essential resources"
    )
    proxy: Optional[str] = Field(None, description="Proxy to use for the request")


class StealthyBrowsingRequest(BaseModel):
    url: str = Field(..., description="URL to browse")
    headless: bool = Field(
        True,
        description="Run browser in headless (invisible) mode by default. Setting to False shows the browser window, which can help bypass certain bot detection systems but may interrupt your workflow.",
    )
    block_images: bool = Field(
        False, description="Prevent loading of images through browser preferences"
    )
    disable_resources: bool = Field(
        False, description="Drop requests of unnecessary resources for a speed boost"
    )
    block_webrtc: bool = Field(
        True, description="Blocks WebRTC entirely to prevent IP leaks"
    )
    humanize: Optional[float] = Field(
        None,
        description="Humanize cursor movement (set to max duration in seconds or True)",
    )
    network_idle: bool = Field(
        True, description="Wait for network connections to be idle"
    )
    timeout: int = Field(
        30000, description="Timeout in milliseconds for page operations"
    )
    proxy: Optional[str] = Field(
        None, description="Proxy to use (string or dict with server/username/password)"
    )


async def quick_browse(request: QuickBrowsingRequest) -> str:
    if request.browser_type == "basic":
        page = await AsyncFetcher.get(request.url, stealthy_headers=True)
    elif request.browser_type == "stealth":
        page = await StealthyFetcher.async_fetch(
            request.url,
            headless=request.headless,
            network_idle=request.network_idle,
            block_webrtc=True,
            disable_resources=request.disable_resources,
            proxy=request.proxy,
        )
    else:
        raise ValueError(f"Unknown browser type: {request.browser_type}")

    return _extract_content(page, request)


def _extract_content(page, request: QuickBrowsingRequest) -> str:
    if request.selector:
        if request.auto_match:
            elements = page.css(request.selector, auto_match=True)
        elif request.auto_save:
            elements = page.css(request.selector, auto_save=True)
        else:
            elements = page.css(request.selector)

        if request.format == "text":
            return "\n".join([el.text for el in elements])
        else:
            return "\n".join([el.html_content for el in elements])
    else:
        if request.format == "text":
            return page.get_all_text(ignore_tags=("script", "style"))
        else:
            return page.html_content


async def stealthy_browse(request: StealthyBrowsingRequest) -> str:
    page = await StealthyFetcher.async_fetch(
        request.url,
        headless=request.headless,
        block_images=request.block_images,
        disable_resources=request.disable_resources,
        block_webrtc=request.block_webrtc,
        humanize=request.humanize,
        network_idle=request.network_idle,
        timeout=request.timeout,
        proxy=request.proxy,
    )
    return page.get_all_text(ignore_tags=("script", "style"))
