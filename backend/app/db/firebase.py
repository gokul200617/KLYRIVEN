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
    """Return the singleton Firestore client, initialising it on first use.

    Retrying here means a transient or fixed-later config problem heals
    without a restart; a persistent one raises with the real cause.
    """
    if _db is None:
        init_firebase()
    return _db


def init_error_summary(exc: Exception) -> str:
    """Short, secret-free description of an initialisation failure."""
    return f"{type(exc).__name__}: {str(exc)[:120]}"


async def firestore_dep() -> AsyncGenerator:
    """FastAPI dependency — yields the singleton Firestore client."""
    yield get_firestore()
