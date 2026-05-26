"""
Ansible Automation Platform MCP Server
========================================
MCP server wrapping the AAP 2.5 REST API as tools
for the AI-driven network remediation agent.

Tools:
    list_job_templates  - List available Ansible job templates
    launch_job          - Trigger a job template execution
    upsert_job_template - Create/update a template for a playbook path
    get_job_status      - Poll job completion status
    get_job_output      - Get stdout from a completed/failed job

Transport: Configurable via MCP_TRANSPORT env var (default: sse)
"""

from typing import Any

from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse

from .config import MCP_HOST, MCP_PORT, MCP_TRANSPORT

mcp = FastMCP(
    "noc-aap",
    instructions=(
        "Ansible Automation Platform tools for triggering remediation playbooks. "
        "Use launch_job to execute Ansible playbooks on the edge cluster. "
        "Always check get_job_status after launching — don't assume success."
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
    """Run the AAP MCP server."""
    mcp.run(transport=MCP_TRANSPORT)


from . import tools as _tools  # noqa: E402, F401

app = mcp.streamable_http_app()
