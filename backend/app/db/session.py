"""
app/db/session.py
-----------------
SQLAlchemy session removed. Firestore client is in app/db/firebase.py.
This file is kept to avoid breaking any stale imports during transition.
"""

from app.db.firebase import firestore_dep as get_db  # noqa: F401
