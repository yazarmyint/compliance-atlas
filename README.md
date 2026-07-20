# Compliance Atlas

An audited, role-agnostic reference that maps compliance frameworks to Microsoft security-stack
capabilities. It answers one question: **"An organization operates in industry X and is subject to
framework Y: where does the Microsoft stack fit, at what claim strength, and at what licence tier?"**

Every row states a coverage level (Direct Support / Partial Support / Evidence Support Only / Not
Covered) and a confidence level, cites at least one official framework source, and carries the date it
was last verified. Mapped products **support or evidence** controls; the atlas never claims a product
satisfies or meets a requirement.

## What's in it

**378 rows · 11 frameworks · 6 products** — every row `verified` against live sources.

| | |
|---|---|
| **Frameworks** | ISO/IEC 27001:2022 (57) · NIST SP 800-53 R5 subset (54) · NIST 800-171 R2 / CMMC L2 (46) · SOC 2 (41) · NIST CSF 2.0 (40) · HIPAA Security Rule (32) · PCI DSS v4.0.1 (31) · Microsoft SSPA DPR (26) · EU GDPR (24) · GLBA Safeguards Rule (21) · FERPA (6) |
| **Products** | Purview (150) · Defender XDR (53) · Entra (48) · Sentinel (46) · Intune (41) · Defender for Cloud (40) |
| **Industry lenses** | 12 |

Each framework is pinned to a specific published version, and each product's licensing strings come
from that product's own authoritative source. The pinned versions and the per-product mapping
discipline are in [`docs/AUTHORING.md`](docs/AUTHORING.md).

## Use it

**→ [yazarmyint.github.io/compliance-atlas](https://yazarmyint.github.io/compliance-atlas/)** —
nothing to install, and every view has its own link you can share.

Or take it offline. The atlas is **one self-contained HTML file** with no external dependencies of
any kind: download `compliance-atlas.html` from the
[latest release](https://github.com/yazarmyint/compliance-atlas/releases/latest) (or clone the repo)
and open it in any browser. It works from `file://`, needs no server and no build step, and behaves
identically to the hosted copy — which makes it usable inside an air-gapped or
restricted-egress environment. `compliance-atlas.json` ships alongside it for anyone consuming the
dataset directly.

## Licence

| What | Licence |
|---|---|
| **Build code** — everything in `build/` | MIT — [`LICENSE`](LICENSE) |
| **Atlas content** — rows, taxonomies, framework/product/industry metadata, the generated `.json` and `.html`, and this documentation | CC BY 4.0 — [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md) |
| **The third-party frameworks and standards mapped to** | Not covered by either; rights belong to ISO, AICPA, PCI SSC, NIST, Microsoft, and the respective regulators |

The atlas paraphrases control intent and reproduces no ISO, AICPA, PCI SSC, or NIST text — that rule is
what makes open licensing of this work possible, and **anyone adapting the atlas must keep it**. Full
reasoning, the attribution format, and the warranty disclaimer are in
[`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).

Copyright © 2026 Yazar. Product and standard names are trademarks of their owners, used for
identification only; this is an independent project, not affiliated with or endorsed by Microsoft.

## Repository guide

| Path | What it is |
|---|---|
| `compliance-atlas.html` | The atlas itself — generated output, never hand-edited |
| `compliance-atlas.json` | Canonical dataset — generated output, never hand-edited |
| `index.html` | Redirect stub so GitHub Pages serves the atlas at the site root — generated output, never hand-edited |
| [`CHANGELOG.md`](CHANGELOG.md) | Reader-facing version history and the MAJOR/MINOR/PATCH policy |
| [`docs/AUTHORING.md`](docs/AUTHORING.md) | Shipping state, file layout, row schema, and the add-a-framework / add-a-product procedures |
| [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md) | Dated maintenance triggers and the framework backlog |
| [`FRAMEWORK-SELECTION.md`](FRAMEWORK-SELECTION.md) | Why these eleven frameworks; rejected candidates and their reasons |
| [`AUDIT-FINDINGS.md`](AUDIT-FINDINGS.md) | Full audit trail: original source audit, per-increment QA, every declared edit |
| [`PROJECT-REVIEW.md`](PROJECT-REVIEW.md) | Independent end-to-end review that set the publishing programme |
| [`CONTENT-REVIEW.md`](CONTENT-REVIEW.md) | Editorial consistency review of the rendered prose |
| [`reference/SOURCES.md`](reference/SOURCES.md) | Provenance and redistribution status of every file in `reference/` |
| `build/` | The generator: row modules, product and solution maps, template, assembler |
| [`tools/`](tools/README.md) | Standing QA: `check_urls.py` resolves every cited URL, `axe_check.mjs` runs WCAG 2.1 A/AA over every view in both themes |

## Regenerate

```powershell
python build/assemble.py      # row modules + maps → compliance-atlas.json
python build/build_html.py    # JSON + template.html → compliance-atlas.html + index.html
```

Edit content in `build/rows_*.py`, maps in `build/common.py`, presentation in `build/template.html`;
never the generated outputs. Full authoring rules: [`docs/AUTHORING.md`](docs/AUTHORING.md).
