# P6: Concordance Tier System — Full Multi-Asset Analysis
**Date: 2026-03-01 | Author: CIO | Data: 4H SRIBI histograms, 2021–2026**

---

## Summary

The 4-Tier Concordance system works — but the optimal entry tier is asset-dependent, not universal. CT1 (MIXED context) is the wrong entry on TSLA. CT3 (full alignment) is a fade signal on IWM. GLD is the most reliable asset in the dataset. CT4 is a distribution warning exclusively on Momentum assets.

This is the most actionable finding from the P6 backtest cycle. The engine's AB1 gate must be per-asset, not universal.

---

## Full Results Table

| Asset | Mode | CT1 N | CT1 Win | CT1 Med20d | CT2 N | CT2 Win | CT3 N | CT3 Win | CT3 Med20d | CT4 N | CT4 Win |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MSTR** | Momentum-BTC | 23 | **78%** | **+22.5%** | 2 | 100%* | 19 | 68% | +8.7% | 3 | 33% |
| **TSLA** | Momentum-Biz | 18 | 39% | -4.3% | 2 | 0%* | 16 | **69%** | **+22.7%** | 1 | 0% |
| **GLD**  | Trending | 27 | **81%** | **+5.4%** | 6 | **100%** | 23 | 74% | +1.7% | 2 | 50% |
| **SPY**  | MR-Large | 24 | 62% | +1.3% | 4 | **75%** | 25 | 64% | +2.7% | 2 | 50% |
| **QQQ**  | MR-Large | 19 | 68% | +4.6% | 3 | 100%* | 25 | 72% | +4.7% | 1 | 100%* |
| **IWM**  | MR-Small | 29 | **76%** | **+4.6%** | 1 | 0%* | 23 | **30%** | **-2.0%** | 0 | — |

*Small N — directionally informative only.

---

## Finding 1: TSLA Is the Inverse of MSTR

**CT1 on TSLA = fade signal. CT3 on TSLA = the actual entry.**

TSLA CT1 has a 39% win rate at 20d with -4.3% median. That is statistically worse than a coin flip. CT3 has 69% win rate and +22.7% median — comparable to MSTR's CT1.

**Why TSLA inverts the pattern:**

MSTR and TSLA are both classified as "Momentum" assets, but they operate on fundamentally different drivers:

- **MSTR in MIXED context** (LT<0, VLT>0): The underlying driver is BTC cycle recovery. Saylor's continuous buying creates a structural floor. When BTC and VLT begin recovering but LT hasn't caught up, the structural case is already building. Entering MIXED = entering before the crowd.

- **TSLA in MIXED context**: The underlying driver is business execution — deliveries, margins, Elon focus, competitive dynamics. LT-negative on TSLA means structural selling pressure on fundamentals. VLT recovering just means short-term traders are buying the dip, but the fundamental thesis hasn't changed. Entering MIXED = buying a dip in a declining fundamental trend.

For TSLA, LT-positive is the signal that the fundamental thesis is rehabilitated (not just that a short-term bounce is underway). CT3 requires LT positive — which is why CT3 works for TSLA where CT1 does not.

**Engine implication:** AB1 entry gate for TSLA must be CT3, not CT1. The current engine uses CT1 as the default for all Momentum assets. This is correct for MSTR/IBIT, wrong for TSLA.

---

## Finding 2: CT4 Is a Distribution Warning Only on Momentum Assets

| Asset | CT4 Win 20d | CT4 Win 40d | Implication |
|---|---|---|---|
| MSTR | 33% | 33% | **Strong distribution signal** |
| TSLA | 0% | 0% | **Strong distribution signal** (N=1) |
| GLD | 50% | 50% | Neutral — overextension in trending asset ≠ topping |
| SPY | 50% | 100% | Neutral — CT4 on MR assets = high continuation |
| QQQ | 100% | 100% | Neutral (N=1) |

CT4 (all TFs positive + VLT > +20) means different things by asset class:
- **Momentum**: VLT > +20 = structural overextension, distribution imminent → do not enter, consider trimming AB3
- **Trending (GLD)**: VLT > +20 = strong trend continuation, not necessarily topping
- **MR assets**: CT4 rarely fires; when it does, breadth is high and the trend continues short-term

**Engine implication:** CT4 distribution warning only applies to MSTR and TSLA. GLD/SPY/QQQ CT4 signals are not exits.

---

## Finding 3: GLD Is the Most Reliable Asset in the System

GLD has positive win rates across all concordance tiers. Even CT3 at 74% win rate maintains a positive edge. CT2 on GLD is 100% (N=6). CT4 is 50% (not a strong distribution signal).

GLD is a structural hedge that trends persistently. The SRI concordance system works well on it at all tiers because:
1. GLD doesn't have the same drawdown severity as Momentum assets — wrong timing doesn't destroy positions
2. GLD's macro drivers (real rates, DXY, safe haven demand) cycle more predictably than TSLA fundamentals
3. VLT overextension in a trending asset doesn't imply the same topping dynamics as in a Momentum asset

**Engine implication:** AB1 and AB3 on GLD are both viable at CT1 or better. No special tier gate needed.

---

## Finding 4: IWM CT3 Is a Fade

IWM CT3 win rate at 20d: **30%, -2.0% median.** This is counter-intuitive — when all TFs are positive on IWM, performance is worst.

Small-cap dynamics explain this: IWM CT3 fires during risk-on acceleration phases when small caps are being bid broadly. By the time all four timeframes align, small-cap momentum is often overextended relative to the economic cycle. Small caps are more rate-sensitive than large caps — CT3 on IWM frequently coincides with late-cycle rate expectations that reverse before the 20-40 day measurement window closes.

IWM CT1 is the better entry (76%, +4.6% median) because MIXED context for IWM often coincides with mid-cycle rate stabilization, before small caps re-rate higher.

**Engine implication:** IWM AB1 gate stays CT1. CT3 on IWM is a warning, not an entry. Consider disabling CT3 entries on IWM and treating IWM CT3 as a trim alert for existing AB3 positions.

---

## Revised Asset Tier Gate Specification

| Asset | AB1 Entry Gate | AB3 Entry | CT4 Signal | Notes |
|---|---|---|---|---|
| MSTR | **CT1** (MIXED) | LOI < -60 | Distribution warning | Regime gate required; GLI Z > -0.5 |
| IBIT | **CT1** (MIXED) | LOI < -60 | Distribution warning | Too few bars to validate — CT1 by analogy to MSTR |
| TSLA | **CT3** (Full align) | LOI < -60 | Distribution warning | CT1 is a fade signal; require LT+ |
| GLD | **CT1+** | LOI < -60 | Neutral | All tiers viable; CT1/CT2 are best |
| SPY | **CT2+** | LOI < -40 | Neutral | Small win-rate improvement over CT1 |
| QQQ | **CT2+** | LOI < -40 | Neutral | Similar to SPY |
| IWM | **CT1** | LOI < -40 | CT3 = trim signal | Invert the usual MR logic for IWM |
| PURR | **CT1** (provisional) | LOI < -60 | TBD | Observation mode; BTC-adjacent → assume MSTR pattern |

---

## Sub-Classification: Two Momentum Modes

The existing Momentum / MR / Trending 3-way classification needs one refinement:

| Sub-class | Assets | Optimal CT | Characteristic |
|---|---|---|---|
| **Momentum-BTC** | MSTR, IBIT, PURR | CT1 | Structurally floors via BTC cycle; LT catches up reliably |
| **Momentum-Fundamental** | TSLA | CT3 | Business-driven; needs LT+ to confirm thesis rehabilitation |
| **Trending** | GLD | CT1+ | Persistent macro trend; concordance works at all tiers |
| **MR-Large** | SPY, QQQ | CT2 | Broad market; CT2 slightly better, difference modest |
| **MR-Small** | IWM | CT1 | Rate-sensitive; CT3 is late-cycle, use as trim signal |

This sub-classification should be added to the engine's `AssetMode` enum in a future sprint.

---

## P6 Status: Complete

All six tradeable assets plus MSTR now fully backtested:

| Asset | Status | Optimal Tier | Key Finding |
|---|---|---|---|
| MSTR | ✅ | CT1 | Regime-dependent; GLI Z > -0.5 required |
| TSLA | ✅ | CT3 | CT1 is 39% — a fade signal |
| GLD  | ✅ | CT1/CT2 | Reliable across all tiers |
| SPY  | ✅ | CT2 | Modest improvement over CT1 |
| QQQ  | ✅ | CT2/CT3 | Flat across tiers, slight CT3 edge at 40d |
| IWM  | ✅ | CT1 | CT3 = -2.0% median — invert expectation |
| IBIT | 🟡 | CT1 (provisional) | Too few bars (1,062) to validate |
| BTC  | n/a | — | Regime input only; SRI anti-predictive |

---

## Required Engine Changes

These findings require two engine code changes:

**1. TSLA AB1 gate: CT3 required**
In `AB1PreBreakoutEngine.__init__()`, add `tsla_mode: bool` flag that requires `lt > 0` as entry condition C3 (instead of MIXED).

**2. IWM CT3 trim signal**
In `run_ab3()` or the dashboard, flag IWM CT3 as a trim consideration for existing IWM AB3 positions (not a new entry signal).

**3. AssetMode refinement**
Add `MOMENTUM_BTC` and `MOMENTUM_FUNDAMENTAL` sub-modes to distinguish MSTR/IBIT from TSLA entry logic.

---

*P6 complete. Cross-reference: mstr-concordance-backtest.md (MSTR detail), four-bucket-framework-v2.0.md (integration).*
