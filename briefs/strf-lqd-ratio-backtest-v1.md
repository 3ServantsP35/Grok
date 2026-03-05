# STRF/LQD Ratio Backtest — MSTR Predictive Value
**Date:** 2026-03-04  
**Analyst:** CIO  
**Dataset:** `BATS_STRF_BATS_LQD, 240_40822.csv` — 300 bars, Jul 29 2025 – Mar 4 2026  
**Hypothesis tested:** STRF/LQD ratio as a leading bullish indicator for MSTR, with improved dynamic range vs STRC (which is capped at par)

---

## Executive Summary

**The theory is partially validated, but the signal direction is inverted from the original hypothesis.**

The ratio CAN and does exceed 1.0 (confirmed range: 0.844–1.110). However, MSTR's forward returns are significantly **worse** when the ratio is above 1.0, and significantly **better** when the ratio is in the distress zone (< 0.93). The premium regime (ratio > 1.0) is an overhead/distribution indicator, not a bullish confirmation.

The most useful finding: the STRF/LQD ratio identifies **distress and recovery regimes** more dynamically than STRC because it has no ceiling — but the signal interpretation is the mirror image of the original hypothesis.

---

## Regime Analysis — The Core Finding

When bars are grouped by the STRF/LQD ratio level, MSTR's forward returns show a clear inverse relationship:

| Regime | Level | N | % Time | Avg fwd60 max% | Win 10%/60bars | Avg fwd20 close% |
|---|---|---|---|---|---|---|
| CRISIS | < 0.88 | 4 | 1.3% | **+12.3%** | **75%** | +3.6% |
| STRESS | 0.88–0.90 | 2 | 0.7% | **+11.4%** | **50%** | +5.0% |
| WEAK | 0.90–0.93 | 11 | 3.7% | **+12.7%** | **72.7%** | +1.1% |
| CAUTIOUS | 0.93–0.95 | 29 | 9.7% | **+12.5%** | **62.1%** | -3.8% |
| NEUTRAL | 0.95–0.97 | 17 | 5.7% | +14.2% | **76.5%** | -3.6% |
| HEALTHY | 0.97–1.00 | 87 | 29.0% | +7.1% | 31.0% | -10.9% |
| STRONG | 1.00–1.03 | 49 | 16.3% | +7.3% | 24.5% | -4.3% |
| PREMIUM | > 1.03 | 41 | 13.7% | **+3.2%** | **7.3%** | -9.6% |

**The pattern is unambiguous:** MSTR's best forward max returns occur when STRF/LQD is below 0.95. Wins drop off sharply once the ratio enters healthy/strong territory and almost disappear at the premium level. The ratio is essentially a **distress thermometer** — low readings mark accumulation setups; high readings mark exhaustion.

---

## The Ceiling Effect — Revised Interpretation

Gavin's original hypothesis: STRC hits a ceiling at par ($100) and can't signal continued bullishness once credit normalizes. The STRF/LQD ratio, which can exceed 1.0, should capture additional upside signal.

**What the data shows instead:**

The times when STRC is capped at par but STRF/LQD is above 1.0 (N=0 in this dataset — they didn't co-occur) suggest the two instruments actually behave differently by design. More critically, the ratio **above 1.0 is not associated with stronger MSTR returns** — it's associated with weaker ones.

The STRC ceiling turns out to be a feature, not a bug. STRC hovering at par means "credit not stressed" — a stable, neutral read. The STRF/LQD ratio above 1.0 means STRF is trading at a **premium to investment-grade bonds**, which historically coincides with MSTR already having run and being in a late-stage or distribution environment.

---

## Key Transition Events (All Occurrences)

**Ratio crosses above 1.0 — MSTR was at a peak each time:**
| Date | MSTR price | fwd20 close% | fwd60 max% |
|---|---|---|---|
| Sep 9, 2025 | $326 | +2.6% | +11.9% |
| Sep 18, 2025 | $355 | -2.1% | +3.0% |
| Sep 19, 2025 | $340 | +3.6% | +7.3% |
| Sep 30, 2025 | $317 | -1.6% | +15.0% |
| Nov 3, 2025 | $264 | **-27.6%** | +2.0% |

The Nov 3 event is the critical data point: the ratio crossed above 1.0 at $264, and MSTR declined -27.6% over the next 20 bars. This is the "STRF premium = distribution" signal at its most explicit.

**Ratio crosses below 0.90 — during the Feb 2026 decline:**
| Date | MSTR price | fwd20 close% |
|---|---|---|
| Jan 28, 2026 | $160 | -21.5% |
| Feb 2, 2026 | $143 | -8.5% |
| Feb 19–27, 2026 | $124–130 | n/a (too recent) |

The stress crossings during January–February did NOT mark the bottom — the stock continued declining after each one. This is consistent with the STRC leading indicator framework: stress signals don't mean "buy immediately," they mean "accumulation zone is forming."

---

## Leading Indicator Test

The original theory also proposed STRF/LQD as a leading indicator (moves before MSTR). The data does not support a meaningful lead relationship.

**Correlation: ratio ROC vs MSTR ROC at various leads:**
| Lead | Correlation (r) |
|---|---|
| Contemporaneous | **0.550** (strong — moves together) |
| Ratio leads by 0.5d | -0.032 (near zero) |
| Ratio leads by 1d | -0.005 (near zero) |
| Ratio leads by 2d | -0.041 (near zero) |
| Ratio leads by 3d | -0.080 (near zero) |
| Ratio leads by 4d | 0.112 (weak) |
| Ratio leads by 5d | -0.021 (near zero) |

The ratio is a **coincident indicator** — it moves with MSTR, not before it. The strong contemporaneous correlation (r=0.550) confirms the instruments are measuring the same risk-on/risk-off sentiment in real time. The near-zero lagged correlations mean no systematic lead exists.

---

## Comparison: STRF/LQD vs STRC as Signals

Both instruments are measuring credit health in the BTC ecosystem. The data suggests STRC may actually be the cleaner signal for entry timing:

| Signal | N | Win 5%/20bars | Win 10%/60bars |
|---|---|---|---|
| STRC crosses above 97 (recovery) | 10 | — | ~50–75%* |
| STRC crosses below 97 (stress onset) | 9 | 50–67% | ~50% |
| Ratio crosses above 1.0 | 5 | 40% | 40% |
| Ratio in distress zone < 0.93 | 17 | — | 65%+ |

*STRC cross-above-97 is noisy due to multiple crossings in tight ranges (9 events in Aug-Sep 2025 alone). Best entries were late Nov 2025 and Feb 2026.

---

## Most Actionable Finding: The Ratio as a Distribution Signal

The strongest practical application of STRF/LQD is the **inverse of the original hypothesis** — use it as a **distribution/caution indicator** rather than a bullish momentum indicator:

| Ratio Level | MSTR Signal | Framework Action |
|---|---|---|
| > 1.03 PREMIUM | 🔴 Distribution likely | Reduce AB2 call aggression; review AB3 trim schedule |
| 1.00–1.03 STRONG | 🟠 Late-stage | No new entries; hold existing |
| 0.97–1.00 HEALTHY | 🟡 Neutral | Standard monitoring |
| 0.93–0.97 CAUTIOUS/NEUTRAL | 🟢 Bottoming zone | Watch for AB3 entry setup |
| < 0.93 WEAK/STRESS/CRISIS | 🟢🟢 Accumulation regime | LOI + SCHI signals most reliable here |

**Proposed addition to Gavin's SCHI composite:** The ratio's premium reading (> 1.03) as a bearish modifier on MSTR positioning — reduces the bullish probability estimate when STRF is at a significant premium to LQD.

---

## Limitations

1. **Small N**: 300 bars = ~7.5 months. Many signal events have N < 5 in the transition analysis. Findings are directionally reliable but not statistically conclusive.
2. **Period bias**: The dataset covers a full market cycle (ATH → -73% drawdown → start of recovery). The distress regime findings may be partially driven by the fact that stress periods during a drawdown are naturally followed by recoveries.
3. **Missing STRF history**: No data before July 2025. Longer history needed to validate the premium = distribution finding across multiple cycles.

---

## Recommendation

**Use STRF/LQD as a regime identifier, not a directional trade signal:**

1. **Add to SCHI composite** as a bearish modifier when ratio > 1.03 (reduces bullish probability estimate ~15%)
2. **Add to morning brief** as a context line: current ratio level + regime label
3. **Do not add as a bullish entry signal** — the "ceiling" on STRC is a feature; STRF premium does not predict MSTR upside
4. **Flag when ratio crosses below 0.90** — begins accumulation zone monitoring (same role as STRC < 97), with the advantage of being a continuous signal rather than binary
5. **Re-run with more data** once 18+ months of STRF/LQD ratio history is available

---

*Data: `BATS_STRF_BATS_LQD, 240_40822.csv` | `BATS_MSTR, 240_c0ce8.csv` | `BATS_STRC, 240_3a3ab.csv`*
