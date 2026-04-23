"""
Digital Readiness Self-Assessment — Streamlit App
Run locally:  python -m streamlit run app.py
Deploy:       share.streamlit.io  (connect GitHub repo → Deploy)
"""

import base64
import io
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data import (
    MATURITY_LEVELS, PILLARS, RESOURCES, SCORE_DESCRIPTIONS,
    SCORE_LABELS, TIER_KEY, TOP_ACTIONS, compute_results,
)
from database import (
    delete_token, generate_token, get_all_assessments, get_all_tokens,
    get_token_info, init_db, is_token_valid, save_assessment,
)
from pdf_report import generate_pdf
from email_report import send_assessment_email
from sheets import append_to_sheet

# ── Paths ─────────────────────────────────────────────────────────────────────
APP_DIR   = Path(__file__).parent
LOGO_PATH = APP_DIR / "images" / "meridian-logoV5.png"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Readiness Assessment | Meridian Digital Advisory",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Logo helper (cached) ──────────────────────────────────────────────────────
@st.cache_data
def _logo_b64() -> str | None:
    if LOGO_PATH.exists():
        return base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return None


def _scroll_to_top():
    """Scroll the Streamlit main panel to the top on page/pillar transitions."""
    import streamlit.components.v1 as components
    current = (
        st.session_state.get("page", ""),
        st.session_state.get("current_pillar", 0),
    )
    if st.session_state.get("_prev_nav") != current:
        st.session_state["_prev_nav"] = current
        components.html(
            """<script>
            (function tryScroll(attempts) {
                var doc = window.parent.document;
                // Ordered by most-likely to work in current Streamlit versions first
                var selectors = [
                    '[data-testid="stMain"]',
                    '[data-testid="stAppViewContainer"]',
                    '[data-testid="stMainBlockContainer"]',
                    'section.main',
                    '.main',
                    '[data-testid="block-container"]'
                ];
                var scrolled = false;
                for (var i = 0; i < selectors.length; i++) {
                    var el = doc.querySelector(selectors[i]);
                    if (el) {
                        el.scrollTop = 0;
                        scrolled = true;
                        break;
                    }
                }
                try { window.parent.scrollTo(0, 0); } catch(e) {}
                // Retry a few times to handle Streamlit's async rendering
                if (!scrolled && attempts > 0) {
                    setTimeout(function() { tryScroll(attempts - 1); }, 120);
                }
            })(8);
            </script>
            <style>iframe { display: none !important; }</style>""",
            height=0,
            scrolling=False,
        )


def _logo_tag(height: int = 48) -> str:
    b64 = _logo_b64()
    if not b64:
        return ""
    ext = LOGO_PATH.suffix.lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return (
        f'<img src="data:image/{mime};base64,{b64}" '
        f'style="height:{height}px;object-fit:contain;'
        f'vertical-align:middle;margin-right:14px">'
    )


# ── Secrets helpers ───────────────────────────────────────────────────────────
def _secret(key: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(key, default))
    except Exception:
        return default


# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer    {visibility: hidden;}
html, body, [class*="css"] { font-family: 'Segoe UI', Arial, sans-serif; }

.header-bar {
    background: linear-gradient(135deg,#1F3864 0%,#2E75B6 100%);
    padding: 18px 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}
.header-bar .header-text h1 {
    color:white; margin:0; font-size:1.5rem; font-weight:700; line-height:1.2;
}
.header-bar .header-text p {
    color:#BDD7EE; margin:3px 0 0 0; font-size:0.85rem;
}

.pillar-header {
    background:#2E75B6; padding:16px 20px; border-radius:8px;
    color:white; margin-bottom:16px;
}
.pillar-header h2 { color:white; margin:0; font-size:1.2rem; }
.pillar-header p  { color:#DEEAF1; margin:4px 0 0 0; font-size:0.82rem; }

.question-card {
    background:#F8FBFD; border-left:4px solid #2E75B6;
    padding:13px 17px; border-radius:0 8px 8px 0; margin-bottom:10px;
}
.question-card p { margin:0; font-size:0.95rem; color:#1F3864; font-weight:500; }

.tip-box {
    background:#E2EFDA; border-left:4px solid #70AD47;
    padding:12px 16px; border-radius:0 8px 8px 0;
    font-size:0.88rem; color:#375623; margin:12px 0;
}
.action-item {
    background:white; border:1px solid #DEEAF1; border-radius:8px;
    padding:10px 14px; margin:6px 0; font-size:0.9rem; color:#1F3864;
}
.action-item::before { content:"→ "; color:#2E75B6; font-weight:bold; }

.access-denied {
    text-align:center; padding:60px 20px;
}
.access-denied h2 { color:#1F3864; }
.access-denied p  { color:#595959; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page":                   "welcome",
        "client_name":            "",
        "client_surname":         "",
        "client_business":        "",
        "client_email":           "",
        "client_industry":        "",
        "client_service_product": "",
        "client_business_age":    "",
        "business_size":          None,
        "current_pillar":         0,
        "active_token":           None,
        "_saved_to_db":           False,
        "_pdf_bytes":             None,
        "_pdf_fname":             None,
        "_email_sent_ok":         None,
        "_email_sent_msg":        "",
        "admin_auth":             False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    for p in PILLARS:
        for qi in range(4):
            key = f"score_{p['id']}_{qi}"
            if key not in st.session_state:
                st.session_state[key] = None


def collect_scores() -> dict:
    return {
        p["id"]: [st.session_state.get(f"score_{p['id']}_{qi}") for qi in range(4)]
        for p in PILLARS
    }


def pillar_complete(pid: int) -> bool:
    return all(st.session_state.get(f"score_{pid}_{qi}") is not None for qi in range(4))


def all_complete() -> bool:
    return all(pillar_complete(p["id"]) for p in PILLARS)


def answered_count() -> int:
    return sum(
        1 for p in PILLARS for qi in range(4)
        if st.session_state.get(f"score_{p['id']}_{qi}") is not None
    )


# ── Shared UI helpers ─────────────────────────────────────────────────────────
def render_header(subtitle: str = "Professional Services  ·  Australia"):
    logo = _logo_tag(52)
    st.markdown(f"""
    <div class="header-bar">
        {logo}
        <div class="header-text">
            <h1>Digital Readiness Assessment</h1>
            <p>Meridian Digital Advisory &nbsp;·&nbsp; {subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_progress(current_step: int):
    """Step indicator: Welcome(0) → P1–P7(1–7) → Results(8)."""
    steps  = ["Welcome"] + [f"P{i}" for i in range(1, 8)] + ["Results"]
    cols   = st.columns(len(steps))
    for i, (col, label) in enumerate(zip(cols, steps)):
        if i < current_step:
            col.markdown(
                f"<div style='text-align:center;color:#70AD47;"
                f"font-size:0.9rem;font-weight:700'>✓ {label}</div>",
                unsafe_allow_html=True,
            )
        elif i == current_step:
            col.markdown(
                f"<div style='text-align:center;color:#2E75B6;"
                f"font-size:0.95rem;font-weight:800;"
                f"border-bottom:2px solid #2E75B6;padding-bottom:2px'>"
                f"● {label}</div>",
                unsafe_allow_html=True,
            )
        else:
            col.markdown(
                f"<div style='text-align:center;color:#AAAAAA;"
                f"font-size:0.9rem'>○ {label}</div>",
                unsafe_allow_html=True,
            )
    st.markdown("<div style='margin-bottom:18px'></div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# GATE PAGES
# ═════════════════════════════════════════════════════════════════════════════
def page_no_access():
    render_header()
    st.markdown("""
    <div class="access-denied">
        <div style="font-size:3rem">🔒</div>
        <h2>Access Required</h2>
        <p>This assessment is invitation-only.<br>
        Please contact <strong>Meridian Digital Advisory</strong>
        to receive your personalised assessment link.</p>
    </div>
    """, unsafe_allow_html=True)


def page_invalid_token():
    render_header()
    st.markdown("""
    <div class="access-denied">
        <div style="font-size:3rem">⚠️</div>
        <h2>Link Unavailable</h2>
        <p>This invitation link has already been used or is no longer valid.<br>
        Please contact <strong>Meridian Digital Advisory</strong>
        if you believe this is an error.</p>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# WELCOME PAGE
# ═════════════════════════════════════════════════════════════════════════════
def page_welcome():
    _scroll_to_top()
    render_header()

    st.markdown("""
    This assessment evaluates your business's digital maturity across **7 key pillars** — from
    strategy and data governance to security and client experience. It takes about **10–15 minutes**
    and is tailored to your business size.

    At the end you'll receive a **Digital Readiness Score**, a personalised **Maturity Level**,
    and a **priority action plan** — plus a downloadable PDF report.
    """)
    st.markdown(
        "<div class='tip-box'>💡 <strong>Tip:</strong> Score based on what is "
        "<em>actually in place</em>, not what you intend to implement. "
        "Honest scoring gives you the most useful results.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("Your Details")

    INDUSTRIES = [
        "",
        "Accounting & Finance",
        "Architecture & Engineering",
        "Construction & Trades",
        "Creative & Design",
        "Education & Training",
        "Healthcare & Allied Health",
        "Hospitality & Tourism",
        "HR & Recruitment",
        "IT & Technology Services",
        "Legal Services",
        "Management Consulting",
        "Marketing & Communications",
        "Not-for-Profit",
        "Real Estate & Property",
        "Retail & E-commerce",
        "Other",
    ]
    BUSINESS_AGES = [
        "",
        "Less than 1 year",
        "1–2 years",
        "3–5 years",
        "6–10 years",
        "More than 10 years",
    ]

    col1, col2 = st.columns(2)
    with col1:
        name    = st.text_input("First name *",    value=st.session_state.client_name,    placeholder="e.g. Sandra")
    with col2:
        surname = st.text_input("Surname *",       value=st.session_state.client_surname, placeholder="e.g. Smith")

    col3, col4 = st.columns(2)
    with col3:
        business = st.text_input("Business name *", value=st.session_state.client_business, placeholder="e.g. Meridian Advisory")
    with col4:
        email = st.text_input("Email address *",    value=st.session_state.client_email,    placeholder="e.g. sandra@meridian.com.au")

    col5, col6 = st.columns(2)
    with col5:
        industry_idx = INDUSTRIES.index(st.session_state.client_industry) \
                       if st.session_state.client_industry in INDUSTRIES else 0
        industry = st.selectbox("Industry *", INDUSTRIES, index=industry_idx,
                                format_func=lambda x: "— Select your industry —" if x == "" else x)
    with col6:
        service_product = st.text_input("Service / Product *",
                                        value=st.session_state.client_service_product,
                                        placeholder="e.g. Cleaning services")

    age_idx = BUSINESS_AGES.index(st.session_state.client_business_age) \
              if st.session_state.client_business_age in BUSINESS_AGES else 0
    business_age = st.selectbox("How long has your business been operating? *",
                                BUSINESS_AGES, index=age_idx,
                                format_func=lambda x: "— Select an option —" if x == "" else x)

    st.markdown("---")
    st.subheader("Business Size")
    st.caption("Select the option that best describes your business.")

    size_options = {
        "Sole Trader":   ("👤", "1 person"),
        "Small Business":("👥", "2 – 19 employees"),
        "Medium Business":("🏢","20 – 199 employees"),
    }
    current_size = st.session_state.business_size
    cols = st.columns(3)
    for col, (size, (icon, staff)) in zip(cols, size_options.items()):
        selected = current_size == size
        border   = "2px solid #2E75B6" if selected else "2px solid #DEEAF1"
        bg       = "#DEEAF1" if selected else "white"
        col.markdown(f"""
        <div style="border:{border};background:{bg};border-radius:10px;
                    padding:16px;text-align:center;min-height:100px">
            <div style="font-size:2rem">{icon}</div>
            <div style="font-weight:700;color:#1F3864;font-size:0.9rem;margin:4px 0">{size}</div>
            <div style="font-size:0.75rem;color:#595959">{staff}</div>
        </div>""", unsafe_allow_html=True)
        if col.button(f"Select {size}", key=f"size_{size}", use_container_width=True,
                      type="primary" if selected else "secondary"):
            st.session_state.business_size = size
            st.rerun()

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    errors = []
    if not name.strip():                       errors.append("Please enter your first name.")
    if not surname.strip():                    errors.append("Please enter your surname.")
    if not business.strip():                   errors.append("Please enter your business name.")
    if not email.strip():                      errors.append("Please enter your email address.")
    if not industry:                           errors.append("Please select your industry.")
    if not service_product.strip():            errors.append("Please enter your service or product.")
    if not business_age:                       errors.append("Please select how long your business has been operating.")
    if not st.session_state.business_size:    errors.append("Please select a business size.")

    if st.button("Start Assessment →", type="primary", use_container_width=True):
        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.client_name            = name.strip()
            st.session_state.client_surname         = surname.strip()
            st.session_state.client_business        = business.strip()
            st.session_state.client_email           = email.strip()
            st.session_state.client_industry        = industry
            st.session_state.client_service_product = service_product.strip()
            st.session_state.client_business_age    = business_age
            st.session_state.current_pillar         = 0
            st.session_state.page                   = "pillar"
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PILLAR PAGES
# ═════════════════════════════════════════════════════════════════════════════
def page_pillar():
    _scroll_to_top()
    idx    = st.session_state.current_pillar
    pillar = PILLARS[idx]
    pid    = pillar["id"]
    key    = TIER_KEY[st.session_state.business_size]
    questions = pillar[key]

    render_header(f"{st.session_state.client_name}  ·  {st.session_state.client_business}")
    render_progress(idx + 1)

    answered = answered_count()
    st.progress(answered / 28, text=f"{answered} of 28 questions answered")
    st.markdown("")

    st.markdown(f"""
    <div class="pillar-header">
        <h2>{pillar['icon']}  Pillar {pid} of 7 — {pillar['name']}</h2>
        <p>{pillar['description']}</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("")

    for qi, q in enumerate(questions):
        st.markdown(f"<div class='question-card'><p>Q{qi+1}.&nbsp; {q}</p></div>",
                    unsafe_allow_html=True)

        score_key = f"score_{pid}_{qi}"
        existing  = st.session_state.get(score_key)
        idx_default = (existing - 1) if existing is not None else None

        # Use per-question custom labels if available, else fall back to generic
        _letters = ["a", "b", "c", "d", "e"]
        opts_key = key + "_labels"
        if opts_key in pillar and qi < len(pillar[opts_key]):
            q_labels = [f"{_letters[i]} — {lbl}" for i, lbl in enumerate(pillar[opts_key][qi])]
        else:
            generic = list(SCORE_LABELS.values())
            q_labels = [f"{_letters[i]} — {lbl.split(' — ', 1)[1]}" for i, lbl in enumerate(generic)]

        chosen = st.radio(
            label=f"score_radio_{pid}_{qi}",
            options=q_labels,
            index=idx_default,
            horizontal=True,
            label_visibility="collapsed",
            key=f"radio_{pid}_{qi}",
        )
        if chosen is not None:
            val = _letters.index(chosen.split(" — ")[0]) + 1
            st.session_state[score_key] = val
        st.markdown("")

    # Navigation
    st.markdown("---")
    col_prev, col_mid, col_next = st.columns([1, 2, 1])
    with col_prev:
        if idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_pillar = idx - 1
                st.rerun()
        else:
            if st.button("← Back to Welcome", use_container_width=True):
                st.session_state.page = "welcome"
                st.rerun()

    with col_mid:
        if pillar_complete(pid):
            st.markdown(
                "<div style='text-align:center;color:#70AD47;font-size:0.85rem;"
                "padding-top:8px'>✅ All questions answered</div>",
                unsafe_allow_html=True,
            )
        else:
            n = sum(1 for qi in range(4) if st.session_state.get(f"score_{pid}_{qi}") is None)
            st.markdown(
                f"<div style='text-align:center;color:#ED7D31;font-size:0.85rem;"
                f"padding-top:8px'>⚠️ {n} question(s) still need a score</div>",
                unsafe_allow_html=True,
            )

    with col_next:
        if idx < len(PILLARS) - 1:
            nxt = f"Next: {PILLARS[idx+1]['name'].split(' ')[0]}… →"
            if st.button(nxt, type="primary", use_container_width=True,
                         disabled=not pillar_complete(pid)):
                st.session_state.current_pillar = idx + 1
                st.rerun()
        else:
            if st.button("See My Results →", type="primary", use_container_width=True,
                         disabled=not all_complete()):
                st.session_state.page = "results"
                st.rerun()

    if idx == len(PILLARS) - 1 and not all_complete():
        st.warning("⚠️ Please answer all questions before viewing results. "
                   "Use '← Previous' to go back and complete any unanswered questions.")


# ═════════════════════════════════════════════════════════════════════════════
# RESULTS PAGE
# ═════════════════════════════════════════════════════════════════════════════
def _radar_chart(results: dict) -> go.Figure:
    short  = [f"P{p['id']} {p['name'].split(' ')[0]}" for p in PILLARS]
    values = [results["pillar_avgs"].get(p["id"], 0) for p in PILLARS]
    vc     = values + [values[0]]
    lc     = short  + [short[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vc, theta=lc, fill="toself",
        fillcolor="rgba(46,117,182,0.2)",
        line=dict(color="#2E75B6", width=2),
        name="Your Score",
        hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
    ))
    fig.add_trace(go.Scatterpolar(
        r=[5]*(len(short)+1), theta=lc, fill="toself",
        fillcolor="rgba(200,200,200,0.08)",
        line=dict(color="#DDDDDD", width=1, dash="dot"),
        name="Maximum (5)",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,5], tickvals=[1,2,3,4,5],
                            tickfont=dict(size=10,color="#595959"), gridcolor="#E0E0E0"),
            angularaxis=dict(tickfont=dict(size=12,color="#1F3864",family="Arial"),
                             gridcolor="#E0E0E0"),
            bgcolor="white",
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
        margin=dict(t=30,b=60,l=60,r=60), height=420,
        paper_bgcolor="white", font=dict(family="Arial"),
    )
    return fig


def page_results():
    _scroll_to_top()
    scores  = collect_scores()
    results = compute_results(scores)
    maturity = results["maturity"]
    level    = maturity["level"]

    # ── Build client_info dict (used for save + PDF) ─────────────────────────
    client_info = {
        "name":            st.session_state.client_name,
        "surname":         st.session_state.client_surname,
        "business":        st.session_state.client_business,
        "email":           st.session_state.client_email,
        "size":            st.session_state.business_size,
        "industry":        st.session_state.client_industry,
        "service_product": st.session_state.client_service_product,
        "business_age":    st.session_state.client_business_age,
        "date":            date.today().strftime("%d %B %Y").lstrip("0"),
    }

    # ── Save to DB + Sheets + generate PDF — all exactly once per session ────
    if not st.session_state._saved_to_db:
        token = st.session_state.active_token or "no-token"
        try:
            save_assessment(token, client_info, results, raw_scores=scores)
        except Exception:
            pass
        try:
            append_to_sheet(client_info, results, raw_scores=scores)
        except Exception:
            pass

        # Generate PDF then email it to the configured notify address
        with st.spinner("Preparing your report…"):
            try:
                pdf_bytes = generate_pdf(
                    client_info, results, PILLARS, MATURITY_LEVELS,
                    TOP_ACTIONS, RESOURCES, LOGO_PATH
                )
                fname = (
                    f"Digital_Readiness_"
                    f"{st.session_state.client_business.replace(' ', '_')}_"
                    f"{date.today().strftime('%Y%m%d')}.pdf"
                )
                st.session_state._pdf_bytes = pdf_bytes
                st.session_state._pdf_fname = fname
            except Exception as e:
                st.session_state._pdf_bytes = None
                st.session_state._email_sent_ok  = False
                st.session_state._email_sent_msg = f"PDF generation failed: {e}"

            # Email the report — capture result so it's visible on the page
            if st.session_state._pdf_bytes:
                try:
                    ok, msg = send_assessment_email(
                        st.session_state._pdf_bytes,
                        st.session_state._pdf_fname or fname,
                        client_info,
                        results,
                    )
                    st.session_state._email_sent_ok  = ok
                    st.session_state._email_sent_msg = msg
                except Exception as e:
                    st.session_state._email_sent_ok  = False
                    st.session_state._email_sent_msg = f"{type(e).__name__}: {e}"

        st.session_state._saved_to_db = True

    render_header(f"{st.session_state.client_name}  ·  {st.session_state.client_business}")
    render_progress(8)
    st.balloons()

    # Maturity hero
    st.markdown(f"""
    <div style="background:{maturity['color']};border-radius:12px;
                padding:24px 28px;margin-bottom:16px;
                border:2px solid {maturity['badge_bg']}">
        <div style="font-size:0.78rem;color:{maturity['text_color']};
                    font-weight:600;text-transform:uppercase;letter-spacing:1px">
            Digital Maturity Level
        </div>
        <div style="font-size:1.9rem;font-weight:800;
                    color:{maturity['text_color']};margin:4px 0">
            Level {level} — {maturity['label']}
        </div>
        <div style="font-size:0.84rem;color:{maturity['text_color']};opacity:0.85">
            Average score: {results['avg_score']:.2f} / 5.00  ·  {maturity['range']}
        </div>
        <div style="font-size:0.88rem;color:{maturity['text_color']};margin-top:10px">
            {maturity['description']}
        </div>
    </div>""", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Average Score",       f"{results['avg_score']:.2f} / 5.00")
    with m2: st.metric("Total Score",          f"{results['total_score']} / 140")
    with m3: st.metric("Questions Answered",   f"{results['answered']} / 28")

    st.markdown("---")
    st.subheader("📡 Digital Readiness by Pillar")
    st.plotly_chart(_radar_chart(results), use_container_width=True)

    st.subheader("🏆 Pillar Breakdown")
    table_data = []
    for p in PILLARS:
        pid  = p["id"]
        avg  = results["pillar_avgs"].get(pid, 0)
        tot  = results["pillar_totals"].get(pid, 0)
        ridx = max(0, min(4, round(avg) - 1))
        bar  = "█" * round(avg * 2) + "░" * (10 - round(avg * 2))
        table_data.append({
            "Pillar":         f"{p['icon']} {p['name']}",
            "Score":          f"{avg:.1f}/5",
            "Total":          f"{tot}/20",
            "Progress":       bar,
            "What this means": p["rubric"][ridx] if avg > 0 else "—",
        })
    st.dataframe(
        pd.DataFrame(table_data),
        use_container_width=True, hide_index=True,
        column_config={
            "Pillar":          st.column_config.TextColumn("Pillar",       width="medium"),
            "Score":           st.column_config.TextColumn("Avg Score",    width="small"),
            "Total":           st.column_config.TextColumn("Total (/20)",  width="small"),
            "Progress":        st.column_config.TextColumn("Visual",       width="small"),
            "What this means": st.column_config.TextColumn("At this score…", width="large"),
        },
    )

    st.markdown("---")
    st.subheader(f"🎯 Priority Actions — {maturity['label']}")
    for action in TOP_ACTIONS[level]:
        st.markdown(f"<div class='action-item'>{action}</div>", unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📚 Key Australian Resources"):
        for name, url in RESOURCES:
            st.markdown(f"- [{name}]({url})")

    st.markdown("---")
    st.subheader("📄 Download Your Report")
    if st.session_state._pdf_bytes:
        st.download_button(
            "⬇️ Download Your Report",
            data=st.session_state._pdf_bytes,
            file_name=st.session_state._pdf_fname,
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )
    else:
        # Fallback: generate on demand if auto-generation failed on first load
        if st.button("⬇️ Download Your Report", type="primary", use_container_width=True):
            with st.spinner("Generating your report…"):
                try:
                    pdf_bytes = generate_pdf(
                        client_info, results, PILLARS, MATURITY_LEVELS,
                        TOP_ACTIONS, RESOURCES, LOGO_PATH
                    )
                    fname = (
                        f"Digital_Readiness_"
                        f"{st.session_state.client_business.replace(' ', '_')}_"
                        f"{date.today().strftime('%Y%m%d')}.pdf"
                    )
                    st.session_state._pdf_bytes = pdf_bytes
                    st.session_state._pdf_fname = fname
                    ok, msg = send_assessment_email(pdf_bytes, fname, client_info, results)
                    st.session_state._email_sent_ok  = ok
                    st.session_state._email_sent_msg = msg
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not generate report: {e}")

    # ── Email notification status ─────────────────────────────────────────────
    email_ok  = st.session_state.get("_email_sent_ok")
    email_msg = st.session_state.get("_email_sent_msg", "")
    if email_ok is True:
        st.caption(f"📧 {email_msg}")
    elif email_ok is False:
        st.warning(
            f"⚠️ **Email notification failed.**\n\n{email_msg}\n\n"
            "Your PDF download above is not affected. "
            "Check the Email tab in the Admin Dashboard to diagnose."
        )

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Start a New Assessment", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    with c2:
        if st.button("✏️ Revise My Answers", use_container_width=True):
            st.session_state.page = "pillar"
            st.session_state.current_pillar = 0
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# ADMIN PAGE  —  accessed via /?admin=true
# ═════════════════════════════════════════════════════════════════════════════
def page_admin():
    # ── Logo + title ──────────────────────────────────────────────────────────
    logo = _logo_tag(40)
    st.markdown(f"""
    <div style="background:#1F3864;padding:16px 22px;border-radius:10px;
                margin-bottom:20px;display:flex;align-items:center">
        {logo}
        <div>
            <span style="color:white;font-size:1.2rem;font-weight:700">
                Admin Dashboard</span><br>
            <span style="color:#BDD7EE;font-size:0.8rem">
                Meridian Digital Advisory — Digital Readiness Tool</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Password gate ─────────────────────────────────────────────────────────
    admin_pwd = _secret("ADMIN_PASSWORD", "meridian2024")
    if not st.session_state.admin_auth:
        st.subheader("🔐 Admin Login")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", type="primary"):
            if pwd == admin_pwd:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    if st.button("🔓 Log out", type="secondary"):
        st.session_state.admin_auth = False
        st.rerun()

    st.markdown("---")
    tab_invite, tab_records, tab_tokens, tab_sheets = st.tabs(
        ["✉️  Generate Invites", "📋  Assessment Records", "🔑  Manage Tokens", "⚙️  Integrations"]
    )

    # ── TAB 1: Generate invite links ──────────────────────────────────────────
    with tab_invite:
        st.markdown("### Generate a New Invite Link")
        base_url = _secret("BASE_URL", "http://localhost:8501")
        st.caption(f"App URL (set BASE_URL in secrets.toml): `{base_url}`")

        with st.form("invite_form"):
            c1, c2 = st.columns(2)
            with c1:
                inv_name  = st.text_input("Client first name (optional)")
            with c2:
                inv_email = st.text_input("Client email (optional)")
            inv_notes = st.text_input("Internal notes (not shown to client, optional)")
            submitted = st.form_submit_button("Generate Invite Link →", type="primary")

        if submitted:
            token = generate_token(inv_name, inv_email, inv_notes)
            link  = f"{base_url.rstrip('/')}/?token={token}"
            st.success("✅ Invite link created!")
            st.code(link, language=None)
            st.info("Copy the link above and send it to your client. "
                    "It is single-use — once they complete the assessment it expires.")

            # ── Email draft ───────────────────────────────────────────────────
            greeting_name = inv_name.strip() if inv_name.strip() else "there"
            email_subject = "Your Digital Readiness Assessment — Meridian Digital Advisory"
            email_body = f"""Subject: {email_subject}

Dear {greeting_name},

I hope this message finds you well.

As part of our work together at Meridian Digital Advisory, I'd like to invite you to complete our Digital Readiness Assessment. This tailored assessment evaluates your business's digital maturity across 7 key areas — from strategy and data governance to security and client experience.

It takes approximately 10–15 minutes to complete. At the end you'll receive:
  • A personalised Digital Readiness Score
  • A breakdown across 7 digital pillars
  • A Priority Action Plan tailored to your business
  • A downloadable PDF report

Please use your unique, single-use link below to access the assessment:

{link}

Please note this link is for your use only — it cannot be shared or reused once completed.

If you have any questions or need assistance, please don't hesitate to reach out.

Kind regards,
[Your Name]
Meridian Digital Advisory"""

            st.markdown("---")
            st.markdown("#### ✉️ Email Draft")
            st.caption("Copy the text below and paste it into your email client.")
            st.code(email_body, language=None)

        st.markdown("---")
        st.markdown("### Pending Invites (not yet used)")
        all_tokens = get_all_tokens()
        pending    = [t for t in all_tokens if not t["is_used"]]
        if pending:
            rows = []
            for t in pending:
                link = f"{base_url.rstrip('/')}/?token={t['token']}"
                rows.append({
                    "Client name":  t["client_name"]  or "—",
                    "Email":        t["client_email"] or "—",
                    "Notes":        t["notes"]        or "—",
                    "Created":      t["created_at"],
                    "Link":         link,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No pending invites. Generate one above.")

    # ── TAB 2: Assessment records ─────────────────────────────────────────────
    with tab_records:
        st.markdown("### Completed Assessments")
        records = get_all_assessments()
        if records:
            df = pd.DataFrame([{
                "Date":             r["completed_at"][:10],
                "Time":             r["completed_at"][11:16],
                "First Name":       r["client_name"],
                "Surname":          r.get("client_surname", ""),
                "Business":         r["client_business"],
                "Email":            r["client_email"],
                "Industry":         r.get("industry", ""),
                "Service/Product":  r.get("service_product", ""),
                "Biz Age":          r.get("business_age", ""),
                "Size":             r["business_size"],
                "Avg Score":        round(r["avg_score"], 2),
                "Maturity":         r["maturity_level"],
                "Total /140":       r["total_score"],
                "P1": r["p1_avg"], "P2": r["p2_avg"], "P3": r["p3_avg"],
                "P4": r["p4_avg"], "P5": r["p5_avg"], "P6": r["p6_avg"],
                "P7": r["p7_avg"],
            } for r in records])

            st.dataframe(df, use_container_width=True, hide_index=True,
                         column_config={
                             "Avg Score":  st.column_config.NumberColumn(format="%.2f"),
                             "P1": st.column_config.NumberColumn("P1", format="%.1f"),
                             "P2": st.column_config.NumberColumn("P2", format="%.1f"),
                             "P3": st.column_config.NumberColumn("P3", format="%.1f"),
                             "P4": st.column_config.NumberColumn("P4", format="%.1f"),
                             "P5": st.column_config.NumberColumn("P5", format="%.1f"),
                             "P6": st.column_config.NumberColumn("P6", format="%.1f"),
                             "P7": st.column_config.NumberColumn("P7", format="%.1f"),
                         })

            # Export CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️  Export all records to CSV",
                data=csv,
                file_name=f"assessments_{date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

            st.markdown(f"**{len(records)} assessment(s) on record.**")
        else:
            st.info("No completed assessments yet.")

    # ── TAB 3: Manage tokens ──────────────────────────────────────────────────
    with tab_tokens:
        st.markdown("### All Tokens")
        all_tokens = get_all_tokens()
        if all_tokens:
            for t in all_tokens:
                status = "✅ Used" if t["is_used"] else "⏳ Pending"
                used_at = t["used_at"] or "—"
                with st.expander(f"{status}  ·  {t['client_name'] or 'Unnamed'}  ·  Created {t['created_at'][:10]}"):
                    st.write(f"**Email:** {t['client_email'] or '—'}")
                    st.write(f"**Notes:** {t['notes'] or '—'}")
                    st.write(f"**Used at:** {used_at}")
                    link = f"{_secret('BASE_URL','http://localhost:8501')}/?token={t['token']}"
                    st.code(link, language=None)
                    if not t["is_used"]:
                        if st.button("🗑️ Delete this token", key=f"del_{t['token']}"):
                            delete_token(t["token"])
                            st.rerun()
        else:
            st.info("No tokens created yet.")

    # ── TAB 4: Google Sheets & Email diagnostics ─────────────────────────────
    with tab_sheets:
        from sheets import test_connection
        from email_report import test_email_connection

        # ── Sheets section ────────────────────────────────────────────────────
        st.markdown("### Google Sheets Integration")
        sheet_id = _secret("SHEET_ID", "")
        if sheet_id:
            st.markdown(f"**Sheet ID configured:** `{sheet_id[:20]}…`")
        else:
            st.warning("SHEET_ID is not set in Streamlit secrets yet.")

        if st.button("🔌 Test Google Sheets Connection", type="primary"):
            with st.spinner("Testing connection…"):
                ok, msg = test_connection()
            if ok:
                st.success(msg)
            else:
                st.error(f"Connection failed:\n\n{msg}")
                st.markdown(
                    "**Common fixes:**\n"
                    "- Make sure `SHEET_ID` is added to Streamlit Cloud Secrets\n"
                    "- Make sure `[gcp_service_account]` block is in Streamlit Cloud Secrets\n"
                    "- Make sure the Google Sheet is shared (Editor) with the service account email\n"
                    "- Check that the `private_key` value uses `\\\\n` for line breaks — not actual newlines\n"
                    "- Ensure Sheets API and Drive API are enabled in your Google Cloud project"
                )

        st.markdown("---")

        # ── Email section ──────────────────────────────────────────────────────
        st.markdown("### Email Notifications (Gmail)")
        st.markdown(
            "When a client completes an assessment the PDF report is automatically "
            "emailed to **NOTIFY_EMAIL**."
        )

        gmail_addr   = _secret("GMAIL_ADDRESS", "")
        notify_addr  = _secret("NOTIFY_EMAIL", gmail_addr)

        if gmail_addr:
            st.markdown(f"**Sending from:** `{gmail_addr}`")
            st.markdown(f"**Sending to:**   `{notify_addr or gmail_addr}`")
        else:
            st.warning("GMAIL_ADDRESS is not set in Streamlit secrets yet.")

        if st.button("📧 Send Test Email", type="primary"):
            with st.spinner("Sending test email…"):
                ok, msg = test_email_connection()
            if ok:
                st.success(msg)
            else:
                st.error(f"Email failed:\n\n{msg}")

        st.markdown("---")
        st.markdown("#### Gmail App Password setup (one-time)")
        st.info(
            "You cannot use your regular Gmail password here — Google requires an "
            "**App Password** for third-party apps.\n\n"
            "**Steps:**\n"
            "1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)\n"
            "2. Make sure **2-Step Verification** is ON\n"
            "3. Search for **App Passwords** in the search bar\n"
            "4. Choose app: **Mail** · device: **Windows Computer** (any label works)\n"
            "5. Click **Generate** — copy the 16-character code shown\n"
            "6. Paste it as `GMAIL_APP_PASSWORD` in Streamlit secrets (no spaces needed)"
        )
        st.markdown("**Add these three lines to Streamlit secrets:**")
        st.code(
            "GMAIL_ADDRESS      = \"you@gmail.com\"\n"
            "GMAIL_APP_PASSWORD = \"xxxx xxxx xxxx xxxx\"\n"
            "NOTIFY_EMAIL       = \"you@gmail.com\"   # where reports are sent",
            language="toml",
        )
        st.markdown(
            "**Also keep your existing secrets** (`SHEET_ID`, `GCP_JSON`) — "
            "those are still needed for Google Sheets."
        )


# ═════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═════════════════════════════════════════════════════════════════════════════
def main():
    init_db()
    init_state()

    # ── Admin route (?admin=true) ─────────────────────────────────────────────
    if st.query_params.get("admin") == "true":
        page_admin()
        return

    # ── Token gating ──────────────────────────────────────────────────────────
    require_token = _secret("REQUIRE_TOKEN", "false").lower() == "true"
    url_token     = st.query_params.get("token")

    if require_token:
        if not url_token:
            page_no_access()
            return
        if not is_token_valid(url_token):
            page_invalid_token()
            return

    # Store token in session (once) and pre-fill name/email if available
    if url_token and not st.session_state.active_token:
        st.session_state.active_token = url_token
        info = get_token_info(url_token)
        if info:
            if info.get("client_name")  and not st.session_state.client_name:
                st.session_state.client_name  = info["client_name"]
            if info.get("client_email") and not st.session_state.client_email:
                st.session_state.client_email = info["client_email"]

    # ── Assessment routing ────────────────────────────────────────────────────
    page = st.session_state.page
    if page == "welcome":
        page_welcome()
    elif page == "pillar":
        page_pillar()
    elif page == "results":
        page_results()
    else:
        st.session_state.page = "welcome"
        st.rerun()


if __name__ == "__main__":
    main()
