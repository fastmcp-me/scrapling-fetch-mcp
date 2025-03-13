import asyncio
from importlib.metadata import version as pkg_ver

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, ErrorData, TextContent, Tool
from pydantic import ValidationError

from scrapling_mcp.scrapling import (
    QuickBrowsingRequest,
    StealthyBrowsingRequest,
    quick_browse,
    stealthy_browse,
)

quick_browse_tool = Tool(
    name="scrapling_browse_quick",
    description="Browses a webpage using Scrapling with bot-detection avoidance. "
    "Supports basic and stealth browser types. "
    "Returns full page content or specific elements based on CSS selectors.",
    inputSchema=QuickBrowsingRequest.model_json_schema(),
)

stealthy_browse_tool = Tool(
    name="scrapling_browse_stealth",
    description="Performs advanced stealth browsing of a website with Scrapling's most powerful anti-detection capabilities. "
    "Uses StealthyFetcher for maximum protection against bot detection with options for human-like behavior.",
    inputSchema=StealthyBrowsingRequest.model_json_schema(),
)


async def serve() -> None:
    server: Server = Server("scrapling-mcp", pkg_ver("scrapling-mcp"))

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return [quick_browse_tool, stealthy_browse_tool]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "scrapling_browse_quick":
                request = QuickBrowsingRequest(**arguments)
                content = await quick_browse(request)
                return [TextContent(type="text", text=content)]
            elif name == "scrapling_browse_stealth":
                request = StealthyBrowsingRequest(**arguments)
                content = await stealthy_browse(request)
                return [TextContent(type="text", text=content)]
            else:
                raise McpError(
                    ErrorData(code=INVALID_PARAMS, message=f"Unknown tool: {name}")
                )
        except ValidationError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))
        except Exception as e:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR, message=f"Error processing {name}: {str(e)}"
                )
            )

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
            raise_exceptions=True,
        )


def run_server():
    asyncio.run(serve())


if __name__ == "__main__":
    run_server()
