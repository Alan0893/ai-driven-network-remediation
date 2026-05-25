"""
LokiStack MCP Server
======================
MCP server for querying LokiStack via the LogQL API.
Gives the AI remediation agent access to historical log data.

Tools:
    query_logs        - Run a LogQL query against LokiStack
    get_recent_errors - Get recent error logs from a namespace/app
    count_errors      - Count error occurrences in a time window

Transport: Configurable via MCP_TRANSPORT env var (default: sse)
"""

from typing import Any

from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse

from .config import MCP_HOST, MCP_PORT, MCP_TRANSPORT

mcp = FastMCP(
    "noc-lokistack",
    instructions=(
        "LokiStack log query tools using LogQL. "
        "Use get_recent_errors for quick error lookups. "
        "Use query_logs for complex LogQL queries. "
        "Time range: use relative durations like '1h', '30m', '7d'."
    ),
    host=MCP_HOST,
    port=MCP_PORT,
    stateless_http=(MCP_TRANSPORT == "streamable-http"),
)


@mcp.custom_route("/health", methods=["GET"])  # type: ignore
async def health(request: Any) -> JSONResponse:
    """Health check endpoint for Kubernetes probes."""
    return JSONResponse({"status": "OK"})


def main() -> None:
    """Run the LokiStack MCP server."""
    mcp.run(transport=MCP_TRANSPORT)


from .tools import tools

for _tool in tools:
    mcp.add_tool(_tool)

app = mcp.streamable_http_app()
