# SRI AB1-2 Top Formation - MSTR — Spec v1
**Date:** 2026-03-29  
**Owner:** CIO / Gavin  
**Status:** Draft v1  
**Purpose:** Define a dedicated MSTR-specific topping-formation indicator that combines the tactical role previously split across AB1 and AB2 bearish interpretation into one staged conviction framework.

---

## 1. Indicator Identity

### Title
`SRI AB1-2 Top Formation - MSTR`

### Short Name
`AB1-2 MSTR`

### Scope
This indicator is **MSTR-specific**.

It is not intended to be a generic topping indicator for all assets. MSTR’s:
- volatility,
- BTC sensitivity,
- squeeze behavior,
- and support-vacuum dynamics

justify a dedicated design tuned to its own behavior.

---

## 2. Objective

The indicator should answer one question:

> **How far along is the current MSTR topping formation, and is it now viable for AB1 tactical bearish monetization or AB2 directional bearish positioning?**

It should replace confusing overlap between separate AB1 and AB2 bearish overlays with a single staged topping monitor.

---

## 3. Core Design Principle

### The ladder is made of topping phases
- Phase A — Rejection / Exhaustion
- Phase B — Deterioration / Compression Collapse
- Phase C — Structure Break / Tactical Failure
- Phase D — Support Vacuum / Downside Release

### The signals inside each phase are:
- non-sequential,
- role-based,
- weighted,
- and clustered.

This means the indicator should **not** require a rigid step-by-step signal order.

---

## 4. Output Architecture

## Primary visual output
The primary output should be **candle-specific markers above bars**.

### Marker family
Use a single letter marker:
- **T** = topping formation

### Marker colors and meaning

#### Green T
- topping process begins
- early warning only
- not yet a trade by itself

#### Yellow T
- topping process confirmed enough
- **AB1 viable**
- tactical bearish monetization state

#### Red T
- topping process mature enough
- **AB2 viable**
- directional bearish credibility active

---

## 5. Marker Trigger Logic (Conceptual v1)

## Green T — Topping Begins
Print once when the topping score crosses into early-warning territory.

### Intended meaning
- Phase A active
- or early Phase B developing
- local top suspicion is now real enough to mark historically

### Suggested conditions
- at least one rejection / exhaustion signal
- plus at least one deterioration signal
- but not yet enough for tactical activation

---

## Yellow T — AB1 Viable
Print once when the topping process crosses into tactical trade viability.

### Intended meaning
- late Phase B or Phase C
- internal deterioration cluster active
- structure beginning to fail
- tactical call-sale / bearish monetization now justified

### Suggested conditions
- topping score crosses AB1 threshold
- and downside path is sufficient for a fast move

---

## Red T — AB2 Viable
Print once when the topping process matures into directional bearish credibility.

### Intended meaning
- Phase C to D transition or full Phase D
- broader structure failure present
- failed reclaim behavior visible
- support vacuum active
- bearish move no longer just tactical

### Suggested conditions
- topping score crosses AB2 threshold
- LT participation visible
- directional downside path credible

---

## 6. Signal Buckets

The indicator should derive conviction from weighted buckets.

## Bucket A — Rejection / Exhaustion
Examples:
- rejection candle at key resistance
- upper-wick rejection
- failed reclaim
- failure at turquoise resistance

## Bucket B — Deterioration / Compression Collapse
Examples:
- ST green collapses onto blue robust fit
- LT green collapses onto blue robust fit
- reversal band slope turns down
- green expansion compresses bearishly

## Bucket C — Structure Break / Tactical Failure
Examples:
- price crosses below ST slow trackline
- ST red support band crosses below ST slow trackline
- fast tracklines turn bearish / red
- robust-fit line begins acting as resistance

## Bucket D — Support Vacuum / Downside Release
Examples:
- VLT blue robust-fit too far below price to help now
- LT red support too far below price to help now
- downside air pocket exists
- lower turquoise support becomes the only meaningful nearby catch zone

## Bucket E — FF ROC Tactical Deterioration
Examples:
- ROC cluster turns negative
- acceleration deteriorates
- force weakens before the broader structure fully breaks

---

## 7. Suggested Scoring Concept (v1)

### Suggested initial weighting
- Bucket A evidence: **+1 each**
- Bucket B evidence: **+1 each**
- Bucket C evidence: **+1 each**
- Bucket D support-vacuum evidence: **+2 primary / +1 secondary**
- Bucket E FF ROC deterioration: **+2 primary / +1 secondary**

### Suggested state mapping
- **0–2:** no marker / inactive
- **3–4:** Green T
- **5–6:** Yellow T
- **7+:** Red T

This is a starting framework only and should be validated on live chart/CSV replay.

---

## 8. MSTR-Specific Calibration Priorities

This indicator should be tuned specifically for MSTR’s behavior.

### Priority calibration areas
1. **Support-vacuum distance threshold**
   - what gap between price and VLT/LT support is meaningful for MSTR?
2. **Fast trackline failure threshold**
   - how much emphasis should early ST failure carry?
3. **FF ROC tactical deterioration sensitivity**
   - how early should force deterioration begin to matter?
4. **ST vs LT weighting**
   - MSTR often tops tactically before LT fully rolls; this should be reflected.
5. **Failed reclaim threshold**
   - MSTR often traps aggressively around failed reclaim levels.

---

## 9. Table Design

The table should be minimalist and directly decision-oriented.

### Required fields only
- **Status**
- **Phase**
- **Conviction**
- **AB1 viability**
- **AB2 viability**
- **Invalidation**

### Suggested table meanings

#### Status
- Inactive
- Green T active
- Yellow T active
- Red T active

#### Phase
- A / B / C / D
or optional plain-English labels

#### Conviction
- Low / Medium / High
or numeric score

#### AB1 viability
- No
- Watch
- Yes

#### AB2 viability
- No
- Developing
- Yes

#### Invalidation
- key reclaim / structure recovery level that negates the topping read

### Exclude
- irrelevant multi-asset references
- old broad legend clutter
- general bullish-entry educational rows

---

## 10. Tracklines in This Indicator

### Recommended default
- **Fast trackline ON by default**
- **Slow trackline optional**

### Why
The fast trackline is especially valuable here because this indicator is trying to detect topping / tactical failure **early**, before slower structure fully confirms.

Fast trackline failure is therefore a core part of the topping model.

---

## 11. Alerts

The alert set should mirror the marker transitions.

### Alert 1
**Green T — Topping Begins**
- local top process beginning
- warning only

### Alert 2
**Yellow T — AB1 Viable**
- topping formation now tactically tradable
- call-sale / tactical bearish monetization state

### Alert 3
**Red T — AB2 Viable**
- topping formation now directionally credible
- broader bearish setup maturing

### Alert 4 (optional)
**Topping invalidated**
- failed topping structure undone by reclaim / re-expansion

---

## 12. Relationship to Existing Scripts

### Immediate role
This should begin as a **new dedicated indicator**.

### Why not replace AB1/AB2 immediately
- lower implementation risk
- easier validation
- cleaner chart review
- easier calibration against fresh CSVs

### Longer-term option
If the new indicator proves clearly superior, older bearish overlay logic in AB1 and AB2 can later be simplified or retired.

---

## 13. One-Sentence Summary

> `SRI AB1-2 Top Formation - MSTR` should be a dedicated MSTR-specific topping indicator that stages bearish conviction using Green/Yellow/Red T markers above candles, with a minimal table focused only on current status, conviction, and AB1/AB2 trade viability.
