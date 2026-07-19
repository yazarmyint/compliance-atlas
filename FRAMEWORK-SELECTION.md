# FRAMEWORK-SELECTION — v1 scope decision

**Date:** 2026-07-16 · **Status:** proposed, awaiting approval
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
- **Compliance Manager premium template:** **Yes — "NIST CSF 2.0"** (verified; legacy "NIST CSF" 1.1 template also still listed).

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
| Higher education | GLBA Safeguards (Title IV) · PCI DSS · CSF 2.0 · *(FERPA: backlog note)* |
| Retail & e-commerce | PCI DSS · CSF 2.0 · SOC 2 · GDPR (as state-privacy analog, annotated) |
| SaaS & technology | SOC 2 · ISO 27001 · GDPR · CSF 2.0 · HIPAA (if PHI) |
| Manufacturing | CSF 2.0 · ISO 27001 · 800-171 (if DIB) · GDPR (if EU) |
| Microsoft suppliers & partners | SSPA DPR v12 · ISO 27001 · SOC 2 |

**Projected dataset size:** ~56 audited/migrated rows + ~85 new rows ≈ **140 rows** across 9 frameworks — consistent with the 12–25-rows-per-framework discipline.

**Cloud-availability policy:** every 800-171/CMMC row gets a verified GCC High/DoD note from the Microsoft 365 US Government service descriptions; other frameworks carry notes only where a mapped feature has a known government-cloud gap. UNVERIFIED rows (if any survive Phase 3) render with a visible warning in the HTML.
