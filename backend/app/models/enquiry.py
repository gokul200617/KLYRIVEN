"""
app/models/enquiry.py
---------------------
Dataclass representing an enquiry document stored in Firestore.

Collection: ``enquiries``
Document ID: UUID string (also stored as the ``id`` field inside the doc).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Enquiry:
    """In-memory representation of a Firestore enquiry document."""

    id: str                         # UUID string — used as Firestore doc ID
    name: str
    email: str
    service_interest: str
    description: str
    consent_given: bool
    status: str = "new"
    company: Optional[str] = None
    estimated_budget: Optional[str] = None
    timeline: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def new_id() -> str:
        return str(uuid.uuid4())

    def to_dict(self) -> dict:
        """Serialise to a plain dict suitable for Firestore ``set()``."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "company": self.company,
            "service_interest": self.service_interest,
            "estimated_budget": self.estimated_budget,
            "timeline": self.timeline,
            "description": self.description,
            "consent_given": self.consent_given,
            "status": self.status,
            "created_at": self.created_at or datetime.now(timezone.utc),
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Enquiry:
        """Deserialise from a Firestore document dict."""
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            company=data.get("company"),
            service_interest=data["service_interest"],
            estimated_budget=data.get("estimated_budget"),
            timeline=data.get("timeline"),
            description=data["description"],
            consent_given=data.get("consent_given", False),
            status=data.get("status", "new"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
