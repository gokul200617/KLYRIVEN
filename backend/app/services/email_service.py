"""
app/services/email_service.py
------------------------------
Email notification service for enquiry submissions.
"""

from __future__ import annotations

import asyncio
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import aiosmtplib
from aiosmtplib import SMTPAuthenticationError

from app.core.config import settings
from app.models.enquiry import Enquiry

logger = logging.getLogger(__name__)


def _format_enquiry_email(enquiry: Enquiry) -> str:
    """Format enquiry details into a readable email body (HTML)."""

    budget = enquiry.estimated_budget or "Not specified"
    timeline = enquiry.timeline or "Not specified"
    company = enquiry.company or "Not provided"

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #1B1E4A;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #1B1E4A;
            color: #F2F0E8;
            padding: 20px;
            border-radius: 8px 8px 0 0;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 300;
            letter-spacing: -0.02em;
        }}
        .content {{
            background-color: #ffffff;
            border: 1px solid #E5E5E5;
            border-top: none;
            padding: 30px;
            border-radius: 0 0 8px 8px;
        }}
        .field {{
            margin-bottom: 20px;
        }}
        .label {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #D21319;
            margin-bottom: 6px;
        }}
        .value {{
            font-size: 15px;
            color: #1B1E4A;
            padding: 8px 0;
        }}
        .description {{
            background-color: #F9F9F9;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #D21319;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .meta {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #E5E5E5;
            font-size: 13px;
            color: #777;
        }}
        .service-badge {{
            display: inline-block;
            background-color: #1B1E4A;
            color: #F2F0E8;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.03em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 New Project Enquiry</h1>
    </div>

    <div class="content">
        <div class="field">
            <div class="label">Service Interest</div>
            <div class="value">
                <span class="service-badge">{enquiry.service_interest}</span>
            </div>
        </div>

        <div class="field">
            <div class="label">Client Name</div>
            <div class="value">{enquiry.name}</div>
        </div>

        <div class="field">
            <div class="label">Email Address</div>
            <div class="value">
                <a href="mailto:{enquiry.email}" style="color: #D21319; text-decoration: none;">{enquiry.email}</a>
            </div>
        </div>

        <div class="field">
            <div class="label">Company</div>
            <div class="value">{company}</div>
        </div>

        <div class="field">
            <div class="label">Estimated Budget</div>
            <div class="value">{budget}</div>
        </div>

        <div class="field">
            <div class="label">Timeline</div>
            <div class="value">{timeline}</div>
        </div>

        <div class="field">
            <div class="label">Project Description</div>
            <div class="value description">{enquiry.description}</div>
        </div>

        <div class="meta">
            <strong>Enquiry ID:</strong> {enquiry.id}<br>
            <strong>Submitted:</strong> {enquiry.created_at.strftime('%B %d, %Y at %I:%M %p UTC')}<br>
            <strong>Status:</strong> {enquiry.status.upper()}
        </div>
    </div>
</body>
</html>
"""
    return html


async def send_enquiry_notification(enquiry: Enquiry) -> bool:
    """Send email notification for a new enquiry.

    Args:
        enquiry: The enquiry object to send notification for

    Returns:
        True if email sent successfully, False otherwise
    """
    if not settings.EMAIL_ENABLED:
        logger.warning("Email notifications disabled (EMAIL_ENABLED=false), skipping")
        print("⚠️  Email notifications disabled. Set EMAIL_ENABLED=true in .env")
        return False

    if not settings.EMAIL_USERNAME or not settings.EMAIL_PASSWORD:
        logger.error("Email credentials not configured, skipping notification")
        print(f"❌ Email credentials missing:")
        print(f"   EMAIL_USERNAME: {'SET' if settings.EMAIL_USERNAME else 'NOT SET'}")
        print(f"   EMAIL_PASSWORD: {'SET' if settings.EMAIL_PASSWORD else 'NOT SET'}")
        return False

    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Enquiry: {enquiry.service_interest} — {enquiry.name}"
        message["From"] = settings.EMAIL_FROM
        message["To"] = settings.EMAIL_TO
        message["Reply-To"] = enquiry.email

        # Plain text fallback
        text_body = f"""
New Project Enquiry Received
=============================

SERVICE INTEREST: {enquiry.service_interest}

CLIENT DETAILS
--------------
Name: {enquiry.name}
Email: {enquiry.email}
Company: {enquiry.company or 'Not provided'}

PROJECT DETAILS
---------------
Budget: {enquiry.estimated_budget or 'Not specified'}
Timeline: {enquiry.timeline or 'Not specified'}

DESCRIPTION
-----------
{enquiry.description}

---
Enquiry ID: {enquiry.id}
Submitted: {enquiry.created_at.strftime('%B %d, %Y at %I:%M %p UTC')}
Status: {enquiry.status.upper()}
"""

        html_body = _format_enquiry_email(enquiry)

        # Attach parts
        part1 = MIMEText(text_body, "plain", "utf-8")
        part2 = MIMEText(html_body, "html", "utf-8")
        message.attach(part1)
        message.attach(part2)

        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_USERNAME,
            password=settings.EMAIL_PASSWORD,
            use_tls=True,
            timeout=10,
        )

        logger.info(
            "Enquiry notification email sent",
            extra={
                "enquiry_id": enquiry.id,
                "to": settings.EMAIL_TO,
                "service": enquiry.service_interest,
            }
        )
        return True

    except aiosmtplib.SMTPAuthenticationError as e:
        logger.error(
            f"SMTP authentication failed: {e}",
            extra={"enquiry_id": enquiry.id},
            exc_info=True
        )
        print(f"❌ SMTP Authentication Error: {e}")
        print(f"   Check your EMAIL_USERNAME and EMAIL_PASSWORD")
        print(f"   Make sure you're using an app password from Zoho Mail")
        return False

    except aiosmtplib.SMTPException as e:
        logger.error(
            f"SMTP error sending enquiry notification: {e}",
            extra={"enquiry_id": enquiry.id},
            exc_info=True
        )
        print(f"❌ SMTP Error: {e}")
        print(f"   Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        return False

    except Exception as e:
        logger.error(
            f"Unexpected error sending enquiry notification: {e}",
            extra={"enquiry_id": enquiry.id},
            exc_info=True
        )
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False
