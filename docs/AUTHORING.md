# Authoring the atlas

Maintainer reference for everything upstream of the generated files: the dataset's current shipping
state, the repository layout, the row schema, and the procedures for regenerating the build or adding
a framework or a product. Reader-facing orientation lives in [`../README.md`](../README.md).

## Contents (v2.9.0 — full version history in `CHANGELOG.md`)

| Framework | Version pinned | Rows (all products) |
|---|---|---|
| Microsoft SSPA DPR | v12 (March 2026) | 26 |
| ISO/IEC 27001:2022 | 2022 (Amd 1:2024 noted) | 57 |
| SOC 2 | 2017 TSC, 2022 revised points of focus | 41 |
| HIPAA Security Rule | 45 CFR 164 Subpart C (current; NPRM flagged) | 32 |
| NIST 800-171 R2 / CMMC L2 | R2 per 32 CFR 170; 48 CFR phased rollout | 46 |
| NIST 800-53 R5 (subset) | Rev 5, Release 5.2.0 (Aug 2025): data-protection subset + identity/endpoint/detection/audit-and-IR/cloud-posture extensions | 54 |
| NIST CSF 2.0 | Feb 2024 | 40 |
| PCI DSS v4.0.1 | Sole active version | 31 |
| GLBA Safeguards Rule | 16 CFR 314 incl. May 2024 breach amendment | 21 |
| FERPA | 34 CFR Part 99 (current; ED rulemaking watch) | 6 |
| EU GDPR | 2016/679 | 24 |

**378 rows across 11 frameworks and six products: Purview (150), Entra (48), Intune (41), Defender XDR (53),
Sentinel (46), and Defender for Cloud (40), all `verified` against live sources.** By framework: ISO/IEC 27001:2022
(57), NIST SP 800-53 R5 subset (54), NIST 800-171 R2 / CMMC L2 (46), SOC 2 (41), NIST CSF 2.0 (40), HIPAA Security
Rule (32), PCI DSS v4.0.1 (31), Microsoft SSPA DPR (26), EU GDPR (24), GLBA Safeguards Rule (21), FERPA (6). Claim taxonomy: Coverage = Direct Support /
Partial Support / Evidence Support Only / Not Covered; Confidence = High / Medium / Low. Mapped products **support or
evidence** controls; the artifact never claims a product satisfies or meets a requirement. Sentinel's mapping
discipline: it **evidences and detects, it does not enforce**: Direct Support only where the control's namesake
activity is log collection/retention, correlation/analysis, or security monitoring/alerting. Defender for Cloud's
mapping discipline: it **assesses and detects, it does not remediate**: posture recommendations are advisory
(Azure Policy/IaC/operators execute fixes), so hardening controls rate Partial where the product only finds the gap;
Direct is reserved for configuration/compliance assessment, cloud vulnerability assessment, resource inventory, and
cloud workload threat detection namesakes. Its regulatory compliance dashboard rows all carry an assessment-scope
caveat: the dashboard assesses **onboarded cloud resources** against a standard's technically-assessable subset,
never M365 workloads or procedural controls, and it is not an attestation (Purview Compliance Manager assesses the
M365 estate: a seam, not an overlap).
## Files

```
compliance-atlas.html          ← the output (generated; never hand-edit)
compliance-atlas.json          ← canonical dataset (generated; never hand-edit)
AUDIT-FINDINGS.md              ← audit trail: legacy-xlsx audit, per-increment QA, generalization log
CHANGELOG.md                   ← reader-facing version history + the MAJOR/MINOR/PATCH policy
FRAMEWORK-SELECTION.md         ← framework scoping decisions; rejected candidates & backlog
build/
  common.py                    ← PRODUCTS + RELATED_PRODUCTS maps, SOLUTIONS registry, LIC strings, URLs, GOV notes
  dependency_migration.py      ← mechanical split of non_purview_dependencies → structured model
  rows_<framework>.py          ← one module per framework: FRAMEWORK metadata + ROWS (product-tagged)
  assemble.py                  ← merges modules + products + industries + BRAND → compliance-atlas.json
  template.html                ← HTML/CSS/JS shell with /*__DATA__*/ placeholder (four generalized views)
  build_html.py                ← injects minified JSON into the template → the HTML
reference/
  SOURCES.md                   ← provenance + redistribution status of every file here (read before adding one)
  baseline-pre-refactor.json   ← 150-row snapshot used as the generalization regression baseline
  dependency-migration-log.json← original-string → parsed-structure log for every migrated row
  <source documents>           ← public-domain framework texts (NIST, eCFR) used for verification.
                                 Copyrighted/licensed sources (AICPA, PCI SSC, Microsoft vendor docs) are
                                 deliberately NOT in this repo; see reference/SOURCES.md for where to get them.
```
*(Public name settled 2026-07-19; parameterized in one place, `BRAND` in `build/assemble.py`.)*

> **File rename (2026-07-17, platform generalization):** the canonical JSON was `purview-compliance-map.json` →
> now **`compliance-atlas.json`**; the output was `purview-compliance-map.html` → now **`compliance-atlas.html`**.
> The old filenames are gone; do not look for them.
## Regenerate the HTML

```powershell
python build/assemble.py      # row modules + maps → compliance-atlas.json (with integrity checks + dep migration)
python build/build_html.py    # JSON + template.html → compliance-atlas.html
```

Edit content in `build/rows_*.py`, maps in `build/common.py`, presentation in `build/template.html`; never the outputs.
The build is fully regenerable from source: `assemble.py` re-derives the JSON (and re-runs the dependency migration as a
pure transform) every run, so it is idempotent and cannot double-migrate.
## Row schema (current)

Each row is a dict with these fields:

| Field | Notes |
|---|---|
| `id` | unique slug |
| `product` | product slug; must exist in `common.py → PRODUCTS` (`purview`, `entra`, `intune`, `defender-xdr`, …) |
| `framework`, `framework_version` | framework slug + pinned version |
| `control_ref`, `control_domain`, `control_intent` | control identity + short paraphrased intent |
| `purview_solution`, `also_involves` | the product's primary solution + secondary solutions (canonical names in `SOLUTIONS`; `"None (boundary row)"` for boundary rows). *Field name retained for schema stability; it is the mapped-solution field for whatever product owns the row.* |
| `capability_detail`, `how_it_supports`, `config_evidence_example`, `operational_evidence_example` | the substance |
| `coverage`, `confidence` | fixed taxonomies (see above) |
| `license_requirement` | SKU/entitlement string from the product's authoritative licensing source |
| `licensing_model` | discriminator: `per_user` \| `consumption` \| `included` \| `n/a`. Defaults from the product's `default_licensing_model`; `n/a` for boundary rows. Exists so consumption-priced products (Sentinel, Defender for Cloud) fit without a SKU-only field. |
| `related_microsoft` | **structured** list of Microsoft-product dependencies: `{product, solution?, role: primary\|contributing, note?}`. `product` is a slug in `PRODUCTS` or `RELATED_PRODUCTS`. When a related product gains its own rows, row-level links attach here without another migration. |
| `external_dependencies` | free text for everything that is **not** a Microsoft product (processes, contracts, CMDB, customer-side ops, generic SIEM/tooling categories). |
| `legacy_dependencies` | the original pre-split `non_purview_dependencies` string, preserved verbatim for provenance. |
| `cloud_availability_note` | GCC/GCC High/DoD caveats where they exist |
| `sources` | ≥1 official framework URL + ≥1 Microsoft Learn URL (boundary rows, coverage `Not Covered`, carry the framework URL only) |
| `status`, `last_verified` | `verified` \| `UNVERIFIED`; per-row date governs currency |

Authoring modules still write the **free-text `non_purview_dependencies`** (via the `row()` helper); `assemble.py` splits
it into `related_microsoft` / `external_dependencies` / `legacy_dependencies` at build time via
`dependency_migration.py`. The parser only assigns a Microsoft product when a segment names one of five unambiguous
families (Entra, Intune, Defender, Sentinel, Priva); everything else, including Microsoft-adjacent platform features
(BitLocker, Key Vault, SharePoint, M365 service encryption), stays in `external_dependencies` and is flagged in the log
rather than guessed into a product.
## Add a framework

1. **Verify first.** Pin the current version against the official source (regulator/SDO, not blogs, not memory).
   Highest hallucination-risk items: control IDs, license entitlements, Compliance Manager template names.
2. Create `build/rows_<id>.py` exposing `FRAMEWORK` (id, name, full_name, version, authority, official_source,
   document_url, compliance_manager_template {exists, name, note, source}, domains, applies_to, notes) and `ROWS`
   using the `row()` helper. Rules:
   - Map only controls where the product has a **genuine** role (~12–25 rows, not exhaustive); boundary rows
     (`purview_solution: "None (boundary row)"`, coverage `Not Covered`) are encouraged where the question
     comes up anyway.
   - Paraphrase control intent; never reproduce ISO/AICPA/PCI text (copyrighted); paraphrase NIST/US law too.
   - Every row: ≥1 official framework source. Every row with coverage other than `Not Covered` also carries
     ≥1 Microsoft Learn URL. **Boundary rows are exempt from the Microsoft half** — a `Not Covered` verdict has
     no Microsoft capability to cite, so the framework source stands alone (six rows do this today: `dpr-j48`,
     `soc2-p1-p3`, `soc2-a1`, `soc2-pi1`, `53-mp-6`, `gdpr-30`). `assemble.py` enforces both halves.
     Anything unconfirmed ships as `status: "UNVERIFIED"` (renders with a red warning), never silently.
   - `license_requirement` comes from the product's authoritative licensing source only (for Purview, the
     **service description per-feature tables** in `common.py → LIC`); `cloud_availability_note` from the US
     Government service descriptions (`GOV`).
   - Mapped solutions only in `purview_solution`/`also_involves` (canonical names in `common.py → SOLUTIONS`);
     other Microsoft products (Entra/Defender/Intune/Priva/Sentinel) belong in the free-text
     `non_purview_dependencies`, where the migration lifts them into `related_microsoft`.
3. Add the module name to `MODULES` in `assemble.py`; wire the framework id into `INDUSTRIES`.
4. Rebuild (both commands above), then QA: re-verify a random row sample, run the URL check
   (see AUDIT-FINDINGS §7 for the pattern), and confirm JSON↔HTML row counts reconcile.
## Add a product

Mirrors add-a-framework; the data model and all four UI views already generalize over products.
**The product roadmap is complete (six products, closed 2026-07-18); this procedure is retained for maintenance
reference only; no further products are planned.** Entra (product #2), Intune (#3), Defender XDR (#4, all
2026-07-17), Sentinel (#5, 2026-07-18), and Defender for Cloud (#6, 2026-07-18) are the worked references.
Defender XDR is the multi-solution worked example (one product, four workload solutions); Sentinel is the
**consumption-licensing** worked example (`default_licensing_model: consumption`, `SENTINEL_LIC` strings describing
meters not SKUs); Defender for Cloud is the **non-M365/multicloud** worked example (per-resource meters in `MDC_LIC`,
an Azure-platform scope boundary, and the regulatory-compliance-dashboard assessment-scope caveat pattern). The
steps below were corrected against those real executions (see AUDIT-FINDINGS §11–§15; Intune, Defender XDR,
Sentinel, and Defender for Cloud ran as clean clones with only the refinements in §12.5 and §13.6).

1. **Verify the product naming AND per-capability licensing first** on Microsoft Learn (do not recall it; names
   churn; "Azure AD" is retired). Capture the official product name, the **authoritative licensing source** (the
   product's own service description, e.g., `entra/fundamentals/licensing`, not the Purview one; for consumption
   products the Azure pricing/meters page), and each capability's tier. **Run any product-retirement gate first**
   (Entra example: Permissions Management/CIEM was retired 2025-10-01 → not mapped, historical note only).
2. In `build/common.py`:
   - Add the product to `PRODUCTS` (`id, official_name, short_name, naming_source, solutions: []`,
     `licensing_source, default_licensing_model, notes`). Leave `solutions` empty here; it's derived (next bullet).
   - Register the product's solutions **in the shared `SOLUTIONS` registry, each tagged `"product": "<id>"`**
     (the JSON `solutions` map must contain every product's solutions so the HTML can render their solution pages).
     Then derive per-product lists: the bottom of `common.py` tags legacy Purview entries `product="purview"`,
     merges the new product's solutions, and sets `PRODUCTS[pid]["solutions"] = [k for k,v in SOLUTIONS.items() if
     v["product"]==pid]`. This keeps product isolation (a product's pivot/matrix only shows its own solutions).
   - Add the product's `<PID>_LIC` / `<PID>_URLS` / `<PID>_GOV` dicts (do not overload Purview's `LIC`/`URLS`/`GOV`).
   - Remove the product's slug from `RELATED_PRODUCTS` (it graduates to `PRODUCTS`; existing `related_microsoft`
     entries pointing at it stay valid; `prodFull()` resolves either map).
3. Author rows **into the existing `build/rows_<framework>.py` modules** (a mapping attaches to a control, and
   controls live in framework modules; there is no `rows_<product>.py`). Append an Entra-style block at the end of
   each module: `from common import <PID>_LIC, <PID>_URLS, <PID>_GOV, prow, rel`, a thin `er(...)` closure calling
   `prow("<pid>", FRAMEWORK["id"], "<framework_version>", ...)`, then `ROWS += [ er(...), ... ]`. **Do not touch the
   existing Purview `row()` calls**; append only, so Purview content stays byte-identical.
   - **New product rows are authored STRUCTURED, not free-text.** Use `prow`/`rel` (in `common.py`): pass an explicit
     `related_microsoft` list (`[rel("purview","contributing","…","Audit"), …]`) and free-text `external_dependencies`;
     `prow` sets `legacy_dependencies=""` (there is no legacy string; the free-text→structured migration was a
     one-time Purview import). Do NOT author `non_purview_dependencies` on new-product rows (that field triggers the
     migration path, which only recognizes 5 product tokens and would misparse).
   - **Product isolation:** the mapped capability (`purview_solution` field, a schema-stable and product-agnostic name)
     must be one of *this* product's solutions. Other products go in `related_microsoft` (role `primary`/`contributing`,
     never referencing this product itself; same-product secondary solutions go in `also_involves`).
   - Same caps and verification rules as Purview: genuine-role only, curated per framework (Entra: 1–9/framework,
     concentrated in the AC/identity/auth/privileged/governance dense zone), paraphrased intent, ≥1 official + ≥1
     Learn source per row, honest coverage/confidence (identity products skew Direct; that's correct, but keep
     boundary/monitoring/foreign-IdP rows at Partial), per-capability `license_requirement` + tier from the product's
     own source, government-cloud `cloud_availability_note` where it differs.
   - Save after each framework (each `.py` append is a durable, resumable save).
4. **Reconcile the seam.** Existing rows may reference the new product in `related_microsoft`. Where an existing row
   names it **primary**, confirm a matching new-product row now exists for that control (so the framework view stacks
   both). Flag, don't delete, any primary reference with no matching row. (Entra: 6/6 primary references matched;
   Intune: 8/8 references gained matching rows; Defender XDR: 4/4 primary + 12 contributing stacked, 9 deliberately
   link-only, §13.4.) Two mechanics matter here (§13.6): **stacking requires exact `control_ref` string equality**
   (mirror a multi-ref control's ref exactly; an adjacent-family row does not stack), and **every solution needs at
   least one primary row** or its pivot page renders empty (give narrow-band solutions one genuine primary row, or
   consciously accept the empty page).
5. **Extend framework-level metadata the new product touches.** `FRAMEWORK["domains"]` lists and scoping notes were
   written from the first product's map; when the new product adds control families (e.g., PCI Req 1/2/5/6, 800-53
   CM/MP), extend the domains list and adjust subset/scoping notes. Framework metadata is not row content, so this
   does not violate the prior-product no-drift gate (verify rows separately).
6. **Update the state text in this document** (Contents table row counts, product list, totals); the procedure text and the
   shipping-state text are separate things and the latter is easy to forget (both §11 and §12 caught staleness here).
7. `INDUSTRIES` is framework-keyed, so a cross-industry product (identity) needs no industries edit; it surfaces
   under every framework already listed. Add entries only for a product that introduces a *new* industry lens, and
   refresh industry `note` text where the new product changes the leading story (Intune: healthcare, DIB).
8. Regenerate (`python build/assemble.py && python build/build_html.py`) and run the regression gate: prior product's
   row count unchanged with zero content drift; new-URL resolution (log gov WAF blocks, not failures); re-verify
   every Direct-Support row (overclaim risk) and every P2/Suite/consumption-gated licensing value (licensing-error
   risk); JSON↔HTML reconcile at the new total; multi-product stacking renders in light + dark; product-aware search;
   print expansion.