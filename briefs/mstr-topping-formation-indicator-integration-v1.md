# MSTR Topping Formation Ladder v1 — AB1 / AB2 Indicator Integration Spec
**Date:** 2026-03-29  
**Owner:** CIO / Gavin  
**Status:** Draft v1  
**Depends on:** `briefs/mstr-topping-formation-ladder-v1.md`

---

## 1. Purpose

This document defines how the **MSTR Topping Formation Ladder v1** should be integrated into the AB1 and AB2 indicators.

The topping ladder should not replace the existing AB1 / AB2 logic. It should act as a:
- **meta-layer**,
- **gating layer**,
- **confidence modifier**,
- and **tactical override**

that improves bearish reversal detection and local-top identification.

### 1.1 Updated execution architecture (2026-03-30)
A key refinement emerged from prototype testing:

- **MSTR** should be treated primarily as the **theta / PMCC / premium-harvest vehicle**.
- **BTC / IBIT** should be treated as the cleaner **directional delta-expression layer**.

Implications:
- Continue using MSTR for cheapness detection, capital-base building, PMCC income, and Green-regime call-sale management.
- Do **not** force MSTR to also be the best vehicle for pre-plunge timing, local-bottom detection, or AB2 directional entries.
- Directional AB2-style research should increasingly migrate toward **BTC / IBIT**, where the signal family appears structurally cleaner and less distorted by MSTR-specific business-model effects (dilution, preferred issuance, mNAV dynamics, equity reflexivity).

This means the topping/Yellow/B work on MSTR should be interpreted mainly as **theta-management research**, while directional/exhaustion research that behaves better on BTC should be viewed as a candidate input to a future **BTC/IBIT AB2 stack**.

---

## 2. Key Principle

### Do not hard-code a rigid sequence
The topping ladder should not be implemented as:
- signal 1 then signal 2 then signal 3 then signal 4.

It should be implemented as:
- phase-aware,
- bucket-weighted,
- non-sequential confirmation clustering.

### The ladder is made of phases
- Phase A — Rejection / Exhaustion
- Phase B — Deterioration / Compression Collapse
- Phase C — Structure Break / Tactical Failure
- Phase D — Support Vacuum / Downside Release

### The signals are weighted evidence inside those phases
This is the critical design rule.

---

## 3. Integration Goal by Indicator

## AB1 goal
AB1 should become more sensitive to **early tactical topping formation pressure**.

It should answer:
- is a local top forming?
- is the short-horizon bearish reversal becoming actionable?
- is there enough downside path to monetize tactically?

## AB2 goal
AB2 should only upgrade when the topping formation has progressed into **directional bearish credibility**.

It should answer:
- is this more than a tactical fade?
- has broader deterioration joined the move?
- is there enough directional quality for a larger bearish expression?

---

## 4. Shared Topping Buckets

Both indicators should consume a common topping-pressure input built from these buckets:

### Bucket A — Rejection / Exhaustion
Examples:
- rejection candle at resistance
- upper-wick rejection
- failed breakout
- failed reclaim

### Bucket B — Band Collapse / Deterioration
Examples:
- ST green collapse onto blue
- LT green collapse onto blue
- slope flips down
- bullish band expansion disappears

### Bucket C — Trackline Failure
Examples:
- price below ST slow TL
- support band below ST slow TL
- fast TLs turning red
- robust-fit line turning into resistance

### Bucket D — Support Vacuum / Support-Distance Failure
Examples:
- VLT/LT support too far away to matter now
- open air beneath broken support
- nearest meaningful support materially lower

### Bucket E — FF ROC Tactical Deterioration
Examples:
- ROC cluster negative
- acceleration negative
- base FF still constructive, but ROC tactically bearish

---

## 5. Shared Topping Score (Conceptual)

### Suggested starting score bands
- **0–2:** warning only
- **3–4:** topping pressure watch
- **5–6:** tactical topping active
- **7+:** directional bearish credibility active

This score should not directly fire trades by itself. It should modify / gate AB1 and AB2 behavior.

---

## 6. AB1 Integration Spec

## 6.1 Role
AB1 is the tactical monetization layer.

It should respond earlier in the topping sequence because it is designed for:
- short-horizon moves,
- income-oriented tactical positioning,
- local reversals,
- and fast premium capture.

## 6.2 AB1 topping states
Recommended states:
- **Inactive**
- **Watch**
- **Active**
- **High-Confidence Active**

## 6.3 Suggested mapping

### Inactive
- score 0–2
- only isolated warnings
- no meaningful cluster

### Watch
- score 3–4
- Phase A and/or B present
- topping possible, but not yet strong enough for confident tactical deployment

### Active
- score 5–6
- Phase B/C active
- structure is failing enough for tactical bearish monetization

### High-Confidence Active
- score 7+
- Phase C/D active
- support vacuum present
- FF ROC deterioration confirms downside path

## 6.4 Tactical override for AB1
AB1 should explicitly allow this rule:

> If base Force Field is still constructive, but FF ROC deterioration is clustered and topping score is active, AB1 should turn bearish-active or call-sale favorable even before broader bullish structure fully breaks.

This is a direct protection against missing local tops because the structural backdrop still looks mildly supportive.

---

## 7. AB2 Integration Spec

## 7.1 Role
AB2 is the directional conviction layer.

It should not react as early as AB1. It should require broader evidence that the topping process is no longer just a tactical fade opportunity.

## 7.2 AB2 topping states
Recommended states:
- **Inactive**
- **Developing**
- **Active**

## 7.3 Suggested mapping

### Inactive
- score below 5
- no LT participation
- no credible downside path yet

### Developing
- score 5–6
- AB1 already active
- LT deterioration beginning to appear
- failed reclaim behavior visible

### Active
- score 7+
- Phase C/D active
- LT participation present
- support vacuum present
- failed reclaim structure confirms directional bearish credibility

## 7.4 AB2 confirmation rule
AB2 should require all of the following:
- AB1 active first
- topping score high enough
- LT deterioration visible
- failed reclaim or inability to recover broken level
- enough downside path to justify a directional bearish structure

This prevents AB2 from triggering on shallow tactical noise.

---

## 8. Output Recommendations for Indicators

The indicator layer should expose the topping logic in simple readable states.

### AB1 outputs
- Topping pressure: Low / Medium / High
- Topping state: Inactive / Watch / Active / High-Confidence Active
- Tactical message example: “Tactical topping formation active — call-sale favorable”

### AB2 outputs
- Topping directional credibility: Low / Medium / High
- Topping state: Inactive / Developing / Active
- Directional message example: “Bearish topping formation developing — AB2 directional setup maturing”

---

## 9. Invalidation Rules

Both indicator integrations should use invalidation rules based on the topping process being undone.

### Examples
- reclaim and hold above failed resistance
- bullish re-expansion of ST band
- FF ROC re-accelerates upward
- support vacuum closes because support is reclaimed or nearby support strengthens

### Important principle
A topping signal should not be invalidated by one strong candle.
It should be invalidated when the **failure process reverses structurally**.

---

## 10. Implementation Notes

### Python side
Per project rule, avoid adding new classes directly into `sri_engine.py`.

Recommended approach:
- build the topping logic in a separate module
- import it into the AB1 / AB2 pipeline as a scoring or gating component

### Pine side
Recommended approach:
- add topping-pressure overlay logic as a dedicated section
- do not replace the core AB1 / AB2 logic
- expose topping state visually and optionally as alert conditions

---

## 11. Intended Outcome

This integration should improve the AB1 / AB2 indicators by:
- recognizing local tops earlier,
- avoiding overreliance on residual bullish structure,
- giving FF ROC a true tactical role,
- and distinguishing tactical bearish opportunity from broader directional bearish credibility.

The main objective is to reduce the chance of missing breakdowns like the 134 failure because structural repair still looked possible in isolation.

---

## 12. One-Sentence Summary

> The MSTR Topping Formation Ladder should be integrated into AB1 and AB2 as a weighted, phase-based meta-layer that increases AB1 sensitivity to early topping pressure and requires stronger directional confirmation before AB2 turns actively bearish.
