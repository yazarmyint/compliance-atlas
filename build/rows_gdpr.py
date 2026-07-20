"""EU GDPR rows — Regulation (EU) 2016/679. Article subjects verified against the EUR-Lex consolidated text 2026-07-16.
These rows also serve as the annotated analog for the deferred US state-privacy composite (see FRAMEWORK-SELECTION.md)."""
from common import LIC, URLS, GOV, VERIFIED_DATE

EURLEX = "https://eur-lex.europa.eu/eli/reg/2016/679/oj"

FRAMEWORK = {
    "id": "gdpr",
    "name": "EU GDPR",
    "full_name": "Regulation (EU) 2016/679 (General Data Protection Regulation)",
    "version": "Regulation (EU) 2016/679 (consolidated; stable text)",
    "authority": "European Union",
    "official_source": EURLEX,
    "document_url": EURLEX,
    "compliance_manager_template": {"exists": True, "name": "EU GDPR (General Data Protection Regulation) (premium)",
        "note": "Verified on the Compliance Manager regulations list 2026-07-16.",
        "source": URLS["cm_regs"]},
    "domains": ["Art. 5 Principles", "Arts. 15–20 Data subject rights", "Art. 25 By design", "Art. 30 ROPA",
                "Art. 32 Security", "Arts. 33–34 Breach", "Art. 35 DPIA"],
    "applies_to": "Controllers/processors handling EU residents' personal data (extraterritorial scope)",
    "notes": ("Microsoft Priva (Subject Rights Requests, Privacy Risk Management) is the tooled privacy layer and appears only as a "
              "dependency per ground rules. Rows annotated for reuse against US state privacy laws (CPRA and peers) pending the v2 composite."),
}

def row(id, ref, domain, intent, sol, cap, how, cfg, op, deps, cov, conf, lic, cloud, sources, also=None):
    return {
        "id": id, "product": "purview", "framework": "gdpr",
        "framework_version": "2016/679", "control_ref": ref, "control_domain": domain,
        "control_intent": intent, "purview_solution": sol, "also_involves": also or [],
        "capability_detail": cap, "how_it_supports": how,
        "config_evidence_example": cfg, "operational_evidence_example": op,
        "non_purview_dependencies": deps, "coverage": cov, "confidence": conf,
        "license_requirement": lic, "cloud_availability_note": cloud,
        "sources": sources, "status": "verified", "last_verified": VERIFIED_DATE,
    }

ROWS = [
    row("gdpr-5-1-c", "Art. 5(1)(c)", "Art. 5 Principles",
        "Data minimization: personal data must be adequate, relevant, and limited to what the purpose requires.",
        "Data Classification", "Personal-data discovery (EU-relevant SITs, Data explorer) making accumulation visible; DSPM surfacing over-retained/overshared personal data",
        "Evidences whether minimization is holding in collaboration estates and gives the review a concrete target list. Minimization decisions at collection points are application/process design.",
        "EU personal-data SITs scoped; recurring discovery",
        "Trended personal-data footprint reports feeding minimization reviews",
        "Collection-point design; purpose specification (privacy office)",
        "Evidence Support Only", "Medium", LIC["classification_analytics"], None,
        [EURLEX, URLS["data_explorer"], URLS["dspm"]], also=["DSPM"]),

    row("gdpr-5-1-e", "Art. 5(1)(e)", "Art. 5 Principles",
        "Storage limitation: keep personal data identifiable no longer than the purpose requires.",
        "Data Lifecycle Management", "Retention policies/labels enforcing purpose-aligned retention periods with automatic deletion; adaptive scopes for population-specific schedules",
        "Directly implements storage limitation for personal data in M365 workloads. Retention schedule design and non-M365 stores are outside.",
        "Retention policies mapped to the ROPA's retention column",
        "Deletion logs; retention policy inventory",
        "Approved retention schedule; application-store purges",
        "Direct Support", "High", LIC["retention_basic"] + "; " + LIC["retention_advanced"], None,
        [EURLEX, URLS["retention"]], also=["Records Management"]),

    row("gdpr-5-2", "Art. 5(2)", "Art. 5 Principles",
        "Accountability: the controller must be able to demonstrate compliance with the processing principles.",
        "Compliance Manager", "GDPR premium assessment tracking technical/organizational measures; Purview policy configuration + audit trail as demonstrable-compliance artifacts",
        "Supplies a standing, exportable demonstration layer (assessments, control status, policy evidence, activity logs) for the M365 processing estate. Accountability governance (DPO, ROPA, DPIAs) is organizational.",
        "Active EU GDPR assessment; policy exports retained",
        "Assessment reports; audit extracts evidencing control operation",
        "DPO function; ROPA; processor agreements",
        "Evidence Support Only", "Medium", LIC["cm"], GOV["cm"],
        [EURLEX, URLS["cm"], URLS["audit"]], also=["Audit"]),

    row("gdpr-15", "Art. 15", "Arts. 15–20 Data subject rights",
        "Right of access: confirm processing and provide the data subject a copy of their personal data.",
        "eDiscovery", "eDiscovery search/collection locating a subject's personal data across Exchange/SharePoint/OneDrive/Teams; export for response assembly",
        "Implements locate/collect/export for M365 content in access-request fulfillment. Intake, identity verification, redaction of third-party data, and response are process/Priva.",
        "Documented DSR search procedure with eDiscovery case template",
        "Per-request search/export records within the one-month clock",
        "Microsoft Priva Subject Rights Requests (if licensed); line-of-business system search",
        "Partial Support", "Medium", LIC["ediscovery_std"], GOV["edisc"],
        [EURLEX, URLS["edisc"]], also=["Data Classification"]),

    row("gdpr-17", "Art. 17", "Arts. 15–20 Data subject rights",
        "Right to erasure: delete a subject's personal data without undue delay when grounds apply.",
        "eDiscovery", "eDiscovery locating all instances; retention/deletion actions and targeted purge for mail items; documented deletion evidence",
        "Implements find-then-erase for M365 content with an evidence trail. Erasure-grounds assessment, exemption analysis, and app-database deletion are process territory; bulk purge in M365 has product limits worth flagging in design.",
        "Erasure runbook: eDiscovery search → per-location deletion steps → verification search",
        "Before/after search results as deletion proof",
        "Priva SRR (if licensed); application-level deletion; backup-cycle policy statement",
        "Partial Support", "Medium", LIC["ediscovery_std"] + "; " + LIC["retention_basic"], None,
        [EURLEX, URLS["edisc"], URLS["retention"]], also=["Data Lifecycle Management"]),

    row("gdpr-20", "Art. 20", "Arts. 15–20 Data subject rights",
        "Data portability: provide the subject's data in a structured, commonly used, machine-readable format.",
        "eDiscovery", "Collection/export of a subject's content in native formats (PST, native files, load files)",
        "Supports the collection/export step; 'structured machine-readable' delivery for provided-data sets is largely an application/CRM export concern.",
        "Export procedure per format requirements",
        "Export manifests per request",
        "Application-level structured exports; Priva",
        "Partial Support", "Low", LIC["ediscovery_std"], None,
        [EURLEX, URLS["edisc"]]),

    row("gdpr-25", "Art. 25", "Art. 25 By design",
        "Data protection by design and by default: embed technical/organizational measures (e.g., minimization, pseudonymization) into processing.",
        "Information Protection", "Default sensitivity labels, auto-labeling, default-deny DLP posture, and default retention as by-design/by-default technical measures for the collaboration estate",
        "Implements 'by default' concretely in M365: new content lands labeled, protected, retention-bound without user action. System/application design outside M365 is the broader obligation.",
        "Default label policy; auto-labeling; baseline DLP; default retention",
        "Coverage metrics: % content labeled by default; policy inventory",
        "Privacy engineering in product/app design; DPIA-driven measures",
        "Partial Support", "Medium", LIC["labels_auto"] + "; " + LIC["dlp_core"] + "; " + LIC["retention_basic"], None,
        [EURLEX, URLS["labels"], URLS["dlp"], URLS["retention"]], also=["Data Loss Prevention", "Data Lifecycle Management"]),

    row("gdpr-30", "Art. 30", "Art. 30 ROPA",
        "Maintain records of processing activities (purposes, categories, recipients, transfers, retention, security measures).",
        "None (boundary row)", "n/a",
        "Deliberate boundary row: the ROPA is a governance register core Purview does not produce. Purview outputs (data inventory, retention configuration) feed ROPA fields, but the record itself is Priva/GRC/process tooling.",
        "n/a", "n/a",
        "ROPA tooling/process (Priva, GRC platform, registers); DPO ownership",
        "Not Covered", "High", "n/a", None,
        [EURLEX]),

    row("gdpr-32-1-a", "Art. 32(1)(a)", "Art. 32 Security",
        "Security of processing: pseudonymization and encryption of personal data as risk-appropriate measures.",
        "Information Protection", "Label-based encryption on personal-data content (auto-applied); Customer Key/DKE options; SIT detection guarding pseudonymized sets against re-identification leakage",
        "Implements the encryption measure for personal data in M365 and evidences pseudonymization hygiene. Database-layer crypto and pseudonymization engineering are outside.",
        "Auto-label + encrypt on personal-data tiers; Customer Key where adopted",
        "Encrypted personal-data item distribution; RMS logs",
        "Application/database encryption; pseudonymization tooling; key management",
        "Partial Support", "High", LIC["labels_auto"] + "; " + LIC["customer_key"], GOV["customer_key"],
        [EURLEX, URLS["label_encrypt"], URLS["customer_key"]], also=["Data Classification"]),

    row("gdpr-32-1-d", "Art. 32(1)(d)", "Art. 32 Security",
        "Regularly test, assess, and evaluate the effectiveness of technical and organizational security measures.",
        "Compliance Manager", "GDPR assessment with continuous automated control testing; DLP simulation-mode reports and policy-effectiveness analytics as measure-testing artifacts",
        "Evidences a recurring effectiveness-evaluation mechanism for the M365 measure set. Penetration testing and org-wide evaluation are the broader program.",
        "GDPR assessment active with automated testing; DLP simulation reviews scheduled",
        "Assessment score trend; simulation/effectiveness reports",
        "Pen-test program; audit function",
        "Evidence Support Only", "Medium", LIC["cm"], GOV["cm"],
        [EURLEX, URLS["cm"], URLS["dlp"]], also=["Data Loss Prevention"]),

    row("gdpr-33-34", "Arts. 33 & 34", "Arts. 33–34 Breach",
        "Notify the supervisory authority within 72 hours (with nature, categories, and approximate numbers of subjects/records), document all breaches (33(5)), and communicate high-risk breaches to data subjects.",
        "Audit", "Audit (Premium) scope-of-access forensics quantifying categories and approximate numbers of data subjects/records concerned; eDiscovery preserving breach evidence; DLP/IRM alerts starting the 72-hour clock with timestamps",
        "Produces precisely the notification-content facts Art. 33(3) demands and the documentation Art. 33(5) requires, inside the 72-hour window. Risk assessment, notification decisions, and filings are legal/organizational.",
        "Alert policies + audit retention across breach lookback windows",
        "Breach workpapers: audit timeline, affected-subject estimates, evidence holds",
        "Breach counsel; supervisory-authority filing process; subject-communication mechanics",
        "Evidence Support Only", "High", LIC["audit_prem"], GOV["audit"],
        [EURLEX, URLS["audit"], URLS["edisc"]], also=["eDiscovery", "Data Loss Prevention"]),

    row("gdpr-35", "Art. 35", "Art. 35 DPIA",
        "Conduct data protection impact assessments before high-risk processing (systematic description, necessity, risks, measures).",
        "DSPM", "DSPM data-risk views describing what personal data a processing surface touches and how exposed it is; DSPM for AI supplying the AI-processing visibility DPIAs for AI systems need",
        "Feeds the DPIA's 'systematic description of processing and risks' with live estate evidence, especially for Copilot/AI-adoption DPIAs where DSPM for AI reports are the concrete data-flow record. The DPIA method, necessity test, and sign-off are the privacy office's.",
        "DSPM enabled over in-scope estates; DSPM for AI reports for AI DPIAs",
        "DSPM/AI-activity reports attached to DPIA workpapers",
        "DPIA methodology and register; DPO consultation",
        "Evidence Support Only", "Medium", LIC["dspm"] + "; " + LIC["dspm_ai"], GOV["dspm_ai"],
        [EURLEX, URLS["dspm"]], also=["DSPM for AI", "Data Classification"]),
]


# ==== Microsoft Entra rows (product #2, added 2026-07-17) ====
from common import ENTRA_LIC, ENTRA_URLS, ENTRA_GOV, prow, rel
_E = "2026-07-17"
def er(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("entra", "gdpr", "2016/679", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _E, also_involves=also)

ROWS += [
    er("gdpr-32-1-b-entra", "Art. 32(1)(b)", "Art. 32 Security",
       "Security of processing: ensure the ongoing confidentiality, integrity, availability, and resilience of processing systems, including access control as a technical measure.",
       "Conditional Access & Authentication",
       "Conditional Access, MFA, and least-privilege access governance restricting access to systems processing personal data; PIM for privileged access",
       "Implements access control and strong authentication as Art. 32 technical measures for Entra-integrated systems processing personal data. Encryption/pseudonymization and non-Entra systems are complementary.",
       "Conditional Access baseline; MFA; access reviews; PIM",
       "Sign-in grant/block evidence; access-review and PIM records",
       [rel("purview", "contributing", "Sensitivity-label encryption and DLP provide the confidentiality/encryption measures for personal data", "Information Protection")],
       "Encryption/pseudonymization of personal data; access control in non-Entra systems",
       "Partial Support", "High",
       ENTRA_LIC["ca"] + " " + ENTRA_LIC["gov_core"],
       ENTRA_GOV["ca"],
       [FRAMEWORK["official_source"], ENTRA_URLS["ca"], ENTRA_URLS["pim"]],
       also=["Privileged Identity Management", "Entra ID Governance"]),

    er("gdpr-25-entra", "Art. 25", "Art. 25 By design",
       "Data protection by design and by default: implement appropriate technical and organizational measures such as access minimization into processing.",
       "Entra ID Governance",
       "Least-privilege access packages, access reviews, and default-deny Conditional Access as by-default technical measures minimizing who can access personal data",
       "Implements the access-minimization dimension of data protection by default for Entra-governed systems: least privilege and recertification limit personal-data access. Broader privacy-by-design in app/system design is organizational.",
       "Least-privilege access packages; default-deny Conditional Access; recurring reviews",
       "Entitlement/least-privilege metrics; access-review completions",
       [rel("purview", "contributing", "Default sensitivity labels, DLP, and retention are by-default data-protection measures for content", "Information Protection")],
       "Privacy engineering in application/system design; DPIA-driven measures",
       "Partial Support", "Medium",
       ENTRA_LIC["gov_core"] + " " + ENTRA_LIC["ca"],
       ENTRA_GOV["gov"],
       [FRAMEWORK["official_source"], ENTRA_URLS["entitlement"], ENTRA_URLS["ca"]],
       also=["Conditional Access & Authentication"]),
]


# ==== Microsoft Intune rows (product #3, added 2026-07-17) ====
from common import INTUNE_LIC, INTUNE_URLS, INTUNE_GOV
_I = "2026-07-17"
def ir(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("intune", "gdpr", "2016/679", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _I, also_involves=also)

ROWS += [
    ir("gdpr-32-1-a-intune", "Art. 32(1)(a)", "Art. 32 Security",
       "Security of processing: pseudonymization and encryption of personal data as risk-appropriate measures.",
       "Endpoint Security",
       "Disk-encryption policy enforcing BitLocker/FileVault on endpoints processing personal data, with compliance attestation; app protection policies encrypting personal data handled in managed mobile apps on corporate and BYO devices",
       "Implements the device-layer encryption measure, a recognized technical and organizational measure (TOM) under Art. 32, for managed endpoints and mobile apps. Content-layer encryption in M365 is the Purview seam; pseudonymization engineering and database crypto are external.",
       "Disk-encryption profiles; compliance encryption requirement; app protection policies for mobile processing",
       "Encryption status report; compliance encryption state; app-protection delivery status: TOM evidence for Art. 30 records and processor assurances",
       [rel("purview", "contributing", "Label-based encryption with customer key options implements content-layer encryption of personal data", "Information Protection")],
       "Pseudonymization tooling; application/database encryption; key management",
       "Partial Support", "High",
       INTUNE_LIC["p1"],
       None,
       [FRAMEWORK["official_source"], INTUNE_URLS["disk_encryption"], INTUNE_URLS["app_protection"]],
       also=["Device Compliance", "App Protection & Management"]),

    ir("gdpr-32-1-b-intune", "Art. 32(1)(b)", "Art. 32 Security",
       "Security of processing: ensure the ongoing confidentiality, integrity, availability, and resilience of processing systems, including access control as a technical measure.",
       "Device Compliance",
       "Device compliance and configuration policies keeping endpoints that process personal data in a continuously verified secure state (encryption, OS currency, credential, threat level), with noncompliant devices losing access via Conditional Access; selective wipe removing personal/org data from lost or departing devices",
       "Implements the endpoint-confidentiality slice of the ongoing-security obligation, a demonstrable TOM: devices must prove a secure state to keep processing access, and data on lost devices is recoverable-proof. Identity access control is the Entra layer; availability/resilience of processing systems is infrastructure.",
       "Compliance policies per platform; require-compliant-device Conditional Access on personal-data systems; wipe/retire runbook for lost devices",
       "Compliance status reports; Conditional Access grant/block evidence; wipe action records",
       [rel("entra", "contributing", "Conditional Access and MFA implement the identity access-control measure under the same article", "Conditional Access & Authentication"),
        rel("purview", "contributing", "DLP and label encryption implement content-layer confidentiality measures", "Information Protection")],
       "Availability/resilience measures (backup, DR); security of non-endpoint processing systems",
       "Partial Support", "Medium",
       INTUNE_LIC["p1_ca"],
       None,
       [FRAMEWORK["official_source"], INTUNE_URLS["compliance"], INTUNE_URLS["wipe_corporate_data"]],
       also=["Device Configuration & Baselines", "App Protection & Management"]),
]


# ==== Microsoft Defender XDR rows (product #4, added 2026-07-17) ====
from common import DEFENDER_LIC, DEFENDER_URLS, DEFENDER_GOV
_D = "2026-07-17"
def dr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("defender-xdr", "gdpr", "2016/679", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _D, also_involves=also)

ROWS += [
    dr("gdpr-32-1-b-defender", "Art. 32(1)(b)", "Art. 32 Security",
       "Security of processing: ensure the ongoing confidentiality, integrity, availability, and resilience of processing systems, including access control as a technical measure.",
       "Defender for Endpoint",
       "Threat prevention, detection, and response protecting the confidentiality and integrity of processing systems: next-gen antivirus and attack surface reduction preventing compromise, EDR and cross-workload correlation detecting it, automated investigation and attack disruption containing it before personal data is exposed",
       "Implements the threat-defense dimension of ongoing confidentiality/integrity: a system compromised by malware or an intruder can guarantee neither. Stacks with the Entra row (access control) and Intune row (device hardening); availability/resilience engineering (backup, redundancy) is separate.",
       "AV and ASR in block mode; EDR onboarding across systems processing personal data; attack disruption enabled",
       "Incident detection/containment reports for systems processing personal data; threat-protection status reports",
       [rel("entra", "contributing", "Conditional Access and MFA implement the access-control measure (the stacked Entra row)", "Conditional Access & Authentication"),
        rel("intune", "contributing", "Intune enforces device encryption and hardening (the stacked Intune rows)", "Endpoint Security"),
        rel("purview", "contributing", "DLP and sensitivity labels protect the personal data itself", "Data Loss Prevention")],
       "Availability and resilience engineering (backup, redundancy, DR); protection for non-Microsoft processing systems",
       "Partial Support", "High",
       DEFENDER_LIC["mde_p2"],
       None,
       [FRAMEWORK["official_source"], DEFENDER_URLS["mde"], DEFENDER_URLS["attack_disruption"]],
       also=["Defender for Office 365"]),

    dr("gdpr-32-1-d-defender", "Art. 32(1)(d)", "Art. 32 Security",
       "Regularly test, assess, and evaluate the effectiveness of technical and organizational security measures.",
       "Defender for Endpoint",
       "Recurring technical-measure assessment: Defender Vulnerability Management continuously assessing vulnerabilities and secure-configuration posture against baselines, Microsoft Secure Score in the Defender portal quantifying security posture and tracking improvement, attack simulation training (Defender for Office 365 Plan 2) empirically testing the phishing-resistance measure",
       "Implements a continuously running test-assess-evaluate mechanism for the technical measures on the Microsoft estate, stacking with the Purview row's Compliance Manager evidence. Penetration testing, audits, and evaluation of organizational measures remain the broader program.",
       "MDVM secure-configuration assessment active; Secure Score review cadence; recurring attack-simulation campaigns",
       "Configuration-assessment and Secure Score trend exports; attack-simulation result reports as measure-effectiveness evidence",
       [rel("purview", "contributing", "Compliance Manager continuous control testing evidences the assessment process (the stacked Purview row)", "Compliance Manager")],
       "Penetration testing and independent audits; evaluation of organizational measures",
       "Partial Support", "Medium",
       DEFENDER_LIC["mdvm"] + " Attack simulation training: " + DEFENDER_LIC["mdo_p2"],
       None,
       [FRAMEWORK["official_source"], DEFENDER_URLS["mdvm"], DEFENDER_URLS["attack_sim"]],
       also=["Defender for Office 365"]),

    dr("gdpr-33-34-defender", "Arts. 33 & 34", "Arts. 33–34 Breach",
       "Notify the supervisory authority within 72 hours (with nature, categories, and approximate numbers of subjects/records), document all breaches (33(5)), and communicate high-risk breaches to data subjects.",
       "Defender for Endpoint",
       "Breach detection and scoping that starts and feeds the 72-hour clock: cross-workload detection surfacing the breach promptly ('awareness' under Art. 33(1)), incident investigation establishing attack path and affected systems, containment limiting the breach's scope, and Action center/incident records feeding the Art. 33(5) documentation duty",
       "Implements the detect-investigate-contain foundation the notification obligations rest on: a breach cannot be notified within 72 hours if it is not detected and scoped quickly. Stacks with the Purview row (which data/subjects were affected). The risk assessment, notification decision, and filings are legal/organizational.",
       "Detection coverage across systems processing personal data; incident notification rules to the DPO/privacy team; investigation SOPs aligned to the 72-hour timeline",
       "Incident timeline records (first-detection timestamps to containment); investigation reports feeding breach documentation",
       [rel("purview", "primary", "Audit (Premium) forensics quantify categories and approximate numbers of data subjects/records, the Art. 33(3) content (the stacked Purview row)", "Audit"),
        rel("sentinel", "contributing", "Sentinel extends breach detection to non-Microsoft processing systems")],
       "Breach risk assessment and notification decisioning (DPO/legal); supervisory-authority filings; data-subject communications",
       "Partial Support", "High",
       DEFENDER_LIC["mde_p2"],
       None,
       [FRAMEWORK["official_source"], DEFENDER_URLS["incidents"], DEFENDER_URLS["air"]],
       also=["Defender for Office 365", "Defender for Identity"]),
]


# ==== Microsoft Sentinel rows (product #5, added 2026-07-18) ====
from common import SENTINEL_LIC, SENTINEL_URLS, SENTINEL_GOV, prow, rel
_S = "2026-07-18"
def sr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("sentinel", "gdpr", "2016/679", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _S, licensing_model="consumption", also_involves=also)

ROWS += [
    sr("gdpr-32-1-b-sentinel", "Art. 32(1)(b)", "Art. 32 Security",
       "Security of processing: ensure the ongoing confidentiality, integrity, availability, and resilience of processing systems, including access control as a technical measure.",
       "Analytics Rules & Detections",
       "The ongoing-assurance monitoring measure across all processing systems: continuous detection over Microsoft workloads and, via connectors, the non-Microsoft processing systems the stacked Defender row leaves external (databases, applications, infrastructure); availability/error anomaly detection from operational log streams contributing to the availability-and-resilience dimension; alerting that turns a CIA failure into a response within hours, not months",
       "Implements the monitoring measure that makes 'ongoing' meaningful: confidentiality and integrity cannot be ensured on an ongoing basis without a mechanism that notices when they fail, and Sentinel is that mechanism at estate scope. Stacks as the fourth technical-measure card (Entra: access control; Intune: device protection; Defender: threat defense). Resilience engineering itself (backup, redundancy) remains separate.",
       "Connector coverage across systems processing personal data; detection rules per system class; availability/error anomaly detections",
       "Continuous-monitoring reports across processing systems; detection and response-time evidence",
       [rel("entra", "contributing", "Conditional Access and MFA implement the access-control measure (the stacked Entra row)", "Conditional Access & Authentication"),
        rel("intune", "contributing", "Intune enforces device encryption and hardening (the stacked Intune row)", "Endpoint Security"),
        rel("defender-xdr", "contributing", "Defender XDR prevents and detects compromise on Microsoft workloads (the stacked Defender row); Sentinel extends detection to every other processing system", "Defender for Endpoint")],
       "Availability and resilience engineering (backup, redundancy, DR); log generation on non-Microsoft processing systems",
       "Partial Support", "High",
       SENTINEL_LIC["ingest"],
       None,
       [FRAMEWORK["official_source"], SENTINEL_URLS["analytics"], SENTINEL_URLS["connect"]],
       also=["Data Collection & Connectors"]),

    sr("gdpr-32-1-d-sentinel", "Art. 32(1)(d)", "Art. 32 Security",
       "Regularly test, assess, and evaluate the effectiveness of technical and organizational security measures.",
       "Analytics Rules & Detections",
       "Effectiveness evidence for the detection-and-response measures themselves: MITRE ATT&CK coverage mapping showing which techniques the analytics estate detects and where gaps sit, analytics-rule health monitoring proving the measures run, and SOC incident metrics (detection volumes, response times, trend lines) as the recurring assessment artifact for the monitoring measure",
       "Evidences the regular-evaluation obligation for one class of technical measures (the organization's detection and response capability), with artifacts a DPO can put in the Art. 32 file. It does not test the measures (no simulation or scanning); the stacked Defender row carries continuous technical assessment and the Purview row the structured assessment program.",
       "MITRE coverage review cadence; rule health monitoring enabled; SOC metrics workbook in the assessment procedure",
       "Coverage-gap review records; rule health reports; SOC metric trend exports in assessment documentation",
       [rel("purview", "contributing", "Compliance Manager structures the assessment program (the stacked Purview row)", "Compliance Manager"),
        rel("defender-xdr", "contributing", "Defender Vulnerability Management and attack simulation actively test technical measures (the stacked Defender row)", "Defender for Endpoint")],
       "Penetration testing and audits; evaluation of organizational measures; assessment ownership",
       "Evidence Support Only", "Medium",
       SENTINEL_LIC["ingest"],
       None,
       [FRAMEWORK["official_source"], SENTINEL_URLS["soc_metrics"], SENTINEL_URLS["analytics"]],
       also=["Incident Management & Investigation"]),

    sr("gdpr-33-34-sentinel", "Arts. 33 & 34", "Arts. 33–34 Breach",
       "Notify the supervisory authority within 72 hours (with nature, categories, and approximate numbers of subjects/records), document all breaches (33(5)), and communicate high-risk breaches to data subjects.",
       "Incident Management & Investigation",
       "The breach-clock and documentation machinery at controller scope: detection across every connected processing system, including the non-Microsoft systems the stacked Defender row cannot see, starting Art. 33(1) awareness promptly; the incident timeline (first detection through containment) as the 72-hour narrative and the without-undue-delay evidence; playbooks driving the DPO-notification workflow the moment a qualifying incident opens; incident records feeding the Art. 33(5) breach register",
       "Implements breach detection for the whole processing estate and produces the facts-and-effects documentation Art. 33(5) demands as a durable record. The stacked Purview row quantifies affected subjects/records; the risk assessment, notification decision, and filings are the DPO's and counsel's.",
       "Connector coverage across processing systems; DPO-notification playbook on qualifying incident classes; breach-register export procedure",
       "Incident timelines evidencing awareness-to-notification elapsed time; playbook run history; breach documentation exports",
       [rel("purview", "primary", "Audit (Premium) forensics quantify categories and approximate numbers of data subjects/records, the Art. 33(3) content (the stacked Purview row)", "Audit"),
        rel("defender-xdr", "contributing", "Defender XDR detects and contains Microsoft-workload breaches (the stacked Defender row); Sentinel extends detection estate-wide and holds the documented record", "Defender for Endpoint")],
       "Breach risk assessment and notification decisioning (DPO/legal); supervisory-authority filings; data-subject communications",
       "Partial Support", "High",
       SENTINEL_LIC["ingest"] + " " + SENTINEL_LIC["soar"],
       None,
       [FRAMEWORK["official_source"], SENTINEL_URLS["incidents"], SENTINEL_URLS["playbooks"]],
       also=["Automation & Playbooks (SOAR)", "Analytics Rules & Detections"]),
]


# ==== Microsoft Defender for Cloud rows (product #6, added 2026-07-18) ====
from common import MDC_LIC, MDC_URLS, MDC_GOV
_M = "2026-07-18"
def mr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("defender-cloud", "gdpr", "2016/679", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _M, licensing_model="consumption", also_involves=also)

ROWS += [
    mr("gdpr-32-1-b-mdc", "Art. 32(1)(b)", "Art. 32 Security",
       "Security of processing: ensure the ongoing confidentiality, integrity, availability, and resilience of processing systems, including access control as a technical measure.",
       "Defender CSPM",
       "Technical measures for personal data processed on cloud infrastructure: sensitive data discovery locates cloud storage and databases holding personal-data patterns (powered by the Microsoft Purview classification engine, using the same SITs and sensitivity labels, importable including custom types), attack path analysis surfaces exploitable routes to those stores, CIEM right-sizes the identities that can reach them, and workload threat detection guards the processing systems at runtime",
       "Contributes the appropriate-technical-measures showing for the cloud-infrastructure slice of the processing estate: the controller can demonstrate it knows where personal data sits in cloud stores, what threatens it, and that detection is active. Classification-scope seam: Purview is the classification and protection authority for M365 and connected sources (full scanning, labeling, DLP); Defender for Cloud samples cloud datastores for posture prioritization using Purview's taxonomy; it discovers and prioritizes, it does not label or protect content. The four stacked product rows carry the identity, device, endpoint, and monitoring measures.",
       "Sensitive data discovery enabled with personal-data SITs (custom types imported from Purview); attack-path review covering personal-data stores; workload plans on processing subscriptions",
       "Sensitive-data discovery findings per cloud store; attack-path reports scoped to personal-data resources; CIEM over-permission findings and remediation history",
       [rel("purview", "primary", "Purview is the classification/protection authority; its SIT taxonomy powers this discovery, and it labels and protects the content itself in M365 (different classification scopes, one taxonomy)", "Data Classification"),
        rel("entra", "contributing", "Entra ID carries the access-control technical measure this article names (the stacked Entra row)", "Conditional Access & Authentication"),
        rel("defender-xdr", "contributing", "Defender XDR protects the endpoint/workload processing path (the stacked Defender row)", "Defender for Endpoint")],
       "Backup/resilience measures (Azure Backup/Site Recovery, outside this product); encryption implementation; DPIA and lawful-basis obligations; on-premises processing systems",
       "Partial Support", "High",
       MDC_LIC["cspm"] + " " + MDC_LIC["workload"],
       MDC_GOV["gaps"],
       [FRAMEWORK["official_source"], MDC_URLS["dspm"], MDC_URLS["ciem"]],
       also=["Workload Protection Plans"]),

    mr("gdpr-32-1-d-mdc", "Art. 32(1)(d)", "Art. 32 Security",
       "Regularly test, assess, and evaluate the effectiveness of technical and organizational security measures.",
       "Regulatory Compliance Dashboard",
       "A standing test-assess-evaluate mechanism for cloud-hosted processing systems: the regulatory compliance dashboard continuously assesses onboarded cloud resources against the EU GDPR built-in standard and MCSB with per-control pass/fail, secure score trends the effectiveness of technical measures over time, and agentless vulnerability assessment supplies the regular technical-testing input",
       "Implements the regularly-assessing-and-evaluating activity for technical measures on the cloud slice of the processing estate. Assessment-scope boundary: it assesses onboarded cloud resources against technically-assessable criteria, not organizational measures, not M365/on-premises processing systems (the stacked Purview row's Compliance Manager and the Sentinel evidence row cover their planes), and its output demonstrates technical posture, not Art. 32 compliance as such. Penetration testing and audit remain the controller's program.",
       "EU GDPR standard assigned to processing-system subscriptions (requires a paid plan); assessment reports wired into the Art. 32(1)(d) evaluation cadence",
       "Per-standard compliance reports over time; secure score trend; vulnerability assessment history for the evaluation record",
       [rel("purview", "contributing", "Purview Compliance Manager's GDPR assessment covers the M365 processing estate (the stacked Purview row); complementary evaluation scopes, a seam not an overlap", "Compliance Manager"),
        rel("sentinel", "contributing", "Sentinel evidences monitoring-measure operation estate-wide (the stacked Sentinel row)", "Analytics Rules & Detections")],
       "Penetration testing and security audits; evaluation of organizational measures; DPO oversight and documentation",
       "Partial Support", "High",
       MDC_LIC["dashboard"],
       MDC_GOV["dashboard"],
       [FRAMEWORK["official_source"], MDC_URLS["dashboard"], MDC_URLS["reg_standards"]],
       also=["Defender CSPM", "Foundational CSPM"]),
]
