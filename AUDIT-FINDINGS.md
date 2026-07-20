# AUDIT-FINDINGS — Purview Compliance Mapping Matrix

**Audit date:** 2026-07-16
**Auditor:** Claude (Fable 5) — automated audit with live-source verification
**Subject:** `Purview-Compliance-Mapping-Matrix.xlsx`, sheet "Mapping Matrix" (44 data rows: 14 Microsoft SDPR, 15 ISO/IEC 27001:2022, 15 SOC 2)
**Method:** Every control reference checked against the current official framework source (DPR v12 PDF, AICPA 2017 TSC w/ 2022 revised points of focus PDF, ISO/IEC 27001:2022 catalog + Microsoft-hosted control cross-references). Every named Purview capability checked against current Microsoft Learn documentation. Coverage/Confidence ratings assessed for defensibility under the claim-strength taxonomy (Direct Support / Partial Support / Evidence Support Only / Not Covered × High / Medium / Low).

**Verdict key:** `CONFIRMED` (carries forward as-is, possibly reworded) · `CORRECTED` (ref, capability naming, or rating changed) · `REMOVED` (row dropped) · `ADDED` (gap filled with a new row).

---

## 1. Framework-level findings

### F-1. "Microsoft SDPR (DPR v12)" — version CONFIRMED current; name CORRECTED
- **Claim:** Sheet maps "Microsoft SDPR" at "DPR v12".
- **Verdict:** v12 **is the current version** — *Microsoft Supplier Data Protection Requirements, Version 12, March 2026* (FY26 SSPA cycle). Not superseded as of 2026-07-16. The v12 revision reduced total requirements from 67 to 63 (consolidations + 2 net-new in Sections J & K); **all 14 requirement numbers referenced in the sheet survive under v12 numbering** (verified individually below against the v12 PDF).
- **Correction:** "SDPR" is not the official label. The program is **SSPA** (Supplier Security and Privacy Assurance); the document is the **DPR**. Dataset will use framework name **"Microsoft SSPA DPR"**, version **"v12 (March 2026)"**.
- **Sources:** https://www.microsoft.com/en-us/procurement/sspa · v12 PDF: https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/accex/documents/presentations/FY26-Microsoft-Supplier-Data-Protection-Requirements-v12_en-US.pdf (local copy: `reference/DPR-v12.pdf`)

### F-2. ISO/IEC 27001:2022 — CONFIRMED current
- 2022 is the current edition (third edition). Amendment 1:2024 (climate-action wording in clause 4 context) does not change Annex A controls. All 15 Annex A references in the sheet exist under 2022 numbering; spot-verified against Microsoft-hosted ISO 27001:2022 control mappings (MCSB v2 pages reference A.8.3, A.8.11, A.8.16, A.8.24 etc. under the 2022 scheme).
- **Sources:** https://www.iso.org/standard/27001 · https://learn.microsoft.com/azure/compliance/offerings/offering-iso-27001 · https://learn.microsoft.com/security/benchmark/azure/mcsb-v2-data-protection

### F-3. SOC 2 — CONFIRMED current; citation pinned
- Current criteria: **2017 Trust Services Criteria (With Revised Points of Focus — 2022)**, AICPA TSP Section 100. The 2022 revision changed points of focus only, not the criteria. All criteria IDs referenced in the sheet verified against the TSC document text (local copy: `reference/AICPA-TSC-2017-2022POF.pdf`).
- **Source:** https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022

### F-4. Purview product-name drift since the sheet was built — CORRECTED across rows
Verified against Microsoft Learn (2026-07-16):
1. **eDiscovery:** classic Content Search / eDiscovery (Standard) / eDiscovery (Premium) experiences **retired August 31, 2025**. Current solution is unified **Microsoft Purview eDiscovery** (premium features license-gated). Rows now say "eDiscovery (premium features)" where relevant. Source: https://learn.microsoft.com/purview/edisc · https://learn.microsoft.com/purview/ediscovery
2. **Content Explorer:** new **Data explorer** now coexists with **Content explorer (classic)** under Information Protection → Explorers. Rows updated to "Data explorer / Content explorer (classic)". Source: https://learn.microsoft.com/purview/data-classification-data-explorer
3. **DSPM:** two generations exist — **DSPM (classic)** and the current expanded **Data Security Posture Management** (covers Azure/Fabric/third-party SaaS; subsumes **DSPM for AI (classic)** going forward). License: M365 E5 or **Microsoft Purview Suite (formerly Microsoft 365 E5 Compliance)**. Sources: https://learn.microsoft.com/purview/data-security-posture-management-learn-about · https://learn.microsoft.com/purview/data-security-posture-management-get-started
4. **Audit:** Audit (Standard) default retention is now **180 days**; Audit (Premium) gives 1-year default for Entra/Exchange/SharePoint/OneDrive records + retention policies up to 1 year (10 years with add-on). Source: https://learn.microsoft.com/purview/audit-solutions-overview
5. **Licensing SKU rename:** "Microsoft 365 E5 Compliance" add-on now marketed as **Microsoft Purview Suite**. License fields in the new dataset use service-description names. Source: https://learn.microsoft.com/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-purview-service-description
6. **Information Barriers:** current, not deprecated (multi-segment mode is the current architecture; legacy mode being upgraded). Source: https://learn.microsoft.com/purview/information-barriers-teams
7. **New solution not in the sheet or canonical list:** **Microsoft Purview Data Security Investigations** (AI-assisted incident-scoped data investigation) now appears in Learn as a data-security solution. Not added to v1 rows (kept to the agreed canonical list) — flagged as a backlog candidate. Source: https://learn.microsoft.com/purview/purview (data security solutions list)

### F-5. Migration scaffolding dropped — per project ground rules
`Source-tenant current state`, `Destination-tenant target state`, `Migration action` columns do not carry forward. `Control owner / Status / Notes` tracker columns also dropped (engagement-specific). Replaced by the new row schema (see `README.md`).

---

## 2. Row-by-row findings — Microsoft SSPA DPR v12

All DPR requirement text verified in the v12 PDF (March 2026). Requirement numbering: Sections A(1–5), B(6), C(7–8), D(9–11), E(12–13), F(14–22), G(23–28), H(29), I(30–32), J(33–50), K(51–63).

| # | Row | Claim audited | Verdict | Notes |
|---|-----|---------------|---------|-------|
| 1 | SDPR-A5 (A #5) | Process only per documented instructions; policies accessible → config exports + admin audit as evidence (Evidence Support Only / High) | **CONFIRMED** | v12 A#5 verbatim intent match. Purview shows *what is configured and when it changed*; the contractual instruction itself is non-Purview. |
| 2 | SDPR-D9 (D #9) | Collection minimization → Content Explorer/DSPM/SITs (Partial / Medium) | **CONFIRMED** (capability renamed) | v12 D#9 requires suppliers to **monitor** collection so only required data is collected — classification analytics genuinely implement the monitoring half. Capability now "Data explorer / Content explorer (classic) + DSPM". |
| 3 | SDPR-D11 (D #11) | Reduced-identifiability data sets → SIT detection (Evidence Support Only / Low) | **CONFIRMED** | v12 D#11 covers pseudonymous/NPI/unlinked data sets. SITs detecting direct identifiers inside such stores evidences non-re-identification hygiene. |
| 4 | SDPR-E12 (E #12) | Retain no longer than necessary → DLM retention (Direct / Medium) | **CONFIRMED** (scope note added) | Direct within M365 workloads; supplier data outside M365 is out of Purview's reach — noted in row. |
| 5 | SDPR-E13 (E #13) | Return/destroy on completion + disposition record → Records Management disposition (Partial / Medium) | **CONFIRMED** | v12 E#13: return **or** destroy at Microsoft's discretion. Disposition review + records of disposition = the destruction-evidence half; return-of-data is manual. |
| 6 | SDPR-F14 (F #14–22) | DSR support → "Microsoft Priva (primary); eDiscovery/Content Explorer to locate" (Partial / Medium) | **CORRECTED** | Range F#14–22 verified (all of Section F). **Ground-rule fix:** Priva can never be the mapped capability. Row now maps **eDiscovery** (+ Data explorer) for locate/collect/record-keeping; Priva moved to `non_purview_dependencies`. Coverage stays Partial / Medium. |
| 7 | SDPR-I30 (I #30–31) | Incident response & notification → alerts + audit trail (Evidence Support Only / High) | **CONFIRMED** (strengthened wording) | v12 I#30 explicitly requires giving Microsoft "a scope of data accessed" — Audit (Premium) + Activity explorer directly produce that artifact. I#31 remediation tracking verified. |
| 8 | SDPR-J35 (J #35) | Asset inventory incl. data classification → labels + Content Explorer (Partial / Medium) | **CONFIRMED** | v12 J#35 evidence bullet explicitly includes "Data classification of the data on the asset". |
| 9 | SDPR-J36 (J #36) | Access-rights mgmt, MFA, 48h deprovisioning → label encryption contributes (Partial / Medium) | **CORRECTED** (confidence → Low) | v12 J#36 is squarely an identity control (lockout, MFA, 48-hour deactivation, least privilege — Entra/IdP territory). Label-based encryption is a real but small data-layer contributor. Partial stands; Medium confidence was not defensible. |
| 10 | SDPR-J40 (J #40) | DLP program; classify/label/protect → DLP + Endpoint DLP (**Direct** / High) | **CORRECTED** (coverage → Partial) | v12 J#40 text *mandates* host/network/cloud IDS and IPS, breach analysis, and offboarding comms as minimum elements of the DLP program — that half is non-Purview. Classification/labeling/DLP core is genuinely Direct, but the requirement as written cannot be Direct-supported by Purview alone. Partial / High. IRM + Adaptive Protection added to capability detail for the "monitor for unauthorized activity" element. |
| 11 | SDPR-J47 (J #47) | Encrypt in transit (TLS/IPsec) → label encryption complements (Partial / Low) | **CORRECTED** (→ Not Covered / High) | v12 J#47 is transport-layer: TLS/IPsec per NIST 800-52/57, refuse unencrypted delivery, certificate lifecycle. Purview implements none of it and evidences none of it. Sensitivity-label encryption travels with content but does not satisfy or evidence a transport-encryption control. Kept as an explicit boundary row. |
| 12 | SDPR-J48 (J #48) | Full-disk encryption → "Endpoint DLP assumes managed devices" (Evidence Support Only / Medium) | **CORRECTED** (→ Not Covered / High) | FDE is BitLocker/FileVault + Intune compliance. Purview neither implements nor evidences it — Endpoint DLP requiring onboarded devices is not evidence of disk encryption. Boundary row. |
| 13 | SDPR-J49 (J #49) | Encrypt at rest, enumerated types → auto-label + encrypt (Partial / Medium) | **CONFIRMED** (enriched) | v12 J#49 enumerates credential, payment, medical, government-ID, DOB, geolocation, customer-content data etc. — nearly all have built-in SIT coverage for auto-labeling with encryption. Microsoft Purview Customer Key noted for the M365 at-rest layer; platform service encryption remains a dependency. |
| 14 | SDPR-J50 (J #50) | Anonymize data in dev/test → SIT detection flags PII in non-prod (Evidence Support Only / Medium) | **CONFIRMED** | Purview detects, does not anonymize. |

**ADDED (SDPR):**

| Row | Rationale | Sources |
|-----|-----------|---------|
| SDPR-J33 (J #33) → **Compliance Manager** + Audit, Evidence Support Only / Medium | v12 J#33 requires annual security assessments (risk/vuln to CIA of Microsoft Personal Data) + change review + change logs. Compliance Manager assessments structure and evidence the assessment activity for the M365 estate; Purview admin audit supplies policy change logs. No existing row covered Section J's assessment requirement. | DPR v12 PDF · https://learn.microsoft.com/purview/compliance-manager |

**Consciously NOT added (SDPR):** Section K (AI Systems, K#51–63) was evaluated line-by-line. These govern the *supplier's own AI systems* (transparency disclosures, rollback plans, model update processes) — organizational/engineering controls with no defensible Purview mapping. Staff use of third-party AI with Microsoft data is already addressed inside the J#40 row's capability detail (endpoint DLP for AI sites / DSPM for AI visibility). Overreach avoided deliberately.

---

## 3. Row-by-row findings — ISO/IEC 27001:2022 Annex A

All 15 referenced control IDs exist under 2022 Annex A numbering. Control intent stays paraphrased (ISO text is copyrighted).

| # | Row | Claim audited | Verdict | Notes |
|---|-----|---------------|---------|-------|
| 15 | ISO-5.9 Inventory of information & associated assets → Data explorer/DSPM (Partial / Medium) | **CONFIRMED** (capability renamed) | Purview produces the *information/data* half of the inventory for M365; device/system inventory is CMDB territory. |
| 16 | ISO-5.10 Acceptable use → label handling guidance + DLP policy tips (Partial / Medium) | **CONFIRMED** | |
| 17 | ISO-5.12 Classification of information → sensitivity labels + SITs (Direct / High) | **CONFIRMED** | Canonical mapping. |
| 18 | ISO-5.13 Labelling of information → sensitivity labels content marking (Direct / High) | **CONFIRMED** | Canonical mapping. |
| 19 | ISO-5.14 Information transfer → DLP external sharing + label encryption (**Direct** / Medium) | **CORRECTED** (→ Partial / High) | A.5.14 spans rules/agreements/procedures for electronic, physical and verbal transfer. Purview enforces the electronic-transfer restrictions inside M365 strongly — but transfer agreements and non-M365 channels sit outside. Partial is the defensible claim, held with High confidence. |
| 20 | ISO-5.33 Protection of records → Records Management (Direct / **Medium**) | **CORRECTED** (confidence → High) | Under-claim: RM is purpose-built for this control (record immutability, file plan, disposition proof) within M365. |
| 21 | ISO-5.34 Privacy & PII protection → "Priva (primary)" listed as capability (Partial / Medium) | **CORRECTED** | Ground-rule fix as with SDPR-F14: mapped capabilities now classification (locate PII) + DLM retention + DLP; **Priva → dependency**. Partial / Medium stands. |
| 22 | ISO-8.1 User endpoint devices → Endpoint DLP (Partial / Medium) | **CONFIRMED** | Intune/Defender primary; Endpoint DLP is the data-protection slice on endpoints. |
| 23 | ISO-8.3 Information access restriction → label-based encryption (Partial / Medium) | **CONFIRMED** | Entra/CA primary; label encryption + DLP restrictions are genuine content-layer access restriction. |
| 24 | ISO-8.10 Information deletion → retention delete + disposition (Direct / Medium) | **CONFIRMED** (scope note) | Direct within M365 estate. |
| 25 | ISO-8.11 Data masking → SIT detection, "masking itself is non-Purview" (**Partial** / Low) | **CORRECTED** (→ Evidence Support Only / Medium) | The row's own text concedes Purview performs no masking. Detection of unmasked PII in non-prod = evidence, not implementation. Confidence raised — the evidence claim itself is reliable. |
| 26 | ISO-8.12 Data leakage prevention → DLP + Endpoint DLP (Direct / High) | **CONFIRMED** | The control *is* DLP; Purview DLP directly implements it for M365, endpoints, and Edge. Network-layer egress controls noted as dependency. |
| 27 | ISO-8.15 Logging → Audit (Premium) + Activity explorer (**Direct** / High) | **CORRECTED** (→ Partial / High) | Audit is direct logging for M365 data-plane activity, but A.8.15 covers estate-wide logging (systems, network, apps) — SIEM dependency owns the rest. Scope-trimmed to Partial. |
| 28 | ISO-8.16 Monitoring activities → Activity explorer + alerts + Adaptive Protection (Partial / Medium) | **CONFIRMED** (enriched) | Insider Risk Management anomaly detection added to capability detail — it was missing from the sheet entirely. |
| 29 | ISO-8.24 Use of cryptography → label encryption (Partial / Medium) | **CONFIRMED** (enriched) | Customer Key + Double Key Encryption noted; key management/TLS/platform crypto remain dependencies. |

**ADDED (ISO/IEC 27001:2022):**

| Row | Rationale | Sources |
|-----|-----------|---------|
| **A.5.3 Segregation of duties → Information Barriers**, Partial / Low | IB restricts communication/collaboration between conflicting groups (ethical walls). Narrow but real contributor to SoD for conflict-of-interest scenarios; role-based SoD stays with Entra. Fills the Information Barriers gap (solution absent from sheet). | https://learn.microsoft.com/purview/information-barriers |
| **A.5.25 Assessment of information security events → DLP/IRM alert triage + Activity explorer + Audit**, Evidence Support Only / Medium | Alert triage queues and activity forensics supply the event-assessment detail; the decision process is organizational. | https://learn.microsoft.com/purview/audit-solutions-overview |
| **A.5.28 Collection of evidence → eDiscovery**, Partial / High | Identification, collection, preservation of evidence with defensible process (holds, collections, exports) for M365 content. eDiscovery was near-absent from the sheet as a primary capability. | https://learn.microsoft.com/purview/edisc |
| **A.5.31 Legal/regulatory/contractual requirements → Compliance Manager**, Evidence Support Only / Medium | Regulatory templates catalog applicable requirements and map them to improvement actions. | https://learn.microsoft.com/purview/compliance-manager-regulations-list |
| **A.5.36 Compliance with policies/rules/standards → Compliance Manager**, Evidence Support Only / Medium | Assessments + continuous control testing evidence adherence checking. Compliance Manager was absent from the sheet entirely. | https://learn.microsoft.com/purview/compliance-manager |
| **A.7.10 Storage media → Endpoint DLP removable-media controls**, Partial / Medium | Restrict/audit copy to removable media on onboarded devices; physical media lifecycle stays organizational. | https://learn.microsoft.com/purview/dlp-learn-about-dlp |

---

## 4. Row-by-row findings — SOC 2 (2017 TSC, 2022 points of focus)

All criteria IDs verified against the TSC PDF. Criterion intent paraphrased (AICPA copyright).

| # | Row | Claim audited | Verdict | Notes |
|---|-----|---------------|---------|-------|
| 30 | SOC2-CC6.1 logical access → label encryption contributes (Partial / Medium) | **CONFIRMED** | Entra primary; content-layer restriction is a genuine CC6.1 contributor. |
| 31 | SOC2-CC6.5 discontinue protections / dispose (Partial / Medium) | **CONFIRMED** | TSC text: discontinue protections only after data recoverability diminished — retention delete + disposition proof map to the data half. |
| 32 | SOC2-CC6.7 restrict transmission/movement/removal (Direct / High) | **CONFIRMED** (scope note) | DLP (cloud + endpoint incl. removable media) is the canonical CC6.7 technology for M365 estates; physical transport/backup media noted as dependency. |
| 33 | SOC2-CC7.2 monitor for anomalies (Partial / Medium) | **CONFIRMED** (enriched) | IRM anomaly detection + Adaptive Protection added — IRM was absent from the sheet. |
| 34 | SOC2-CC7.3 evaluate security events (Evidence Support Only / Medium) | **CONFIRMED** | |
| 35 | SOC2-CC7.4 respond to incidents (Evidence Support Only / Medium) | **CONFIRMED** | |
| 36 | SOC2-CC8.1 change management (Evidence Support Only / Medium) | **CONFIRMED** | Admin audit of policy changes = change evidence for the data-protection layer. |
| 37 | SOC2-C1.1 identify/maintain confidential info (Direct / High) | **CONFIRMED** | Canonical. |
| 38 | SOC2-C1.2 dispose of confidential info (Partial / Medium) | **CONFIRMED** | |
| 39 | SOC2-P1-3 notice/choice/collection → Not Covered (**Medium** confidence) | **CORRECTED** (confidence → High) | If the verdict is "core Purview does not address notice/consent", that verdict is held with High confidence. Kept as a deliberate boundary row spanning P1.1/P2.1/P3.1–P3.2, rationale documented. |
| 40 | SOC2-P4 "P4.1–P4.2" limit use/retention/**disposal** (Direct / Medium) | **CORRECTED + SPLIT** | **Reference error:** disposal is **P4.3**, outside the cited range. Split into three rows: **P4.1** use limitation (Partial / Low — DLP fences where personal data can flow; semantic purpose-limitation is process), **P4.2** retention (Direct / High — retention policies are the control), **P4.3** secure disposal (Direct / Medium — retention delete + disposition records). |
| 41 | SOC2-P6 "P6.1–P6.7" — "Access, correction, and disclosure to third parties (DSR)" (Partial / Medium) | **CORRECTED + SPLIT** | **Conflation:** data-subject *access* is **P5.1** and *correction* is **P5.2** — not P6. P6 covers third-party disclosure. Replaced by: **P5.1–P5.2** locate/collect for access & correction (eDiscovery + Data explorer, Partial / Medium, Priva dependency) and **P6.2–P6.3** records of authorized/unauthorized disclosures (Audit, Evidence Support Only / Medium). P6.1/P6.4/P6.5/P6.7 documented as excluded (consent + vendor-commitment + accounting processes — organizational/contractual). |
| 42 | SOC2-P8 monitoring/enforcement of privacy commitments (**Partial** / Medium) | **CORRECTED** (→ Evidence Support Only / Medium) | P8.1's operative process is complaints/dispute resolution with periodic compliance monitoring. Purview supplies the monitoring signals (Activity explorer, Audit, Communication Compliance, DLP reports); the process itself is organizational. |
| 43 | SOC2-A1 availability (A-series) (Evidence Support Only / Low) | **CORRECTED** (→ Not Covered / High) — kept coarse | "Supplementary evidence" for availability criteria would not survive auditor scrutiny — same discipline as J#47/J#48. Kept as a coarse boundary row (uniform verdict across A1.1–A1.3), ref normalized. |
| 44 | SOC2-PI1 processing integrity (PI-series) (Evidence Support Only / Low) | **CORRECTED** (→ Not Covered / High) — kept coarse | Same logic; processing integrity lives in application controls. Ref normalized to "PI1.1–PI1.5". |

**Coarse-range decision (documented):** ranges are split **where the Purview story differs across the range** (P4, P5/P6) and kept **where it is uniform** (P1–P3 boundary row, A-series, PI-series) with the rationale in each row's notes. CC-series refs were already per-criterion.

**ADDED (SOC 2):**

| Row | Rationale | Sources |
|-----|-----------|---------|
| **CC1.1 integrity & ethical values → Communication Compliance**, Evidence Support Only / Low | Conduct-violation detection (harassment/threats/sensitive info in comms) evidences enforcement of ethical standards. Fills the Communication Compliance gap beyond privacy. Low confidence flagged deliberately — auditors vary on accepting this. | https://learn.microsoft.com/purview/communication-compliance-solution-overview |
| **CC4.1 ongoing/separate evaluations → Compliance Manager**, Evidence Support Only / Medium | Continuous control assessment + assessment reports = structured evaluation evidence for the data-protection control set. | https://learn.microsoft.com/purview/compliance-manager |

---

## 5. Completeness findings — Purview solutions absent from the sheet

| Solution | Status in xlsx | Resolution |
|---|---|---|
| Insider Risk Management | Absent | Added to capability detail of monitoring rows (ISO-8.16, SOC2-CC7.2, SDPR-J40); will be a primary mapping in new frameworks (HIPAA §164.308(a)(1)(ii)(D), 800-171 3.1.x/3.14.x, GLBA monitoring, CSF DE.CM). |
| Communication Compliance | One mention (P8) | Added SOC2-CC1.1; primary mappings planned for GLBA/finance conduct rows where applicable. |
| Information Barriers | Absent | Added ISO-A.5.3; relevant to SOC 2 CC6.1 capability detail. |
| eDiscovery (as primary) | Locate-only mentions | Added ISO-A.5.28; carries the P5/F-section DSR rows. |
| Compliance Manager | Absent | Added SDPR-J33, ISO-A.5.31, ISO-A.5.36, SOC2-CC4.1. |
| Audit (as primary) | Present (8.15) | Confirmed; scope-corrected. |
| DSPM / DSPM for AI | DSPM present; DSPM for AI absent | DSPM for AI reserved for new-framework rows where AI usage is in scope (CSF 2.0, GDPR Art. 32 context) — kept out of legacy frameworks to avoid overreach. |
| Data Lifecycle Mgmt / Records Mgmt / IP / DLP / classification | Present | Confirmed with naming refresh. |

**Row count after audit (legacy frameworks):** SSPA DPR 15 (14 audited + 1 added) · ISO 27001 21 (15 + 6) · SOC 2 20 (12 surviving rows after split/merges + 6 split-derived + 2 added). Exact final counts materialize in `purview-compliance-map.json` at Phase 3.

---

## 6. Purview claim verification sources (capability side)

Verified live on Microsoft Learn 2026-07-16: sensitivity labels & encryption, SITs, trainable classifiers, Data/Content/Activity explorer, DLP + Endpoint DLP, DLM retention, Records Management & disposition, Audit Standard/Premium (180-day/1-year defaults), unified eDiscovery, Insider Risk Management + Adaptive Protection, Communication Compliance, Information Barriers, Compliance Manager (+ premium regulations list), DSPM (current + classic), DSPM for AI (classic), Customer Key. Primary URLs recorded per row in the dataset; licensing claims will come exclusively from the **Microsoft Purview service description** per-feature tables at Phase 3 (https://learn.microsoft.com/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-purview-service-description).

---

## 7. Phase 5 QA results (2026-07-16)

### 7.1 Row-count reconciliation — PASS
- Canonical JSON: **124 rows / 9 frameworks / 9 industries** (assemble.py integrity checks: unique ids, known frameworks, valid coverage/confidence/status enums, ≥1 source per row — all pass).
- Rendered HTML (headless Edge, `file://`): landing stats show **124 control mappings / 9 frameworks / 13 solutions / 15 direct-support / 0 unverified**; footer shows 124 rows; density matrix grand total **Σ = 124** with per-framework row totals 15·21·20·12·13·12·10·9·12 matching the JSON exactly, and per-solution column totals summing to 124.

### 7.2 Source-URL resolution — 39/41 PASS, 2 documented WAF blocks
All 41 distinct URLs across rows, framework metadata, and solution registry were requested with a browser user-agent:
- **39 → HTTP 200.**
- **2 → HTTP 403 to automated agents** (server-side WAF, confirmed via a second independent fetcher):
  `https://dodcio.defense.gov/cmmc/` and `https://www.hhs.gov/hipaa/for-professionals/security/index.html`.
  Both are the canonical human-facing URLs, were referenced by multiple sources retrieved this session, and open normally in a browser. Every row citing them also carries a machine-resolving official source (eCFR / csrc.nist.gov). Retained deliberately; noted here.

### 7.3 Random 10-row end-to-end re-verification — 10/10 PASS
Seeded sample (`random.seed(20260716)`, sample of 10 from 124 ids):

| Row | Control-ref check (authoritative text) | Purview claim check (Learn) | License check (service description) | Verdict |
|---|---|---|---|---|
| soc2-cc4-1 | CC4.1 verbatim in AICPA TSC PDF (COSO P16, ongoing/separate evaluations) | compliance-manager (continuous assessment) | CM section: baseline all plans; premium templates | PASS |
| iso-a-5-12 | A.5.12 under 2022 Annex A numbering (ISO catalog + Microsoft MCSB v2 cross-refs) | sensitivity-labels | Labeling section: manual E3+, automatic E5-tier | PASS |
| dpr-j50 | J#50 verbatim in DPR v12 PDF ("Anonymize all Microsoft Personal Data used in a development or test environment") | dlp-learn-about-dlp | DLP EXO/SPO/ODB: E3+ | PASS |
| soc2-cc6-5 | CC6.5 verbatim in TSC (discontinue protections after recoverability diminished) | disposition | Records Management: E5-tier | PASS |
| iso-a-8-16 | A.8.16 in 2022 numbering (MCSB v2 mapping) | insider-risk-management + adaptive protection | IRM: E5/A5/G5, Purview Suite, or IRM add-on | PASS |
| iso-a-5-9 | A.5.9 in 2022 numbering | data-classification-data-explorer | Data classification analytics: E5-tier (verbatim SD row) | PASS |
| soc2-p8-1 | P8.1 verbatim in TSC incl. the "periodically monitors compliance" clause the row leans on | activity explorer + communication compliance | Audit Std incl. broadly; CC: E5-tier | PASS |
| soc2-cc1-1 | CC1.1 verbatim in TSC ("commitment to integrity and ethical values") | communication-compliance-solution-overview | CC: E5-tier | PASS |
| glba-314-4-c6 | §314.4(c)(6) verbatim in eCFR ("no later than two years after the last date the information is used…") | retention + disposition | Retention E3+ / adaptive+records E5-tier | PASS |
| gdpr-20 | Art. 20 confirmed against EUR-Lex consolidated text | edisc (export capabilities) | eDiscovery: E3 base, premium features E5-tier | PASS |

### 7.4 Rendering & build verification — PASS
- Headless Edge (`file://`, no network): landing, industry, framework, solution, matrix, cell, and search views all render; JS passes `node --check`.
- Density matrix: angled headers, direct-labeled cells, sequential single-hue ramp (validated light + dark via the palette validator: lightness band, chroma floor, CVD separation, contrast — ALL PASS for both badge palettes).
- Print: `--print-to-pdf` produces expanded rows (`::details-content` + beforeprint fallback) — 9-page GLBA framework dossier confirmed containing full row bodies, GOV caveats, sources, and verification footers.
- Rebuild is idempotent: `python build/assemble.py && python build/build_html.py` regenerates JSON + HTML from the row modules; the HTML is never hand-edited.

**Phase 5 verdict: SHIP.** 124/124 rows `verified`; zero UNVERIFIED rows in v1.

---

## 8. Increment 1 (2026-07-17) — NIST SP 800-53 Rev 5 (subset) + FERPA promoted from backlog

**Result: 124 → 150 rows (+21 NIST 800-53, +5 FERPA), 11 frameworks, 10 industries (new "US federal & FedRAMP-adjacent" lens; FERPA added to both education lenses). All 26 new rows `verified`; zero UNVERIFIED.**

### 8.1 Currency re-verification (Phase 0)
- **NIST SP 800-53:** current release is **Rev 5, Release 5.2.0 (Aug 27, 2025)** — supersedes the Rel 5.1.1 noted in v1. Release 5.2.0 added SA-15(13), SA-24, SI-2(07) and revised SI-7(12) (secure-software focus) — none in the mapped subset. No Rev 6 announced. Sources: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final · https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls
- **FERPA:** 34 CFR Part 99 current text verified against eCFR (2026-07-15 issue, via the versioner API; base 53 FR 11943 as amended). ED's Fall 2024 Unified Agenda signaled intent to propose amendments — **no NPRM published** as of 2026-07-17; recorded as a watch item in framework metadata. Sources: https://www.ecfr.gov/current/title-34/subtitle-A/part-99 · https://studentprivacy.ed.gov/ferpa
- **Compliance Manager templates re-verified verbatim on the regulations list (fetched fresh 2026-07-17):** **"NIST 800-53 rev.5"** and **"US - Family Educational Rights and Privacy Act (FERPA)"**. Source: https://learn.microsoft.com/purview/compliance-manager-regulations-list
- **Subset scope decision** recorded in FRAMEWORK-SELECTION.md (Increment 1) before authoring: 21 rows covering 22 controls; IR-8 and RA-5 dropped from the v1 memo's anchor set after validation; AC-22, CM-12, IR-9, PS-4, SI-4, SI-12, SI-19 added; PT and PM families evaluated and excluded.

### 8.2 Per-row change log — all rows ADDED (no existing rows modified)

| Framework | Control | Solution | Coverage / Confidence | Control source · Purview source |
|---|---|---|---|---|
| 800-53 R5 | AC-3 | Information Protection | Partial / Low | csrc 800-53r5 · learn: encryption-sensitivity-labels |
| 800-53 R5 | AC-4 | Data Loss Prevention | Partial / High (xref 171 3.1.3) | csrc · learn: dlp-learn-about-dlp |
| 800-53 R5 | AC-21 | Data Loss Prevention | Partial / Medium | csrc · learn: dlp + sensitivity-labels |
| 800-53 R5 | AC-22 | Data Loss Prevention | Partial / High (xref 171 3.1.22) | csrc · learn: dlp + DSPM |
| 800-53 R5 | AU-2, AU-12 | Audit | Partial / High (xref 171 3.3.1; combined — uniform story) | csrc · learn: audit-solutions-overview |
| 800-53 R5 | AU-6 | Audit | Partial / Medium | csrc · learn: audit-search + activity explorer |
| 800-53 R5 | AU-9 | Audit | Partial / Medium (xref 171 3.3.8) | csrc · learn: audit-solutions-overview |
| 800-53 R5 | AU-11 | Audit | Partial / High | csrc · learn: audit-solutions-overview |
| 800-53 R5 | CM-12 | Data Classification | Partial / High | csrc · learn: data-explorer + DSPM |
| 800-53 R5 | IR-4 | Audit | Evidence / High (xref 171 3.6.1–3.6.2) | csrc · learn: audit + edisc |
| 800-53 R5 | IR-9 | Data Loss Prevention | Partial / High | csrc · learn: dlp + edisc + audit |
| 800-53 R5 | MP-3 | Information Protection | Partial / High (xref 171 3.8.4) | csrc · learn: sensitivity-labels |
| 800-53 R5 | MP-6 | None (boundary row) | **Not Covered / High** | csrc (content deletion ≠ media sanitization; consistent with v1 leaving 171 3.8.3 unmapped) |
| 800-53 R5 | MP-7 | Data Loss Prevention | Partial / Medium (xref 171 3.8.7) | csrc · learn: endpoint-dlp |
| 800-53 R5 | PS-4 | Insider Risk Management | Partial / Medium (xref 171 3.9.2) | csrc · learn: insider-risk-management |
| 800-53 R5 | RA-3 | Data Classification | Evidence / Medium | csrc · learn: data-explorer + DSPM |
| 800-53 R5 | SC-8 | Information Protection | Partial / Medium (xref 171 3.13.8) | csrc · learn: encryption-sensitivity-labels + dlp |
| 800-53 R5 | SC-28 | Information Protection | Partial / High (xref 171 3.13.16) | csrc · learn: encryption + customer-key |
| 800-53 R5 | SI-4 | Insider Risk Management | Partial / Low (xref 171 3.14.7) | csrc · learn: irm + activity explorer |
| 800-53 R5 | SI-12 | Data Lifecycle Management | **Direct / High** | csrc · learn: retention + records-management |
| 800-53 R5 | SI-19 | Data Classification | Evidence / Medium | csrc · learn: SIT definitions + data-explorer |
| FERPA | §99.10 | eDiscovery | Partial / Medium | eCFR part 99 · learn: edisc |
| FERPA | §99.31(a)(1)(ii) | Information Protection | Partial / Medium | eCFR · learn: encryption + dlp |
| FERPA | §99.30 & §99.33 | Data Loss Prevention | Partial / Low | eCFR · learn: dlp |
| FERPA | §99.32 | Audit | Evidence / Medium | eCFR · learn: audit + retention |
| FERPA | §99.31(a)(6)(iii)(C) & §99.35(b)(2) | Data Lifecycle Management | Partial / Medium | eCFR · learn: retention + disposition |

Coverage mix of the increment: 20 Partial, 4 Evidence, 1 Direct (SI-12 — consistent with the GLBA §314.4(c)(6)/GDPR Art. 5(1)(e) retention ratings), 1 Not Covered boundary. Every 800-53 mapped row carries a verified GCC/GCC High/DoD note (MP-6 boundary row legitimately has none); FERPA rows carry none (no known government-cloud caveat for the mapped features in education tenants).

### 8.3 Increment QA
- **URL resolution:** all **5 new distinct URLs → HTTP 200** (both csrc.nist.gov pages, eCFR part-99, studentprivacy.ed.gov, learn audit-search). No WAF blocks in this increment; the two v1 blocks (hhs.gov, dodcio) are untouched.
- **Sample re-verification:** **all 5 FERPA rows** + **5 seeded 800-53 rows** (`random.seed(20260717)`: MP-3, IR-4, AU-6, SC-8, AU-9) re-checked end-to-end against the local authoritative texts (official NIST PDF; eCFR XML) — **10/10 REF OK**; capability and license claims re-checked against the same Learn/service-description sources as v1.
- **Row-count reconciliation:** JSON 150 = landing stat 150 = footer 150 = matrix Σ 150; new matrix rows total 21 (800-53) and 5 (FERPA); per-solution column totals sum to 150. Cell click-through hrefs present for both new frameworks.
- **No-regression:** all nine v1 frameworks unchanged (15·21·20·12·13·12·10·9·12 = 124); v1 row ids untouched; spot-render of existing views unchanged.
- **Views:** industry lens (new "US federal & FedRAMP-adjacent" card; FERPA on both education cards), framework view (9 domains for 800-53 incl. Release 5.2.0 callout; 5 FERPA rows with the 45-day language), Purview pivot (SI-12 and FERPA destruction row surface under Data Lifecycle Management; spillage under DLP), density matrix — all verified in headless rendering, light theme screenshots taken.

**Increment 1 verdict: SHIP.** Total 150/150 rows `verified`.

---

## 9. Platform generalization — resumed and completed (2026-07-17)

Single-product → multi-product platform refactor. **Zero content changes:** the only permitted data restructuring
was the dependency-field split (Phase 2). Proven below by a field-level diff against the pre-generalization baseline
snapshot (`reference/baseline-pre-refactor.json`, 150 rows).

### 9.1 Where the prior run stopped (verified from disk, not assumed)
The prior session terminated (billing/model error) **immediately after writing the generalized `build/template.html`**,
before regenerating the HTML or updating docs. Confirmed by file state: `template.html` was the newest artifact;
`build/build_html.py` still pointed at the old `purview-compliance-map.*` names; no `compliance-atlas.html` existed;
both the old and new canonical JSONs were present.

Phase status found on resume:

| Phase | Found | Action taken this run |
|---|---|---|
| 1 — Data model | ✅ DONE | Verified only. products map (purview) + related_products (6 slugs); all 150 rows `product: purview`; `licensing_model` on all (142 `per_user`, 8 `n/a`); JSON renamed in `assemble.py`. |
| 2 — Dependency migration | ✅ DONE & CLEAN | Verified only (not re-run destructively). 150/150 rows carry `related_microsoft` / `external_dependencies` / `legacy_dependencies`; 0 retain old free-text; 0 empty legacy. |
| 3 — UI generalization | ⚠️ template only | `template.html` generalized but never built. **Completed** by building + rendering QA. |
| 4 — Build + docs | ⚠️ PARTIAL | **Completed:** fixed `build_html.py` → `compliance-atlas.{json,html}`; regenerated HTML; removed lingering old files; rewrote README (rename note, new-field schema table, add-a-product procedure). |
| 5 — Regression QA | ❌ NOT DONE | **Completed** — full gate below. |

### 9.2 Idempotency / double-migration guard (the highest-risk item)
The build regenerates the JSON from the row modules every run; the dependency migration is a **pure transform applied
at assemble time** (`dependency_migration.migrate_row`), not an in-place mutation of a persisted JSON. Verified:
re-running `assemble.py` produces **byte-identical output** (excluding the `meta.generated` timestamp), per-row
dependency structures identical, and **no double-parse symptom** (no related entry duplicated; no legacy segment
duplicated). The row modules still carry only the free-text `non_purview_dependencies` (source of truth intact); none
carry structured fields. `migrate_row` also guards: it skips any row already structured. **Double-migration is
structurally impossible here.**

### 9.3 Zero-content-change proof
Field-level diff, atlas vs. baseline, over all 18 protected fields (framework, control_ref, control_intent,
purview_solution, capability_detail, how_it_supports, both evidence fields, coverage, confidence, license_requirement,
cloud_availability_note, sources, also_involves, status, last_verified, framework_version, control_domain):
**id sets identical; 0 diffs.** The only row-level changes are the intended ones: `product` normalized `Purview`→`purview`
(slug), and `non_purview_dependencies` split into the three structured fields (original preserved verbatim in
`legacy_dependencies`).

### 9.4 Dependency-migration stats
- **150/150 rows migrated**; `legacy_dependencies` populated on every row (0 empty).
- **44 rows** carry `related_microsoft` entries; **53 entries** total — by product: Entra 14, Defender XDR 12,
  Priva 11, Sentinel 9, Intune 7; by role: 47 contributing, 6 primary.
- **27 rows** have platform-token external segments **flagged** in `reference/dependency-migration-log.json` and
  deliberately left in `external_dependencies` (Microsoft-adjacent but not one of the five parsed product families —
  e.g., "M365 service encryption (inherited)", "Azure Key Vault key ceremony for Customer Key",
  "SPO/Teams external-sharing settings", BitLocker, non-M365 stores). Never guessed into a product assignment.
- **Zero information loss** confirmed by reconstruction: every `;`-segment of each original string appears verbatim in
  either `external_dependencies` or a `related_microsoft` note (10-row sample audited + related-heavy spot-checks:
  dpr-j36, iso-a-8-16, 53-si-4, soc2-cc7-2, csf-de-cm-03 — all zero-loss, correct primary/contributing roles).

### 9.5 Regression QA results
- **Row count:** baseline **150** = JSON 150 = landing stat 150 = footer 150 = density-matrix grand Σ 150
  (per-framework Σ 15·21·20·12·13·21·12·10·9·5·12 = 150) = per-product column 150 = print output. **Match.**
- **Spot-check** (10 rows, seeded, across soc-2, hipaa-security, soc-2, iso-27001-2022, sspa-dpr, ferpa, nist-800-171):
  rendered substance (capability_detail, how_it_supports, coverage/confidence badges, sources) **identical to baseline**;
  all present verbatim in the built HTML. (One initial "fail" was a test-harness artifact — the checker HTML-escaped an
  apostrophe that the JSON data island stores raw; re-checked with raw matching → 10/10 pass.)
- **Four views** (Industries, Frameworks, Product Pivot, Density Matrix) render in **light and dark**; Product Pivot
  lands directly on Microsoft Purview via the generalized single-product path; Framework view renders control-grouped,
  product-stacked mapping cards (ready to stack a second product under one control); Density Matrix renders
  frameworks × products at top level with the frameworks × solutions drill-through beneath.
- **Product-aware search:** `entra` returns 15 rows (matching `related_microsoft` notes + text) — the product dimension
  is indexed.
- **Print:** the FERPA dossier prints fully expanded (7 pages) with the new dependency sections, related-products block,
  and the persistent legal footer.
- **Rename cleanup:** old `purview-compliance-map.json` and `purview-compliance-map.html` **removed**; only
  `compliance-atlas.json` / `compliance-atlas.html` remain. No active code path references the old names (two
  remaining mentions are rename-documentation comments). **No rename collision** (the new files were built and verified
  before the old ones were deleted).

### 9.6 Content errors observed but deliberately NOT fixed
- **None in the row content** — the atlas is byte-identical to baseline on all protected fields.
- **One future-refinement note (not a content error):** the dependency parser buckets every "Defender" mention to the
  single `defender-xdr` family slug. All current mentions are genuine Defender XDR workloads — Defender for Endpoint
  (MDE), Defender for Cloud Apps (MDA), and "Defender XDR/generic" — and **no** "Defender for Cloud" (the separate CSPM
  product, slug `defender-cloud`) is mis-bucketed (confirmed: zero occurrences). The verbatim segment is preserved in
  each entry's `note`, so nothing is lost. When Defender products gain their own rows, revisit whether MDA/MDE warrant
  finer per-workload attribution than the family slug. Logged here for that future product pass.

**Platform generalization verdict: COMPLETE.** Baseline 150 = final 150. One canonical JSON. Zero content changes;
dependency split clean and lossless; four views generalized and verified in both themes.

---

## 10. Generalization integrity audit (2026-07-17, pre-Entra verification pass)

Verification-and-cleanup pass on the multi-product generalization output, before any Entra authoring. Worked from
the source modules (`build/rows_*.py`), the assembled `compliance-atlas.json`, `reference/dependency-migration-log.json`,
`reference/baseline-pre-refactor.json`, and the built HTML DOM.

**Outcome: zero defects found. No fixes applied, no rows repaired, no slugs corrected.** The "empty or partially
populated" concern resolved to legitimate state-(a) empty arrays (rows whose dependencies are purely external/process).

| # | Check | Result |
|---|---|---|
| 1 | Empty vs. malformed `related_microsoft` | **DONE — 0 defects.** (a) `[]` legitimately empty: **106**; (b) non-empty well-formed: **44**; (c) malformed: **0**. Deeper dropped-entry test: every empty-array row's `legacy_dependencies` genuinely contains no product token; inverse test: every product token in every legacy string produced a matching entry. |
| 2 | Role completeness | **DONE — 0 defects.** True distribution across 53 entries: **6 primary / 47 contributing / 0 missing-or-blank**. Reconciles exactly (6+47=53). The "4 contributing / 6 primary (=10)" in the concern was a **mis-transcription of "47 contributing"** (§9.4 already recorded 47/6) — not a data problem. |
| 3 | Product-slug validity | **DONE — 0 defects.** Slugs used: entra 14, defender-xdr 12, priva 11, sentinel 9, intune 7. All resolve in `common.py`; all ⊆ intended set {entra, intune, defender-xdr, defender-cloud, sentinel, priva, purview}. `defender-cloud` is defined but not yet used (forward-looking). No typos/retired slugs. |
| 4 | Migration faithfulness (15 fresh rows) | **DONE — 0 defects.** Sample (seed 4242, disjoint from the resume-QA 15): pci-4-2-2, soc2-cc1-1, dpr-j35, csf-rs-an-03, csf-de-cm-03-ai, 53-ir-4, 171-3-13-8, soc2-p5, gdpr-32-1-a, gdpr-15, dpr-j33, ferpa-99-30-33, soc2-cc8-1, soc2-cc7-4, ferpa-99-32. Every legacy segment accounted exactly once (external XOR ≥1 related note); zero loss, zero duplication, no double-migration. Also verified: current JSON dep-structures == fresh `assemble.py` rebuild, byte-for-byte. |
| 5 | Defender bucketing (§9.6 follow-through) | **DONE — worklist below.** 12 `defender-xdr` entries; **0 to re-bucket to `defender-cloud`** (none reference CSPM/CWPP/Azure resource posture); 3 flagged to verify at the Defender session. |
| 6 | Disclaimer footer renders | **DONE — confirmed in DOM.** All five required phrases render (extracted from headless DOM, not just source). Exact strings quoted below. |

### 10.1 Defender-for-Cloud re-bucket worklist (ready-to-action for the Defender for Cloud session)
All 12 entries currently carry `product: defender-xdr`, `role: contributing`. **Do not re-bucket now — `defender-cloud`
is not yet a product in the atlas.** When the Defender session lands, re-evaluate each note against the then-authored
Defender product boundaries. Current classification (from note text):

| Row | control_ref | Note (verbatim) | Classification | Action |
|---|---|---|---|---|
| iso-a-7-10 | A.7.10 | device control (Defender for Endpoint) | MDE → Defender XDR workload | STAY |
| iso-a-8-1 | A.8.1 | Defender for Endpoint | MDE → Defender XDR workload | STAY |
| iso-a-8-12 | A.8.12 | Defender for Cloud Apps for unsanctioned SaaS | MDCA → Defender XDR workload | STAY |
| iso-a-8-16 | A.8.16 | Sentinel/Defender XDR for network and system monitoring | Defender XDR (generic) | STAY |
| soc2-cc7-2 | CC7.2 | Sentinel/Defender XDR (infrastructure anomalies) | Defender XDR (generic) | STAY |
| 171-3-14-7 | 3.14.7 | Defender XDR/Sentinel for system-level detection | Defender XDR (generic) | STAY |
| 53-si-4 | SI-4 | Defender XDR/Sentinel (attack detection, network monitoring) | Defender XDR (generic) | STAY |
| csf-rs-an-03 | RS.AN-03 | Defender XDR/Sentinel forensics | Defender XDR (generic) | STAY |
| csf-de-cm-03-ai | DE.CM-03 | network AI-app discovery (Defender for Cloud Apps) | MDCA → Defender XDR workload | STAY |
| dpr-j40 | J #40 | IDS/IPS and network monitoring (Defender/SIEM) | Generic "Defender" family | **VERIFY** at Defender session (IDS/IPS could touch Defender for Servers/Cloud) |
| 171-3-8-7 | 3.8.7 | Intune/Defender device control (port-level) | Endpoint device control (MDE + Intune) | **VERIFY** (likely Intune-primary + MDE) |
| 53-mp-7 | MP-7 | Intune/Defender device control (port/device-class level) | Endpoint device control (MDE + Intune) | **VERIFY** (likely Intune-primary + MDE) |

**Summary: 0 confirmed re-buckets; 3 to verify (dpr-j40, 171-3-8-7, 53-mp-7).** Confirms §9.6: all current Defender
mentions are Defender XDR workloads (MDE/MDCA/XDR), no Defender-for-Cloud CSPM mentions. The three "verify" rows note
generic device-control/IDS-IPS that may want finer Intune/Defender-family attribution once those products exist — the
verbatim note preserves the full text, so no information is at risk.

### 10.2 Rendered footer (exact strings, extracted from the built HTML DOM)
Legal footer (`<ul id="footLegal">`):
1. "Informational reference only — not legal, audit, or compliance advice."
2. "Independent community project. Not affiliated with, sponsored, or endorsed by Microsoft Corporation."
3. "Framework and standard names are the property of their respective owners and are used for identification only."
4. "Currency is governed by each row's last-verified date; product capabilities and licensing change frequently — verify at engagement time."

Disclaimer (`<div id="footDisc">`): "Mapped products support or evidence controls; they do not by themselves make an
organization compliant with any framework. Control references are practical intent mappings in original words, not
quotations of the standards. Licensing claims derive from each product's authoritative licensing source and can change;
verify at engagement time."

### 10.3 Post-audit reconciliation
No fixes were required, so content is unchanged. Final clean rebuild: **150 rows = baseline 150; id sets identical;
0 protected-content-field diffs; 53 related_microsoft entries across 44 rows.** JSON and HTML rebuilt in lockstep.

**Audit verdict: generalization output is structurally sound. Clear to proceed to Entra authoring in a later session.**

---

## 11. Entra product addition (2026-07-17)

Second product added to the multi-product atlas — the worked reference for Intune/Defender/Sentinel/Defender-for-Cloud.
**48 Entra rows across all 11 frameworks; new atlas total 150 → 198.** Purview unchanged (150, zero content drift).

### 11.1 Product registration & the Permissions Management gate
- Registered `entra` in `PRODUCTS` (official name **Microsoft Entra**; directory **Microsoft Entra ID**, "Azure AD" retired). Moved `entra` out of `RELATED_PRODUCTS`.
- 4 Entra solutions registered in the shared `SOLUTIONS` map (product-tagged; per-product lists derived): **Conditional Access & Authentication** (Entra ID core: CA, MFA/auth methods & strengths, RBAC, SSPR, sign-in/audit logs), **Entra ID Protection**, **Privileged Identity Management**, **Entra ID Governance**.
- Licensing verified against the **Entra** licensing service description (not Purview's): CA = P1; MFA = Free/P1; ID Protection & PIM = **P2**; access reviews/entitlement management baseline = **P2**; **Lifecycle Workflows = Entra ID Governance SKU**. Government-cloud availability verified (CA/MFA/ID Protection/PIM/ID Governance all available in GCC/GCC High/DoD).
- **Permissions Management gate — DECISION: NOT MAPPED.** Microsoft Entra Permissions Management (CIEM) reached end-of-sale 2025-04-01 and was **retired/support-discontinued 2025-10-01** (verified: Entra what's-new archive; `aka.ms/MEPMretire`). No forward-looking mappings created; recorded here as a historical note. (Residual CIEM logic moved into Defender for Cloud — a future Defender-for-Cloud concern.)

### 11.2 Rows added — per framework & coverage
| Framework | Entra rows | Control refs |
|---|---|---|
| SSPA DPR | 2 | J #36, J #45 |
| ISO/IEC 27001:2022 | 9 | A.5.3, A.5.15, A.5.16, A.5.17, A.5.18, A.8.2, A.8.3, A.8.5, A.8.16 |
| SOC 2 | 5 | CC6.1, CC6.2, CC6.3, CC6.6, CC7.2 |
| HIPAA Security Rule | 5 | §164.308(a)(3), (a)(4), (a)(5)(ii)(C)–(D), §164.312(a)(1), (d) |
| NIST 800-171 R2 / CMMC L2 | 6 | 3.1.1, 3.1.2, 3.1.5, 3.1.7, 3.1.11, 3.5.3 |
| NIST 800-53 R5 | 6 | AC-2, AC-3, AC-6, AC-7, IA-2, IA-5 |
| NIST CSF 2.0 | 5 | PR.AA-01, PR.AA-02, PR.AA-03, PR.AA-05, DE.CM-03 |
| PCI DSS v4.0.1 | 4 | 7.2.1, 8.2.1, 8.3.1, 8.4.2 |
| GLBA Safeguards | 3 | §314.4(c)(1), (c)(5), (c)(8) |
| FERPA | 1 | §99.31(a)(1)(ii) |
| EU GDPR | 2 | Art. 32(1)(b), Art. 25 |

**Coverage:** 29 Direct Support · 19 Partial Support · 0 Evidence · 0 Not Covered.
**Confidence:** 39 High · 9 Medium.
**By solution:** Conditional Access & Authentication 26 · Entra ID Governance 14 · PIM 4 · Entra ID Protection 4.

The Direct skew is expected and defensible — Entra is the *primary enforcer* for identity/authentication/access-control/privileged-access/access-review controls. Inflation was resisted: identity-*monitoring* rows (A.8.16, CC7.2, DE.CM-03, §314.4(c)(8)) are Partial; PCI rows are Partial (CDE may authenticate via a separate IdP); HIPAA administrative-safeguard and boundary rows are Partial; the term "satisfies/compliant" appears nowhere. All 29 Direct rows are core AC/IA/PAM/governance controls where Entra directly implements the control activity.

### 11.3 Phase 3 — seam reconciliation (result: clean)
14 existing Purview rows reference `entra` in `related_microsoft` (6 primary, 8 contributing). **All 6 primary references now have a matching Entra row** (dpr-j36, iso-a-5-3, iso-a-8-3, soc2-cc6-1, 53-ac-3, glba-314-4-c1) → the framework view stacks both products under each. **0 latent inconsistencies.** 3 of 8 contributing references also gained matching Entra rows (hipaa-308-a4, pci-7-2-1, ferpa-99-31-a1ii); the other 5 (iso-a-5-14, 171-3-3-2, 171-3-9-2, 53-ac-21, 53-ps-4) remain contributing-only by deliberate curation — Entra plays a supporting role there (e.g., leaver deprovisioning under a Purview/IRM-primary control) already captured in the cross-link. No `related_microsoft` references were deleted. Entra rows carry reverse cross-links (16 → Purview) plus Intune/Defender/Sentinel contributing links where genuine.

### 11.4 Phase 5 — QA results
- **Purview no-regression:** 150 rows before = 150 after; **0 protected-content-field diffs** vs. `reference/baseline-pre-refactor.json`.
- **Reconciliation:** JSON 198 = landing/footer 198 = density Σ 198 (per-framework 17·30·25·17·19·27·17·14·12·6·14); Entra column + drill-through populated; Product Pivot shows 2 products.
- **New source URLs:** all **14 distinct `learn.microsoft.com/entra` URLs resolve 200** (incl. the higher-risk `what-are-lifecycle-workflows`, `entitlement-management-access-package-incompatible`, `concept-authentication-strengths`). No WAF blocks this increment. Framework-source URLs unchanged (iso.org still cited as canonical, as for Purview ISO rows).
- **Direct-Support re-verification:** all 29 Direct rows confirmed as primary-enforcer AC/IA/PAM/governance controls; refs verified against local framework sources (HIPAA/eCFR, 800-53, 800-171, TSC) and Microsoft MCSB cross-mappings (ISO A.5.15–5.18/A.8.2/A.8.5, CSF PR.AA-*).
- **Licensing re-verification (P2/Governance-gated = highest error risk):** PIM & ID Protection rows = P2; access-reviews/entitlement-management rows = P2 baseline; **Lifecycle Workflows rows (A.5.16, PR.AA-01) = Entra ID Governance SKU** (not P2); CA/MFA rows = P1. All correct per the Entra licensing service description.
- **Rendering:** multi-product stacking verified (SOC 2 CC6.1 = Purview Partial/Medium + Entra Direct/High stacked; 800-171 in dark theme shows Entra cards) in light **and** dark; product-aware search returns Entra results (35 for "conditional access", 63 for "entra"); print dossier expands fully with Entra rows, related-products blocks, and the legal footer.

### 11.5 Add-a-product template corrections (applied to README §"Add a product")
Executing the procedure for real surfaced gaps, now fixed in the README so the next four products inherit a clean template:
1. **Structured authoring for products #2+** was undocumented. New-product rows must use the new `prow`/`rel` helpers in `common.py` (explicit `related_microsoft` + `external_dependencies`, `legacy_dependencies=""`) — **not** the free-text `non_purview_dependencies` field, whose one-time migration only recognises 5 product tokens and would misparse (e.g., it has no "Purview" token). Documented.
2. **Solution registration** clarified from the vague "extend SOLUTIONS or add a registry" to the actual clean pattern: put every product's solutions in the shared `SOLUTIONS` map **tagged with `product`**, then derive `PRODUCTS[pid]["solutions"]` by filter (keeps the JSON `solutions` map complete for rendering while preserving per-product pivot isolation).
3. **`related_microsoft` self-reference rule** added: a row's cross-links reference *other* products only; same-product secondary solutions go in `also_involves`. (Caught and fixed one instance — soc2-cc6-6 initially self-referenced Entra ID Protection.)
4. **Process note:** appending large row blocks via shell heredoc is fragile (quote parsing) — Write the fragment to a temp file and `cat`-append, then syntax-check. Not a README item; recorded for the workflow.

**Entra addition verdict: SHIP.** 198/198 rows verified; Purview untouched; seam clean; all four views multi-product.


## 12. Intune product addition (2026-07-17)

Third product added to the multi-product atlas — the first clone of the add-a-product template that Entra (§11) established.
**41 Intune rows across 10 of 11 frameworks (FERPA deliberately skipped); new atlas total 198 → 239.** Purview (150) and Entra (48) unchanged, zero content drift.

### 12.1 Product registration & scope decisions
- Registered `intune` in `PRODUCTS` (official name **Microsoft Intune** — the "Microsoft Endpoint Manager" umbrella branding is retired; Configuration Manager is a separate product). Moved `intune` out of `RELATED_PRODUCTS`. **Note for future products: the Intune docs migrated off `learn.microsoft.com/mem/intune/*` to `learn.microsoft.com/intune/*`** with a restructure into areas (`device-security/`, `device-configuration/`, `app-management/`, `device-enrollment/`, `device-management/`, `device-updates/`, `epm/`) — all 34 cited URLs use the new structure and resolve 200.
- 5 Intune solutions registered in the shared `SOLUTIONS` map (product-tagged; per-product list derived): **Device Compliance** (the signal Entra Conditional Access consumes), **Device Configuration & Baselines**, **Endpoint Security** (AV, disk encryption, firewall, ASR, App Control, LAPS, EDR onboarding, EPM), **App Protection & Management** (MAM), **Enrollment & Device Lifecycle**.
- **Licensing verified against the Intune licensing article + advanced-capabilities article (NOT the Purview/Entra sources).** Plans: Intune Plan 1 (base) / Plan 2 / Microsoft Intune Suite, plus separately gated add-ons (EPM, Advanced Analytics, Remote Help, Cloud PKI, Enterprise App Management). **A licensing restructure is landing exactly now (July 2026): Suite capabilities distribute across Microsoft 365 tiers — E3 gets Plan 2 + Remote Help + Advanced Analytics; E5/E7 add EPM, Cloud PKI, EAM; other plans buy Suite separately.** Core-capability rows use Plan 1 strings; compliance-signal rows note that Conditional Access enforcement additionally requires Entra ID P1; the EPM row (53-ac-6-intune) carries the add-on/Suite/E5-E7 string. Flagged as a maintenance trigger (README).
- **Government-cloud verification (Intune GCC High/DoD service description):** core MDM (compliance/configuration/app policies) and endpoint security policies (incl. Defender security settings management) available in GCC High/DoD; **Windows Autopilot NOT available in GCC High/DoD** (Autopilot device preparation partially available — user-driven only); **Windows Autopatch and Windows feature/quality/expedite/driver update policies not yet available** (planned); Windows Device Health Attestation not yet available; EPM/Advanced Analytics/EAM/Tunnel-for-MAM/FOTA/specialty devices supported; Cloud PKI (GCC High) and Remote Help planned/not available. Encoded as `INTUNE_GOV` notes; every 800-171/CMMC and 800-53 Intune row carries one.
- **ConfigMgr/SCCM scope — DECISION: NOT A SEPARATE ATLAS PRODUCT.** The atlas is cloud-forward; co-management is noted inside relevant Intune rows only (the ISO A.8.9 row's external dependencies note that some configuration workloads may remain with Configuration Manager in co-managed estates). Recorded in the product notes.
- **Endpoint DLP boundary reaffirmed:** Endpoint DLP remains Purview and is not mapped on Intune rows; the Intune media-protection rows (3.8.7, MP-7) claim only the port/device-class layer and cross-link Purview for the content-aware layer.

### 12.2 Rows added — per framework & coverage
| Framework | Intune rows | Control refs |
|---|---|---|
| SSPA DPR | 2 | J #35, J #48 |
| ISO/IEC 27001:2022 | 6 | A.5.9, A.6.7, A.8.1, A.8.7, A.8.9, A.8.24 |
| SOC 2 | 3 | CC6.1, CC6.7, CC6.8 |
| HIPAA Security Rule | 4 | §164.308(a)(5)(ii)(B), §164.310(b)–(c), §164.310(d)(1)+(d)(2)(iii), §164.312(a)(2)(iv) |
| NIST 800-171 R2 / CMMC L2 | 7 | 3.1.1, 3.1.18, 3.1.19, 3.4.1, 3.4.2, 3.8.7, 3.13.16 |
| NIST 800-53 R5 | 6 | AC-6, AC-19, CM-2, CM-6, MP-7, SC-28 |
| NIST CSF 2.0 | 5 | ID.AM-01, PR.PS-01, PR.PS-02, PR.PS-05, PR.DS-01 |
| PCI DSS v4.0.1 | 4 | 1.5.1, 2.2.1, 5.3.1+5.3.5, 6.3.3 |
| GLBA Safeguards | 2 | §314.4(c)(2), §314.4(c)(3) |
| FERPA | 0 | deliberate skip (below) |
| EU GDPR | 2 | Art. 32(1)(a), Art. 32(1)(b) |

**Coverage:** 10 Direct Support · 31 Partial Support · 0 Evidence · 0 Not Covered.
**Confidence:** 28 High · 13 Medium.
**By solution:** Endpoint Security 18 · Device Configuration & Baselines 11 · Device Compliance 6 · Enrollment & Device Lifecycle 5 · App Protection & Management 1 (primary; MAM appears as also_involves on 11 rows).

Coverage discipline notes:
- **Direct only where the control's namesake activity is device configuration/connection control** (DPR J #48 full-disk encryption on devices; ISO A.8.1 user endpoint devices; A.8.9 + 3.4.2 + CM-6 + PR.PS-01 configuration enforcement; 3.1.18 + AC-19 mobile-device connection control; 3.1.19 encrypt-CUI-on-mobile — the control itself is device-scoped; PCI 1.5.1 host controls on dual-connected devices).
- **Encryption-at-rest rows held at Partial** where the control's scope exceeds managed endpoints (HIPAA §164.312(a)(2)(iv), 3.13.16, SC-28, PR.DS-01, GLBA (c)(3), GDPR 32(1)(a)) — the known atlas boundary trap. Every encryption row's `how_it_supports` states that Intune **enforces and attests** platform encryption while **the OS performs it** (BitLocker/FileVault).
- Anti-malware rows (A.8.7, CC6.8, §164.308(a)(5)(ii)(B), PCI 5.3.x) are Partial with `related_microsoft` naming Defender as the engine (`defender-xdr`, role primary) — Intune claims only the policy-management layer, never Defender's detection capability.
- **FERPA — DECISION: NO INTUNE ROWS.** §99.31(a)(1)(ii)'s "reasonable methods"/direct-control requirement is about scoping which school officials access which education records — an access-control story (Entra) with a data story (Purview). Generic device management does not implement the record-scoping the control asks for; forcing a row would be exactly the sprawl the curation rule prohibits. Density matrix renders the empty cell honestly.

### 12.3 Phase 3 — seam reconciliation (result: clean)
Pre-addition, 8 rows referenced `intune` in `related_microsoft` (the 7 found by the pre-Entra audit §10 + 1 added by the Entra session), **all role=contributing, none primary**. All 8 now have a genuine Intune row under the same control: dpr-j35, dpr-j48 (the Purview disk-encryption boundary row that pointed at "BitLocker/FileVault via Intune (primary)" in free text — now stacked with an Intune Direct row), iso-a-8-1, 171-3-8-7, 171-3-13-16, 171-3-1-1-entra, 53-mp-7, 53-sc-28. No cross-links deleted.
- **The Entra↔Intune device-compliance seam is now a mirror pair:** 171-3-1-1-entra (CA consumes the signal; rel→intune contributing) stacks with 171-3-1-1-intune (produces the signal; rel→entra primary). Same pattern on soc2-cc6-1 (three-product stack: Purview Partial + Entra Direct + Intune Partial under CC6.1).
- Two Entra rows mention device conditions descriptively without a cross-link (soc2-cc6-6-entra "Conditional Access conditions (device compliance, location, risk)"; iso-a-5-15-entra "device… conditions"): reviewed — capability descriptions of CA's condition set, not primary Intune dependencies; no Intune rows warranted on those controls. Deliberate.
- Intune rows carry reverse cross-links where genuine: 14 → purview, 8 → entra, 10 → defender-xdr (forward links to a not-yet-authored product, per the established pattern — revisit when Defender XDR lands).

### 12.4 Phase 5 — QA results
- **No-regression:** Purview 150 before = 150 after with **0 protected-content-field diffs** vs `reference/baseline-pre-refactor.json`; Entra 48 rows with per-framework distribution, coverage (29 Direct/19 Partial), and confidence (39 High/9 Medium) all matching §11.2 exactly.
- **Reconciliation:** JSON 239 = landing/footer 239 = density Σ 239 (per-framework 19·36·28·21·26·33·22·18·14·6·16); Intune column populated in the density matrix; Product Pivot shows 3 products with the Intune page listing 41 mappings, all 5 solutions, and the 8 referenced-by rows.
- **Source verification:** every row authored against the Learn pages fetched live this session (licensing, gov service description, compliance/CA integration, endpoint security, disk encryption, APP/MAM, enrollment, update rings, EPM). Framework refs verified against local official sources: 800-171 (3.1.1/3.1.18/3.1.19/3.4.1/3.4.2 exact text incl. the 3.1.19 full-device-vs-container discussion and the NIST 3.1.18→AC-19 mapping table), 800-53 (AC-19 incl. AC-19(5), CM-2, CM-6), CSF 2.0 (ID.AM-01, PR.PS-01/02/05, PR.DS-01), HIPAA (§164.310(b)/(c)/(d) + accountability spec from eCFR text), TSC (CC6.8), PCI numbering via the Azure Policy initiative page + Microsoft PCI guidance pages (1.5.1, 2.2.1, 5.3.1/5.3.5 exact text, 6.3.3).
- **Direct-Support re-verification (10 rows, highest overclaim risk):** each confirmed as a device-configuration/connection/encryption-enforcement control where Intune is the enforcement mechanism, with OS-performs-encryption wording on J #48 and 3.1.19. No Direct claim rests on Defender-owned detection or Purview-owned data controls.
- **Licensing re-verification (add-on gating = highest error risk):** the single Intune-Suite-add-on value (EPM on 53-ac-6-intune) matches the endpoint-security-policies article ("standalone add-on or as part of the Microsoft Intune Suite") plus the July 2026 E5/E7 distribution; p1_ca rows correctly state the Entra ID P1 dependency for CA enforcement (per the device-based CA requirements page); no Intune row borrows a Purview or Entra license string.
- **URL resolution: 34/34 distinct new URLs return 200** (all `learn.microsoft.com/intune/*` and `/windows/deployment/windows-autopatch/*` plus the PCI initiative page). Zero WAF blocks this increment.
- **Rendering:** all four views verified in light **and** dark via headless-browser captures — landing (3 products · 239 mappings · 55 Direct claims · 0 unverified; updated healthcare/DIB industry notes), SOC 2 framework view with the **CC6.1 three-product stack** (Purview + Entra + Intune cards) plus CC6.7/CC6.8 Intune cards, Product Pivot (Intune page), Density Matrix (Intune column, FERPA cell empty). Print-to-PDF smoke test on the 800-171 view produced a fully expanded dossier.

### 12.5 Add-a-product template verdict — HELD, with 3 small corrections
The Entra-corrected procedure (README §"Add a product") executed as a clean clone: structured `prow`/`rel` authoring, product-tagged SOLUTIONS with derived lists, per-module append blocks, per-product `_LIC`/`_URLS`/`_GOV`, RELATED_PRODUCTS graduation, and the seam-reconciliation step all worked without rework. Corrections applied for the next three products:
1. **README header/Contents staleness:** the Contents table and row-count line still showed pre-Entra numbers (150/2-product era) — the Entra session updated the procedure but not the shipping-state text. Both now updated to 239/3 products; future sessions should treat "update README state text" as an explicit final step.
2. **Row-schema note staleness:** the schema table's `product` row still said *"today always purview"* — fixed to reference the product registry.
3. **New template step — extend framework-level metadata when a product adds control families:** `FRAMEWORK["domains"]` and scoping notes are framework-level and were written from Purview's map (the PCI domains list lacked Req 1/2/5/6 for Intune *and* Req 8 from the Entra session; the 800-53 notes described a "21-control data-protection subset" that product additions now extend). Both fixed; added to the README procedure.

**Intune addition verdict: SHIP.** 239/239 rows verified; Purview and Entra untouched; seams reconciled bidirectionally; all four views three-product.


## 13. Defender XDR product addition (2026-07-17)

Fourth product added to the multi-product atlas — the second clone of the add-a-product template (Entra §11 established, Intune §12 first-cloned).
**53 Defender XDR rows across 10 of 11 frameworks (FERPA deliberately skipped); new atlas total 239 → 292.** Purview (150), Entra (48), and Intune (41) unchanged, zero content drift.

### 13.1 Product registration & scope decisions
- Registered `defender-xdr` in `PRODUCTS` (official name **Microsoft Defender XDR** — lineage Microsoft Threat Protection → Microsoft 365 Defender → Microsoft Defender XDR, verified on the XDR overview page). Moved `defender-xdr` out of `RELATED_PRODUCTS` (existing links stay valid).
- **ONE product, four workload solutions** registered in the shared `SOLUTIONS` map (product-tagged, per-product list derived): **Defender for Endpoint** (MDE — also carries the cross-workload XDR surface: unified incidents, advanced hunting, attack disruption, on rows where correlation is the story), **Defender for Office 365** (MDO), **Defender for Identity** (MDI), **Defender for Cloud Apps** (MDCA; formerly Microsoft Cloud App Security). Same pattern as Entra's CA/PIM/ID-Protection/Governance solutions.
- **Licensing verified against the Microsoft Defender service description + MDO service description + MDE/MDVM/MDI/MDCA product docs** (NOT the Purview/Entra/Intune sources). The high-risk axes encoded in `DEFENDER_LIC`:
  - **MDE P1 vs P2**: P1 (standalone, M365 E3/A3/G3) = NGAV, ASR, device control, endpoint firewall, network protection, web content filtering, tamper protection, manual response. P2 (standalone, M365 E5/A5/G5, E5 Security, Win 10/11 Enterprise E5/A5, Defender Suite) adds EDR, AIR, MDVM core, threat analytics, sandbox, advanced hunting. Every row's license string was chosen per capability (e.g., web-filtering and AV-currency rows = P1; EDR/TVM/threat-analytics rows = P2).
  - **MDVM**: core in P2; premium capabilities = separate add-on; standalone exists for non-P2 customers. Encoded as one three-part string.
  - **MDO P1 vs P2**: P1 = standalone, Business Premium, and **included in Office 365 E3/Microsoft 365 E3 effective July 1, 2026 (already in force — captured in the string)**. P2-only: Threat Explorer, AIR, attack simulation training, campaign views, **Defender XDR integration**.
  - **MDI**: standalone, EMS E5/A5, M365 E5/A5/G5, E5/F5 Security, Defender Suite.
  - **MDCA**: standalone, EMS E5, M365 E5/A5/G5, Defender Suite; **Conditional Access App Control additionally requires Entra ID P1** (per the Defender service description) — encoded in the string.
  - **XDR itself**: no separate license — entitlement follows onboarded workloads; attack disruption + threat analytics require MDE P2 (per XDR prerequisites page).
- **Government clouds** (Defender XDR US Government page + per-workload gov pages): all four workloads available in GCC/GCC High/DoD (dedicated offerings; GCC commercial-tenant transitions required); **Microsoft Threat Experts not available in any gov cloud**; previews commercial-only; MDVM add-on trial unavailable GCC High/DoD (purchase to be confirmed per tenant). Encoded as `DEFENDER_GOV`; every 800-171 and 800-53 row carries a note.
- **Scope boundaries enforced:** Defender for Cloud (CSPM/CWPP, consumption-priced) and Sentinel remain future products. No Azure-resource posture mapped; where server-side coverage came up (PCI 5.2, DPR J #38) the row notes separate server licensing in free text. `licensing_model: per_user` on all 53 rows.

### 13.2 Rows added — per framework, solution & coverage
| Framework | Rows | Control refs |
|---|---|---|
| SSPA DPR | 3 | J #37, J #38, J #40 |
| ISO/IEC 27001:2022 | 9 | A.5.7, A.5.23, A.5.25, A.8.7, A.8.8, A.8.12, A.8.16 (×2: MDE + MDI), A.8.23 |
| SOC 2 | 6 | CC6.7, CC6.8, CC7.1, CC7.2, CC7.3, CC7.4 |
| HIPAA Security Rule | 4 | §164.308(a)(1)(ii)(A), (a)(1)(ii)(D), (a)(5)(ii)(B), (a)(6)(ii) |
| NIST 800-171 R2 / CMMC L2 | 8 | 3.1.20, 3.6.1–3.6.2, 3.11.2–3.11.3, 3.14.2, 3.14.3, 3.14.4–3.14.5, 3.14.6, 3.14.7 |
| NIST 800-53 R5 | 6 | IR-4, RA-5, SI-2, SI-3, SI-4, SI-8 |
| NIST CSF 2.0 | 7 | ID.RA-01, DE.CM-01, DE.CM-03, DE.CM-09, DE.AE-02, RS.AN-03, RS.MI-01–02 |
| PCI DSS v4.0.1 | 5 | 5.2.1–5.2.2, 5.3.1+5.3.5, 5.4.1, 6.3.1, 11.3.1 |
| GLBA Safeguards | 2 | §314.4(c)(8), §314.4(d) |
| FERPA | 0 | deliberate skip — detection/response tooling does not implement the record-scoping access story (§12.2 rationale class) |
| EU GDPR | 3 | Art. 32(1)(b), Art. 32(1)(d), Arts. 33 & 34 |

**By solution (primary):** Defender for Endpoint 45 · Defender for Cloud Apps 5 · Defender for Office 365 2 · Defender for Identity 1. Workloads additionally appear via `also_involves`: MDO on 22 rows, MDI on 15, MDCA on 11, MDE on 1 — the narrow-band workloads are represented mostly as secondary involvement on cross-workload rows, deliberately (their detections surface through the unified incident queue).
**Coverage:** 16 Direct Support · 36 Partial Support · 1 Evidence Support Only · 0 Not Covered. **Confidence:** 47 High · 6 Medium.
Direct discipline: Direct only where Defender is the engine performing the control's namesake activity — anti-malware engine rows (J #38, A.8.7, CC6.8, §164.308(a)(5)(ii)(B), 3.14.2, 3.14.4–5, SI-3, PCI 5.2/5.3), vulnerability management (A.8.8, RA-5, ID.RA-01), runtime monitoring (DE.CM-09), web filtering (A.8.23), spam/phishing at the mail entry point (SI-8, PCI 5.4.1). All monitoring/IR rows with estate-scope caveats held at Partial; MDCA never above Partial.

### 13.3 The MDCA boundary (highest-accuracy-risk item — enforced)
Session and access controls are **reverse-proxy (non-Edge) / in-browser (Edge) only; native desktop and mobile clients bypass session policies entirely** unless access policies block native-client sign-in (verified on the Conditional Access app control page, which documents the `*.mcas.ms` proxy pattern and the recommendation to block native clients). Enforcement in the atlas:
- The boundary is stated in the MDCA **solution registry scope** (renders on the solution page) and in **both session-control rows** (iso-a-8-12-defender, soc2-cc6-7-defender), each with `rel(purview, primary)` to content-aware DLP.
- **Zero MDCA rows rate Direct Support**; the three non-session MDCA rows (A.5.23, 3.1.20, DE.CM-03) claim only discovery/monitoring/governance value.
- MDCA↔Purview DLP seam: represented as cross-links (MDCA rows point at Purview DLP as primary; Purview's iso-a-8-12 row's defender-xdr link now stacks) — never conflated.

### 13.4 Phase 3 — seam reconciliation (27 pre-existing defender-xdr references; result: clean)
Pre-addition the atlas carried **27** `related_microsoft` references to `defender-xdr`: **12 on Purview rows** (the migrated set — matches §10.1's table exactly), **13 on Intune rows**, **2 on Entra rows** (§11's "3 Entra ID Protection links" recounts as 2 in the modules; both now stacked).
- **All 4 primary references now have a stacked Defender row on the exact control:** iso-a-8-7-intune, soc2-cc6-8-intune, hipaa-308-a5-b-intune → MDE engine rows; **pci-5-3-intune required a mirrored row at the exact ref** (`pci-5-3-defender`, "5.3.1, 5.3.5") because the framework view stacks by exact `control_ref` equality — the tamper-protection + auto-update engine capabilities are genuinely that control's content. **Template learning recorded in README.**
- **12 contributing references now stack:** dpr-j40, iso-a-8-1 (+ iso-a-8-1-intune), iso-a-8-12, iso-a-8-16 (+ iso-a-8-16-entra), soc2-cc7-2, 171-3-14-7, 53-si-4, csf-de-cm-03-ai (+ csf-de-cm-03-entra), csf-rs-an-03.
- **pci-6-3-3-intune resolved by adjacency:** its note names the 6.3.1 risk-ranking capability; the Defender row was authored at 6.3.1 where that capability lives (separate control group by design).
- **9 references deliberately remain link-only (flagged, none deleted):** iso-a-7-10, 171-3-8-7 (+ intune mirror), 53-mp-7 (+ intune mirror) — device control stays **Intune-primary policy + MDE-contributing enforcement**; a duplicate MDE row would restate the Intune row's capability text. 171-3-4-2-intune, 53-cm-6-intune — MDE security-settings-management is deployment plumbing on configuration controls, not a Defender capability claim. csf-pr-ps-02-intune, csf-pr-ps-05-intune — software maintenance/execution-control policy layer (App Control for Business is a Windows platform capability managed via Intune). pci-1-5-1-intune — host-firewall enforcement.
- **§10.1 VERIFY worklist closed:** dpr-j40 → STAY (host/cloud IDS-IPS slices = the new MDE/XDR row, stacked; network-appliance IDS/IPS stays external; nothing re-buckets to defender-cloud). 171-3-8-7 / 53-mp-7 → confirmed Intune-primary + MDE enforcement link, no re-bucket. **0 references re-bucketed to `defender-cloud`.**
- **MDI ↔ Entra ID Protection seam:** parallel cards on ISO A.8.16 — the MDI row (on-prem AD sensors) mirrors iso-a-8-16-entra (cloud sign-in risk), each cross-linking the other's product with an explicit "seam, not overlap" note; 12 entra links on Defender rows carry the same boundary. Never conflated.
- **Forward links parked this session:** 21 `sentinel` contributing links on Defender rows (SIEM/estate-wide correlation — the established forward pattern; revisit at the Sentinel session). **No structured `defender-cloud` links authored**; Defender for Cloud appears only in free-text external notes (server licensing on PCI 5.2/DPR J #38; cloud-resource posture on A.5.23/A.8.8/ID.RA-01).

### 13.5 Phase 5 — QA results
- **No-regression:** Purview 150 = baseline 150, id sets identical, **0 protected-content-field diffs**; Entra 48 rows with coverage 29 Direct/19 Partial and confidence 39 High/9 Medium (= §11.2 exactly); Intune 41 rows with 10 Direct/31 Partial and 28 High/13 Medium (= §12.2 exactly).
- **Reconciliation:** JSON 292 = HTML footer 292 = density Σ 292 (per-framework 22·45·34·25·34·39·29·23·16·6·19); landing shows 4 products · 292 mappings · 71 Direct claims · 0 unverified.
- **Source verification:** every row authored against Learn pages fetched live this session (XDR overview/prerequisites, Defender service description, MDO service description + cheat sheet, MDE P1 overview, MDVM plans-comparison, MDI prerequisites, MDCA CAAC page, per-workload gov pages). Framework refs verified against local official sources: DPR v12 J #37/#38/#40 exact text; 800-171 3.1.20/3.11.2–3/3.14.2–7 exact text; TSC CC7.1 wording; HIPAA/GLBA from eCFR text (§314.4(d)(2)'s continuous-monitoring alternative quoted from source); PCI numbering via the Azure Policy initiative page.
- **Direct-Support re-verification (16 rows):** each confirmed as engine-performs-the-namesake-activity; the two licensing-sensitive P1 claims spot-checked on live docs — **web content filtering prerequisites list MDE P1 explicitly** (iso-a-8-23) and **tamper protection is P1-inclusive** (pci-5-3). No Direct claim rests on a P2-only capability under a P1 license string.
- **MDE P1-vs-P2 licensing re-verification:** all EDR/AIR/TVM/threat-analytics/advanced-hunting rows carry `mde_p2` or `mdvm`; all NGAV/ASR/web-filtering/AV-currency rows carry `mde_p1`; composed strings used where a row spans layers (CC6.8: P1 engine + P2 EDR). MDO P2-only capabilities (Explorer/AIR/attack-sim/XDR-integration) never appear on `mdo_p1`-only rows.
- **URL resolution: 36/36 distinct new URLs return 200** (all learn.microsoft.com, incl. both service descriptions and the four gov pages). Zero WAF blocks this increment.
- **Rendering:** all four views verified light + dark via headless Edge — landing (4-product stat line, refreshed industry notes), ISO framework view with the **A.8.16 four-card stack (Purview + Entra + MDE + MDI)** and stacked A.8.7/A.8.12/A.5.25, Product Pivot (Defender XDR page: 53 mappings, 4 solution cards with per-workload counts, 27-row referenced-by list), **solution-level filtering confirmed: the MDCA solution page shows exactly its 5 primary mappings + 11 contributing appearances**, Density Matrix (Defender column Σ 53, FERPA cell honestly empty). Print-to-PDF smoke test on the 800-171 view produced a fully expanded dossier.

### 13.6 Add-a-product template verdict — HELD, with 2 refinements
Second clean clone of the procedure: structured `prow`/`rel` authoring, product-tagged SOLUTIONS with derived lists, per-module append blocks, per-product `_LIC`/`_URLS`/`_GOV`, RELATED_PRODUCTS graduation, seam reconciliation, and framework-metadata extension all worked without rework. Refinements recorded in the README:
1. **Stacking requires exact `control_ref` equality** (template groups by the literal string). When a prior product's primary reference sits on a multi-ref control (pci-5-3-intune "5.3.1, 5.3.5"), the new product's row must mirror that exact ref to stack — an adjacent-family row does not.
2. **A solution with zero primary rows renders as an empty pivot page.** If a narrow-band workload lands only in `also_involves`, give it at least one genuine primary row where its slice is truly the story (MDI on ISO A.8.16, mirroring the Entra ID Protection card) — or consciously accept the empty page.

**Defender XDR addition verdict: SHIP.** 292/292 rows verified; Purview, Entra, and Intune untouched; 27 seams reconciled; §10.1 worklist closed; all four views four-product. Remaining product backlog: **Sentinel** and **Defender for Cloud** (the 21 sentinel forward links and the defender-cloud external notes are their entry points).

## 14. Sentinel product addition (2026-07-18)

Fifth product added — the third clean clone of the add-a-product template, and the **first consumption-priced product** (the pattern Defender for Cloud will inherit).
**46 Sentinel rows across 10 of 11 frameworks (FERPA deliberately skipped); new atlas total 292 → 338.** Purview (150), Entra (48), Intune (41), and Defender XDR (53) unchanged, zero content drift.

### 14.1 Product registration, platform-state verification & scope decisions
- Registered `sentinel` in `PRODUCTS` (official name **Microsoft Sentinel** — "Azure Sentinel" is retired branding; verified on the Sentinel overview page). Moved `sentinel` out of `RELATED_PRODUCTS` (all 33 existing links stay valid).
- **Platform state verified live 2026-07-18** (the surface has been in heavy flux — nothing recalled):
  - **Portal:** Sentinel is GA in the Microsoft Defender portal, including for customers *without* Defender XDR or E5. The **Azure-portal experience retires March 31, 2027** — *extended* from the previously announced July 1, 2026 (partner announcement Feb 12, 2026). New tenants auto-onboard to the Defender portal since July 2025. Rows describe the Defender-portal experience.
  - **Data model (2025 platform change):** two tiers — **analytics tier** (90-day included retention for Sentinel tables, extendable to 2 years at a prorated charge) mirrored into the **Microsoft Sentinel data lake** with **total retention up to 12 years**; lake-only tier for high-volume/low-touch sources. For onboarded workspaces this replaces the former Basic/Auxiliary/Archive story (billing article states lake meters supersede the long-term-retention/search/auxiliary meters). Data lake caveat carried in the solution registry: **customer-managed keys are not supported for lake-stored data**.
  - **China:** all Sentinel features retire in Azure operated by 21Vianet on Aug 18, 2026 — noted in README maintenance triggers, irrelevant to US-focused rows.
- **ONE product, seven functional solutions** registered product-tagged in the shared `SOLUTIONS` map (Sentinel has no workload sub-brands; the functional surfaces are the consulting pivot): **Data Collection & Connectors**, **Analytics Rules & Detections**, **Incident Management & Investigation**, **Automation & Playbooks (SOAR)**, **UEBA & Hunting**, **Threat Intelligence**, **Log Retention & Data Lake**. Hunting and workbooks were consolidated (UEBA & Hunting; workbooks appear as capability detail) so every solution earns ≥1 primary row (§13.6 refinement respected — verified 7/7 below).
- **Scope boundaries enforced:** Defender for Cloud (CSPM/CWPP) remains the final future product — **no structured `defender-cloud` links authored on Sentinel rows** (its alert types appear only inside the free-data-sources licensing text, consistent with §13.4's treatment). MDCA-style boundary statements are carried in the solution registry scopes (sources generate their own records; SOAR orchestrates but integrated products remediate; coverage follows the connector estate).

### 14.2 The consumption licensing model — first use of `licensing_model: consumption`
- `default_licensing_model: "consumption"`; **all 46 rows carry `licensing_model: consumption`** (verified in QA). `licensing_source` = the Sentinel billing article (not a service description — there is none for a meter-priced product).
- `SENTINEL_LIC` strings describe **meters, not SKUs** (verified against the billing article + manage-data-overview + the M365 benefit offer page, all fetched live):
  - **ingest**: PAYG per GB or commitment tiers from 100 GB/day (a 50 GB tier entered public preview Oct 2025 — README maintenance trigger to confirm GA); simplified tiers combine Log Analytics + Sentinel meters.
  - **retention**: analytics-tier retention beyond the included 90 days billed per GB (to 2 years); data-lake total retention to 12 years billed per compressed GB/month (6:1 compression assumption) plus per-GB query/processing meters — **the consulting insight carried on every retention row: 12-month (PCI 10.5.1) and multi-year (CMMC 3.3.1 / 800-53 AU-11) mandates are consumption costs driven by ingest volume and tiering, not license tiers**.
  - **free_benefit**: free data sources (Office 365 audit activity, Azure Activity, SentinelHealth, and *all* Defender security alerts/incidents — while **raw** Defender/Entra logs are paid) plus the **Microsoft 365 E7/E5/A5/F5/G5 and E5 Security data grant: up to 5 MB/user/day** covering Entra ID sign-in/audit logs, MDCA shadow-IT discovery, Purview Information Protection logs, and Defender XDR advanced-hunting tables. Verified on the offer page (now branded **E7**, E5, A5, F5, G5 — E7 is new); eligible SKU list includes USGOV_GCCHIGH and USGOV_DOD variants; EA/EAS/CSP agreements.
  - **soar**: automation rules included; Logic Apps playbooks billed separately under Azure Logic Apps meters.
- **Rendering:** the template's licensing chip is value-agnostic (`${esc(r.licensing_model)}`), so `consumption` rendered correctly on first build with no template change — confirmed visually (6 consumption chips on the ISO framework page; chips in the print dossier). No per-user badge logic existed to break.
- **Government clouds** (`SENTINEL_GOV`, verified against unified-secops/gov-support + the Sentinel feature-availability page + the cloud feature-availability fundamentals page): Defender-portal GA features supported in GCC/GCC High/DoD (portal URLs security.microsoft.us / security.apps.mil); previews commercial-only; GCC cannot run advanced-hunting queries spanning Sentinel + XDR tables. Azure Government gaps: summary rules, SOC optimization, SIEM migration, repositories, MDTI matching analytics, URL detonation, TI GeoLocation/WhoIs enrichment; UEBA core GA (peer/blast-radius commercial-only). **Office 365 DoD: the Defender XDR connector is listed as not available** — carried as a DoD caveat. E5/G5 benefit includes GCC High/DoD SKUs. Carried on all 800-171 and 800-53 rows.

### 14.3 Rows added — per framework, solution & coverage
| Framework | Rows | Control refs |
|---|---|---|
| SSPA DPR | 2 | I #30–31, J #40 |
| ISO/IEC 27001:2022 | 6 | A.5.7, A.5.25, A.5.26, A.5.28, A.8.15, A.8.16 |
| SOC 2 | 3 | CC7.2, CC7.3, CC7.4 |
| HIPAA Security Rule | 3 | §164.308(a)(1)(ii)(D), §164.308(a)(6)(ii), §164.312(b) |
| NIST 800-171 R2 / CMMC L2 | 7 | 3.3.1, 3.3.4, 3.3.5, 3.6.1–3.6.2, 3.14.3, 3.14.6, 3.14.7 |
| NIST 800-53 R5 | 8 | AU-2, AU-12 (mirrored ref), AU-6, AU-9, AU-11, IR-4, IR-5, SI-4, RA-10 |
| NIST CSF 2.0 | 6 | PR.PS-04, DE.AE-02, DE.AE-03, DE.CM-01, RS.AN-03, RS.MI-01–02 (mirrored ref) |
| PCI DSS v4.0.1 | 5 | 10.3.3, "10.4.1, 10.4.1.1", 10.5.1, 10.7.2, 12.10.5 |
| GLBA Safeguards | 3 | §314.4(c)(8), §314.4(d), §314.4(h) |
| FERPA | 0 | deliberate skip — no FERPA provision's namesake activity is security logging/monitoring; §99.32's recordkeeping concerns *disclosure* records (Purview Audit's row), not SIEM telemetry. Third honest product zero after Intune-adjacent and Defender skips. |
| EU GDPR | 3 | Art. 32(1)(b), Art. 32(1)(d), Arts. 33 & 34 |

**By solution (primary):** Analytics Rules & Detections 18 · Incident Management & Investigation 10 · Data Collection & Connectors 7 · Automation & Playbooks (SOAR) 4 · Log Retention & Data Lake 3 · UEBA & Hunting 2 · Threat Intelligence 2 — every solution has ≥1 primary row (7/7; §13.6 refinement satisfied; contributing appearances via also_involves: Data Collection 13, SOAR 7, UEBA & Hunting 7, Incident Mgmt 9, Log Retention 6, Analytics 8, TI 1).
**Coverage: 15 Direct Support · 28 Partial Support · 3 Evidence Support Only · 0 Not Covered. Confidence: 44 High · 2 Medium.**

**Why the Direct count is 15 (33%) and why that is not inflation.** The instruction anticipated a distribution skewed away from Defender's Direct-heavy shape. The *proportion* (33% vs Defender's 30%) is similar, but the **composition** is categorically different, and composition is what the discipline governs:
- **Every one of the 15 Directs is an AU-family/logging namesake control** — the exact band the discipline reserves Direct for: ISO A.8.15 (logging) + A.8.16 (monitoring); HIPAA §164.308(a)(1)(ii)(D) (activity review) + §164.312(b) (audit controls); 800-171 3.3.1 (create/retain audit records) + 3.3.5 (correlate audit review — correlation is the definition of SIEM); 800-53 AU-6 (review/analysis/reporting) + AU-11 (retention); CSF PR.PS-04 (logs made available for continuous monitoring) + DE.AE-02 (events analyzed) + DE.AE-03 (information correlated from multiple sources — the single most Sentinel-shaped control in any framework); PCI 10.3.3 (central log server) + 10.4.1/10.4.1.1 (automated log review) + 10.5.1 (12-month retention); GLBA §314.4(c)(8) (monitor and log user activity).
- **Zero Directs on incident response, SOAR, threat detection, or TI rows.** All 9 IR/SOAR rows rate Partial (orchestration honesty: Sentinel coordinates, integrated products remediate — stated in the SOAR solution scope and on every row); both TI rows Partial; RA-10 hunting Partial (tooling ≠ capability); SI-4/DE.CM-01/3.14.6 monitoring rows held at Partial where the sensing layer is external appliances.
- **Borderline calls resolved downward:** AU-2/AU-12 held at **Partial** (record *generation* is a per-component capability; Sentinel owns only the DCR selection surface — contrast 3.3.1, whose namesake includes create-and-**retain** of the record estate); IR-5 (track/document incidents) held at **Partial** despite the incident queue being a literal tracking system (completeness depends on organizational routing of non-telemetry incidents); SOC 2 CC7.2 held at **Partial** to match the four-Partial stack (the criterion spans control-operation monitoring beyond security telemetry).
- The concentration effect is curation, not inflation: Sentinel is mapped only where it has a genuine role, and its genuine role *is* the audit/monitoring band — so its mapped rows over-sample exactly the controls where Direct is sanctioned. Evidence Support Only appears where honesty demands it (ISO A.5.28 evidence procedures, GLBA §314.4(h) written-plan execution, GDPR 32(1)(d) effectiveness evidence).
- 2 Medium confidences: pci-10-3-3 (sub-requirement text of the license-gated standard paraphrased; numbering verified via the Azure Policy initiative page) and gdpr-32-1-d (interpretive evidence claim).

### 14.4 Phase 3 — seam reconciliation (33 pre-existing sentinel references; result: 33/33 stacked, clean)
Pre-addition the atlas carried **33** `related_microsoft` references to `sentinel`: **21 on Defender rows** (parked at §13.4), **3 on Entra rows** (iso-a-8-16-entra, soc2-cc7-2-entra, glba-314-4-c8-entra), **9 on Purview rows** (the migrated set: iso-a-8-15, iso-a-8-16, soc2-cc7-2, 171-3-3-1, 171-3-14-7, 53-au-2-12, 53-si-4, csf-pr-ps-04, csf-rs-an-03).
- **All 33 now stack: every referencing row has a Sentinel row at its exact `control_ref`.** 0 link-only leftovers, 0 flagged as non-substantive, 0 deleted. Two refs required exact-string mirroring per §13.6: `3.6.1–3.6.2`, `RS.MI-01–02` (en-dashes), plus multi-ref mirrors `AU-2, AU-12` and `I #30–31` — all verified grouping correctly.
- **Defender ↔ Sentinel seam (the one to get right):** written as explicit "seam, not overlap" notes on both sides of every stacked pair — *Defender XDR is the native detection/containment engine inside Microsoft workloads (alerts ingest free); Sentinel ingests, correlates across sources, retains beyond XDR's 30-day window, and orchestrates response — including the non-Microsoft systems Defender cannot reach.* Detection is never claimed as Sentinel's; cross-source correlation/retention is never claimed as Defender's. Representative pairs: SI-4 (workload sensor vs cross-source monitor), CC7.3 (Defender evaluates its workloads, Sentinel evaluates the estate), RS.AN-03 (device story vs estate story), RS.MI-01–02 / IR-4 (Defender contains its workloads, Sentinel orchestrates everything else), DE.AE-03 (XDR incidents join estate-wide correlation as one source among many), A.5.7 (Defender produces tenant-contextual TI, Sentinel manages/matches the multi-source TI estate).
- **Purview Audit ↔ Sentinel seam:** cross-linked, never conflated, on every shared audit control — *Purview Audit generates and retains the M365 source record (its own 180-day/1-yr/10-yr retention); the Microsoft 365 connector ingests OfficeActivity free; Sentinel is the estate-wide log platform and retains the workspace copy.* Stated on A.8.15, §164.312(b), 3.3.1, AU-2/AU-12, AU-11, PR.PS-04, §164.308(a)(1)(ii)(D).
- **No new forward links parked pointing at `defender-cloud`** — deliberate (§14.1). Defender for Cloud's entry points remain the free-text notes on PCI 5.2 / DPR J #38 / A.5.23 / A.8.8 / ID.RA-01 plus its alert types among Sentinel's free data sources.

### 14.5 Phase 5 — QA results
- **No-regression:** Purview 150 = baseline 150, id sets identical, **0 protected-content-field diffs**; Entra 48 (29 Direct/19 Partial; 39 High/9 Medium = §11.2 exactly); Intune 41 (10/31; 28/13 = §12.2 exactly); Defender XDR 53 (16/36/1; 47/6 = §13.2 exactly).
- **Reconciliation:** JSON 338 = HTML embed 338 = density Σ 338 (per-framework 24·51·37·28·41·47·35·28·19·6·22); landing shows 5 products · 338 mappings · 86 Direct claims (71+15) · 0 unverified; Sentinel matrix column Σ 46 with the FERPA cell honestly empty.
- **Source verification:** every row authored against sources fetched live this session (Sentinel overview/Defender-portal/move-to-defender pages, billing article, manage-data-overview, data lake overview + service limits, feature-availability, unified-SecOps gov-support, cloud feature-availability fundamentals, M365 benefit offer page). Framework refs verified against local official texts: DPR v12 I #30–31 / J #40 exact text; 800-171 3.3.1/3.3.4/3.3.5/3.6.x/3.14.x exact text; 800-53 AU-6/AU-11/AU-2/IR-5/RA-10 exact text; CSF PR.PS-04/DE.AE-03/DE.CM-01/RS.MI-02 exact text; HIPAA/GLBA from eCFR-derived local texts; PCI numbering via the Azure Policy PCI DSS 4.0 initiative page (the local pci-dss-401.pdf turned out to be a saved HTML error page — the license-gated route; initiative-page route used instead, per the established pattern).
- **Direct-Support re-verification (15 rows):** each confirmed as namesake-activity-performed (§14.3 composition analysis); zero Direct claims on detection/response/orchestration rows. Two GA-vs-preview precision fixes applied during QA against the feature-availability table: the **hunts** experience marked public preview (not in Azure Gov) on 53-ra-10-sentinel; **UEBA Active Directory sync via MDI** marked public preview on 171-3-14-7-sentinel.
- **Consumption/free-benefit re-verification:** every `SENTINEL_LIC` string re-checked against the live billing article and offer page (commitment tiers 100 GB+ / 50 GB preview; 90-day/2-yr/12-yr retention values; 6:1 lake compression; free sources list; 5 MB/user/day grant with the four covered data classes; E7 SKU addition; gov SKU eligibility). All 46 rows `licensing_model: consumption`, `status: verified`.
- **URL resolution: 23/23 distinct new Microsoft URLs return 200** (Learn + the DPR CDN + the SSPA page; the offer page verified via live fetch). **Zero WAF blocks this increment.**
- **Rendering** (headless Edge, light + dark, per the §12 technique): landing (5-product stat line, refreshed industry notes for healthcare/DIB/finserv/retail/federal), ISO framework view with the **A.8.16 five-product stack (Purview + Entra + MDE + MDI + Sentinel)** confirmed at DOM level, Product Pivot Sentinel page (46 mappings, 7 solution cards with per-solution counts, product-notes block showing the consumption story, 33-row referenced-by list), **solution-level filtering confirmed: Log Retention & Data Lake shows exactly its 3 primary + 6 contributing mappings**, Density Matrix (Sentinel column Σ 46, FERPA `·`), **consumption licensing chip rendering confirmed** (6 chips on the ISO page; present in print output). Print-to-PDF on the PCI view produced a 30-page fully expanded dossier containing the Sentinel Req-10 rows and consumption strings. Hero as-of date bumped to 2026-07-18.

### 14.6 Add-a-product template verdict — HELD, no new refinements required
Third clean clone: structured `prow`/`rel` authoring, product-tagged SOLUTIONS with derived lists, per-module append blocks, per-product `_LIC`/`_URLS`/`_GOV`, RELATED_PRODUCTS graduation, exact-ref stacking (§13.6 #1 applied four times), ≥1-primary-row-per-solution (§13.6 #2 applied at design time), seam reconciliation, and framework-metadata review all worked without rework. The only generalization exercised for the first time — `licensing_model: consumption` + a meters-not-SKUs `_LIC` dict — worked as designed with zero template changes. **For Defender for Cloud, inherit:** the consumption `_LIC` pattern verbatim, the free-alert-ingestion cross-over (MDC alerts are already free Sentinel data types), and the seam discipline (MDC will need a three-way seam against both Defender XDR and Sentinel).

**Sentinel addition verdict: SHIP.** 338/338 rows verified; Purview, Entra, Intune, and Defender XDR untouched; 33/33 sentinel seams stacked; all four views five-product; consumption licensing renders cleanly. Remaining product backlog: **Defender for Cloud** (final product).

## 15. Defender for Cloud product addition (2026-07-18) — ROADMAP COMPLETE

Sixth and **final** product — the fourth clean clone of the add-a-product template, the second consumption-priced
product (inheriting Sentinel's meters-not-SKUs pattern verbatim per §14.6), and the **first non-M365 product**
(cloud infrastructure across Azure/AWS/GCP, not Microsoft 365 workloads).
**40 Defender for Cloud rows across 10 of 11 frameworks (FERPA deliberately skipped); new atlas total 338 → 378.**
Purview (150 — 0 protected-field diffs vs the 150-row baseline, id sets identical), Entra (48: 29D/19P, 39H/9M),
Intune (41: 10D/31P, 28H/13M), Defender XDR (53: 16D/36P/1E, 47H/6M), and Sentinel (46: 15D/28P/3E, 44H/2M) all
unchanged — distributions equal §11.2/§12.2/§13.2/§14.3 exactly; zero content drift.

### 15.1 Product registration, live verification & scope decisions
- Registered `defender-cloud` in `PRODUCTS` (official name **Microsoft Defender for Cloud** — CNAPP, verified on the
  product introduction page). Moved `defender-cloud` out of `RELATED_PRODUCTS`. `licensing_source` = the **Azure
  pricing page** (a consumption product has no service description — Sentinel precedent), fetched live.
- **Everything verified live 2026-07-18, nothing recalled:** plan list (Defender CSPM/Foundational CSPM, Servers
  P1/P2, Containers, Storage, Databases ×4 sub-plans, App Service, Key Vault, Resource Manager, APIs P1–P5, AI
  Services), the free-vs-paid CSPM boundary, the dashboard's paid-plan gate, CIEM state, Servers P1/P2 content, the
  per-resource meters, and the Azure Government support matrix. **Defender for DNS is legacy-only** (existing
  subscriptions since Aug 1, 2023; DNS alerts ride in Servers P2 for new subs) — no solution registered. **Defender
  Experts for Servers** is a separately-sold managed service — out of scope.
- **ONE product, five functional solutions** (consolidations documented in `common.py`): **Foundational CSPM**
  (free tier; multicloud connectors folded in — connectors are free and never the control story alone),
  **Defender CSPM**, **Regulatory Compliance Dashboard**, **Defender for Servers** (stands alone for its MDE
  licensing seam and P2 feature band), **Workload Protection Plans** (Storage, Databases, Containers, App Service,
  Key Vault, Resource Manager, APIs, AI Services consolidated — none of the eight leads a control story in these
  11 frameworks on its own). All 5 solutions have ≥6 primary rows (§13.6 #2 satisfied by a wide margin).
- **CIEM carry-forward RESOLVED (the §11.1 open item):** Microsoft Learn states explicitly that the Microsoft Entra
  Permissions Management deprecation (2025-10-01) "doesn't affect any existing CIEM capabilities in Microsoft
  Defender for Cloud" — **CIEM is a native component of the Defender CSPM plan** (multicloud identity discovery,
  effective-permission analysis, lateral-movement detection via attack paths). Mapped inside the Defender CSPM
  solution scope and on `gdpr-32-1-b-mdc`; **CIEM is NA in Azure Government** (carried in `MDC_GOV["gaps"]`).
- **Azure-platform scope boundary DECIDED and recorded:** this product maps Defender for Cloud only. Azure platform
  security services — **Key Vault as a service, Azure networking/Firewall/WAF, Azure Policy, Azure RBAC, Azure
  Update Manager, Azure Backup** — are NOT mapped capabilities; they appear only in `external_dependencies` (the
  recurring pattern: "remediation executes via Azure Policy/IaC — outside this product"). This boundary defines what
  a hypothetical future "Azure platform security" product would have covered; **with the roadmap closed, these stay
  out-of-atlas permanently.** (Defender for Key Vault — the *threat-detection plan for* Key Vault — is mapped under
  Workload Protection Plans; Key Vault itself is not. The distinction is stated in the solution scope.)
- **Consumption licensing (2nd use):** `default_licensing_model: consumption`; **all 40 rows carry
  `licensing_model: consumption`** (verified in QA). `MDC_LIC` describes meters: per server/hour (Servers P1/P2),
  per storage account/month + per-transaction overage + per-GB malware scanning, per database server / per RU
  (Cosmos), per vCore (Containers), per vault, per subscription (ARM), per 1K tokens (AI), call-volume plan tiers
  (APIs), per billable resource (Defender CSPM); 30-day trial (malware scanning excluded); 1-year pre-purchase
  Commit Units up to 22% discount. **Servers P1/P2 axis encoded precisely: the integrated MDE-for-Servers license
  rides with BOTH plans** (MDE-for-Servers licensees can request a price adjustment — FAQ verified); premium MDVM,
  FIM, JIT, agentless scanning, OS baseline/updates assessment, DNS alerts, and the **500 MB/day workspace ingestion
  benefit** (applies to Sentinel simplified meters — a direct Sentinel cost seam) are P2.
- **Government clouds:** for an Azure-resource product, "gov" = **Azure Government** (US Gov Arizona/Texas/Virginia;
  the M365 GCC/GCC High/DoD distinction does not apply to Azure resources — stated in `MDC_GOV`). GA in Gov:
  Foundational + Defender CSPM, Servers P1/P2 (FIM GA except GovCon Cloud Moderate), Storage (malware scanning GA;
  sensitive-data threat detection NA), Containers, Key Vault, Resource Manager, SQL/OSS databases, and the
  regulatory compliance dashboard. NA in Gov: APIs, App Service, AI Services, Cosmos DB, DevOps security, CIEM,
  Data & AI security dashboard, EASM/ServiceNow/code-to-runtime. Carried on all 800-171/800-53 rows.
  China (21Vianet): all Defender for Cloud features retire Oct 1, 2026 — README maintenance trigger.
- **Declared metadata edits to prior products** (product notes, not row content): `PRODUCTS["defender-xdr"].notes`
  and `PRODUCTS["sentinel"].notes` updated from "future atlas product" phrasing to name Defender for Cloud as a
  shipped product with its seam. Row content untouched (drift gate proven above).

### 15.2 The regulatory compliance dashboard (the meta-capability — treated precisely)
- **The free-vs-paid gate, verified on the assign-standards prerequisites page:** the default MCSB assessment is
  free with Defender for Cloud; **assigning additional built-in or custom standards requires at least one paid
  plan — any plan except Defender for Servers Plan 1 and Defender for APIs Plan 1.** Encoded as
  `MDC_LIC["dashboard"]` and carried on all 8 dashboard rows.
- **Current standards catalog captured live** (both portal pivots): ISO/IEC 27001:2022, SOC 2/SOC 2023, PCI DSS
  v4.0.1, NIST SP 800-53 R5.1.1, NIST 800-171 (now offering **R3** — the atlas pins R2; the revision-mismatch
  caution is written into `171-3-12-1-3-mdc`), NIST CSF 2.0, CMMC L2 v2.0, HIPAA + HITRUST CSF v11.3.0, GDPR,
  FedRAMP H/M, CIS benchmarks, NIS2, SWIFT, and others; custom standards supported. **No GLBA, FERPA, or SSPA DPR
  standard exists** — dashboard rows appear only in frameworks the catalog genuinely serves.
- **The assessment-scope caveat appears on every one of the 8 dashboard rows** (verified in QA; three rows carry it
  in row-appropriate words — e.g., the CMMC row: "neither a self-assessment submission (SPRS) nor a C3PAO
  certification artifact"): the dashboard assesses **the cloud resource scope onboarded to Defender for Cloud**
  against a standard's **technically-assessable control subset** — never M365 workloads, on-premises systems, or
  administrative/procedural controls — and is **not an attestation, audit, or compliance determination**. The same
  boundary is stated in the solution registry scope and the product notes (three layers, mirroring the MDCA
  browser-only treatment §13.3).
- **Purview Compliance Manager seam:** every dashboard row carries a `rel("purview", …, "Compliance Manager")`
  link with "complementary assessment scopes — a seam, not an overlap"; 4 of the 8 dashboard rows stack directly
  against existing Purview Compliance Manager rows at the exact ref (ISO A.5.36, SOC 2 CC4.1, HIPAA §164.308(a)(8),
  800-171 "3.12.1, 3.12.3") — the framework view renders the two assessment engines side by side.
- **Direct Support on dashboard rows is held to the sanctioned band:** ISO A.5.36 (regularly verify compliance —
  the namesake), 800-53 CA-7 (ongoing assessments/metrics/status/reporting — the namesake), CSF ID.IM-01
  (improvements identified from evaluations; Medium confidence). CA-2, 3.12.1/3.12.3, §164.308(a)(8), CC4.1
  (Medium), and GDPR 32(1)(d) all held at **Partial** — the assessment program, the nontechnical halves, and the
  non-cloud estate are outside the mechanism.

### 15.3 Rows added — per framework, solution & coverage
| Framework | Rows | Control refs |
|---|---|---|
| SSPA DPR | 2 | J #38, J #40 |
| ISO/IEC 27001:2022 | 6 | A.5.23, A.5.36, A.8.7, A.8.8, A.8.9, A.8.16 |
| SOC 2 | 4 | CC4.1, CC6.8, CC7.1, CC7.2 |
| HIPAA Security Rule | 4 | §164.308(a)(1)(ii)(A), §164.308(a)(5)(ii)(B), §164.308(a)(8), §164.312(c) |
| NIST 800-171 R2 / CMMC L2 | 5 | 3.4.1, 3.11.1, 3.11.2–3.11.3, "3.12.1, 3.12.3", 3.14.6 |
| NIST 800-53 R5 | 7 | CA-2, CA-7, CM-6, CM-8, RA-5, SI-4, SI-7 |
| NIST CSF 2.0 | 5 | ID.AM-02, ID.IM-01, ID.RA-01, PR.PS-01, DE.CM-09 |
| PCI DSS v4.0.1 | 3 | 2.2.1, 5.2.1–5.2.2, 11.3.1 |
| GLBA Safeguards | 2 | §314.4(c)(2), §314.4(d) |
| FERPA | 0 | deliberate skip — FERPA governs education-record access and disclosure; cloud-infrastructure posture/workload tooling implements no record-scoping activity. Fourth honest product zero. |
| EU GDPR | 2 | Art. 32(1)(b), Art. 32(1)(d) |

**By solution (primary):** Defender CSPM 10 · Foundational CSPM 9 · Regulatory Compliance Dashboard 8 · Workload
Protection Plans 7 · Defender for Servers 6 (5/5 solutions ≥1 primary; contributing via also_involves: Foundational
14, Servers 12, Workload 7, CSPM 4, Dashboard 2).
**Coverage: 12 Direct Support · 28 Partial Support · 0 Evidence Support Only · 0 Not Covered. Confidence: 38 High ·
2 Medium** (soc2-cc4-1-mdc — COSO-interpretive; csf-id-im-01-mdc — interpretive Direct).
**Why 12 Directs (30%) is composition, not inflation** (the §14.3 analysis repeated for this product's band): every
Direct is an assessment/inventory/scanning/integrity-verification namesake — vulnerability assessment (A.8.8,
3.11.2–3.11.3, RA-5, ID.RA-01, 11.3.1, CC7.1), compliance/control-state assessment (A.5.36, CA-7, ID.IM-01),
resource inventory (CM-8, ID.AM-02), and integrity-verification tooling (SI-7 FIM). **Zero Directs on hardening,
configuration-enforcement, malware, monitoring, or dashboard-in-CMMC rows**: every detects-but-does-not-remediate
control (A.8.9, CM-6, PR.PS-01, 2.2.1, 3.4.1) held at Partial per the enforces-vs-detects line inherited from
Intune/Sentinel; every malware row (J #38, A.8.7, CC6.8, §164.308(a)(5)(ii)(B), 5.2.1–5.2.2) held at Partial with
`rel(defender-xdr, primary)` because the engine is MDE — Defender for Cloud is the per-server licensing/deployment
vehicle plus the storage-scanning plane; all monitoring rows (A.8.16, CC7.2, 3.14.6, SI-4, DE.CM-09, J #40) Partial.

### 15.4 Phase 3 — seam reconciliation (result: clean; 0 pre-existing structured links, 5 free-text entry points all stacked)
- Pre-addition the atlas carried **zero structured `defender-cloud` links** (deliberate — §13.4/§14.4); the entry
  points were free-text notes. **All five located and stacked at exact refs:** PCI 5.2 ("separate server licensing"
  on pci-5-2-defender at '5.2.1–5.2.2') → `pci-5-2-mdc` mirrors the exact ref; DPR J #38 ("Server anti-malware
  licensing is separate…Defender for Servers") → `dpr-j38-mdc`; ISO A.5.23 ("IaaS/PaaS posture — separate product")
  → `iso-a-5-23-mdc`; ISO A.8.8 ("cloud-resource posture — separate product") → `iso-a-8-8-mdc`; CSF ID.RA-01
  ("cloud resources — separate product") → `csf-id-ra-01-mdc`. Prior rows untouched — their "separate product"
  phrasing remains true and now renders beside the stacked card.
- **Defender for Cloud ↔ Defender XDR** (both sides): alerts/incidents integrate into the Microsoft Defender portal
  (concept-integration-365 — correlation, no duplication, informational alerts excluded); Defender for Servers
  carries the integrated MDE-for-Servers license. Written on every shared row as "MDE protects endpoints under
  Defender XDR; Defender for Cloud protects cloud workloads and posture" — the malware rows make the engine-vs-
  vehicle split explicit with `rel(defender-xdr, primary)`.
- **Defender for Cloud ↔ Sentinel:** Defender for Cloud security alerts are free Sentinel data types (already in
  `SENTINEL_LIC["free_benefit"]` — the §14.6 crossover honored); Sentinel correlates estate-wide and retains beyond
  the portal window; the Servers P2 500 MB/day benefit applies against Sentinel simplified meters. Written on the
  monitoring/detection rows both ways; never conflated with detection ownership.
- **Dashboard ↔ Compliance Manager** and **data-aware posture ↔ Purview classification** seams per §15.2 and the
  three data-aware rows (`gdpr-32-1-b-mdc`, `glba-314-4-c2-mdc`, `hipaa-308-a1-a-mdc`): sensitive data discovery is
  *powered by the Microsoft Purview classification engine* (same SITs/labels, importable custom types) but samples
  cloud datastores for posture prioritization — it does not label or protect content; "different classification
  scopes, one taxonomy." Purview remains the classification authority.
- **7 deliberately new refs** (no co-stacked product, correct): 800-171 3.11.1; 800-53 CA-2, CA-7, CM-8, SI-7;
  CSF ID.AM-02 (chosen over stacking at Intune's ID.AM-01 — honesty over stacking: cloud resources are
  "software, services, and systems," not "hardware"; the Intune adjacency is a rel note, per the pci-6-3-3
  precedent §13.4), ID.IM-01. The CA family enters the 800-53 subset (FRAMEWORK domains + notes extended).

### 15.5 Phase 5 — QA results
- **No-regression:** per the header — all five prior products' counts and distributions exact; Purview 150 vs
  150-row baseline: id sets identical, **0 protected-content-field diffs**.
- **Reconciliation:** JSON 378 = HTML embed 378 (build output) = landing stats (6 products · 11 frameworks ·
  **378 control mappings · 98 direct-support claims (86+12) · 0 unverified**) = per-framework density
  26·57·41·32·46·54·40·31·21·6·24 (Σ 378).
- **Source verification:** every fact authored against pages fetched live this session (intro, CSPM concept/enable,
  CIEM, regulatory-compliance concept/assign/FAQ, Servers overview/plan-select/FAQ/data-benefit, DSPM concept,
  storage-sensitivity, support matrix, concept-integration-365, Azure pricing page). Framework refs for stacked rows
  reuse the exact verified intents of the existing rows; the 7 new refs verified against local official texts —
  CA-2/CA-7/CM-8/SI-7 against `reference/nist-800-53r5.txt`, 3.11.1 against `nist-800-171r2.txt`, ID.AM-02/ID.IM-01
  against `nist-csf-2.txt` (all verbatim matches).
- **Direct-Support re-verification (12 rows):** each confirmed as namesake-performed within stated scope (§15.3
  composition); the licensing-sensitive claims re-checked: agentless scanning/attack paths/CIEM/data-aware posture
  are Defender CSPM (paid); FIM/OS-baseline/updates/500MB are Servers P2; the dashboard's standards-assignment gate
  is any-paid-plan-except-Servers-P1/APIs-P1; **no Direct claim rests on a paid capability under a free-tier
  license string.**
- **URL resolution: 43/43 distinct new URLs return 200** (42 learn.microsoft.com + the Azure pricing page). **Zero
  WAF blocks this increment.**
- **Rendering** (headless Edge DOM-level + screenshots, light + dark): landing six-product stat line; ISO framework
  view **A.8.16 six-card stack confirmed at DOM level (purview + entra + defender ×2 + sentinel + mdc — the first
  six-product stack)** and the A.5.36 Compliance-Manager-beside-Dashboard pair confirmed visually; Product Pivot
  Defender for Cloud page (40 mappings, 5 solution cards with per-solution counts, product-notes block rendering the
  full mapping discipline); **solution filtering confirmed: the Regulatory Compliance Dashboard solution page shows
  exactly its 8 primary rows**; Density Matrix six-product with Defender for Cloud column; consumption chips render
  (12 on the ISO page). Print-to-PDF on the 800-171 view produced a 1.5 MB fully-expanded dossier.

### 15.6 Add-a-product template verdict — HELD (4th clean clone); ROADMAP CLOSURE
Fourth clean clone: structured `prow`/`rel`, product-tagged SOLUTIONS with derived lists, per-module `mr()` append
blocks, `MDC_LIC`/`MDC_URLS`/`MDC_GOV`, RELATED_PRODUCTS graduation, exact-ref stacking (§13.6 #1 applied at
'5.2.1–5.2.2', '3.11.2–3.11.3', '3.12.1, 3.12.3', '§164.312(c)'), ≥1-primary-per-solution (§13.6 #2 by design), the
consumption `_LIC` pattern (§14.6 inheritance verbatim), seam discipline, and framework-metadata extension all
worked without rework or template changes. The three §14.6 inheritance items were all exercised: consumption `_LIC`
✓, free-alert-ingestion crossover ✓, three-way XDR+Sentinel seam ✓.

**Roadmap-closure audit (no product will ever be added again):**
- **Forward links pointing at never-to-be-authored products:** exactly one slug remains in `RELATED_PRODUCTS` —
  **`priva` (11 contributing links, 0 primary, on 10 privacy-domain rows:** dpr-f14-22, iso-a-5-34 ×2, soc2-p1-p3,
  soc2-p4-1, soc2-p5, gdpr-15/17/20/25/30). **Decision: keep as a permanent reference-only product, not converted
  to plain notes** — the `RELATED_PRODUCTS` mechanism renders these correctly without a product page, all 11 are
  contributing (nothing implies a promised future row), and flattening them to free text would discard structure
  for no benefit. Documented in the `common.py` comment and README. **Zero structured links point at
  `defender-cloud` from anywhere** (verified in QA) — nothing dangles.
- **Whole-atlas consistency-pass checklist** (for the next session — NOT performed here): see §15.7.

**Defender for Cloud addition verdict: SHIP.** 378/378 rows verified; five prior products untouched; 5/5 free-text
entry points stacked; all four views six-product; the dashboard caveat carried on 8/8 rows; roadmap complete.

### 15.7 Whole-atlas consistency-pass checklist (produced at roadmap closure; execute before publishing)
1. **Stale cross-product phrasing sweep:** grep all row text and FRAMEWORK/solution/product notes for "future
   product", "separate product", "not yet", and product counts — the five prior-product free-text mentions of
   Defender for Cloud as "separate product" (rows_iso 520/561, rows_csf 339, rows_pci 292, rows_dpr 298) are still
   *true* but predate the stacked rows; decide whether to normalize them to "(the stacked Defender for Cloud row)"
   — this touches prior-product row content, so it must be a declared, whole-atlas edit with its own drift ledger.
2. **Intent-string variants at stacked refs:** the grouped view renders variant intents when stacked rows differ;
   sweep all multi-product refs for unintended intent drift (deliberate variants exist, e.g., A.5.3).
3. **Terminology normalization:** "Microsoft cloud security benchmark" capitalization; en-dash vs hyphen in
   multi-ref strings; "Azure Government" (MDC) vs "GCC High/DoD" (M365 products) in industry notes — ensure no
   sentence implies the M365 gov taxonomy applies to Azure resources or vice versa.
4. **Coverage-tier symmetry audit at stacked controls:** confirm each stack's tier spread is intentional (e.g.,
   malware: MDE Direct / Intune Partial / MDC Partial; assessment: CM Evidence-or-Partial / dashboard Direct-or-
   Partial) and add a one-line rationale where a reader might infer inconsistency.
5. **Oldest-content recency sample:** Purview rows carry last_verified 2026-07-16 (oldest in the atlas); before
   publishing, re-verify a sample of Purview licensing strings (Purview Suite naming, DSPM current-version state)
   and the two documented WAF-blocked URLs (§7.2).
6. **Dependency-migration flagged segments:** re-review the 27 flagged platform-token external segments
   (BitLocker/Key Vault/SharePoint/M365 encryption) — confirm each should remain external now that the product set
   is final (none should become structured links; Key Vault/platform items align with the §15.1 boundary).
7. **Cross-document count reconciliation:** FRAMEWORK-SELECTION.md, README, and the JSON meta all cite totals —
   reconcile at 378/11/6 and the per-framework counts; confirm `VERIFIED_DATE` (2026-07-16 default) is still the
   right meta default when most rows carry later per-row dates.
8. **Search and pivot spot-checks for the new vocabulary:** "CSPM", "CIEM", "attack path", "MCSB", "FIM" should
   surface the right rows product-aware; confirm no solution-name collisions in the flat SOLUTIONS registry
   (verified none exist today — 38 unique keys across 6 products).
9. **Print dossier full pass:** one print-to-PDF per framework (only spot frameworks were smoke-tested at each
   increment); verify six-product stacks paginate cleanly.
10. **Licensing-volatility triggers parked in README:** Intune July-2026 restructure settling, MDO P1-in-E3
    rollout, Sentinel 50 GB tier GA status, MDC dashboard standards churn (800-171 R3), and the MDC gov gap list —
    execute the re-verification batch as part of the publishing pass.

## 16. Whole-atlas humanization pass (2026-07-18) — declared prose edit across all six products

A style-only pass removing machine-writing tells from the atlas prose, run at the user's direction via the
agentic-humanizer workflow (Core mode; no on-device detector available on this platform). **This is the first
declared edit to prior products' row prose since each shipped** — the §15.7 item-1 mechanism (a whole-atlas edit
with its own drift ledger) exercised ahead of the consistency pass. User decisions governing the pass: scope =
rendered atlas content + README (AUDIT-FINDINGS §1–§15 untouched as the historical record); **all house formulas
kept** ("the stacked X row", "seam, not overlap", "Boundary:", "Directly implements…", "namesake"); **strict-zero
em dashes** in prose.

### 16.1 What was found (audit before editing)
- **697 em dashes** in rendered content (673 spaced), across 241 of 378 rows plus the registry/notes strings —
  the dominant tell by two orders of magnitude. **5 ALL-CAPS emphasis runs** in the sentinel/defender-cloud
  product notes. **43 tailing negations** (retained where they state claim boundaries). Classic AI-vocabulary,
  "-ing" tack-ons, copula avoidance, filler, signposting, and curly quotes: **zero genuine instances** — every
  "crucial" hit is Microsoft's own feature name (Audit Premium "crucial events"), protected as product terminology.
- All 47 en dashes are numeric/reference ranges (21 in `control_ref` — load-bearing for stacking — plus 26 range
  mentions like "Arts. 15–20"); ranges are exempt and untouched.

### 16.2 What was changed
- **Every prose em dash replaced** (period/comma/colon/semicolon/parentheses chosen per sentence) across all 11
  row modules, `common.py` (PRODUCTS notes, all 38 SOLUTIONS scopes, LIC/GOV dicts), `assemble.py` (INDUSTRIES
  notes, FOOTER_LINES, BRAND tagline), `template.html` UI copy (separators normalized to the existing `·` idiom),
  and README.md. The 5 ALL-CAPS runs sentence-cased ("Sentinel evidences and detects; it does not enforce").
  Boundary-row placeholder values `"—"` → `"n/a"` (21 fields); the template's empty-value fallback → "None
  recorded". Shared `control_intent` strings edited identically across stacked rows via count-asserted
  replacements, so no group gained intent variants (verified: zero groups lost intent consistency).
- **Deliberate keeps (3 rendered em dashes remain):** the official document titles "ISO/IEC 27001:2022
  Information security management systems — Requirements" and SOC 2's "…(With Revised Points of Focus — 2022)"
  (title + version string) — proper names under the secondhand-text carve-out.
- **Kept by decision:** all house formulas and claim-boundary negations ("assesses and detects, it does not
  remediate"; "a technical assessment, not an attestation"); "crucial events"; every fact, number, URL, control
  ref, solution name, coverage/confidence value, and licensing claim.

### 16.3 Drift ledger and verification
- Baseline snapshot: **`reference/baseline-pre-humanization.json`** (the 378-row pre-pass state).
- Post-pass: 378 rows, id sets identical; **0 diffs on protected fields** (product, framework, framework_version,
  control_ref, purview_solution, also_involves, coverage, confidence, licensing_model, status, last_verified,
  sources); `related_microsoft` structure (product/role/solution) unchanged on all rows (notes are prose and were
  edited); coverage and confidence distributions byte-equal to §15.
- **Prose footprint: 264 of 378 rows edited** — how_it_supports 222, capability_detail 67, rel notes 68,
  license_requirement 60 (via shared LIC constants), control_intent 41, cloud notes 29, external_dependencies 13,
  evidence examples 17. `legacy_dependencies` mirrors the 13 Purview source-string edits (the original xlsx
  strings remain in `reference/dependency-migration-log.json` and the baselines); the migration parser was not
  disturbed — no product-family tokens added or removed (proven by the unchanged related_microsoft structures and
  the unchanged 150-migrated/27-flagged migration stats).
- Rebuild green at 378/11/6; rendered ISO view shows exactly 1 em dash (the ISO title) with all 57 cards rendering.
- **Gate note for future sessions:** prose-field comparisons now anchor to `baseline-pre-humanization.json` (or
  later); `baseline-pre-refactor.json` remains valid for structure/ids/protected fields but Purview prose
  intentionally differs from it as of this pass.

---

## 17. Content-consistency + de-consulting editorial pass (2026-07-18) — Tier-1 prose only

A two-task editorial pass run at the user's direction, proposed in `CONTENT-REVIEW.md` (Phase 1, report) and
applied here (Phase 2) after explicit approval of all 26 findings (**CR-001…CR-026**). **Task A** normalized the
length/depth of presentation-layer prose (industry/product/solution/framework descriptive text); **Task B** removed
the consultant-reader lens so the atlas reads equally for an in-house engineer, a consultant, or a curious reader.
**Scope was Tier-1 (presentation layer) + README only.** Tier-2 row narratives (`control_intent`,
`capability_detail`, `how_it_supports`, evidence fields) were audited and reported (CONTENT-REVIEW §4) but
**deliberately not edited** this pass — the same discipline as §16's row/registry split. AUDIT-FINDINGS §1–§16
untouched (historical record).

### 17.1 What was changed (files and findings)
- **`build/assemble.py`** — `INDUSTRIES`: 9 of 10 notes rewritten to a common shape (S1 anchor frameworks + who it
  applies to; then per-product hooks only where a genuine story exists). Four stubs expanded (K-12 14→54w,
  Manufacturing 9→51w, Higher-ed 21→72w, MS-supplier 14→63w); five long notes tightened (DIB 166→118, Healthcare
  121→100, Federal 120→113, Finserv 110→99, Retail 109→99). SaaS (59w) already in band, left as-is.
  `FOOTER_LINES[3]` and `META["disclaimer"]`: "verify at engagement time" → "verify before relying on it" (B).
- **`build/common.py`** — `PRODUCTS` notes: Purview expanded (27→69w); Defender XDR / Sentinel / Defender-for-Cloud
  compressed (130→118, 193→124, 222→151), with deep licensing/meter detail left in the `*_LIC` strings rather than
  deleted; Sentinel "Cost levers that matter **to clients**" → "Cost levers that matter" (B). `SOLUTIONS` scope:
  5 short Purview scopes expanded to a floor; 11 long Defender/Sentinel/Defender-for-Cloud scopes trimmed by removing
  connective wording only (every named capability preserved). One non-rendered code comment de-consulted (CR-025).
- **`build/template.html`** — landing hero (B): "Start from **the client's world**" → "Start from an industry";
  "Pick **the client's** industry, drill into the frameworks **they** answer to" → "Pick an industry, open the
  frameworks it answers to".
- **`build/rows_80053.py`** — `FRAMEWORK["notes"]` trimmed 155→123w: dropped inline authoring-date provenance and
  connective redundancy; **every per-product control-ref list preserved** (the ≤60w target was not forced because
  reaching it would drop factual control refs — flagged, not cut).
- **`build/rows_171.py`** `FRAMEWORK["notes"]`, **`build/rows_glba.py`** CM-template note: "at engagement time" →
  "before relying on it" (B).
- **`build/rows_soc2.py`** `FRAMEWORK["applies_to"]`/`["notes"]` (CR-020, DECISION): SOC 2's domain-correct
  "engagement" softened to "examination" per the approved apply-all instruction (reversible; the term is accurate
  for in-house teams and consultants alike).
- **`README.md`** (B): "engagement-agnostic" → "role-agnostic"; "This client operates in industry X" → "An
  organization operates in industry X"; "encouraged where consultants will ask" → "where the question comes up";
  "in CMMC engagements" → "in CMMC assessments"; "the deliverable" → "the output" (×2).

### 17.2 Deliberate keeps (false positives preserved)
Not consulting-lens; changing them would alter meaning or introduce error, so left verbatim:
- **SSPA-DPR row bodies (×11):** "engagement" = the supplier's contracted work for Microsoft ("engagement data" ≠
  "organization data"). Row `soc2-cc5-…` "before analyst **engagement**" = ordinary English; `rows_80053.py:612`
  "in any 800-53/CMMC engagement" = compliance effort (Tier-2, report-only). **13 row-body "engagement" tokens,
  count unchanged.**
- "**advisory**" (Defender-for-Cloud posture recommendations), "**advisors**" (financial advisors, GLBA
  `applies_to`), "native/mobile **clients**" (software clients, MDCA scope), FERPA "**advising**" (academic
  advising) — all domain-correct.

### 17.3 Length results (rendered word counts)
| Content type | Before | After | Note |
|---|---|---|---|
| Industry notes | 9–166 | 50–118 | stubs eliminated; range σ collapsed |
| Product notes | 27–222 | 69–151 | 3 densest stay >110 (factual discipline/boundary text; not padded) |
| Solution scope | 9–109 | 12–84 | longest = the dashboard's factual standards list |
| Framework notes | 25–155 | 25–123 | 800-53 outlier reduced |

Where a passage could not reach the target ceiling without dropping a factual claim (CR-006 DIB, CR-010 product
notes, CR-011 long scopes, CR-012 800-53 note), trimming stopped at the last fact-preserving point — the CR-006/
CR-010 **DECISION** the user pre-approved ("stop before dropping a claim").

### 17.4 §16 em-dash invariant — checked and preserved
The Task-A/B rewrites reintroduced **19 prose em dashes across 15 rendered fields**, regressing §16's strict-zero-
em-dash-in-prose rule. All 19 were replaced with §16-style punctuation (comma/colon/semicolon/parentheses) before
finalizing. **Rendered em dashes are back to exactly the 3 documented keeps** (ISO title, SOC 2 title, SOC 2
version string). No new AI-writing tells introduced (claim-boundary negations like "assesses and detects, it does
not remediate" kept, per §16). Paraphrase rule intact: additions reference only control identifiers (§164.310,
CA-7, 3.3.1, etc.), never verbatim ISO/AICPA/PCI/NIST text.

### 17.5 Drift ledger and regression gate — PASS
- Baseline for protected fields: session-start snapshot of all 378 rows (13 protected fields: coverage, confidence,
  license_requirement, licensing_model, sources, status, last_verified, control_ref, product, purview_solution,
  also_involves, framework, framework_version).
- **Row count 378** (per-product **Purview 150 · Entra 48 · Intune 41 · Defender XDR 53 · Sentinel 46 · Defender
  for Cloud 40** — all unchanged); **id sets identical**; **0 diffs on protected fields**.
- **Tier-2 row prose untouched by construction:** no `ROWS` list was edited (all row-module edits were to the
  `FRAMEWORK` metadata dicts only); corroborated by row-field em-dash count unchanged at 0 and the 13 domain-correct
  row-body "engagement" tokens preserved. (The 517-field delta vs `baseline-pre-humanization.json` is §16's
  footprint, predating this session, not this pass.)
- Rebuild green: `assemble.py` + `build_html.py` → **378 rows / 11 frameworks / 6 products**; app JS compiles;
  embedded-JSON ↔ JSON row counts reconcile at 378.

**Pass verdict: SHIP.** Editorial-only; zero drift on coverage/confidence/licensing/sources/status/dates/refs/
product-solution assignments; §16 prose invariant preserved; Tier-2 normalization remains a separately-approvable
future pass (CONTENT-REVIEW §4).

---

## 18. Progressive-disclosure restructure (2026-07-19) — Tier-1 *depth*, not density

Follow-up to §17. §17 made the top-level prose consistent in *density* but at the wrong *depth*: industry/product/
framework descriptions became 98–151w walls of control citations (§164.312(b), 3.11.2–3.11.3), SKU/meter strings, and
scope caveats sitting at the top level. This pass **relocates that depth behind a collapsed toggle** — a plain 25–52w
summary on top, the full original text one interaction away — **deleting nothing**. Proposed in `CONTENT-REVIEW.md`
(2026-07-19 section, finding IDs **PD-001…PD-064**) and applied here after approval of all findings plus the three
DECISIONs (PD-001 relocate the pivot explainer to the index; PD-014/PD-017 split the two sub-55w industry notes for a
uniform grid; PD-040..043 split the four long Defender-for-Cloud scopes). **Scope: Tier-1 presentation prose only.**
Row bodies (`ROWS`) untouched by construction — 0 rows changed.

### 18.1 What changed (files and mechanism)
- **Data-model split (24 fields).** For each split field the existing key becomes the **summary** and the *verbatim
  original* is moved to a new sibling `_detail` key — done by **renaming the existing multi-line string literal's key**
  (never retyping it), so every `_detail` is byte-identical to the pre-edit value.
  - `build/assemble.py` — `INDUSTRIES` ×10: `note` → 39–49w summary; `note_detail` = original (50–118w).
  - `build/common.py` — `PRODUCTS` ×6: `notes` → 41–52w summary; `notes_detail` = original (69–151w). `SOLUTIONS` ×4
    (the four Defender-for-Cloud scopes >55w: Regulatory Compliance Dashboard, Defender for Servers, Workload
    Protection Plans, Defender CSPM): `scope` → 18–25w summary; `scope_detail` = original (62–84w).
  - `build/rows_{hipaa,171,80053,ferpa}.py` — `FRAMEWORK["notes"]` ×4 (the >55w notes): `notes` → 36–44w summary;
    `notes_detail` = original (57–123w). The **7 short framework notes (≤48w) were left untouched** — already
    single-idea summaries; splitting would create empty details. `applies_to` / `full_name` untouched.
- **Template (`build/template.html`).**
  - New shared helper `detailToggle(detail, label)` → emits a collapsed `<details class="disclose">` only when a
    `_detail` exists; the summary stays in its native container (`.full` / `.callout`). Wired at four page sites:
    `vIndustry` (`note_detail`, "Full industry notes"), `vProduct` (`notes_detail`, "Full mapping notes"),
    `vFramework` (`notes_detail`, "Full framework notes"), `vSolution` (`scope_detail`, "Full scope"). Cards render
    the summary only (they are already click-to-navigate; no nested toggles).
  - New `.disclose` CSS uses only existing theme tokens (`--rule`, `--paper-2`, `--ink-2/3`), so light/dark are
    automatic; the chevron reuses the global `details[open] .flip` rotation.
  - **Print integration** mirrors the existing `details.row` path: the `@media print` `::details-content` rule and the
    `beforeprint`/`afterprint` handlers now target `details.row, details.disclose`, so toggles auto-expand in print.
  - Native `<details>` ⇒ no JS to toggle, works offline from `file://`, zero new dependencies.
- **Boilerplate (PD-001).** The "One configuration, many frameworks…" sentence was **already a single template string**
  (`template.html`, `vProduct`), *not* duplicated in any product's `notes` — so there was no per-field duplication to
  remove. It re-rendered on all six product pages (a UX repeat). Extracted to a named constant `PIVOT_EXPLAINER` and
  rendered **once** on the Products **index** (`vProducts`); each product page now leads with its own summary. The
  deictic "each solution below" was adapted to "Open a product below…" to fit the index context (necessary consequence
  of the relocation; meaning preserved). The other cross-field repeats (PD-060..064) are the same *fact* in two
  distinct navigation contexts; the split already demotes them into the collapsed layer, so they were kept in context,
  not force-consolidated.

### 18.2 Regression gate — PASS (275 automated checks + runtime render + JS parse)
Baseline: pre-edit `compliance-atlas.json` snapshot.
- **Rows:** 378 total; per-product **Purview 150 · Entra 48 · Intune 41 · Defender XDR 53 · Sentinel 46 · Defender for
  Cloud 40** (unchanged); id sets identical; **0 rows changed** (full-row equality — no protected-field drift possible).
- **Byte-equality gate:** all 24 `_detail` values are byte-identical to their baseline originals (10 ind + 6 prod +
  4 sol + 4 fw); every summary is genuinely rewritten (additive). Word-count accounting: summary + detail ≥ original
  holds for all (summary is additive; detail = original).
- **Non-split fields unchanged:** the 7 short framework notes, all `applies_to`/`full_name`, all non-Defender-for-Cloud
  solution scopes, industry framework-lists, and product metadata (names, licensing_source, solutions) all identical.
- **§16 em-dash invariant:** em-dash *characters* unchanged at 4, across the 3 documented keep-fields (ISO title,
  which carries two; SOC 2 title; SOC 2 version). **0 introduced** in any of the 24 new summaries (checked per field).
- **Build:** `assemble.py` + `build_html.py` → 378 rows / 11 frameworks / **10 industries** / 6 products; JSON↔HTML
  embed reconcile at 378. App script passes `node --check` (syntax valid).
- **Runtime render (Node DOM stub, real `app.js`):** each split view emits the summary **and** `<details
  class="disclose">` **and** the verbatim detail **and** the correct label; the product page no longer contains the
  old boilerplate; a non-split framework (`gdpr`) and non-split solution (`Audit`) render **no** toggle; the pivot
  explainer appears on the Products index. All assertions green.
- **Offline / theme / print:** structural — native `<details>` (offline toggle, no deps), CSS-variable-only styling
  (dark mode automatic), and the two print handlers extended to `details.disclose` (auto-expand in print, mirroring
  rows).

**Pass verdict: SHIP.** Depth relocated, nothing deleted (every `_detail` byte-equal to its original); zero row-field
drift; §16 prose invariant preserved; scannable card grid restored; the atlas's dense detail survives one click away.

---

## 19. Version control, copyright triage, and licensing (2026-07-19)

Execution of PROJECT-REVIEW roadmap item 1 (findings **PR-040** no version control, **PR-042** copyrighted
documents in the tree, **PR-041** no licence). **No build source or generated output was modified; no rebuild was
run.** The atlas remains at 378 rows / 11 frameworks / 6 products, byte-unchanged.

### 19.1 Copyright triage of `reference/` — performed BEFORE `git init`

Order was deliberate: git history is permanent and this repository is intended to become public, so
redistribution-restricted documents had to leave the tree before any commit existed. **6 of 23 files moved out**
to the sibling directory `../compliance-atlas-reference-private/` (moved, not deleted; they remain available
locally for re-verification passes).

| Excluded file | Basis |
|---|---|
| `AICPA-TSC-2017-2022POF.pdf` · `.txt` | Copyright AICPA; download licence for the recipient's own use. The `.txt` is a derivative and carries the same restriction. |
| `DPR-v12.pdf` · `.txt` | Microsoft supplier-programme document, published for enrolled suppliers, not licensed for third-party redistribution. |
| `pci-dss-401.pdf` | PCI SSC document-library capture. **Also confirmed misnamed** (file begins `<!DOCTYPE html>`, not `%PDF`) — it is the HTML gate page, corroborating §14.5's finding that the local PDF was unusable and that PCI numbering was verified via the Azure Policy initiative page instead. Excluded on both grounds. |
| `purview-service-description.md` | Verbatim Microsoft Learn content under the Microsoft Terms of Use, not an open licence. The live URL is the citation of record in the dataset, so nothing is lost. |

**17 files kept**, all safe to publish: the NIST publications (SP 800-53 R5, SP 800-171 R2, CSF 2.0) and eCFR
extracts (45 CFR 164, 16 CFR 314, 34 CFR 99) as US-government public domain under 17 U.S.C. §105, plus
`hipaa-sections.txt` (derived from public-domain eCFR text) and the project's own generated artifacts
(`baseline-pre-refactor.json`, `baseline-pre-humanization.json`, `dependency-migration-log.json`,
`xlsx-extract.json`).

New file **`reference/SOURCES.md`** records, per file: what it is, its official re-download URL, and its
redistribution status — plus a decision rule for future additions (government publication → commit; standards
body or vendor documentation → never commit; uncertain → treat as restricted).

**None of the excluded documents is a build input.** `assemble.py` and `build_html.py` read only `build/`; these
were human/agent verification inputs. Their absence does not affect regenerability.

### 19.2 Version control established

`git init` on branch `main`; single commit `2f1d38a`, **45 files tracked**.

Verification gate run before pushing anywhere:
- `git status` clean;
- explicit tracked-file scan for all six excluded filenames plus a regex sweep on
  `aicpa|dpr-v|pci-dss|service-description` — **zero matches**;
- tracked PDFs enumerated: the three NIST publications only;
- `.gitignore` backstop tested with `git check-ignore` — all four restricted paths correctly ignored, while the
  public-domain `nist-csf-2.pdf` correctly is not.

The same scan was re-run against the pushed remote tree via the GitHub API: 45 blobs, zero restricted files.

**`.gitattributes` added (`* text=auto eol=lf`).** The working tree was mixed at first commit: the row modules,
`compliance-atlas.html`, `compliance-atlas.json`, and the reference snapshots were CRLF (Python's text-mode write
on Windows), while `assemble.py`, `common.py`, `template.html`, and the documentation were LF. The machine's
global `core.autocrlf=true` would have baked that inconsistency into history. Normalizing to LF means a rebuild
that changes no content produces no diff, which makes `git diff` usable as a drift check alongside the existing
manual ledgers. **Consequence to note:** the generated artifacts' on-disk line endings change at the next
checkout. This is safe — the §16.3 and §18.2 drift gates compare parsed JSON field values, not raw file bytes,
and both artifacts regenerate from `build/`.

### 19.3 Licensing decision (owner: Yazar)

| Scope | Licence | File |
|---|---|---|
| Build code — all of `build/` | **MIT** | `LICENSE` |
| Atlas content, dataset, generated artifacts, project documentation | **CC BY 4.0** | `LICENSE-CONTENT.md` |

A "Licensing" section in `README.md` states the split. **No footer line was added to the artifact** — that is a
`template.html`/`assemble.py` change reserved for the publishing session, per PR-041's roadmap sequencing.

`LICENSE-CONTENT.md` makes the dependency explicit: open licensing of this work is only possible *because* the
atlas paraphrases control intent rather than quoting standards text. That authoring rule is therefore promoted
from an internal discipline to a **licence condition on anyone adapting the atlas** — adapters must not
substitute verbatim standard text for the paraphrases. The licence also disclaims any rights in third-party
framework texts and trademarks, and restates the not-legal-advice / not-an-attestation position.

### 19.4 Remote

Private GitHub repository created via `gh`: **https://github.com/yazarmyint/compliance-atlas**.
Visibility confirmed by `gh repo view`: `"isPrivate": true`, `"visibility": "PRIVATE"`. `main` tracks
`origin/main`; working tree clean and in sync. No credentials stored in the repository.

**Verdict: COMPLETE.** The project is under version control with an off-machine private backup, the permanent
copyright exposure identified in PR-042 is closed before it could be created, and the licence position is
settled. PR-040, PR-041, and PR-042 are resolved. Remaining pre-publish blockers: **PR-001** (keyboard and
screen-reader navigation) and **PR-043** (public name / `working_title`).

## 20. Presentation and metadata quick-wins (2026-07-19)

Execution of PROJECT-REVIEW roadmap item 3 (**PR-043**) and section 5(b) items 8, 9, 10, 11, 14 and 17
(**PR-012**, **PR-010**, **PR-003**, **PR-014a/b**, **PR-046**, **PR-006**, **PR-007**). **All work is in
`build/template.html`, `build/assemble.py` and `build/build_html.py`. No `rows_*.py` module was opened and no
row field was changed** — proven mechanically in §20.9. Accessibility (PR-001, PR-002) was deliberately left
alone even where this session edited adjacent markup; it is the next session.

### 20.1 PR-043 — public name settled

`BRAND.title` = **Compliance Atlas**, `working_title` = **False**, so the header's "· working title" suffix is
gone. `BRAND.tagline` is now the short **"Mapping frameworks to the Microsoft security stack"** and is rendered
as its own element (hero overline, brand tooltip) rather than concatenated into any title string. The
`<title>`/`document.title` base is "Compliance Atlas". The old tagline's substance ("honest about claim
strength") is not lost: it is carried by the hero lede and, from this session, by the taxonomy legend itself.

### 20.2 PR-012 — search index (highest value-per-hour item in the review)

Six fields added to the `hay()` concatenation: `cloud_availability_note`, `config_evidence_example`,
`operational_evidence_example`, `coverage`, `confidence`, `id`.

| Query | Before | After | Rows containing the exact phrase |
|---|---|---|---|
| `gcc high` | 2 | **222** | 216 |
| `azure government` | 2 | **90** | 89 |
| `dod` | 2 | **179** | 179 |
| `direct support` | 8 | **128** | 128 |

Search returns slightly more than the exact-phrase count because it is a term-AND match, not a phrase match
(a row carrying "GCC" and "High" in different sentences matches "gcc high"); the review's acceptance figures of
~216/~89/~179 are the phrase counts and are met exactly. Row ids now resolve: `csf-pr-ps-04-sentinel`,
`hipaa-312-b-sentinel`, `iso-a-8-16-mdc` each return their one row.

§15.7 item-8 spot checks re-run, all still product-correct: **CSPM** 26 → 35 (all Defender for Cloud), **CIEM**
1 → 18 (all MDC), **attack path** 15 → 15 (MDC + Defender XDR), **MCSB** 18 → 25 (all MDC), **FIM** 2 → 2 (all
MDC). FIM stays at 2 because only two rows use the acronym at all; the indexing change suppressed nothing.

### 20.3 PR-010 — the claim taxonomy is now on screen

Three placements, all reading from `META`; **no definition text is duplicated in the template**, so a
definition cannot drift between dataset and UI.

1. **Landing legend** under the stats bar ("How to read a mapping"): four coverage levels, three confidence
   levels, four licensing models, each with its `META` definition, rendered with the live badge/meter/chip
   components so the legend and the rows are visibly the same objects.
2. **Tooltips**: `covBadge()` and `confMeter()` now carry `title="<label> — <definition>"`, and the licensing
   chip gained a tooltip via a new `licChip()` helper (previously it had none).
3. **Compact coverage legend** at the top of the framework view, immediately above the stacked product cards,
   where the Direct/Partial/Evidence distinction is most acute (the PR-013 `PR.PS-04` case).

When the about page is written (PR-044) it must take its definitions from `META` the same way.

### 20.4 PR-003 — per-route `document.title`

`render()` derives a view name per route and sets `"<view> · Compliance Atlas"` at the end of the render; the
landing page keeps the bare brand. Verified across nine routes (§20.8). A `dec()` helper tolerates malformed
percent-encoding in a hash segment rather than throwing.

### 20.5 PR-014(a)(b) — verification currency surfaced

(a) `last_verified` renders as a muted `✓ 2026-07-17` chip in the **collapsed** row summary, so footer line 4's
"currency is governed by each row's last-verified date" is legible without expanding anything.
(b) The hand-maintained `brand.as_of` (already stale at 2026-07-18) is **removed** and replaced by
`meta.verified_range`, computed in `assemble.py` from the rows' own `last_verified` values. The hero reads
"rows verified 2026-07-16 – 2026-07-18" and cannot go stale by construction.

**Not done, deliberately:** `default_last_verified` is untouched (2026-07-16), no row's `last_verified` was
changed, and the re-verification of the 124-row 2026-07-16 Purview cohort remains §15.7 item 5 / PR-014(d) for
its own session. Surfacing the dates makes that cohort's age visible, which is the point.

### 20.6 PR-006, PR-007 — small fixes

`color-scheme: light` on `:root` and `color-scheme: dark` on `[data-theme="dark"]`, so scrollbars and native
form chrome follow the theme. A `<p class="loading">Loading the atlas…</p>` placeholder inside `<main>`, which
`render()` replaces wholesale on first run.

### 20.7 PR-046 — page metadata

`meta.description_meta` is composed in `assemble.py` from the tagline plus the live row/framework/product
counts, so the social and search summary cannot drift from the dataset. `build_html.py` substitutes
`__BRAND_TITLE__` and `__META_DESCRIPTION__` into the head **before** the data payload is inserted (so dataset
content can never be mistaken for a marker), asserting on each marker as it already does for `/*__DATA__*/`.
The head now carries `<meta name="description">`, `og:type`, `og:title`, `og:description`, and an inline SVG
data-URI favicon of the ¶ brand glyph in the accent ink.

**`og:image` deliberately skipped.** It requires an absolute hosted URL, which would cost the zero-external-
asset property that makes the `file://` copy fully self-contained. Confirmed: the built head contains **zero**
non-`data:` `src`/`href` references.

### 20.8 Verification

A Node harness runs the built file's application script against a minimal DOM stub and asserts against the
rendered HTML — 29 checks, 0 failures: nine per-route titles; the landing legend containing all eleven `META`
definitions verbatim; the compact framework legend; `covBadge`/`confMeter`/`licChip` tooltips carrying their
`META` definitions; the `last_verified` chip inside `<summary>` (that is, visible while collapsed); the three
search acceptance counts; row-id search; and the brand strings including the absence of the working-title
suffix.

Rendered checks in headless Chrome from `file://`, confirming the offline path still works end to end:
landing page in **light** and **dark** (legend legible in both; every custom property the new CSS uses is
defined in both theme blocks — checked mechanically, only the two font variables are `:root`-only, which is
pre-existing and correct), and the framework view showing the compact legend and the verification chips in
place without disturbing the row grid.

**Print:** the GLBA framework printed to PDF before and after — **22 → 23 pages**. The single extra page is the
compact legend plus chip reflow; pagination is otherwise unchanged and rows still expand under `beforeprint`.
The full per-framework print pass remains §15.7 item 9.

### 20.9 Gate: the dataset did not move

The `.gitattributes` normalization from §19.2 makes `git diff` a usable drift check, and this is its first real
use. Against the pre-session baseline, `compliance-atlas.json` shows **10 insertions, 6 deletions, all inside
`meta`**:

- `brand.working_title` `true` → `false`
- `brand.tagline` replaced
- `brand.as_of` removed
- `meta.generated` timestamp bumped
- `meta.verified_range` and `meta.description_meta` added

Parsed deep-equality against the baseline confirms **`rows` identical (378 == 378)**, and `products`,
`related_products`, `solutions`, `frameworks` and `industries` identical. JSON↔HTML reconcile: the embedded
data island parses to an object equal to `compliance-atlas.json`, 378 rows.

**Verdict: COMPLETE.** PR-043, PR-012, PR-010, PR-003, PR-014(a)(b), PR-006, PR-007 and PR-046 are resolved.
With PR-043 cleared, **PR-001 (keyboard and screen-reader navigation) is the last remaining pre-publish
blocker**.

## 21. Keyboard and screen-reader accessibility (2026-07-19)

Execution of PROJECT-REVIEW roadmap item 2 (**PR-001** navigation is inaccessible, **PR-002** the whole
`<main>` is an `aria-live` region), plus two findings this session's tooling discovered that the review had
missed (**PR-055** nested interactive controls, **PR-056** colour contrast). **All work is in
`build/template.html`. No `rows_*.py` module was opened, `assemble.py` and `build_html.py` were not modified,
and no row field changed**, proven mechanically in §21.7. With this section closed, the atlas has no
remaining pre-publish accessibility blocker.

### 21.1 Tooling established

Prior sessions verified rendering with a Node DOM stub and ad-hoc headless Chrome runs. This session needed
repeatable assertions about focus, so a harness was built on **puppeteer-core driving the installed Chrome**
(no bundled browser download) with **axe-core 4.x**, plus `pixelmatch`/`pngjs` for render comparison and
`pdf-lib` for real page counts. Five scripts, all run from `file://`:

| Script | What it proves |
|---|---|
| `axe-run.mjs` | WCAG 2.1 A/AA sweep over 11 routes x 2 themes = 22 combinations |
| `keywalk.mjs` | The seven required journeys using only Tab/Shift+Tab/Enter/Space key events |
| `mouse.mjs` | Card and cell hit areas, hover styles, row disclosure by real mouse events |
| `shots.mjs` + `compare.mjs` | Full-page renders and element geometry, before vs after |
| `print.mjs` + `pages.mjs` | The beforeprint/afterprint path and A4 page counts |

### 21.2 The baseline was worse than PROJECT-REVIEW recorded

Running axe **before** editing anything produced **1,567 violation nodes** in two rules. PR-001 predicted the
keyboard problem correctly, but the review, written without running a browser, could not see either of these:

| Rule | Nodes | Cause |
|---|---|---|
| `color-contrast` (1.4.3 AA) | 907 | Six palette tokens under 4.5:1, **not flagged anywhere in PROJECT-REVIEW** |
| `nested-interactive` (4.1.2 A) | 660 | Every row `<summary>` carried the solution chip as a link |

Both were put to the owner as scoped decisions rather than absorbed silently, because each carried a real
cost: the nesting fix removes a click affordance, and the contrast fix moves a deliberately tuned palette.
Both were authorised. This is why the section covers four findings, not two.

### 21.3 PR-001 - real, focusable, activatable navigation

Every click-only navigation element is now a true link. A sweep of `onclick` across the template audited all
eleven hits; after the change the only survivors are button behaviour (`window.print()`, expand/collapse,
`setFwFilter`), and **zero** contain `location.hash`.

- **Cards** (industry, framework on two views, product, solution) are `<a class="card">` with `display:block`.
  The whole card remains the click target, verified by clicking **nine points** across a card including all
  four corners and the minibar, all navigating. Each card carries an `aria-label` of its heading, so tabbing a
  link list reads as headings rather than whole card bodies.
- **Matrix cells** are `<td><a>` with the anchor filling the cell (measured 54x38 link in a 54x38 cell).
  Cell links are named "row x column: n row(s)"; a bare "12" carries nothing out of context. Empty cells keep
  the decorative dot and expose a plain "0".
- **Table semantics**: the corner cell is a `<td>` (it heads nothing), every `<th>` carries `scope`, bottom
  totals are `<td>`, and each table is named with `aria-label`. A visually-hidden `<caption>` was tried first
  and rejected: Chrome reserves a border-spacing gap for the caption box even when it is absolutely positioned,
  which pushed the table body down 2px.
- **Brand** is an `<a href="#/">`.
- **Skip link** is the first focusable element, revealed on focus, `position:fixed` so it cannot shift layout.
  It moves focus itself rather than letting the browser navigate to `#app`, because **the hash router would
  otherwise parse `app` as a route and render "not found"**. Confirmed: after activation the route is still `#/`.
- **Focus visibility** uses the search field's focus ink on every interactive element. `--link` clears 4.5:1
  against paper in both themes, so the ring is visible in each. It is drawn **inset** on row summaries, which
  `details.row` would otherwise clip via its `overflow:hidden`.
- **Non-navigation controls audited**: theme and print buttons gained accessible names with their glyphs
  marked `aria-hidden`, and the theme button's name states what activating it will do and follows the state;
  coverage filters gained `aria-pressed`; all buttons are `type="button"`; `<details>` summaries were already
  native and keyboard-operable. Tabs mark the active route with `aria-current="page"`.

### 21.4 PR-002 - screen-reader announcement model

`aria-live` is removed from `<main>`. In its place:

- Focus moves to the view's `<h1>` (`tabindex="-1"`, no visible ring) after each render, which is what actually
  relocates a screen reader's reading cursor into the new view.
- **Except on first paint**, where focus stays at the top of the document so the skip link is the first Tab
  stop and nothing talks over the browser's own page-load announcement. Verified: on a fresh load the status
  region is empty and one Tab lands on the skip link.
- A visually-hidden `role="status" aria-live="polite"` region announces view plus content, for example
  "NIST CSF 2.0 - 40 mappings". Row-listing views count the **rendered DOM**, so the number announced is the
  number on screen; index views count what they list.
- The coverage filter re-render restores focus to the button that was pressed instead of dropping it to
  `<body>`, and re-announces: "NIST CSF 2.0 - 12 mappings, filtered to Direct Support".
- **Loading placeholder sanity-check (requested explicitly):** it sits outside any live region and is replaced
  before the first announcement, so it cannot be announced at all.

### 21.5 PR-055 (new) - no interactive controls nested in row summaries

Chips rendered inside a `<summary>` are now plain spans; the same destinations are real links in the expanded
row body's foot line via a new `solLinks()` helper, beside the framework link already there. Collapsed rows are
visually unchanged, because `.chip.sol` and `.chip` already set their own colour, so the anchor contributed
nothing but a hover underline.

**Accepted behaviour change:** a mouse user can no longer jump to a solution from a *collapsed* row and must
expand it first. Chosen over restructuring `<details>`/`<summary>` into a div plus an `aria-expanded` button,
which would have cost click-to-expand on the row body and the native `beforeprint` expansion path.

### 21.6 PR-056 (new) - colour contrast meets WCAG 1.4.3 AA

907 nodes reduced to six root causes, all near-misses. Each value was solved against **every** surface the
token is actually used on (card, paper, paper-2, heat-0), not just one:

| Token | Was | Now | Worst ratio after |
|---|---|---|---|
| `--ink-3` light | `#8a8f99` (3.03) | `#656870` | 4.59 |
| `--ink-3` dark | `#7c818c` (3.97) | `#8a8f99` | 4.54 |
| `--evidence` light | `#96690f` (4.13) | `#8d630e` | 4.57 |
| `--evidence` dark | `#b3861f` (4.27) | `#b68b28` | 4.52 |
| `--direct` dark | `#35a370` (4.30) | `#3da776` | 4.52 |
| `--nocover` light | `#6e6a63` (4.47) | `#6d6962` | 4.55 |

The **matrix heat ramp** needed more than a nudge and is the one genuine design change in this session. Its
figures flipped from `--ink` to `--heat-txt-hi` above 55% of max, and both sides of that flip failed. Solving
it showed **no threshold can work at the old 86% ramp top**: past roughly 62% the mixed background lands in a
luminance band where neither a near-black nor a near-white figure reaches 4.5:1. The ramp is therefore capped
at **55% `--partial`** and every cell keeps a single `--ink` figure; `--heat-txt-hi` is deleted as dead. The
`.6` exponent is unchanged so the low end still separates. Worst case across the whole ramp is 5.53 light and
4.70 dark, and 55% is the ceiling: 58% already fails at 4.48. Empty cells move from `--ink-3` at 0.55 opacity
(1.66:1) to `--ink` at 0.7 (5.29 light / 6.32 dark) and stay recessive.

### 21.7 Gate

**1. Dataset did not move.** `git diff` on `compliance-atlas.json` against the pre-session commit shows
**one changed line, `meta.generated`**. Parsed deep-equality confirms `rows` identical (378 == 378), and
`products`, `related_products`, `solutions`, `frameworks` and `industries` identical, with no `meta` key added
or removed. JSON to HTML reconcile: the embedded data island parses to an object equal to the JSON, 378 rows.

**2. axe-core, WCAG 2.1 A/AA.** All four view types plus the ISO 27001 framework page (57 rows, 16 controls
carrying stacked multi-product cards, max stack 5), the Audit solution page, and the product, matrix-drill,
cell and search views. 11 routes x light and dark:

```
ZERO violations at WCAG 2.1 A/AA across 22 page/theme combinations.
   baseline:  color-contrast      907 nodes  ->  0
              nested-interactive  660 nodes  ->  0
```

**No violations were suppressed and none are being reported as false positives.** The sweep is a true zero.

**3. Keyboard walk**, fresh load, only Tab/Shift+Tab/Enter/Space, focus logged at every step:

```
[ 1] fresh load                    (document body)
[ 2] Tab #1                        a[href="#app"]  "Skip to main content"      <- (a) first stop
[ 3] Enter on skip link            main            (route still #/, not hijacked)
[ 4] +1 Tab                        a[href="#/industry/healthcare"]             <- (b)
[ 5] Enter                         h1 "Healthcare & life sciences"   announced "... - 5 frameworks"
[ 6] +2 Tab                        a[href="#/framework/hipaa-security"]        <- (c)
[ 7] Enter                         h1 "HIPAA Security Rule"          announced "... - 32 mappings"
[ 8] +10 Tab                       summary "Purview Data Classification + DSPM ..."   <- (d)
[ 9] Enter                         row open; Enter collapses; Space also toggles
[10] +6 Tab                        button[aria-pressed=false] "Direct Support (7)"    <- (e)
[11] Enter                         32 -> 7 rows; focus stayed on the pressed button;
                                   announced "HIPAA Security Rule - 7 mappings, filtered to Direct Support"
[12] Shift+Tab                     button "All (32)"; Space restores all 32 rows
[13] +46 Tab                       button "Switch to light theme"                     <- (f)
[14] Enter                         dark -> light; name follows state; Space toggles back
[15] +1 Tab (on #/matrix)          a "Microsoft SSPA DPR x Purview: 15 row(s)"        <- (g)
[16] Enter                         h1 "Microsoft Purview density"    announced "... - 150 mappings"
[17] +1 Tab                        a "Microsoft SSPA DPR x Information Protection: 2 row(s)"
[18] Enter                         h1; announced "... - 2 mappings"
```

All seven required journeys were reached and activated by keyboard alone, with no JS errors.

**4. Mouse behaviour unchanged, no layout shift.** Nine points across a card all navigate; the card still
lifts on hover (`translateY(-2px)`), is not underlined, and keeps body ink rather than link blue; the matrix
link fills its cell exactly and clicks land at all three probe points; the cell keeps its hover outline
(none -> solid); clicking a row body still expands it with no stray route change.

Geometry across all 16 page/theme render combinations: **identical document height, and identical position and
size for every card, mapping row, matrix cell, page heading, badge and summary**. On the matrix specifically,
the 66 data cells and 11 row headers are geometrically identical and table width is unchanged. Pixel diffs are
therefore ink shade only: 0.00 to 0.01% on dark non-matrix pages, 0.09 to 0.44% light, and 1.97% light /
0.54% dark on the matrix, which is the intended heat-ramp and figure-colour change from §21.6.

**5. Print and `file://`.** Header, search and icon buttons are still hidden in print; `beforeprint` still
expands every row (21/21, 40/40) and `afterprint` still restores them; the skip link stays off-screen when
unfocused. Zero JS errors from `file://` before or after. A4 page counts: FERPA 8 = 8, NIST CSF 2.0 46 = 46,
matrix 2 = 2, landing 3 = 3, **GLBA Safeguards 22 -> 23**. The single extra page is the `solLinks()` foot line
from §21.5 wrapping on GLBA's longer solution names; it affects the expanded and print state only, never the
collapsed row.

**Verdict: COMPLETE.** PR-001, PR-002, PR-055 and PR-056 are resolved. **The atlas is fully navigable by
keyboard and usable with a screen reader, at a clean zero on WCAG 2.1 A/AA for every check axe can run, in
both themes, across every view type.** The last pre-publish blocker is cleared. Remaining roadmap: PR-044
about page, PR-035/036/037 licensing re-verification, and the §15.7 consistency pass.

**Note for the next session:** PROJECT-REVIEW.md does not yet carry PR-055 or PR-056; they were raised here.
Nothing in axe's automated coverage substitutes for a pass with a real screen reader (NVDA or JAWS), which
remains unperformed. axe checks roughly a third of WCAG success criteria and cannot judge whether the
announcements read *well*, only that the machinery is correct.
