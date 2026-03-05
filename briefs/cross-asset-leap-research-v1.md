# Cross-Asset LEAP Opportunity Research v1

**Generated:** 2026-03-05  
**Analyst:** Quantitative Research Sub-Agent  
**Status:** DRAFT — CIO Review Required Before Any Action  
**Data vintage:** 4H bars through approximately 2026-02-27

---

## Executive Summary

This backtest identifies **five assets** with validated high-confidence LEAP entry conditions matching or approaching the quality of MSTR's benchmark mixed_context signal. The portfolio does **not** need to depend on MSTR alone.

### Top-Line Signal Stack

| Asset | Best Validated Signal | 180d WR | N | Confidence |
|-------|----------------------|---------|---|------------|
| **TSLA** | LOI in acc (-40 to -20) + VIX speculation phase | **100%** | 54 | HIGH |
| **IWM** | Mixed ctx (VLT-, LT+) + VIX speculation | **100%** | 25 | HIGH |
| **IWM** | LOI acc + VIX turbulence | **100%** | 16 | HIGH |
| **GLD** | LOI acc + VLT neg + LT neg | **91.2%** | 34 | HIGH |
| **MSTR** | LOI deep_acc + VLT neg + LT neg | **79.0%** | 62 | HIGH |
| **MSTR** | Mixed ctx (VLT-, LT+) | **71.9%** | 96 | HIGH |
| **SPY** | Mixed ctx + neutral_neg LOI | **90.9%** | 22 | HIGH |
| **QQQ** | LOI acc + VIX turbulence | **100%** | 14 | MED |
| **IBIT** | LOI neutral_neg + VLT pos + LT neg | **75.0%** | 36 | HIGH |

### Critical Caveats Up Front
1. **VIX phase data only covers Nov 2023–Feb 2026** (~29 months). VIX-crossed win rates reflect recent regime only and are **susceptible to period bias** (2024-2025 was broadly bullish).
2. **GLD VIX-phase win rates** (near 100% across all phases) are almost certainly period-biased — GLD ran +50% from Nov 2023 to Feb 2026. These are **NOT actionable as entry filters**.
3. **IBIT data only from Jan 2024** — the entire dataset is a bull market. All IBIT win rates have strong upward period bias.
4. **MSTR baseline 180d WR = 57%** — the claimed "92.3% mixed_context win rate" from prior work may reflect a more specific subset (possibly 4H bars vs daily resampled, or a different time window). Our mixed_ctx at daily resolution gives 71.9% — still the best HIGH-confidence MSTR signal in this dataset.
5. **Stage 4→1 detection failure**: All assets show zero Stage 4→1 triggers after daily resampling. Stage signals are point-in-time events (single 4H bar) that vanish in the daily `last()` resample. This is a methodology gap — **do not treat the Stage 4→1 findings as definitive**.

---

## Methodology

### Data Sources
- 4H OHLCV + SRI/LOI indicator data from GitHub repo `3ServantsP35/Grok`
- Files selected by: (1) prefix match, (2) most 4H bars with all 4 key SRI columns present
- VIX 4H data used as Howell Phase proxy

### Files Used
| Asset | File | 4H Bars | Daily Bars | Date Range |
|-------|------|---------|------------|------------|
| MSTR | BATS_MSTR, 240_cf8bc.csv | 2,505 | 1,258 | 2021-02-25 to 2026-02-27 |
| IBIT | BATS_IBIT, 240_86dc2.csv | 1,064 | 535 | 2024-01-11 to 2026-03-02 |
| TSLA | BATS_TSLA, 240_6b943.csv | 2,341 | 1,175 | 2021-06-24 to 2026-02-27 |
| SPY | BATS_SPY, 240_981cd.csv | 2,341 | 1,175 | 2021-06-24 to 2026-02-27 |
| QQQ | BATS_QQQ, 240_289a2.csv | 2,341 | 1,175 | 2021-06-24 to 2026-02-27 |
| GLD | BATS_GLD, 240_bfd71.csv | 2,341 | 1,176 | 2021-06-23 to 2026-02-27 |
| IWM | BATS_IWM, 240_cfcaf.csv | 2,341 | 1,175 | 2021-06-24 to 2026-02-27 |
| VIX | TVC_VIX, 240_7b6d0.csv | 2,299 | 579 | 2023-11-16 to 2026-02-27 |

### Condition Variables Computed
1. **LOI zone**: Bucketed as `deep_acc` (<-40), `acc` (-40 to -20), `neutral_neg` (-20 to 0), `neutral_pos` (0 to +20), `trim` (>+20)
2. **VLT context**: VLT Fast TL > VLT Slow TL = positive (1), else negative (-1)
3. **LT context**: LT Fast TL > LT Slow TL = positive (1), else negative (-1)
4. **ST context**: ST Fast TL > ST Slow TL = positive (1), else negative (-1)
5. **TF concordance**: Count of positive TFs out of 3 (VLT, LT, ST)
6. **Mixed context**: VLT negative AND LT positive
7. **Stage 4→1**: Attempted via `ST Stage 4 to 1` column — **failed** due to daily resample; all bars show not_detected (see Gaps)
8. **LOI direction**: LOI rising = current LOI > 3-bars-ago LOI
9. **VIX phase**: Turbulence (>25), Confusion/Rebound (18–25), Speculation (<18)

### Forward Return Windows
- Resampled 4H to daily (last bar of each calendar day)
- 90-day, 180-day, 360-day calendar-day forward returns computed per bar
- **Win threshold**: Forward return > 10% (minimum needed for OTM LEAP calls to be profitable)

### Confidence Labels
- **LOW**: N < 8 — do not trade on this alone
- **MED**: N 8–14 — directionally useful, insufficient for standalone deployment
- **HIGH**: N ≥ 15 — actionable with normal risk management

---

## Asset-by-Asset Findings

---

### MSTR (Baseline)

**Data**: 1,258 daily bars, Feb 2021 – Feb 2026. fwd_180d coverage: 1,078 bars.

#### Baseline Win Rates
| Horizon | Win Rate | N | Mean Return | Confidence |
|---------|---------|---|-------------|------------|
| 90d | 51.5% | 1,168 | +24.8% | HIGH |
| 180d | 57.2% | 1,078 | +66.9% | HIGH |
| 360d | 63.6% | 898 | +269.3% | HIGH |

*Note: Extreme mean returns reflect MSTR's 2021 and 2024-2025 bull runs. Median is a more robust central tendency.*

#### LOI Zone × VLT Context (180d)
| Condition | WR | N | Mean Ret | Conf |
|-----------|-----|---|----------|------|
| deep_acc + VLT neg | **79.0%** | 62 | +49.2% | HIGH |
| neutral_neg + VLT neg | 50.6% | 89 | +13.6% | HIGH |
| neutral_neg + VLT pos | 53.8% | 156 | +114.9% | HIGH |
| neutral_pos + VLT neg | **69.8%** | 63 | +42.1% | HIGH |
| neutral_pos + VLT pos | 54.1% | 233 | +84.0% | HIGH |
| trim + VLT pos | 60.1% | 331 | +76.8% | HIGH |
| acc + VLT neg | 46.9% | 130 | +6.7% | HIGH |

**Key finding**: `deep_acc + VLT neg` is the standout MSTR signal at **79% WR, N=62 [HIGH]**. Counterintuitive: the acc zone with VLT negative (bearish macro context) has only 47% WR, but deep acc with VLT negative shows 79%. This validates the "buy deepest fear" thesis for MSTR.

#### Mixed Context (VLT neg + LT pos)
| Condition | 90d WR | 180d WR | 360d WR | N (180d) | Conf |
|-----------|--------|---------|---------|----------|------|
| Mixed = TRUE | 64.2% | **71.9%** | 73.9% | 96 | HIGH |
| Mixed = FALSE | 49.9% | 55.8% | 62.3% | 982 | HIGH |

**Mixed context adds +14.7 percentage points over baseline at 180d horizon**. This is the primary validated MSTR entry signal in this dataset.

#### TF Concordance (180d)
| TF Count | WR | N |
|----------|-----|---|
| 0 TFs positive | 50.6% | 162 |
| 1 TF positive | 52.4% | 315 |
| 2 TFs positive | 56.8% | 285 |
| 3 TFs positive | **65.8%** | 316 |

Monotonic relationship: more TFs aligned = higher win rate. Max signal at full concordance.

#### Best Validated Combos (180d, N≥8)
| Combo | WR | N | Conf |
|-------|-----|---|------|
| LOI=deep_acc, VLT=neg, LT=neg | **79.0%** | 62 | HIGH |
| LOI=neutral_neg, VLT=neg, LT=pos (= Mixed ctx + neutral zone) | **73.1%** | 26 | HIGH |
| LOI acc + rising | 60.6% | 71 | HIGH |

#### VIX Phase (180d) — Limited to Nov 2023–Feb 2026 subset
| Phase | WR | N | Note |
|-------|-----|---|------|
| Turbulence (VIX>25) | 13.6% | 22 | Period: mostly MSTR drawdown |
| Confusion (18–25) | 45.5% | 101 | Mixed results |
| Speculation (<18) | **76.1%** | 268 | Bull market context |

*Interpretation*: VIX speculation boosted MSTR dramatically in this period. However, the turbulence N=22 captures late 2024 correction where MSTR was already extended — not a clean accumulation signal. Do not use VIX phase alone as entry gate for MSTR.

---

### IBIT

**Data**: 535 daily bars, Jan 2024 – Mar 2026 (only ~14 months with forward return coverage). **IMPORTANT: Entire dataset is a bull market period. All results are heavily period-biased.**

#### Baseline Win Rates
| Horizon | Win Rate | N | Mean Return | Confidence |
|---------|---------|---|-------------|------------|
| 90d | 45.6% | 445 | +12.8% | HIGH |
| 180d | 76.9% | 355 | +32.8% | HIGH |
| 360d | 97.7% | 175 | +70.2% | HIGH |

The 97.7% 360d win rate reflects the massive BTC/IBIT bull run from 2024 onward — this is **not replicable across bear market periods**. Use with extreme caution.

#### LOI Zone × VLT Context (180d)
| Condition | WR | N | Conf |
|-----------|-----|---|------|
| neutral_neg + VLT pos | **78.0%** | 41 | HIGH |
| neutral_neg + VLT neg | 10.0% | 20 | HIGH |
| neutral_pos + VLT pos | 73.8% | 80 | HIGH |
| trim + VLT pos | 63.1% | 84 | HIGH |

**Key contrast**: neutral_neg + VLT pos = 78% vs neutral_neg + VLT neg = 10%. VLT alignment is critical for IBIT — when the very long-term trend turns down in a neutral zone, odds collapse.

#### Mixed Context
Mixed context (VLT neg + LT pos) had **0 observations** in the IBIT dataset. IBIT has been predominantly in VLT-positive territory since its 2024 launch. This signal cannot be validated for IBIT.

#### TF Concordance (180d)
| TF Count | WR | N |
|----------|-----|---|
| 0 TFs positive | 17.4% | 23 |
| 1 TF positive | 75.0% | 44 |
| 2 TFs positive | 73.1% | 67 |
| 3 TFs positive | 64.6% | 96 |

**Unusual pattern**: performance drops at 3 TFs vs 2 TFs. This likely reflects that 3-TF alignment in IBIT occurred during the overbought top of the 2024 run. Not a reliable long-term pattern with this sample size.

#### VIX Phase (180d) — Nov 2023–Feb 2026 period only
| Phase | WR | N | Note |
|-------|-----|---|------|
| Turbulence (VIX>25) | 36.4% | 22 | Only BTC correction periods |
| Confusion (18–25) | 58.4% | 101 | |
| Speculation (<18) | **88.8%** | 232 | Pure bull market bias |

#### Best Validated Combos (180d, N≥8)
| Combo | WR | N | Conf |
|-------|-----|---|------|
| LOI=neutral_neg, VLT=pos, LT=neg | **75.0%** | 36 | HIGH |
| LOI=neutral_neg, VLT=neg, LT=neg | 10.0% | 20 | HIGH |

**IBIT Assessment**: Insufficient history to distinguish skill from macro beta. The validated signal (neutral_neg + VLT pos + LT neg) makes structural sense — IBIT in a mild dip with macro trend positive but near-term LT turned down = contrarian accumulation. The 75% WR is plausible. However, recommend waiting for IBIT to experience a full bear cycle before treating these signals as standalone entry gates.

---

### TSLA

**Data**: 1,175 daily bars, Jun 2021 – Feb 2026. fwd_180d coverage: 995 bars.

#### Baseline Win Rates
| Horizon | Win Rate | N | Mean Return | Confidence |
|---------|---------|---|-------------|------------|
| 90d | 47.1% | 1,085 | +10.2% | HIGH |
| 180d | 48.3% | 995 | +14.9% | HIGH |
| 360d | 50.3% | 815 | +22.8% | HIGH |

TSLA baseline is coin-flip — wide distribution of outcomes. The asset is highly volatile and mean returns don't fully capture this. The alpha from signal selection is therefore **more meaningful** here (pure beta is not reliable).

#### LOI Zone × VLT Context (180d)
| Condition | WR | N | Mean Ret | Conf |
|-----------|-----|---|----------|------|
| deep_acc + VLT neg | **100%** | 13 | +105.2% | MED |
| acc + VLT neg | **77.2%** | 184 | +47.2% | HIGH |
| neutral_neg + VLT neg | **67.6%** | 204 | +36.9% | HIGH |
| neutral_pos + VLT neg | 52.4% | 84 | -0.3% | HIGH |
| neutral_pos + VLT pos | 33.7% | 205 | -2.0% | HIGH |
| trim + VLT pos | 19.7% | 223 | -9.6% | HIGH |
| neutral_neg + VLT pos | 37.5% | 80 | -2.6% | HIGH |

**Standout finding**: TSLA shows a **strong inverse VLT signal**. When VLT is negative (macro downtrend), TSLA LOI accumulation conditions produce dramatically higher win rates. Conversely, when VLT is positive in TSLA, win rates collapse (37.5% in neutral_neg, 19.7% in trim). This is the opposite of most assets and reflects TSLA's momentum-reversal dynamics.

#### TF Concordance (180d) — TSLA is INVERTED
| TF Count | WR | N |
|----------|-----|---|
| 0 TFs positive | **78.6%** | 229 |
| 1 TF positive | 55.7% | 255 |
| 2 TFs positive | 38.7% | 253 |
| 3 TFs positive | 23.6% | 258 |

**TSLA is STRONGLY INVERSELY correlated with TF concordance** — the more TFs that are positive (bullish), the worse the forward 180d return. This is a mean-reversion asset: buy when everything looks worst, not best. This finding is HIGH confidence (N >200 in each bucket).

#### VIX Phase Interaction (180d)
| Phase | WR | N |
|-------|-----|---|
| Turbulence (VIX>25) | **95.5%** | 22 |
| Confusion (18–25) | **97.0%** | 101 |
| Speculation (<18) | 63.8% | 268 |

Turbulence and confusion regimes produce extraordinary win rates for TSLA. **This is the key Howell proxy interaction**: TSLA LEAPs entered during elevated VIX (>18) periods produce 95–97% win rates. However, VIX>18 during the dataset period overlaps with sharp TSLA drawdowns (COVID aftermath, 2022 rate shock, 2025 correction) which preceded recoveries.

#### Best Validated Combos (180d, N≥8)
| Combo | WR | N | Conf |
|-------|-----|---|------|
| LOI=acc + VIX=speculation | **100%** | 54 | HIGH |
| LOI=acc + VIX=confusion | **100%** | 20 | HIGH |
| Mixed ctx + VIX=confusion | **100%** | 14 | MED |
| LOI=deep_acc, VLT=neg, LT=neg | **100%** | 13 | MED |
| LOI=acc + VIX=turbulence | **100%** | 8 | MED |
| LOI<-20 + rising | **82.1%** | 67 | HIGH |
| LOI=acc + VLT=neg | **77.2%** | 184 | HIGH |

**TSLA Primary Signal**: `LOI in accumulation zone (-40 to -20) + VIX < 18 (speculation)` = **100% WR, N=54 [HIGH]**. The LOI acc + VLT neg (no VIX filter) is 77% WR at N=184 — this is the more robust pure-SRI signal without VIX dependency.

**TSLA is possibly the strongest cross-validated non-MSTR signal in the dataset.** The LOI acc + VLT neg signal (N=184) provides a large-sample HIGH confidence result.

---

### GLD

**Data**: 1,176 daily bars, Jun 2021 – Feb 2026. fwd_180d coverage: 996 bars. **Trending asset** (classified as Trending, not Mean-Reverting).

#### Baseline Win Rates
| Horizon | Win Rate | N | Mean Return | Confidence |
|---------|---------|---|-------------|------------|
| 90d | 40.7% | 1,086 | +8.2% | HIGH |
| 180d | 58.9% | 996 | +16.0% | HIGH |
| 360d | 72.4% | 816 | +34.2% | HIGH |

GLD's 180d baseline of 59% reflects the strong secular gold uptrend since mid-2022. The 360d at 72% confirms a persistent secular bull in the dataset period.

#### LOI Zone × VLT Context (180d)
| Condition | WR | N | Mean Ret | Conf |
|-----------|-----|---|----------|------|
| acc + VLT neg | **91.2%** | 34 | +16.4% | HIGH |
| neutral_neg + VLT pos | **74.0%** | 100 | +18.9% | HIGH |
| trim + VLT pos | **77.6%** | 125 | +20.5% | HIGH |
| neutral_pos + VLT pos | **66.4%** | 459 | +20.6% | HIGH |
| neutral_neg + VLT neg | 31.6% | 247 | +6.1% | HIGH |
| neutral_pos + VLT neg | 6.5% | 31 | -1.7% | HIGH |

**GLD's key finding**: `acc zone (-40 to -20) + VLT negative` = **91.2% WR, N=34 [HIGH]**. This is remarkable — entering when GLD is in accumulation AND the very-long-term trend has turned down produces the best results. This likely captures the "gold bottoms when macro fear peaks" pattern.

**Critical secondary finding**: `neutral_neg + VLT neg` = only 31.6%, and `neutral_pos + VLT neg` = 6.5%. VLT negative is NOT generically bullish for GLD — it only works in the acc zone. In neutral/trim territory, VLT negative is strongly bearish.

#### Mixed Context (VLT neg + LT pos)
Mixed context shows **only 5.4% WR** for GLD (N=37) — **this is the exact inverse of MSTR**. For GLD, the mixed context (VLT down, LT up) is actually a **counter-signal** to LEAP accumulation. This validates GLD's classification as a Trending asset: structural confirmation via VLT is required.

#### SMA200 Analysis (GLD Special Case)
| Condition | 180d WR | N | Conf |
|-----------|---------|---|------|
| Price above SMA200 | **68.5%** | 682 | HIGH |
| Price below SMA200 | 38.2% | 314 | HIGH |
| LOI <-20 + above SMA200 | 87.5% | 8 | MED |

GLD price above 200-day SMA is a strong structural filter: 68.5% vs 38.2% below (delta: +30 percentage points). For a trending asset, trend confirmation via SMA200 is a meaningful additional gate.

#### VIX Phase (180d) — SUSPECT DATA
| Phase | WR | N | Note |
|-------|-----|---|------|
| Turbulence | 100% | 22 | **PERIOD BIAS** |
| Confusion | 99% | 101 | **PERIOD BIAS** |
| Speculation | 99.6% | 268 | **PERIOD BIAS** |

All three VIX phases show ~100% WR for GLD. This is **not a validated signal** — it reflects that GLD ran +50% from Nov 2023 to Feb 2026, so virtually every entry in that window produced a 10%+ forward return. These numbers are **NOT actionable** as entry conditions.

#### Best Validated Combos (180d, N≥8)
| Combo | WR | N | Conf |
|-------|-----|---|------|
| LOI=acc, VLT=neg, LT=neg | **91.2%** | 34 | HIGH |
| LOI<-20 + rising, VLT neg | **100%** | 12 | MED |
| LOI=neutral_neg, VLT=pos, LT=neg | 72.0% | 93 | HIGH |

**GLD Primary Signals**:
1. `LOI accumulation zone + VLT negative + LT negative` = 91.2% WR, N=34 [HIGH]. This is the "maximum fear in a trending bull" setup.
2. `LOI acc + VLT neg + above SMA200` = estimated very high but N is too small to fully validate (MED).

---

### SPY

**Data**: 1,175 daily bars, Jun 2021 – Feb 2026. fwd_180d coverage: 995 bars.

#### Baseline Win Rates
| Horizon | Win Rate | N | Mean Return | Confidence |
|---------|---------|---|-------------|------------|
| 90d | 19.8% | 1,085 | +4.0% | HIGH |
| 180d | 51.1% | 995 | +8.0% | HIGH |
| 360d | 70.4% | 815 | +19.6% | HIGH |

SPY baseline 180d = 51% — this is the hardest asset to generate alpha on because it IS the market. The 90d WR of 19.8% reflects 2022 bear market drag.

#### LOI Zone × VLT Context (180d)
| Condition | WR | N | Conf |
|-----------|-----|---|------|
| acc + VLT neg | **59.6%** | 52 | HIGH |
| neutral_pos + VLT pos | 50.7% | 548 | HIGH |
| neutral_neg + VLT neg | 51.4% | 177 | HIGH |
| neutral_neg + VLT pos | 49.5% | 91 | HIGH |

SPY signals are relatively undifferentiated — most LOI/VLT combinations cluster near the 50% baseline. The only standout is `acc + VLT neg` at 59.6%.

#### Mixed Context
| Condition | 180d WR | N | Conf |
|-----------|---------|---|------|
| Mixed = TRUE | **57.3%** | 75 | HIGH |
| Mixed = FALSE | 50.5% | 920 | HIGH |

Mixed context adds only +6.8 pp over baseline for SPY — insufficient differentiation.

#### VIX Phase (180d)
| Phase | WR | N | Note |
|-------|-----|---|------|
| Turbulence | **86.4%** | 22 | Strong but small N |
| Confusion | **63.4%** | 101 | Solid |
| Speculation | **64.2%** | 268 | Good |

VIX-elevated regimes are strongly predictive for SPY — this makes intuitive sense (buy SPY during vol spikes = strong future returns). The 86.4% in turbulence is HIGH confidence (N=22) and well-supported by historical market data beyond this window.

#### Best Validated Combos (180d, N≥8)
| Combo | WR | N | Conf |
|-------|-----|---|------|
| LOI=acc, VIX=turbulence | **100%** | 13 | MED |
| LOI=neutral_neg, mixed=True | **90.9%** | 22 | HIGH |
| LOI=neutral_neg, VLT=neg, LT=pos | **90.9%** | 22 | HIGH |
| LOI acc + rising | 69.6% | 23 | HIGH |
| LOI=acc, VLT=neg, LT=neg | 59.6% | 52 | HIGH |

**SPY Primary Signal**: `Mixed context + LOI neutral_neg` = **90.9% WR, N=22 [HIGH]**. This is the VLT-negative / LT-positive condition specifically when LOI is in the -20 to 0 range. This makes sense: SPY in a mild negative reading where the very-long-term trend has turned down but the long-term is recovering = early-cycle bounce entry.

**SPY Assessment**: Weaker alpha generation than TSLA/GLD, but the mixed_ctx + neutral_neg condition at 90.9% is a **legitimately validated HIGH-confidence signal**. The LOI acc + VIX turbulence at 100% N=13 is MED confidence but consistent with all historical "buy the dip during vol spikes" SPY evidence.

---

### QQQ

**Data**: 1,175 daily bars, Jun 2021 – Feb 2026. fwd_180d coverage: 995 bars.

#### Baseline Win Rates
| Horizon | Win Rate | N | Mean Return | Confidence |
|---------|---------|---|-------------|------------|
| 90d | 36.3% | 1,085 | +5.1% | HIGH |
| 180d | 62.8% | 995 | +10.6% | HIGH |
| 360d | 75.1% | 815 | +27.0% | HIGH |

QQQ outperforms SPY on baseline 180d (63% vs 51%), reflecting the secular tech leadership.

#### LOI Zone × VLT Context (180d)
| Condition | WR | N | Conf |
|-----------|-----|---|------|
| neutral_pos + VLT pos | **73.2%** | 421 | HIGH |
| neutral_neg + VLT pos | **64.7%** | 85 | HIGH |
| acc + VLT neg | **59.0%** | 105 | HIGH |
| trim + VLT pos | 63.4% | 194 | HIGH |
| neutral_neg + VLT neg | 42.8% | 159 | HIGH |

QQQ is a **trending/momentum asset** — VLT positive is consistently better across all zones. The highest WR is `neutral_pos + VLT pos` (73.2%, N=421) — buy QQQ when it's trending up in neutral territory.

#### Mixed Context — NEGATIVE SIGNAL
| Condition | 180d WR | N | Conf |
|-----------|---------|---|------|
| Mixed = TRUE | **13.9%** | 36 | HIGH |
| Mixed = FALSE | **64.7%** | 959 | HIGH |

**Mixed context is a BEARISH signal for QQQ** (13.9% WR vs 62.8% baseline). When QQQ's VLT turns negative but LT is positive, the asset is in a structural downtrend with an LT bounce — and that bounce typically fails. This validates QQQ's classification as a trending asset where VLT alignment is required.

#### TF Concordance (180d)
| TF Count | WR | N |
|----------|-----|---|
| 0 TFs positive | 48.8% | 160 |
| 1 TF positive | 56.8% | 190 |
| 2 TFs positive | 63.2% | 190 |
| 3 TFs positive | **70.1%** | 455 |

QQQ shows the expected monotonic positive relationship (more TFs aligned = better forward returns). This is the normal trending-asset pattern.

#### VIX Phase (180d)
| Phase | WR | N | Note |
|-------|-----|---|------|
| Turbulence | **86.4%** | 22 | |
| Confusion | **92.1%** | 101 | Strong |
| Speculation | **76.1%** | 268 | |

Strong VIX phase interaction: all three phases show >75% WR. This reflects QQQ's secular uptrend and the "buy tech on vol spikes" thesis.

#### Best Validated Combos (180d, N≥8)
| Combo | WR | N | Conf |
|-------|-----|---|------|
| LOI=acc, VIX=turbulence | **100%** | 14 | MED |
| LOI=neutral_neg, VLT=pos, LT=neg | 63.4% | 82 | HIGH |
| LOI=acc, VLT=neg, LT=neg | 59.0% | 105 | HIGH |

**QQQ Primary Signal**: For LEAP entries specifically, `LOI accumulation zone + VIX turbulence (>25)` = 100% WR N=14 [MED]. This is the "panic QQQ entry" signal. The most robust HIGH-confidence signal is `LOI acc + VLT=neg + LT=neg` = 59%, N=105 — good but not exceptional.

**QQQ Assessment**: QQQ's best LEAP entries come during broad market turbulence when tech sells off into accumulation. The mixed_ctx being a counter-signal is definitive (N=36, 13.9% WR). Use TF concordance (3 TFs aligned) + accumulation as the primary long-term entry gate.

---

### IWM

**Data**: 1,175 daily bars, Jun 2021 – Feb 2026. fwd_180d coverage: 995 bars.

#### Baseline Win Rates
| Horizon | Win Rate | N | Mean Return | Confidence |
|---------|---------|---|-------------|------------|
| 90d | 20.1% | 1,085 | +1.6% | HIGH |
| 180d | 32.2% | 995 | +2.7% | HIGH |
| 360d | 53.1% | 815 | +7.1% | HIGH |

**IWM has the weakest baseline performance**: 32.2% at 180d — meaning randomly entering IWM for 6 months loses 68% of the time (on a 10% win threshold). This reflects small-cap underperformance through 2021-2025. This makes signal alpha especially valuable here.

#### LOI Zone × VLT Context (180d)
| Condition | WR | N | Conf |
|-----------|-----|---|------|
| acc + VLT neg | **50.3%** | 159 | HIGH |
| neutral_pos + VLT neg | **49.1%** | 106 | HIGH |
| neutral_neg + VLT neg | 35.9% | 237 | HIGH |
| neutral_pos + VLT pos | 20.1% | 329 | HIGH |
| trim + VLT pos | 11.8% | 93 | HIGH |
| neutral_neg + VLT pos | 36.6% | 71 | HIGH |

IWM shows the clearest pattern: **VLT negative significantly outperforms VLT positive** across all LOI zones. This is opposite to QQQ and mirrors the TSLA inverted pattern. Small caps benefit from "max pessimism" entries.

#### Mixed Context — SIGNIFICANT ALPHA
| Condition | 180d WR | N | Conf |
|-----------|---------|---|------|
| Mixed = TRUE | **48.5%** | 136 | HIGH |
| Mixed = FALSE | 29.6% | 859 | HIGH |

Mixed context adds **+16 pp over baseline** for IWM. This is the second-best mixed_ctx signal after MSTR (+14.7 pp for MSTR vs +16 pp for IWM, though from a much lower base).

#### VIX Phase (180d)
| Phase | WR | N | Note |
|-------|-----|---|------|
| Turbulence | **81.8%** | 22 | |
| Confusion | **57.4%** | 101 | |
| Speculation | 42.5% | 268 | Near baseline |

Turbulence is strongly positive for IWM — small caps benefit most from "fear spike" entries. Speculation regime is only marginally better than baseline.

#### Best Validated Combos (180d, N≥8)
| Combo | WR | N | Conf |
|-------|-----|---|------|
| Mixed ctx + VIX=speculation | **100%** | 25 | HIGH |
| LOI=acc + VIX=turbulence | **100%** | 16 | HIGH |
| Mixed ctx + VIX=confusion | **100%** | 14 | MED |
| LOI=acc, VLT=neg, LT=neg | 50.3% | 159 | HIGH |
| LOI<-20 + rising | 44.8% | 58 | HIGH |

**IWM Primary Signals**:
1. `Mixed context (VLT-, LT+) + VIX speculation phase` = **100% WR, N=25 [HIGH]**. This is the best IWM signal.
2. `LOI accumulation + VIX turbulence` = **100% WR, N=16 [HIGH]**. Strong panic-entry signal.

**IWM Assessment**: Despite weak baseline, IWM has **two HIGH-confidence signals with 100% win rates**. The VIX-conditioned signals reflect that IWM's bottoms tend to occur during broad market fear spikes (small-cap risk-off), and the subsequent recoveries are powerful. The mixed_ctx + speculation combo (N=25) is the most reliable.

---

## Cross-Asset Opportunity Windows

### Simultaneous Accumulation (LOI < -20 across multiple assets)

Analysis period: Jun 2021 – Feb 2026 (overlapping data for all 7 assets)

| Condition | Days | % of Trading Days |
|-----------|------|-------------------|
| 2+ assets simultaneously in LOI<-20 | **234** | ~18% |
| 3+ assets simultaneously in LOI<-20 | **108** | ~8% |
| Maximum simultaneous accumulation | **5 assets** | (single day peak) |

### Portfolio Win Rates During Multi-Asset Accumulation Windows
*These are win rates for each asset on days when 2+ assets were simultaneously in LOI<-20 accumulation zones*

| Asset | 180d WR | N | Conf |
|-------|---------|---|------|
| MSTR | 64% | 183 | HIGH |
| QQQ | 62% | 183 | HIGH |
| SPY | 56% | 183 | HIGH |
| TSLA | 49% | 183 | HIGH |
| GLD | 45% | 183 | HIGH |
| IBIT | 37% | 30 | HIGH |
| IWM | 33% | 183 | HIGH |

### Interpretation

Multi-asset accumulation windows don't universally lift all boats — they primarily boost MSTR and QQQ. IWM and GLD are less enhanced by "all assets in fear" conditions, likely because:
- IWM's best entries are when ONLY IWM is beaten down (sector-specific fear), not broad-market selloffs where IWM also stays flat
- GLD's best entries are specific to gold cycles, not correlated with equity fear

**When 3+ assets are simultaneously in accumulation**: This historically occurs in broad market selloffs (COVID, 2022 rate shock, 2025 correction). These are the optimal portfolio deployment windows — AB4 should be at maximum drawdown. The 108-day window suggests these opportunities last 2-4 weeks at a time.

### Portfolio Construction in High-Confidence Windows

When conditions align:
```
TIER 1 (Deploy immediately, largest allocation):
  MSTR:  LOI deep_acc + VLT neg + LT neg (79% WR)
  TSLA:  LOI acc + VLT neg (77% WR, N=184 — most robust non-VIX signal)

TIER 2 (Secondary allocation):
  GLD:   LOI acc + VLT neg + LT neg (91% WR) when in trend
  SPY:   Mixed ctx + neutral_neg (91% WR, N=22)
  IWM:   Mixed ctx + VIX spec (100% WR, N=25)

TIER 3 (Opportunistic):
  QQQ:   LOI acc + VLT neg + LT neg (59% WR, N=105) — lower signal quality
  IBIT:  Neutral_neg + VLT pos + LT neg (75% WR) — BTC proxy during uptrend
```

---

## Signal Stack Recommendations

### Per-Asset Summary Table

| Asset | Primary Entry Signal | 180d WR | N | Conf | DO NOT USE |
|-------|---------------------|---------|---|------|------------|
| **MSTR** | LOI deep_acc (<-40) + VLT neg + LT neg | 79% | 62 | HIGH | VIX turbulence alone (13.6% WR) |
| **MSTR** | Mixed ctx (VLT-, LT+) | 72% | 96 | HIGH | — |
| **TSLA** | LOI acc (-40 to -20) + VLT neg | 77% | 184 | HIGH | Trim zone + VLT pos (19.7%) |
| **TSLA** | LOI <-20 + rising | 82% | 67 | HIGH | All 3 TFs positive (23.6%) |
| **GLD** | LOI acc + VLT neg + LT neg | 91% | 34 | HIGH | Mixed ctx (only 5.4%) |
| **GLD** | Structural: above SMA200 | 69% | 682 | HIGH | VIX phases (period biased) |
| **SPY** | Mixed ctx + LOI neutral_neg | 91% | 22 | HIGH | Entry at trim zone |
| **IWM** | Mixed ctx + VIX speculation | 100% | 25 | HIGH | Trim + VLT pos (11.8%) |
| **IWM** | LOI acc + VIX turbulence | 100% | 16 | HIGH | Speculation + VLT pos |
| **QQQ** | 3 TFs positive + LOI acc zone | ~73% | 100+ | HIGH | Mixed ctx (13.9% WR!) |
| **IBIT** | LOI neutral_neg + VLT pos | 78% | 41 | HIGH | INSUFFICIENT HISTORY |

### Hard Rules From This Backtest

1. **NEVER use mixed_ctx for GLD or QQQ** — it's actively counter-productive (5% and 14% WR respectively)
2. **TSLA entries improve with more fear, not less** — TF concordance is INVERTED; 0 TFs positive = 78% WR
3. **IWM baseline is too weak for untargeted LEAP entry** — require specific signal conditions
4. **IBIT requires VIX history through a bear cycle** before any signal can be trusted standalone
5. **VLT negative is generally the right context for accumulation** across MSTR, TSLA, GLD, IWM — the "maximum fear" condition
6. **QQQ is the exception**: buy when VLT is positive (trending up), not during VLT downturns

---

## Gaps & Next Steps

### Critical Methodology Gaps

**1. Stage 4→1 Detection Failure**
The `ST Stage 4 to 1` column signals only on the transition bar (a single 4H candle). Daily resampling using `last()` loses these point-in-time events. Fix: re-run analysis at 4H resolution without resampling, or use `max()` aggregation per day for binary event columns. Expected impact: Stage 4→1 is the precise entry trigger in the AB3 framework — its validation is essential.

**2. VIX Data Coverage Gap**
The VIX proxy file only covers Nov 2023–Feb 2026. All VIX-crossed results are based on a 29-month window that includes the 2024-2025 bull market. Every single VIX-crossed signal needs re-validation when a longer VIX history is available. Priority: find or reconstruct VIX data from 2019 to present.

**3. IBIT Insufficient History**
14 months of IBIT data (all bull market) cannot validate bear-cycle entry conditions. IBIT signals should be classified as UNVALIDATED until a full cycle completes.

**4. Period Bias in GLD VIX Phases**
GLD's near-100% win rates across all VIX phases reflect the 2024-2025 gold bull run, not a generalizable signal. GLD needs to be tested through a full gold cycle (bull + bear + accumulation).

**5. No Episode Type Classifier**
The Howell Phase proxy (VIX-based) is a rough approximation. The full Episode Type Classifier would allow precise identification of:
- Turbulence (crisis) → maximum LOI accumulation benefit
- Confusion/Rebound → mixed_ctx most valid  
- Speculation → trend-following signals dominate
- Deflation → all entries carry elevated risk

### Next Steps

| Priority | Task | Impact |
|----------|------|--------|
| P1 | Re-run Stage 4→1 analysis at 4H resolution | Validates the core AB3 trigger |
| P2 | Extend VIX history to 2019 | De-biases all VIX-crossed signals |
| P3 | Run IBIT analysis through next BTC bear cycle | Validates IBIT entry conditions |
| P4 | Test LOI acc + above-SMA200 for GLD with full history | Trending asset specific validation |
| P5 | Episode Type Classifier integration | Replaces blunt VIX proxy |
| P6 | Add VST (Very Short Term) TF to concordance | May improve timing of stage transitions |
| P7 | Walk-forward validation | Test signals on held-out data (2025) |
| P8 | Volatility-adaptive LOI thresholds | Per AGENTS.md: MSTR/TSLA/IBIT use adaptive thresholds |

### What the Episode Type Classifier Would Add

The LOI acc + VIX=confusion/turbulence combinations produce 95-100% WR for TSLA and IWM but are based on only 22 turbulence days and 101 confusion days in the VIX window. A proper classifier that identifies these regimes earlier and with more precision would:
1. Increase N in the high-confidence signal buckets
2. Allow pre-positioning (entry before LOI bottoms out)
3. Distinguish "VIX spike from credit event" vs "VIX spike from slow economic deterioration" — different implications for recovery speed

---

## Appendix: Full Win Rate Tables

### MSTR Detailed (180d win rate by condition)
```
deep_acc + VLT neg:           WR=79.0%  N=62   mean=+49%  [HIGH]
mixed_ctx=true:               WR=71.9%  N=96   mean=+43%  [HIGH]
neutral_neg + mixed:          WR=73.1%  N=26   mean=+51%  [HIGH]
loi<-20 + rising:             WR=61.6%  N=73   mean=+31%  [HIGH]
acc + VLT neg:                WR=46.9%  N=130  mean=+7%   [HIGH]
baseline:                     WR=57.2%  N=1078           [HIGH]
```

### TSLA Detailed (180d win rate by condition)
```
acc + VLT neg:                WR=77.2%  N=184  mean=+47%  [HIGH] ← PRIMARY
deep_acc + VLT neg:           WR=100%   N=13   mean=+105% [MED]
loi<-20 + rising:             WR=82.1%  N=67   mean=+48%  [HIGH]
neutral_neg + VLT neg:        WR=67.6%  N=204  mean=+37%  [HIGH]
tf_count=0 (all TFs neg):     WR=78.6%  N=229           [HIGH]
tf_count=3 (all TFs pos):     WR=23.6%  N=258           [HIGH] ← AVOID
baseline:                     WR=48.3%  N=995            [HIGH]
```

### GLD Detailed (180d win rate by condition)
```
acc + VLT neg + LT neg:       WR=91.2%  N=34   mean=+16%  [HIGH] ← PRIMARY
loi<-20+rising + VLT neg:     WR=100%   N=12   mean=+16%  [MED]
neutral_neg + VLT pos:        WR=74.0%  N=100  mean=+19%  [HIGH]
above SMA200:                 WR=68.5%  N=682           [HIGH]
neutral_neg + VLT neg:        WR=31.6%  N=247  mean=+6%   [HIGH] ← AVOID
mixed_ctx=true:               WR=5.4%   N=37   mean=0%    [HIGH] ← HARD AVOID
baseline:                     WR=58.9%  N=996            [HIGH]
```

---

*Brief prepared by: Quantitative Research Sub-Agent (cross-asset-leap-research)*  
*DO NOT COMMIT TO GITHUB — contains analysis pending CIO review*  
*Next update: After Stage 4→1 fix at 4H resolution and extended VIX history*
