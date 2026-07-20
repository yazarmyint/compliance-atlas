# Maintenance

Dated triggers worth diarising — licensing restructures, product retirements, framework version
refreshes, and naming churn — plus the framework backlog.

## The trigger table

**Triggers are defined in one place: `build/common.py` → `MAINTENANCE`.** They ship in the dataset at
`meta.maintenance.triggers`, and the build evaluates them on every run. This document does not list
them, because two copies of a trigger list drift — which is exactly the defect this mechanism was
built to fix (PROJECT-REVIEW PR-050).

To see what is due:

```powershell
python build/assemble.py                       # warnings print to stderr; build still exits 0
python build/assemble.py --maintenance-report  # same, without the 12-item display cap
python build/assemble.py --strict-maintenance  # exit 1 if anything is due (opt-in, for CI)
```

Warnings are **advisory**. The build succeeds with them present, so an unrelated fix can ship while
rows are aging. Four prefixes, each pointing at a section of the runbook below:

| Prefix | Means | Where it comes from |
|---|---|---|
| `TRIGGER` | A trigger is past its `next_review` date | `MAINTENANCE[].next_review` |
| `STALE` | A licensing constant is past its class cadence | the constant's re-verification pass date vs `STALENESS_CLASSES` |
| `NAMING` | A retired product name appears un-glossed | `RETIRED_NAMES`, no clock involved |
| summary | Counts, and the strict-mode hint | — |

`STALE` warns per **constant**, not per row. A row's `last_verified` is derived from the licensing
constants it rests on (`assemble.py`, re-verification passes), so the constant is the unit of work:
49 of them govern 370 of the 378 rows. The other 8 are the `licensing_model: "n/a"` boundary rows,
which carry no licensing claim and are named individually under the `boundary` class.

### Volatility classes

| Class | Constants | Cadence | Why |
|---|---|---|---|
| `consumption` | `SENTINEL_LIC`, `MDC_LIC` | 90 d | Meters and promo windows move on Azure pricing-page cadence. Both PR-036 misses were here. |
| `sku-volatile` | `DEFENDER_LIC`, `ENTRA_LIC`, `INTUNE_LIC` | 120 d | The rename-prone SKU families; PR-035 landed here. |
| `sku-stable` | `LIC` (Purview) | 180 d | One authoritative source on one publisher cadence. See the note in `STALENESS_CLASSES` on why §22.2's apparent volatility was mostly a one-time systemic fix. |
| `boundary` | — (the 8 `n/a` rows) | 365 d | A `Not Covered` verdict rests on framework text, so it ages at framework speed. |

Trigger `type` carries its own cadence (`TYPE_CADENCE`): `licensing` 90 d, `naming` 120 d,
`framework` 365 d, `sovereign` 180 d, `watch` 365 d, and `retirement` no cadence at all — its
`next_review` is the announced date minus a 90-day lead.

### Known ledger gap

`*_GOV` and `*_URLS` constants validate as trigger coordinates but have **no re-verification ledger**,
so they get no `STALE` warning. Only the six `*_LIC` dicts carry pass dates. Three triggers point at
GOV/URLS constants today and are covered by their `next_review` date alone. Closing this is a job for
the next re-verification pass — see Step 3 of the runbook.

## Framework backlog

Backlog (documented in FRAMEWORK-SELECTION.md): US state-privacy composite (CPRA-anchored),
SEC 17a-4/FINRA (strong RM + Communication Compliance stories), NIS2/DORA. *(FERPA and the 800-53 subset shipped in Increment 1.)*
**Product roadmap: complete.** Defender for Cloud shipped 2026-07-18 as product #6, the final planned product
(§15). *(Entra #2, Intune #3, Defender XDR #4 all 2026-07-17; Sentinel #5 2026-07-18.)* The five Defender-for-Cloud
free-text entry points (PCI 5.2 / DPR J #38 / A.5.23 / A.8.8 / ID.RA-01) all gained stacked rows at their exact
control refs (§15). The only remaining `RELATED_PRODUCTS` slug is **priva** (11 contributing links on privacy rows),
deliberately kept as a permanent reference-only product, never to be authored (§15). Next: a whole-atlas
consistency pass, then publishing.
