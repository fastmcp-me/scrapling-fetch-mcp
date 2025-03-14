import asyncio
from importlib.metadata import version as pkg_ver

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, ErrorData, TextContent, Tool
from pydantic import ValidationError

from scrapling_mcp._scrapling import UrlFetchRequest, fetch_url

url_fetch_tool = Tool(
    name="fetch_url",
    description="Fetches a URL using Scrapling with bot-detection avoidance. "
    "Supports three modes: basic (fast), stealth (balanced), and max-stealth (maximum protection). "
    "Returns HTML or markdown content.",
    inputSchema=UrlFetchRequest.model_json_schema(),
)


async def serve() -> None:
    server: Server = Server("scrapling-fetch-mcp", pkg_ver("scrapling-fetch-mcp"))

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return [url_fetch_tool]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "fetch_url":
                request = UrlFetchRequest(**arguments)
                content = await fetch_url(request)
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
