"""
Digital Readiness Self-Assessment — PDF Report Generator
Uses ReportLab for layout and Matplotlib for the radar chart.
"""

import io
import math
import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak, KeepTogether,
)
from reportlab.platypus.flowables import BalancedColumns

# ── Colours ───────────────────────────────────────────────────────────────────
DARK_BLUE    = HexColor("#1F3864")
MED_BLUE     = HexColor("#2E75B6")
LIGHT_BLUE   = HexColor("#DEEAF1")
ACCENT_BLUE  = HexColor("#BDD7EE")
DARK_GREEN   = HexColor("#375623")
MED_GREEN    = HexColor("#70AD47")
LIGHT_GREEN  = HexColor("#E2EFDA")
ORANGE       = HexColor("#ED7D31")
LIGHT_ORANGE = HexColor("#FCE4D6")
PURPLE       = HexColor("#7030A0")
LIGHT_PURPLE = HexColor("#EAD1DC")
GOLD         = HexColor("#BF8F00")
LIGHT_GOLD   = HexColor("#FFF2CC")
GREY         = HexColor("#595959")
LIGHT_GREY   = HexColor("#F2F2F2")
WHITE        = white
BLACK        = black

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
CW = PAGE_W - 2 * MARGIN  # content width


# ── Styles ─────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    def add(name, parent="Normal", **kwargs):
        styles[name] = ParagraphStyle(name=name, parent=base[parent], **kwargs)

    add("title",       fontSize=22, textColor=WHITE,     alignment=TA_CENTER, spaceAfter=4, leading=26, fontName="Helvetica-Bold")
    add("subtitle",    fontSize=11, textColor=LIGHT_BLUE, alignment=TA_CENTER, spaceAfter=2, fontName="Helvetica")
    add("h1",          fontSize=14, textColor=DARK_BLUE,  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
    add("h2",          fontSize=12, textColor=MED_BLUE,   spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
    add("h3",          fontSize=10, textColor=DARK_BLUE,  spaceBefore=6,  spaceAfter=2, fontName="Helvetica-Bold")
    add("body",        fontSize=9,  textColor=black,      spaceAfter=4,   leading=13, fontName="Helvetica")
    add("body_small",  fontSize=8,  textColor=GREY,       spaceAfter=3,   leading=12, fontName="Helvetica")
    add("pillar_name", fontSize=10, textColor=WHITE,      fontName="Helvetica-Bold", leading=14)
    add("score_label", fontSize=9,  textColor=WHITE,      alignment=TA_CENTER, fontName="Helvetica")
    add("score_val",   fontSize=16, textColor=WHITE,      alignment=TA_CENTER, fontName="Helvetica-Bold")
    add("action",      fontSize=9,  textColor=black,      leftIndent=8,   spaceAfter=3, leading=13, fontName="Helvetica")
    add("resource",    fontSize=8,  textColor=MED_BLUE,   spaceAfter=3, fontName="Helvetica")
    add("footer",      fontSize=7,  textColor=GREY,       alignment=TA_CENTER, fontName="Helvetica")
    add("level_title", fontSize=18, textColor=white,      fontName="Helvetica-Bold", alignment=TA_CENTER, leading=22)
    add("level_sub",   fontSize=10, textColor=LIGHT_BLUE, alignment=TA_CENTER, fontName="Helvetica")

    return styles


# ── Radar chart (matplotlib → PNG bytes) ──────────────────────────────────────
def make_radar_png(results: dict, pillars: list) -> bytes:
    labels = [f"P{p['id']}\n{p['name'].split(' ')[0]}" for p in pillars]
    values = [results["pillar_avgs"].get(p["id"], 0) for p in pillars]
    N = len(labels)

    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    values_plot = values + values[:1]

    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#FAFCFE")

    # Grid
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=7, color="#AAAAAA")
    ax.yaxis.set_tick_params(pad=4)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=8, color="#1F3864", fontfamily="DejaVu Sans")
    ax.grid(color="#E0E0E0", linewidth=0.8)
    ax.spines["polar"].set_color("#CCCCCC")

    # Max fill
    ax.fill(angles, [5] * len(angles), color="#DDDDDD", alpha=0.12)

    # Data fill
    ax.plot(angles, values_plot, color="#2E75B6", linewidth=2, linestyle="solid")
    ax.fill(angles, values_plot, color="#2E75B6", alpha=0.25)

    # Data points
    ax.scatter(angles[:-1], values, color="#1F3864", s=40, zorder=5)

    # Labels at each point
    for angle, val, label in zip(angles[:-1], values, labels):
        ax.annotate(
            f"{val:.1f}",
            xy=(angle, val),
            xytext=(angle, val + 0.35),
            ha="center", va="center",
            fontsize=7.5, color="#1F3864", fontweight="bold",
        )

    plt.tight_layout(pad=1.2)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ── Score bar helper ───────────────────────────────────────────────────────────
def score_color(avg: float) -> HexColor:
    if avg < 2:   return HexColor("#ED7D31")
    if avg < 3:   return HexColor("#BF8F00")
    if avg < 3.5: return HexColor("#2E75B6")
    if avg < 4.5: return HexColor("#70AD47")
    return HexColor("#7030A0")


# ── Header/footer callbacks ───────────────────────────────────────────────────


# ── Main PDF generator ────────────────────────────────────────────────────────
def generate_pdf(client_info: dict, results: dict, pillars: list,
                 maturity_levels: list, top_actions: dict, resources: list,
                 logo_path=None) -> bytes:
    buf = io.BytesIO()
    styles = build_styles()
    maturity = results["maturity"]

    FOOTER_H  = 1.8 * cm          # space reserved at the bottom for the footer
    COVER_TOP = 4.5 * inch        # content starts 4.5 inches from top on cover page

    # ── Page frames ───────────────────────────────────────────────────────────
    # Cover frame: content begins 4.5 inches from the top (overlaid on samplePDF.pdf)
    cover_frame = Frame(
        MARGIN,
        FOOTER_H,
        CW,
        PAGE_H - COVER_TOP - FOOTER_H,
        id="cover",
    )
    # Body frame: normal top margin for all subsequent pages
    body_frame = Frame(
        MARGIN,
        FOOTER_H,
        CW,
        PAGE_H - MARGIN - FOOTER_H,
        id="body",
    )

    def on_cover_page(canvas, doc):
        _draw_header_footer(canvas, doc, client_info, is_cover=True, logo_path=logo_path)

    def on_body_page(canvas, doc):
        _draw_header_footer(canvas, doc, client_info, is_cover=False, logo_path=logo_path)

    doc = BaseDocTemplate(
        buf,
        pagesize=A4,
        title="Digital Readiness Self-Assessment Report",
        author=client_info.get("business", ""),
    )
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=on_cover_page),
        PageTemplate(id="Body",  frames=[body_frame],  onPage=on_body_page),
    ])

    story = []
    # Switch to Body template after the first PageBreak
    story.append(NextPageTemplate("Body"))

    # ══════════════════════════════════════════════════════
    # PAGE 1: CLIENT SUMMARY — overlaid onto samplePDF.pdf cover
    # ══════════════════════════════════════════════════════

    # Client info table
    client_rows = [
        ["Prepared for:", client_info.get("name", "")],
        ["Business:",     client_info.get("business", "")],
        ["Email:",        client_info.get("email", "")],
        ["Business size:", client_info.get("size", "")],
        ["Date:",         client_info.get("date", "")],
    ]
    client_tbl = Table(
        [[Paragraph(r, styles["h3"]), Paragraph(v, styles["body"])] for r, v in client_rows],
        colWidths=[4 * cm, CW - 4 * cm],
    )
    client_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), LIGHT_GREY),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GREY, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#DDDDDD")),
    ]))
    story.append(client_tbl)
    story.append(Spacer(1, 10 * mm))

    # Maturity level hero block
    mat_color    = HexColor(maturity["color"])
    mat_badge_bg = HexColor(maturity["badge_bg"])
    mat_text     = HexColor(maturity["text_color"])

    maturity_tbl = Table(
        [[
            Paragraph(f"Level {maturity['level']}", ParagraphStyle(
                "badge_lvl", fontName="Helvetica-Bold", fontSize=16,
                textColor=WHITE, alignment=TA_CENTER, leading=20)),
            Paragraph(
                f"{maturity['label']}<br/>"
                f"<font size='10' color='#FFFFFF'>Average score: {results['avg_score']:.2f} / 5.00  ·  {maturity['range']}</font><br/><br/>"
                f"<font size='9'>{maturity['description']}</font>",
                ParagraphStyle("badge_text", fontName="Helvetica-Bold", fontSize=16,
                               textColor=WHITE, leading=20)
            ),
        ]],
        colWidths=[2.5 * cm, CW - 2.5 * cm],
    )
    maturity_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), mat_badge_bg),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 18),
        ("LEFTPADDING",  (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        # Tight horizontal padding on the badge cell so "Level X" never wraps
        ("LEFTPADDING",  (0, 0), (0, -1),  4),
        ("RIGHTPADDING", (0, 0), (0, -1),  4),
        ("LINEAFTER",    (0, 0), (0, -1), 1, WHITE),
    ]))
    story.append(maturity_tbl)
    story.append(Spacer(1, 8 * mm))

    # Top-line metrics
    metrics = [
        (f"{results['avg_score']:.2f}/5.00", "Average Score"),
        (f"{results['total_score']}/140",    "Total Score"),
        (f"{results['answered']}/28",        "Questions Answered"),
    ]
    metrics_tbl = Table(
        [[Paragraph(v, styles["score_val"]) for v, _ in metrics],
         [Paragraph(l, styles["score_label"]) for _, l in metrics]],
        colWidths=[CW / 3] * 3,
    )
    metrics_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), DARK_BLUE),
        ("TEXTCOLOR",    (0, 0), (-1, -1), WHITE),
        ("TOPPADDING",   (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 12),
        ("INNERGRID",    (0, 0), (-1, -1), 0.3, MED_BLUE),
        ("BOX",          (0, 0), (-1, -1), 0, DARK_BLUE),
    ]))
    story.append(metrics_tbl)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # PAGE 2: RADAR CHART + PILLAR SCORES
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("Your Digital Readiness Profile", styles["h1"]))
    story.append(HRFlowable(width=CW, thickness=1, color=MED_BLUE, spaceAfter=6))

    # Radar chart
    radar_png = make_radar_png(results, pillars)
    radar_img = Image(io.BytesIO(radar_png), width=11 * cm, height=11 * cm)
    radar_img.hAlign = "CENTER"
    story.append(radar_img)
    story.append(Spacer(1, 4 * mm))

    # Pillar scores table
    story.append(Paragraph("Pillar Scores", styles["h2"]))

    col_widths = [0.8 * cm, 5.8 * cm, 1.8 * cm, 1.8 * cm, CW - 10.2 * cm]
    header_row = [
        Paragraph("#", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("Pillar", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE)),
        Paragraph("Avg/5", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("Tot/20", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("At this score…", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE)),
    ]
    p_rows = [header_row]
    for p in pillars:
        pid = p["id"]
        avg = results["pillar_avgs"].get(pid, 0)
        tot = results["pillar_totals"].get(pid, 0)
        rounded = max(1, min(5, round(avg))) if avg > 0 else 1
        rubric = p["rubric"][rounded - 1]
        p_rows.append([
            Paragraph(str(pid), ParagraphStyle("td_c", fontSize=8, alignment=TA_CENTER, fontName="Helvetica-Bold")),
            Paragraph(f"{p['icon']}  {p['name']}", styles["body"]),
            Paragraph(f"{avg:.1f}", ParagraphStyle("td_c", fontSize=9, alignment=TA_CENTER, fontName="Helvetica-Bold",
                                                    textColor=score_color(avg))),
            Paragraph(str(tot), ParagraphStyle("td_c", fontSize=9, alignment=TA_CENTER)),
            Paragraph(rubric, styles["body_small"]),
        ])

    p_tbl = Table(p_rows, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 0), (-1, -1), 0.3, HexColor("#DDDDDD")),
    ]
    for i in range(1, len(p_rows)):
        bg = LIGHT_BLUE if i % 2 == 0 else WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    p_tbl.setStyle(TableStyle(style_cmds))
    story.append(p_tbl)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # PAGE 3: ACTION PLAN
    # ══════════════════════════════════════════════════════
    story.append(Paragraph(f"Your Priority Action Plan — {maturity['label']}", styles["h1"]))
    story.append(HRFlowable(width=CW, thickness=1, color=MED_BLUE, spaceAfter=6))
    story.append(Paragraph(maturity["description"], styles["body"]))
    story.append(Spacer(1, 4 * mm))

    # Banner
    level_banner = Table(
        [[Paragraph(f"Level {maturity['level']}  ·  {maturity['label']}  ·  Average: {results['avg_score']:.2f}",
                    ParagraphStyle("banner", fontName="Helvetica-Bold", fontSize=12, textColor=WHITE, alignment=TA_CENTER))]],
        colWidths=[CW],
    )
    level_banner.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), mat_badge_bg),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
    ]))
    story.append(level_banner)
    story.append(Spacer(1, 6 * mm))

    # Actions
    for i, action in enumerate(top_actions[maturity["level"]], 1):
        action_row = Table(
            [[
                Paragraph(str(i), ParagraphStyle("num", fontName="Helvetica-Bold", fontSize=11,
                                                  textColor=WHITE, alignment=TA_CENTER)),
                Paragraph(action, styles["body"]),
            ]],
            colWidths=[0.7 * cm, CW - 0.7 * cm],
        )
        action_row.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (0, 0), mat_badge_bg),
            ("BACKGROUND",   (1, 0), (1, 0), mat_color),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",   (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
            ("LEFTPADDING",  (1, 0), (1, 0), 10),
            ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ]))
        story.append(action_row)
        story.append(Spacer(1, 1.5 * mm))

    story.append(Spacer(1, 6 * mm))

    # All 5 maturity level summaries
    story.append(Paragraph("All Maturity Levels — Reference Guide", styles["h2"]))
    story.append(Spacer(1, 2 * mm))
    for ml in maturity_levels:
        bg = HexColor(ml["color"])
        tc = HexColor(ml["text_color"])
        is_current = ml["level"] == maturity["level"]
        ml_row = Table(
            [[
                Paragraph(f"<b>L{ml['level']}</b>", ParagraphStyle("ml_num", fontSize=11 if is_current else 9,
                                                                     fontName="Helvetica-Bold", textColor=tc, alignment=TA_CENTER)),
                Paragraph(
                    f"<b>{ml['label']}</b>  <font size='8'>({ml['range']})</font>",
                    ParagraphStyle("ml_label", fontSize=9 if is_current else 8, fontName="Helvetica-Bold" if is_current else "Helvetica", textColor=tc)
                ),
            ]],
            colWidths=[1 * cm, CW - 1 * cm],
        )
        border_color = HexColor(ml["badge_bg"]) if is_current else HexColor("#DDDDDD")
        ml_row.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), bg),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",   (0, 0), (-1, -1), 6 if is_current else 4),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 6 if is_current else 4),
            ("LEFTPADDING",  (0, 0), (-1, -1), 8),
            ("BOX",          (0, 0), (-1, -1), 2 if is_current else 0.3, border_color),
        ]))
        story.append(ml_row)
        story.append(Spacer(1, 1 * mm))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # PAGE 4: RESOURCES + NEXT STEPS
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("Key Australian Resources", styles["h1"]))
    story.append(HRFlowable(width=CW, thickness=1, color=MED_BLUE, spaceAfter=6))

    for r_name, r_url in resources:
        res_row = Table(
            [[Paragraph(f"<b>{r_name}</b><br/><font size='7' color='#2E75B6'>{r_url}</font>", styles["body"])]],
            colWidths=[CW],
        )
        res_row.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), LIGHT_BLUE),
            ("TOPPADDING",   (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
            ("LEFTPADDING",  (0, 0), (-1, -1), 10),
            ("BOX",          (0, 0), (-1, -1), 0.3, HexColor("#AAAAAA")),
        ]))
        story.append(res_row)
        story.append(Spacer(1, 1.5 * mm))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Next Steps", styles["h2"]))
    story.append(Paragraph(
        "This report is your starting point. We recommend scheduling a 30-minute review session "
        "to discuss your results and agree on two or three priority actions to implement in the "
        "next 90 days. Reassess in 6–12 months to track your progress.",
        styles["body"],
    ))
    story.append(Spacer(1, 4 * mm))

    # About
    about_tbl = Table(
        [[Paragraph(
            "<b>About this Assessment</b><br/>"
            "This Digital Readiness Self-Assessment is aligned to the Australian Government Digital First "
            "Framework and the Australian Cyber Security Centre (ACSC) guidance. It is designed for "
            "professional services businesses in Australia.<br/><br/>"
            "<i>This report is confidential and intended for the use of the business named on the cover page only.</i>",
            styles["body_small"]
        )]],
        colWidths=[CW],
    )
    about_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), LIGHT_GREY),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("BOX",          (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
    ]))
    story.append(about_tbl)

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc.build(story)
    buf.seek(0)
    report_bytes = buf.read()

    # ── Merge: overlay generated page 1 onto samplePDF.pdf cover ─────────────
    # Page 1 of our report (client info at 4.5") is drawn ON TOP of the cover
    # template so the branding shows through behind it.
    # Pages 2-N of our report are appended unchanged.
    _app_dir   = logo_path.parent.parent if logo_path else None
    _cover_pdf = _app_dir / "samplePDF.pdf" if _app_dir else None

    if _cover_pdf and _cover_pdf.exists():
        try:
            from pypdf import PdfWriter, PdfReader
            cover_reader  = PdfReader(str(_cover_pdf))
            report_reader = PdfReader(io.BytesIO(report_bytes))

            writer = PdfWriter()

            # Page 1: cover template as base, our content overlaid on top
            cover_page = cover_reader.pages[0]
            cover_page.merge_page(report_reader.pages[0])
            writer.add_page(cover_page)

            # Pages 2-N: generated report pages as-is
            for page in report_reader.pages[1:]:
                writer.add_page(page)

            merged = io.BytesIO()
            writer.write(merged)
            merged.seek(0)
            return merged.read()
        except Exception:
            pass  # fall through and return un-merged report

    return report_bytes


def _draw_header_footer(canvas, doc, client_info, is_cover=False, logo_path=None):
    canvas.saveState()

    if not is_cover:
        # Header line
        canvas.setStrokeColor(MED_BLUE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_H - MARGIN + 4 * mm, PAGE_W - MARGIN, PAGE_H - MARGIN + 4 * mm)
        # Header text (left side)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(GREY)
        canvas.drawString(MARGIN, PAGE_H - MARGIN + 5 * mm, "Digital Readiness Self-Assessment Report")
        # Logo in header (right side), or text fallback
        if logo_path and hasattr(logo_path, "exists") and logo_path.exists():
            try:
                logo_h = 0.55 * cm
                from reportlab.lib.utils import ImageReader
                img_reader = ImageReader(str(logo_path))
                iw, ih = img_reader.getSize()
                logo_w = logo_h * (iw / ih)
                logo_x = PAGE_W - MARGIN - logo_w
                logo_y = PAGE_H - MARGIN + 3 * mm
                canvas.drawImage(str(logo_path), logo_x, logo_y,
                                 width=logo_w, height=logo_h, preserveAspectRatio=True, mask="auto")
            except Exception:
                canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 5 * mm,
                                       f"{client_info.get('business', '')}  ·  {client_info.get('date', '')}")
        else:
            canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 5 * mm,
                                   f"{client_info.get('business', '')}  ·  {client_info.get('date', '')}")

    # Footer
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)
    canvas.setStrokeColor(LIGHT_BLUE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.2 * cm, PAGE_W - MARGIN, 1.2 * cm)
    canvas.drawCentredString(
        PAGE_W / 2, 0.7 * cm,
        f"Meridian Digital Advisory  ·  Digital Readiness Self-Assessment  ·  {client_info.get('business', '')}  "
        f"·  {client_info.get('date', '')}  ·  Page {doc.page}",
    )

    canvas.restoreState()
