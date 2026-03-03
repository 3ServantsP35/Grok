# Updated Alert Approach — Architecture-Layer Alert Framework v1.0
**Date:** 2026-03-03
**Status:** Proposal — awaiting Gavin review
**Author:** CIO

---

## The Fundamental Shift

**Old model:** Alerts fire when a trade is ready. The alert *is* the trade signal.

**New model:** Alerts fire when the *state of a layer changes*. Each layer of the architecture has its own event vocabulary. A Layer 0 alert (GLI regime shift) is macro context. A Layer 3 alert (entry signal) is directly actionable. Users understand where in the architecture the change occurred and can interpret it accordingly.

This is a monitoring architecture, not a trading notification system. The analogy: a weather service that tells you "pressure is dropping" (Layer 0), then "clouds forming" (Layer 1), then "rain likely in 2 hours" (Layer 2), then "get your umbrella now" (Layer 3). Each alert is useful even if the later ones never fire.

---

## Alert Taxonomy — Five Layers

---

### Layer 0 — GLI (Global Liquidity)
*Fires rarely. When it does, it changes the base rate for every signal below it.*

| Alert Code | Trigger | Significance |
|---|---|---|
| `GLI_REGIME_SHIFT` | Z-score crosses zero (positive → negative or negative → positive) | Major: bullish/bearish base rate changes by ~20% across all assets |
| `GLI_ZSCORE_EXTREME` | Z-score crosses ±1.0 | Elevated: strong contraction or expansion signal |
| `GEGI_CROSS` | GEGI crosses 1.0 | Bullish/bearish: liquidity growth above/below asset price growth |

**Routing:** #mstr-cio-alerts | **Cadence:** On trigger only | **Frequency:** Expected: 2–6x per year

---

### Layer 0.5 — Howell Phase Engine
*Fires on macro cycle transitions. Sets Gate Zero eligibility for all entries.*

| Alert Code | Trigger | Significance |
|---|---|---|
| `HOWELL_PHASE_TRANSITION` | Phase changes (existing) | Gate Zero eligibility changes for one or more assets |
| `HOWELL_CONFIDENCE_SHIFT` | Confidence crosses 50% threshold (low → high or high → low) | Phase call strengthens or weakens |
| `HOWELL_SECTOR_FLIP` | Any key sector (XLK, XLY, XLF) flips BEAR → NEUTRAL or NEUTRAL → BULL | Early leading indicator of phase transition |
| `HOWELL_GATE_ZERO_CHANGE` | Gate Zero status changes for a specific asset (blocked → eligible or eligible → blocked) | Direct entry eligibility change — most actionable Layer 0.5 alert |

**Routing:** #mstr-cio-alerts | **Cadence:** On trigger | **Frequency:** Expected: 1–3x per month

---

### Layer 1 — Regime Engine (LOI Gate States)
*Fires when an asset's structural position changes. Income and LEAP posture changes.*

| Alert Code | Trigger | Significance |
|---|---|---|
| `LOI_THRESHOLD_CROSS` | LOI crosses any key level: −45 (Momentum Watch), −40 (MR Watch), −20, 0, +20 (MR DM), +40 (Momentum DM) | Stage state transition may follow; gate state change imminent |
| `GATE_STATE_CHANGE` | AB2 gate changes: NO_CALLS → OTM_INCOME → DELTA_MGMT (or reverse) | Income eligibility changes immediately |
| `LOI_TROUGH_CONFIRMED` | LOI reverses upward after reaching below −45 (Momentum) or −40 (MR) | VLT Recovery Clock starts; Watch phase formally begins |
| `LOI_ROLLOVER` | LOI reverses downward after reaching above +40 (Momentum) or +20 (MR) | Distribution trim schedule initiates |
| `MNAV_THRESHOLD` | MSTR mNAV crosses 1.0x, 1.5x, 2.0x, 3.0x | MSTR/IBIT relative weight signal; pair trade implication |

**Routing:** Asset-specific channels and #mstr-cio-alerts | **Cadence:** On trigger | **Frequency:** Expected: 3–8x per month across all assets

---

### Layer 2 — Signal Engine (Stage State, CPS, VLT Clock)
*Fires on confirmation ladder events. Most dense layer — fires multiple times per transition.*

| Alert Code | Trigger | Significance |
|---|---|---|
| `STAGE_WATCH_DECLARED` | Confirmation ladder Watch conditions met | Monitor begins; small initial positioning may be warranted |
| `STAGE_FORMING_DECLARED` | Confirmation ladder Forming conditions met | First tranche consideration if score qualifies |
| `STAGE_CONFIRMED` | All confirmation conditions met | Full entry eligible (pending personal gate) |
| `STAGE_INVALIDATED` | Invalidation conditions met on an active transition | Stop monitoring; reset to prior stage |
| `LEAP_SCORE_CHANGE` | MSR LEAP Attractiveness Score crosses 4, 6, 7, or 8 | Actionability threshold changes |
| `VLT_CLOCK_START` | VLT Recovery Clock starts (LOI trough confirmed + VLT first crosses zero) | Begin counting; 6-bar target in effect |
| `VLT_CLOCK_RESOLVED` | VLT clock resolves ≤ 6 bars | Strong timing confirmation; +0.5 to score |
| `VLT_CLOCK_WARNING` | VLT clock at 12 bars without resolution | Reduce sizing to 75%; conviction weakening |
| `VLT_CLOCK_ABORT` | VLT clock at 20 bars without resolution | Exit any anticipatory tranche; thesis broken |
| `CPS_THRESHOLD` | CPS crosses 55, 65 (once wired) | Classifier confidence milestones |
| `BREADTH_DIVERGENCE` | IWM strong while SPY/QQQ correcting (LOI divergence) | SPY/QQQ entry BLOCKED — narrow selling signal |
| `TRENDLINE_PROXIMITY` | Price within 2% of a key trend line (when Trend Line Engine built) | Test imminent; watch for break or bounce |
| `TRENDLINE_BREAK` | Confirmed price break of a key trend line with volume | Stage State implication depends on context |

**Routing:** Asset-specific channels and #mstr-cio-alerts | **Cadence:** On trigger | **Frequency:** Expected: 5–15x per month across all assets

---

### Layer 3 — Allocation Engine (Entry/Exit Actions)
*Fires when a specific portfolio action is warranted. Highest actionability.*

| Alert Code | Trigger | Significance |
|---|---|---|
| `ANTICIPATORY_TRANCHE_ELIGIBLE` | MSR score ≥ 6 + Forming rung confirmed + income gate expected within 30 days | First tranche consideration — see PPR for sizing |
| `FULL_ENTRY_SIGNAL` | MSR score ≥ 8 (all modifiers applied) | Full AB3 deployment authorized — see PPR |
| `AB2_INCOME_GATE_OPEN` | Gate state changes to OTM_INCOME or DELTA_MGMT | Begin call-selling cycle on this asset |
| `AB2_INCOME_GATE_CLOSED` | Gate state changes to NO_CALLS | Stop selling calls; protect LEAP upside |
| `TRIM_SCHEDULE_TRIGGER` | LOI crosses +20 (first trim), +40 (second), +60 (third) | Begin reducing AB3 position per trim schedule |
| `KILL_CONDITION` | VLT clock abort, or price breaks kill floor with volume | Exit immediately — thesis broken |
| `AB4_CEILING_BREACH` | AB4 allocation exceeds 25% soft ceiling | Income engine underbuilt — deploy to qualifying signal |
| `WEEKLY_MSR_PUBLISHED` | Every Monday AM | New Market Structure Reports available for all assets |

**Routing:** User-specific dedicated channels (#mstr-greg, #mstr-gavin) | **Cadence:** On trigger | **Frequency:** Expected: 2–5x per month per user

---

## Alert Structure — Standard Format

Every alert follows a consistent structure regardless of layer:

```
[LAYER] ALERT_CODE — ASSET
━━━━━━━━━━━━━━━━━━━━━━━━━━
Layer:     Layer 1 — Regime Engine
Event:     LOI_THRESHOLD_CROSS
Asset:     MSTR
Change:    LOI crossed −45.0 (−46.2) ← Momentum Watch threshold
Previous:  LOI −42.3 (above Watch)
New state: S4→1 WATCH DECLARED

Ladder impact: Watch phase begins. 2 of 11 rungs now cleared.
Stage implication: VLT Recovery Clock will start on next VLT zero-cross.
Score change: Base score unchanged until Forming conditions met.
Watch: VLT trough confirmation | IWM breadth state | Howell Gate Zero

Next expected: LOI_TROUGH_CONFIRMED within 5–10 bars if momentum continues
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Key principles:
- **Context before action:** Every alert states what changed AND what it means in stage context
- **Next watch level:** Always states what the next milestone is
- **No orphaned alerts:** Every alert references the current stage state so the alert is interpretable without prior knowledge
- **Hypothesis linkage:** Layer 3 alerts link to any open trade hypothesis that is affected

---

## Alert Routing Matrix

| Layer | Channel | Who sees it |
|---|---|---|
| Layer 0 (GLI) | #mstr-cio-alerts | All |
| Layer 0.5 (Howell) | #mstr-cio-alerts | All |
| Layer 1 (Regime) | #mstr-cio-alerts | All |
| Layer 2 (Signal) | #mstr-cio-alerts | All |
| Layer 3 (Allocation) | #mstr-greg / #mstr-gavin (dedicated only) | Individual user only |
| PPR trigger | #mstr-greg / #mstr-gavin | Individual user only |

**Layer 3 alerts are never in the shared alerts channel.** Portfolio-specific actions stay in dedicated channels only — privacy rule applies.

---

## Priority / Urgency Levels

| Level | Icon | Description | Example |
|---|---|---|---|
| 🔵 INFO | Blue | State change noted; no immediate action needed | `HOWELL_SECTOR_FLIP` |
| 🟡 WATCH | Yellow | Monitoring threshold crossed; begin watching | `STAGE_WATCH_DECLARED`, `LOI_THRESHOLD_CROSS` |
| 🟠 FORMING | Orange | Transition building; assess positioning | `STAGE_FORMING_DECLARED`, `VLT_CLOCK_START` |
| 🔴 ACTION | Red | Immediate portfolio implication | `FULL_ENTRY_SIGNAL`, `KILL_CONDITION`, `GATE_STATE_CHANGE` |
| ⚫ CRITICAL | Black | Structural regime change | `GLI_REGIME_SHIFT`, `HOWELL_PHASE_TRANSITION` |

---

## What This Replaces vs Extends

| Current system | New system |
|---|---|
| PMCC gate change alert | → Replaced by `GATE_STATE_CHANGE` (Layer 1) — same trigger, richer context |
| Howell phase transition alert | → Replaced by full `HOWELL_PHASE_TRANSITION` (Layer 0.5) + new `HOWELL_GATE_ZERO_CHANGE` |
| No GLI alerts | → New: `GLI_REGIME_SHIFT`, `GLI_ZSCORE_EXTREME`, `GEGI_CROSS` |
| No stage state alerts | → New: entire Layer 2 vocabulary |
| No entry/exit signals | → New: entire Layer 3 vocabulary |
| Alerts mixed with trade recs | → Separated: alerts are state changes; trade recs are separate (Trade Rec Engine, backlog #7) |

---

## Implementation Sequence

**Sprint 1 (after crontab install):**
- Wire Layer 1 LOI threshold alerts (all assets) into `pmcc_alerts.py`
- Wire Layer 0.5 `HOWELL_GATE_ZERO_CHANGE` alert (most immediately useful)
- Wire Layer 2 `LEAP_SCORE_CHANGE` and `VLT_CLOCK_*` alerts (once VLT Clock built)

**Sprint 2:**
- Wire Layer 0 GLI alerts
- Wire Layer 2 Stage State transition alerts (Watch/Forming/Confirmed/Invalidated)
- Wire Layer 3 entry/exit allocation alerts (dedicated channels only)

**Sprint 3:**
- Wire trend line alerts (once Trend Line Engine built)
- Tune alert thresholds based on first month of live data

---

## Open Question for Gavin

**Subscription model:** Should users be able to opt in/out of individual alert codes, or do all users receive all alerts in their routed channels? I recommend all-in as the default (no configuration required), with individual muting possible in Discord at the channel level. But if fine-grained control is important, we can build a subscription table in the DB.

---

*Next step: Gavin reviews and approves alert vocabulary → CIO builds Sprint 1 immediately post-crontab install*
