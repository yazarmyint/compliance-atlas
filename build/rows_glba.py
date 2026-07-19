"""GLBA Safeguards Rule rows — 16 CFR Part 314 as amended (verified against eCFR 2026-07-14 issue).
Notification amendment (§314.4(j), effective May 13, 2024) included."""
from common import LIC, URLS, GOV, VERIFIED_DATE

ECFR = "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-314"
FTC = "https://www.ftc.gov/legal-library/browse/rules/safeguards-rule"

FRAMEWORK = {
    "id": "glba-safeguards",
    "name": "GLBA Safeguards Rule",
    "full_name": "FTC Standards for Safeguarding Customer Information (GLBA Safeguards Rule), 16 CFR Part 314",
    "version": "As amended (2021 amendments fully effective Jun 9, 2023; breach-notification amendment effective May 13, 2024); verified against eCFR 2026-07-14",
    "authority": "US Federal Trade Commission",
    "official_source": ECFR,
    "document_url": FTC,
    "compliance_manager_template": {"exists": True, "name": "Gramm-Leach-Bliley Act, Title V, Subtitle A, Financial Privacy (premium)",
        "note": "Verified on the Compliance Manager regulations list 2026-07-16. Template spans GLBA Title V; confirm safeguards-element coverage before relying on it. A separate 'FTC Privacy of Consumer Financial Information' template also exists.",
        "source": URLS["cm_regs"]},
    "domains": ["§314.4(b) Risk assessment", "§314.4(c) Safeguards", "§314.4(d) Testing & monitoring",
                "§314.4(h) Incident response", "§314.4(j) FTC notification"],
    "applies_to": "Non-bank financial institutions under FTC jurisdiction (lenders, advisors, fintech, auto dealers, mortgage/collections), plus Title IV higher-education institutions (FSA-enforced)",
    "notes": ("Banking regulators (OCC/Fed/FDIC/NCUA) enforce parallel interagency guidelines for depository institutions; this mapping "
              "targets the FTC rule. §314.4(c)(5) MFA and (c)(4) secure development are deliberately unmapped (identity/SDLC territory)."),
}

def row(id, ref, domain, intent, sol, cap, how, cfg, op, deps, cov, conf, lic, cloud, sources, also=None):
    return {
        "id": id, "product": "purview", "framework": "glba-safeguards",
        "framework_version": "16 CFR 314 (as amended)", "control_ref": ref, "control_domain": domain,
        "control_intent": intent, "purview_solution": sol, "also_involves": also or [],
        "capability_detail": cap, "how_it_supports": how,
        "config_evidence_example": cfg, "operational_evidence_example": op,
        "non_purview_dependencies": deps, "coverage": cov, "confidence": conf,
        "license_requirement": lic, "cloud_availability_note": cloud,
        "sources": sources, "status": "verified", "last_verified": VERIFIED_DATE,
    }

ROWS = [
    row("glba-314-4-b", "§314.4(b)", "§314.4(b) Risk assessment",
        "Base the security program on a written risk assessment identifying foreseeable internal/external risks to customer information, with criteria for risk evaluation and safeguard adequacy.",
        "Data Classification", "Customer-information discovery (financial SITs, Data explorer) and DSPM risk analytics feeding the written assessment's data-inventory and exposure inputs",
        "Supplies the where-is-customer-information and how-exposed-is-it evidence the written risk assessment must rest on. The assessment document, criteria, and periodic refresh are the Qualified Individual's program work.",
        "Financial SITs enabled; DSPM assessments over customer-data locations",
        "Data explorer exports and DSPM reports cited in the risk assessment",
        "Written risk-assessment methodology; Qualified Individual ownership",
        "Evidence Support Only", "Medium", LIC["classification_analytics"] + "; " + LIC["dspm"], None,
        [ECFR, FTC, URLS["data_explorer"], URLS["dspm"]], also=["DSPM"]),

    row("glba-314-4-c1", "§314.4(c)(1)", "§314.4(c) Safeguards",
        "Implement and periodically review access controls, limiting access to customer information to authorized users and to what each needs.",
        "Information Protection", "Label-based encryption restricting customer-information content to authorized groups wherever it travels; DLP constraining exposure paths",
        "Adds data-layer need-to-know enforcement over customer information in M365. Account provisioning, RBAC, and periodic access reviews are the identity plane.",
        "Encrypted 'Customer NPI' label scoped to servicing roles",
        "RMS access logs; label coverage on customer-data stores",
        "Entra RBAC + access reviews (primary); application entitlements",
        "Partial Support", "Medium", LIC["label_encryption"], None,
        [ECFR, URLS["label_encrypt"], URLS["dlp"]], also=["Data Loss Prevention"]),

    row("glba-314-4-c2", "§314.4(c)(2)", "§314.4(c) Safeguards",
        "Identify and manage the data, personnel, devices, systems, and facilities that enable business purposes, per their importance.",
        "Data Classification", "Data explorer / Content explorer (classic) + DSPM as the customer-information inventory across M365 (locations, volumes, sensitivity)",
        "Implements the *data* dimension of the required inventory continuously. Personnel/devices/systems/facilities dimensions live in HR/ITAM/CMDB.",
        "Financial/NPI SIT scoping; recurring discovery sweeps",
        "Inventory exports trended over time",
        "CMDB/ITAM; HR systems; facilities records",
        "Partial Support", "High", LIC["classification_analytics"] + "; " + LIC["dspm"], None,
        [ECFR, URLS["data_explorer"], URLS["dspm"]], also=["DSPM"]),

    row("glba-314-4-c3", "§314.4(c)(3)", "§314.4(c) Safeguards",
        "Encrypt all customer information in transit over external networks and at rest (or use approved equivalent controls).",
        "Information Protection", "Auto-labeling with encryption on customer-information content; Customer Key for M365 at-rest key control; Purview Message Encryption for external email",
        "Implements item-level encryption for customer information in M365, layered on inherited platform encryption, and encrypts external mail flows. Database/application-layer encryption and TLS management are outside.",
        "Auto-label policy: financial SITs → encrypted label; Message Encryption rules for external sends",
        "Encrypted-item distribution; encrypted-mail logs",
        "TLS on external transmission paths; database encryption; key management",
        "Partial Support", "High", LIC["labels_auto"] + "; " + LIC["customer_key"], GOV["customer_key"],
        [ECFR, URLS["label_encrypt"], URLS["customer_key"]], also=["Data Classification"]),

    row("glba-314-4-c6", "§314.4(c)(6)", "§314.4(c) Safeguards",
        "Securely dispose of customer information no later than two years after last use for the customer (absent legitimate need/legal requirement), and periodically review retention to minimize unnecessary holding.",
        "Data Lifecycle Management", "Retention labels/policies enforcing the two-year disposal clock on customer-information stores; disposition review producing disposal records; event-based retention keyed to relationship end",
        "Directly implements the disposal mandate for M365-resident customer information (one of the few hard retention clocks in US federal rules) with reviewable proof. Non-M365 systems (loan servicing, CRM) need equivalent purge routines.",
        "Retention labels with ≤2-year delete actions (or event-based on relationship end) on NPI stores",
        "Deletion/disposition logs; retention policy review records",
        "Application-database purge routines; paper records destruction",
        "Direct Support", "High", LIC["retention_basic"] + "; " + LIC["retention_advanced"] + "; " + LIC["records"], None,
        [ECFR, URLS["retention"], URLS["disposition"]], also=["Records Management"]),

    row("glba-314-4-c7", "§314.4(c)(7)", "§314.4(c) Safeguards",
        "Adopt change-management procedures.",
        "Audit", "Unified audit log of configuration/policy changes in the data-protection layer as change-execution evidence",
        "Evidences that changes to data-security controls are attributable and timestamped. The change procedure, approvals, and testing are organizational.",
        "Policy export snapshots per change window",
        "Admin audit extracts joined to change records",
        "Change-management process/tooling",
        "Evidence Support Only", "Low", LIC["audit_std"], None,
        [ECFR, URLS["audit"]]),

    row("glba-314-4-c8", "§314.4(c)(8)", "§314.4(c) Safeguards",
        "Monitor and log authorized-user activity and detect unauthorized access, use, or tampering with customer information.",
        "Audit", "Unified audit log of user activity on customer information; Insider Risk Management detecting misuse/exfiltration by authorized users; DLP alerts on unauthorized movement",
        "Directly implements activity logging and adds behavioral detection of exactly what the rule targets (authorized users misusing customer information) for the M365 estate. Core banking/CRM systems need their own monitoring.",
        "Audit retention policy; IRM policies over NPI locations; DLP alerting",
        "Audit extracts; IRM alert/case history",
        "SIEM for application/infrastructure logs; core-system audit trails",
        "Partial Support", "High", LIC["audit_std"] + "; " + LIC["irm"], GOV["irm"],
        [ECFR, URLS["audit"], URLS["irm"]], also=["Insider Risk Management", "Data Loss Prevention"]),

    row("glba-314-4-h", "§314.4(h)", "§314.4(h) Incident response",
        "Maintain a written incident response plan for security events materially affecting customer information (goals, roles, communication, remediation, documentation).",
        "Audit", "DLP/IRM alerts as detection input; Audit (Premium) scope-of-access forensics; eDiscovery evidence preservation feeding the plan's documentation requirements",
        "Supplies detection, forensic scope (whose customer information, how much), and preserved evidence that the written plan's documentation element requires. The plan itself is organizational.",
        "Alert policies on NPI egress; audit retention through investigation windows",
        "Incident documentation packs with audit timelines",
        "Written IR plan; legal/communications; SIEM/SOAR",
        "Evidence Support Only", "Medium", LIC["audit_prem"] + "; " + LIC["dlp_core"], GOV["audit"],
        [ECFR, URLS["audit"], URLS["edisc"]], also=["Data Loss Prevention", "eDiscovery"]),

    row("glba-314-4-j", "§314.4(j)", "§314.4(j) FTC notification",
        "Notify the FTC within 30 days of discovering a notification event involving unencrypted customer information of 500+ consumers.",
        "Audit", "Audit (Premium) + eDiscovery quantifying affected data and consumer count: the notice's required scope facts; encryption state of affected items from label reports",
        "Produces the affected-scope evidence (what was acquired, how many consumers, was it encrypted) that determines whether the 500-consumer threshold is met and populates the FTC form. The determination and filing are legal/organizational.",
        "Audit Premium enabled; label/encryption state reporting available",
        "Scope-quantification workpapers from audit + search results",
        "Breach counsel determination; FTC filing process",
        "Evidence Support Only", "Medium", LIC["audit_prem"], GOV["audit"],
        [ECFR, FTC, URLS["audit"], URLS["edisc"]], also=["eDiscovery", "Information Protection"]),
]


# ==== Microsoft Entra rows (product #2, added 2026-07-17) ====
from common import ENTRA_LIC, ENTRA_URLS, ENTRA_GOV, prow, rel
_E = "2026-07-17"
def er(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("entra", "glba-safeguards", "16 CFR 314 (as amended)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _E, also_involves=also)

ROWS += [
    er("glba-314-4-c1-entra", "§314.4(c)(1)", "§314.4(c) Safeguards",
       "Implement and periodically review access controls, limiting access to customer information to authorized users and to what each needs.",
       "Entra ID Governance",
       "Role-based access via access packages, access reviews/recertification, and Conditional Access authorization limiting access to customer-information systems integrated with Entra",
       "Directly implements access controls and their periodic review for Entra-governed systems holding customer information. Access in non-Entra line-of-business systems is the dependency.",
       "Access packages mapped to need-to-know; recurring access reviews; Conditional Access",
       "Entitlement/approval records; access-review completions; sign-in grant/block evidence",
       [rel("purview", "contributing", "Sensitivity-label encryption adds content-layer restriction on customer-information documents", "Information Protection")],
       "Access control in non-Entra line-of-business/core systems",
       "Direct Support", "High",
       ENTRA_LIC["gov_core"] + " " + ENTRA_LIC["ca"],
       ENTRA_GOV["gov"],
       [FRAMEWORK["official_source"], ENTRA_URLS["access_reviews"], ENTRA_URLS["ca"]],
       also=["Conditional Access & Authentication"]),

    er("glba-314-4-c5-entra", "§314.4(c)(5)", "§314.4(c) Safeguards",
       "Implement multifactor authentication for any individual accessing any information system (unless an approved reasonably equivalent control is used).",
       "Conditional Access & Authentication",
       "Conditional Access enforcing MFA (phishing-resistant methods) for all users accessing Entra-integrated information systems",
       "Directly implements the Safeguards Rule's explicit MFA requirement for access through Entra: the canonical Entra GLBA control. MFA at non-Entra system boundaries is the dependency.",
       "Conditional Access requiring MFA for all users; phishing-resistant authentication strength",
       "Sign-in logs evidencing MFA; MFA-coverage reports",
       [],
       "MFA at non-Entra information-system boundaries; Qualified Individual approval of equivalents",
       "Direct Support", "High",
       ENTRA_LIC["ca"] + " Methods: " + ENTRA_LIC["mfa"],
       ENTRA_GOV["ca"] + " " + ENTRA_GOV["mfa"],
       [FRAMEWORK["official_source"], ENTRA_URLS["ca"], ENTRA_URLS["mfa"]]),

    er("glba-314-4-c8-entra", "§314.4(c)(8)", "§314.4(c) Safeguards",
       "Monitor and log authorized-user activity and detect unauthorized access to or use of customer information.",
       "Entra ID Protection",
       "Sign-in and audit logs of authorized-user activity plus Entra ID Protection risk detection (leaked credentials, impossible travel) flagging unauthorized/anomalous access",
       "Implements the identity slice of activity monitoring and unauthorized-access detection for Entra-authenticated access. Data-activity monitoring and non-Entra system logs are dependencies.",
       "Sign-in/audit log retention or SIEM export; ID Protection risk policies",
       "Sign-in/audit log extracts; risky-sign-in reports",
       [rel("purview", "contributing", "Audit and Insider Risk Management monitor customer-information data activity", "Audit"),
        rel("sentinel", "contributing", "Sentinel ingests Entra sign-in and risk logs for correlation and retention")],
       "Monitoring for non-Entra core systems; SOC process",
       "Partial Support", "Medium",
       ENTRA_LIC["id_protection"],
       ENTRA_GOV["id_protection"],
       [FRAMEWORK["official_source"], ENTRA_URLS["id_protection"]]),
]


# ==== Microsoft Intune rows (product #3, added 2026-07-17) ====
from common import INTUNE_LIC, INTUNE_URLS, INTUNE_GOV
_I = "2026-07-17"
def ir(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("intune", "glba-safeguards", "16 CFR 314 (as amended)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _I, also_involves=also)

ROWS += [
    ir("glba-314-4-c2-intune", "§314.4(c)(2)", "§314.4(c) Safeguards",
       "Identify and manage the data, personnel, devices, systems, and facilities that enable business purposes, per their importance.",
       "Enrollment & Device Lifecycle",
       "Intune device inventory as the managed implementation of the *devices* dimension: enrolled endpoints with ownership, user, and configuration state, kept current through the enrollment/retire lifecycle",
       "Implements the devices slice of the required identify-and-manage inventory. The data dimension is the Purview seam; personnel, systems, and facilities dimensions live in HR/CMDB/facilities records.",
       "Enrollment coverage for devices touching customer information; inventory collection enabled",
       "All-devices inventory export reconciled to the ITAM register; lifecycle action history",
       [rel("purview", "contributing", "Data explorer and DSPM implement the data dimension of the same inventory", "Data Classification")],
       "HR systems (personnel); CMDB/ITAM for servers and systems; facilities records",
       "Partial Support", "High",
       INTUNE_LIC["p1"],
       None,
       [FRAMEWORK["official_source"], INTUNE_URLS["manage_devices"]]),

    ir("glba-314-4-c3-intune", "§314.4(c)(3)", "§314.4(c) Safeguards",
       "Encrypt all customer information in transit over external networks and at rest (or use approved equivalent controls).",
       "Endpoint Security",
       "Disk-encryption policy enforcing BitLocker/FileVault on endpoints holding customer information, with compliance attestation; app protection policies encrypting org data in mobile apps used for customer information",
       "Implements the endpoint slice of the at-rest encryption mandate: enforcing and attesting platform encryption on managed devices. Content-layer encryption in M365 is the Purview seam; database encryption and TLS on transmission paths are separate layers.",
       "Disk-encryption profiles on customer-information endpoints; compliance encryption requirement; app protection policies",
       "Encryption status report; compliance encryption state per device",
       [rel("purview", "contributing", "Label-based encryption and Message Encryption implement content- and mail-layer encryption of customer information", "Information Protection")],
       "TLS on external transmission paths; database/application encryption; key management",
       "Partial Support", "High",
       INTUNE_LIC["p1"],
       None,
       [FRAMEWORK["official_source"], INTUNE_URLS["disk_encryption"], INTUNE_URLS["app_protection"]],
       also=["Device Compliance", "App Protection & Management"]),
]


# ==== Microsoft Defender XDR rows (product #4, added 2026-07-17) ====
from common import DEFENDER_LIC, DEFENDER_URLS, DEFENDER_GOV
_D = "2026-07-17"
def dr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("defender-xdr", "glba-safeguards", "16 CFR 314 (as amended)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _D, also_involves=also)

ROWS += [
    dr("glba-314-4-c8-defender", "§314.4(c)(8)", "§314.4(c) Safeguards",
       "Monitor and log authorized-user activity and detect unauthorized access, use, or tampering with customer information.",
       "Defender for Endpoint",
       "The unauthorized-access detection layer: EDR flagging anomalous behavior on endpoints holding customer information, Defender for Identity detecting identity misuse and lateral movement toward data stores, Defender for Cloud Apps anomaly detection (mass download, impossible travel) on SaaS activity, correlated into incidents",
       "Implements detection of unauthorized access/use across endpoints, identities, and cloud apps, stacking with the Purview row (activity logging + insider misuse) and Entra row (sign-in anomalies). Monitoring inside core banking/CRM systems requires their own audit facilities.",
       "EDR onboarding on devices handling customer information; MDI sensors deployed; MDCA anomaly policies on in-scope apps",
       "Incident and anomaly alert reports tied to customer-information systems; detection-coverage reviews",
       [rel("purview", "contributing", "Unified audit log and Insider Risk Management supply activity logging and insider-misuse detection (the stacked Purview row)", "Audit"),
        rel("entra", "contributing", "Entra ID Protection detects anomalous sign-ins to systems holding customer information (the stacked Entra row)", "Entra ID Protection")],
       "Monitoring within core banking/CRM platforms; monitoring procedures and response ownership",
       "Partial Support", "High",
       DEFENDER_LIC["xdr"],
       DEFENDER_GOV["xdr"],
       [FRAMEWORK["official_source"], DEFENDER_URLS["xdr"], DEFENDER_URLS["mdi"]],
       also=["Defender for Identity", "Defender for Cloud Apps"]),

    dr("glba-314-4-d-defender", "§314.4(d)", "§314.4(d) Testing & monitoring",
       "Regularly test or monitor the effectiveness of safeguards, including attack/intrusion detection; for information systems, use continuous monitoring or, absent it, annual penetration testing plus biannual vulnerability assessments.",
       "Defender for Endpoint",
       "Continuous monitoring of exactly the kind the rule names as the alternative to periodic testing: Defender Vulnerability Management continuously detecting system changes that create vulnerabilities (new CVEs, configuration drift, new software), EDR detecting actual and attempted attacks/intrusions, with exportable evidence of both",
       "Directly supplies the 'continuous monitoring or other systems to detect, on an ongoing basis, changes in information systems that may create vulnerabilities' that §314.4(d)(2) accepts in place of annual pen tests and biannual vulnerability assessments, for the onboarded estate. Whether the deployment qualifies as effective continuous monitoring for the whole institution is a program-level determination; non-onboarded systems still need testing.",
       "MDVM assessments and EDR active across systems handling customer information; monitoring-effectiveness review cadence",
       "Continuous vulnerability-detection exports; attack/intrusion detection reports; coverage reconciliation against the information-system inventory",
       [rel("intune", "contributing", "Intune remediates the vulnerabilities and configuration drift the monitoring surfaces", "Device Configuration & Baselines"),
        rel("sentinel", "contributing", "Sentinel extends continuous monitoring to non-Microsoft systems")],
       "Qualified-individual determination that continuous monitoring is effective; penetration testing where elected or required; coverage for core banking/CRM and network infrastructure",
       "Partial Support", "High",
       DEFENDER_LIC["mdvm"] + " Attack-detection layer: " + DEFENDER_LIC["mde_p2"],
       DEFENDER_GOV["mdvm"],
       [FRAMEWORK["official_source"], DEFENDER_URLS["mdvm"], DEFENDER_URLS["edr"]]),
]


# ==== Microsoft Sentinel rows (product #5, added 2026-07-18) ====
from common import SENTINEL_LIC, SENTINEL_URLS, SENTINEL_GOV, prow, rel
_S = "2026-07-18"
def sr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("sentinel", "glba-safeguards", "16 CFR 314 (as amended)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _S, licensing_model="consumption", also_involves=also)

ROWS += [
    sr("glba-314-4-c8-sentinel", "§314.4(c)(8)", "§314.4(c) Safeguards",
       "Monitor and log authorized-user activity and detect unauthorized access, use, or tampering with customer information.",
       "Analytics Rules & Detections",
       "Monitor-log-detect for the whole institution: the core banking, CRM, and application audit trails all three stacked rows defer are ingested via connectors and AMA alongside M365, identity, and endpoint signal; UEBA baselines authorized-user behavior and scores deviations (unusual record access, off-hours volume, tampering patterns); analytics correlate across systems and retention preserves the activity log the rule requires",
       "Directly implements the monitor-and-log-and-detect activity this safeguard names, at the scope the stacked rows cannot reach (the institution's core systems), provided their logs are forwarded. Purview covers M365 activity, Entra sign-ins, Defender workload detection; Sentinel is where the institution-wide picture exists. Log generation inside core platforms and the response procedures remain the institution's.",
       "Core banking/CRM log sources connected; UEBA enabled; analytics covering unauthorized-access and tampering patterns per system; retention per the records schedule",
       "Cross-system activity and detection reports; UEBA anomaly history for users touching customer information; connector coverage against the system inventory",
       [rel("purview", "contributing", "Unified audit log and Insider Risk Management cover M365 activity and insider misuse (the stacked Purview row)", "Audit"),
        rel("entra", "contributing", "Entra ID Protection detects anomalous sign-ins (the stacked Entra row)", "Entra ID Protection"),
        rel("defender-xdr", "contributing", "Defender XDR detects unauthorized access on endpoints/identities/SaaS (the stacked Defender row); seam: workload sensors detect, Sentinel monitors and logs institution-wide", "Defender for Endpoint")],
       "Log generation on core banking/CRM platforms; monitoring procedures and response ownership",
       "Direct Support", "High",
       SENTINEL_LIC["ingest"] + " " + SENTINEL_LIC["included"],
       None,
       [FRAMEWORK["official_source"], SENTINEL_URLS["connect"], SENTINEL_URLS["ueba"], SENTINEL_URLS["analytics"]],
       also=["UEBA & Hunting", "Data Collection & Connectors"]),

    sr("glba-314-4-d-sentinel", "§314.4(d)", "§314.4(d) Testing & monitoring",
       "Regularly test or monitor the effectiveness of safeguards, including attack/intrusion detection; for information systems, use continuous monitoring or, absent it, annual penetration testing plus biannual vulnerability assessments.",
       "Analytics Rules & Detections",
       "The institution-wide arm of the continuous-monitoring alternative §314.4(d)(2) accepts: always-on detection of attacks and intrusions across every connected system, including the network infrastructure and core platforms the stacked Defender row leaves external, with analytics-rule and connector-health records evidencing that monitoring itself operates continuously",
       "Extends the continuous-monitoring posture to the systems Defender cannot onboard, completing the coverage argument a Qualified Individual must make for the (d)(2) alternative. Sentinel monitors and evidences; whether the combined deployment qualifies as effective continuous monitoring is a program-level determination, and vulnerability-detection depth on non-onboarded systems may still need scanners.",
       "Connector estate spanning the information-system inventory; attack/intrusion analytics per source class; monitoring-effectiveness review workbook",
       "Continuous-detection reports across systems; monitoring-coverage reconciliation; connector uptime evidence",
       [rel("defender-xdr", "contributing", "Defender Vulnerability Management + EDR are the continuous-monitoring engine for the onboarded estate (the stacked Defender row)", "Defender for Endpoint")],
       "Qualified-individual effectiveness determination; penetration testing where elected; vulnerability assessment for non-onboarded systems",
       "Partial Support", "High",
       SENTINEL_LIC["ingest"],
       None,
       [FRAMEWORK["official_source"], SENTINEL_URLS["analytics"], SENTINEL_URLS["health"]],
       also=["Data Collection & Connectors"]),

    sr("glba-314-4-h-sentinel", "§314.4(h)", "§314.4(h) Incident response",
       "Maintain a written incident response plan for security events materially affecting customer information (goals, roles, communication, remediation, documentation).",
       "Incident Management & Investigation",
       "Execution evidence for the written plan: each security event tracked as an incident with timeline, roles (ownership/assignment mirroring the plan's defined roles), remediation actions, and closure: the documentation-and-remediation elements of §314.4(h) materialized as exportable records; playbooks encode the plan's communication steps with run history",
       "Evidences that the written plan operates. The plan itself is a document the rule requires the institution to author, and Sentinel cannot substitute for it; what Sentinel supplies is the documented execution trail (who did what, when, how communicated) each incident under the plan produces. The stacked Purview row supplies the affected-data forensics.",
       "Incident workflow mapped to the plan's roles and phases; communication playbooks per the plan; documentation export procedure",
       "Incident records demonstrating plan execution; playbook run history for communication steps",
       [rel("purview", "primary", "Audit (Premium) forensics and eDiscovery quantify the affected customer information (the stacked Purview row)", "Audit"),
        rel("defender-xdr", "contributing", "Defender XDR executes containment on Microsoft-estate events", "Defender for Endpoint")],
       "The written IR plan and its required elements; legal/communications ownership; FTC notification duties (§314.4(j))",
       "Evidence Support Only", "High",
       SENTINEL_LIC["ingest"] + " " + SENTINEL_LIC["soar"],
       None,
       [FRAMEWORK["official_source"], SENTINEL_URLS["incidents"], SENTINEL_URLS["playbooks"]],
       also=["Automation & Playbooks (SOAR)"]),
]


# ==== Microsoft Defender for Cloud rows (product #6, added 2026-07-18) ====
from common import MDC_LIC, MDC_URLS, MDC_GOV
_M = "2026-07-18"
def mr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("defender-cloud", "glba-safeguards", "16 CFR 314 (as amended)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _M, licensing_model="consumption", also_involves=also)

ROWS += [
    mr("glba-314-4-d-mdc", "§314.4(d)", "§314.4(d) Testing & monitoring",
       "Regularly test or monitor the effectiveness of safeguards, including attack/intrusion detection; for information systems, use continuous monitoring or, absent it, annual penetration testing plus biannual vulnerability assessments.",
       "Defender CSPM",
       "The continuous-monitoring alternative for cloud-hosted customer-information systems: agentless vulnerability scanning re-assesses VMs/containers/databases continuously (standing in for the biannual vulnerability-assessment floor with a materially stronger cadence), MCSB recommendations continuously test safeguard configuration, and workload threat detection supplies the attack/intrusion-detection element §314.4(d)(1) names",
       "Extends the §314.4(d)(2) continuous-monitoring path the stacked Defender XDR row establishes for endpoints to the cloud-infrastructure estate: banking workloads in Azure/AWS/GCP get continuous safeguard-effectiveness monitoring rather than point-in-time testing. Penetration testing (where the institution stays on the (d)(2)(i) path), non-cloud systems, and the documented testing program remain external.",
       "Defender CSPM with agentless scanning on customer-information subscriptions; workload protection plans for intrusion detection; monitoring approach documented as the (d)(2) election",
       "Continuous vulnerability assessment records; safeguard-configuration finding history; intrusion-detection alert logs for the testing file",
       [rel("defender-xdr", "contributing", "MDVM continuous vulnerability management covers endpoint devices (the stacked Defender XDR row); together they ground the §314.4(d)(2) continuous-monitoring election across device and cloud planes", "Defender for Endpoint"),
        rel("sentinel", "contributing", "Sentinel supplies the estate-wide monitoring record (the stacked Sentinel row)", "Analytics Rules & Detections")],
       "Annual penetration testing where elected; testing for on-premises core-banking systems; the documented testing/monitoring program",
       "Partial Support", "High",
       MDC_LIC["cspm"] + " " + MDC_LIC["workload"],
       MDC_GOV["gaps"],
       [FRAMEWORK["official_source"], MDC_URLS["agentless"], MDC_URLS["alerts"]],
       also=["Workload Protection Plans", "Foundational CSPM"]),

    mr("glba-314-4-c2-mdc", "§314.4(c)(2)", "§314.4(c) Safeguards",
       "Identify and manage the data, personnel, devices, systems, and facilities that enable business purposes, per their importance.",
       "Foundational CSPM",
       "The systems half of the identify-and-manage safeguard for cloud estates: asset inventory automatically enumerates every onboarded cloud resource with security state; sensitive data discovery (Defender CSPM) identifies which cloud storage and databases actually hold customer-information-pattern data, joining the systems register to the data it carries; criticality tagging weights business importance in the security graph",
       "Maintains the cloud-systems inventory and, through data-aware posture, connects systems to the customer information they hold, which is the per-their-importance dimension the safeguard names. The stacked Purview row identifies and classifies the data itself in M365 (Purview is the classification authority; its SITs power this discovery); Intune inventories devices; personnel and facilities are organizational registers.",
       "Cloud estates onboarded; sensitive data discovery enabled with financial-data SITs; criticality tags applied per business importance",
       "Asset inventory exports; sensitive-data discovery findings mapping systems to customer information; tagged-criticality coverage reports",
       [rel("purview", "primary", "Purview data classification identifies and manages the customer information itself in M365 (the stacked Purview row); its sensitive information types power Defender for Cloud's discovery; different classification scopes, one taxonomy", "Data Classification"),
        rel("intune", "contributing", "Intune inventories and manages the device dimension (the stacked Intune row)", "Enrollment & Device Lifecycle")],
       "Personnel and facilities registers; data inventory for non-cloud stores; the importance-ranking methodology",
       "Partial Support", "High",
       MDC_LIC["foundational"] + " " + MDC_LIC["cspm"],
       MDC_GOV["gaps"],
       [FRAMEWORK["official_source"], MDC_URLS["inventory"], MDC_URLS["dspm"]],
       also=["Defender CSPM"]),
]
