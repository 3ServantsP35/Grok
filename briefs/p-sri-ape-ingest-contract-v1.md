# P-SRI APE Ingest Contract v1

**Project:** P-SRI-V3.2.2 / Layer 0.75 APE Integration  
**Date:** 2026-05-01  
**Author:** Cyler (CIO)  
**Status:** v1 contract brief for Archie implementation and CRO-side handshake

---

## 1. Executive summary

v3.2.2 already defines **Visser / APE** as an external branch that should feed Layer 0.75, not be reimplemented inside the MSTR engine.

What is missing is the **handoff contract**.

My recommendation for v1 is deliberately conservative:

- **Do not ingest raw RIS internals directly into SRI.**
- **Do ingest a single human-readable routed digest** modeled on the APE-side live artifact pattern already in production.
- **Treat APE intelligence as an advisory branch-intelligence layer**, not as an override of Howell phase, AB4 benchmark posture, or resolver math.
- **Make freshness explicit** and degrade gracefully when stale.

This keeps v1 implementable, legible, and close to what the APE-side CRO already uses daily.

---

## 2. MSTR-side architectural context

The governing architecture is already clear in v3.2.2:

- Layer 0 = GLI macro backdrop
- Layer 0.5 = Howell phase engine
- **Layer 0.75 = theme routing and ingest layer**
- Layer 1+ = shared regime, signal, and allocation logic

Per `Training/SRI-Engine-Tutorial-v3.md`:
- Visser is an **externally constructed strategy branch owned by APE**
- SRI should ingest APE strategic output rather than recreate it
- APE should ideally provide structured payload fields including:
  - Era State
  - Thesis State
  - Security Universe / Sleeve Composition
  - Target Weights
  - Internal Conviction / Confidence
  - Watchlist Promotion / Demotion Signals
  - Strategic Warnings / Cautions

Per the same doc, the key doctrine line is:

> **APE builds the ETF; SRI decides how much ETF, when, and under what macro and timing conditions.**

That sentence should govern the contract.

---

## 3. APE-side live source reality observed during coordination

I did **not** design this contract from a blank page. I anchored it to the current APE/CRO side.

### 3.1 Observed live artifact
The CRO workspace already contains:

- `today-ris-brief.md`

Current observed characteristics:
- single Markdown artifact
- regenerated nightly
- routed / ranked for CRO attention
- explicitly based on **RIS v2 insights**
- explicitly includes / expects these semantics:
  - **conviction**
  - **dialectic**
  - **corroboration**
  - **route**
  - **recommended_action**
- daily CRO digest filters to `pipeline_status='ready'`, last 1 day, `min_conviction=50`
- explicitly omits low-conviction items below threshold from the daily digest
- can be freshly generated even when **no qualifying routed insights** exist for the day

### 3.2 Observed production notes
From the APE-side workspace docs and producer scripts:
- `today-ris-brief.md` is described as the **session-start artifact** for CRO
- it is regenerated nightly by **`scripts/emit_cro_ris_digest.py`** in the AI Portfolio Engine
- the producer writes directly to `~/.openclaw-cro/workspace-cro/today-ris-brief.md`
- it is part of the **DAILY_RIS** cron group
- documented production flow is `daily_insight_brief.py` followed by `emit_cro_ris_digest.py`
- if missing or older than 24 hours, CRO is supposed to flag the RIS pipeline as stale/failed

### 3.3 Contract implication
That means the highest-probability successful v1 design is:

- **mirror the same operational pattern into MSTR-CIO**
- do **not** require MSTR to query APE databases directly
- do **not** require MSTR to ingest every RIS object class in v1
- consume a **published APE digest** that is already curated and routed upstream

---

## 4. Contract decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | **v1 payload landing artifact is a single Markdown file** | This matches the live APE-side operating pattern (`today-ris-brief.md`) and makes Cyler session-start loading trivial. |
| D2 | **Target path in MSTR workspace: `mstr-knowledge/ape_intel.md`** | It belongs alongside `ab_profile.md`, `phase_state.md`, and `cycle_state.md` as a readable context artifact, not hidden in a generic feed directory for v1. |
| D3 | **Publisher remains on APE side** | APE owns Visser branch intelligence. MSTR should consume a published artifact, not reconstruct RIS logic. |
| D4 | **v1 includes only routed RIS intelligence, not raw council outputs** | MSTR needs the distilled intelligence layer, not every upstream deliberation artifact. Keep the contract narrow and legible. |
| D5 | **Howell / AB4 remain authoritative for benchmark and phase classification** | APE is advisory branch intelligence, not the benchmark engine. This preserves v3.2.2 doctrine. |
| D6 | **APE contradictions are surfaced as warnings and sizing/timing cautions, not silent overrides** | This follows the existing v3.2.2 conflict-handling doctrine for Visser. |
| D7 | **Freshness is explicit and non-fatal by default** | MSTR should degrade gracefully when APE stalls, the same way it already surfaces stale cycle-state warnings. |
| D8 | **Raw JSONL / multi-file registry is deferred to v2** | Valuable later, but unnecessary to unblock morning-read intelligence now. |

---

## 5. Payload shape

## 5.1 v1 landing artifact

**Canonical v1 artifact:**

- `mstr-knowledge/ape_intel.md`

This file should be generated by an APE-side publisher and copied or synced into the MSTR workspace.

## 5.2 Why Markdown, not JSONL, for v1

Reasons:
- Cyler is already designed to **read knowledge Markdown files at session start**.
- APE already operates with a **daily Markdown digest**.
- Archie needs something buildable fast and debuggable by humans.
- This layer is currently a **reasoning input**, not an event stream processor.

## 5.3 Required file structure

Recommended structure:

```markdown
# APE Intelligence Digest

_Generated by `<publisher>` at `<timestamp>`._
_Source workspace: `~/.openclaw-cro/workspace-cro/`._
_Source artifact / query basis: `today-ris-brief.md` and RIS v2 routed insights._
_Freshness state: `<fresh | aging | stale | failed>`._
_Threshold rule: items below conviction `<X>` omitted from v1 daily digest._

## Summary

- Era state: `...`
- Thesis state: `...`
- Route posture: `...`
- Visser deployment bias: `increase | maintain | reduce | defer`
- Critical cautions: `...`

## Routed Insights

| Scope | Route | Conviction | Direction | Recommended action | Why it matters |
|---|---|---:|---|---|---|
| ... | ... | 72 | bullish | ... | ... |

## Watchlist / Promotion-Demotion Signals

- ...

## Strategic warnings / contradictions

- ...

## Provenance snapshot

- Source families seen in this digest: `Visser`, `RSS`, `YouTube`, `SEC/EDGAR`, `other RIS-native sources`
- CRO route classes represented: `Portfolio Action`, `Governance`, `Thesis/Underwriting/Watchlist`, `Monitor/Informational`

## Freshness / health

- Generated at: `...`
- Source age hours: `...`
- Publisher status: `ok | partial | failed`
- Notes: `...`
```

## 5.4 Required metadata fields

At minimum, the digest must expose these top-level fields, whether as Markdown prose, a front-matter block, or a clearly labeled header section:

| Field | Required | Meaning |
|---|---|---|
| `generated_at` | yes | Time the MSTR-facing digest was generated |
| `source_generated_at` | yes | Time the upstream APE digest or RIS query basis was generated |
| `source_workspace` | yes | APE-side workspace / producer source |
| `publisher` | yes | Script or process that emitted the MSTR-facing file |
| `freshness_state` | yes | `fresh`, `aging`, `stale`, or `failed` |
| `conviction_threshold` | yes | Omission threshold used for the daily digest |
| `item_count` | yes | Number of routed items included |
| `source_families` | yes | Which source families contributed to the digest |
| `route_classes_present` | yes | Which route classes are represented |
| `notes` | optional | Freeform health or publisher notes |

## 5.5 Required per-item fields

Each routed insight row or bullet should carry:

| Field | Required | Meaning |
|---|---|---|
| `scope` | yes | Ticker, theme, sleeve, or portfolio scope |
| `route` | yes | CRO/RIS route class |
| `conviction` | yes | Numeric conviction score |
| `direction` | yes | Bullish / bearish / mixed / informational |
| `recommended_action` | yes | Suggested action from APE/RIS side |
| `dialectic` | yes | Main tension or opposing argument summary |
| `corroboration` | yes | Whether / how the thesis is corroborated |
| `summary` | yes | One-paragraph or one-line why-it-matters note |
| `source_family` | yes | Visser / RSS / YouTube / SEC-EDGAR / etc. |
| `horizon` | optional | Tactical / medium-term / strategic |

## 5.6 Taxonomy for v1

### Route taxonomy
Use two layers explicitly.

**APE/CRO routing engine route families:**
- `PORTFOLIO_EXIT`
- `PORTFOLIO_ENTRY`
- `PORTFOLIO_SIZE_UP`
- `PORTFOLIO_SIZE_DOWN`
- `THESIS_CHALLENGE`
- `THESIS_REINFORCE`
- `WATCHLIST_ADD`
- `WATCHLIST_REMOVE`
- `MONITOR`
- `NOISE`

**Digest display buckets for Cyler:**
- `Portfolio Action`
- `Governance / Thesis Change`
- `Watchlist / Promotion-Demotion`
- `Monitor / Informational`

### Direction taxonomy
Use:
- `bullish`
- `bearish`
- `mixed`
- `informational`

### Freshness taxonomy
Use:
- `fresh`
- `aging`
- `stale`
- `failed`

### Scope taxonomy
Allow:
- ticker
- sub-theme
- Visser sleeve
- macro / portfolio-level

---

## 6. Schedule and ordering

## 6.1 Recommended cadence

**Daily** is the correct v1 cadence.

Reason:
- APE/CRO already uses a nightly routed digest model.
- Cyler’s morning reasoning needs a stable pre-read artifact.
- Weekly is too slow for the intended “morning brief / current intelligence” use.
- Intraday push semantics are useful later, but not necessary for the first contract.

## 6.2 Ordering requirement

Recommended order for the daily chain:

1. APE / RIS nightly processing completes.
2. APE emits its CRO digest (`today-ris-brief.md`) and then the MSTR-facing publisher artifact.
3. MSTR workspace receives `mstr-knowledge/ape_intel.md`.
4. Cyler session-start load reads:
   - `ab_profile.md`
   - `phase_state.md`
   - `cycle_state.md`
   - `ape_intel.md`
5. Morning brief / PPR reasoning proceeds.

## 6.3 Timing recommendation

v1 target:
- artifact should land **before the MSTR morning brief window**, not after it
- practical target: **publish no later than 08:00 local system time of the producer chain**
- if APE’s own nightly digest already lands earlier, preserve that earlier cadence

The critical requirement is not the exact clock minute. It is this:

> **Cyler should never read APE intelligence before the APE nightly pipeline has completed for the current day.**

---

## 7. Target workspace path

## Decision

**Canonical path:**

- `mstr-knowledge/ape_intel.md`

## Why not `data-feed/ape/` in v1

A `data-feed/ape/` directory is attractive if we later want structured multi-file artifacts, archives, or JSON sidecars.

But for v1, that adds operational surface without solving the main problem.

The main problem is:
- Cyler lacks a readable APE/Visser intelligence artifact at session start.

A single knowledge file solves that directly.

## Recommended optional v1.1 addition

If Archie wants archival traceability without changing Cyler’s read path, add:

- `data-feed/ape/archive/YYYY-MM-DD-ape-intel.md`

and have:
- `mstr-knowledge/ape_intel.md` be the latest published copy.

That is optional for v1.

---

## 8. Source contract on the APE side

## 8.1 What should flow through in v1

**Include:**
- routed RIS v2 intelligence that has already survived APE-side filtering / ranking
- Visser-relevant strategic signals
- promotion / demotion signals
- strategic warnings / cautions
- route metadata
- conviction metadata
- source-family provenance
- enough claim metadata to preserve the meaning of the surfaced item (`extracted_claim` summary, first ticker/scope, source tier, direction, recommended action)

**Do not include directly in v1:**
- raw Bear/Bull/Systems Architect/Portfolio Fit/Flow-Quant council transcripts
- raw evidence objects
- full RIS internal databases
- every low-conviction monitor note

## 8.2 Why the council outputs are excluded in v1

Those outputs are valuable inside APE.

But exporting them wholesale into MSTR would:
- create noise
- duplicate reasoning layers
- blur ownership boundaries
- force Cyler to interpret APE internals instead of ingesting APE conclusions

The right v1 principle is:

> **publish the intelligence APE wants downstream consumers to act on, not every internal deliberation artifact.**

## 8.3 Publisher script ownership

Current documented APE-side nightly digest generator:
- `scripts/emit_cro_ris_digest.py`

Recommended v1 publisher approach:
- either extend that script, or add a sibling publisher such as
  - `scripts/publish_mstr_ape_digest.py`

The MSTR contract does **not** require APE to redesign RIS.
It only requires a stable publisher that writes the MSTR-facing digest.

## 8.4 Producer-side location

Documented producer environment from CRO docs:
- AI Portfolio Engine
- publisher script family under `scripts/`
- source workspace `~/.openclaw-cro/workspace-cro/`

Archie should therefore implement against an APE-owned producer path, not a consumer-side scraper.

---

## 9. Cyler session-start integration

## 9.1 Load-list placement

Add `mstr-knowledge/ape_intel.md` to the session-start load list **after `cycle_state.md` and before `notional_delta_convention.md`**.

Recommended order:
1. `active-tasks.md`
2. `SOUL.md`
3. `lessons.md`
4. `mstr-knowledge/system-learnings.md`
5. `mstr-knowledge/portfolio-state.md`
6. `mstr-knowledge/trading-rules.md`
7. `mstr-knowledge/ab_profile.md`
8. `mstr-knowledge/phase_state.md`
9. `mstr-knowledge/cycle_state.md`
10. `mstr-knowledge/ape_intel.md`
11. `mstr-knowledge/notional_delta_convention.md`
12. `mstr-knowledge/ppr_template.md` (load only when needed)

## 9.2 Why this slot is correct

That placement preserves the doctrinal order:
- first read the **benchmark and macro state**
- then read the **advisory external branch intelligence**
- then read technical implementation references

That prevents APE from being implicitly elevated above Howell / AB4.

## 9.3 Interaction with `phase_state.md` and `cycle_state.md`

Recommended interpretation:

- `phase_state.md` = **authoritative benchmark / macro posture input**
- `cycle_state.md` = **secondary timing overlay**, currently warning-prone because staleness already exists
- `ape_intel.md` = **branch-intelligence advisory context** for Visser sleeve deployment interpretation

So `ape_intel.md` should inform:
- whether Visser sleeve conviction is rising or fading
- whether a deviation into or away from Visser is strategically supported
- whether certain names or sub-themes deserve promotion / demotion attention

It should **not** directly rewrite:
- Howell phase
- AB4 benchmark weights
- AB3 tolerance bands
- resolver classification math

---

## 10. Doctrine for conflicts

## Decision

When APE intelligence contradicts MSTR Engine phase classification:

- **Howell / AB4 wins on benchmark posture and classification**
- **APE remains advisory on strategic branch conviction**
- the contradiction must be **surfaced explicitly** in Cyler’s reasoning

## Examples

### Example A
- APE says infrastructure names are strategically attractive
- Howell is in `Turbulence`

Result:
- do **not** increase benchmark risk posture because of APE
- do allow Cyler to say: strategic branch still attractive, but deployment should be reduced / staged / deferred because phase is hostile

### Example B
- APE says promote a new Visser beneficiary
- Howell is supportive, but TA says overextended

Result:
- contradiction lives in the recommendation
- likely outcome is **smaller size, staged entry, or monitor-only**

### Example C
- APE says reduce conviction while Howell remains supportive

Result:
- benchmark may still allow branch exposure
- Cyler can recommend **underweight versus benchmark** or tighter scrutiny of Visser deviations

## Governing principle

> **APE controls strategic content; SRI controls macro conditioning, benchmark posture, and timing discipline.**

---

## 11. Failure modes and staleness handling

## 11.1 Freshness thresholds

Recommended thresholds:

- **fresh** = artifact age `<= 24h` and publisher completed successfully
- **aging** = artifact age `> 24h and <= 48h`
- **stale** = artifact age `> 48h`
- **failed** = file missing, malformed, or publisher explicitly marked failed

Additionally, distinguish **artifact freshness** from **intelligence dormancy**:
- a file may be `fresh` even if there are **0 qualifying routed insights**
- that should be rendered as `fresh / no qualifying items`, not mistaken for publisher failure

## 11.2 Behavior by state

| State | Cyler behavior |
|---|---|
| `fresh` | Use normally as advisory Layer 0.75 context |
| `aging` | Use with caution and mention age if relying on it materially |
| `stale` | Do not use for decisive Visser sleeve recommendations without explicit warning |
| `failed` | Ignore as an input and state that APE intelligence is unavailable |

## 11.3 Hard fail vs soft warn

**Recommendation:** default to **soft warn**, not hard fail.

Reason:
- the rest of v3.2.2 can still function without APE
- MSTR branch logic and AB4 benchmark logic should remain operable
- this matches the project’s existing tolerance for stale secondary artifacts, with explicit warning banners
- the live APE-side system already has a meaningful distinction between:
  - publisher failure,
  - no ready rows above threshold,
  - and genuinely stale / dormant upstream intelligence

## 11.4 When staleness becomes operationally binding

If the user specifically asks for:
- Visser sleeve allocation
- APE-informed branch sizing
- cross-theme strategic comparison involving Visser

and `ape_intel.md` is `stale` or `failed`, then Cyler should say so explicitly and narrow the confidence of the answer.

That is stronger than a soft warn, but still not a global session hard fail.

---

## 12. Out of scope for v1

Deferred to v2:

1. **Raw JSONL or database-native contract**
   - useful later for machine querying, unnecessary for v1
2. **Bidirectional control loop**
   - MSTR sending structured feedback back into APE automatically
3. **Intraday push / alert contract**
   - v1 is daily pull/read semantics
4. **Full council-output export**
   - too noisy for first contract
5. **Security-level target-weight enforcement inside MSTR**
   - v1 is advisory intake, not APE-driven execution authority
6. **Shared TV-ingest or shared infrastructure library**
   - already explicitly deferred elsewhere
7. **Archive index / manifest / version registry**
   - optional later if the digest becomes machine-consumed by multiple scripts
8. **Formal contradiction scoring engine**
   - for now, contradiction is surfaced narratively in Cyler output

---

## 13. Implementation scaffolding

## 13.1 Recommended filesystem contract

### On APE side
Producer emits:
- canonical CRO digest: existing `today-ris-brief.md`
- MSTR-facing digest: new published artifact

### On MSTR side
Consumer reads:
- `mstr-knowledge/ape_intel.md`

Optional archive:
- `data-feed/ape/archive/YYYY-MM-DD-ape-intel.md`

## 13.2 Minimal sample payload

```markdown
# APE Intelligence Digest

_Generated by `publish_mstr_ape_digest.py` at 2026-05-02T07:40:00-07:00._
_Source digest generated at 2026-05-02T07:37:41-07:00._
_Source workspace: `~/.openclaw-cro/workspace-cro/`._
_Freshness state: `fresh`._
_Conviction threshold: `50`._
_Item count: `2`._

## Summary

- Era state: Infrastructure-heavy, power/grid beneficiaries still favored
- Thesis state: intact but selective
- Route posture: thesis-supportive, sizing-cautious
- Visser deployment bias: maintain / selective add
- Critical cautions: macro support weaker than strategic narrative

## Routed Insights

| Scope | Route | Conviction | Direction | Recommended action | Why it matters |
|---|---|---:|---|---|---|
| Power / Grid | Thesis / Underwriting / Watchlist | 74 | bullish | keep priority high | strategic bottleneck thesis still corroborated across sources |
| Hyperscaler capex second-order names | Monitor / Informational | 58 | mixed | selective only | narrative intact, but entry quality varies and macro backdrop is less forgiving |

## Watchlist / Promotion-Demotion Signals

- Promote names tied to durable grid bottlenecks only when valuation / structure are acceptable
- Do not treat narrative breadth as automatic deployment breadth

## Strategic warnings / contradictions

- APE strategic conviction remains constructive, but Howell phase may still justify reduced branch size or slower deployment

## Provenance snapshot

- Source families seen in this digest: Visser, RSS, YouTube, SEC/EDGAR
- Route classes represented: Thesis / Underwriting / Watchlist, Monitor / Informational

## Freshness / health

- Generated at: 2026-05-02T07:40:00-07:00
- Source age hours: 0.0
- Publisher status: ok
- Notes: none
```

## 13.3 Recommended AGENTS.md insertion patch

```markdown
*** Begin Patch
*** Update File: AGENTS.md
@@
 8. `mstr-knowledge/phase_state.md` — current Howell phase + sector signals (auto-generated daily)
 9. `mstr-knowledge/cycle_state.md` — Camel cycle state replication (auto-generated daily)
-10. `mstr-knowledge/notional_delta_convention.md` — option/spread notional + delta convention
-11. `mstr-knowledge/ppr_template.md` — Portfolio Posture Report template (load only when emitting a PPR)
+10. `mstr-knowledge/ape_intel.md` — APE / Visser Layer 0.75 intelligence digest (advisory branch context; check freshness banner)
+11. `mstr-knowledge/notional_delta_convention.md` — option/spread notional + delta convention
+12. `mstr-knowledge/ppr_template.md` — Portfolio Posture Report template (load only when emitting a PPR)
*** End Patch
```

---

## 14. Open items requiring Gavin input

| Item | Question | My recommendation |
|---|---|---|
| O1 | Should the MSTR-facing digest carry only Visser-relevant routed items, or the full APE routed digest with non-Visser items filtered in Cyler? | Prefer **Visser-relevant / downstream-relevant only** in v1. |
| O2 | Should conviction threshold remain `50`, mirroring CRO’s daily digest pattern, or be lower for MSTR? | Start with **50** for parity and legibility. |
| O3 | Should `ape_intel.md` be loaded every session, or only when a Visser sleeve is active / under review? | Load every session once the file exists, because contradiction context can still matter. |
| O4 | Does Gavin want an optional archive directory from day one? | Nice-to-have, not required for v1. |
| O5 | Does Gavin want a second machine-readable sidecar in v1 (`ape_intel.json`)? | I would defer it unless Archie says it materially reduces parser effort. |

---

## 15. Final recommendation

The clean v1 answer is:

- **APE publishes one MSTR-facing daily digest**
- **that digest lands at `mstr-knowledge/ape_intel.md`**
- **Cyler reads it after `phase_state.md` and `cycle_state.md`**
- **Howell / AB4 remain authoritative**
- **APE informs strategic Visser interpretation, not benchmark math**
- **staleness is surfaced explicitly and handled as soft-warn degradation**

That is narrow enough to build now, faithful to the current APE-side operating reality, and fully consistent with the v3.2.2 architecture.
