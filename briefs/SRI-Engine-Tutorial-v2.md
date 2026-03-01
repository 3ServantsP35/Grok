# SRI Decision Engine — Complete Methodology Tutorial
**Version 2.1 | Date: 2026-03-05 | Author: CIO Engine**

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Data Architecture — 16 CSV Files](#2-data-architecture)
3. [SRI Framework Fundamentals](#3-sri-framework-fundamentals)
4. [ST-Primary Framework](#4-st-primary-framework)
5. [Context Classification: Headwind / Mixed / Tailwind](#5-context-classification)
6. [GLI Engine — Layer 0](#6-gli-engine--layer-0)
7. [Regime Engine — Layer 1](#7-regime-engine--layer-1)
8. [LOI — LEAP Opportunity Index](#8-loi--leap-opportunity-index)
9. [AB1 — Tactical LEAP Engine](#9-ab1--tactical-leap-engine)
10. [AB2 — Credit Spread Engine](#10-ab2--credit-spread-engine)
11. [AB3 — Strategic LEAP Accumulation](#11-ab3--strategic-leap-accumulation)
12. [AB4 — Cash & STRC Reserve](#12-ab4--cash--strc-reserve)
13. [Capital Allocation Engine](#13-capital-allocation-engine)
14. [PC Val — MSTR Perpetual Call Valuation](#14-pc-val--mstr-perpetual-call-valuation)
15. [Asset Classification](#15-asset-classification)
16. [Signal Cross-Reference & Priority Rules](#16-signal-cross-reference--priority-rules)
17. [Validated Performance Numbers](#17-validated-performance-numbers)
18. [Current Engine State (2026-03-05)](#18-current-engine-state)

---

## 1. Architecture Overview

The engine is organized into four layers. Each layer has a distinct function and feeds the next.

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 0: GLI ENGINE (Global Liquidity Index)               │
│  Central bank balance sheets → probability adjusters        │
│  Inputs: Fed (WALCL/M2), PBoC, ECB, BOJ + 42 Macro GRID    │
│  Output: GLI Z-score, GEGI score, Paradigm label            │
│  Function: Adjusts Layer 1 probabilities, NOT entry signals │
└─────────────────────────────────┬───────────────────────────┘
                                  │ probability weights
┌─────────────────────────────────▼───────────────────────────┐
│  LAYER 1: REGIME ENGINE                                     │
│  8 market inputs → composite score + vehicle selection      │
│  Inputs: BTC, MSTR/IBIT ratio, StableDom, STRC,            │
│          TLT, DXY, HYG, VIX                                 │
│  Output: Score -7 to +7, regime label, vehicle (MSTR/IBIT) │
└─────────────────────────────────┬───────────────────────────┘
                                  │ gates entry; sets sizing
┌─────────────────────────────────▼───────────────────────────┐
│  LAYER 2: SIGNAL LAYER                                      │
│  8 trading assets × 3 signal engines                        │
│  AB1: Pre-breakout LEAPs (tactical, 1w-90d)                 │
│  AB2: Credit spreads (MIXED context, 1-2 weeks)             │
│  AB3: LEAP accumulation (strategic, cycle-length)           │
└─────────────────────────────────┬───────────────────────────┘
                                  │ signals + context
┌─────────────────────────────────▼───────────────────────────┐
│  LAYER 3: ALLOCATION ENGINE                                 │
│  Bucket tracking: AB1/AB2/AB3/AB4                           │
│  AB1→AB3 transition logic                                   │
│  Floors, ceilings, portfolio independence                   │
└─────────────────────────────────────────────────────────────┘
```

**Technology stack:**
- TradingView: sensor layer — exports raw SRI data as 4H CSV files
- Python (`sri_engine.py`): decision layer — all signal logic
- Pine scripts: mirror layer — reflects engine state for visual coaching/diagnosis
- GitHub: data transport — Gavin pushes 16 CSVs daily; engine pulls and processes

**Critical rule:** Pine scripts do NOT generate signals. They display what the Python engine computed. Divergence between chart and engine is prohibited.

---

## 2. Data Architecture

### 2.1 Trading Assets (8) — Signal Layer

These assets generate AB1/AB2/AB3 signals.

| Asset | Exchange | File Prefix | Mode | Bars |
|---|---|---|---|---|
| MSTR | BATS | `BATS_MSTR, ` | Momentum | 2,341 |
| IBIT | BATS | `BATS_IBIT, ` | Momentum | 1,062 |
| TSLA | BATS | `BATS_TSLA, ` | Momentum | 2,361 |
| PURR | BATS | `BATS_PURR, ` | Momentum | 117 (observation) |
| SPY | BATS | `BATS_SPY, ` | Mean-Reverting | 2,341 |
| QQQ | BATS | `BATS_QQQ, ` | Mean-Reverting | 2,341 |
| GLD | BATS | `BATS_GLD, ` | Trending | 2,341 |
| IWM | BATS | `BATS_IWM, ` | Mean-Reverting | 2,341 |

All files: 4H candles, ~45 columns each.

### 2.2 Regime Inputs (8) — Layer 1

These assets are NOT traded. They inform the regime score and context.

| Asset | Exchange | File Prefix | Role |
|---|---|---|---|
| BTC | BITSTAMP | `BITSTAMP_BTCUSD` | Bitcoin cycle phase, vol regime |
| MSTR/IBIT Ratio | BATS | `BATS_MSTR_BATS_IBIT` | Vehicle selection (MSTR vs IBIT) |
| Stablecoin Dom | CRYPTOCAP | `CRYPTOCAP_STABLE.C.D` | Crypto risk appetite |
| STRC | BATS | `BATS_STRC` | Saylor engine health + hurdle rate |
| TLT | BATS | `BATS_TLT` | Rates regime |
| DXY | TVC | `TVC_DXY` | Dollar strength / liquidity |
| HYG | BATS | `BATS_HYG` | Credit stress |
| VIX | CBOE | `TVC_VIX` | Vol regime → AB2 strategy/sizing |

### 2.3 CSV Column Format

Each file contains:
```
time (unix) | open | high | low | close
VST SRI Bias Histogram
ST SRI Bias Histogram
LT SRI Bias Histogram
VLT SRI Bias Histogram
VST Fast Trackline | VST Slow Trackline
ST Fast Trackline | ST Slow Trackline
LT Fast Trackline | LT Slow Trackline
VLT Fast Trackline | VLT Slow Trackline
VST Reversal Support | Resistance | Robust Fit
ST Reversal Support | Resistance | Robust Fit
LT Reversal Support | Resistance | Robust Fit
VLT Reversal Support | Resistance | Robust Fit
VST Stage 4to1 | 1to2 | 2to3 | 3to4
ST Stage 4to1 | 1to2 | 2to3 | 3to4
LT Stage 4to1 | 1to2 | 2to3 | 3to4
VLT Stage 4to1 | 1to2 | 2to3 | 3to4
```

**File naming:** `{EXCHANGE}_{TICKER}, 240_{hash}.csv`  
Hash changes on each new export. Engine matches by prefix only (not exact filename).

**Daily workflow:** Gavin exports from TradingView and pushes to GitHub repo `3ServantsP35/Grok`. Engine fetches via GitHub API.

---

## 3. SRI Framework Fundamentals

### 3.1 What is SRIBI?

SRIBI (SRI Bias Index) is a multi-timeframe momentum indicator built on the Wyckoff accumulation/distribution framework. It measures the balance of buying vs selling pressure at four timeframes simultaneously.

**Positive SRIBI:** Fast Trackline (FTL) > Slow Trackline (STL) — buying pressure dominant  
**Negative SRIBI:** FTL < STL — selling pressure dominant  
**Zero cross:** The critical event — a shift in structural momentum

### 3.2 Four Timeframes

| TF | Role | Resolution | FTL Period | STL Period |
|---|---|---|---|---|
| **VST** | Entry timing | 2H | 2H | 1D |
| **ST** | Trade decision | 4H | 2H | 1D |
| **LT** | Structural context | 1D | 4H | 1W |
| **VLT** | Macro context | 2D | 8H | 2W |

**Key insight:** Each TF has a distinct role. They are NOT redundant. Do not average them.

### 3.3 The Four Stages

The SRI framework identifies four Wyckoff stages based on FTL/STL relationship:

| Stage | FTL vs STL | SRIBI | Description |
|---|---|---|---|
| **Stage 1** | FTL > STL, rising | Positive, low | Accumulation completing — markup beginning |
| **Stage 2** | FTL >> STL, accelerating | Positive, high | Markup in progress — strong uptrend |
| **Stage 3** | FTL > STL, declining | Positive, falling | Distribution — topping process |
| **Stage 4** | FTL < STL, declining | Negative | Markdown — downtrend |

**Stage 4→1 transition** (FTL crosses above STL from below) = the most important signal in the framework. It marks the end of markdown and the beginning of accumulation-to-markup.

### 3.4 The Structural Bullish Bias

The SRI framework is designed as a Wyckoff accumulation detector — it is structurally biased toward finding bullish setups. This is intentional.

**Implication:** Bearish FTL crosses (Stage 2→3, 3→4) are contra-indicators, not primary signals. The engine does not trade bearish SRI signals directly. It uses them for context only.

### 3.5 Why BTC Is a Regime Input, Not a Trading Asset

Backtest finding: SRI has never reliably predicted BTC direction.

| Era | ST Cross+ Win Rate | Key Factor |
|---|---|---|
| Pre-MSTR (2017-2020) | 50% | Random |
| Early Saylor (2020-2023) | 41% | Saylor buying absorbs dips |
| ETF era (2023-2024) | 43% | Institutional flows dominate |
| Preferred era (2024+) | 43% | Permanent buyer in market |

Additional finding: bearish ST crosses on BTC had 54% downside prediction pre-MSTR, but only **38% in the preferred era** — bearish signals now point UP because Saylor absorbs every dip. BTC SRI signals are anti-predictive in the current regime.

**Decision:** BTC stays in the data feed as regime input (cycle phase, vol regime). IBIT is used for crypto exposure in the trading universe.

---

## 4. ST-Primary Framework

This is the core decision framework. It was validated by Gavin (2026-03-01) and is the foundation of all signal generation.

### 4.1 Role of Each Timeframe

```
VST = TIMING     "When to execute — entry precision"
 ST = DECISION   "Whether to trade — the primary signal"
 LT = CONTEXT    "Structural environment — sizing + exit rules"
VLT = CONTEXT    "Macro environment — same as LT, longer horizon"
```

**Critical:** LT and VLT are NOT confirmation gates for entry. They do not need to agree with ST before entering. They define the environment and inform exit timing.

### 4.2 The Old Error vs. The New Rule

**Old AB1 (broken):** Wait for LT to confirm before entering.  
→ This caused entries AFTER the move, when the structural headwind had already resolved.

**New AB1 (correct):** Enter when ST crosses positive, LT is still negative.  
→ LT turning positive = EXIT signal (structural catch-up complete, profit capture)

### 4.3 Context Rules for Sizing

| Context | LT | VLT | Sizing | Notes |
|---|---|---|---|---|
| **TAILWIND** | Positive | Positive | Full size | Structure aligned. Good for existing positions. |
| **MIXED** | Negative | Positive | Full size | Best entry context. "Room to run." |
| **HEADWIND** | Negative | Negative | Half size or avoid | Structural resistance. Higher failure rate. |

**MIXED is the sweet spot for new entries.** When LT is still negative but VLT is recovering, the structural headwind hasn't fully resolved. This means the trade has maximum upside runway before LT catches up. LT catching up = the trade has matured = take profit.

---

## 5. Context Classification

Context is determined by LT and VLT SRIBI values at the time of the signal.

```python
if LT < 0 and VLT < 0:  → HEADWIND
if LT > 0 and VLT > 0:  → TAILWIND
else:                    → MIXED   # (LT-, VLT+) or (LT+, VLT-)
```

The most common MIXED configuration for entries is **(LT negative, VLT positive)** — this is the "structural lag, macro support" configuration that precedes the most reliable moves.

### 5.1 Validated Win Rates by Context — AB1

| Asset | HEADWIND | MIXED | TAILWIND |
|---|---|---|---|
| MSTR | 36% | **85%** | 72% |
| QQQ | — | **86%** | 65% |
| IWM | 100% (n=1) | **83%** | 50% |
| GLD | — | **82%** | 82% |

**Pattern:** MIXED context consistently outperforms TAILWIND for entry. HEADWIND entries are high risk (except rare capitulation setups).

### 5.2 The LT Exit Rule

When LT turns positive after entry in MIXED context:
- Structural catch-up is complete
- The divergence that made the trade attractive has resolved
- This is the primary exit signal for AB1 and AB2

**Validated:** LT_POSITIVE exit accounts for ~90% of all profitable AB2 exits in the backtest. Average hold time: 4-6 trading days.

---

## 6. GLI Engine — Layer 0

### 6.1 Purpose and Role

The GLI Engine sits above the market-based Regime Engine. It measures **global monetary liquidity** — the aggregate expansion or contraction of central bank balance sheets worldwide — and converts this into **probability adjusters** that modify how the Regime Engine interprets bullish and bearish signals.

Layer 0 does **not** generate buy/sell signals directly. It shifts the probability of Layer 1 regime calls being correct.

**Key research finding (Michael Howell, CrossBorder Capital):**
- GLI leads BTC price by **13 weeks** (correlation ρ = 0.58)
- Global liquidity expansions precede BTC rallies; contractions precede corrections
- This is the most reliable macro leading indicator for crypto and risk assets

### 6.2 GLI Proxy Components (Public FRED Sources)

The engine builds a GLI proxy entirely from publicly available Federal Reserve Economic Data (FRED). No paid API required.

**US Liquidity Block (primary):**

| Component | FRED Series | Weight | Interpretation |
|---|---|---|---|
| Fed Balance Sheet | WALCL | Primary | Total Fed assets — QE/QT direction |
| Bank Reserves | RESBALNS | Supporting | Reserve availability — credit multiplier |
| M2 Money Supply | WM2NS | Supporting | Broad money growth rate |
| SOFR-IORB Spread | SOFR - IORB | Signal | Funding stress indicator |

**International Block (proxies):**

| Central Bank | Proxy Method | Notes |
|---|---|---|
| PBoC (China) | M2 China (via FRED MYAGM2CNM189S) | Largest contributor to global liquidity after Fed |
| ECB (Europe) | ECB balance sheet (ECBASSETSW) | Euro area monetary base |
| BOJ (Japan) | BOJ balance sheet (JPNASSETS or proxy) | Persistent QE; yen carry trade signal |

**Combined GLI Index:**  
Sum of rolling 26-week change across all components (USD-normalized). Normalized to Z-score against 2-year rolling mean and standard deviation.

### 6.3 GLI Output: Z-Score and Trend

| Z-Score | Interpretation | Action |
|---|---|---|
| > +1.0 | Strong liquidity expansion | High confidence in bullish regime calls |
| +0.5 to +1.0 | Moderate expansion | Slight bullish tilt |
| -0.5 to +0.5 | Neutral | No adjustment to Layer 1 |
| -0.5 to -1.0 | Moderate contraction | Slight bearish tilt |
| < -1.0 | Strong contraction | High confidence in bearish regime calls |

### 6.4 GEGI — Global Economic Growth Index

The GEGI (Global Economic Growth Index) is a composite economic health measure separate from monetary liquidity. It combines:

| Component | Weight | Source |
|---|---|---|
| Fiscal policy impulse | 40% | Deficit-to-GDP direction (FRED) |
| Monetary policy stance | 30% | Rate cycle phase (Fed dot plot / actual) |
| External demand drivers | 30% | Trade balance, PMI composites |

**GEGI output:** Normalized score.  
- **GEGI > 1.0:** Amplify bullish regime signals  
- **GEGI < 0:** Amplify bearish regime signals  
- **GEGI 0–1.0:** Neutral — no amplification

### 6.5 Probability Adjustment Rules

These rules are applied to Layer 1 regime probabilities before generating entry gates:

```
GLI Z-score > +0.5:
  → Reduce bearish stage probability ~20%
  → Treat SRI Stage 4 as likely consolidation, not confirmed downtrend

GLI Z-score < -0.5:
  → Reduce bullish stage probability ~20%
  → Treat SRI Stage 1 as likely false bottom, not confirmed markup

GEGI > 1.0:
  → Amplify bullish regime overrides (higher confidence on risk-on calls)

GEGI < 0:
  → Amplify bearish regime overrides (higher confidence on risk-off calls)
```

**Critical: These are probability adjusters, not hard gates.** A GLI Z < -0.5 does not block AB1 entries. It raises the confidence threshold required and tags the signal with "GLI HEADWIND" in the output.

### 6.6 42 Macro GRID / Paradigm Framework

The GRID model classifies the macro regime along two axes:

```
         Growth ↑          Growth ↓
         ──────────────────────────────
Infl ↓ │ GOLDILOCKS        DEFLATION
Infl ↑ │ REFLATION         STAGFLATION
```

**Portfolio implications by GRID regime:**

| GRID Regime | Risk Assets | Bonds | Commodities | BTC/Crypto |
|---|---|---|---|---|
| **GOLDILOCKS** | Bullish | Bullish | Neutral | Bullish (lagged) |
| **REFLATION** | Bullish | Bearish | Very Bullish | Bullish |
| **STAGFLATION** | Bearish | Bearish | Bullish | Bearish |
| **DEFLATION** | Bearish | Very Bullish | Bearish | Bearish |

**Paradigm Framework (42 Macro):**  
Characterizes the structural monetary policy environment in multi-year phases:

| Paradigm | Description | Dominant Theme |
|---|---|---|
| **A** | Tightening — rate hikes, QT | Favor defensive, cash, short duration |
| **B** | Cutting — rate cuts, neutral QT | Risk recovery; bonds and gold lead |
| **C** | Largesse — fiscal + deregulation + reshoring | Risk assets, commodities, crypto; broadening rally |

### 6.7 42 Macro KISS and Dr. Mo Signals

**KISS (Keep It Simple, Stupid) model:** Binary portfolio signals — what to hold long vs short in the current regime. Updated weekly by 42 Macro.

**Dr. Mo:** Momentum-based confirmation signals. Confirms KISS portfolio direction with price momentum data.

Integration rule: KISS signals inform which assets to favor in the AB2 credit spread selection (e.g., KISS Bullish LQD → short-duration corporate credit is favorable; risk of spread blowout is low). These are advisory signals, not entry triggers.

### 6.8 Current Global Macro State (as of Jan 9, 2026 — 42 Macro Report)

```
GRID Regime:   GOLDILOCKS (growth ↑, inflation ↓) — modal medium-term outcome
Paradigm:      C — Fiscal/monetary largesse + deregulation + reshoring
GLI Trend:     Higher — significant uptrend medium-term per key leading indicators
GLI Peak:      Peaked; next trough expected ~2027 (Howell)

Dr. Mo:        Bullish → LQD (investment-grade corporate credit)
               Bearish → (none active)

Macro Weather Model (3-month outlook):
  Bullish:    Bonds, USD
  Bearish:    Stocks, Bitcoin, Commodities
  Warning:    Low probability of sustaining risk-on regime next 3 months

Positioning:   Reasonable crash risk (↓20%) medium-to-long term
               High crowding in equities — concentrated long exposure
               Warsh nomination = short-term risk-off for gold and stocks

Key catalysts:
  Fed RMOP:  $40B/month QT since Dec 2025
  SLR:       Supplementary Leverage Ratio reduction expected by Mar 2026
             (favorable for bank balance sheet expansion → liquidity positive)
  Dollar:    Structural headwinds — Paradigm C typically dollar-negative medium-term
```

**BTC-specific GLI signal (Howell):**  
GLI leading indicator peaked in late 2025. 13-week lag implies BTC faces meaningful headwinds in H1 2026. Target from Howell's model: potential retest toward $30K before next liquidity upcycle (~2027 base case). The $45T global refinancing wall by 2030 is the structural tailwind for risk assets beyond this correction.

**How this adjusts our Layer 1 scores:**  
- GLI Z-score currently declining from peak → trending toward -0.5 threshold  
- When GLI Z crosses below -0.5: any Stage 1 SRI signals on BTC/MSTR get tagged "likely false bottom" — require additional confirmation before AB1 entry  
- GEGI currently neutral (Paradigm C supports fiscal impulse; monetary policy still cutting) → no amplification currently

### 6.9 Implementation Status

| Component | Status | Location |
|---|---|---|
| GLI proxy (FRED) | 🔄 In Progress | `/mnt/mstr-scripts/gli_engine.py` (pending) |
| GEGI calculation | 🔄 Queued | To be appended to `gli_engine.py` |
| Layer 0 → Layer 1 wire | 🔄 Queued | `RegimeEngine.compute()` receives `GLIState` |
| 42 Macro manual import | ✅ Active | CIO reads report; applies rules manually until automated |
| FRED API client | ✅ Ready | `python-dotenv` + `requests`; no SSL issues in container |

**Manual protocol until `GLIEngine` is built:**  
When CIO produces a Morning Brief or trade recommendation, it reads the most recent 42 Macro research update and applies the probability adjustment rules manually. The GRID regime, Paradigm, and Dr. Mo signals are stated explicitly in the brief.

---

## 7. Regime Engine — Layer 1

### 7.1 Purpose

The Regime Engine reads 8 market-based regime inputs and produces:
1. A composite score (-7 to +7)
2. A regime label
3. A vehicle recommendation (MSTR or IBIT)
4. VIX level (for AB2 strategy selection)

Layer 0 (GLI) probability adjustments are applied to these outputs before regime gates are enforced on the Signal Layer.

### 7.2 Scoring Rules

| Input | Bullish (+1) | Neutral (0) | Bearish (-1) |
|---|---|---|---|
| **BTC** | Avg SRIBI > +10 | -20 to +10 | Avg SRIBI < -20 |
| **Stablecoin Dom** | ST < 0 (capital deploying) | — | ST > 0 (capital fleeing) |
| **DXY** | ST < 0 (weak dollar) | MIXED context | ST > 0 (strong dollar) |
| **HYG** | ST > 0 (credit healthy) | MIXED context | ST < 0 (credit stress) |
| **TLT** | ST > 0 (rates falling) | — | ST < 0 (rates rising) |
| **STRC** | ST > 0 AND price ≥ $97 | price ≥ $97 neutral | price < $97 stress |
| **VIX** | — (no direction score) | VIX 18-25 | VIX < 18 (low vol) |
| **MSTR/IBIT** | (vehicle selection only, no score) | | |

**VIX note:** VIX does not score bullish/bearish direction. It adjusts AB2 sizing: VIX > 25 = +25% size; VIX < 18 = -50% size.

### 7.3 Regime Labels

| Score | Label | Action |
|---|---|---|
| +4 to +7 | RISK-ON | Full allocation, favor momentum |
| +2 to +3 | CAUTIOUS BULLISH | Standard allocation |
| 0 to +1 | NEUTRAL | 50% size, favor MR/GLD |
| -2 to -1 | CAUTIOUS BEARISH | Defensive, spreads + cash |
| -3 to -7 | RISK-OFF | Cash/STRC only, no new entries |

**Entry gate:** No new AB1 or AB2 entries when regime score ≤ -2.

### 7.4 Vehicle Selection (MSTR/IBIT Ratio)

The MSTR/IBIT ratio SRIBI context determines which vehicle to use for crypto exposure:

| Ratio Context | Reading | Vehicle |
|---|---|---|
| MIXED (LT-, VLT+) | Premium expanding | **MSTR** (outperformance ahead) |
| TAILWIND (LT+, VLT+) | Premium peaked | **IBIT** (MSTR premium about to compress) |
| HEADWIND (LT-, VLT-) | Premium compressing | **IBIT** (wait for MSTR) |

**Current (Mar 5, 2026):** See Section 18 for latest regime state.

---

## 8. LOI — LEAP Opportunity Index

The LOI is a composite oscillator (-100 to +100) that measures the structural opportunity for LEAP accumulation.

### 8.1 Formula

```
LOI = (VLT_SRIBI_normalized × 40) + (VLT_acceleration × 30) + (LT_SRIBI_normalized × 15) + (Concordance × 15)
```

| Component | Weight | What it measures |
|---|---|---|
| VLT SRIBI (normalized) | 40% | Primary structural direction |
| VLT acceleration (ROC) | 30% | Rate of change — momentum of momentum |
| LT SRIBI (normalized) | 15% | Medium-term confirmation |
| Concordance | 15% | % of TFs in agreement (bull count) |

### 8.2 Thresholds by Asset Mode

| Signal | Momentum Assets | Mean-Reverting Assets |
|---|---|---|
| Deep Accumulation | LOI < -80 | LOI < -60 |
| Accumulation | LOI < -60 | LOI < -40 |
| Trim 25% | LOI > +40 | LOI > +10 |
| Trim 50% | LOI > +60 | LOI > +30 |
| Trim 75% | LOI > +80 | LOI > +50 |

### 8.3 LOI Deep Dive — What Each Zone Means

**LOI < -80 (Deep Accumulation):**  
All TFs negative, VLT accelerating downward. This is extreme fear. Historical: fired twice on BTC equivalent since 2021 (FTX bottom, current cycle Feb 2026). On MSTR: fired ~7 times total since 2021, 80%+ forward return at 90 days.

**LOI -60 to -80 (Accumulation):**  
VLT negative and decelerating, LT negative. Classic "spring" setup in Wyckoff terms — selling pressure exhausting. Best entry zone for long-duration LEAPs.

**LOI 0 to +40 (Recovery):**  
VLT recovering. First trims appropriate. Trade is working but not mature.

**LOI > +60 (Distribution):**  
VLT positive and high. Second and third trims appropriate. Structural overextension likely.

**LOI > +80 (Extreme):**  
All TFs positive and high. Final exits. GLD hit +80 in Feb 2026 — max trim zone.

---

## 9. AB1 — Tactical LEAP Engine

### 9.1 Philosophy

AB1 is the tactical LEAP bucket. It buys LEAPs **before** a high-probability breakout, captures the 10-40%+ underlying move over 1 week to 90 days, and exits when the structural move completes (LT turns positive). It is NOT a long-term hold — that's AB3.

Key distinction from AB3:
- **AB1:** Enter at pre-breakout signal, hold 1-90 days, capture the swing
- **AB3:** Enter at LOI deep accumulation, hold months to cycle completion, exit on phased trims

### 9.2 Entry Conditions (All 5 Required)

```
C1: AB3 ANCHOR — LOI was below acc_thresh within last 120 bars
    (Momentum: < -60 | MR: < -40)
    Purpose: Confirms a structural bottom was established recently

C2: STAGE 4→1 TRANSITION — FTL crossed above STL (ST or LT timeframe)
    within last 30 bars
    Purpose: Wyckoff markup initiation detected

C3: MIXED CONTEXT — LT < 0, VLT > 0
    Purpose: Room to run; structural headwind hasn't resolved yet

C4: VST POSITIVE — VST SRIBI > 0
    Purpose: Entry timing confirmed; short-term momentum aligned

C5: ST POSITIVE — ST SRIBI > 0
    Purpose: Trade direction confirmed by primary decision timeframe
```

**Cooldown:** 40 bars (6.7 trading days) minimum between signals on same asset.

### 9.3 Confidence Scoring

| Condition | Bonus |
|---|---|
| Base (5 conditions met) | 60% |
| LT cross (stronger than ST) | +10% |
| Deep anchor (LOI < acc - 20) | +10% |
| LOI recovering above 0 | +10% |
| Maximum | 90% |

### 9.4 LEAP Strategy

- **Strike:** 5-15% OTM (captures maximum leverage on a 10-30% underlying move)
- **Expiry:** 90-180 DTE at entry to allow the thesis to develop
- **Target:** 10%+ underlying move → 3-5× LEAP return (OTM leverage)
- **Max hold:** 90 calendar days (6 bars/day × 540 bars)

### 9.5 Exit Rules

| Trigger | Rule |
|---|---|
| **LT turns positive (primary)** | Exit immediately — structural catch-up complete |
| 90-day time stop | Exit at max hold regardless of position |

### 9.6 Failure → AB3 Transition

If the breakout fails:
- **Failure definition:** ST cross negative (ST SRIBI drops below 0) within 40 bars of entry AND underlying price gain < 5%
- **Action:** Tag the LEAP as AB3 (accounting change — do NOT force close)
- **Rationale:** If you bought a 1-year LEAP at a genuine accumulation bottom and the 90-day breakout didn't materialize, the long-term thesis likely still holds. Reclassify rather than realize a loss.

### 9.7 Validated Performance

| Asset | N | 30d Hit 10%+ | 60d Hit 10%+ | 90d Hit 10%+ | Max/90d |
|---|---|---|---|---|---|
| TSLA | 10 | 20% | 40% | 38% | **100%** |
| GLD | 5 | **60%** | **80%** | **80%** | **100%** |
| QQQ | 10 | 33% | 56% | **88%** | **88%** |
| MSTR | 8 | **75%** | 57% | **80%** | **80%** (med +361%) |
| SPY | 9 | 12% | 50% | 75% | 75% |
| IWM | 6 | 20% | 40% | 40% | 80% |

**Key finding:** Max achievable within 90d window is 80-100% for most assets. The move DOES happen — the variable is timing. Exit rules (LT-positive) capture the move rather than relying on a fixed calendar date.

---

## 10. AB2 — Credit Spread Engine

### 10.1 Philosophy

AB2 sells premium INTO structural divergence. When the market shows ST recovery but LT is still lagging (MIXED context), the spread premium decays as LT catches up. This is a mean-reversion premium capture play.

**The divergence thesis:** MIXED context (LT-, VLT+) = LT hasn't confirmed the recovery yet. Short-duration Bull Put spreads benefit from the passage of time as the structural recovery matures. LT turning positive = catch-up complete = exit the spread and capture theta.

### 10.2 Entry Conditions

```
C1: ST crosses positive (ST SRIBI crosses from below zero to above)
C2: VST positive (VST SRIBI > 0) — entry timing confirmed
C3: MIXED context (LT < 0 AND VLT > 0) — structural divergence active
C4: Regime score ≥ -1 (not in risk-off regime)
C5: VIX > 18 (premium worth selling)
```

**Critical:** MIXED context is the non-negotiable gate. This is what distinguishes AB2 v2 from v1, and why win rates improved dramatically across all assets.

### 10.3 Strategy Type

**Bull Put Spread:** Sell a put, buy a put further OTM. Profits from upward movement or neutral price action while LT recovers.

Spreads currently validated on: MSTR, TSLA, SPY, QQQ, GLD, IWM  
**IBIT is disabled for AB2** — MIXED context does not predict reliable LT catch-up timing on crypto-adjacent assets.

### 10.4 Exit Rules

| Trigger | Priority |
|---|---|
| **LT turns positive** | Primary — structural divergence resolved, exit immediately |
| 90-bar time stop (~15 trading days) | Secondary — if LT hasn't confirmed, cut the position |

### 10.5 VIX Scaling

| VIX | Action |
|---|---|
| > 25 | +25% position size (high premium = favorable) |
| 18-25 | Standard sizing |
| < 18 | -50% position size (low premium = unfavorable) |

### 10.6 Validated Performance (v2)

| Asset | N | Win% | Avg Underlying P&L | Avg Hold |
|---|---|---|---|---|
| **QQQ** | 25 | **84%** | +1.8% | 4 days |
| MSTR | 18 | **72%** | +4.7% | 4 days |
| IWM | 24 | **75%** | +0.2% | 4 days |
| GLD | 32 | **75%** | +0.9% | 3 days |
| SPY | 27 | 67% | +0.1% | 4 days |
| TSLA | 18 | 61% | -0.7% | 5 days |

Note: P&L shown is underlying % change from entry to exit. Actual spread P&L will differ based on strike selection, premium received, and IV at entry. Use as timing signal — selection details handled by portfolio owner.

**Exit breakdown:** ~90% of exits are LT_POSITIVE; <10% are TIME_STOP. TIME_STOP exits average -8 to -17% underlying — this is the tail risk.

### 10.7 What Changed from v1 to v2

| Parameter | v1 | v2 | Impact |
|---|---|---|---|
| Entry context | Any | MIXED only | +13% win rate on MSTR |
| Bear Call | MR assets only | Removed for now | Simplification — insufficient signals |
| Iron Condor | GLD/QQQ/IWM | Removed for now | Needs VIX gate before re-enabling |
| IBIT | Enabled (67%) | Disabled | MIXED context doesn't predict LT on IBIT |

---

## 11. AB3 — Strategic LEAP Accumulation

### 11.1 Philosophy

AB3 is the long-duration LEAP bucket. It identifies major cycle bottoms using the LOI oscillator and enters with the explicit expectation of holding through the full cycle (months to a year+). Exits are phased — it never tries to pick a top; it trims in tranches as LOI confirms distribution.

### 11.2 State Machine

The AB3 engine runs a cycle state machine with 4 states:

```
NEUTRAL ──LOI crosses below acc_thresh──► ACCUMULATING
    ▲                                          │
    │ LOI returns below reset level         LOI rises > acc + hysteresis
    │                                          │
TRIMMING ◄── all trims fired ──────── HOLDING
    │                                    │
    └── exit signal                      │── trim signals fire in sequence
```

**State rules:**

| State | Entry condition | Exit condition |
|---|---|---|
| NEUTRAL | Starting state | LOI crosses below threshold |
| ACCUMULATING | LOI < acc_thresh | LOI > acc_thresh + hysteresis |
| HOLDING | Exiting accumulation | LOI > first trim level |
| TRIMMING | LOI > final trim level | EXIT signal fires |

### 11.3 Thresholds by Asset Mode

| Parameter | Momentum | Mean-Reverting |
|---|---|---|
| Accumulation threshold | -60 | -40 |
| Deep accumulation threshold | -80 | -60 |
| Hysteresis band | 20 pts | 15 pts |
| Trim 1 | +40 | +10 |
| Trim 2 | +60 | +30 |
| Trim 3 | +80 | +50 |
| Exit | Full exit | Full exit |

**Cooldown:** 30 bars minimum between signals. Prevents re-firing during volatile LOI oscillations.

### 11.4 Trim Schedule

Gavin's decision (2026-02-28): **25% equal tranches across all assets.**

| Signal | Position Reduction |
|---|---|
| TRIM_25% | Sell 25% of position |
| TRIM_50% | Sell another 25% (50% total trimmed) |
| TRIM_75% | Sell another 25% (75% total trimmed) |
| EXIT_100% | Sell final 25% (full exit) |

When AB3 exits at +80 LOI, the full cycle from accumulation to distribution has completed. A new accumulation cycle may begin immediately if LOI drops back below the threshold.

### 11.5 Validated Performance

| Asset | N/yr | Acc Signal Win% at 20d | Notes |
|---|---|---|---|
| SPY | 11.7/yr | **89%** | Best MR performer |
| QQQ | 11.1/yr | **88%** | Excellent MR signal |
| GLD | 3.4/yr | 75% | Less frequent, high quality |
| MSTR | 4.3/yr | 50% (n=2) | Sparse signals, very high median gain |
| IBIT | 1.9/yr | 100% (n=1) | Too few signals to validate |
| IWM | 12.0/yr | 57% | Acceptable |
| TSLA | 4.2/yr | 0% (n=2) | ACC signals timing too early |

### 11.6 Current Open Positions (Mar 5, 2026)

| Asset | State | Last Signal | Date | Price |
|---|---|---|---|---|
| **TSLA** | 🔴 ACCUMULATING | ACC | Feb 5, 2026 | $397 (LOI -72.2) |
| MSTR | 🟡 TRIMMING | TRIM_25% | Feb 25, 2026 | $137 |
| IBIT | 🟡 TRIMMING | TRIM_25% | Jan 23, 2026 | $52 |
| SPY | 🟡 TRIMMING | TRIM_25% | Feb 9, 2026 | $694 |
| QQQ | 🟡 TRIMMING | TRIM_25% | Feb 25, 2026 | $615 |
| IWM | 🟡 TRIMMING | TRIM_25% | Feb 27, 2026 | $261 |
| GLD | 🟡 TRIMMING | TRIM_25% | Feb 27, 2026 | $481 |

**TSLA is the live accumulation signal** at LOI -72.2 — deep accumulation territory.

---

## 12. AB4 — Cash & STRC Reserve

### 12.1 Purpose

AB4 is the capital preservation bucket. When signals are absent or regime is bearish, capital sits here rather than being deployed into lower-probability trades.

### 12.2 STRC as the Hurdle Rate

STRC (Strategy Credit — Saylor's preferred share series) yields approximately **10% annual (~0.83%/month)**. This is the risk-free rate for this system.

**Decision rule:** Any AB1/AB2 trade must beat 0.83%/month expected return, or the capital stays in STRC.

### 12.3 STRC as a Regime Indicator

STRC price < $97 = credit stress signal. Saylor's funding engine is under pressure. This typically precedes BTC weakness and MSTR drawdowns.

STRC SRI state is included in the regime composite score.

### 12.4 Floor

**AB4 minimum: 10%.** Regardless of opportunity set, 10% of each portfolio stays in AB4 at all times. This ensures liquidity for emerging opportunities and prevents full deployment at cycle peaks.

---

## 13. Capital Allocation Engine

### 13.1 Baseline Allocation

| Bucket | Purpose | Target % | Floor | Ceiling |
|---|---|---|---|---|
| AB1 | Tactical LEAPs | 25% | None | None |
| AB2 | Credit spreads | 25% | None | None |
| AB3 | Strategic LEAPs | 25% | None | **35%** |
| AB4 | Cash/STRC | 25% | **10%** | None |

### 13.2 AB1 → AB3 Transition

When an AB1 LEAP fails to break out within the failure window:

1. **Trigger:** ST turns negative within 40 bars AND underlying gain < 5%
2. **Action:** Tag the LEAP as AB3 (accounting change only — LEAP stays open)
3. **Rationale:** If the LEAP was entered at a genuine accumulation bottom, the long-term thesis holds even if the short-term breakout failed
4. **Capital flow:** AB1 bucket shrinks, AB3 bucket grows by the same amount
5. **Alert:** If AB3 would exceed 35%, engine alerts portfolio owner for guidance

**Key:** This is never a forced close. It is a reclassification of intent and accounting.

### 13.3 AB3 Ceiling Enforcement

- **35% ceiling is mark-to-market**, not deployment-based
- If AB3 positions appreciate past 35% (e.g., MSTR doubles), an alert fires
- Engine does NOT automatically trim — it alerts the portfolio owner
- Owner may instruct a rebalance, or override and allow AB3 to stay above 35%

### 13.4 Portfolio Independence

Three portfolios are tracked independently:
- **Greg** ($5M, live trading)
- **Gavin** ($1M, paper trading)  
- **Gary** (TBD, educational)

Allocation decisions in one portfolio have zero implications for others.

### 13.5 Bucket Compression Priority

When AB3 receives capital via AB1 transitions, AB1 compresses automatically. If further adjustment is needed, the engine asks the portfolio owner for guidance. AB4 (cash) is the last resort and never goes below 10%.

---

## 14. PC Val — MSTR Perpetual Call Valuation

### 14.1 Model

MSTR is modeled as a **perpetual call option on its Bitcoin holdings**. The theoretical fair value is computed using Black-Scholes modified for perpetual options.

**Intuition:** MSTR holds Bitcoin as its primary asset. Its equity value above the net liability stack (debt + preferred - cash) is similar to a call option that expires whenever Saylor decides to realize the gains.

### 14.2 Formula

```
Underlying = BTC/share = (BTC holdings × BTC price) / shares
Strike = (Debt + Preferred - Cash) / shares
Tenor = 5 years (perpetual proxy)
Volatility = 30-day realized BTC vol
Risk-free = US 2Y yield

Fair Value = Black-Scholes(Underlying, Strike, T=5, vol, rf)
Band = ±1 standard deviation of historical FV
```

### 14.3 Constants (last updated from 8-K filings)

| Parameter | Value |
|---|---|
| BTC Holdings | 717,130 BTC |
| Shares (diluted) | 333,750,000 |
| Total Debt | $8.19B |
| Preferred Equity | $6.92B |
| Cash | $2.30B |
| Dilution Rate | 5%/yr |
| Tenor | 5 years |

**Staleness check:** Engine warns if holdings data is >90 days old. Update from EDGAR (8-K filings) after each quarterly filing.

### 14.4 Signal Interpretation

| Position vs Fair Value | Interpretation | AB Signal |
|---|---|---|
| > 40% premium | Extreme premium | Sell calls aggressively (AB2 Bear Call) |
| 15-40% premium | Premium | Sell calls selectively |
| -5% to +15% | Fair value | Neutral |
| -5% to -20% | Discount | Sell puts (AB2 Bull Put) |
| < -20% | Deep discount | Strong buy signal; LEAP entry (AB1) |
| At bottom band | Buy zone | Highest confidence LEAP entry |

### 14.5 Where It Lives

PC Val is computed entirely in Python from live BTC price + 8-K constants. No TradingView dependency.

---

## 15. Asset Classification

### 15.1 Three Asset Modes

**Momentum Assets** (BTC/MSTR/TSLA/IBIT dynamics):
- High volatility, trending behavior
- SRI: higher accumulation thresholds needed (LOI < -60)
- AB2: Bull Puts only (no Bear Calls, no IC)
- AB3: larger move expected; hold longer

**Mean-Reverting Assets** (SPY/QQQ/IWM dynamics):
- Lower volatility, oscillating behavior
- SRI: earlier accumulation signals (LOI < -40)
- AB2: Bull Puts valid; Bear Calls in HEADWIND possible
- AB3: more frequent signals, smaller moves

**Trending Assets** (GLD dynamics):
- Sustained directional moves, less mean-reversion
- Uses Momentum thresholds for LOI
- Backtested: AB1 100% win rate, AB2 75%, AB3 high signal frequency

### 15.2 Auto-Detection Logic

```python
if ticker in ['MSTR','BTC','BTCUSD','TSLA','IBIT','GBTC','BITO']:
    mode = MOMENTUM
elif ticker in ['GLD','IAU']:
    mode = TRENDING
else:
    mode = MEAN_REVERTING  # default for equities/ETFs
```

### 15.3 Observation Mode

**PURR** (AI company, listed Dec 2025): Only 117 bars as of March 2026. Engine tracks but does not generate signals. Minimum bar threshold: **500 bars** (~3 months at 4H). Expected to graduate from observation mode by ~June 2026.

---

## 16. Signal Cross-Reference & Priority Rules

### 16.1 Signal Hierarchy

When multiple signals fire on the same asset, priority order:

1. **Layer 0 (GLI) flag** — "GLI HEADWIND" tag reduces confidence; does not block
2. **Regime gate** — if score ≤ -2, override all entry signals
3. **AB3 deep accumulation (LOI < -80)** — highest priority entry
4. **AB1 pre-breakout** — tactical entry on confirmed Stage 4→1
5. **AB3 accumulation (LOI < acc_thresh)** — standard strategic entry
6. **AB2 Bull Put** — spread entry in MIXED context
7. **AB3 trim signals** — reduce existing positions
8. **AB2/AB1 LT exit** — close positions on structural catch-up

### 16.2 Conflict Resolution

**AB3 ACC fires while AB2 BULL_PUT is open:**  
Both are bullish. Keep the spread running. The AB3 entry builds a longer position alongside the spread.

**AB1 pre-breakout fires while AB3 TRIM is active:**  
The trim is AB3 reducing an existing large position. The AB1 is a new tactical position. These can coexist if bucket allocation allows.

**Regime turns RISK-OFF while spreads are open:**  
Do NOT forcefully close open spreads — their max loss is defined. Apply regime gate to NEW entries only. Alert the portfolio owner.

**GLI Z < -0.5 + AB1 signal fires:**  
Tag signal as "GLI HEADWIND — elevated false bottom risk." Raise minimum confidence threshold to 80% (vs standard 60%). Require deep anchor (LOI < -80) rather than -60. Signal is not blocked — it requires stronger confirmation.

### 16.3 The AB1/AB3 Sequencing Pattern

The ideal pattern is:
```
1. AB3 fires LOI < -60 (deep accumulation) → build AB3 strategic position
2. LOI recovers, Stage 4→1 fires → AB1 pre-breakout entry (tactical LEAP)
3. AB1 LEAP captures 10-40% move in 30-90 days (exit at LT+)
4. AB3 position continues holding through full cycle
5. LOI reaches +60-80 → AB3 begins phased trims
```

AB1 and AB3 are complementary, not competing. They use the same accumulation signal (LOI bottom) but with different time horizons and exit rules.

---

## 17. Validated Performance Numbers

### 17.1 AB1 Pre-Breakout (Underlying Returns)

| Asset | N | 60d 10%+ hit | 90d 10%+ hit | Max 90d |
|---|---|---|---|---|
| GLD | 5 | 80% | 80% | **100%** |
| QQQ | 10 | 56% | **88%** | 88% |
| MSTR | 8 | 57% | 80% | 80% (med +361%) |
| TSLA | 10 | 40% | 38% | **100%** |
| SPY | 9 | 50% | 75% | 75% |
| IWM | 6 | 40% | 40% | 80% |

### 17.2 AB2 MIXED-Context Bull Put (Underlying Signal)

| Asset | N | Win% | Avg P&L | Hold |
|---|---|---|---|---|
| QQQ | 25 | **84%** | +1.8% | 4d |
| GLD | 32 | **75%** | +0.9% | 3d |
| IWM | 24 | **75%** | +0.2% | 4d |
| MSTR | 18 | **72%** | +4.7% | 4d |
| SPY | 27 | 67% | +0.1% | 4d |
| TSLA | 18 | 61% | -0.7% | 5d |

### 17.3 AB3 Accumulation Signal (20d forward return)

| Asset | Win% at 20d | Median Return |
|---|---|---|
| SPY | **89%** | +5.2% |
| QQQ | **88%** | +7.6% |
| GLD | 75% | +7.8% |
| IWM | 57% | +1.0% |
| MSTR | 50% (n=2) | +7.5% |

### 17.4 Context Impact Summary

The single most impactful parameter change validated in backtesting:

**Adding MIXED context gate to AB2 Bull Put entries:**
- MSTR: 59% → 72% (+13 pp)
- IWM: 57% → 75% (+18 pp)
- QQQ: 74% → 84% (+10 pp)

This confirms the ST-Primary Framework's core thesis: MIXED context (LT-, VLT+) is the sweet spot for entries across ALL signal types (AB1 and AB2).

---

## 18. Current Engine State

*As of 2026-03-05 data (last CSV push)*

### 18.1 Layer 0 — Global Macro

```
42 Macro GRID:    GOLDILOCKS (growth ↑, inflation ↓)
Paradigm:         C — Fiscal/monetary largesse + deregulation + reshoring
GLI Trend:        Declining from peak (peaked late 2025)
GLI Z-Score:      Approaching -0.5 threshold — monitor weekly
GEGI:             Neutral (no amplification active)
Dr. Mo:           Bullish → LQD | Bearish → none
Warsh Warning:    Short-term risk-off for gold and equities
3-Month Outlook:  Macro Weather bearish for Stocks, BTC, Commodities
                  Low probability of sustaining risk-on regime next 3 months
BTC GLI Target:   Potential retest $30K if GLI trough arrives ~mid-2026
                  (Howell model; 13-week lead time)
SLR Catalyst:     Expected Mar 2026 — net liquidity positive for equities
GLI Adjustment:   Stage 1 SRI signals on BTC/MSTR tagged "false bottom risk"
                  until GLI Z recovers above -0.5
```

### 18.2 Layer 1 — Regime (Market-Based)

```
Composite Score: +1 / 7
Regime:  NEUTRAL — 50% size, favor MR/GLD
Vehicle: IBIT (MSTR/IBIT ratio in TAILWIND — premium peaked)
VIX:     19.9 (Normal — standard AB2 sizing)

Bullish:  Stablecoin Dom (-1 → risk-on), Credit (HYG healthy), Rates (TLT positive)
Bearish:  BTC (avg SRIBI -34), DXY (strong dollar)
Neutral:  STRC ($100), VIX (20)
```

### 18.3 Asset State

| Asset | Price | Context | LOI | AB3 State |
|---|---|---|---|---|
| MSTR | $129.63 | MIXED | -35.6 | TRIMMING |
| IBIT | $37.20 | HEADWIND | -75.3 | TRIMMING |
| TSLA | $402.42 | MIXED | -2.5 | **ACCUMULATING** |
| SPY | $686.17 | HEADWIND | -15.6 | TRIMMING |
| QQQ | $607.38 | HEADWIND | -29.1 | TRIMMING |
| GLD | $483.73 | TAILWIND | **+80.0** | TRIMMING |
| IWM | $261.43 | MIXED | +11.6 | TRIMMING |

### 18.4 Open AB2 Spreads

| Asset | Entry Date | Entry Price | Status |
|---|---|---|---|
| TSLA | Feb 13, 2026 | $420.62 | 🟢 OPEN (19 bars) |
| SPY | Feb 9, 2026 | $694.23 | 🟢 OPEN (27 bars) |
| QQQ | Feb 25, 2026 | $615.41 | 🟢 OPEN (5 bars) |

### 18.5 Live AB1 Signals

| Asset | Entry Date | Price | Conf | Status |
|---|---|---|---|---|
| TSLA | Feb 11, 2026 | $424.76 | 80% | Recent — within 90d window |
| SPY | Feb 25, 2026 | $692.31 | 70% | Recent — within 90d window |
| QQQ | Jan 23, 2026 | $623.20 | 70% | Recent — within 90d window |
| GLD | Feb 25, 2026 | $473.38 | 60% | Recent but GLD in TAILWIND |

---

## Appendix A: Decision Tree — New Trade

```
Incoming signal on asset X:

0. Check Layer 0 (GLI):
   - GLI Z < -0.5? → Tag signal "GLI HEADWIND"; raise confidence threshold
   - GEGI < 0? → Reduce position size; amplify bearish regime weight
   - Dr. Mo bearish on asset class? → Flag for human review before entry

1. Is regime score ≤ -2? → NO new entries
2. Is asset in observation mode (< 500 bars)? → track only
3. What is current context?
   - HEADWIND → reduce/avoid new entries
   - MIXED → prime entry zone
   - TAILWIND → existing positions OK, new entries cautious
4. Which bucket applies?
   - AB3 LOI < acc_thresh → AB3 strategic LEAP
   - AB1 conditions all met → AB1 tactical LEAP
   - MIXED + ST cross + VST → AB2 spread
5. Check bucket allocation:
   - AB3 already at 35%? → alert owner before new AB3
   - AB4 at 10%? → no new entries until rebalance
6. Vehicle selection (for crypto exposure):
   - MSTR/IBIT ratio MIXED → MSTR
   - MSTR/IBIT ratio TAILWIND/HEADWIND → IBIT
7. Size by regime score:
   - Score +4 to +7 → 100% target size
   - Score +1 to +3 → 75% target size  
   - Score -1 to 0 → 50% target size
   - Score ≤ -2 → 0% (blocked)
```

## Appendix B: Glossary

| Term | Definition |
|---|---|
| SRIBI | SRI Bias Index — momentum measure from FTL/STL relationship |
| FTL | Fast Trackline — shorter-period SRI moving average |
| STL | Slow Trackline — longer-period SRI moving average |
| LOI | LEAP Opportunity Index — composite accumulation/distribution signal |
| MIXED | Context where LT < 0, VLT > 0 (or opposite) — structural divergence |
| Stage 4→1 | FTL crossing above STL — Wyckoff markup initiation |
| mNAV | MSTR market cap / (BTC holdings × BTC price) — premium to NAV |
| PC Val | Perpetual Call Valuation — MSTR fair value via Black-Scholes |
| STRC | Saylor preferred share; 10% yield; regime indicator |
| AB1/2/3/4 | Allocation Buckets — Tactical LEAP / Spreads / Strategic LEAP / Cash |
| GLI | Global Liquidity Index — aggregate central bank balance sheet measure |
| GEGI | Global Economic Growth Index — fiscal + monetary + external demand composite |
| GRID | 42 Macro growth/inflation regime matrix (Goldilocks/Reflation/Stagflation/Deflation) |
| Paradigm | 42 Macro multi-year monetary cycle phase (A=tighten, B=cut, C=largesse) |
| KISS | 42 Macro model portfolio — binary long/short signals by asset class |
| Dr. Mo | 42 Macro momentum confirmation model — validates KISS portfolio direction |
| RMOP | Reserve Management and Operations Program — Fed QT mechanism |
| SLR | Supplementary Leverage Ratio — bank capital rule; reduction = liquidity expansion |

---

*Tutorial reflects engine state as of 2026-03-05. Next update: after GLIEngine Python class is built and wired into RegimeEngine.compute().*
