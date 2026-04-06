# Digital Readiness Self-Assessment App

A Streamlit web application for conducting digital maturity assessments across
**Sole Traders**, **Small Businesses**, and **Medium Businesses** in Australian
professional services.

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
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## Deploying to Streamlit Community Cloud (Free — recommended)

This is the closest experience to Vercel: connect a GitHub repo and it deploys automatically.

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit — Digital Readiness App"
git remote add origin https://github.com/YOUR_USERNAME/digital-readiness-app.git
git push -u origin main
```

### Step 2 — Deploy
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
2. Click **New app**
3. Select your repository, branch (`main`), and set the main file to `app.py`
4. Click **Deploy** — it will be live in ~2 minutes at a URL like:
   `https://digital-readiness-yourname.streamlit.app`

### Step 3 — Share
Send the URL to clients. They open it in any browser — no installation needed.

---

## Deploying to Other Platforms

### Railway / Render (also free tiers)
Add a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Fly.io
Add a `fly.toml` and `Dockerfile` (ask your developer or use the Fly CLI).

---

## Project Structure

```
digital-readiness-app/
├── app.py              ← Main Streamlit app (UI + routing)
├── data.py             ← All assessment content (questions, rubrics, actions)
├── pdf_report.py       ← PDF report generator (ReportLab + Matplotlib)
├── requirements.txt    ← Python dependencies
├── .streamlit/
│   └── config.toml     ← Theme and server settings
└── README.md           ← This file
```

---

## Customisation

### Add your branding
- Edit the header in `app.py` → `render_header()` to include your business name/logo
- Update colours in `.streamlit/config.toml`
- Edit the footer text in `pdf_report.py` → `_draw_header_footer()`

### Add your contact details to the PDF
In `pdf_report.py`, find the **Page 4** section and add your firm's details to the "Next Steps" paragraph.

### Modify questions
All questions are in `data.py` in the `PILLARS` list. Each pillar has `"st"`, `"sb"`, and `"mb"` keys for Sole Trader, Small Business, and Medium Business questions respectively.

---

## Dependencies

| Package     | Purpose                        |
|-------------|--------------------------------|
| streamlit   | Web app framework              |
| plotly      | Interactive radar chart        |
| pandas      | Results table display          |
| reportlab   | PDF report generation          |
| matplotlib  | Radar chart image for PDF      |
| numpy       | Radar chart maths              |

---

*Aligned to the Australian Government Digital First Framework, the ACSC Cyber Security Guidance, and the Office of the Australian Information Commissioner (OAIC) Privacy Act 1988 obligations.*
