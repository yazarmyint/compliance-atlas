"""Assemble compliance-atlas.json from per-framework row modules.
Run:  python build/assemble.py
Add a framework: create build/rows_<name>.py exposing FRAMEWORK (dict) and ROWS (list), append to MODULES.
Add a product: see docs/AUTHORING.md "Add a product" — products-map entry in common.py, row modules with
product=<id>, solutions registered in SOLUTIONS and the product's solutions list.

Canonical file renamed 2026-07-17: purview-compliance-map.json -> compliance-atlas.json (platform generalization)."""
import collections, importlib, json, os, re, shutil, sys, datetime
from urllib.parse import urlparse

# ---- stale-bytecode guard (PR-058). MUST stay above the sibling imports below. ----
# Python validates cached bytecode on (source mtime truncated to whole seconds, source size), so a
# same-length edit written in the same second as the previous build leaves a .pyc that validates as
# fresh. The build then regenerates the artifact from OLD constants -- silently, with exit 0. That
# is not hypothetical: it was hit and reproduced against a date edit in common.py (AUDIT-FINDINGS
# §26.8), and a re-verification pass makes exactly that kind of edit.
#
# The cache is therefore removed outright, before the first sibling import. Setting
# sys.dont_write_bytecode alone would NOT close this: it stops new .pyc files being written, not
# existing stale ones being loaded, which is the failure above exactly. It is set as well so the
# purge does not simply re-litter the tree each run.
#
# Deliberately inline rather than factored into a shared build/ module: any such module would have
# to be imported to run, and that import is itself served from the cache this code exists to
# distrust. Six duplicated lines beat a guard that depends on what it is guarding against.
sys.dont_write_bytecode = True
shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__"),
              ignore_errors=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (SOLUTIONS, PRODUCTS, RELATED_PRODUCTS, VERIFIED_DATE,
                    reverify_passes, MAINTENANCE, RETIRED_NAMES, STALENESS_CLASSES,
                    TRIGGER_TYPES, TYPE_CADENCE, constant_dicts, lic_dicts, staleness_class,
                    REVERIFY_DATE, REVERIFY_DATE_2, REVERIFIED_LIC_KEYS, REVERIFIED_LIC_KEYS_2)
from dependency_migration import migrate_row
import license_bands

# Order controls display order in the HTML.
MODULES = ["rows_dpr", "rows_iso", "rows_soc2", "rows_hipaa", "rows_171", "rows_80053", "rows_csf", "rows_pci", "rows_glba", "rows_ferpa", "rows_gdpr"]

# Hosts that count as *Microsoft capability documentation* for the source-composition rule.
# Anything else in a row's sources counts as the official framework authority — which is why
# microsoft.com/procurement/sspa is correctly an official source on the DPR rows (Microsoft is
# the framework author there) while learn.microsoft.com never is.
MS_DOC_HOSTS = {"learn.microsoft.com", "docs.microsoft.com", "azure.microsoft.com", "techcommunity.microsoft.com"}
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

INDUSTRIES = {
    "healthcare": {"name": "Healthcare & life sciences",
        "frameworks": ["hipaa-security", "pci-dss-4", "nist-csf-2", "soc-2", "iso-27001-2022"],
        "note": "For hospitals, clinics, and life-sciences firms, where the HIPAA Security Rule is the anchor and card payments pull in PCI. The Microsoft stack splits the work across products: protecting clinical devices, defending against ransomware, capturing audit trails from EHR systems, and covering the cloud-hosted server estate.",
        "note_detail": "HIPAA Security Rule anchors; PCI for patient payments; state privacy composite on backlog. "
                "Intune carries the workstation/device safeguards (§164.310, device encryption for §164.312(a)(2)(iv)) common in clinical settings. "
                "Defender XDR carries the ransomware-facing controls: malicious-software protection (§164.308(a)(5)(ii)(B)), incident response (§164.308(a)(6)), and vulnerability input to risk analysis. "
                "Sentinel extends the §164.312(b) audit mechanism and §164.308(a)(1)(ii)(D) activity review to EHR/clinical systems via Syslog/CEF, the record-and-examine layer Purview Audit cannot see. "
                "Defender for Cloud covers the cloud-hosted EHR server estate: file integrity monitoring for §164.312(c), per-server anti-malware licensing, and HIPAA/HITRUST on the regulatory compliance dashboard (cloud-resource scope; Compliance Manager assesses the M365 side)."},
    "dib": {"name": "Defense industrial base",
        "frameworks": ["nist-800-171", "nist-csf-2", "iso-27001-2022"],
        "note": "For defense contractors and their suppliers that handle controlled unclassified information, where NIST 800-171 and CMMC set the bar. The stack lines up product by product across endpoint hardening, threat detection, audit trails, and cloud enclaves, with government-cloud limits that recur throughout this sector.",
        "note_detail": "CMMC Level 2 Phase 2 (third-party certification in new contracts) begins Nov 10, 2026; GCC High notes sit on every 800-171 row. "
                "Intune anchors the endpoint CM/mobile/encryption families (3.1.18/3.1.19, 3.4.1/3.4.2, 3.13.16), though Windows Autopilot and update policies are limited in GCC High/DoD. "
                "Defender XDR carries the assessment-heavy 3.11/3.14 detection band (MDVM scanning, malware protection, system monitoring) plus 3.6 incident response; all workloads run in GCC High/DoD, though Microsoft Threat Experts does not. "
                "Sentinel carries the 3.3 audit-and-accountability band (3.3.1 create/retain, 3.3.4 failure alerting, 3.3.5 correlation); multi-year retention is a consumption meter at data-lake rates. "
                "Defender for Cloud assesses CUI cloud enclaves for 3.11.2–3.11.3 and 3.12, cloud-resource scope only, with CIEM and several CSPM features absent in Azure Government."},
    "finserv": {"name": "Financial services",
        "frameworks": ["glba-safeguards", "pci-dss-4", "soc-2", "nist-csf-2", "iso-27001-2022"],
        # "insurers" removed from this note when the dedicated Insurance lens shipped (PR-020): insurers
        # are GLBA financial institutions, but their operative rule is a state one, and this note is
        # written about banks and lenders. See INDUSTRIES["insurance"].
        "note": "For banks, lenders, and fintechs under the GLBA Safeguards Rule, with PCI reaching card data and SOC 2 covering service commitments. The stack fits best on continuous vulnerability monitoring, institution-wide audit trails, and extending both to cloud-hosted banking workloads.",
        "note_detail": "SEC 17a-4 / FINRA supervision (strong Records Management + Communication Compliance stories) on v2 backlog. "
                "For the amended Safeguards Rule, Defender Vulnerability Management supplies the §314.4(d)(2) continuous-monitoring alternative to annual pen tests plus biannual vulnerability assessments, a cheaper path for smaller institutions. "
                "Sentinel completes §314.4(c)(8) institution-wide by ingesting the banking/CRM audit trails the workload products cannot see, and carries the PCI Req 10 retention/review story for the CDE. "
                "Defender for Cloud extends the §314.4(d)(2) election to cloud-hosted banking workloads (agentless assessment well beyond the biannual floor) and joins cloud systems to the customer information they hold for §314.4(c)(2)."},
    "insurance": {"name": "Insurance",
        "frameworks": ["glba-safeguards", "soc-2", "pci-dss-4", "nist-csf-2"],
        "note": "For carriers, brokers, and managing general agents: financial institutions under GLBA, card handlers under PCI, and SOC 2 respondents to their distribution partners, with NIST CSF 2.0 as the program frame examiners increasingly expect. One caveat on GLBA applies to insurers specifically.",
        "note_detail": "The GLBA caveat: insurers are GLBA Title V financial institutions, but the FTC Safeguards Rule at 16 CFR 314 — the text these rows cite — exempts entities regulated by a state insurance authority. The operative requirement is usually the NAIC Insurance Data Security Model Law, adopted in most states, or New York's 23 NYCRR 500. Both track 16 CFR 314 closely enough that the control mappings read across; the citations do not. Take these rows for the control substance and cite your own state's text. "
                "PCI reaches premium and claims payments wherever cards are accepted, directly or through a portal, and SOC 2 arrives from the other direction: MGAs, third-party administrators, and insurtech vendors are asked for it by the carriers they distribute for. "
                "Purview is Audit-heavy here (13 of 51 rows): the record-keeping and retention obligations across policy, claims, and underwriting files are the densest part of the sector's data layer, with classification and DLP over policyholder information. "
                "Sentinel carries the institution-wide audit and detection story the workload products cannot see — policy administration, claims, and underwriting systems are typically third-party or mainframe-adjacent and reach the security program through connectors rather than native integration. "
                "Defender for Cloud's 14 rows cover the cloud-hosted side of that estate, which is where modern quoting and claims platforms increasingly sit."},
    "higher-ed": {"name": "Higher education",
        "frameworks": ["ferpa", "glba-safeguards", "pci-dss-4", "nist-csf-2"],
        "note": "For colleges and universities, which answer to FERPA for education records and, as Title IV institutions, to the GLBA Safeguards Rule as well, with PCI reaching campus payments. The stack mostly protects and locates student records and supplies the Safeguards Rule's continuous-monitoring path.",
        "note_detail": "FERPA governs education records; Title IV institutions also answer to the GLBA Safeguards Rule (FSA-enforced), with PCI reaching campus card payments and CSF 2.0 as the working baseline. "
                "The stack's role centers on protecting and locating those records (sensitivity labeling and DLP over student data, eDiscovery and audit for records requests), while Defender Vulnerability Management supplies the §314.4(d)(2) continuous-monitoring path for the Safeguards Rule. "
                "State student-privacy laws remain on backlog."},
    "k12": {"name": "K-12 education",
        "frameworks": ["ferpa", "nist-csf-2"],
        "note": "For school districts, where FERPA governs student education records and CSF 2.0 is the working security baseline. The Microsoft stack mainly protects and locates those records: labeling and DLP over student data, plus eDiscovery and audit for records requests and access logging.",
        "note_detail": "FERPA governs the education records K-12 districts hold; CSF 2.0 is the working security baseline where no sector mandate applies. "
                "The Microsoft stack's role here is protecting and locating those records: sensitivity labeling and DLP over student data, eDiscovery and audit for records requests and access logging. "
                "State student-privacy laws remain on backlog."},
    "retail": {"name": "Retail & e-commerce",
        "frameworks": ["pci-dss-4", "nist-csf-2", "soc-2", "gdpr"],
        "note": "For merchants and e-commerce operators, where PCI DSS governs card data and GDPR stands in for US state privacy. The stack covers the anti-malware and anti-phishing requirements, the central log-collection and retention engine PCI expects, and cloud-hosted parts of the cardholder environment.",
        "note_detail": "GDPR rows double as the analog for US state privacy (composite on backlog). "
                "PCI Req 5 stacks the full anti-malware story (Defender engine + Intune policy), and Defender for Office 365 carries the 5.4.1 anti-phishing requirement new in v4. "
                "Sentinel is the Req 10 engine: central log collection (10.3.3), the automated daily review 10.4.1.1 mandates, and 12-month retention with a 3-month hot window (10.5.1), priced by ingest volume. "
                "Defender for Cloud covers cloud-hosted CDE components: agentless scanning against the 11.3.1 cadence, per-server anti-malware for Req 5, and Req 2 hardening monitoring (ASV external scans and non-cloud segments stay external)."},
    "saas": {"name": "SaaS & technology",
        "frameworks": ["soc-2", "iso-27001-2022", "gdpr", "nist-csf-2", "hipaa-security", "pci-dss-4"],
        "note": "For software and technology providers running on cloud infrastructure, typically examined under SOC 2 and ISO 27001, with HIPAA or PCI applying when they touch health or payment data. Because production lives in the cloud, Defender for Cloud is the anchor, including free multicloud coverage for AWS and GCP.",
        "note_detail": "HIPAA applies when handling PHI as a business associate; PCI when in the payment path. "
                "For SaaS providers the product runs on cloud infrastructure, so Defender for Cloud is the production-posture anchor: CC7.1 configuration/vulnerability detection rated Direct, the SOC 2 dashboard standard for cloud resources, and ISO A.5.23/A.8.9 cloud-service posture, with AWS/GCP multicloud coverage included via the free connectors."},
    "legal": {"name": "Legal & professional services",
        "frameworks": ["soc-2", "iso-27001-2022", "gdpr", "hipaa-security"],
        "note": "For law firms, accountancies, and consultancies, where client assurance drives SOC 2 and ISO 27001, client personal data pulls in GDPR, and health-sector engagements bring HIPAA obligations. The stack concentrates on matter confidentiality, need-to-know access, and a persistently targeted endpoint and mailbox estate.",
        "note_detail": "SOC 2 is the client-assurance ask; ISO 27001 certification often accompanies it at firms with international clients. GDPR binds the firm both as controller of its own client data and as processor acting on client instructions, while HIPAA applies only when the firm is a business associate — health-sector litigation, benefits counsel, life-sciences advisory — so treat those rows as conditional on handling PHI. "
                "Purview carries the confidentiality core: sensitivity labels and label-based encryption for matter material, DLP on the outbound path, retention and records management for engagement-file destruction schedules, and eDiscovery for the firm's own holds rather than its clients'. "
                "Entra carries need-to-know, with Conditional Access over the unmanaged and personal devices common in partner-heavy firms and ID Governance access packages for matter- and client-scoped teams. Information Barriers appears once (A.5.3) and is the nearest thing here to an ethical wall, though the wall itself is a matter-intake decision rather than a product setting. "
                "Defender XDR is 22 rows, 18 of them Defender for Endpoint: legal is a standing target for business email compromise and departing-partner data theft, and the endpoint and mail surface is where that lands. "
                "Defender for Cloud's 16 rows apply only where a firm runs its own cloud estate; most buy practice-management SaaS instead, in which case the vendor's own SOC 2 report is the relevant artifact."},
    "manufacturing": {"name": "Manufacturing",
        "frameworks": ["nist-csf-2", "iso-27001-2022", "nist-800-171", "gdpr"],
        "note": "For manufacturers, who juggle general security baselines (CSF 2.0, ISO 27001), the defense-supply-chain rules that apply to some of them (NIST 800-171 and CMMC), and GDPR for any EU operations. The stack's heaviest fit is on the defense-industrial-base control families.",
        "note_detail": "Manufacturers straddle two regimes: CSF 2.0 and ISO 27001 as general security baselines, and NIST 800-171/CMMC for the defense-industrial-base suppliers among them, with GDPR reaching any EU operations. "
                "The stack maps most heavily on the 800-171 endpoint, audit, and detection families, the rows detailed under the Defense industrial base lens."},
    "federal": {"name": "US federal & FedRAMP-adjacent",
        "frameworks": ["nist-800-53", "nist-csf-2"],
        "note": "For federal-civilian agencies and cloud providers pursuing FedRAMP, mapped against NIST 800-53 as a curated data-protection subset. Sentinel deepens the audit family and Defender for Cloud adds continuous monitoring, all within a government-cloud scope worth confirming when you plan.",
        "note_detail": "Federal-civilian (FISMA) agencies and SaaS providers pursuing FedRAMP; 800-53 is mapped as a curated data-protection subset. GCC High is assessed against NIST SP 800-53 at FIPS 199 High. Distinct from the DIB/CMMC lens (800-171). "
                "Sentinel deepens the AU family (AU-6 automated review and AU-11 organization-defined retention rated Direct) and adds RA-10 threat hunting; check the Azure Government gap list (summary rules, SOC optimization, MDTI matching absent) when scoping. "
                "Defender for Cloud brings the CA family in: CA-7 continuous monitoring rated Direct via the dashboard's NIST 800-53 standard, plus CM-8 cloud inventory and SI-7 file integrity monitoring; cloud-resource scope, so verify the Azure Government gaps (CIEM, Data & AI dashboard, several plans absent)."},
    "ms-supplier": {"name": "Microsoft suppliers & partners",
        "frameworks": ["sspa-dpr", "iso-27001-2022", "soc-2"],
        "note": "For vendors and partners enrolled in Microsoft's Supplier Security and Privacy Assurance program, whose contracts drive the Data Protection Requirements. This is the most Purview-centric lens: classification, DLP, retention, records, audit, and eDiscovery carry the data-handling obligations, while non-data controls stay deliberately unmapped.",
        "note_detail": "SSPA enrollment drives DPR compliance; ISO 27001 certification can qualify for SSPA alternative-compliance paths, and SOC 2 reports often accompany them. "
                "The DPR story is Purview-dense: classification and DLP for the data-handling requirements, retention and records management for return-or-destroy, and audit plus eDiscovery for the incident and data-subject obligations. "
                "Requirements outside the data layer (identity, transport encryption, supplier AI systems) stay deliberately unmapped."},
}

BRAND = {
    # Public name settled 2026-07-19 (PROJECT-REVIEW PR-043). The tagline is rendered as its own
    # element (hero overline, brand tooltip), never concatenated into the title string.
    "title": "Compliance Atlas",
    "working_title": False,
    "tagline": "Mapping frameworks to the Microsoft security stack",
    # Bumped 2.0.0 -> 2.9.0 for the first public release (PR-045). 2.0.0 was set at the platform
    # generalization and never moved through the eight milestones after it; CHANGELOG.md backfills
    # those from the audit record and applies the versioning policy to them retroactively, which is
    # what produces 2.9.0. 2.9.0 was a MINOR bump on 2.8.1 under that policy: features and
    # industry lenses added, no data-model or product-scope change.
    # 2.9.1 is a PATCH: American English unified across rendered text. Row prose changed in 53
    # places, no claim did — no coverage, confidence, source, or last_verified field was touched.
    # 2.10.0 is a MINOR: META gained the maintenance-trigger table (PR-050). Additive and
    # structural — a new key under meta, no change to the row data model, no row touched. The
    # policy's bands are written around readers, and this addition is invisible to one; the
    # discriminator that actually decides it is compatibility, and no consumer must change code
    # for an added key. Reasoning in full in CHANGELOG.md and AUDIT-FINDINGS §26.
    # 3.1.0 is a MINOR: reader-facing polish — the legend layout fix (PR-059), a footer feedback
    # link, and an og:image social card. No row changed; compliance-atlas.json is byte-identical to
    # 3.0.0 apart from this version field. Sorted MINOR because a reader gains features (a link
    # preview, an error-report path), which the policy's MINOR band names; the counter-argument that
    # no *dataset* addition occurred was weighed and set aside. Reasoning in AUDIT-FINDINGS §29.5.
    "atlas_version": "3.1.0",
    # No hand-maintained as_of: the landing page shows meta.verified_range, derived from the rows
    # themselves at assemble time, so the stated currency cannot drift from the data (PR-014).
}

FOOTER_LINES = [
    "Informational reference only; not legal, audit, or compliance advice.",
    "Independent community project. Not affiliated with, sponsored, or endorsed by Microsoft Corporation.",
    "Framework and standard names are the property of their respective owners and are used for identification only.",
    "Currency is governed by each row's last-verified date; product capabilities and licensing change frequently, so verify before relying on it.",
    # PR-041. Plain text, no markup: footer_lines are escaped on render. The reasoning behind the
    # split — that open licensing is only safe because the atlas paraphrases rather than quotes
    # standards text — lives on the about page and in LICENSE-CONTENT.md, not here.
    "Atlas content © 2026 Yazar, licensed CC BY 4.0; the build code is MIT. Reuse and adapt it freely with attribution.",
]

LICENSING_MODELS = ("per_user", "consumption", "included", "n/a")

# Who maintains this and where corrections go (PR-044). Shipped in META so the about page and the
# footer render the same strings; nothing here is hand-typed into template.html.
PROJECT = {
    "maintainer": "Yazar",
    "repo_url": "https://github.com/yazarmyint/compliance-atlas",
    "issues_url": "https://github.com/yazarmyint/compliance-atlas/issues",
    "changelog_url": "https://github.com/yazarmyint/compliance-atlas/blob/main/CHANGELOG.md",
    "content_license": "CC BY 4.0",
    "code_license": "MIT",
}

# PR-021: sectors a reader might expect and won't find, each gated on a framework the atlas does not
# map. Rendered twice — a short line on the Industries index, the full list on the about page — from
# this one definition, so the two cannot drift. Keep the reasons honest about which are decisions and
# which are gaps: CJIS is a genuine omission (PROJECT-REVIEW PR-025), the other two are structural.
ABSENT_INDUSTRIES = [
    {"sector": "State & local government", "framework": "CJIS Security Policy",
     "reason": "Its control areas line up well with these six products, so this is a gap rather than a decision — it is the strongest candidate for the next framework added."},
    {"sector": "Energy & utilities", "framework": "NERC CIP",
     "reason": "Built around the operational technology and control systems that run the bulk electric system, which none of the six products reach."},
    {"sector": "Pharmaceuticals & medical devices", "framework": "21 CFR Part 11",
     "reason": "Turns on validation and electronic-signature semantics for FDA-regulated records rather than the security controls mapped here."},
]

# <meta name="description"> and og:description, substituted into the template head by build_html.py.
# The counts are filled from the assembled dataset so the summary cannot drift from it.
DESCRIPTION = ("{tagline}. {rows} control mappings across {frameworks} compliance frameworks and {products} "
               "Microsoft security products, each rated for claim strength and verified against an official source.")

META = {
    "title": BRAND["title"],
    "version": BRAND["atlas_version"],
    "brand": BRAND,
    "project": PROJECT,
    "absent_industries": ABSENT_INDUSTRIES,
    # Stated on the about page. Deliberately a statement of intent with no service promise attached:
    # this is a one-person project and pretending otherwise would be the dishonest option.
    "reverification_policy": ("Every row carries the date its claims were last checked against a live source. "
                              "Full re-verification passes are run at least twice a year, and targeted ones whenever a "
                              "diarized change lands — a framework revision, a Microsoft rename, a licensing restructure. "
                              "This is a single-maintainer project, so treat those dates as the real currency signal "
                              "rather than any assumption that the whole atlas is refreshed continuously."),
    "footer_lines": FOOTER_LINES,
    # No build timestamp here, deliberately (PR-057). Nothing in compliance-atlas.json is
    # time-derived, so a rebuild with no content change produces a strictly empty git diff on it
    # and the diff becomes a zero-tolerance drift check. The footer's "Built …" line is unchanged
    # as a feature; build_html.py stamps that timestamp into the HTML at generation time instead.
    "default_last_verified": VERIFIED_DATE,
    "product_scope": list(PRODUCTS.keys()),
    "licensing_models": {
        "per_user": "Licensed per user/SKU (e.g., Microsoft 365 E5-family, Purview Suite add-ons).",
        "consumption": "Usage-based pricing (e.g., ingestion/compute billed via Azure).",
        "included": "Included with a platform entitlement at no separate charge.",
        "n/a": "No license claim (boundary rows).",
    },
    # PR-015. The license-tier lens. Definitions live in build/license_bands.py beside the
    # mapping that produces them, so the legend a reader sees and the derivation cannot
    # drift apart. Static strings only -- nothing here is computed at build time.
    "license_bands": license_bands.BAND_DEFS,
    "license_band_partial": license_bands.BAND_PARTIAL_DEF,
    "license_band_scope": license_bands.BAND_SCOPE_NOTE,
    "coverage_levels": {
        "Direct Support": "The product directly implements/enforces the control activity (within the stated scope).",
        "Partial Support": "The product implements part; a control outside it is also required.",
        "Evidence Support Only": "The product supplies evidence; the control itself lives elsewhere.",
        "Not Covered": "The product does not address this; another tool or process owns it (boundary row).",
    },
    "confidence_levels": {
        "High": "Mapping is well-established and expected to withstand auditor scrutiny.",
        "Medium": "Reasonable mapping; acceptance may vary by assessor/scope.",
        "Low": "Defensible but narrow or contested; position carefully.",
    },
    "disclaimer": ("Mapped products support or evidence controls; they do not by themselves make an organization "
                   "compliant with any framework. Control references are practical intent mappings in original words, "
                   "not quotations of the standards. Licensing claims derive from each product's authoritative "
                   "licensing source and can change; verify before relying on it."),
    # PR-050. The maintenance-trigger table, shipped so the dataset carries its own
    # re-verification schedule rather than leaving it in prose nobody executes.
    #
    # DECLARATIVE ONLY, and this is load-bearing: every value here is a static date,
    # a static string, or a static integer copied straight out of common.py. Nothing
    # time-derived is serialized. Staleness is evaluated in maintenance_report() and
    # written to stderr, never to this dict -- because a computed field here would make
    # a content-free rebuild produce a non-empty git diff, which is the drift check the
    # whole QA method rests on.
    "maintenance": {
        "triggers": MAINTENANCE,
        "trigger_types": {t: TYPE_CADENCE[t] for t in TRIGGER_TYPES},
        "staleness_classes": STALENESS_CLASSES,
        "retired_names": RETIRED_NAMES,
    },
}

# Retired names are flagged only when they appear UN-GLOSSED. The atlas deliberately
# writes "Microsoft Defender Suite (formerly Microsoft 365 E5 Security)" and
# "Defender for Cloud Apps (MDCA; formerly Microsoft Cloud App Security)", so the
# suppression window has to reach back past an abbreviation and separator, not just
# past a bare "(".
GLOSS = re.compile(r"formerly[^)]{0,4}$", re.IGNORECASE)

def check_maintenance_table(row_ids):
    """Structural validation of MAINTENANCE. Pure assertions, no dates evaluated.

    The point of these is that an orphaned trigger becomes impossible: a coordinate
    that no longer resolves, or a constant nobody is scheduled to re-check, fails the
    build the moment it appears rather than sitting in prose for months.
    """
    dicts = constant_dicts()
    seen = set()
    for t in MAINTENANCE:
        tid = t["id"]
        assert tid not in seen, f"duplicate trigger id: {tid}"
        seen.add(tid)
        assert t["type"] in TRIGGER_TYPES, f"trigger {tid} bad type: {t['type']}"
        assert t["title"] and t["note"], f"trigger {tid} missing title or note"
        # cadence_days is None for a fixed-date trigger (an announced retirement, a
        # regulatory milestone), where a rolling clock would add nothing.
        cad = t["cadence_days"]
        assert cad is None or (isinstance(cad, int) and cad > 0), f"trigger {tid} bad cadence_days: {cad}"
        for field in ("next_review", "last_executed"):
            val = t[field]
            if val is None:
                continue
            assert ISO_DATE.fullmatch(val), f"trigger {tid} {field} not an ISO date: {val!r}"
            datetime.date.fromisoformat(val)  # raises on an impossible date
        assert t["last_executed"] is None or \
            datetime.date.fromisoformat(t["last_executed"]) <= datetime.date.today(), \
            f"trigger {tid} last_executed is in the future: {t['last_executed']}"
        for dict_name, key in t["affects"]:
            assert dict_name in dicts, f"trigger {tid} names unknown dict: {dict_name}"
            assert key in dicts[dict_name], f"trigger {tid} names missing key {dict_name}[{key!r}]"
        for rid in t["rows"]:
            assert rid in row_ids, f"trigger {tid} names a row that does not exist: {rid}"

    # Every licensing constant must be claimed by at least one trigger. This is the
    # assertion that found the three ownership gaps the prose list had (ENTRA_LIC's
    # seven keys, SENTINEL_LIC soar/included, MDC_LIC workload) on its first run.
    owned = {(d, k) for t in MAINTENANCE for d, k in t["affects"]}
    unowned = sorted({(d, k) for d, keys in lic_dicts().items() for k in keys} - owned)
    assert not unowned, ("licensing constants with no maintenance trigger: "
                         + ", ".join(f"{d}[{k!r}]" for d, k in unowned))


def retired_name_hits():
    """Un-glossed retired names across the constant registries and the assembled rows.

    Clock-free by design. A cadence check would not have caught PR-035 -- the rename
    landed days after those strings were authored, long inside any sane cadence -- but
    the defect was statically visible: one SKU and its own former name presented as
    two alternatives. This is the limb that sees that.
    """
    hits = []

    def scan(label, text):
        if not isinstance(text, str) or not text:
            return
        for pair in RETIRED_NAMES:
            for old in pair["retired"]:
                for m in re.finditer(r"(?<!\w)" + re.escape(old) + r"(?!\w)", text):
                    if GLOSS.search(text[max(0, m.start() - 24):m.start()]):
                        continue
                    hits.append((label, old, pair["current"]))

    for name, d in constant_dicts().items():
        for key, val in d.items():
            if isinstance(val, str):
                scan(f"{name}[{key!r}]", val)
            elif isinstance(val, dict):
                for f in ("official_name", "short_name", "notes", "full_name", "scope"):
                    scan(f"{name}[{key!r}].{f}", val.get(f, ""))
                if name == "SOLUTIONS":
                    scan(f"{name} key {key!r}", key)
    return hits


def maintenance_report(rows, today, stream, limit=12):
    """Evaluate staleness and emit it. Returns the number of warnings emitted.

    Deliberately returns a count and nothing else: no caller can write any of this
    back into the dataset, because there is nothing to write. Every value below is
    computed here, printed, and discarded.
    """
    lines, counts = [], {"trigger": 0, "stale": 0, "naming": 0}

    # --- limb 1a: triggers past their next_review -------------------------------
    due = []
    for t in MAINTENANCE:
        if not t["next_review"]:
            continue
        overdue = (today - datetime.date.fromisoformat(t["next_review"])).days
        if overdue > 0:
            due.append((overdue, t))
    counts["trigger"] = len(due)
    for overdue, t in sorted(due, key=lambda x: -x[0])[:limit]:
        aff = ", ".join(f"{d}[{k!r}]" for d, k in t["affects"]) or "no constants"
        n_rows = len({r["id"] for r in rows for d, k in t["affects"]
                      if d in lic_dicts() and lic_dicts()[d][k] in (r.get("license_requirement") or "")})
        lines.append(f"  TRIGGER  {t['id']} [{t['type']}] next_review {t['next_review']} "
                     f"-- {overdue} days overdue")
        lines.append(f"           {t['title']}")
        lines.append(f"           affects {aff}"
                     + (f" ({n_rows} rows)" if n_rows else "")
                     + f" | last executed {t['last_executed'] or 'never'}")
        lines.append(f"           runbook: docs/MAINTENANCE.md#{t['type']}")
        lines.append("")

    # --- limb 1b: licensing constants past their class cadence ------------------
    # A constant's verification date is the latest pass that re-fetched it. That is
    # read from the same declarative ledger last_verified is derived from, so the two
    # can never disagree.
    verified_on = {}
    for date, keys in ((REVERIFY_DATE, REVERIFIED_LIC_KEYS), (REVERIFY_DATE_2, REVERIFIED_LIC_KEYS_2)):
        for coord in keys:
            verified_on[coord] = date

    stale = []
    for dict_name, d in lic_dicts().items():
        cls = staleness_class(dict_name)
        if not cls:
            continue
        cls_name, cadence = cls
        for key, value in d.items():
            date = verified_on.get((dict_name, key))
            if not date:
                continue
            age = (today - datetime.date.fromisoformat(date)).days
            if age > cadence:
                n_rows = sum(1 for r in rows if value in (r.get("license_requirement") or ""))
                stale.append((age, dict_name, key, cls_name, cadence, date, n_rows))
    counts["stale"] = len(stale)
    for age, dict_name, key, cls_name, cadence, date, n_rows in sorted(stale, key=lambda x: -x[0])[:limit]:
        lines.append(f"  STALE    {dict_name}[{key!r}] [{cls_name}, {cadence}d] "
                     f"verified {date} -- {age} days old")
        lines.append(f"           governs {n_rows} rows")
        lines.append("")

    # Boundary rows carry no licensing constant, so they are named individually.
    # There are eight of them; a list that short is clearer than an aggregate.
    b_cadence = STALENESS_CLASSES["boundary"]["cadence_days"]
    boundary = [r for r in rows if r.get("licensing_model") == "n/a"
                and (today - datetime.date.fromisoformat(r["last_verified"])).days > b_cadence]
    if boundary:
        oldest = min(r["last_verified"] for r in boundary)
        counts["stale"] += 1
        lines.append(f"  STALE    {len(boundary)} boundary rows [boundary, {b_cadence}d] "
                     f"oldest {oldest} -- {(today - datetime.date.fromisoformat(oldest)).days} days old")
        lines.append("           " + ", ".join(sorted(r["id"] for r in boundary)))
        lines.append("")

    # --- limb 2: the clock-free naming lint -------------------------------------
    hits = retired_name_hits()
    counts["naming"] = len(hits)
    for label, old, current in hits[:limit]:
        lines.append(f"  NAMING   {label} contains retired name {old!r} un-glossed; "
                     f"current name is {current!r}")
        lines.append("")

    total = counts["trigger"] + counts["stale"] + counts["naming"]
    if not total:
        return 0

    print("\nbuild/assemble.py: maintenance warnings (non-fatal; build succeeded)\n", file=stream)
    for line in lines:
        print(line, file=stream)
    hidden = max(0, counts["trigger"] - limit) + max(0, counts["stale"] - limit) + max(0, counts["naming"] - limit)
    if hidden:
        print(f"  ... and {hidden} more; run with --maintenance-report for the full list\n", file=stream)
    governed = sum(1 for r in rows if r.get("licensing_model") != "n/a")
    print(f"  {counts['trigger']} triggers due | {counts['stale']} constants past cadence "
          f"({governed} of {len(rows)} rows governed) | {counts['naming']} naming defects", file=stream)
    print("  These are advisory. Re-run with --strict-maintenance to fail the build instead.\n",
          file=stream)
    return total


def main():
    frameworks, rows, dep_log = {}, [], []
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            print(f"  [skip] {m} (not written yet)")
            continue
        fw = mod.FRAMEWORK
        frameworks[fw["id"]] = fw
        rows.extend(mod.ROWS)
        print(f"  [ok]   {m}: {len(mod.ROWS)} rows ({fw['name']})")

    # ---- dependency-model migration (mechanical; see dependency_migration.py) ----
    for r in rows:
        rec = migrate_row(r)
        if rec:
            dep_log.append(rec)

    # ---- last_verified: re-verification passes (see common.py, AUDIT-FINDINGS SS22) ----
    # A row's date moves only if its licensing constant was re-fetched live in that pass
    # (whether it changed or passed) or its sources changed. Rows resting on constants that
    # were not re-checked keep their older date, which is the honest answer for them.
    # Passes run in date order, so the latest pass that verified something the row rests
    # on is the date the row carries.
    verified_rows = set()
    for pass_date, reverified_strings, source_rows in reverify_passes():
        basis = {}
        for r in rows:
            lic = r.get("license_requirement") or ""
            by_lic = any(s in lic for s in reverified_strings)
            by_src = r["id"] in source_rows
            if by_lic or by_src:
                basis[r["id"]] = ("licensing+sources" if by_lic and by_src
                                  else "licensing" if by_lic else "sources")
                r["last_verified"] = pass_date
        verified_rows |= set(basis)
        print(f"  Re-verified {len(basis)}/{len(rows)} rows to {pass_date} "
              f"({sum(1 for v in basis.values() if v != 'sources')} via licensing constants, "
              f"{sum(1 for v in basis.values() if v != 'licensing')} via sources).")
        unknown = source_rows - {r["id"] for r in rows}
        assert not unknown, f"re-verified source rows that do not exist: {sorted(unknown)}"
    print(f"  {len(rows) - len(verified_rows)} rows untouched by any pass keep their authoring date.")

    # ---- integrity checks ----
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate row ids: " + str({i for i in ids if ids.count(i) > 1})
    for r in rows:
        assert r["framework"] in frameworks, f"row {r['id']} references unknown framework {r['framework']}"
        assert r["coverage"] in META["coverage_levels"], f"row {r['id']} bad coverage {r['coverage']}"
        assert r["confidence"] in META["confidence_levels"], f"row {r['id']} bad confidence"
        assert r["status"] in ("verified", "UNVERIFIED"), f"row {r['id']} bad status"
        assert r["sources"], f"row {r['id']} has no sources"
        assert (r.get("control_ref") or "").strip(), f"row {r['id']} has empty control_ref"
        # last_verified: well-formed ISO date, and never in the future (PR-051)
        lv = r.get("last_verified") or ""
        assert ISO_DATE.fullmatch(lv), f"row {r['id']} last_verified not an ISO date: {lv!r}"
        try:
            lv_date = datetime.date.fromisoformat(lv)
        except ValueError as exc:
            raise AssertionError(f"row {r['id']} last_verified is not a real date: {lv}") from exc
        assert lv_date <= datetime.date.today(), f"row {r['id']} last_verified is in the future: {lv}"
        # source composition (PR-039). A covered row must cite both the framework authority and
        # Microsoft's own documentation. Boundary rows are exempt from the Microsoft half: a
        # "Not Covered" verdict has no Microsoft capability to cite, which is the point.
        src_hosts = [urlparse(s).netloc for s in r["sources"]]
        assert any(h not in MS_DOC_HOSTS for h in src_hosts), f"row {r['id']} has no official framework source"
        if r["coverage"] != "Not Covered":
            assert any(h in MS_DOC_HOSTS for h in src_hosts), f"row {r['id']} ({r['coverage']}) has no Microsoft source"
        # product dimension
        pid = r.get("product")
        assert pid in PRODUCTS, f"row {r['id']} product not in products map: {pid}"
        prod = PRODUCTS[pid]
        sol = r["purview_solution"]
        assert sol in prod["solutions"] or sol == "None (boundary row)", f"row {r['id']} non-canonical solution: {sol}"
        # also_involves must name real solutions belonging to this row's own product (PR-045/PR-051)
        for extra in r.get("also_involves") or []:
            assert extra in SOLUTIONS, f"row {r['id']} also_involves unknown solution: {extra}"
            assert SOLUTIONS[extra].get("product") == pid, (
                f"row {r['id']} also_involves {extra!r}, which belongs to product "
                f"{SOLUTIONS[extra].get('product')!r}, not {pid!r}")
        # licensing model discriminator (row override allowed; derived default otherwise)
        r.setdefault("licensing_model", "n/a" if r["license_requirement"] == "n/a" else prod["default_licensing_model"])
        assert r["licensing_model"] in LICENSING_MODELS, f"row {r['id']} bad licensing_model"
        # structured dependencies
        assert "related_microsoft" in r and "external_dependencies" in r and "legacy_dependencies" in r, f"row {r['id']} missing dependency fields"
        for dep in r["related_microsoft"]:
            assert dep["product"] in RELATED_PRODUCTS or dep["product"] in PRODUCTS, f"row {r['id']} unknown related product {dep['product']}"
            assert dep["role"] in ("primary", "contributing"), f"row {r['id']} bad dependency role"
            # A row cannot depend on its own product (§11.5 item 3, after the soc2-cc6-6 bug)
            assert dep["product"] != pid, f"row {r['id']} related_microsoft self-references its own product: {pid}"

    # ---- license bands (PR-015) ----
    # Derived AFTER the integrity loop, because G3 cross-checks the band against
    # licensing_model and that field is defaulted in the loop above.
    #
    # This writes two NEW fields. It does not touch license_requirement or
    # licensing_model, which are protected: the band is a derived view of the license
    # string, and the string remains the authority the row renders in full.
    license_bands.check_bands_cover(lic_dicts())                       # G1
    license_bands.check_overrides({r["id"] for r in rows})
    lic_index = license_bands.value_index(lic_dicts())
    for r in rows:
        band, partial = license_bands.derive(r, lic_index)             # G2 + G4 inside
        r["license_band"] = band
        r["license_band_partial"] = partial
        # G3: the two licensing fields must agree about which family the row is in. They
        # are derived from different sources -- licensing_model from the product's
        # default, the band from the row's own license string -- so agreement is a real
        # check rather than a restatement.
        model = r["licensing_model"]
        assert (band == "consumption") == (model == "consumption"), (
            f"row {r['id']}: license_band {band!r} disagrees with licensing_model {model!r} "
            f"about consumption pricing")
        assert (band == "na") == (model == "n/a"), (
            f"row {r['id']}: license_band {band!r} disagrees with licensing_model {model!r} "
            f"about being a boundary row")
    band_counts = collections.Counter(r["license_band"] for r in rows)
    n_partial = sum(1 for r in rows if r["license_band_partial"])
    print("  License bands: "
          + ", ".join(f"{b} {band_counts[b]}" for b in license_bands.BAND_ORDER if band_counts[b])
          + f" | {n_partial} rows flagged partial"
          + f" | {len(license_bands.ROW_OVERRIDES)} row override(s)")

    # ---- maintenance table: structural validation only (PR-050) ----
    # No dates are compared against today here. This block asks only "is the table
    # internally coherent and does every coordinate still resolve", which is what
    # makes an orphaned trigger impossible.
    check_maintenance_table(set(ids))

    # Verification currency, derived from the rows rather than declared by hand (PR-014b).
    # default_last_verified and every row's last_verified are read-only here.
    vdates = sorted(r["last_verified"] for r in rows if r.get("last_verified"))
    verified_range = {"earliest": vdates[0], "latest": vdates[-1]} if vdates else {}

    description = DESCRIPTION.format(tagline=BRAND["tagline"], rows=len(rows),
                                     frameworks=len(frameworks), products=len(PRODUCTS))

    meta = dict(META, verified_range=verified_range, description_meta=description)
    out = {"meta": meta, "products": PRODUCTS, "related_products": RELATED_PRODUCTS,
           "solutions": SOLUTIONS, "frameworks": frameworks, "industries": INDUSTRIES, "rows": rows}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "compliance-atlas.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    logpath = os.path.join(root, "reference", "dependency-migration-log.json")
    with open(logpath, "w", encoding="utf-8") as f:
        json.dump(dep_log, f, indent=1, ensure_ascii=False)
    n_rel = sum(1 for r in rows if r["related_microsoft"])
    n_flag = sum(1 for rec in dep_log if rec["flagged"])
    print(f"Wrote {path}: {len(rows)} rows, {len(frameworks)} frameworks, {len(INDUSTRIES)} industries, {len(PRODUCTS)} product(s)")
    print(f"Dependency migration: {len(dep_log)} rows migrated; {n_rel} rows with related_microsoft entries; {n_flag} rows with flagged (platform-token) external segments -> {logpath}")

    # ---- maintenance warnings (PR-050) ----
    # Deliberately AFTER the write. There is no code path by which a computed
    # staleness value can reach the serializer, because the serializer has already
    # run. Warnings go to stderr so stdout stays the build record; the build exits 0
    # regardless, so an unrelated fix can ship while rows are aging.
    full = "--maintenance-report" in sys.argv
    n = maintenance_report(rows, datetime.date.today(), sys.stderr, limit=10**6 if full else 12)
    if n and "--strict-maintenance" in sys.argv:
        print(f"assemble.py: --strict-maintenance set and {n} maintenance warning(s) present; failing.",
              file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
