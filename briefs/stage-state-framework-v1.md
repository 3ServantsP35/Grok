# Stage State Framework — v1.1
**Author:** CIO
**Approved by:** Gavin (rizenshine5359)
**Date:** 2026-03-03 (v1.0) | Updated 2026-03-03 (v1.1)
**Status:** ACTIVE

---

## Purpose

This document formalizes the Stage State Taxonomy, Confirmation Ladders, LEAP Attractiveness scoring, and Portfolio Implications used in Market Structure Reports. It is the canonical reference for all stage declarations across assets tracked by the engine.

---

## The 10 Stage States

| Code | Name | Plain Language |
|---|---|---|
| **S1** | Accumulation | Price below realized value. Bear structure intact but exhaustion building. Smart money entering. |
| **S1→2** | Breakout Formation | LOI rising from trough. VLT recovering. Pre-breakout window. AB1 entry zone. |
| **S2** | Markup | Trending bull. Slow Trackline green/orange, no red. AB2 income active. |
| **S2C** | Stage 2 Continuation | Mid-bull correction within an intact trend. NOT a top. Confirmed by classifier. |
| **S2→3** | Distribution Warning | First structural deterioration signal. Possible top forming. Could still recover. |
| **S3** | Distribution | Confirmed top formation. Exit zone. |
| **S3→4** | Markdown Initiation | Trend broken. Bear structure forming. |
| **S4** | Markdown | Bear trend confirmed. Slow Trackline red dominant. LOI falling. |
| **S4C** | Stage 4 Continuation | Bear market bounce. Temporary. Does NOT change trend. |
| **S4→1** | Bottom Formation | Trough conditions met. Stage 1 criteria approaching. AB3 deployment zone. |

---

## Threshold Differentiation by Asset Class

> ⚠️ Thresholds below reflect Momentum assets. MR asset thresholds require backtesting validation before standardization.

| Parameter | Momentum (MSTR, TSLA, IBIT) | MR (SPY, QQQ, GLD, IWM) |
|---|---|---|
| S4→1 Watch LOI threshold | ≤ -45 | ≤ -40 |
| DELTA_MGMT LOI threshold | > +40 | > +20 |
| AB3 full entry CPS threshold | TBD (backtest) | TBD (backtest) |

> **Backtest item:** Validate whether confirmation ladder thresholds should differ between Momentum and MR assets. Specifically: VLT Recovery Clock timing, CPS minimums, LT SRIBI slope sensitivity. See `active-tasks.md`.

---

## Confirmation Ladders

Each transition has three tiers: **Watch** (possible), **Forming** (probable), **Confirmed** (actionable).

Tiers are sequential — Forming cannot be declared without Watch conditions met. Confirmed cannot be declared without Forming conditions met.

---

### S4→1 — Bottom Formation → Accumulation
*AB3 entry zone. Most consequential transition — getting it wrong in either direction is expensive.*

**WATCH triggers:**
- LOI crosses below -45 (Momentum) / -40 (MR)
- First candidate trough visible
- Howell phase not at peak Turbulence (T score ≥ +5 with conf > 50% = Watch suppressed)

**FORMING conditions (all required):**
- VLT trough confirmed — deceleration arrested, first uptick visible
- STH-MVRV < 1.0
- Episode type: Structural (CPS-typing system)
- IWM state: broad flush (LT<0 + VLT<0) OR IWM also at trough concurrently

**CONFIRMED conditions (all required):**
- VLT Recovery Clock ≤ 6 bars above zero
- CPS ≥ threshold (pending calibration)
- LT SRIBI slope turning (not yet positive — direction change sufficient)
- BTC bottom confirmed (LT SRIBI positive on BTC or STH-MVRV recovery)
- Howell Gate Zero passes (phase ≠ Turbulence, or T score declining)

**INVALIDATION:**
- VLT still negative at 20 bars after Watch fires
- LOI makes new low below prior Watch trough level
- Howell transitions to T score ≥ +5 with conf > 50%
- BTC breaks below prior cycle low with volume > 2x ADV

**Confirmation score guidance:**
- Watch only: AB3 awareness, begin STRC reduction gradually
- Forming: AB3 25% first tranche eligible
- Confirmed: AB3 full sizing per deployment rules

---

### S4C — Stage 4 Continuation (Bear Rally)
*The dangerous state. Looks like S4→1 early. Distinguishing this from S4→1 protects capital.*

**WATCH triggers:**
- Price bounces 5–15% off LOI trough
- VLT shows uptick
- BUT LOI has NOT crossed -45 threshold (Momentum) — bounce without depth

**FORMING conditions:**
- VLT Recovery Clock slow: 7–12 bars (sluggish recovery)
- CPS below threshold
- IWM strong at trough (narrow selling — breadth divergence pattern)
- LT SRIBI shows no slope change

**CONFIRMED conditions:**
- VLT fails to sustain above zero
- LOI rolls back below prior level
- Price retraces > 50% of bounce
- BTC also showing failed recovery (BTC LT SRIBI remains negative)

**INVALIDATION (reclassify as S4→1):**
- LOI breaks below -45 on next leg down
- VLT Recovery Clock resolves ≤ 6 bars on re-test

**Portfolio implication:**
- No AB3 new entries
- Hold existing AB3 LEAPs from prior cycle — do not exit prematurely
- AB2 gate stays NO_CALLS
- Watch re-test of trough for true S4→1 Watch entry

---

### S2C — Stage 2 Continuation (Mid-Bull Correction)
*Healthy pause within an intact uptrend. Classifier is designed to confirm this state in real-time.*

**WATCH triggers:**
- LOI pulls back from positive territory
- Slow Trackline shows first orange bar after extended green run

**FORMING conditions:**
- VLT corrects but LT SRIBI remains positive
- IWM shows headwind (LT<0 + VLT<0) — broad flush, not isolated
- CPS score ≥ 55
- Howell phase eligible (Rebound, Calm, or Speculation)

**CONFIRMED conditions:**
- VLT Recovery Clock resolves ≤ 6 bars
- CPS ≥ 65
- Slow Trackline: no red bars during correction
- IWM begins recovering concurrently with MSTR

**INVALIDATION (reclassify as S2→3 Warning):**
- Slow Trackline produces 3+ consecutive red bars
- CPS < 40
- IWM strong while SPY/QQQ corrects (BREADTH_DIVERGENCE alert)

**Portfolio implication:**
- Hold AB3 LEAPs — do not exit
- AB2 call-selling pauses at trough, resumes at Confirmed
- AB1 add eligible on Confirmed if LOI re-accelerates

---

### S2→3 — Distribution Warning → Stage 3
*Hardest call. False positives are common. Multiple confirmation required before acting.*

**WATCH triggers:**
- First red bar on Slow Trackline after extended S2 run
- SRIBI showing deceleration at distribution levels
- LOI retreating from trim zone

**FORMING conditions (all required):**
- 3+ consecutive red bars on Slow Trackline
- SRIBI negative zero-cross with ≥ 30 magnitude prior peak
- IWM strong while SPY/QQQ corrects (BREADTH_DIVERGENCE signature)

**CONFIRMED conditions (all required):**
- LT SRIBI turns negative
- STH-MVRV declining from peak
- LOI crosses below DELTA_MGMT threshold
- Howell phase transitioning from Calm/Speculation toward Turbulence

**INVALIDATION:**
- Slow Trackline returns to green within 3 bars
- LT SRIBI recovers above zero
- Price makes new high above prior peak

**Portfolio implication:**
- Watch: Tighten AB2 delta — reduce to minimum allowed range
- Forming: Close AB1 positions; halt new AB3 entries
- Confirmed: Begin AB3 trim schedule (25% at LOI +20, phased per distribution rules); exit AB1 entirely

---

### S1→2 — Breakout Formation (AB1 Entry Zone)
*Pre-breakout. AB1 is specifically designed for this window.*

**WATCH triggers:**
- S4→1 Confirmed declared
- LOI rising from trough
- Slow Trackline shifting orange

**FORMING conditions:**
- LT SRIBI crossing zero from below with ≥ 20 magnitude
- STH-MVRV approaching 1.0 from below
- Slow Trackline: sustained orange, no red
- LOI > -20 and accelerating upward
- Howell phase: Rebound or Calm

**CONFIRMED conditions:**
- Slow Trackline: first sustained green bar
- LT SRIBI positive and holding
- LOI positive
- Price making higher highs with volume confirmation

**INVALIDATION:**
- VLT reversal below zero after Watch fires
- LT SRIBI fails at zero and turns back negative
- Price breaks below Stage 1 support level

**Portfolio implication:**
- AB1 entry at Forming (pre-breakout is the design purpose of AB1)
- AB3 already deployed at S4→1; no new adds needed
- AB2 gate activates on Confirmed — begin call-selling cycle

---

## LEAP Attractiveness Score

A 0–10 composite output for each Market Structure Report. Maps directly to stage state with modifiers.

### Base Score by State

| Score | Stage State |
|---|---|
| 9–10 | S4→1 Confirmed / S1 |
| 7–8 | S4→1 Forming / S1→2 Watch |
| 5–6 | S1→2 Forming / S2C Confirmed |
| 3–4 | S2 / S2C Watch / S2C Forming |
| 1–2 | S2→3 Watch / Forming |
| 0 | S3 / S3→4 / S4 / S4C |

### Active Modifiers

| Condition | Adjustment |
|---|---|
| Howell Turbulence active (any confidence) | –1.5 |
| Howell Turbulence high confidence (conf > 50%) | –2.0 (replaces above) |
| BTC bottom not confirmed (for MSTR/IBIT) | –0.5 |
| GLI Z-score negative (contraction) | –0.5 |
| IWM breadth: strong at trough (narrow selling) | –1.0 |
| Howell Rebound confirmed | +1.0 |
| BTC LT SRIBI positive | +0.5 |
| mNAV < 1.0x (MSTR-specific) | +0.5 (discount creates structural margin of safety) |

**Floor: 0. Ceiling: 10.**

### Action thresholds

| Score | AB Implication |
|---|---|
| ≥ 8 | AB3 full entry eligible — deploy per capital rules |
| 6–7 | AB3 first tranche (25%) eligible if Forming rungs cleared |
| 4–5 | Watch only — STRC holding is correct |
| ≤ 3 | No entry — reduce existing exposure per distribution rules |

---

## Standardized Portfolio Implications by Stage

| Stage | AB3 Entry | AB3 Hold | AB2 Call-Selling | AB1 | AB4 / STRC |
|---|---|---|---|---|---|
| S4→1 Watch | 25% tranche if Forming rungs clearing | Hold | NO_CALLS | Watch begins | Primary posture |
| S4→1 Forming | 25% tranche eligible | Hold | NO_CALLS | Watch | Reduce gradually |
| S4→1 Confirmed | Full sizing | Hold | NO_CALLS | Watch → Forming | Deploy per signal |
| S1 | Hold — no new adds | Hold | NO_CALLS | Active | Minimal |
| S1→2 Watch | Hold | Hold | NO_CALLS | Entry eligible | Minimal |
| S1→2 Confirmed | Hold | Hold | Activates | Active | Minimal |
| S2 | Hold | Hold | Active — OTM_INCOME | Active | Minimal |
| S2C Watch/Forming | Hold | Hold | Pause | Hold | Minimal |
| S2C Confirmed | Hold | Hold | Resume | Add eligible | Minimal |
| S2→3 Watch | No new | Hold | Tighten delta | Exit |Rebuild |
| S2→3 Confirmed | No new | Begin trim | Pause | Exit fully | Rebuild aggressively |
| S3 / S3→4 | No | Trim schedule | Pause | None | Full rebuild |
| S4 / S4C | No | Hold legacy | NO_CALLS | None | Primary posture |

---

## Report Cadence

- **Scheduled:** Weekly, Monday mornings, all tracked assets
- **On-demand:** Any time a stage rung confirmation or invalidation event fires, or upon request
- **Location:** `/workspace/market-structure-reports/`
- **Naming:** `market-structure-report-{ASSET}-{YYYY-MM-DD}.md`

---

---

## Platform Value Modifier (v1.1)

### Concept

The Platform Value modifier captures the yield delta between what STRC currently provides and what a functioning PMCC platform would generate. It answers: *how much incremental income per month is the portfolio forfeiting by not having the LEAP infrastructure in place?*

STRC yield is the floor and counts as current income. The Platform Value modifier is not triggered by income being zero — it is triggered by the gap between STRC yield and the achievable PMCC yield remaining uncaptured due to insufficient LEAP coverage.

### Income Framework Defaults

| Parameter | Default | Notes |
|---|---|---|
| Income target | 2.0%/month | Applied to deployable capital (excl. 10% hard cash floor) |
| STRC hurdle rate | 0.83%/month | Always counts as current income; sets the yield floor |
| Acceptable monthly range | 0–5% | High volatility tolerance; monthly swings are expected |
| Structural shortfall threshold | > 0.25% gap | Below this, no modifier applies — PMCC is adequately covering |

### Yield Delta Calculation

```
Yield Delta = Income Target − Current Yield
Current Yield = STRC yield on AB4 + active PMCC yield on existing LEAPs
```

The PMCC incremental potential (above STRC) depends on IV regime at gate-open:
- MSTR IV 82% (current): PMCC yields ~3–5%/month above STRC when gate is open
- MSTR IV normal (50–70%): ~1.5–3%/month above STRC
- MSTR IV low (<30%): PMCC paused; STRC is sole income source

### Platform Value Modifier Tiers

| Yield Delta | Tier | Modifier |
|---|---|---|
| > 1.0%/month | HIGH | +1.5 |
| 0.5–1.0%/month | MEDIUM | +1.0 |
| 0.25–0.5%/month | LOW | +0.25 |
| < 0.25%/month | None | 0 |

### Gate Proximity Bonus

When the AB2 income gate is expected to open imminently (LOI recovering toward threshold), Platform Value increases because the time-to-income is short — early LEAP acquisition now directly enables income within weeks.

| LOI Distance from Gate | Bonus |
|---|---|
| Within 10 pts of -20 (gate opening soon) | +0.5 |
| 10–30 pts from -20 | +0.25 |
| > 30 pts from -20 | 0 |

**Maximum Platform Value modifier: +2.0**

---

## Risk/Reward Modifier (v1.1)

Captures structural value asymmetry when fundamental discount is exceptional. Applies independently of Platform Value.

| Condition | Modifier |
|---|---|
| mNAV < 1.0x (MSTR below BTC NAV) | +0.5 |
| Floor-to-current price < 15% | +0.5 |
| Cycle target > 3x current price | +0.25 |

**Maximum Risk/Reward modifier: +1.25**

---

## Updated LEAP Attractiveness Score (v1.1)

### Full modifier set

| Category | Condition | Adjustment |
|---|---|---|
| **Negative — Macro** | Howell Turbulence active (any confidence) | −1.5 |
| | Howell Turbulence high confidence (conf > 50%) | −2.0 (replaces above) |
| | GLI Z-score negative (contraction) | −0.5 |
| **Negative — Signal** | BTC bottom not confirmed (MSTR/IBIT only) | −0.5 |
| | IWM strong at trough (narrow selling) | −1.0 |
| **Positive — Macro** | Howell Rebound confirmed | +1.0 |
| | BTC LT SRIBI positive | +0.5 |
| **Positive — Value** | mNAV < 1.0x | +0.5 |
| | Floor-to-current < 15% | +0.5 |
| | Cycle target > 3x current | +0.25 |
| **Positive — Platform** | Yield delta HIGH (> 1.0%/month) | +1.5 |
| | Yield delta MEDIUM (0.5–1.0%) | +1.0 |
| | Yield delta LOW (0.25–0.5%) | +0.25 |
| | Gate proximity bonus (LOI within 10 pts) | +0.5 |
| | Gate proximity partial (LOI 10–30 pts) | +0.25 |

**Floor: 0. Ceiling: 10.**

### Action thresholds

| Score | Action |
|---|---|
| ≥ 8 | AB3 full entry — deploy per capital rules |
| 6–7 | **Anticipatory tranche** — first partial entry eligible (see below) |
| 4–5 | Watch only — hold STRC, monitor ladder |
| ≤ 3 | No entry — reduce exposure per distribution rules |

### Anticipatory Tranche Rules

An anticipatory tranche is a structured early partial entry — smaller than full AB3 sizing — taken when Platform Value or Risk/Reward modifiers push the score into the 6–7 range before full confirmation.

**Eligibility:**
- Score 6–7 (modifiers pushing above 5, below 8)
- At least one Forming rung confirmed on the ladder
- NO_CALLS gate accepted — entry is for platform positioning, not immediate income
- Income gate expected to open within 30 days (LOI recovery trajectory confirms)

**Sizing:**
- Default: 25% of target AB3 allocation
- Income urgency overrides (yield delta HIGH + gate proximity HIGH): up to 35%
- Never: full AB3 sizing on anticipatory tranche alone

**Accounting:**
- Recorded separately in trade_log with `entry_type = ANTICIPATORY`
- Hypothesis block required: primary hypothesis must address timing uncertainty explicitly
- Kill condition: LOI makes new low below prior Watch trough → close immediately

---

## Personalized Portfolio Report (PPR)

### Concept

The PPR is the personal counterpart to the Market Structure Report. Where the MSR answers *what is the market doing*, the PPR answers *what should you specifically do about it, given your portfolio state and income profile*.

The MSR is shared and objective. The PPR is private and individual. They are downstream of each other: the PPR imports the MSR's stage declaration and base score, then applies the user's portfolio context to produce a personalized score, adjusted action thresholds, and sized trade guidance.

### Privacy rules — NON-NEGOTIABLE

- PPR is generated **only within the user's dedicated channel** (#mstr-greg, #mstr-gavin, #mstr-gary)
- PPR is **never committed to GitHub** — not even anonymized versions
- PPR is **never shared cross-channel** — Greg's PPR is never visible to Gavin or Gary and vice versa
- PPR may be stored in `/mnt/mstr-data/mstr.db` (private DB) but never in `/workspace/briefs/` or any repo-linked path

### Generation workflow

1. User requests PPR in their dedicated channel (on-demand only — no scheduled generation)
2. CIO asks: *"Is anything different from your default profile this week?"*
3. If no changes: CIO pulls current state from DB (positions, AB4 level, recent income) and generates
4. If changes: user provides updates; CIO incorporates before generating
5. PPR references the most recent MSR for market context — does not repeat the shared analysis
6. Report stays in the channel

### User profile schema

Each user has a profile that governs PPR generation:

```
income_target:       2.0%/month (default; user-adjustable)
income_range:        0–5%/month (acceptable volatility band)
strc_hurdle:         0.83%/month (fixed — STRC benchmark)
cash_floor:          10% (hard minimum, true cash only)
deploy_gate:         8.0 (full AB3 entry threshold; user-adjustable)
anticipatory_gate:   6.0 (anticipatory tranche threshold; user-adjustable)
anticipatory_size:   25% of target AB3 allocation (user-adjustable)
risk_posture:        standard / research / educational
```

**Current profiles:**

| User | Income Target | Deploy Gate | Anticipatory Gate | Risk Posture | PPR Channel |
|---|---|---|---|---|---|
| Greg | 2.0%/month | 8.0 | 6.5 | Standard | #mstr-greg |
| Gavin | 2.0%/month | 7.5 | 6.0 | Research | #mstr-gavin |
| Gary | N/A | N/A | N/A | Educational | #mstr-gary |

> Note: Greg and Gavin's deploy gates and anticipatory gates are provisional. Each user can tune these in their dedicated channel. Gary's profile activates when a portfolio is established.

### PPR structure

1. **Portfolio snapshot** — current positions, AB4 level, recent income (last 30 days)
2. **Income engine status** — current yield vs. target; yield delta; Platform Value tier
3. **MSR reference** — stage, base score (pulled from latest MSR; not repeated in full)
4. **Personalized score** — base score + user-specific modifiers applied
5. **Action recommendation** — specific to user's score, gate, and current portfolio state
6. **Sizing guidance** — tranche size, strike/expiry range, budget from AB4
7. **Hypothesis block** — required for any recommended entry (same format as trade recs)

---

## Report Architecture Summary

| Report | Audience | Cadence | Privacy | Location |
|---|---|---|---|---|
| Market Structure Report (MSR) | All — shared | Weekly Monday AM + on-demand | Public-safe | `/workspace/market-structure-reports/` |
| Personalized Portfolio Report (PPR) | Individual only | On-demand only | Private — channel only | Discord channel + DB |
| Stage State Framework (this doc) | All — reference | Updated as needed | Public-safe | `/workspace/briefs/` |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2026-03-03 | Initial framework. Approved by Gavin. |
| v1.1 | 2026-03-03 | Added: Platform Value modifier, Risk/Reward modifier, updated LEAP Attractiveness Score, Anticipatory Tranche rules, PPR spec and privacy rules, Report Architecture summary. Approved by Gavin. |

---

*Pending: MR vs Momentum threshold differentiation (backtest validation required before publishing MR-specific thresholds)*
