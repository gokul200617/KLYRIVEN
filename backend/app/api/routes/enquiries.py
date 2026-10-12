"""
app/api/routes/enquiries.py
----------------------------
Enquiry submission endpoint — backed by Firestore.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.db.firebase import firestore_dep
from app.schemas.enquiry import EnquiryCreate, EnquiryResponse
from app.services import enquiry_service

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(tags=["enquiries"])


@router.post(
    "/enquiries",
    response_model=EnquiryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new project enquiry",
    responses={
        201: {"description": "Enquiry received successfully."},
        422: {"description": "Validation error — check the request body."},
        429: {"description": "Too many requests or duplicate submission."},
        503: {"description": "Service temporarily unavailable."},
    },
)
@limiter.limit(settings.RATE_LIMIT_ENQUIRIES)
async def submit_enquiry(
    request: Request,
    payload: EnquiryCreate,
    db=Depends(firestore_dep),
) -> EnquiryResponse:
    """Accept and persist a new client enquiry to Firestore.

    - Validated against :class:`~app.schemas.enquiry.EnquiryCreate`.
    - Rate-limited to ``RATE_LIMIT_ENQUIRIES`` (default 5/minute) per IP.
    - Duplicate submissions from the same email within 5 minutes are rejected.
    """
    try:
        enquiry = await enquiry_service.create_enquiry(db=db, data=payload)
    except HTTPException:
        raise
    except Exception as exc:
        logger.critical("Unexpected error during enquiry creation: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An unexpected error occurred. Please try again later.",
        ) from exc

    logger.info(
        "Enquiry submitted successfully",
        extra={"enquiry_id": enquiry.id, "service_interest": enquiry.service_interest},
    )
    return EnquiryResponse.model_validate(enquiry, from_attributes=True)
