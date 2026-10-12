# KLYRIVEN — Setup & Development Guide

Premium digital agency website with a FastAPI backend and Firebase Firestore database.

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.11+ | 3.12 recommended |
| Firebase project | — | Firestore must be enabled (see step 1) |
| PowerShell | 5.1+ | Pre-installed on Windows 10/11 |

---

## 1. Enable Firestore in Firebase Console

Before anything else, the Cloud Firestore API must be active in your Firebase project.

1. Go to [Firebase Console → Firestore](https://console.firebase.google.com/project/klyriven-effb8/firestore)
2. Click **Create database**
3. Choose **Production mode**
4. Select a region (e.g. `europe-west2` for UK, `us-central` for US)
5. Wait ~60 seconds for provisioning to complete

---

## 2. Place the Firebase Credentials File

The service account key file is **never committed to the repository**. Place it at:

```
backend/firebase-credentials.json
```

This file is already listed in `backend/.gitignore`. If you need to regenerate it:

1. Go to [Firebase Console → Project Settings → Service accounts](https://console.firebase.google.com/project/klyriven-effb8/settings/serviceaccounts/adminsdk)
2. Click **Generate new private key**
3. Save the downloaded JSON as `backend/firebase-credentials.json`

---

## 3. Configure Environment

```powershell
cd C:\Users\M354421\Desktop\KLYRIVEN\backend

Copy-Item .env.example .env
```

Edit `.env` with your values:

```ini
APP_ENV=development
APP_DEBUG=true
SECRET_KEY=generate-a-long-random-string-here

# Path to the service account JSON (relative to where you run uvicorn from)
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json

CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
RATE_LIMIT_ENQUIRIES=5/minute
```

**Never commit `.env` or `firebase-credentials.json`.**

---

## 4. Create a Virtual Environment and Install Dependencies

```powershell
cd C:\Users\M354421\Desktop\KLYRIVEN\backend

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# If execution policy blocks activation, run once:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
python -m pip install -r requirements.txt
```

---

## 5. Seed Portfolio Projects (optional)

Projects are stored as Firestore documents in the `projects` collection.
Each document ID is the project's `slug`.

You can add projects directly in the [Firebase Console → Firestore](https://console.firebase.google.com/project/klyriven-effb8/firestore)
or via the API once the server is running.

**Required fields for a project document:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "slug": "smart-evac-command",
  "name": "Smart Evac Command",
  "category": "Smart Systems & IoT",
  "summary": "Multi-floor smart evacuation system with real-time telemetry.",
  "description": "Full description here...",
  "image_urls": [],
  "published": true,
  "display_order": 1,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": null
}
```

---

## 6. Start the Application

The FastAPI backend serves both the API and the static frontend from a single process:

```powershell
# From backend/ with .venv active
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open: **http://localhost:8000**

---

## 7. Verify Everything is Working

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/api/health" | Select-Object -ExpandProperty Content

# Test enquiry submission
$body = @{
  name             = "Test User"
  email            = "test@example.com"
  company          = "Test Co"
  service_interest = "Website Design & Development"
  description      = "This is a test enquiry with enough characters to pass validation."
  consent_given    = $true
} | ConvertTo-Json

Invoke-WebRequest `
  -Uri "http://localhost:8000/api/enquiries" `
  -Method POST `
  -Body $body `
  -ContentType "application/json" | Select-Object -ExpandProperty Content

# List published projects
Invoke-WebRequest -Uri "http://localhost:8000/api/projects" | Select-Object -ExpandProperty Content
```

Expected health response:
```json
{"status":"ok","database":"connected","timestamp":"...","version":"2.0.0"}
```

---

## 8. Run the Test Suite

```powershell
# From backend/ with .venv active
python -m pytest tests/ -v
```

> **Note:** The existing test suite was written for PostgreSQL/SQLAlchemy. Tests will need to be updated to mock Firestore. Until then, run them to check for import and routing errors only.

---

## 9. Available Routes

### Frontend Pages

| URL | Page |
|-----|------|
| `http://localhost:8000/` | Home |
| `http://localhost:8000/portfolio.html` | Work / Portfolio |
| `http://localhost:8000/services.html` | Services |
| `http://localhost:8000/process.html` | Process |
| `http://localhost:8000/about.html` | About |
| `http://localhost:8000/contact.html` | Contact |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check with Firestore status |
| `POST` | `/api/enquiries` | Submit a project enquiry |
| `GET` | `/api/projects` | List published projects (filter: `?category=`) |
| `GET` | `/api/projects/{slug}` | Get a single published project by slug |

API docs (debug mode only): **http://localhost:8000/api/docs**

---

## 10. Firestore Collections

### `enquiries/{uuid}`

Automatically created when a visitor submits the contact form.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | UUID — matches the document ID |
| `name` | string | Submitter's name |
| `email` | string | Normalised to lowercase |
| `company` | string \| null | Optional |
| `service_interest` | string | One of the allowed service values |
| `estimated_budget` | string \| null | Optional budget bracket |
| `timeline` | string \| null | Optional delivery horizon |
| `description` | string | Project overview (20–5000 chars) |
| `consent_given` | boolean | Must be `true` |
| `status` | string | `"new"` on creation |
| `created_at` | timestamp | Set on write |
| `updated_at` | timestamp \| null | Set on subsequent edits |

### `projects/{slug}`

Managed manually in the Firebase Console or via a seed script.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | UUID |
| `slug` | string | URL-safe identifier — matches the document ID |
| `name` | string | Display name |
| `category` | string | e.g. `"Smart Systems & IoT"` |
| `summary` | string \| null | Short description for list views |
| `description` | string \| null | Full case-study copy |
| `image_urls` | string[] | Array of image URLs |
| `published` | boolean | Only `true` documents are returned by the API |
| `display_order` | integer | Lower = first in list |
| `created_at` | timestamp | |
| `updated_at` | timestamp \| null | |

---

## 11. Troubleshooting

### `PERMISSION_DENIED` / Firestore API disabled
Enable the API in the [Google Cloud Console](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=klyriven-effb8), then wait ~60 seconds and retry.

### `FileNotFoundError: firebase-credentials.json`
The credentials file is missing from `backend/`. See **Step 2** above.

### `ModuleNotFoundError`
Ensure your virtual environment is activated (`.venv\Scripts\Activate.ps1`) and dependencies are installed (`pip install -r requirements.txt`).

### `INVALID_ARGUMENT` on Firestore query
A compound query (e.g. filter + order by) may require a Firestore composite index. The error message includes a direct link to create it in the console — click the link and the index is created automatically.

### Port 8000 already in use
```powershell
netstat -ano | findstr :8000
Stop-Process -Id <PID>
```

---

## Project Structure

```
KLYRIVEN/
├── frontend/
│   ├── index.html              # Home — hero with architecture background
│   ├── portfolio.html          # Work / Portfolio
│   ├── services.html           # Services
│   ├── process.html            # Process
│   ├── about.html              # About
│   ├── contact.html            # Contact (phone: 871 210 9466)
│   ├── sitemap.xml
│   ├── robots.txt
│   ├── assets/
│   │   └── images/
│   │       └── hero-architecture.jpg   # Hero background image
│   ├── css/
│   │   ├── tokens.css          # Design system tokens (colours, type, spacing)
│   │   ├── base.css            # Reset and base typography
│   │   ├── layout.css          # Grid and containers
│   │   ├── components.css      # Navigation, buttons, cards, forms, footer
│   │   ├── pages.css           # Page-specific styles (hero, work grid, etc.)
│   │   └── responsive.css      # Breakpoint overrides
│   └── js/
│       ├── app.js              # Bootstrap and utilities
│       ├── navigation.js       # Scroll behaviour, mobile menu, active links
│       ├── animations.js       # IntersectionObserver reveals, hero entrance
│       ├── portfolio.js        # Project filtering and loading
│       ├── contact.js          # Form validation and submission
│       └── api.js              # API client (enquiry + project fetching)
└── backend/
    ├── .env                    # Local secrets — never commit
    ├── .env.example            # Configuration template
    ├── .gitignore
    ├── firebase-credentials.json   # Service account key — never commit
    ├── requirements.txt
    └── app/
        ├── main.py             # FastAPI app factory + Firebase lifespan
        ├── core/
        │   ├── config.py       # Settings (pydantic-settings)
        │   └── security.py     # Input sanitisation utilities
        ├── db/
        │   ├── firebase.py     # Firebase init + Firestore dependency
        │   ├── session.py      # Compatibility stub
        │   └── base.py         # Compatibility stub
        ├── models/
        │   ├── enquiry.py      # Enquiry dataclass (Firestore document)
        │   └── project.py      # Project dataclass (Firestore document)
        ├── schemas/
        │   ├── enquiry.py      # Pydantic v2 request/response schemas
        │   └── project.py      # Pydantic v2 request/response schemas
        ├── api/routes/
        │   ├── health.py       # GET /api/health
        │   ├── enquiries.py    # POST /api/enquiries
        │   └── projects.py     # GET /api/projects, GET /api/projects/{slug}
        ├── services/
        │   └── enquiry_service.py  # Duplicate check + Firestore write
        └── tests/
            ├── conftest.py
            ├── test_health.py
            ├── test_enquiries.py
            └── test_projects.py
```

---

## Security Notes

- `.env` and `firebase-credentials.json` are in `.gitignore` — never commit secrets
- CORS is restricted to configured origins only
- All form inputs validated server-side with Pydantic v2
- Enquiry submissions rate-limited to 5 per minute per IP (configurable)
- Duplicate submissions from the same email blocked within a 5-minute window
- Input sanitised (control characters stripped, Unicode normalised, length capped)
- Stack traces never exposed in production responses

---

## Production Deployment

1. Set `APP_ENV=production` and `APP_DEBUG=false` in `.env`
2. Generate a strong `SECRET_KEY` (`python -c "import secrets; print(secrets.token_hex(32))"`)
3. Restrict `CORS_ORIGINS` to your actual domain
4. Store `firebase-credentials.json` securely (environment secret or secret manager — not in the repo)
5. Use a reverse proxy (nginx / Caddy) with HTTPS
6. Use a process manager (systemd, Docker, or a PaaS like Railway / Render)
7. Set Firestore security rules to deny direct client access (all writes go through the API)
8. Configure log aggregation and uptime monitoring
