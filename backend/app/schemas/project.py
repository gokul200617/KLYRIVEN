"""
app/schemas/project.py
----------------------
Pydantic v2 schemas for the projects endpoint.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# List-view schema (lean — omit heavy fields)
# ---------------------------------------------------------------------------
class ProjectResponse(BaseModel):
    """Returned in the paginated list of projects."""

    id: uuid.UUID
    slug: str
    name: str
    category: str
    summary: str | None = None
    image_urls: list[str] = Field(default_factory=list)
    display_order: int

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Detail schema (full data)
# ---------------------------------------------------------------------------
class ProjectDetail(BaseModel):
    """Returned for a single project page."""

    id: uuid.UUID
    slug: str
    name: str
    category: str
    summary: str | None = None
    description: str | None = None
    image_urls: list[str] = Field(default_factory=list)
    published: bool
    display_order: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
