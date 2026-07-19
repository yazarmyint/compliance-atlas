"""Mechanical migration of free-text `non_purview_dependencies` into the structured
dependency model (platform generalization, 2026-07-17).

Rules — deterministic, no interpretation:
- Split the original string on ';' into segments (the atlas's consistent delimiter).
- A segment naming one of five unambiguous Microsoft product families becomes a
  related_microsoft entry: {product, solution: None, role, note: <segment verbatim>}.
  Token rules (case-sensitive substrings, chosen from the actual corpus):
      "Entra"    -> entra          "Intune"  -> intune       "Defender" -> defender-xdr
      "Sentinel" -> sentinel       "Priva"   -> priva
  A segment naming two products yields one entry per product (same verbatim note).
- role = "primary" if the segment contains "primary", else "contributing".
- Segments with no product token move verbatim to external_dependencies.
- Zero information loss by construction: every segment appears verbatim in either
  external_dependencies or a related_microsoft note, and the full original string is
  preserved in legacy_dependencies.
- Ambiguity policy (per brief): Microsoft-adjacent platform/feature mentions that are
  NOT one of the five product families (BitLocker, Azure Key Vault, SharePoint/SPO,
  Teams, M365 platform, Microsoft 365 Backup, generic "Microsoft") are deliberately
  LEFT IN external_dependencies and flagged for the audit log — never guessed into a
  product assignment. Generic "SIEM"/"SOAR" without "Sentinel" stays external (tooling
  category, not a product claim).
"""

PRODUCT_TOKENS = [
    ("Entra", "entra"),
    ("Intune", "intune"),
    ("Defender", "defender-xdr"),
    ("Sentinel", "sentinel"),
    ("Priva", "priva"),
]

# Platform/feature tokens that are Microsoft-adjacent but deliberately not parsed.
AMBIGUOUS_TOKENS = ["BitLocker", "Azure Key Vault", "SharePoint", "SPO/", "SPO ", "Teams",
                    "M365", "Microsoft 365", "Microsoft datacenter", "Microsoft-managed", "Microsoft)"]


def migrate_dependency_string(original: str):
    """Return (related_microsoft, external_dependencies, flagged_segments)."""
    related, external, flagged = [], [], []
    segments = [s.strip() for s in original.split(";") if s.strip()]
    for seg in segments:
        hits = [slug for tok, slug in PRODUCT_TOKENS if tok in seg]
        role = "primary" if "primary" in seg.lower() else "contributing"
        if hits:
            for slug in dict.fromkeys(hits):  # de-dupe, keep order
                related.append({"product": slug, "solution": None, "role": role, "note": seg})
        else:
            external.append(seg)
            if any(tok in seg for tok in AMBIGUOUS_TOKENS):
                flagged.append(seg)
    return related, "; ".join(external), flagged


def migrate_row(row: dict):
    """Mutate a row in place: non_purview_dependencies -> structured model.
    Returns a log record for the audit trail. Rows already authored with the
    structured fields (future products) pass through untouched."""
    if "related_microsoft" in row and "non_purview_dependencies" not in row:
        return None
    original = row.pop("non_purview_dependencies", "")
    related, external, flagged = migrate_dependency_string(original)
    row["related_microsoft"] = related
    row["external_dependencies"] = external
    row["legacy_dependencies"] = original
    return {"id": row["id"], "original": original, "related": related,
            "external": external, "flagged": flagged}
