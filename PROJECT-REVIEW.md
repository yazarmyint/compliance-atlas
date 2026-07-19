# PROJECT-REVIEW — pre-publication review of the Compliance Atlas

**Reviewer:** Claude (Opus 4.8), acting as reviewing manager
**Review date:** 2026-07-19
**Subject:** `compliance-atlas.html` / `compliance-atlas.json` (378 rows · 11 frameworks · 6 products · 10 industries), the `build/` pipeline, and the project's four working documents
**Scope:** review only. No file in this repository was modified except this one.
**Method:** full read of README.md, AUDIT-FINDINGS.md (§1–§18), FRAMEWORK-SELECTION.md, CONTENT-REVIEW.md, `build/common.py`, `build/assemble.py`, `build/build_html.py`, `build/dependency_migration.py`, `build/template.html`, all eleven `rows_*.py` modules (via the assembled dataset and targeted source reads), plus the generated HTML and JSON. Independent verification: a live 156-URL resolution sweep, an 18-row seeded accuracy sample re-verified against authoritative sources, a live re-check of all 11 Compliance Manager template names, and eight structural-integrity queries against the dataset.

---

## 1. Executive summary

This is a serious piece of work and it is much closer to publishable than most projects that call themselves finished. The claim taxonomy is disciplined and — as far as I could test it — honestly applied; the control references I sampled are correct against authoritative text without exception; the Compliance Manager template names, the single highest hallucination-risk field in the dataset, match the live regulations list verbatim on all ten frameworks that have one; the build is genuinely regenerable and idempotent; and the audit trail in AUDIT-FINDINGS.md is the most convincing artifact in the repository, because it repeatedly records decisions *not* to claim things. The dataset is in good shape.

What is not in good shape is the **artifact around the dataset**. The atlas is currently a private research output wearing the clothes of a public reference. The gap between those two things is where nearly all my severe findings sit: the entire navigation layer is unusable without a mouse, the claim-strength taxonomy that is the atlas's core intellectual contribution is defined in the data and never shown to a reader, search silently misses 214 of the 216 rows that mention GCC High, there is no license, no changelog, no correction channel, no about page, and — the thing that worried me most — no version control at all under 380 hand-verified rows.

The five findings that matter most:

1. **PR-001 (Blocker) — the atlas cannot be navigated by keyboard or screen reader.** Every industry card, framework card, product card, solution card, and matrix cell is a click-only `<div>`/`<td>` with no `role`, no `tabindex`, and no key handler. This is the primary navigation of all four views. Publishing it in this state is a WCAG 2.1 A failure on the most basic criterion there is.
2. **PR-002 (Blocker) — there is no version control, no license, and no changelog.** `git rev-parse` returns "not a git repository". Roughly 1 MB of individually verified compliance claims exists in exactly one place, with the drift ledgers in AUDIT-FINDINGS.md doing version control's job by hand. A publishable reference also needs a license telling people what they may do with it.
3. **PR-010 (High) — the claim taxonomy is invisible to readers.** `META.coverage_levels`, `confidence_levels`, and `licensing_models` ship in the JSON and are referenced *nowhere* in `template.html` (verified: zero occurrences in the rendered HTML outside the data island). A reader sees a "Partial Support" badge and "●●○ Medium" with no definition anywhere on the site. The distinction between Direct/Partial/Evidence is the whole product.
4. **PR-012 (High) — global search does not index the government-cloud notes or the evidence fields.** Searching "GCC High" returns 2 rows; 216 rows contain the phrase. "Azure Government" returns 1; 89 contain it. For the DIB and federal user stories this is a retrieval failure at the exact point those readers need retrieval.
5. **PR-015 (High) — there is no way to filter or view by license tier.** Both stated user stories end in "…and at what license tier?" The tier is present on every row and reachable only by expanding rows one at a time. There is no E3-vs-E5 lens, no tier filter, no per-tier count.

None of these is a data problem. All five are between the dataset and the reader, which is a much better position to be in three weeks before publishing than the reverse.

---

## 2. What's working well

Held to the same evidence standard as the findings.

**W-1 — Control references are accurate.** I drew a seeded 18-row sample stratified across all six products and re-verified every control reference against authoritative text (methodology and per-row results in §4). 18/18 pass. Six were checked verbatim against the local eCFR extracts (`§164.316(b)(1)`, `§164.308(a)(8)`, `§164.308(a)(1)(ii)(D)`, `§164.312(b)`, `§314.4(c)(2)` ×2), four against the NIST source texts (`AC-7`, `CM-2`, `IR-4`, `PR.PS-04`, `DE.CM-09`), one against the AICPA TSC text (`CC8.1`). Not one reference was misnumbered, misattributed, or paraphrased into a different control.

**W-2 — Compliance Manager template names are exactly right.** I fetched `compliance-manager-regulations-list` live and compared all ten claimed template names character by character. All ten match: `HIPAA/HITECH`, `NIST 800-171`, `CMMC v2 Level 1`/`Level 2`, `NIST CSF 2.0`, `PCI DSS v4.0`, `Gramm-Leach-Bliley Act, Title V, Subtitle A, Financial Privacy`, `EU GDPR (General Data Protection Regulation)`, `NIST 800-53 rev.5`, `US - Family Educational Rights and Privacy Act (FERPA)`, `ISO/IEC 27001:2022`, `System and Organization Controls (SOC) 2`. The SSPA DPR row's `exists: false` is also correct — no such template is on the list. The `LIC["cm"]` claim that E5/A5/G5 customers get three premium templates free is confirmed verbatim on the same page. Given that the README names this as the top hallucination risk, getting 10/10 is the single most reassuring result in this review.

**W-3 — Source URLs resolve, and the two that don't are the two you already documented.** Independent sweep of all 156 distinct URLs across rows, framework metadata, solution registry, and product metadata: **154 → HTTP 200**, 2 → HTTP 403 from a server-side WAF (`dodcio.defense.gov/cmmc/`, `hhs.gov/hipaa/for-professionals/security/index.html`). Those are precisely the two blocks recorded in AUDIT-FINDINGS §7.2, unchanged, and every row citing them carries a machine-resolving alternate. Reproducing a year-old QA result exactly is a good sign about the QA.

**W-4 — Structural integrity holds under queries the build doesn't run.** I tested several invariants `assemble.py` does not assert: `also_involves` entries that are unknown or belong to another product (0 defects across all 378 rows), solution-key collisions in the flat 38-key registry (0 — all unique, confirming §15.7 item 8), solutions whose pivot page would render empty for lack of a primary row (0 — the §13.6 #2 refinement held across all six products), and JSON↔HTML embed reconciliation (378 = 378). The data is as clean as the audit claims.

**W-5 — Claim discipline is real, not decorative.** 8 boundary rows carry `Not Covered` with `None (boundary row)` — including two (`dpr-j47` transport encryption, `dpr-j48` full-disk encryption) that an atlas trying to look impressive would have rated Evidence and gotten away with. The coverage distribution (98 Direct / 229 Partial / 43 Evidence / 8 Not Covered) is Partial-dominant, which is the honest shape for this problem. AUDIT-FINDINGS §14.3's defence of Sentinel's 33% Direct rate — arguing composition rather than proportion, and listing every Direct row's namesake control — is the kind of reasoning that survives an auditor asking "why".

**W-6 — The build is genuinely regenerable.** The dependency migration is a pure transform applied at assemble time with a guard against re-processing structured rows (`dependency_migration.migrate_row` early-returns), so the double-migration risk flagged as highest-risk in §9.2 is structurally impossible rather than merely tested. `build_html.py` escapes `</` in the payload so the data island cannot break out of its `<script>`. `esc()` is applied consistently at every interpolation site I checked in `template.html`. The built app passes `node --check`.

**W-7 — The progressive-disclosure restructure (§18) was the right call and was executed carefully.** Summary-on-top with the verbatim original one click away, implemented as native `<details>` so it needs no JS, works from `file://`, and joins the existing print-expansion path. The byte-equality gate on all 24 `_detail` values is exactly the right verification for a "relocate, delete nothing" change. Rendering the pivot explainer once on the Products index instead of six times is a small change that meaningfully improves the product pages.

**W-8 — The seam discipline across products is the atlas's best original content.** The Defender↔Sentinel "detection versus correlation" seam, the MDCA browser-only boundary carried in three layers (§13.3), the Compliance Manager↔regulatory-compliance-dashboard "complementary assessment scopes" pairing, and the "MDE is the engine, Defender for Cloud is the licensing vehicle" split on malware rows are all distinctions a reader will not find stated this cleanly in Microsoft's own documentation. This is where the atlas earns its existence rather than restating docs.

---

## 3. Findings

Severity key: **Blocker-for-publish** · **High** · **Medium** · **Low**.

### Dimension A — UI/UX and rendering

> Honesty note: everything in this section is reasoned from `build/template.html` and the generated HTML, not from looking at pixels. I did not run a browser. Findings marked **[VISUAL]** need you to confirm them on screen before acting; the rest are determinable from code.

---

**PR-001 · Blocker-for-publish · Navigation is inaccessible to keyboard and screen-reader users**

*Evidence:* `build/template.html` — every navigation affordance is a click-only non-interactive element. `vHome` line 407 (`<div class="card" onclick="location.hash='#/industry/${id}'">`), `vIndustry` line 422, `vFrameworks` line 434, `vProducts` line 473, `vProduct` line 494 (solution cards), `matrixTable` line 541 (`<td … onclick="location.hash='${href}'">`), and the brand element at line 226. A grep for `tabindex`, `role=` across the whole template returns nothing; the only `aria-` attributes in the file are `aria-label` on the search input and `aria-live` on `<main>`. These elements are not focusable, are not announced as links or buttons, and cannot be activated by Enter or Space.

*Why it matters:* This is not a polish issue. The industry lens *is* user story 1's entry point and the framework list *is* user story 2's; a keyboard-only or screen-reader user cannot reach either. It fails WCAG 2.1 **2.1.1 Keyboard** (Level A) and **4.1.2 Name, Role, Value** (Level A). For an artifact aimed at compliance professionals — a readership that includes accessibility-regulated public-sector and higher-education organizations, two of your own industry lenses — shipping this is an avoidable embarrassment and a legitimate reason for an institution to decline to link to it.

*Recommendation:* Convert every navigating card and cell to a real link. The cleanest fix given the hash router: wrap the card's heading in `<a href="#/industry/${id}">` and make the card a presentational container, or make the card itself `<a class="card" href="…">` with `display:block`. Matrix cells become `<td><a href="…">count</a></td>`. Add `:focus-visible` outlines (you already have a focus style on the search input to copy). Add a skip-to-content link. This is a template-only change; no data touched, no rebuild of rows.

*Effort:* 3–5 hours including a keyboard walk of all four views and a screen-reader smoke test.

---

**PR-002 · High · The whole `<main>` is an `aria-live` region**

*Evidence:* `template.html:244` — `<main id="app" class="wrap" aria-live="polite">`. `render()` replaces `app.innerHTML` wholesale on every hash change.

*Why it matters:* Every route change queues the entire page — up to 57 mapping cards on the ISO framework view — for announcement to a screen reader. The intent (announce that navigation happened) is right; the mechanism makes the site unusable with assistive tech, which partly defeats the fix in PR-001.

*Recommendation:* Remove `aria-live` from `<main>`. Instead, after `render()`, move focus to the view's `<h1>` (give it `tabindex="-1"`), and optionally add a small visually-hidden `aria-live="polite"` status element that announces just the view name and row count.

*Effort:* 1 hour, best done in the same session as PR-001.

---

**PR-003 · Medium · `document.title` never changes across routes** **[partially VISUAL]**

*Evidence:* `template.html:655` — `document.title = META.brand.title;` executes once at startup. No view function touches it. All 40+ reachable routes therefore share the title "Compliance Atlas".

*Why it matters:* Practitioners bookmark and paste reference pages. Ten bookmarks to ten different frameworks are indistinguishable; browser history is useless; a link pasted into Teams or an email previews identically regardless of destination. This directly degrades the "I am subject to framework Z" story, whose natural end state is *sending someone the framework page*.

*Recommendation:* Set `document.title` at the end of `render()` from the active view — `"NIST CSF 2.0 · Compliance Atlas"`, `"Healthcare & life sciences · Compliance Atlas"`, and so on. Ten lines.

*Effort:* 1 hour.

---

**PR-004 · Medium · Individual mapping rows cannot be linked to**

*Evidence:* `rowCard()` emits `<details class="row" id="${r.id}">`, so every row has a DOM id — but the router owns the hash (`location.hash.replace(/^#\/?/, "")`), so `#hipaa-312-b-sentinel` is parsed as a route named `hipaa-312-b-sentinel` and falls through to `vMissing("page", …)`. There is no route that opens a single row, and no fragment-scroll behaviour; `render()` ends with `window.scrollTo(0,0)`.

*Why it matters:* The atomic unit of this product is the row. "Here is where Sentinel sits on §164.312(b), and here's the source" is the sentence a reader wants to send to a colleague. Today the best they can do is send a framework page and say "scroll to audit controls, it's the fifth card". A reference sheet whose references can't be cited is working against itself.

*Recommendation:* Add a `#/row/<id>` route that renders the single row expanded with breadcrumbs back to its framework and product, and add a small "link" affordance in each row's footer (the footer already prints the ID). Alternatively, support `#/framework/<id>?row=<rowid>` and auto-open plus scroll. The first is cleaner.

*Effort:* 2–3 hours.

---

**PR-005 · Medium · Site header will likely overflow on phones** **[VISUAL — please confirm]**

*Evidence:* `template.html:50` — `header.site .bar{display:flex; align-items:center; gap:18px; padding:12px 0}` with **no `flex-wrap`**, containing: brand (glyph + title + version string), a 4-item `nav.tabs`, a spacer, a search input, and two icon buttons. The `@media (max-width:840px)` block narrows the input to 160px and tightens tab padding but does not allow wrapping. At 360–390px viewport width the flex row's minimum content width appears to exceed the viewport substantially.

*Why it matters:* Horizontal overflow on the sticky header means the body scrolls sideways on every page, which is the single most noticeable "this site is broken on my phone" symptom. A meaningful share of the readership will meet this atlas via a phone link in a Teams message.

*Recommendation:* Add `flex-wrap:wrap` to `.bar`, and under 640px collapse the tab strip to a horizontally scrollable row (`overflow-x:auto; -webkit-overflow-scrolling:touch`) or a select. Also reduce `.hero h1` from 42px in the mobile block — it is currently unscaled. **Verify on a real device before and after**; I am reasoning from CSS, not measurements.

*Effort:* 2 hours including device checks.

---

**PR-006 · Low · No `color-scheme` declaration, so browser chrome ignores dark mode**

*Evidence:* The dark theme is implemented entirely through `[data-theme="dark"]` custom properties. There is no `<meta name="color-scheme">` and no `color-scheme:` CSS property on `:root`.

*Why it matters:* In dark mode, scrollbars, the search input's clear button, and any native form chrome render light against a dark page. Small, but visible on the one page every reader lands on.

*Recommendation:* Add `color-scheme: light` / `color-scheme: dark` to the `:root` and `[data-theme="dark"]` blocks respectively.

*Effort:* 15 minutes.

---

**PR-007 · Low · Single 968 KB HTML file, parsed and `JSON.parse`d on every load**

*Evidence:* Built output is 968 KB; the data island holds the full 1,037 KB JSON minified. `build_html.py` reports size at build time.

*Why it matters:* Genuinely fine for the offline `file://` use case, which is a real strength. Over a mobile connection it is a slow first paint with no loading state — `<main>` is empty until the script runs. Not worth re-architecting; worth knowing.

*Recommendation:* Leave the architecture alone (zero-dependency offline operation is worth more than the bytes). If hosting, ensure gzip/brotli is on — this content compresses extremely well. Optionally add a one-line "Loading…" placeholder inside `<main>` so a slow load doesn't show a blank page.

*Effort:* 30 minutes.

---

### Dimension B — Digestibility

---

**PR-010 · High · The claim-strength and confidence taxonomies are never shown to the reader**

*Evidence:* `assemble.py:115–125` defines `META["coverage_levels"]` (four one-sentence definitions) and `META["confidence_levels"]` (three), and `META["licensing_models"]` (four). All three ship in `compliance-atlas.json`. Grep of `build/template.html` for `coverage_levels|confidence_levels|licensing_models` returns **no matches**; the rendered HTML outside the data island contains zero occurrences of the string "The product directly implements" or "Mapping is well-established". The only in-UI hint is `confMeter()`'s `title="Confidence: High"`, which restates the value rather than defining it, and the `licensing_model` chip which has no tooltip at all.

*Why it matters:* This is the finding I would escalate hardest. The atlas's differentiating claim is that it is *honest about claim strength* — that is in the tagline, the README's first paragraph, and every audit section. A first-time visitor sees a green "Direct Support" pill next to a blue "Partial Support" pill on the same control (the six-product ISO A.8.16 stack) and has no way to learn what the difference means. Worse, they will guess — and the natural guess ("Direct = it covers this, Partial = it mostly covers this") is exactly the overclaim the taxonomy exists to prevent. The definitions are already written, already verified, already shipped. They are just not on screen.

*Recommendation:* Three placements, in priority order: (1) a legend block on the landing page under the stats bar, showing all four coverage levels with their definitions and the three confidence levels; (2) `title` attributes on `covBadge()`, `confMeter()`, and the licensing chip, sourced from `META` so they stay in sync; (3) a compact repeat of the coverage legend at the top of the framework view, where stacked cards make the comparison most acute. The `minibar()` already has a coverage tooltip — extend that idiom.

*Effort:* 2–3 hours.

---

**PR-011 · High · No glossary; substantial vocabulary is assumed and never defined**

*Evidence:* Terms that appear in rendered row bodies, solution scopes, and product notes with no in-artifact definition include: CSPM, CWPP, CNAPP, CIEM, MCSB, SIT, EDM, DKE, DCR, FIM, UEBA, SOAR, MDE/MDO/MDI/MDCA, GCC/GCC High/DoD, CUI, C3PAO, SPRS, ROPA, DSR, MAM/MAM-WE, EPM, ASR, EDR, AIR. Sample: the `defender-cloud` product summary opens "cloud-native protection for Azure, AWS, and GCP infrastructure … posture management plus workload threat detection"; the `notes_detail` behind it leads with "cloud-native application protection (CNAPP): CSPM plus CWPP".

*Why it matters:* User story 2 says "I am **subject to** (or tasked with implementing) framework Z". A large fraction of that readership is GRC, audit, legal, or privacy — people fluent in "§164.312(b)" and not in "MDCA". They are precisely the readers who most need a Microsoft-capability map, and they hit an acronym wall in the first paragraph of most product and solution pages. The Microsoft-fluent reader loses nothing from a glossary; the GRC reader is currently locked out of half the substance.

*Recommendation:* Add a `GLOSSARY` dict to `assemble.py` (term → one-sentence plain definition), ship it in `META`, and render it two ways: a dedicated `#/glossary` route linked from the footer, and — higher value — a first-use `<abbr title="…">` wrap for the ~25 highest-frequency acronyms in rendered prose, applied by a small post-processing pass in `esc()`-adjacent rendering rather than by editing row text. Do **not** edit row prose to expand acronyms; that would reopen the §16/§17 drift ledger for no benefit.

*Effort:* 4–6 hours (2h to write the definitions, 2–3h for the render path, 1h QA that the abbr pass doesn't corrupt escaped text).

---

**PR-012 · High · Global search does not index the government-cloud notes, evidence examples, coverage, confidence, or row id**

*Evidence:* `template.html:593–597` — the `hay` function concatenates `control_ref`, `control_intent`, solution, `also_involves`, `capability_detail`, `how_it_supports`, `external_dependencies`, `legacy_dependencies`, related-product notes, `license_requirement`, `licensing_model`, `product`, `prodFull`, framework name, `control_domain`. Absent: `cloud_availability_note`, `config_evidence_example`, `operational_evidence_example`, `coverage`, `confidence`, `status`, `id`, `framework_version`.

Measured impact on the current dataset:

| Query | Rows returned by search | Rows that actually contain the phrase |
|---|---|---|
| `gcc high` | **2** | **216** |
| `azure government` | **1** | **89** |
| `dod` | **2** | **179** |

265 of 378 rows carry a `cloud_availability_note`, and that entire field — the most sector-specific content in the atlas — is invisible to search.

*Why it matters:* Two of your ten industry lenses (Defense industrial base, US federal & FedRAMP-adjacent) are defined by government-cloud constraints, and the README's own add-a-product procedure treats the GCC High note as mandatory on every 800-171 and 800-53 row. A DIB reader's most likely first search is "GCC High". They get two results and reasonably conclude the atlas doesn't cover it. Searching a coverage level ("Direct Support") or a row id also fails, which blocks the natural "find me everything rated Direct" query.

*Recommendation:* Add the five missing text fields plus `coverage`, `confidence`, and `id` to the `hay` concatenation. One line. Then re-run the §15.7 item-8 search spot-checks ("CSPM", "CIEM", "attack path", "MCSB", "FIM") plus the three above, and consider showing which field matched.

*Effort:* 1 hour including verification. This is the highest value-per-hour item in the review.

---

**PR-013 · Medium · Coverage-tier asymmetry at stacked controls is visible in the badges but justified only inside the row body**

*Evidence:* CSF `PR.PS-04` ("Log records are generated and made available for continuous monitoring") stacks two cards: `csf-pr-ps-04` (Purview, **Partial Support** / High — "Directly generates and exposes the M365 log records…") and `csf-pr-ps-04-sentinel` (Sentinel, **Direct Support** / High — "Directly implements availability-for-monitoring at estate scope… Generation remains per-system"). On the same control, the product that *does* generate the records rates lower than the product that does not. The reasoning is sound and stated in each `how_it_supports`, and it is internally consistent with the deliberate `AU-2, AU-12` downgrade to Partial (`53-au-2-12-sentinel`: "Record generation itself remains a per-component capability"). But the badge is what scans, and the badge reads as an inversion.

*Why it matters:* A practitioner comparing stacked cards forms a fast judgement from the pills; if one stack looks internally inconsistent, they discount the taxonomy everywhere. This is exactly the risk AUDIT-FINDINGS §15.7 item 4 anticipated ("add a one-line rationale where a reader might infer inconsistency") — the checklist item was written and has not been executed.

*Recommendation:* Execute §15.7 item 4 as its own session. Sweep the multi-product stacks for tier spreads a reader could misread, and add a short rationale line rendered at the *control group* level (in `renderControlGroups`, above the stacked cards) rather than burying it in each card. `PR.PS-04` and the malware family (MDE Direct / Intune Partial / MDC Partial) are the two clearest candidates. I found no case where I thought a rating was *wrong* — only cases where the reason for the spread deserves to be on screen.

*Effort:* 4–6 hours for the sweep and the render change.

---

**PR-014 · Medium · A reader cannot tell how current a row is without expanding it**

*Evidence:* `last_verified` renders only in the row footer inside the expanded body (`rowCard()`, line 340). The landing hero shows `META.brand.as_of` = **2026-07-18**, which is already behind the last content pass (§18, 2026-07-19) and the JSON's `generated` timestamp (2026-07-19T17:16). `META.default_last_verified` is still **2026-07-16**, the v1 date, which §15.7 item 7 flags as needing a decision. Distribution across rows: 124 at 2026-07-16, 168 at 2026-07-17, 86 at 2026-07-18.

*Why it matters:* Footer line 4 makes currency the load-bearing caveat — "Currency is governed by each row's last-verified date". If that date is two clicks away, the caveat is decorative. And the oldest cohort is 124 Purview rows carrying the v1 date, which §15.7 item 5 specifically asks you to re-sample before publishing.

*Recommendation:* (a) Surface `last_verified` in the collapsed row summary as a small muted chip. (b) Show the dataset's verification date *range* on the landing page rather than a single `as_of`. (c) Bump `brand.as_of` and decide on `default_last_verified` as part of the publishing pass. (d) Execute §15.7 item 5 (re-verify a sample of the 2026-07-16 Purview licensing strings) — see PR-023, where I found evidence that cohort has begun to drift.

*Effort:* 2 hours for (a)–(c); (d) is its own session, ~4 hours.

---

**PR-015 · High · There is no license-tier lens anywhere in the artifact**

*Evidence:* Both stated user stories end "…and at what license tier?". `license_requirement` is on all 378 rows and rendered only inside the expanded row body. The framework view offers a coverage filter only (`fwFilter`, four buttons). There is no tier filter, no tier column, no tier count, and no way to answer "what does this framework look like if I only have E3?".

*Why it matters:* This is the question that actually changes what an organization does. "Does the Microsoft stack cover ISO A.8.12?" is interesting; "does it cover A.8.12 *on what we already own*" is the decision. The data supports the question fully — the strings are per-capability and verified from each product's authoritative source, which is a genuine achievement — and the UI cannot ask it. Note this is harder than a simple filter because Sentinel and Defender for Cloud are consumption-priced and don't have a tier; that is a design problem, not a reason to skip it.

*Recommendation:* Start with the cheap 80%: derive a coarse `license_band` at build time (`included` / `E3-tier` / `E5-tier` / `add-on` / `consumption` / `n/a`) by pattern-matching the `LIC`/`*_LIC` constants — there are only a few dozen distinct strings, so this can be a hand-maintained mapping keyed on the constant name rather than a fragile regex over prose. Render it as a chip in the row summary next to the coverage badge, and add a filter row on the framework view mirroring the existing coverage filter. Do not attempt a full tier matrix in v1.

*Effort:* 6–8 hours. Worth doing before publish if you can afford one large item; otherwise the first post-publish feature.

---

### Dimension C — Industry coverage

---

**PR-020 · Medium · Two high-value lenses are available for free from frameworks already shipped**

*Evidence:* `INDUSTRIES` (assemble.py:17–82) has ten entries, all keyed on frameworks already in the atlas. Two obvious readerships have no lens despite every framework they need already being mapped:

- **Legal & professional services** — law firms, accounting firms, consultancies. They answer to SOC 2 (client assurance), ISO 27001, GDPR, and HIPAA when handling client PHI. All four are shipped. This readership is unusually likely to pick up a compliance reference sheet.
- **Insurance** — carriers, brokers, MGAs. GLBA Safeguards (they are financial institutions), SOC 2, PCI (premium payments), NIST CSF. All four shipped. Currently they would land on "Financial services", whose note is written about banks and lenders.

*Why it matters:* User story 1 begins "I operate in industry Y". Industry is the front door — it is literally the first view. A reader who scans ten cards and finds nothing describing their world concludes the atlas isn't for them, even though 100% of their content is present one click away under a different label. The cost is zero new rows.

*Recommendation:* Add both lenses. Each needs a `name`, a `frameworks` list drawn from existing ids, a 39–49-word `note`, and a `note_detail` — the shape is fully established by the ten existing entries and the §18 summary/detail split.

*Effort:* 2 hours for both, including verifying the framework lists are defensible.

---

**PR-021 · Medium · The industries the atlas cannot serve are gated on frameworks, and that should be said out loud**

*Evidence:* The realistically-missing sectors are **state & local government** (needs CJIS), **energy & utilities** (needs NERC CIP), and **pharma/medical devices** (needs 21 CFR Part 11). None can be added without a framework, so they are framework findings (PR-025) rather than industry findings. Meanwhile there is no statement anywhere in the artifact about which industries are *deliberately* out of scope.

*Why it matters:* A reader from a sector with no lens cannot distinguish "not covered yet" from "considered and rejected". The atlas is scrupulous about this distinction inside rows (boundary rows exist precisely to say "we looked and the answer is no") and silent about it at the industry level.

*Recommendation:* Add a short "What's not here" section to the Industries index — three or four lines naming the sectors that would need frameworks the atlas doesn't map, with the reason. This is cheap honesty that matches the artifact's existing voice.

*Effort:* 1 hour (best folded into the about page, PR-032).

---

### Dimension D — Framework and regulation coverage

I read FRAMEWORK-SELECTION.md before forming views. Below I concur or argue against by name.

---

**PR-025 · Medium · CJIS Security Policy is missing from the candidate list entirely — a genuine omission rather than a rejection**

*Evidence:* FRAMEWORK-SELECTION.md's selection criteria name six target industries (healthcare, education, DIB, finance, retail, SaaS). The rejected/backlog table lists the state-privacy composite, SEC 17a-4/FINRA, NYDFS 23 NYCRR 500, NIS2, DORA, and ISO 27701. **CJIS appears nowhere** — not selected, not rejected, not backlogged. Yet a Compliance Manager premium template exists (`Criminal Justice Information Services (CJIS) Security Policy`, confirmed on the live regulations list I fetched), and the policy's control areas map densely onto exactly the six products in the atlas: audit and accountability (Purview Audit, Sentinel), identification and authentication with its advanced-authentication mandate (Entra), mobile device management (Intune), malicious code protection (Defender XDR), and cloud-resource posture (Defender for Cloud).

*Why it matters:* CJIS unlocks an entire industry lens (state & local government, plus every vendor selling to law enforcement) that the atlas currently cannot serve at all. Because it was never evaluated, there is no documented rationale for its absence — which is out of character for a project that documents why it *didn't* map Section K of the DPR line by line. Its maintenance cost is moderate (the policy revises roughly annually), which is a fair argument against, but that argument has not been made.

*Recommendation:* Evaluate CJIS explicitly and record the outcome in FRAMEWORK-SELECTION.md either way. If it goes ahead, my estimate is 20–28 rows spanning all six products — a full framework increment, not an addendum.

*Effort:* 2 hours to evaluate and document the decision. 20–30 hours if you decide to map it.

---

**PR-026 · Medium · I argue against the backlog ordering: SEC 17a-4 / FINRA should outrank the state-privacy composite**

*Evidence and argument:* FRAMEWORK-SELECTION.md's backlog table designates "US state privacy composite (CPRA-anchored)" as the **v2** item, while 17a-4/FINRA sits in a lower row described as an unsolicited observation — despite that same row conceding it is "the strongest untapped Purview story in finance (Records Management immutability + Communication Compliance supervision are purpose-built for it)". I think the ordering is backwards, on the document's own stated criteria:

1. *Maintenance cost*, criterion 3. The memo's own rejection rationale for the state composite is that "~20 divergent, still-churning state laws = highest maintenance cost of any candidate". 17a-4 is the opposite: a stable rule whose last substantive amendment (the 2022 electronic-recordkeeping modernization) is settled, plus FINRA supervision rules that change slowly. Promoting the cheapest-to-maintain candidate over the most expensive one follows the memo's own logic.
2. *Density of genuine relevance*, criterion 2. The memo already concedes 17a-4's density. The state composite's own rationale concedes the reverse: "Purview stories are near-duplicates of the GDPR rows". Near-duplicate rows are precisely what the ~12–25-rows-per-framework curation discipline exists to prevent.
3. **Portfolio balance, which the memo does not weigh.** Records Management and Communication Compliance are the two thinnest Purview solutions in the shipped atlas by primary-row count — Communication Compliance in particular carries essentially one narrow primary mapping (SOC 2 CC1.1, itself rated Evidence/Low with a note that auditors vary on accepting it). 17a-4/FINRA is the one framework that would make both of them Direct on their namesake activity. It doesn't just add rows; it corrects a coverage imbalance in the existing product map.

*Recommendation:* Re-rank the backlog in FRAMEWORK-SELECTION.md with the rationale above recorded, so the decision is legible rather than reversed silently. Keep the state composite backlogged on its existing (sound) grounds.

*Effort:* 1 hour to re-document. 18–24 hours if you subsequently map 17a-4/FINRA.

---

**PR-027 · Low · I concur with the state-privacy, NIS2/DORA, and ISO 27701 deferrals — but the NIS2/DORA rationale is missing**

*Evidence:* The backlog table gives a substantive rationale for the state composite (churn, duplication) and for 17a-4 (strong story, deferred). NIS2, DORA, NYDFS, and ISO 27701 are listed in a single parenthetical with no reason attached beyond "flagged".

*My position:* I concur with all three deferrals. State privacy: the churn argument is correct and the GDPR-as-analog annotation is a legitimate interim answer. ISO 27701: it is a privacy extension whose tooled layer is Priva, which the atlas has permanently and correctly declined to map (§15 roadmap closure) — mapping 27701 would produce a framework whose best answer is a product the atlas won't cover. DORA/NIS2: both are weighted toward operational resilience, ICT third-party risk, and governance obligations rather than data-layer or endpoint controls, so honest mapping would yield a thin, Evidence-heavy row set — a real reason, and one that isn't written down.

*Recommendation:* Record the actual rationale for each so a future session doesn't relitigate. Two sentences apiece.

*Effort:* 30 minutes.

---

**PR-028 · Low · FRAMEWORK-SELECTION.md's own state text is stale**

*Evidence:* The header still reads "**Status:** proposed, awaiting approval" and "**Hard cap:** 6 new frameworks in v1"; the "Projected dataset size" line says "≈ **140 rows** across 9 frameworks"; the "Resulting v1 industry coverage" table lists **8** industries and marks higher education as "*(FERPA: backlog note)*". Shipped state is 378 rows, 11 frameworks, 10 industries, FERPA fully mapped (its own Increment 1 section, added later in the same file, says so).

*Why it matters:* This is one of only two scoping documents, and the review prompt correctly treats it as the record of what was decided. A reader — including future you — hitting "awaiting approval" and "~140 rows" has to work out which parts are current. §15.7 item 7 flags cross-document count reconciliation and it hasn't run.

*Recommendation:* Add a short "Current state (2026-07-19)" block at the top, correct the projection line and industry table, and change the status. Keep the original v1 projections visible as history — the doc's value is partly that it shows what was predicted versus what shipped.

*Effort:* 1 hour, folded into §15.7 item 7.

---

### Dimension E — Product coverage

---

**PR-030 · Low · I concur that the roadmap should stay closed at six**

*Evidence and argument:* README closes the roadmap 2026-07-18 and AUDIT-FINDINGS §15.1 records the Azure-platform boundary decision (Key Vault, Firewall/WAF, Azure Policy, RBAC, Update Manager, Backup are external dependencies, never mapped capabilities). I tested the obvious challenge — that a seventh "Azure platform security" product would serve readers — and I do not think it survives. The boundary is stated crisply, it is applied consistently (I found the "remediation executes via Azure Policy/IaC, outside this product" pattern used as designed), and the marginal reader value is low because Azure Policy's compliance story is *already* represented through Defender for Cloud's regulatory compliance dashboard rows. Against that, the marginal maintenance cost is high: six products already generate a maintenance-trigger list of fourteen items (README), and Azure platform services churn faster than any of the six.

The stronger challenge is portfolio balance, not scope: within the *existing* six, Communication Compliance and Records Management are underrepresented. That is a framework problem, addressed in PR-026, not a product problem.

*Recommendation:* Keep the roadmap closed. Say so on the about page, since "why isn't Azure Firewall here?" is a question readers will ask and the answer is a decision, not an oversight.

*Effort:* Nil beyond PR-032.

---

**PR-031 · Medium · Priva is referenced 11 times as the answer and is unreachable, with no explanation on screen**

*Evidence:* `RELATED_PRODUCTS = {"priva": "Microsoft Priva"}` — 11 contributing links across 10 privacy-domain rows (`dpr-f14-22`, `iso-a-5-34` ×2, `soc2-p1-p3`, `soc2-p4-1`, `soc2-p5`, `gdpr-15/17/20/25/30`). `relatedBlock()` renders these as "▸ **Microsoft Priva** · contributing · <note>" with no link, because there is no product page. AUDIT-FINDINGS §15 records the decision to keep Priva as a permanent reference-only product and explains it well — in the audit document, not in the artifact.

*Why it matters:* These 11 links sit on exactly the rows where a GDPR or SOC 2 privacy reader arrives. They are told, repeatedly, that the tooled answer is a Microsoft product, and given nothing further — no page, no link, no note explaining that this is deliberate. Coming from an artifact this careful about boundaries, the silence reads as an unfinished edge rather than a decision. This is the one place where "closed at six" leaves a visible user-story hole.

*Recommendation:* Do not reopen the roadmap. Instead: (a) render `RELATED_PRODUCTS` entries with a short "reference-only — not mapped in this atlas" qualifier and a link to Microsoft's Priva overview; (b) add a two-sentence "Reference-only products" note to the Products index explaining the boundary. The structured `related_microsoft` model already carries everything needed.

*Effort:* 2 hours.

---

### Dimension F — Accuracy

The methodology and full per-row results are in §4. The findings that emerged from it:

---

**PR-035 · Medium · Defender license strings list a renamed SKU alongside its old name, as if they were two products**

*Evidence:* `DEFENDER_LIC["mde_p2"]` (common.py:691) reads "…included in Microsoft 365 E5/A5/G5, **Microsoft 365 E5 Security**, Windows 10/11 Enterprise E5/A5, **or Microsoft Defender Suite**." The live Microsoft Entra licensing article now states plainly: "**Microsoft Defender Suite (formerly Microsoft 365 E5 Security)**". The live Defender service description's P2 plan list no longer mentions E5 Security at all — it reads: standalone, Windows 11/10 Enterprise E5/A5, Microsoft 365 E5/A5/G5, **Microsoft Defender Suite/EDU/GOV/FLW**, Microsoft Defender + Purview Suite FLW. The same old-name/new-name pairing appears in `mdo_p2`, `mdi`, `mdca`, `mdvm`, and `xdr`. Because these are shared constants, the drift reaches all 53 Defender XDR rows.

*Why it matters:* The tier is still correct — nobody will buy the wrong thing — so this is a credibility rather than a correctness defect. But a reader who knows the SKU landscape sees the atlas listing a product and its own former name as alternatives, which undercuts the "verified against the authoritative licensing source" claim that is the atlas's warrant. The `EDU/GOV/FLW` variants are also now absent, and the GOV variant matters for the DIB and federal lenses.

*Recommendation:* Re-derive the six `DEFENDER_LIC` strings from the current Defender service description in one pass. Prefer "Microsoft Defender Suite (formerly Microsoft 365 E5 Security)" so readers holding the old paperwork still recognise it. Since these are shared constants, this is a small edit with wide reach — and it touches `license_requirement`, a protected field, so it needs a declared drift ledger in the §16/§17 style.

*Effort:* 3–4 hours including the drift ledger and rebuild.

---

**PR-036 · Medium · The Sentinel 50 GB commitment-tier note is out of date; its own maintenance trigger has fired**

*Evidence:* `SENTINEL_LIC["ingest"]` and the README maintenance trigger both describe the 50 GB tier as "public preview (Oct 2025, promo through Mar 2026)" and ask you to "confirm GA status at next pass". Live: the promotion was extended to June 30, 2026 (Microsoft partner announcement, March 12, 2026) and **extended again through December 31, 2026** (announcement June 26, 2026), with purchase pricing locked to March 31, 2027. It remains public preview. Today is 2026-07-19, so the atlas's stated promo end date is nearly four months in the past.

*Why it matters:* Sentinel is consumption-priced, and the atlas's own stated consulting insight is that retention mandates are consumption costs. A reader sizing a 50 GB/day workload against an expired promotion window gets a materially wrong cost picture. This is the clearest case in the dataset of a maintenance trigger being correctly diarised and not executed — which is a process finding as much as a content one (see PR-046).

*Recommendation:* Update the string to "public preview; promotional pricing extended through December 31, 2026, with purchased pricing locked to March 31, 2027" and reset the trigger. While in the billing article, also capture the two meters the atlas doesn't yet mention: **advanced data insights** (per compute hour, notebook sessions and jobs) and the **Sentinel graph** meters.

*Effort:* 2 hours.

---

**PR-037 · Low · Two license strings omit currently-qualifying SKUs**

*Evidence:* (a) `ENTRA_LIC["ca"]` says Conditional Access is "Microsoft Entra ID P1 (included in Microsoft 365 E3/E5 and Business Premium)". The live Entra licensing article lists P1 as included with Microsoft 365 **E3, E5, E7**, **F1, F3**, EMS E3, and Business Premium. E7 is missing, and the atlas already recognises E7 elsewhere (Intune and Sentinel strings both name it). (b) `LIC["audit_prem"]` names "Microsoft 365 E5/A5/G5, Microsoft Purview Suite, or E5 eDiscovery & Audit add-on"; the live Purview service description table also lists **Office 365 E5/A5/G5** as qualifying — a real SKU an Office-only customer might hold.

*Why it matters:* Under-listing entitlements causes a specific failure: a reader concludes they need to buy something they already own. Low severity because it errs conservative, but it is directly contrary to the atlas's purpose.

*Recommendation:* Fold into the PR-035 licensing re-verification pass rather than doing separately.

*Effort:* Included in PR-035.

---

**PR-038 · Low · Seven cited URLs now redirect to renamed or consolidated pages**

*Evidence:* All 156 URLs resolve, but seven do so via a genuine content move (excluding trivial `/en-us/` locale insertion, which accounts for the other 130):

| Cited | Now resolves to |
|---|---|
| `entra/fundamentals/whatis` | `entra/fundamentals/what-is-entra` |
| `entra/identity/authentication/concept-authentication-methods` | `entra/identity/authentication/overview-authentication` |
| `defender-endpoint/overview-attack-surface-reduction` | `defender-endpoint/attack-surface-reduction-overview` |
| `azure/sentinel/detect-threats-built-in` | `azure/sentinel/threat-detection` |
| `azure/sentinel/automate-responses-with-playbooks` | `azure/sentinel/automation/automate-responses-with-playbooks` |
| `azure/defender-for-cloud/defender-for-storage-malware-scan` | `azure/defender-for-cloud/introduction-malware-scanning` |
| `intune/fundamentals/manage-devices` | `intune/fundamentals/core-concepts#devices` |

The last is the notable one: the cited page was consolidated into a different article and now lands on an anchor within it. It is cited by `glba-314-4-c2-intune` as that row's sole Microsoft source, so the reader lands mid-page on a general concepts article rather than on device-management documentation.

*Why it matters:* Microsoft's redirects are reliable, so nothing is broken today. But redirects get retired, and the `manage-devices` case already degrades the citation's usefulness. The first one is also the `naming_source` for the entire Entra product.

*Recommendation:* Update all seven to their current targets and re-verify `glba-314-4-c2-intune`'s source choice specifically. Add a redirect-detection step (compare final URL to requested URL, ignoring `/en-us/`) to the standing URL check — my sweep script does this in about ten lines and it turns a 156-URL pass/fail into a drift detector.

*Effort:* 2 hours including adding the check to the QA routine.

---

**PR-039 · Low · The README's per-row source rule is violated by construction, and the build doesn't enforce either half**

*Evidence:* README ("Add a framework", rule 2) states: "Every row: ≥1 official framework source + ≥1 Microsoft Learn URL." Six rows carry no Microsoft source at all: `dpr-j48`, `soc2-p1-p3`, `soc2-a1`, `soc2-pi1`, `53-mp-6`, `gdpr-30`. All six are boundary rows — for a `Not Covered` verdict there is no Microsoft capability to cite, so their behaviour is *correct* and the rule as written is wrong. Separately, `assemble.py`'s integrity block asserts only `r["sources"]` is non-empty; it does not check for an official source, a Microsoft source, or a minimum count.

*Why it matters:* Documentation accuracy, plus a latent gap: nothing would catch a future non-boundary row shipping with a single source.

*Recommendation:* Amend the README rule to state the boundary-row exception explicitly, and add the corresponding assertion to `assemble.py` (`if coverage != "Not Covered": require ≥1 official and ≥1 Microsoft source`). Fold in the `also_involves` validity check from PR-045 at the same time.

*Effort:* 1.5 hours.

---

### Dimension G — Publishing readiness

---

**PR-040 · Blocker-for-publish · No version control**

*Evidence:* `git rev-parse --is-inside-work-tree` → "fatal: not a git repository (or any of the parent directories): .git". The repository root contains no `.git`, and the only backups are the two hand-made snapshots in `reference/` (`baseline-pre-refactor.json` at 150 rows, `baseline-pre-humanization.json` at 378).

*Why it matters:* This is the finding I would raise first in a real management conversation, ahead of the accessibility one, because it is the only one where a bad day destroys the work rather than degrading it. 378 individually source-verified rows, roughly 500 KB of Python, and a 1,085-line audit trail exist in a single directory on one Windows machine. There is no history, no diff, no revert, no branch for a risky pass, and no off-machine copy. The drift ledgers in §16/§17/§18 — genuinely impressive engineering — are a manual reimplementation of `git diff`, and they only prove what was checked. Once published, you also cannot show anyone what changed between dataset versions.

*Recommendation:* `git init` today, before any other work in this review. Commit the current state as the pre-publish baseline, push to a private remote. Add a `.gitignore` for `build/__pycache__`. Consider whether `reference/*.pdf` (the framework source documents) belong in the repository or in a sibling directory — several are copyrighted standards texts, so keeping them out of a public remote matters (see PR-042).

*Effort:* 1–2 hours, including the copyright triage of `reference/`.

---

**PR-041 · Blocker-for-publish · The artifact has no license**

*Evidence:* No `LICENSE`, `COPYING`, or licensing statement in the repository or in the rendered footer. `FOOTER_LINES` covers disclaimers and trademark attribution but says nothing about what a reader may do with the atlas itself.

*Why it matters:* Without a license, the default is all-rights-reserved: nobody may republish, excerpt, or adapt it. That is probably not what you want from something described as an "independent community project", and it blocks exactly the uses that would make it useful — a consultant putting a framework page in a client deck, a university linking it in a course. It also leaves you exposed on the inverse question of what you are warranting.

*Recommendation:* Two decisions. (1) **Content**: CC BY 4.0 fits the stated intent (attribution required, adaptation allowed) and is the norm for reference datasets. (2) **Code** (`build/`): MIT or Apache-2.0. Add `LICENSE`, state both in the README, and add a fifth footer line. Note the interaction with the paraphrase discipline: the atlas deliberately never quotes ISO/AICPA/PCI/NIST text, which is what makes permissive licensing of your own prose safe — that reasoning is worth stating on the about page.

*Effort:* 2 hours including the decision.

---

**PR-042 · High · `reference/` contains copyrighted standards texts that must not reach a public remote**

*Evidence:* `reference/` holds `AICPA-TSC-2017-2022POF.pdf` (and its `.txt` extraction), `pci-dss-401.pdf`, `DPR-v12.pdf`, and the NIST PDFs. The AICPA and PCI SSC documents are licensed for the downloader's use, not redistribution. The NIST documents and eCFR extracts are US-government public domain and fine. The DPR is a Microsoft supplier document.

*Why it matters:* Interacts directly with PR-040 — the natural next step after `git init` is a remote, and if that remote ever becomes public the AICPA and PCI files are a redistribution problem entirely separate from anything in the atlas itself. The project has been careful about copyright in the *content* (paraphrase-only, documented repeatedly); this is the same risk arriving through the back door.

*Recommendation:* Before the first push: move the copyrighted source documents out of the repository tree into a sibling `reference-private/`, or `.gitignore` them explicitly and note in the README where they came from and how to re-download. Keep the NIST/eCFR texts — they are public domain and their presence makes the verification story reproducible.

*Effort:* 1 hour.

---

**PR-043 · Blocker-for-publish · The public name is unresolved and the header advertises it**

*Evidence:* `BRAND = {"title": "Compliance Atlas", "working_title": True, …}`; `template.html:657` renders `"v" + atlas_version + (working_title ? " · working title" : "")`, so every page's header currently reads "**Compliance Atlas** v2.0.0 · working title". README line 3 confirms the public name is TBD.

*Why it matters:* You cannot publish something that tells every visitor its own name is provisional; it reads as a draft leaked early and undermines the authority the content has earned. The parameterization is good engineering — one constant — but the decision itself is a blocker.

*Recommendation:* Decide the name, set `working_title: False`. Two notes on the decision: (1) "Compliance Atlas" is generic enough to collide with existing commercial products — search before committing; (2) whatever you choose, avoid anything implying Microsoft endorsement, since footer line 2 disclaims exactly that.

*Effort:* 2 hours (mostly the naming decision and a trademark search).

---

**PR-044 · High · There is no about/methodology page and no correction channel**

*Evidence:* Four views exist: Industries, Frameworks, Product Pivot, Density Matrix. There is no About, no Methodology, no Contact. The footer carries four legal lines and a generation timestamp. The methodology genuinely exists — the coverage taxonomy, the "never claims a product satisfies a requirement" rule, the paraphrase-only discipline, the ≥1-official-plus-≥1-Microsoft source rule, the curation cap, the boundary-row convention, the seam discipline — and it is documented entirely in AUDIT-FINDINGS.md and README.md, neither of which a reader receives.

*Why it matters:* For a reference sheet making claims about regulated subject matter, methodology *is* the credibility. A reader deciding whether to trust "Direct Support / High" on §164.312(b) needs to know how that verdict was reached and who reached it. Right now the answer is a disclaimer and an anonymous footer. Equally: when a reader finds an error — and with 378 rows across six churning products, they will — there is no way to tell you. The atlas's whole currency model rests on errors being findable and fixable, and there is no inbound path.

*Recommendation:* One `#/about` route covering: what this is and is not (attestation, legal advice); how a row is made and verified; what the four coverage levels and three confidence levels mean (shares content with PR-010); the paraphrase and sourcing rules; the product-scope boundary and why the roadmap is closed at six (PR-030); reference-only products (PR-031); what's deliberately absent at industry and framework level (PR-021); who maintains it; the license (PR-041); and a correction channel. For the channel, a GitHub issues link is best if the repository goes public; otherwise a dedicated address. Link it from the footer and the header nav.

*Effort:* 6–8 hours. Most of the text can be adapted from README and AUDIT-FINDINGS rather than written fresh — but it needs a rewrite for a reader who has never seen the build.

---

**PR-045 · High · No dataset versioning or changelog visible to readers**

*Evidence:* `BRAND["atlas_version"] = "2.0.0"` renders in the header. There is no changelog anywhere — not in the repository, not in the artifact. The version's meaning is undocumented (2.0.0 marks the platform generalization; nothing records that). `META.generated` is a build timestamp, which changes on every rebuild whether or not content changed.

*Why it matters:* A returning reader has no way to answer "what's changed since I last looked?" — which is *the* question for a reference that exists because the underlying products churn. It also means you cannot cite a version: "as of Atlas v2.1" is unverifiable if v2.1 isn't described anywhere. Third, without a changelog you have no mechanism to tell readers you fixed something they reported, which kills the correction loop PR-044 opens.

*Recommendation:* Add `CHANGELOG.md` with a versioning policy (suggest: major = data-model or product-scope change; minor = framework or product addition; patch = row corrections and re-verifications), backfilled from the AUDIT-FINDINGS section headers, which already contain the material. Render the current version's entry, or a link to it, on the about page. Separate "content version" from "build timestamp" in the footer so a rebuild with no content change doesn't look like an update.

*Effort:* 4 hours including backfilling from AUDIT-FINDINGS.

---

**PR-046 · Medium · No page metadata: description, favicon, social preview**

*Evidence:* Verified against the built HTML: no `<meta name="description">`, no `rel="icon"`, no `og:*` or `twitter:*` tags. `<html lang="en">` and the viewport meta are present and correct.

*Why it matters:* A link shared into Teams, Slack, or LinkedIn — the realistic distribution path for this artifact — renders as a bare URL with no title card. Search engines get no summary. Combined with PR-003 (static title), every shared link looks identical and uninformative.

*Recommendation:* Add a description meta, an inline SVG data-URI favicon (keeps the zero-external-dependency property), and Open Graph tags. Note that `og:image` requires a hosted absolute URL, so either skip it or accept one external asset for the hosted copy while the `file://` copy stays self-contained.

*Effort:* 2 hours.

---

### Dimension H — Process, data model, and maintenance (added)

---

**PR-050 · Medium · The maintenance-trigger list is growing, undated, and unowned**

*Evidence:* README's "Maintenance triggers worth diarising" now has **14 bullets** spanning fixed dates (CMMC Phase 2 Nov 10 2026; Sentinel Azure-portal retirement Mar 31 2027; HIPAA final rule ~Jul 2027), rolling reviews ("annual ~Q1"), and open-ended watches ("Defender family renames are frequent", "re-check the portal-pivot state at each maintenance pass"). None carries an owner, a next-review date, or a completion record. AUDIT-FINDINGS §15.7 item 10 adds a further re-verification batch to be executed "as part of the publishing pass".

I found direct evidence the list has already gone stale in practice: PR-036 (Sentinel 50 GB tier) is a diarised trigger whose underlying fact changed twice — March 2026 and June 2026 — with the atlas still describing the original state. PR-035 (Defender Suite rename) sits under the "Defender family renames are frequent" trigger and has likewise not been caught.

*Why it matters:* The atlas's entire value proposition is currency; footer line 4 makes that explicit. A prose list of 14 heterogeneous reminders inside a README is not a mechanism — it is a note to self, and the two misses above show it behaving like one. This is the single biggest medium-term risk to the artifact after publication, because degradation is silent: nothing in the build or the UI turns red when a licensing string goes stale.

*Recommendation:* Convert the list to a structured `MAINTENANCE` table (trigger, type, next-review date, affected constants or row ids, last-executed date), ship it in `META`, and surface the next-review date on the about page. Then make the build noisy: `assemble.py` prints a warning when a trigger's next-review date is in the past, and warns when any row's `last_verified` exceeds N days. That turns a prose list into a build-time signal.

*Effort:* 4–6 hours.

---

**PR-051 · Medium · `assemble.py` integrity checks don't cover the invariants most likely to break**

*Evidence:* The integrity block (assemble.py:151–173) validates: unique ids, known framework, valid coverage/confidence/status enums, non-empty sources, product in `PRODUCTS`, primary solution canonical for that product, valid `licensing_model`, presence of the three dependency fields, and valid related-product slug and role. Not validated: `also_involves` entries exist in `SOLUTIONS` and belong to the row's own product; source composition (PR-039); `last_verified` well-formed and not in the future; `control_ref` non-empty; the "no self-reference in `related_microsoft`" rule that §11.5 item 3 established after a real bug (`soc2-cc6-6` self-referencing Entra ID Protection) — a rule now enforced only by author discipline.

I tested the unenforced invariants against the current data and found **zero defects** — the discipline is holding. That is the argument for encoding it now, while the data is clean and the assertions will pass on first run.

*Why it matters:* Each of these is a real class of error the project has either hit once or narrowly avoided, and every one is silent in the UI: a bad `also_involves` key produces a chip linking to a dead solution page; a self-reference produces a card claiming a product depends on itself.

*Recommendation:* Add the five assertions. Since the data is clean, this is purely additive with no remediation work attached.

*Effort:* 2 hours.

---

**PR-052 · Low · `purview_solution` as the product-agnostic solution field is durable debt**

*Evidence:* The field name is retained for schema stability (README schema table; `prow()` docstring; `rowSolution()` in the template exists solely to alias it). It now holds Entra, Intune, Defender, Sentinel, and Defender for Cloud solution names on 228 of 378 rows.

*Why it matters:* Low for the HTML, which aliases it once. Higher for the JSON, which is a publishable artifact in its own right: anyone consuming `compliance-atlas.json` — the most likely form of reuse if you license it openly (PR-041) — meets a field called `purview_solution` containing "Defender for Cloud Apps" and has to be told it doesn't mean what it says.

*Recommendation:* If the JSON is published, emit **both** keys at assemble time: the new canonical `solution` plus `purview_solution` retained as a deprecated alias. Zero risk to the build, and it lets external consumers write correct code. Document the deprecation in the changelog. Don't rename in the row modules — the stability argument for that is sound.

*Effort:* 2 hours.

---

**PR-053 · Medium · Single-maintainer key-person risk, with the reasoning held in one 1,085-line document**

*Evidence:* Every session in AUDIT-FINDINGS is single-author. The verification method depends on judgement that lives in prose: "genuine role only", "Direct only where the control's namesake activity is X", the composition-not-proportion defence of Direct rates (§14.3, §15.3), the seam discipline. The add-a-product procedure is documented in detail and — the roadmap being closed — will never run again, so the most rehearsed process is the one now retired. Meanwhile the *recurring* process (re-verify, correct, republish) is documented only as the 14-bullet trigger list (PR-050) and the §15.7 checklist, neither of which has executed a full cycle.

*Why it matters:* Publishing converts a private project into a commitment. If the atlas goes quiet for a year, it becomes actively harmful — readers will trust stale licensing and stale GA states, which is worse than no atlas. The artifact currently has no way to signal its own staleness (PR-014), no second pair of hands, and no written *maintenance* procedure to hand to one.

*Recommendation:* Two concrete steps, neither requiring another person today. (1) Write the maintenance procedure as an explicit runbook — the re-verification cycle, in the same style as the add-a-product procedure that worked so well, so the knowledge is transferable. (2) Make staleness visible rather than silent: publish the intended re-verification cadence on the about page, and if a row's `last_verified` passes an agreed threshold, render a muted "verification due" marker rather than letting it look current. An atlas that admits when it is behind stays trustworthy; one that can't is fragile.

*Effort:* 4 hours for the runbook; the staleness marker folds into PR-014.

---

**PR-054 · Low · CONTENT-REVIEW §4 (Tier-2 row narratives) remains an open, approved-in-principle backlog**

*Evidence:* CONTENT-REVIEW §4 reports the statistical distribution of row-body field lengths per product and recommends an approach, with nothing proposed for edit; §17.1 records that Tier-2 was "audited and reported but deliberately not edited". No session since has taken it up.

*Why it matters:* Noting rather than re-finding — you already know. My judgement having read a substantial number of row bodies: the Tier-2 variance is real but is **not** a publish blocker. Row bodies live behind a click, are read one at a time by a reader who has already chosen that control, and the §18 progressive-disclosure change addressed the density problem where it actually hurt (the top level). I would put this behind everything in §5(a) and §5(b) below, and behind PR-015.

*Recommendation:* Keep backlogged. Revisit after publication, informed by which rows readers actually open — which you will only know if you have any analytics, and you may well decide you'd rather not.

*Effort:* n/a (deferral).

---

## 4. Accuracy spot-check: methodology and results

### 4.1 Methodology

**Sample.** Seeded (`random.seed(20260719)`), stratified by product with quotas roughly proportional to product size and a floor of 2: Purview 6, Defender XDR 3, Entra 3, Sentinel 2, Intune 2, Defender for Cloud 2 = **18 rows**. Within each stratum, rows were sorted by id before sampling so the draw is reproducible. All 11 frameworks are not covered by an 18-row draw; 9 of 11 are represented (SSPA DPR and PCI DSS did not come up).

**Checks per row.** (1) Control reference exists and its intent paraphrase matches authoritative text — verified against the local authoritative sources in `reference/` (eCFR extracts for HIPAA/GLBA/FERPA, NIST SP 800-53 R5 and 800-171 R2 texts, NIST CSF 2.0 text, AICPA TSC text) or against the live official source. ISO/IEC 27001 references were checked indirectly (the standard is paywalled; control identity confirmed against Microsoft-hosted 2022 Annex A cross-references, consistent with the approach in AUDIT-FINDINGS §F-2). (2) `license_requirement` re-verified against the product's authoritative licensing source, fetched live. (3) Coverage-level honesty assessed on every Direct Support row: does the product perform the control's namesake activity within the stated scope? (4) `purview_solution` and `also_involves` validity.

**Additional whole-dataset checks.** (a) URL resolution: all 156 distinct URLs across rows, framework metadata, solution registry, and product metadata, requested with a browser user-agent, with serial retry for rate-limited hosts and redirect-target comparison. (b) Compliance Manager template names: all 11 frameworks re-verified against a live fetch of `compliance-manager-regulations-list`. (c) Eight structural-integrity queries (§2, W-4). (d) JSON↔HTML embed reconciliation. (e) `node --check` on the built application script.

### 4.2 Control-reference results — 18/18 PASS

| # | Row id | Product | Framework · ref | Verified against | Result |
|---|---|---|---|---|---|
| 1 | `gdpr-5-1-e` | Purview | GDPR Art. 5(1)(e) | EUR-Lex consolidated text — storage limitation | PASS |
| 2 | `soc2-cc8-1` | Purview | SOC 2 CC8.1 | AICPA TSC text — verbatim match on change-management criterion | PASS |
| 3 | `glba-314-4-c2` | Purview | 16 CFR §314.4(c)(2) | eCFR — verbatim ("Identify and manage the data, personnel, devices…") | PASS |
| 4 | `csf-pr-ps-04` | Purview | CSF 2.0 PR.PS-04 | NIST CSF 2.0 — verbatim | PASS |
| 5 | `hipaa-316-b` | Purview | 45 CFR §164.316(b)(1), (b)(2)(i) | eCFR — verbatim (Documentation; 6-year time limit) | PASS |
| 6 | `hipaa-308-a8` | Purview | §164.308(a)(8) | eCFR — verbatim (Standard: Evaluation) | PASS |
| 7 | `53-ir-4-defender` | Defender XDR | 800-53 R5 IR-4 | NIST 800-53r5 — verbatim (Incident Handling) | PASS |
| 8 | `gdpr-33-34-defender` | Defender XDR | GDPR Arts. 33 & 34 | EUR-Lex — breach notification to authority / to data subject | PASS |
| 9 | `hipaa-308-a1-d-defender` | Defender XDR | §164.308(a)(1)(ii)(D) | eCFR — verbatim (Information system activity review) | PASS |
| 10 | `gdpr-25-entra` | Entra | GDPR Art. 25 | EUR-Lex — data protection by design and by default | PASS |
| 11 | `53-ac-7-entra` | Entra | 800-53 R5 AC-7 | NIST 800-53r5 — verbatim (Unsuccessful Logon Attempts) | PASS |
| 12 | `iso-a-8-2-entra` | Entra | ISO/IEC 27001:2022 A.8.2 | Indirect (privileged access rights, 2022 numbering) | PASS (indirect) |
| 13 | `csf-pr-ps-04-sentinel` | Sentinel | CSF 2.0 PR.PS-04 | NIST CSF 2.0 — verbatim | PASS ref · see PR-013 |
| 14 | `hipaa-312-b-sentinel` | Sentinel | §164.312(b) | eCFR — verbatim (Audit controls: "record and examine activity") | PASS |
| 15 | `53-cm-2-intune` | Intune | 800-53 R5 CM-2 | NIST 800-53r5 — verbatim (Baseline Configuration) | PASS |
| 16 | `glba-314-4-c2-intune` | Intune | 16 CFR §314.4(c)(2) | eCFR — verbatim | PASS · source URL now redirects, see PR-038 |
| 17 | `csf-de-cm-09-mdc` | Defender for Cloud | CSF 2.0 DE.CM-09 | NIST CSF 2.0 — verbatim | PASS |
| 18 | `iso-a-8-16-mdc` | Defender for Cloud | ISO/IEC 27001:2022 A.8.16 | Indirect (monitoring activities, 2022 numbering) | PASS (indirect) |

No misnumbered, misattributed, or drifted references. Paraphrase discipline held throughout: no sampled `control_intent` reproduced protected standard text.

### 4.3 Coverage-honesty results on Direct Support rows in the sample

Five of the 18 rate Direct Support. Assessment:

| Row | Claim | Assessment |
|---|---|---|
| `gdpr-5-1-e` | Purview DLM, Art. 5(1)(e) storage limitation | **Sound.** Retention policies are the implementing mechanism, and `how_it_supports` explicitly scopes to M365 workloads and excludes schedule design and non-M365 stores. |
| `hipaa-316-b` | Purview DLM, §164.316(b) 6-year documentation retention | **Sound**, with the right confidence (Medium). Enforces retention; explicitly disclaims producing the documentation. |
| `iso-a-8-2-entra` | Entra PIM, A.8.2 privileged access rights | **Sound.** PIM is the enforcement mechanism for the control's namesake activity. |
| `hipaa-312-b-sentinel` | Sentinel, §164.312(b) audit controls | **Sound.** The regulation's own words are "mechanisms that record and examine activity"; that is what a SIEM is. |
| `csf-pr-ps-04-sentinel` | Sentinel, PR.PS-04 | **Defensible but reads inconsistently in the UI.** The argument (Direct on availability-for-monitoring, generation disclaimed) is explicit and internally consistent with the deliberate AU-2/AU-12 downgrade. My concern is presentational, not analytical — see **PR-013**. |

I did not find an overclaim in the sample.

### 4.4 License-string results — 9 checked, 6 clean, 3 with findings

| Constant | Rows affected | Verified against | Result |
|---|---|---|---|
| `LIC["retention_basic"]` / `["retention_advanced"]` | `gdpr-5-1-e`, `hipaa-316-b` | Purview service description | **PASS** — E3-tier baseline, E5-tier adaptive/auto-apply |
| `LIC["audit_std"]` | `soc2-cc8-1` | Purview SD + audit-solutions-overview | **PASS** — 180-day default confirmed, including the Oct 17 2023 change from 90 days |
| `LIC["audit_prem"]` | `csf-pr-ps-04` | Purview SD | **PASS with omission** — tiers correct; Office 365 E5/A5/G5 missing (PR-037) |
| `LIC["cm"]` | `hipaa-308-a8` | Regulations list | **PASS** — three free premium templates at A5/E5/G5, verbatim |
| `LIC["classification_analytics"]` | `glba-314-4-c2` | Purview SD | **PASS** — E5-tier |
| `ENTRA_LIC["pim"]` | `iso-a-8-2-entra` | Entra licensing article | **PASS** — "either Microsoft Entra ID Governance licenses or Microsoft Entra ID P2", exactly as claimed |
| `ENTRA_LIC["gov_core"]` | `gdpr-25-entra` | Entra licensing article | **PASS** — matches the "capabilities previously generally available in Microsoft Entra ID P2" table rows precisely |
| `ENTRA_LIC["mfa"]` / `["ca"]` | `53-ac-7-entra` | Entra licensing article | **PASS with omission** — tiers correct; E7 and F1/F3 missing from the CA string (PR-037) |
| `INTUNE_LIC["p1"]` | `53-cm-2-intune`, `glba-314-4-c2-intune` | Intune licensing article | **PASS** — E3/E5/E7 and EMS E3/E5 all current |
| `DEFENDER_LIC["mde_p2"]` | all 3 sampled Defender rows (+50 more) | Defender service description | **FINDING** — see PR-035 |
| `SENTINEL_LIC["ingest"]` | both sampled Sentinel rows (+44 more) | Sentinel billing article + partner announcements | **FINDING** — see PR-036 |
| `MDC_LIC` workload meters | both sampled MDC rows | Defender for Storage docs | **PASS in substance** — per-storage-account plus per-GB malware scanning confirmed; the "73M transactions" overage figure is corroborated only in a Microsoft Q&A answer, not in first-party pricing documentation. Not called wrong; flagged as a volatile figure to re-source at the next pass. |

### 4.5 Compliance Manager template names — 11/11 PASS

Live fetch of `learn.microsoft.com/purview/compliance-manager-regulations-list`, compared verbatim. All ten claimed names match exactly (see W-2). `sspa-dpr`'s `exists: false` is correct. One nuance worth a note at the next pass: the atlas's CSF note says "legacy NIST CSF 1.1 template also listed"; the live list shows the legacy entry as simply "NIST CSF" without a version, so the "1.1" is an interpretation rather than a quoted name.

### 4.6 URL resolution — 154/156 → 200

| Outcome | Count | Detail |
|---|---|---|
| HTTP 200 | 154 | |
| HTTP 403 (WAF, documented) | 2 | `dodcio.defense.gov/cmmc/`, `hhs.gov/hipaa/…/security/index.html` — exactly the two in §7.2; both remain human-reachable and both have machine-resolving alternates on every citing row |
| Genuine content redirects | 7 | See PR-038 |
| Locale-only redirects (`/en-us/`) | 130 | Benign |

Note on method: an initial 12-way parallel sweep produced 40 HTTP 429s from `learn.microsoft.com` rate limiting. All 40 returned 200 on serial retry. **If you automate this check, throttle it** — a naive parallel run will report a large false-failure set.

### 4.7 Verdict

**The dataset earns a clean bill on control references, Compliance Manager template names, source resolution, structural integrity, and coverage honesty.** Every finding in this section is licensing-string currency (PR-035, PR-036, PR-037) or source-URL drift (PR-038) — the two fields the project's own maintenance triggers correctly identify as the most volatile. That the drift showed up exactly where the README predicted it would is, in its way, a point in the project's favour. That it had not been caught is the process finding at PR-050.

---

## 5. Prioritized roadmap

Sequenced so each item is a self-contained work session.

### (a) Pre-publish blockers

| # | Item | Finding | Effort | Note |
|---|---|---|---|---|
| 1 | **`git init`, first commit, private remote** — with copyright triage of `reference/` first | PR-040, PR-042 | 2–3 h | Do this before anything else in this list. Everything below becomes reversible once it's done. |
| 2 | **Fix keyboard and screen-reader navigation** — cards and matrix cells to real links, focus styles, skip link, remove `aria-live` from `<main>` | PR-001, PR-002 | 4–6 h | The largest blocker by effort. Template-only. |
| 3 | **Decide the public name; clear `working_title`** | PR-043 | 2 h | Gates the header, the about page, and the license text. |
| 4 | **Add `LICENSE` (content + code) and a footer line** | PR-041 | 2 h | |
| 5 | **Write the about/methodology page with a correction channel** | PR-044 | 6–8 h | Absorbs content from PR-010, PR-021, PR-030, PR-031. Write after items 3 and 4 so it can state the name and licence. |
| 6 | **Licensing re-verification pass** — Defender Suite naming, Sentinel 50 GB, Entra CA, Audit Premium; declared drift ledger | PR-035, PR-036, PR-037 | 4–5 h | Touches `license_requirement`; needs the §16/§17 ledger treatment. |
| 7 | **§15.7 items 5 and 7** — re-verify the 2026-07-16 Purview cohort; reconcile counts across README, FRAMEWORK-SELECTION, and JSON meta | PR-014, PR-028 | 4 h | The §15.7 checklist was written for exactly this moment. |

**Subtotal: ~24–30 hours.**

### (b) Quick wins worth doing before publish

Ordered by value per hour.

| # | Item | Finding | Effort |
|---|---|---|---|
| 8 | **Add the five missing fields to the search index** | PR-012 | 1 h |
| 9 | **Render the coverage/confidence/licensing taxonomies** — landing legend plus badge tooltips | PR-010 | 2–3 h |
| 10 | **Per-route `document.title`** | PR-003 | 1 h |
| 11 | **Surface `last_verified` in the row summary; show a date range on the landing page; bump `as_of`** | PR-014 | 2 h |
| 12 | **Fix the seven redirected URLs; add redirect detection to the URL check** | PR-038 | 2 h |
| 13 | **Two new industry lenses (legal & professional services, insurance)** | PR-020 | 2 h |
| 14 | **Page metadata: description, favicon, Open Graph** | PR-046 | 2 h |
| 15 | **Header `flex-wrap` and mobile hero sizing** — *verify on a device* | PR-005 | 2 h |
| 16 | **Add the five `assemble.py` assertions; correct the README source rule** | PR-039, PR-051 | 2–3 h |
| 17 | **`color-scheme` declaration; loading placeholder** | PR-006, PR-007 | 1 h |
| 18 | **`CHANGELOG.md` backfilled from AUDIT-FINDINGS; content-version vs build-timestamp split** | PR-045 | 4 h |

**Subtotal: ~23–26 hours.** Items 8, 9, and 10 are the three I would not publish without; the rest are genuinely optional-but-cheap.

### (c) Post-publish backlog

Ordered by my view of value, not urgency.

| # | Item | Finding | Effort |
|---|---|---|---|
| 19 | **License-tier lens** — derived `license_band`, summary chip, framework-view filter | PR-015 | 6–8 h |
| 20 | **Structured `MAINTENANCE` table + build-time staleness warnings** | PR-050 | 4–6 h |
| 21 | **Maintenance runbook** (the recurring counterpart to the retired add-a-product procedure) | PR-053 | 4 h |
| 22 | **Row-level deep links** (`#/row/<id>` plus a copy-link affordance) | PR-004 | 2–3 h |
| 23 | **Glossary + first-use `<abbr>` pass** | PR-011 | 4–6 h |
| 24 | **§15.7 item 4: coverage-tier symmetry audit at stacked controls**, with group-level rationale lines | PR-013 | 4–6 h |
| 25 | **Reference-only product treatment for Priva** | PR-031 | 2 h |
| 26 | **Dual-key `solution` / `purview_solution` in the published JSON** | PR-052 | 2 h |
| 27 | **Framework-backlog decisions**: evaluate and document CJIS; re-rank 17a-4/FINRA above the state composite; record NIS2/DORA/27701 rationales | PR-025, PR-026, PR-027 | 4 h (decisions only) |
| 28 | **§15.7 items 1, 2, 3, 6, 9** — remaining consistency-pass items (stale cross-product phrasing, intent variants at stacked refs, terminology normalization, flagged dependency segments, full print pass) | — | 8–12 h |
| 29 | **Map SEC 17a-4 / FINRA** if item 27 confirms the re-ranking | PR-026 | 18–24 h |
| 30 | **Map CJIS** if item 27 says yes; then add the state & local government lens | PR-025 | 20–30 h |
| 31 | **Tier-2 row-narrative normalization** (CONTENT-REVIEW §4) | PR-054 | Deferred |

---

## 6. Closing note

The thing that most distinguishes this project is that its documentation records what it declined to claim: Section K of the DPR evaluated line by line and left unmapped; four separate honest zeroes on FERPA; `dpr-j47` and `dpr-j48` downgraded from Evidence to Not Covered when the easier path was available; the MDCA browser-only boundary carried in three places; PR-013's inversion argued out in the row body rather than smoothed over. That habit is the reason I trusted the dataset enough to spend most of this review outside it — and the reason the 18/18 and 11/11 results below did not surprise me.

The work that remains is not compliance work. It is the work of turning a verified dataset into a public artifact: making it navigable by everyone, explaining its own method, saying who to tell when it's wrong, and building a mechanism — not a list — for keeping it true. That is a smaller job than what has already been done, and it is the job standing between this and being genuinely useful to people who will never read AUDIT-FINDINGS.md.

**Review verdict: not yet ready to publish; approximately one to two focused weeks from it.** No finding requires reopening the dataset, the product roadmap, or the data model.
