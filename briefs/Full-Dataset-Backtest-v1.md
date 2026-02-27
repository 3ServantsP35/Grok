# Full Dataset Backtest — All Majors, All 4 Timeframes
**Date:** February 27, 2026  
**Assets:** BTC (3,048d), MSTR (2,630d), SPY (2,630d), GLD (2,630d), DXY (2,614d), STRC (150d), MSTR/IBIT (534d), Stable Coin Dom (285d)  
**Data:** Daily candles, full indicator suite (VST/ST/LT/VLT SRI + SRIBI + on-chain)  
**Architecture Reference:** MSTR Engine Architecture v1.0

---

## Dataset Summary

| Asset | Rows | History | Current Price | Role |
|---|---|---|---|---|
| **BTC** | 3,048 | Oct 2017–Feb 2026 | $65,302 | Risk tier, Bitcoin Cycle anchor |
| **MSTR** | 2,630 | Sep 2015–Feb 2026 | $129.30 | Primary vehicle, AB2/AB3 |
| **SPY** | 2,630 | Sep 2015–Feb 2026 | $684.65 | Quality tier |
| **GLD** | 2,630 | Sep 2015–Feb 2026 | $480.39 | Safety tier |
| **DXY** | 2,614 | Nov 2015–Feb 2026 | $97.59 | Macro overlay |
| **STRC** | 150 | Jul 2025–Feb 2026 | $100.02 | Cost-of-capital benchmark |
| **MSTR/IBIT** | 534 | Jan 2024–Feb 2026 | $3.48 | Relative value |
| **Stable Coin Dom** | 285 | May 2025–Feb 2026 | $13.80 | Crypto risk appetite |

All 4 TFs (VST/ST/LT/VLT) at 100% completeness across all assets. BTC ST gap is fixed.

---

## Finding #1: Concordance Tiers Validated Across All Assets

The CT system works — and each asset reveals its character:

### BTC (3,048 days — full dataset with ST)

| Tier | n | 5d | 20d | 40d | Win% 20d |
|---|---|---|---|---|---|
| CT1 Scout | 497 | +1.12% | +4.29% | +8.16% | 52% |
| CT2 Early | 1,029 | +1.72% | +6.63% | +11.89% | 58% |
| CT3 Confirmed | 880 | +1.79% | +6.95% | +12.21% | 60% |
| **CT4 High Conv** | 469 | **+2.66%** | **+8.94%** | **+14.76%** | **64%** |
| All Negative | 674 | — | +0.81% | +1.77% | 52% |

**With 4 TFs (including ST), the edge is STRONGER than the 3-TF test.** CT4 went from +4.40% → +8.94% at 20d. The ST timeframe adds significant discriminating power.

**BTC CT spread: CT4 minus All Negative = +8.13% at 20d.** This is a massive, tradeable edge.

### MSTR Post-BTC Strategy (Aug 2020+, 1,400 days)

| Tier | n | 20d | 40d | Win% 20d |
|---|---|---|---|---|
| CT1 Scout | 215 | +12.22% | +19.33% | 60% |
| CT2 Early | 499 | +10.64% | +16.48% | 54% |
| CT3 Confirmed | 465 | +10.73% | +15.84% | 54% |
| **CT4 High Conv** | 217 | **+17.22%** | **+19.49%** | **58%** |
| All Negative | 408 | +6.94% | +16.04% | 50% |

**MSTR amplifies BTC.** CT4 = +17.22% at 20d. But even All Negative delivers +6.94% — MSTR mean-reverts violently from deep bearish. This is structurally different from BTC.

**Key MSTR insight:** The CT spread is narrower than BTC (CT4 vs All Neg: +10.28% vs +8.13%). MSTR's mean-reversion from extremes compresses the edge. This means:
- **AB2 spreads work in ANY concordance state** (MSTR always bounces)
- **AB1 directional needs CT4** to justify the risk premium over AB2
- **All Negative is actually an AB2 accumulation signal for MSTR** (sell puts)

### SPY (2,630 days)

| Tier | n | 20d | 40d | Win% 20d |
|---|---|---|---|---|
| CT4 High Conv | 593 | +0.50% | +1.20% | 68% |
| All Negative | 578 | **+1.51%** | **+3.12%** | 65% |

**SPY confirmed mean-reverting.** All Negative outperforms CT4 by 3x. Concordance Tiers are INVERTED for SPY — high concordance = lower forward returns. The system should buy SPY weakness, not SPY strength.

### GLD (2,630 days)

| Tier | n | 20d | 40d | Win% 20d |
|---|---|---|---|---|
| CT1 Scout | 422 | +1.41% | +2.89% | 59% |
| CT4 High Conv | 410 | +1.81% | +2.90% | 62% |
| All Negative | 674 | +1.00% | +1.77% | 58% |

**GLD is a weak trend-follower.** CT tiers differentiate modestly (+0.81% spread at 20d). GLD allocation should be driven primarily by macro regime (Howell Layer 1), not by concordance signals.

### DXY (2,614 days)

**DXY shows NO directional edge from concordance.** All quintiles cluster around 0%. This confirms DXY is a macro/regime indicator, not a tradeable signal via SRI — it belongs in Layer 1 (Regime Engine) as context, not Layer 2 (Signal Layer).

---

## Finding #2: The 1/N Breadth Trap Confirmed With 4 TFs

BTC FTL>STL breadth across all 4 TFs:

| Breadth | n | 20d | 40d | Win% |
|---|---|---|---|---|
| 0/4 (all bear) | 775 | +1.20% | +2.66% | 51% |
| **1/4 (trap)** | 185 | **-0.01%** | **+0.72%** | **52%** |
| 2/4 | 953 | +2.23% | +5.05% | 53% |
| **3/4 (trap)** | 78 | **-3.62%** | **+0.98%** | **47%** |
| 4/4 (all bull) | 1,057 | +6.05% | +11.25% | 54% |

**The trap zones are now ODD numbers (1/4 and 3/4).** 3/4 is actually WORSE than 1/4. This generalizes the finding: **partial concordance in either direction is dangerous.** The system wants either full agreement (0/4 or 4/4) or balanced split (2/4).

**Rule update:** Avoid directional trades at 1/4 or 3/4 breadth. Wait for resolution to 0/4 (AB2 spreads) or 4/4 (full deployment).

---

## Finding #3: RORO Rebuilt With Multi-TF Data

### Risk Phase Distribution (2,096 overlapping days)

| Phase | Days | % | BTC 20d |
|---|---|---|---|
| **RP1 Early** | 250 | 11.9% | **-1.44%** |
| RP2 Broadening | 101 | 4.8% | +0.56% |
| **RP3 Risk-On** | 574 | 27.4% | **+6.82%** |
| RP4 Late | 63 | 3.0% | +8.55% |
| RP5 Risk-Off | 210 | 10.0% | +1.88% |
| RP0 Mixed | 898 | 42.8% | +5.36% |

**RP0 (Mixed) is 43% of the time** — the classification needs tightening. Many days don't cleanly fit the 5-phase model. This is expected with only 3 assets (GLD/SPY/BTC) instead of the full tier structure. Adding TLT, QQQ, and TSLA will reduce RP0.

**RP1 is the only phase with negative BTC returns (-1.44%).** Confirms: don't go directional in RP1. Current state is RP1.

### Bitcoin Cycle Distribution

| Phase | Days | % | BTC 20d |
|---|---|---|---|
| BC1 Markdown | 375 | 17.9% | +2.95% |
| BC2 Accumulation | 302 | 14.4% | -1.27% |
| BC3 Early Markup | 393 | 18.8% | +0.13% |
| **BC4 Markup** | 746 | 35.6% | **+11.62%** |
| BC6 Distribution | 280 | 13.4% | -0.27% |

**BC4 is the money phase** — 36% of the time, +11.62% at 20d. BC2 (Accumulation) is actually negative — this is the "false dawn" zone where SRIBI improves but price hasn't turned yet.

### RP × BC Matrix (BTC 20d return / win% / n)

| | BC1 | BC2 | BC3 | BC4 | BC6 |
|---|---|---|---|---|---|
| **RP1** | +4.7%/60%/89 | +3.1%/59%/46 | **-10.9%/21%/75** | n<10 | n<10 |
| RP2 | n<10 | +5.2%/54%/24 | -6.2%/38%/26 | +3.7%/37%/35 | n<10 |
| **RP3** | n<10 | n<10 | +3.7%/45%/42 | **+9.8%/61%/405** | -2.5%/41%/101 |
| RP4 | n<10 | n<10 | n<10 | **+14.6%/80%/35** | n<10 |
| RP5 | +4.9%/66%/82 | **-10.0%/30%/47** | +9.2%/61%/59 | n<10 | **-11.7%/27%/11** |

**Key findings from the matrix:**

1. **RP1×BC3 is the worst cell: -10.9%, 21% win rate.** This is the trap we identified — early BTC markup while risk is still off. NEVER go directional here.

2. **RP3×BC4 is the money cell: +9.8%, 61% win, n=405.** This is where most profits are made. Full deployment.

3. **RP4×BC4 is the best return: +14.6%, 80% win** but only 35 instances. Late-cycle euphoria — ride it but watch for BC6 transition.

4. **RP5×BC2 and RP5×BC6 are catastrophic** (-10% and -12%). Full risk-off in Bucket 4.

5. **RP1×BC1 (CURRENT): +4.7%, 60% win, n=89.** This is actually positive — the mean-reversion at deep bearish extremes. Confirms AB2 spreads and AB3 Path B are appropriate.

6. **RP5×BC3 is surprisingly strong: +9.2%, 61% win.** After full panic (RP5), if BTC shows early markup (BC3), it's a powerful recovery signal. Watch for this transition.

---

## Finding #4: MSTR/IBIT Ratio Signals

| Tier | n | Current SRIBI |
|---|---|---|
| VST | 534 | +35 (BULL) |
| ST | 534 | +20 (BULL) |
| LT | 534 | +35 (BEAR — FTL<STL) |
| VLT | 534 | +5 (BEAR) |

**MSTR is outperforming IBIT on shorter timeframes (VST/ST bullish) but not yet on longer (LT/VLT bearish).** This means the premium expansion is early — MSTR's mNAV premium is rebuilding from shorter TFs up. If LT flips bullish, MSTR directional calls become the vehicle over IBIT.

---

## Finding #5: STRC Confirms Safety

STRC: All 4 TFs bullish (VST=+25, ST=+25, LT=+40, VLT=+50). CT4 High Conviction on STRC. Credit market is healthy — no stress signals. STRC hurdle (0.83%/mo) remains the appropriate benchmark.

---

## Finding #6: Stable Coin Dominance Rising

Stable Coin Dom: All 4 TFs bullish (VST=+50, ST=+10, LT=+15, VLT=+10). Rising stablecoin dominance = capital flowing to safety within crypto. This CONFIRMS RP1 + BC1 — crypto participants are de-risking. Watch for VST to flip negative (capital leaving stablecoins) as an early re-risk signal.

---

## Current State Summary

```
REGIME ENGINE:
  Macro: Liquidity Contracting (GLI Z=-1.01) | Rates Cutting
  Risk Phase: RP1 Early (Safety=+41, Quality=-11, Risk=-48)
  Bitcoin Cycle: BC1 Markdown (LT SRIBI=-65, FTL<STL)
  RP×BC Cell: RP1×BC1 (+4.7% historical, 60% win, n=89)

SIGNAL LAYER:
  BTC Concordance: Pre-CT1 (all SRIBI negative: VST=-55, ST=-40, LT=-65, VLT=-30)
  MSTR Concordance: Mixed (VST=+15, ST=+5, LT=+10, VLT=-50) — NOT aligned with BTC
  Bear Triggers: BT3 Capitulation zone (SOPR=-0.29, all SRIBI negative)
  Preferred: STRC CT4 (healthy, all TFs bullish)
  MSTR/IBIT: VST/ST bullish, LT/VLT bearish (premium rebuilding)
  Stable Coin Dom: All TFs bullish (de-risking in progress)

ALLOCATION ENGINE:
  RP1×BC1 → AB1=0% | AB2=15-20% | AB3=5-8% (Path B) | AB4=72-80%
  Concordance gate: Pre-CT1 → AB2 spreads only (sell premium into mean-reversion)
  STRC hurdle: Active (0.83%/mo)
```

---

## Refinements to Architecture v1.0

### New Rules

1. **Odd-breadth trap (generalizes 1/3 finding):** At 1/4 or 3/4 TF breadth, avoid directional. Wait for 0/4, 2/4, or 4/4.

2. **MSTR mean-reversion rule:** MSTR All Negative still delivers +6.94% at 20d post-BTC strategy. AB2 spreads (sell puts) are valid in ANY concordance state for MSTR. AB1 directional requires CT4.

3. **RP1×BC3 kill zone:** -10.9% at 20d, 21% win rate. If BTC enters BC3 (early markup) while still RP1, this is the most dangerous state in the matrix. Absolute no-go for AB1.

4. **Stablecoin Dom as RP1 confirmation:** When Stable Coin Dom is CT4 bullish, RP1 is confirmed. Watch for VST flip as early de-risk exit signal.

5. **MSTR/IBIT ratio as vehicle selector:** When ratio VST/ST are bullish (premium expanding), MSTR calls beat IBIT. When ratio LT/VLT flip bullish, shift AB1 vehicle from IBIT to MSTR.

6. **DXY excluded from Signal Layer:** No directional edge from SRI concordance. Kept in Regime Engine as macro context only.

### RP0 Reduction Plan

42.8% of days classified as RP0 (Mixed) is too high. Fixing this requires:
- Adding TLT (safety tier — currently only GLD)
- Adding QQQ (quality tier — currently only SPY)  
- Adding TSLA (speculative tier — currently none)
- This will create more discriminating tier averages and reduce RP0 to <20%

---

## What We Still Need

1. **TLT, QQQ, TSLA** daily multi-TF exports — to complete RORO tiers and reduce RP0
2. **MSTR on-chain validation** — the on-chain columns in MSTR export show BTC values (expected since MSTR doesn't have its own on-chain). Confirm this is intentional.
3. **RP1×BC1→BC2 transition detection** — we're in RP1×BC1 now. BC2 (Accumulation) is actually negative (-1.27%). We need to identify the BC1→BC2→BC3 sequence to avoid the BC2 false dawn and the RP1×BC3 trap.
4. **Backtest AB2 spread returns by RP×BC cell** — validate that selling premium works across the matrix.
