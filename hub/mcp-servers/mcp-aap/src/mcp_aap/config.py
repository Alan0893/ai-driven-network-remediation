"""AAP MCP server configuration."""

import os
from typing import Literal

MCP_TRANSPORT: Literal["stdio", "sse", "streamable-http"] = os.environ.get(
    "MCP_TRANSPORT", "sse"
)  # type: ignore[assignment]
MCP_PORT = int(os.environ.get("MCP_PORT", "8004"))
MCP_HOST = os.environ.get("MCP_HOST", "0.0.0.0")

AAP_URL = os.getenv("AAP_URL", "https://aap.aap.svc")
AAP_API_PREFIX = os.getenv("AAP_API_PREFIX", "/api/v2")
AAP_USERNAME = os.environ["AAP_USERNAME"]
AAP_PASSWORD = os.environ["AAP_PASSWORD"]
AAP_VERIFY_SSL = os.getenv("AAP_VERIFY_SSL", "true").lower() == "true"
