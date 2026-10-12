"""
app/models/project.py
---------------------
Dataclass representing a project document stored in Firestore.

Collection: ``projects``
Document ID: slug string (also stored as the ``slug`` field inside the doc).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """In-memory representation of a Firestore project document."""

    id: str                         # UUID string
    slug: str                       # Used as Firestore doc ID
    name: str
    category: str
    published: bool = False
    display_order: int = 0
    summary: Optional[str] = None
    description: Optional[str] = None
    image_urls: list = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # ── Helpers ───────────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialise to a plain dict suitable for Firestore ``set()``."""
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "category": self.category,
            "summary": self.summary,
            "description": self.description,
            "image_urls": self.image_urls or [],
            "published": self.published,
            "display_order": self.display_order,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Project:
        """Deserialise from a Firestore document dict."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            slug=data["slug"],
            name=data["name"],
            category=data["category"],
            summary=data.get("summary"),
            description=data.get("description"),
            image_urls=data.get("image_urls") or [],
            published=data.get("published", False),
            display_order=data.get("display_order", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
