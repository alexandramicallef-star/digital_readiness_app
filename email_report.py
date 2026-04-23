"""
email_report.py — SMTP notification for Meridian Digital Advisory
Sends the completed PDF report to the configured notify address.

Setup (one-time) — add to .streamlit/secrets.toml (local) or Streamlit Cloud Secrets:

    SMTP_USER     = "info@meridiandigitaladvisory.com.au"
    SMTP_PASSWORD = "your-email-password"
    SMTP_HOST     = "meridiandigitaladvisory.sslsvc.com"
    SMTP_PORT     = 465
    NOTIFY_EMAIL  = "info@meridiandigitaladvisory.com.au"   # where reports are delivered

SMTP_HOST and SMTP_PORT default to the Meridian hosting server if not set.
NOTIFY_EMAIL defaults to SMTP_USER if not set.
"""

import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ── Internal helpers ──────────────────────────────────────────────────────────

def _get_email_config() -> tuple[str, str, str, str, str, int]:
    """Return (user, password, notify_email, host, port, error).
    error is '' on success, message string on failure.
    """
    try:
        import streamlit as st
        user   = str(st.secrets.get("SMTP_USER",     "")).strip()
        pw     = str(st.secrets.get("SMTP_PASSWORD", "")).strip()
        notify = str(st.secrets.get("NOTIFY_EMAIL",  user)).strip() or user
        host   = str(st.secrets.get("SMTP_HOST", "meridiandigitaladvisory.sslsvc.com")).strip()
        port   = int(st.secrets.get("SMTP_PORT", 465))
        if not user:
            return "", "", "", "", 0, "SMTP_USER is not set in Streamlit secrets."
        if not pw:
            return "", "", "", "", 0, "SMTP_PASSWORD is not set in Streamlit secrets."
        return user, pw, notify, host, port, ""
    except Exception as e:
        return "", "", "", "", 0, f"Could not read email secrets: {e}"


def _smtp_send(user: str, pw: str, to: str, msg: MIMEMultipart,
               host: str, port: int) -> tuple[bool, str]:
    """Authenticate and send via SSL SMTP (port 465). Returns (ok, error_msg)."""
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=ctx) as server:
            server.login(user, pw)
            server.sendmail(user, to, msg.as_string())
        return True, ""
    except smtplib.SMTPAuthenticationError:
        return False, (
            "SMTP authentication failed — check SMTP_USER and SMTP_PASSWORD in Streamlit secrets.\n\n"
            "Make sure you are using the correct email address and password for "
            f"{host}."
        )
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {e}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


# ── Public API ────────────────────────────────────────────────────────────────

def send_assessment_email(
    pdf_bytes: bytes,
    pdf_filename: str,
    client_info: dict,
    results: dict,
) -> tuple[bool, str]:
    """
    Email the PDF report to the configured NOTIFY_EMAIL address.
    Returns (success: bool, message: str).
    """
    user, pw, notify, host, port, err = _get_email_config()
    if err:
        return False, err

    maturity    = results.get("maturity", {})
    pillar_avgs = results.get("pillar_avgs", {})
    avg_score   = results.get("avg_score", 0)
    total_score = results.get("total_score", 0)

    # ── Subject ───────────────────────────────────────────────────────────────
    full_name = f"{client_info.get('name', '')} {client_info.get('surname', '')}".strip()
    subject   = (
        f"New Assessment: {full_name} — {client_info.get('business', '')} "
        f"[Score {avg_score:.2f}/5 · Level {maturity.get('level', '?')} "
        f"{maturity.get('label', '')}]"
    )

    # ── Plain-text body ───────────────────────────────────────────────────────
    pillar_names = [
        "Strategy & Leadership",
        "Data Management",
        "Technology & Tools",
        "Processes & Automation",
        "People & Capability",
        "Client Experience",
        "Security & Compliance",
    ]
    pillar_lines = "\n".join(
        f"  P{i+1} {name:<28} {pillar_avgs.get(i+1, 0):.1f} / 5"
        for i, name in enumerate(pillar_names)
    )

    body = f"""\
New Digital Readiness Assessment Completed
==========================================

CLIENT DETAILS
  Name:             {full_name}
  Business:         {client_info.get('business', '')}
  Email:            {client_info.get('email', '')}
  Industry:         {client_info.get('industry', '')}
  Service/Product:  {client_info.get('service_product', '')}
  Business size:    {client_info.get('size', '')}
  Business age:     {client_info.get('business_age', '')}
  Date:             {client_info.get('date', '')}

RESULTS
  Overall Score:    {avg_score:.2f} / 5.00
  Total Score:      {total_score} / 140
  Maturity Level:   Level {maturity.get('level', '?')} — {maturity.get('label', '')}

PILLAR BREAKDOWN
{pillar_lines}

The full PDF report is attached.

— Meridian Digital Advisory Assessment App
"""

    # ── Build MIME message ────────────────────────────────────────────────────
    msg              = MIMEMultipart()
    msg["From"]      = user
    msg["To"]        = notify
    msg["Subject"]   = subject
    msg.attach(MIMEText(body, "plain"))

    part = MIMEBase("application", "pdf")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{pdf_filename}"')
    msg.attach(part)

    ok, err = _smtp_send(user, pw, notify, msg, host, port)
    if ok:
        return True, f"Report emailed to {notify}"
    return False, err


def send_invite_email(
    to_email: str,
    body: str,
    subject: str = "Your Digital Readiness Assessment — Meridian Digital Advisory",
) -> tuple[bool, str]:
    """
    Send the client invite email.
    Returns (success: bool, message: str).
    """
    user, pw, _notify, host, port, err = _get_email_config()
    if err:
        return False, err

    msg            = MIMEMultipart()
    msg["From"]    = user
    msg["To"]      = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    ok, err = _smtp_send(user, pw, to_email, msg, host, port)
    if ok:
        return True, f"✅ Invite email sent to {to_email}"
    return False, err


def test_email_connection() -> tuple[bool, str]:
    """
    Send a short test email to verify SMTP credentials.
    Returns (success: bool, message: str).
    """
    user, pw, notify, host, port, err = _get_email_config()
    if err:
        return False, err

    msg            = MIMEMultipart()
    msg["From"]    = user
    msg["To"]      = notify
    msg["Subject"] = "✅ Meridian App — Email Notification Test"
    msg.attach(MIMEText(
        "This is a test message from the Meridian Digital Advisory Assessment App.\n\n"
        "If you received this, your email notifications are configured correctly.\n"
        "PDF reports will be sent to this address whenever a client completes an assessment.\n\n"
        "— Meridian Digital Advisory",
        "plain",
    ))

    ok, err = _smtp_send(user, pw, notify, msg, host, port)
    if ok:
        return True, f"✅ Test email sent to {notify} — check your inbox."
    return False, err
