"""
tests/test_enquiries.py
-----------------------
Automated tests for POST /api/enquiries.
"""

import pytest
from httpx import AsyncClient


VALID_PAYLOAD = {
    "name": "Evelyn Vance",
    "email": "evelyn@vancemedia.com",
    "company": "Vance Media International",
    "service_interest": "Website Design & Development",
    "estimated_budget": "£25k–£50k",
    "timeline": "1–3 months",
    "description": "We are seeking a bespoke digital agency partner to redesign our corporate flagship with a focus on editorial typography and international performance.",
    "consent_given": True,
}


@pytest.mark.asyncio
async def test_valid_enquiry_success(client: AsyncClient):
    """Submitting valid enquiry data creates an enquiry record and returns 201."""
    response = await client.post("/api/enquiries", json=VALID_PAYLOAD)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == VALID_PAYLOAD["name"]
    assert data["email"] == VALID_PAYLOAD["email"]
    assert data["service_interest"] == VALID_PAYLOAD["service_interest"]
    assert data["status"] == "new"
    assert "created_at" in data
    assert "message" in data


@pytest.mark.asyncio
async def test_missing_required_fields(client: AsyncClient):
    """Empty payload returns HTTP 422 Unprocessable Entity."""
    response = await client.post("/api/enquiries", json={})
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_invalid_email_format(client: AsyncClient):
    """Malformed email is rejected with HTTP 422."""
    payload = {**VALID_PAYLOAD, "email": "not-an-email"}
    response = await client.post("/api/enquiries", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_description_too_short(client: AsyncClient):
    """Description shorter than 20 characters is rejected with HTTP 422."""
    payload = {**VALID_PAYLOAD, "description": "Too brief."}
    response = await client.post("/api/enquiries", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_consent_not_given(client: AsyncClient):
    """Missing or false consent is rejected with HTTP 422."""
    payload = {**VALID_PAYLOAD, "consent_given": False}
    response = await client.post("/api/enquiries", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_service_rejected(client: AsyncClient):
    """Unrecognized service name is rejected with HTTP 422."""
    payload = {**VALID_PAYLOAD, "service_interest": "Crypto Web3 Token"}
    response = await client.post("/api/enquiries", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_duplicate_submission_blocked(client: AsyncClient):
    """Duplicate submission with identical email within short window is rejected with 429."""
    # First submission
    resp1 = await client.post("/api/enquiries", json={**VALID_PAYLOAD, "email": "dup@example.com"})
    assert resp1.status_code == 201

    # Immediate second submission with same email
    resp2 = await client.post("/api/enquiries", json={**VALID_PAYLOAD, "email": "dup@example.com"})
    assert resp2.status_code == 429

