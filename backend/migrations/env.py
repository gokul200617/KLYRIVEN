"""
migrations/env.py
-----------------
Alembic async migration environment.

Supports both offline (SQL script generation) and online (live DB) modes.
DATABASE_URL is read from the environment / .env file — never from alembic.ini —
so credentials don't end up in source control.
"""

from __future__ import annotations

import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ---------------------------------------------------------------------------
# Make sure the `app` package is importable from this script, regardless of
# how alembic is invoked (e.g. from a different working directory).
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Import Base so that target_metadata includes all table definitions.
from app.db.base import Base  # noqa: E402  (import after sys.path tweak)
import app.models  # noqa: F401, E402  (ensure all models are registered)

# ---------------------------------------------------------------------------
# Alembic config object — gives access to values in alembic.ini
# ---------------------------------------------------------------------------
config = context.config

# Wire up Python logging from alembic.ini [loggers] section.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The metadata object that Alembic will diff against.
target_metadata = Base.metadata

# ---------------------------------------------------------------------------
# Resolve DATABASE_URL
# ---------------------------------------------------------------------------
def _get_database_url() -> str:
    """Return the database URL from environment, falling back to .env file."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        # Try loading from .env relative to the project root.
        env_path = Path(__file__).resolve().parents[1] / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
            url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Copy .env.example to .env and fill in your credentials."
        )
    return url


# ---------------------------------------------------------------------------
# Offline mode — generate SQL without a live connection
# ---------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Emit migration SQL to stdout instead of executing against a live DB."""
    url = _get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online mode — run migrations against a live async connection
# ---------------------------------------------------------------------------
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and delegate to the sync callback."""
    url = _get_database_url()
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # don't pool connections during migrations
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
