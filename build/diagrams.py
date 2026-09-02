"""
Vector diagrams for the Universal DI Framework PMO Model PDF.

All shapes are drawn with reportlab primitives so they render crisp at any
zoom and add no external asset dependency. Palette matches EgD canon:
cream #fdfaf4, cream-2 #f7f2e7, ink #1a1a1a, line #e7e1d3, mute #6b665c,
accent orange #e87722.
"""

from reportlab.graphics.shapes import (
    Drawing, Rect, Polygon, Line, String, Group, Circle,
)
from reportlab.lib.colors import HexColor

CREAM   = HexColor("#fdfaf4")
CREAM2  = HexColor("#f7f2e7")
INK     = HexColor("#1a1a1a")
LINE    = HexColor("#e7e1d3")
MUTE    = HexColor("#6b665c")
ACCENT  = HexColor("#e87722")

FONT_BODY = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def _label(x, y, text, size=8, color=INK, anchor="middle", bold=False):
    s = String(x, y, text, textAnchor=anchor)
    s.fontName = FONT_BOLD if bold else FONT_BODY
    s.fontSize = size
    s.fillColor = color
    return s


def three_sovereignties(width=680, height=440):
    """
    Sovereignty as the first move in data quality.

    Frame: SAP programmes routinely audit structured business data
    (ACDOCA, master data, mappings) and call that "data quality."
    That is a symptom-level check. The wider problem is the quality
    of the reasoning behind the numbers — workshop context,
    decisions, corrections, assumptions — and that reasoning is what
    Individual / Client / Vendor Sovereign scoping actually decides.

    Slide reads top-down:
      1. Symptom band: structured-data-only quality checks.
      2. Root band: three sovereignty columns showing where the
         reasoning lives, since that is what data-quality scoping
         should have been about all along.
      3. Bottom line: sovereignty scoping is the first data-quality
         decision on the programme.
    """
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=CREAM2, strokeColor=None))

    # Title band
    d.add(_label(width / 2, height - 24,
                 "Data quality starts with sovereignty scoping",
                 size=13, color=INK, bold=True))
    d.add(_label(width / 2, height - 40,
                 "structured-data-only checks are the symptom, not the fix",
                 size=8, color=MUTE))

    # ---------- Symptom band ----------
    sb_x = 20
    sb_w = width - 40
    sb_y = height - 130
    sb_h = 74
    d.add(Rect(sb_x, sb_y, sb_w, sb_h,
               fillColor=CREAM, strokeColor=MUTE, strokeWidth=0.9,
               strokeDashArray=[3, 2]))
    d.add(_label(sb_x + 14, sb_y + sb_h - 16,
                 "Symptom — what most SAP programmes check today",
                 size=10, color=MUTE, bold=True, anchor="start"))
    sym_items = [
        "ACDOCA and master-data integrity",
        "Field mappings and reconciliations",
        "Row counts, duplicates, referential checks",
    ]
    # Two-column layout inside the band
    for i, txt in enumerate(sym_items):
        col = i % 3
        x = sb_x + 14 + col * (sb_w / 3)
        y = sb_y + sb_h - 40
        d.add(Circle(x + 4, y + 4, 1.8, fillColor=MUTE, strokeColor=MUTE))
        d.add(_label(x + 14, y, txt, size=9, color=INK, anchor="start"))
    d.add(_label(sb_x + sb_w / 2, sb_y + 12,
                 "This is a symptom-level check. Necessary. Not sufficient.",
                 size=9, color=MUTE, bold=True))

    # Down arrow from symptom to root
    ar_x = width / 2
    ar_top = sb_y - 4
    ar_bot = sb_y - 22
    line = Line(ar_x, ar_top, ar_x, ar_bot + 6)
    line.strokeColor = ACCENT
    line.strokeWidth = 2
    d.add(line)
    d.add(Polygon([
        ar_x - 5, ar_bot + 6,
        ar_x + 5, ar_bot + 6,
        ar_x,     ar_bot,
    ], fillColor=ACCENT, strokeColor=ACCENT))
    d.add(_label(ar_x, ar_bot - 12,
                 "root cause: where does the reasoning live?",
                 size=9, color=ACCENT, bold=True))

    # Three columns — sit below the symptom band + arrow
    col_top = height - 178
    col_bot = 60
    col_h = col_top - col_bot
    gap = 14
    col_w = (width - 40 - 2 * gap) / 3
    xs = [20, 20 + col_w + gap, 20 + 2 * (col_w + gap)]
    header_pad = 14

    # Column definitions: (title, subtitle, owner, holds[], on_exit, header_color, border_color)
    cols = [
        (
            "Individual",
            "Sovereign",
            "the consultant",
            [
                "Their own kit and identity",
                "Their working methods",
                "Their personal twin",
                "Portable across engagements",
                "Reads, but does not retain, data",
            ],
            "Goes home with the consultant.",
            INK, INK,
        ),
        (
            "Client",
            "Sovereign",
            "the client",
            [
                "Their DMZ and network",
                "Their existing data estate",
                "The context reasoning repository",
                "Every decision, spec, and correction",
                "Their trade secret — stays here",
            ],
            "Stays with the client.",
            ACCENT, ACCENT,
        ),
        (
            "Vendor",
            "Sovereign",
            "the packaged platform",
            [
                "Their cloud and their login",
                "Their agent and their models",
                "Client context put in during use",
                "The reasoning built on their side",
                "Their asset — accumulates there",
            ],
            "Stays with the vendor.",
            MUTE, MUTE,
        ),
    ]

    for x, (t1, t2, owner, items, on_exit, hdr_col, border_col) in zip(xs, cols):
        # Column card
        dashed = (border_col == MUTE)
        d.add(Rect(x, col_bot, col_w, col_h,
                   fillColor=CREAM, strokeColor=border_col,
                   strokeWidth=1.2,
                   strokeDashArray=[3, 2] if dashed else None))

        # Header block
        d.add(_label(x + header_pad, col_top - 22, t1,
                     size=15, color=hdr_col, bold=True, anchor="start"))
        d.add(_label(x + header_pad, col_top - 38, t2,
                     size=15, color=hdr_col, bold=True, anchor="start"))
        d.add(_label(x + header_pad, col_top - 54,
                     f"owner: {owner}",
                     size=9, color=MUTE, anchor="start"))

        # Divider under header
        div_y = col_top - 62
        div = Line(x + header_pad, div_y, x + col_w - header_pad, div_y)
        div.strokeColor = LINE
        div.strokeWidth = 0.8
        d.add(div)

        # "holds" label
        d.add(_label(x + header_pad, div_y - 14,
                     "holds", size=8, color=MUTE, bold=True, anchor="start"))

        # Bulleted list
        list_top = div_y - 30
        line_h = 17
        for i, item in enumerate(items):
            y = list_top - i * line_h
            d.add(Circle(x + header_pad + 4, y + 4, 1.8,
                         fillColor=hdr_col, strokeColor=hdr_col))
            d.add(_label(x + header_pad + 14, y, item,
                         size=9, color=INK, anchor="start"))

        # Divider before on-exit
        exit_div_y = col_bot + 40
        div2 = Line(x + header_pad, exit_div_y,
                    x + col_w - header_pad, exit_div_y)
        div2.strokeColor = LINE
        div2.strokeWidth = 0.8
        d.add(div2)

        # On engagement end
        d.add(_label(x + header_pad, exit_div_y - 14,
                     "when the engagement ends",
                     size=8, color=MUTE, bold=True, anchor="start"))
        d.add(_label(x + header_pad, exit_div_y - 27, on_exit,
                     size=9, color=hdr_col, bold=True, anchor="start"))

    # Bottom caption
    d.add(_label(width / 2, 30,
                 "Sovereignty scoping is the first data-quality decision on the programme.",
                 size=10, color=INK, bold=True))
    d.add(_label(width / 2, 16,
                 "The PMO builds inside Client Sovereign, using Individual Sovereign twins, and never crosses into Vendor Sovereign.",
                 size=8, color=MUTE))

    # Outer frame
    d.add(Rect(0, 0, width, height, fillColor=None,
               strokeColor=LINE, strokeWidth=0.75))
    return d


def team_triangle(width=480, height=210):
    """
    Lilian at the apex with four consultant triangles beneath, each with
    its own twin. Shows the "everyone runs their own twin, Lilian sits at
    the top of the triangles" story.
    """
    d = Drawing(width, height)

    # Background band
    d.add(Rect(0, 0, width, height, fillColor=CREAM2, strokeColor=None))

    # Apex triangle (Lilian)
    apex_cx = width / 2
    apex_cy = height - 32
    apex = Polygon([
        apex_cx - 34, apex_cy - 22,
        apex_cx + 34, apex_cy - 22,
        apex_cx,      apex_cy + 22,
    ])
    apex.fillColor = ACCENT
    apex.strokeColor = ACCENT
    d.add(apex)
    d.add(_label(apex_cx, apex_cy - 3, "Lilian", size=9, color=CREAM, bold=True))
    d.add(_label(apex_cx, apex_cy - 14, "Practice Lead", size=7, color=CREAM))

    # Four consultant triangles beneath
    n = 4
    margin = 40
    span = width - 2 * margin
    step = span / (n - 1)
    tri_cy = 68
    for i in range(n):
        cx = margin + step * i
        tri = Polygon([
            cx - 26, tri_cy - 18,
            cx + 26, tri_cy - 18,
            cx,      tri_cy + 18,
        ])
        tri.fillColor = CREAM
        tri.strokeColor = INK
        tri.strokeWidth = 1
        d.add(tri)
        d.add(_label(cx, tri_cy - 2, f"Consultant {i+1}", size=7, color=INK, bold=True))
        d.add(_label(cx, tri_cy - 11, "+ twin", size=6, color=MUTE))

        # Line from apex down to this triangle
        line = Line(apex_cx, apex_cy - 22, cx, tri_cy + 18)
        line.strokeColor = MUTE
        line.strokeWidth = 0.6
        d.add(line)

        # Twin marker (small circle to the right of each triangle)
        tw_cx = cx + 34
        tw_cy = tri_cy - 4
        c = Circle(tw_cx, tw_cy, 5)
        c.fillColor = ACCENT
        c.strokeColor = ACCENT
        d.add(c)
        d.add(_label(tw_cx, tw_cy - 2, "T", size=6, color=CREAM, bold=True))

    # Bottom caption band
    d.add(_label(width / 2, 18,
                 "Every consultant runs their own twin. Lilian keeps the programme moving as one thing.",
                 size=7, color=MUTE))

    # Frame
    d.add(Rect(0, 0, width, height, fillColor=None, strokeColor=LINE, strokeWidth=0.75))
    return d


def wall_diagram(width=520, height=280):
    """
    DMZ vs rented model. Left panel: AI model running inside the client
    DMZ, context reasoning stays with the client. Right panel: rented
    model on a vendor cloud, client data and context reasoning cross
    the boundary to be processed on the vendor's side.

    The point the diagram must make in one glance: the reasoning
    that gets built up over a project — workshops, decisions,
    language, patterns, priorities — is a trade secret. It either
    accumulates inside the DMZ (yours forever) or accumulates on a
    rented platform (theirs the moment the contract ends).
    """
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=CREAM2, strokeColor=None))

    wall_x = width / 2
    top = height - 32
    bot = 56

    # ---------- Left panel: inside the DMZ ----------
    lx = 20
    lw = wall_x - lx - 14
    d.add(Rect(lx, bot, lw, top - bot,
               fillColor=CREAM, strokeColor=INK, strokeWidth=0.9))
    d.add(_label(lx + lw / 2, top - 14, "Inside your DMZ",
                 size=10, color=INK, bold=True))
    d.add(_label(lx + lw / 2, top - 26, "AI model runs on your systems",
                 size=7, color=MUTE))

    # Model box
    mbx = lx + 18
    mby = bot + 108
    mbw = lw - 36
    d.add(Rect(mbx, mby, mbw, 40, fillColor=ACCENT, strokeColor=ACCENT))
    d.add(_label(mbx + mbw / 2, mby + 25, "AI model",
                 size=10, color=CREAM, bold=True))
    d.add(_label(mbx + mbw / 2, mby + 12, "open weights or private endpoint",
                 size=7, color=CREAM))

    # Context reasoning vault
    cbx = lx + 18
    cby = bot + 30
    cbw = lw - 36
    d.add(Rect(cbx, cby, cbw, 62, fillColor=CREAM2,
               strokeColor=INK, strokeWidth=0.8))
    d.add(_label(cbx + cbw / 2, cby + 48, "Context reasoning",
                 size=9, color=INK, bold=True))
    d.add(_label(cbx + cbw / 2, cby + 36, "workshops · decisions · language",
                 size=7, color=MUTE))
    d.add(_label(cbx + cbw / 2, cby + 26, "patterns · priorities · corrections",
                 size=7, color=MUTE))
    d.add(_label(cbx + cbw / 2, cby + 12,
                 "your trade secret — accumulates here",
                 size=7, color=ACCENT, bold=True))

    # Arrow: model reads from context, stays inside
    l1 = Line(cbx + cbw / 2, cby + 62, mbx + mbw / 2, mby)
    l1.strokeColor = INK
    l1.strokeWidth = 0.9
    d.add(l1)
    d.add(_label(cbx + cbw / 2 + 40, cby + 66,
                 "reads + writes", size=6, color=MUTE))

    # ---------- Wall ----------
    wall = Line(wall_x, bot - 32, wall_x, top + 6)
    wall.strokeColor = ACCENT
    wall.strokeWidth = 3
    d.add(wall)
    d.add(_label(wall_x, top + 16, "YOUR BOUNDARY",
                 size=8, color=ACCENT, bold=True))

    # ---------- Right panel: rented vendor model ----------
    rx = wall_x + 14
    rw = width - rx - 20
    d.add(Rect(rx, bot, rw, top - bot,
               fillColor=CREAM, strokeColor=MUTE, strokeWidth=0.9,
               strokeDashArray=[3, 2]))
    d.add(_label(rx + rw / 2, top - 14, "Rented model, vendor cloud",
                 size=10, color=MUTE, bold=True))
    d.add(_label(rx + rw / 2, top - 26, "AI model runs on their systems",
                 size=7, color=MUTE))

    # Vendor model box
    vmx = rx + 18
    vmy = bot + 108
    vmw = rw - 36
    d.add(Rect(vmx, vmy, vmw, 40, fillColor=CREAM2,
               strokeColor=MUTE, strokeWidth=0.9))
    d.add(_label(vmx + vmw / 2, vmy + 25, "Vendor AI model",
                 size=10, color=MUTE, bold=True))
    d.add(_label(vmx + vmw / 2, vmy + 12, "you pay per call, forever",
                 size=7, color=MUTE))

    # Context reasoning stuck on vendor side
    vcx = rx + 18
    vcy = bot + 30
    vcw = rw - 36
    d.add(Rect(vcx, vcy, vcw, 62, fillColor=CREAM,
               strokeColor=MUTE, strokeWidth=0.8, strokeDashArray=[2, 2]))
    d.add(_label(vcx + vcw / 2, vcy + 48, "Context reasoning",
                 size=9, color=MUTE, bold=True))
    d.add(_label(vcx + vcw / 2, vcy + 36, "workshops · decisions · language",
                 size=7, color=MUTE))
    d.add(_label(vcx + vcw / 2, vcy + 26, "patterns · priorities · corrections",
                 size=7, color=MUTE))
    d.add(_label(vcx + vcw / 2, vcy + 12,
                 "their asset — accumulates on their platform",
                 size=7, color=MUTE, bold=True))

    # Bottom caption — left panel
    d.add(_label(lx + lw / 2, bot - 14,
                 "Nothing crosses the boundary.",
                 size=8, color=INK, bold=True))
    d.add(_label(lx + lw / 2, bot - 26,
                 "When the engagement ends, the reasoning stays with you.",
                 size=7, color=MUTE))

    # Bottom caption — right panel
    d.add(_label(rx + rw / 2, bot - 14,
                 "Everything crosses the boundary.",
                 size=8, color=MUTE, bold=True))
    d.add(_label(rx + rw / 2, bot - 26,
                 "When the contract ends, the reasoning stays with them.",
                 size=7, color=MUTE))

    # Frame
    d.add(Rect(0, 0, width, height, fillColor=None,
               strokeColor=LINE, strokeWidth=0.75))
    return d


def repo_scope(width=620, height=380):
    """
    DMZ-bound context reasoning repository — scope.

    Frames the whole DMZ with two zones inside:
      1. Project execution corpus (unstructured + semi-structured):
         workshops, minutes, decisions, emails, specs, tickets, chat,
         corrections — the human record of the programme.
      2. Connectivity into the existing sovereign data estate:
         AWS / Azure / Snowflake / data lake / SAP ACDOCA.

    The twin sits between them and reasons over both. Everything stays
    inside the DMZ. The line the diagram lands: planning and execution
    assumptions are reasoned against actual business data, and that
    reasoning never leaves the boundary.
    """
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=CREAM2, strokeColor=None))

    # DMZ frame
    dmz_x, dmz_y = 20, 46
    dmz_w, dmz_h = width - 40, height - 78
    d.add(Rect(dmz_x, dmz_y, dmz_w, dmz_h,
               fillColor=CREAM, strokeColor=ACCENT, strokeWidth=2))
    d.add(_label(dmz_x + 12, dmz_y + dmz_h - 16,
                 "Inside your DMZ", size=10, color=ACCENT, bold=True,
                 anchor="start"))
    d.add(_label(dmz_x + 12, dmz_y + dmz_h - 27,
                 "context reasoning repository — scope",
                 size=7, color=MUTE, anchor="start"))

    # Central twin box — with the connector meaning INSIDE the box,
    # so it never sits on top of the connector line where it meets
    # the box edge.
    tw_w, tw_h = 150, 66
    tw_x = dmz_x + (dmz_w - tw_w) / 2
    tw_y = dmz_y + (dmz_h - tw_h) / 2 - 10
    d.add(Rect(tw_x, tw_y, tw_w, tw_h, fillColor=ACCENT, strokeColor=ACCENT))
    d.add(_label(tw_x + tw_w / 2, tw_y + 48, "Twin",
                 size=13, color=CREAM, bold=True))
    d.add(_label(tw_x + tw_w / 2, tw_y + 30,
                 "reads project corpus", size=8, color=CREAM))
    d.add(_label(tw_x + tw_w / 2, tw_y + 18,
                 "queries live data", size=8, color=CREAM))
    d.add(_label(tw_x + tw_w / 2, tw_y + 6,
                 "reasons over both", size=8, color=CREAM, bold=True))

    # ---------- Left zone: unstructured + semi-structured corpus ----------
    lz_x = dmz_x + 14
    lz_w = tw_x - lz_x - 22
    lz_y = dmz_y + 24
    lz_h = dmz_h - 70
    d.add(Rect(lz_x, lz_y, lz_w, lz_h,
               fillColor=CREAM2, strokeColor=INK, strokeWidth=0.9))
    # Header, left-aligned with 14pt inner padding
    header_pad = 14
    d.add(_label(lz_x + header_pad, lz_y + lz_h - 20,
                 "Project execution corpus",
                 size=11, color=INK, bold=True, anchor="start"))
    d.add(_label(lz_x + header_pad, lz_y + lz_h - 34,
                 "unstructured + semi-structured",
                 size=8, color=MUTE, anchor="start"))

    left_items = [
        "Workshops and meeting minutes",
        "Decisions and corrections log",
        "Emails, chat, tickets",
        "Specs, blueprints, drafts",
        "Risk log and change log",
        "Test scripts and evidence",
    ]
    # Left-aligned bulleted list, 10pt body, 16pt line height
    list_top = lz_y + lz_h - 56
    line_h = 18
    for i, txt in enumerate(left_items):
        y = list_top - i * line_h
        # Bullet
        d.add(Circle(lz_x + header_pad + 4, y + 4, 1.8,
                     fillColor=ACCENT, strokeColor=ACCENT))
        d.add(_label(lz_x + header_pad + 14, y, txt,
                     size=10, color=INK, anchor="start"))

    # ---------- Right zone: sovereign data estate ----------
    rz_x = tw_x + tw_w + 22
    rz_w = dmz_x + dmz_w - rz_x - 14
    rz_y = dmz_y + 24
    rz_h = dmz_h - 70
    d.add(Rect(rz_x, rz_y, rz_w, rz_h,
               fillColor=CREAM2, strokeColor=INK, strokeWidth=0.9))
    d.add(_label(rz_x + header_pad, rz_y + rz_h - 20,
                 "Client Sovereign data estate",
                 size=11, color=INK, bold=True, anchor="start"))
    d.add(_label(rz_x + header_pad, rz_y + rz_h - 34,
                 "your existing systems — read where they live",
                 size=8, color=MUTE, anchor="start"))

    right_items = [
        "SAP S/4HANA (ACDOCA)",
        "AWS, Azure, GCP",
        "Snowflake, Databricks",
        "Data lake and warehouse",
        "Datasphere, BW",
        "ALM, ITSM, ticketing",
    ]
    for i, txt in enumerate(right_items):
        y = list_top - i * line_h
        d.add(Circle(rz_x + header_pad + 4, y + 4, 1.8,
                     fillColor=ACCENT, strokeColor=ACCENT))
        d.add(_label(rz_x + header_pad + 14, y, txt,
                     size=10, color=INK, anchor="start"))

    # Connector lines: twin ↔ left zone, twin ↔ right zone
    mid_y = tw_y + tw_h / 2
    l_left = Line(lz_x + lz_w, mid_y, tw_x, mid_y)
    l_left.strokeColor = INK
    l_left.strokeWidth = 1.1
    d.add(l_left)
    l_right = Line(tw_x + tw_w, mid_y, rz_x, mid_y)
    l_right.strokeColor = INK
    l_right.strokeWidth = 1.1
    d.add(l_right)

    # No text labels on or near the connector lines.
    # The connector meaning is stated INSIDE the twin box above.

    # Bottom caption band (inside the DMZ, above the boundary line)
    d.add(_label(dmz_x + dmz_w / 2, dmz_y + 12,
                 "Planning and execution assumptions are reasoned against actual business data.",
                 size=8, color=INK, bold=True))

    # Below the DMZ frame, outside caption
    d.add(_label(width / 2, 22,
                 "Nothing on this page ever leaves the DMZ. That is the point.",
                 size=8, color=ACCENT, bold=True))

    # Outer frame
    d.add(Rect(0, 0, width, height, fillColor=None,
               strokeColor=LINE, strokeWidth=0.75))
    return d


def surfaces_flow(width=480, height=170):
    """
    Four surface boxes (Documents, Risks, Changes, Tests) flowing left to
    right, all landing in "your repository" on the right.
    """
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=CREAM2, strokeColor=None))

    names = ["Documents", "Risks", "Changes", "Tests"]
    refs = ["IKEA", "Vodafone", "ALM record", "SAP Activate"]

    box_w = 78
    box_h = 60
    gap = 8
    total_w = 4 * box_w + 3 * gap
    start_x = 24
    y = height / 2 - box_h / 2

    for i, (name, ref) in enumerate(zip(names, refs)):
        x = start_x + i * (box_w + gap)
        d.add(Rect(x, y, box_w, box_h, fillColor=CREAM,
                   strokeColor=INK, strokeWidth=0.8))
        d.add(_label(x + box_w / 2, y + box_h - 16, name,
                     size=9, color=INK, bold=True))
        d.add(_label(x + box_w / 2, y + box_h - 30, "ref:", size=6, color=MUTE))
        d.add(_label(x + box_w / 2, y + box_h - 38, ref, size=7, color=ACCENT, bold=True))
        d.add(_label(x + box_w / 2, y + 8, "on your systems",
                     size=6, color=MUTE))

    # Arrow to repo
    ar_start = start_x + total_w + 4
    ar_end = ar_start + 46
    ar_y = y + box_h / 2
    line = Line(ar_start, ar_y, ar_end - 6, ar_y)
    line.strokeColor = ACCENT
    line.strokeWidth = 2
    d.add(line)
    # Arrowhead
    d.add(Polygon([
        ar_end - 6, ar_y - 4,
        ar_end - 6, ar_y + 4,
        ar_end,     ar_y,
    ], fillColor=ACCENT, strokeColor=ACCENT))

    # Repo box
    repo_x = ar_end + 4
    repo_w = width - repo_x - 24
    d.add(Rect(repo_x, y, repo_w, box_h, fillColor=ACCENT, strokeColor=ACCENT))
    d.add(_label(repo_x + repo_w / 2, y + box_h - 20, "Your",
                 size=9, color=CREAM, bold=True))
    d.add(_label(repo_x + repo_w / 2, y + box_h - 32, "repository",
                 size=9, color=CREAM, bold=True))
    d.add(_label(repo_x + repo_w / 2, y + 10, "trade secret",
                 size=7, color=CREAM))

    # Caption
    d.add(_label(width / 2, 14,
                 "Four surfaces. All drafted on your systems. All versioned in your repository.",
                 size=7, color=MUTE))

    # Frame
    d.add(Rect(0, 0, width, height, fillColor=None, strokeColor=LINE, strokeWidth=0.75))
    return d
