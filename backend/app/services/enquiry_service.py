"""
app/services/enquiry_service.py
--------------------------------
Business-logic layer for enquiry operations — backed by Firestore.

All Firestore calls are synchronous (firebase-admin is sync-only); they are
run in a thread-pool via ``asyncio.to_thread`` so the FastAPI event loop is
never blocked.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status

from app.core.security import sanitize_optional, sanitize_string
from app.models.enquiry import Enquiry
from app.schemas.enquiry import EnquiryCreate
from app.services.email_service import send_enquiry_notification

logger = logging.getLogger(__name__)

_COLLECTION = "enquiries"
_DUPLICATE_WINDOW_MINUTES = 5


async def create_enquiry(db, data: EnquiryCreate) -> Enquiry:
    """Validate, de-duplicate, and persist a new enquiry to Firestore.

    Raises:
        HTTPException 429 — duplicate submission from the same email within
                            ``_DUPLICATE_WINDOW_MINUTES`` minutes.
    """
    # ── 1. Duplicate check ────────────────────────────────────────────────────
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=_DUPLICATE_WINDOW_MINUTES)
    normalised_email = data.email.strip().lower()

    def _check_duplicate() -> bool:
        # Single-field equality only (no composite index needed); the time
        # window is filtered in Python.
        query = db.collection(_COLLECTION).where("email", "==", normalised_email)
        new_description = sanitize_string(data.description, max_length=5_000)
        for doc in query.stream():
            existing = doc.to_dict() or {}
            created = existing.get("created_at")
            if (
                created is not None
                and created >= cutoff
                and existing.get("description") == new_description
            ):
                return True
        return False

    is_duplicate = await asyncio.to_thread(_check_duplicate)

    if is_duplicate:
        logger.warning(
            "Duplicate enquiry blocked",
            extra={"email_hash": hash(normalised_email), "window_minutes": _DUPLICATE_WINDOW_MINUTES},
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                "We've already received this exact enquiry. "
                "There's no need to submit it again — we'll be in touch soon."
            ),
        )

    # ── 2. Build document ─────────────────────────────────────────────────────
    enquiry_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    enquiry = Enquiry(
        id=enquiry_id,
        name=sanitize_string(data.name, max_length=100),
        email=normalised_email,
        company=sanitize_optional(data.company, max_length=200),
        service_interest=sanitize_string(data.service_interest, max_length=100),
        estimated_budget=sanitize_optional(data.estimated_budget, max_length=50),
        timeline=sanitize_optional(data.timeline, max_length=50),
        description=sanitize_string(data.description, max_length=5_000),
        consent_given=data.consent_given,
        status="new",
        created_at=now,
    )

    # ── 3. Persist ────────────────────────────────────────────────────────────
    def _save() -> None:
        db.collection(_COLLECTION).document(enquiry_id).set(enquiry.to_dict())

    await asyncio.to_thread(_save)

    logger.info(
        "New enquiry created",
        extra={"enquiry_id": enquiry_id, "service": enquiry.service_interest},
    )

    # ── 4. Send email notification (non-blocking) ─────────────────────────────
    # Fire-and-forget: don't block the response on email delivery
    asyncio.create_task(send_enquiry_notification(enquiry))

    return enquiry


async def get_enquiry_by_id(db, enquiry_id: uuid.UUID) -> Optional[Enquiry]:
    """Return an :class:`Enquiry` by its UUID, or *None* if not found."""

    def _get() -> Optional[Enquiry]:
        doc = db.collection(_COLLECTION).document(str(enquiry_id)).get()
        if doc.exists:
            return Enquiry.from_dict(doc.to_dict())
        return None

    return await asyncio.to_thread(_get)
