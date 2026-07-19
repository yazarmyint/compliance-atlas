# CONTENT-REVIEW — editorial audit (Phase 1, report only)

**Date:** 2026-07-18 · **Scope:** Task A (prose length/depth/voice consistency) + Task B (remove the consulting lens) · **Status:** PROPOSAL — no source files edited. Awaiting approval by finding ID before any Phase 2 change.

> **How to respond:** approve all, or a subset by ID (e.g. "apply CR-001, CR-004..CR-012, skip CR-018"). Findings marked **DECISION** need your call on direction, not just yes/no. Nothing here has been applied.

---

## 0. Conclusion first

- **Task A is real and measurable.** User-facing prose length is driven by *when* an entry was last touched, not by editorial intent. Industry notes span **9–166 words** on the same card grid; product notes **27–222w**; solution scope **9–109w**. The four "un-expanded" industry cards (K-12 14w, Manufacturing 9w, Higher-ed 21w, MS-supplier 14w) read as stubs beside the six multi-product notes (DIB 166w, Healthcare 121w, Federal 120w, …).
- **Tier 2 (row narratives) has the same pattern but by product, not at random.** `capability_detail`/`how_it_supports` grow monotonically with authoring recency: Purview ≈16/25w → Sentinel ≈49/50w → Defender-for-Cloud ≈50/56w. Within each product the spread is small (σ ≈ 5–9w). Recommendation is **conservative top-end trimming + no expansion**, as a separately-approved pass — **no row rewrites proposed here** (per instructions).
- **Task B is small and mostly surgical.** 7 rendered consulting-lens hits to neutralise, 2 SOC 2 uses that are domain-correct (**DECISION**), README's framing line, and 1 non-rendered code comment. Most apparent "client/engagement/advisory" hits are **false positives** and must be left alone (see §4.1).
- **Guardrail check:** every proposal below is editorial. None touches coverage, confidence, licensing values, URLs, sources, status, dates, control refs, or product/solution assignments. Where tightening would drop a factual claim, it is flagged **DECISION** rather than rewritten.

**Location correction:** the Tier-1 brief points at `build/common.py` for `INDUSTRIES`; `INDUSTRIES`, `BRAND`, `FOOTER_LINES`, and `META` (incl. the rendered disclaimer) actually live in **`build/assemble.py`**. `PRODUCTS`, `SOLUTIONS`/`*_SOLUTIONS`, and the `*_LIC`/`GOV` strings live in `common.py`. Findings cite the true file.

---

## 1. Proposed style targets per content type (Task A, Tier 1)

Each is a rendered surface. "Renders where" is verified against `template.html`.

| Content type | Source | Renders where | Current range | **Proposed target** | Structural pattern |
|---|---|---|---|---|---|
| **Industry note** | `assemble.py → INDUSTRIES[x].note` | Home card `.desc` + industry-page `.full` | 9–166w (σ≈57) | **35–75 words, 2–4 sentences** | S1: anchor framework(s) + who it applies to (every card). S2–S4: only the *distinctive* stack hooks for that industry, one clause per product that has a genuine story. No padding where a lens is genuinely thin — floor is a complete S1+one hook, not filler. |
| **Product note** | `common.py → PRODUCTS[x].notes` | Product-pivot card `.desc` + product-page callout | 27–222w | **60–110 words** | S1: product identity in one line. S2: licensing model in a phrase. S3: mapping-discipline sentence (the "evidences not enforces" / "assesses not remediates" line). Deep licensing minutiae belong in the `*_LIC` strings, not the note. |
| **Solution scope** | `common.py → SOLUTIONS[x].scope` | Solution card `.desc` + solution-page header | 9–109w | **15–40 words** | A scannable capability list (noun phrases), one register throughout. Expand the terse Purview stubs to a floor; compress the MDC 100w+ scopes to a ceiling. |
| **Framework `notes`** | `rows_*.py → FRAMEWORK["notes"]` | Framework-page `.callout` | 25–155w | **25–60 words** | One idea per note: the key scoping caveat / deliberate exclusion. Trim the 800-53 outlier (155w). |
| **Framework `applies_to`** | `rows_*.py → FRAMEWORK["applies_to"]` | Framework/industry card `.desc` | 8–18w | **10–20 words** (already conformant) | Who the framework binds. No action beyond Task B fix on SOC 2. |

**Voice (all types):** keep the atlas's existing register — dense, factual, semicolon/em-dash tolerant, no promotional adjectives, no second-person imperative except in the landing hero. The goal is *consistency of density*, not a rewrite of the voice. Sample rewrites in §3 model it.

---

## 2. Findings table

Task codes: **A1** = Task A Tier-1 (presentation layer, actionable) · **A2** = Task A Tier-2 (row narratives, report-only) · **B** = Task B (de-consulting).
"Rewrite?" → **§3** means a full proposed rewrite is provided; "dir." means direction only (rewrite deferred to Phase 2 on approval).

| ID | File · location | Task | Current excerpt (wc) | Issue | Recommended change | Rewrite? |
|---|---|---|---|---|---|---|
| **CR-001** | `assemble.py` · `INDUSTRIES` (all 10 notes) | A1 | notes span 9–166w | Length set by authoring recency, not intent; stubs beside essays on one grid | Adopt the 35–75w / S1+hooks target (§1). Expand 4 stubs; trim 3 long. Sub-findings below. | §3 (3 samples) |
| CR-002 | `INDUSTRIES["k12"].note` | A1 | "FERPA anchors; state student-privacy laws on backlog; CSF 2.0 is the working security baseline." (14w) | Stub; no stack-role sentence | Expand to target, grounded only in existing FERPA/CSF rows | **§3.1** |
| CR-003 | `INDUSTRIES["manufacturing"].note` | A1 | "800-171/CMMC applies to DIB suppliers; GDPR for EU operations." (9w) | Shortest; omits its own CSF/ISO frameworks entirely | Expand; name all four frameworks it lists; cross-ref DIB lens | **§3.2** |
| CR-004 | `INDUSTRIES["higher-ed"].note` | A1 | "FERPA governs education records; Title IV institutions also answer to the GLBA Safeguards Rule (FSA-enforced). State student-privacy laws remain on backlog." (21w) | Stub relative to peers | Expand to floor with GLBA/FERPA stack hooks already in-atlas | dir. |
| CR-005 | `INDUSTRIES["ms-supplier"].note` | A1 | "SSPA enrollment drives DPR compliance; ISO 27001 certification can qualify for SSPA alternative-compliance paths." (14w) | Stub | Expand to floor (DPR is the anchor product story — Purview-dense) | dir. |
| CR-006 | `INDUSTRIES["dib"].note` | A1 | 166w, one sentence per product | Longest; over the 75w ceiling | Tighten wording to ≤~120w keeping **all four** product hooks; going <110w drops a product claim → **DECISION** | **§3.3** |
| CR-007 | `INDUSTRIES["healthcare"].note` | A1 | 121w | Over ceiling | Tighten to ≤~90w without dropping claims | dir. |
| CR-008 | `INDUSTRIES["federal"].note` | A1 | 120w | Over ceiling | Tighten to ≤~90w without dropping claims | dir. |
| CR-009 | `INDUSTRIES["finserv"/"retail"].note` | A1 | 110w / 109w | Slightly over ceiling | Light trim to ≤~90w | dir. |
| CR-010 | `common.py` · `PRODUCTS` notes (6) | A1 | 27–222w | Purview stub (27w) vs Sentinel 193w / MDC 222w | Apply 60–110w target: expand Purview/Entra; compress Sentinel/MDC top-matter. **DECISION:** compression must not drop a licensing fact — move detail to `*_LIC`, don't delete | dir. |
| CR-011 | `common.py` · `SOLUTIONS`/`*_SOLUTIONS` scope (38) | A1 | 9–109w | Purview scopes 9–16w (noun stubs) vs MDC 106–109w | Apply 15–40w target; expand Purview stubs, compress MDC scopes | dir. |
| CR-012 | `rows_80053.py` · `FRAMEWORK["notes"]` | A1 | 155w | 3× the next-longest framework note | Trim to ≤60w; keep the Release 5.2.0 currency callout | dir. |
| **CR-013** | `template.html` · `vHome()` lede (l.375) | B | "Pick the **client's** industry, drill into the frameworks **they** answer to…" | Assumes a consultant advising a third party (highest-visibility copy) | "Pick an industry, open the frameworks it answers to, and read off each control's product mappings: claim strength, license tier, evidence examples, and the source behind every statement." | **§3.4** |
| **CR-014** | `template.html` · `vHome()` h2 (l.385) | B | "Start from the **client's** world" | Same | "Start from an industry" | **§3.4** |
| CR-015 | `common.py` · `PRODUCTS["sentinel"].notes` (l.97) | B | "Cost levers that matter to **clients**:" | Consulting lens | "Cost levers that matter:" | dir. |
| CR-016 | `assemble.py` · `FOOTER_LINES[3]` (l.79) | B | "…so **verify at engagement time**." | Presumes a consulting engagement (rendered in every page footer) | "…so verify before relying on it." | dir. |
| CR-017 | `assemble.py` · `META["disclaimer"]` (l.112) | B | "…and can change; **verify at engagement time**." | Same (rendered as footer disclaimer) | "…and can change; verify before relying on it." | dir. |
| CR-018 | `rows_171.py` · `FRAMEWORK["notes"]` (l.29) | B | "…confirm tenant-specific feature status **at engagement time**." | Consulting lens | "…confirm tenant-specific feature status before relying on it." | dir. |
| CR-019 | `rows_glba.py` · `compliance_manager_template["note"]` (l.17) | B | "…confirm safeguards-element coverage **at engagement time**." | Consulting lens (renders as the CM-chip tooltip) | "…confirm safeguards-element coverage before relying on it." | dir. |
| CR-020 | `rows_soc2.py` · `FRAMEWORK["applies_to"]` (l.21) + `["notes"]` (l.22) | B | "criteria selected per **engagement scope**" · "applicability varies by **engagement**" | **DECISION:** in SOC 2, *engagement* is the correct term for the CPA examination — accurate for in-house and consultant alike. Not the consulting-reader lens. | Recommend **KEEP**. If you want zero "engagement" tokens, soften to "per examination scope" / "varies by examination". | dir. |
| CR-021 | `README.md` l.5 | B | "engagement-agnostic reference" | Frames neutrality in consulting terms | "role-agnostic reference" | dir. |
| CR-022 | `README.md` l.6 | B | "**This client** operates in industry X and is subject to framework Y…" | The headline example assumes a client | "An organization operates in industry X and is subject to framework Y…" | dir. |
| CR-023 | `README.md` l.121 | B | "boundary rows … encouraged where **consultants will ask** the question anyway" | Consulting lens (author-guidance section) | "…where the question comes up anyway" | dir. |
| CR-024 | `README.md` l.222 | B | "before relying on MDVM-premium capabilities **in CMMC engagements**." | Maintainer "Maintenance triggers" section; low visibility | "…in CMMC assessments." (optional) | dir. |
| CR-025 | `common.py` l.428 (code comment) | B | "…the pivot that **consultants** actually reason in" | **Non-rendered** Python comment — not user-facing | Optional: "…the pivot the functional surfaces map to." Include only if you want the source itself lens-free. | dir. |
| CR-026 | `README.md` l.20, l.56 · "the deliverable" | B | "the deliverable (generated…)" | Build-artifact sense, not client-deliverable | **Likely KEEP** (means build output). Flag only; change to "the output" if you want zero "deliverable" tokens. | dir. |

---

## 3. Sample rewrites (representative subset — judge the voice here)

Grounding note: every expansion below draws **only** on facts already present in that industry's mapped rows or already stated in the note. No new coverage/licensing claim is introduced.

### 3.1 CR-002 · K-12 education (14w → 46w)
> **Before:** FERPA anchors; state student-privacy laws on backlog; CSF 2.0 is the working security baseline.
>
> **After:** FERPA governs the education records K-12 districts hold; CSF 2.0 is the working security baseline where no sector mandate applies. The Microsoft stack's role here is protecting and locating those records — sensitivity labeling and DLP over student data, eDiscovery and audit for records requests and access logging. State student-privacy laws remain on backlog.

*(Draws on existing FERPA rows: §99.31 Information Protection + DLP, §99.10 eDiscovery, §99.32 Audit.)*

### 3.2 CR-003 · Manufacturing (9w → 44w)
> **Before:** 800-171/CMMC applies to DIB suppliers; GDPR for EU operations.
>
> **After:** Manufacturers straddle two regimes: CSF 2.0 and ISO 27001 as general security baselines, and NIST 800-171 / CMMC for the defense-industrial-base suppliers among them, with GDPR reaching any EU operations. The stack maps most heavily on the 800-171 endpoint, audit, and detection families — the rows detailed under the Defense industrial base lens.

*(Names all four frameworks the lens already lists; cross-references the DIB note rather than restating it.)*

### 3.3 CR-006 · Defense industrial base (166w → 121w, all four product hooks preserved)
> **After (tightened; DECISION if you want it shorter):** CMMC Level 2 Phase 2 (third-party certification in new contracts) begins Nov 10, 2026; GCC High notes sit on every 800-171 row. Intune anchors the endpoint CM / mobile / encryption families (3.1.18/3.1.19, 3.4.1/3.4.2, 3.13.16), though Windows Autopilot and update policies are limited in GCC High/DoD. Defender XDR carries the assessment-heavy 3.11/3.14 detection band (MDVM scanning, malware protection, system monitoring) plus 3.6 incident response — all workloads run in GCC High/DoD, though Microsoft Threat Experts does not. Sentinel carries the 3.3 audit-and-accountability band (3.3.1 create/retain, 3.3.4 failure alerting, 3.3.5 correlation); multi-year retention is a consumption meter at data-lake rates. Defender for Cloud assesses CUI cloud enclaves for 3.11.2–3.11.3 and 3.12 — cloud-resource scope only, with CIEM and several CSPM features absent in Azure Government.
>
> *Every control ref and product claim in the 166w original is retained; only connective wording was cut. Trimming below ~110w would require dropping a product hook — flagged for your decision, not done here.*

### 3.4 CR-013 / CR-014 · Landing hero
> **h2 before:** Start from the client's world → **after:** Start from an industry
>
> **lede before:** Pick the client's industry, drill into the frameworks they answer to, and read off each control's product mappings: claim strength, license tier, evidence examples, and the source behind every statement.
>
> **lede after:** Pick an industry, open the frameworks it answers to, and read off each control's product mappings: claim strength, license tier, evidence examples, and the source behind every statement.

*(Reads identically for an in-house engineer, a consultant, or a curious reader. Meaning unchanged.)*

---

## 4. Tier 2 (row narratives) — statistical summary + recommended approach (NO rewrites)

Fields audited across all 378 rows: `control_intent`, `capability_detail`, `how_it_supports`, `config_evidence_example`, `operational_evidence_example`. Word counts computed from the assembled JSON (what actually renders).

### 4.1 Distribution per field, per product (mean words; σ in parens)

| Field | purview (150) | entra (48) | intune (41) | defender-xdr (53) | sentinel (46) | defender-cloud (40) | **overall σ** |
|---|---|---|---|---|---|---|---|
| `control_intent` | 14.8 (5.0) | 14.1 (4.0) | 14.7 (6.3) | 16.4 (6.9) | 15.8 (6.5) | 17.4 (6.6) | 5.8 |
| `capability_detail` | 15.9 (5.2) | 17.6 (3.3) | 27.9 (4.7) | 37.0 (6.5) | 49.0 (5.2) | 50.0 (6.7) | **14.7** |
| `how_it_supports` | 25.0 (6.9) | 21.1 (4.2) | 32.3 (4.3) | 33.3 (6.7) | 49.7 (6.9) | 55.8 (9.2) | **13.3** |
| `config_evidence_example` | 8.5 (2.8) | 8.9 (2.2) | 11.7 (2.6) | 16.4 (3.8) | 17.4 (2.8) | 19.6 (3.2) | 5.2 |
| `operational_evidence_example` | 7.1 (2.6) | 6.4 (1.6) | 9.7 (2.4) | 11.2 (2.1) | 12.5 (2.2) | 14.3 (2.5) | 3.6 |

### 4.2 What the numbers say
- **The inconsistency is between products, not within them.** Every product's rows are internally tight (σ ≈ 2–9w). The variance is a clean monotonic climb with authoring recency: the two newest products (Sentinel, Defender-for-Cloud) run ~3× the narrative length of Purview/Entra on `capability_detail` and `how_it_supports`. `control_intent` is already uniform across products (means 14–17w) — leave it.
- **`control_intent` is a paraphrase field** (control-text-shaped); its uniformity is correct and it should not be touched (paraphrase rule + meaning risk).
- **The `≤3w` fields are not defects.** 8 rows show 1-word `capability_detail`/evidence fields (`dpr-j47`, `dpr-j48`, `soc2-p1-p3`, `soc2-a1`, `soc2-pi1`, `53-mp-6`, `pci-4-2-1`, `gdpr-30`) — all **Not-Covered boundary rows** carrying deliberate `"n/a"` placeholders. This is a consistent, intentional convention; **exclude from any normalization.**

### 4.3 Recommended approach (for a separately-approved Tier-2 pass — nothing proposed now)
1. **Do not expand** the terse Purview/Entra rows. They are complete; padding them would add words without facts and risks the paraphrase/no-new-claim guardrails.
2. **Conservative top-end trim only.** Target the genuine outliers — `how_it_supports` at 60–87w (Defender-for-Cloud has several) and `capability_detail` at 60–69w — tightening connective wording toward each product's own p90, never below it. Set soft ceilings: `capability_detail` ≤ ~45w, `how_it_supports` ≤ ~55w.
3. **Leave `control_intent` and boundary `"n/a"` fields alone.**
4. **Cross-product harmonization is out of scope for editorial-only work.** Compressing Sentinel/MDC to Purview's density would delete real capability facts (guardrail violation). If you want it, it is a content decision, not a copy-edit — flag per row.
5. **Tier-2 "engagement" tokens (13 in row bodies)** are domain-correct and should stay: the 11 in `rows_dpr.py` mean the *supplier's contracted work for Microsoft* (SSPA sense — "engagement data" ≠ "organization data"; changing it alters meaning); `rows_soc2.py:465` "before analyst engagement" is ordinary English; `rows_80053.py:612` "in any 800-53/CMMC engagement" is the only borderline one (report-only).

---

## 5. Summary counts

### By task
| Task | Findings | Notes |
|---|---|---|
| A1 (Tier-1 length/depth) | CR-001…CR-012 (12) | 1 umbrella + 8 industry + product-notes + solution-scope + 800-53 note |
| A2 (Tier-2 narratives) | 0 findings; §4 report only | recommended approach, no rewrites (per instructions) |
| B (de-consulting) | CR-013…CR-026 (14) | 7 rendered fixes · 1 DECISION (SOC 2) · 3 README · 1 non-rendered comment · 2 likely-keep flags |
| **Total** | **26** | |

### By file
| File | Findings | IDs |
|---|---|---|
| `build/assemble.py` (INDUSTRIES, FOOTER, disclaimer) | 3 | CR-001(+002–009), CR-016, CR-017 |
| `build/common.py` (PRODUCTS, SOLUTIONS, comment) | 3 | CR-010, CR-011, CR-015, CR-025 |
| `build/template.html` (hero copy) | 2 | CR-013, CR-014 |
| `build/rows_80053.py` | 1 | CR-012 |
| `build/rows_171.py` | 1 | CR-018 |
| `build/rows_glba.py` | 1 | CR-019 |
| `build/rows_soc2.py` (DECISION) | 1 | CR-020 |
| `README.md` | 4 | CR-021, CR-022, CR-023, CR-024, CR-026 |

### Decisions needed from you
- **CR-020** — keep SOC 2 "engagement" (domain-correct) or force it to "examination"?
- **CR-006 / CR-010** — approve trimming that must stop before dropping a factual claim (I'll stop and flag rather than cut a fact).
- **CR-024 / CR-025 / CR-026** — include the low-visibility / non-rendered / build-sense items, or leave them?

---

**Phase 1 complete. Please review CONTENT-REVIEW.md and tell me which findings (all, or a subset by ID) to apply.** I will not edit any source file until you approve. On approval I will edit only `build/` sources (+ README), rebuild with `python build/assemble.py && python build/build_html.py`, run the regression gate (378 rows, per-product counts unchanged, no coverage/confidence/licensing/source/date/ref drift, JSON↔HTML reconcile), and append a dated section to `AUDIT-FINDINGS.md`.

---
---

# CONTENT-REVIEW — progressive-disclosure restructure (Phase 1, report only)

**Date:** 2026-07-19 · **Scope:** revise Task A. Task A normalized descriptions to a consistent *density* but at the wrong *depth* — the top-level industry/product/framework prose is now dense (98–151w) with control citations (§164.312(b), 3.11.2–3.11.3), SKU/meter strings, and scope caveats sitting at the top level. **This pass relocates that depth behind an expandable toggle without deleting anything.** · **Status:** PROPOSAL — no source files edited. `PD-###` finding IDs (Progressive Disclosure), distinct from the `CR-###` set above.

> **How to respond:** approve all, or a subset by ID (e.g. "apply PD-001, PD-010..PD-025, defer PD-040..PD-043"). Findings marked **DECISION** need a direction call. Nothing here is applied. Task B (de-consulting) is done and untouched by this pass.

## 0. Conclusion first

- **The fix is a summary/detail split, not a trim.** Every long description keeps its full text **verbatim**, moved into a collapsed `<details>` block. On top of it goes a **new 25–50-word plain-language summary** answering "why would I look here?" — no control-refs, no SKU/meter strings, no cross-reference caveats.
- **Cards get shorter for free.** The home industry grid, product-pivot grid, and solution grid render only the summary field, so the scannable surfaces become scannable. The detail toggle lives on the **entity page**, one interaction away (cards are already click-to-navigate; no nested toggles).
- **Mechanism:** the existing field (`note` / `notes` / `scope`) becomes the **summary**; a new sibling (`note_detail` / `notes_detail` / `scope_detail`) holds the **verbatim original**. Template gains one shared `discloseBlock()` helper + a `.disclose` `<details>` style that reuses existing CSS variables (dark mode automatic) and joins the existing print-expansion path.
- **Split rule (uniform, explainable):** split a field when its top-level text **carries citations, SKU/meter strings, or cross-reference caveats, OR exceeds ~55w**. That catches **all 10 industry notes, all 6 product notes, 4 of 11 framework notes, and 4 solution scopes** (34 fields). The 7 short framework notes and the short solution scopes are *already* single-idea summaries with nothing to hide — splitting them would create empty details, so they stay.
- **Boilerplate:** the "One configuration, many frameworks…" sentence is **already a single template string** (`template.html:462`), *not* copied into any product's `notes` — so there is no per-field duplication to remove. What remains is a **UX** repeat (it re-renders on all six product pages); the fix is to relocate it to the Products **index** once. Other cross-field repeats are the same *fact* in two genuinely different navigation contexts, not scaffolding — progressive disclosure already demotes them into the collapsed layer. Details in §4.
- **Guardrails:** editorial/structural only. No row-field changes (coverage, confidence, licensing, sources, status, dates, control_ref, product/solution assignments). Summaries **generalize**; none asserts anything the detail doesn't already state. §16 zero-em-dash-in-prose invariant respected in every draft below (checked: 0 em dashes introduced).

---

## 1. Proposed structure per content type + the UI mechanism

### 1.1 Data-model change (all edits in `build/` sources)

| Content type | Source location | Existing field → **summary** | New field → **detail (verbatim original)** | Render sites |
|---|---|---|---|---|
| Industry note | `assemble.py → INDUSTRIES[x]` | `note` | `note_detail` | home card `.desc` (summary) · industry page `.full` (summary + toggle) |
| Product note | `common.py → PRODUCTS[x]` | `notes` | `notes_detail` | product-pivot card `.desc` (summary) · product page (summary + toggle) |
| Framework note | `rows_*.py → FRAMEWORK` | `notes` | `notes_detail` | framework page `.callout` (summary + toggle) |
| Solution scope | `common.py → SOLUTIONS[x]` | `scope` | `scope_detail` | solution card `.desc` (summary) · solution page `.full` (summary + toggle) |

- **Existing field keeps its name and becomes the summary.** Card render code is then *unchanged* — cards already read `note`/`notes`/`scope`, and now that value is the short summary. Only the **page** render sites add the toggle.
- **`_detail` is optional.** Fields not split (short framework notes, short scopes, `applies_to`, `full_name`) get **no** `_detail` and render exactly as today. The template shows a toggle only when a `_detail` exists.
- **`applies_to` / `full_name` are untouched** (8–26w identity strings; they answer "who does this bind" on cards, not walls of text). Deliberate keep — PD-051.

### 1.2 UI mechanism — `.disclose` toggle (offline, zero-dep, print-aware, theme-aware)

Native `<details>`/`<summary>` (no JS to toggle; works from `file://`), collapsed by default, styled only with existing CSS variables so light/dark both work. It **joins the existing `details.row` print-expansion path** so it auto-opens when printing.

Shared render helper (new, in `template.html`):
```js
function discloseBlock(summary, detail, label){
  const s = summary ? `<div class="disc-sum">${esc(summary)}</div>` : "";
  if(!detail) return s;                          // short field: summary only, no toggle
  return `${s}<details class="disclose"><summary>${esc(label)} <span class="flip">›</span></summary>
    <div class="disc-body">${esc(detail)}</div></details>`;
}
```
Rendered shape on an entity page:
```
  Healthcare & life sciences
  For hospitals, clinics, and life-sciences firms, where the HIPAA Security      ← summary (.disc-sum), ~42w
  Rule is the anchor and card payments pull in PCI. The Microsoft stack …
  ▸ Full mapping notes                                                            ← <details class="disclose">, collapsed
      (expands to the verbatim 99-word original with every §-citation intact)
```
New CSS (variables reused ⇒ dark mode free):
```css
details.disclose{margin:10px 0 2px; border:1px solid var(--rule); border-radius:8px; background:var(--paper-2)}
details.disclose>summary{list-style:none; cursor:pointer; padding:8px 12px; font:600 12px var(--font-body);
  letter-spacing:.04em; color:var(--ink-2); display:flex; align-items:center; gap:6px}
details.disclose>summary::-webkit-details-marker{display:none}
details.disclose>summary:hover{color:var(--ink)}
details.disclose[open]>summary{border-bottom:1px solid var(--rule)}
details.disclose .disc-body{padding:12px 14px; font-size:13px; color:var(--ink-2); line-height:1.55}
.disc-sum{color:var(--ink-2); font-size:14px}
```
(The chevron reuses the existing global `details[open] .flip{transform:rotate(90deg)}` rule — same affordance as mapping rows.)

Print integration (two one-line extensions, mirroring today's row behavior):
- CSS `@media print`, line 199: `details.row::details-content` → `details.row::details-content, details.disclose::details-content`.
- JS `beforeprint`/`afterprint`, lines 629–630: `querySelectorAll("details.row")` → `querySelectorAll("details.row, details.disclose")`.

Page-level wiring (summary drafts feed these):
- `vIndustry` l.398: `<div class="full">${esc(i.note)}</div>` → `<div class="full">${discloseBlock(i.note, i.note_detail, "Full industry notes")}</div>`
- `vProduct` l.462/468: drop the boilerplate `.full` (see §4); render `discloseBlock(p.notes, p.notes_detail, "Full mapping notes")`
- `vFramework` l.435: `${f.notes?…callout…}` → callout containing `discloseBlock(f.notes, f.notes_detail, "Full framework notes")`
- `vSolution` l.492: `${esc(s.full_name)}. ${esc(s.scope)}` → `${esc(s.full_name)}. ` + `discloseBlock(s.scope, s.scope_detail, "Full scope")`

### 1.3 What "nothing deleted" means here (the Phase-2 gate)

`_detail` = the **exact pre-edit field text** (byte-identical snapshot taken before editing). So for every split field, `words(summary) + words(detail) = words(original) + words(summary) ≥ words(original)`, and "no sentence lost" is provable by equality against the snapshot. The summary is strictly **additive**. The only text that leaves a field entirely is consolidated boilerplate — and no field currently contains any (§4), so every `_detail` is a clean equality. If, while drafting a summary, I find a sentence that fits neither layer, I **flag it** (per your instruction) rather than drop it.

---

## 2. Three worked examples (judge the voice here)

Each shows the **new top-level summary** and confirms the **detail layer** = the current text verbatim. Summaries carry no §-citations, no SKU/meter strings, no cross-ref caveats, and no em dashes.

### 2.1 PD-010 · Healthcare & life sciences (industry note · 99w → 42w summary + 99w detail)
> **Summary (new, ~42w):** For hospitals, clinics, and life-sciences firms, where the HIPAA Security Rule is the anchor and card payments pull in PCI. The Microsoft stack splits the work across products: protecting clinical devices, defending against ransomware, capturing audit trails from EHR systems, and covering the cloud-hosted server estate.
>
> **Detail (verbatim, collapsed):** *"HIPAA Security Rule anchors; PCI for patient payments; state privacy composite on backlog. Intune carries the workstation/device safeguards (§164.310, device encryption for §164.312(a)(2)(iv)) common in clinical settings. Defender XDR carries the ransomware-facing controls: malicious-software protection (§164.308(a)(5)(ii)(B))… Sentinel extends the §164.312(b) audit mechanism… Defender for Cloud covers the cloud-hosted EHR server estate: file integrity monitoring for §164.312(c)… (cloud-resource scope; Compliance Manager assesses the M365 side)."* — all 99 words, every citation retained.

*Accounting: 42 + 99 = 141 ≥ 99. No sentence dropped (detail = original).*

### 2.2 PD-021 · Microsoft Sentinel (product note · 122w → 44w summary + 122w detail)
> **Summary (new, ~44w):** Microsoft's cloud-native SIEM and SOAR: it collects security logs from across the estate, correlates them into incidents, and retains them for the long-dated mandates other tools cannot satisfy. Priced by data volume rather than per user. It evidences and detects; it does not enforce.
>
> **Detail (verbatim, collapsed):** the full 122w note — the consumption/commitment-tier billing, the 90-day→2-year→12-year data-lake retention mechanism, the free-data-source and E5/E7 data-grant cost levers, the "Direct Support only where the namesake activity is log collection/retention/correlation/monitoring" discipline, and the Defender-for-Cloud posture seam.

*The honesty hook ("evidences and detects; it does not enforce") stays in the summary — it is a generalization the detail states verbatim, not a citation or meter. Accounting: 44 + 122 = 166 ≥ 122.*

### 2.3 PD-032 · NIST 800-53 R5 (framework note · 123w → 42w summary + 123w detail)
> **Summary (new, ~42w):** Why this framework is here as a curated subset, not a full catalog mapping: 800-53 has over a thousand controls, so the atlas maps only the data-protection core plus targeted identity, endpoint, detection, audit, and cloud-posture families. Government-cloud scope is noted on every row.
>
> **Detail (verbatim, collapsed):** the full 123w note — the 21-control Purview subset, the per-product control-family lists (Entra AC/IA; Intune AC-19/CM/MP/SC; Defender XDR SI-2/3/4/8, RA-5, IR-4; Sentinel AU/IR/RA-10; Defender for Cloud CA-2/CA-7, CM-6/CM-8, RA-5, SI-4/SI-7), the 800-171 cross-reference rule, the PT/PM exclusion, the Release 5.2.0 note, and FIPS 199 High.

*Accounting: 42 + 123 = 165 ≥ 123. This is the 123w outlier you flagged; every control-ref survives in the detail.*

---

## 3. Findings table (everything else to restructure)

Split rule reminder: **split** = write a ~25–50w summary, move the verbatim original into `_detail`; **keep** = already summary-length/citation-free, no change. "wc" = current field word count (measured from source, 2026-07-19).

### 3.1 Industry notes — `assemble.py → INDUSTRIES[x].note` (all 10 split)

| ID | Industry | wc | Proposed top-level summary (draft) |
|---|---|---|---|
| **PD-010** | Healthcare & life sciences | 99 | *(worked example §2.1)* |
| PD-011 | Defense industrial base | 118 | For defense contractors and their suppliers that handle controlled unclassified information, where NIST 800-171 and CMMC set the bar. The stack lines up product by product across endpoint hardening, threat detection, audit trails, and cloud enclaves, with government-cloud limits that recur throughout this sector. |
| PD-012 | Financial services | 98 | For banks, lenders, insurers, and fintechs under the GLBA Safeguards Rule, with PCI reaching card data and SOC 2 covering service commitments. The stack fits best on continuous vulnerability monitoring, institution-wide audit trails, and extending both to cloud-hosted banking workloads. |
| PD-013 | Higher education | 70 | For colleges and universities, which answer to FERPA for education records and, as Title IV institutions, to the GLBA Safeguards Rule as well, with PCI reaching campus payments. The stack mostly protects and locates student records and supplies the Safeguards Rule's continuous-monitoring path. |
| PD-014 | K-12 education | 53 | For school districts, where FERPA governs student education records and CSF 2.0 is the working security baseline. The Microsoft stack mainly protects and locates those records: labeling and DLP over student data, plus eDiscovery and audit for records requests and access logging. |
| PD-015 | Retail & e-commerce | 99 | For merchants and e-commerce operators, where PCI DSS governs card data and GDPR stands in for US state privacy. The stack covers the anti-malware and anti-phishing requirements, the central log-collection and retention engine PCI expects, and cloud-hosted parts of the cardholder environment. |
| PD-016 | SaaS & technology | 59 | For software and technology providers running on cloud infrastructure, typically examined under SOC 2 and ISO 27001, with HIPAA or PCI applying when they touch health or payment data. Because production lives in the cloud, Defender for Cloud is the anchor, including free multicloud coverage for AWS and GCP. |
| PD-017 | Manufacturing | 50 | For manufacturers, who juggle general security baselines (CSF 2.0, ISO 27001), the defense-supply-chain rules that apply to some of them (NIST 800-171 and CMMC), and GDPR for any EU operations. The stack's heaviest fit is on the defense-industrial-base control families. |
| PD-018 | US federal & FedRAMP-adjacent | 112 | For federal-civilian agencies and cloud providers pursuing FedRAMP, mapped against NIST 800-53 as a curated data-protection subset. Sentinel deepens the audit family and Defender for Cloud adds continuous monitoring, all within a government-cloud scope worth confirming when you plan. |
| PD-019 | Microsoft suppliers & partners | 63 | For vendors and partners enrolled in Microsoft's Supplier Security and Privacy Assurance program, whose contracts drive the Data Protection Requirements. This is the most Purview-centric lens: classification, DLP, retention, records, audit, and eDiscovery carry the data-handling obligations, while non-data controls stay deliberately unmapped. |

*Note: K-12 (PD-014) and Manufacturing (PD-017) are already ≤55w and near-citation-free. I recommend splitting them anyway for a uniform home grid (their `_detail` just holds the short original); if you'd rather leave sub-55w notes as-is, say so and I'll treat these two as keeps.* **DECISION (minor).**

### 3.2 Product notes — `common.py → PRODUCTS[x].notes` (all 6 split)

| ID | Product | wc | Proposed top-level summary (draft) |
|---|---|---|---|
| PD-020 | Microsoft Purview | 69 | Microsoft's data security, governance, and compliance suite for the Microsoft 365 estate: classification and labeling, data loss prevention, lifecycle and records, insider risk, eDiscovery, and audit. Licensed per user. It implements and evidences data-layer controls, and marks deliberate gaps honestly rather than overclaiming. |
| **PD-021** | Microsoft Sentinel | 122 | *(worked example §2.2)* |
| PD-022 | Microsoft Entra | 72 | Microsoft's identity and access platform (formerly Azure AD), covering conditional access, authentication, privileged access, and identity governance. Licensing is tiered and capability-specific, so the exact entitlement depends on the feature. Permissions Management was retired and is deliberately left off the map. |
| PD-023 | Microsoft Intune | 94 | Microsoft's cloud endpoint management for devices and apps: compliance, configuration, security baselines, app protection, and enrollment. Licensing is tiered with several separately gated add-ons, and a 2026 restructure is redistributing them across Microsoft 365 plans. Configuration Manager and Endpoint DLP sit outside its scope here. |
| PD-024 | Microsoft Defender XDR | 116 | Microsoft's unified detection and response across endpoints, email, identity, and SaaS apps, run from one portal. Each workload has its own plan gating, so the covered capabilities depend on what is licensed. Azure-resource posture and SIEM live in separate atlas products, a deliberate seam rather than a gap. |
| PD-025 | Microsoft Defender for Cloud | 151 | Microsoft's cloud-native protection for Azure, AWS, and GCP infrastructure rather than Microsoft 365: posture management plus workload threat detection. Priced per protected resource, with a free posture tier. It assesses and detects rather than remediates, so many hardening controls rate partial, and its compliance dashboard scores cloud resources, not the whole estate. |

### 3.3 Framework notes — `rows_*.py → FRAMEWORK["notes"]` (4 split; 7 kept)

| ID | Framework | wc | Split? | Proposed top-level summary (draft) |
|---|---|---|---|---|
| PD-030 | HIPAA Security Rule | 57 | split | How to read the HIPAA rows: they map the Security Rule as it stands today. A 2025 proposal would tighten several requirements but is not final, and Privacy Rule crossovers are held for a later version. |
| PD-031 | NIST 800-171 / CMMC L2 | 59 | split | Why these rows pin Revision 2: DoD's class deviation keeps CMMC on R2 even though a newer revision exists. FIPS-validated cryptography is left unmapped as a platform attribute, and CUI environments are usually government-cloud, noted on every row. |
| **PD-032** | NIST 800-53 R5 (subset) | 123 | split | *(worked example §2.3)* |
| PD-033 | FERPA | 71 | split | Why the FERPA rows are lighter than most: the law prescribes almost no specific technical safeguards, so the mapping leans toward labeling and access controls and rates mostly partial or evidence-only. The registrar's student-information system stays the system of record throughout. |
| PD-050 | 7 short framework notes | 25–48 | **keep** | `sspa-dpr` 29 · `iso-27001-2022` 28 · `soc-2` 25 · `nist-csf-2` 48 · `pci-dss-4` 37 · `glba-safeguards` 27 · `gdpr` 38 — each is already a single-idea caveat with no §-citation wall; no detail to hide. Rendered as-is. |

### 3.4 Solution scopes — `common.py → SOLUTIONS[x].scope` (4 split; rest kept) · **DECISION: lower priority**

Solution scopes are capability *lists*, not citation narratives, so this is the secondary application of the pattern. I propose splitting only the four Defender-for-Cloud scopes >60w (their `.desc` on the solution grid is a genuine wall); the summary is a capability gist and the verbatim list + "Boundary:" clause move to detail.

| ID | Solution (product) | wc | Proposed top-level summary (draft) |
|---|---|---|---|
| PD-040 | Regulatory Compliance Dashboard (defender-cloud) | 84 | Continuous assessment of your onboarded cloud resources against built-in and custom standards, with per-control pass/fail and downloadable reports. |
| PD-041 | Defender for Servers (defender-cloud) | 72 | Threat protection for Windows and Linux servers across Azure, AWS, GCP, and on-premises via Azure Arc, split into two plans with progressively deeper coverage. |
| PD-042 | Workload Protection Plans (defender-cloud) | 71 | Per-resource threat detection and hardening for storage, databases, containers, App Service, Key Vault, Resource Manager, APIs, and AI services. |
| PD-043 | Defender CSPM (defender-cloud) | 62 | The paid posture plan that adds attack-path analysis and risk prioritization, agentless scanning, data-aware posture, and cloud entitlement management on top of the free tier. |
| PD-052 | All other scopes (Purview/Entra/Intune/Defender XDR/Sentinel + Foundational CSPM) | 12–54 | **keep** | already 12–54w scannable lists; no split. |

### 3.5 Deliberate keeps

| ID | Item | Rationale |
|---|---|---|
| PD-050 | 7 short framework notes (§3.3) | Already single-idea summaries; splitting creates empty details. |
| PD-051 | `FRAMEWORK.applies_to` (8–26w) · `SOLUTIONS.full_name` | Identity strings ("who it binds" / official name), rendered on cards; not walls of text. Untouched. |
| PD-052 | Short solution scopes (§3.4) | Scannable capability lists already within target. |

---

## 4. Boilerplate-deduplication plan

**Finding PD-001 (the sentence you named):** `"One configuration, many frameworks: each solution below lists every control it supports across the atlas. A control implemented once shows up as posture everywhere it maps."`

- **Ground truth:** this string lives **only** at `template.html:462`, inside `vProduct()`. It is **not** copied into any product's `notes` field (verified by search across `build/`). So there is **no per-field duplication to remove** — it is already single-sourced in the template.
- **What's actually wrong:** it is a *reader-orientation* explainer (how the product pivot works, identical for every product), yet it **re-renders on all six product pages**. That is the "duplicated on every product page" you're seeing.
- **Plan:** extract it to a named constant and render it **once** on the Products **index** (`vProducts`, l.446–455) as the pivot's explainer subtitle; remove it from the individual product page, whose `.full` then leads with that product's **own summary** (§3.2) instead of generic scaffolding. Net: reader meets the explainer once at the pivot entry, and each product page opens with something product-specific.
- **Tradeoff / DECISION:** a deep link straight to `#/product/sentinel` bypasses the index and so wouldn't show the explainer (it would show Sentinel's summary, which is more useful anyway). If you'd rather guarantee the explainer on every product page, the alternative is to keep a **one-clause** version there. **Recommendation: index-only.**

**Other verbatim / near-verbatim repeats found (full corpus scan). None is scaffolding; each is the same domain *fact* in two genuinely different navigation contexts, which the split already demotes into the collapsed detail layer. Recommend keep-in-context, do not force-consolidate:**

| ID | Repeated text | Where | Recommendation |
|---|---|---|---|
| PD-060 | "State student-privacy laws remain on backlog." | `IND:higher-ed` + `IND:k12` | Lands in each note's **detail**. A 6-word contextual caveat; a shared component would read worse. **Keep.** |
| PD-061 | "remediation executes in the resource platform" | `SOL:Defender CSPM` + `SOL:Workload Protection Plans` | The mapping-discipline boundary clause; lands in each scope's **detail**. **Keep.** |
| PD-062 | assessment-scope caveat: "…not an attestation (Purview Compliance Manager assesses the M365 estate: a seam, not an overlap)" | `PROD:defender-cloud` note + `SOL:Regulatory Compliance Dashboard` scope | Substantive caveat relevant on both the product page and the dashboard solution page (different reader paths). Lands in **both details**. **Keep (cross-context).** |
| PD-063 | data-lake retention phrasing: "…mirrored into the Microsoft Sentinel data lake for total retention up to 12 years…" | `PROD:sentinel` note + `SOL:Log Retention & Data Lake` scope | Same mechanism, two contexts; both go to **detail** (product) / stay in the short scope. **Keep.** |
| PD-064 | GLBA DVM clause: "Defender Vulnerability Management supplies the §314.4(d)(2) continuous-monitoring…" | `IND:finserv` + `IND:higher-ed` notes | Same GLBA fact in two industry lenses; lands in each **detail**. **Keep.** |

*Rationale: consolidating a caveat into shared scaffolding pulls it away from the page it qualifies, hurting the reader who arrives via only one path. The progressive-disclosure move already removes these from the scannable top level, which is the actual goal.*

---

## 5. Phase 2 plan (on approval)

1. **Snapshot** current `note`/`notes`/`scope` values for the byte-equality gate.
2. Edit `build/assemble.py` (INDUSTRIES ×10), `build/common.py` (PRODUCTS ×6, SOLUTIONS ×4), `build/rows_{hipaa,171,80053,ferpa}.py` (FRAMEWORK ×4): rewrite each split field to its approved summary; add `<field>_detail` = the snapshot text verbatim.
3. Edit `build/template.html`: add `discloseBlock()` + `.disclose` CSS; wire the 4 page render sites; extend the two print lines; relocate PD-001 explainer to `vProducts`.
4. **Rebuild:** `python build/assemble.py && python build/build_html.py`.
5. **Regression gate:** 378 rows and per-product counts unchanged (Purview 150 · Entra 48 · Intune 41 · Defender XDR 53 · Sentinel 46 · Defender for Cloud 40); zero drift on the 13 protected row fields; JSON↔HTML reconcile; per-field word-count accounting (summary + detail ≥ original; `_detail` byte-equal to snapshot); `.disclose` renders + toggles in light **and** dark, works from `file://`, and expands in print; 0 prose em dashes (§16). Append a dated section to `AUDIT-FINDINGS.md`.

**Summary of what needs your call:**
- **PD-001** — relocate the pivot explainer to the index (recommended) vs keep a one-clause version on each product page.
- **PD-014 / PD-017** — split K-12 and Manufacturing for grid uniformity (recommended) vs leave the two sub-55w notes as-is.
- **PD-040..PD-043** — apply the split to the four long solution scopes now, or defer (they are the secondary, capability-list application).
- Any voice edits to the sample summaries in §2 and the drafts in §3.

**Phase 1 complete. Please review this section and tell me which findings (all, or a subset by ID) to apply, plus the three DECISIONs above.** No `build/` file will change until you approve.
