"""
Quick test script to verify email configuration and sending.
"""
import asyncio
from datetime import datetime, timezone
from app.core.config import settings
from app.models.enquiry import Enquiry
from app.services.email_service import send_enquiry_notification

async def test_email():
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION TEST")
    print("="*60)

    # Check configuration
    print(f"\n✓ EMAIL_ENABLED: {settings.EMAIL_ENABLED}")
    print(f"✓ EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"✓ EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"✓ EMAIL_USERNAME: {settings.EMAIL_USERNAME}")
    print(f"✓ EMAIL_PASSWORD: {'***SET***' if settings.EMAIL_PASSWORD and settings.EMAIL_PASSWORD != 'PASTE_YOUR_ZOHO_APP_PASSWORD_HERE' else '❌ NOT SET'}")
    print(f"✓ EMAIL_FROM: {settings.EMAIL_FROM}")
    print(f"✓ EMAIL_TO: {settings.EMAIL_TO}")

    if not settings.EMAIL_ENABLED:
        print("\n❌ ERROR: EMAIL_ENABLED is False")
        print("   Set EMAIL_ENABLED=true in your .env file")
        return

    if not settings.EMAIL_PASSWORD or settings.EMAIL_PASSWORD == 'PASTE_YOUR_ZOHO_APP_PASSWORD_HERE':
        print("\n❌ ERROR: EMAIL_PASSWORD is not set")
        print("   Please set your Zoho app password in .env file")
        print("\n📝 To get a Zoho app password:")
        print("   1. Go to https://mail.zoho.in")
        print("   2. Settings → Security → App Passwords")
        print("   3. Generate new app password")
        print("   4. Copy it and paste in .env file")
        return

    # Create test enquiry
    print("\n" + "-"*60)
    print("Sending test email...")
    print("-"*60)

    test_enquiry = Enquiry(
        id="test-email-" + datetime.now().strftime("%Y%m%d-%H%M%S"),
        name="Test Client",
        email="test@example.com",
        company="Test Company Ltd",
        service_interest="Website Design & Development",
        estimated_budget="$10,000 - $25,000",
        timeline="2-3 months",
        description="This is a test enquiry to verify the email notification system is working correctly. If you receive this email, everything is configured properly!",
        consent_given=True,
        status="new",
        created_at=datetime.now(timezone.utc),
    )

    try:
        success = await send_enquiry_notification(test_enquiry)

        if success:
            print("\n✅ SUCCESS! Email sent successfully!")
            print(f"   Check {settings.EMAIL_TO} for the test email")
            print(f"\n   Subject: New Enquiry: {test_enquiry.service_interest} — {test_enquiry.name}")
        else:
            print("\n❌ FAILED: Email was not sent")
            print("   Check the logs above for errors")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_email())
