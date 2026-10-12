"""
app/db/firebase.py
------------------
Firebase / Firestore initialisation and FastAPI dependency.

Call ``init_firebase()`` once during application startup.
Use ``firestore_dep`` as a FastAPI Depends() in route handlers.
"""

from __future__ import annotations

import logging
from typing import AsyncGenerator

import firebase_admin
from firebase_admin import credentials, firestore as fb_firestore

from app.core.config import settings

logger = logging.getLogger(__name__)

_firebase_app: firebase_admin.App | None = None
_db = None  # google.cloud.firestore.Client


def init_firebase() -> None:
    """Initialise the Firebase app and Firestore client (idempotent)."""
    global _firebase_app, _db

    if _firebase_app is not None:
        return  # already initialised — safe to call multiple times

    if settings.FIREBASE_CREDENTIALS_JSON.strip():
        import json

        cred = credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS_JSON))
    else:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    _firebase_app = firebase_admin.initialize_app(cred)
    _db = fb_firestore.client()
    logger.info("Firebase initialised — Firestore client ready")


def get_firestore():
    """Return the singleton Firestore client.

    Raises RuntimeError if ``init_firebase()`` has not been called.
    """
    if _db is None:
        raise RuntimeError(
            "Firestore client is not initialised. "
            "Ensure init_firebase() is called during application startup."
        )
    return _db


async def firestore_dep() -> AsyncGenerator:
    """FastAPI dependency — yields the singleton Firestore client."""
    yield get_firestore()
