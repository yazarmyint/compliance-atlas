"""Shared constants for the compliance-atlas dataset builders."""

VERIFIED_DATE = "2026-07-16"

# ---------------------------------------------------------------------------
# Data re-verification passes (AUDIT-FINDINGS SS22).
#
# last_verified is a claim about when a row's facts were last checked against an
# authoritative source, so it is bumped only where that is true. A row earns a
# pass's date on exactly one of three bases:
#
#   A  its license_requirement changed in that pass
#   B  its sources changed in that pass
#   C  the licensing constant governing it was re-fetched live in that pass and
#      confirmed still correct (a PASS is a verification, not a non-event)
#
# A and C are both derived from the pass's LIC-key set: it names every constant
# whose governing authoritative source was actually fetched on that date, whether
# the string changed or passed. Constants absent from every set were NOT re-checked
# at all, so rows resting solely on them keep their authoring date. That is the
# point of the mechanism, and it is why the 2026-07-19 pass moved 324 of 378 rows
# rather than all of them. Do not add a key without fetching its source.
#
# Passes are applied in order by REVERIFY_PASSES, so a row touched by more than one
# pass ends on the latest date that actually verified something it rests on.
# ---------------------------------------------------------------------------
REVERIFY_DATE = "2026-07-19"

# (dict name, key) pairs re-derived or re-confirmed against a live fetch on 2026-07-19.
REVERIFIED_LIC_KEYS = {
    # Purview service description per-feature tables
    ("LIC", "labels_manual"), ("LIC", "labels_auto"), ("LIC", "label_encryption"),
    ("LIC", "customer_key"), ("LIC", "classification_analytics"), ("LIC", "dlp_core"),
    ("LIC", "dlp_teams"), ("LIC", "dlp_endpoint"), ("LIC", "retention_basic"),
    ("LIC", "retention_advanced"), ("LIC", "records"), ("LIC", "audit_std"),
    ("LIC", "audit_prem"), ("LIC", "ediscovery_std"), ("LIC", "irm"), ("LIC", "cc"),
    ("LIC", "ib"), ("LIC", "cm"),
    # Entra licensing article
    ("ENTRA_LIC", "ca"), ("ENTRA_LIC", "mfa"), ("ENTRA_LIC", "id_protection"),
    ("ENTRA_LIC", "pim"), ("ENTRA_LIC", "gov_core"), ("ENTRA_LIC", "gov_lcw"),
    ("ENTRA_LIC", "free"),
    # Defender service description + Defender XDR prerequisites
    ("DEFENDER_LIC", "mde_p1"), ("DEFENDER_LIC", "mde_p2"), ("DEFENDER_LIC", "mdvm"),
    ("DEFENDER_LIC", "mdo_p1"), ("DEFENDER_LIC", "mdo_p2"), ("DEFENDER_LIC", "mdi"),
    ("DEFENDER_LIC", "mdca"), ("DEFENDER_LIC", "xdr"),
    # Sentinel billing article (+ Partner Center announcement for the 50 GB tier)
    ("SENTINEL_LIC", "ingest"), ("SENTINEL_LIC", "retention"), ("SENTINEL_LIC", "soar"),
    ("SENTINEL_LIC", "included"),
    # Azure pricing page for Defender for Cloud
    ("MDC_LIC", "foundational"), ("MDC_LIC", "cspm"), ("MDC_LIC", "workload"),
}

# ---------------------------------------------------------------------------
# Completion pass, 2026-07-20 (AUDIT-FINDINGS SS22.11). The eight constants the
# 2026-07-19 pass left unverified, and the five source families it did not reach,
# were fetched live on 2026-07-20. Nothing is now carried as "not re-verified".
# ---------------------------------------------------------------------------
REVERIFY_DATE_2 = "2026-07-20"

# (dict name, key) pairs re-derived or re-confirmed against a live fetch on 2026-07-20.
#   INTUNE_LIC p1, p1_ca, epm      - Intune licensing article + planning guide step 3
#   MDC_LIC servers_p1, servers_p2 - Defender for Servers plan-selection / overview / FAQ
#   MDC_LIC dashboard              - update-regulatory-compliance-packages prerequisites
#   SENTINEL_LIC free_benefit      - Microsoft 365 Sentinel benefit offer page
#   LIC dspm, dspm_ai              - DSPM get-started + DSPM-for-AI prerequisites
REVERIFIED_LIC_KEYS_2 = {
    ("INTUNE_LIC", "p1"), ("INTUNE_LIC", "p1_ca"), ("INTUNE_LIC", "epm"),
    ("MDC_LIC", "servers_p1"), ("MDC_LIC", "servers_p2"), ("MDC_LIC", "dashboard"),
    ("SENTINEL_LIC", "free_benefit"),
    ("LIC", "dspm"), ("LIC", "dspm_ai"),
}

# Rows whose sources array changed on 2026-07-19 (basis B, PR-038 URL currency).
REVERIFIED_SOURCE_ROWS = {
    "171-3-14-6-sentinel", "171-3-3-4-sentinel", "171-3-3-5-sentinel", "171-3-4-1-intune",
    "53-au-6-sentinel", "53-ia-5-entra", "53-ir-4-sentinel", "53-si-4-sentinel",
    "csf-de-ae-02-sentinel", "csf-de-ae-03-sentinel", "csf-de-cm-01-sentinel",
    "csf-id-am-01-intune", "csf-pr-aa-01-entra", "csf-pr-aa-02-entra",
    "csf-rs-mi-01-02-sentinel", "dpr-j35-intune", "dpr-j38-mdc", "dpr-j40-sentinel",
    "gdpr-32-1-b-sentinel", "gdpr-32-1-d-sentinel", "gdpr-33-34-sentinel",
    "glba-314-4-c2-intune", "glba-314-4-c8-sentinel", "glba-314-4-d-sentinel",
    "glba-314-4-h-sentinel", "hipaa-308-a1-d-sentinel", "hipaa-308-a5-b-mdc",
    "hipaa-310-d1-intune", "iso-a-5-17-entra", "iso-a-5-25-sentinel",
    "iso-a-5-26-sentinel", "iso-a-5-9-intune", "iso-a-8-16-sentinel", "iso-a-8-7-mdc",
    "pci-10-4-1-sentinel", "pci-10-7-2-sentinel", "pci-8-2-1-entra",
    "soc2-cc6-8-defender", "soc2-cc6-8-mdc", "soc2-cc7-2-sentinel",
    "soc2-cc7-3-sentinel", "soc2-cc7-4-sentinel",
}


def reverified_license_strings(keys=None):
    """The literal license strings governed by a constant re-verified in a pass."""
    dicts = {"LIC": LIC, "ENTRA_LIC": ENTRA_LIC, "INTUNE_LIC": INTUNE_LIC,
             "DEFENDER_LIC": DEFENDER_LIC, "SENTINEL_LIC": SENTINEL_LIC, "MDC_LIC": MDC_LIC}
    out = set()
    for dict_name, key in (REVERIFIED_LIC_KEYS if keys is None else keys):
        value = dicts[dict_name][key]
        assert value, f"re-verified key names an empty constant: {dict_name}[{key!r}]"
        out.add(value)
    return out


def reverify_passes():
    """Re-verification passes in date order: (date, license strings, source rows).

    Applied in this order, so a row covered by more than one pass ends on the
    latest date that verified something it actually rests on.
    """
    return [
        (REVERIFY_DATE, reverified_license_strings(REVERIFIED_LIC_KEYS), REVERIFIED_SOURCE_ROWS),
        (REVERIFY_DATE_2, reverified_license_strings(REVERIFIED_LIC_KEYS_2), frozenset()),
    ]

# ---------------------------------------------------------------------------
# Product dimension (platform generalization, 2026-07-17).
# PRODUCTS = products that HAVE mapping rows in the atlas. Seeded with Purview only.
# RELATED_PRODUCTS = Microsoft products that rows may reference as dependencies
# (related_microsoft.product slugs). When one of these is promoted to a full atlas
# product, it moves into PRODUCTS and row-level links can be attached without a
# further data migration (the slug is already the join key).
# ---------------------------------------------------------------------------
PRODUCTS = {
    "purview": {
        "id": "purview",
        "official_name": "Microsoft Purview",  # verified 2026-07-17 against https://learn.microsoft.com/purview/purview ("Learn about Microsoft Purview")
        "short_name": "Purview",
        "naming_source": "https://learn.microsoft.com/purview/purview",
        "solutions": [],  # derived at import bottom from SOLUTIONS entries tagged product="purview"
        "licensing_source": "https://learn.microsoft.com/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-purview-service-description",
        "default_licensing_model": "per_user",
        "notes": "Microsoft's data security, governance, and compliance suite for the Microsoft 365 estate: classification and labeling, data loss prevention, lifecycle and records, insider risk, eDiscovery, and audit. Licensed per user. It implements and evidences data-layer controls, and marks deliberate gaps honestly rather than overclaiming.",
        "notes_detail": ("Microsoft Purview: data security, governance, and compliance across the Microsoft 365 estate: "
                  "classification and labeling, DLP, data lifecycle and records, insider risk, communication compliance, "
                  "eDiscovery, and audit. Licensed per user, drawn exclusively from the Microsoft Purview service "
                  "description per-feature tables (E3-tier for the baseline capabilities, E5-tier or the Purview Suite for "
                  "the advanced ones). Mapping discipline: Purview implements and evidences data-layer controls; deliberate "
                  "gaps render as 'None (boundary row)'."),
    },
    "entra": {
        "id": "entra",
        # Family name is "Microsoft Entra"; the core directory is "Microsoft Entra ID" (formerly Azure AD — retired). Verified 2026-07-17.
        "official_name": "Microsoft Entra",
        "short_name": "Entra",
        "naming_source": "https://learn.microsoft.com/entra/fundamentals/what-is-entra",
        "solutions": [],  # derived at import bottom from SOLUTIONS entries tagged product="entra"
        "licensing_source": "https://learn.microsoft.com/entra/fundamentals/licensing",
        "default_licensing_model": "per_user",
        "notes": "Microsoft's identity and access platform (formerly Azure AD), covering conditional access, authentication, privileged access, and identity governance. Licensing is tiered and capability-specific, so the exact entitlement depends on the feature. Permissions Management was retired and is deliberately left off the map.",
        "notes_detail": ("Microsoft Entra identity & access. 'Azure AD' is retired; the directory is 'Microsoft Entra ID'. "
                  "Licensing tiers: Entra ID Free / P1 / P2, plus the Microsoft Entra ID Governance SKU and Microsoft Entra Suite. "
                  "Per-capability tiers matter: Conditional Access = P1; ID Protection & PIM = P2; Lifecycle Workflows = ID Governance SKU. "
                  "Microsoft Entra Permissions Management (CIEM) was retired 2025-10-01 and is deliberately not mapped (historical note in AUDIT-FINDINGS §11)."),
    },
    "intune": {
        "id": "intune",
        # Product name is "Microsoft Intune" (the "Microsoft Endpoint Manager" umbrella branding was retired;
        # Configuration Manager is a separate product). Docs moved to learn.microsoft.com/intune/* (no /mem/). Verified 2026-07-17.
        "official_name": "Microsoft Intune",
        "short_name": "Intune",
        "naming_source": "https://learn.microsoft.com/intune/fundamentals/what-is-intune",
        "solutions": [],  # derived at import bottom from SOLUTIONS entries tagged product="intune"
        "licensing_source": "https://learn.microsoft.com/intune/fundamentals/licensing",
        "default_licensing_model": "per_user",
        "notes": "Microsoft's cloud endpoint management for devices and apps: compliance, configuration, security baselines, app protection, and enrollment. Licensing is tiered with several separately gated add-ons, and a 2026 restructure is redistributing them across Microsoft 365 plans. Configuration Manager and Endpoint DLP sit outside its scope here.",
        "notes_detail": ("Microsoft Intune cloud-based unified endpoint management (devices + apps). Licensing: Intune Plan 1 (base) / "
                  "Plan 2 / Microsoft Intune Suite, plus per-capability add-ons (Endpoint Privilege Management, Advanced Analytics, "
                  "Remote Help, Cloud PKI, Enterprise App Management), each separately gated. July 2026 restructure distributes Suite "
                  "capabilities across Microsoft 365 tiers (E3: Plan 2 + Remote Help + Advanced Analytics; E5/E7: adds EPM, Cloud PKI, EAM). "
                  "Scope decisions: Configuration Manager (ConfigMgr/SCCM) is not a separate atlas product (cloud-forward scope); "
                  "co-management is noted on relevant Intune rows only (AUDIT-FINDINGS §12). Endpoint DLP belongs to Purview, not Intune."),
    },
    "defender-xdr": {
        "id": "defender-xdr",
        # Product name is "Microsoft Defender XDR" (lineage: Microsoft Threat Protection → Microsoft 365 Defender →
        # Microsoft Defender XDR). ONE product; the four workloads (MDE, MDO, MDI, MDCA) are solutions under the
        # unified portal (security.microsoft.com), not separate atlas products. Verified 2026-07-17.
        "official_name": "Microsoft Defender XDR",
        "short_name": "Defender XDR",
        "naming_source": "https://learn.microsoft.com/defender-xdr/microsoft-365-defender",
        "solutions": [],  # derived at import bottom from SOLUTIONS entries tagged product="defender-xdr"
        "licensing_source": "https://learn.microsoft.com/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-defender-service-description",
        "default_licensing_model": "per_user",
        "notes": "Microsoft's unified detection and response across endpoints, email, identity, and SaaS apps, run from one portal. Each workload has its own plan gating, so the covered capabilities depend on what is licensed. Azure-resource posture and SIEM live in separate atlas products, a deliberate seam rather than a gap.",
        "notes_detail": ("Microsoft Defender XDR: unified pre-/post-breach detection & response across endpoints (Defender for "
                  "Endpoint), email & collaboration (Defender for Office 365), on-prem/hybrid identity (Defender for "
                  "Identity), and SaaS apps (Defender for Cloud Apps). Per-workload plan gating matters: MDE Plan 1 "
                  "(E3-tier) has no EDR/AIR/vulnerability-management (those are Plan 2, E5-tier); MDO Plan 2 (not Plan 1) "
                  "carries Threat Explorer/AIR/attack simulation and full XDR integration. Defender XDR has no separate "
                  "license; entitlement follows the onboarded workloads. Defender for Cloud (CSPM/CWPP) and Sentinel are "
                  "separate atlas products, so no Azure-resource posture is mapped here (a seam; Defender for Cloud "
                  "alerts surface in the same Defender portal). MDCA session/access controls are reverse-proxy/"
                  "browser-scoped and never rated as covering native-client scenarios (AUDIT-FINDINGS §13)."),
    },
    "sentinel": {
        "id": "sentinel",
        # Product name is "Microsoft Sentinel" ("Azure Sentinel" is retired branding). Cloud-native SIEM + SOAR,
        # generally available in the Microsoft Defender portal (unified SecOps) including for customers without
        # Defender XDR or E5; the Azure-portal experience retires March 31, 2027 (extended from July 1, 2026 —
        # partner announcement Feb 12, 2026). New tenants are auto-onboarded to the Defender portal since July 2025.
        # Verified 2026-07-18.
        "official_name": "Microsoft Sentinel",
        "short_name": "Sentinel",
        "naming_source": "https://learn.microsoft.com/azure/sentinel/overview",
        "solutions": [],  # derived at import bottom from SOLUTIONS entries tagged product="sentinel"
        "licensing_source": "https://learn.microsoft.com/azure/sentinel/billing",
        "default_licensing_model": "consumption",
        "notes": "Microsoft's cloud-native SIEM and SOAR: it collects security logs from across the estate, correlates them into incidents, and retains them for the long-dated mandates other tools cannot satisfy. Priced by data volume rather than per user. It evidences and detects; it does not enforce.",
        "notes_detail": ("Microsoft Sentinel: cloud-native SIEM + SOAR, and the first consumption-priced atlas product, billed "
                  "on data ingestion and retention, never per user (pay-as-you-go or commitment tiers; per-row "
                  "license_requirement carries the meter detail). The 2025 platform change mirrors the analytics tier "
                  "(90-day included retention, extendable to 2 years) into the Microsoft Sentinel data lake for total "
                  "retention up to 12 years, the mechanism behind long-dated log-retention mandates. Cost levers that "
                  "matter: free data sources (Office 365 audit, Azure Activity, all Defender alerts) and the Microsoft 365 "
                  "E5/E7 data grant. Mapping discipline: Sentinel evidences and detects, it does not enforce; Direct "
                  "Support only where the namesake activity is log collection, retention, correlation/analysis, or "
                  "security monitoring/alerting. Defender for Cloud (product #6) owns posture and cloud-workload detection."),
    },
    "defender-cloud": {
        "id": "defender-cloud",
        # Product name is "Microsoft Defender for Cloud" (lineage: Azure Security Center + Azure Defender →
        # Microsoft Defender for Cloud). CNAPP: CSPM + CWPP for Azure, AWS, and GCP resources. Verified 2026-07-18.
        # FIRST NON-M365 product in the atlas — it assesses and protects cloud infrastructure, not M365 workloads.
        "official_name": "Microsoft Defender for Cloud",
        "short_name": "Defender for Cloud",
        "naming_source": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction",
        "solutions": [],  # derived at import bottom from SOLUTIONS entries tagged product="defender-cloud"
        "licensing_source": "https://azure.microsoft.com/pricing/details/defender-for-cloud/",
        "default_licensing_model": "consumption",
        "notes": "Microsoft's cloud-native protection for Azure, AWS, and GCP infrastructure rather than Microsoft 365: posture management plus workload threat detection. Priced per protected resource, with a free posture tier. It assesses and detects rather than remediates, so many hardening controls rate partial, and its compliance dashboard scores cloud resources, not the whole estate.",
        "notes_detail": ("Microsoft Defender for Cloud: cloud-native application protection (CNAPP): CSPM plus CWPP for Azure, "
                  "AWS, and GCP resources, and the first non-M365 atlas product (it assesses cloud infrastructure, not "
                  "Microsoft 365 workloads). Second consumption-priced product: billed per protected resource, with a "
                  "free Foundational CSPM tier (secure score, MCSB recommendations, asset inventory, multicloud "
                  "connectors); per-row license_requirement carries the meter detail. Mapping discipline: it assesses and "
                  "detects, it does not remediate; recommendations are advisory, so hardening controls rate Partial "
                  "where the product only finds the gap; Direct is reserved for configuration/compliance assessment, "
                  "vulnerability assessment, inventory, and cloud-workload threat detection. The regulatory compliance "
                  "dashboard covers onboarded cloud resources against a standard's technically-assessable subset only, "
                  "not M365, on-premises, or procedural controls, and not an attestation (Purview Compliance Manager "
                  "assesses the M365 estate: a seam, not an overlap). Azure platform services (Key Vault, Firewall/WAF, "
                  "Azure Policy, RBAC) are not this product; they appear only as external dependencies."),
    },
}

# Products a row may reference as a dependency (related_microsoft.product) but that do NOT yet
# have their own rows. When one graduates to a full atlas product it moves into PRODUCTS above.
# Entra graduated 2026-07-17; Intune graduated 2026-07-17 (same day, later session);
# Defender XDR graduated 2026-07-17 (later session again); Sentinel graduated 2026-07-18;
# Defender for Cloud graduated 2026-07-18 (final product — the roadmap is complete; priva stays
# reference-only permanently, per the roadmap-closure decision in AUDIT-FINDINGS §15).
# prodFull()/relatedBlock() in the template resolve either map.
RELATED_PRODUCTS = {
    "priva": "Microsoft Priva",
}

# Canonical Purview solution names (pivot keys). Display metadata lives in SOLUTIONS.
SOLUTIONS = {
    "Information Protection": {
        "full_name": "Microsoft Purview Information Protection",
        "scope": "Sensitivity labels with label-based encryption and content marking, Double Key Encryption, and Customer Key; persistent, portable protection that travels with the content",
        "url": "https://learn.microsoft.com/purview/information-protection",
    },
    "Data Classification": {
        "full_name": "Microsoft Purview data classification (SITs, trainable classifiers, EDM, explorers)",
        "scope": "Sensitive information types, trainable classifiers, exact data match, Data explorer / Content explorer (classic), Activity explorer",
        "url": "https://learn.microsoft.com/purview/data-classification-overview",
    },
    "Data Loss Prevention": {
        "full_name": "Microsoft Purview Data Loss Prevention",
        "scope": "DLP for Exchange/SharePoint/OneDrive/Teams, Endpoint DLP, browser & network DLP, on-premises scanner, DLP for AI",
        "url": "https://learn.microsoft.com/purview/dlp-learn-about-dlp",
    },
    "Insider Risk Management": {
        "full_name": "Microsoft Purview Insider Risk Management",
        "scope": "Risk policies (data theft/leaks), sequence & anomaly detection, forensic evidence, Adaptive Protection",
        "url": "https://learn.microsoft.com/purview/insider-risk-management",
    },
    "Communication Compliance": {
        "full_name": "Microsoft Purview Communication Compliance",
        "scope": "Detection and remediation of policy-violating messages across Exchange, Teams, Viva Engage, Copilot",
        "url": "https://learn.microsoft.com/purview/communication-compliance-solution-overview",
    },
    "Information Barriers": {
        "full_name": "Microsoft Purview Information Barriers",
        "scope": "Segment-based restriction of two-way communication and collaboration between conflicting groups (ethical walls) in Teams, SharePoint, and OneDrive",
        "url": "https://learn.microsoft.com/purview/information-barriers",
    },
    "Data Lifecycle Management": {
        "full_name": "Microsoft Purview Data Lifecycle Management",
        "scope": "Retention policies and labels with retain-and-delete actions, adaptive scopes, inactive-mailbox handling, and mailbox archiving across the M365 estate",
        "url": "https://learn.microsoft.com/purview/data-lifecycle-management",
    },
    "Records Management": {
        "full_name": "Microsoft Purview Records Management",
        "scope": "File plan, record and regulatory-record declaration, event-based retention, single- and multi-stage disposition review, and proof of disposal",
        "url": "https://learn.microsoft.com/purview/records-management",
    },
    "eDiscovery": {
        "full_name": "Microsoft Purview eDiscovery",
        "scope": "Unified eDiscovery: searches, holds, cases; premium features (custodians, review sets, analytics). Classic experiences retired Aug 2025",
        "url": "https://learn.microsoft.com/purview/edisc",
    },
    "Audit": {
        "full_name": "Microsoft Purview Audit (Standard/Premium)",
        "scope": "Unified audit log; Premium: 1-yr default retention (10-yr add-on), crucial events (MailItemsAccessed), higher API bandwidth",
        "url": "https://learn.microsoft.com/purview/audit-solutions-overview",
    },
    "Compliance Manager": {
        "full_name": "Microsoft Purview Compliance Manager",
        "scope": "Regulatory assessment templates, improvement actions with continuous control testing, and a compliance score tracking control implementation across the tenant",
        "url": "https://learn.microsoft.com/purview/compliance-manager",
    },
    "DSPM": {
        "full_name": "Microsoft Purview Data Security Posture Management",
        "scope": "Data risk discovery/analytics across M365 + Azure/Fabric/third-party (current version); DSPM (classic) for M365",
        "url": "https://learn.microsoft.com/purview/data-security-posture-management-learn-about",
    },
    "DSPM for AI": {
        "full_name": "Microsoft Purview DSPM for AI (classic; converging into DSPM)",
        "scope": "Visibility and policy for AI interactions: M365 Copilot, agents, Entra-registered and third-party AI apps",
        "url": "https://learn.microsoft.com/purview/dspm-for-ai",
    },
}

# License strings — sourced ONLY from the Microsoft Purview service description per-feature rows.
SD = "https://learn.microsoft.com/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-purview-service-description"
LIC = {
    "labels_manual": "Manual sensitivity labeling: Microsoft 365 E5/A5/G5/E3/A3/G3/F1/F3 or Business Premium; also Office 365 E5/A5/E3/A3, Enterprise Mobility + Security E3/E5, OneDrive for Business (Plan 2), and Azure Information Protection Plan 1/Plan 2",
    "labels_auto": "Automatic/policy-based sensitivity labeling: Microsoft 365 E5/A5/G5, Office 365 E5/A5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Information Protection & Governance",
    "label_encryption": "Label-based encryption: included with sensitivity labeling entitlements (manual E3+; automatic application E5-tier)",
    "customer_key": "Customer Key: Microsoft 365 E5/A5/G5, Office 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, or Microsoft 365 E5/A5/F5/G5 Information Protection & Governance",
    "classification_analytics": "Data classification analytics (Data/Content/Activity explorer): Microsoft 365 E5/A5/G5, Office 365 E5, Microsoft 365 E5/A5/G5 Compliance (Purview Suite), or Microsoft 365 E5/A5/G5 Information Protection & Governance; E3/A3/G3 tenants keep the underlying Content explorer data aggregation without the explorer interfaces",
    "dlp_core": "DLP for Exchange/SharePoint/OneDrive: Microsoft 365 E5/A5/G5/E3/A3/G3 or Business Premium; also Office 365 E5/A5/G5/E3/A3/G3, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, SharePoint Online Plan 2, OneDrive for Business (Plan 2), or Exchange Online Plan 2",
    "dlp_teams": "DLP for Teams: Microsoft 365 E5/A5/G5, Office 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Information Protection & Governance",
    "dlp_endpoint": "Endpoint DLP: Microsoft 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Information Protection & Governance (no Office 365 path; Endpoint DLP is Microsoft 365 only)",
    "retention_basic": "Org/location-wide retention policies & manual retention labels: Microsoft 365 E5/A5/G5/E3/A3/G3 or Business Premium; also Office 365 E5/A5/G5/E3/A3/G3, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Information Protection & Governance",
    "retention_advanced": "Adaptive scopes / auto-apply retention: Microsoft 365 E5/A5/G5, Office 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Information Protection & Governance",
    "records": "Records Management (file plan, record declaration, disposition review): Microsoft 365 E5/A5/G5, Office 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Information Protection & Governance",
    "audit_std": "Audit (Standard): included across Microsoft 365/Office 365 enterprise, government, and business plans (180-day retention)",
    "audit_prem": "Audit (Premium): Microsoft 365 E5/A5/G5, Office 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/G5/F5 eDiscovery & Audit; 10-year retention needs the add-on license",
    "ediscovery_std": "eDiscovery (search, cases, hold, export): Microsoft 365 E3 or Office 365 E3/A3/G3/F3; premium features (custodians, review sets, analytics): Microsoft 365 E5/A5/F5/G5, Office 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, or Microsoft 365 E5/A5/F5/G5 eDiscovery & Audit",
    "irm": "Insider Risk Management: Microsoft 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Insider Risk Management",
    "cc": "Communication Compliance: Microsoft 365 E5/A5/G5, Office 365 E5/A5/G5, Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/A5/F5/G5 Insider Risk Management",
    "ib": "Information Barriers: Microsoft 365 E5/A5/G5, Microsoft Purview Suite, or E5 Insider Risk Management add-on (restricted users need licenses)",
    "cm": "Compliance Manager: baseline included with Microsoft 365/Office 365 plans; premium regulation templates licensed separately (3 premium templates included at E5/A5/G5)",
    "dspm": "DSPM: Microsoft 365 E5 or Microsoft Purview Suite (per DSPM get-started documentation; not yet a service-description row)",
    "dspm_ai": "DSPM for AI: Microsoft 365 E5 or Microsoft Purview Suite; monitored Copilot users need Microsoft 365 Copilot licenses; some non-M365 sources are pay-as-you-go",
}

# Frequently cited Learn URLs
URLS = {
    "labels": "https://learn.microsoft.com/purview/sensitivity-labels",
    "label_encrypt": "https://learn.microsoft.com/purview/encryption-sensitivity-labels",
    "ip": "https://learn.microsoft.com/purview/information-protection",
    "sit": "https://learn.microsoft.com/purview/sit-sensitive-information-type-entity-definitions",
    "classifiers": "https://learn.microsoft.com/purview/trainable-classifiers-learn-about",
    "data_explorer": "https://learn.microsoft.com/purview/data-classification-data-explorer",
    "content_explorer": "https://learn.microsoft.com/purview/data-classification-content-explorer",
    "activity_explorer": "https://learn.microsoft.com/purview/data-classification-activity-explorer",
    "dlp": "https://learn.microsoft.com/purview/dlp-learn-about-dlp",
    "dlp_endpoint": "https://learn.microsoft.com/purview/endpoint-dlp-learn-about",
    "dlp_policy": "https://learn.microsoft.com/purview/dlp-policy-reference",
    "retention": "https://learn.microsoft.com/purview/retention",
    "dlm": "https://learn.microsoft.com/purview/data-lifecycle-management",
    "records": "https://learn.microsoft.com/purview/records-management",
    "disposition": "https://learn.microsoft.com/purview/disposition",
    "edisc": "https://learn.microsoft.com/purview/edisc",
    "audit": "https://learn.microsoft.com/purview/audit-solutions-overview",
    "audit_search": "https://learn.microsoft.com/purview/audit-search",
    "irm": "https://learn.microsoft.com/purview/insider-risk-management",
    "adaptive": "https://learn.microsoft.com/purview/insider-risk-management-adaptive-protection",
    "cc": "https://learn.microsoft.com/purview/communication-compliance-solution-overview",
    "ib": "https://learn.microsoft.com/purview/information-barriers",
    "cm": "https://learn.microsoft.com/purview/compliance-manager",
    "cm_regs": "https://learn.microsoft.com/purview/compliance-manager-regulations-list",
    "dspm": "https://learn.microsoft.com/purview/data-security-posture-management-learn-about",
    # No "dspm_ai" URL: /purview/dspm-for-ai now carries a "(classic)" banner naming
    # data-security-posture-management-learn-about as its replacement (confirmed live 2026-07-20), so
    # the two rows that cited it were repointed to URLS["dspm"] — which both already cited, making the
    # repoint a de-duplication. LIC["dspm_ai"] and the "DSPM for AI" solution stay: the classic solution
    # is still a distinct licensed thing in the portal, and SOLUTIONS["DSPM for AI"] correctly keeps the
    # classic article as its own documentation. See docs/MAINTENANCE.md for the retirement trigger.
    "customer_key": "https://learn.microsoft.com/purview/customer-key-overview",
    "sd": SD,
    "gcch": "https://learn.microsoft.com/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/plan-for-microsoft-purview-gcc-high-deployments",
}

# GCC High/DoD note fragments (verified against the GCC High deployment guide, 2026-07-16)
GOV = {
    "dlp_endpoint": "Endpoint DLP, Teams DLP, and on-premises scanner: Available in GCC/GCC High/DoD (Purview GCC High deployment guide).",
    "labels_auto": "Auto-labeling for Exchange/SharePoint/OneDrive, Office apps, and containers: Available in GCC High; named-entity SITs remain on engineering backlog in GCC High.",
    "classification": "Content/Activity explorer analytics: Available in GCC High (Teams data in Content explorer still in development).",
    "audit": "Audit (Standard/Premium) incl. 1-year and 10-year retention: Available in GCC High/DoD.",
    "edisc": "eDiscovery standard and premium features: Available in GCC High (a few premium items, e.g., Teams transcript collection, in development).",
    "records": "Records Management incl. disposition review and proof of disposal: Available in GCC High; auto-apply record labels via trainable classifiers in development.",
    "irm": "IRM core policies (data theft by departing users, general data leaks, forensic evidence): Available in GCC High; analytics and several policy templates in preview/development.",
    "cc": "Communication Compliance core: Available in GCC High.",
    "ib": "Information Barriers: Available in GCC High.",
    "cm": "Compliance Manager: Available in GCC/GCC High/DoD; CMMC templates included by default for government tenants.",
    "customer_key": "Customer Key and Double Key Encryption: Available in GCC High.",
    "dspm_ai": "DSPM for AI in GCC High/DoD: available for supported AI sites only; browse-to-URL policies cannot be created.",
}

# ===========================================================================
# Entra (product #2, added 2026-07-17).
# Licensing verified against the Microsoft Entra licensing service description
# (https://learn.microsoft.com/entra/fundamentals/licensing) and ID Governance
# licensing fundamentals — NOT the Purview service description. Naming and
# government-cloud availability verified on Microsoft Learn 2026-07-17.
# ===========================================================================
ENTRA_SOLUTIONS = {
    "Conditional Access & Authentication": {
        "product": "entra",
        "full_name": "Microsoft Entra ID core: Conditional Access, authentication & directory access controls",
        "scope": "Entra ID core: Conditional Access policy engine (grant/block/session; device, location, app, risk conditions); MFA; authentication methods and strengths (phishing-resistant/FIDO2); authentication policies; RBAC; self-service password reset & password protection; unique identities; sign-in and audit logs",
        "url": "https://learn.microsoft.com/entra/identity/conditional-access/overview",
    },
    "Entra ID Protection": {
        "product": "entra",
        "full_name": "Microsoft Entra ID Protection",
        "scope": "Sign-in and user risk detection, risk-based Conditional Access, risky users / risky sign-ins reports, automated risk remediation",
        "url": "https://learn.microsoft.com/entra/id-protection/overview-identity-protection",
    },
    "Privileged Identity Management": {
        "product": "entra",
        "full_name": "Microsoft Entra Privileged Identity Management (PIM)",
        "scope": "Just-in-time, time-bound, approval-gated privileged role activation; activation MFA; PIM for Entra ID / Azure roles and groups; privileged-access alerts and audit history",
        "url": "https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure",
    },
    "Entra ID Governance": {
        "product": "entra",
        "full_name": "Microsoft Entra ID Governance",
        "scope": "Access reviews / recertification, entitlement management (access packages, approvals, expiration), lifecycle workflows (joiner-mover-leaver automation), separation-of-duties via incompatible access packages",
        "url": "https://learn.microsoft.com/entra/id-governance/identity-governance-overview",
    },
}

# ===========================================================================
# Intune (product #3, added 2026-07-17).
# Naming, capability surfaces, licensing, and government-cloud availability
# verified on Microsoft Learn 2026-07-17 against the Intune docs (current base
# learn.microsoft.com/intune/*), the Intune licensing article, and the
# "Microsoft Intune for US Government GCC High and DoD service description".
# ===========================================================================
INTUNE_SOLUTIONS = {
    "Device Compliance": {
        "product": "intune",
        "full_name": "Microsoft Intune device compliance policies",
        "scope": "Per-platform device compliance rules (encryption required, minimum OS version, password/PIN, jailbreak/root detection, Defender or Mobile Threat Defense threat level), tenant-wide compliance policy settings, actions for noncompliance with grace periods, and compliance status reported to Microsoft Entra ID, which is the device signal Conditional Access consumes",
        "url": "https://learn.microsoft.com/intune/device-security/compliance/overview",
    },
    "Device Configuration & Baselines": {
        "product": "intune",
        "full_name": "Microsoft Intune device configuration (settings catalog, configuration profiles, security baselines)",
        "scope": "Settings catalog and configuration profiles across Windows/macOS/iOS/Android/Linux, Microsoft-recommended security baselines (Windows MDM, Defender for Endpoint, Edge, M365 Apps), device restrictions, Wi-Fi/VPN/certificate deployment, Windows update rings and update policies",
        "url": "https://learn.microsoft.com/intune/device-configuration/overview",
    },
    "Endpoint Security": {
        "product": "intune",
        "full_name": "Microsoft Intune endpoint security policies",
        "scope": "Focused security policy surfaces: antivirus (Defender settings management), disk encryption (BitLocker/FileVault/Personal Data Encryption), firewall, attack surface reduction, App Control for Business, account protection incl. Windows LAPS, EDR onboarding policy, Endpoint Privilege Management (separately licensed add-on)",
        "url": "https://learn.microsoft.com/intune/device-security/endpoint-security-policies",
    },
    "App Protection & Management": {
        "product": "intune",
        "full_name": "Microsoft Intune app management and app protection policies (MAM)",
        "scope": "App protection policies for iOS/iPadOS and Android with or without device enrollment (encrypt org data inside managed apps, restrict cut/copy/paste and save-to-personal, app PIN, selective wipe of org data), app configuration policies, managed app deployment",
        "url": "https://learn.microsoft.com/intune/app-management/protection/overview",
    },
    "Enrollment & Device Lifecycle": {
        "product": "intune",
        "full_name": "Microsoft Intune device enrollment and lifecycle management",
        "scope": "Enrollment across Windows (automatic enrollment, Windows Autopilot), Apple (Automated Device Enrollment), and Android Enterprise; enrollment restrictions by platform/ownership; device inventory; remote actions (wipe, retire, remote lock); device retirement/decommissioning",
        "url": "https://learn.microsoft.com/intune/device-enrollment/guide",
    },
}

# ===========================================================================
# Defender XDR (product #4, added 2026-07-17).
# Naming, capability surfaces, per-workload licensing, and government-cloud
# availability verified on Microsoft Learn 2026-07-17 against the Microsoft
# Defender service description, the MDO service description, the MDE/MDVM/MDI/
# MDCA product docs, and the Defender US Government pages.
# ONE product, four workload solutions — the same pattern as Entra's CA/PIM/
# ID Protection/Governance. Cross-workload XDR-platform rows (unified incidents,
# advanced hunting, attack disruption) are carried by the workload owning the
# dominant signal (usually Defender for Endpoint) with the others in also_involves.
# ===========================================================================
DEFENDER_SOLUTIONS = {
    "Defender for Endpoint": {
        "product": "defender-xdr",
        "full_name": "Microsoft Defender for Endpoint (MDE)",
        "scope": ("Endpoint protection across Windows/macOS/Linux/iOS/Android: next-generation antivirus, attack surface "
                  "reduction, device control, endpoint firewall, network/web protection (Plan 1); EDR, automated "
                  "investigation & remediation, Defender Vulnerability Management core, threat analytics, advanced hunting "
                  "(Plan 2). Also carries the Defender XDR cross-workload surface (unified incidents, correlation, "
                  "automatic attack disruption)"),
        "url": "https://learn.microsoft.com/defender-endpoint/microsoft-defender-endpoint",
    },
    "Defender for Office 365": {
        "product": "defender-xdr",
        "full_name": "Microsoft Defender for Office 365 (MDO)",
        "scope": ("Email and collaboration threat protection for Exchange Online, Teams, SharePoint, and OneDrive: Safe "
                  "Attachments, Safe Links, anti-phishing/impersonation protection, real-time detections (Plan 1); Threat "
                  "Explorer, automated investigation & response, attack simulation training, campaign views, and full "
                  "Defender XDR integration (Plan 2)"),
        "url": "https://learn.microsoft.com/defender-office-365/mdo-about",
    },
    "Defender for Identity": {
        "product": "defender-xdr",
        "full_name": "Microsoft Defender for Identity (MDI)",
        "scope": ("Identity threat detection for on-premises and hybrid Active Directory: sensors on domain controllers, "
                  "AD FS/AD CS, and Entra Connect servers detecting reconnaissance, credential theft (pass-the-hash, "
                  "DCSync), lateral movement, and domain-dominance techniques; identity posture assessments. Boundary: "
                  "cloud-identity sign-in/user risk is Microsoft Entra ID Protection, a seam, not an overlap"),
        "url": "https://learn.microsoft.com/defender-for-identity/what-is",
    },
    "Defender for Cloud Apps": {
        "product": "defender-xdr",
        "full_name": "Microsoft Defender for Cloud Apps (MDCA; formerly Microsoft Cloud App Security)",
        "scope": ("CASB / SaaS security: Cloud Discovery of shadow IT, app risk scoring and sanctioning, OAuth app "
                  "governance, SaaS activity/anomaly monitoring, SaaS security posture management, and Conditional Access "
                  "App Control access/session policies. Boundary: session controls are reverse-proxy/Edge-in-browser only; "
                  "native desktop and mobile clients bypass them unless access policies block native-client sign-in"),
        "url": "https://learn.microsoft.com/defender-cloud-apps/what-is-defender-for-cloud-apps",
    },
}

# ===========================================================================
# Sentinel (product #5, added 2026-07-18).
# Naming, portal state, data-tier/retention model, consumption pricing, free/
# benefit data sources, and government-cloud availability verified on Microsoft
# Learn 2026-07-18 against the Sentinel overview, the Defender-portal and
# move-to-defender pages, the billing article, manage-data-overview (tiers &
# retention), the data lake overview, the M365 E5 benefit offer page, the
# Sentinel feature-availability page, and the unified-SecOps gov-support page.
# ONE product, seven functional solutions (Sentinel has no workload sub-brands;
# the functional surfaces are the natural pivot to reason in).
# Discipline: Sentinel evidences/detects, it does not enforce (see PRODUCTS notes).
# ===========================================================================
SENTINEL_SOLUTIONS = {
    "Data Collection & Connectors": {
        "product": "sentinel",
        "full_name": "Microsoft Sentinel data collection (connectors, Content hub, data collection rules)",
        "scope": ("Centralized security-log collection: 350+ out-of-the-box connectors (Microsoft 365 audit, Entra ID, "
                  "Defender XDR, Azure Activity, Defender for Cloud) plus third-party/on-premises ingestion via CEF/Syslog, "
                  "the Codeless Connector Platform, and Logstash; Content hub solutions; data collection rules; "
                  "SentinelHealth telemetry. Boundary: Sentinel centralizes, it does not create the source audit trail"),
        "url": "https://learn.microsoft.com/azure/sentinel/connect-data-sources",
    },
    "Analytics Rules & Detections": {
        "product": "sentinel",
        "full_name": "Microsoft Sentinel analytics (scheduled/NRT rules, Fusion correlation, ML anomalies)",
        "scope": ("KQL scheduled and near-real-time analytics rules, Microsoft security rules, Fusion multistage "
                  "correlation, ML anomaly detections, MITRE ATT&CK mapping, and event-to-incident promotion across every "
                  "connected source. Boundary: coverage follows the connector estate, and Defender XDR remains the native "
                  "detection engine inside Microsoft workloads"),
        "url": "https://learn.microsoft.com/azure/sentinel/threat-detection",
    },
    "Incident Management & Investigation": {
        "product": "sentinel",
        "full_name": "Microsoft Sentinel incident management and investigation",
        "scope": ("Unified incident queue in the Defender portal (bi-directional Defender XDR sync), incident tasks, case "
                  "management, entity pages and investigation timeline, incident advanced search, and SOC incident audit "
                  "metrics: the durable, auditable record of what was detected, investigated, decided, and by whom"),
        "url": "https://learn.microsoft.com/azure/sentinel/investigate-cases",
    },
    "Automation & Playbooks (SOAR)": {
        "product": "sentinel",
        "full_name": "Microsoft Sentinel automation (automation rules + Azure Logic Apps playbooks)",
        "scope": ("Automation rules for triage at scale (assignment, tagging, severity, suppression, closure) and Logic Apps "
                  "playbooks for response (enrich with TI, notify/ticket, invoke containment). Boundary: SOAR orchestrates; "
                  "remediation executes in the integrated enforcement products (Defender device isolation, Entra account "
                  "disable, firewall block), not Sentinel itself"),
        "url": "https://learn.microsoft.com/azure/sentinel/automate-incident-handling-with-automation-rules",
    },
    "UEBA & Hunting": {
        "product": "sentinel",
        "full_name": "Microsoft Sentinel User and Entity Behavior Analytics and threat hunting",
        "scope": ("UEBA behavioral baselining and anomaly scoring over Entra ID, on-premises AD (via MDI), and connected "
                  "activity (BehaviorAnalytics/IdentityInfo tables); proactive hunting queries, hunts, bookmarks, "
                  "livestream; search jobs over long-term data for historical hunts"),
        "url": "https://learn.microsoft.com/azure/sentinel/identify-threats-with-entity-behavior-analytics",
    },
    "Threat Intelligence": {
        "product": "sentinel",
        "full_name": "Microsoft Sentinel threat intelligence management",
        "scope": ("Ingestion, curation, and management of threat indicators via STIX/TAXII connectors, the upload API, TI "
                  "platform connectors, and the free Microsoft Defender Threat Intelligence feed; TI matching analytics "
                  "against ingested logs; threat intelligence workbook and research experience"),
        "url": "https://learn.microsoft.com/azure/sentinel/understand-threat-intelligence",
    },
    "Log Retention & Data Lake": {
        "product": "sentinel",
        "full_name": "Microsoft Sentinel data tiers and retention (analytics tier + data lake)",
        "scope": ("Per-table retention: analytics-tier retention (90 days included, extendable to 2 years) mirrored into "
                  "the Microsoft Sentinel data lake for total retention up to 12 years, a lake-only tier for high-volume "
                  "sources, and search/restore jobs for archived data: the mechanism behind 12-month (PCI) and multi-year "
                  "(CMMC/800-53) retention mandates. Boundary: customer-managed keys unsupported for data-lake data"),
        "url": "https://learn.microsoft.com/azure/sentinel/manage-data-overview",
    },
}

# ===========================================================================
# Defender for Cloud (product #6, added 2026-07-18 — the FINAL product; the roadmap is complete).
# Naming, plan structure, free-vs-paid CSPM boundary, regulatory-compliance-dashboard gate,
# CIEM state, Servers P1/P2 content, consumption meters, and Azure Government availability all
# verified live 2026-07-18 against the Defender for Cloud introduction, CSPM concept + enable
# pages, the CIEM page (permissions-management), the regulatory-compliance standards/assign
# pages, the Defender for Servers overview + plan-selection + data-ingestion-benefit pages,
# the support matrix, and the Azure pricing page.
# ONE product, five functional solutions (consolidation decisions: multicloud connectors fold
# into Foundational CSPM's scope — connectors are free and never the control story on their own;
# the eight per-resource CWPP plans other than Servers consolidate into one Workload Protection
# solution — Servers stands alone for its MDE licensing seam and P2 feature band; Defender for
# DNS is legacy-only since Aug 2023 — DNS alerts ride in Servers P2 for new subscriptions and
# no solution is registered; Defender Experts for Servers is a separately-sold managed service,
# out of scope).
# Discipline: Defender for Cloud assesses/detects, it does not remediate (see PRODUCTS notes).
# ===========================================================================
MDC_SOLUTIONS = {
    "Foundational CSPM": {
        "product": "defender-cloud",
        "full_name": "Microsoft Defender for Cloud Foundational CSPM (free tier)",
        "scope": ("The free posture layer on every onboarded subscription: secure score, security recommendations against "
                  "the Microsoft cloud security benchmark (MCSB, the default standard), asset inventory across "
                  "Azure/AWS/GCP, agentless multicloud connectors, and centralized security policy. Boundary: "
                  "recommendations are advisory, not remediation"),
        "url": "https://learn.microsoft.com/azure/defender-for-cloud/concept-cloud-security-posture-management",
    },
    "Defender CSPM": {
        "product": "defender-cloud",
        "full_name": "Microsoft Defender CSPM (paid posture plan)",
        "scope": "The paid posture plan that adds attack-path analysis and risk prioritization, agentless scanning, data-aware posture, and cloud entitlement management on top of the free tier.",
        "scope_detail": ("Advanced posture over the cloud security graph: attack path analysis and risk prioritization, cloud "
                  "security explorer, agentless vulnerability and secrets scanning, agentless container vulnerability "
                  "assessment, data-aware security posture (sensitive data discovery via the Purview classification "
                  "engine), CIEM (continuing after Entra Permissions Management's 2025 retirement), governance rules, and "
                  "AI security posture management. Boundary: identifies and prioritizes risk; remediation executes in the "
                  "resource platform"),
        "url": "https://learn.microsoft.com/azure/defender-for-cloud/tutorial-enable-cspm-plan",
    },
    "Regulatory Compliance Dashboard": {
        "product": "defender-cloud",
        "full_name": "Microsoft Defender for Cloud regulatory compliance dashboard",
        "scope": "Continuous assessment of your onboarded cloud resources against built-in and custom standards, with per-control pass/fail and downloadable reports.",
        "scope_detail": ("Continuous assessment of onboarded cloud resources against built-in standards (MCSB by default; "
                  "assignable standards include ISO/IEC 27001:2022, SOC 2/SOC 2023, PCI DSS v4.0.1, NIST SP 800-53 "
                  "R5.1.1, NIST 800-171, NIST CSF 2.0, CMMC L2 v2.0, HIPAA/HITRUST, GDPR, FedRAMP, and CIS benchmarks; "
                  "custom standards supported) with per-control pass/fail and downloadable reports. Scope boundary: it "
                  "covers onboarded cloud resources against a standard's technically-assessable subset, not M365, "
                  "on-premises, or procedural controls, and not an attestation (Purview Compliance Manager assesses the "
                  "M365 estate: a seam, not an overlap)"),
        "url": "https://learn.microsoft.com/azure/defender-for-cloud/regulatory-compliance-dashboard",
    },
    "Defender for Servers": {
        "product": "defender-cloud",
        "full_name": "Microsoft Defender for Servers (Plan 1 / Plan 2)",
        "scope": "Threat protection for Windows and Linux servers across Azure, AWS, GCP, and on-premises via Azure Arc, split into two plans with progressively deeper coverage.",
        "scope_detail": ("Server workload protection for Windows/Linux across Azure, AWS, GCP, and on-premises via Azure Arc. "
                  "Plan 1 centers on the integrated Defender for Endpoint for Servers (EDR; the MDE license rides with "
                  "the plan, a seam with Defender XDR). Plan 2 adds agentless machine scanning, premium Defender "
                  "Vulnerability Management, file integrity monitoring, just-in-time VM access, OS-baseline and "
                  "system-updates assessment, DNS-layer alerts, and a 500 MB/day ingestion allowance on the associated "
                  "Log Analytics/Sentinel workspace"),
        "url": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-servers-overview",
    },
    "Workload Protection Plans": {
        "product": "defender-cloud",
        "full_name": ("Microsoft Defender for Cloud workload protection plans (Storage, Databases, Containers, "
                      "App Service, Key Vault, Resource Manager, APIs, AI Services)"),
        "scope": "Per-resource threat detection and hardening for storage, databases, containers, App Service, Key Vault, Resource Manager, APIs, and AI services.",
        "scope_detail": ("Per-resource threat detection and hardening plans: Defender for Storage (activity monitoring, "
                  "on-upload malware scanning, sensitive data threat detection), Databases (SQL injection, brute-force, "
                  "anomaly detection, SQL vulnerability assessment across Azure SQL, SQL-on-machines, OSS databases, "
                  "Cosmos DB), Containers (Kubernetes hardening, image vulnerability assessment, runtime protection), "
                  "App Service, Key Vault and Resource Manager (control-plane anomaly detection), APIs, and AI Services. "
                  "Alerts stream into the Defender portal and Sentinel; remediation executes in the resource platform"),
        "url": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction",
    },
}

# Tag existing (Purview) solutions, then merge Entra + Intune + Defender + Sentinel + Defender-for-Cloud
# solutions into the shared registry.
for _v in SOLUTIONS.values():
    _v.setdefault("product", "purview")
SOLUTIONS.update(ENTRA_SOLUTIONS)
SOLUTIONS.update(INTUNE_SOLUTIONS)
SOLUTIONS.update(DEFENDER_SOLUTIONS)
SOLUTIONS.update(SENTINEL_SOLUTIONS)
SOLUTIONS.update(MDC_SOLUTIONS)

# Derive each product's ordered solution list from the shared registry (product isolation).
PRODUCTS["purview"]["solutions"] = [k for k, v in SOLUTIONS.items() if v.get("product") == "purview"]
PRODUCTS["entra"]["solutions"] = [k for k, v in SOLUTIONS.items() if v.get("product") == "entra"]
PRODUCTS["intune"]["solutions"] = [k for k, v in SOLUTIONS.items() if v.get("product") == "intune"]
PRODUCTS["defender-xdr"]["solutions"] = [k for k, v in SOLUTIONS.items() if v.get("product") == "defender-xdr"]
PRODUCTS["sentinel"]["solutions"] = [k for k, v in SOLUTIONS.items() if v.get("product") == "sentinel"]
PRODUCTS["defender-cloud"]["solutions"] = [k for k, v in SOLUTIONS.items() if v.get("product") == "defender-cloud"]

# Entra licensing strings — from the Entra licensing service description (per-capability tiers).
ENTRA_LIC = {
    "ca": "Microsoft Entra Conditional Access: Microsoft Entra ID P1 (included in Microsoft 365 E3/E5/E7, Microsoft 365 F1/F3, Enterprise Mobility + Security E3, and Business Premium). Risk-based conditions additionally require Entra ID P2.",
    "mfa": "Multifactor authentication & authentication methods: Microsoft Entra ID Free (basic) and P1; authentication strengths and full policy control require Entra ID P1.",
    "id_protection": "Microsoft Entra ID Protection (risk-based policies, risky users/sign-ins): Microsoft Entra ID P2 (included in Microsoft 365 E5/E7, Microsoft Defender Suite (formerly Microsoft 365 E5 Security), and Enterprise Mobility + Security E5) or Microsoft Entra Suite.",
    "pim": "Privileged Identity Management: Microsoft Entra ID P2 or the Microsoft Entra ID Governance SKU.",
    "gov_core": "Access reviews & entitlement management (baseline capabilities previously GA in Entra ID P2): Microsoft Entra ID P2; advanced governance requires the Microsoft Entra ID Governance SKU or Microsoft Entra Suite.",
    "gov_lcw": "Lifecycle Workflows: Microsoft Entra ID Governance SKU or Microsoft Entra Suite (not included in standalone Entra ID P2).",
    "free": "Included with Microsoft Entra ID Free (all Microsoft cloud subscriptions).",
}

ENTRA_URLS = {
    "entra_id": "https://learn.microsoft.com/entra/fundamentals/what-is-entra",
    "ca": "https://learn.microsoft.com/entra/identity/conditional-access/overview",
    "mfa": "https://learn.microsoft.com/entra/identity/authentication/concept-mfa-howitworks",
    "auth_methods": "https://learn.microsoft.com/entra/identity/authentication/overview-authentication",
    "auth_strengths": "https://learn.microsoft.com/entra/identity/authentication/concept-authentication-strengths",
    "id_protection": "https://learn.microsoft.com/entra/id-protection/overview-identity-protection",
    "pim": "https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure",
    "id_gov": "https://learn.microsoft.com/entra/id-governance/identity-governance-overview",
    "access_reviews": "https://learn.microsoft.com/entra/id-governance/access-reviews-overview",
    "entitlement": "https://learn.microsoft.com/entra/id-governance/entitlement-management-overview",
    "lcw": "https://learn.microsoft.com/entra/id-governance/what-are-lifecycle-workflows",
    "sod": "https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-incompatible",
    "licensing": "https://learn.microsoft.com/entra/fundamentals/licensing",
    "gov_licensing": "https://learn.microsoft.com/entra/id-governance/licensing-fundamentals",
    "gov_feature": "https://learn.microsoft.com/entra/identity/authentication/feature-availability",
    "sspr": "https://learn.microsoft.com/entra/identity/authentication/concept-sspr-howitworks",
    "rbac": "https://learn.microsoft.com/entra/identity/role-based-access-control/custom-overview",
}

# Entra government-cloud notes (verified against the Entra feature-availability page, 2026-07-17).
ENTRA_GOV = {
    "ca": "Conditional Access: available in Azure Government (GCC, GCC High, DoD).",
    "mfa": "MFA and authentication methods (incl. passwordless/FIDO2, certificate-based auth): available in Azure Government (GCC/GCC High/DoD).",
    "id_protection": "ID Protection risk detections, risky-account investigation, and SIEM connectivity: available in Azure Government; Microsoft Entra threat-intelligence detection is not available in gov clouds.",
    "pim": "Privileged Identity Management: available in Azure Government (GCC/GCC High/DoD).",
    "gov": "Access reviews, entitlement management, PIM, and Lifecycle Workflows (Microsoft Entra ID Governance): available in GCC, GCC High, and DoD.",
}

# Intune licensing strings — from the Microsoft Intune licensing article + advanced-capabilities
# article (July 2026 licensing model), NOT the Purview or Entra service descriptions.
INTUNE_LIC = {
    "p1": "Microsoft Intune Plan 1 (the base Intune service; included in Microsoft 365 bundles such as E3/E5/E7 and Enterprise Mobility + Security E3/E5, also available standalone)",
    "p1_ca": "Microsoft Intune Plan 1; enforcing the compliance signal through Conditional Access additionally requires Microsoft Entra ID P1",
    "epm": "Endpoint Privilege Management: included in Microsoft 365 E5 and E7 since July 2026, when Intune Suite capabilities were distributed across Microsoft 365 tiers; on any other plan it remains a separate Intune add-on license or the Microsoft Intune Suite, in addition to Intune Plan 1",
}

INTUNE_URLS = {
    "what_is": "https://learn.microsoft.com/intune/fundamentals/what-is-intune",
    "compliance": "https://learn.microsoft.com/intune/device-security/compliance/overview",
    "compliance_actions": "https://learn.microsoft.com/intune/device-security/compliance/configure-noncompliance-actions",
    "ca_integration": "https://learn.microsoft.com/intune/device-security/conditional-access-integration/overview",
    "config": "https://learn.microsoft.com/intune/device-configuration/overview",
    "settings_catalog": "https://learn.microsoft.com/intune/device-configuration/settings-catalog",
    "baselines": "https://learn.microsoft.com/intune/device-security/security-baselines/overview",
    "endpoint_security": "https://learn.microsoft.com/intune/device-security/endpoint-security-policies",
    "es_policy_types": "https://learn.microsoft.com/intune/device-configuration/endpoint-security/manage-policies",
    "disk_encryption": "https://learn.microsoft.com/intune/device-configuration/endpoint-security/disk-encryption",
    "bitlocker": "https://learn.microsoft.com/intune/device-configuration/endpoint-security/encrypt-bitlocker-windows",
    "filevault": "https://learn.microsoft.com/intune/device-configuration/endpoint-security/encrypt-filevault-macos",
    "monitor_encryption": "https://learn.microsoft.com/intune/device-management/monitor-encryption",
    "app_protection": "https://learn.microsoft.com/intune/app-management/protection/overview",
    "enrollment": "https://learn.microsoft.com/intune/device-enrollment/guide",
    "enrollment_windows": "https://learn.microsoft.com/intune/device-enrollment/windows/guide",
    "enrollment_restrictions": "https://learn.microsoft.com/intune/device-enrollment/restrictions",
    "epm": "https://learn.microsoft.com/intune/epm/overview",
    "antivirus": "https://learn.microsoft.com/intune/device-configuration/endpoint-security/antivirus",
    "asr": "https://learn.microsoft.com/intune/device-configuration/endpoint-security/attack-surface-reduction",
    "app_control": "https://learn.microsoft.com/intune/device-configuration/endpoint-security/manage-app-control",
    "device_actions": "https://learn.microsoft.com/intune/device-management/actions/",
    "retire": "https://learn.microsoft.com/intune/device-management/actions/retire",
    "wipe": "https://learn.microsoft.com/intune/device-management/actions/wipe",
    "wipe_corporate_data": "https://learn.microsoft.com/intune/app-management/protection/wipe-corporate-data",
    "app_dp_framework": "https://learn.microsoft.com/intune/app-management/protection/data-protection-framework",
    "update_rings": "https://learn.microsoft.com/intune/device-updates/windows/manage-update-rings",
    "windows_updates": "https://learn.microsoft.com/intune/device-updates/windows/",
    "manage_devices": "https://learn.microsoft.com/intune/device-management/inventory-and-status/device-details",
    "autopatch": "https://learn.microsoft.com/windows/deployment/windows-autopatch/overview/windows-autopatch-overview",
    "licensing": "https://learn.microsoft.com/intune/fundamentals/licensing",
    "gov": "https://learn.microsoft.com/intune/fundamentals/government-service",
    "advanced": "https://learn.microsoft.com/intune/fundamentals/advanced-capabilities",
}

# Intune government-cloud notes (verified against the Intune GCC High/DoD service description, 2026-07-17).
# Note: Intune GCC is the commercial Intune instance; "gov cloud" caveats below are GCC High/DoD.
INTUNE_GOV = {
    "core": "Core Intune MDM (compliance policies, configuration profiles, app policies) is available in GCC High/DoD; Intune for GCC runs on the commercial Intune instance.",
    "esp": "Endpoint security policies, incl. Defender for Endpoint security settings management, are supported in GCC, GCC High, and DoD.",
    "autopilot": "Windows Autopilot is not available in GCC High/DoD; Windows Autopilot device preparation is partially available (user-driven today; self-deploying and pre-provisioning modes still planned).",
    "updates": "Windows Autopatch and Windows feature/quality/expedite/driver update policies are not yet available in GCC High/DoD (planned).",
    "dha": "Windows Device Health Attestation is not yet available in GCC High/DoD, so compliance evaluations that rely on health attestation are limited there.",
    "suite": "In GCC High/DoD: Endpoint Privilege Management, Advanced Analytics, Enterprise App Management, Tunnel for MAM, firmware-over-the-air updates, and specialty devices management are supported; Cloud PKI (GCC High) and Remote Help are planned/not available.",
}

# Defender licensing strings — from the Microsoft Defender service description (per-workload sections),
# the MDO service description, and the MDE/MDVM/MDI product docs. NOT the Purview/Entra/Intune sources.
# Highest-risk axis in this product: MDE Plan 1 vs Plan 2 (EDR/AIR/vuln-mgmt/threat-analytics are P2-only)
# and MDO Plan 1 vs Plan 2 (Explorer/AIR/attack-sim/XDR-integration are P2-only).
DEFENDER_LIC = {
    "mde_p1": ("Microsoft Defender for Endpoint Plan 1: standalone or included in Microsoft 365 E3/A3/G3. "
               "P1 covers next-gen antivirus, attack surface reduction, device control, endpoint firewall, network "
               "protection, and manual response actions. EDR, automated investigation & remediation, vulnerability "
               "management, and threat analytics require Plan 2."),
    "mde_p2": ("Microsoft Defender for Endpoint Plan 2: standalone or included in Microsoft 365 E5/A5/G5, "
               "Windows 11/10 Enterprise E5/A5, Microsoft Defender Suite (formerly Microsoft 365 E5 Security)/EDU/GOV/FLW, "
               "or Microsoft Defender + Purview Suite FLW."),
    "mdvm": ("Defender Vulnerability Management core capabilities: included with Microsoft Defender for Endpoint Plan 2 "
             "(Microsoft 365 E5/A5/G5, Microsoft Defender Suite (formerly Microsoft 365 E5 Security)/EDU/GOV/FLW, or "
             "standalone P2). Premium capabilities (security baselines assessment, block vulnerable applications, "
             "browser-extension/certificate/hardware-firmware assessment) require the Defender Vulnerability Management "
             "add-on, available to Defender for Endpoint Plan 2, Microsoft 365 E5/A5/G5, Microsoft Defender Suite/EDU/GOV/FLW, "
             "Microsoft Defender + Purview Suite FLW, and Windows 11/10 Enterprise E5/A5/G5 customers; an MDVM standalone "
             "exists for non-P2 customers."),
    "mdo_p1": ("Microsoft Defender for Office 365 Plan 1: standalone, Microsoft 365 Business Premium, Microsoft 365 E5/A5/G5, "
               "Office 365 E5/A5/G5, Microsoft Defender Suite (formerly Microsoft 365 E5 Security)/EDU/GOV/FLW, or Microsoft "
               "Defender + Purview Suite FLW. Effective July 1, 2026 it is also included in Microsoft 365 E3/G3 and Office 365 "
               "E3/G3; that rollout began June 2026 and Microsoft expects it to complete during 2026."),
    "mdo_p2": ("Microsoft Defender for Office 365 Plan 2: standalone or included in Microsoft 365 E5/A5/G5, "
               "Office 365 E5/A5/G5, Microsoft Defender Suite (formerly Microsoft 365 E5 Security)/EDU/GOV/FLW, or Microsoft "
               "Defender + Purview Suite FLW. Threat Explorer, automated investigation & response, attack simulation training, "
               "campaign views, and Defender XDR integration are Plan 2-only."),
    "mdi": ("Microsoft Defender for Identity: standalone or included in Enterprise Mobility + Security E5/A5, "
            "Microsoft 365 E5/A5/G5, Microsoft Defender Suite (formerly Microsoft 365 E5 Security)/EDU/GOV/FLW, Microsoft "
            "Defender + Purview Suite FLW, or Microsoft Defender for Identity for Users."),
    "mdca": ("Microsoft Defender for Cloud Apps: standalone or included in Enterprise Mobility + Security E5, "
             "Microsoft 365 E5/A5/G5, Microsoft Defender Suite (formerly Microsoft 365 E5 Security)/EDU/GOV/FLW, "
             "Microsoft Purview Suite/EDU/GOV/FLW, Microsoft Defender + Purview Suite FLW, or Microsoft 365 E5/F5/G5 "
             "Information Protection and Governance. Conditional Access App Control additionally requires Microsoft "
             "Entra ID P1 licensing."),
    "xdr": ("Microsoft Defender XDR has no separate license; the unified portal and correlation come with any "
            "qualifying workload license (Microsoft 365 E5/A5; Microsoft 365 E3 with the Microsoft Defender Suite or "
            "Enterprise Mobility + Security E5 add-on; Microsoft 365 A3 with the A5 Security add-on; Windows 11/10 "
            "Enterprise E5/A5; Enterprise Mobility + Security E5/A5; Office 365 E5/A5; Microsoft 365 Business Premium; "
            "or standalone Defender workload licenses). Automatic attack disruption and threat analytics require "
            "Defender for Endpoint Plan 2."),
}

DEFENDER_URLS = {
    "xdr": "https://learn.microsoft.com/defender-xdr/microsoft-365-defender",
    "xdr_prereq": "https://learn.microsoft.com/defender-xdr/prerequisites",
    "incidents": "https://learn.microsoft.com/defender-xdr/investigate-incidents",
    "hunting": "https://learn.microsoft.com/defender-xdr/advanced-hunting-overview",
    "custom_detections": "https://learn.microsoft.com/defender-xdr/custom-detections-overview",
    "attack_disruption": "https://learn.microsoft.com/defender-xdr/automatic-attack-disruption",
    "air": "https://learn.microsoft.com/defender-xdr/m365d-autoir",
    "threat_analytics": "https://learn.microsoft.com/defender-xdr/threat-analytics",
    "mde": "https://learn.microsoft.com/defender-endpoint/microsoft-defender-endpoint",
    "mde_p1": "https://learn.microsoft.com/defender-endpoint/defender-endpoint-plan-1",
    "ngav": "https://learn.microsoft.com/defender-endpoint/microsoft-defender-antivirus-windows",
    "edr": "https://learn.microsoft.com/defender-endpoint/overview-endpoint-detection-response",
    "asr": "https://learn.microsoft.com/defender-endpoint/attack-surface-reduction-overview",
    "device_control": "https://learn.microsoft.com/defender-endpoint/device-control-overview",
    "network_protection": "https://learn.microsoft.com/defender-endpoint/network-protection",
    "web_content_filtering": "https://learn.microsoft.com/defender-endpoint/web-content-filtering",
    "mdvm": "https://learn.microsoft.com/defender-vulnerability-management/defender-vulnerability-management",
    "mdvm_plans": "https://learn.microsoft.com/defender-vulnerability-management/defender-vulnerability-management-capabilities",
    "mdo": "https://learn.microsoft.com/defender-office-365/mdo-about",
    "safe_attachments": "https://learn.microsoft.com/defender-office-365/safe-attachments-about",
    "safe_links": "https://learn.microsoft.com/defender-office-365/safe-links-about",
    "anti_phishing": "https://learn.microsoft.com/defender-office-365/anti-phishing-protection-about",
    "attack_sim": "https://learn.microsoft.com/defender-office-365/attack-simulation-training-get-started",
    "threat_explorer": "https://learn.microsoft.com/defender-office-365/threat-explorer-real-time-detections-about",
    "mdi": "https://learn.microsoft.com/defender-for-identity/what-is",
    "mdca": "https://learn.microsoft.com/defender-cloud-apps/what-is-defender-for-cloud-apps",
    "caac": "https://learn.microsoft.com/defender-cloud-apps/proxy-intro-aad",
    "cloud_discovery": "https://learn.microsoft.com/defender-cloud-apps/set-up-cloud-discovery",
    "app_governance": "https://learn.microsoft.com/defender-cloud-apps/app-governance-manage-app-governance",
    "sd": "https://learn.microsoft.com/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-defender-service-description",
    "mdo_sd": "https://learn.microsoft.com/office365/servicedescriptions/office-365-advanced-threat-protection-service-description",
    "gov": "https://learn.microsoft.com/defender-xdr/usgov",
    "mde_gov": "https://learn.microsoft.com/defender-endpoint/gov",
    "mdo_gov": "https://learn.microsoft.com/defender-office-365/mdo-gov",
    "mdi_gov": "https://learn.microsoft.com/defender-for-identity/us-govt-gcc-high",
}

# Defender government-cloud notes (verified against the Defender XDR US Government page and the
# per-workload US Government pages, 2026-07-17).
DEFENDER_GOV = {
    "xdr": ("Defender XDR (unified portal, incidents, advanced hunting, attack disruption): available in GCC, GCC High, "
            "and DoD; Microsoft Threat Experts is not available in gov clouds; preview features are commercial-only."),
    "mde": ("Defender for Endpoint: available in GCC, GCC High, and DoD (G3 includes Plan 1; G5/G5 Security include "
            "Plan 2); some capabilities lag commercial, so verify per feature on the MDE US Government page."),
    "mdvm": ("Defender Vulnerability Management core (with MDE Plan 2): available in GCC, GCC High, and DoD; the MDVM "
             "add-on trial is not available in GCC High/DoD, so confirm add-on purchase options for gov tenants."),
    "mdo": ("Defender for Office 365: available in GCC, GCC High, and DoD (Plan 2 via G5, E5 for GCC High, G5 for DoD, "
            "Defender Suite, or standalone licenses)."),
    "mdi": ("Defender for Identity: available in GCC, GCC High, and DoD (dedicated gov offerings; sensor endpoints on "
            ".azure.us for GCC High/DoD)."),
    "mdca": ("Defender for Cloud Apps: available in GCC, GCC High, and DoD as dedicated gov offerings (commercial-tenant "
             "MDCA must transition to the GCC version for gov eligibility)."),
}

# Sentinel licensing strings — CONSUMPTION model, from the Sentinel billing article, the manage-data-overview
# tiers/retention article, and the Microsoft 365 E5 benefit offer page (azure.microsoft.com/offers/
# sentinel-microsoft-365-offer). NOT per-user, NOT from any service description. Every Sentinel row sets
# licensing_model="consumption". Highest-risk axes: free-vs-paid data types (alerts free, raw logs paid)
# and the retention meters (analytics-tier vs data-lake) behind multi-year retention mandates.
SENTINEL_LIC = {
    "ingest": ("Microsoft Sentinel is consumption-priced on data ingestion (no per-user license): pay-as-you-go per GB "
               "into the analytics tier, or commitment tiers from 100 GB/day at discounted effective rates; simplified "
               "pricing combines Log Analytics + Sentinel meters. A 50 GB/day commitment tier launched Oct 1, 2025 and "
               "remains in public preview: its promotional pricing was extended through Dec 31, 2026, and customers who "
               "sign up in that window lock in the discounted rate through Mar 31, 2027."),
    "retention": ("Consumption-priced retention: analytics-tier retention beyond the included 90 days is billed per GB "
                  "(extendable to 2 years); Microsoft Sentinel data lake total retention up to 12 years is billed per "
                  "compressed GB/month (6:1 compression assumption) plus per-GB query/processing meters when archived "
                  "data is scanned. These are the meters behind 12-month (PCI DSS) and multi-year (CMMC/800-53) retention mandates."),
    "free_benefit": ("Free data sources: Office 365 audit activity (SharePoint/Exchange/Teams), Azure Activity, and all "
                     "Microsoft Defender security alerts/incidents ingest at no charge. Microsoft 365 E7/E5/A5/F5/G5 and "
                     "their Security counterparts additionally get a data grant of up to 5 MB/user/day covering Entra ID "
                     "sign-in/audit logs, Defender for Cloud Apps shadow-IT discovery, Purview Information Protection "
                     "logs, and Defender XDR advanced-hunting tables; the grant requires an Enterprise, Enterprise "
                     "Subscription, or CSP agreement, and raw Microsoft logs beyond it are paid ingestion."),
    "soar": ("Microsoft Sentinel automation rules are included with the workspace (consumption-priced service); Logic "
             "Apps playbooks are billed separately under Azure Logic Apps consumption meters."),
    "included": ("Included with Microsoft Sentinel on the workspace (no separate license); cost follows the "
                 "consumption-priced data volume the capability operates over."),
}

SENTINEL_URLS = {
    "overview": "https://learn.microsoft.com/azure/sentinel/overview",
    "defender_portal": "https://learn.microsoft.com/azure/sentinel/microsoft-sentinel-defender-portal",
    "billing": "https://learn.microsoft.com/azure/sentinel/billing",
    "offer": "https://azure.microsoft.com/offers/sentinel-microsoft-365-offer/",
    "tiers": "https://learn.microsoft.com/azure/sentinel/manage-data-overview",
    "table_mgmt": "https://learn.microsoft.com/azure/sentinel/manage-table-tiers-retention",
    "datalake": "https://learn.microsoft.com/azure/sentinel/datalake/sentinel-lake-overview",
    "connect": "https://learn.microsoft.com/azure/sentinel/connect-data-sources",
    "connectors_ref": "https://learn.microsoft.com/azure/sentinel/data-connectors-reference",
    "cef_syslog": "https://learn.microsoft.com/azure/sentinel/connect-cef-syslog-ama",
    "xdr_connector": "https://learn.microsoft.com/azure/sentinel/connect-microsoft-365-defender",
    "o365_connector": "https://learn.microsoft.com/azure/sentinel/connect-services-api-based",
    "analytics": "https://learn.microsoft.com/azure/sentinel/threat-detection",
    "nrt": "https://learn.microsoft.com/azure/sentinel/near-real-time-rules",
    "fusion": "https://learn.microsoft.com/azure/sentinel/fusion",
    "anomalies": "https://learn.microsoft.com/azure/sentinel/soc-ml-anomalies",
    "incidents": "https://learn.microsoft.com/azure/sentinel/investigate-cases",
    "incident_tasks": "https://learn.microsoft.com/azure/sentinel/incident-tasks",
    "soc_metrics": "https://learn.microsoft.com/azure/sentinel/manage-soc-with-incident-metrics",
    "automation_rules": "https://learn.microsoft.com/azure/sentinel/automate-incident-handling-with-automation-rules",
    "playbooks": "https://learn.microsoft.com/azure/sentinel/automation/automate-responses-with-playbooks",
    "ueba": "https://learn.microsoft.com/azure/sentinel/identify-threats-with-entity-behavior-analytics",
    "hunting": "https://learn.microsoft.com/azure/sentinel/hunting",
    "search": "https://learn.microsoft.com/azure/sentinel/search-jobs",
    "ti": "https://learn.microsoft.com/azure/sentinel/understand-threat-intelligence",
    "ti_matching": "https://learn.microsoft.com/azure/sentinel/use-matching-analytics-to-detect-threats",
    "health": "https://learn.microsoft.com/azure/sentinel/health-audit",
    "workbooks": "https://learn.microsoft.com/azure/sentinel/monitor-your-data",
    "feature_avail": "https://learn.microsoft.com/azure/sentinel/feature-availability",
    "gov": "https://learn.microsoft.com/unified-secops/gov-support",
    "cloud_support": "https://learn.microsoft.com/azure/security/fundamentals/feature-availability",
}

# Sentinel government-cloud notes (verified 2026-07-18 against the unified-SecOps gov-support page, the
# Sentinel feature-availability page, and the cloud feature-availability fundamentals page).
SENTINEL_GOV = {
    "portal": ("Sentinel in the Defender portal: all generally-available unified-SecOps features are supported in GCC, "
               "GCC High, and DoD (portal URLs security.microsoft.us / security.apps.mil); preview features are "
               "commercial-cloud only; in GCC, advanced-hunting queries spanning both Sentinel and Defender XDR tables "
               "are not supported."),
    "azgov": ("Azure Government feature gaps: summary rules, SOC optimization, SIEM migration, repositories, MDTI "
              "matching analytics, URL detonation, and TI GeoLocation/WhoIs enrichment are not available; scheduled/NRT/"
              "Fusion analytics, automation rules, playbooks, watchlists, and core UEBA are GA (peer/blast-radius "
              "enrichments commercial-only). The M365 E5/G5 Sentinel data-grant benefit includes USGOV_GCCHIGH and "
              "USGOV_DOD SKUs."),
    "dod": ("Office 365 DoD pairing: the Microsoft Defender XDR connector is listed as not available for DoD tenants "
            "(alert-level data types via other Defender connectors vary), so verify raw XDR-table ingestion per tenant "
            "before relying on it in DoD."),
}

# Defender for Cloud licensing strings — CONSUMPTION model (the Sentinel pattern: meters, not SKUs),
# from the Azure pricing page (azure.microsoft.com/pricing/details/defender-for-cloud/), the CSPM
# concept/enable pages, the assign-regulatory-compliance-standards prerequisites, the Defender for
# Servers overview/plan-selection pages, and the data-ingestion-benefit page — all fetched live
# 2026-07-18. NOT per-user, NOT from any service description. Every Defender for Cloud row sets
# licensing_model="consumption". Highest-risk axes: the free-Foundational vs paid-Defender-CSPM
# feature boundary, the regulatory-compliance-dashboard paid-plan gate (any plan EXCEPT Servers P1
# and APIs P1), and the Servers P1/P2 split (MDE license rides with BOTH plans; premium MDVM, FIM,
# JIT, agentless scanning, and the 500 MB/day ingestion benefit are P2).
MDC_LIC = {
    "foundational": ("Foundational CSPM is free on every subscription/account onboarded to Defender for Cloud (secure "
                     "score, MCSB security recommendations, asset inventory, multicloud connectors): no per-user "
                     "license and no charge. The paid plans below are consumption-priced per protected resource."),
    "cspm": ("Defender CSPM: consumption-priced per billable resource per month. It protects all multicloud workloads "
             "but bills only on servers, storage accounts, databases (OSS/SQL incl. servers-on-machines), and "
             "serverless resources (conversion ratios apply). 30-day free trial on first enablement; a 1-year "
             "pre-purchase plan (Commit Units) discounts up to 22%."),
    "servers_p1": ("Defender for Servers Plan 1: consumption-priced per protected server per hour, billed monthly. "
                   "Plan 1 centers on the integrated Microsoft Defender for Endpoint for Servers license (EDR); "
                   "customers already licensed for MDE for Servers can request a price adjustment through Azure "
                   "support (the MDE portion is not double-charged)."),
    "servers_p2": ("Defender for Servers Plan 2: consumption-priced per protected server per hour, billed monthly. "
                   "Includes everything in Plan 1 (incl. the integrated MDE for Servers license) plus agentless "
                   "machine scanning, premium Defender Vulnerability Management capabilities, file integrity "
                   "monitoring, just-in-time VM access, OS baseline/system-updates assessment, DNS-layer alerts, and "
                   "a 500 MB/day free security-data ingestion allowance on the associated Log Analytics/Microsoft "
                   "Sentinel workspace (applies to designated security tables)."),
    "workload": ("Consumption-priced per protected resource, metered by plan: Defender for Storage per storage "
                 "account/month plus per-transaction overage above 73M/month and per-GB malware scanning; Defender "
                 "for Databases per database server (Cosmos DB per provisioned RU); Defender for Containers per vCore "
                 "of Kubernetes worker nodes (includes a monthly image-scan allowance); Defender for App Service per "
                 "app instance; Defender for Key Vault per vault/month; Defender for Resource Manager per "
                 "subscription/month; Defender for APIs by call-volume plan tier (Plans 1–5); AI Services per 1K "
                 "tokens. 30-day free trial on first enablement (malware scanning excluded)."),
    "dashboard": ("Regulatory compliance dashboard: the default Microsoft cloud security benchmark (MCSB) assessment "
                  "is included free with Defender for Cloud. Assigning additional built-in or custom compliance "
                  "standards requires at least one paid Defender for Cloud plan on the assessed scope, meaning any "
                  "plan except Defender for Servers Plan 1 and Defender for APIs Plan 1."),
}

MDC_URLS = {
    "overview": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction",
    "cspm": "https://learn.microsoft.com/azure/defender-for-cloud/concept-cloud-security-posture-management",
    "cspm_enable": "https://learn.microsoft.com/azure/defender-for-cloud/tutorial-enable-cspm-plan",
    "secure_score": "https://learn.microsoft.com/azure/defender-for-cloud/secure-score-security-controls",
    "recommendations": "https://learn.microsoft.com/azure/defender-for-cloud/security-policy-concept",
    "inventory": "https://learn.microsoft.com/azure/defender-for-cloud/asset-inventory",
    "onboard_aws": "https://learn.microsoft.com/azure/defender-for-cloud/quickstart-onboard-aws",
    "onboard_gcp": "https://learn.microsoft.com/azure/defender-for-cloud/quickstart-onboard-gcp",
    "attack_path": "https://learn.microsoft.com/azure/defender-for-cloud/concept-attack-path",
    "explorer": "https://learn.microsoft.com/azure/defender-for-cloud/how-to-manage-cloud-security-explorer",
    "agentless": "https://learn.microsoft.com/azure/defender-for-cloud/concept-agentless-data-collection",
    "ciem": "https://learn.microsoft.com/azure/defender-for-cloud/permissions-management",
    "dspm": "https://learn.microsoft.com/azure/defender-for-cloud/concept-data-security-posture",
    "governance": "https://learn.microsoft.com/azure/defender-for-cloud/governance-rules",
    "mcsb": "https://learn.microsoft.com/azure/defender-for-cloud/concept-regulatory-compliance",
    "reg_standards": "https://learn.microsoft.com/azure/defender-for-cloud/concept-regulatory-compliance-standards",
    "assign_standards": "https://learn.microsoft.com/azure/defender-for-cloud/assign-regulatory-compliance-standards",
    "dashboard": "https://learn.microsoft.com/azure/defender-for-cloud/regulatory-compliance-dashboard",
    "servers": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-servers-overview",
    "servers_plan": "https://learn.microsoft.com/azure/defender-for-cloud/plan-defender-for-servers-select-plan",
    "mde_integration": "https://learn.microsoft.com/azure/defender-for-cloud/integration-defender-for-endpoint",
    "data_benefit": "https://learn.microsoft.com/azure/defender-for-cloud/data-ingestion-benefit",
    "fim": "https://learn.microsoft.com/azure/defender-for-cloud/file-integrity-monitoring-overview",
    "jit": "https://learn.microsoft.com/azure/defender-for-cloud/just-in-time-access-overview",
    "updates": "https://learn.microsoft.com/azure/defender-for-cloud/enable-periodic-system-updates",
    "os_misconfig": "https://learn.microsoft.com/azure/defender-for-cloud/operating-system-misconfiguration",
    "storage": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-storage-introduction",
    "storage_sensitivity": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-storage-data-sensitivity",
    "malware_scan": "https://learn.microsoft.com/azure/defender-for-cloud/introduction-malware-scanning",
    "containers": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-containers-introduction",
    "databases": "https://learn.microsoft.com/azure/defender-for-cloud/tutorial-enable-databases-plan",
    "sql": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-sql-introduction",
    "app_service": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-app-service-introduction",
    "key_vault": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-key-vault-introduction",
    "arm": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-resource-manager-introduction",
    "apis": "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-apis-introduction",
    "ai": "https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection",
    "alerts": "https://learn.microsoft.com/azure/defender-for-cloud/alerts-overview",
    "xdr_integration": "https://learn.microsoft.com/azure/defender-for-cloud/concept-integration-365",
    "export_siem": "https://learn.microsoft.com/azure/defender-for-cloud/export-to-siem",
    "workflow": "https://learn.microsoft.com/azure/defender-for-cloud/workflow-automation",
    "support_matrix": "https://learn.microsoft.com/azure/defender-for-cloud/support-matrix-defender-for-cloud",
    "pricing": "https://azure.microsoft.com/pricing/details/defender-for-cloud/",
}

# Defender for Cloud government-cloud notes (verified against the Defender for Cloud support matrix
# cloud-support table, 2026-07-18). For an Azure-resource product, "government cloud" = Azure
# Government (US Gov Arizona/Texas/Virginia — the Azure platform serving GCC High/DoD organizations);
# the M365 GCC/GCC High/DoD distinction does not apply to Azure resources.
MDC_GOV = {
    "core": ("Available in Azure Government: Foundational CSPM (asset inventory, MCSB recommendations, secure score), "
             "Defender CSPM, Defender for Servers (P1/P2), Defender for Storage, Containers, Key Vault, Resource "
             "Manager, and the SQL/open-source database plans are GA."),
    "gaps": ("Azure Government gaps: Defender for APIs, Defender for App Service, AI Services threat protection, "
             "Defender for Cosmos DB, and DevOps security are not available; within Defender CSPM, CIEM, the Data & AI "
             "security dashboard, EASM integration, ServiceNow integration, and code-to-runtime mapping are not "
             "available; Defender for Storage sensitive data threat detection is not available (DSPM sensitive data "
             "scanning is GA)."),
    "dashboard": ("Regulatory compliance dashboard: GA in Azure Government (configuration via the Azure portal "
                  "experience; available standards vary by cloud, so verify the standard list in the target cloud)."),
    "servers": ("Defender for Servers P1/P2: GA in Azure Government; file integrity monitoring GA (not supported in "
                "GovCon Cloud Moderate)."),
}


# ---------------------------------------------------------------------------
# Reusable structured-row builders for products #2+ (Entra, then Intune/Defender/
# Sentinel/Defender-for-Cloud). Unlike the legacy Purview rows (free-text
# non_purview_dependencies split by the one-time migration), new product rows are
# authored with STRUCTURED dependencies directly — no heuristic parsing, primary/
# contributing stated explicitly. legacy_dependencies is "" (there is no legacy string).
# ---------------------------------------------------------------------------
def rel(product, role, note, solution=None):
    """Build one related_microsoft entry. role ∈ {primary, contributing}."""
    assert role in ("primary", "contributing"), f"bad role {role}"
    return {"product": product, "solution": solution, "role": role, "note": note}


def prow(product, framework, framework_version, id, control_ref, control_domain, control_intent,
         solution, capability_detail, how_it_supports, config_evidence_example, operational_evidence_example,
         related_microsoft, external_dependencies, coverage, confidence, license_requirement,
         cloud_availability_note, sources, last_verified, licensing_model="per_user",
         also_involves=None, status="verified"):
    """Structured row for a non-migrated product. `solution` populates the schema-stable
    `purview_solution` field (the mapped-solution field, product-agnostic despite its name)."""
    return {
        "id": id, "product": product, "framework": framework, "framework_version": framework_version,
        "control_ref": control_ref, "control_domain": control_domain, "control_intent": control_intent,
        "purview_solution": solution, "also_involves": also_involves or [],
        "capability_detail": capability_detail, "how_it_supports": how_it_supports,
        "config_evidence_example": config_evidence_example, "operational_evidence_example": operational_evidence_example,
        "related_microsoft": related_microsoft, "external_dependencies": external_dependencies,
        "legacy_dependencies": "",
        "coverage": coverage, "confidence": confidence,
        "license_requirement": license_requirement, "licensing_model": licensing_model,
        "cloud_availability_note": cloud_availability_note, "sources": sources,
        "status": status, "last_verified": last_verified,
    }
