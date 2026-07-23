# Changelog

All notable changes to Compliance Atlas — the dataset (`compliance-atlas.json`), the rendered artifact
(`compliance-atlas.html`), and the licensing and provenance position around them.

## Versioning policy

| Bump | Means |
|---|---|
| **MAJOR** | A data-model change, or a change to what the atlas is scoped to cover. Consumers of `compliance-atlas.json` may need to change their code; readers may find rows organized differently. |
| **MINOR** | A framework, product, industry lens, or reader-facing feature added. Existing rows keep their shape and their meaning. |
| **PATCH** | Row corrections and re-verifications. Claims may change; nothing structural does. |

**Machinery-only changes are PATCH.** Build code, tooling, documentation, and process — where no
reader gains anything, no claim moves, and the shape of `compliance-atlas.json` does not change — sort
PATCH, because the version number speaks to readers and consumers and to them nothing happened. All
three conditions must hold: a change that alters the dataset's shape is sorted by that change, not by
who it was for. This is why 2.10.0 was a MINOR — it added `meta.maintenance` to the published dataset,
which is consumer-visible — while the runbook that shipped alongside it would have been a PATCH on its
own.

**A change that never touches the built artifact takes no version bump at all — not even PATCH.** Editing
documentation that ships outside `compliance-atlas.json` (this changelog, `FRAMEWORK-SELECTION.md`, the
maintenance runbook, the READMEs) leaves the artifact byte-identical, so there is nothing to version: the
version number identifies the artifact, and a bump whose only effect would be to rewrite `meta.version`
would tell every consumer the artifact moved when it did not. The converse is the harder half, and it is
absolute: anything that *does* change the published bytes takes a bump, machinery included, down to PATCH —
because one version must identify exactly one artifact, and two different `compliance-atlas.json` files may
never both claim the same number. That is why the two `meta.maintenance` triggers added in 3.1.2 are a
PATCH, not a free ride, even though they are pure backlog bookkeeping.

**Where a bump is argued from consequence, that argument is scoped to `meta.*`.** 2.10.1 removed a
published key, `meta.generated`, and was sorted PATCH on the grounds that no realistic consumer was
relying on it. That reasoning is admissible **only for the shape of the `meta.*` namespace**, whose
keys describe the artifact rather than form part of it. Any shape change to **rows, to claims, or to
the dataset model is MAJOR unconditionally** — no argument about how few consumers exist, how recently
a field shipped, or how little the field mattered is admitted there. 2.10.1 is not a precedent for
removing a row-level field, and may not be cited as one.

Two things this deliberately does **not** track. A rebuild that changes no content does not move the version —
the footer's "built" timestamp moves instead, which is why the two are shown separately. And the per-row
`last_verified` dates, not the version, are the authoritative currency signal for any individual claim.

**Entries before 2.9.0 are backfilled** from the project's own audit record (`AUDIT-FINDINGS.md`), which was
kept from the first release. They are reconstructions of milestones that were never published under a version
number, dated to when the work actually landed; the policy above was applied to them retroactively. Nothing
before 2.9.0 was ever public.

---

## 3.4.1 — 2026-07-22

Priva reference-only treatment (PR-031, Session 17). Microsoft Priva is named on eleven privacy-row mentions
as a contributing product and has no page of its own, by design. The atlas now says so where a reader meets
it, and says why in About.

**For readers.** Every expanded row's **Related Microsoft products** block now opens with a short muted line
— *"Related-product mentions are pointers to adjacent products, not banded or audited claims"* — the same
wording the license-tier scope note already carries, so the two surfaces state one policy. And the About
page's *"Some products appear only as references"* passage is rewritten: it now says what Microsoft Priva is,
that the atlas treats it as reference-only on purpose rather than as an unfinished edge, and why — the
product roadmap closed at six mapped products and Priva sits outside it, so where a privacy control needs it
the atlas points to it rather than authoring a seventh product. No row moved; the eleven mentions are
unchanged.

**For consumers of `compliance-atlas.json`.** Nothing. Both additions live in the page template; the dataset
is byte-identical to 3.4.0 apart from `meta.version` / `meta.brand.atlas_version`, this bump itself. No row,
no `meta` key, no protected field changed.

**Why PATCH.** The change clarifies existing presentation and adds no reader capability — no route, filter,
card, or toggle. That is the line between this and 3.1.0, which was a MINOR because it *added* features (a
social card, an error-report path): the policy sorts by what a reader gains, and a reader here gains a
clarification, not a feature, while nothing structural moves. The built HTML bytes changed, so it still takes
a bump (§31). Full reasoning in AUDIT-FINDINGS §35.

## 3.4.0 — 2026-07-22

Stacked-control tier rationales (PR-013, Session 16). On the framework view, one control can carry several
product cards, and where their coverage badges differ the order can read as an inconsistency before the row
prose resolves it — the clearest case being CSF `PR.PS-04`, where the product that *generates* the log
records (Purview, Partial) sits below the one that makes them available (Sentinel, Direct). A new
group-level line now states, for the 22 stacks where that misreading risk is real, why the tiers
legitimately differ.

**For readers.** Above the stacked cards on a control whose products rate differently, a short **"Why the
tiers differ"** line explains the split in terms of role and scope — which product runs the namesake
activity, which covers a slice, which reaches a different part of the estate. It appears only where a
reader could reasonably misread the badges; stacks whose spread is self-explanatory (the primary product
rates highest) are left unannotated. The lines make no new coverage or licensing claim: they restate what
the rows already say, and licensing stays with the tier legend.

**For consumers of `compliance-atlas.json`.** The dataset gains one key, `meta.stack_rationales` (a
`framework → control_ref → rationale` map, 22 entries), and is otherwise byte-identical to 3.3.0 apart from
`meta.version` and `meta.brand.atlas_version`. No row moved — every row is byte-identical, including every
coverage, confidence, licensing, source, and last-verified field. The lines live in one place
(`build/stack_rationales.py`), and a build guard fails if any key is not a live coverage-tier spread, so the
prose cannot drift from the data it explains.

**Why MINOR.** A reader-facing feature was added and existing rows kept their shape and meaning — the exact
shape of 3.3.0's `meta.glossary` and 2.10.0's `meta.maintenance`: a new consumer-visible key under `meta`,
additive, no data-model or scope change, so no consumer must change code. Not PATCH — readers gain a
capability, not a correction; no protected field moved. Full record in AUDIT-FINDINGS §34.

## 3.3.0 — 2026-07-22

Reader glossary (PR-011, Session 15). The atlas assumes fluency in two vocabularies at once — compliance
frameworks and the Microsoft security stack — and a reader who knows one half hits an acronym wall in the
other. A new **Glossary** defines the 47 acronyms and initialisms that recur across the rows, in plain
language, reachable from the footer and cross-linked from About.

**For readers.** `#/glossary` lists every recurring acronym (DLP, XDR, CSPM, MDCA, ROPA, CDE, C3PAO, GCC
High …) with a one- or two-sentence definition written for whichever half of the material you don't
already know. Definitions describe the term and never make a coverage or licensing claim — those stay on
the rows. A restrained first-use `<abbr>` pass in the About page expands the framework short-forms and a
handful of capability acronyms on hover; row and list prose are deliberately left unmarked, because
"first use" is meaningless once a filter reorders the page.

**For consumers of `compliance-atlas.json`.** The dataset gains one key, `meta.glossary` (a
`term → definition` map), and is otherwise byte-identical to 3.2.0 apart from `meta.version` and
`meta.brand.atlas_version`. No row key added or removed, no schema or scope change. The definitions live
in one place (`build/glossary.py`), so the rendered page and the JSON cannot drift.

**Why MINOR.** A reader-facing feature was added and existing rows kept their shape and meaning. This is
the exact shape of 2.10.0, which added `meta.maintenance`: a new consumer-visible key under `meta`,
additive, no data-model or scope change, so no consumer must change code. Not PATCH — readers gain a
capability, not a correction. Full record in AUDIT-FINDINGS §33.

## 3.2.0 — 2026-07-21

Row deep links (PR-004, Session 14). Any single mapping row is now citable on its own. `#/row/<id>`
resolves to a dedicated view of that row, rendered expanded, with a breadcrumb and product chip so the
reader can see which framework, control, and product it is and reach the surrounding framework in one
click. Every row's expanded footer gains a **Copy link** button.

**For readers.** Paste `#/row/<id>` and you land on that one row, the same way regardless of any filter
active when the link was made. A copy button on each row hands you the public link to it. An unknown id
shows a not-found state that names the id and points back to the framework index, rather than a blank
page. The copied link is always the hosted `compliance-atlas.html` address, even when you are reading a
downloaded `file://` copy, because a local path was never shareable and the row id is the same in both.

**For consumers of `compliance-atlas.json`.** Nothing changes but the version. The dataset is
byte-identical to 3.1.2 apart from `meta.version` and `meta.brand.atlas_version`: no row key added or
removed, no schema or scope change. Row ids, always present, are now also **permanent public
identifiers** — a published id is never renamed or reused, so a link minted today keeps resolving. A new
committed inventory, `reference/row-ids.txt`, and a build check enforce that; both live in the repo, not
the dataset.

**Why MINOR.** A reader-facing feature was added and existing rows kept their shape and meaning, which is
the MINOR band. It is not MAJOR: no data-model or scope change, and the id inventory and its build guard
are machinery, not part of the dataset. It is not PATCH: readers gain a capability, not a correction. The
feature's bytes live in `compliance-atlas.html`, which moved, so a bump is required. Full record in
AUDIT-FINDINGS §32.

## 3.1.2 — 2026-07-21

Framework-backlog decisions (Session 13). CJIS Security Policy v6.0 was evaluated and **deferred** —
not declined, not mapped — and two dated maintenance triggers were added to record the conditions under
which it is reconsidered. The rest of the session is docs-only decision records that do not touch the
artifact.

**For consumers of `compliance-atlas.json`.** `meta.maintenance.triggers` gains two entries:
`TRG-CJIS-DEMAND` (a demand-criterion check, next review 2026-08-20) and `TRG-CJIS-V6-REVISIT` (CJIS v6.0
P2-P4 controls fully auditable, next review 2027-10-01). No row, no claim, and no other `meta` value moved.

**For readers.** Nothing visible changes: the maintenance table is maintainer metadata carried in the
dataset, not rendered in the page.

**Recorded elsewhere.** The full evaluation (both drafted entries, the demand thresholds, and the
no-page-instrumentation ruling), the SEC 17a-4/FINRA re-ranking, and the NIS2 / DORA / ISO 27701:2025
rejection rationales are in `FRAMEWORK-SELECTION.md` and AUDIT-FINDINGS §31; the framework backlog in
`docs/MAINTENANCE.md` is re-ranked to match.

**Why PATCH.** The two triggers change the published bytes of `compliance-atlas.json`, so the
machinery-only rule applies: machinery that alters the artifact is a PATCH. The version must uniquely
identify one artifact — two different JSON files may never both claim 3.1.1 — so bookkeeping that changes
the bytes still bumps. The docs-only records that shipped alongside touch no artifact and take no bump,
per the clarifying line added to the versioning policy this session.

## 3.1.1 — 2026-07-21

Spelling unification. A manual edit had left the British spelling of "license" mixed in with the
American spelling the atlas uses everywhere else, and the mix had become reader-visible — most
obviously in the license-tier legend, where a boundary row's definition carried the British form.
Every occurrence in shipped text is now American "license" (noun and verb).

**For readers.** The four license-tier legend/definition strings read "license" consistently. Nothing
else visible changes.

**For consumers of `compliance-atlas.json`.** Four `meta.license_band*` definition strings change by a
single letter each; the four values are otherwise byte-identical. No row, no claim, no
`license_requirement`, no source, and no `last_verified` moved — spelling is not verification, so live
source re-verification was waived (drift ledger and the three-way protected-field check in
AUDIT-FINDINGS §30).

**Guardrail.** A build-failing spelling lint (`BANNED_SPELLINGS`) now scans the outputs and shippable
docs on every build, so the British spelling cannot creep back in — including into this changelog,
which is why the before-form is recorded only in the §30 ledger (a dated record the lint excludes).

**Why PATCH.** Corrections, not features: no claim moved, no row shape changed, and the §27.4
row-shape-is-MAJOR fence does not apply (nothing at row level was touched). Squarely a PATCH.

## 3.1.0 — 2026-07-20

Reader-facing polish: a legend that fits again, an invitation to report errors, and a social card
for shared links. No row changed — `compliance-atlas.json` is byte-identical to 3.0.0 apart from the
version field itself.

**For readers.**

- **The "How to read a mapping" legend is compact again (PR-059).** Its four taxonomies had spilled
  onto two rows with the License tier column running more than twice the height of its neighbours;
  the legend now lays out in balanced columns whose width drives the column count, and the long
  commercial-licensing scope note moved into a collapsed **"scope & limitations"** disclosure beneath
  it. The taxonomy definitions themselves stay visible by default, and the commercial-only caveat
  stays in the always-visible summary. The legend block is 30–47% shorter at desktop widths.
- **A way to say something's wrong.** The footer now carries *"Spotted an error? Open an issue,"*
  and the about page's existing corrections invitation is unchanged. Corrections are recorded.
- **A social card.** Sharing an atlas link now previews a card with the atlas name and subtitle in
  the site's own visual language, instead of a bare URL.

**For consumers of `compliance-atlas.json`.** Nothing. The dataset is unchanged; the additions are
in the page template, the docs, and a committed image asset. The only JSON movement is
`meta.version` / `meta.brand.atlas_version`, this bump itself.

**Why MINOR.** The policy sorts a bump by what a reader gains, and a reader gains a link-preview card
and a clearer error-report path — "reader-facing feature added," the MINOR trigger. Existing rows
keep their shape and meaning (not MAJOR), and nothing here is a row correction (PATCH would undersell
it). The counter-argument — that every prior MINOR coincided with a *dataset* addition and this one
leaves the JSON byte-identical — was weighed and set aside: the policy says *reader*, not *JSON
consumer*. Full reasoning in AUDIT-FINDINGS §29.5.

## 3.0.0 — 2026-07-20

The license-tier lens (PR-015). Both stated user stories end "…and at what license tier?", and
until now the artifact could not answer it: the entitlement string was on every row but reachable
only by expanding rows one at a time.

**For readers.** Every row now carries a coarse **license tier band** — `E3`, `E5`, `Add-on`,
`Consumption`, or `n/a` — shown as a chip in the row summary and explained in the row's license
block. The framework view gains a **tier filter**, so you can ask "what does ISO 27001 look like
if I only own E3?" and get an answer. Rows where the band is the *floor* rather than the whole
story carry a **partial** badge meaning "reduced capability at this tier — read the license
requirement". That badge is not decoration: **114 of the 175 E3-band rows carry it**, so "E3"
alone would systematically over-promise without it.

The band never replaces the verbatim license string, which stays rendered in full on every row.
It is a coarse signpost derived from that string, and where the two seem to disagree the string
is the authority.

Two limits stated wherever the feature is explained: bands describe **commercial** Microsoft 365
licensing only (no G3/G5, F-series, or Business Premium dimension — government licensing stays in
the per-row cloud availability notes), and **consumption-priced products have no seat tier at
all**. Sentinel and Defender for Cloud are metered per GB and per resource and do not care which
seat SKU you hold, so they sit on their own axis: a separate include/exclude toggle, defaulting to
include, rather than a fifth tier. Related-product "(if licensed)" mentions are pointers, not
banded claims.

**For consumers of `compliance-atlas.json`.** Two new row keys, both **additive** — no existing
key changed, moved, or was removed:

- `license_band` — one of `e3` | `e5` | `addon` | `consumption` | `na`
- `license_band_partial` — boolean

Plus `meta.license_bands`, `meta.license_band_partial`, and `meta.license_band_scope` carrying the
reader-facing definitions. Existing code that ignores unknown keys needs no change.

**Why MAJOR rather than MINOR,** given the change is additive and breaks nothing: the policy above
defines MAJOR as *a data-model change*, not as a breaking change, and defines MINOR as *existing
rows keep their shape* — which they do not here. AUDIT-FINDINGS §27.4 additionally rules that any
shape change to rows is MAJOR unconditionally, with no consumer-population argument admitted. The
argument that additive changes are harmless is exactly the class of reasoning that scoping was
written to exclude. Sorted MAJOR on the policy as written; amending the policy to sort additive
row changes as MINOR is a separate discussion to have on its own merits, not while holding a
change that would benefit from it.

- **Added** `build/license_bands.py`: the 49-entry mapping from licensing constant to band, the
  floor-determination rules F1–F7, and the two-entry row-override table. The mapping is keyed on
  the **constant coordinate**, not on the 110 distinct prose strings those constants compose into
  and not on substring heuristics over prose — so it is a reviewed table, not a pile of guesses.
- **Added** four build guards, all hard failures: a licensing constant with no band (G1), a row
  whose license string matches no constant and is not the `n/a` literal (G2), a band that
  disagrees with `licensing_model` about consumption or boundary status (G3), and a tier claim
  written into row prose where the mapping cannot see it (G4). There is no silent default band.
- **Added** URL state for the tier filter and consumption toggle: `#/framework/<id>?tier=e3`,
  `?meter=exclude`. A filtered view is now linkable. The complete key registry — including `cov`
  and PR-004's `#/row/<id>`, both reserved and deliberately unimplemented — is in
  `docs/AUTHORING.md` so PR-004 inherits the scheme instead of retrofitting it.
- **Unchanged:** `license_requirement` and `licensing_model` were read and not written. No claim
  moved, no coverage or confidence rating changed, and no `last_verified` date moved.

## 2.10.1 — 2026-07-20

Build integrity. Nothing a reader sees changes; nothing in any row changes.

- **Removed** `meta.generated` from `compliance-atlas.json`. The dataset now contains nothing
  time-derived, so a rebuild that changes no content leaves it byte-identical — which turns
  `git diff compliance-atlas.json` into a strict drift check instead of one that tolerated a
  one-line floor. The footer's **built** timestamp is unaffected as a feature: `build_html.py`
  stamps it into the page at generation time, in the same format, rendering the same line.
- **Changed** `compliance-atlas.html` accordingly: it now carries the moving timestamp on its own and
  diffs on every rebuild. That is deliberate. The dataset is the artifact held byte-stable; the
  timestamp is a property of the page.
- **Fixed** a build defect that could produce a confidently wrong artifact. Python validates cached
  bytecode on `(mtime, size)`, so a same-length edit — a date or a SKU string changed in place,
  rebuilt in the same second — could leave the build importing stale code and regenerating the
  dataset from the old values, silently and with exit 0. The build entry points now clear
  `build/__pycache__` before importing anything. This replaces a manual step in the maintenance
  runbook, which only worked as far as it was remembered.
- **Note on the version bump.** Machinery only, so PATCH under the policy above — with one argument
  against it recorded rather than buried: removing `meta.generated` removes a *published* key, and
  the MAJOR row covers changes where consumers of the JSON may need to change their code. The key was
  a build timestamp carrying no claim, it was public for two weeks, and a 3.0.0 on an atlas whose
  content did not move would misinform every reader about what happened. Sorted PATCH on that
  reasoning; the full argument both ways is in AUDIT-FINDINGS §27.4.

---

## 2.10.0 — 2026-07-20

Maintenance machinery. Nothing a reader sees changes; nothing in any row changes.

- **Added** a structured maintenance-trigger table to the dataset at `meta.maintenance`, replacing the
  prose list that had grown to twenty undated bullets in `docs/MAINTENANCE.md`. Each trigger carries a
  type, a cadence, a next-review date, the constants and rows it affects, and the date it was last
  executed. Triggers are now defined in exactly one place.
- **Added** build-time staleness warnings. `python build/assemble.py` reports triggers past their
  review date and licensing constants past their volatility-class cadence, and flags retired product
  names appearing without their "(formerly …)" gloss. Warnings go to stderr and are advisory — the
  build still succeeds, so an unrelated fix can ship while claims are aging.
- **Added** the re-verification runbook to `docs/MAINTENANCE.md`: how a recurring pass is scoped,
  sourced, recorded, and gated. The project's recurring process had never been written down.
- **Note on the version bump.** This is additive and structural: the JSON gained a key under `meta`,
  and the row data model is untouched. The policy below sorts MINOR by what a reader gains and PATCH
  by what a claim gains, and this is neither — it is maintainer machinery. It is filed as MINOR
  because the discriminator that actually separates the bands is compatibility: MAJOR is reserved for
  changes where consumers of `compliance-atlas.json` may need to change their code, and nobody needs
  to change code for an added key.
- No coverage level, confidence level, cited source, or `last_verified` date was touched, and the row
  count is unchanged at 378.

## 2.9.1 — 2026-07-20

- **Fixed** inconsistent spelling: the atlas mixed British and American English, sometimes within a
  single view. Rendered text is now American English throughout — 53 strings across 27 rows, plus the
  README, changelog, license documents and authoring docs. The most visible cases were
  `organisational`, `pseudonymisation`, `minimisation`, `labelled` and `fulfilment`.
- **Note on the GDPR rows.** Eleven of them carried `organisational` and `minimisation` because that
  is the spelling of the regulation's own authentic English text. They were changed anyway: these are
  `control_intent` and `how_it_supports` fields, which this project defines as paraphrase and which
  deliberately reproduce no source text, so nothing quoted was altered. Readers searching the
  regulation's exact phrasing should expect the `-isation` forms there.
- No claim changed. No coverage level, confidence level, cited source, or `last_verified` date was
  touched, and the row count is unchanged at 378.

## 2.9.0 — 2026-07-20

Everything a reader needs around the dataset, rather than in it.

- **Added** an about/methodology page at `#/about`, linked from the header nav and the footer: what the atlas
  is and is not, how a row is made and sourced, what the coverage and confidence taxonomies mean, where scope
  stops, how current it is, who maintains it, and how to report an error.
- **Added** two industry lenses, both drawn entirely from frameworks already shipped: **Legal & professional
  services** (SOC 2, ISO 27001, GDPR, HIPAA) and **Insurance** (GLBA Safeguards, SOC 2, PCI DSS, NIST CSF 2.0).
  Zero new rows. The Insurance lens states the caveat that the FTC Safeguards Rule these rows cite exempts
  state-regulated insurers, whose operative text is normally the NAIC model law.
- **Added** a statement of which industries are deliberately absent and which framework each would need —
  state & local government (CJIS), energy & utilities (NERC CIP), pharmaceuticals & medical devices
  (21 CFR Part 11) — on the Industries index and in full on the about page.
- **Added** this changelog, and a footer license line: content CC BY 4.0, build code MIT.
- **Changed** the footer to separate content version from build timestamp, so a rebuild that changed nothing
  no longer looks like an update.
- **Changed** two rows' citations (`csf-de-cm-03-ai`, `gdpr-35`) off the deprecated "DSPM for AI (classic)"
  article and onto the current unified Data Security Posture Management article.
- **Changed** the Financial services lens note to stop claiming insurers, who now have their own.

## 2.8.1 — 2026-07-20

- **Fixed** the licensing and source claims across the atlas in a full re-verification pass against live
  sources. Every coverage and confidence verdict survived unchanged; the defects were naming drift and
  under-listed SKU entitlements. Seven cited URLs were repointed to current canonical targets, and
  `tools/check_urls.py` was added as standing QA for citation resolution and redirect drift.
- **Fixed** an over-broad `last_verified` policy: 324 of 378 rows were re-dated on evidence, and 54 were
  deliberately left alone rather than bulk-stamped.

## 2.8.0 — 2026-07-19

- **Added** keyboard and screen-reader accessibility: reachable navigation, per-view focus management, a
  status region that announces the view a reader lands on, and a skip link that works with the hash router.
- **Fixed** nested interactive controls inside row disclosures and several color-contrast failures, both
  found by tooling rather than by review. Clean at WCAG 2.1 A/AA on every check axe can automate.

## 2.7.0 — 2026-07-19

- **Added** per-route document titles, so a bookmark or a pasted link identifies the view.
- **Added** page metadata (description, social preview) and taxonomy legends rendered from the dataset's own
  definitions, so the on-screen explanation of a term cannot drift from the data.
- **Changed** the public name to **Compliance Atlas**, retiring the "working title" marker the header carried.

## 2.6.1 — 2026-07-19

Repository and licensing only — the built artifact is byte-identical to 2.6.0.

- **Added** the license position: MIT for the build code, CC BY 4.0 for the content, with the paraphrase-only
  authoring rule promoted to a condition on anyone adapting the work.
- **Removed** redistribution-restricted source documents (AICPA, PCI SSC, and vendor material) from the tree
  before any commit history existed, and recorded the provenance and re-download route for every file kept.

## 2.6.0 — 2026-07-19

- **Changed** the presentation layer to progressive disclosure: a plain-language summary on top, the full
  detail one interaction away. Nothing was deleted — depth moved rather than shrank.

## 2.5.1 — 2026-07-18

- **Changed** prose across all six products in a style-only pass, removing machine-writing tells and the
  consultant-reader lens so the atlas reads the same for an in-house engineer or a curious reader. No claim,
  citation, or verdict changed.

## 2.5.0 — 2026-07-18

- **Added** Microsoft Defender for Cloud (40 rows) — the sixth and final product. **The product roadmap is
  now closed.** Atlas total 378 rows.
- Mapping discipline for it: assesses and detects, does not remediate. Its regulatory compliance dashboard
  rows all carry the caveat that the dashboard assesses onboarded cloud resources, never Microsoft 365
  workloads, and is not an attestation.

## 2.4.0 — 2026-07-18

- **Added** Microsoft Sentinel (46 rows), and with it the first consumption-priced product, which required a
  licensing model expressed as meters rather than SKUs. Atlas total 338 rows.
- Mapping discipline for it: evidences and detects, does not enforce.

## 2.3.0 — 2026-07-17

- **Added** Microsoft Defender XDR (53 rows) across four workloads. Atlas total 292 rows.

## 2.2.0 — 2026-07-17

- **Added** Microsoft Intune (41 rows). Atlas total 239 rows.

## 2.1.0 — 2026-07-17

- **Added** Microsoft Entra (48 rows) as the second product, establishing the template every later product
  reused. Atlas total 198 rows.

## 2.0.0 — 2026-07-17

**Breaking.** The atlas stopped being a Purview reference and became a multi-product one.

- **Changed** the data model: every row now carries a product, and cross-product relationships became
  structured fields rather than free text.
- **Changed** the canonical filenames to `compliance-atlas.json` / `compliance-atlas.html`.
- No content changed in the same step — the refactor was proven against a field-level diff of the 150-row
  pre-refactor snapshot.

## 1.1.0 — 2026-07-17

- **Added** NIST SP 800-53 Rev 5 as a curated data-protection subset (21 rows) and FERPA (5 rows), taking the
  atlas to 11 frameworks and 150 rows.
- **Added** a US federal / FedRAMP-adjacent industry lens.

## 1.0.0 — 2026-07-16

- First release: 124 rows mapping Microsoft Purview against 9 frameworks — Microsoft SSPA DPR, ISO/IEC
  27001:2022, SOC 2, HIPAA Security Rule, NIST 800-171 R2 / CMMC L2, NIST CSF 2.0, PCI DSS v4.0.1, GLBA
  Safeguards Rule, and EU GDPR — with 9 industry lenses.
- Established the conventions everything since has kept: version-pinned frameworks, paraphrased control
  intent rather than quoted standard text, at least one official and one Microsoft source per row, a
  four-level coverage and three-level confidence taxonomy, and boundary rows that record where a product
  does *not* reach.
