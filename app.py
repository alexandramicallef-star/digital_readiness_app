"""
Digital Readiness Self-Assessment — Streamlit App
Run locally:  streamlit run app.py
Deploy:       streamlit.io/cloud  (connect GitHub repo → Deploy)
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date

from data import (
    PILLARS, MATURITY_LEVELS, TOP_ACTIONS, RESOURCES,
    SCORE_LABELS, SCORE_DESCRIPTIONS, TIER_KEY, compute_results,
)
from pdf_report import generate_pdf

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Readiness Assessment",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hide default Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Global font */
html, body, [class*="css"] { font-family: 'Segoe UI', Arial, sans-serif; }

/* Top header bar */
.header-bar {
    background: linear-gradient(135deg, #1F3864 0%, #2E75B6 100%);
    padding: 24px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    color: white;
}
.header-bar h1 { color: white; margin: 0; font-size: 1.8rem; font-weight: 700; }
.header-bar p  { color: #BDD7EE; margin: 4px 0 0 0; font-size: 0.95rem; }

/* Pillar header */
.pillar-header {
    background: #2E75B6;
    padding: 16px 20px;
    border-radius: 8px;
    color: white;
    margin-bottom: 16px;
}
.pillar-header h2 { color: white; margin: 0; font-size: 1.25rem; }
.pillar-header p  { color: #DEEAF1; margin: 4px 0 0 0; font-size: 0.85rem; }

/* Question card */
.question-card {
    background: #F8FBFD;
    border-left: 4px solid #2E75B6;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 12px;
}
.question-card p { margin: 0; font-size: 0.95rem; color: #1F3864; font-weight: 500; }

/* Rubric box */
.rubric-box {
    background: #DEEAF1;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.8rem;
    color: #1F3864;
    margin-top: 8px;
}

/* Maturity badge */
.maturity-badge {
    display: inline-block;
    padding: 10px 24px;
    border-radius: 24px;
    font-weight: 700;
    font-size: 1.1rem;
    color: white;
    margin: 8px 0;
}

/* Score metric */
.score-metric {
    background: #1F3864;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    color: white;
}
.score-metric .value { font-size: 2.2rem; font-weight: 700; }
.score-metric .label { font-size: 0.8rem; color: #BDD7EE; margin-top: 2px; }

/* Progress step */
.step-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

/* Tip/info box */
.tip-box {
    background: #E2EFDA;
    border-left: 4px solid #70AD47;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    font-size: 0.88rem;
    color: #375623;
    margin: 12px 0;
}

/* Action item */
.action-item {
    background: white;
    border: 1px solid #DEEAF1;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.9rem;
    color: #1F3864;
}
.action-item::before { content: "→ "; color: #2E75B6; font-weight: bold; }

/* Welcome tier cards */
.tier-card {
    border: 2px solid #DEEAF1;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s;
}
.tier-card:hover { border-color: #2E75B6; }
.tier-card.selected { border-color: #2E75B6; background: #DEEAF1; }

/* divider */
.section-divider { border-top: 2px solid #DEEAF1; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)


# ── Session state initialisation ──────────────────────────────────────────────
def init_state():
    defaults = {
        "page":            "welcome",
        "client_name":     "",
        "client_business": "",
        "client_email":    "",
        "business_size":   None,
        "current_pillar":  0,        # 0-indexed
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Initialise per-question score keys
    for p in PILLARS:
        for qi in range(4):
            key = f"score_{p['id']}_{qi}"
            if key not in st.session_state:
                st.session_state[key] = None


def collect_scores() -> dict:
    """Collect all scored values from session state into {pillar_id: [s1..s4]}."""
    scores = {}
    for p in PILLARS:
        scores[p["id"]] = [
            st.session_state.get(f"score_{p['id']}_{qi}") for qi in range(4)
        ]
    return scores


def pillar_complete(pillar_id: int) -> bool:
    return all(
        st.session_state.get(f"score_{pillar_id}_{qi}") is not None
        for qi in range(4)
    )


def all_complete() -> bool:
    return all(pillar_complete(p["id"]) for p in PILLARS)


def answered_count() -> int:
    return sum(
        1 for p in PILLARS for qi in range(4)
        if st.session_state.get(f"score_{p['id']}_{qi}") is not None
    )


# ── Reusable header ───────────────────────────────────────────────────────────
def render_header(subtitle="Professional Services · Australia"):
    st.markdown(f"""
    <div class="header-bar">
        <h1>📊 Digital Readiness Assessment</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_progress(current_step: int):
    """Show step indicator: Welcome → P1 → … → P7 → Results"""
    steps = ["Welcome"] + [f"P{i}" for i in range(1, 8)] + ["Results"]
    cols = st.columns(len(steps))
    for i, (col, label) in enumerate(zip(cols, steps)):
        if i < current_step:
            col.markdown(f"<div style='text-align:center;color:#70AD47;font-size:0.7rem;font-weight:600'>✓ {label}</div>", unsafe_allow_html=True)
        elif i == current_step:
            col.markdown(f"<div style='text-align:center;color:#2E75B6;font-size:0.7rem;font-weight:700;border-bottom:2px solid #2E75B6;padding-bottom:2px'>● {label}</div>", unsafe_allow_html=True)
        else:
            col.markdown(f"<div style='text-align:center;color:#AAAAAA;font-size:0.7rem'>○ {label}</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: WELCOME
# ═════════════════════════════════════════════════════════════════════════════
def page_welcome():
    render_header()
    render_progress(0)

    st.markdown("""
    This assessment evaluates your business's digital maturity across **7 key pillars** — from strategy
    and data governance to security and client experience. It takes about **10–15 minutes** to complete
    and is tailored to your business size.

    At the end you'll receive a **Digital Readiness Score**, a personalised **Maturity Level**,
    and a **priority action plan** — plus a downloadable PDF report.
    """)

    st.markdown("<div class='tip-box'>💡 <strong>Tip:</strong> Score based on what is <em>actually in place</em>, not what you intend to implement. Honest scoring gives you the most useful results.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Your Details")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("First name *", value=st.session_state.client_name,
                             placeholder="e.g. Sandra")
    with col2:
        business = st.text_input("Business name *", value=st.session_state.client_business,
                                 placeholder="e.g. Meridian Advisory")
    email = st.text_input("Email address *", value=st.session_state.client_email,
                          placeholder="e.g. sandra@meridiandvisory.com.au")

    st.markdown("---")
    st.subheader("Business Size")
    st.caption("Select the option that best describes your business.")

    size_options = {
        "Sole Trader": ("👤", "Just you — all digital decisions made by one person.", "1 person"),
        "Small Business": ("👥", "A growing team with some structure beginning to emerge.", "2 – 19 employees"),
        "Medium Business": ("🏢", "A more established organisation with defined roles and formal processes.", "20 – 199 employees"),
    }

    current_size = st.session_state.business_size
    cols = st.columns(3)
    for col, (size, (icon, desc, staff)) in zip(cols, size_options.items()):
        selected = current_size == size
        border = "2px solid #2E75B6" if selected else "2px solid #DEEAF1"
        bg = "#DEEAF1" if selected else "white"
        col.markdown(f"""
        <div style="border:{border};background:{bg};border-radius:10px;padding:16px;text-align:center;min-height:110px">
            <div style="font-size:2rem">{icon}</div>
            <div style="font-weight:700;color:#1F3864;font-size:0.9rem;margin:4px 0">{size}</div>
            <div style="font-size:0.75rem;color:#595959">{staff}</div>
        </div>
        """, unsafe_allow_html=True)
        if col.button(f"Select {size}", key=f"size_{size}", use_container_width=True,
                      type="primary" if selected else "secondary"):
            st.session_state.business_size = size
            st.rerun()

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # Validation & proceed
    errors = []
    if not name.strip():       errors.append("Please enter your first name.")
    if not business.strip():   errors.append("Please enter your business name.")
    if not email.strip():      errors.append("Please enter your email address.")
    if not st.session_state.business_size: errors.append("Please select a business size.")

    if st.button("Start Assessment →", type="primary", use_container_width=True):
        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.client_name = name.strip()
            st.session_state.client_business = business.strip()
            st.session_state.client_email = email.strip()
            st.session_state.current_pillar = 0
            st.session_state.page = "pillar"
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: PILLAR ASSESSMENT
# ═════════════════════════════════════════════════════════════════════════════
def page_pillar():
    idx = st.session_state.current_pillar   # 0-indexed
    pillar = PILLARS[idx]
    pid = pillar["id"]
    key = TIER_KEY[st.session_state.business_size]
    questions = pillar[key]

    render_header(f"{st.session_state.client_name}  ·  {st.session_state.client_business}")
    render_progress(idx + 1)

    answered = answered_count()
    st.progress(answered / 28, text=f"{answered} of 28 questions answered")
    st.markdown("")

    # Pillar header
    st.markdown(f"""
    <div class="pillar-header">
        <h2>{pillar['icon']}  Pillar {pid} of 7 — {pillar['name']}</h2>
        <p>{pillar['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Scoring rubric expander
    with st.expander("📖 Scoring guide for this pillar — click to expand"):
        for score, rubric in enumerate(pillar["rubric"], 1):
            st.markdown(f"**{score} — {list(SCORE_LABELS.values())[score-1].split(' — ')[1]}:** {rubric}")

    st.markdown("")

    # Questions
    score_vals = []
    for qi, q in enumerate(questions):
        st.markdown(f"<div class='question-card'><p>Q{qi+1}.&nbsp; {q}</p></div>", unsafe_allow_html=True)

        score_key = f"score_{pid}_{qi}"
        existing = st.session_state.get(score_key)

        # Pre-select index if already scored
        radio_options = list(SCORE_LABELS.values())
        idx_default = (existing - 1) if existing is not None else None

        chosen = st.radio(
            label=f"score_radio_{pid}_{qi}",
            options=radio_options,
            index=idx_default,
            horizontal=True,
            label_visibility="collapsed",
            key=f"radio_{pid}_{qi}",
        )
        if chosen is not None:
            # Extract numeric value from label
            val = int(chosen.split(" — ")[0])
            st.session_state[score_key] = val
            score_vals.append(val)
        else:
            score_vals.append(None)

        # Show description hint
        if chosen:
            val = int(chosen.split(" — ")[0])
            st.caption(f"ℹ️ {SCORE_DESCRIPTIONS[val]}")
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
        # Show pillar completion status
        complete = pillar_complete(pid)
        if complete:
            st.markdown("<div style='text-align:center;color:#70AD47;font-size:0.85rem;padding-top:8px'>✅ All questions in this pillar answered</div>", unsafe_allow_html=True)
        else:
            unanswered = sum(1 for qi in range(4) if st.session_state.get(f"score_{pid}_{qi}") is None)
            st.markdown(f"<div style='text-align:center;color:#ED7D31;font-size:0.85rem;padding-top:8px'>⚠️ {unanswered} question(s) still need a score</div>", unsafe_allow_html=True)

    with col_next:
        if idx < len(PILLARS) - 1:
            next_label = f"Next: {PILLARS[idx+1]['name'].split(' ')[0]}… →"
            if st.button(next_label, type="primary", use_container_width=True, disabled=not pillar_complete(pid)):
                st.session_state.current_pillar = idx + 1
                st.rerun()
        else:
            if st.button("See My Results →", type="primary", use_container_width=True, disabled=not all_complete()):
                st.session_state.page = "results"
                st.rerun()

    if idx == len(PILLARS) - 1 and not all_complete():
        st.warning("⚠️ Please answer all questions before viewing your results. Use '← Previous' to go back and complete any unanswered questions.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: RESULTS
# ═════════════════════════════════════════════════════════════════════════════
def make_radar_chart(results: dict) -> go.Figure:
    pillar_names = [f"P{p['id']} {p['name']}" for p in PILLARS]
    # Wrap long names
    pillar_labels = [
        "<br>".join(n.split(" ")[0:2]) + ("<br>" + " ".join(n.split(" ")[2:])) if len(n) > 20 else n
        for n in pillar_names
    ]
    short_labels = [f"P{p['id']} {p['name'].split(' ')[0]}" for p in PILLARS]
    values = [results["pillar_avgs"].get(p["id"], 0) for p in PILLARS]
    # Close the polygon
    values_closed = values + [values[0]]
    labels_closed = short_labels + [short_labels[0]]

    fig = go.Figure()

    # Fill area
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(46,117,182,0.2)",
        line=dict(color="#2E75B6", width=2),
        name="Your Score",
        hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
    ))

    # Max reference
    fig.add_trace(go.Scatterpolar(
        r=[5] * (len(short_labels) + 1),
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(200,200,200,0.08)",
        line=dict(color="#DDDDDD", width=1, dash="dot"),
        name="Maximum (5)",
        hovertemplate="Max: 5<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                tickfont=dict(size=10, color="#595959"),
                gridcolor="#E0E0E0",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#1F3864", family="Arial"),
                gridcolor="#E0E0E0",
            ),
            bgcolor="white",
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
        margin=dict(t=30, b=60, l=60, r=60),
        height=420,
        paper_bgcolor="white",
        font=dict(family="Arial"),
    )
    return fig


def page_results():
    scores = collect_scores()
    results = compute_results(scores)
    maturity = results["maturity"]
    level = maturity["level"]

    render_header(f"{st.session_state.client_name}  ·  {st.session_state.client_business}")
    render_progress(9)  # last step

    st.balloons()

    # ── Hero: maturity level ──────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:{maturity['color']};border-radius:12px;padding:24px 28px;margin-bottom:16px;border:2px solid {maturity['badge_bg']}">
        <div style="font-size:0.8rem;color:{maturity['text_color']};font-weight:600;text-transform:uppercase;letter-spacing:1px">
            Digital Maturity Level
        </div>
        <div style="font-size:2rem;font-weight:800;color:{maturity['text_color']};margin:4px 0">
            Level {level} — {maturity['label']}
        </div>
        <div style="font-size:0.85rem;color:{maturity['text_color']};opacity:0.85">
            Average score: {results['avg_score']:.2f} / 5.00  ·  {maturity['range']}
        </div>
        <div style="font-size:0.9rem;color:{maturity['text_color']};margin-top:10px">
            {maturity['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Top metrics ───────────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Average Score", f"{results['avg_score']:.2f} / 5.00")
    with m2:
        st.metric("Total Score", f"{results['total_score']} / 140")
    with m3:
        st.metric("Questions Answered", f"{results['answered']} / 28")

    st.markdown("---")

    # ── Radar chart ───────────────────────────────────────────────────────────
    st.subheader("📡 Digital Readiness by Pillar")
    fig = make_radar_chart(results)
    st.plotly_chart(fig, use_container_width=True)

    # ── Pillar scores table ───────────────────────────────────────────────────
    st.subheader("🏆 Pillar Breakdown")
    table_data = []
    for p in PILLARS:
        pid = p["id"]
        avg = results["pillar_avgs"].get(pid, 0)
        total = results["pillar_totals"].get(pid, 0)
        rubric_text = p["rubric"][round(avg) - 1] if 1 <= round(avg) <= 5 else "—"
        # Simple bar representation
        bar = "█" * round(avg * 2) + "░" * (10 - round(avg * 2))
        table_data.append({
            "Pillar": f"{p['icon']} {p['name']}",
            "Score": f"{avg:.1f}/5",
            "Total": f"{total}/20",
            "Progress": bar,
            "What this means": rubric_text,
        })

    df = pd.DataFrame(table_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Pillar": st.column_config.TextColumn("Pillar", width="medium"),
            "Score": st.column_config.TextColumn("Avg Score", width="small"),
            "Total": st.column_config.TextColumn("Total (/20)", width="small"),
            "Progress": st.column_config.TextColumn("Visual", width="small"),
            "What this means": st.column_config.TextColumn("At this score level…", width="large"),
        }
    )

    st.markdown("---")

    # ── Priority actions ──────────────────────────────────────────────────────
    st.subheader(f"🎯 Your Priority Actions — {maturity['label']}")
    st.markdown(f"Based on your Level {level} result, here are your top recommended actions:")
    for action in TOP_ACTIONS[level]:
        st.markdown(f"<div class='action-item'>{action}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Resources ─────────────────────────────────────────────────────────────
    with st.expander("📚 Key Australian Resources"):
        for name, url in RESOURCES:
            st.markdown(f"- [{name}]({url})")

    st.markdown("---")

    # ── PDF download ──────────────────────────────────────────────────────────
    st.subheader("📄 Download Your Report")
    st.markdown("Generate a branded PDF report with your scores, maturity level, and action plan.")

    if st.button("⬇️ Generate & Download PDF Report", type="primary", use_container_width=True):
        with st.spinner("Generating your personalised report…"):
            try:
                client_info = {
                    "name":     st.session_state.client_name,
                    "business": st.session_state.client_business,
                    "email":    st.session_state.client_email,
                    "size":     st.session_state.business_size,
                    "date":     date.today().strftime("%d %B %Y").lstrip("0"),
                }
                pdf_bytes = generate_pdf(client_info, results, PILLARS, MATURITY_LEVELS, TOP_ACTIONS, RESOURCES)
                filename = f"Digital_Readiness_{st.session_state.client_business.replace(' ', '_')}_{date.today().strftime('%Y%m%d')}.pdf"
                st.download_button(
                    label="📥 Click here to download your PDF",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.success("✅ Your report is ready!")
            except Exception as e:
                st.error(f"PDF generation error: {e}")
                st.info("Please take a screenshot of your results as an alternative.")

    st.markdown("---")

    # ── Restart ───────────────────────────────────────────────────────────────
    col_r, col_s = st.columns(2)
    with col_r:
        if st.button("🔄 Start a New Assessment", use_container_width=True):
            # Clear all state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col_s:
        if st.button("✏️ Revise My Answers", use_container_width=True):
            st.session_state.page = "pillar"
            st.session_state.current_pillar = 0
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═════════════════════════════════════════════════════════════════════════════
def main():
    init_state()

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
