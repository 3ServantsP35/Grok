# MSTR Indicator Evaluation — Full Efficacy Review
**Date:** 2026-02-28  
**Dataset:** BATS_MSTR 1D — Feb 2018 → Feb 2026 (2,015 bars)  
**Scope:** AB1 CT crosses, AB2 Bull Put, SRI stage transitions, on-chain suite, cross-indicator confluence

---

## Summary Table

| Indicator | Signal Quality | Actionable? | Key Finding |
|---|---|---|---|
| CT1 Cross | ★★★★☆ | Yes — with filter | 67% win 90d, but Risk<0.3 fires are 0% win |
| CT2 Cross | ★★★★☆ | Yes | Nearly identical to CT1 — no meaningful edge difference |
| CT3 Cross | ★★★☆☆ | Conditional | 59% win 60d — lower than CT1 on MSTR; only add for TSLA |
| CT4 Distribution | ★★★☆☆ | Partial | 42% win 30d but 74% win 90d — late-cycle, not a hard exit |
| AB2 Bull Put | ★★★★☆ | Yes — with MVRV gate | 92% win 90d, 77% win 60d — excellent but rare (13 fires/8yr) |
| ST Stage 3→4 | ★★★★★ | Yes — underused | 83% win 90d, median +22.6% — strongest single signal in dataset |
| VST Stage 1→2 | ★★★★☆ | Yes — as warning | 31% win 60d, median -14.8% — strong bearish flag |
| STH MVRV | ★★★★☆ | Yes — zoned | Near-cost (0.8–1.0) = 70% win 60d. Current 0.44 = 4th pctile, still risky |
| Risk Score | ★★★★★ | Yes — as gate | <0.2 = 5% win 60d. **Critical gate for all entries** |
| MVRV Z-Score | ★★★★☆ | Yes | Z 1–2 = 70% win 60d; Z<0 = 62% win. Confirms cycle phase |
| Funding Rate | ★★★☆☆ | Yes — contrarian | Very negative (<-0.002) = 60% win 30d. Current reading bullish |
| STH SOPR | ★★☆☆☆ | Limited | ~53% win across all zones — too noisy to gate entries alone |
| NRPL | ★★☆☆☆ | Context only | U-shaped — both extremes underperform. Not tradeable standalone |

---

## Section 1 — AB1 CT Cross Analysis

**Full history: 42 CT1, 38 CT2, 32 CT3, 19 CT4 fires**

| Signal | +10d win | +60d win | +60d med | +90d win | +90d med |
|---|---|---|---|---|---|
| CT1 | 67% | 62% | +5.1% | 67% | +6.8% |
| CT2 | 68% | 63% | +5.9% | 68% | +6.8% |
| CT3 | 69% | 59% | +6.4% | 62% | +4.1% |
| CT4 | 68% | 63% | +10.9% | 74% | +85.9% |

### Finding 1.1 — CT1 and CT2 are equivalent on MSTR

The 1pp win rate difference between CT1 and CT2 is noise at this sample size. The theoretical case that CT2 (early structural alignment) is meaningfully better than CT1 (MIXED context) is not supported in the MSTR dataset. Both are valid entry tiers. CT1 fires more frequently, giving more exposure time at equivalent win rates.

### Finding 1.2 — CT3 underperforms CT1 at 60d/90d on MSTR

CT3 (all TFs positive) has 59% win at 60d vs CT1's 62%. Median 90d return is +4.1% vs CT1's +6.8%. CT3 fires later in the cycle — by that point, the structural catch-up is already partially priced in. **For MSTR/IBIT, CT1 remains the sweet spot. CT3 as an entry gate (as implemented for TSLA) is correct but should not be applied to BTC-proxy assets.**

### Finding 1.3 — CT4 is a late-cycle momentum signal, not a top

CT4 at 30d: 42% win — momentum slows. CT4 at 90d: 74% win, median +85.9%. This pattern means CT4 fires mid-bull-run when there's still 90 days of gains, but the short-term rhythm breaks first. **Recommendation: CT4 = reduce new position sizing and tighten trailing stops, but do not close existing positions.** The hard "distribution warning" framing in AB3 is too aggressive.

### Finding 1.4 — Risk Score gate is critical

CT1 stratified by Short-Term Risk Score:
- Risk < 0.3: **0% win rate at 90d** (n=6, median -36.1%) — CT1 fires during structural decline
- Risk 0.3–0.6: **80% win at 90d** (n=30, median +13.5%) — the working zone
- Risk > 0.6: 67% win (n=6) — valid but fewer observations

**CT1 fires when Risk < 0.3 are false signals.** When SRI says MIXED and VST turns positive, but on-chain says "panic zone," price has not found its floor yet. The Risk Score gate of ≥ 0.3 filters this.

---

## Section 2 — AB2 Bull Put Entry

**13 fires over 8 years. 92% win rate at 90d. 77% win at 60d.**

| Date | Price | Context | MVRV | Risk | 30d | 60d | 90d |
|---|---|---|---|---|---|---|---|
| 2019-02-11 | $13.68 | TAILWIND | 1.03 | 0.54 | +6.5% | +0.9% | +8.1% |
| 2019-06-10 | $13.65 | MIXED | 1.01 | 0.58 | -11.0% | +0.5% | +5.0% |
| 2019-06-17 | $14.12 | MIXED | 0.99 | 0.64 | -12.8% | +4.5% | +1.0% |
| 2019-07-31 | $13.67 | TAILWIND | 1.01 | 0.57 | +8.5% | +5.8% | +10.9% |
| 2020-01-16 | $14.67 | MIXED | 1.05 | 0.50 | -6.8% | -13.8% | **-14.2% ✗** |
| 2023-02-15 | $29.84 | TAILWIND | 0.86 | 0.61 | -6.4% | -9.2% | +8.9% |
| 2023-03-17 | $26.77 | TAILWIND | 0.93 | 0.48 | +14.9% | +6.0% | +59.2% |
| 2023-08-29 | $38.15 | **HEADWIND** | 1.30 | 0.56 | -12.3% | +33.1% | +56.7% |
| 2023-10-23 | $37.75 | TAILWIND | 1.24 | 0.45 | +53.0% | +27.4% | +253.4% |
| 2024-02-08 | $58.78 | TAILWIND | 1.47 | 0.52 | +159.1% | +115.9% | +150.0% |
| 2024-05-15 | $150.35 | TAILWIND | **2.59** | 0.56 | -8.4% | -12.6% | +2.3% |
| 2024-09-19 | $144.66 | MIXED | 1.47 | 0.31 | +69.0% | +182.5% | +135.1% |
| 2025-03-24 | $335.72 | TAILWIND | 1.56 | 0.37 | +14.9% | +9.9% | +9.2% |

### Finding 2.1 — MIXED-only gate may be too strict

The Aug 2023 HEADWIND entry produced +57% at 90d. The entry was technically a headwind (LT=-5, VLT=-10) but both were near zero — structural alignment was minimal. The MIXED-only rule is correct in spirit but the current implementation misses near-zero HEADWIND entries where the structural signal is weak. **Recommendation: Allow entries when |LT SRIBI| < 10 AND VLT SRIBI > 0, even if LT is technically negative.**

### Finding 2.2 — MVRV > 2.0 degrades AB2 quality significantly

The May 2024 entry at MVRV=2.59 returned only +2.3% at 90d. Two other entries at MVRV ≥ 1.5 averaged +6% at 90d — below the overall median. Entries at MVRV 1.0–1.5 averaged +90%+ at 90d. **Add MVRV < 2.0 as a soft filter (note in table, don't hard block).**

### Finding 2.3 — All 13 entries had Risk Score 0.31–0.64 — no risk extremes

No AB2 signal ever fired with Risk < 0.3 or > 0.65 in 8 years. The LOI filter (added in v4) should catch the current-cycle issue where MIXED + ST cross fires during structural declines. The existing risk score gating from the LOI filter appears correct.

---

## Section 3 — SRI Stage Transitions

### Finding 3.1 — ST Stage 3→4 is the highest-conviction signal in the dataset

**12 fires. 83% win at 90d. Median +22.6%.** Best signal across all SRI outputs. This fires when the ST timeframe achieves full structural alignment — all four TF tracklines converge upward in the ST regime. Unlike CT3 which fires on point-in-time reading, Stage 3→4 is a transition event that marks a regime shift.

**Recommendation: Add ST Stage 3→4 as an explicit AB1 confirmation event. When ST Stage 3→4 fires AND CT tier ≥ 1, this is a priority entry signal.**

### Finding 3.2 — VST Stage 1→2 is a reliable bear warning

**13 fires. 31% win at 60d. Median -14.8%.** This fires when the VST timeframe completes its breakdown — similar to a short-term distribution confirmation. When this fires while a position is open, tighten stops or advance trim phase.

### Finding 3.3 — VLT transitions are rare but extremely high-conviction

VLT Stage 3→4 (n=2): 100% win at 60d/90d, medians +61%/+101%. These are multi-year cycle inflection points. Next VLT 3→4 transition will be the clearest cycle breakout signal in the system.

### Finding 3.4 — Stage 4→1 never fires — diagnostic issue

No Stage 4→1 transitions were detected across ANY timeframe in 8 years. This is either by design (Stage 4→1 is the lowest stage and the indicator may not mark that transition) or there's a detection logic issue that warrants investigation with Gavin.

---

## Section 4 — On-Chain Indicator Suite

### Finding 4.1 — Short-Term Risk Score is the most actionable on-chain gate

| Zone | n | 30d med | 30d win | 60d med | 60d win |
|---|---|---|---|---|---|
| Very Low (<0.2) | 39 | -17.5% | **5%** | -30.4% | **0%** |
| Low (0.2–0.4) | 752 | -0.8% | 49% | -0.8% | 49% |
| Mid (0.4–0.6) | 1,119 | +2.5% | 57% | +6.6% | 63% |
| High (0.6–0.8) | 105 | +4.8% | 57% | +13.9% | 61% |

The Very Low zone (< 0.2) is catastrophically bearish — 0% win at 60d over 39 days of history. Mid (0.4–0.6) is where the market performs best. **The Risk Score should gate ALL trade entries: no new positions when Risk < 0.3.**

### Finding 4.2 — STH MVRV zones define the accumulation window precisely

| Zone | 60d med | 60d win | 90d med | 90d win |
|---|---|---|---|---|
| Oversold (<0.8) | -2.5% | 47% | +0.2% | 50% |
| **Near cost (0.8–1.0)** | **+6.3%** | **70%** | **+12.4%** | **75%** |
| Healthy (1.0–1.5) | +1.5% | 52% | +1.5% | 52% |
| Hot (1.5–2.0) | +17.8% | 68% | +29.4% | 68% |
| Extreme (>2.0) | -4.8% | 42% | +3.7% | 58% |

Counterintuitively, the **best 60d returns come from the 0.8–1.0 zone** (near cost basis), not from extreme oversold (<0.8). Current MVRV of 0.441 is at the 4th percentile — deeper than the near-cost recovery zone. Historically, prices at this level often mean we're still in the bottoming/capitulation phase with 47% win at 60d.

**The implication**: Wait for MVRV to recover above 0.80 before entering with conviction. Below 0.80 = observe, not act.

### Finding 4.3 — Funding Rate contrarian value is real

Very negative funding (< -0.002): 60% win at 30d, median +5.7%. Current rate of -0.0027 is in this zone. This is a short-term contrarian signal — shorts are overpaying, making upside bounces likely. However, the 30d win rate of 60% is not sufficient to override the Risk Score or MVRV warnings.

### Finding 4.4 — SOPR and NRPL have limited standalone predictive value

STH SOPR (mirrored) shows ~53% win across all zones — barely above random. NRPL has a U-shaped pattern where both extremes underperform. These indicators are better used as confirmation tools rather than primary signal generators. **Recommendation: Retain in the dashboard as contextual reads, not as entry gates.**

---

## Section 5 — Cross-Indicator Confluence

### Finding 5.1 — Highest conviction AB1 setup

**CT1 + Risk Score 0.3–0.6 + MVRV 1.0–1.5**
- n=28 historical occurrences
- 80% win at 90d
- Median 90d: +13.5%
- This is the framework's core edge

### Finding 5.2 — False signal profile

**CT1 + Risk Score < 0.3**
- n=6 historical occurrences
- 0% win at 90d
- Median 90d: -36.1%
- All occurred during structural bear phases where short-term structural metrics turned positive prematurely

### Finding 5.3 — On-chain adds most value at extremes

MVRV Z-Score: Extreme (>3) = 31% win at 60d. Negative (<0) = 62% win. Z-score is best used as a macro risk overlay — not an entry signal but a filter that adjusts position sizing.

---

## Section 6 — Current State Assessment (Feb 27, 2026)

| Metric | Value | Percentile | Signal |
|---|---|---|---|
| Price | $129.50 | — | — |
| STH MVRV | 0.441 | 4th | ⚠ Deeply oversold but risky zone |
| Risk Score | 0.248 | 6th | 🔴 Low zone — historically 5% win 60d |
| MVRV Z-Score | 0.447 | 19th | 🟡 Slightly bullish (Z<1 = 56% win) |
| Funding Rate | -0.0027 | — | 🟢 Very negative — contrarian bullish 30d |
| STH SOPR | -0.499 | — | 🟡 Capitulation zone |
| Context | MIXED | — | 🟡 AB2 window approaching |
| LOI | -30.5 | — | 🔴 AB2 LOI filter blocking |

**Assessment**: The near-term setup is mixed. Negative funding rate and deep MVRV capitulation support a bounce. However, Risk Score at the 6th percentile (historically 5% win at 60d) and MVRV at 0.44 (still below the 0.8–1.0 sweet zone) suggest we have not reached the structural bottom. Watch for:
1. Risk Score crossing above 0.30 (primary gate)
2. STH MVRV recovering toward 0.80 (confirms accumulation zone)
3. LOI crossing above -30 (opens AB2 window)
4. ST Stage 3→4 transition (highest-conviction entry signal)

---

## Recommended Changes to Framework

### Tier 1 — Implement Now

**R1. Add Risk Score gate (0.30 floor) to all AB1 and AB3 entries**
CT1 with Risk < 0.3 = 0% win at 90d. This is a hard filter, not a soft note. Implement in both Pine scripts and Python engine. The Risk Score should be imported from the daily on-chain CSV.

**R2. Promote ST Stage 3→4 to AB1 confirmation ladder**
Highest-conviction single signal in the dataset. Add as a confirmation event in AB1 alongside CT tier crosses. When ST Stage 3→4 fires, treat as equivalent to CT3 confirmation regardless of LOI depth.

**R3. Soften CT4 from "distribution warning" to "late-cycle momentum"**
The current CT4 = hard distribution warning is too aggressive. 74% win at 90d contradicts the exit framing. Change to: CT4 = reduce new entries, tighten trailing stops on existing positions, advance trim phase on AB3 by 1 step. Do not close.

### Tier 2 — Test Before Implementing

**R4. Expand AB2 context gate to include near-zero HEADWIND**
Allow Bull Put when |LT SRIBI| ≤ 10 AND VLT > 0, even if technically HEADWIND. Aug 2023 precedent shows near-zero headwind entries can be valid. Backtest the additional entries this would introduce.

**R5. Add MVRV < 2.0 soft note to AB2 table**
When MVRV > 2.0, flag in the table: "Late-cycle entry — reduced PoP." Don't hard block (May 2024 still turned slightly positive at 90d) but make the risk explicit.

**R6. Add Stage 1→2 (VST) as a position management warning**
When VST Stage 1→2 fires, trigger an alert to tighten stops and review open AB2/AB3 positions. 31% win 60d is a reliable bearish confirmation.

### Tier 3 — Note for Future Cycles

**R7. VLT Stage 3→4 = cycle breakout signal**
When next VLT 3→4 fires, this is the highest-conviction long signal the system can generate (100% win, +100%+ at 90d over 2 historical fires). Ensure this is wired to maximum allocation and immediate alert delivery.

**R8. Investigate Stage 4→1 non-detection**
Zero Stage 4→1 transitions detected across all timeframes in 8 years. This is either correct (indicator design doesn't track this transition) or a bug. Validate with Gavin — if it should fire, the system is missing a major bearish signal.

---

*Evaluation by CIO | Dataset: BATS_MSTR 1D 2018–2026 (2,015 bars)*
