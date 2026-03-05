# System Learnings — Cross-Agent Institutional Memory

Curated by the CIO. Read by all agents at session start.
Only ACTIVE entries should be loaded. SUPERSEDED entries are retained for historical reference but skipped during loading.

When reading this file, load the most recent ACTIVE entries first. If context window is tight, prioritize entries tagged for your domain.

---

## 2026-03-03 — Liquidity Regime Determines Optimal Signal Timeframe
- **Source agent:** CIO (backtest analysis)
- **Affects:** All agents; especially Options Strategist (IV timing), SRI Agent (signal weighting), Macro Analyst (regime inputs)
- **Insight:** In EXPANDING liquidity regimes (HYG SRIBI > 0, VIX LOI < 0), shorter timeframes (VST/ST) carry more signal — momentum sustains longer due to central bank flows. In CONTRACTING regimes (HYG SRIBI < 0, VIX LOI > 0), LT/VLT are more reliable and should be required for confirmation. ST is the all-weather timeframe, least sensitive to regime. Current regime: CONTRACTING → require LT/VLT confirmation before AB3 deployment.
- **Evidence:** 15-month backtest on MSTR. VST bear accuracy in EXPANDING = 82% (n=11). LT bull accuracy in CONTRACTING = 75% (n=4). Data window too short for statistical certainty — directional confidence only.
- **Recommended action:** Macro Analyst should tag every report with liquidity regime and active TF weight. Options Strategist should defer to LT-confirmed signals in CONTRACTING regime when sizing PMCC calls. SRI Agent: weight LT/VLT higher in CONTRACTING; VST/ST higher in EXPANDING.
- **Status:** ACTIVE (UNVALIDATED — 15-month window; re-validate at 24+ months)

## 2026-03-03 — Vol-Adaptive LOI Thresholds Outperform Fixed Thresholds
- **Source agent:** CIO (backtest analysis)
- **Affects:** CIO (AB3 deployment), Options Strategist (LEAP entry timing), SRI Agent (accumulation signal)
- **Insight:** Fixed LOI thresholds (-45 MOMENTUM, -40 MR) misfire severely in low-vol regimes. HIGH volatility entries on MSTR produce +26.3% 60-bar median return; LOW volatility entries produce -26.8%. The adaptive formula `threshold = base × (median_ATR_ratio / current_ATR_ratio)` normalizes for vol regime and dramatically improves signal quality. Key mechanism: low-vol environments produce shallow LOI dips that quickly reverse. High-vol drawdowns are the genuine accumulation opportunities. Note: direction of vol-LOI relationship is INVERTED from initial hypothesis — high vol produces MORE negative LOI troughs (not less), but the adaptive formula is still valid.
- **Evidence:** MSTR fixed threshold = 3 signals / 0% accuracy. Adaptive = 1 signal / 100% accuracy / +12.2% return. Pearson r (ATR/Close vs LOI depth): MSTR -0.383 (p=0.012*), TSLA -0.801 (p<0.001***), SPY -0.967 (p<0.001***).
- **Recommended action:** Use adaptive thresholds in sri_engine.py (implemented). Pine scripts: add dynamic threshold visualization line. Options Strategist: prefer LEAP entries when vol is elevated (CRS index should weight current vol regime as a positive factor for entry).
- **Status:** ACTIVE (UNVALIDATED — 15-month window; statistical significance needs confirmation at 24+ months)

*No additional system learnings recorded yet. The CIO will continue populating this file as cross-agent patterns emerge from trade post-mortems and signal accuracy tracking.*

## 2026-03-05 — TSLA TF Concordance Inverted: Buy Maximum Fear, Not Confirmation
- **Source agent:** CIO (cross-asset LEAP backtest)
- **Affects:** mstr-sri (stage calls), mstr-options (AB2 gate), CIO (allocation)
- **Insight:** TSLA 180d forward win rates INVERT with timeframe concordance: 0 TFs positive = 78% WR (N=229); 3 TFs positive = 23.6% WR (N=258). This is HIGH confidence and statistically definitive. Entering TSLA LEAPs when everything looks worst outperforms entering when everything looks bullish. CT4 on TSLA (all TFs positive) is a DISTRIBUTION warning, not a confidence booster. The validated primary entry is: LOI acc (-40 to -20) + VLT negative = 77.2% WR, N=184.
- **Evidence:** cross-asset-leap-research-v1.md, TSLA section; N>200 in both buckets
- **Recommended action:** mstr-sri should flag CT4 on TSLA as entry-quality degrading. mstr-options should apply tighter AB2 exit gates when TSLA is at CT3/CT4. CIO should weight TSLA entries on LOI depth + VLT negative, not TF concordance.
- **Status:** ACTIVE

## 2026-03-05 — Mixed Context is a Counter-Signal for GLD and QQQ
- **Source agent:** CIO (cross-asset LEAP backtest)
- **Affects:** mstr-sri (stage calls), CIO (allocation), mstr-options (asset selection)
- **Insight:** Mixed context (VLT negative, LT positive) produces dramatically DIFFERENT outcomes by asset class. For MSTR: +14.7pp over baseline (72% WR). For GLD: 5.4% WR (N=37, HIGH confidence) — nearly guaranteed loss. For QQQ: 13.9% WR (N=36, HIGH confidence). Both GLD and QQQ require VLT POSITIVE for LEAP entries. GLD's validated entry is: LOI acc + VLT neg + LT neg = 91% WR (N=34) — specifically during maximum fear in a trending bull. QQQ's best entry is: 3 TFs positive + LOI accumulation zone (~73% WR). Applying mixed_ctx universally is a significant error for GLD/QQQ.
- **Evidence:** cross-asset-leap-research-v1.md, GLD and QQQ sections
- **Recommended action:** mstr-sri must apply asset-specific mixed_ctx interpretation. Mixed_ctx is BULLISH for MSTR/IWM, BEARISH for GLD/QQQ. CIO should never use mixed_ctx as an entry rationale for GLD or QQQ positions.
- **Status:** ACTIVE

## 2026-03-05 — GLD SMA200 is a Meaningful Structural Filter (+30pp)
- **Source agent:** CIO (cross-asset LEAP backtest)
- **Affects:** mstr-sri (stage calls for GLD), CIO (GLD allocation gate), mstr-technical (GLD trend analysis)
- **Insight:** GLD price above 200-day SMA: 68.5% 180d WR (N=682). GLD price below 200-day SMA: 38.2% WR (N=314). Delta = +30.3 percentage points. For a trending asset, structural trend confirmation is required before LEAP entry. Best GLD entry: LOI acc + VLT neg + LT neg + above SMA200 = estimated >85% WR (MED confidence due to small N when all conditions combined). GLD LEAP entries should be gated on SMA200 confirmation as a hard filter.
- **Evidence:** cross-asset-leap-research-v1.md, GLD section; SMA200 analysis N=996 total
- **Recommended action:** mstr-technical should include GLD SMA200 status in every GLD analysis. CIO should add SMA200 as a hard gate for GLD AB3 entries — do not deploy GLD LEAPs when price is below the 200-day. mstr-sri should incorporate SMA200 into GLD stage designation.
- **Status:** ACTIVE

## 2026-03-05 — Multi-Asset Simultaneous Accumulation Windows = Maximum AB4 Deployment Signal
- **Source agent:** CIO (cross-asset LEAP backtest)
- **Affects:** CIO (capital allocation), all analysts (heightened priority periods)
- **Insight:** When 3+ in-scope assets simultaneously show LOI < -20, this historically occurs ~8% of trading days (~108 days in the 2021-2026 period). These correspond to broad market selloffs (2022 rate shock, 2025 corrections). MSTR 180d WR during these windows = 64%; QQQ = 62%. These are maximum portfolio deployment windows — AB4 should be at minimum (near 10% floor) and all available capital should be deployed across the highest-conviction signals. Single-asset accumulation is good; multi-asset accumulation is rare and exceptional.
- **Evidence:** cross-asset-leap-research-v1.md, Cross-Asset Opportunity Windows section
- **Recommended action:** CIO should monitor count of assets in LOI < -20 daily. When count ≥ 3, escalate AB4 deployment priority. When count ≥ 4, this is a maximum deployment event. Wire into morning brief as "Cross-Asset Accumulation Count" metric.
- **Status:** ACTIVE

<!-- FORMAT FOR NEW ENTRIES:

## YYYY-MM-DD — [Cross-agent insight title]
- **Source agent:** mstr-[agent]
- **Affects:** mstr-[agent], mstr-[agent]
- **Insight:** [The specific finding]
- **Evidence:** [Trade IDs, dates, data points]
- **Recommended action:** [How affected agents should adjust]
- **Status:** ACTIVE / SUPERSEDED / UNVALIDATED

-->
