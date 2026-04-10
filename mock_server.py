"""
Mock External MCP Server — for testing mcp-gateway relay & directory.

Provides simple tools to validate MCP protocol end-to-end:
  - echo(text): return text unchanged (request/response validation)
  - get_time(): return current UTC time (no-arg tool)
  - add(a, b): integer addition (multi-arg tool)

Dual transport:
  stdio:  python mock_server.py              → for gateway stdio relay testing
  HTTP:   python mock_server.py --http 8400  → for gateway remote directory testing
"""

import argparse
import asyncio
import datetime
import logging
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="mock-external-server",
    instructions="Mock MCP server for testing. Provides echo, time, and add tools.",
)


@mcp.tool(description="Echo: return the input text unchanged.")
def echo(
    text: Annotated[str, Field(description="Text to echo back")],
) -> str:
    return text


@mcp.tool(description="Return current UTC time as ISO 8601 string.")
def get_time() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@mcp.tool(description="Add two numbers and return the sum.")
def add(
    a: Annotated[float, Field(description="First number")],
    b: Annotated[float, Field(description="Second number")],
) -> str:
    return str(a + b)


async def main():
    parser = argparse.ArgumentParser(description="Mock External MCP Server")
    parser.add_argument(
        "--http", type=int, metavar="PORT", default=None,
        help="Run as Streamable HTTP server on PORT (default: stdio)",
    )
    args = parser.parse_args()

    if args.http:
        logger.info("Mock server starting on HTTP port %d", args.http)
        await mcp.run_streamable_http_async(host="127.0.0.1", port=args.http)
    else:
        logger.info("Mock server starting on stdio")
        await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
