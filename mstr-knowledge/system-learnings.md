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

<!-- FORMAT FOR NEW ENTRIES:

## YYYY-MM-DD — [Cross-agent insight title]
- **Source agent:** mstr-[agent]
- **Affects:** mstr-[agent], mstr-[agent]
- **Insight:** [The specific finding]
- **Evidence:** [Trade IDs, dates, data points]
- **Recommended action:** [How affected agents should adjust]
- **Status:** ACTIVE / SUPERSEDED / UNVALIDATED

-->
