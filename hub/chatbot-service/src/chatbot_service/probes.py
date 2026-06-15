"""HTTP health probes for MCP servers and ServiceNow."""

from __future__ import annotations

from typing import Any

import httpx

from .config import (
    SERVICENOW_API_KEY,
    SERVICENOW_MODE,
    SERVICENOW_PASSWORD,
    SERVICENOW_URL,
    SERVICENOW_USERNAME,
)


def is_real_servicenow() -> bool:
    return SERVICENOW_MODE == "real" or bool(SERVICENOW_USERNAME and SERVICENOW_PASSWORD)


async def probe_http(url: str, timeout: float = 4.0) -> dict[str, Any]:
    """Probe a service endpoint. Treats 200/401/403/404/405 as reachable."""
    try:
        async with httpx.AsyncClient(timeout=timeout, verify=False) as client:
            resp = await client.get(url)
            reachable = resp.status_code in {200, 401, 403, 404, 405}
            return {
                "status": "up" if reachable else f"http-{resp.status_code}",
                "http_code": resp.status_code,
                "reachable": reachable,
            }
    except Exception:
        return {"status": "down", "http_code": None, "reachable": False}


async def fetch_servicenow_incident_count() -> tuple[int, str]:
    """Get open incident count from ServiceNow (real or mock)."""
    try:
        async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
            if is_real_servicenow():
                resp = await client.get(
                    f"{SERVICENOW_URL}/api/now/table/incident?sysparm_limit=100&sysparm_fields=number",
                    auth=(SERVICENOW_USERNAME, SERVICENOW_PASSWORD),
                )
                if resp.status_code == 200:
                    return len(resp.json().get("result", [])), "up"
                return 0, f"http-{resp.status_code}"

            resp = await client.get(
                f"{SERVICENOW_URL}/api/now/table/incident",
                headers={"X-API-Key": SERVICENOW_API_KEY} if SERVICENOW_API_KEY else {},
            )
            if resp.status_code == 200:
                data = resp.json()
                return int(data.get("count", 0)), "up"
            return 0, f"http-{resp.status_code}"
    except Exception:
        return 0, "down"
