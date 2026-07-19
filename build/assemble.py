"""Assemble compliance-atlas.json from per-framework row modules.
Run:  python build/assemble.py
Add a framework: create build/rows_<name>.py exposing FRAMEWORK (dict) and ROWS (list), append to MODULES.
Add a product: see README.md "Add a product" — products-map entry in common.py, row modules with
product=<id>, solutions registered in SOLUTIONS and the product's solutions list.

Canonical file renamed 2026-07-17: purview-compliance-map.json -> compliance-atlas.json (platform generalization)."""
import importlib, json, os, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SOLUTIONS, PRODUCTS, RELATED_PRODUCTS, VERIFIED_DATE
from dependency_migration import migrate_row

# Order controls display order in the HTML.
MODULES = ["rows_dpr", "rows_iso", "rows_soc2", "rows_hipaa", "rows_171", "rows_80053", "rows_csf", "rows_pci", "rows_glba", "rows_ferpa", "rows_gdpr"]

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
        "note": "For banks, lenders, insurers, and fintechs under the GLBA Safeguards Rule, with PCI reaching card data and SOC 2 covering service commitments. The stack fits best on continuous vulnerability monitoring, institution-wide audit trails, and extending both to cloud-hosted banking workloads.",
        "note_detail": "SEC 17a-4 / FINRA supervision (strong Records Management + Communication Compliance stories) on v2 backlog. "
                "For the amended Safeguards Rule, Defender Vulnerability Management supplies the §314.4(d)(2) continuous-monitoring alternative to annual pen tests plus biannual vulnerability assessments, a cheaper path for smaller institutions. "
                "Sentinel completes §314.4(c)(8) institution-wide by ingesting the banking/CRM audit trails the workload products cannot see, and carries the PCI Req 10 retention/review story for the CDE. "
                "Defender for Cloud extends the §314.4(d)(2) election to cloud-hosted banking workloads (agentless assessment well beyond the biannual floor) and joins cloud systems to the customer information they hold for §314.4(c)(2)."},
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
    "atlas_version": "2.0.0",
    "as_of": "2026-07-18",
}

FOOTER_LINES = [
    "Informational reference only; not legal, audit, or compliance advice.",
    "Independent community project. Not affiliated with, sponsored, or endorsed by Microsoft Corporation.",
    "Framework and standard names are the property of their respective owners and are used for identification only.",
    "Currency is governed by each row's last-verified date; product capabilities and licensing change frequently, so verify before relying on it.",
]

LICENSING_MODELS = ("per_user", "consumption", "included", "n/a")

META = {
    "title": BRAND["title"],
    "version": BRAND["atlas_version"],
    "brand": BRAND,
    "footer_lines": FOOTER_LINES,
    "generated": None,  # set at assemble time
    "default_last_verified": VERIFIED_DATE,
    "product_scope": list(PRODUCTS.keys()),
    "licensing_models": {
        "per_user": "Licensed per user/SKU (e.g., Microsoft 365 E5-family, Purview Suite add-ons).",
        "consumption": "Usage-based pricing (e.g., ingestion/compute billed via Azure).",
        "included": "Included with a platform entitlement at no separate charge.",
        "n/a": "No license claim (boundary rows).",
    },
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
}

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

    # ---- integrity checks ----
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate row ids: " + str({i for i in ids if ids.count(i) > 1})
    for r in rows:
        assert r["framework"] in frameworks, f"row {r['id']} references unknown framework {r['framework']}"
        assert r["coverage"] in META["coverage_levels"], f"row {r['id']} bad coverage {r['coverage']}"
        assert r["confidence"] in META["confidence_levels"], f"row {r['id']} bad confidence"
        assert r["status"] in ("verified", "UNVERIFIED"), f"row {r['id']} bad status"
        assert r["sources"], f"row {r['id']} has no sources"
        # product dimension
        pid = r.get("product")
        assert pid in PRODUCTS, f"row {r['id']} product not in products map: {pid}"
        prod = PRODUCTS[pid]
        sol = r["purview_solution"]
        assert sol in prod["solutions"] or sol == "None (boundary row)", f"row {r['id']} non-canonical solution: {sol}"
        # licensing model discriminator (row override allowed; derived default otherwise)
        r.setdefault("licensing_model", "n/a" if r["license_requirement"] == "n/a" else prod["default_licensing_model"])
        assert r["licensing_model"] in LICENSING_MODELS, f"row {r['id']} bad licensing_model"
        # structured dependencies
        assert "related_microsoft" in r and "external_dependencies" in r and "legacy_dependencies" in r, f"row {r['id']} missing dependency fields"
        for dep in r["related_microsoft"]:
            assert dep["product"] in RELATED_PRODUCTS or dep["product"] in PRODUCTS, f"row {r['id']} unknown related product {dep['product']}"
            assert dep["role"] in ("primary", "contributing"), f"row {r['id']} bad dependency role"

    meta = dict(META, generated=datetime.datetime.now().isoformat(timespec="seconds"))
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

if __name__ == "__main__":
    main()
