"""
app/main.py
-----------
FastAPI application factory and startup configuration.
Database: Firebase Firestore (replaces PostgreSQL/SQLAlchemy).
"""

from __future__ import annotations

import logging
import sys
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Windows requires SelectorEventLoop for some async I/O operations.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.core.config import settings
from app.db.firebase import init_firebase
from app.api.routes import health as health_router
from app.api.routes import enquiries as enquiries_router
from app.api.routes import projects as projects_router

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.APP_DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate limiter (module-level singleton)
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])


# ---------------------------------------------------------------------------
# Lifespan — startup / shutdown
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("KLYRIVEN API starting up (env=%s)", settings.APP_ENV)

    try:
        init_firebase()
        logger.info("Firestore: connected")
    except Exception as exc:
        logger.warning("Firebase initialisation failed at startup: %s", exc)

    yield

    logger.info("KLYRIVEN API shutting down")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
def create_app() -> FastAPI:
    app = FastAPI(
        title="KLYRIVEN API",
        description="Backend API for the KLYRIVEN digital agency website.",
        version="2.0.0",
        docs_url="/api/docs" if settings.APP_DEBUG else None,
        redoc_url="/api/redoc" if settings.APP_DEBUG else None,
        openapi_url="/api/openapi.json" if settings.APP_DEBUG else None,
        lifespan=lifespan,
    )

    # ── Rate limiting ─────────────────────────────────────────────────────────
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ── Middleware ────────────────────────────────────────────────────────────
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # ── Routers ───────────────────────────────────────────────────────────────
    api_prefix = "/api"
    app.include_router(health_router.router, prefix=api_prefix)
    app.include_router(enquiries_router.router, prefix=api_prefix)
    app.include_router(projects_router.router, prefix=api_prefix)

    # ── Static frontend files ─────────────────────────────────────────────────
    try:
        from pathlib import Path
        from fastapi.staticfiles import StaticFiles

        frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
        if not frontend_dir.exists():
            frontend_dir = Path("../frontend").resolve()

        if frontend_dir.exists():
            app.mount(
                "/",
                StaticFiles(directory=str(frontend_dir), html=True),
                name="frontend",
            )
            logger.info("Frontend static files mounted from %s", frontend_dir)
        else:
            logger.info("Frontend directory not found — skipping static mount.")
    except Exception as exc:
        logger.info("Static file mount skipped: %s", exc)

    # ── Exception handlers ────────────────────────────────────────────────────
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = []
        for error in exc.errors():
            loc = " → ".join(str(p) for p in error.get("loc", []))
            errors.append({"field": loc, "message": error.get("msg", "Invalid value")})
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Validation failed.", "errors": errors},
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.critical(
            "Unhandled exception on %s %s: %s",
            request.method, request.url, exc,
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An internal server error occurred. Please try again later."},
        )

    return app


# ---------------------------------------------------------------------------
# ASGI entry point
# ---------------------------------------------------------------------------
app = create_app()
