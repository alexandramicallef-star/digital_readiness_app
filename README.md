# Digital Readiness Self-Assessment App
### Meridian Digital Advisory

A Streamlit web application for conducting digital maturity assessments across
**Sole Traders**, **Small Businesses** (2–19 employees), and **Medium Businesses** (20–199 employees)
in Australian professional services.

Aligned to the Australian Government Digital First Framework and ACSC guidance.

---

## Running Locally

```bash
# 1. Clone or copy this folder to your machine
# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python -m streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

> **Windows tip:** If `streamlit` is not recognised, always use `python -m streamlit run app.py`

---

## Project Structure

```
digital-readiness-app/
├── app.py                ← Main Streamlit app (UI, routing, admin page)
├── data.py               ← All assessment content (questions, rubrics, actions)
├── database.py           ← SQLite CRM — tokens + assessment records
├── pdf_report.py         ← PDF report generator (ReportLab + Matplotlib)
├── requirements.txt      ← Python dependencies
├── images/
│   └── meridian-logoV3.jpg   ← Meridian logo (used in app header + PDF)
├── .streamlit/
│   ├── config.toml       ← Theme and server settings
│   └── secrets.toml      ← Admin password + feature flags (never commit!)
└── README.md             ← This file
```

---

## Configuration — secrets.toml

Before running, make sure `.streamlit/secrets.toml` exists (already included).
Edit the values to suit your deployment:

```toml
# Admin dashboard password
ADMIN_PASSWORD = "meridian2024"

# Base URL for generating invite links
# Change to your live URL when deployed
BASE_URL = "http://localhost:8501"

# Set to "true" to require an invite token to access the assessment
# Set to "false" for open access (good for testing)
REQUIRE_TOKEN = "false"
```

> **Security note:** Add `.streamlit/secrets.toml` to your `.gitignore` before pushing to GitHub.

---

## Admin Dashboard

Access the admin panel by navigating to:

```
http://localhost:8501/?admin=true
```

You will be prompted for the admin password (set in `secrets.toml`).

### Admin tabs

**1 · Generate Invites**
- Enter a client's name, email, and optional notes
- Click **Generate Invite Link** — a unique single-use URL is created
- Copy the link and send it to your client (e.g. via email)
- Example link: `http://localhost:8501/?token=abc123xyz`

**2 · Assessment Records**
- View all completed assessments with timestamps
- See client name, business, score, maturity level, and per-pillar averages

**3 · Manage Tokens**
- View all generated invite tokens (used and unused)
- Delete unused tokens if a client no longer needs access

### Token workflow

```
Admin generates token  →  Client receives personalised link
       ↓
Client opens link  →  Name/email pre-filled  →  Completes assessment
       ↓
Results saved to DB (assessments.db)  →  Token marked as used
       ↓
Admin reviews results in Assessment Records tab
```

- Each token is **single-use** — it cannot be shared or reused after completion
- If `REQUIRE_TOKEN = "true"`, the assessment is completely inaccessible without a valid token
- The admin page URL (`?admin=true`) is not linked from the public-facing app

---

## Deploying to Streamlit Community Cloud (Free — recommended)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit — Digital Readiness App"
git remote add origin https://github.com/YOUR_USERNAME/digital-readiness-app.git
git push -u origin main
```

> Add `assessments.db` and `.streamlit/secrets.toml` to `.gitignore`

### Step 2 — Add secrets in Streamlit Cloud
In your Streamlit Cloud app settings → **Secrets**, paste:
```toml
ADMIN_PASSWORD = "your-secure-password"
BASE_URL = "https://your-app-name.streamlit.app"
REQUIRE_TOKEN = "true"
```

### Step 3 — Deploy
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
2. Click **New app**
3. Select your repository, branch (`main`), and set the main file to `app.py`
4. Click **Deploy** — live in ~2 minutes

---

## Customisation

- **Logo:** replace `images/meridian-logoV3.jpg` with your own (keep the same filename, or update `LOGO_PATH` in `app.py`)
- **Colours:** edit `.streamlit/config.toml`
- **Footer text:** edit `pdf_report.py` → `_draw_header_footer()`
- **Questions:** edit `data.py` → `PILLARS` list (`"st"`, `"sb"`, `"mb"` keys per business tier)
- **Admin password:** update `ADMIN_PASSWORD` in `.streamlit/secrets.toml`

---

## Dependencies

| Package     | Purpose                              |
|-------------|--------------------------------------|
| streamlit   | Web app framework                    |
| plotly      | Interactive radar chart              |
| pandas      | Results table display                |
| reportlab   | PDF report generation                |
| matplotlib  | Radar chart image for PDF            |
| numpy       | Radar chart maths                    |

*(sqlite3 is part of the Python standard library — no install needed)*

---

*Aligned to the Australian Government Digital First Framework, the ACSC Cyber Security Guidance, and the Office of the Australian Information Commissioner (OAIC) Privacy Act 1988 obligations.*
