"""
F.O.C.U.S. Futures Trade Projections (FFTP) — User Documentation
Jachbit 2026  |  generate_docs.py

Run: python generate_docs.py
Requires: pip install reportlab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from datetime import datetime
import os

# ── Brand Colors ─────────────────────────────────────────────────────────────
NAVY       = colors.Color(0.0,      0.168627, 0.360784)
ORANGE     = colors.Color(0.901961, 0.360784, 0.0)
DARK_GREY  = colors.Color(0.266667, 0.266667, 0.266667)
BLACK      = colors.black
WHITE      = colors.white
LIGHT_GREY = colors.Color(0.94, 0.94, 0.94)
MID_GREY   = colors.Color(0.82, 0.82, 0.82)
ROW_ALT    = colors.Color(0.97, 0.97, 0.97)
GREEN_DARK = colors.Color(0.05, 0.38, 0.15)
RED_DARK   = colors.Color(0.55, 0.10, 0.02)
BLUE_MID   = colors.Color(0.10, 0.35, 0.65)

# ── Page Geometry ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN_L = MARGIN_R = 48.0
MARGIN_T = MARGIN_B = 52.0
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

PROJECT_TITLE = "F.O.C.U.S. — Futures Trade Projections (FFTP)"
NOW_STR  = datetime.now().strftime("%Y-%m-%d %H:%M")
DATE_STR = datetime.now().strftime("%Y-%m-%d")

# ── Style Factory ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=9, leading=13,
             textColor=BLACK, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

CTIT_S  = S("ct",  fontName="Helvetica-Bold", fontSize=22, textColor=NAVY,      leading=28, alignment=TA_CENTER)
CSUB_S  = S("cs",  fontSize=11, textColor=ORANGE, leading=15, alignment=TA_CENTER)
CDATE_S = S("cd",  fontSize=8,  textColor=DARK_GREY, leading=12, alignment=TA_CENTER)
DISC_S  = S("ds",  fontName="Helvetica-Oblique", fontSize=7.5, textColor=DARK_GREY, leading=11, alignment=TA_CENTER)
SEC_S   = S("sc",  fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,  leading=14)
BODY_S  = S("bd",  fontSize=8.5, textColor=BLACK,     leading=13)
BOLD_S  = S("bo",  fontName="Helvetica-Bold", fontSize=8.5, textColor=BLACK, leading=13)
NAVY_S  = S("nv",  fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY,  leading=13)
SMALL_S = S("sm",  fontSize=7.5, textColor=DARK_GREY, leading=11)
WARN_S  = S("wn",  fontName="Helvetica-Bold", fontSize=8.5, textColor=RED_DARK, leading=13)
BUL_S   = S("bl",  fontSize=8.5, textColor=BLACK, leading=13, leftIndent=14)
BUL2_S  = S("bl2", fontSize=8,   textColor=DARK_GREY, leading=12, leftIndent=26)
TH_S    = S("th",  fontName="Helvetica-Bold", fontSize=8, textColor=NAVY,  leading=11, alignment=TA_CENTER)
TD_S    = S("td",  fontSize=8,   textColor=BLACK, leading=11, alignment=TA_CENTER)
TD_L    = S("tdl", fontSize=8,   textColor=BLACK, leading=11, alignment=TA_LEFT)
TD_B    = S("tdb", fontName="Helvetica-Bold", fontSize=8, textColor=NAVY,  leading=11, alignment=TA_LEFT)
TD_G    = S("tdg", fontName="Helvetica-Bold", fontSize=8, textColor=GREEN_DARK, leading=11, alignment=TA_CENTER)
TD_O    = S("tdo", fontName="Helvetica-Bold", fontSize=8, textColor=ORANGE, leading=11, alignment=TA_CENTER)

# ── Page Header / Footer ──────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, PAGE_H - 30, PAGE_W, 30, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, PAGE_H - 32, PAGE_W, 2, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(MARGIN_L, PAGE_H - 19, PROJECT_TITLE)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(DARK_GREY)
    canvas.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 19, f"Jachbit 2026  |  {DATE_STR}")
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, 22, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, 22, PAGE_W, 1.5, fill=1, stroke=0)
    canvas.setFillColor(DARK_GREY)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(PAGE_W / 2, 8,
        "For educational and planning purposes only. Not financial advice. Trade responsibly.")
    canvas.setFillColor(NAVY)
    canvas.drawRightString(PAGE_W - MARGIN_R, 8, f"Page {doc.page}")
    canvas.restoreState()

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(n=6):
    return Spacer(1, n)

def section_bar(text):
    return KeepTogether([
        Paragraph(text, SEC_S),
        HRFlowable(width=CONTENT_W, thickness=1.5, color=ORANGE, spaceAfter=0, spaceBefore=3),
    ])

def orange_rule():
    return HRFlowable(width=CONTENT_W, thickness=1.5, color=ORANGE, spaceAfter=8, spaceBefore=4)

def grey_rule():
    return HRFlowable(width=CONTENT_W, thickness=0.5, color=MID_GREY, spaceAfter=6, spaceBefore=4)

def bullet(text, sub=False):
    sty = BUL2_S if sub else BUL_S
    prefix = "–" if sub else "•"
    return Paragraph(f"{prefix}  {text}", sty)

def std_table_style():
    return TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND",    (0, 0), (-1,  0), LIGHT_GREY),
        ("LINEBELOW",     (0, 0), (-1,  0), 1.5, ORANGE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, ROW_ALT]),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.3, MID_GREY),
        ("BOX",           (0, 0), (-1, -1), 0.7, MID_GREY),
        ("GRID",          (0, 0), (-1, -1), 0.3, MID_GREY),
    ])

def info_style():
    return TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [WHITE, ROW_ALT]),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.4, MID_GREY),
        ("LINEAFTER",     (0, 0), (0,  -1), 1.5, ORANGE),
        ("BOX",           (0, 0), (-1, -1), 0.7, MID_GREY),
    ])

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       f"FFTP_User_Guide_{ts}.pdf")

    doc = SimpleDocTemplate(
        out, pagesize=letter,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T,  bottomMargin=MARGIN_B,
        title="FFTP User Guide — F.O.C.U.S. Futures Trade Projections",
        author="Jachbit 2026",
    )

    story = []

    # ── Title Block ───────────────────────────────────────────────────────────
    story += [
        sp(10),
        Paragraph("F.O.C.U.S.STOCKS", CSUB_S),
        sp(6),
        Paragraph("Futures Trade Projections", CTIT_S),
        sp(4),
        Paragraph("FFTP — User Guide &amp; Quick Reference", CDATE_S),
        sp(4),
        Paragraph(f"Generated: {NOW_STR}  ·  Jachbit 2026", DISC_S),
        sp(12),
        orange_rule(),
        sp(4),
    ]

    # ── What Is FFTP ──────────────────────────────────────────────────────────
    story.append(section_bar("WHAT IS FFTP?"))
    story += [sp(8),
        Paragraph(
            "F.O.C.U.S. Futures Trade Projections (FFTP) is a free, browser-based planning tool "
            "for futures traders. It helps you project capital growth over 52 weeks using a "
            "<b>conservative, disciplined contract scaling strategy</b> — you add exactly one "
            "contract for every starting-capital increment of profit you earn. No guessing, "
            "no over-leveraging, no emotion.", BODY_S),
        sp(6),
        Paragraph(
            "Your data is saved automatically in your own browser. Nobody else can see or "
            "overwrite it — each user keeps their own private copy.", BODY_S),
        sp(10),
    ]

    # ── Access ────────────────────────────────────────────────────────────────
    story.append(section_bar("HOW TO ACCESS"))
    story += [sp(8),
        Paragraph("Open your web browser and go to:", BODY_S),
        sp(4),
        Paragraph("https://jachbit.github.io/FFTP", S("url",
            fontName="Helvetica-Bold", fontSize=10, textColor=BLUE_MID,
            leading=14, alignment=TA_CENTER)),
        sp(6),
        Paragraph(
            "Works on any device — desktop, laptop, tablet, or mobile phone. "
            "No app to install, no account to create, no login required.", BODY_S),
        sp(10),
    ]

    # ── Contract Scaling Rule ─────────────────────────────────────────────────
    story.append(section_bar("THE GOLDEN RULE — CONTRACT SCALING"))
    story += [sp(8),
        Paragraph(
            "The core discipline of FFTP is simple and conservative:", BODY_S),
        sp(6),
    ]

    rule_data = [
        [Paragraph("RULE", TH_S), Paragraph("DETAIL", TH_S)],
        [Paragraph("Starting point", TD_B),
         Paragraph("Begin with your chosen Starting Contracts at your Starting Capital. Default is 1 contract — e.g. 3 contracts at $5,000.", TD_L)],
        [Paragraph("When to add contracts", TD_B),
         Paragraph("Each time your running equity grows by another Starting Capital increment of profit, add Starting Contracts more.", TD_L)],
        [Paragraph("Maximum increment per week", TD_B),
         Paragraph("Always one level only — even if a big week crosses multiple thresholds, only one upgrade fires per week.", TD_L)],
        [Paragraph("Never skip levels", TD_B),
         Paragraph("The app enforces this automatically — you earn each contract increment one step at a time.", TD_L)],
        [Paragraph("Flexible scaling", TD_B),
         Paragraph("Set Starting Contracts = 1 for the most conservative plan (+1 each upgrade). Set to 3 for faster scaling (+3 each upgrade). The discipline is the same either way.", TD_L)],
        [Paragraph("Why?", TD_B),
         Paragraph("Prevents over-leveraging during a hot streak. Capital growth is earned contract by contract, level by level.", TD_L)],
    ]
    rule_t = Table(rule_data, colWidths=[CONTENT_W * 0.28, CONTENT_W * 0.72])
    rule_t.setStyle(std_table_style())
    story += [rule_t, sp(8)]

    # Two side-by-side examples
    ex_label_s = S("exl", fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY, leading=12)
    story += [
        Paragraph("Example A — Conservative: $1,500 capital, Starting Contracts = 1 (MNQ, 16 pts/day)", ex_label_s),
        sp(4),
    ]
    ex_data_a = [
        [Paragraph("Running Equity", TH_S), Paragraph("Profit Earned", TH_S),
         Paragraph("Contracts", TH_S), Paragraph("Daily Profit @ $2/pt", TH_S)],
        [Paragraph("$1,500", TD_S), Paragraph("$0",     TD_S), Paragraph("1",  TD_O), Paragraph("16 pts = $32/day",  TD_S)],
        [Paragraph("$3,000", TD_S), Paragraph("$1,500", TD_S), Paragraph("2",  TD_G), Paragraph("16 pts = $64/day",  TD_S)],
        [Paragraph("$4,500", TD_S), Paragraph("$3,000", TD_S), Paragraph("3",  TD_G), Paragraph("16 pts = $96/day",  TD_S)],
        [Paragraph("$6,000", TD_S), Paragraph("$4,500", TD_S), Paragraph("4",  TD_G), Paragraph("16 pts = $128/day", TD_S)],
        [Paragraph("$7,500", TD_S), Paragraph("$6,000", TD_S), Paragraph("5",  TD_G), Paragraph("16 pts = $160/day", TD_S)],
        [Paragraph("$9,000", TD_S), Paragraph("$7,500", TD_S), Paragraph("6",  TD_G), Paragraph("16 pts = $192/day", TD_S)],
    ]
    ex_t_a = Table(ex_data_a, colWidths=[CONTENT_W*0.25]*4)
    ex_t_a.setStyle(std_table_style())
    story += [ex_t_a, sp(8),
        Paragraph("Example B — Faster scaling: $5,000 capital, Starting Contracts = 3 (MNQ, 16 pts/day)", ex_label_s),
        sp(4),
    ]
    ex_data_b = [
        [Paragraph("Running Equity", TH_S), Paragraph("Profit Earned", TH_S),
         Paragraph("Contracts", TH_S), Paragraph("Daily Profit @ $2/pt", TH_S)],
        [Paragraph("$5,000",  TD_S), Paragraph("$0",      TD_S), Paragraph("3",  TD_O), Paragraph("16 pts = $96/day",  TD_S)],
        [Paragraph("$10,000", TD_S), Paragraph("$5,000",  TD_S), Paragraph("6",  TD_G), Paragraph("16 pts = $192/day", TD_S)],
        [Paragraph("$15,000", TD_S), Paragraph("$10,000", TD_S), Paragraph("9",  TD_G), Paragraph("16 pts = $288/day", TD_S)],
        [Paragraph("$20,000", TD_S), Paragraph("$15,000", TD_S), Paragraph("12", TD_G), Paragraph("16 pts = $384/day", TD_S)],
        [Paragraph("$25,000", TD_S), Paragraph("$20,000", TD_S), Paragraph("15", TD_G), Paragraph("16 pts = $480/day", TD_S)],
        [Paragraph("$30,000", TD_S), Paragraph("$25,000", TD_S), Paragraph("18", TD_G), Paragraph("16 pts = $576/day", TD_S)],
    ]
    ex_t_b = Table(ex_data_b, colWidths=[CONTENT_W*0.25]*4)
    ex_t_b.setStyle(std_table_style())
    story += [ex_t_b, sp(10)]

    # ── Three Tabs ────────────────────────────────────────────────────────────
    story.append(section_bar("THE THREE TABS"))
    story += [sp(8)]

    tabs_data = [
        [Paragraph("TAB", TH_S), Paragraph("PURPOSE", TH_S), Paragraph("KEY FEATURES", TH_S)],
        [Paragraph("Projection", TD_B),
         Paragraph("52-week capital growth forecast", TD_L),
         Paragraph("Equity curve chart · Contract scaling table · PDF &amp; CSV export", TD_L)],
        [Paragraph("Trading Log", TD_B),
         Paragraph("Record your real daily trades", TD_L),
         Paragraph("Per-row instrument P&amp;L · Milestone alerts · Running equity tracker", TD_L)],
        [Paragraph("Target Tables", TD_B),
         Paragraph("Set your income goals by year", TD_L),
         Paragraph("Daily &amp; annual targets · Instrument values reference · Both fully editable", TD_L)],
    ]
    tabs_t = Table(tabs_data, colWidths=[CONTENT_W*0.18, CONTENT_W*0.32, CONTENT_W*0.50])
    tabs_t.setStyle(std_table_style())
    story += [tabs_t, sp(10)]

    # ── Tab 1: Projection ─────────────────────────────────────────────────────
    story.append(section_bar("TAB 1 — PROJECTION"))
    story += [sp(8),
        Paragraph("<b>Setup inputs (top bar):</b>", BODY_S), sp(4),
        bullet("Instrument: choose MNQ/NQ (Nasdaq) or MES/ES (S&amp;P 500)"),
        bullet("Contract Size: Micro or Mini"),
        bullet("Starting Capital ($): your account size — this is also the profit increment that triggers a contract upgrade"),
        bullet("Risk % Per Day: shows your max daily risk in dollars and suggested points target"),
        bullet("Daily Points Target: how many points you aim to capture per trading day"),
        bullet("Plan Start Date: the Monday your plan begins — weekly dates auto-fill"),
        bullet("Starting Contracts: how many contracts to begin with (default 1). Each upgrade adds this same number."),
        bullet("Weeks to Project: default 52 (1 year)"),
        sp(8),
        Paragraph("<b>Risk Calculator strip:</b>", BODY_S), sp(4),
        Paragraph(
            "When you enter a Risk % and Starting Capital, the strip shows your dollar risk "
            "and the equivalent points target for your chosen instrument. Click "
            "<b>Use This Target</b> to apply it instantly.", BODY_S),
        sp(8),
        Paragraph("<b>Summary cards:</b>", BODY_S), sp(4),
        Paragraph(
            "Final Equity · Total Profit · Total Return · Max Contracts · Avg Weekly Profit · "
            "Plan End Date — all update every time you click Recalculate.", BODY_S),
        sp(8),
        Paragraph("<b>Projection table:</b>", BODY_S), sp(4),
        bullet("Shows every week: equity start, contracts, points, profit, equity end, % week, % month"),
        bullet("Month-end rows are highlighted with an orange border"),
        bullet("Contract upgrade weeks show a ▲ indicator"),
        bullet("Week dates are editable — click any date to override (e.g. if you skipped a week)"),
        sp(10),
    ]

    # ── Tab 2: Trading Log ────────────────────────────────────────────────────
    story.append(section_bar("TAB 2 — TRADING LOG"))
    story += [sp(8),
        Paragraph(
            "The Trading Log is where you record what actually happened each day vs. your plan. "
            "It tracks your real running equity and tells you exactly when to size up.", BODY_S),
        sp(8),
        Paragraph("<b>Each log row contains:</b>", BODY_S), sp(4),
        bullet("Date · No Trade checkbox · Instrument (all 14 contracts supported)"),
        bullet("Target Pts — your planned daily points"),
        bullet("Actual Pts — what you really captured (positive for wins, negative for losses)"),
        bullet("Contracts · Fees ($) · Notes"),
        bullet("Gross P&L, Net P&L, and vs Plan calculated automatically per row"),
        sp(8),
    ]

    # Winning / Losing / No Trade table
    wl_data = [
        [Paragraph("SCENARIO", TH_S), Paragraph("WHAT TO ENTER", TH_S), Paragraph("RESULT", TH_S)],
        [Paragraph("Winning day", S("w", fontName="Helvetica-Bold", fontSize=8, textColor=GREEN_DARK, leading=11)),
         Paragraph("Enter a <b>positive</b> number in Actual Pts — e.g. +12", TD_L),
         Paragraph("P&L shown in green, added to running equity", TD_L)],
        [Paragraph("Losing day", S("l", fontName="Helvetica-Bold", fontSize=8, textColor=RED_DARK, leading=11)),
         Paragraph("Enter a <b>negative</b> number in Actual Pts — e.g. -8", TD_L),
         Paragraph("P&L shown in red, deducted from running equity", TD_L)],
        [Paragraph("No trade", S("n", fontName="Helvetica-Bold", fontSize=8, textColor=DARK_GREY, leading=11)),
         Paragraph("Tick the <b>No Trade</b> checkbox", TD_L),
         Paragraph("Row is greyed out, zero P&L, equity unchanged", TD_L)],
    ]
    wl_t = Table(wl_data, colWidths=[CONTENT_W*0.18, CONTENT_W*0.42, CONTENT_W*0.40])
    wl_t.setStyle(std_table_style())
    story += [wl_t, sp(8),
        Paragraph("<b>Milestone alerts:</b>", BODY_S), sp(4),
        Paragraph(
            "A green banner appears in the log <i>after</i> the trade row that pushed your "
            "running equity past the next $startingCapital threshold. It tells you exactly "
            "how many contracts to move to — you decide when to act on it.", BODY_S),
        sp(6),
        Paragraph(
            "Example: Starting Capital = $1,500. After a trade your running equity crosses "
            "$3,000 — the banner fires: <b>Add 1 contract → now 2 contracts.</b>", BODY_S),
        sp(8),
        Paragraph("<b>Summary strip (top of log):</b>", BODY_S), sp(4),
        Paragraph(
            "Days Logged · Days Traded · Total Actual Pts · Target Pts · Pts vs Plan · "
            "Gross P&amp;L · Net P&amp;L (after fees) · Avg Pts/Day", BODY_S),
        sp(10),
    ]

    # ── Tab 3: Target Tables ──────────────────────────────────────────────────
    story.append(section_bar("TAB 3 — TARGET TABLES"))
    story += [sp(8),
        Paragraph(
            "Two editable reference tables to guide your long-term planning:", BODY_S),
        sp(8),
    ]

    tgt_data = [
        [Paragraph("TABLE", TH_S), Paragraph("COLUMNS / STRUCTURE", TH_S), Paragraph("NOTES", TH_S)],
        [Paragraph("Income Goals", TD_B),
         Paragraph("Year · Daily Target ($) · Annual Target ($) · Age · Notes", TD_L),
         Paragraph("Annual auto-calculates as Daily × 240 trading days. Editable to override. Change Year in row 1 — all rows cascade automatically.", TD_L)],
        [Paragraph("Instrument Values", TD_B),
         Paragraph("Instrument · Tick ($) · Point ($) · # Ticks/Point · Notes", TD_L),
         Paragraph("Reference sheet for all 14 supported futures contracts. All cells editable.", TD_L)],
        [Paragraph("Stock Scalping Share Sizing", TD_B),
         Paragraph("Matrix: Price Move (rows) × Shares (columns) = Profit ($)", TD_L),
         Paragraph("Add/remove rows and columns freely. Values auto-calculated. PDF export available.", TD_L)],
    ]
    tgt_t = Table(tgt_data, colWidths=[CONTENT_W*0.22, CONTENT_W*0.37, CONTENT_W*0.41])
    tgt_t.setStyle(std_table_style())
    story += [tgt_t, sp(8),
        Paragraph("<b>Stock Scalping Share Sizing — sample (default values):</b>", BODY_S), sp(4),
    ]

    # Share sizing sample matrix
    share_moves = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    share_sizes = [200, 300, 400, 500, 1000, 2000, 3000]
    sh_head = [Paragraph("MOVE ↓ / SHARES →", TH_S)] + [Paragraph(str(s), TH_S) for s in share_sizes]
    sh_body = []
    for m in share_moves:
        row = [Paragraph(f"${m:.2f}", S("mo", fontName="Helvetica-Bold", fontSize=8, textColor=ORANGE, leading=11))]
        for s in share_sizes:
            profit = int(m * s)
            row.append(Paragraph(f"${profit:,}", S("pr", fontName="Helvetica-Bold", fontSize=8, textColor=GREEN_DARK, leading=11)))
        sh_body.append(row)
    sh_cw = [CONTENT_W * 0.14] + [CONTENT_W * 0.86 / len(share_sizes)] * len(share_sizes)
    sh_t = Table([sh_head] + sh_body, colWidths=sh_cw)
    sh_t.setStyle(std_table_style())
    story += [sh_t, sp(10)]

    # ── Instruments Supported ─────────────────────────────────────────────────
    story.append(section_bar("SUPPORTED INSTRUMENTS"))
    story += [sp(8)]

    ins_data = [
        [Paragraph("MICRO", TH_S), Paragraph("MINI", TH_S),
         Paragraph("MICRO $/PT", TH_S), Paragraph("MINI $/PT", TH_S), Paragraph("MARKET", TH_S)],
        [Paragraph("MNQ", TD_O), Paragraph("NQ",  TD_S), Paragraph("$2",    TD_G), Paragraph("$20",   TD_S), Paragraph("Nasdaq 100", TD_L)],
        [Paragraph("MES", TD_O), Paragraph("ES",  TD_S), Paragraph("$5",    TD_G), Paragraph("$50",   TD_S), Paragraph("S&amp;P 500", TD_L)],
        [Paragraph("MGC", TD_O), Paragraph("GC",  TD_S), Paragraph("$10",   TD_G), Paragraph("$100",  TD_S), Paragraph("Gold", TD_L)],
        [Paragraph("M2K", TD_O), Paragraph("RTY", TD_S), Paragraph("$5",    TD_G), Paragraph("$50",   TD_S), Paragraph("Russell 2000", TD_L)],
        [Paragraph("MYM", TD_O), Paragraph("YM",  TD_S), Paragraph("$1",    TD_G), Paragraph("$5",    TD_S), Paragraph("Dow Jones", TD_L)],
        [Paragraph("MCL", TD_O), Paragraph("CL",  TD_S), Paragraph("$100",  TD_G), Paragraph("$1,000",TD_S), Paragraph("Crude Oil", TD_L)],
        [Paragraph("SIL", TD_O), Paragraph("SI",  TD_S), Paragraph("$500",  TD_G), Paragraph("$5,000",TD_S), Paragraph("Silver", TD_L)],
    ]
    ins_cw = [CONTENT_W*0.13, CONTENT_W*0.13, CONTENT_W*0.15,
              CONTENT_W*0.15, CONTENT_W*0.44]
    ins_t = Table(ins_data, colWidths=ins_cw)
    ins_t.setStyle(std_table_style())
    story += [ins_t,
        sp(6),
        Paragraph("Note: 10 Micros = 1 Mini for most instruments (MYM/YM is 5:1).", SMALL_S),
        sp(10),
    ]

    # ── CSV & PDF Export ──────────────────────────────────────────────────────
    story.append(section_bar("SAVING, EXPORTING &amp; SHARING DATA"))
    story += [sp(8)]

    save_data = [
        [Paragraph("FEATURE", TH_S), Paragraph("HOW TO USE", TH_S), Paragraph("NOTES", TH_S)],
        [Paragraph("Auto-Save", TD_B),
         Paragraph("Happens automatically on every change", TD_L),
         Paragraph("Data stored in your browser's localStorage — no internet needed to save", TD_L)],
        [Paragraph("Export CSV", TD_B),
         Paragraph("Click Export CSV on the Projection tab", TD_L),
         Paragraph("Downloads a spreadsheet of your full projection table", TD_L)],
        [Paragraph("Import CSV", TD_B),
         Paragraph("Click Import CSV and select a previously exported file", TD_L),
         Paragraph("Restores your projection on any device or browser", TD_L)],
        [Paragraph("Export Log CSV", TD_B),
         Paragraph("Click Export Log CSV on the Trading Log tab", TD_L),
         Paragraph("Downloads all your trade log entries", TD_L)],
        [Paragraph("PDF Export", TD_B),
         Paragraph("Click Export PDF on any tab", TD_L),
         Paragraph("Generates a white-background PDF: Projection, Log, Goals, Instruments, or Share Sizing", TD_L)],
    ]
    save_t = Table(save_data, colWidths=[CONTENT_W*0.18, CONTENT_W*0.37, CONTENT_W*0.45])
    save_t.setStyle(std_table_style())
    story += [save_t, sp(10)]

    # ── Important Notes ───────────────────────────────────────────────────────
    story.append(section_bar("IMPORTANT NOTES"))
    story += [sp(8),
        bullet("Your data is <b>private to your own browser</b>. Other users cannot see or change it."),
        bullet("If you clear your browser cache or use a different browser, your data will be lost."),
        bullet("<b>Export CSV regularly</b> to keep a backup of your projection and trading log."),
        bullet("To move your data to a new device: Export CSV on the old device, Import CSV on the new one."),
        bullet("The projection is a <b>planning tool only</b> — actual results depend on your trading performance."),
        bullet("Always trade within your risk parameters. Contracts should only be increased after profits are confirmed."),
        sp(10),
        Paragraph(
            "For support or feedback, contact Jachbit 2026.", SMALL_S),
        sp(4),
        Paragraph(
            "For educational and planning purposes only. Not financial advice. Trade responsibly.",
            S("disc2", fontName="Helvetica-Oblique", fontSize=7.5,
              textColor=RED_DARK, leading=11)),
    ]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"\nPDF generated: {out}\n")

if __name__ == "__main__":
    build()
