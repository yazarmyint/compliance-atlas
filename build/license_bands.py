"""License-tier banding (PR-015).

Derives a coarse `license_band` (+ `license_band_partial`) per row at build time, so the
reader can ask "what does this framework look like on E3?" — the question both user
stories end on and that the UI could not previously answer.

WHAT THIS IS NOT: it does not replace `license_requirement`. The verbatim entitlement
string stays rendered on every row, and the band is a signpost to it. The band is coarse
by construction and the string is the authority; where they seem to disagree, the string
wins and the mapping below is wrong and should be fixed.

COMMERCIAL LICENSING ONLY. The bands describe Microsoft 365 commercial SKUs. There is no
G3/G5, F-series, or Business Premium dimension — government licensing remains covered by
the per-row GOV notes, and the legend and About page state this limitation where a reader
meets the feature.

Related-product "(if licensed)" mentions (Priva and friends) are OUT of banding scope.
They are pointers to adjacent products, not audited entitlement claims, and they do not
enter the derivation.

---------------------------------------------------------------------------
THE TAXONOMY (five bands, fixed)
---------------------------------------------------------------------------
  e3           included at Microsoft 365 E3 or below
  e5           requires Microsoft 365 E5 or the relevant E5 step-up
  addon        requires an add-on or standalone SKU (E5 Compliance, E5 Security,
               Intune Suite, per-product standalone licenses)
  consumption  consumption/meter-billed (Sentinel, Defender for Cloud); no seat tier
  na           the `licensing_model: "n/a"` boundary rows

Ordering applies to the SEAT bands only: e3 < e5 < addon. `consumption` and `na` sit
outside the ordering and are never compared against it (rule F6).

---------------------------------------------------------------------------
FLOOR-DETERMINATION RULES
---------------------------------------------------------------------------
The band is the LOWEST tier at which any mapped capability functions; `partial` then
flags that something at that tier is reduced. A row is never promoted to a higher band
just because part of it needs more — that would hide the capability the reader can
actually reach — and never left un-flagged when part of it is out of reach.

  F1  Within a constant, "or" routes take the MINIMUM and do NOT set partial.
      Alternative routes to the same capability are doors to one room.
      "E5 or E5 Compliance add-on" -> e5, partial false.

  F2  Within a constant, a capability SPLIT takes the minimum and DOES set partial.
      "X at tier A; advanced/premium Y requires tier B" -> A, partial true.

  F3  Across constants in one row: band = min(bands), partial = any(partials) OR
      (the bands are not all equal). A row citing audit_std (e3) and audit_prem (e5)
      bands e3/partial — something works at E3, not everything.

  F4  An "additionally requires X" clause sets partial ONLY IF X is not already
      satisfied at the floor band. Entra ID P1 is included in E3, so "additionally
      requires Entra ID P1" reduces nothing at an e3 or e5 floor.

  F5  A reduction BELOW the floor band never sets partial. There is no band under e3,
      and badging "reduced at this tier" would assert something false about E3.

  F6  consumption and na never mix with seat bands. Verified continuously by G3 and by
      the assertion in derive(): no row cites both families.

  F7  "Functions" means READER-USABLE CAPABILITY. Background processing with no
      reachable interface does not band. (Owner decision, Session 10, escalation E1.)

TAXONOMY RULE — partial is NOT permitted in the consumption band. "Reduced capability at
this tier" is meaningless where the band asserts that no seat tier exists. Free-vs-paid
and grant-vs-metered nuances are real, but they live in the verbatim string, not in a
badge that would imply a tier relationship the product does not have. Enforced by
assertion in derive(). (Owner decision, Session 10, escalation E5.)
"""

# ---------------------------------------------------------------------------
# The six licensing dicts this derivation reads, by name. Kept as a tuple rather than
# discovered dynamically so that adding a licensing dict to common.py is a deliberate,
# reviewed act here rather than something that silently widens the derivation.
# ---------------------------------------------------------------------------
LIC_DICT_NAMES = ("LIC", "ENTRA_LIC", "INTUNE_LIC", "DEFENDER_LIC", "SENTINEL_LIC", "MDC_LIC")

SEAT_ORDER = {"e3": 0, "e5": 1, "addon": 2}
BAND_ORDER = ("e3", "e5", "addon", "consumption", "na")

# ---------------------------------------------------------------------------
# THE MAPPING. (dict_name, key) -> (band, partial)
#
# One entry per licensing constant, 49 of them. This is the reviewed table: it is keyed
# on the CONSTANT COORDINATE, not on the 110 distinct prose strings those constants
# compose into, and not on substring heuristics over prose that could silently
# misclassify a future string. Each entry cites the constant's own text.
#
# Adding a licensing constant to common.py without adding it here FAILS THE BUILD (G1).
# ---------------------------------------------------------------------------
BANDS = {
    # ---- Purview -----------------------------------------------------------
    # "E5/A5/G5/E3/A3/G3/F1/F3 or Business Premium" — E3 named directly.
    ("LIC", "labels_manual"): ("e3", False),
    # E5/A5/G5 + Office 365 E5/A5 + Suite routes. No E3 path.
    ("LIC", "labels_auto"): ("e5", False),
    # "manual E3+; automatic application E5-tier" — F2 split.
    ("LIC", "label_encryption"): ("e3", True),
    ("LIC", "customer_key"): ("e5", False),
    # F7. "E3/A3/G3 tenants keep the underlying Content explorer data aggregation
    # WITHOUT THE EXPLORER INTERFACES" — the mapped capability is the explorers, and at
    # E3 the reader cannot open any of them. Aggregation the reader cannot reach is not
    # a functioning capability, so this bands e5 rather than e3+partial.
    ("LIC", "classification_analytics"): ("e5", False),
    # "E5/A5/G5/E3/A3/G3 or Business Premium" — E3 named directly.
    ("LIC", "dlp_core"): ("e3", False),
    ("LIC", "dlp_teams"): ("e5", False),
    # "no Office 365 path; Endpoint DLP is Microsoft 365 only".
    ("LIC", "dlp_endpoint"): ("e5", False),
    ("LIC", "retention_basic"): ("e3", False),
    ("LIC", "retention_advanced"): ("e5", False),
    ("LIC", "records"): ("e5", False),
    # "included across Microsoft 365/Office 365 enterprise, government, and business plans".
    ("LIC", "audit_std"): ("e3", False),
    # "10-year retention needs the add-on license" — F2 split above an e5 floor.
    ("LIC", "audit_prem"): ("e5", True),
    # "Microsoft 365 E3 or Office 365 E3/A3/G3/F3; premium features ... E5" — F2 split.
    ("LIC", "ediscovery_std"): ("e3", True),
    ("LIC", "irm"): ("e5", False),
    ("LIC", "cc"): ("e5", False),
    # "E5/A5/G5, Purview Suite, or E5 Insider Risk Management add-on" — F1, floor e5.
    ("LIC", "ib"): ("e5", False),
    # "baseline included with Microsoft 365/Office 365 plans; premium regulation
    # templates licensed separately" — F2 split at an e3 floor.
    ("LIC", "cm"): ("e3", True),
    ("LIC", "dspm"): ("e5", False),
    # "M365 E5 or Purview Suite; monitored Copilot users need Microsoft 365 Copilot
    # licenses; some non-M365 sources are pay-as-you-go" — an e5 floor that carries both
    # a further per-seat license and consumption meters. partial, not a band change:
    # the seat floor is real and the extras are qualifications on top of it.
    ("LIC", "dspm_ai"): ("e5", True),

    # ---- Entra -------------------------------------------------------------
    # "P1 (included in Microsoft 365 E3/E5/E7 ...). Risk-based conditions additionally
    # require Entra ID P2" — F2 split: base CA at E3, risk conditions at E5.
    ("ENTRA_LIC", "ca"): ("e3", True),
    # "Entra ID Free (basic) and P1; authentication strengths ... require P1". P1 is
    # included in E3, so the capability is whole at the floor. The reduction is at Free,
    # which is below the band — F5, no partial.
    ("ENTRA_LIC", "mfa"): ("e3", False),
    ("ENTRA_LIC", "id_protection"): ("e5", False),
    # "P2 or the Entra ID Governance SKU" — F1; P2 is included in E5, so floor e5.
    ("ENTRA_LIC", "pim"): ("e5", False),
    # "baseline ...: P2; advanced governance requires the Governance SKU or Entra
    # Suite" — F2 split above an e5 floor.
    ("ENTRA_LIC", "gov_core"): ("e5", True),
    # "Governance SKU or Entra Suite (NOT INCLUDED IN STANDALONE ENTRA ID P2)". No E5
    # route exists, so this is the atlas's one genuine addon-band constant. Do not fold
    # it into e5 to tidy the distribution — an E5 reader does not have this.
    ("ENTRA_LIC", "gov_lcw"): ("addon", False),
    # "Included with Microsoft Entra ID Free (all Microsoft cloud subscriptions)".
    ("ENTRA_LIC", "free"): ("e3", False),

    # ---- Intune ------------------------------------------------------------
    # "included in Microsoft 365 bundles such as E3/E5/E7 and EMS E3/E5".
    ("INTUNE_LIC", "p1"): ("e3", False),
    # Intune P1 + Entra ID P1. Both are present at E3, so nothing is reduced there — F4.
    ("INTUNE_LIC", "p1_ca"): ("e3", False),
    # "included in Microsoft 365 E5 and E7 since July 2026 ...; on any other plan it
    # remains a separate Intune add-on license or the Intune Suite" — F1: e5 and addon
    # are two routes, floor is e5.
    ("INTUNE_LIC", "epm"): ("e5", False),

    # ---- Defender ----------------------------------------------------------
    # "included in Microsoft 365 E3/A3/G3 ... EDR, automated investigation & remediation,
    # vulnerability management, and threat analytics require Plan 2" — F2 split.
    ("DEFENDER_LIC", "mde_p1"): ("e3", True),
    ("DEFENDER_LIC", "mde_p2"): ("e5", False),
    # "core capabilities: included with MDE Plan 2 ...; premium capabilities (security
    # baselines assessment, block vulnerable applications, ...) require the MDVM add-on".
    ("DEFENDER_LIC", "mdvm"): ("e5", True),
    # OWNER DECISION, Session 10 escalation E2. "Effective July 1, 2026 it is also
    # included in Microsoft 365 E3/G3 and Office 365 E3/G3; that rollout began June 2026
    # and Microsoft expects it to complete DURING 2026." The effective date has passed,
    # so E3 is the honest floor — but the rollout is incomplete, so an E3 tenant may not
    # have it yet, which is what the partial flag records.
    #
    # THIS PAIR IS A HARD-CODED LITERAL AND MUST STAY ONE. Deriving it by comparing the
    # effective date against today's date would make the band move on a calendar
    # boundary with no commit behind it, breaking the strict empty-diff drift check
    # (AUDIT-FINDINGS SS27.1). The re-check is scheduled, not computed: see
    # TRG-MDO-P1-E3G3, which owns dropping this partial flag when the rollout completes.
    ("DEFENDER_LIC", "mdo_p1"): ("e3", True),
    ("DEFENDER_LIC", "mdo_p2"): ("e5", False),
    ("DEFENDER_LIC", "mdi"): ("e5", False),
    # "Conditional Access App Control additionally requires Entra ID P1" — P1 is
    # included well below the e5 floor, so nothing is reduced at the band. F4.
    ("DEFENDER_LIC", "mdca"): ("e5", False),
    # "no separate license; comes with any qualifying workload license (M365 E5/A5;
    # M365 E3 WITH the Defender Suite or EMS E5 add-on; ...)". E3 alone does not
    # qualify; E5 qualifies unaided. F1 takes the lowest tier that qualifies without a
    # further purchase, so e5, and the add-on route does not make this addon-band.
    ("DEFENDER_LIC", "xdr"): ("e5", False),

    # ---- Sentinel — consumption-priced throughout, no seat tier exists ------
    ("SENTINEL_LIC", "ingest"): ("consumption", False),
    ("SENTINEL_LIC", "retention"): ("consumption", False),
    # The E5 data grant (5 MB/user/day) is a real seat-tier effect on the BILL, but not
    # on capability, and the taxonomy rule forbids partial in this band. The grant stays
    # described in the verbatim string. (Session 10, escalation E5.)
    ("SENTINEL_LIC", "free_benefit"): ("consumption", False),
    ("SENTINEL_LIC", "soar"): ("consumption", False),
    ("SENTINEL_LIC", "included"): ("consumption", False),

    # ---- Defender for Cloud — consumption-priced throughout -----------------
    ("MDC_LIC", "foundational"): ("consumption", False),
    ("MDC_LIC", "cspm"): ("consumption", False),
    ("MDC_LIC", "servers_p1"): ("consumption", False),
    ("MDC_LIC", "servers_p2"): ("consumption", False),
    ("MDC_LIC", "workload"): ("consumption", False),
    # "MCSB assessment included free; assigning additional standards requires at least
    # one paid plan" — free-vs-paid, not tier-vs-tier. No partial in this band.
    ("MDC_LIC", "dashboard"): ("consumption", False),
}

# ---------------------------------------------------------------------------
# ROW OVERRIDES. row id -> (band | None, partial | None, reason)
#
# The escape hatch for rows whose license_requirement carries a tier claim in PROSE that
# no constant covers. `None` means "leave the derived value alone", so an override can
# adjust the partial flag without silently restating a band.
#
# A reason string is REQUIRED and is asserted non-empty: an override is a documented
# exception to a mechanical rule, and one without a stated basis is indistinguishable
# from a mistake. This table is also G4's acknowledged-override list — a row may carry
# un-constanted tier prose only if it appears here.
#
# Keep this table SMALL. If it grows, the right fix is usually to move the claim into a
# licensing constant where the maintenance triggers can see it, not to add entries here.
# ---------------------------------------------------------------------------
ROW_OVERRIDES = {
    "iso-a-5-10": (None, True,
                   "String appends 'advanced policy tips: E5-tier (service description)' after "
                   "LIC['labels_manual'] (e3, no partial). The E5 caveat is row prose that no "
                   "constant covers, so the derived partial=False would drop a stated tier claim. "
                   "Band stays e3; partial forced true."),
    "53-ac-21": (None, True,
                 "String appends 'advanced policy tips: E5-tier (service description)' after "
                 "LIC['dlp_core'] (e3, no partial). Same case as iso-a-5-10: the E5 caveat lives "
                 "in row prose, not in a constant. Band stays e3; partial forced true."),
}

# Tier tokens that must not appear in a row's residual prose — the text left over once
# every licensing constant is removed — unless the row is an acknowledged override.
# This is G4: it catches an author writing "requires E5" into a row instead of into a
# constant, which is the one way a constant-keyed mapping can silently under-report.
import re

TIER_TOKEN = re.compile(
    r"\b(?:E[357]|A[35]|G[35]|F[135]|P[12])\b"
    r"|\bPlan [12]\b"
    r"|\badd-on\b"
    r"|\bBusiness Premium\b",
    re.IGNORECASE,
)


def value_index(dicts):
    """constant value -> (dict_name, key), for substring resolution against a row string.

    Asserts the two properties that make substring matching sound: values are unique,
    and no value is a substring of another. Both hold today; a future constant that
    breaks either would make resolution ambiguous, and this fails the build rather than
    quietly banding a row off the wrong constant.
    """
    index = {}
    for dict_name in LIC_DICT_NAMES:
        for key, value in dicts[dict_name].items():
            assert value not in index, (
                f"licensing constant value is duplicated across coordinates: "
                f"{dict_name}[{key!r}] repeats {index[value][0]}[{index[value][1]!r}]")
            index[value] = (dict_name, key)
    values = sorted(index, key=len, reverse=True)
    for i, outer in enumerate(values):
        for inner in values[i + 1:]:
            assert inner not in outer, (
                f"licensing constant {index[inner]} is a substring of {index[outer]}; "
                f"substring resolution can no longer tell them apart")
    return index


def check_bands_cover(dicts):
    """G1: every licensing constant has a band. Fails when a constant is ADDED.

    Deliberately keyed on the constant rather than on rows, so it fires at the earliest
    possible point — when the constant appears in common.py, before any row uses it —
    rather than waiting for a row to pick it up.
    """
    coords = {(d, k) for d in LIC_DICT_NAMES for k in dicts[d]}
    missing = coords - set(BANDS)
    assert not missing, (
        "licensing constants with no BAND_MAP entry (add them to build/license_bands.py "
        f"BANDS, citing the string's own text): {sorted(missing)}")
    extra = set(BANDS) - coords
    assert not extra, f"BAND_MAP entries for constants that no longer exist: {sorted(extra)}"
    for coord, (band, partial) in BANDS.items():
        assert band in BAND_ORDER, f"BAND_MAP {coord} has unknown band {band!r}"
        assert isinstance(partial, bool), f"BAND_MAP {coord} partial is not a bool"
        assert not (band == "consumption" and partial), (
            f"BAND_MAP {coord}: partial is not permitted in the consumption band "
            f"(taxonomy rule, Session 10 escalation E5)")


def check_overrides(row_ids):
    """Structural validation of ROW_OVERRIDES: real rows, stated reasons, real effect."""
    unknown = set(ROW_OVERRIDES) - set(row_ids)
    assert not unknown, f"ROW_OVERRIDES names rows that do not exist: {sorted(unknown)}"
    for rid, (band, partial, reason) in ROW_OVERRIDES.items():
        assert band is None or band in BAND_ORDER, f"ROW_OVERRIDES[{rid!r}] bad band {band!r}"
        assert partial is None or isinstance(partial, bool), f"ROW_OVERRIDES[{rid!r}] bad partial"
        assert not (band is None and partial is None), (
            f"ROW_OVERRIDES[{rid!r}] overrides nothing; remove the entry")
        assert reason and reason.strip(), (
            f"ROW_OVERRIDES[{rid!r}] has no stated reason. An override is a documented "
            f"exception to a mechanical rule; one without a basis is indistinguishable "
            f"from a mistake.")
        assert not (band == "consumption" and partial), (
            f"ROW_OVERRIDES[{rid!r}]: partial is not permitted in the consumption band")


def derive(row, index):
    """Return (band, partial) for one row. Pure function of committed content.

    Nothing here reads the clock, the filesystem, or the network, and the fold is
    order-independent (min over a total order, any over booleans). Two identical
    checkouts produce identical bands — which is what keeps the strict empty-diff drift
    check from Session 9 meaningful.
    """
    text = row.get("license_requirement") or ""
    coords = sorted({coord for value, coord in index.items() if value in text})

    if not coords:
        # G2: the only string legitimately carrying no licensing constant is the
        # boundary-row literal. Anything else is free-prose licensing that the mapping
        # cannot see, and banding it would mean inventing a default — the silent
        # misclassification this whole design exists to prevent.
        assert text.strip() == "n/a", (
            f"row {row['id']}: license_requirement matches no licensing constant and is not "
            f"the boundary literal 'n/a'. Either compose it from a constant in common.py, or "
            f"— if it is genuinely a boundary row — set it to 'n/a'. Got: {text[:120]!r}")
        band, partial = "na", False
    else:
        pairs = [BANDS[c] for c in coords]
        seat = [b for b, _ in pairs if b in SEAT_ORDER]
        other = [b for b, _ in pairs if b not in SEAT_ORDER]
        # F6: the two families never mix. Verified across all 378 rows; asserted so a
        # future row that mixed them would fail loudly rather than band off whichever
        # family happened to sort first.
        assert not (seat and other), (
            f"row {row['id']} cites both seat-tier and non-seat licensing constants "
            f"({sorted(coords)}); rule F6 says these families do not mix, so the floor is "
            f"undefined. Resolve by splitting the row or by re-banding a constant.")
        if seat:
            band = min(seat, key=lambda b: SEAT_ORDER[b])
            # F3: partial if any constituent is itself partial, OR if the constituents
            # sit at different tiers (something works at the floor, not everything).
            partial = any(p for _, p in pairs) or len(set(seat)) > 1
        else:
            band = other[0]
            assert len(set(other)) == 1, (
                f"row {row['id']} cites conflicting non-seat bands {sorted(set(other))}")
            partial = any(p for _, p in pairs)

    # G4: tier prose outside any constant. Checked before overrides are applied, so an
    # override is what SILENCES it — that is the whole point of the acknowledged list.
    residual = text
    for value, coord in index.items():
        if value in residual:
            residual = residual.replace(value, " ")
    hit = TIER_TOKEN.search(residual)
    assert not hit or row["id"] in ROW_OVERRIDES, (
        f"row {row['id']}: license_requirement carries the tier token {hit.group(0)!r} in prose "
        f"outside any licensing constant, so the derived band cannot see it. Residual text: "
        f"{residual.strip()[:160]!r}. Either move the claim into a constant in common.py, or add "
        f"an entry to ROW_OVERRIDES with a stated reason.")

    if row["id"] in ROW_OVERRIDES:
        ob, op, _reason = ROW_OVERRIDES[row["id"]]
        if ob is not None:
            band = ob
        if op is not None:
            partial = op

    assert not (band == "consumption" and partial), (
        f"row {row['id']} derived consumption+partial, which the taxonomy forbids")
    return band, partial


# Reader-facing definitions, serialized into meta so the legend and the About page are
# generated from the same source as the derivation rather than restating it in the
# template (where the two could drift apart).
BAND_DEFS = {
    "e3": "Included at Microsoft 365 E3 or below.",
    "e5": "Requires Microsoft 365 E5 or the relevant E5 step-up.",
    "addon": "Requires an add-on or standalone SKU beyond the base seat license.",
    "consumption": "Consumption/meter-billed (Sentinel, Defender for Cloud). No seat tier applies.",
    "na": "No license claim — boundary rows, where the verdict is that the product does not cover the control.",
}

BAND_PARTIAL_DEF = ("Reduced capability at this tier — the band is the lowest tier where something "
                    "mapped here works, and part of the mapping needs a higher tier. Read the license "
                    "requirement on the row for what is and is not included.")

BAND_SCOPE_NOTE = ("Bands describe Microsoft 365 COMMERCIAL licensing only: there is no G3/G5, F-series, "
                   "or Business Premium dimension, and government licensing is covered by the per-row "
                   "cloud availability notes instead. Consumption-priced products (Microsoft Sentinel, "
                   "Defender for Cloud) have no seat tier at all, so they appear under every tier filter "
                   "unless you exclude them with the No seat tier toggle — which is what the \"+n\" on each "
                   "tier button counts: rows at that tier, plus rows that have no tier at all. The band is derived from each "
                   "row's license requirement and is a coarse signpost to it, never a replacement — the "
                   "full entitlement string stays on every row. Related-product mentions marked "
                   "\"(if licensed)\" are pointers to adjacent products, not banded or audited claims.")
