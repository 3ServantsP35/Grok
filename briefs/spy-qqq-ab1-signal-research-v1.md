# SPY/QQQ AB1 Signal Research v1
**Date:** 2026-03-04  
**Purpose:** Determine whether any SRI-derived signal reliably precedes 10%+ moves on SPY/QQQ within 60 days (≈360 4H bars). Find candidates for both entry and distribution (X) markers.

---

## Executive Summary

QQQ shows multiple actionable AB1 entry signals: `ct2_active`, `lt_flip_with_st_pos`, `st_flip_pos`, `ct3_cross`, and `lt_flip_pos` all clear the 60% win-rate-at-10% threshold within 360 bars, with QQQ `ct2_active` achieving 100% win rate across 7 de-duplicated occurrences. SPY falls short — no bullish signal with N≥5 clears 60%; the best is `ct2_active` at 57% — marginal and insufficient for a standalone AB1 trigger. Distribution signals on both SPY and QQQ are weak (best: QQQ `loi_rollover` at 55% for 3% drawdown) and do not clear the 60% threshold. In contrast, MSTR signals are dramatically stronger — `mixed_context` achieves 92% at 10% within 360 bars — validating the Momentum vs MR asset distinction.

**Recommendation (Bottom Line):** Hybrid approach — descope SPY from AB1; retain QQQ with `lt_flip_with_st_pos` or `ct3_cross` as primary entry signal; do not add a reliable X marker until distribution signal accuracy improves.

---

## Dataset

| Asset | Bars | Date Range | Data Notes |
|-------|------|-----------|------------|
| SPY   | 634  | 2024-11-19 to 2026-03-03 | Full signal columns present; all key indicators non-null |
| QQQ   | 634  | 2024-11-19 to 2026-03-03 | Full signal columns present; all key indicators non-null |
| MSTR  | 574  | 2025-01-07 to 2026-03-04 | Full signal columns present; smaller date window |

**Data Quality Notes:**
- SPY/QQQ LOI range is compressed vs MSTR: SPY LOI range [-24.9, +21.4], QQQ [-26.0, +24.4], MSTR [-52.2, +52.1]. **Neither SPY nor QQQ ever hit LOI < -30 or > +40 in this dataset**, meaning `loi_below_neg30`, `loi_below_neg40`, and `loi_above_40` fire zero times. SPY/QQQ are structurally lower-volatility assets — the AB3 LOI deep-accumulation signal is simply incompatible with these assets in this regime.
- `loi_cross_neg20_up` fires only N=1 on SPY and N=1 on QQQ — statistically unreliable despite 100% hit rate; excluded from top-3 rankings.
- De-duplication applied: 20-bar quiet period between signal occurrences.

---

## Signal Accuracy — SPY

All bullish signals, sorted by composite score (win_rate_10pct_360bar × median_peak_gain):

| Signal | N | Win5% (180-bar) | Win10% (360-bar) | Median Peak Gain | Avg Fwd-60 Drawdown | Score |
|--------|---|----------------|-----------------|-----------------|---------------------|-------|
| loi_cross_neg20_up | 1 | 100.0% | 100.0% | +27.4% | -0.9% | 27.4 ⚠️ N=1 |
| loi_cross_zero_up | 4 | 25.0% | 75.0% | +12.1% | -2.4% | 9.1 ⚠️ N=4 |
| ct2_active | 7 | 71.4% | **57.1%** | +10.1% | -1.7% | **5.8** |
| lt_flip_pos | 21 | 47.6% | 47.6% | +9.5% | -2.5% | 4.5 |
| vlt_flip_pos | 26 | 46.2% | 46.2% | +8.8% | -3.3% | 4.1 |
| lt_flip_with_st_pos | 19 | 52.6% | 42.1% | +8.7% | -2.6% | 3.7 |
| ct3_cross | 17 | 47.1% | 41.2% | +8.7% | -2.8% | 3.6 |
| st_flip_pos | 26 | 50.0% | 42.3% | +8.4% | -3.5% | 3.6 |
| ct1_cross | 21 | 42.9% | 42.9% | +8.0% | -3.8% | 3.4 |
| ct2_cross | 17 | 47.1% | 41.2% | +8.0% | -2.8% | 3.3 |
| ct4_active | 15 | 46.7% | 40.0% | +8.0% | -3.2% | 3.2 |
| ct3_active | 18 | 44.4% | 38.9% | +8.1% | -2.7% | 3.2 |
| vlt_pos_and_lt_pos | 19 | 52.6% | 36.8% | +8.2% | -2.7% | 3.0 |
| mixed_context | 15 | 20.0% | 40.0% | +3.7% | -4.7% | 1.5 |
| ct1_active | 15 | 20.0% | 40.0% | +3.4% | -4.9% | 1.4 |
| mixed_and_st_pos | 15 | 20.0% | 40.0% | +3.4% | -4.9% | 1.4 |
| loi_below_neg30 | 0 | — | — | — | — | — |
| loi_below_neg40 | 0 | — | — | — | — | — |

**⚠️ Threshold note:** No SPY signal with N≥5 clears 60% win rate at 10% within 360 bars. Best qualifying signal is `ct2_active` at 57.1% (N=7).

---

## Signal Accuracy — QQQ

All bullish signals, sorted by composite score:

| Signal | N | Win5% (180-bar) | Win10% (360-bar) | Median Peak Gain | Avg Fwd-60 Drawdown | Score |
|--------|---|----------------|-----------------|-----------------|---------------------|-------|
| loi_cross_neg20_up | 1 | 100.0% | 100.0% | +36.8% | -0.7% | 36.8 ⚠️ N=1 |
| ct2_active | 7 | 85.7% | **100.0%** | +14.5% | -1.8% | **14.5** ✅ |
| loi_cross_zero_up | 3 | 66.7% | 66.7% | +15.9% | -2.0% | 10.6 ⚠️ N=3 |
| lt_flip_with_st_pos | 20 | 65.0% | **70.0%** | +13.5% | -4.3% | **9.5** ✅ |
| st_flip_pos | 24 | 58.3% | **66.7%** | +13.5% | -4.5% | **9.0** ✅ |
| ct1_cross | 18 | 50.0% | **66.7%** | +13.5% | -5.1% | **9.0** ✅ |
| lt_flip_pos | 21 | 61.9% | **66.7%** | +13.4% | -4.2% | **8.9** ✅ |
| ct3_cross | 16 | 56.2% | **68.8%** | +12.6% | -3.6% | **8.7** ✅ |
| ct2_cross | 15 | 53.3% | **66.7%** | +12.5% | -3.7% | **8.3** ✅ |
| vlt_pos_and_lt_pos | 18 | 61.1% | **66.7%** | +12.3% | -3.4% | **8.2** ✅ |
| vlt_flip_pos | 24 | 54.2% | 62.5% | +12.3% | -4.6% | 7.7 |
| ct3_active | 17 | 52.9% | 64.7% | +11.1% | -3.7% | 7.2 |
| ct4_active | 11 | 63.6% | 45.5% | +9.8% | -4.3% | 4.5 |
| mixed_and_st_pos | 13 | 38.5% | 38.5% | +7.3% | -6.2% | 2.8 |
| mixed_context | 13 | 38.5% | 38.5% | +7.3% | -6.2% | 2.8 |
| ct1_active | 12 | 25.0% | 41.7% | +4.1% | -6.7% | 1.7 |
| loi_below_neg30 | 0 | — | — | — | — | — |
| loi_below_neg40 | 0 | — | — | — | — | — |

**✅ Multiple QQQ signals clear 60% win rate at 10%** with sufficient sample size (N≥15).

---

## Best Signals

### SPY — Top 3 (by composite score, N≥5)

| Rank | Signal | N | Win10% (360-bar) | Median Peak Gain | Score | Clears 60%? |
|------|--------|---|-----------------|-----------------|-------|-------------|
| 1 | **ct2_active** | 7 | 57.1% | +10.1% | 5.8 | ❌ No (57%) |
| 2 | lt_flip_pos | 21 | 47.6% | +9.5% | 4.5 | ❌ No |
| 3 | vlt_flip_pos | 26 | 46.2% | +8.8% | 4.1 | ❌ No |

SPY does not have a tradable AB1 signal at the 60% threshold.

### QQQ — Top 3 (by composite score, N≥5)

| Rank | Signal | N | Win10% (360-bar) | Median Peak Gain | Score | Clears 60%? |
|------|--------|---|-----------------|-----------------|-------|-------------|
| 1 | **ct2_active** | 7 | 100.0% | +14.5% | 14.5 | ✅ Yes (100%) |
| 2 | **lt_flip_with_st_pos** | 20 | 70.0% | +13.5% | 9.5 | ✅ Yes (70%) |
| 3 | **st_flip_pos** | 24 | 66.7% | +13.5% | 9.0 | ✅ Yes (67%) |

QQQ has three viable signals. `ct2_active` is highest conviction but rare (N=7). `lt_flip_with_st_pos` (N=20) provides the best balance of sample size and win rate. `st_flip_pos` (N=24) offers the most occurrences with 67% win rate.

---

## Distribution Signal Accuracy

### SPY — Distribution Signals

| Signal | N | % Fall 5%+ (180-bar) | % Fall 3%+ (60-bar) | Median DD (180-bar) | Clears 60% (3% dd)? |
|--------|---|---------------------|---------------------|---------------------|---------------------|
| all_extended | 11 | 27.3% | 27.3% | -1.9% | ❌ No |
| loi_above_40 | 0 | — | — | — | — |
| vlt_above_20 | 15 | 33.3% | 33.3% | -2.1% | ❌ No |
| loi_rollover | 31 | 32.3% | 32.3% | -2.6% | ❌ No |

**No SPY distribution signal clears the 60% threshold at 3% drawdown.**

### QQQ — Distribution Signals

| Signal | N | % Fall 5%+ (180-bar) | % Fall 3%+ (60-bar) | Median DD (180-bar) | Clears 60% (3% dd)? |
|--------|---|---------------------|---------------------|---------------------|---------------------|
| all_extended | 10 | 40.0% | 40.0% | -3.3% | ❌ No |
| loi_above_40 | 0 | — | — | — | — |
| vlt_above_20 | 14 | 42.9% | 42.9% | -3.2% | ❌ No |
| loi_rollover | 31 | 41.9% | **54.8%** | -4.0% | ❌ No (55%) |

**No QQQ distribution signal clears 60%.** `loi_rollover` at 55% is the closest but insufficient as a standalone X marker. Note: QQQ `loi_above_40` fires zero times in this dataset — LOI never exceeded +40 on QQQ, confirming the structural LOI compression on MR assets.

---

## MSTR Comparison

Running the same top QQQ signals (`ct2_active`, `lt_flip_with_st_pos`, `mixed_context`) on MSTR:

| Signal | Asset | N | Win5% (180-bar) | Win10% (360-bar) | Median Peak Gain | Avg Fwd-60 DD |
|--------|-------|---|----------------|-----------------|-----------------|---------------|
| ct2_active | QQQ | 7 | 85.7% | 100.0% | +14.5% | -1.8% |
| ct2_active | MSTR | 5 | 80.0% | 80.0% | +15.2% | -11.0% |
| lt_flip_with_st_pos | QQQ | 20 | 65.0% | 70.0% | +13.5% | -4.3% |
| lt_flip_with_st_pos | MSTR | 11 | 81.8% | 63.6% | +16.0% | -23.9% |
| mixed_context | QQQ | 13 | 38.5% | 38.5% | +7.3% | -6.2% |
| mixed_context | MSTR | 13 | **100.0%** | **92.3%** | **+24.6%** | -21.6% |

**MSTR full signal table (top signals only):**

| Signal | N | Win5% (180-bar) | Win10% (360-bar) | Median Peak Gain | Score |
|--------|---|----------------|-----------------|-----------------|-------|
| mixed_and_st_pos | 12 | 100.0% | 91.7% | +30.2% | **27.7** |
| mixed_context | 13 | 100.0% | 92.3% | +24.6% | **22.7** |
| ct1_active | 11 | 90.9% | 81.8% | +24.6% | **20.1** |
| vlt_flip_pos | 18 | 100.0% | 83.3% | +18.7% | **15.6** |
| vlt_pos_and_lt_pos | 11 | 90.9% | 81.8% | +16.5% | **13.5** |
| loi_below_neg30 | 9 | 66.7% | 55.6% | +15.4% | 8.5 |
| loi_below_neg40 | 4 | 100.0% | 50.0% | +10.8% | 5.4 |

**MSTR Distribution signals** (all dramatically stronger than SPY/QQQ):

| Signal | N | % Fall 5%+ (180-bar) | % Fall 3%+ (60-bar) | Median DD (180-bar) |
|--------|---|---------------------|---------------------|---------------------|
| all_extended | 2 | 100.0% | 100.0% | -36.6% |
| loi_above_40 | 2 | 100.0% | 100.0% | -39.9% |
| vlt_above_20 | 3 | 100.0% | 100.0% | -44.5% |
| loi_rollover | 28 | 92.9% | 89.3% | -35.6% |

**The MSTR vs SPY/QQQ contrast is stark and definitive.** MSTR `mixed_context` = 92% win rate at 10% gains; SPY `mixed_context` = 40%. MSTR `loi_rollover` = 89% at 3% drawdown; SPY = 32%. This is the empirical proof of the Momentum vs MR asset behavioral difference. AB1 SRI signals were designed for momentum assets. Applying them to MR assets produces noise, not signal.

---

## Gap Analysis

### Bullish Signals — 60% Win Rate at 10% Within 360 Bars?

| Asset | Best Signal | Win Rate | Clears 60%? | Useable? |
|-------|------------|----------|-------------|---------|
| SPY | ct2_active (N=7) | 57.1% | ❌ No | No — below threshold, too few occurrences |
| QQQ | ct2_active (N=7) | 100.0% | ✅ Yes | Conditionally — N=7 is small but perfect record |
| QQQ | lt_flip_with_st_pos (N=20) | 70.0% | ✅ Yes | **Yes — best balance of sample + accuracy** |
| QQQ | st_flip_pos (N=24) | 66.7% | ✅ Yes | Yes — most occurrences, still above threshold |
| MSTR | mixed_context (N=13) | 92.3% | ✅ Yes | Strong |

**SPY finding:** No tradable AB1 entry signal found on SPY. LOI never reaches meaningful accumulation levels (max compression: -24.9). CT signals are present but SPY's mean-reverting nature limits the duration and magnitude of trending moves — producing fewer sustained 10%+ runs. All tested signals miss the 60% hurdle.

**QQQ finding:** AB1 is viable on QQQ using structural timeframe flip signals (`lt_flip_with_st_pos`, `st_flip_pos`) or CT2+ confirmation. The SPY/QQQ divergence is meaningful — QQQ is more momentum-like (tech-heavy) and has produced more sustained trending episodes.

### Distribution Signals — 60% at 3% Drawdown Within 60 Bars?

| Asset | Best Signal | Rate | Clears 60%? |
|-------|------------|------|-------------|
| SPY | loi_rollover (N=31) | 32.3% | ❌ No |
| QQQ | loi_rollover (N=31) | 54.8% | ❌ No (borderline) |
| MSTR | loi_rollover (N=28) | 89.3% | ✅ Yes |

**No tradable distribution/X signal on SPY or QQQ at 60% threshold.** These assets grind rather than collapse after SRI extended readings. A 3% drawdown is common regardless of signal state on SPY/QQQ, which explains the low signal-to-noise ratio. MSTR's `loi_rollover` and `vlt_above_20` would both be excellent X markers for momentum assets but are inappropriate for SPY/QQQ.

### What's Missing?

1. **LOI depth for SPY/QQQ** — The system was designed around LOI signals that require -30 to -40 penetration. SPY and QQQ never reach these levels in the current dataset. The AB3 deep-accumulation signal is structurally incompatible with MR-Large assets.

2. **Longer lookback** — With only 634 bars (Nov 2024–Mar 2026), several signals have N≤7. A 3–5 year 4H dataset would provide 1,500–2,500+ bars and meaningfully improve signal reliability estimates.

3. **Regime conditioning** — SPY/QQQ signals may be regime-dependent (perform well in uptrend, poorly in correction). A regime-conditioned analysis (e.g., only run signals when GLI Z-score > 0.5) might improve SPY accuracy.

---

## Recommendation

**C) Hybrid approach:**

**SPY: Descope from standalone AB1.** No signal clears the 60% hurdle. SPY can remain in scope for AB3 (PMCC income overlay via AB2 against existing LEAPs) and for portfolio hedge purposes, but should not be a primary AB1 entry target. If SPY must be included, use `ct2_active` with secondary confirmation (GLI Z > 0.5 AND LOI crossing upward) as a gatekeeping filter — but flag as low-confidence.

**QQQ: Retain with `lt_flip_with_st_pos` as primary AB1 entry signal.** This is the best-supported signal: N=20, 70% win rate at 10%, median +13.5% peak gain, avg drawdown of only -4.3% before the move materializes. Secondary confirmation: `ct3_cross` or `st_flip_pos`. Entry confirmation: wait for the `lt_flip_pos` bar where `st_pos` is already true (i.e., ST was already positive when LT flipped). This reduces false early entries.

**QQQ Distribution (X marker): Not yet viable.** `loi_rollover` at 55% is the closest, but use only as a caution flag, not a hard exit trigger. Revisit when dataset extends to 2-year+ window.

**MSTR: No change needed.** Current signal set is performing strongly — `mixed_context` at 92%, `mixed_and_st_pos` at 92%, `vlt_flip_pos` at 83%. All MSTR distribution signals clear 60% by a wide margin. The MSTR signal architecture is working as designed.

**Strategic implication:** The SRI Bias Histogram signal framework is most potent on high-beta momentum assets (MSTR, TSLA, IBIT, BTC). For MR-Large assets, the signals fire but the magnitude of subsequent moves is insufficient to clear LEAP-appropriate thresholds consistently. QQQ sits on the borderline — keep, but size smaller than MSTR positions.

---

*Research conducted by CIO sub-agent. Data source: GitHub repo `3ServantsP35/Grok`, 4H bars via TradingView/BATS feed.*  
*Forward returns computed over next 20/60/180/360 bars from signal bar. De-duplication: 20-bar quiet period.*  
*Note: Results for N≤5 should be treated as directional only, not statistically robust.*
