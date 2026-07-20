# Maintenance

Dated triggers worth diarising — licensing restructures, product retirements, framework version
refreshes, and naming churn — plus the framework backlog. Several entries encode verification dates
and pending re-checks that later sessions depend on; keep their wording intact when acting on them.

## Maintenance triggers worth diarising

- **Nov 10, 2026**: CMMC Phase 2: C3PAO Level 2 certifications required in new applicable DoD contracts.
- **~Jul 2027**: HIPAA Security Rule final rule target (per OMB agenda); rows flag proposed changes as direction-of-travel.
- **Annual (~Q1)**: SSPA DPR version refresh (v12 → v13 likely early 2027); requirement numbering can shift.
- Microsoft renames: check the Purview service description and solution overview pages; the atlas already reflects the
  unified eDiscovery (classic retired Aug 2025), Data explorer, DSPM current version, and "Microsoft Purview Suite" SKU naming.
- **When the classic DSPM pages retire, re-evaluate the `dspm` / `dspm_ai` constant split.** Both
  `/purview/dspm-for-ai` and `/purview/data-security-posture-management` now carry "(classic)" banners pointing at the
  unified `data-security-posture-management-learn-about` article. As of 2026-07-20 the split is still correct: the
  portal shows **DSPM** and **DSPM for AI (classic)** as separate solutions with separate entitlements, so
  `LIC["dspm"]`/`LIC["dspm_ai"]`, `GOV["dspm_ai"]`, and the two `SOLUTIONS` entries all describe real distinctions.
  `URLS["dspm_ai"]` is already gone — the two rows that cited the classic article were repointed to the unified one
  (AUDIT-FINDINGS §23). **The trigger:** once the classic solutions leave the portal, collapse `dspm_ai` into `dspm`,
  fold `GOV["dspm_ai"]` into the unified GCC High note, and drop the "(classic; converging into DSPM)" gloss from
  `SOLUTIONS["DSPM for AI"]`. That is a row-modeling change (`purview_solution` on `csf-de-cm-03-ai` and the
  `also_involves` entry on `gdpr-35`), so it needs a session authorized to touch protected fields.
- **Intune licensing restructure (July 2026 — in effect, documentation still catching up)**: Suite capabilities are now
  distributed into Microsoft 365 tiers (E3: Plan 2 + Remote Help + Advanced Analytics; E5/E7: adds EPM, Cloud PKI, EAM).
  Confirmed live 2026-07-20 and `INTUNE_LIC["epm"]` was rewritten to the present tense. **Still pending:** the
  restructure is stated in exactly one Learn location, the [planning guide](https://learn.microsoft.com/intune/fundamentals/planning-guide)
  step 3. The canonical [Intune licensing article](https://learn.microsoft.com/intune/fundamentals/licensing) was
  rewritten to drop per-bundle contents entirely (it now names only Plan 1 / Plan 2 / Suite and defers to the commercial
  pricing page), and `fundamentals/advanced-capabilities` says only "select Microsoft 365 bundles" without naming them.
  Re-check both once they carry the mapping again; until then the planning guide is the sole first-party citation for
  which tier includes EPM. Note also the article moved from `fundamentals/licenses` to `fundamentals/licensing`.
- Intune docs migrated to `learn.microsoft.com/intune/*` (off `/mem/intune`). *(The forward `defender-xdr` links on
  Intune/Entra rows were reconciled when Defender XDR landed; see AUDIT-FINDINGS §13.4.)*
- **MDO Plan 1 in E3/G3 (effective July 1, 2026)**: encoded in `DEFENDER_LIC["mdo_p1"]`. Confirmed live 2026-07-19:
  rollout began June 2026 and Microsoft expects completion during 2026, but the Defender service description's MDO
  Plan 1 SKU list does **not** yet name E3/G3. Re-check that list once the rollout completes and drop the dated
  qualifier from the string when the service description catches up.
- **Microsoft Defender Suite naming**: the SKU formerly called Microsoft 365 E5 Security is now **Microsoft Defender
  Suite**, with EDU/GOV/FLW variants plus Microsoft Defender + Purview Suite FLW. All six `DEFENDER_LIC` strings were
  re-derived 2026-07-19 and carry the "(formerly Microsoft 365 E5 Security)" gloss so holders of older paperwork still
  recognize it. Drop the gloss once the old name has fully left circulation.
- **MDVM add-on in GCC High/DoD**: the add-on trial is unavailable there; confirm purchase availability for gov
  tenants before relying on MDVM-premium capabilities in CMMC assessments.
- Defender family renames are frequent (MTP → M365 Defender → Defender XDR; MCAS → Defender for Cloud Apps); re-check
  `PRODUCTS["defender-xdr"]` naming and the four workload names at each maintenance pass.
- **Mar 31, 2027: Microsoft Sentinel Azure-portal retirement** (extended from Jul 1, 2026; announced Feb 12, 2026).
  After this date Sentinel is Defender-portal only; the atlas already describes the Defender-portal experience.
- **Dec 31, 2026 / Mar 31, 2027: Sentinel 50 GB commitment tier promo**: launched Oct 1, 2025 in public preview;
  promotional pricing extended twice and now runs through **Dec 31, 2026**, with sign-ups in that window locking the
  discounted rate through **Mar 31, 2027** (Partner Center announcement, Jun 26, 2026; re-verified 2026-07-19).
  Encoded in `SENTINEL_LIC["ingest"]`. Two things to check at the next pass: whether the tier reaches GA, and whether
  the promo is extended a third time. Note the billing article still describes commitment tiers as starting at
  100 GB/day, so the 50 GB tier is documented only in the promo announcement and the pricing page.
- **Sentinel data lake meters**: ingestion, processing, storage (6:1 compression), and query are encoded in
  `SENTINEL_LIC["retention"]`. Two further meters exist on the billing article and are **not** modelled in any row,
  deliberately, because no current row makes a claim that rests on them: **advanced data insights** (per compute hour
  for notebook sessions/jobs and custom-graph node/edge building; pools of 12/32/80 vCores) and the **Sentinel graph**
  meters (custom graph build/query per compute hour; embedded graphs in the Defender and Purview portals are free,
  but MCP graph tool access is charged). Revisit if a row ever claims notebook or graph capability.
- **Sentinel E5/E7 data grant**: 5 MB/user/day, eligible SKUs incl. E7, verified 2026-07-18 on the offer page;
  re-check annually. *(Not re-verified in the 2026-07-19 pass — the offer page was not fetched; see AUDIT-FINDINGS §22.)*
- **Sentinel in China (21Vianet) retires Aug 18, 2026**: irrelevant to US-focused rows; noted for completeness.
- **Defender for Cloud in China (21Vianet) retires Oct 1, 2026**: likewise noted for completeness only.
- **Defender for Cloud is migrating experiences into the Defender portal**: rows describe capabilities, not portal
  location; re-check the portal-pivot state (support matrix "Defender portal" column) at each maintenance pass.
- **Regulatory compliance dashboard standards catalog churns**: the built-in list tracks current publications
  (e.g., it now offers NIST 800-171 **R3** while the atlas pins R2, noted on `171-3-12-1-3-mdc`); re-verify the
  standards named in dashboard rows and the paid-plan gate (any plan except Servers P1/APIs P1) at each pass.
- **Defender for Servers / CSPM feature boundaries move**: re-verify the free-vs-paid CSPM split, the Servers P2
  inclusion list (premium MDVM, FIM, JIT, 500 MB/day ingestion benefit), and the Azure Government gap list (CIEM,
  Data & AI dashboard, APIs/App Service/AI Services plans absent as of 2026-07-18).
Backlog (documented in FRAMEWORK-SELECTION.md): US state-privacy composite (CPRA-anchored),
SEC 17a-4/FINRA (strong RM + Communication Compliance stories), NIS2/DORA. *(FERPA and the 800-53 subset shipped in Increment 1.)*
**Product roadmap: complete.** Defender for Cloud shipped 2026-07-18 as product #6, the final planned product
(§15). *(Entra #2, Intune #3, Defender XDR #4 all 2026-07-17; Sentinel #5 2026-07-18.)* The five Defender-for-Cloud
free-text entry points (PCI 5.2 / DPR J #38 / A.5.23 / A.8.8 / ID.RA-01) all gained stacked rows at their exact
control refs (§15). The only remaining `RELATED_PRODUCTS` slug is **priva** (11 contributing links on privacy rows),
deliberately kept as a permanent reference-only product, never to be authored (§15). Next: a whole-atlas
consistency pass, then publishing.
