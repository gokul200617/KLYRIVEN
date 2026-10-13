# 🔧 Production Email Troubleshooting

## Email Not Working in Production? Follow These Steps

### Step 1: Check Environment Variables

**On your hosting platform dashboard**, verify ALL these variables are set:

```bash
EMAIL_ENABLED=true
EMAIL_HOST=smtp.zoho.in
EMAIL_PORT=587
EMAIL_USERNAME=contact.klyriven@zohomail.in
EMAIL_PASSWORD=EPjYj9tUC628
EMAIL_FROM=contact.klyriven@zohomail.in
EMAIL_TO=contact.klyriven@zohomail.in
```

#### Common Mistakes:
- ❌ `EMAIL_ENABLED=false` → Should be `true`
- ❌ `EMAIL_PASSWORD=<EPjYj9tUC628>` → Remove the `< >` brackets
- ❌ Extra spaces: `EMAIL_PASSWORD= EPjYj9tUC628` → No space after `=`
- ❌ Wrong quotes: `EMAIL_HOST="smtp.zoho.in"` → Remove quotes (depends on platform)

### Step 2: Restart Your Service

After setting environment variables:
1. **Deploy** the latest code from GitHub (commit `f8a320a`)
2. **Restart** the backend service completely
3. Wait for restart to complete

### Step 3: Check Backend Logs

Look for these in your production logs:

#### ✅ Success:
```
INFO: New enquiry created
INFO: Enquiry notification email sent
```

#### ❌ Common Errors:

**"Email notifications disabled"**
```
WARNING: Email notifications disabled (EMAIL_ENABLED=false)
```
→ Set `EMAIL_ENABLED=true`

**"Email credentials missing"**
```
ERROR: Email credentials not configured
```
→ Set `EMAIL_USERNAME` and `EMAIL_PASSWORD`

**"SMTP Authentication Error"**
```
ERROR: SMTP authentication failed
```
→ Check the password is `EPjYj9tUC628` (no brackets, no spaces)

**"Connection refused"**
```
ERROR: Error connecting to smtp.zoho.in on port 587
```
→ Your hosting provider may block SMTP. See Step 5 below.

### Step 4: Run Diagnostic Script

Upload `diagnose_production.py` to your server and run:

```bash
python diagnose_production.py
```

This will:
- ✅ Check all environment variables
- ✅ Test network connectivity to Zoho SMTP
- ✅ Verify required packages are installed
- ✅ Attempt to send a test email

### Step 5: Check SMTP Port Access

Some hosting providers (Render, Railway, etc.) **block outbound SMTP ports** for security.

#### Test:
```bash
python diagnose_production.py
```

If you see:
```
❌ Cannot connect to smtp.zoho.in:587
   Your server may be blocking outbound SMTP connections
```

#### Solutions:

**Option A: Use Render/Railway SMTP Add-on**
- Some platforms have built-in email services
- Check your hosting docs for email services

**Option B: Use SendGrid/Mailgun Instead**
- Free tier available
- Most hosting providers allow these
- Requires code changes

**Option C: Contact Hosting Support**
- Ask them to enable SMTP on port 587
- Mention you need it for transactional emails

**Option D: Use Port 465 (SSL)**
Try changing:
```bash
EMAIL_PORT=465
```
And update the code to use `use_tls=True` instead of `start_tls=True`

### Step 6: Verify Dependencies

Make sure `requirements.txt` was installed:

```bash
pip list | grep aiosmtplib
```

Should show:
```
aiosmtplib    5.1.3
```

If missing:
```bash
pip install -r requirements.txt
```

### Step 7: Test from Production

1. Go to your live website: `https://your-domain.com/contact.html`
2. Fill out the form completely
3. Submit
4. Check backend logs immediately
5. Check `contact.klyriven@zohomail.in` inbox

---

## Platform-Specific Guides

### Render

1. Dashboard → Your Web Service
2. Environment → Add Environment Variables
3. Paste each variable (no quotes needed)
4. Click "Save Changes"
5. Service will auto-restart

**SMTP Access**: Render blocks port 25 but **allows 587** ✅

### Railway

1. Project → Variables tab
2. Click "+ New Variable"
3. Add each variable
4. Click "Deploy"

**SMTP Access**: Railway **may block SMTP** ❌
- Solution: Use Railway's email plugin or SendGrid

### Heroku

1. Settings → Config Vars
2. Click "Reveal Config Vars"
3. Add each variable
4. Restart dynos: `heroku restart -a your-app`

**SMTP Access**: Heroku allows port 587 ✅

### Vercel/Netlify

⚠️ These are **frontend-only** platforms.
Your backend must be hosted elsewhere (Render, Railway, etc.)

---

## Quick Checklist

Use this checklist to verify everything:

- [ ] Latest code deployed (commit `f8a320a` or later)
- [ ] `EMAIL_ENABLED=true` (not false)
- [ ] `EMAIL_PASSWORD=EPjYj9tUC628` (no brackets, no spaces)
- [ ] All 7 EMAIL_* variables set
- [ ] Backend service restarted
- [ ] Dependencies installed (`aiosmtplib` available)
- [ ] Port 587 accessible (run diagnostic script)
- [ ] Backend logs show no errors
- [ ] Test submission attempted

---

## Still Not Working?

### Get Detailed Logs

1. Run diagnostic script: `python diagnose_production.py`
2. Submit a test enquiry
3. Copy the full error from logs
4. Check which specific step is failing

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Environment variable not found" | Set all variables in hosting dashboard |
| "Module 'aiosmtplib' not found" | Run `pip install -r requirements.txt` |
| "Connection timeout" | SMTP port blocked - contact hosting support |
| "Authentication failed" | Wrong password - use `EPjYj9tUC628` |
| "Email disabled" | Set `EMAIL_ENABLED=true` |
| Works locally, not production | Environment variables not set in production |

---

## Alternative: SendGrid (If SMTP is Blocked)

If your hosting blocks SMTP completely, switch to SendGrid:

1. Sign up: https://sendgrid.com (free tier: 100 emails/day)
2. Get API key
3. Install: `pip install sendgrid`
4. Set environment variable: `SENDGRID_API_KEY=your-key`
5. I can update the code to use SendGrid instead

Let me know if you need this solution!

---

## Need More Help?

**Share these details:**
1. Your hosting platform (Render/Railway/Heroku/etc.)
2. Output from `python diagnose_production.py`
3. Error messages from backend logs
4. Which environment variables are set

This will help identify the exact issue quickly.
