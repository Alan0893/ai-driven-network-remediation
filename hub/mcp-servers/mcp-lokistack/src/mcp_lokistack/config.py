"""LokiStack MCP server configuration."""

import os
from typing import Literal

MCP_TRANSPORT: Literal["stdio", "sse", "streamable-http"] = os.environ.get(
    "MCP_TRANSPORT", "sse"
)  # type: ignore[assignment]
MCP_PORT = int(os.environ.get("MCP_PORT", "8002"))
MCP_HOST = os.environ.get("MCP_HOST", "0.0.0.0")

LOKI_URL = os.getenv("LOKI_URL", "http://logging-loki-gateway.openshift-logging.svc:8080")
LOKI_TOKEN = os.getenv("LOKI_TOKEN", "")
DEFAULT_NAMESPACE = os.getenv("DEFAULT_NAMESPACE", "dark-noc-edge")
