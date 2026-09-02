"""
Render each diagram to a standalone PNG for review.
Does NOT touch docs/ — outputs land in preview/.
"""

from pathlib import Path
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas as _canvas

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from diagrams import (  # noqa: E402
    three_sovereignties, team_triangle, wall_diagram, surfaces_flow, repo_scope,
)

OUT = Path(__file__).resolve().parent.parent / "preview"
OUT.mkdir(parents=True, exist_ok=True)

for name, fn in [
    ("00-three-sovereignties", three_sovereignties),
    ("01-team-triangle", team_triangle),
    ("02-wall-diagram",  wall_diagram),
    ("03-surfaces-flow", surfaces_flow),
    ("04-repo-scope",    repo_scope),
]:
    d = fn()
    out_path = OUT / f"{name}.pdf"
    pad = 24
    c = _canvas.Canvas(str(out_path), pagesize=(d.width + 2 * pad, d.height + 2 * pad))
    renderPDF.draw(d, c, pad, pad)
    c.save()
    print(f"[preview] {out_path.name}  {d.width:.0f}x{d.height:.0f}")
