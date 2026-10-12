"""
tests/test_health.py
--------------------
Automated tests for GET /api/health.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_structure(client: AsyncClient):
    """GET /api/health should always return 200 with structured status."""
    response = await client.get("/api/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "timestamp" in data
    assert "version" in data
    assert data["status"] in ("ok", "degraded")
    assert data["database"] in ("connected", "unavailable")

