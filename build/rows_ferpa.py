"""FERPA rows — 34 CFR Part 99, verified against eCFR (2026-07-15 issue; local copy reference/ecfr-34-99.txt).
Deliberately slim (5 rows) per FRAMEWORK-SELECTION.md Increment 1: FERPA is an access-and-disclosure-governance
regime, not a security-controls catalog. The student information system (SIS) is the primary education-records
store; Purview's reach covers the M365 collaboration copies (advising files, shared rosters, counseling notes,
email threads) where FERPA exposure actually concentrates."""
from common import LIC, URLS, GOV, VERIFIED_DATE

V2_DATE = "2026-07-17"
ECFR99 = "https://www.ecfr.gov/current/title-34/subtitle-A/part-99"
ED = "https://studentprivacy.ed.gov/ferpa"

FRAMEWORK = {
    "id": "ferpa",
    "name": "FERPA",
    "full_name": "Family Educational Rights and Privacy Act, 34 CFR Part 99 (implementing 20 U.S.C. § 1232g)",
    "version": "34 CFR Part 99, current text (verified against eCFR 2026-07-15 issue; base 53 FR 11943 as amended)",
    "authority": "US Department of Education, Student Privacy Policy Office",
    "official_source": ECFR99,
    "document_url": ED,
    "compliance_manager_template": {"exists": True, "name": "US - Family Educational Rights and Privacy Act (FERPA) (premium)",
        "note": "Re-verified on the Compliance Manager regulations list 2026-07-17.",
        "source": URLS["cm_regs"]},
    "domains": ["Subpart B: Right to inspect & review", "Subpart D: Disclosure & recordkeeping"],
    "applies_to": "Educational agencies and institutions receiving US Department of Education funds (K-12 districts and postsecondary institutions)",
    "notes": "Why the FERPA rows are lighter than most: the law prescribes almost no specific technical safeguards, so the mapping leans toward labeling and access controls and rates mostly partial or evidence-only. The registrar's student-information system stays the system of record throughout.",
    "notes_detail": ("FERPA sets almost no prescriptive technical safeguards; §99.31(a)(1)(ii) itself frames the choice as 'physical or "
              "technological access controls' versus an effective administrative policy, which is exactly where the labeling/DLP story "
              "lands. Rows skew Partial/Evidence by design; the SIS and registrar processes remain the primary record store and system "
              "of record throughout. Watch item: ED signaled intent (Fall 2024 Unified Agenda) to propose FERPA regulation amendments; "
              "no NPRM published as of 2026-07-17."),
}

def row(id, ref, domain, intent, sol, cap, how, cfg, op, deps, cov, conf, lic, cloud, sources, also=None):
    return {
        "id": id, "product": "purview", "framework": "ferpa",
        "framework_version": "34 CFR Part 99 (current)", "control_ref": ref, "control_domain": domain,
        "control_intent": intent, "purview_solution": sol, "also_involves": also or [],
        "capability_detail": cap, "how_it_supports": how,
        "config_evidence_example": cfg, "operational_evidence_example": op,
        "non_purview_dependencies": deps, "coverage": cov, "confidence": conf,
        "license_requirement": lic, "cloud_availability_note": cloud,
        "sources": sources, "status": "verified", "last_verified": V2_DATE,
    }

ROWS = [
    row("ferpa-99-10", "§99.10", "Subpart B: Right to inspect & review",
        "Give a parent or eligible student the opportunity to inspect and review the student's education records, responding within a reasonable period and no more than 45 days after the request.",
        "eDiscovery", "eDiscovery search locating a student's education-record content scattered across Exchange, SharePoint, OneDrive, and Teams; export for the review response",
        "Implements the locate/collect step for the M365-resident portion of a records request inside the 45-day clock: advising emails, shared documents, counseling notes that never made it into the SIS. Request intake, identity verification, §99.12 limitation review, and the SIS extract are registrar/process work.",
        "Documented records-request runbook using an eDiscovery case per request",
        "Per-request search and export records with dates against the 45-day window",
        "SIS/registrar extract (primary record store); request intake and verification process; §99.12 redaction review",
        "Partial Support", "Medium", LIC["ediscovery_std"], None,
        [ECFR99, ED, URLS["edisc"]], also=["Data Classification"]),

    row("ferpa-99-31-a1ii", "§99.31(a)(1)(ii)", "Subpart D: Disclosure & recordkeeping",
        "Use reasonable methods (the regulation names physical or technological access controls) to ensure school officials access only education records in which they have legitimate educational interests.",
        "Information Protection", "Sensitivity labels with encryption scoping student-record content to authorized official groups; DLP restricting movement outside those groups; IRM flagging anomalous bulk access to student records",
        "Supplies the 'technological access controls' the regulation prefers, for education records living in M365: labeled and encrypted content opens only for officials with the configured interest basis, and out-of-scope movement raises alerts. SIS role-based access and the legitimate-educational-interest criteria themselves are institutional.",
        "'Student records' label tier with encryption scoped to official roles; DLP rules on student-record SITs/label",
        "RMS access-denied events; DLP alerts; IRM anomalous-access cases for student-record stores",
        "SIS role-based access (primary); annual notification defining school-official criteria (§99.7); Entra group hygiene",
        "Partial Support", "Medium", LIC["label_encryption"] + "; " + LIC["labels_auto"] + "; " + LIC["dlp_core"], None,
        [ECFR99, ED, URLS["label_encrypt"], URLS["dlp"]], also=["Data Loss Prevention", "Insider Risk Management"]),

    row("ferpa-99-30-33", "§99.30 & §99.33", "Subpart D: Disclosure & recordkeeping",
        "Obtain signed, dated written consent before disclosing personally identifiable information from education records (outside §99.31 exceptions), and bind recipients against redisclosure without consent.",
        "Data Loss Prevention", "DLP rules guarding student-record content against egress to unauthorized external recipients across email, Teams, and sharing links",
        "Implements the prevention layer under the consent rule: unconsented disclosure paths from M365 are blocked or forced through justification, shrinking the accidental-disclosure surface §99.30 exists to police. Consent capture, exception determinations, and recipient redisclosure obligations are process and contract work.",
        "DLP policy: student-record SITs/label + external recipient → block with override justification",
        "Blocked/justified external-send events for student-record content",
        "Consent workflow and records; §99.31 exception determinations; disclosure agreements binding recipients (§99.33)",
        "Partial Support", "Low", LIC["dlp_core"], None,
        [ECFR99, ED, URLS["dlp"]], also=["Information Protection"]),

    row("ferpa-99-32", "§99.32", "Subpart D: Disclosure & recordkeeping",
        "Maintain, with each student's education records, a record of each request for access and each disclosure (requesting parties, their legitimate interests), kept as long as the records themselves.",
        "Audit", "Unified audit log of access and sharing events on student-record content in M365; retention labels keeping the disclosure log itself for the required period",
        "Evidences who accessed and shared M365-resident student-record content, feeding the formal §99.32 disclosure log, and enforces the log's own keep-as-long-as-the-records retention. The maintained log itself (tied to each student's records with parties and interests) is a registrar/SIS artifact.",
        "Audit enabled with retention policy; retention label on the disclosure-log library",
        "Audit extracts of access/sharing events reconciled to the disclosure log",
        "Registrar-maintained disclosure record (primary); SIS access logging",
        "Evidence Support Only", "Medium", LIC["audit_std"] + "; " + LIC["audit_prem"] + "; " + LIC["retention_basic"], None,
        [ECFR99, ED, URLS["audit"], URLS["retention"]], also=["Data Lifecycle Management"]),

    row("ferpa-99-31a6-35", "§99.31(a)(6)(iii)(C) & §99.35(b)(2)", "Subpart D: Disclosure & recordkeeping",
        "Destroy personally identifiable information shared under the studies and audit/evaluation exceptions once it is no longer needed for that purpose.",
        "Data Lifecycle Management", "Retention labels with delete actions (or event-based retention keyed to study/audit end) on the M365 locations holding shared study or evaluation datasets; disposition review producing destruction evidence",
        "Directly enforces the destroy-when-no-longer-needed clock for shared datasets that live in M365 (research collaboration sites, evaluation workspaces) and produces the destruction proof the written agreements call for. Agreement drafting and destruction in recipients' non-M365 environments are outside.",
        "Retention label with end-of-study delete action on study-data sites; disposition review enabled",
        "Deletion/disposition records mapped to study or audit closure dates",
        "Written agreements specifying destruction terms (§99.31(a)(6)(iii)); recipient-side destruction attestation",
        "Partial Support", "Medium", LIC["retention_basic"] + "; " + LIC["retention_advanced"] + "; " + LIC["records"], None,
        [ECFR99, ED, URLS["retention"], URLS["disposition"]], also=["Records Management"]),
]


# ==== Microsoft Entra rows (product #2, added 2026-07-17) ====
from common import ENTRA_LIC, ENTRA_URLS, ENTRA_GOV, prow, rel
_E = "2026-07-17"
def er(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("entra", "ferpa", "34 CFR Part 99 (current)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _E, also_involves=also)

ROWS += [
    er("ferpa-99-31-a1ii-entra", "§99.31(a)(1)(ii)", "Subpart D: Disclosure & recordkeeping",
       "Use reasonable methods (the regulation names physical or technological access controls) to ensure school officials access only education records in which they have legitimate educational interests.",
       "Conditional Access & Authentication",
       "Conditional Access and RBAC restricting access to education-record systems, with access packages/reviews (Entra ID Governance) scoping officials to their legitimate-interest role and MFA authenticating each",
       "Directly provides the 'technological access controls' the regulation prefers for education-record systems integrated with Entra: authentication plus role-scoped access and recertification. The student information system (SIS) is the primary record store and may enforce its own access.",
       "Conditional Access requiring MFA; access packages mapped to school-official roles; access reviews",
       "Sign-in grant/block evidence; access-review records for education-record roles",
       [rel("purview", "contributing", "Sensitivity labels and DLP restrict student-record content in M365 collaboration copies", "Information Protection")],
       "SIS role-based access (primary record store); legitimate-educational-interest criteria and annual notification",
       "Partial Support", "High",
       ENTRA_LIC["ca"] + " Access reviews: " + ENTRA_LIC["gov_core"],
       ENTRA_GOV["ca"],
       [FRAMEWORK["official_source"], ENTRA_URLS["ca"], ENTRA_URLS["access_reviews"]],
       also=["Entra ID Governance"]),
]
