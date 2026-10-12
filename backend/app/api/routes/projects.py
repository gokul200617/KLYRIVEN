"""
app/api/routes/projects.py
---------------------------
Read-only project portfolio endpoints — backed by Firestore.

Only published projects are ever exposed through these routes.
"""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db.firebase import firestore_dep
from app.models.project import Project
from app.schemas.project import ProjectDetail, ProjectResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["projects"])

_COLLECTION = "projects"


@router.get(
    "/projects",
    response_model=list[ProjectResponse],
    summary="List published projects",
)
async def list_projects(
    category: str | None = Query(default=None, description="Filter by category name"),
    db=Depends(firestore_dep),
) -> list[ProjectResponse]:
    """Return published projects ordered by ``display_order`` ascending.

    Optionally filter by **category** (exact, case-sensitive match).
    """
    def _query() -> list[Project]:
        col = db.collection(_COLLECTION)
        query = col.where("published", "==", True)
        if category:
            query = query.where("category", "==", category)
        items = [Project.from_dict(doc.to_dict()) for doc in query.stream()]
        items.sort(key=lambda p: p.display_order)
        return items

    projects = await asyncio.to_thread(_query)
    return [ProjectResponse.model_validate(p, from_attributes=True) for p in projects]


@router.get(
    "/projects/{slug}",
    response_model=ProjectDetail,
    summary="Get a single published project by slug",
    responses={
        200: {"description": "Project found."},
        404: {"description": "Project not found or not published."},
    },
)
async def get_project(
    slug: str,
    db=Depends(firestore_dep),
) -> ProjectDetail:
    """Return full detail for a **published** project identified by *slug*.

    Returns 404 for both non-existent and unpublished projects so that
    internal content is never accidentally disclosed.
    """
    def _get() -> Project | None:
        doc = db.collection(_COLLECTION).document(slug).get()
        if doc.exists:
            data = doc.to_dict()
            if data.get("published"):
                return Project.from_dict(data)
        return None

    project = await asyncio.to_thread(_get)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{slug}' not found.",
        )

    return ProjectDetail.model_validate(project, from_attributes=True)
