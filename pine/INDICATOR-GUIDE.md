# SRI Pine Indicator Guide

**Repo:** 3ServantsP35/Grok  
**Last updated:** 2026-03-04  
**Pine version:** v6  

---

## Quick Reference

| Indicator | File | Type | Purpose | Framework Use |
|---|---|---|---|---|
| SRI VST | [SRI_VST.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRI_VST.pine) | Price overlay | Precision entry/exit | Exhaustion timing |
| SRI ST | [SRI_ST.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRI_ST.pine) | Price overlay | Primary execution | All trade entries |
| SRI LT | [SRI_LT.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRI_LT.pine) | Price overlay | Trend & stage | Stage designation |
| SRI VLT | [SRI_VLT.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRI_VLT.pine) | Price overlay | Final confirmation | Stage confirmation |
| SRIBI VST | [SRIBI_VST.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRIBI_VST.pine) | Oscillator | Leading momentum | VST LOI input |
| SRIBI ST | [SRIBI_ST.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRIBI_ST.pine) | Oscillator | Decision signal | ST LOI input |
| SRIBI LT | [SRIBI_LT.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRIBI_LT.pine) | Oscillator | Context/headwind | LT LOI input |
| SRIBI VLT | [SRIBI_VLT.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRIBI_VLT.pine) | Oscillator | Structural confirm | VLT LOI input |
| SRI Forecast AB1 | [SRI_Forecast_AB1.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRI_Forecast_AB1.pine) | Price overlay | Pre-breakout entry | AB1 LEAP entries |
| SRI Forecast AB2 | [SRI_Forecast_AB2.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRI_Forecast_AB2.pine) | Price overlay | PMCC conditions | AB2 spread setup |
| SRI Forecast AB3 | [SRI_Forecast_AB3.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/SRI_Forecast_AB3.pine) | Oscillator | LEAP accumulation | AB3 core signal |
| AB2 CRS v2 | [AB2_CRS.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/AB2_CRS.pine) | Oscillator | Call-selling ripeness | AB2 income sizing |
| STRF/LQD Ratio | [STRF_LQD_Ratio.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/STRF_LQD_Ratio.pine) | Oscillator | Saylor credit quality ratio | Layer 1 Regime input |
| Force Field | [MSTR_Suite_Force_Field.pine](https://github.com/3ServantsP35/Grok/blob/main/pine/MSTR_Suite_Force_Field.pine) | Oscillator | 5-factor composite force | Layer 0.75 entry gate |

All files: https://github.com/3ServantsP35/Grok/tree/main/pine

---

## How to Add an Indicator to TradingView

1. Go to the file link in the table above
2. Click the **Raw** button — copy all text
3. In TradingView: **Pine Script Editor** → **New indicator** → Paste → **Add to chart**

> **Tip:** SRI and SRI Forecast indicators go on the **price chart** (overlay). SRIBI, SRI Forecast AB3, and AB2 CRS go in a **separate pane** (not overlay).

---

## Indicator Family Overview

There are four families of indicators in this suite:

1. **SRI Price Overlays** (SRI VST/ST/LT/VLT) — Reversal Bands and Tracklines on the price chart. Visualize support/resistance and stage transitions.
2. **SRIBI Oscillators** (SRIBI VST/ST/LT/VLT) — Bias Histograms in a separate pane. Measure momentum numerically and feed the LOI composite.
3. **SRI Forecast Strategy Indicators** (AB1/AB2/AB3) — Strategy-specific decision tools, each covering one of the three trade buckets.
4. **AB2 CRS** — Standalone call-selling scoring tool for the AB2 income overlay.
5. **Regime & Force Indicators** (STRF/LQD Ratio, Force Field) — External force model for structural regime context. Layer 0.75 — above GLI, below Regime Engine. These do not drive individual trade entries directly; they set the backdrop that governs sizing confidence and gate state.

---

## Understanding the Core Concepts

### Reversal Band
A **statistical envelope** around price, computed on a fixed higher timeframe. Three lines:
- **Red line** — Support (regression midpoint minus one standard deviation)
- **Blue line** — Robust Fit (linear regression midpoint)
- **Green line** — Resistance (regression midpoint plus one standard deviation)

In a bullish RSI environment (RSI ≥ 50), all three lines display. In bearish (RSI < 50), the Resistance line collapses to the Robust Fit — signaling the model is no longer projecting upside.

### Tracklines
ATR-based dynamic support/resistance lines. Two per indicator (Fast and Slow), each on a different timeframe:
- **Green** = rising (bullish trend in that timeframe)
- **Red** = falling (bearish trend)
- **Orange** = flat (transitioning)

The relative position of Fast vs Slow Trackline defines the **stage**:
- Price above Fast Trackline → bullish bias
- Price below Slow Trackline → bearish bias
- Between the two → transitional / staging

### Stage Transitions
Each SRI overlay plots four labeled signals when conditions for a stage transition are met:
- **4→1** (below bar, green label): Bottoming signal
- **1→2** (below bar, lime label): Bull confirmation  
- **2→3** (above bar, orange label): Topping warning
- **3→4** (above bar, red label): Bear confirmation

These require multiple conditions simultaneously (Trackline crossover, Stochastic, RSI from a higher timeframe). They are high-conviction signals, not noise.

### LOI (Leap Opportunity Index)
A composite score from -100 to +100 that summarizes the structural opportunity across all four timeframes. Computed inside AB3 and AB1 from four components:
- VLT SRIBI score (40% weight)
- VLT acceleration / rate-of-change (30%)
- LT SRIBI score (15%)
- 4-TF Concordance count (15%)

**Negative LOI = opportunity** (accumulate). **Positive LOI = extended** (trim or wait).

---

## Family 1 — SRI Price Overlays

---

### SRI VST (Very Short Term)

**File:** `pine/SRI_VST.pine`  
**Type:** Price overlay  
**Timeframes used:** Reversal Band: 2H | Fast Trackline: 2H | Slow Trackline: 1D  
**Framework role:** Precision timing tool — catches intraday exhaustion signals and fine-tunes entry/exit timing after ST has confirmed direction.

#### What It Shows

Three thin lines on the price chart form the 2-hour Reversal Band (red support, blue midpoint, green resistance). A circle-style plot traces the 2-hour Fast Trackline (color changes green/red/orange with direction), and a solid line traces the 1-day Slow Trackline. Labeled stage transition signals (4→1, 1→2, 2→3, 3→4) appear at the bar where conditions align.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for the linear regression (Reversal Band). Longer = smoother but slower. |
| Deviation Multiplier | 1.0 | Width of the band (±1 standard deviation at default). Increase to widen the envelope. |
| RSI Length for Bear Condition | 14 | RSI period used to determine whether to collapse the Resistance line to midpoint. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for Fast Trackline width. Larger = wider (further from price). |
| Fast Trackline Period | 14 | ATR smoothing period for Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for Slow Trackline. |
| Slow Trackline Period | 14 | ATR smoothing period for Slow Trackline. |

#### How to Use It

1. **Add to a 15-minute or 1-hour chart.** The VST indicator pulls its own fixed timeframes (2H and 1D) regardless of the chart timeframe you're viewing.
2. **Watch the Fast Trackline color.** Green = 2H uptrend in progress. Red = 2H downtrend. Orange = pausing.
3. **Use the Reversal Band as a bounce/rejection zone.** Entries near the red support line (with price bouncing) are high-probability in a bullish context. Rejections at the green resistance line are exit signals.
4. **Watch for 4→1 labels** as a short-term bottoming signal. Use only when ST also shows a constructive setup — VST signals alone are noisy.
5. **Pair with SRIBI VST** to confirm the bias score is turning positive before acting on a 4→1 signal.

#### Key Signals

- **VST 4→1 label**: Precision bottom signal. Requires Fast/Slow Trackline crossover, Stochastic crossover, RSI < 30 on 1D. High-conviction when it fires.
- **Fast Trackline turns green** (after being red): VST momentum has flipped positive — fine-tune long entry.
- **Price bouncing off red Reversal Support**: Potential reload zone in an ongoing bull trend.
- **VST 2→3 label**: Precision exit warning. Check ST/LT before exiting a core position.

#### Framework Connection

VST is the "microscope" for timing. It does not drive position decisions — ST does. Use VST to tighten your entry after ST confirms the trade. In AB2 CRS, the VST bias score is the **Exercise Risk input** — if VST momentum is strongly positive (VST histogram > 5 and rising), exercise risk on short calls is elevated.

#### Common Mistakes

- **Acting on VST signals without ST confirmation.** VST fires 3–4× more often than ST. Most VST 4→1 signals are noise unless ST is also setting up.
- **Using VST for position sizing decisions.** It's a timing tool only — accumulation thresholds are set by AB3 (LOI).
- **Ignoring the RSI collapse on Resistance.** When RSI < 50, the green resistance line snaps to the blue midpoint — this is a warning that the regime has shifted bearish and resistance targets should not be used.

---

### SRI ST (Short Term)

**File:** `pine/SRI_ST.pine`  
**Type:** Price overlay  
**Timeframes used:** Reversal Band: 4H | Fast Trackline: 2H | Slow Trackline: 1D  
**Framework role:** Primary execution tool — the one chart every active trade entry references first.

#### What It Shows

Three medium-weight lines form the 4-hour Reversal Band. Circle-style Fast Trackline (2H) and solid Slow Trackline (1D), drawn at linewidth=2 (slightly thicker than VST). Stage transition labels (4→1, 1→2, 2→3, 3→4) with same logic as VST but on 4H/2H/1D resolution.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for the 4H linear regression midpoint. |
| Deviation Multiplier | 1.0 | Band width multiplier (±1 std dev at 1.0). |
| RSI Length for Bear Condition | 14 | RSI period for collapsing Resistance in bearish regime. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for 2H Fast Trackline. |
| Fast Trackline Period | 14 | ATR period for 2H Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for 1D Slow Trackline. |
| Slow Trackline Period | 14 | ATR period for 1D Slow Trackline. |

#### How to Use It

1. **This is your go-to indicator for every entry decision.** Check ST before executing any AB1 or AB3 trade.
2. **Look for 1D Slow Trackline direction first** — if it's red (falling), you're in a bear structure at the ST level. Avoid new entries until it stabilizes.
3. **Use the 4H Reversal Band for target levels.** In a bullish setup, the green resistance line is your first upside target; the red support line is your stop reference.
4. **ST 4→1 signal** is a primary AB3 bounce confirmation signal. This is one of the key inputs that separates a real bottom from a head-fake.
5. **After an ST 1→2 signal**, the structure has confirmed bullish — the Slow (1D) Trackline should be rising or at minimum flat-to-up.

#### Key Signals

- **ST 4→1 label**: Stage 4-to-1 transition. Primary AB3 bounce signal. Requires LT context to be constructive.
- **ST 1→2 label**: Bull trend confirmation. Full LEAP sizing appropriate once AB3 LOI also crosses accumulation threshold.
- **1D Slow Trackline color change from red to green**: The most important structural shift at the ST level.
- **Price crossing 4H Reversal Resistance**: Breakout confirmation; target: next price structure above band.
- **ST 2→3 label**: Trim warning. Begin executing AB3 trim schedule.

#### Framework Connection

ST is the "all-weather" monitoring signal — the most stable across liquidity regimes. In contracting liquidity (HYG below 50-SMA, VIX > 25), ST confirmation is required before deploying AB2 or AB3 capital even if VST is constructive. SRIBI ST feeds the ST LOI input and is the primary decision signal for whether to trade at all.

#### Common Mistakes

- **Entering before 1D Slow Trackline stabilizes.** Fast Trackline (2H) can turn green while Slow (1D) is still falling — this is a short-covering bounce, not a trend reversal.
- **Treating the 4H Reversal Band as absolute support.** In high-volatility regimes (MSTR, BTC), price can wick through the band and recover. The band is a probability zone, not a hard stop.
- **Ignoring ST when VST is screaming.** VST signals feel urgent. Always check ST first.

---

### SRI LT (Long Term)

**File:** `pine/SRI_LT.pine`  
**Type:** Price overlay  
**Timeframes used:** Reversal Band: 1D | Fast Trackline: 4H | Slow Trackline: 1W  
**Framework role:** Stage designation and primary trend context — tells you whether you're in a structural bull or bear and where you are in the cycle.

#### What It Shows

Three thick lines (linewidth=3) form the 1-day Reversal Band. Circle-style 4-hour Fast Trackline and solid 1-week Slow Trackline, both at linewidth=3. Stage transition labels appear at weekly-resolution turning points. This indicator moves slowly and deliberately — that's the point.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for 1D linear regression. |
| Deviation Multiplier | 1.0 | Band width (±1 std dev at 1.0). |
| RSI Length for Bear Condition | 14 | RSI period for bear regime collapse of Resistance line. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for 4H Fast Trackline. |
| Fast Trackline Period | 14 | ATR period for 4H Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for 1W Slow Trackline. |
| Slow Trackline Period | 14 | ATR period for 1W Slow Trackline. |

#### How to Use It

1. **Check LT first for any new position thesis.** If the 1W Slow Trackline is red (falling), you are in a structural bear. New LEAP entries require higher conviction from all other signals.
2. **LT 4→1 signal** is early stage designation — price is attempting to bottom at the structural level. This precedes ST by days to weeks.
3. **"LT positive"** means the 4H Fast Trackline has crossed above the 1W Slow Trackline — a bullish structural confirmation used as the AB2 exit trigger.
4. **Watch the 1D Reversal Band in trending markets.** In a Stage 2 bull, price tends to hold above the 1D Robust Fit (blue). Dips to the 1D support (red) are reload zones.
5. **Use alongside SRIBI LT** to verify that the structural momentum (LT SRIBI > 0) agrees with the visual picture.

#### Key Signals

- **LT 4→1**: Early structural bottom signal. High-value when preceded by multiple weeks of Stage 4 compression.
- **1W Slow Trackline color change from red to green**: The primary structural bull confirmation. This is what "LT positive" means in the AB2 indicator.
- **1D Robust Fit (blue) acting as support**: Stage 2 in progress. Reload opportunities.
- **LT 2→3**: Major topping warning. Begin AB3 trim schedule; reconsider AB2 call-selling strategy.

#### Framework Connection

LT is the designated stage instrument. In AB1 (Forecast), LT direction defines the MIXED context: when LT is negative and VLT is positive, you're in MIXED — the AB2 bull put window. When LT turns positive, that window closes. LT also provides the structural Tracklines plotted by the AB1 and AB2 forecast indicators for visual reference.

#### Common Mistakes

- **Over-trading based on LT signals.** LT moves slowly. A single LT 4→1 signal might represent a multi-month opportunity window — don't size in all at once; wait for ST confirmation.
- **Confusing "LT positive" with "fully bullish."** LT positive simply means the 4H Fast Trackline has crossed the 1W Slow Trackline. VLT may still be negative (that's actually the ideal MIXED setup for AB2).
- **Using LT as a short-term entry timer.** It's not. VST and ST are for timing; LT is for context.

---

### SRI VLT (Very Long Term)

**File:** `pine/SRI_VLT.pine`  
**Type:** Price overlay  
**Timeframes used:** Reversal Band: 2D | Fast Trackline: 8H | Slow Trackline: 2W  
**Framework role:** Lagging final confirmation — the last signal to turn, meaning when it finally confirms, the move is well-established.

#### What It Shows

Four very thick lines (linewidth=4) form the 2-day Reversal Band (the heaviest visual weight in the suite). The 8-hour Fast Trackline (circles) and 2-week Slow Trackline (solid) anchor the structural level. Because this uses 2-week data, signals fire infrequently and carry significant weight.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for 2D linear regression. |
| Deviation Multiplier | 1.0 | Band width (±1 std dev). |
| RSI Length for Bear Condition | 14 | RSI period for bear regime detection. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for 8H Fast Trackline. |
| Fast Trackline Period | 14 | ATR period for 8H Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for 2W Slow Trackline. |
| Slow Trackline Period | 14 | ATR period for 2W Slow Trackline. |

#### How to Use It

1. **Don't wait for VLT to enter.** VLT confirming is Stage 3 of the confirmation ladder. By the time VLT turns positive, much of the move has already happened.
2. **Use VLT to manage position sizing.** VLT positive = near full allocation is justified. VLT negative but LT positive = MIXED context, be selective.
3. **VLT "positive" (vlt_sribi > 0)** is one of the conditions that closes the AB2 MIXED window — when VLT also turns positive, the structural catch-up is complete.
4. **VLT 4→1 signal** is a very high-conviction long-term bottom signal — this will have been preceded by weeks of VST, ST, and LT signals. Consider it structural confirmation.
5. **Watch 2W Slow Trackline direction** as the ultimate structural trend filter.

#### Key Signals

- **VLT > 0 in SRIBI VLT**: Structural tailwind confirmed. Full allocation appropriate.
- **VLT 4→1 label**: The most lagging but highest-conviction bottom signal in the suite.
- **2W Slow Trackline turning green**: Multi-month bull structure confirmed.
- **CT4 in AB3**: When all four timeframes are positive AND VLT > 20 in the SRIBI framework, distribution warning triggers.

#### Framework Connection

VLT drives 40% of the LOI calculation (the largest single weight). VLT SRIBI being negative is the primary driver that pushes LOI into accumulation territory. VLT turning positive is what closes the AB2 spread window and pushes LOI toward neutral/trim territory. In CT classification, "VLT > 0" is a required condition for CT3/CT4.

#### Common Mistakes

- **Using VLT as a trigger to enter.** By definition it's late. Enter on ST/LT signals with VLT as a context sanity check.
- **Treating VLT negative as a reason to avoid all trades.** VLT negative + LT positive = MIXED context = the ideal AB2 window and a viable AB1 CT1 setup.
- **Expecting frequent signals.** With 2-week resolution, VLT transitions can be weeks apart. Plan accordingly.

---

## Family 2 — SRIBI Oscillators

> All four SRIBI indicators share identical logic — they differ only in their fixed timeframes. Add each to a **separate pane** below the price chart.

---

### Understanding the SRIBI Histogram

The **SRI Bias Score** is a composite momentum score ranging roughly from -100 to +100. It combines:

| Component | Max Points | What it measures |
|---|---|---|
| Trackline direction score | ±30 | Are Fast and Slow Tracklines rising or falling? |
| Slope score | ±35 | How steeply are the Tracklines moving? |
| Cross score | ±30 | Did Fast cross above/below Slow? Did price bounce/reject? |
| Band position score | ±15 | Is price above/below the Robust Fit midpoint? Are bands curving? |
| Linger score | ±10 | Is price staying above support or below resistance? |

**Histogram color:**
- **Red bars above zero** = bullish bias (positive score)
- **Green bars below zero** = bearish bias / depressed (negative score)
- Brighter = stronger (>50 or <-50 = strong signal)
- **Aqua ROC line** = positive rate-of-change (momentum improving)
- **Orange ROC line** = negative rate-of-change (momentum fading)

**Key interpretation:** The ROC line turning aqua while the histogram is still green (negative) is one of the most valuable early signals — momentum drag is diffusing before the histogram crosses zero.

---

### SRIBI VST (Very Short Term)

**File:** `pine/SRIBI_VST.pine`  
**Type:** Oscillator (separate pane)  
**Timeframes used:** Reversal Band: 8H | Fast Trackline: 2H | Slow Trackline: 1D  
**Framework role:** Leading momentum indicator — the earliest signal in the LOI ladder and the primary input for the AB2 CRS Exercise Risk calculation.

#### What It Shows

A histogram of the VST Bias Score (positive = red bars, negative = green bars) with dotted reference lines at +50 (strong bull) and -50 (strong bear). An aqua/orange ROC line shows whether momentum is accelerating or decelerating. The zero line is neutral.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for 8H Reversal Band regression. |
| Deviation Multiplier | 1.0 | Band width for the 8H envelope. |
| RSI Length for Bear Condition | 14 | RSI period for bear regime detection. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for 2H Fast Trackline. |
| Fast Trackline Period | 14 | ATR period for 2H Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for 1D Slow Trackline. |
| Slow Trackline Period | 14 | ATR period for 1D Slow Trackline. |
| ROC Lookback | 5 | Bars of history for rate-of-change (calibrated: VST=5 ≈ 10 hours). |
| ROC EMA Smoothing | 3 | EMA smoothing on the ROC line. |
| Show ROC Line | true | Toggle the ROC line visibility. |

#### How to Use It

1. **Watch the ROC line first.** A ROC turning aqua while the histogram is still negative is an early warning that bearish momentum is fading.
2. **SRIBI VST crossing above zero** confirms the 2H/8H timeframe has flipped bullish — this is the VST component that contributes to concordance in the LOI.
3. **Strong bull (histogram > 50)**: Momentum is strong; exercise risk on short calls is elevated (use in AB2 CRS to guide strike width).
4. **Exhaustion pattern**: If SRIBI VST is at extreme levels (>50 or <-50) and the ROC is diverging (histogram at highs but ROC turning orange), exhaustion may be near.
5. **Align with SRIBI ST** before acting. VST alone is high-frequency noise.

#### Key Signals

- **ROC turns aqua while histogram is negative**: Early mean-reversion signal — bearish drag is losing force.
- **Histogram crosses above zero (0 line)**: VST now contributing positive to the LOI concordance count.
- **Histogram > 50**: Strong bull — Exercise Risk is HIGH in the AB2 CRS (widen call strikes by +5%).
- **Histogram < -50**: Strong bear exhaustion — potential bottoming zone if ST/LT agree.

#### Framework Connection

SRIBI VST feeds the **VST component** of the LOI composite (indirectly via concordance count). More directly, the VST SRI Bias Histogram value is used by **AB2 CRS** as the "VST Source" input to calculate Exercise Risk. High/rising VST bias = HIGH exercise risk → CRS recommends wider OTM strikes.

#### Common Mistakes

- **Trading off VST signals alone.** They fire frequently and are easily invalidated. Always require ST agreement.
- **Ignoring exhaustion at extremes.** A histogram pinned at +80 for several bars with a fading ROC is more bearish than a histogram at +20 with an accelerating ROC.
- **Setting ROC Lookback too long.** The default of 5 bars is calibrated to the 2H fast TF. Changing it will alter the timing relationship.

---

### SRIBI ST (Short Term)

**File:** `pine/SRIBI_ST.pine`  
**Type:** Oscillator (separate pane)  
**Timeframes used:** Reversal Band: 1D | Fast Trackline: 8H | Slow Trackline: 3D  
**Framework role:** The primary decision signal — whether conditions are favorable enough to trade at all.

#### What It Shows

Histogram of the ST Bias Score (1D/8H/3D timeframes). Same visual format as SRIBI VST. ROC default lookback is 6 bars (calibrated to the 8H fast TF ≈ 2 days of history).

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for 1D Reversal Band regression. |
| Deviation Multiplier | 1.0 | Band width. |
| RSI Length for Bear Condition | 14 | RSI period for bear regime detection. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for 8H Fast Trackline. |
| Fast Trackline Period | 14 | ATR period for 8H Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for 3D Slow Trackline. |
| Slow Trackline Period | 14 | ATR period for 3D Slow Trackline. |
| ROC Lookback | 6 | Bars for rate-of-change (calibrated: ST=6 ≈ 48h on 8H TF). |
| ROC EMA Smoothing | 3 | EMA smoothing on ROC line. |
| Show ROC Line | true | Toggle ROC visibility. |

#### How to Use It

1. **SRIBI ST is the "weather report."** Positive = favorable to trade. Negative = headwind, be defensive.
2. **SRIBI ST > 0** is required for the AB2 MIXED window to be "open" (Green background in SRI Forecast AB2). If ST is negative, the window is at most Orange (MIXED but not confirmed).
3. **When SRIBI ST is deeply negative (< -50)**, this is a significant headwind — position sizing should be reduced even if LOI says accumulate.
4. **Watch for the ROC line (ST)** crossing to aqua as an early signal that the 8H/1D momentum is turning.
5. **ST > 0 for multiple bars** confirms the trend, not just a one-bar spike.

#### Key Signals

- **ST histogram crosses above zero**: ST now contributing positive to LOI concordance. AB2 window condition potentially met.
- **ST histogram strongly negative (<-30) and declining ROC**: Headwind regime — defer new entries, focus on defensive management.
- **ROC line diverges from histogram**: Early warning of trend change (hours before the histogram crosses).
- **ST 2→3 label on SRI ST price overlay**: Corresponds to SRIBI ST deteriorating — confirm by watching histogram.

#### Framework Connection

SRIBI ST is the "primary decision signal" for whether to trade. It feeds the **ST concordance input** in the LOI. In AB2 Forecast, ST positive is one of two required conditions (alongside MIXED context) for the Green background (window open). In contracting liquidity regimes, ST must be positive before adding new AB2 call-selling positions.

#### Common Mistakes

- **Entering when ST is negative but VST is strongly positive.** VST recovers first; ST confirms. Wait for ST.
- **Assuming ST positive = full bull.** ST positive just means 8H/1D is constructive. VLT may still be negative (MIXED) which is fine — but be aware of the structural context.
- **Ignoring SRIBI ST during position management.** If you're long LEAPs and SRIBI ST turns deeply negative, that's a signal to review your trim schedule, not ignore.

---

### SRIBI LT (Long Term)

**File:** `pine/SRIBI_LT.pine`  
**Type:** Oscillator (separate pane)  
**Timeframes used:** Reversal Band: 3D | Fast Trackline: 1D | Slow Trackline: 1W  
**Framework role:** Structural context — headwind or tailwind for position sizing decisions.

#### What It Shows

Histogram of the LT Bias Score (3D/1D/1W timeframes). ROC default lookback is 7 bars (calibrated to the 1D fast TF ≈ 7 trading days).

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for 3D Reversal Band regression. |
| Deviation Multiplier | 1.0 | Band width. |
| RSI Length for Bear Condition | 14 | RSI period. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for 1D Fast Trackline. |
| Fast Trackline Period | 14 | ATR period for 1D Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for 1W Slow Trackline. |
| Slow Trackline Period | 14 | ATR period for 1W Slow Trackline. |
| ROC Lookback | 7 | Bars for rate-of-change (calibrated: LT=7 ≈ 7 trading days). |
| ROC EMA Smoothing | 3 | EMA smoothing on ROC line. |
| Show ROC Line | true | Toggle ROC visibility. |

#### How to Use It

1. **SRIBI LT > 0** means the 1D/1W structure is bullish — tailwind for long positions.
2. **SRIBI LT < 0** while SRIBI VLT > 0 = MIXED context = the AB2 structural condition. This is the main thing to watch on this oscillator.
3. **LT SRIBI contributes 15% to the LOI score** — meaningful but not the dominant driver (VLT is 40%).
4. **Watch for LT turning positive** as a signal that the MIXED window may be closing — AB2 bull put window will close when LT positive is confirmed.
5. **LT ROC** accelerating upward while histogram is near zero = structural transition likely imminent.

#### Key Signals

- **SRIBI LT crosses below zero**: LT now contributing negatively to LOI — could be the start of a MIXED or HEADWIND setup.
- **SRIBI LT < 0 with SRIBI VLT > 0**: MIXED confirmed — AB2 window potentially open.
- **SRIBI LT crosses above zero**: AB2 MIXED window closing; LT catch-up complete.
- **LT histogram near zero, ROC aqua**: LT turning positive imminent — watch for window close.

#### Framework Connection

LT SRIBI directly feeds the **LT weight (15%)** in the LOI composite. LT direction (positive vs negative) is also the defining characteristic of the MIXED context used by AB2 Forecast. The LT Tracklines are what the AB1 and AB2 Forecast indicators display on the price chart for structural reference.

#### Common Mistakes

- **Confusing SRIBI LT with the LT Trackline direction.** These are related but not identical. SRIBI LT is the relative score (fast vs slow); the Trackline direction in SRI LT is the directional trend itself.
- **Expecting LT to confirm quickly.** LT reflects weekly structure. Transitions can take 1–3 weeks to confirm.
- **Ignoring SRIBI LT when adding to positions.** A positive SRIBI ST with a deeply negative SRIBI LT means you have a short-term recovery in a structural downtrend. Size accordingly.

---

### SRIBI VLT (Very Long Term)

**File:** `pine/SRIBI_VLT.pine`  
**Type:** Oscillator (separate pane)  
**Timeframes used:** Reversal Band: 1D | Fast Trackline: 2D | Slow Trackline: 2W  
**Framework role:** Final structural confirmation — the highest-weight driver of the LOI composite.

#### What It Shows

Histogram of the VLT Bias Score (1D/2D/2W timeframes). ROC default lookback is 8 bars (calibrated to the 2D fast TF ≈ 16 trading days). This histogram moves the slowest of all four SRIBI indicators.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Regression Length | 50 | Lookback for 1D Reversal Band regression. |
| Deviation Multiplier | 1.0 | Band width. |
| RSI Length for Bear Condition | 14 | RSI period. |
| Fast Trackline Coeff | 1.0 | ATR multiplier for 2D Fast Trackline. |
| Fast Trackline Period | 14 | ATR period for 2D Fast Trackline. |
| Slow Trackline Coeff | 1.0 | ATR multiplier for 2W Slow Trackline. |
| Slow Trackline Period | 14 | ATR period for 2W Slow Trackline. |
| ROC Lookback | 8 | Bars for rate-of-change (calibrated: VLT=8 ≈ 16 trading days). |
| ROC EMA Smoothing | 3 | EMA smoothing on ROC line. |
| Show ROC Line | true | Toggle ROC visibility. |

#### How to Use It

1. **Watch SRIBI VLT as the LOI anchor.** It contributes 40% of the LOI score — when VLT is deeply negative, LOI will be in accumulation territory regardless of the other inputs.
2. **VLT histogram deeply negative (<-50)**: Maximum accumulation zone for AB3. This is when the best LEAP entries happen.
3. **VLT ROC turning aqua while histogram is still green (negative)**: The most powerful early signal in the entire suite — structural momentum is turning before any other indicator has confirmed.
4. **VLT histogram crossing above zero**: LOI will shift meaningfully upward. Begin preparing the trim schedule.
5. **VLT > +20 with all other TFs positive**: CT4 territory — distribution warning for momentum assets (MSTR, TSLA).

#### Key Signals

- **VLT histogram crosses below -50**: Deep accumulation zone. LOI likely below AB3 threshold.
- **VLT ROC turns aqua (histogram still negative)**: Earliest structural recovery signal in the suite.
- **VLT histogram crosses above zero**: LOI shifting from accumulation to neutral/hold.
- **VLT > +20**: CT4 condition — distribution warning if momentum asset.

#### Framework Connection

SRIBI VLT is the **primary driver of the LOI** (40% weight). It also drives the VLT ROC component (30% of LOI when applied to the acceleration calculation). Combined, VLT-related signals account for 70% of the LOI score. This is why VLT is described as "lagging final confirmation" — because its signals are slow, but when it confirms, the LOI signal is very high confidence.

#### Common Mistakes

- **Waiting for SRIBI VLT to cross below the threshold before deploying.** By then, you've often missed the best entry. Use VLT as the confirmation that you're in the zone; AB3 vol-adaptive threshold handles precision timing.
- **Treating VLT > 0 as an all-clear for continued buying.** VLT crossing above zero is when you start the trim schedule, not when you add more.
- **Using a short-term chart to read VLT.** VLT uses 2-week resolution. It may appear to freeze on intraday charts. Verify on a daily or weekly chart view.

---

## Family 3 — SRI Forecast Strategy Indicators

---

### SRI Forecast AB1

**File:** `pine/SRI_Forecast_AB1.pine`  
**Type:** Price overlay  
**Timeframes used:** Internally computes all four TFs (VST=2H/1D, ST=4H/1D, LT=4H/1W, VLT=8H/2W) plus LOI  
**Framework role:** Determines when pre-breakout conditions are favorable for an AB1 LEAP entry (CT-gated, asset-class-aware).

#### What It Shows

Background color indicates current CT tier status — the most important visual. LT Tracklines are plotted on the price chart for structural reference (teal=bullish, maroon=bearish). Small markers at the bottom of the chart show CT tier crossings. An info table (bottom-right) shows the asset class, CT tier, concordance details, LOI, and current condition assessment.

**CT Tiers:**
| Tier | Condition | Meaning |
|---|---|---|
| CT0 | No alignment | Not yet |
| CT1 | VST+, ST+, LT<0, VLT>0 | MIXED context — sweet spot for BTC-proxy |
| CT2 | VST+, LT+, VLT>-20 | Early structural confirmation |
| CT3 | All four TFs positive | Full alignment (required for TSLA) |
| CT4 | All four TFs+ AND VLT>+20 | Overextended — distribution warning |

**Background colors:**
- **Green** = CT tier is favorable for this asset class
- **Yellow** = Watch closely (building)
- **Orange** = LT caught up (TAILWIND trap for BTC-proxy)
- **Red** = Avoid (CT4 on momentum assets, or CT3 on IWM)

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Asset Class | Auto-Detect | Sets CT optimization per asset. Auto-detects from ticker. |
| Trackline ATR Period | 14 | ATR period for internal trackline calculations. |
| Trackline ATR Coefficient | 1.0 | ATR multiplier for trackline width. |
| Show Info Table | true | Shows/hides the summary table (bottom-right). |
| Show Legend | true | Shows/hides the CT legend. |
| Show CT Tier Background | true | Shows/hides the background color coding. |
| Show LT Tracklines | true | Shows/hides the LT Tracklines on the price chart. |

**Asset class CT rules (baked in):**

| Asset Class | Favorable CT | Watch | Avoid |
|---|---|---|---|
| BTC-Proxy (MSTR/IBIT) | CT1 | CT2 | CT4 |
| TSLA | CT3 | CT2 | CT4 |
| GLD | CT1+ | CT0 | None |
| MR-Large (SPY/QQQ) | CT2+ | CT1 | None |
| IWM | CT1 | CT2 | CT3, CT4 |

#### How to Use It

1. **Set or verify the Asset Class** — Auto-Detect works for most tickers, but manually confirm for ambiguous symbols.
2. **Watch for background to turn Green** — this is the AB1 entry signal for your asset class.
3. **For MSTR/IBIT**: Green = CT1 (MIXED — LT still negative, room to run as LT catches up). Don't wait for CT3 — by then LT has caught up and the AB1 opportunity has passed.
4. **For TSLA**: Wait for Green = CT3. TSLA requires full LT confirmation before an AB1 LEAP is appropriate.
5. **For IWM**: Green = CT1 only. Orange/Red at CT3 means late-cycle small-cap — this is a trim warning, not an entry.
6. **Confirm with AB3 LOI**: An AB1 entry should have LOI above the deep accumulation threshold (ideally near or above the accumulation threshold — the setup is CT-driven, not depth-driven).

#### Key Signals

- **Background turns Green**: Favorable CT tier reached for this asset class. Begin AB1 LEAP entry process.
- **CT1 crossing (yellow circle below bar)**: First step of the confirmation ladder.
- **CT3 crossing (diamond below bar)**: Full alignment. Required for TSLA; means "LT caught up" for BTC-proxy.
- **CT4 X-cross (above bar, red)**: Distribution warning on momentum assets — exit timing, not entry.
- **IWM CT3 X-cross (above bar, orange)**: Late-cycle trim signal for IWM.

#### Framework Connection

AB1 is the tactical LEAP bucket (60–120 DTE, CT1/CT2 pre-breakout entries). The CT tier ladder here is the primary signal — it's what triggers a new AB1 entry. A failed AB1 entry (background turns red before profit) is reclassified as AB3. The indicator also shows LOI inline for reference, so you can confirm structural depth without switching charts.

#### Common Mistakes

- **Using the same CT tier for all assets.** MSTR at CT3 is NOT a great AB1 entry — LT has already caught up. Always check what tier is "favorable" for your specific asset.
- **Ignoring the LOI anchor.** Even in a favorable CT tier, if LOI never touched the accumulation threshold in the past 120 bars, the structural setup may lack depth.
- **Entering on the CT1 crossing alone without confirmation.** The crossing is a "watch" signal. Wait for the background to turn Green (favorable condition met), not just for the ladder to step up.

---

### SRI Forecast AB2

**File:** `pine/SRI_Forecast_AB2.pine`  
**Type:** Price overlay  
**Timeframes used:** Same four TF combinations as AB1 (all computed internally)  
**Framework role:** Identifies the MIXED structural window for AB2 bull put spreads and PMCC credit strategies.

#### What It Shows

Background color signals the credit spread opportunity context. LT Tracklines shown on the price chart. An info table (bottom-right) shows asset class, context (HEADWIND/MIXED/TAILWIND), SRIBI levels, LOI, and whether the window is open or closed.

**Background colors:**
| Color | Meaning |
|---|---|
| **Green** | MIXED + ST+ → window OPEN (best setup for bull put spreads) |
| **Yellow** | ST+ but not MIXED (sub-optimal, note context) |
| **Orange** | MIXED but ST not yet positive (wait for ST to confirm) |
| **Red/dim** | TAILWIND (LT already positive — window closed) or HEADWIND (avoid) |

**MIXED context** = LT SRIBI < 0 AND VLT SRIBI > 0. This means: VLT says structural bull; LT is lagging. The window exists while LT is catching up.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Asset Class | Auto-Detect | Auto-detects ticker; IBIT auto-disabled (see below). |
| Trackline ATR Period | 14 | ATR period for internal tracklines. |
| Trackline ATR Coefficient | 1.0 | ATR multiplier. |
| LOI Floor for Bull Put | -30.0 | LOI must be above this level to consider a bull put. Below = structural decline risk. |
| Show Info Table | true | Toggle summary table. |
| Show Legend | true | Toggle legend. |
| Show Context Background | true | Toggle background color coding. |
| Show Forecast Ribbon | false | Optional ribbon visualization. |
| Show LT Tracklines | true | LT Tracklines on price chart for context. |

> **IBIT note:** IBIT (and GBTC, BITO) is automatically disabled. The MIXED context does not reliably predict LT catch-up for crypto-adjacent ETFs. When IBIT is detected, the indicator shows a warning and does not generate window signals.

> **LOI floor note:** Data analysis (Jul 2025–Feb 2026) found that all 29 MIXED+ST+ windows with LOI below -20 resulted in 15–51% drawdowns. The default floor of -30 filters the worst of these. Do not lower below -20 without strong reason.

#### How to Use It

1. **Wait for Green background** — this is the only setup where all conditions align: MIXED context + ST positive + LOI above floor.
2. **Orange background** (MIXED, ST waiting): The structural setup is in place. Watch for ST to turn positive — entry may be days away.
3. **Yellow background** (ST positive, not MIXED): Structure isn't aligned yet. Note the context but do not enter a bull put spread.
4. **For PMCC (covered call on LEAP)**: This indicator also signals favorable AB2 call-selling conditions. Green background = ST momentum supporting existing LEAP position.
5. **Exit signal**: When LT turns positive (TAILWIND), the MIXED window closes. Begin exiting the bull put or rolling the PMCC call.

#### Key Signals

- **Background turns Green**: MIXED + ST+ — window open. Size into bull put at appropriate strikes.
- **Background turns Red from Green**: Window closed (LT caught up or HEADWIND). Exit or roll.
- **Background turns Orange**: MIXED confirmed, ST catching up — prep for entry.
- **LOI below -30**: Even in a Green background, do not enter if LOI is below the floor — structural decline risk overrides the MIXED setup.

#### Framework Connection

AB2 bull put entries (and PMCC setups) require MIXED context. When the window is Green, delta gates apply: OTM delta ≤ 0.25 in neutral zone, ≤ 0.40 in trim zone. In CONTRACTING liquidity regime, defer AB2 call-selling increases until LT/VLT confirms upward momentum (use the SRI VLT indicator to verify). The AB2 window should also be paused when AB1 is active on the same asset (AB1 supersedes AB2 during breakout setups).

#### Common Mistakes

- **Entering on Orange (MIXED, ST not yet positive).** Wait for the full Green signal. Entering early into a MIXED window without ST confirmation has a materially lower win rate.
- **Ignoring the LOI floor.** Green background + LOI below -30 is a dangerous combination. The structural decline risk overrides the short-term setup.
- **Using AB2 on IBIT.** The indicator will warn you, but the reason is real: crypto-adjacent ETFs have erratic LT catch-up behavior that makes MIXED context unreliable for credit spreads.

---

### SRI Forecast AB3 (v5)

**File:** `pine/SRI_Forecast_AB3.pine`  
**Type:** Oscillator (separate pane)  
**Timeframes used:** Internally computes all four TFs (same as AB1/AB2) and the LOI composite  
**Framework role:** The core AB3 accumulation signal — tells you when to deploy LEAP capital, how much, and when to trim.

#### What It Shows

The LOI line (color-coded by zone), accumulation/trim threshold lines, an optional vol-adaptive threshold line (orange), zone background shading, and an info table. A trim cycle tracker shows current trim phase.

**LOI Zone Colors:**
| Color | Zone | Action |
|---|---|---|
| Bright green line | LOI < Deep Acc threshold | Deep accumulation — maximum entry size |
| Green line | Acc threshold to mild opp | Accumulate — standard sizing |
| Gray line | Neutral zone | Hold — no action required |
| Orange line | Trim Watch to Trim Active | Begin trimming (25% → 50% → 75%) |
| Red line | Distribute zone | Exit / distribute fully |
| Red line + CT4 overlay | CT4 active on momentum asset | Distribution warning overrides neutral |

**Per-asset LOI thresholds (defaults):**

| Asset Class | Accumulate | Deep Acc | Trim 25% | Trim 50% | Trim 75% |
|---|---|---|---|---|---|
| BTC-Proxy (MSTR/IBIT) | -45 | -65 | +40 | +60 | +80 |
| TSLA | -45 | -65 | +40 | +60 | +80 |
| GLD | -45 | -65 | +40 | +60 | +80 |
| MR-Large (SPY/QQQ) | -40 | -60 | +10 | +30 | +50 |
| MR-Small (IWM) | -40 | -60 | +10 | +30 | +50 |

> **Threshold note:** The default BTC-proxy accumulation threshold was adjusted to -45 (not -60 as shown in the v5 header comments). Data analysis from Jul 2025–Feb 2026 showed MSTR LOI hit a minimum of -52.2 at the $106.96 absolute bottom — the original -60 threshold never triggered. The -45 default ensures the signal fires during real accumulation windows.

#### The Vol-Adaptive Threshold — Why It Matters

This is the most important feature of AB3 v5, added 2026-03-03.

**The problem:** A flat LOI threshold of -45 does not account for market volatility. In high-volatility environments, the best LEAP entries occur even when LOI is only moderately depressed. In low-volatility environments, the LOI may never reach -45 even during genuine weakness.

**The formula:**
```
adaptive_threshold = base_threshold × (median_ATR_ratio / current_ATR_ratio)
```

Where `ATR_ratio = ATR(14) / close` (normalizes for price level). `median_ATR_ratio` is a 200-bar SMA of the ratio (approximately 33 trading days on a 4H chart).

**Intuition:**
- **High volatility** (current ATR ratio >> median): The multiplier compresses below 1.0, pushing the threshold closer to zero. It becomes *easier* to trigger.
- **Low volatility** (current ATR ratio << median): The multiplier expands above 1.0, pushing the threshold more negative. It becomes *harder* to trigger.

**Why this matters — the evidence:** MSTR backtest (Jul 2025–Feb 2026) showed:
- HIGH vol entries: **+26% median return** over 60 bars
- LOW vol entries: **-27% median return** over 60 bars

The adaptive threshold acts as a quality filter, favoring entries during high-volatility washouts where the expected return is dramatically better.

**Caps:** The multiplier is capped at 60%–130% of the base threshold to prevent extreme adjustments during crisis or unusually calm periods.

**The orange line** on the chart is the adaptive threshold. When LOI drops below the orange line, the light-orange background highlights the adaptive entry zone. This is the actual trigger to watch — not just the fixed green line.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Asset Class | Auto-Detect | Sets all thresholds. Override if Auto-Detect mis-classifies. |
| Trackline ATR Period | 14 | ATR period for tracklines. |
| Trackline ATR Coefficient | 1.0 | ATR multiplier. |
| Custom Acc Level | 0 | Override accumulation threshold (0 = use default). |
| Custom Deep Acc Level | 0 | Override deep accumulation threshold. |
| Custom Trim 1 Level | 0 | Override first trim threshold. |
| Min LOI Depth to Qualify Bounce | -35.0 | LOI must reach this level before a bounce signal fires. Prevents false signals on shallow dips. |
| VLT SRIBI Weight | 40 | LOI composite weight for VLT score. |
| VLT Acceleration Weight | 30 | LOI composite weight for VLT ROC. |
| LT SRIBI Weight | 15 | LOI composite weight for LT score. |
| Concordance Weight | 15 | LOI composite weight for 4-TF alignment count. |
| LEAP Strike Price | 0 | Optional: Enter your LEAP strike for P&L display in table. |
| Entry Cost Per Contract | 0 | Optional: Entry cost for P&L calculations. |
| Number of Contracts | 0 | Optional: Position size for P&L display. |
| Show Info Table | true | Toggle summary table. |
| Show Legend | true | Toggle legend. |
| Show Zone Background | true | Toggle zone shading. |
| Show Signal Markers | true | Toggle accumulation/trim signal dots. |
| Show CT4 / IWM Warnings | true | Toggle distribution warning overlays. |
| Show Vol-Adaptive Threshold | true | Toggle the orange adaptive threshold line. |
| ATR Period (vol-adaptive) | 14 | ATR period for the adaptive calculation. |
| Median ATR Window | 200 | Long-run window for median ATR ratio (≈33 trading days on 4H). |

#### How to Use It

1. **Add this indicator to your chart.** Set Asset Class to your target ticker or let Auto-Detect handle it.
2. **Watch the LOI line color.** Green = accumulation zone. Gray = hold. Orange/red = trim territory.
3. **Watch the orange adaptive threshold line.** When LOI drops below it, the background highlights in light orange — this is the most refined entry signal.
4. **Wait for bounce confirmation.** The indicator requires LOI to have touched the accumulation depth (min -35 by default) before a bounce signal fires. This prevents you from entering on a shallow dip that hasn't reached real accumulation.
5. **Track the trim status in the table.** Once you enter, the trim cycle tracker shows you where you are: 0% → 25% → 50% → 75% → CLOSED.
6. **For IWM:** CT3 on this asset is shown as an orange warning (trim signal, not accumulate) — respect it.
7. **For MSTR/TSLA:** When CT4 fires, the LOI line turns red regardless of LOI level — distribution warning is in effect.

#### Key Signals

- **LOI crosses below adaptive threshold (orange background)**: Primary AB3 entry signal — vol-adjusted accumulation confirmed.
- **LOI < deep accumulation level (bright green)**: Maximum sizing opportunity.
- **LOI crosses above Trim 25% level**: Execute first trim; table shows "25% trimmed."
- **CT4 active (red LOI line)**: Distribution signal on momentum assets — override neutral/hold zone.
- **Bounce minimum met + LOI rising**: Structural bottom formed — confirm with ST 4→1 signal.

#### Framework Connection

AB3 is the core portfolio engine. The LOI generated here feeds into every other strategic decision: AB2 Forecast uses LOI as a floor filter; AB2 CRS uses the LOI as its primary stage classification input; AB1 uses LOI inline for structural depth reference. The trim schedule is a mechanical process — once trim 1 fires, execute 25% reduction regardless of conviction.

#### Common Mistakes

- **Ignoring the vol-adaptive threshold.** The fixed green line is a reference; the orange adaptive line is the actual entry signal. Entering only when LOI crosses the fixed line misses the vol-adjustment entirely.
- **Entering in deep accumulation (< -65) and not sizing up.** Deep accumulation is where the best expected returns occur. This is the signal to add to position, not to wait for "more confirmation."
- **Not respecting the trim schedule.** The trim levels are mechanical. Overriding them because "the asset feels strong" defeats the risk management purpose. Trim at the levels; re-enter if LOI re-enters accumulation.
- **Treating CT4 as a buy signal for TSLA.** On TSLA specifically, TF concordance is *inverted* — 3 TFs positive = 23.6% WR vs 0 TFs positive = 78.6% WR (N>200, HIGH confidence). CT4 on TSLA signals distribution, not accumulation. The validated TSLA entry is LOI acc (-40 to -20) + VLT negative.
- **Using mixed context as a universal entry signal.** Mixed context (VLT negative, LT positive) is the primary MSTR entry signal (72% WR) but is actively harmful for GLD (5.4% WR) and QQQ (13.9% WR). Always check which asset you're analyzing before applying mixed_ctx logic.
- **Ignoring the SMA200 for GLD.** GLD is a trending asset. Price below the 200-day SMA reduces 180d WR from 68.5% to 38.2% (N=996). Never enter GLD LEAPs below the SMA200.

---

## Family 4 — AB2 Call Ripeness Score

---

### AB2 CRS v2

**File:** `pine/AB2_CRS.pine`  
**Type:** Oscillator (separate pane)  
**Timeframes used:** Uses LOI source and VST source from other indicators on the same chart (not fixed internally)  
**Framework role:** Tells you when and how aggressively to sell short calls in the AB2 PMCC strategy — stage-adaptive, three-output decision tool.

#### What It Shows

Three key outputs displayed in a table (bottom-right) and as plotted lines:

1. **Income Score (0–10)**: Is the premium environment worth selling calls right now?
2. **Strike Width (%)**: How far OTM should the strike be? Auto-adjusts for stage and exercise risk.
3. **Exercise Risk (LOW / MED / HIGH)**: What is the snap-recovery risk based on VST momentum?

Plus a stage label showing the current LOI zone (ACTIVE DECLINE, S1 CHOP, RECOVERY, S2 STD, TRIM APPROACH, DELTA_MGMT).

**Stage Mode Reference:**

| LOI Range | Stage Code | Call-Selling Posture |
|---|---|---|
| Below -45 | ACTIVE DECLINE | **NO CALLS** — stock in directional decline |
| -45 to -20 | S1 CHOP ★ | **Primary income window** — 80% success rate at +10% OTM (backtest) |
| -20 to 0 | RECOVERY | Viable but widen strike; monitor VST closely |
| 0 to +20 | S2 STANDARD | Standard income cycle |
| +20 to +40 | TRIM APPROACH | Tighten strike; trimming of LEAP begins |
| Above +40 | DELTA_MGMT | Near-ATM trim; maximum call aggression |

> **S1 CHOP is the primary income window.** The classic instinct is "don't sell calls at the bottom." The backtest data says the opposite — 80% of calls at +10% OTM during the LOI -45 to -20 range expired worthless. This is because the asset is in a sideways/choppy structure, not a recovery.

#### The Three Outputs in Detail

**Income Score (0–10)** — composite of four components:

| Component | Max Points | Source |
|---|---|---|
| IV / Premium attractiveness | 4 pts | Historical Vol percentile (HV vs 252-bar lookback) |
| Stage income quality | 4 pts | Current LOI zone (S1 CHOP = 4 pts, S2 STD = 3 pts, RECOVERY = 2 pts) |
| Chop confirmation | 2 pts | MACD histogram ≤ 0 (+1) + OBV below 20-SMA (+1) |
| Howell Phase modifier | ±0.5 | TURBULENCE=+0.5, SPECULATION=-0.5, CONFUSION=-0.25 |
| Liquidity regime modifier | ±0.5 | CONTRACTING=+0.5, EXPANDING=-0.25 |

Score ≥ 7: High conviction — sell calls aggressively.  
Score 5–6: Favorable — standard sizing.  
Score 3–4: Marginal — conservative sizing or skip.  
Score < 3: Skip this cycle.

**Strike Width (%)** — how far OTM:

| Stage | Base Strike Width | Rationale |
|---|---|---|
| ACTIVE DECLINE | NO CALLS | — |
| S1 CHOP | +12% OTM | Primary income zone, room to be wrong |
| RECOVERY | +17% OTM | Wide to protect emerging recovery |
| S2 STANDARD | +10% OTM | Standard cycle |
| TRIM APPROACH | +5% OTM | Tighter, trimming in progress |
| DELTA_MGMT | +1% OTM (ATM) | Aggressive trim via assignment |

Plus **Exercise Risk adjustment**:
- Exercise Risk HIGH (VST > 5 AND rising): +5% wider OTM
- Exercise Risk MED (either condition): +3% wider
- Exercise Risk LOW: no adjustment

Example: S1 CHOP + HIGH exercise risk = +12% + 5% = **+17% OTM strike**.

**Exercise Risk (LOW / MED / HIGH)** — driven by VST momentum:
- **HIGH**: VST source value > 5 AND 3-bar slope > 3. Snap-recovery likely. Widen significantly.
- **MED**: One of the two conditions. Modest recovery risk.
- **LOW**: VST neutral or bearish. Call exercise risk is minimal.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| LOI Plot | (required) | Select the LOI plot from your AB3 indicator. |
| VST SRI Bias Histogram | (required) | Select the VST histogram from your AB3 or SRIBI VST indicator. |
| Active Decline Gate | -45.0 | LOI below this = NO CALLS. |
| S1 Chop Zone lower bound | -45.0 | Bottom of the S1 chop zone. |
| S1 Chop Zone upper bound | -20.0 | Top of the S1 chop zone. |
| Recovery Zone upper bound | 0.0 | Top of recovery zone (S2 STD starts here). |
| S2 Standard upper bound | +20.0 | Top of S2 standard zone. |
| Trim Approach upper bound | +40.0 | Above this = DELTA_MGMT. |
| Historical Vol Period | 20 bars | Period for HV calculation. |
| HV Percentile Lookback | 252 bars | Rolling window for HV percentile rank. |
| Howell Phase | TURBULENCE | Manual input from morning brief. |
| Auto-detect Liquidity Regime | true | Uses HYG + VIX to detect CONTRACTING/EXPANDING/NEUTRAL. |
| Asset Class | MOMENTUM | MOMENTUM / MR / TRENDING / BTC_CORRELATED. Used for display context. |
| Show Info Table | true | Toggle summary table. |
| Show Stage Labels | true | Toggle stage label on chart. |

#### How to Use It

1. **Add this indicator to the same chart as your AB3 and/or SRIBI VST indicator.**
2. **Connect the sources**: In indicator settings, set "LOI Plot" to the LOI plot from AB3, and "VST SRI Bias Histogram" to the VST bias histogram.
3. **Update Howell Phase manually** from the morning brief (REBOUND / SPECULATION / TURBULENCE / CONFUSION).
4. **Check Income Score** before selling any call. Score ≥ 7 = full size. Score 3–4 = half size or skip.
5. **Read Strike Width** for the exact OTM target. Add the Exercise Risk adjustment — this is already included in the displayed Strike Width.
6. **Check Exercise Risk** before entering. HIGH exercise risk means VST is surging — widen further or wait one bar.
7. **Never sell calls in ACTIVE DECLINE** (Income Score = 0, Strike Width = "NO CALLS"). LOI below -45 means directional decline, not chop.

#### Key Signals

- **Stage = S1 CHOP + Income Score ≥ 7**: Ideal call-selling setup. Sell at the displayed strike width.
- **Exercise Risk turns HIGH (red in table)**: Snap-recovery risk elevated. Widen the strike or delay entry.
- **Stage transitions to DELTA_MGMT**: Near-ATM call selling is appropriate — this is the trim phase, not income phase.
- **Income Score drops below 3**: Skip this cycle. Premium is not worth the risk.
- **Liquidity turns CONTRACTING**: Score gets a +0.5 boost — sideways macro context supports call-selling.

#### Framework Connection

AB2 CRS is the income layer over AB3 LEAPs. It does not stand alone — it requires:
1. An active AB3 LEAP position (AB2 sells calls *against* existing LEAPs)
2. LOI source from the AB3 indicator (the CRS classifies its own stage from this)
3. VST source (SRIBI VST or VST histogram from AB3) for exercise risk detection

The Howell Phase input connects to the macro regime from the morning brief. When TURBULENCE is reported, call-selling income is more reliable. When SPECULATION, reduce sizing. STRC yield (~0.83%/month) is the hurdle — if the expected call premium is below that, stay in STRC instead.

#### Common Mistakes

- **Selling calls in ACTIVE DECLINE.** The indicator blocks this (Income Score = 0), but the temptation is real. LOI below -45 means structural decline — short calls will expire in the money.
- **Ignoring Exercise Risk.** S1 CHOP is favorable, but if VST is surging (HIGH exercise risk), selling at only +12% OTM will get called away. Add the +5% adjustment.
- **Not connecting the LOI source.** If you leave "LOI Plot" on the default `close`, the stage classification will be wrong. Always connect it to the actual LOI plot from AB3.
- **Treating S2 STANDARD as better than S1 CHOP.** Counterintuitively, S1 CHOP scores higher income quality (4 pts vs 3 pts). This is because the chop thesis has higher directional certainty — the stock is not going anywhere fast.

---

## Putting It All Together

### The Four-Chart Setup

For a complete view, use four panels:

1. **Price chart** — Add SRI ST (primary), SRI LT (context), SRI VST (timing), SRI Forecast AB1 or AB2 or AB3 depending on active bucket
2. **SRIBI pane** — Add SRIBI ST (primary), SRIBI LT (context), SRIBI VLT (structural anchor)
3. **AB3 pane** — SRI Forecast AB3 (LOI line, zone color, adaptive threshold)
4. **CRS pane** — AB2 CRS v2 (income score, strike width, exercise risk)

### Decision Hierarchy

| Question | Answer comes from |
|---|---|
| What is the current structural force regime? | Force Field F_net zone + Gate state |
| Am I in a structural bull? | SRI LT + SRIBI LT |
| Is the trend extended or depressed? | LOI in AB3 (green = depressed, red = extended) |
| Should I open an AB3 LEAP? | LOI < adaptive threshold + ST 4→1 bounce |
| Asset calibration check | See per-asset calibration rules: TSLA (inverted concordance), GLD (SMA200 + VLT req), QQQ (VLT+ required), MSTR/IWM (mixed_ctx valid) |
| Which CT tier is the asset in? | SRI Forecast AB1 background color |
| Is the AB2 window open? | SRI Forecast AB2 background color (Green) |
| Should I sell a call today? | AB2 CRS Income Score + Strike Width + Exercise Risk |
| When do I trim? | AB3 trim level crossings (25% → 50% → 75% → close) |

### Confirmation Ladder

The suite is designed so that signals cascade from slower to faster:

1. **SRIBI VLT** turns negative → LOI enters accumulation territory
2. **SRIBI LT** shows MIXED (negative while VLT positive) → AB2 window opens
3. **SRI LT** shows Stage 4 → 1 transition → early structural bottom
4. **SRIBI ST** turns negative then starts recovering → ST momentum clearing
5. **SRI ST** shows 4→1 signal → primary bounce confirmation
6. **AB3 LOI** crosses adaptive threshold → AB3 entry confirmed
7. **SRI VST** shows 4→1 → timing entry

Never skip steps. When you enter on step 6 without step 3, you're front-running structure.

---


---

## Family 5 — Regime & Force Indicators

---

### STRF/LQD Ratio

**File:** `pine/STRF_LQD_Ratio.pine`
**Type:** Oscillator (separate pane)
**Data sources:** NASDAQ:STRF (MicroStrategy preferred) / BATS:LQD (IG corporate bond ETF)
**Framework role:** Layer 1 Regime — Saylor credit precision signal. Strips interest-rate noise from STRF by normalising against IG credit. What remains is the MSTR-specific credit premium — a leading indicator for MSTR equity direction (credit typically recovers 3–7 bars before equity).

#### What It Shows

The STRF/LQD ratio line (teal = above Slow TL, maroon = below), a Fast EMA(20) trackline (yellow), a Slow SMA(50) trackline, a momentum histogram (FTL − STL), and a 1-year rolling percentile band. Signal markers for Credit Recovery (CR ▲), Credit Warn (CW ▼), and Credit Stress Entry (CS ✕).

**Key states:**
| State | Condition | MSTR Signal |
|---|---|---|
| Credit Stress | Ratio ≤ 20th percentile | Bearish divergence if BTC stable/rising |
| Credit Warn | Ratio crosses below Fast TL | Deterioration beginning — monitor |
| Neutral | 20th–40th percentile | No actionable signal |
| Credit Recovery | Ratio crosses above 40th percentile | Leading bull signal (3–7 bar lead) |
| Credit Healthy | Ratio ≥ 60th percentile | Structural tailwind confirmed |

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| Fast Trackline Length | 20 bars | EMA period for the fast trackline |
| Slow Trackline Length | 50 bars | SMA period for the slow trackline |
| Percentile Band Lookback | 252 bars | Rolling 1-year window for high/low percentile bands |
| Credit Stress Threshold | 0.20 | Ratio below the 20th percentile = stress |
| Credit Recovery Threshold | 0.40 | Ratio above the 40th percentile = recovery signal |
| Show Percentile Bands | true | Toggle the 1-year high/low fill and threshold lines |
| Show Momentum Histogram | true | Toggle the FTL−STL histogram bars |

#### How to Use It

1. **Watch for Credit Recovery (CR ▲)** when the ratio crosses the 40th percentile — this is the primary leading signal. It tends to precede MSTR equity recovery by 3–7 bars (12–28 hours on a 4H chart).
2. **Red background (Credit Stress)** with a stable/rising BTC = a bearish divergence — the market doubts the rally. Treat as a headwind.
3. **Momentum histogram** (FTL − STL): teal bars = improving credit spread, maroon bars = deteriorating. Bright = accelerating, faded = decelerating.
4. **BTC stable/rising but STRF/LQD falling**: Red flag. Market is discounting Saylor credit quality despite the BTC price.
5. **CR fires before MSTR equity recovers**: High-conviction AB3 entry setup. This is the signal Gavin identified as having a 3–7 day lead.
6. **Export as CSV** for the Python regime engine (17th regime input: STRF_LQD).

#### Key Signals

- **CR ▲ marker**: Credit Recovery — ratio crossed above 40th percentile. 3–7 bar lead time on MSTR. Primary leading bull signal.
- **CW ▼ marker**: Credit Warn — ratio dropped below Fast TL. Early deterioration; not yet stress.
- **CS ✕ marker**: Credit Stress Entry — entered the bottom 20th percentile. Structural headwind.
- **Red background activated**: Active credit stress zone. Reduce sizing on new entries.
- **Teal flash background**: Credit Recovery bar — the bar where CR fired.

#### Framework Connection

STRF/LQD is a Layer 1 Regime input that feeds the Python engine (`mstr_suite_engine.py`) via CSV export. Inside the Force Field indicator, STRF/LQD ratio fast/slow gap is the **primary force component** — it determines both the direction and the magnitude of the composite F_net signal. When STRF/LQD LT direction is MOMENTUM_BULL, the Force Field flips bullish.

#### Common Mistakes

- **Acting on a single CR signal without checking F_net.** A standalone CR marker is suggestive but not sufficient — the Force Field composite provides the full picture.
- **Using this indicator on a crypto-only view.** STRF/LQD only exists during MSTR trading hours. On 24/7 crypto charts, the ratio will show gaps. Use on MSTR 4H chart.
- **Ignoring the histogram direction.** The ratio level matters less than whether momentum is improving. A ratio at the 25th percentile with a bright teal histogram is more bullish than a ratio at the 30th percentile with maroon bars.

---

### Force Field Oscillator (MSTR Suite)

**File:** `pine/MSTR_Suite_Force_Field.pine`
**Type:** Oscillator (separate pane)
**Framework role:** Layer 0.75 — sits above the GLI macro layer and below the Regime Engine. Synthesizes five external force signals (STRF/LQD, MSTR/IBIT, STRC, STABLE.D, MSTR self) into a single composite F_net reading. Used as a structural gate on trade sizing confidence and entry timing.

> **Architecture note:** This indicator replicates the Python `mstr_suite_engine.py` force model in real-time. The Python engine (run from CSVs nightly) is the authoritative source. The Pine indicator provides live intraday tracking. They should agree closely at bar close; intraday divergence is normal.

#### What It Shows

F_net plotted as a colored line through five zones with background shading, horizontal threshold lines, and zone transition markers (triangles/X at zone crossings). An info table (top-right) shows zone, F_net value, trend direction, multiplier state, and all four component values.

**The Five Zones:**

| Zone | F_net Range | Confidence | Trading Implication |
|---|---|---|---|
| STRONG BULL | F > −0.19 | ⚠ PROVISIONAL | Do not enter bullish trades until gate confirmed (see Gate) |
| MOD BULL | −0.60 to −0.19 | ⚠ PROVISIONAL | Same — await 2026-09-08 checkpoint |
| NEUTRAL | −1.15 to −0.60 | — | No directional force; monitor |
| MOD BEAR | −1.66 to −1.15 | ✓ HIGH (75% WR +10d, N=36) | Bearish structural headwind active |
| STRONG BEAR | F < −1.66 | ✓ HIGH (76% WR +10d, N=29) | Maximum bearish force — defer all new longs |

> **Confidence asymmetry:** The BEAR zones are validated at HIGH confidence (75–91% WR at +10–30d, N≥29). The BULL zones are PROVISIONAL — the 2025–2026 backtesting period was predominantly bearish and did not generate sufficient bullish zone data. The 6-month checkpoint (2026-09-08) will evaluate whether STRONG_BULL graduates to HIGH confidence. Until then, bull zones require the Gate check below.

**The MSTR/IBIT LT Gate:**
Before entering any bullish trade when F_net is in a bull zone, check the info table for "Multiplier" state:
- `BULL` or `DECEL+` = gate met, proceed
- `TRANSIT` = gate not met, wait for MSTR/IBIT LT to confirm MOMENTUM_BULL
- `BEAR` = gate not met, do not enter bullish trades regardless of F_net

#### The Force Model Explained

F_net is a composite of five force vectors:

```
F_net = multiplier × f_primary + f_credit + f_stable + f_self
```

**f_primary — STRF/LQD (the primary force)**
The most predictive single component. Uses the LT direction (EMA20 vs SMA50 on the STRF/LQD ratio) as the directional gate, and ST magnitude (EMA5 vs SMA50) as the force amplitude. `STRF/LQD LT DECEL_BULL` had 100% WR at +10–30d in the backtest (N=6). This is the engine's strongest signal.

**multiplier — MSTR/IBIT LT (the amplifier)**
MSTR/IBIT ratio LT direction (EMA20 vs SMA50) acts as a multiplier, not an additive component. When MSTR/IBIT LT confirms the same direction as f_primary, the multiplier ranges 1.0–1.5×. When it conflicts, the multiplier compresses to 0.4–1.0×. Think of it as: "Does the premium expansion story support the credit signal?"

**f_credit — STRC ST × 0.5**
STRC (MicroStrategy preferred STRC) ST fast/slow gap using the exact ATR/RSI trackline formula from the SRI scripts (2H fast, 1D slow). When STRC credit is healthy and improving, this adds positive force. When STRC is stressed, it adds negative force. Weight: 0.5×.

**f_stable — STABLE.D LT × 0.4 (inverted)**
Stablecoin dominance (CRYPTOCAP:STABLE.C.D). Rising stablecoin dominance = capital flowing out of risk assets = bearish for MSTR. The component is inverted: rising STABLE.D *reduces* F_net. LT timeframe (4H fast, 1W slow). Weight: 0.4×. Note: STABLE.D has a ~10-day lag before it manifests in MSTR price — this component is most useful for 30-day+ trade structures.

**f_self — MSTR ST × 0.3 (self-reference)**
MSTR's own ST trackline gap (exact ATR/RSI formula, 2H fast / 1D slow) provides a self-referential component. Prevents the indicator from generating bullish force while MSTR itself is in active ST decline. Weight: 0.3×.

#### Trackline Method

| Instrument | Trackline Method | Timeframes |
|---|---|---|
| STRC | ATR/RSI supertrend (exact SRI formula) | ST: 2H fast / 1D slow |
| STABLE.D | ATR/RSI supertrend (exact SRI formula) | LT: 4H fast / 1W slow |
| MSTR self | ATR/RSI supertrend (exact SRI formula) | ST: 2H fast / 1D slow |
| STRF/LQD ratio | EMA fast / SMA slow on ratio close | LT: EMA20 / SMA50; ST: EMA5 / SMA50 |
| MSTR/IBIT ratio | EMA fast / SMA slow on ratio close | LT: EMA20 / SMA50 |

The ATR/RSI trackline (for single instruments) is the exact formula used by SRI_LT.pine and SRI_ST.pine: `ATR = ta.rma(ta.tr(true), 14)`, trails the low when RSI ≥ 50, trails the high when RSI < 50. Ratio instruments use EMA/SMA because synthetic ratios lack OHLC data for TR computation.

#### Inputs / Settings

| Setting | Default | What it does |
|---|---|---|
| ATR Period | 14 | ATR period for single-instrument tracklines (STRC, STABLE.D, MSTR) |
| ATR Coefficient | 1.0 | ATR multiplier. Increase to widen the trailing stops. |
| Fast EMA Length | 20 bars | EMA period for ratio tracklines (STRF/LQD, MSTR/IBIT) |
| Slow SMA Length | 50 bars | SMA period for ratio slow trackline |
| ST Fast EMA | 5 bars | Short-term EMA for STRF/LQD magnitude component |
| STRONG BULL threshold | −0.19 | F_net above this = STRONG BULL zone. Update after 2026-09-08 if graduated. |
| MOD BULL threshold | −0.60 | F_net above this = MOD BULL zone |
| MOD BEAR threshold | −1.15 | F_net below this = MOD BEAR zone |
| STRONG BEAR threshold | −1.66 | F_net below this = STRONG BEAR zone |
| Show Component Lines | false | Toggle individual f_primary, f_credit, f_stable, f_self lines |
| Show Zone Background | true | Toggle zone background shading |

**Ticker verification:** If any component shows `na` in the info table, the exchange prefix may need adjustment. Default tickers:
- STRC: `NASDAQ:STRC` — if na, try `BATS:STRC`
- STRF: `NASDAQ:STRF` — if na, try `BATS:STRF`
- STABLE.D: `CRYPTOCAP:STABLE.C.D`
- LQD: `BATS:LQD`
- IBIT: `BATS:IBIT`
- MSTR: `BATS:MSTR`

#### How to Use It

1. **Add to MSTR 4H chart** as a separate pane. The indicator pulls all six instruments internally — no other indicators needed.
2. **Read the zone first.** The background color and the zone label in the top-right table tell you the current structural regime.
3. **Check the Multiplier state.** If F_net is in a bull zone but Multiplier shows `TRANSIT` or `BEAR`, the gate is not met — do not enter bullish trades.
4. **In BEAR zones, reduce sizing confidence.** MOD BEAR means a 75% historical probability that MSTR will decline over the next 10 days. STRONG BEAR is 76%. These are not certainties — use them to size down, not to panic-sell.
5. **Toggle "Show Component Lines"** to see which force is dominating. If f_primary is strongly negative but f_credit is positive, credit is resilient — credit recovery may precede STRF/LQD turning.
6. **Set alerts** for zone transitions using the four built-in alert conditions.
7. **Trend direction** (↗/↘/→ in the table) tells you if F_net is improving or deteriorating within the current zone. RISING within a bear zone = force is recovering, not yet confirmed.

#### Key Signals

- **F_net enters BEAR zone (triangle ▼ marker)**: Structural headwind confirmed. Reduce position sizing confidence.
- **F_net enters STRONG BEAR (X marker)**: Maximum headwind. 76%+ WR historically. Do not open new longs.
- **F_net enters BULL zone (triangle ▲ marker) + Gate = BULL**: Provisional bullish signal. Requires MSTR/IBIT LT gate confirmation.
- **Trend = RISING while in BEAR zone**: Recovery beginning. Watch for zone transition. Not yet actionable.
- **f_primary turns positive while f_stable still negative**: STRF/LQD credit recovered before liquidity — early bull signal, still waiting for macro confirmation.

#### Force Field ROC — Interpretation Rule

**File:** `pine/MSTR Suite — Force Field ROC`
**Role:** Tactical derivative layer for the Force Field. The original Force Field remains the **base regime/state indicator**; the ROC version becomes the **primary operational read** when evaluating whether force is strengthening or weakening.

**Formal rule:**
- **Original Force Field wins on regime/state.** Use it to answer: *What force zone are we in right now?*
- **Force Field ROC wins on change/timing.** Use it to answer: *Is that regime strengthening, weakening, accelerating, or exhausting?*

This means the two indicators are **complementary, not redundant**.

**Interpretation hierarchy:**
1. **Read the original Force Field first** for current zone/state (`STRONG BULL`, `MOD BULL`, `NEUTRAL`, `MOD BEAR`, `STRONG BEAR`).
2. **Read Force Field ROC second** for the condition of that state:
   - `F_net ROC > 0` and rising = force improving
   - `F_net ROC < 0` = force deteriorating
   - `F_net Acceleration > 0` = improvement itself is strengthening
   - `F_net Acceleration < 0` = thrust is fading
3. **When they differ in tone, let ROC control the tactical interpretation without overriding the base regime.** Example: `F_net` still bullish while ROC turns down = **bullish regime, but decelerating** — do not treat as a fresh expansion leg.

**Operational decision rule:**
- **Original FF bullish + ROC rising/accelerating** → bullish and strengthening; continuation odds improving.
- **Original FF bullish + ROC falling/decelerating** → bullish but tiring; prioritize consolidation/exhaustion risk over breakout enthusiasm.
- **Original FF bearish + ROC rising** → bearish regime under repair; reduce urgency but do not front-run a full reversal.
- **Original FF bearish + ROC falling** → bearish and worsening; highest confidence defensive posture.

#### MSTR Topping Formation Ladder v1 — integration rule

For MSTR, Force Field ROC should now also be read inside the **MSTR Topping Formation Ladder v1**:
- **Phase A — Rejection / Exhaustion**
- **Phase B — Deterioration / Compression Collapse**
- **Phase C — Structure Break / Tactical Failure**
- **Phase D — Support Vacuum / Downside Release**

The important change is that the ladder is made of **phases**, while the underlying chart signals are treated as **non-sequential, role-based, weighted confirmation evidence**.

**Why this matters:**
FF ROC should no longer be treated as a generic supporting diagnostic. For MSTR topping formations, it should act as a **tactical override input** when structural bullish remnants still exist but short-term deterioration is accelerating.

**Required tactical rule:**
> When higher-timeframe bullish structure remains technically alive, but ST/LT deterioration cluster is active and meaningful support is too far away, tactical topping-formation signals take priority over residual bullish structure.

This is especially important for:
- **AB1** tactical bearish monetization (for example, call-sale timing against LEAPs)
- **AB2** bearish directional credibility after broader structure failure is underway

**Why the ROC version matters:**
The original Force Field correctly identifies the **state** (for example, `F_net` remains positive), but it can understate the most important new information: whether that positive force is **strengthening or fading**. The ROC layer captures the difference between:
- **bullish and accelerating**
- **bullish but decelerating**

That distinction is often the highest-value tactical edge.

**Current framework stance:**
- Keep **`MSTR_Suite_Force_Field.pine`** as the **canonical state/regime indicator**.
- Use **`MSTR Suite — Force Field ROC`** as the **default analytical / decision-support indicator**.
- Do **not** deprecate the original Force Field yet; it remains the anchor for zone logic and structural backdrop.

#### Setting Alerts

Four alert conditions are built in (configure via TradingView Alerts panel):

| Alert | Trigger | Action |
|---|---|---|
| `Force -> Bear Zone` | Any entry into MOD BEAR or STRONG BEAR | Review open positions; tighten stops |
| `Force -> STRONG BEAR` | Entry into STRONG BEAR specifically | Notify CIO; consider defensive action |
| `Force -> Bull Zone (PROV)` | Entry into MOD BULL or STRONG BULL | Check gate; do not act until MSTR/IBIT LT confirmed |
| `Force Zone Change` | Any zone transition | General notification |

#### 2026-09-08 Checkpoint

On or after September 8, 2026, Gavin will run the calibration command to evaluate whether STRONG_BULL should be graduated from PROVISIONAL to HIGH confidence:

```bash
docker exec openclaw-sbx-agent-mstr-cio-7db631bb python3 /mnt/mstr-scripts/mstr_suite_engine.py --calibrate 10 --zone STRONG_BULL
```

If the win rate is ≥ 70% with N ≥ 10, update the `engine_config` table and adjust the threshold inputs in this indicator accordingly.

#### Framework Connection

The Force Field sits at **Layer 0.75** in the four-layer architecture:

```
Layer 0:    GLI Engine (macro liquidity — global)
Layer 0.5:  Howell Phase Engine (asset allocation phase)
Layer 0.75: Force Field (MSTR-specific credit/liquidity force)
Layer 1:    Regime Engine (SRI stage, HYG, VIX, SRI)
Layer 2:    Signal Engine (AB1/AB2/AB3 entry signals)
Layer 3:    Allocation Engine (sizing, trim schedule)
```

The Force Field does not replace the SRI stage signal — it provides the structural backdrop that governs how much sizing confidence to apply. A Stage 2 bounce signal in STRONG BEAR context should be traded at reduced size (50% of normal). The same signal in MOD BULL context warrants full sizing.

The Python engine (`mstr_suite_engine.py`) stores signals to the `mstr_suite_signals` table in `mstr.db` on each daily analysis cycle. The morning brief (Section 4) includes the current zone and gate state. The Pine indicator provides live tracking between brief cycles.

#### Common Mistakes

- **Treating PROVISIONAL bull zones as HIGH confidence signals.** The bull zones have not been statistically validated yet. Until the 2026-09-08 checkpoint, treat STRONG BULL as a gate check only — require additional confirmation from SRI stage and STRF/LQD CR signal.
- **Acting on F_net without checking the Gate.** F_net = STRONG BULL + Multiplier = TRANSIT = do nothing. The MSTR/IBIT LT gate is the final gating condition for bull trades.
- **Ignoring the Trend direction.** F_net can be in NEUTRAL with a FALLING trend — it's headed toward MOD BEAR. That's a different posture than NEUTRAL with a RISING trend.
- **Assuming daily Python engine and live indicator will always match.** The Python engine reads from CSVs exported at market close. Intraday, the Pine indicator may show a different value as conditions evolve. Both agree at close. If they diverge significantly at close, investigate the CSV data freshness (check `csv_freshness_check.py` output).
- **Using this on non-MSTR charts.** The indicator can technically be applied to any chart, but all force components reference MSTR-ecosystem instruments. On any other asset, the readings are meaningless.

*Guide updated 2026-03-08. All scripts: Pine v6. Repo: [3ServantsP35/Grok](https://github.com/3ServantsP35/Grok/tree/main/pine).*
