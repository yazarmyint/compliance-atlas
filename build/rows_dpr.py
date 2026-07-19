"""Microsoft SSPA DPR v12 (March 2026) rows — audited migration from the legacy matrix.
Control refs verified against the v12 PDF on 2026-07-16 (see AUDIT-FINDINGS.md)."""
from common import LIC, URLS, GOV, VERIFIED_DATE

SSPA = "https://www.microsoft.com/en-us/procurement/sspa"
DPR_PDF = "https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/accex/documents/presentations/FY26-Microsoft-Supplier-Data-Protection-Requirements-v12_en-US.pdf"

FRAMEWORK = {
    "id": "sspa-dpr",
    "name": "Microsoft SSPA DPR",
    "full_name": "Microsoft Supplier Data Protection Requirements (Supplier Security and Privacy Assurance program)",
    "version": "v12 (March 2026)",
    "authority": "Microsoft Procurement (SSPA program)",
    "official_source": SSPA,
    "document_url": DPR_PDF,
    "compliance_manager_template": {"exists": False, "name": None,
        "note": "No Compliance Manager template: supplier program requirements, not a public regulation. Verified absent from the Compliance Manager regulations list 2026-07-16.",
        "source": URLS["cm_regs"]},
    "domains": ["A Management", "B Notice", "C Choice & Consent", "D Collection", "E Retention",
                "F Data Subjects", "G Subcontractors", "H Quality", "I Monitoring & Enforcement",
                "J Security", "K AI Systems"],
    "applies_to": "Suppliers processing Microsoft Personal Data and/or Microsoft Confidential Data (SSPA-enrolled)",
    "notes": "v12 (63 requirements) is current for FY26. Sections B, C, G, H and K carry no defensible Purview mapping (contractual/organizational or supplier-AI-system controls); these are deliberate exclusions, see AUDIT-FINDINGS.md.",
}

def row(id, ref, domain, intent, sol, cap, how, cfg, op, deps, cov, conf, lic, cloud, sources, also=None):
    return {
        "id": id, "product": "purview", "framework": "sspa-dpr",
        "framework_version": "v12 (March 2026)", "control_ref": ref, "control_domain": domain,
        "control_intent": intent, "purview_solution": sol, "also_involves": also or [],
        "capability_detail": cap, "how_it_supports": how,
        "config_evidence_example": cfg, "operational_evidence_example": op,
        "non_purview_dependencies": deps, "coverage": cov, "confidence": conf,
        "license_requirement": lic, "cloud_availability_note": cloud,
        "sources": sources, "status": "verified", "last_verified": VERIFIED_DATE,
    }

ROWS = [
    row("dpr-a5", "A #5", "A Management",
        "Process Microsoft Personal Data only per Microsoft's documented instructions; keep instructions, policies, and procedures electronically accessible to staff on the engagement.",
        "Audit", "Unified audit log of admin/policy changes; exportable policy configuration",
        "Evidences what data-protection controls are configured and when they changed. The contractual instruction itself, and its accessibility to staff, are organizational.",
        "Exports of label/DLP/retention policy configuration (Security & Compliance PowerShell)",
        "Unified audit log extract of policy create/modify events over the review period",
        "Contract/DPA and SOW terms; policy management and document-control process",
        "Evidence Support Only", "High", LIC["audit_std"], None,
        [SSPA, DPR_PDF, URLS["audit"]]),

    row("dpr-d9", "D #9", "D Collection",
        "Monitor collection of Microsoft Personal/Confidential Data so that only data required to perform the engagement is collected (minimization).",
        "Data Classification", "Data explorer / Content explorer (classic) baseline of sensitive data; DSPM posture trends",
        "Surfaces where Microsoft personal/sensitive data accumulates across M365 so over-collection is visible and reviewable, which implements the monitoring half of the requirement.",
        "SIT selection and label taxonomy scoped to Microsoft data categories",
        "Recurring Data explorer export trended quarter-over-quarter; DSPM oversharing/risk reports",
        "Data-mapping exercise; collection controls in intake apps/forms",
        "Partial Support", "Medium", LIC["classification_analytics"], None,
        [SSPA, DPR_PDF, URLS["data_explorer"], URLS["dspm"]], also=["DSPM"]),

    row("dpr-d11", "D #11", "D Collection",
        "Preserve reduced-identifiability of data sets received from Microsoft (pseudonymous/NPI/unlinked); no re-identification.",
        "Data Classification", "SITs detect direct identifiers; labels mark de-identified stores",
        "Detecting direct identifiers appearing inside stores that should hold only de-identified data evidences that reduced identifiability is holding (or flags a breach of it).",
        "Auto-labeling/DLP rules scoped to the de-identified data locations",
        "DLP/auto-label alerts on identifier presence in those locations",
        "De-identification/anonymization process and tooling (primary); analytics environment controls",
        "Evidence Support Only", "Low", LIC["labels_auto"], None,
        [SSPA, DPR_PDF, URLS["sit"]]),

    row("dpr-e12", "E #12", "E Retention",
        "Retain Microsoft Personal/Confidential Data no longer than needed to perform (or as law requires).",
        "Data Lifecycle Management", "Retention labels/policies with delete actions aligned to the engagement retention schedule",
        "Automatically enforces maximum retention and deletion for Microsoft data held in M365 workloads. Data held outside M365 needs equivalent controls there.",
        "Get-ComplianceTag / retention policy export showing schedule-aligned periods",
        "Deletion/disposition logs; Activity explorer retention-label events",
        "Legal-approved retention schedule; retention controls for non-M365 repositories",
        "Direct Support", "Medium", LIC["retention_basic"] + "; " + LIC["retention_advanced"], None,
        [SSPA, DPR_PDF, URLS["retention"], URLS["dlm"]]),

    row("dpr-e13", "E #13", "E Retention",
        "On completion (at Microsoft's discretion) return or securely destroy Microsoft data and keep a record of disposition.",
        "Records Management", "Disposition review (single/multi-stage) with records of disposition; retention label delete actions",
        "The disposition workflow produces reviewable, exportable proof of destruction for M365-resident content. Return-of-data and physical media destruction are manual/organizational.",
        "File plan with disposition-review settings on engagement data labels",
        "Completed disposition records ('proof of disposal') exported from the portal",
        "Return-of-data procedure; physical media destruction and certificates",
        "Partial Support", "Medium", LIC["records"], GOV["records"],
        [SSPA, DPR_PDF, URLS["disposition"], URLS["records"]], also=["Data Lifecycle Management"]),

    row("dpr-f14-22", "F #14–22", "F Data Subjects",
        "Assist Microsoft with data-subject rights: locate, access, correct, delete; record requests, actions, dates, and recipients of shared data.",
        "eDiscovery", "eDiscovery searches to locate/collect a subject's Microsoft Personal Data across Exchange/SharePoint/OneDrive/Teams; Data explorer to scope where identifiers live",
        "Implements the locate/collect step of DSR fulfilment for M365 content and evidences the search actions taken. Request intake, decisioning, and response records are process/tooling outside core Purview.",
        "eDiscovery case + search configuration for DSR fulfilment",
        "Per-request search/export records; DSR fulfilment log",
        "Microsoft Priva Subject Rights Requests (if licensed); privacy operations process; app-level data stores",
        "Partial Support", "Medium", LIC["ediscovery_std"], None,
        [SSPA, DPR_PDF, URLS["edisc"]], also=["Data Classification"]),

    row("dpr-i30-31", "I #30–31", "I Monitoring & Enforcement",
        "Maintain an incident response plan; notify Microsoft without undue delay on a Data Incident, cooperate with investigation (including scope of data accessed), remediate and track resolution.",
        "Audit", "Audit (Premium) crucial events (e.g., MailItemsAccessed) + Activity explorer forensic timeline; DLP/IRM alerts as detection signal",
        "Directly produces the 'scope of data accessed' artifact v12 requires during incident cooperation, plus the detection signals feeding the IR process. The plan, notification, and remediation tracking are organizational.",
        "Alert policies enabled; audit retention configured (1-year default Premium)",
        "Audit extracts and Activity explorer timeline captured during an incident; alert-to-ticket records",
        "IR plan and breach-notification process; SupplierWeb security contacts; SIEM/SOAR",
        "Evidence Support Only", "High", LIC["audit_prem"], GOV["audit"],
        [SSPA, DPR_PDF, URLS["audit"], URLS["activity_explorer"]], also=["Data Loss Prevention"]),

    row("dpr-j33", "J #33", "J Security",
        "Perform annual security assessments (risks/vulnerabilities to confidentiality, integrity, availability of Microsoft Personal Data), review major changes, and keep change logs.",
        "Compliance Manager", "Assessments with improvement actions and continuous control testing for the M365 estate; Purview admin audit as change log for data-protection policies",
        "Structures and evidences the annual assessment activity for the M365 environment and records data-protection policy changes. Infrastructure vulnerability scanning and org-wide risk assessment are outside Purview.",
        "Active Compliance Manager assessment (e.g., Data Protection Baseline) with assigned actions",
        "Assessment report exports; unified audit log of policy changes with approver identity",
        "Vulnerability scanning/pen-test program; enterprise risk assessment; change-management system",
        "Evidence Support Only", "Medium", LIC["cm"], GOV["cm"],
        [SSPA, DPR_PDF, URLS["cm"], URLS["audit"]], also=["Audit"]),

    row("dpr-j35", "J #35", "J Security",
        "Account for all physical and virtual assets supporting the engagement, with owners; inventory includes data classification of the data on each asset, recovery and disposal records.",
        "Data Classification", "Sensitivity labels as the classification dimension of the asset inventory; Data explorer as the data-on-asset view for M365",
        "Supplies the 'data classification of the data on the asset' element the v12 evidence bullet demands, for M365-resident data. The device/asset register itself is CMDB territory.",
        "Label taxonomy documentation; published label policies",
        "Data explorer/Content explorer label distribution export mapped to the asset register",
        "CMDB/asset register; device lifecycle (recovery/disposal) records; Intune device inventory",
        "Partial Support", "Medium", LIC["labels_manual"] + "; analytics: " + LIC["classification_analytics"], None,
        [SSPA, DPR_PDF, URLS["labels"], URLS["data_explorer"]], also=["Information Protection"]),

    row("dpr-j36", "J #36", "J Security",
        "Access-rights management preventing unauthorized access to Microsoft data: identification, lockout, auto-logoff, strong credentials, MFA, least-privilege reviews, deactivation within 48 hours of termination.",
        "Information Protection", "Label-based encryption restricting who can open protected content regardless of location",
        "Adds a content-layer access restriction on labelled Microsoft data, a narrow contributor. The requirement's substance (accounts, MFA, lockout, 48-hour deprovisioning, access reviews) is identity-platform territory.",
        "Label encryption permission configuration on top-tier labels",
        "Encrypted-item counts; access-denied events for protected content in audit log",
        "Entra ID, Conditional Access/MFA, PIM, access reviews, joiner-mover-leaver process (primary)",
        "Partial Support", "Low", LIC["label_encryption"], None,
        [SSPA, DPR_PDF, URLS["label_encrypt"]]),

    row("dpr-j40", "J #40", "J Security",
        "Run a DLP program: data classified, labelled, and protected; monitor systems processing Microsoft data for intrusions, loss, and unauthorized activity; program must include IDS/IPS, breach analysis, and offboarding communications.",
        "Data Loss Prevention", "DLP across Exchange/SharePoint/OneDrive/Teams + Endpoint DLP; sensitivity labels for the classify/label/protect chain; IRM + Adaptive Protection for unauthorized-activity monitoring",
        "Directly implements the classification/labeling/DLP core of the program, including egress blocking and endpoint/browser channels (covering staff use of third-party AI sites with Microsoft data). The mandated IDS/IPS layer and network monitoring are non-Purview.",
        "DLP policy/rule export across workloads; Endpoint DLP settings; IRM policy configuration",
        "DLP alert and user-override reports; IRM alerts; Activity explorer egress events",
        "IDS/IPS and network monitoring (Defender/SIEM); offboarding communications process",
        "Partial Support", "High", LIC["dlp_core"] + "; " + LIC["dlp_teams"] + "; " + LIC["dlp_endpoint"], GOV["dlp_endpoint"],
        [SSPA, DPR_PDF, URLS["dlp"], URLS["dlp_endpoint"], URLS["adaptive"]],
        also=["Information Protection", "Insider Risk Management"]),

    row("dpr-j47", "J #47", "J Security",
        "Encrypt all engagement data in transit across networks with TLS or IPsec (per NIST 800-52/800-57); refuse unencrypted delivery; manage certificate lifecycle.",
        "None (boundary row)", "n/a",
        "Purview does not implement or evidence transport-layer encryption or certificate management. Sensitivity-label encryption keeps protected files encrypted wherever they travel: complementary data-layer protection, but it does not support this control's transport requirement.",
        "n/a", "n/a",
        "TLS/IPsec configuration on services and network gear; certificate lifecycle management; M365 platform TLS (Microsoft-managed)",
        "Not Covered", "High", "n/a", None,
        [SSPA, DPR_PDF, URLS["label_encrypt"]]),

    row("dpr-j48", "J #48", "J Security",
        "Full-disk encryption on all supplier devices that access or handle Microsoft Personal/Confidential Data.",
        "None (boundary row)", "n/a",
        "Disk encryption is implemented and evidenced by BitLocker/FileVault with Intune compliance reporting, not by Purview. Endpoint DLP requires onboarded devices but that is not evidence of disk encryption.",
        "n/a", "n/a",
        "BitLocker/FileVault via Intune; device compliance policy reports (primary)",
        "Not Covered", "High", "n/a", None,
        [SSPA, DPR_PDF]),

    row("dpr-j49", "J #49", "J Security",
        "Encrypt at rest (per NIST 800-111) all Microsoft Personal/Confidential Data, including enumerated categories: credentials, payment data, medical, government IDs, DOB, geolocation, customer content, and more.",
        "Information Protection", "Auto-labeling with label-based encryption targeting the enumerated categories via built-in SITs; Customer Key for the M365 at-rest encryption layer",
        "Adds item-level encryption to at-rest sensitive content in M365 and lets the tenant hold the root keys (Customer Key). Nearly every enumerated v12 category has a built-in SIT for automatic targeting. Platform storage encryption (BitLocker/DEP in Microsoft datacenters) is the inherited base layer.",
        "Auto-labeling policies (simulation → enforce) scoped to enumerated-category SITs; label encryption settings; DEP/Customer Key configuration",
        "Encrypted/labelled item counts from Data explorer; Azure RMS usage logs",
        "M365 service encryption (inherited); encryption for non-M365 stores; Azure Key Vault key ceremony for Customer Key",
        "Partial Support", "Medium", LIC["labels_auto"] + "; " + LIC["customer_key"], GOV["customer_key"],
        [SSPA, DPR_PDF, URLS["label_encrypt"], URLS["customer_key"], URLS["sit"]], also=["Data Classification"]),

    row("dpr-j50", "J #50", "J Security",
        "Anonymize Microsoft Personal Data before use in development or test environments; real personal data must not enter non-production.",
        "Data Loss Prevention", "DLP/auto-label detection rules scoped to dev/test SharePoint sites and Teams; SIT hits as the violation signal",
        "Detects (does not perform) anonymization failures: personal-data identifiers appearing in non-production locations raise alerts. The anonymization itself needs data-engineering tooling.",
        "DLP rule scoped to dev/test locations with Microsoft-data SITs",
        "Alert history for PII detections in non-prod; Data explorer view of non-prod locations",
        "Anonymization/synthetic-data tooling in the engineering pipeline (primary)",
        "Evidence Support Only", "Medium", LIC["dlp_core"], None,
        [SSPA, DPR_PDF, URLS["dlp"], URLS["sit"]]),
]


# ==== Microsoft Entra rows (product #2, added 2026-07-17) ====
from common import ENTRA_LIC, ENTRA_URLS, ENTRA_GOV, prow, rel
_E = "2026-07-17"
def er(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("entra", "sspa-dpr", "v12 (March 2026)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _E, also_involves=also)

ROWS += [
    er("dpr-j36-entra", "J #36", "J Security",
       "Access-rights management preventing unauthorized access to Microsoft data: identification, lockout, auto-logoff, strong credentials, MFA, least-privilege reviews, and deactivation within 48 hours of termination.",
       "Conditional Access & Authentication",
       "Conditional Access enforcing MFA and sign-in-frequency/session (auto-logoff) controls; smart lockout on failed attempts; strong authentication methods; Entra ID Governance access reviews and leaver lifecycle for least-privilege recertification and timely deactivation",
       "Directly implements the identity core of J#36: MFA, lockout, session controls, strong credentials, and (via ID Governance) least-privilege review and deactivation. Content-layer restriction on labelled Microsoft data is the Purview seam.",
       "Conditional Access policy set (MFA + session controls); smart-lockout thresholds; recurring access reviews; leaver lifecycle workflow",
       "Sign-in logs evidencing MFA; access-review completion records; deprovisioning audit within 48 hours",
       [rel("purview", "contributing", "Sensitivity-label encryption adds a content-layer access restriction on labelled Microsoft data", "Information Protection")],
       "HR termination feed and offboarding process (drives the 48-hour deprovisioning trigger)",
       "Direct Support", "High",
       ENTRA_LIC["ca"] + " Least-privilege reviews & deprovisioning: " + ENTRA_LIC["gov_core"],
       ENTRA_GOV["ca"] + " " + ENTRA_GOV["gov"],
       [FRAMEWORK["official_source"], ENTRA_URLS["ca"], ENTRA_URLS["access_reviews"]],
       also=["Entra ID Governance"]),

    er("dpr-j45-entra", "J #45", "J Security",
       "Authenticate the identity of an individual before granting access to Microsoft data, and ensure the access is appropriate.",
       "Conditional Access & Authentication",
       "Entra ID authentication (MFA, passwordless/FIDO2, certificate-based) with Conditional Access gating application and data access on verified identity and session conditions",
       "Directly implements identity authentication before access. Entra is the primary authentication authority for Microsoft cloud and federated apps. Application- and data-store authorization layers on top.",
       "Authentication-methods policy (phishing-resistant MFA); Conditional Access requiring MFA before app access",
       "Sign-in logs evidencing authenticated access; authentication-method registration reports",
       [],
       "Application/service authorization models; identity proofing at onboarding",
       "Direct Support", "High",
       ENTRA_LIC["ca"] + " Authentication methods: " + ENTRA_LIC["mfa"],
       ENTRA_GOV["ca"] + " " + ENTRA_GOV["mfa"],
       [FRAMEWORK["official_source"], ENTRA_URLS["ca"], ENTRA_URLS["mfa"]]),
]


# ==== Microsoft Intune rows (product #3, added 2026-07-17) ====
from common import INTUNE_LIC, INTUNE_URLS, INTUNE_GOV, prow, rel
_I = "2026-07-17"
def ir(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("intune", "sspa-dpr", "v12 (March 2026)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _I, also_involves=also)

ROWS += [
    ir("dpr-j35-intune", "J #35", "J Security",
       "Account for all physical and virtual assets supporting the engagement, with owners; inventory includes data classification of the data on each asset, recovery and disposal records.",
       "Enrollment & Device Lifecycle",
       "Intune device inventory (all enrolled devices with ownership, user, and hardware attributes) as the managed-endpoint asset register; retire/wipe device actions producing an auditable disposal trail for devices leaving the engagement",
       "Supplies the managed-device slice of the asset inventory and the wipe/retire action history that feeds recovery/disposal records. Non-device assets (VMs, services), unmanaged devices, and the org-wide CMDB with owner records remain external.",
       "Enrollment coverage for all engagement devices; hardware-inventory/properties collection enabled",
       "All-devices inventory export; device-action (retire/wipe) history for disposed devices",
       [rel("purview", "contributing", "Data classification supplies the 'classification of data on the asset' dimension of the inventory", "Data Classification")],
       "CMDB/asset register for non-managed and non-device assets; asset ownership records",
       "Partial Support", "Medium",
       INTUNE_LIC["p1"],
       None,
       [FRAMEWORK["official_source"], INTUNE_URLS["manage_devices"], INTUNE_URLS["device_actions"]]),

    ir("dpr-j48-intune", "J #48", "J Security",
       "Full-disk encryption on all supplier devices that access or handle Microsoft Personal/Confidential Data.",
       "Endpoint Security",
       "Endpoint security disk-encryption policy enforcing BitLocker (Windows) and FileVault (macOS) with recovery-key escrow; device compliance policy requiring encryption and reporting per-device encryption status",
       "Directly enforces and attests full-disk encryption on Intune-managed devices: the enforcement and reporting layer this requirement asks for. The encryption itself is performed by the OS (BitLocker/FileVault); devices not managed by Intune need equivalent enforcement.",
       "Disk-encryption profiles (BitLocker/FileVault) assigned to all engagement devices; compliance policy with encryption required",
       "Device encryption report; compliance-policy per-device encryption status export",
       [rel("purview", "contributing", "Sensitivity-label encryption adds content-layer protection that travels with files: complementary to, not a substitute for, disk encryption", "Information Protection"),
        rel("entra", "contributing", "Conditional Access can require a compliant (encrypted) device before granting access to Microsoft data", "Conditional Access & Authentication")],
       "BitLocker/FileVault are OS platform capabilities; equivalent enforcement for unmanaged devices",
       "Direct Support", "High",
       INTUNE_LIC["p1"],
       None,
       [FRAMEWORK["official_source"], INTUNE_URLS["disk_encryption"], INTUNE_URLS["monitor_encryption"]]),
]


# ==== Microsoft Defender XDR rows (product #4, added 2026-07-17) ====
from common import DEFENDER_LIC, DEFENDER_URLS, DEFENDER_GOV
_D = "2026-07-17"
def dr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("defender-xdr", "sspa-dpr", "v12 (March 2026)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _D, also_involves=also)

ROWS += [
    dr("dpr-j37-defender", "J #37", "J Security",
       "Patch management prioritizing security patches for systems processing Microsoft data: monthly vulnerability scans with twelve months of compliance reporting, risk-based prioritization, emergency patching, coverage of OS and server software, and retirement of unsupported software.",
       "Defender for Endpoint",
       "Defender Vulnerability Management: continuous agent-based vulnerability assessment across Windows/macOS/Linux (exceeds the monthly-scan cadence), risk-based prioritization using Microsoft threat intelligence and exploit likelihood, remediation requests with tracking, end-of-support software identification, and exportable per-device assessment reporting",
       "Implements the vulnerability-scanning, risk-prioritization, and unsupported-software elements of the patch program with continuous assessment and an exportable evidence trail. The patch deployment itself and the documented procedure with severity definitions, approvals, and exceptions are outside Defender.",
       "Devices onboarded to Defender for Endpoint with vulnerability management assessments active; remediation-request workflow in use",
       "Vulnerability assessment exports trended monthly across the prior 12 months; remediation-activity history; end-of-support software report",
       [rel("intune", "contributing", "Windows update rings/Autopatch and configuration policies perform the patch deployment that Defender Vulnerability Management prioritizes", "Device Configuration & Baselines")],
       "Patch management procedure with severity definitions, approvals, and exception records; patching for network devices and systems not onboarded to Defender",
       "Partial Support", "High",
       DEFENDER_LIC["mdvm"],
       DEFENDER_GOV["mdvm"],
       [SSPA, DPR_PDF, DEFENDER_URLS["mdvm"], DEFENDER_URLS["mdvm_plans"]]),

    dr("dpr-j38-defender", "J #38", "J Security",
       "Install anti-virus/anti-malware software on all equipment connected to networks used to process Microsoft Personal/Confidential Data (servers and desktops, all operating systems including Linux), kept patched and current with definitions updated daily; records must show the protection is active.",
       "Defender for Endpoint",
       "Microsoft Defender Antivirus (next-generation protection) across Windows, macOS, and Linux with cloud-delivered protection and multiple-times-daily security intelligence updates; device health and antivirus status reporting showing engine, platform, and definition currency per device",
       "Directly implements the anti-malware requirement on onboarded equipment (real-time protection with continuously current definitions across all mandated operating systems) and produces the active-protection records the evidence bullet demands.",
       "Defender for Endpoint onboarding across engagement servers and desktops; antivirus in active mode with cloud protection and daily-or-faster intelligence updates",
       "Device health and antivirus status reports (engine/definition versions per device); threat protection reports",
       [rel("intune", "contributing", "Intune endpoint security antivirus policy manages and attests the Defender Antivirus configuration on managed devices", "Endpoint Security")],
       "Server anti-malware licensing is separate (Microsoft Defender for Endpoint for Servers / Defender for Servers); equivalent records for systems not onboarded to Defender",
       "Direct Support", "High",
       DEFENDER_LIC["mde_p1"],
       DEFENDER_GOV["mde"],
       [SSPA, DPR_PDF, DEFENDER_URLS["ngav"]]),

    dr("dpr-j40-defender", "J #40", "J Security",
       "Run a DLP program: data classified, labelled, and protected; monitor systems processing Microsoft data for intrusions, loss, and unauthorized activity; program must include IDS/IPS, breach analysis, and offboarding communications.",
       "Defender for Endpoint",
       "The intrusion-detection/prevention and breach-analysis layer of the program: EDR behavioral sensors as host IDS/IPS on endpoints and servers, network protection blocking malicious destinations, automated investigation & remediation, and the unified Defender XDR incident queue for compromise-detection monitoring and post-breach analysis; Defender for Cloud Apps anomaly detection supplies the cloud-app monitoring slice",
       "Implements the host- and cloud-level IDS/IPS and system-compromise monitoring the requirement mandates, plus post-breach analysis of affected systems (incident investigation with vulnerability follow-up). The classify/label/protect DLP core is Purview's; network-appliance IDS/IPS for non-endpoint infrastructure remains external.",
       "Devices onboarded with EDR in block mode and network protection enabled; automated investigation remediation level set; Defender for Cloud Apps app connectors and anomaly policies active",
       "Incident queue exports with resolution evidence; automated investigation history; Defender for Cloud Apps anomaly alerts",
       [rel("purview", "primary", "The DLP program core (classification, labeling, protection, and egress monitoring) is Microsoft Purview DLP/Information Protection", "Data Loss Prevention"),
        rel("sentinel", "contributing", "SIEM correlation and retention for estate-wide monitoring beyond M365/endpoint telemetry")],
       "Network-appliance IDS/IPS for non-endpoint infrastructure; incident response and management process; offboarding communications process",
       "Partial Support", "High",
       DEFENDER_LIC["mde_p2"],
       DEFENDER_GOV["xdr"],
       [SSPA, DPR_PDF, DEFENDER_URLS["edr"], DEFENDER_URLS["incidents"], DEFENDER_URLS["air"]],
       also=["Defender for Cloud Apps"]),
]


# ==== Microsoft Sentinel rows (product #5, added 2026-07-18) ====
from common import SENTINEL_LIC, SENTINEL_URLS, SENTINEL_GOV, prow, rel
_S = "2026-07-18"
def sr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("sentinel", "sspa-dpr", "v12 (March 2026)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _S, licensing_model="consumption", also_involves=also)

ROWS += [
    sr("dpr-i30-31-sentinel", "I #30–31", "I Monitoring & Enforcement",
       "Maintain an incident response plan; notify Microsoft without undue delay on a Data Incident, cooperate with investigation (including scope of data accessed), remediate and track resolution.",
       "Incident Management & Investigation",
       "Auditable track-to-resolution record for every detected Data Incident: unified incident queue with timeline, ownership, and status; incident tasks encoding the response procedure's steps; automation rules stamping assignment and severity at creation; playbooks orchestrating notification/ticketing steps; SOC incident metrics (time-to-acknowledge/time-to-close) evidencing that tracking operates",
       "Implements the remediation-tracking and investigation-cooperation record the requirement demands. Each incident on connected telemetry exists as a documented case from detection to closure, with notification steps automatable as playbook actions. Sentinel documents and orchestrates; the IR plan itself, the without-undue-delay notification duty to Microsoft, and incidents outside connected sources are organizational.",
       "Automation rules assigning owner/severity on creation; incident task templates mirroring the Data Incident procedure; notification playbook wired to the escalation path",
       "Incident history exports with timeline and closure state; SOC incident audit metrics; playbook run history for notification steps",
       [rel("purview", "contributing", "Audit (Premium) crucial events and Activity explorer supply the scope-of-data-accessed forensic artifact (the stacked Purview row)", "Audit"),
        rel("defender-xdr", "contributing", "Defender XDR detections feed the unified incident queue for Microsoft-workload Data Incidents", "Defender for Endpoint")],
       "IR plan and breach-notification process; SupplierWeb security contacts; incidents on systems not connected to the workspace",
       "Partial Support", "High",
       SENTINEL_LIC["ingest"] + " " + SENTINEL_LIC["soar"],
       None,
       [SSPA, DPR_PDF, SENTINEL_URLS["incidents"], SENTINEL_URLS["soc_metrics"]],
       also=["Automation & Playbooks (SOAR)"]),

    sr("dpr-j40-sentinel", "J #40", "J Security",
       "Run a DLP program: data classified, labelled, and protected; monitor systems processing Microsoft data for intrusions, loss, and unauthorized activity; program must include IDS/IPS, breach analysis, and offboarding communications.",
       "Analytics Rules & Detections",
       "The estate-wide monitoring layer of the program: CEF/Syslog-over-AMA ingestion of the mandated network IDS/IPS and firewall alert streams alongside Purview DLP/IRM and Defender signals, scheduled/NRT analytics and Fusion correlation across those sources, and a retained monitoring record satisfying the 'procedures for monitoring system compromise detection tools' bullet from one pane",
       "Implements the monitor-information-systems slice across the whole estate. The requirement's mandated IDS/IPS tools emit alerts that Sentinel ingests, correlates, and retains, closing the network-infrastructure gap both stacked rows leave external. Sentinel monitors and evidences; the classify/label/protect DLP core is Purview's and the host IDS/IPS engine is Defender's.",
       "IDS/IPS and firewall connectors (CEF/Syslog via AMA) alongside the Purview and Defender XDR connectors; analytics rules covering intrusion and data-loss detections; alert-to-incident grouping configured",
       "Cross-source incident and detection trend reports; connector health showing continuous ingestion from compromise-detection tools",
       [rel("purview", "primary", "The DLP program core (classification, labeling, protection, and egress monitoring) is Microsoft Purview DLP/Information Protection (the stacked Purview row)", "Data Loss Prevention"),
        rel("defender-xdr", "contributing", "Defender for Endpoint EDR is the host IDS/IPS engine whose detections Sentinel correlates (the stacked Defender row)", "Defender for Endpoint")],
       "Network-appliance IDS/IPS platforms themselves; offboarding communications process; incident response and management process",
       "Partial Support", "High",
       SENTINEL_LIC["ingest"] + " " + SENTINEL_LIC["free_benefit"],
       None,
       [SSPA, DPR_PDF, SENTINEL_URLS["cef_syslog"], SENTINEL_URLS["analytics"]],
       also=["Data Collection & Connectors"]),
]


# ==== Microsoft Defender for Cloud rows (product #6, added 2026-07-18) ====
from common import MDC_LIC, MDC_URLS, MDC_GOV
_M = "2026-07-18"
def mr(id, ref, dom, intent, sol, cap, how, cfg, op, related, ext, cov, conf, lic, cloud, sources, also=None):
    return prow("defender-cloud", "sspa-dpr", "v12 (March 2026)", id, ref, dom, intent, sol, cap, how, cfg, op,
                related, ext, cov, conf, lic, cloud, sources, _M, licensing_model="consumption", also_involves=also)

ROWS += [
    mr("dpr-j38-mdc", "J #38", "J Security",
       "Install anti-virus/anti-malware software on all equipment connected to networks used to process Microsoft Personal/Confidential Data (servers and desktops, all operating systems including Linux), kept patched and current with definitions updated daily; records must show the protection is active.",
       "Defender for Servers",
       "Extends the anti-malware mandate to cloud and hybrid server estates: Defender for Servers deploys and licenses the integrated Microsoft Defender for Endpoint for Servers (Windows and Linux across Azure, AWS, GCP, and on-premises via Azure Arc) per protected server, with endpoint-protection assessment recommendations flagging machines whose anti-malware is missing, unhealthy, or out of date; Defender for Storage adds on-upload malware scanning for blob storage used to exchange supplier data",
       "Covers the supplier's server estate, the equipment class the stacked Defender XDR row's per-user endpoint licensing does not reach. The engine is Microsoft Defender Antivirus under MDE (the stacked Defender XDR row); Defender for Servers is the per-server consumption vehicle that deploys it across clouds and evidences that protection is active, and storage malware scanning is Defender-for-Cloud-native. Desktop coverage and definition-currency operations remain the endpoint story.",
       "Defender for Servers enabled on every subscription whose servers process Microsoft data; endpoint-protection assessment recommendations remediated; Defender for Storage malware scanning on data-exchange storage accounts",
       "Per-server plan coverage export; endpoint-protection assessment recommendation history showing active/healthy protection; storage malware-scan verdict log",
       [rel("defender-xdr", "primary", "Microsoft Defender Antivirus/MDE is the anti-malware engine on servers and desktops (the stacked Defender XDR row); seam: Defender for Servers licenses and deploys it per server for cloud estates; MDE covers user endpoints under per-user licensing", "Defender for Endpoint")],
       "Anti-malware deployment on equipment outside Azure/Arc onboarding; daily definition-update operations on every OS image; records retention for AV status",
       "Partial Support", "High",
       MDC_LIC["servers_p1"],
       MDC_GOV["servers"],
       [SSPA, DPR_PDF, MDC_URLS["servers"], MDC_URLS["mde_integration"], MDC_URLS["malware_scan"]],
       also=["Workload Protection Plans"]),

    mr("dpr-j40-mdc", "J #40", "J Security",
       "Run a DLP program: data classified, labelled, and protected; monitor systems processing Microsoft data for intrusions, loss, and unauthorized activity; program must include IDS/IPS, breach analysis, and offboarding communications.",
       "Workload Protection Plans",
       "Cloud-workload intrusion detection for systems processing Microsoft data in Azure/AWS/GCP: threat-detection plans for Storage (suspicious access, unusual extraction, malware distribution), Databases (SQL injection, brute force, anomalous access), Containers (runtime and control-plane attacks), Key Vault and Resource Manager (credential/control-plane abuse), and Servers (behavioral, fileless, and network-layer alerts; DNS-layer alerts with Plan 2). Alerts stream into the Microsoft Defender portal and Sentinel",
       "Supplies the intrusion-detection slice for the cloud-workload plane that neither stacked detection row natively senses: storage accounts, databases, Kubernetes, and the cloud control plane. Defender for Cloud detects for cloud workloads; the DLP program core is Purview's, host IDS/IPS on endpoints is Defender XDR's, network-appliance IDS/IPS stays external, and breach analysis runs in the SOC.",
       "Workload protection plans enabled on subscriptions processing Microsoft data; alert export to the Defender portal/Sentinel configured; email notifications for high-severity alerts",
       "Cloud workload alert history by plan; incident correlation records in the Defender portal; plan-coverage report per subscription",
       [rel("purview", "primary", "The DLP program core (classification, labeling, protection, egress monitoring) is Microsoft Purview (the stacked Purview row)", "Data Loss Prevention"),
        rel("defender-xdr", "contributing", "Defender for Endpoint carries host-level IDS/IPS on endpoints; Defender for Cloud alerts correlate with it in the same Defender portal; seam, not overlap", "Defender for Endpoint"),
        rel("sentinel", "contributing", "Defender for Cloud security alerts ingest into Sentinel free of charge for estate-wide correlation and retention (the stacked Sentinel row)", "Data Collection & Connectors")],
       "Network-appliance IDS/IPS platforms; breach-analysis and offboarding-communication processes",
       "Partial Support", "High",
       MDC_LIC["workload"],
       MDC_GOV["gaps"],
       [SSPA, DPR_PDF, MDC_URLS["alerts"], MDC_URLS["xdr_integration"]],
       also=["Defender for Servers"]),
]
