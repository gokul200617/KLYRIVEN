"""
app/schemas/enquiry.py
----------------------
Pydantic v2 schemas for the enquiry endpoint.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ALLOWED_SERVICES: frozenset[str] = frozenset(
    {
        "Website Design & Development",
        "UI/UX Design",
        "Brand Identity & Strategy",
        "E-commerce Experiences",
        "Digital Strategy & SEO",
        "Business Automation",
        "Not Sure Yet",
    }
)


# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------
class EnquiryCreate(BaseModel):
    """Validated payload for POST /api/enquiries."""

    name: Annotated[str, Field(min_length=2, max_length=100, examples=["Jane Smith"])]
    email: Annotated[EmailStr, Field(examples=["jane@example.com"])]
    company: Annotated[str | None, Field(default=None, max_length=200)]
    service_interest: Annotated[
        str,
        Field(examples=["Website Design & Development"]),
    ]
    estimated_budget: Annotated[str | None, Field(default=None, max_length=50)]
    timeline: Annotated[str | None, Field(default=None, max_length=50)]
    description: Annotated[
        str,
        Field(
            min_length=20,
            max_length=5000,
            examples=["We need a new e-commerce website for our fashion brand."],
        ),
    ]
    consent_given: Annotated[bool, Field(examples=[True])]

    # ── Field-level validators ────────────────────────────────────────────────

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("service_interest")
    @classmethod
    def validate_service(cls, v: str) -> str:
        v = v.strip()
        if v not in ALLOWED_SERVICES:
            allowed = ", ".join(f"'{s}'" for s in sorted(ALLOWED_SERVICES))
            raise ValueError(
                f"service_interest must be one of: {allowed}"
            )
        return v

    @field_validator("description", mode="before")
    @classmethod
    def strip_description(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    # ── Model-level validators ────────────────────────────────────────────────

    @model_validator(mode="after")
    def require_consent(self) -> EnquiryCreate:
        if not self.consent_given:
            raise ValueError(
                "consent_given must be true to submit an enquiry."
            )
        return self

    model_config = {"str_strip_whitespace": True}


# ---------------------------------------------------------------------------
# Response schema
# ---------------------------------------------------------------------------
class EnquiryResponse(BaseModel):
    """Shape of the data returned to the client after a successful submission."""

    id: uuid.UUID
    name: str
    email: str
    service_interest: str
    status: str
    created_at: datetime
    message: str = "Thank you for your enquiry. We'll be in touch within 1–2 business days."

    model_config = {"from_attributes": True}
