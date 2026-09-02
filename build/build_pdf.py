"""Build the Universal DI Framework PMO Model brief.

Canon (per EgD-BOOT-001):
- Cream/orange palette; Fraunces (display) + Inter (body).
- EVEglyph rotated watermark on every page.
- Header line: "EVEglyphDesign · Controlled copy" + EgD-KEY-2026-07.
- Footer: SHA-256 (first 16), ISO-8601 UTC timestamp, "Page X of N",
  closing mark "Pour le bien-être du peuple".
- Two-pass build: pass one discovers the page count; pass two stamps it.
- Clickable links only.
- Lilian named at the top of the PDF (public site is team-only; PDF names her).
"""

from __future__ import annotations

import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.platypus.flowables import Flowable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diagrams import (  # noqa: E402
    three_sovereignties,
    team_triangle,
    wall_diagram,
    surfaces_flow,
    repo_scope,
)
from content import (  # noqa: E402
    TITLE,
    TAGLINE,
    LEAD,
    VERSION,
    LEDE,
    SURFACES,
    TEAM_HEADING,
    TEAM_PARAS,
    CALLOUT_KICKER,
    CALLOUT,
    COMPARE_HEADING,
    COMPARE_INTRO,
    COMPARE_LEFT_HEADER,
    COMPARE_RIGHT_HEADER,
    COMPARE_ROWS,
    CLOSING_LINE,
    FRAMEWORK_HEADING,
    FRAMEWORK_PARA,
    FRAMEWORK_LINKS,
    CTA_HEADING,
    CTA_PARA,
    CTA_LABEL,
    CTA_URL,
)

# --- Canon --------------------------------------------------------------

CREAM = HexColor("#fdfaf4")
CREAM2 = HexColor("#f7f2e7")
INK = HexColor("#1a1a1a")
LINE = HexColor("#e7e1d3")
MUTE = HexColor("#6b665c")
ORANGE = HexColor("#e87722")

KEY_ID = "EgD-KEY-2026-07"
CLOSING = "Pour le bien-être du peuple"

OUT_DIR = Path(__file__).resolve().parent.parent / "docs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "EVEglyphDesign_Universal_DI_PMO.pdf"
OUT_PATH_PHONE = OUT_DIR / "EVEglyphDesign_Universal_DI_PMO_phone.pdf"
LUZID_SVG = OUT_DIR / "luzid-wordmark.svg"


class SVGImage(Flowable):
    """Flowable that renders an SVG file at a target height, aspect kept."""

    def __init__(self, path: Path, height: float):
        super().__init__()
        self._path = str(path)
        self._target_h = height
        drawing = svg2rlg(self._path)
        self._raw_w = drawing.width
        self._raw_h = drawing.height
        self._scale = height / drawing.height
        self.width = drawing.width * self._scale
        self.height = height

    def draw(self):
        drawing = svg2rlg(self._path)
        drawing.scale(self._scale, self._scale)
        drawing.width = self.width
        drawing.height = self.height
        renderPDF.draw(drawing, self.canv, 0, 0)


class DiagramFlowable(Flowable):
    """Flowable that scales a reportlab.graphics Drawing to a target width.
    Aspect ratio preserved."""

    def __init__(self, drawing, target_width: float):
        super().__init__()
        self._raw = drawing
        self._raw_w = drawing.width
        self._raw_h = drawing.height
        self._scale = target_width / drawing.width
        self.width = target_width
        self.height = drawing.height * self._scale

    def draw(self):
        d = self._raw
        d.scale(self._scale, self._scale)
        d.width = self.width
        d.height = self.height
        renderPDF.draw(d, self.canv, 0, 0)

# Phone-first page: narrow enough that fit-to-width on a 390px phone
# renders body text around 14-16pt effective size. 100mm x 178mm is a
# tall, phone-aspect page with generous type.
PHONE_PAGE = (100 * mm, 178 * mm)
PHONE_MARGIN_SIDE = 7.5 * mm
PHONE_MARGIN_TOP = 14 * mm
PHONE_MARGIN_BOTTOM = 14 * mm


# --- Fonts --------------------------------------------------------------

def _register_fonts() -> tuple[str, str, str, str]:
    candidates = {
        "Fraunces": [
            "/usr/share/fonts/truetype/fraunces/Fraunces-Regular.ttf",
        ],
        "Fraunces-Bold": [
            "/usr/share/fonts/truetype/fraunces/Fraunces-Bold.ttf",
        ],
        "Inter": [
            "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
        ],
        "Inter-Bold": [
            "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
        ],
    }
    resolved = {}
    for name, paths in candidates.items():
        for p in paths:
            if Path(p).exists():
                try:
                    pdfmetrics.registerFont(TTFont(name, p))
                    resolved[name] = name
                    break
                except Exception:
                    continue
    display = resolved.get("Fraunces", "Times-Roman")
    display_bold = resolved.get("Fraunces-Bold", "Times-Bold")
    body = resolved.get("Inter", "Helvetica")
    body_bold = resolved.get("Inter-Bold", "Helvetica-Bold")
    return display, display_bold, body, body_bold


DISPLAY, DISPLAY_BOLD, BODY, BODY_BOLD = _register_fonts()


# --- Styles -------------------------------------------------------------

def _styles(phone: bool = False):
    scale = 1.55 if phone else 1.0
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow", fontName=BODY_BOLD, fontSize=8 * scale, leading=10 * scale,
            textColor=ORANGE, spaceAfter=6, alignment=TA_LEFT,
        ),
        "title": ParagraphStyle(
            "title", fontName=DISPLAY_BOLD,
            fontSize=(22 if phone else 26), leading=(26 if phone else 30),
            textColor=INK, spaceAfter=6,
        ),
        "tagline": ParagraphStyle(
            "tagline", fontName=DISPLAY,
            fontSize=(14 if phone else 15), leading=(18 if phone else 19),
            textColor=MUTE, spaceAfter=14,
        ),
        "lead": ParagraphStyle(
            "lead", fontName=BODY_BOLD, fontSize=9.5 * scale, leading=12 * scale,
            textColor=INK, spaceAfter=2,
        ),
        "version": ParagraphStyle(
            "version", fontName=BODY, fontSize=8.5 * scale, leading=11 * scale,
            textColor=MUTE, spaceAfter=16,
        ),
        "lede": ParagraphStyle(
            "lede", fontName=DISPLAY,
            fontSize=(13 if phone else 13.5), leading=(18 if phone else 19),
            textColor=INK, spaceAfter=18, alignment=TA_LEFT,
        ),
        "h2": ParagraphStyle(
            "h2", fontName=DISPLAY_BOLD,
            fontSize=(17 if phone else 16), leading=(22 if phone else 20),
            textColor=INK, spaceBefore=18, spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "h3", fontName=DISPLAY_BOLD,
            fontSize=(14 if phone else 12.5), leading=(18 if phone else 16),
            textColor=INK, spaceBefore=12, spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body", fontName=BODY, fontSize=10 * scale, leading=14 * scale,
            textColor=INK, spaceAfter=8, alignment=TA_LEFT,
        ),
        "ref": ParagraphStyle(
            "ref", fontName=BODY, fontSize=8.5 * scale, leading=11 * scale,
            textColor=MUTE, spaceAfter=4, alignment=TA_LEFT,
        ),
        "callout": ParagraphStyle(
            "callout", fontName=BODY, fontSize=10 * scale, leading=14 * scale,
            textColor=INK, spaceAfter=0, alignment=TA_LEFT,
            leftIndent=10, rightIndent=6,
        ),
        "cellhead": ParagraphStyle(
            "cellhead", fontName=BODY_BOLD, fontSize=8.5 * scale, leading=11 * scale,
            textColor=INK,
        ),
        "cell_left": ParagraphStyle(
            "cell_left", fontName=BODY, fontSize=8.5 * scale, leading=11.5 * scale,
            textColor=INK,
        ),
        "cell_right": ParagraphStyle(
            "cell_right", fontName=BODY, fontSize=8.5 * scale, leading=11.5 * scale,
            textColor=INK,
        ),
        "rowlabel": ParagraphStyle(
            "rowlabel", fontName=BODY_BOLD, fontSize=8 * scale, leading=10 * scale,
            textColor=ORANGE, spaceAfter=2, spaceBefore=2,
        ),
        "compare_head_left": ParagraphStyle(
            "compare_head_left", fontName=BODY_BOLD, fontSize=9 * scale,
            leading=11 * scale, textColor=ORANGE,
        ),
        "compare_head_right": ParagraphStyle(
            "compare_head_right", fontName=BODY_BOLD, fontSize=9 * scale,
            leading=11 * scale, textColor=MUTE,
        ),
        "stack_label": ParagraphStyle(
            "stack_label", fontName=BODY_BOLD, fontSize=9.5, leading=12,
            textColor=ORANGE, spaceBefore=8, spaceAfter=2,
        ),
        "stack_value_left": ParagraphStyle(
            "stack_value_left", fontName=BODY, fontSize=12, leading=16,
            textColor=INK, spaceAfter=4,
        ),
        "stack_value_right": ParagraphStyle(
            "stack_value_right", fontName=BODY, fontSize=12, leading=16,
            textColor=MUTE, spaceAfter=8,
        ),
        "closing": ParagraphStyle(
            "closing", fontName=DISPLAY_BOLD,
            fontSize=(13 if phone else 13), leading=(17 if phone else 17),
            textColor=ORANGE, spaceBefore=8, spaceAfter=6, alignment=TA_LEFT,
        ),
        "link": ParagraphStyle(
            "link", fontName=BODY, fontSize=9.5 * scale, leading=13 * scale,
            textColor=ORANGE, spaceAfter=3, leftIndent=12,
            bulletIndent=2,
        ),
        "cta_label": ParagraphStyle(
            "cta_label", fontName=BODY_BOLD, fontSize=11 * scale, leading=14 * scale,
            textColor=INK, spaceAfter=3,
        ),
        "cta_body": ParagraphStyle(
            "cta_body", fontName=BODY, fontSize=10 * scale, leading=14 * scale,
            textColor=INK, spaceAfter=6,
        ),
        "cta_link": ParagraphStyle(
            "cta_link", fontName=BODY_BOLD, fontSize=11 * scale, leading=14 * scale,
            textColor=ORANGE, spaceAfter=0,
        ),
    }


# --- Page frames --------------------------------------------------------

def _draw_page_chrome(c: canvas.Canvas, doc, phone: bool, sha_short: str,
                      built_at: str, total_pages: int | None):
    width, height = c._pagesize
    # Watermark: rotated "EVEglyph" faint diagonal
    c.saveState()
    c.setFont(DISPLAY, 60 if not phone else 42)
    c.setFillColor(HexColor("#f2ecdd"))
    c.translate(width / 2, height / 2)
    c.rotate(30)
    c.drawCentredString(0, 0, "EVEglyph")
    c.restoreState()

    # Header
    c.saveState()
    c.setFont(BODY, 7.5 if not phone else 7)
    c.setFillColor(MUTE)
    header_y = height - (10 * mm if not phone else 6 * mm)
    if phone:
        c.drawString(PHONE_MARGIN_SIDE, header_y,
                     f"EVEglyphDesign · Controlled copy · {KEY_ID}")
    else:
        c.drawString(0.75 * inch(), header_y,
                     "EVEglyphDesign · Controlled copy")
        c.drawRightString(width - 0.75 * inch(), header_y, KEY_ID)
    c.restoreState()

    # Footer
    c.saveState()
    c.setFont(BODY, 7 if not phone else 6.5)
    c.setFillColor(MUTE)
    footer_y = 8 * mm if not phone else 6 * mm
    page_str = (f"Page {doc.page} of {total_pages}"
                if total_pages is not None else f"Page {doc.page}")
    stamp = f"SHA-256 {sha_short} · {built_at}"
    if phone:
        c.drawString(PHONE_MARGIN_SIDE, footer_y, stamp)
        c.drawRightString(width - PHONE_MARGIN_SIDE, footer_y, page_str)
        # closing mark
        c.setFont(DISPLAY, 7)
        c.setFillColor(ORANGE)
        c.drawCentredString(width / 2, footer_y - 3 * mm, CLOSING)
    else:
        c.drawString(0.75 * inch(), footer_y, stamp)
        c.drawRightString(width - 0.75 * inch(), footer_y, page_str)
        c.setFont(DISPLAY, 8.5)
        c.setFillColor(ORANGE)
        c.drawCentredString(width / 2, footer_y - 4 * mm, CLOSING)
    c.restoreState()


def inch():
    from reportlab.lib.units import inch as _inch
    return _inch


# --- Story --------------------------------------------------------------

def _link(text: str, url: str) -> str:
    return f'<a href="{url}" color="#e87722"><u>{text}</u></a>'


def _build_story(phone: bool, content_width: float | None = None):
    S = _styles(phone=phone)
    story = []

    def diagram(fn, caption: str | None = None, target_w: float | None = None):
        """Insert a scaled diagram plus optional caption. Desktop-only —
        phone stays text-only."""
        if phone or content_width is None:
            return
        w = target_w if target_w is not None else content_width
        drawing = fn()
        story.append(Spacer(1, 6))
        story.append(DiagramFlowable(drawing, w))
        if caption:
            story.append(Spacer(1, 2))
            story.append(Paragraph(caption, S["ref"]))
        story.append(Spacer(1, 8))

    # Header block
    story.append(Paragraph("EVEglyphDesign · PMO offering", S["eyebrow"]))
    story.append(Paragraph(TITLE, S["title"]))
    story.append(Paragraph(TAGLINE, S["tagline"]))
    story.append(Paragraph(LEAD, S["lead"]))
    story.append(Paragraph(VERSION, S["version"]))

    # Lede
    story.append(Paragraph(LEDE, S["lede"]))

    # Sovereignty definitional slide — opens the argument.
    diagram(three_sovereignties,
            caption="Data quality starts with sovereignty scoping. "
                    "Structured-data checks are the symptom, not the fix.")

    # Section: What you get
    story.append(Paragraph("What you get", S["h2"]))
    story.append(Paragraph(
        "Four things, delivered by the team, kept by you.", S["body"]))

    # Surfaces flow diagram at the top of "What you get".
    diagram(surfaces_flow,
            caption="Four surfaces, one repository. "
                    "Everything the team produces lands in the client’s "
                    "Client Sovereign repo.")

    for s in SURFACES:
        # No KeepTogether on phone: reference and body should flow with the
        # heading rather than force blank pages when a block is too tall.
        block = [
            Paragraph(s["name"], S["h3"]),
            Paragraph(f'<b>{s["ref_kicker"]}</b> <i>{s["ref"]}</i>', S["ref"]),
            Paragraph(s["body"], S["body"]),
        ]
        if phone:
            story.extend(block)
        else:
            story.append(KeepTogether(block))

    # Team block
    story.append(Paragraph(TEAM_HEADING, S["h2"]))
    for p in TEAM_PARAS:
        story.append(Paragraph(p, S["body"]))

    # Team triangle: Lilian at the apex, four consultants + their
    # individual sovereign twins below.
    diagram(team_triangle,
            caption="Lilian keeps the programme moving. "
                    "Each consultant runs their own Individual Sovereign twin.")

    # Callout
    callout_text = f'<b><font color="#e87722">{CALLOUT_KICKER}</font></b> {CALLOUT}'
    callout_para = Paragraph(callout_text, S["callout"])
    callout_tbl = Table(
        [[callout_para]],
        colWidths=[None],
    )
    callout_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM2),
        ("LINEBEFORE", (0, 0), (0, -1), 2, ORANGE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(Spacer(1, 4))
    story.append(callout_tbl)
    story.append(Spacer(1, 8))

    # DMZ vs rented model — sits right after the trade-secret callout.
    diagram(wall_diagram,
            caption="Reasoning built inside your DMZ stays yours. "
                    "Reasoning built on a vendor’s cloud accumulates on "
                    "their side of the wall.")

    # DMZ-bound repo scope — what the twin sees inside the wall.
    story.append(Paragraph("Inside the boundary, what the twin sees",
                           S["h3"]))
    story.append(Paragraph(
        "The context reasoning repository is the twin’s working memory: "
        "the unstructured and semi-structured project record on one side, "
        "and read-only connectivity to your Client Sovereign data estate "
        "on the other. Planning and execution assumptions are reasoned "
        "against the actual business data — something no company should "
        "ever want done outside their DMZ.",
        S["body"]))
    diagram(repo_scope,
            caption="Nothing on this page ever leaves the DMZ. That is the point.")

    # Comparison section
    story.append(Paragraph(COMPARE_HEADING, S["h2"]))
    story.append(Paragraph(COMPARE_INTRO, S["body"]))

    if phone:
        # Stacked cards on phone. For the row where the right value is
        # literally "Luzid.", replace the kicker to avoid the comic
        # "Luzid. Luzid." double.
        for label, left, right in COMPARE_ROWS:
            story.append(Paragraph(label, S["stack_label"]))
            story.append(Paragraph(
                f'<b><font color="#e87722">Our model.</font></b> {left}',
                S["stack_value_left"]))
            right_stripped = right.strip().rstrip(".")
            if right_stripped.lower() == "luzid":
                story.append(Paragraph(
                    f'<b><font color="#6b665c">Luzid.</font></b>',
                    S["stack_value_right"]))
            else:
                story.append(Paragraph(
                    f'<b><font color="#6b665c">Luzid.</font></b> {right}',
                    S["stack_value_right"]))
    else:
        # Real side-by-side table on desktop. Luzid wordmark rendered
        # in the right header cell above the label.
        right_cells = []
        if LUZID_SVG.exists():
            try:
                right_cells.append(SVGImage(LUZID_SVG, height=14))
                right_cells.append(Spacer(1, 3))
            except Exception:
                pass
        right_cells.append(Paragraph("packaged AI assistant",
                                     S["compare_head_right"]))
        header_row = [
            Paragraph(COMPARE_LEFT_HEADER, S["compare_head_left"]),
            right_cells,
        ]
        data = [header_row]
        row_bg_flags = [False]  # track which rows are label rows
        for label, left, right in COMPARE_ROWS:
            # Label row spans both cols
            data.append([Paragraph(label, S["rowlabel"]), ""])
            row_bg_flags.append("label")
            data.append([
                Paragraph(left, S["cell_left"]),
                Paragraph(right, S["cell_right"]),
            ])
            row_bg_flags.append(False)
        tbl = Table(data, colWidths=[3.25 * inch(), 3.25 * inch()])
        ts = [
            ("BACKGROUND", (0, 0), (-1, 0), CREAM2),
            ("LINEBELOW", (0, 0), (-1, 0), 0.75, LINE),
            ("LINEAFTER", (0, 0), (0, -1), 0.5, LINE),
            ("BOX", (0, 0), (-1, -1), 0.75, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
        for i, flag in enumerate(row_bg_flags):
            if flag == "label":
                ts.append(("SPAN", (0, i), (-1, i)))
                ts.append(("BACKGROUND", (0, i), (-1, i), CREAM2))
                ts.append(("LINEBELOW", (0, i), (-1, i), 0.5, LINE))
                ts.append(("TOPPADDING", (0, i), (-1, i), 6))
                ts.append(("BOTTOMPADDING", (0, i), (-1, i), 3))
            elif i > 0:
                ts.append(("LINEBELOW", (0, i), (-1, i), 0.5, LINE))
                ts.append(("BACKGROUND", (0, i), (0, i),
                           HexColor("#faf5ea")))
        tbl.setStyle(TableStyle(ts))
        story.append(tbl)

    story.append(Spacer(1, 8))
    story.append(Paragraph(CLOSING_LINE, S["closing"]))

    # Framework block
    story.append(Paragraph(FRAMEWORK_HEADING, S["h2"]))
    story.append(Paragraph(FRAMEWORK_PARA, S["body"]))
    for label, url in FRAMEWORK_LINKS:
        story.append(Paragraph(
            f'• {_link(label, url)}', S["link"]))

    # CTA
    story.append(Spacer(1, 12))
    story.append(Paragraph(CTA_HEADING, S["h2"]))
    story.append(Paragraph(CTA_PARA, S["cta_body"]))
    story.append(Paragraph(_link(CTA_LABEL + " → " + CTA_URL, CTA_URL),
                           S["cta_link"]))

    return story


# --- Build passes -------------------------------------------------------

def _build_pdf(out_path: Path, phone: bool, total_pages: int | None,
               sha_short: str, built_at: str) -> tuple[int, bytes]:
    if phone:
        pagesize = PHONE_PAGE
        left = PHONE_MARGIN_SIDE
        right = PHONE_MARGIN_SIDE
        top = PHONE_MARGIN_TOP
        bottom = PHONE_MARGIN_BOTTOM
    else:
        pagesize = LETTER
        left = right = 0.75 * inch()
        top = 0.85 * inch()
        bottom = 0.75 * inch()

    doc = BaseDocTemplate(
        str(out_path),
        pagesize=pagesize,
        leftMargin=left,
        rightMargin=right,
        topMargin=top,
        bottomMargin=bottom,
        title=TITLE,
        author="EVEglyphDesign",
        subject="Universal DI Framework PMO Model",
    )
    frame = Frame(
        left, bottom,
        pagesize[0] - left - right,
        pagesize[1] - top - bottom,
        id="normal",
        showBoundary=0,
    )

    def _on_page(c, d):
        _draw_page_chrome(c, d, phone, sha_short, built_at, total_pages)

    doc.addPageTemplates([
        PageTemplate(id="main", frames=[frame], onPage=_on_page),
    ])
    content_width = pagesize[0] - left - right
    story = _build_story(phone=phone, content_width=content_width)
    doc.build(story)

    data = out_path.read_bytes()
    # Count pages using pdfminer-free approach: look for /Type /Page (not /Pages)
    # Robust enough for reportlab output
    import re
    pages_matches = len(re.findall(rb"/Type\s*/Page[^s]", data))
    return pages_matches, data


def build(phone: bool) -> Path:
    out_path = OUT_PATH_PHONE if phone else OUT_PATH
    # Pass 1: build without page count to discover it
    built_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_pages, data = _build_pdf(out_path, phone, None, "PENDING", built_at)
    sha_short = hashlib.sha256(data).hexdigest()[:16]
    # Pass 2: rebuild with real page count and real sha of the content shape
    total_pages, data = _build_pdf(out_path, phone, total_pages, sha_short,
                                   built_at)
    # Third pass to stabilise SHA of final rendered bytes
    final_sha = hashlib.sha256(out_path.read_bytes()).hexdigest()[:16]
    print(f"[build] {out_path.name}: {total_pages} pages · SHA {final_sha}")
    return out_path


def main():
    build(phone=False)
    build(phone=True)


if __name__ == "__main__":
    main()
