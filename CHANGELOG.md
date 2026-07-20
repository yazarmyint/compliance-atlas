# Changelog

All notable changes to Compliance Atlas — the dataset (`compliance-atlas.json`), the rendered artifact
(`compliance-atlas.html`), and the licensing and provenance position around them.

## Versioning policy

| Bump | Means |
|---|---|
| **MAJOR** | A data-model change, or a change to what the atlas is scoped to cover. Consumers of `compliance-atlas.json` may need to change their code; readers may find rows organized differently. |
| **MINOR** | A framework, product, industry lens, or reader-facing feature added. Existing rows keep their shape and their meaning. |
| **PATCH** | Row corrections and re-verifications. Claims may change; nothing structural does. |

Two things this deliberately does **not** track. A rebuild that changes no content does not move the version —
the footer's "built" timestamp moves instead, which is why the two are shown separately. And the per-row
`last_verified` dates, not the version, are the authoritative currency signal for any individual claim.

**Entries before 2.9.0 are backfilled** from the project's own audit record (`AUDIT-FINDINGS.md`), which was
kept from the first release. They are reconstructions of milestones that were never published under a version
number, dated to when the work actually landed; the policy above was applied to them retroactively. Nothing
before 2.9.0 was ever public.

---

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
- **Added** this changelog, and a footer licence line: content CC BY 4.0, build code MIT.
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
- **Fixed** nested interactive controls inside row disclosures and several colour-contrast failures, both
  found by tooling rather than by review. Clean at WCAG 2.1 A/AA on every check axe can automate.

## 2.7.0 — 2026-07-19

- **Added** per-route document titles, so a bookmark or a pasted link identifies the view.
- **Added** page metadata (description, social preview) and taxonomy legends rendered from the dataset's own
  definitions, so the on-screen explanation of a term cannot drift from the data.
- **Changed** the public name to **Compliance Atlas**, retiring the "working title" marker the header carried.

## 2.6.1 — 2026-07-19

Repository and licensing only — the built artifact is byte-identical to 2.6.0.

- **Added** the licence position: MIT for the build code, CC BY 4.0 for the content, with the paraphrase-only
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
