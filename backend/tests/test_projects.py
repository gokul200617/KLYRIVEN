"""
tests/test_projects.py
----------------------
Automated tests for GET /api/projects and GET /api/projects/{slug}.
"""

import uuid
from datetime import datetime, timezone
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


@pytest.mark.asyncio
async def test_get_projects_empty(client: AsyncClient):
    """When no projects exist in the database, returns an empty list."""
    response = await client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_published_project_retrieval(client: AsyncClient, db_session: AsyncSession):
    """Published projects are returned in the list and can be queried by slug."""
    proj = Project(
        id=uuid.uuid4(),
        slug="meridian",
        name="Meridian",
        category="Brand Identity",
        summary="A comprehensive visual identity for an architecture firm.",
        description="Detailed project body text.",
        image_urls=[],
        published=True,
        display_order=1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(proj)
    await db_session.commit()

    # List endpoint
    list_resp = await client.get("/api/projects")
    assert list_resp.status_code == 200
    projects = list_resp.json()
    assert len(projects) == 1
    assert projects[0]["slug"] == "meridian"
    assert projects[0]["name"] == "Meridian"

    # Detail endpoint
    detail_resp = await client.get("/api/projects/meridian")
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert detail["slug"] == "meridian"
    assert detail["category"] == "Brand Identity"


@pytest.mark.asyncio
async def test_unpublished_project_hidden(client: AsyncClient, db_session: AsyncSession):
    """Unpublished projects are not exposed in list or detail endpoints."""
    unpublished = Project(
        id=uuid.uuid4(),
        slug="secret-project",
        name="Internal Confidential",
        category="Web Design",
        summary="Internal draft project.",
        description="Draft details.",
        image_urls=[],
        published=False,  # unpublished
        display_order=2,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(unpublished)
    await db_session.commit()

    # Should not appear in list
    list_resp = await client.get("/api/projects")
    assert list_resp.status_code == 200
    assert list_resp.json() == []

    # Detail query should return 404
    detail_resp = await client.get("/api/projects/secret-project")
    assert detail_resp.status_code == 404


@pytest.mark.asyncio
async def test_nonexistent_project_404(client: AsyncClient):
    """Querying a nonexistent slug returns HTTP 404."""
    response = await client.get("/api/projects/does-not-exist")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_category_filtering(client: AsyncClient, db_session: AsyncSession):
    """Category filter parameter returns only matching published projects."""
    p1 = Project(
        id=uuid.uuid4(),
        slug="proj-brand",
        name="Brand Project",
        category="Brand Identity",
        summary="Brand summary",
        description="Brand desc",
        image_urls=[],
        published=True,
        display_order=1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    p2 = Project(
        id=uuid.uuid4(),
        slug="proj-web",
        name="Web Project",
        category="Web Design",
        summary="Web summary",
        description="Web desc",
        image_urls=[],
        published=True,
        display_order=2,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add_all([p1, p2])
    await db_session.commit()

    # Filter for Brand Identity
    resp = await client.get("/api/projects", params={"category": "Brand Identity"})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["slug"] == "proj-brand"

