"""Reader glossary (PR-011).

Plain-language definitions of the acronyms and initialisms that recur across the atlas,
so a reader fluent in one half of the material (compliance frameworks, or the Microsoft
stack) is not locked out of the other. The finding: a GRC/audit/legal reader hits an
acronym wall in the first paragraph of most product and solution pages ("MDCA", "CSPM"),
while a Microsoft-fluent reader hits the reverse wall ("ROPA", "CDE", "C3PAO").

WHERE THIS SHIPS. `assemble.py` imports GLOSSARY into `META["glossary"]`, exactly as it
imports `license_bands.BAND_DEFS` into `META["license_bands"]`. The single source is here;
the #/glossary route renders from META and cannot drift from this file, and JSON consumers
get the vocabulary too. Adding the block is a MINOR (a reader-facing feature; the analogue
is 2.10.0, which added meta.maintenance) -- see CHANGELOG 3.3.0 and AUDIT-FINDINGS §33.

THE CONTRACT: definitions DESCRIBE, they do not CLAIM. No entry states that a product
covers, satisfies, or is licensed for anything -- coverage lives on the rows, licensing on
the rows and the tier bands, accreditation status nowhere (it moves and would go stale).
GCC High is described by purpose and the standard it is assessed against, never by a live
authorization it "has". CMMC is the model, dateless (the rollout phase lives in the
maintenance trigger, not here). This mirrors the license_bands rule that the band is a
signpost, never the authority.

TERM CUT (Session 15, owner-reviewed). 47 terms ship. Notable exclusions and why, recorded
because the cut being on the record is part of the value (AUDIT-FINDINGS §33):
  - WORM, DIB      excluded: ZERO occurrences in the shipped artifact. The atlas writes
                   "immutable"/"records" and "Defense industrial base" spelled out. A
                   glossary defines what a reader actually meets.
  - CM             excluded: irreducibly ambiguous -- "Compliance Manager" (product) vs the
                   NIST 800-53 "CM" (Configuration Management) control family.
  - PII            excluded: universal across both audiences; defining it over-signals.
  - framework      excluded as a class (HIPAA, GDPR, PCI DSS, ISO, SOC, GLBA, FERPA, NIST,
    short-names    CSF): each carries its full name on its own framework card. CMMC is kept
                   because it is a program referenced far from its card (gov notes, 800-171).
  - E3/E5/tier     excluded: the tier legend and license bands already define these with
    and control    sourcing; and control-ref tokens (CC6, PR, AC, CFR-as-citation, TSC/POF)
    tokens         are navigation, not vocabulary.

AMBIGUITY RESOLUTIONS baked into the definitions (do not "simplify" them away):
  IRM  = Insider Risk Management here, NOT the legacy Information Rights Management.
  FIM  = File Integrity Monitoring here, NOT the retired Forefront Identity Manager.
  CIEM = the discipline; the product that carried the name (Entra Permissions Management)
         was retired 2025-10-01, so the definition names the discipline, not the product.
  MDCA = Defender for Cloud APPS; the definition states the atlas never shortens Defender
         for Cloud itself to "MDC", which is the collision it prevents.
  DoD  = the cloud ENVIRONMENT (SRG IL5), not the department.
  DLP / XDR = the discipline, with the mapped Microsoft product named as a second clause.
  C3PAO = the leading C is for "CMMC", not "Certified" (a common misreading).

Expansions verified where non-obvious: SSPA/DPR (Microsoft procurement + service assurance),
GCC/GCC High/DoD (Office 365 US Government service descriptions), CMMC/C3PAO/SPRS (Cyber AB,
SPRS/DISA), MCSB (Microsoft cloud security benchmark), and the Defender family names against
the atlas's own verified row prose. Sources in AUDIT-FINDINGS §33.

HOUSE-VOICE NOTE: every definition ran through /agentic-humanizer (Session 15, Phase 2).
The pass was light because the drafts were already de-slopped; its one mechanical output
rule, pattern 14 (strip em/en dashes), rewrote four entries (CDE, DKE, DPR, SIT). Keep new
entries em-dash-free to match.
"""

# term (as displayed) -> one-to-two-sentence plain definition.
# Authored in case-insensitive alphabetical order so the serialized meta.glossary reads in
# lookup order; the #/glossary route sorts case-insensitively regardless.
GLOSSARY = {
    "AIR": "Automated Investigation and Response: automation that investigates an alert and, where permitted, remediates it without an analyst driving each step.",
    "ASR": "Attack Surface Reduction: Microsoft Defender for Endpoint rules that block common exploit and malware behaviors.",
    "C3PAO": "CMMC Third-Party Assessment Organization: an assessor accredited by the Cyber AB to perform official CMMC Level 2 certification assessments. The leading C is for \"CMMC\", not \"Certified\", which is a common misreading.",
    "CDE": "Cardholder Data Environment: in PCI DSS, the systems and networks that store, process, or transmit payment-card data, which is the scope the standard's controls apply to.",
    "CIEM": "Cloud Infrastructure Entitlement Management: analyzing and right-sizing the permissions identities hold across cloud infrastructure. (The former standalone product, Microsoft Entra Permissions Management, was retired in 2025.)",
    "CMMC": "Cybersecurity Maturity Model Certification: the US Department of Defense program requiring defense contractors to implement NIST SP 800-171 controls, with Level 2 assessed either by self-assessment or by an independent C3PAO depending on the contract.",
    "CNAPP": "Cloud-Native Application Protection Platform: an umbrella category combining posture management (CSPM) and workload protection (CWPP) for cloud-native applications.",
    "CSPM": "Cloud Security Posture Management: continuous assessment of cloud configuration against a security baseline, surfacing misconfigurations and posture recommendations.",
    "CUI": "Controlled Unclassified Information: US-government information that is sensitive but not classified, and the object of the NIST SP 800-171 and CMMC protection requirements.",
    "CWPP": "Cloud Workload Protection Platform: runtime threat protection for cloud workloads such as servers, containers, and databases.",
    "DKE": "Double Key Encryption: encryption that uses two keys, one held by the customer and one by Microsoft, so that Microsoft alone cannot decrypt the content.",
    "DLP": "Data Loss Prevention: the practice of detecting and stopping sensitive data from leaving controlled boundaries. The atlas maps Microsoft's implementation, Microsoft Purview Data Loss Prevention.",
    "DoD": "The Microsoft 365 cloud environment reserved for the US Department of Defense, meeting the department's own security requirements (SRG Impact Level 5). Here \"DoD\" names that environment, not the department itself.",
    "DPIA": "Data Protection Impact Assessment: a GDPR assessment of privacy risk, required before certain high-risk processing of personal data.",
    "DPO": "Data Protection Officer: the GDPR role responsible for overseeing an organization's data-protection compliance.",
    "DPR": "Data Protection Requirements: Microsoft's Supplier Data Protection Requirements, the versioned control set (v12, March 2026 here) that suppliers must meet under SSPA. In this atlas, the mapped framework.",
    "DSPM": "Data Security Posture Management: continuous discovery and risk assessment of where sensitive data lives and how it is exposed.",
    "DSR": "Data Subject Request (also DSAR, Data Subject Access Request): an individual's request to access, correct, or delete their personal data under privacy law.",
    "EDR": "Endpoint Detection and Response: continuous monitoring of endpoints to detect, investigate, and respond to threats on them.",
    "EHR": "Electronic Health Record: a patient's digital clinical record, held in the healthcare systems the atlas treats as outside the Microsoft stack.",
    "FIM": "File Integrity Monitoring: detecting unauthorized changes to critical files and system objects. (Not the retired \"Forefront Identity Manager\".)",
    "GCC": "Government Community Cloud: a Microsoft 365 environment segregated for US public-sector customers and their partners, meeting US federal requirements. Eligibility is validated before purchase.",
    "GCC High": "Government Community Cloud High: a more strictly isolated US-government environment assessed against NIST SP 800-53 at a High categorization, for organizations handling export-controlled (ITAR/DFARS) or defense-adjacent data. Feature availability and timing often differ from the commercial cloud.",
    "IRM": "Insider Risk Management: the Microsoft Purview capability that detects and manages risky insider activity, such as data theft by a departing employee. Not the older \"Information Rights Management\" encryption feature.",
    "MAM": "Mobile Application Management: protecting corporate data inside apps, with or without full device enrollment.",
    "MCSB": "Microsoft cloud security benchmark: Microsoft's baseline of security recommendations, mapped to industry frameworks, used to assess Azure and multicloud resources.",
    "MDCA": "Microsoft Defender for Cloud Apps: Microsoft's cloud access security broker for discovering and governing SaaS-app usage. Distinct from Defender for Cloud, which this atlas never shortens to \"MDC\".",
    "MDE": "Microsoft Defender for Endpoint: Microsoft's endpoint detection-and-response and threat-protection product.",
    "MDI": "Microsoft Defender for Identity: Microsoft's product for detecting identity-based attacks against Active Directory and related identity signals.",
    "MDM": "Mobile Device Management: managing enrolled devices' configuration and compliance, for example through Microsoft Intune.",
    "MDO": "Microsoft Defender for Office 365: Microsoft's email and collaboration threat-protection product.",
    "MDTI": "Microsoft Defender Threat Intelligence: Microsoft's threat-intelligence data and tooling for enriching investigations.",
    "MDVM": "Microsoft Defender Vulnerability Management: Microsoft's capability for assessing vulnerabilities and tracking their remediation.",
    "MFA": "Multifactor Authentication: requiring more than one form of evidence to sign in.",
    "PHI": "Protected Health Information: individually identifiable health information protected under the US HIPAA rules.",
    "PIM": "Privileged Identity Management: the Microsoft Entra capability for just-in-time, time-bound activation and oversight of privileged roles.",
    "RBAC": "Role-Based Access Control: granting permissions through roles assigned to users, rather than to individuals directly.",
    "RMS": "Rights Management Service: the Microsoft encryption-and-usage-rights technology that underlies sensitivity-label protection.",
    "ROPA": "Records of Processing Activities: the register of an organization's personal-data processing required by GDPR Article 30.",
    "SIEM": "Security Information and Event Management: a platform that centralizes logs from across an estate for correlation, alerting, and investigation.",
    "SIT": "Sensitive Information Type: a pattern-based classifier (for example, a credit-card or passport number) that Microsoft Purview uses to detect a specific kind of sensitive data.",
    "SOAR": "Security Orchestration, Automation, and Response: automating investigation and response steps, usually as playbooks attached to a SIEM.",
    "SPRS": "Supplier Performance Risk System: the US Department of Defense database where contractors record their NIST SP 800-171 / CMMC assessment scores.",
    "SSPA": "Supplier Security and Privacy Assurance: Microsoft's procurement program requiring suppliers that handle personal or Microsoft data to attest compliance with its Data Protection Requirements (DPR).",
    "SSPR": "Self-Service Password Reset: the Microsoft Entra capability that lets users reset their own passwords after verifying their identity.",
    "UEBA": "User and Entity Behavior Analytics: detection that baselines normal behavior for users and devices, then flags anomalies against it.",
    "XDR": "Extended Detection and Response: correlating alerts across endpoints, identities, email, and cloud into single incidents. Microsoft's product is named Microsoft Defender XDR.",
}


def check_glossary():
    """Structural validation, mirroring license_bands' guard style. Pure assertions.

    Fails the build if a definition is empty, if a term smells like an unresolved
    duplicate, or -- the one that matters -- if a definition slips an em dash back in,
    since the humanizer pass (pattern 14) established em-dash-free as the house rule here.
    """
    assert GLOSSARY, "GLOSSARY is empty"
    for term, definition in GLOSSARY.items():
        assert term.strip() == term and term, f"glossary term {term!r} has whitespace or is empty"
        assert definition.strip(), f"glossary term {term!r} has an empty definition"
        assert "—" not in definition and "–" not in definition, \
            f"glossary term {term!r} contains an em/en dash; keep entries em-dash-free (see module docstring)"
    return len(GLOSSARY)
