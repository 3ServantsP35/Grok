# MSTR Chart Suite — Hypothesis Document v1.0
**Project:** P-MSTR-SUITE  
**Date:** 2026-03-05  
**Author:** CIO (from Gavin's hypothesis, sharpened)  
**Status:** Phase 1 Complete — Research pending

---

## Purpose

The MSTR Chart Suite is a focused 5-chart confirmation ladder for assessing MSTR's 30–60 day directional outlook with high probability. It operates *above* the signal layer — not replacing the SRI engine, LOI oscillator, or stage framework, but sharpening the macro/credit/momentum context that those signals operate within.

When 4+ charts align, the directional confidence is high enough to drive weekend portfolio positioning decisions. When signals diverge, the divergence itself is informative — it tells you which layer of the thesis is weakest.

---

## The Confirmation Ladder

| # | Chart | Signal Type | Predictive Horizon | Direction |
|---|-------|------------|-------------------|-----------|
| ① | MSTR SRI LT | Price structure + trend | 30–90d | MSTR price direction |
| ② | STRC SRI LT | Credit stress leading indicator | 7–21d (lead) | BTC/MSTR direction |
| ③ | Stablecoin Dom SRI LT | Capital deployment pressure | 14–45d | Crypto capital flow |
| ④ | STRF/LQD SRI LT | Crypto vs IG credit health | 7–30d | Sector risk appetite |
| ⑤ | MSTR/IBIT SRI LT | MSTR alpha vs BTC | 14–60d | MSTR vs BTC relative |

---

## Chart-by-Chart Signal Specification

### ① MSTR SRI LT — Primary Price Structure

**Gavin's hypothesis:** Price crossing reversal bands and fast/slow tracklines on the LT TF is the primary lens. VST/ST give advance warning. Slope of reversal bands critically important.

**Refined signal hierarchy:**

The LT SRI Forecast displays two distinct signal types that must be tracked separately:

**Regime signals (structure, weeks-to-months):**
- Price crosses above/below **LT Fast Trackline** → LT trend changes
- **LT Fast TL crosses LT Slow TL** → full structural regime change (rare, high conviction)
- **VLT Fast TL direction** → the master timeframe; VLT positive = structural bull; VLT negative = structural headwind

**Entry signals (tactical, days-to-weeks):**
- Price crosses Reversal Support → short-term reversal candidate
- Price reclaims Reversal Robust Fit → trend resumption signal
- Price crosses Reversal Resistance → momentum confirmation

**TF hierarchy (Gavin's established framework):**
- **VLT** = Structure (defines the regime these signals fire into)
- **LT** = Trend (the primary lens per this chart)
- **ST** = Decision (triggers entry)
- **VST** = Timing (executes entries)

**The "advance warning" mechanism:** When ST histogram turns negative while LT is still positive, this is an early warning of LT trend deterioration. It fires 2–5 days before the LT itself turns negative.

**Bullish confirmation (score 1):**
- Price above LT Fast TL AND LT histogram positive

**Critical precision — "slope of reversal bands":**
The slope of the reversal bands represents the *rate of change* of the underlying SRI regression. A steep positive slope = momentum accelerating; flat = momentum stalling; negative = reversal risk. The slope of the **Slow Trackline** is the structural confirmation — if the Slow TL slope turns positive, the bull trend is validated.

---

### ② STRC SRI LT — BTC Credit Stress Leading Indicator

**Gavin's hypothesis:** When green line collapses onto blue line, BTC price highly likely to fall. Visible in advance on VST/ST, certain once LT green line collapses.

**Refined signal hierarchy:**

The "green line" = **Fast Trackline**. The "blue line" = **Slow Trackline**. These are the SRI LT regression tracklines applied to STRC's price series.

**Three distinct states:**

| State | Conditions | MSTR Implication |
|-------|-----------|-----------------|
| 🟢 NO STRESS | Fast TL >> Slow TL, both rising, price > $99 | Bullish — credit healthy |
| 🟡 STRESS FORMING | Fast TL declining toward Slow TL, price $97–99, fast_slope < 0 | Watch closely — 1–2 week lead time |
| 🔴 STRESS CONFIRMED | Fast TL crosses below Slow TL AND price < $97 | BTC/MSTR weakness probable within days |

**Precision corrections to original hypothesis:**
- "Certain" overstates confidence even at Stage 3. Better: "highly probable, timing within 1–2 weeks."
- The **price level** ($97 = stress, $101+ = healthy) is as important as the TL relationship. Fast TL collapse at $99.50 is much less severe than at $97.20.
- VST/ST give 3–7 day advance warning; LT confirmation reduces uncertainty but doesn't eliminate it.

**Bullish confirmation (score 1):** NO STRESS state (price > $99, Fast TL > Slow TL, histogram positive)

---

### ③ Stablecoin Dominance SRI LT — Capital Deployment Pressure

**Gavin's hypothesis:** When green line collapses, extremely bullish for MSTR, especially when slope of blue reversal band line is negative.

**Refined signal hierarchy:**

Stablecoin dominance falling = capital flowing from stables into crypto = bullish for BTC/MSTR.
The SRI indicator applied to stablecoin dom shows *momentum of dominance*, not just price.

**Two distinct "collapse" moments (critically different):**

| Moment | Description | MSTR Signal |
|--------|-------------|-------------|
| **Early decline** | Fast TL begins rolling over (slope < 0), price crosses below fast TL | Start building positions — 2–6 weeks to full signal |
| **Fast TL collapses to Slow TL** | Fast TL converges with Slow TL; both declining | Maximum confidence "all-in" signal — stablecoin dom bottom likely near |

**Precision corrections:**
- The "extremely bullish" signal fires at the *second* moment, not the first. The first is the warning, the second is the confirmation.
- "Especially when slope of blue line is negative" = CORRECT and essential. The Slow TL slope negative means the structural trend in stablecoin dom has turned down — not just a temporary dip. This is the most important qualifier.
- **Nuance:** Stablecoin dom can rise two ways: (a) new stables being minted (capital *entering* crypto but parking in stables — actually bullish), or (b) existing crypto converting to stables (risk-off). The SRI indicator doesn't distinguish these. Volume context (USDT market cap growth vs stablecoin share shift) adds this distinction, but is not available in the current suite.

**Bullish confirmation (score 1):** LT histogram negative AND fast TL slope negative (stablecoin dom actively declining at LT level)

---

### ④ STRF/LQD SRI LT — Crypto Credit Health vs IG Bonds

**Gavin's hypothesis:** Similar to STRC SRI LT. Positive momentum = strong. As blue line slope fades and green line collapses, reversals highly likely.

**Refined signal hierarchy:**

STRF/LQD ratio = STRF price / LQD price. Rising = crypto preferred outperforming IG bonds = risk-on. Falling = credit stress in crypto sector.

**The absolute level matters (missing from original hypothesis):**

| Level | State | MSTR Implication |
|-------|-------|-----------------|
| > 1.0, rising fast TL | Premium + momentum | Full tailwind — crypto credit leadership |
| < 1.0 but rising fast TL | Recovering from stress | Partial tailwind — healing, not yet confirmed |
| < 1.0 and falling fast TL | Discount + weakening | Headwind — credit stress active |
| Fast TL crosses below Slow TL | Structural deterioration | Bearish — mirrors STRC signal |

**Precision corrections:**
- "Similar to STRC SRI LT" is directionally correct — both falling = bearish for MSTR. But the mechanism is different: STRC is a direct BTC credit instrument; STRF/LQD is a relative signal (crypto vs investment grade).
- A ratio of 0.91 (current) with rising fast TL is "recovering from stress," not "positive momentum." The signal is bullish only when ratio sustains **above 1.0**.
- The LOI on STRF/LQD is valuable: deeply negative LOI = maximum credit stress accumulation; deeply positive = credit euphoria (trim zone).

**Bullish confirmation (score 1):** Ratio > 1.0 AND fast TL > slow TL AND fast_slope > 0
**Partial credit (0.5):** Ratio < 1.0 but fast TL > slow TL and recovering

---

### ⑤ MSTR/IBIT SRI LT — MSTR Alpha vs BTC

**Gavin's hypothesis:** Works similar to STRF/LQD in terms of momentum signals.

**Refined signal hierarchy:**

MSTR/IBIT is a **different signal type** from STRF/LQD. This is the most important sharpening in the suite.

- **STRF/LQD** = absolute sector health (rising = sector healthy → all crypto assets benefit)
- **MSTR/IBIT** = relative alpha (rising = MSTR gaining premium over BTC exposure → MSTR-specific tailwind)

These are complementary, not equivalent.

**The reversal interpretation is also different:**

| STRF/LQD falling | Bearish — absolute credit stress |
|------------------|----------------------------------|
| **MSTR/IBIT falling from elevated level** | Can be bullish — MSTR returning to BTC parity (BTC leading MSTR, MSTR will catch up) |
| **MSTR/IBIT falling from low level** | Bearish — MSTR discount to BTC worsening, underperformance cycle |

**Use MSTR/IBIT as two distinct tools:**

1. **Alpha cycle detector:** All 4 TF histograms positive → MSTR in outperformance cycle → LEAPs have premium expansion as a tailwind in addition to BTC gains
2. **Mean reversion gauge:** Ratio at historical extremes high + fast TL rolling over → mean reversion risk (MSTR to underperform BTC near-term)

**Current context (mNAV anchor):** MSTR/IBIT ratio should be read alongside mNAV (currently 1.22x). Low mNAV + MSTR/IBIT rising = double confirmation that MSTR is recovering from discount to BTC exposure. High mNAV + MSTR/IBIT at extremes = premium bubble risk.

**Bullish confirmation (score 1):** 3+ TF histograms positive (MSTR in alpha outperformance cycle)

---

## What's Missing — Recommended Chart 6

**BTC SRI LT** — Not currently in the suite but recommended as a background validation layer.

MSTR is 95%+ BTC-correlated. If MSTR's LT SRI is positive but BTC's LT SRI is negative, this is a divergence that should reduce confidence. If both align, conviction increases.

Proposed addition to suite in Phase 2 after validation.

---

## Composite Scoring

| Score | Label | Interpretation | Portfolio Action |
|-------|-------|---------------|-----------------|
| 4.5–5.0 | 🟢 STRONG BULLISH | Full suite aligned | Maximum AB3 deployment; AB4 near floor |
| 3.5–4.5 | 🟢 BULLISH | Majority aligned | Standard AB3 additions on LOI signals |
| 2.5–3.5 | 🟡 CAUTIOUSLY BULLISH | Mixed, trend intact | Hold current; watch for resolution |
| 1.5–2.5 | 🟠 NEUTRAL | No clear edge | No new positions; tighten AB2 deltas |
| 0.0–1.5 | 🔴 CAUTIOUS | Multiple warnings | Reduce sizing; review open positions |

---

## Weekly Report Cadence

**Delivery:** Every Friday at 4:30 PM ET (market close + 30 min)  
**Channels:** #mstr-cio (primary), summary to #mstr-greg and #mstr-gary  
**CSV prerequisite:** All 5 suite CSVs must be pushed to GitHub by 4:00 PM ET Friday  
**Reminder alert:** Automated reminder at 3:30 PM ET Friday

**On-demand:** Gavin, Greg, or Gary can request an instant report at any time. CIO will generate using the most recently available CSVs.

---

## Research Roadmap (Phases 2 & 3)

### Phase 2 — Quantitative Validation
For each chart's "trigger signal" (as defined above), backtest against MSTR forward 30d and 60d returns:
- Minimum N ≥ 15 for HIGH confidence
- WIN = MSTR +10%+ in forward window (consistent with LEAP entry threshold)
- Validate: do individual signals independently predict? Or only the composite?

### Phase 3 — Composite Score Validation
- When score ≥ 4.0, what is the historical MSTR 30d and 60d win rate?
- What is the false positive rate on STRC stress signals?
- Can the stablecoin dom "early warning" be quantified (average days to full signal)?
- Add mNAV as a 6th scoring dimension (low mNAV = bonus half-point)?

---

*Document version: 1.0 | Next update: after Phase 2 backtest results*  
*NOT for GitHub — internal working document*
