"""
app/api/routes/health.py
------------------------
Health-check endpoint.  Always returns HTTP 200 so load balancers and
container orchestrators can probe it without special handling.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.db.firebase import firestore_dep

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

API_VERSION = "2.0.0"


@router.get("/health", summary="Health check")
async def health_check(db=Depends(firestore_dep)) -> dict:
    """Return service health.

    - **status**: ``"ok"`` when all subsystems are healthy, ``"degraded"`` otherwise.
    - **database**: ``"connected"`` or ``"unavailable"``.
    - **timestamp**: ISO-8601 UTC timestamp of this response.
    - **version**: current API version string.
    """
    db_status = "unavailable"
    overall_status = "degraded"

    try:
        def _ping() -> None:
            # Lightweight Firestore round-trip — read at most 1 doc from a
            # sentinel collection that may not even exist (that's fine).
            list(db.collection("_healthcheck").limit(1).stream())

        await asyncio.to_thread(_ping)
        db_status = "connected"
        overall_status = "ok"
    except Exception as exc:
        logger.warning("Health check: Firestore unavailable — %s", exc)

    return {
        "status": overall_status,
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": API_VERSION,
    }
