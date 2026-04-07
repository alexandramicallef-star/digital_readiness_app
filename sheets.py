"""
sheets.py — Google Sheets integration for Meridian Digital Advisory
Appends one row per completed assessment to a nominated Google Sheet.

Setup (one-time):
  1. Create a Google Cloud project and enable Sheets + Drive APIs.
  2. Create a Service Account and download the JSON key file.
  3. Share your target Google Sheet with the service account email
     (the email looks like xxx@project.iam.gserviceaccount.com).
  4. Add credentials to .streamlit/secrets.toml (local) or Streamlit Cloud
     Secrets (deployed) — see README for exact format.
  5. Add SHEET_ID = "your-sheet-id" to secrets as well.

The sheet ID is the long string in your Sheet's URL:
  https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit
"""

import traceback

# ── Column headers (row 1 of the Sheet) ────────────────────────────────────────
HEADERS = [
    "Timestamp",
    "First Name", "Surname", "Business", "Email",
    "Business Size", "Industry", "Service / Product", "Business Age",
    "Avg Score", "Total Score", "Maturity Level",
    # Pillar averages
    "P1 Strategy & Leadership",
    "P2 Data Management",
    "P3 Technology & Tools",
    "P4 Processes & Automation",
    "P5 People & Capability",
    "P6 Client Experience",
    "P7 Security & Compliance",
    # Per-question scores  (pillar × question)
    "Q1.1", "Q1.2", "Q1.3", "Q1.4",
    "Q2.1", "Q2.2", "Q2.3", "Q2.4",
    "Q3.1", "Q3.2", "Q3.3", "Q3.4",
    "Q4.1", "Q4.2", "Q4.3", "Q4.4",
    "Q5.1", "Q5.2", "Q5.3", "Q5.4",
    "Q6.1", "Q6.2", "Q6.3", "Q6.4",
    "Q7.1", "Q7.2", "Q7.3", "Q7.4",
]


def _get_client():
    """Authenticate and return a (gspread_client, error_string) tuple."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        import streamlit as st

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # Validate the secret exists
        try:
            creds_raw = st.secrets["gcp_service_account"]
        except KeyError:
            return None, "Secret 'gcp_service_account' not found in Streamlit secrets."
        except Exception as e:
            return None, f"Could not read secrets: {e}"

        creds_dict = dict(creds_raw)

        # Common issue: private_key newlines need to be actual \n chars
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        gc = gspread.authorize(creds)
        return gc, None

    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _get_sheet(gc, sheet_id: str, tab_name: str = "Assessments"):
    """Open (or create) the named worksheet inside the spreadsheet."""
    import gspread
    spreadsheet = gc.open_by_key(sheet_id)
    try:
        ws = spreadsheet.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=tab_name, rows=1000, cols=len(HEADERS))
    return ws


def _ensure_headers(ws):
    """Write the header row if the sheet is empty."""
    existing = ws.row_values(1)
    if not existing or existing[0] != "Timestamp":
        ws.insert_row(HEADERS, index=1)


def test_connection() -> tuple[bool, str]:
    """
    Verify that Google Sheets credentials and SHEET_ID are configured correctly.
    Returns (success: bool, message: str).
    Call this from the admin panel to diagnose setup issues.
    """
    try:
        import streamlit as st

        # 1. Check SHEET_ID
        try:
            sheet_id = str(st.secrets.get("SHEET_ID", "")).strip()
        except Exception as e:
            return False, f"Cannot read SHEET_ID from secrets: {e}"

        if not sheet_id:
            return False, (
                "SHEET_ID is not set in Streamlit secrets.\n"
                "Add: SHEET_ID = \"your-google-sheet-id\""
            )

        # 2. Check credentials
        gc, err = _get_client()
        if gc is None:
            return False, f"Authentication failed: {err}"

        # 3. Try opening the sheet
        try:
            import gspread
            spreadsheet = gc.open_by_key(sheet_id)
            title = spreadsheet.title
        except gspread.SpreadsheetNotFound:
            return False, (
                f"Spreadsheet not found (ID: {sheet_id[:20]}…).\n"
                "Make sure the Sheet is shared with the service account email."
            )
        except Exception as e:
            return False, f"Could not open spreadsheet: {type(e).__name__}: {e}"

        # 4. Check/get the Assessments tab
        try:
            ws = _get_sheet(gc, sheet_id)
            row_count = len(ws.get_all_values())
        except Exception as e:
            return False, f"Could not access worksheet: {e}"

        return True, (
            f"✅ Connected to \"{title}\"\n"
            f"Worksheet: Assessments  |  Rows (incl. header): {row_count}"
        )

    except Exception as e:
        return False, f"Unexpected error: {traceback.format_exc()}"


def append_to_sheet(client_info: dict, results: dict,
                    raw_scores: dict | None = None) -> tuple[bool, str]:
    """
    Append one row of assessment data to the Google Sheet.
    Returns (success: bool, error_message: str).
    """
    try:
        import streamlit as st

        # Check SHEET_ID
        try:
            sheet_id = str(st.secrets.get("SHEET_ID", "")).strip()
        except Exception:
            sheet_id = ""

        if not sheet_id:
            return False, "SHEET_ID not configured — skipping Sheets write."

        gc, err = _get_client()
        if gc is None:
            return False, f"Auth failed: {err}"

        ws = _get_sheet(gc, sheet_id)
        _ensure_headers(ws)

        # ── Build the row ─────────────────────────────────────────────────────
        from datetime import datetime
        pa = results.get("pillar_avgs", {})

        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            client_info.get("name", ""),
            client_info.get("surname", ""),
            client_info.get("business", ""),
            client_info.get("email", ""),
            client_info.get("size", ""),
            client_info.get("industry", ""),
            client_info.get("service_product", ""),
            client_info.get("business_age", ""),
            round(results.get("avg_score", 0), 2),
            results.get("total_score", 0),
            results.get("maturity", {}).get("label", ""),
            # Pillar avgs
            round(pa.get(1, 0), 2),
            round(pa.get(2, 0), 2),
            round(pa.get(3, 0), 2),
            round(pa.get(4, 0), 2),
            round(pa.get(5, 0), 2),
            round(pa.get(6, 0), 2),
            round(pa.get(7, 0), 2),
        ]

        # Individual question scores — 7 pillars × 4 questions
        for pid in range(1, 8):
            pillar_scores = (raw_scores or {}).get(pid, [None, None, None, None])
            for qi in range(4):
                val = pillar_scores[qi] if qi < len(pillar_scores) else ""
                row.append(val if val is not None else "")

        ws.append_row(row, value_input_option="USER_ENTERED")
        return True, ""

    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
