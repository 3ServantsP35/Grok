# MSTR Suite Report — Refactor Plan v1
**Project:** P-MSTR-SUITE  
**Date:** 2026-03-18  
**Author:** Cyler (CIO)  
**Status:** Implementation plan — translates the new suite specification into concrete script work for `scripts/mstr_suite_report.py`

---

## Objective

Refactor `scripts/mstr_suite_report.py` from an **old 5-chart confirmation ladder** into a **force-aware MSTR path forecasting report**.

The refactored script must align with:
- `briefs/mstr-chart-suite-spec-v2.md`
- `projects/README.md`
- `pine/INDICATOR-GUIDE.md` Force Field / FF ROC interpretation rule

---

## Current State Summary

### What already works
- CSV loading framework exists
- 5-chart analyzers exist:
  - MSTR LT
  - STRC LT
  - Stablecoin Dominance LT
  - STRF/LQD LT
  - MSTR/IBIT LT
- Discord reminder/report plumbing exists
- General report scaffolding exists

### What is missing
- Force Field integration
- FF ROC interpretation
- ST SRI companion views alongside LT views
- ST/LT slow-trackline progression / cross logic
- trend line geometry integration
- Fibonacci retracement confluence layer
- scenario engine
- bucket strategy translation
- correct weighting hierarchy

---

## Refactor Philosophy

### Old primary logic
- count chart confirmations
- derive score
- assign outlook

### New primary logic
1. determine **force state**
2. determine **force quality**
3. determine **trend line confrontation**
4. use 5-chart suite as corroboration
5. produce path scenarios
6. translate to bucket posture

The old chart-count approach should be demoted to a **supporting corroboration metric**, not removed entirely.

---

## Required Output Structure

The refactored report should produce these sections in order:

### 1. Structural State
- 5-chart suite states
- broad alignment summary
- original Force Field zone

### 2. Force Diagnostics
- `F_net`
- `F_net ROC 1`
- `F_net ROC 3`
- `F_net ROC 5`
- `F_net Acceleration`
- original FF vs FF ROC interpretation

### 3. Trend Line Geometry
- local resistance
- global resistance
- first reset support
- deeper reset / 1B support
- projected line values
- line quality / confidence (if available)

### 4. Scenario Probabilities
Minimum scenarios:
- immediate breakout continuation
- shallow reset then breakout
- deeper 1B reset
- bearish structure failure

### 5. CIO Conclusion
- most likely path
- what matters next
- invalidation conditions

### 6. Bucket Strategy Translation
- AB3 posture
- AB2 posture
- AB1 posture
- AB4 posture

Constraint:
- no exact trade structures
- no strikes/expiries
- no account-specific execution

---

## Concrete Refactor Plan

## Phase A — Preserve and isolate reusable components

### Keep as-is or near-as-is
- environment loading
- CSV loading utilities
- message splitting / Discord posting
- reminder mode
- freshness assumptions

### Preserve but relocate
Move current per-chart analyzers into a dedicated “structural analyzers” block:
- `analyze_mstr_lt()`
- `analyze_strc_lt()`
- `analyze_stab_dom()`
- `analyze_strf_lqd()`
- `analyze_mstr_ibit()`

Then add ST companion analyzers or extensions for the same charts where data/columns exist.

These should feed **Section 1 — Structural State**.

---

## Phase B — Add Force Field / FF ROC layer

### New required function
`analyze_force_state(df_mstr: pd.DataFrame) -> dict`

Expected inputs:
- MSTR CSV containing Force Field export columns

Expected fields:
- `f_net`
- `f_net_roc_1`
- `f_net_roc_3`
- `f_net_roc_5`
- `f_net_accel`
- bull/bear zone classification from original FF thresholds
- interpretation label:
  - bullish and strengthening
  - bullish but decelerating
  - bearish but repairing
  - bearish and worsening
  - exhausted / rebuilding

### Required outputs
- state label
- change label
- tactical note
- whether force supports:
  - breakout
  - reset
  - deeper reset
  - breakdown risk

---

## Phase C — Add trend line geometry layer

### Dependency
Use `scripts/trend_line_engine.py`

### New required interface
`analyze_trend_geometry(df_mstr: pd.DataFrame) -> dict`

Minimum outputs:
- `local_resistance`
- `global_resistance`
- `local_support`
- `global_support`
- `first_reset_support`
- `deeper_reset_support`
- `distance_to_local_resistance_pct`
- `distance_to_global_resistance_pct`
- `distance_to_local_support_pct`
- `distance_to_global_support_pct`
- projected values by date
- confidence / fit quality if available

### Important rule
Trend lines should be treated as **decision geometry**, not decorative analytics.

The trend geometry layer must answer:
- is price near a decisive line?
- is force sufficient to break it?
- if not, where is the likely reset destination?

---

## Phase C.75 — Add Fibonacci retracement layer

### New required function
`analyze_fibonacci_context(df, trend) -> dict`

Minimum outputs:
- dominant swing low
- dominant swing high
- 38.2% retracement zone
- 50% retracement zone
- 61.8% retracement zone
- confluence notes vs trend lines / SRI supports

### Best-practice rule
Use Fibonacci retracement as a **confluence layer**, not a standalone trigger. It should help distinguish likely shallow reset zones from deeper 1B candidate zones.

## Phase C.5 — Add ST progression layer

### New required function
`analyze_st_progression(...) -> dict`

Minimum outputs:
- ST state for each core chart where available
- ST slow-trackline slope
- LT slow-trackline slope
- ST vs LT slow-trackline relationship
- whether an ST/LT slow-trackline cross is forming, confirmed, or failing

### Why this matters
ST views are not optional garnish. They are the **transition layer** that helps identify whether macro stage progression is actually advancing before LT alone fully confirms. In particular, **ST/LT crosses of slow tracklines** should be treated as structurally important progression signals.

## Phase D — Replace old composite score logic

### Old model to demote
Chart-count alignment should no longer be the main score.

### New hierarchy
Use weighted narrative logic in this order:
1. force regime
2. force quality
3. ST/LT progression state
4. trend line confrontation
5. Fibonacci confluence
6. 5-chart corroboration

### Transitional scoring option
If a numeric score is still desired, use category weights instead of equal chart-count weights.

Suggested conceptual weighting:
- Force regime: 22.5%
- Force quality / ROC: 22.5%
- ST/LT progression: 20%
- Trend line geometry: 17.5%
- Fibonacci confluence: 7.5%
- 5-chart alignment corroboration: 10%

This can remain qualitative at first; no need to overfit prematurely.

---

## Phase E — Add scenario engine

### New required function
`build_scenarios(structural, force, trend) -> list[dict]`

Minimum scenarios:
1. immediate breakout continuation
2. shallow reset then breakout
3. deeper 1B reset
4. bearish structure failure

For each scenario output:
- name
- probability estimate
- supporting conditions
- invalidation conditions
- brief narrative

### Current practical rule
Until validated statistically, probabilities are discretionary-CIO estimates based on the integrated model.

---

## Phase F — Add bucket translation layer

### New required function
`translate_to_buckets(scenarios, force, structural) -> dict`

Outputs:
- `AB3`: add / hold / wait / de-risk
- `AB2`: bullish directional / bearish directional / no AB2 edge
- `AB1`: favorable theta / avoid theta / neutral
- `AB4`: deploy / preserve / raise cash staging

### Hard boundary
This layer must stop at strategy posture only.

No:
- specific trades
- strikes
- expiries
- user/account execution

Those belong in PPR.

---

## Phase G — Rewrite report builder

### New report builder should assemble:
1. structural state
2. force diagnostics
3. trend geometry
4. scenarios
5. CIO conclusion
6. bucket translation

### Existing report sections to de-emphasize or remove
- simplistic “score = outlook” framing
- chart count as the primary confidence engine
- generic action items that do not reference force or trend lines

---

## Recommended Function Layout

```python
load_env()
load_csv()

analyze_mstr_lt()
analyze_strc_lt()
analyze_stab_dom()
analyze_strf_lqd()
analyze_mstr_ibit()

analyze_force_state()
analyze_trend_geometry()

build_structural_state()
build_scenarios()
translate_to_buckets()

build_report()
send_discord()
```

---

## Immediate Build Sequence

### Step 1
Audit column availability in current MSTR suite CSVs for FF / FF ROC fields.

### Step 2
Implement `analyze_force_state()` using existing MSTR CSV exports.

### Step 3
Add ST companion-view / ST-LT progression analysis, with explicit handling for ST/LT slow-trackline relationships and crosses.

### Step 4
Audit `trend_line_engine.py` interface and define the smallest usable integration for local/global resistance + support projections.

### Step 5
Refactor the report output to include the new sections before changing reminder/automation behavior.

### Step 6
Only after the live discretionary report looks correct, revisit automation and validation.

---

## Alignment Checks

The refactor is complete when:
- the report no longer depends primarily on chart-count alignment
- FF and FF ROC are first-class report sections
- trend line geometry is explicitly included
- scenarios are presented as path probabilities
- bucket translation is present
- no trade-ticket logic appears in the suite report

---

## Recommended Next Coding Task

**Task 1:** add Force Field / FF ROC analysis to `scripts/mstr_suite_report.py` and expose it in the report before touching full scenario generation.

Reason:
- smallest high-value upgrade
- directly aligned with current live analytical edge
- lets the suite begin evolving immediately without waiting for full trend line integration
