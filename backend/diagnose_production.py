"""
Production Email Diagnostic Script
Run this on your production server to diagnose email issues
"""
import os
import sys

print("\n" + "="*70)
print("PRODUCTION EMAIL DIAGNOSTICS")
print("="*70)

# Check environment variables
print("\n1. ENVIRONMENT VARIABLES CHECK")
print("-" * 70)

env_vars = [
    'EMAIL_ENABLED',
    'EMAIL_HOST',
    'EMAIL_PORT',
    'EMAIL_USERNAME',
    'EMAIL_PASSWORD',
    'EMAIL_FROM',
    'EMAIL_TO'
]

missing = []
for var in env_vars:
    value = os.getenv(var)
    if var == 'EMAIL_PASSWORD':
        status = "SET" if value and len(value) > 5 else "MISSING"
        print(f"{var:20s} = {'***' + status + '***':30s}")
    else:
        status = "SET" if value else "MISSING"
        print(f"{var:20s} = {value or 'NOT SET':30s} [{status}]")

    if not value or (var == 'EMAIL_PASSWORD' and len(value) < 5):
        missing.append(var)

if missing:
    print(f"\n❌ MISSING VARIABLES: {', '.join(missing)}")
    print("\nSet these environment variables and restart your service!")
else:
    print("\n✅ All required variables are set")

# Check Python version
print("\n2. PYTHON ENVIRONMENT")
print("-" * 70)
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")

# Check installed packages
print("\n3. INSTALLED PACKAGES CHECK")
print("-" * 70)

required_packages = {
    'aiosmtplib': 'Email sending',
    'fastapi': 'Web framework',
    'firebase_admin': 'Firestore database',
    'pydantic': 'Data validation',
    'dotenv': 'Environment loading'
}

for package, purpose in required_packages.items():
    try:
        __import__(package)
        print(f"✅ {package:20s} - {purpose}")
    except ImportError:
        print(f"❌ {package:20s} - MISSING - {purpose}")

# Network test
print("\n4. NETWORK CONNECTIVITY TEST")
print("-" * 70)

import socket

def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

smtp_host = os.getenv('EMAIL_HOST', 'smtp.zoho.in')
smtp_port = int(os.getenv('EMAIL_PORT', '587'))

print(f"Testing connection to {smtp_host}:{smtp_port}...")
if check_port(smtp_host, smtp_port):
    print(f"✅ Can connect to {smtp_host}:{smtp_port}")
else:
    print(f"❌ Cannot connect to {smtp_host}:{smtp_port}")
    print("   Your server may be blocking outbound SMTP connections")
    print("   Contact your hosting provider about SMTP port access")

# Test DNS resolution
print(f"\nResolving {smtp_host}...")
try:
    ip = socket.gethostbyname(smtp_host)
    print(f"✅ DNS resolved: {smtp_host} → {ip}")
except Exception as e:
    print(f"❌ DNS resolution failed: {e}")

# Quick email test
print("\n5. EMAIL SENDING TEST")
print("-" * 70)

if not missing and os.getenv('EMAIL_ENABLED', 'false').lower() == 'true':
    print("Attempting to send test email...")
    try:
        import asyncio
        from email.mime.text import MIMEText
        import aiosmtplib

        async def quick_test():
            msg = MIMEText("Production diagnostic test from KLYRIVEN backend")
            msg['Subject'] = "Production Test - KLYRIVEN"
            msg['From'] = os.getenv('EMAIL_FROM')
            msg['To'] = os.getenv('EMAIL_TO')

            await aiosmtplib.send(
                msg,
                hostname=os.getenv('EMAIL_HOST'),
                port=int(os.getenv('EMAIL_PORT')),
                username=os.getenv('EMAIL_USERNAME'),
                password=os.getenv('EMAIL_PASSWORD'),
                start_tls=True,
                timeout=15,
            )

        asyncio.run(quick_test())
        print("✅ Test email sent successfully!")
        print(f"   Check {os.getenv('EMAIL_TO')} inbox")

    except Exception as e:
        print(f"❌ Email test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        print("\nFull error:")
        traceback.print_exc()
else:
    if missing:
        print("⏭️  Skipping email test - environment variables not set")
    else:
        print("⏭️  Skipping email test - EMAIL_ENABLED is false")

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70 + "\n")

# Summary
print("SUMMARY:")
if missing:
    print(f"❌ Set these variables: {', '.join(missing)}")
else:
    print("✅ Environment variables configured")

print("\nNext steps:")
print("1. Fix any issues shown above")
print("2. Restart your backend service")
print("3. Submit a test enquiry from your website")
print("4. Check email inbox within 30 seconds")
print()
