"""Stacked-control tier rationales (PR-013).

A "stacked control" is >=2 rows sharing (framework, control_ref); the framework view renders
them as product-tagged cards beneath one control heading. Where their coverage tiers differ, the
badge order can read to a scanner as an inconsistency before the row prose resolves it (the PR-013
exemplar: on CSF PR.PS-04 the product that generates the log records rates below the one that makes
them available). This module holds a short, group-level line explaining WHY those tiers legitimately
differ, rendered above the cards. 22 groups carry one; the rest of the spreads are either
self-explanatory (the namesake product rates highest) or were escalated, not papered over.

SCOPE DISCIPLINE (Session 16, owner-reviewed). A rationale explains ROLE and SCOPE only. It never
restates licensing: the tier legend and license bands own that, so no "per-user", "per-server",
"priced per", or SKU language appears here. Every phrase traces to the member rows' own verified
how_it_supports / capability_detail; no new capability or licensing claim is introduced. A rationale
is NEVER a substitute for fixing a tier: where a spread looked like a possible authoring error it was
recorded as an open finding for a re-verification pass (AUDIT-FINDINGS), not smoothed over here.

WHERE THIS SHIPS. `assemble.py` imports STACK_RATIONALES into `META["stack_rationales"]`, exactly as
it imports `glossary.GLOSSARY` and `license_bands.BAND_DEFS`. One source, so the framework view and
any JSON consumer cannot drift; the page renders from META and holds no copy of the text. Adding the
block is a MINOR (a reader-facing META addition, the shape of 2.10.0's meta.maintenance and 3.3.0's
meta.glossary) -- see CHANGELOG 3.4.0 and AUDIT-FINDINGS.

THE GUARD IS SELF-HONEST. `check_stack_rationales(rows)` fails the build if any key does not resolve
to a real coverage-tier SPREAD group. A rationale therefore cannot outlive its spread: if a future
re-verification collapses a group to a uniform tier, or a control_ref is renamed, the key stops
resolving and the build breaks until the line is removed or moved. It also enforces the house
em-dash-free rule (PR-011 pattern 14) so a later edit cannot quietly reintroduce a dash.

HOUSE-VOICE NOTE: every line ran through /agentic-humanizer before the gate, and ships dash-free.
"""

# framework slug -> control_ref -> one-to-two-sentence tier rationale.
# Keys are byte-exact control refs; order follows the framework display order.
STACK_RATIONALES = {
    "sspa-dpr": {
        "J #38": "Defender for Endpoint rates Direct as the anti-malware engine the requirement runs on across all mandated operating systems. Defender for Cloud rates Partial because it covers a different part of scope, the supplier's cloud and hybrid server estate, deploying that same engine where the endpoint row does not reach.",
    },
    "iso-27001-2022": {
        "A.5.36": "Compliance Manager evidences recurring adherence checking for the Microsoft 365 data-protection control set, so it rates Evidence. The Defender for Cloud dashboard rates Direct because continuous technical compliance review of onboarded cloud resources is the activity this control names, for a complementary scope: a seam, not an overlap.",
        "A.8.15": "Purview generates and protects the audit records for the Microsoft 365 slice, so it rates Partial against a control whose scope is every system. Sentinel rates Direct because estate-wide collection, protection, and analysis across all connected sources is its namesake function, and it consumes the records the Purview row produces.",
        "A.8.7": "Defender for Endpoint rates Direct as the malware prevention and detection engine the control's namesake activity runs on. Intune rates Partial because it manages and enforces that engine's policy rather than being the engine, and Defender for Cloud rates Partial because it extends the control to cloud storage and server workloads the endpoint story does not reach.",
    },
    "soc-2": {
        "CC4.1": "Compliance Manager evidences a functioning ongoing-evaluation mechanism for the Microsoft 365 control set, so it rates Evidence. The Defender for Cloud dashboard supplies one continuous technical input for the cloud slice, so it rates Partial; neither is the entity's full COSO Principle 16 program, and their scopes are complementary.",
        "CC6.8": "Defender for Endpoint rates Direct as the engine that prevents, detects, and responds to malicious software. Intune rates Partial because it supplies the policy and application-control layer on managed endpoints rather than the engine, and Defender for Cloud rates Partial because it extends the control set to server workloads and the cloud-storage introduction path.",
        "CC7.1": "Defender for Cloud rates Direct because misconfiguration detection and vulnerability identification for cloud infrastructure are its namesake activities. Defender for Endpoint rates Partial because it performs the same two checks for the onboarded endpoint estate only: a seam, not an overlap.",
    },
    "hipaa-security": {
        "§164.308(a)(1)(ii)(D)": "Purview produces the Microsoft 365 activity records and the Defender row the security-incident tracking, each a Partial slice of the review. Sentinel rates Direct because continuous review of audit logs, access reports, and incident tracking across the whole ePHI estate, including clinical-system logs the other two defer, is the activity this safeguard names.",
        "§164.308(a)(5)(ii)(B)": "Defender for Endpoint rates Direct as the engine that guards against and detects malicious software on endpoints accessing ePHI. Intune rates Partial because it enforces that the engine runs and stays current rather than performing detection, and Defender for Cloud rates Partial because it extends the same engine to server estates and the cloud-storage upload path.",
    },
    "nist-800-171": {
        "3.3.1": "Purview creates and retains the audit records for the Microsoft 365 enclave, a Partial slice of an all-systems requirement. Sentinel rates Direct because aggregating and retaining logs from the endpoints, servers, and network devices the enclave also spans is its namesake function.",
        "3.12.1, 3.12.3": "Compliance Manager structures and evidences the periodic assessment and monitoring for the Microsoft 365 control slice, so it rates Evidence. The Defender for Cloud dashboard contributes continuous technical assessment for cloud resources in the CUI boundary, so it rates Partial; the full 110-requirement assessment stays the assessor's scope.",
        "3.11.2–3.11.3": "Defender for Cloud rates Direct because scanning cloud systems for vulnerabilities is its namesake activity across the CUI boundary. Defender for Endpoint rates Partial because it covers the onboarded endpoint slice, and non-cloud, non-endpoint components still need their own scanning: a seam, not an overlap.",
    },
    "nist-800-53": {
        "AU-6": "Purview supplies the review and triage surface for Microsoft 365 audit records, a Partial slice. Sentinel rates Direct because continuous, scheduled review and correlation across every connected source is the activity AU-6 names, run at the frequency the control assigns.",
        "AU-11": "Purview provides policy-driven retention for Microsoft 365 audit records, one log source, so it rates Partial. Sentinel rates Direct because organization-defined retention across every source in the workspace, at the multi-year periods federal schedules assign, is its namesake function.",
    },
    "nist-csf-2": {
        "PR.PS-04": "Purview directly generates the Microsoft 365 log records but rates Partial because the subcategory also requires making records available across the whole estate. Sentinel rates Direct on the made-available-for-monitoring half at estate scope, the layer this outcome is only met inside, and it consumes the records the Purview row generates.",
        "DE.CM-09": "Defender for Endpoint rates Direct because monitoring endpoint hardware, software, and runtime is its EDR namesake. Defender for Cloud rates Partial because it adds the cloud-workload and PaaS-runtime equivalents no endpoint agent can see, a different plane rather than the same coverage.",
    },
    "pci-dss-4": {
        "10.5.1": "Purview meets the twelve-month retention bar for in-scope Microsoft 365 service logs, a Partial slice. Sentinel rates Direct because it implements the same retention and three-month hot window for every in-scope source, which for PCI is primarily the CDE systems that sit outside Microsoft 365.",
        "5.3.1, 5.3.5": "Defender for Endpoint rates Direct because automatic currency and tamper protection are engine capabilities it implements. Intune rates Partial because it enforces those same settings by policy on the managed-endpoint slice of scope rather than being the engine; CDE servers are covered separately.",
        "5.2.1–5.2.2": "Defender for Endpoint rates Direct as the detect, remove, and block engine on in-scope workstations and servers. Defender for Cloud rates Partial because it covers the cloud-hosted CDE server components the endpoint row leaves out, deploying that same engine rather than adding a different capability.",
        "11.3.1": "Defender for Cloud rates Direct because continuous internal vulnerability assessment of cloud-hosted CDE components is its namesake activity. Defender for Endpoint rates Partial because agent-based assessment of onboarded components is one input a PCI assessor may still expect to see alongside discrete scan reports for network devices and appliances.",
    },
    "glba-safeguards": {
        "§314.4(c)(8)": "Purview logs and detects misuse of customer information in Microsoft 365, Entra covers the identity slice, and Defender the endpoint and cloud-app slice, so each rates Partial. Sentinel rates Direct because monitoring, logging, and detection across the institution's core banking and application systems, once their logs are forwarded, is where the institution-wide picture exists.",
    },
    "gdpr": {
        "Art. 32(1)(d)": "Each product covers a different plane of the same testing obligation: Compliance Manager evidences the structured assessment program and Sentinel evidences that the detection-and-response measures run, so both rate Evidence, while Defender for Endpoint and the Defender for Cloud dashboard actively assess technical measures on the endpoint and cloud estates, so both rate Partial. None is a complete Article 32 evaluation, which stays the controller's program.",
    },
}

def check_stack_rationales(rows):
    """Structural validation, mirroring check_glossary's guard style. Pure assertions.

    Every (framework, control_ref) key must resolve to a stacked control group that is a
    coverage-tier SPREAD: at least two rows and at least two distinct coverage tiers. This is the
    self-honesty property -- a rationale cannot outlive its spread. Also fails on an empty line or
    any em/en dash (keep rationales dash-free; see module docstring).
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for r in rows:
        groups[(r["framework"], r["control_ref"])].append(r)
    spread = {k for k, mem in groups.items()
              if len(mem) >= 2 and len({m["coverage"] for m in mem}) >= 2}
    seen = 0
    for fw, byref in STACK_RATIONALES.items():
        for ref, text in byref.items():
            assert (fw, ref) in spread, (
                f"stack_rationale ({fw!r}, {ref!r}) is not a coverage-tier spread group; "
                "a rationale cannot outlive its spread -- remove or move it")
            assert text.strip(), f"stack_rationale ({fw!r}, {ref!r}) is empty"
            assert "—" not in text and "–" not in text, (
                f"stack_rationale ({fw!r}, {ref!r}) contains an em/en dash; keep rationales dash-free")
            seen += 1
    return seen
