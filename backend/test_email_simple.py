"""
Simple email test without full app configuration
"""
import asyncio
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load .env file
load_dotenv()

async def test_email_simple():
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION TEST")
    print("="*60)

    # Check configuration from environment
    email_enabled = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
    email_host = os.getenv('EMAIL_HOST', '')
    email_port = int(os.getenv('EMAIL_PORT', '587'))
    email_username = os.getenv('EMAIL_USERNAME', '')
    email_password = os.getenv('EMAIL_PASSWORD', '')
    email_from = os.getenv('EMAIL_FROM', '')
    email_to = os.getenv('EMAIL_TO', '')

    print(f"\n✓ EMAIL_ENABLED: {email_enabled}")
    print(f"✓ EMAIL_HOST: {email_host}")
    print(f"✓ EMAIL_PORT: {email_port}")
    print(f"✓ EMAIL_USERNAME: {email_username}")
    print(f"✓ EMAIL_PASSWORD: {'***SET***' if email_password else '❌ NOT SET'}")
    print(f"✓ EMAIL_FROM: {email_from}")
    print(f"✓ EMAIL_TO: {email_to}")

    if not email_enabled:
        print("\n❌ ERROR: EMAIL_ENABLED is False")
        return

    if not email_password:
        print("\n❌ ERROR: EMAIL_PASSWORD is not set")
        return

    # Test email sending
    print("\n" + "-"*60)
    print("Sending test email...")
    print("-"*60)

    try:
        import aiosmtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Test Email from KLYRIVEN Backend - {datetime.now().strftime('%H:%M:%S')}"
        message["From"] = email_from
        message["To"] = email_to

        text_body = """
KLYRIVEN Email Test
===================

This is a test email from your KLYRIVEN backend.

If you received this email, your email configuration is working correctly!

Test Details:
- Host: {host}
- Port: {port}
- From: {from_addr}
- Time: {time}

✅ Email notifications are ready to use!
""".format(
            host=email_host,
            port=email_port,
            from_addr=email_from,
            time=datetime.now(timezone.utc).strftime('%B %d, %Y at %I:%M %p UTC')
        )

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1B1E4A;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #1B1E4A;
            color: #F2F0E8;
            padding: 30px 20px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .content {{
            background-color: #ffffff;
            border: 1px solid #E5E5E5;
            border-top: none;
            padding: 30px;
            border-radius: 0 0 8px 8px;
        }}
        .success {{
            background-color: #D4EDDA;
            border: 1px solid #C3E6CB;
            color: #155724;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            text-align: center;
            font-weight: 600;
        }}
        .meta {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #E5E5E5;
            font-size: 13px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ KLYRIVEN Email Test</h1>
    </div>
    <div class="content">
        <p>This is a test email from your <strong>KLYRIVEN backend</strong>.</p>

        <div class="success">
            ✅ Email notifications are working correctly!
        </div>

        <p>Your email configuration is set up properly and ready to send enquiry notifications.</p>

        <div class="meta">
            <strong>Configuration:</strong><br>
            Host: {email_host}:{email_port}<br>
            From: {email_from}<br>
            Time: {datetime.now(timezone.utc).strftime('%B %d, %Y at %I:%M %p UTC')}
        </div>
    </div>
</body>
</html>
"""

        part1 = MIMEText(text_body, "plain", "utf-8")
        part2 = MIMEText(html_body, "html", "utf-8")
        message.attach(part1)
        message.attach(part2)

        # Send email
        print(f"Connecting to {email_host}:{email_port}...")
        await aiosmtplib.send(
            message,
            hostname=email_host,
            port=email_port,
            username=email_username,
            password=email_password,
            start_tls=True,
            timeout=15,
        )

        print("\n✅ SUCCESS! Email sent successfully!")
        print(f"   Check {email_to} for the test email")
        print(f"   Subject: {message['Subject']}")

    except aiosmtplib.SMTPAuthenticationError as e:
        print(f"\n❌ SMTP Authentication Error: {e}")
        print(f"   Check your EMAIL_USERNAME and EMAIL_PASSWORD")
        print(f"   Make sure you're using an app password from Zoho Mail")

    except aiosmtplib.SMTPException as e:
        print(f"\n❌ SMTP Error: {e}")
        print(f"   Host: {email_host}:{email_port}")

    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_email_simple())
