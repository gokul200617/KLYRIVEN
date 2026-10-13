# Quick Start: Email Notifications

## Step 1: Get Your Zoho App Password

1. Open your browser and go to: **https://mail.zoho.in**
2. Login with: `contact.klyriven@zohomail.in`
3. Click on the **gear icon** (Settings) in the top right
4. Go to: **Security** → **App Passwords**
5. Click **Generate New Password**
6. Enter name: `KLYRIVEN Backend`
7. **Copy the password** (you won't see it again!)

## Step 2: Configure Your Local Environment

1. Open the file: `backend/.env`
2. Find this line:
   ```
   EMAIL_PASSWORD=PASTE_YOUR_ZOHO_APP_PASSWORD_HERE
   ```
3. Replace `PASTE_YOUR_ZOHO_APP_PASSWORD_HERE` with the password from Step 1
4. Save the file

Your `.env` should look like:
```bash
EMAIL_ENABLED=true
EMAIL_HOST=smtp.zoho.in
EMAIL_PORT=587
EMAIL_USERNAME=contact.klyriven@zohomail.in
EMAIL_PASSWORD=abcd1234efgh5678ijkl
EMAIL_FROM=contact.klyriven@zohomail.in
EMAIL_TO=contact.klyriven@zohomail.in
```

## Step 3: Test Locally

```bash
cd backend
python test_email.py
```

You should see:
```
✅ SUCCESS! Email sent successfully!
   Check contact.klyriven@zohomail.in for the test email
```

If you see errors, the script will tell you what's wrong.

## Step 4: Configure Production

For your production server (Render, Railway, Heroku, etc.):

1. Go to your hosting dashboard
2. Find **Environment Variables** settings
3. Add these variables:

```
EMAIL_ENABLED=true
EMAIL_HOST=smtp.zoho.in
EMAIL_PORT=587
EMAIL_USERNAME=contact.klyriven@zohomail.in
EMAIL_PASSWORD=<your-app-password-from-step-1>
EMAIL_FROM=contact.klyriven@zohomail.in
EMAIL_TO=contact.klyriven@zohomail.in
```

4. **Restart** your backend service

## Step 5: Test Production

1. Go to your live website's contact page
2. Fill out and submit the form
3. Check `contact.klyriven@zohomail.in` inbox
4. You should receive an email within seconds!

## Troubleshooting

### "Email notifications disabled"
- Make sure `EMAIL_ENABLED=true` (not `false`)

### "Email credentials missing"
- Check that `EMAIL_PASSWORD` is set in `.env` or environment variables
- Make sure there are no extra spaces

### "SMTP Authentication Error"
- You're using your regular password instead of an app password
- Go back to Step 1 and generate an app password
- App passwords are different from your login password!

### "Connection refused" or timeout
- Check if your server can make outbound connections on port 587
- Some hosting providers block SMTP ports
- Try using port 465 with SSL instead (change `EMAIL_PORT=465`)

### Email goes to spam
- Check your spam folder
- This is normal for first few emails
- Mark as "Not Spam" to train the filter

## Quick Debug Commands

Check if settings are loaded:
```bash
cd backend
python -c "from app.core.config import settings; print('Enabled:', settings.EMAIL_ENABLED); print('Password set:', bool(settings.EMAIL_PASSWORD))"
```

Test email sending:
```bash
cd backend
python test_email.py
```

## Production Checklist

- [ ] Generate Zoho app password
- [ ] Set all EMAIL_* environment variables on production
- [ ] Restart backend service
- [ ] Test by submitting a form
- [ ] Check inbox for notification
- [ ] Verify all details appear correctly
- [ ] Test Reply-To by replying to the email

---

**Need Help?**

1. Run `python test_email.py` - it will tell you exactly what's wrong
2. Check the backend logs for error messages
3. Make sure you're using an **app password**, not your regular password
