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
    """Authenticate and return a (gspread_client, error_string) tuple.

    Supports two secrets formats (tries GCP_JSON first, then gcp_service_account block):

    Option A — paste the whole JSON file as one string (recommended, avoids key issues):
        GCP_JSON = '{ "type": "service_account", "private_key": "-----BEGIN PRIVATE KEY-----\\n..." }'

    Option B — individual TOML fields:
        [gcp_service_account]
        type = "service_account"
        private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
        ...
    """
    try:
        import json
        import gspread
        from google.oauth2.service_account import Credentials
        import streamlit as st

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds_dict = None

        # ── Option A: full JSON string (most reliable) ─────────────────────────
        try:
            raw_json = str(st.secrets.get("GCP_JSON", "")).strip()
            if raw_json:
                creds_dict = json.loads(raw_json)
        except Exception:
            creds_dict = None

        # ── Option B: individual TOML fields ───────────────────────────────────
        if not creds_dict:
            try:
                creds_raw = st.secrets["gcp_service_account"]
                creds_dict = dict(creds_raw)
                # Fix mangled private key newlines (common TOML copy-paste issue)
                if "private_key" in creds_dict:
                    key = creds_dict["private_key"]
                    # Replace literal \n (2 chars) with real newline
                    key = key.replace("\\n", "\n")
                    # Ensure PEM header/footer are on their own lines
                    key = key.replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n").replace(
                          "-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----")
                    # Collapse any double newlines introduced above
                    import re
                    key = re.sub(r"\n{3,}", "\n", key)
                    creds_dict["private_key"] = key
            except KeyError:
                return None, (
                    "No credentials found. Add either:\n"
                    "  GCP_JSON = '{...}'  (paste the full JSON file as a string)\n"
                    "or a [gcp_service_account] block — see the Google Sheets tab for instructions."
                )
            except Exception as e:
                return None, f"Could not read gcp_service_account secret: {e}"

        if not creds_dict:
            return None, "Credentials are empty after parsing."

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


def upload_pdf_to_drive(pdf_bytes: bytes, filename: str) -> tuple[bool, str]:
    """
    Upload a PDF to Google Drive using the service account credentials.

    Optionally place it in a specific folder by adding to Streamlit secrets:
        DRIVE_FOLDER_ID = "your-google-drive-folder-id"

    The folder ID is the last segment of the folder's URL:
        https://drive.google.com/drive/folders/<DRIVE_FOLDER_ID>

    The service account must have Edit access to that folder.
    If DRIVE_FOLDER_ID is not set, the file is saved to the service account's root Drive.

    Returns (success: bool, error_message: str).
    """
    try:
        import json, requests as req
        import streamlit as st
        from google.oauth2.service_account import Credentials
        from google.auth.transport.requests import Request as GoogleRequest

        # ── Rebuild credentials (same logic as _get_client) ───────────────────
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds_dict = None
        try:
            raw_json = str(st.secrets.get("GCP_JSON", "")).strip()
            if raw_json:
                creds_dict = json.loads(raw_json)
        except Exception:
            creds_dict = None

        if not creds_dict:
            try:
                import re
                creds_raw = st.secrets["gcp_service_account"]
                creds_dict = dict(creds_raw)
                if "private_key" in creds_dict:
                    k = creds_dict["private_key"].replace("\\n", "\n")
                    k = k.replace("-----BEGIN PRIVATE KEY-----",
                                  "-----BEGIN PRIVATE KEY-----\n")
                    k = k.replace("-----END PRIVATE KEY-----",
                                  "\n-----END PRIVATE KEY-----")
                    k = re.sub(r"\n{3,}", "\n", k)
                    creds_dict["private_key"] = k
            except KeyError:
                return False, "No GCP credentials configured."
            except Exception as e:
                return False, f"Credential read error: {e}"

        if not creds_dict:
            return False, "Credentials are empty."

        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        creds.refresh(GoogleRequest())

        # ── Optional target folder ─────────────────────────────────────────────
        folder_id = str(st.secrets.get("DRIVE_FOLDER_ID", "")).strip()

        # ── Multipart upload to Drive v3 API ───────────────────────────────────
        metadata = {"name": filename}
        if folder_id:
            metadata["parents"] = [folder_id]

        boundary = "meridian_pdf_boundary"
        meta_part = (
            f"--{boundary}\r\n"
            "Content-Type: application/json; charset=UTF-8\r\n\r\n"
            f"{json.dumps(metadata)}\r\n"
        ).encode("utf-8")
        data_part = (
            f"--{boundary}\r\n"
            "Content-Type: application/pdf\r\n\r\n"
        ).encode("utf-8") + pdf_bytes + f"\r\n--{boundary}--".encode("utf-8")

        response = req.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers={
                "Authorization": f"Bearer {creds.token}",
                "Content-Type": f"multipart/related; boundary={boundary}",
            },
            data=meta_part + data_part,
            timeout=30,
        )
        response.raise_for_status()
        file_id = response.json().get("id", "unknown")
        return True, file_id

    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
