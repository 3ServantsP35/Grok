# MSTR Chart Suite — Re-Scoped Specification v2.0
**Project:** P-MSTR-SUITE  
**Date:** 2026-03-18  
**Author:** Cyler (CIO)  
**Status:** Active re-scope — replaces the original “5-chart confirmation ladder” framing as the primary design direction

---

## Executive Summary

P-MSTR-SUITE should no longer be treated as a simple **5-chart alignment ladder**.

That framing was directionally useful, but the recent Force Field work demonstrated that the highest-value medium-term question is not just:

> “How many charts are aligned?”

It is:

> **“What is the current force regime, is that force strengthening or weakening, and does it have enough energy to break the relevant structural trend lines?”**

Accordingly, the suite is re-scoped as a:

# **Force-Aware MSTR Path Forecasting Dashboard**

Its job is to estimate the **next 2–8 week path** for MSTR by combining:
1. structural chart-state inputs,
2. Force Field state,
3. Force Field ROC / acceleration,
4. trend line geometry,
5. scenario probabilities.

---

## Why the Re-Scope Is Necessary

### Old model limitation
The original suite hypothesis assumed that directional confidence could be approximated by counting how many of five LT charts pointed the same way.

That remains helpful, but it misses the most important distinction:

- **aligned and accelerating**
vs
- **aligned but fading**

The recent FF / FF ROC work on MSTR showed clearly that:
- the force regime can remain bullish,
- while the tactical quality of that bullishness deteriorates.

That distinction is the difference between:
- immediate breakout,
- shallow reset then breakout,
- deeper 1B reset.

### Trend line omission
The suite also proved incomplete without explicit **trend line geometry**. The most important practical medium-term question is often:

> **Does current force have enough strength to break the local/global resistance lines, or does price need a reset first?**

That is explicitly a P10 dependency.

---

## New Primary Objective

Produce a weekly and on-demand report that answers:

1. **What force regime is MSTR in right now?**
2. **Is force strengthening, weakening, or exhausting?**
3. **What structural barriers/supports matter most right now?**
4. **What is the highest-probability 2–8 week path?**
5. **What would confirm or invalidate that path?**

---

## Core Dependencies

### 1. Force Field (Original)
**Role:** Base regime/state indicator  
**Question answered:** *What force zone are we in?*

Use for:
- bull / neutral / bear zone classification
- structural backdrop
- base confidence regime

### 2. Force Field ROC
**Role:** Tactical change-of-state indicator  
**Question answered:** *Is that regime strengthening, weakening, accelerating, or exhausting?*

Use for:
- `F_net ROC 1`
- `F_net ROC 3`
- `F_net ROC 5`
- `F_net Acceleration`
- distinguishing bullish expansion from bullish deceleration

### 3. Trend Line Engine (P10)
**Role:** Structural geometry dependency  
**Question answered:** *What support/resistance line is price confronting, and is current force sufficient to break it?*

Use for:
- local resistance
- global resistance
- projected support lines
- first-reset vs deeper-reset path framing
- scenario branching

**Current maturity assessment:**
- Practical utility: HIGH
- Engineering maturity: MEDIUM
- Statistical validation: LOW–MEDIUM
- Ready for suite dependency: YES

### 4. Existing 5-chart suite inputs
These remain relevant as structure/context inputs:
1. MSTR LT
2. STRC LT
3. Stablecoin Dominance LT
4. STRF/LQD LT
5. MSTR/IBIT LT

---

## New Report Architecture

### Section 1 — Structural State
Purpose: establish the base chart-state backdrop.

Include:
- MSTR LT structure
- STRC LT state
- Stablecoin Dom LT state
- STRF/LQD LT state
- MSTR/IBIT LT state
- original Force Field zone

Output:
- Structural state label
- Broad directional bias
- Alignment summary

### Section 2 — Force Diagnostics
Purpose: explain whether the state is improving or deteriorating.

Include:
- `F_net`
- `F_net ROC 1`
- `F_net ROC 3`
- `F_net ROC 5`
- `F_net Acceleration`
- FF zone + FF ROC interpretation

Output labels:
- bullish and strengthening
- bullish but decelerating
- bearish but repairing
- bearish and worsening
- exhausted / rebuilding

### Section 3 — Trend Line Geometry
Purpose: identify the structural lines price must break or hold.

Include:
- local resistance line
- global resistance line
- first reset support
- deeper reset / 1B support
- projected line values by date
- confidence / fit quality when available

Output:
- break candidate
- likely test/reject level
- reset destination map

### Section 4 — Scenario Probabilities
Purpose: translate structure + force + geometry into paths.

Minimum scenarios:
1. immediate breakout continuation
2. shallow reset then breakout
3. deeper 1B reset
4. bearish structure failure

Each scenario should include:
- estimated probability
- confirming signals
- invalidation signals

### Section 5 — CIO Conclusion
Purpose: produce a decision-quality call.

Must answer:
- most likely 2–8 week path
- what matters next
- what confirms the thesis
- what would break the thesis

---

## Revised Scoring Logic

### Old logic
- Count 4/5 aligned = high confidence

### New logic
Use a weighted hierarchy:

1. **Force regime** (original FF)
2. **Force quality** (FF ROC)
3. **Trend line geometry** (P10)
4. **5-chart structural alignment**

### Proposed interpretation rule
- Structural alignment without improving force = weaker than previously assumed
- Strong force without trend line clearance = likely test, not confirmed breakout
- Bullish state + falling ROC into resistance = late-markup / reset risk
- Bullish state + rising ROC at support = reload / breakout attempt quality improving

---

## Recommended Development Sequence

### Phase 1 — Re-Scope and output redesign
- Approve this spec
- Update project tracker language
- Treat P10 as explicit dependency

### Phase 2 — `mstr_suite_report.py` revision
Refactor the script to output:
- structural state
- force diagnostics
- trend line geometry
- scenario probabilities
- bottom-line CIO call

### Phase 3 — Validation
Backtest whether:
- FF ROC improves signal quality versus static alignment
- trend line geometry improves path forecasting
- combined force + geometry outperforms chart-count alignment alone

### Phase 4 — Automation
After output design and validation are acceptable:
- Friday reminder
- Friday report
- on-demand generation retained

---

## Immediate Build Priorities

### Priority 1
Inspect `mstr_suite_report.py` and classify:
- reusable pieces
- obsolete alignment-only assumptions
- where FF / ROC / trend line sections should be inserted

### Priority 2
Define a minimal trend line interface for the suite report:
- line type
- anchor points
- current projected value
- distance from price
- fit / confidence metric

### Priority 3
Build the first force-aware report draft for live discretionary use before automation.

---

## Working Decision Rule

Until quantitative validation is complete:

- **Use original FF for state**
- **Use FF ROC for tactical interpretation**
- **Use trend line geometry to determine whether force is sufficient to break or more likely to reset**
- **Use the 5-chart suite for corroboration, not as the sole driver**

---

## Success Condition

The suite is working when it can reliably answer:

> “MSTR is in [state], force is [improving/fading], price is confronting [line], and the highest-probability path over the next 2–8 weeks is [scenario], unless [invalidating condition] occurs.”

That is the actual end product.
