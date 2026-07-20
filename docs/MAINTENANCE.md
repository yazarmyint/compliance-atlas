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

## The re-verification runbook

The recurring counterpart to the add-a-product procedure in
[`AUTHORING.md`](AUTHORING.md#add-a-product). That procedure is retired — the product roadmap closed
at six — so this is now the only process that runs more than once, and it had never been written
down (PROJECT-REVIEW PR-053). It is written to be handed to someone who is not you.

A pass is **scoped, not exhaustive**. You re-verify what the build says is due, and nothing else. The
temptation to sweep everything while you are in there is what makes passes too expensive to run,
which is how the atlas goes quiet.

### When to run one

Two routes in, and they are different sizes:

| Route | Scope | Typical size |
|---|---|---|
| A build warning fired | Only the constants and triggers named in it | 1–12 constants |
| The stated policy (`meta.reverification_policy`: at least twice a year) | Everything past cadence | up to 49 constants |

The second is not an emergency. If the build names 40 constants, that is the twice-yearly pass
arriving on schedule, not a backlog.

### Before you start

1. Branch. Existing convention in git history is `session-<n>-<topic>`.
2. **Read the protected-field rules and do not restate them anywhere.** A re-verification pass writes
   `license_requirement`, `sources`, and `last_verified`, which are protected fields — see the row
   schema in [`AUTHORING.md`](AUTHORING.md#row-schema-current) for what each field means, and
   AUDIT-FINDINGS §22 for the declared-edit convention a pass that touches them must follow. Those
   are the only definitions; this runbook deliberately keeps none of its own.
3. `python build/assemble.py --maintenance-report` and keep the output. It is your worklist and it
   goes in the audit entry.

### Step 1 — scope the pass from the warnings

The warning names **constants**, not rows. That is the unit of work: one constant, one source fetch,
one verdict. Do not scope a pass by row count — 42 rows resting on `SENTINEL_LIC["ingest"]` are one
piece of work, not 42.

Write down the list of `(dict, key)` coordinates you intend to cover before you fetch anything. That
list becomes `REVERIFIED_LIC_KEYS_<n>` in Step 3, and the discipline is that a coordinate only goes
in it if you actually fetched its source.

### Step 2 — fetch live, by trigger type

Never from memory, never from a blog, never from a previous session's notes. The source differs by
`type`, which is why the type column exists:

<a id="licensing"></a>
**`licensing`** — the product's own authoritative licensing source, never another product's:

| Constants | Source |
|---|---|
| `LIC` | Purview service description, per-feature tables |
| `ENTRA_LIC` | Entra licensing article |
| `INTUNE_LIC` | Intune licensing article **and** the planning guide step 3 — see `TRG-INTUNE-LICENSING`, the restructure is currently stated in only one of them |
| `DEFENDER_LIC` | Defender service description; XDR prerequisites for `xdr` |
| `SENTINEL_LIC` | Sentinel billing article + the Azure pricing page; the 50 GB tier is on neither, only the Partner Center announcement |
| `MDC_LIC` | Azure pricing page for Defender for Cloud |

Record a verdict per constant — CHANGED or PASS — even when nothing moved. A PASS is evidence and it
is what lets `last_verified` advance honestly.

<a id="naming"></a>
**`naming`** — service description plus the solution overview pages. When you confirm a rename, add
the pair to `RETIRED_NAMES` in `common.py`.

Understand what that lint does and does not do. It is a **deny-list, so it is a regression check, not
a discovery mechanism.** It cannot catch a rename nobody has heard of yet — it would not have caught
PR-035 before the Defender Suite rename was known. What it guarantees is that once a rename is fixed,
the old name can never quietly return. Discovery is this step, performed by a person reading the live
page; the lint only holds the line afterwards. Two consequences worth remembering: a pair whose
glossed form the atlas deliberately keeps (`"(formerly Microsoft 365 E5 Security)"`) must stay in the
list while the gloss stays, and must be **removed** from it when the gloss is finally dropped, or the
lint will start flagging the gloss itself.

<a id="retirement"></a>
**`retirement`** — the retirement announcement itself. Confirm the date has not moved; it usually
has. Sentinel's Azure-portal retirement has already slipped once (Jul 1 2026 → Mar 31 2027).

<a id="framework"></a>
**`framework`** — the regulator or standards body only. If the version moved, that is not a
re-verification pass: pinning a new framework version changes control numbering and is a separate,
larger piece of work. Record it and stop.

<a id="sovereign"></a>
**`sovereign`** — the US Government service descriptions and per-product government availability
pages. Note the ledger gap above: these constants have no pass date, so your `next_review` is the
only clock on them.

<a id="watch"></a>
**`watch`** — read it, decide, and usually change nothing. Advance `next_review` and move on. A watch
that keeps producing no action for several cycles should be deleted, not carried forever.

### Step 3 — record the pass

**This is the step with no prose equivalent, and the one most likely to be skipped.** You do not
hand-write `last_verified`. It is derived: a row's date moves because a constant it rests on was
re-verified.

In `build/common.py`:

```python
REVERIFY_DATE_3 = "2027-01-20"           # the date you actually fetched
REVERIFIED_LIC_KEYS_3 = {                # ONLY coordinates whose source you fetched
    ("SENTINEL_LIC", "ingest"), ...
}
```

then append to `reverify_passes()`. Passes run in date order, so a row covered by more than one ends
on the latest date that verified something it actually rests on.

**The rule, restated because it is the one that decays first:** a key goes in only if you fetched its
source in this pass — whether it changed or passed. Rows resting on constants you did not check keep
their older date, and that is the honest answer for them. The 2026-07-19 pass moved 324 of 378 rows,
not all 378, precisely because of this.

Then, per trigger you executed: set `last_executed` to the pass date and advance `next_review`. Both
are hand-set static dates. Nothing in `MAINTENANCE` is ever computed.

> **Extend the ledger while you are here.** The `REVERIFIED_LIC_KEYS` convention currently covers only
> the six `*_LIC` dicts. The next pass should extend it to `*_GOV` and `*_URLS` so those constants get
> a real staleness clock instead of relying on a trigger date alone.

### Step 4 — the drift ledger

A per-constant CHANGED/PASS table in the AUDIT-FINDINGS §22.2 format, with the source fetched for
each. Cross-reference §22; do not restate its conventions here.

Two things §22 got right that are worth repeating as method, not policy: treat any prior review's
findings as **leads to re-test, not facts** (one PROJECT-REVIEW finding did not survive re-testing,
§22.5), and record what you did **not** reach as explicitly as what you did (§22.2's "not re-verified"
rows are why the `last_verified` policy is defensible).

### Step 5 — gate

```powershell
python build/assemble.py            # integrity assertions + the maintenance report
python build/build_html.py
python tools/check_urls.py          # citation resolution and redirect drift
node tools/axe_check.mjs            # WCAG 2.1 A/AA, every view, both themes
```

> **You no longer clear `build/__pycache__` by hand — the build does it.** `assemble.py` and
> `build_html.py` each remove `build/__pycache__` before their first sibling import (PR-058), so a
> pass cannot regenerate the artifact from stale bytecode whether or not you remembered a manual step.
> This mattered: Python validates cached bytecode on `(mtime, size)`, a re-verification pass makes
> exactly the edit that defeats that check — a same-length substitution inside a date or a SKU string,
> written in the same second as the last build — and the old behaviour was to rebuild from the **old
> constants, silently and with exit 0**. It was the one failure mode in the gate that produced a
> confidently wrong artifact rather than an error. History and the reproduction are in
> AUDIT-FINDINGS §26.8; the fix and its regression proof are in §26.11.

Then `git diff compliance-atlas.json` and read it. **Expect it to be empty.** There is no noise floor:
since PR-057 the dataset carries nothing time-derived, so a rebuild that changes no content leaves it
byte-identical. Every line you see is a change you intended and can name, or a defect. Re-read the
maintenance report and confirm the warnings you set out to clear are gone.

> **`compliance-atlas.html` is not part of that check and will diff on every rebuild.** `build_html.py`
> stamps the footer's "Built …" timestamp into the page at generation time, so the HTML moves whether or
> not any content did. That is the design, not drift: the timestamp is a property of the page, the
> dataset is the thing held byte-stable. Do not chase it, and do not "fix" it by moving the timestamp
> back into the JSON — that is the state PR-057 removed.

### Step 6 — version and changelog

PATCH under the policy in [`CHANGELOG.md`](../CHANGELOG.md#versioning-policy): re-verifications and
row corrections change claims, not structure. Then append an AUDIT-FINDINGS section following the
existing numbering.

### What a pass may not do

Re-author rows, change coverage or confidence verdicts on anything other than the evidence in front
of you, or add products or frameworks. Those are separate sessions with separate authorizations. The
boundaries are in [`AUTHORING.md`](AUTHORING.md); this runbook does not duplicate them.

## Framework backlog

Backlog (documented in FRAMEWORK-SELECTION.md): US state-privacy composite (CPRA-anchored),
SEC 17a-4/FINRA (strong RM + Communication Compliance stories), NIS2/DORA. *(FERPA and the 800-53 subset shipped in Increment 1.)*
**Product roadmap: complete.** Defender for Cloud shipped 2026-07-18 as product #6, the final planned product
(§15). *(Entra #2, Intune #3, Defender XDR #4 all 2026-07-17; Sentinel #5 2026-07-18.)* The five Defender-for-Cloud
free-text entry points (PCI 5.2 / DPR J #38 / A.5.23 / A.8.8 / ID.RA-01) all gained stacked rows at their exact
control refs (§15). The only remaining `RELATED_PRODUCTS` slug is **priva** (11 contributing links on privacy rows),
deliberately kept as a permanent reference-only product, never to be authored (§15). Next: a whole-atlas
consistency pass, then publishing.
