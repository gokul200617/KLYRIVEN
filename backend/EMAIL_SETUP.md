# Email Notification Setup

This guide explains how to configure email notifications for enquiry form submissions.

## Overview

When a user submits an enquiry through the contact form, the system will automatically send a formatted email notification to `contact.klyriven@zohomail.in` with all the enquiry details.

## Email Format

The email notification includes:
- **Subject**: `New Enquiry: [Service Interest] — [Client Name]`
- **Service Interest**: Highlighted badge showing the selected service
- **Client Details**: Name, email, and company
- **Project Details**: Budget, timeline, and description
- **Metadata**: Enquiry ID, submission timestamp, and status
- **Reply-To**: Set to the client's email for easy responses

## Configuration Steps

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install `aiosmtplib>=3.0.0` which is required for async email sending.

### 2. Set Up Zoho Mail App Password

1. Log into your Zoho Mail account: https://mail.zoho.in
2. Go to Settings → Security → App Passwords
3. Generate a new app password for "KLYRIVEN Backend API"
4. Copy the generated password (you won't see it again)

### 3. Configure Environment Variables

Create or update the `.env` file in the `backend/` directory:

```bash
# Email notifications
EMAIL_ENABLED=true
EMAIL_HOST=smtp.zoho.in
EMAIL_PORT=587
EMAIL_USERNAME=contact.klyriven@zohomail.in
EMAIL_PASSWORD=your-app-password-here
EMAIL_FROM=contact.klyriven@zohomail.in
EMAIL_TO=contact.klyriven@zohomail.in
```

**Important**: 
- Replace `your-app-password-here` with the actual app password from step 2
- Never commit the `.env` file to git (it's already in `.gitignore`)
- For production, set these as environment variables on your hosting platform

### 4. Production Deployment

For production environments (e.g., Render, Railway, Heroku, etc.):

1. Set the following environment variables in your hosting dashboard:
   ```
   EMAIL_ENABLED=true
   EMAIL_HOST=smtp.zoho.in
   EMAIL_PORT=587
   EMAIL_USERNAME=contact.klyriven@zohomail.in
   EMAIL_PASSWORD=<your-app-password>
   EMAIL_FROM=contact.klyriven@zohomail.in
   EMAIL_TO=contact.klyriven@zohomail.in
   ```

2. Restart your backend service

## Testing

### Local Testing

1. Start the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Submit a test enquiry through the contact form at `http://localhost:8000/contact.html`

3. Check the logs for:
   ```
   INFO: Enquiry notification email sent
   ```

4. Verify the email arrived at `contact.klyriven@zohomail.in`

### Production Testing

After deploying:

1. Visit your live website's contact page
2. Submit a test enquiry
3. Check `contact.klyriven@zohomail.in` for the notification email
4. Verify the formatting and all details are present

## Troubleshooting

### Email Not Sending

**Check logs for errors:**
- SMTP authentication errors → Verify EMAIL_USERNAME and EMAIL_PASSWORD
- Connection timeout → Check EMAIL_HOST and EMAIL_PORT
- "Email notifications disabled" → Set EMAIL_ENABLED=true

**Common Issues:**

1. **Invalid credentials**
   - Make sure you're using an app password, not your main Zoho account password
   - Verify the email address matches your Zoho account

2. **SMTP connection refused**
   - Zoho SMTP server: `smtp.zoho.in`
   - Port: `587` (TLS/STARTTLS)
   - Ensure your server can make outbound connections on port 587

3. **Emails going to spam**
   - The emails should have proper headers set
   - Check your Zoho Mail spam folder
   - Verify SPF/DKIM records for your domain (if using custom domain)

### Disabling Email Notifications

To temporarily disable emails without removing configuration:

```bash
EMAIL_ENABLED=false
```

## Email Template Customization

The email template is defined in `app/services/email_service.py` in the `_format_enquiry_email()` function.

To modify the email design:
1. Edit the HTML template in that function
2. Test locally first
3. Deploy changes

## Security Notes

- ✅ Email credentials are stored in environment variables, not in code
- ✅ The `.env` file is git-ignored to prevent credential leaks
- ✅ Email sending is non-blocking (fire-and-forget) to not delay API responses
- ✅ Email failures are logged but don't prevent enquiry submission
- ✅ Reply-To header is set to the client's email for easy responses

## Features

- **Async sending**: Emails are sent asynchronously without blocking the enquiry submission
- **HTML formatting**: Beautiful, responsive email template with brand colors
- **Plain text fallback**: Includes plain text version for email clients that don't support HTML
- **Error handling**: Email failures are logged but don't prevent enquiry persistence
- **Detailed logging**: All email operations are logged for monitoring
- **Reply-To header**: Easy to reply directly to the client from the notification email
