# FRAMEWORK-SELECTION — v1 scope decision

> ## Current state (2026-07-19)
>
> **Status: approved and shipped.** Everything below this box is the original
> 2026-07-16 selection proposal, kept unedited as the record of what was predicted
> versus what shipped. Where the two disagree, this box is authoritative.
>
> | | Proposed (2026-07-16) | Shipped (2026-07-19) |
> |---|---|---|
> | Rows | ≈ 140 | **378** |
> | Frameworks | 9 | **11** |
> | Products | 1 (Purview) | **6** |
> | Industries | 8 | **10** |
>
> **Frameworks (11).** The nine proposed below, plus two promoted from the backlog
> during Increment 1 (2026-07-17): NIST SP 800-53 Rev 5 (curated subset) and FERPA.
> Per-framework row counts: ISO/IEC 27001:2022 57 · NIST SP 800-53 R5 54 · NIST
> 800-171 R2 / CMMC L2 46 · SOC 2 41 · NIST CSF 2.0 40 · HIPAA Security Rule 32 ·
> PCI DSS v4.0.1 31 · Microsoft SSPA DPR 26 · EU GDPR 24 · GLBA Safeguards Rule 21 ·
> FERPA 6.
>
> **Products (6).** The atlas became multi-product after this document was written;
> the roadmap is complete and closed as of 2026-07-18. Purview 150 · Defender XDR 53 ·
> Entra 48 · Sentinel 46 · Intune 41 · Defender for Cloud 40. This is the main reason
> the row count is 2.7x the projection: the projection sized a Purview-only atlas.
>
> **Industries (10).** The eight in the table below, plus **K-12 education** and
> **US federal & FedRAMP-adjacent**. The table's *"(FERPA: backlog note)"* against
> higher education is superseded: FERPA is fully mapped as its own framework
> (see Increment 1), so both education verticals rest on real rows.
>
> **Deferrals still standing:** the state-privacy composite, SEC 17a-4 / FINRA,
> NIS2, DORA, NYDFS, and ISO 27701 all remain out of scope, for the reasons
> recorded in the backlog section and in AUDIT-FINDINGS §15.

**Date:** 2026-07-16 · **Status:** proposed, awaiting approval *(superseded — see Current state above)*
**Hard cap:** 6 new frameworks in v1 (cap fully used). Existing three (Microsoft SSPA DPR v12, ISO/IEC 27001:2022, SOC 2) carry forward after audit — v1 ships **9 frameworks**.

**Selection criteria** (per brief): (1) frequency across US mid-market/enterprise consulting industries — healthcare, education, defense industrial base, finance, retail, SaaS; (2) density of *genuine* Purview relevance (rows we can defend, not rows we can write); (3) maintenance cost of keeping the mapping current.

---

## Selected — 6 new frameworks

### 1. HIPAA Security Rule
- **Version pinned:** 45 CFR Part 160 and Part 164, Subpart C, as currently in force (2003 rule as amended through the 2013 Omnibus Rule).
- **Status verified (2026-07-16):** the December 2024/January 2025 NPRM ("HIPAA Security Rule to Strengthen the Cybersecurity of ePHI", 90 FR 898, published Jan 6 2025) is **not final**; OMB Unified Agenda targets ~July 2027 for final action. v1 maps the current rule and carries a dataset-level note; proposed-rule changes (mandatory encryption, MFA, 72-hour restore, asset inventory) are flagged in relevant rows as "direction of travel," never as requirements.
- **Why:** highest-frequency US regulatory framework in consulting (providers, payers, and the entire business-associate ecosystem — including SaaS vendors touching PHI). Purview density is high and specific: §164.312(b) audit controls → Audit; §164.312(a)(2)(iv)/(e)(2)(ii) encryption (addressable) → sensitivity labels/Customer Key; §164.310(d)(2)(i)-(ii) media disposal/re-use → retention + disposition; §164.308(a)(1)(ii)(D) information system activity review → Audit/Activity explorer/IRM; §164.316(b) documentation retention (6 years) → Records Management; §164.528 accounting of disclosures (Privacy Rule boundary, noted only). Expected ~15–17 rows.
- **Official source:** https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164 (live consolidated text) · HHS: https://www.hhs.gov/hipaa/for-professionals/security/index.html
- **Compliance Manager premium template:** **Yes — "HIPAA/HITECH"** (verified on the regulations list).

### 2. NIST SP 800-171 Rev 2 → CMMC 2.0 Level 2
- **Version pinned:** NIST SP 800-171 **Revision 2** (Feb 2020), the 110 requirements assessed at CMMC Level 2.
- **Status verified (2026-07-16):** 32 CFR Part 170 (CMMC Program rule, final Oct 15 2024, effective Dec 16 2024) anchors Level 2 to SP 800-171 R2; the May 2024 DFARS class deviation keeping R2 (not R3) in force remains active. The 48 CFR acquisition rule published **Sep 10 2025**, contract clauses flowing from **Nov 10 2025** (Phase 1); **Phase 2 — mandatory C3PAO Level 2 certification assessments — begins Nov 10 2026**, four months from now. Rev 3 exists (May 2024) but is *not* the CMMC anchor; noted in framework metadata.
- **Why:** the DIB mid-market is in a compliance crunch right now, and data-centric CUI controls are exactly where Purview lands: 3.1.3 CUI flow control → DLP; 3.1.22 no CUI on public systems → DLP/labels; 3.3.x audit family → Audit; 3.8.x media protection (marking 3.8.4! CUI markings → sensitivity labels) → labels/Endpoint DLP; 3.13.11/3.13.16 CUI cryptography/at-rest → label encryption; 3.6.x incident response evidence. Expected ~14–16 rows. **Every row carries a verified GCC High/DoD cloud-availability note** — CMMC customers overwhelmingly run GCC High, where several Purview features lag or differ.
- **Official sources:** https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final · https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170 · https://dodcio.defense.gov/cmmc/
- **Compliance Manager premium templates:** **Yes — "NIST 800-171" and "CMMC v2 Level 1 / Level 2"** (verified). CMMC L1–L5 (v1) also included by default for GCC/GCC High/DoD tenants.

### 3. NIST Cybersecurity Framework (CSF) 2.0
- **Version pinned:** CSF 2.0 (Feb 26 2024) — confirmed current, no 2.x successor.
- **Why:** the lingua franca for security programs across every industry in scope; the framework a client most often *already speaks*. Purview maps cleanly at subcategory level: ID.AM-07 (data inventory) → Data explorer/DSPM; PR.DS-01/-02/-10 (data at rest/in transit/in use) → labels/DLP; PR.DS-11? no — curated to data-relevant subcategories only: GV (policy evidence via Compliance Manager), ID.AM, PR.DS, PR.AA (data-layer slice), DE.CM (monitoring incl. IRM), RS.AN (forensics via Audit/eDiscovery). Expected ~14–16 rows. Also the natural "translation hub" between frameworks in the HTML pivot.
- **Official source:** https://www.nist.gov/cyberframework · https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
- **Compliance Manager premium template:** **Yes — "NIST CSF 2.0"** (verified; a legacy entry named simply "NIST CSF", with no version attached, is also listed — re-checked 2026-07-19).

### 4. PCI DSS v4.0.1
- **Version pinned:** v4.0.1 (June 2024) — verified as the **only active version**: v3.2.1 retired Mar 31 2024, v4.0 retired Dec 31 2024, and all 51 future-dated requirements became mandatory Mar 31 2025. No v5 on the published horizon.
- **Why:** retail/hospitality/e-commerce frequency plus a distinctive, honest Purview angle: for most M365 estates the goal is **keeping PAN out of collaboration surfaces (scope reduction)** — credit-card SIT + DLP across Exchange/Teams/SPO/endpoints (Req 3 storage minimization support, Req 4 transmission over end-user messaging), plus Req 7 need-to-know (label encryption contribution), Req 9.4 media, Req 10 logging evidence for connected systems, Req 12.10 incident evidence. Claim discipline matters here — Purview does not sit inside a CDE; rows will say "supports scope reduction and evidences," never more. Expected ~12–14 rows.
- **Official source:** https://www.pcisecuritystandards.org/document_library/ (PCI DSS v4.0.1) — requirement intent paraphrased; PCI SSC text is copyrighted.
- **Compliance Manager premium template:** **Yes — "PCI DSS v4.0"** (verified; template pinned at v4.0 — v4.0.1 introduced no new/deleted requirements, noted in framework metadata).

### 5. GLBA Safeguards Rule (FTC)
- **Version pinned:** 16 CFR Part 314 as amended (2021 amendments fully effective Jun 9 2023; breach-notification amendment effective **May 13 2024**).
- **Why:** double-duty framework — non-bank financial institutions (lenders, advisors, fintech, auto dealers, mortgage/collections) **plus all Title IV higher-education institutions** (FSA enforces Safeguards compliance), which partially covers the education vertical without a thin FERPA mapping. §314.4(c) enumerated safeguards are unusually Purview-dense: (c)(2) data inventory → Data explorer/DSPM; (c)(3) access review of customer information → label encryption contribution + audit; (c)(4) encryption at rest/in transit → labels (+dependency note); (c)(6)(ii) **secure disposal within two years** → retention/disposition (a rare hard retention mandate!); (c)(8) monitoring/logging of authorized-user activity → Audit/IRM; §314.4(h) incident response + §314.4(j)(1) FTC notification within 30 days for ≥500 consumers → Audit forensics evidence. Expected ~11–13 rows.
- **Official source:** https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-314 · https://www.ftc.gov/legal-library/browse/rules/safeguards-rule
- **Compliance Manager premium template:** **Yes — "Gramm-Leach-Bliley Act, Title V, Subtitle A, Financial Privacy"** (verified; template spans GLBA Title V — its safeguards coverage should be sanity-checked at engagement time; a separate "FTC Privacy of Consumer Financial Information" template also exists).

### 6. EU GDPR
- **Version pinned:** Regulation (EU) 2016/679 (consolidated text; stable).
- **Why:** the most-requested privacy framework from SaaS/multinational mid-market; also the reference model for the state-privacy composite deferred to backlog (rows annotated so they translate). Purview density high with clean claim boundaries: Art. 5(1)(c)/(e) minimization & storage limitation → classification + retention; Art. 15/17/20 subject rights → eDiscovery/Data explorer locate (+ Priva dependency); Art. 25 data protection by design → labels/DLP as technical measures; Art. 30 ROPA → Not Covered boundary row (Priva/process); Art. 32 security of processing → labels/DLP/encryption/monitoring; Art. 33/34 breach → Audit forensics ("categories and approximate number of data subjects concerned" is literally an Audit/eDiscovery output); Art. 35 DPIA → Evidence. Expected ~14–16 rows.
- **Official source:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Compliance Manager premium template:** **Yes — "EU GDPR (General Data Protection Regulation)"** (verified).

---

## Increment 1 (2026-07-17) — promoted from the backlog

### 7. NIST SP 800-53 Rev 5 — curated data-protection subset
- **Version pinned:** SP 800-53 Rev 5, **Release 5.2.0 (Aug 27, 2025)** — verified current; Release 5.2.0 added SA-15(13), SA-24, SI-2(07) and revised SI-7(12) (secure-software focus, EO 14306) — none in this subset. No Rev 6 announced as of 2026-07-17.
- **Sources:** https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final · https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls
- **Compliance Manager premium template:** **Yes — "NIST 800-53 rev.5"** (re-verified on the regulations list 2026-07-17; a rev.4 template also remains).
- **Scope decision (the v1 backlog rationale is the spec):** not a catalog restatement — a **21-row data-protection subset covering 22 controls** (AU-2 and AU-12 share one row — uniform story), validated control-by-control for genuine Purview relevance. Where the Purview story is materially identical to an existing 800-171 row, the 800-53 row stays concise and cross-references the derived 800-171 requirement instead of re-deriving prose.

| Family | Controls mapped | One-line rationale |
|---|---|---|
| AC | AC-3, AC-4, AC-21, AC-22 | Data-layer access enforcement, information-flow control (DLP core), sharing assistance, public-content control |
| AU | AU-2 & AU-12 (combined — uniform story), AU-6, AU-9, AU-11 | The logging family is Purview Audit's home turf: generation, review surfaces, log protection, retention |
| CM | CM-12 only | "Information location" is the most Purview-shaped control in the catalog — Data explorer *is* the implementation for M365 |
| IR | IR-4, IR-9 | Incident evidence + information-spillage response (DLP detection → eDiscovery purge) |
| MP | MP-3, MP-6 (boundary), MP-7 | Media marking (labels), sanitization (honest Not Covered — content deletion ≠ media sanitization), removable-media use |
| PS | PS-4 | Termination monitoring — IRM departing-user policies |
| RA | RA-3 | Risk-assessment evidence (data discovery/DSPM inputs) |
| SC | SC-8, SC-28 | Data in transit / at rest — content-layer crypto stories mirrored from 800-171 |
| SI | SI-4, SI-12, SI-19 | Monitoring contribution, information management & retention (the catalog's retention control — DLM direct), de-identification evidence |

- **Validated adjustments vs the v1 memo:** **IR-8 dropped** (an IR *plan document* — no Purview hook); **RA-5 dropped** as the memo itself predicted (vuln scanning — marginal); **added** AC-22, CM-12, IR-9, PS-4, SI-4, SI-12, SI-19. **PT family evaluated and excluded** — PT-2 through PT-8 are authority/consent/notice obligations (process-owned; Priva is the tooled layer and stays a dependency). **PM family excluded** (org-level program controls outside the control baselines).
- **Cloud policy:** federal-facing, so every row carries a verified GCC/GCC High/DoD note; framework notes cite GCC High's NIST SP 800-53 FIPS 199 High assessment basis.

### 8. FERPA
- **Version pinned:** 34 CFR Part 99, current text verified against eCFR (2026-07-15 issue; base 53 FR 11943 as amended). **Active rulemaking:** ED signaled intent (Fall 2024 Unified Agenda) to propose FERPA regulation amendments — no NPRM published as of 2026-07-17; noted in framework metadata as a watch item.
- **Sources:** https://www.ecfr.gov/current/title-34/subtitle-A/part-99 · https://studentprivacy.ed.gov/ferpa
- **Compliance Manager premium template:** **Yes — "US - Family Educational Rights and Privacy Act (FERPA)"** (re-verified on the regulations list 2026-07-17).
- **Scope decision:** exactly the slim addendum the backlog specified — **5 rows**, no padding: §99.31(a)(1)(ii) reasonable-methods access restriction (labels/encryption/DLP), §99.30/§99.33 consent-bound disclosure & redisclosure limits (DLP egress guarding), §99.32 disclosure recordkeeping (Audit evidence), §99.10 right to inspect within 45 days (eDiscovery locate/collect), and the destruction obligations in §99.31(a)(6)(iii)(C)/§99.35(b)(2) (retention/disposition). FERPA remains an access-and-disclosure-governance regime — rows skew Partial/Evidence by design, and the student information system (SIS) is flagged throughout as the primary record store outside Purview's reach.

---

## Rejected — documented backlog (remaining)

| Candidate | Decision & rationale | Backlog disposition |
|---|---|---|
| **US state privacy composite** (CCPA/CPRA + CO, VA, CT, TX, …) | ~20 divergent, still-churning state laws = highest maintenance cost of any candidate; Purview stories are near-duplicates of the GDPR rows (minimization, retention, DSR locate, "reasonable security"). CM templates exist for CCPA/CPRA and several states. | v2 as a **CPRA-anchored composite** with a state-variance column; until then the GDPR rows are annotated as the analog and the industries map points retail/SaaS at them. |
| *(observed during verification, unsolicited)* SEC 17a-4 / FINRA books-and-records & supervision; NYDFS 23 NYCRR 500; NIS2; DORA; ISO/IEC 27701 | Not in the candidate list, but flagged: 17a-4/FINRA is the strongest untapped Purview story in finance (Records Management immutability + Communication Compliance supervision are purpose-built for it). | High-value v2 candidates for the finance vertical; CM templates exist for SEC 17-4(a), FINRA checklist, NIS2, DORA. |

---

## Resulting v1 industry coverage (preview of the industries map)

| Industry | Frameworks in v1 |
|---|---|
| Healthcare & life sciences | HIPAA SR · PCI DSS · CSF 2.0 · SOC 2 · ISO 27001 |
| Defense industrial base | 800-171 R2/CMMC L2 · CSF 2.0 · ISO 27001 |
| Financial services | GLBA Safeguards · PCI DSS · SOC 2 · CSF 2.0 · ISO 27001 |
| Higher education | GLBA Safeguards (Title IV) · PCI DSS · CSF 2.0 · *(FERPA: backlog note — superseded, FERPA shipped as a full framework)* |
| Retail & e-commerce | PCI DSS · CSF 2.0 · SOC 2 · GDPR (as state-privacy analog, annotated) |
| SaaS & technology | SOC 2 · ISO 27001 · GDPR · CSF 2.0 · HIPAA (if PHI) |
| Manufacturing | CSF 2.0 · ISO 27001 · 800-171 (if DIB) · GDPR (if EU) |
| Microsoft suppliers & partners | SSPA DPR v12 · ISO 27001 · SOC 2 |

**Projected dataset size:** ~56 audited/migrated rows + ~85 new rows ≈ **140 rows** across 9 frameworks — consistent with the 12–25-rows-per-framework discipline.

> *Shipped: 378 rows across 11 frameworks and 6 products. The 12–25-per-framework
> discipline held per product; the projection assumed a single product. See the
> Current state box at the top.*

**Cloud-availability policy:** every 800-171/CMMC row gets a verified GCC High/DoD note from the Microsoft 365 US Government service descriptions; other frameworks carry notes only where a mapped feature has a known government-cloud gap. UNVERIFIED rows (if any survive Phase 3) render with a visible warning in the HTML.

---

## Session 13 — framework-backlog decisions (2026-07-21)

A decisions-only session: no rows, no template, no build logic changed, and
`compliance-atlas.json` moved only by the two maintenance triggers recorded below.
Everything here was verified live on 2026-07-21 (standing rule: no training knowledge).
This section is appended, not merged into the frozen 2026-07-16 proposal above.

### PR-025 — CJIS Security Policy v6.0: **DEFERRED with two dated triggers**

**Decision: defer.** Not declined, not mapped now. CJIS is reconsidered when a demand
criterion is met or, at the latest, when the policy is fully auditable. Both drafted
entries are recorded below per the document's own rubric — the case for mapping and the
case for declining — followed by the recorded decision and its machinery.

**The finding that sizes the effort:** v6.0 (FBI, dated 2024-12-27) rebased the entire
policy onto **NIST SP 800-53 Rev 5 at the moderate baseline** — 20 policy areas, 180+
primary controls / 1,300+ subcontrols, every control traceable to 800-53. P1 controls are
auditable and sanctionable now; **P2–P4 become fully auditable Oct 1, 2027**; FBI v6.0
audits began Oct 1, 2025. Because the atlas already ships a 21-row / 22-control 800-53
Rev 5 data-protection subset, **roughly 18–20 of those 22 mapped controls fall inside the
moderate baseline CJIS v6.0 now incorporates** — the Purview derivations already exist and
CJIS rows would cross-reference them rather than re-derive, exactly as the 800-53 subset
cross-references 800-171. That is a genuine discount on the expensive part of the work.

#### The case for mapping (selected-framework rubric)

- **Version pinned:** FBI CJIS Security Policy **v6.0** (dated 2024-12-27).
- **Status verified (2026-07-21):** v6.0 rebased the policy onto NIST SP 800-53 Rev 5 at
  the moderate baseline (20 policy areas, 180+ primary controls / 1,300+ subcontrols).
  Phased by priority: P1 auditable and sanctionable now; P2–P4 fully auditable Oct 1, 2027.
  FBI v6.0 audits began Oct 1, 2025; v5.9.5 retired as the audit standard.
- **Why:** the only one of the three deliberately-absent industries the six-product atlas
  can serve well. CJIS maps densely across every product: Audit & Accountability → Purview
  Audit + Sentinel; Identification & Authentication (advanced-authentication mandate) →
  Entra; the Mobile Devices policy area → Intune; Malicious Code Protection → Defender XDR;
  posture and continuous assessment → Defender for Cloud; Access Control and Media
  Protection at the data layer → labels/DLP/retention. The 800-53 rebasing means the
  Purview story for ~18–20 of our 22 mapped 800-53 controls already exists and is reused.
  Expected ~24–30 rows across all six products; effort ~22–28 h (lower-middle of the
  20–30 h roadmap band, calibrated against the Increment 1 authoring rate of 26 rows in one
  session and the 21-row GLBA / 26-row SSPA DPR end-state sizes).
- **Cloud policy:** every row carries a verified government-cloud note. Microsoft attests
  in the **Government clouds** (Azure Government, Office 365 GCC, Dynamics 365 US Gov);
  state and local agencies deploy into GCC, not GCC High. v6.0's moderate / FedRAMP
  alignment is opening an Azure Commercial path Microsoft now markets — recorded as
  direction-of-travel, never as the mapped baseline.
- **Official source:** https://le.fbi.gov/file-repository/cjis_security_policy_v6-0_20241227.pdf
  · Microsoft position: https://learn.microsoft.com/compliance/regulatory/offering-cjis
- **Compliance Manager premium template:** **Yes** — "Criminal Justice Information Services
  (CJIS) Security Policy" (confirmed on the regulations list; the offering page confirms a
  premium assessment template exists).
- **Caveat on record:** Microsoft's offering page (updated 2026-06-11) still describes the
  pre-v6.0 "13 areas" structure and gives a state-coverage list dated Sept 27 2024 (47
  states + DC) that already disagrees with a 2026 figure of 45 (missing DE/LA/OH/SD/WY).
  Per-state agreement status is a moving target and a real maintenance cost.

#### The case for declining (rejection rubric)

| Candidate | Decision & rationale | Backlog disposition |
|---|---|---|
| **CJIS Security Policy v6.0** | Evaluated 2026-07-21, not selected *now*, on the document's own criteria. (1) **Moving target / maintenance cost:** v6.0 is mid-rollout — P2–P4 are not fully auditable until Oct 1 2027, so mapping today pins to a control set whose enforcement and interpretation are still settling, and Microsoft's attestation surface (clouds, per-state agreements) is drifting (47+DC in 2024 → 45 in 2026). (2) **Derivative density:** because v6.0 now traces to 800-53 Rev 5 moderate, ~18–20 of the Purview-relevant controls are near-duplicates of rows the atlas already ships in its 800-53 subset — the same near-duplication objection that defers the state-privacy composite. (3) **No demonstrated demand:** one day post-publication there is zero human-traffic signal (see the demand criterion below), and CJIS is a ~22–28 h increment. | Deferred with dated triggers, not rejected. |

#### Recorded decision

**Defer, and instrument the deferral so it is a criterion, not a vibe.** The map-now case
is real — the 800-53 rebasing makes the marginal cost unusually low while the research is
fresh, and CJIS is the highest-value *industry* unlock available (state and local
government, currently an absent-industry the atlas cannot serve). Its strongest form:
waiting forgoes a cheap, high-differentiation increment and lets the research decay, so
that by Oct 2027 the ramp-up is re-paid. Weighed against that: this is a decisions-only
posture with no demonstrated demand, P2–P4 do not fully bite until Oct 2027, and the honest
move is to hold against a stated threshold. Deferral wins, with two conditions recorded as
triggers rather than prose:

- **`TRG-CJIS-DEMAND`** (type `watch`, `next_review` 2026-08-20) — the demand-criterion
  check, evaluated against a post-bot-wave 4-week window. **Thresholds (authoritative here):**
  a ~22–30 h increment is justified if, over a rolling 4-week window after the publication
  bot-wave settles, **any one** holds: (a) **≥ 3 GitHub stars OR ≥ 1 fork by a non-bot
  account**; (b) **≥ 1 substantive inbound** — an Issue, a `cjis@`-style question, or an
  engagement request that *names a gap the increment fills* (for CJIS: anything from the
  state/local-government audience); (c) **repo unique visitors ≥ ~10/week for 3 of 4 weeks**
  (a sustained trend, not a single spike). Numbers are deliberately modest: a niche B2B
  compliance reference never trends, so the test is direction and specificity — a real
  human, ideally in the target vertical — not volume.
- **`TRG-CJIS-V6-REVISIT`** (type `framework`, `next_review` 2027-10-01) — the backstop:
  P2–P4 fully auditable. The trigger note records that the 800-53 rebasing discount and the
  cross-reference authoring technique are captured in this section, so a future pass starts
  from the research, not from scratch.

**Standing override (recorded so it is not re-litigated):** a concrete state or local
government engagement satisfies the criterion immediately and overrides the wait. The demand
thresholds are the *floor* for speculative work, not a gate on a real client need.

**No-instrumentation decision (recorded so it is not re-proposed):** the demand thresholds
are **repo-side and inbound signals only** — GitHub stars, forks, issues, engagement
requests, and repo unique-visitor counts. **No analytics or telemetry will be added to the
published page.** The atlas is a single, self-contained, zero-dependency artifact that phones
home to nothing; that posture is a deliberate feature (privacy, portability, longevity, and
"no gate-invisible artifact" discipline), not an oversight. A page-side counter was
considered as the one measurement that would see actual readership — the GitHub traffic API
sees only the source repo, not the GitHub Pages site — and **rejected** on the
no-phoning-home principle. Demand is therefore measured with a coarser but honest
repo-side proxy, and that trade is accepted on purpose.

### PR-026 — SEC 17a-4 / FINRA re-ranked above the state-privacy composite: **confirmed**

**17a-4 verified current (2026-07-21):** the Oct 12, 2022 amendments (SEC Release 34-96034)
that retained WORM as an option and added the audit-trail alternative remain the current
state; no further amendment to 17a-4's electronic-recordkeeping provisions has been adopted
since, and the WORM / audit-trail landscape is settled.

The backlog originally listed the state-privacy composite as the lead v2 item and
17a-4/FINRA as a lower "observed during verification" note. That ordering is reversed here,
on this document's own three criteria plus one the original memo never weighed:

1. **Maintenance cost (criterion 3).** The composite's own rejection rationale is that it is
   "~20 divergent, still-churning state laws = highest maintenance cost of any candidate."
   17a-4 is the opposite: a single-regulator rule whose last substantive change (the 2022
   electronic-recordkeeping modernization) is settled and verified unchanged as of
   2026-07-21. Promoting the cheapest-to-maintain candidate over the most expensive follows
   the memo's own logic.
2. **Density of genuine relevance (criterion 2).** The memo already concedes 17a-4 is "the
   strongest untapped Purview story in finance." The composite concedes the reverse — its
   "Purview stories are near-duplicates of the GDPR rows" — which is exactly what the
   12–25-rows-per-framework curation discipline exists to prevent.
3. **Portfolio balance (not weighed originally).** Records Management and Communication
   Compliance are the two thinnest Purview solutions in the shipped atlas by primary-row
   count; Communication Compliance carries essentially one narrow primary mapping (SOC 2
   CC1.1, Evidence/Low). 17a-4's WORM/immutability requirement and FINRA 3110 supervision
   are the *namesake* activities of Records Management and Communication Compliance
   respectively — this framework is the one addition that makes both Direct on their home
   turf. It corrects a coverage imbalance, not just adds rows.

**Decision: confirmed.** SEC 17a-4 / FINRA is the **lead v2 framework candidate**; the
state-privacy composite remains deferred with the GDPR rows as the annotated interim analog.
Effort to map: ~18–24 h. The MAINTENANCE backlog ranking is updated to match.

### PR-027 — NIS2 / DORA / ISO 27701 rejection rationales: **recorded**

Each was considered and not selected; the reasoning was never written down, which reads to
an outside reader as "never considered." Each verified live and dated 2026-07-21.

| Candidate | Decision & rationale | Backlog disposition |
|---|---|---|
| **NIS2 (Directive (EU) 2022/2555)** | Considered, not selected. In force — transposition was due Oct 17 2024, applies from Oct 18 2024 — but transposition is still uneven (≈22–23 of 27 member states transposed as of mid-2026; FR/IE/LU/NL/ES still in legislative procedure), so a mapping would chase 27 divergent national implementations. More decisively, NIS2 is weighted toward governance, incident-reporting, and ICT-risk-management obligations on the entity, not data-layer or endpoint controls; an honest Purview mapping yields a thin, Evidence-heavy row set. | Deferred. ISO 27001 and CSF rows carry the transferable security-of-processing story in the interim. |
| **DORA (Regulation (EU) 2022/2554)** | Considered, not selected. In application since **Jan 17 2025**, so currency is not the issue. Declined for the same substance reason as NIS2, more sharply: DORA is operational-resilience law — ICT third-party risk, resilience testing, incident classification, register-of-information obligations — with almost no data-classification or data-protection surface Purview implements. The defensible row count is very low and mostly Evidence. | Deferred. A finance-vertical framework need is better served by 17a-4/FINRA (PR-026), which is Purview-dense. |
| **ISO/IEC 27701** | Considered, not selected. The **2025 revision (released Oct 14 2025) makes it a standalone privacy standard** rather than the 2019 extension to ISO 27001 — but this does not change the disposition. 27701 is a privacy information-management system whose tooled layer in the Microsoft estate is **Priva**, which the atlas has permanently and deliberately declined to map (§15 roadmap closure; priva is reference-only). Mapping 27701 would produce a framework whose best answer is a product the atlas will not author. | Deferred, effectively permanent while the Priva boundary stands. GDPR rows carry the transferable privacy-control story. |

### Versioning of this session

**PATCH bump to 3.1.2.** The two `meta.maintenance` triggers change the published bytes of
`compliance-atlas.json`, so under the existing machinery-only rule they take a PATCH — the
version must uniquely identify one artifact, and two different JSON files may never both
claim 3.1.1. The docs-only records that shipped alongside (this file, docs/MAINTENANCE.md,
and the CHANGELOG clarifying line) touch no artifact and take no bump on their own. The full
reasoning is recorded in AUDIT-FINDINGS §31; the CHANGELOG versioning policy gained a line
stating the docs-only carve-out.
