# eve-liliantwin-pmo

## Agent entry point

Read [AGENTS.md](AGENTS.md) before work. **Lilian's DI PMO pitch materials use the [Emerson Rush PowerPoint reference](templates/Emerson_Rush_DI_PMO_reference.pptx), not this public site's cream/orange design.** Reuse the [approved four-circle diagram](templates/DI_PMO_Decision_Roles_Map_approved.pptx). The DI PMO model, not a representative's résumé, is the offering.

Public surface for the **Universal DI Framework PMO Model**.

> The PMO that runs inside your systems.

Live site: <https://eveglyphdesign.github.io/eve-liliantwin-pmo/>

Controlled PDFs:
- Desktop / print: [EVEglyphDesign_Universal_DI_PMO.pdf](https://eveglyphdesign.github.io/eve-liliantwin-pmo/EVEglyphDesign_Universal_DI_PMO.pdf)
- Phone: [EVEglyphDesign_Universal_DI_PMO_phone.pdf](https://eveglyphdesign.github.io/eve-liliantwin-pmo/EVEglyphDesign_Universal_DI_PMO_phone.pdf)

Related canon:
- [Decision Intelligence Framework](https://eveglyphdesign.github.io/decision-intelligence-framework/) — the framework this PMO operates inside.
- [Executive Boot Contract](https://eveglyphdesign.github.io/eve-glyph-boot-contract/) — the operating rules for every agent in this system.

## What is here

- `docs/index.html` — public surface, team-only, no individual names.
- `docs/EVEglyphDesign_Universal_DI_PMO.pdf` — controlled PDF, letter format, names the practice lead.
- `docs/EVEglyphDesign_Universal_DI_PMO_phone.pdf` — controlled PDF, phone-readable single column.
- `docs/luzid-wordmark.svg` — third-party wordmark used inside the comparison table, unaltered.
- `build/content.py` — page content, one place to edit.
- `build/build_pdf.py` — two-pass builder, EVEglyph canon (cream + orange, Fraunces + Inter, watermark, SHA-256, key ID, UTC timestamp, closing mark).

## Rebuild

```
python build/build_pdf.py
```

The build is two-pass: the first pass discovers the page count, the second stamps it into the footer alongside the SHA-256 content hash.

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
