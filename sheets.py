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

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds_dict, err = _get_creds_dict()
        if creds_dict is None:
            return None, err or "Credentials are empty."

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


def test_drive_connection() -> tuple[bool, str]:
    """
    Verify that Google Drive credentials are configured and the Drive API is reachable.
    Checks that DRIVE_FOLDER_ID is set and accessible.
    Returns (success: bool, message: str).
    """
    try:
        import streamlit as st
        from google.oauth2.service_account import Credentials
        from google.auth.transport.requests import AuthorizedSession

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # 1. Parse credentials
        creds_dict, err = _get_creds_dict()
        if creds_dict is None:
            return False, f"Authentication failed: {err}"

        creds   = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        session = AuthorizedSession(creds)

        # 2. Hit the Drive API — lightweight list call to prove connectivity
        resp = session.get(
            "https://www.googleapis.com/drive/v3/files"
            "?pageSize=1&supportsAllDrives=true&includeItemsFromAllDrives=true",
            timeout=15,
        )
        if resp.status_code == 403:
            return False, (
                "Drive API returned 403 Forbidden.\n"
                "Make sure the Google Drive API is enabled in your Google Cloud project."
            )
        if resp.status_code != 200:
            return False, f"Drive API returned HTTP {resp.status_code}: {resp.text[:300]}"

        # 3. Check DRIVE_FOLDER_ID
        folder_id = str(st.secrets.get("DRIVE_FOLDER_ID", "")).strip()
        if not folder_id:
            svc_email = creds_dict.get("client_email", "unknown")
            return False, (
                "Drive API is reachable ✅ — but DRIVE_FOLDER_ID is NOT set in secrets.\n"
                f"Service account: {svc_email}\n\n"
                "Without DRIVE_FOLDER_ID, PDFs will be uploaded to the service account's "
                "private Drive — not visible in your Google Drive.\n"
                "Fix: create a Drive folder, share it (Editor) with the service account, "
                "then add DRIVE_FOLDER_ID = \"...\" to Streamlit secrets."
            )

        # 4. Verify the folder — request driveId to detect My Drive vs Shared Drive
        fr = session.get(
            f"https://www.googleapis.com/drive/v3/files/{folder_id}"
            "?fields=name,mimeType,capabilities,driveId"
            "&supportsAllDrives=true",
            timeout=15,
        )
        if fr.status_code == 404:
            return False, (
                f"DRIVE_FOLDER_ID '{folder_id[:20]}…' not found.\n"
                "Share the folder (Editor) with the service account email."
            )
        if fr.status_code == 403:
            return False, (
                f"DRIVE_FOLDER_ID '{folder_id[:20]}…' returned 403 — "
                "service account does not have access. "
                "Share the folder (Editor) with the service account email."
            )
        if fr.status_code != 200:
            return False, f"Folder check returned HTTP {fr.status_code}: {fr.text[:200]}"

        folder_info = fr.json()
        folder_name = folder_info.get("name", folder_id)
        drive_id    = folder_info.get("driveId")          # only present on Shared Drives
        can_edit    = folder_info.get("capabilities", {}).get("canEdit", None)

        # ── Critical check: My Drive folders will always fail with a quota error ─
        if not drive_id:
            svc_email = creds_dict.get("client_email", "unknown")
            return False, (
                f"⛔ Folder \"{folder_name}\" is on a regular My Drive — uploads WILL fail.\n\n"
                "Service accounts have no storage quota on personal My Drive folders.\n"
                "You must use a Shared Drive (formerly Team Drive) instead.\n\n"
                "How to fix:\n"
                "  1. In Google Drive, click '+ New' → 'Shared Drive' to create one\n"
                "     (requires Google Workspace — available on free @gmail.com via Google One)\n"
                "  2. Inside the Shared Drive, right-click → 'Manage members'\n"
                f"  3. Add {svc_email} as a 'Contributor' or 'Content Manager'\n"
                "  4. Copy the Shared Drive's folder ID from its URL and update\n"
                "     DRIVE_FOLDER_ID in Streamlit secrets"
            )

        perm_note = "" if can_edit is None else (" ✅ write access confirmed" if can_edit else " ⚠️ read-only!")
        svc_email = creds_dict.get("client_email", "unknown")
        return True, (
            f"✅ Google Drive API connected — Shared Drive folder verified.\n"
            f"Folder: \"{folder_name}\"{perm_note}\n"
            f"Service account: {svc_email}"
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


def _get_creds_dict() -> tuple[dict | None, str]:
    """Parse GCP credentials from Streamlit secrets. Returns (dict, error_str)."""
    import json, re
    import streamlit as st

    # Option A: full JSON string
    try:
        raw_json = str(st.secrets.get("GCP_JSON", "")).strip()
        if raw_json:
            return json.loads(raw_json), ""
    except Exception as e:
        return None, f"GCP_JSON parse error: {e}"

    # Option B: individual TOML fields
    try:
        creds_raw = st.secrets["gcp_service_account"]
        creds_dict = dict(creds_raw)
        if "private_key" in creds_dict:
            k = creds_dict["private_key"].replace("\\n", "\n")
            k = k.replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n")
            k = k.replace("-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----")
            k = re.sub(r"\n{3,}", "\n", k)
            creds_dict["private_key"] = k
        return creds_dict, ""
    except KeyError:
        return None, "No GCP credentials found (neither GCP_JSON nor [gcp_service_account])."
    except Exception as e:
        return None, f"Credential read error: {e}"


def upload_pdf_to_drive(pdf_bytes: bytes, filename: str) -> tuple[bool, str]:
    """
    Upload a PDF to Google Drive using the service account credentials.

    Set DRIVE_FOLDER_ID in Streamlit secrets to save into a specific folder.
    The folder ID is the last segment of the folder's URL:
        https://drive.google.com/drive/folders/<DRIVE_FOLDER_ID>

    The service account must have Editor access to that folder.
    If DRIVE_FOLDER_ID is not set, the file is saved to the service account's
    root Drive (not visible in your personal Google Drive).

    Returns (success: bool, file_id_or_error_message: str).
    """
    try:
        import json
        import streamlit as st
        from google.oauth2.service_account import Credentials
        from google.auth.transport.requests import AuthorizedSession

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds_dict, err = _get_creds_dict()
        if creds_dict is None:
            return False, err or "Credentials are empty."

        # AuthorizedSession handles token acquisition + refresh automatically
        creds   = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        session = AuthorizedSession(creds)

        # ── Optional target folder ─────────────────────────────────────────────
        folder_id = str(st.secrets.get("DRIVE_FOLDER_ID", "")).strip()

        metadata = {"name": filename}
        if folder_id:
            metadata["parents"] = [folder_id]
        else:
            return (
                False,
                "DRIVE_FOLDER_ID is not configured — file would go to the service "
                "account's private Drive (not visible to you). "
                "Add DRIVE_FOLDER_ID to Streamlit secrets.",
            )

        # ── Build multipart/related body ──────────────────────────────────────
        boundary  = "meridian_pdf_upload_boundary"
        meta_json = json.dumps(metadata).encode("utf-8")

        body = (
            f"--{boundary}\r\n"
            "Content-Type: application/json; charset=UTF-8\r\n\r\n"
        ).encode("utf-8") + meta_json + (
            f"\r\n--{boundary}\r\n"
            "Content-Type: application/pdf\r\n\r\n"
        ).encode("utf-8") + pdf_bytes + (
            f"\r\n--{boundary}--"
        ).encode("utf-8")

        # ── POST to Drive v3  (supportsAllDrives covers Shared / Team Drives) ─
        response = session.post(
            "https://www.googleapis.com/upload/drive/v3/files"
            "?uploadType=multipart&supportsAllDrives=true",
            headers={"Content-Type": f"multipart/related; boundary={boundary}"},
            data=body,
            timeout=60,
        )

        if response.status_code not in (200, 201):
            resp_text = response.text
            # Specific, actionable message for the most common service-account error
            if "storage quota" in resp_text or "do not have storage quota" in resp_text:
                svc_email = creds_dict.get("client_email", "unknown")
                return False, (
                    "Service accounts cannot upload to a regular My Drive folder — "
                    "they have no storage quota.\n\n"
                    "Fix: use a Shared Drive folder instead:\n"
                    "  1. In Google Drive → '+ New' → 'Shared Drive'\n"
                    "  2. Open the Shared Drive → 'Manage members' →\n"
                    f"     add {svc_email} as Contributor or Content Manager\n"
                    "  3. Copy the Shared Drive folder ID from its URL and set\n"
                    "     DRIVE_FOLDER_ID in Streamlit secrets\n\n"
                    "Run the Drive test in the Admin Dashboard to confirm the new folder."
                )
            return False, (
                f"Drive API returned HTTP {response.status_code}: "
                f"{resp_text[:400]}"
            )

        file_id = response.json().get("id", "unknown")
        return True, file_id

    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


# Minimal 1-page PDF (no content, valid structure) used by the test upload below
_TEST_PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 72 72]>>endobj\n"
    b"xref\n0 4\n"
    b"0000000000 65535 f \n"
    b"0000000009 00000 n \n"
    b"0000000058 00000 n \n"
    b"0000000115 00000 n \n"
    b"trailer<</Size 4/Root 1 0 R>>\n"
    b"startxref\n172\n%%EOF\n"
)


def test_drive_upload() -> tuple[bool, str]:
    """
    The ONLY reliable way to verify Drive uploads: actually create a small test
    file in the configured folder, confirm it landed, then delete it.

    Catches permission issues (e.g. storage-quota 403) that metadata-only
    checks cannot detect.

    Returns (success: bool, message: str).
    """
    try:
        import streamlit as st
        from google.oauth2.service_account import Credentials
        from google.auth.transport.requests import AuthorizedSession

        folder_id = str(st.secrets.get("DRIVE_FOLDER_ID", "")).strip()
        if not folder_id:
            return False, "DRIVE_FOLDER_ID is not set in Streamlit secrets."

        # ── 1. Attempt the upload using the exact same path as the real upload ─
        ok, result = upload_pdf_to_drive(_TEST_PDF_BYTES, "_meridian_connection_test.pdf")
        if not ok:
            return False, f"Upload failed:\n\n{result}"

        file_id = result   # on success, result is the created file's ID

        # ── 2. Immediately delete the test file ───────────────────────────────
        creds_dict, err = _get_creds_dict()
        cleanup_note = ""
        if creds_dict:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]
            creds   = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            session = AuthorizedSession(creds)
            del_resp = session.delete(
                f"https://www.googleapis.com/drive/v3/files/{file_id}"
                "?supportsAllDrives=true",
                timeout=15,
            )
            if del_resp.status_code == 204:
                cleanup_note = "Test file created and deleted automatically."
            else:
                cleanup_note = (
                    f"Test file created (ID: {file_id}) but auto-delete returned "
                    f"HTTP {del_resp.status_code} — delete it manually from the folder."
                )
        else:
            cleanup_note = f"Test file created (ID: {file_id}) — delete it manually."

        return True, (
            f"✅ Drive upload confirmed working!\n{cleanup_note}"
        )

    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
