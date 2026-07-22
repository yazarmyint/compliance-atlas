# Authoring the atlas

Maintainer reference for everything upstream of the generated files: the dataset's current shipping
state, the repository layout, the row schema, and the procedures for regenerating the build or adding
a framework or a product. Reader-facing orientation lives in [`../README.md`](../README.md).

## Contents (v3.0.0 — full version history in `CHANGELOG.md`)

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
| `license_band`, `license_band_partial` | **derived, never authored.** `e3` \| `e5` \| `addon` \| `consumption` \| `na`, plus a boolean. Written by `build/license_bands.py` at assemble time from the licensing constants the row's `license_requirement` is composed from. Do not set these in a row module — `assemble.py` overwrites them. See *License bands* below. |
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

## License bands (PR-015)

`license_band` and `license_band_partial` are **derived at build time** by `build/license_bands.py`. Nothing in a
row module sets them. The mapping is keyed on the **licensing constant coordinate** — `("LIC", "dlp_core")` — not on
the row's prose, because the 378 rows compose 110 distinct `license_requirement` strings out of just **49
constants**. Banding the 49 gives a reviewed table; banding the 110 would give a pile of near-duplicates, and
substring heuristics over prose would silently misclassify the next string somebody writes.

**Bands.** `e3` (included at M365 E3 or below) · `e5` (needs E5 or the relevant step-up) · `addon` (needs an add-on
or standalone SKU) · `consumption` (metered; no seat tier exists) · `na` (boundary rows).

**Floor banding.** A row bands at the *lowest* tier where any mapped capability functions, and sets
`license_band_partial` when part of the mapping needs more. Rules F1–F7 are stated in full at the top of
`build/license_bands.py` — read them before adding a mapping entry. Two rules bite most often: an "or" between
routes to the same capability takes the minimum and does **not** set partial (F1), while a genuine capability split
takes the minimum and **does** (F2). Two rules are owner decisions worth knowing: "functions" means reader-usable
capability, so background processing behind no reachable interface does not band (F7), and **partial is not
permitted in the `consumption` band** at all — "reduced at this tier" is meaningless where the band asserts no tier
exists, so billing nuances stay in the verbatim string.

**Commercial licensing only.** No G3/G5, F-series, or Business Premium dimension. Government licensing stays in the
per-row `cloud_availability_note`. Related-product "(if licensed)" mentions are out of scope — pointers, not claims.

**What fails the build.** All four are hard failures; there is deliberately no default band.

| Guard | Fires when | Fix |
|---|---|---|
| G1 | a licensing constant has no `BANDS` entry | add the entry, citing the constant's own text |
| G2 | a row's license string matches no constant and is not the literal `n/a` | compose it from a constant, or set `n/a` if it is genuinely a boundary row |
| G3 | the band disagrees with `licensing_model` about consumption or boundary status | one of the two is wrong; find out which |
| G4 | a tier token (`E5`, `Plan 2`, `add-on`, …) appears in row prose *outside* any constant | move the claim into a constant, or add a `ROW_OVERRIDES` entry **with a stated reason** |

G4 exists because a constant-keyed mapping has exactly one blind spot: prose the constants do not cover. Two rows
hit it today (`iso-a-5-10`, `53-ac-21`, both appending "advanced policy tips: E5-tier"), and both are in
`ROW_OVERRIDES`. Prefer moving a claim into a constant over adding an override — constants are covered by the
maintenance triggers, and override entries are not.

**Never clock-derive a band.** `DEFENDER_LIC["mdo_p1"]` is banded `("e3", True)` as a hard-coded literal even though
its E3 inclusion has a stated effective date, because computing it from `date.today()` would move the band on a
calendar boundary with no commit behind it — breaking the strict empty-diff drift check. Dated re-checks belong in
`MAINTENANCE` (see `TRG-MDO-P1-E3G3`, which owns dropping that partial flag when the rollout completes), not in the
derivation.

## Glossary (PR-011)

The reader glossary is a `term -> definition` dict in `build/glossary.py`, imported into `META["glossary"]` by
`assemble.py` exactly as `license_bands.BAND_DEFS` is — one source, so the `#/glossary` route and any JSON consumer
cannot drift, and adding it was a MINOR (a reader feature; the analogue is 2.10.0's `meta.maintenance`). The route is
reached from the footer nav and cross-linked from About; it is **not** a primary nav tab, because it is reference
material looked up on demand rather than a browse mode.

Three rules govern the content, all asserted by `check_glossary()` or stated in the module docstring:

- **Definitions describe; they never claim.** No entry asserts coverage, licensing, or a live accreditation — those
  live on the rows and the tier bands, and accreditation nowhere (it goes stale). GCC High is defined by purpose and
  the standard it is assessed against; CMMC is the model, dateless.
- **Entries stay em-dash-free.** The Session-15 `/agentic-humanizer` pass established this (pattern 14); the build
  guard fails on an em/en dash so a later edit cannot quietly reintroduce one.
- **The cut is on the record.** 47 terms ship; the exclusions (WORM/DIB as zero-occurrence, CM as ambiguous, PII as
  universal, framework short-names as card-covered) and the ambiguity resolutions (IRM≠Information Rights Management,
  FIM≠Forefront Identity Manager, CIEM the discipline not the retired product, DoD the environment) are recorded in the
  module docstring and AUDIT-FINDINGS §33.

The `<abbr>` first-use pass is **static prose only** (About page): the three framework short-forms in "How a row is
made" and four capability acronyms in the glossary-pointer sentence. Row and list prose are never marked up — "first
use" is unstable under client-side filtering, and per-instance markup makes a screen reader re-announce the expansion.

## Stack rationales (PR-013)

A "stacked control" is ≥2 rows sharing `(framework, control_ref)`, rendered as product-tagged cards
beneath one control heading on the framework view. Where their coverage tiers differ, the badge order can
read as an inconsistency before the row prose resolves it (the exemplar: CSF `PR.PS-04`, where the product
that *generates* the log records rates below the one that makes them available). `build/stack_rationales.py`
holds a short, group-level line for the 22 stacks where that misreading risk is real, imported into
`META["stack_rationales"]` by `assemble.py` exactly as `glossary.GLOSSARY` and `license_bands.BAND_DEFS`
are — one source, so the page and any JSON consumer cannot drift. `renderControlGroups` (in `template.html`)
renders it as a muted line **above the stacked cards**, in reading order after the control ref/intent, so a
screen reader gets the reason before the mappings. Groups whose spread is self-explanatory carry none.

Four rules govern the content; the first three are authoring discipline, the fourth is enforced by
`check_stack_rationales(rows)` in the build's check phase:

- **Scope and role only; never licensing.** A rationale explains why the products play different roles or
  reach different scope. The tier legend and license bands own licensing, so no `per-user`, `per-server`,
  `priced per`, SKU, or tier language appears here (Session-16 rule, owner-reviewed).
- **No new claims.** Every phrase traces to the member rows' own verified `how_it_supports` /
  `capability_detail`. If a rationale can only be written by introducing a capability or licensing claim the
  rows don't carry, the group was misclassified.
- **A rationale is never a substitute for fixing a tier.** Where a spread looks like a possible authoring
  error, it is escalated as an open finding for a re-verification session (AUDIT-FINDINGS), not smoothed
  over with prose. A rationale that only works by explaining a tier you believe is wrong is the signal to
  escalate instead.
- **The guard is self-honest.** Every key must resolve to a live coverage-tier **spread** group (≥2 rows,
  ≥2 distinct tiers) and be em/en-dash-free. A rationale therefore **cannot outlive its spread**: if a
  future re-verification collapses a group to a uniform tier, or renames a `control_ref`, the key stops
  resolving and the build fails until the line is removed or moved. New lines ship dash-free (the PR-011
  house rule) and through `/agentic-humanizer`.

## URL state scheme

The router grammar is:

```
#/<path>[?<key>=<value>&<key>=<value>]
```

The hash is split on `?` **before** the existing `/` split, so every path route predating this scheme still works
and every link minted before it is still valid.

| Key | Values | Owner | Status |
|---|---|---|---|
| `tier` | `e3` \| `e5` \| `addon` | PR-015 | **implemented** |
| `meter` | `exclude` (absent = include) | PR-015 | **implemented** |
| `cov` | a `COV_ORDER` value, URL-encoded | coverage filter | **reserved, not implemented** — the filter is still module state |
| `term` | a glossary term, URL-encoded | PR-011 | **reserved, not implemented** — the glossary is one anchored page (`#/glossary`); `#/glossary?term=<slug>` would scroll to a single term without breaking any link, but a single page does not yet earn per-term deep links |
| `q` | search terms | search | **not migrating**; search stays on the path as `#/search/<q>` |

`#/row/<id>` is the **row deep link** (PR-004, **implemented**). It is deliberately its own route rather than a
fragment on a filtered view: a row link must resolve identically regardless of what filter was active when someone
copied it, or a shared link could land on a row the inherited filter hides. It reads only the id, so it inherits no
filter and ignores any stray query key (rule 2). It renders the row expanded with a breadcrumb and a product chip;
an unknown id renders a not-found state that names the id and links back to the framework index (rule 3), never a
blank view. Each row's expanded footer carries a **Copy link** button that copies the absolute hosted URL — built
from the baked `<link rel="canonical">` href, not from `location`, so the copied link is the public one even from a
`file://` copy. Clipboard access degrades in three tiers (async clipboard, then `execCommand`, then a selected
read-only field the reader copies by hand); the manual tier states plainly that the shown link is the hosted one.

Four rules any new key must obey:

1. **Absent key = no filter.** A default is never written into the URL. `?meter=include` is never emitted because
   include is the default; only `?meter=exclude` appears.
2. **Unknown keys are ignored, not errors** — so a later PR can add one without breaking existing links.
3. **Invalid values fall back to unfiltered** and are not honoured, rather than rendering an empty view a reader
   cannot diagnose.
4. **Filter changes use `history.replaceState`; navigation uses the hash.** Toggling a filter five times must not
   cost five presses of Back.

Focus management: each filter row carries its **own** data attribute (`data-cov`, `data-tier`, `data-meter`) and its
own `opts.focus` value. The router restores focus to the replacement of the button that was just pressed; keying
more than one row off the same attribute would bounce focus into the wrong row.

## Row id permanence

Deep links (`#/row/<id>`) make every published row id a **permanent public identifier**: it is a URL people paste
into tickets and messages, and it must keep resolving. Two rules follow.

1. **A published id is never renamed in place, and never reused for a different row.** Change a row's control
   coverage, prose, license, or product all you like; the id stays. If you rename an id, every inbound link to that
   row silently 404s with no way to tell it apart from a typo.
2. **Retiring a row removes its line from `reference/row-ids.txt` in the same commit that deletes the row.** The
   `#/row/<id>` route then serves its not-found state for that id — which names the id and points back to the
   framework index — and the id is never handed to a new row. A pointer-to-replacement tombstone is the intended
   treatment for a genuine rename-to-replacement, and gets built when the first such retirement actually happens;
   until then the graceful not-found state is the committed floor (it is needed for mistyped ids regardless).

**Build assertion.** `reference/row-ids.txt` is the committed roster of every published id, and `assemble.py`
(`check_row_id_inventory`) checks the built rows against it on every build:

- An id in the roster that **no longer exists** in the rows is a **hard failure** — an accidental rename or deletion
  that would break inbound links, caught loudly instead of shipping silently.
- An id in the rows that is **not yet in the roster** is also a failure, with a one-line instruction to bless it.

**Blessing a new id is a manual act, always.** Run `python build/update_row_ids.py --write` yourself to add new
ids to the roster (dry-run with no flag to preview). **No build or gate script ever invokes it** — that is the
whole point: a new id enters permanence only when a human deliberately commits it, so the guard cannot be satisfied
by accident. Adding a framework or product therefore has one extra step: after the rows are written, bless their
ids, then commit `reference/row-ids.txt` alongside the row module.

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
4. **Bless the new row ids** into the permanent roster: `python build/update_row_ids.py --write`, then commit
   `reference/row-ids.txt` with the module. The build fails until you do (see *Row id permanence*); this step is
   deliberately manual, so a new permanent public id is only ever created on purpose.
5. Rebuild (both commands above), then QA: re-verify a random row sample, run the URL check
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