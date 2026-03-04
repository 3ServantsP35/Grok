# SRI Decision Engine — Complete Methodology Tutorial
**Version 2.5 | Date: 2026-03-04 | Author: CIO Engine**

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Data Architecture — 16 CSV Files](#2-data-architecture)
3. [SRI Framework Fundamentals](#3-sri-framework-fundamentals)
4. [ST-Primary Framework](#4-st-primary-framework)
5. [Context Classification: Headwind / Mixed / Tailwind](#5-context-classification)
6. [GLI Engine — Layer 0](#6-gli-engine--layer-0)
6b. [Howell Phase Engine — Layer 0.5](#6b-howell-phase-engine--layer-05) *(NEW)*
7. [Regime Engine — Layer 1](#7-regime-engine--layer-1)
8. [LOI — LEAP Opportunity Index](#8-loi--leap-opportunity-index)
8a. [LEAP Attractiveness Score](#8a-leap-attractiveness-score) *(NEW v2.3)*
9. [AB1 — Tactical LEAP Engine](#9-ab1--tactical-leap-engine)
10. [AB2 — PMCC Income Engine](#10-ab2--pmcc-income-engine)
11. [AB3 — Strategic LEAP Accumulation](#11-ab3--strategic-leap-accumulation)
12. [AB4 — Capital Reserve & Deployment Ruleset](#12-ab4--capital-reserve--deployment-ruleset)
13. [Capital Allocation Engine](#13-capital-allocation-engine)
13a. [SRIBI ROC Derivative](#13a-sribi-roc-derivative)
13b. [Alert System](#13b-alert-system)
13c. [Market Structure Report (MSR)](#13c-market-structure-report-msr) *(NEW v2.3)*
13d. [Personalized Portfolio Report (PPR)](#13d-personalized-portfolio-report-ppr) *(NEW v2.3)*
14. [PC Val — MSTR Perpetual Call Valuation](#14-pc-val--mstr-perpetual-call-valuation)
15. [Asset Classification](#15-asset-classification)
16. [Signal Cross-Reference & Priority Rules](#16-signal-cross-reference--priority-rules)
17. [Validated Performance Numbers](#17-validated-performance-numbers)
18. [Current Engine State (2026-03-05)](#18-current-engine-state)
19. [P-BEAR Signal Layer: Bearish Top Detection](#19-p-bear-signal-layer-bearish-top-detection) *(NEW v2.4)*
20. [Portfolio Defensive Posture (P-BEAR Phase 2)](#20-portfolio-defensive-posture-p-bear-phase-2) *(NEW v2.4)*
21. [Liquidity Regime and Timeframe Signal Weighting](#21-liquidity-regime-and-timeframe-signal-weighting) *(NEW v2.5)*

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
│  LAYER 0.5: HOWELL PHASE ENGINE (NEW)                       │
│  Sector ETF SRI states → macro cycle phase                  │
│  Inputs: XLK, XLY, XLF, XLE, XLP, TLT, GLD, IWM (LT SRIBI)│
│  Output: Phase (Rebound/Calm/Speculation/Turbulence),       │
│          confidence, per-asset AB3 size multiplier          │
│  Function: Gate Zero — blocks out-of-season entries        │
└─────────────────────────────────┬───────────────────────────┘
                                  │ phase gate + size multiplier
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

## 3a. Stage State Taxonomy

### 3a.1 From Four Stages to Ten States

The classic Wyckoff framework defines four stages: Accumulation (S1), Markup (S2), Distribution (S3), and Markdown (S4). While this four-stage model remains the conceptual foundation, the SRI engine's operational language is a **10-state taxonomy** that captures transition zones between stages with the same precision as the stages themselves.

> **Why this matters:** Two assets can both be in "Stage 4" yet have fundamentally different outlooks. One may be in deep markdown with no floor in sight; another may be showing early trough formation. The 10-state system makes this distinction explicit and maps each state to a specific AB strategy posture.

### 3a.2 The 10-State Taxonomy

| State | Code | Description | AB Posture |
|---|---|---|---|
| Accumulation | **S1** | FTL just crossed above STL; markup beginning | AB3 hold + begin AB2 income |
| Breakout Formation | **S1→2** | LT SRIBI rising; structural confirmation building | AB1 entry eligible; AB3 scaling |
| Markup | **S2** | FTL >> STL; accelerating positive | AB3 hold; AB2 income active |
| Stage 2 Continuation | **S2C** | Markup confirmed continuing; no distribution warning | AB3 full hold; AB2 at full gate |
| Distribution Warning | **S2→3** | SRIBI topping; breadth narrowing; first divergences | AB3 prepare trim; reduce AB2 delta |
| Distribution | **S3** | FTL declining toward STL; topping process | AB3 trim 1; pause new AB2 |
| Markdown Initiation | **S3→4** | FTL crosses below STL; downtrend beginning | AB3 trim 2-3; close AB2 |
| Markdown | **S4** | FTL << STL; sustained downtrend | No entries; AB4 only |
| Stage 4 Continuation | **S4C** | Markdown continuing; no floor signals | No entries; AB4 only |
| Bottom Formation | **S4→1** | LOI approaching deep threshold; VLT trough forming | Watch mode; begin STRC reduction |

### 3a.3 State Transition Flow

```
   S1 ──→ S1→2 ──→ S2 ──→ S2C
   ↑                         │
   │                     S2→3 (distribution warning fires)
   │                         │
S4→1                     S3  │
   ↑                         ↓
  S4C ←── S4 ←── S3→4 ←──────┘
```

### 3a.4 Key Rules

- **States are declared per timeframe** (ST-primary is the operational state; LT and VLT provide context).
- **The S4→1 and S4C distinction is critical:** S4C means all early-recovery criteria are absent. S4→1 means the watch conditions have begun to fire. Never skip from S4 to S1 — the intermediate states must be traversed sequentially.
- **S2C vs S2→3 is the most consequential mid-cycle decision.** Misclassifying S2→3 as S2C is the most common source of premature AB3 holds that become large drawdowns.


---

## 3b. Confirmation Ladders

### 3b.1 The Three-Tier Framework

Every key state transition uses a **Watch → Forming → Confirmed** ladder, with explicit **Invalidation** conditions. A signal stays at Watch until all Forming criteria are met; it stays at Forming until all Confirmed criteria are met. Missing one criterion holds the entire ladder at that tier.

This prevents premature conviction. The engine does not skip tiers.

---

### 3b.2 S4→1 (Bottom Formation — the Most Important Transition)

This is the primary AB3 LEAP entry signal. All three tiers must be evaluated before capital deployment.

#### Watch (Tier 1)
Triggers when:
- LOI ≤ −45 (Momentum assets: MSTR, TSLA, IBIT) **or** LOI ≤ −40 (Mean-Reverting assets: SPY, QQQ, GLD, IWM)

Action at Watch: Begin gradual STRC reduction. Do not buy LEAPs yet.

#### Forming (Tier 2)
Requires ALL of:
- VLT trough confirmed (VLT SRIBI ROC turns positive while VLT SRIBI still negative — "Drag Diffusing")
- STH-MVRV < 1.0 (for BTC-correlated assets: MSTR, IBIT)
- Episode type = Structural (not Cyclical or Idiosyncratic — see episode classification in §13a)

Action at Forming: Sizing preparation complete; early 25% Anticipatory Tranche eligible (see §8a).

#### Confirmed (Tier 3)
Requires ALL of:
- VLT Recovery Clock ≤ 6 bars since VLT trough
- CPS (Confirmation Point Score) ≥ 70
- LT SRIBI slope turning positive (SRIBI ROC > 0 at LT timeframe)
- BTC bottom confirmed (for BTC-correlated assets)
- Howell Gate Zero passes (phase eligible for this asset class)

Action at Confirmed: Full AB3 entry eligible. LEAP buy authorized.

#### Invalidation
- LOI recovers above −20 without triggering Confirmed → reset to NEUTRAL state
- VLT Recovery Clock exceeds 10 bars without reaching Confirmed → downgrade to Watch
- Regime score drops ≤ −2 → suspend until regime recovers

---

### 3b.3 S2C vs S2→3 (The Mid-Cycle Decision)

These two states share the same starting point (active Stage 2 Markup) but diverge on breadth and momentum data.

#### S2C (Stage 2 Continuation) — Confirmed When:
- CPS ≥ 65 (broad multi-timeframe agreement still intact)
- IWM context: NOT a headwind (IWM LT ≥ 0 **or** Howell phase = Calm/Rebound)
- VLT Recovery Clock ≤ 6 bars (recent recovery; not overextended)

#### S2→3 (Distribution Warning) — Confirmed When:
- 3 or more consecutive red bars on Slow Trackline (STL declining)
- **OR** BREADTH_DIVERGENCE active: IWM showing bullish divergence while SPY/QQQ correct (capital crowding into mega-cap — the Speculation-phase top signature)

#### Invalidation of S2→3 (revert to S2C):
- Slow Trackline resumes positive slope for 2+ consecutive bars AND CPS recovers ≥ 65
- IWM rejoins the correction (BREADTH_DIVERGENCE clears)

---

### 3b.4 S1→2 (Breakout Formation)

#### Watch:
- LOI crosses above −20 (exiting accumulation zone)
- ST SRIBI positive for ≥ 2 consecutive bars

#### Forming:
- LT SRIBI turning positive (LT ROC > 0)
- VLT SRIBI recovering (VLT ROC > 0 while VLT SRIBI still negative — "MIXED context intact")
- CT Tier ≥ 2

#### Confirmed:
- CT Tier ≥ 3
- LOI above 0
- Howell Phase = Rebound or Calm (season appropriate)
- Regime score ≥ 0 (NEUTRAL or better)

Action at Confirmed: AB1 pre-breakout LEAP entry eligible.

#### Invalidation:
- ST SRIBI turns negative before LT confirmation → reset to S1

---

### 3b.5 S3→4 (Markdown Initiation)

#### Watch:
- FTL crosses below STL on ST timeframe
- LT SRIBI declining for ≥ 3 bars

#### Forming:
- VLT SRIBI turning negative (VLT ROC < 0)
- Regime score ≤ 0

#### Confirmed:
- LT SRIBI negative AND VLT SRIBI negative (full HEADWIND context)
- LOI drops below 0

Action at Confirmed: Close AB2 calls; advance AB3 trim schedule; shift to AB4 staging.


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

## 6b. Howell Phase Engine — Layer 0.5

### 6b.1 Purpose and Role

The Howell Phase Engine sits between the GLI macro view (Layer 0) and the per-asset regime signal (Layer 1). It answers a structural question neither layer addresses:

> *Which asset classes are "in season" right now within the global liquidity cycle?*

Michael Howell's framework identifies four repeating macro phases — Rebound, Calm, Speculation, Turbulence — driven by the Global Liquidity cycle. Each phase has distinct sector winners and losers. Entering an asset in the wrong phase is equivalent to planting crops in winter: the signal may be technically correct but the macro environment prevents the trade from working.

**The four seasons analogy:**
- 🌱 **Rebound** = Spring — plant equities and risk assets; they emerge fastest from the trough
- ☀️ **Calm** = Summer — everything grows; maximum participation, maximum AB2 income
- 🍂 **Speculation** = Autumn — harvest Commodities/Energy; equity breadth narrows; cyclicals roll over first
- 🌧️ **Turbulence** = Winter — shelter in Bonds and Defensives; preserve optionality; wait for spring

### 6b.2 Phase Detection Methodology

The engine reads **LT SRIBI** from 8 sector ETF CSV exports (same 4H format as trading assets) and classifies each as BULL (LT > +5), BEAR (LT < -5), or NEUTRAL. It then scores each phase against a signature matrix derived from Howell's published traffic light slide (GLIndexes, Slide 35):

| Sector | Proxy | Rebound | Calm | Speculation | Turbulence |
|---|---|---|---|---|---|
| XLK | Technology | + | + | + | **−** |
| XLY | Cyclicals | + | + | **−** | **−** |
| XLF | Financials | + | + | 0 | **−** |
| XLE | Energy | − | + | + | **−** |
| XLP | Defensives | − | + | + | **+** |
| TLT | Bond Duration | − | 0 | − | **+** |
| GLD | Commodities | − | 0 | + | **−** |
| IWM | Cyclicals broad | + | + | **−** | **−** |

Phase score = sum of (expected_sign × actual_signal) for each sector. Highest score wins. Confidence = score gap to next-best phase, normalised 0–100%.

### 6b.3 Gate Zero: AB3 Entry Eligibility by Phase

| Asset | Rebound | Calm | Speculation | Turbulence |
|---|---|---|---|---|
| Beta/Risk On (MSTR, IBIT) | ✅ 100% | ✅ 100% | ⚠️ 50% | ❌ 0% — wait |
| Equities (SPY, QQQ) | ✅ 100% | ✅ 100% | ❌ 0% | ✅ 100% flush only |
| Cyclicals (TSLA, IWM) | ✅ 100% | ✅ 100% | ❌ 0% | ❌ 0% — wait |
| Commodities (GLD) | ❌ 0% | ✅ 100% | ⚠️ 75% | ❌ 0% |
| Bond Duration (TLT) | ❌ 0% | ❌ 0% | ❌ 0% | ✅ 100% |

**Hard rule:** Size multiplier of 0% means the entry is blocked regardless of LOI depth, CPS score, or VLT recovery speed. A CPS of 80 in a blocked phase is still a blocked entry.

### 6b.4 IWM Breadth Gate (SPY/QQQ only — applies inside Turbulence)

When phase = Turbulence and SPY/QQQ LOI crosses -40, a second sub-gate activates:

- **IWM headwind (LT < 0 AND VLT < 0) at the SPY trough** → ✅ broad flush → eligible. Historical continuation rate: 51–63% in Structural episodes.
- **IWM neutral or bull at the SPY trough** → ❌ BREADTH_DIVERGENCE → blocked. This is the Howell Speculation-phase top signal in disguise — capital concentrated in mega-cap while small caps already deteriorated. Historical continuation rate: 10–13%.

This signal is named `BREADTH_DIVERGENCE` in the system.

### 6b.5 AB2 Phase Rules

| Phase | AB2 Call-Selling |
|---|---|
| Rebound | Standard LOI gates; aggressive income harvesting |
| Calm | Maximum AB2 activity; highest income period |
| Speculation | Reduce max_delta by 0.05 on all Equity/Cyclical assets |
| Turbulence | **PAUSE AB2** across all assets — preserve LEAP optionality |

### 6b.6 The Turbulence → Rebound Transition (Primary AB3 Signal for Beta Assets)

In Howell's framework, Beta/Risk On assets (MSTR, IBIT) are the **first to recover** at the beginning of Rebound — they lead the rotation out of Turbulence. This is consistent with BTC historically leading global risk-on recoveries.

**Operational signal:** When MSTR/IBIT LOI begins recovering from deep negative territory (crosses above -20) while phase is still technically Turbulence, this is an **early Rebound indicator**. It typically precedes the full phase shift by 2–4 weeks.

The `HOWELL_PHASE_TRANSITION` Discord alert fires immediately when the engine detects a phase change. This alert is the primary AB3 entry trigger for Beta assets.

### 6b.7 Current Phase and DB State

**Live phase (as of 2026-03-02): 🌧️ Turbulence**
- Score: Turbulence +3 | Speculation +2 (low confidence 12.5% — XLE/GLD anomaly noted)
- XLK/XLY/XLF: BEAR ✅ consistent with Turbulence
- TLT/XLP: BULL ✅ consistent with Turbulence
- XLE/GLD: BULL ⚠️ anomaly — XLE = early-cycle energy; GLD = structural CB demand (known divergence)

**DB tables:** `howell_phase_state` (every daily run), `howell_phase_transitions` (on change)
**Script location:** `HowellPhaseEngine` class in `/mnt/mstr-scripts/sri_engine.py`
**Data inputs:** 5 sector ETF CSVs (XLK/XLY/XLF/XLE/XLP) + TLT/GLD/IWM from existing data directory

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

## 8a. LEAP Attractiveness Score

### 8a.1 Purpose

The LEAP Attractiveness Score is a **0–10 composite rating** published in every Market Structure Report (MSR). It translates the multi-layer signal stack — stage state, Howell phase, macro regime, and BTC confirmation — into a single actionable number that drives position-sizing decisions.

The score is **objective**: all inputs are quantitative and apply equally to all readers of the MSR. Personal modifiers (income gap, platform deployment readiness) are applied only in the Personalized Portfolio Report (PPR) and are never included in the MSR.

### 8a.2 Base Score by Stage State

| Stage State | Base Score | Rationale |
|---|---|---|
| S3 (Distribution) | 0 | Topping; markdown not yet confirmed |
| S4 (Markdown) | 0 | Active downtrend |
| S4C (Stage 4 Continuation) | 0 | No floor in sight |
| S3→4 (Markdown Initiation) | 1 | Transition underway; avoid |
| S2→3 (Distribution Warning) | 2 | Deteriorating; reduce exposure |
| S2C (Stage 2 Continuation) | 4 | Structural hold; not entry |
| S2 (Markup) | 3 | Extended; entry risk high |
| S1 (Accumulation) | 9 | Primary entry zone |
| S1→2 (Breakout Formation) | 8 | AB1 entry zone |
| S4→1 Watch | 5 | Watching; not yet actionable |
| S4→1 Forming | 7 | Anticipatory entry eligible |
| S4→1 Confirmed | 10 | Full AB3 entry authorized |

### 8a.3 Objective Modifiers (applied in MSR)

| Condition | Modifier | Rationale |
|---|---|---|
| Howell Phase = Turbulence (Gate Zero fails) | −1.5 | Wrong season; entry risk elevated |
| GLI contraction (Z-score < −0.5) | −0.5 | Macro headwind; reduced probability |
| BTC bottom unconfirmed (for BTC-correlated assets) | −0.5 | Missing upstream confirmation |
| mNAV < 1.0× (MSTR trading at discount to BTC NAV) | +0.5 | Structural undervaluation bonus |
| Floor proximity < 15% (price within 15% of VLT support) | +0.5 | Near-floor entry reduces downside |
| Cycle target > 3× from current price | +0.25 | Asymmetric upside present |

**Maximum objective modifier:** Capped at +1.5 above base, −2.0 below base. The base score reflects stage state which is the primary driver.

### 8a.4 Platform Value Modifier (PPR Only — Never in MSR)

The Platform Value modifier adjusts the score for an individual user's income generation gap:

```
Income Gap = Target monthly yield (2%/month) − Current STRC + PMCC yield
```

| Income Gap | Modifier |
|---|---|
| Gap > 1.5%/month (severely under-generating) | +1.0 |
| Gap 0.5%–1.5%/month (moderately under-generating) | +0.5 |
| Gap < 0.5% or surplus (on target or above) | 0 |

This modifier acknowledges that a user who has not yet built their income engine may rationally act earlier (at score 6–7 rather than waiting for score 8) because the opportunity cost of waiting is higher — they are losing income every month the platform is not built.

**This modifier is personal, private, and never appears in shared reports.**

### 8a.5 Action Thresholds

| Score | Action |
|---|---|
| ≥ 8 | **Full AB3 entry** — deploy from AB4 at full sizing |
| 6–7 | **Anticipatory Tranche** — 25% of target AB3 size; record as ANTICIPATORY in trade_log |
| 4–5 | **Watch only** — no capital deployment; STRC reduction not yet begun |
| ≤ 3 | **No entry** — ignore any LOI signals; maintain full AB4 posture |

### 8a.6 Anticipatory Tranche (Score 6–7)

When the score is 6–7 — below the full deployment gate but above watch-only — a small early partial position is eligible. Conditions:

1. Score is 6–7 on the MSR objective basis alone (before Platform Value modifier)
2. Platform Value modifier is active (+0.5 or +1.0), lifting final PPR score to ≥ 7
3. Howell Gate Zero passes (phase is not blocked)
4. Regime score ≥ 0 (NEUTRAL or better)

**Tranche size:** 25% of target AB3 sizing. If the position later qualifies for full deployment (score reaches 8), deploy the remaining 75%.

**Trade log entry:** Record with `entry_type = ANTICIPATORY`. This ensures clear distinction from standard AB3 entries in performance attribution.


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

## 10. AB2 — PMCC Income Engine

> **Framework v3.0 (approved 2026-03-02, Gavin).** Bull Put Spreads are retired. AB2 is now exclusively a PMCC (Poor Man's Covered Call) income overlay running against AB3 LEAPs. No new capital required.

### 10.1 Philosophy

AB2 harvests time decay from the AB3 position without requiring additional capital. The AB3 LEAP is the long leg. Short calls (<90 DTE) are sold against it to generate monthly income while the underlying cycles through recovery.

**Core principle:** The short call delta is controlled by where we are in the LOI cycle. Early in recovery (LOI < -20), full upside must be preserved — no calls. Mid-cycle (LOI -20 to threshold), sell OTM calls for income. Late-cycle (LOI > threshold), sell closer-to-the-money calls to intentionally reduce delta as the position matures.

**IBIT re-enabled.** The prior IBIT restriction applied only to Bull Put Spreads (MIXED context unreliable for crypto LT catch-up). PMCC structure is context-independent — if you hold an IBIT AB3 LEAP, you can sell calls against it.

### 10.2 Gate States

The LOI + CT Tier combination determines which calls, if any, can be sold:

| Gate State | LOI Condition | CT Required | Max Delta | Action |
|---|---|---|---|---|
| 🔴 NO_CALLS | LOI < -20 | Any | 0.00 | Accumulation zone — preserve all upside |
| 🟢 OTM_INCOME | -20 ≤ LOI < threshold | CT2+ | 0.25 | Sell OTM calls; never within 20% of spot |
| 🟠 DELTA_MGMT | LOI ≥ threshold + CT3+ | CT3+ | 0.40 | Sell ATM/ITM calls — intentional delta reduction |
| ⏸️ PAUSED_AB1 | AB1 active on same asset | — | 0.00 | Don't cap the breakout |

### 10.3 DELTA_MGMT Threshold by Asset Class

Momentum assets (MSTR, TSLA, IBIT) can run 40–60%/month during Saylor/FOMO cycles. Switching to delta reduction at LOI +20 would cap them prematurely.

| Asset Class | Assets | DELTA_MGMT Threshold |
|---|---|---|
| Momentum | MSTR, TSLA, IBIT | LOI > **+40** |
| Mean-Reverting | SPY, QQQ, GLD, IWM | LOI > **+20** |

**Rationale:** MSTR ran +152% between LOI +20 and +60 during Sep'24–Jan'25. Capping at +20 would have forfeited most of that gain on the LEAP.

**GLI adjustment:** When GLI Z-score > +0.5 or GEGI > 1.0, the Momentum threshold rises to min(base+20, 40). When GLI Z < -0.5, it falls to max(base-10, 10). This reflects liquidity-driven cycle timing.

### 10.4 Strike Selection Rules

- **OTM_INCOME mode:** Select strike at delta ≤ 0.25. Never within 20% of current spot (protects against MSTR gap moves).
- **DELTA_MGMT mode:** Select strike at delta ≤ 0.40. This is deliberate delta reduction, not income maximization.
- **Duration:** Target 30–45 DTE sweet spot for time decay. Hard maximum 90 DTE.
- **Income target:** 2–5%/month of LEAP cost basis (cycle average, not monthly floor).

### 10.5 IV Regime — When to Be Aggressive

| IV Percentile | Action |
|---|---|
| 90th+ (Ultra-High) | Maximum aggression — sell at top of delta range; LEAP entry also ideal |
| 70–90th (High) | Standard cycle — full premium harvest, target 3–5%/month |
| 30–70th (Normal) | Conservative — OTM only, delta ≤ 0.20; skip if premium < 0.83%/month hurdle |
| <30th (Low) | Pause AB2; focus on AB3 LEAP accumulation if LOI signals present |

### 10.6 AB1 Interaction

When an AB1 breakout signal fires on an asset where you hold an AB3 LEAP + open short call:
1. **Pause** new short call sales immediately.
2. **Evaluate** existing open short call — if breakout confirmed, consider closing to free delta.
3. **Resume** call sales when AB1 completes (LT turns positive or 90-bar time stop).

Never sell calls during an active AB1 window. You don't cap a breakout.

### 10.7 Current Gate States (as of Feb 27, 2026)

| Asset | LOI | CT | Gate | Threshold |
|---|---|---|---|---|
| MSTR | -30.5 | CT3 | 🔴 NO_CALLS | LOI > -20 to open |
| IBIT | -20.5 | CT2 | 🔴 NO_CALLS | 0.5 pts from open |
| TSLA | -3.5 | CT0 | 🟢 OTM_INCOME | Open (CT0 caution) |
| SPY | +17.4 | CT3 | 🟢 OTM_INCOME | Open |
| QQQ | +2.5 | CT2 | 🟢 OTM_INCOME | Open |
| GLD | +23.3 | CT4 | 🟠 DELTA_MGMT | Active trim mode |
| IWM | +5.0 | CT3 | 🟢 OTM_INCOME | Open |

### 10.8 Validated Entry-Timing Performance (Legacy AB2 — Bull Put Spreads)

The underlying entry-timing signals are unchanged. These win rates apply to the LOI/CT entry gates that now control PMCC call-selling timing:

| Asset | N | Win% | Avg Underlying Move | Avg Hold |
|---|---|---|---|---|
| **QQQ** | 25 | **84%** | +1.8% | 4 days |
| MSTR | 18 | **72%** | +4.7% | 4 days |
| IWM | 24 | **75%** | +0.2% | 4 days |
| GLD | 32 | **75%** | +0.9% | 3 days |
| SPY | 27 | 67% | +0.1% | 4 days |
| TSLA | 18 | 61% | -0.7% | 5 days |

**PMCC income window availability** (% of bars in OTM_INCOME or DELTA_MGMT gate):

| Asset | Income-Available % | Threshold |
|---|---|---|
| GLD | 97.2% | LOI > +20 (MR) |
| SPY | 95.5% | LOI > +20 (MR) |
| QQQ | 91.1% | LOI > +20 (MR) |
| IBIT | 89.8% | LOI > +40 (Momentum) |
| IWM | 86.6% | LOI > +20 (MR) |
| TSLA | 78.7% | LOI > +40 (Momentum) |
| MSTR | **76.8%** | LOI > +40 (Momentum) |

MSTR has 23.2% NO_CALLS time — concentrated in deep accumulation cycles. Those are exactly the windows when you want to preserve LEAP upside, so this is correct behavior.

### 10.9 Framework Evolution

| Version | AB2 Structure | Status |
|---|---|---|
| v1.0 | Bull Put Spreads (any context) | Retired |
| v2.0 | Bull Put Spreads (MIXED context only) | Retired |
| **v3.0** | **PMCC income overlay on AB3 LEAPs** | **Active** |

Iron Condors and Bear Call Spreads remain retired (pending P14 reactivation — Gavin to sequence).

---

## 11. AB3 — Strategic LEAP Accumulation

### 11.1 Philosophy

AB3 is the long-duration core bucket. It buys **2-year OTM LEAPs** at deep structural discounts — identified by the LOI oscillator crossing below the accumulation threshold with a confirmed Stage 2 bounce. The 2-year duration provides full cycle runway without expiry pressure, and creates the long leg for the AB2 PMCC income overlay.

Exits are phased — AB3 never tries to pick a top. It trims in 25% tranches as LOI confirms distribution. Baseline allocation: **50% of portfolio** (absorbs former AB2 independent allocation).

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

## 12. AB4 — Capital Reserve & Deployment Ruleset

> **Fully codified 2026-03-05 (Gavin).** This section supersedes all prior AB4 descriptions.

### 12.1 Purpose

AB4 is the yield-bearing capital staging area. It earns income while waiting for LEAP entry signals. All-cash (100% AB4) is a valid posture — no forced deployment ever.

### 12.2 Composition

All of the following count as AB4:
- **STRC** (primary staging vehicle — preferred stock, ~10% annual)
- **STRK** (acceptable alternative)
- **STRF** (acceptable alternative)
- **True cash** (T-bills, money market)

**Hard floor rule:** The 10% hard floor must be satisfied by **true cash only**. Preferreds do not count toward the floor. A portfolio that is 15% STRC + 0% cash is violating the floor.

### 12.3 Boundaries

| Boundary | Value | Type | Notes |
|---|---|---|---|
| Hard floor | 10% | **HARD** | True cash only. Never breached under any circumstance. |
| Hard upper | 100% | **HARD** | All-cash is valid. No forced deployment. |
| Soft upper | 25% | Soft | Target ceiling. Above this = actively seek qualifying deployments. |

### 12.4 STRC as Hurdle Rate

**Capital only leaves AB4 if the expected return on the target position exceeds STRC yield (~0.83%/month).**

This is the single decision rule that governs all deployment. If no open signal clears this bar, stay in STRC. Do not deploy into cash drag.

STRC yield also benchmarks AB2: if monthly call premium available is < 0.83%/month of LEAP cost basis, skip the cycle.

### 12.5 STRC as Regime Signal

STRC price is included in the regime composite score and also interpreted directly:

| STRC Price | Signal | Action |
|---|---|---|
| ≥ $97 | Saylor engine healthy | Full deployment eligible |
| $90–$97 | Stress building | Reduce new AB3 entries |
| < $97 | Credit stress signal | ⚠️ Bearish divergence vs BTC |
| < $90 | Flywheel impaired | Defensive posture, maximize AB4 |

The preferred stock suite (STRC/STRK/STRF) is a **3–7 day leading indicator** for BTC bottoms. Preferred spreads widening (prices dropping) often precede MSTR weakness. Preferred spreads healthy while BTC is weak = bullish divergence.

### 12.6 Staging Flow

```
Free cash (AB4 above hard floor)
    │
    ▼
STRC (default) or STRK (alternative)
    │
    ├─ Stage 1 fires (LOI crosses threshold) ──► Begin gradual STRC reduction
    │                                            Don't wait for Stage 2 — preferred
    │                                            stocks can be thin intraday
    │
    ├─ Stage 2 confirmed ─────────────────────► Execute LEAP buy; STRC proceeds
    │                                            fund the position
    │
    └─ No signal / signal below hurdle ────────► Stay in STRC. Wait.
```

### 12.7 Per-Asset Concentration

**Normal mode (AB4 ≤ 25%):**
- Soft cap: 20% of total portfolio in any single asset across all buckets combined.
- This is a soft constraint — it bends when signal landscape demands.

**Excess cash mode (AB4 > 25%):**
- 20% cap **suspends**.
- Allocate to the best available signal regardless of concentration.
- Concentration is acceptable when the entry is prudent (expected return > hurdle, signal quality confirmed).
- If only one asset is showing an entry, overweight it. The system is not afraid of concentration.
- Cap reinstates once AB4 returns to ≤ 25%.

**The only constraint that never bends:** 10% AB4 hard floor.

### 12.8 Deployment Priority

When multiple signals are active simultaneously:

| Priority | Signal | Sizing |
|---|---|---|
| 1 | AB3 Stage 2 bounce | Full sizing — deploy promptly from STRC |
| 2 | AB1 pre-breakout (CT2+) | Deploy promptly; shorter hold period |
| 3 | AB3 Stage 1 watch | Partial — begin STRC reduction; wait for Stage 2 |
| 4 | AB2 PMCC | No new capital; income overlay only |

---

## 13. Capital Allocation Engine

### 13.1 Baseline Allocation (v3.0)

> **Major change from v2.0:** AB2 no longer consumes independent capital. Its 25% allocation is absorbed into AB3. AB3 is now the dominant bucket.

| Bucket | Purpose | Baseline | Floor | Ceiling |
|---|---|---|---|---|
| AB3 | 2-year LEAP accumulation | **50%** | None | 35% (soft alert) |
| AB1 | Tactical pre-breakout LEAPs | **25%** | None | None |
| AB4 | Yield-bearing cash reserve | **25%** | **10% true cash** | 100% |
| AB2 | PMCC income overlay | **0% additional** | — | — |

### 13.2 AB1 → AB3 Transition

When an AB1 LEAP fails to break out within the failure window:

1. **Trigger:** ST turns negative within 40 bars AND underlying gain < 5%
2. **Action:** Reclassify the LEAP as AB3 (accounting change only — position stays open)
3. **Rationale:** If the LEAP was entered at a genuine structural bottom, the long-term thesis holds even if the short-term breakout failed. No forced close.
4. **Capital flow:** AB1 bucket shrinks; AB3 bucket grows by equivalent amount.
5. **Alert:** If AB3 mark-to-market would exceed 35% ceiling, engine alerts owner for guidance.

### 13.3 AB3 Ceiling Enforcement

- 35% ceiling is **mark-to-market** (not deployment-based) — it accounts for position appreciation
- If AB3 grows past 35% due to price appreciation (e.g., MSTR doubles), an alert fires
- Engine does NOT auto-trim — owner decides whether to rebalance or override
- AB2 call sales continue regardless of ceiling breach (income optimization, no new capital)

### 13.4 Regime Gates

| Regime Score | AB3 New Entries | AB1 | AB2 (PMCC) | AB4 |
|---|---|---|---|---|
| +4 to +7 (RISK-ON) | Full | Full | Full | 10% |
| +2 to +3 (BULL) | Full | Full | Full | Normal |
| 0 to +1 (NEUTRAL) | Full | 75% size | Full | Normal |
| -1 (CAUTIOUS BEAR) | Pause new | 50% size | OTM only (δ≤0.20) | Build |
| ≤ -2 (RISK-OFF) | Existing only | No new | Pause | Max |

AB3 existing positions are **never force-closed** by regime. Only new entries are gated.

### 13.5 Multi-Asset Signal Priority

When multiple AB3 entry signals fire simultaneously:
1. Deepest LOI (most negative = most structurally cheap) gets priority
2. Strongest Stage 2 confirmation (2-bar confirmed bounce with depth filter)
3. GLI alignment (bullish GLI → prefer Momentum assets)

When AB4 is overallocated (> 25%) and no signal clearly dominates, concentrate into the best available signal regardless of diversification.

### 13.6 AB1 Multi-Signal Priority

When multiple AB1 pre-breakout signals fire:
1. Deepest LOI anchor
2. Higher CT confidence score
3. GLI Z-score alignment

### 13.7 AB2 Multi-Asset Priority

All AB3 positions with open gates are PMCC candidates. Sort by:
1. Highest IV / premium relative to LEAP cost basis
2. LOI position (OTM_INCOME zone preferred over DELTA_MGMT for fresh cycles)
3. Avoid writing calls during AB1 signal windows on same asset

### 13.8 Portfolio Independence

Three portfolios tracked fully independently:

| Portfolio | Owner | Capital | Mode |
|---|---|---|---|
| Greg | Greg McKelvey | $5M | Live execution |
| Gavin | Gavin | $1M | Paper trading |
| Gary | Gary | TBD | Educational |

Allocation decisions in one portfolio have zero implications for others.

---

## 13a. SRIBI ROC Derivative

### 13a.1 What It Is

The SRIBI ROC (Rate-of-Change) derivative is a momentum wave added to all four SRIBI indicators. It measures how fast the SRIBI is moving, not just where it is.

**Formula (identical across all four timeframes):**
```python
roc_raw  = bias_score - bias_score[lookback]   # difference, not %
roc_line = EMA(roc_raw, smooth=3)              # 3-bar EMA smoothing
```

**Lookbacks calibrated to each timeframe's natural periodicity:**
| TF | Lookback | Equivalent Period |
|---|---|---|
| VST | 5 bars | 20 hours |
| ST | 6 bars | 24 hours |
| LT | 7 bars | 28 hours |
| VLT | 8 bars | 32 hours |

### 13a.2 Four ROC States

| ROC | SRIBI | State | Meaning |
|---|---|---|---|
| > 0 | > 0 | **Accel Bull** | Momentum building — trend strengthening |
| < 0 | > 0 | **Decel Bull** | Early warning — trend still positive but slowing |
| > 0 | < 0 | ★ **Drag Diffusing** | **Primary bottom signal** — momentum turning before zero cross |
| < 0 | < 0 | **Accel Bear** | Full downside momentum |

### 13a.3 Why Drag Diffusing Matters

Backtest (LT ROC-7, MSTR, 27 cycle bottoms 2022–2026):
- **100% lead rate** at all 27 bottoms — zero lags
- **60–120 hour lead time** before price bottoms
- Correctly maintained "Drag Diffusing" through 4 of 5 false LT flips in Feb 2026

The VLT Drag Diffusing signal is the earliest available bottom detection. When VLT ROC turns positive while VLT SRIBI is still negative, the structural downtrend is losing force. This is the first signal to watch before Stage 1 fires.

### 13a.4 Engine Integration

The Python engine computes ROC columns automatically via `add_sribi_roc_columns(df)` before any analysis. All `scan()` and `current_signal()` outputs include:
- `vst_roc`, `st_roc`, `lt_roc`, `vlt_roc` (float values)
- `vst_roc_state`, `st_roc_state`, `lt_roc_state`, `vlt_roc_state` (string labels)

**Current MSTR state (Feb 27, 2026):**
- LT ROC: +21.72 → **Accel Bull** ✅
- VLT ROC: +3.40 → **Drag Diffusing** ⭐ (VLT still negative — bottom detection active)

---

## 13b. Alert System

### 13b.1 Architecture

The alert system (`pmcc_alerts.py`) runs as Step 5 of the daily pipeline. It compares current PMCC gate states against the previous day's stored states, detects transitions, and fires Discord alerts.

State persistence: `mstr.db` table `pmcc_gate_state`. Every daily run updates the stored state.

### 13b.2 Gate Transition Alerts

| Alert Type | Trigger | Emoji | Color |
|---|---|---|---|
| GATE_OPEN | NO_CALLS → OTM_INCOME | 🟢 | Green |
| GATE_UPGRADE | OTM_INCOME → DELTA_MGMT | 🟠 | Orange |
| GATE_DOWNGRADE | DELTA_MGMT → OTM_INCOME | 🟡 | Yellow |
| GATE_CLOSE | Any → NO_CALLS | 🔴 | Red |
| AB1_PAUSE | Any → PAUSED_AB1 | ⏸️ | Yellow |
| AB1_RESUME | PAUSED_AB1 → any | ▶️ | Varies |

### 13b.3 Position Action Alerts

| Alert Type | Trigger | Emoji |
|---|---|---|
| AB3_BUY | Stage 2 bounce signal (< 48h) | 🎯 |
| AB3_TRIM | Any trim tranche fires (< 48h) | ⚠️ |
| AB1_ENTRY | New pre-breakout signal fires | 🚀 |

Every alert footer includes LT + VLT ROC state for immediate context.

### 13b.4 Daily Embed

The daily engine run posts a gate-state column alongside each asset's LOI and context:
```
MSTR  $129.63  MIXE  LOI=-30.5⚪  S=+10 L=+10 VL=-30  🔴NOCALLS
GLD   $283.10  TAIL  LOI=+23.3🟡  S=+10 L=+10 VL=+30  🟠DELTAMGMT
```

### 13b.5 What Is Not Yet Implemented

- **AB3_WATCH** (Stage 1 zone entry alert) — fires when LOI first crosses below accumulation threshold. Not yet built; only Stage 2 alerts are live.
- **Per-asset concentration check** — checks 20% cap at recommendation time. Planned for trade recommendation layer.

### 13b.6 Alert Log

All alerts are logged to `pmcc_alert_log` table in `mstr.db`:
```sql
SELECT timestamp, asset, alert_type, prev_state, new_state, loi, price, sent
FROM pmcc_alert_log ORDER BY timestamp DESC LIMIT 20;
```

---

## 13c. Market Structure Report (MSR)

### 13c.1 Purpose and Audience

The Market Structure Report is a **weekly standardized report** published for every tracked asset in the universe. It is the objective, shared signal document — identical for all readers. No personal information is included.

MSR is generated by the engine every Monday (or after significant state changes mid-week) and published to the shared Discord channel.

### 13c.2 MSR Structure

Each MSR contains the following fields:

```
MARKET STRUCTURE REPORT — [ASSET] — [DATE]
════════════════════════════════════════════════════════

STAGE DECLARATION
  Current State:        [S4→1 Forming / S2C / etc.]
  Previous State:       [Prior state]
  Bars in State:        [N bars since transition]

CONFIRMATION LADDER
  Tier:                 [Watch / Forming / Confirmed]
  Criteria Met:         [List of passed conditions]
  Criteria Pending:     [List of unmet conditions]
  Invalidation Risk:    [Active threats to current state]

LEAP ATTRACTIVENESS SCORE
  Base Score (Stage):   [0–10]
  Objective Modifiers:  [Applied modifier list with values]
  MSR Score:            [Final objective score]
  Action Threshold:     [Full Entry / Anticipatory / Watch / No Entry]

UPSTREAM CONTEXT
  Howell Phase:         [Season + confidence %]
  GLI Z-Score:          [Value + direction]
  RORO Score:           [Regime score + label]
  Vehicle:              [MSTR / IBIT]

LOI STATE
  Current LOI:          [Value]
  AB3 State:            [NEUTRAL / ACCUMULATING / HOLDING / TRIMMING]
  AB2 Gate:             [NO_CALLS / OTM_INCOME / DELTA_MGMT / PAUSED]

KEY TRIGGERS
  Next Bull Trigger:    [Condition that would upgrade state]
  Next Bear Trigger:    [Condition that would downgrade state]
  Watch Levels:         [Price/LOI levels to monitor this week]

════════════════════════════════════════════════════════
```

### 13c.3 Objectivity Rule

The MSR is **identical for all readers**. It contains no personal portfolio information, no individual account balances, and no Platform Value calculations. The LEAP Attractiveness Score in the MSR reflects only objective modifiers from §8a.3.

MSR content is safe to publish to GitHub under the public-facing brief format.

### 13c.4 MSR vs. Prior Daily Embed

The MSR replaces the prior single-line daily gate state embed (MSTR / LOI / Gate) with a structured weekly report. The daily embed remains active for gate transition alerts. The MSR provides the weekly narrative and conviction context.


---

## 13d. Personalized Portfolio Report (PPR)

### 13d.1 Purpose

The Personalized Portfolio Report is a **private, on-demand, per-user report** generated only in each user's dedicated private Discord channel. It takes the objective MSR analysis and translates it into a personal context — accounting for the user's individual income gap, current positions, cost basis, and personal deployment gate.

### 13d.2 What the PPR Adds (Over MSR)

| Component | Source | MSR | PPR |
|---|---|---|---|
| Stage declaration | Engine | ✅ | ✅ |
| Confirmation ladder | Engine | ✅ | ✅ |
| Objective LEAP score | Engine | ✅ | ✅ |
| **Platform Value modifier** | User data | ❌ | ✅ |
| **Income gap calculation** | User data | ❌ | ✅ |
| **Current position context** | trade_log | ❌ | ✅ |
| **Personal deploy gate** | User config | ❌ | ✅ |
| **Risk/Reward modifier** | User data | ❌ | ✅ |
| **Final personalized score** | Composite | ❌ | ✅ |
| **Specific action recommendation** | Engine + user data | ❌ | ✅ |

### 13d.3 Privacy Rules — NON-NEGOTIABLE

The following rules are permanent and cannot be overridden:

1. **PPR content is never committed to GitHub.** Not in summary form, not in anonymized form.
2. **PPR is only delivered in the user's dedicated private Discord channel.** Cross-channel delivery is prohibited.
3. **PPR reports from one user are never visible to another user.** Channel isolation is enforced at the bot level.
4. **No PPR data is logged to any shared database table.** Personal deployment decisions, account balances, and position details remain in user-private storage only.

### 13d.4 Generating a PPR

PPR generation is **on-demand** — triggered by the user requesting their personal report in their private channel. The engine:

1. Fetches the current MSR for all tracked assets
2. Retrieves user's current positions, cost basis, and monthly income from trade_log (user partition)
3. Calculates income gap: `Target (2%/month) − Current (STRC yield + PMCC yield)`
4. Applies Platform Value modifier to each asset's MSR score
5. Applies Risk/Reward modifier based on existing position cost basis relative to current price
6. Outputs personalized action recommendation (buy / add / hold / trim / skip) with sizing

### 13d.5 PPR Output Format

```
PERSONAL PORTFOLIO REPORT — [USER] — [DATE]
══════════════════════════════════════════════

INCOME ENGINE STATUS
  Current Monthly Yield:   [X.XX%/month]
  Target Monthly Yield:    2.00%/month
  Income Gap:              [X.XX%/month]
  Platform Value Modifier: [+0 / +0.5 / +1.0]

PERSONALIZED SCORES THIS WEEK
  Asset    MSR Score   PV Adj   Final   Action
  MSTR     7           +0.5     7.5     Anticipatory Tranche eligible
  IBIT     5           +0.5     5.5     Watch only
  TSLA     4           +0       4.0     No entry
  [...]

CURRENT POSITIONS
  [Asset / Entry / Cost Basis / Current P&L / Next Action]

THIS WEEK'S RECOMMENDATION
  [Specific action with sizing and rationale]

══════════════════════════════════════════════
PPR is private — do not share outside this channel.
```


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

0. **Layer 0.5 (Howell Phase) Gate Zero** — check phase eligibility for the asset class. If size multiplier = 0%, hard block. Also check IWM Breadth Gate for SPY/QQQ. No downstream evaluation until Gate Zero passes.
1. **Layer 0 (GLI) flag** — "GLI HEADWIND" tag reduces confidence; does not block
2. **Regime gate** — if score ≤ -2, override all entry signals
3. **AB3 deep accumulation (LOI < -80)** — highest priority entry
4. **AB1 pre-breakout** — tactical entry on confirmed Stage 4→1
5. **AB3 accumulation (LOI < acc_thresh)** — standard strategic entry
6. **AB2 PMCC** — call-selling on existing LEAPs in eligible LOI zone
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

---

## 19. P-BEAR Signal Layer: Bearish Top Detection

*(New in v2.4)*

### 19.1 Why SRI Lags at Distribution Tops

The SRI framework excels at identifying accumulation zones — it is built on long-term trend momentum. At **distribution tops**, however, SRI carries a **10–20 bar structural lag**. Distribution unfolds slowly: smart money exits into retail buying, price continues to make new highs while internal market structure quietly deteriorates. SRI trend signals only confirm the reversal *after* it has already propagated into the slow trackline.

**SRI is context at tops, not trigger.** The correct role of SRI during a distribution phase:
- Confirms *that the asset is in the distribution zone* (high LOI, VLT positive, price near or above historical resistance)
- Does NOT trigger the bearish trade — that requires a dedicated detection layer

The **P-BEAR (Protective Bearish) Signal Layer** is that detection layer. It reads leading indicators — momentum divergences, volume divergences, and multi-timeframe RSI behaviour — before the SRI reversal prints.

---

### 19.2 Per-Asset-Class Signal Ladders

Each asset class has a confirmation ladder tuned to how that class typically distributes. The ladders are sequential: higher states require all lower-state conditions to have been met or to still be active.

#### MOMENTUM Class — MSTR, TSLA

Assets with high beta and trending characteristics. MACD histogram is the fastest leading indicator.

```
WATCH        → LOI > +40  (Momentum DELTA_MGMT threshold — watch begins)
FORMING      → MACD histogram < 0  AND  LOI > +20
FORMING_PLUS → RSI 4H bearish divergence confirmed
CONFIRMED    → RSI Daily divergence  +  LOI rolling over (−2 pts from 5-bar peak)
CONFIRMED_PLUS → OBV divergence (tertiary — strongest bearish signal)
INVALIDATED  → MACD histogram > 0  AND  price within 0.2% of 20-bar high
```

Signal priority order: **MACD Hist → RSI 4H div → RSI Daily div + LOI rolling → OBV**

#### BTC_CORRELATED Class — IBIT

Bitcoin-correlated ETF. Volume is the primary leading indicator because on-chain flows front-run price.

```
WATCH        → LOI > +20
FORMING      → OBV divergence (OBV < OBV_SMA20  or  OBV < prior peak)
FORMING_PLUS → RSI 4H divergence also fires
CONFIRMED    → RSI Daily also diverging
INVALIDATED  → OBV recovers above SMA20
```

Signal priority order: **OBV primary → RSI 4H → RSI Daily**

#### MR (Mean Reverting) Class — SPY, QQQ, IWM

Broad market indices revert to trend. RSI 4H divergence is the fastest signal in this class.

```
WATCH        → LOI > +20
FORMING      → RSI 4H bearish divergence
FORMING_PLUS → OBV < OBV_SMA20 (volume confirmation)
CONFIRMED    → RSI Daily divergence also fires
CONFIRMED_PLUS → Weekly StochRSI > 80 (overbought on weekly — strongest for MR assets)
INVALIDATED  → RSI 4H recovers  AND  price within 0.2% of 20-bar high
```

Signal priority order: **RSI 4H div → OBV → RSI Daily → Weekly StochRSI >80 (CONFIRMED_PLUS)**

#### TRENDING Class — GLD

Trend-following commodity. Requires simultaneous evidence from both price-derived and volume-derived indicators before a signal fires, reducing false positives.

```
WATCH        → LOI > +20
FORMING      → OBV divergence  AND  RSI 4H divergence  (simultaneous — both required)
CONFIRMED    → Supertrend flips BEAR (daily Supertrend direction reversal)
INVALIDATED  → Supertrend flips back BULL
```

Signal priority order: **OBV + RSI 4H simultaneously → Supertrend flip**

---

### 19.3 P-BEAR State Machine

The system cycles through seven discrete states per asset:

| Value | State | Description |
|-------|-------|-------------|
| 0 | `INACTIVE` | LOI below watch threshold — no monitoring active |
| 1 | `WATCH` | LOI entered elevated zone — divergence monitoring active |
| 2 | `FORMING` | Primary bearish signal fires per asset class ladder |
| 3 | `FORMING_PLUS` | Secondary signal also confirms |
| 4 | `CONFIRMED` | Dual-timeframe confirmation + LOI rolling — AB2 pause strongly recommended |
| 5 | `CONFIRMED_PLUS` | Tertiary confirmation — strongest signal; hedge entry eligible |
| 6 | `INVALIDATED` | Bearish thesis invalidated — monitoring resets to INACTIVE |

**State persistence:** All states and signal flags are persisted to `pbear_state_log` in `mstr.db`. Alerts fire on *transitions only* — not on every engine run.

---

### 19.4 AB2 Fast-Gate: FORMING → Immediate Call-Selling Pause

When any asset reaches `FORMING` (state ≥ 2), the **AB2 fast-gate** fires immediately:

```
P-BEAR state ≥ FORMING → ab2_fast_gate = True → PMCCGateState.NO_CALLS
```

**This override is unconditional.** Even if LOI is in `OTM_INCOME` or `DELTA_MGMT` range, call-selling halts. The rationale string surfaced in the morning brief gate table:

> `"P-BEAR fast-gate: distribution forming (MSTR)"`

The fast-gate protects against short calls going deep ITM as the underlying reverses from a distribution top. The cost of missing premium is far lower than the cost of an adverse assignment.

---

### 19.5 Watch Thresholds

LOI must enter the watch zone before P-BEAR activates. This prevents false positives during normal accumulation phases where bearish indicator noise is common.

| Asset Class | Assets | Watch LOI Threshold |
|-------------|--------|---------------------|
| MOMENTUM | MSTR, TSLA | LOI > +40 |
| BTC_CORRELATED | IBIT | LOI > +20 |
| MR | SPY, QQQ, IWM | LOI > +20 |
| TRENDING | GLD | LOI > +20 |

**Rationale for MOMENTUM at +40:** The AB2 DELTA_MGMT threshold for MSTR/TSLA is LOI > +40. P-BEAR watch begins precisely at the same level — when LOI signals the asset is entering the distribution trim zone, P-BEAR simultaneously starts monitoring for the structural signals that confirm top-formation.

---

### 19.6 Alert Codes

| Code | Trigger | Severity |
|------|---------|----------|
| `PBEAR_WATCH` | INACTIVE → WATCH | 🟡 Yellow — monitor |
| `PBEAR_FORMING` | any → FORMING or FORMING_PLUS | 🟠 Orange — **stop writing new short calls** |
| `PBEAR_CONFIRMED` | any → CONFIRMED or CONFIRMED_PLUS | 🔴 Red — **evaluate hedge entry; close existing short calls** |
| `PBEAR_INVALIDATED` | FORMING+/CONFIRMED+ → INVALIDATED | ✅ Green — resume normal AB2 protocol |

---

## 20. Portfolio Defensive Posture (P-BEAR Phase 2)

*(New in v2.4)*

### 20.1 PortfolioPosture Levels

Phase 2 synthesises per-asset P-BEAR signals into a single **portfolio-level posture**. Four levels are defined:

| Level | Ordinal | Trigger Condition |
|-------|---------|------------------|
| 🟢 NORMAL | 0 | No asset at FORMING or above |
| 🟡 CAUTIOUS | 1 | 1+ assets at FORMING |
| 🟠 DEFENSIVE | 2 | 2+ assets FORMING **OR** 1+ asset CONFIRMED |
| 🔴 MAX_DEFENSIVE | 3 | 2+ assets CONFIRMED **OR** any asset CONFIRMED_PLUS |

The posture is computed on every engine run and persisted to `defensive_posture_log` in `mstr.db`.

---

### 20.2 Per-Level Rules

#### 🟢 NORMAL
- Standard allocation. AB2 call-selling allowed per LOI gate.
- No distribution signals detected across tracked assets.
- AB4 floor: **10%** (standard AGENTS.md floor)
- AB3 new entries: **✅ allowed**
- Expression 3 eligibility: **⬜ no**

#### 🟡 CAUTIOUS
- AB2 paused on affected asset(s) via fast-gate (propagated through `gate_state()`).
- No capital reallocation required — the gate is the sufficient response.
- AB4 floor: **10%** (unchanged)
- AB3 new entries: **✅ allowed** (unaffected assets only)
- Expression 3 eligibility: **⬜ no**
- Morning brief: Affected asset names logged with rationale.

#### 🟠 DEFENSIVE
- AB4 floor rises to **15%** hard (overrides AGENTS.md 10% default for duration of posture).
- No new AB3 entries on **any** asset regardless of LOI signal — dry powder preservation.
- Existing AB2 positions under review: do not roll or extend.
- Expression 3 eligibility: **⬜ no** — not yet at max confirmation.
- The 10% true-cash-only requirement remains in force inside the 15% override.

#### 🔴 MAX_DEFENSIVE
- AB4 floor rises to **20%** hard.
- Begin reducing AB3 positions on confirmed assets.
- No new AB3 or AB2 anywhere in the portfolio.
- Expression 3 trade entry **eligible** (all 4 independent conditions still required — eligibility is not activation).
- The 10% true-cash-only floor remains in force inside the 20% override.

| Posture | AB4 Floor | AB3 New Entries | Expression 3 |
|---------|-----------|-----------------|--------------|
| NORMAL | 10% | ✅ yes | ⬜ no |
| CAUTIOUS | 10% | ✅ yes | ⬜ no |
| DEFENSIVE | 15% | 🚫 halt | ⬜ no |
| MAX_DEFENSIVE | 20% | 🚫 halt | ✅ eligible |

---

### 20.3 Expression 3 — Bearish mNAV Contraction Hedge

Expression 3 is a specific hedging trade that profits from MSTR's premium to NAV (mNAV) compressing toward fair value during a broad distribution cycle.

**Trade structure:** Long MSTR debit put spread (ATM/OTM 20–25%, 90–120 DTE) + Long IBIT  
**Net exposure:** Long mNAV contraction — profits from MSTR premium compression regardless of BTC direction  
**Sizing:** MSTR put spread notional 1.5–2.0× IBIT dollar equivalent

**ALL 4 conditions required for ARMED status:**

| # | Condition | Threshold | Logic |
|---|-----------|-----------|-------|
| 1 | mNAV > 2.0× | MSTR market cap / (717,130 BTC × BTC price) | Premium is elevated enough to justify compression bet |
| 2 | MSTR P-BEAR ≥ FORMING | Distribution signal active | Asset-level confirmation of top-formation |
| 3 | Howell Phase ∈ {Speculation, Turbulence} | GLI deteriorating | Macro season supports broad risk-off |
| 4 | BTC LT SRIBI rolling over | current LT < max(prior 5 bars) − 5 pts | BTC structural weakness confirmed |

**Alert levels:**

| Conditions Met | Level | Alert Code |
|----------------|-------|-----------|
| 4/4 | ARMED 🚨 | `EXPRESSION3_ARMED` |
| 3/4 | SETUP 🟠 | `EXPRESSION3_SETUP` |
| 2/4 | WATCH 👁 | (informational only — no alert fires) |
| 0–1/4 | INACTIVE ⚪ | (no alert) |

Alerts fire on **level transitions only**.

---

### 20.4 Current mNAV Context — Expression 3 Not Near Triggering

As of 2026-03-03, mNAV ≈ **0.91×**.

Expression 3 requires mNAV > **2.0×** as its first condition. At 0.91×, MSTR is trading *below* its BTC NAV — the opposite of a premium compression scenario. This condition is not close to being met under current market structure.

Current Expression 3 status: **👁 WATCH (2/4 conditions)**:
- ✅ Howell Phase: Turbulence (condition 3 met)
- ✅ BTC LT SRIBI rolling over (condition 4 met)
- ❌ mNAV 0.91× — need >2.0× (condition 1 not met)
- ❌ MSTR P-BEAR INACTIVE — no distribution signal (condition 2 not met)

**Practical implication:** Expression 3 is a late-bull-cycle tool. It becomes relevant when MSTR is trading at 2× or more above its BTC holdings value — a situation that last occurred in late 2024 and early 2021. In the current accumulation-phase environment (MSTR in deep negative LOI, BTC in structural downtrend), this trade is not on the radar.

---

### 20.5 Alert Codes — Portfolio Posture

| Code | Trigger | Color |
|------|---------|-------|
| `PORTFOLIO_POSTURE_CHANGE` | Any posture level transition | 🟡 CAUTIOUS / 🔴 DEFENSIVE+ |
| `EXPRESSION3_SETUP` | Expression 3 reaches 3/4 conditions | 🟠 |
| `EXPRESSION3_ARMED` | Expression 3 reaches 4/4 conditions | 🔴 |


---

## 21. Liquidity Regime and Timeframe Signal Weighting

*(New in v2.5 — 2026-03-03 backtest insight)*

### 21.1 The Fundamental Insight

Liquidity conditions modulate which timeframe carries the most predictive signal. This is not a static property of the indicators — it changes with the liquidity cycle.

**Mechanism:**
- **Expanding liquidity** (central bank balance sheets expanding, credit spreads tightening) → trend momentum is sustained longer. Short-timeframe signals (VST/ST) fire earlier and carry further before mean-reversion kicks in. Momentum lasts because central bank flows keep the environment supportive.
- **Contracting liquidity** (balance sheets shrinking, credit spreads widening) → mean-reversion dominates. Short-timeframe signals fire prematurely and fade quickly. Longer-timeframe signals (LT/VLT) are more reliable because they smooth through the volatility of liquidity withdrawal.

**ST is the all-weather timeframe.** Across both regimes, ST (4H/Daily) shows the most consistent accuracy — it is least sensitive to liquidity regime. It is the reliable monitoring signal in all conditions.

### 21.2 Regime × Timeframe Table

| Liquidity Regime | Most Accurate TF | AB3 Deployment Rule | Proxy Signal |
|---|---|---|---|
| EXPANDING | VST/ST | Standard LOI threshold applies | HYG SRIBI > 0, VIX LOI < 0 |
| CONTRACTING | LT/VLT | Require LT/VLT confirmation before deployment | HYG SRIBI < 0, VIX LOI > 0 |
| NEUTRAL | ST (all-weather) | Standard rules | Neither condition met |

**Current regime (2026-03-03): CONTRACTING**
- HYG SRIBI: -35 (credit stress — negative)
- VIX LOI: +41.8 (elevated vol — positive)
- → Require LT/VLT confirmation before any AB3 LEAP deployment

### 21.3 Operational Rules by Regime

**EXPANDING regime:**
- VST/ST signals carry elevated weight in AB3 entry decisions
- Standard LOI accumulation thresholds apply (MSTR/TSLA/IBIT: -45; SPY/QQQ/GLD/IWM: -40)
- AB2: standard call-selling gates; full income harvesting
- SRI Agent: weight VST and ST SRIBI components higher in LOI composite

**CONTRACTING regime:**
- LT and VLT confirmation **required** before AB3 capital deployment (AGENTS.md rule)
- ST serves as monitoring signal only — triggers awareness, not deployment
- AB2: defer call-selling increases until LT/VLT upward momentum confirmed
- SRI Agent: weight LT and VLT SRIBI components higher in LOI composite
- Options Strategist: defer PMCC call-selling increases until LT/VLT aligns

**NEUTRAL regime:**
- Balanced TF weighting — no adjustment to standard rules
- ST is the operational signal as usual

### 21.4 Vol-Adaptive LOI Threshold Formula

Fixed LOI thresholds misfire in low-volatility regimes. HIGH vol entries produce dramatically better outcomes than LOW vol entries.

**Backtest evidence:**
- MSTR: HIGH vol entries → +26.3% median 60-bar return
- MSTR: LOW vol entries → -26.8% median 60-bar return
- MSTR fixed threshold (-45): 3 signals / **0% accuracy**
- MSTR adaptive threshold: 1 signal / **100% accuracy** / +12.2% return

**Why this works:** Low-vol environments produce shallow LOI dips that quickly reverse (head-fakes). High-vol drawdowns produce genuine accumulation opportunities with actual structural bottoms. The adaptive formula normalizes the threshold to the current vol regime.

**Formula:**
```
threshold = base_threshold × (median_ATR_ratio / current_ATR_ratio)
Capped at: base × 0.6 (min compression) to base × 1.3 (max expansion)

Where:
  ATR_ratio        = ATR(14) / Close  (vol normalized by price)
  median_ATR_ratio = SMA(ATR_ratio, 200)  (long-run average vol)
  vol_multiplier   = median_ATR_ratio / current_ATR_ratio
```

**Intuition:** When current vol is HIGH relative to historical (current_ATR_ratio > median), the multiplier < 1, which compresses the threshold closer to zero — easier to trigger. When vol is LOW, multiplier > 1, which pushes threshold deeper negative — harder to trigger. This exactly matches the empirical finding.

**Pearson r (ATR/Close vs LOI depth at threshold crossings):**
| Asset | r | p-value |
|---|---|---|
| MSTR | -0.383 | 0.012* |
| TSLA | -0.801 | <0.001*** |
| SPY  | -0.967 | <0.001*** |

Note: the relationship is **inverted** from the naive hypothesis — high vol produces MORE negative LOI troughs (not less), but the adaptive formula is still valid and outperforms fixed thresholds.

**Asset class application:**
- MOMENTUM/BTC_CORRELATED (MSTR, TSLA, IBIT): adaptive threshold (live-computed by AdaptiveLOIEngine in sri_engine.py)
- MR/TRENDING (SPY, QQQ, IWM, GLD): flat -40 (MR assets already have lower thresholds; vol-adaptive formula less impactful given their lower vol baseline)

### 21.5 Current State Example (CONTRACTING, 2026-03-03)

```
Liquidity Regime: CONTRACTING
HYG SRIBI:  -35   (credit stress)
VIX LOI:   +41.8  (elevated fear)

Active Rules:
  → LT/VLT confirmation required before AB3 deployment
  → AB2 call-selling: defer increases until LT/VLT momentum confirmed
  → ST SRIBI: monitoring signal only; do not deploy on ST signal alone

Sample Adaptive Thresholds:
  MSTR: vol NORMAL  | base -45.0 | adaptive ~-41 to -50 depending on ATR
  TSLA: vol LOW     | base -45.0 | adaptive pushes deeper (~-55 to -65)
  IBIT: vol NORMAL  | base -45.0 | adaptive ~-41 to -50
```

### 21.6 Validation Caveat

**This is an UNVALIDATED insight from a 15-month dataset (Jul 2024 – Oct 2025).**

- Sample sizes are small (n=4 to n=11 per cell)
- Statistical certainty requires 24+ months of data across multiple liquidity cycles
- Current finding: directional confidence only
- **Re-validate at 24+ months (target: Jul 2026)**

The adaptive threshold statistical significance (p<0.05 on MSTR, p<0.001 on TSLA/SPY) is stronger than the liquidity-TF accuracy finding. Both should be treated as directional guidance, not definitive parameters, until validated on a larger dataset.

**Do not use these findings to override core framework rules with high conviction. Use them as probability adjusters — exactly as GLI Z-score adjusts regime calls.**


---

## Appendix A: Decision Tree — New Trade

```
Incoming signal on asset X:

0a. Check Layer 0.5 (Howell Phase — Gate Zero):
   - What is current phase? (Rebound/Calm/Speculation/Turbulence)
   - Is this asset class eligible? (see §6b.3 table)
   - If size multiplier = 0% → HARD BLOCK. Stop. Do not evaluate further.
   - If SPY or QQQ: check IWM breadth state at trough
     IWM headwind (LT<0 AND VLT<0)? → proceed
     IWM neutral/bull? → BREADTH_DIVERGENCE → HARD BLOCK
   - If eligible: apply phase size multiplier to final position size

0b. Check Layer 0 (GLI):
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
| Howell Phase | One of four macro cycle phases (Rebound/Calm/Speculation/Turbulence) derived from sector ETF LT SRIBI states |
| Gate Zero | Howell Phase eligibility check — first filter before CPS, episode type, or VLT clock |
| BREADTH_DIVERGENCE | Signal when IWM is neutral/bull while SPY/QQQ corrects — marks Speculation-phase top; 10–13% continuation |
| HOWELL_PHASE_TRANSITION | Discord alert fired when Howell Phase changes — primary AB3 Beta entry trigger |
| GRID | 42 Macro growth/inflation regime matrix (Goldilocks/Reflation/Stagflation/Deflation) |
| Paradigm | 42 Macro multi-year monetary cycle phase (A=tighten, B=cut, C=largesse) |
| KISS | 42 Macro model portfolio — binary long/short signals by asset class |
| Dr. Mo | 42 Macro momentum confirmation model — validates KISS portfolio direction |
| RMOP | Reserve Management and Operations Program — Fed QT mechanism |
| SLR | Supplementary Leverage Ratio — bank capital rule; reduction = liquidity expansion |
| Stage State | One of 10 operational states (S1, S1→2, S2, S2C, S2→3, S3, S3→4, S4, S4C, S4→1) derived from the four classic Wyckoff stages |
| Confirmation Ladder | Three-tier progression (Watch → Forming → Confirmed) for each state transition, with explicit Invalidation conditions |
| LEAP Attractiveness Score | 0–10 composite rating combining stage state base score and objective modifiers; published in every MSR |
| Anticipatory Tranche | 25% early partial AB3 position eligible when LEAP Attractiveness Score is 6–7 and Platform Value modifier is active |
| MSR | Market Structure Report — weekly objective per-asset report including stage state, confirmation ladder, LEAP score, upstream context |
| PPR | Personalized Portfolio Report — private per-user on-demand report applying Platform Value modifier to MSR data; never shared or committed to GitHub |
| Platform Value Modifier | Personal income gap adjustment (+0 to +1.0) applied only in PPR; reflects gap between target 2%/month yield and current portfolio income |
| CPS | Confirmation Point Score — composite score measuring multi-timeframe structural agreement at key transitions |
| STH-MVRV | Short-Term Holder Market Value to Realized Value — on-chain metric; below 1.0 signals capitulation |

---

*Tutorial v2.3 reflects engine state as of 2026-03-03. Added: Stage State Taxonomy (§3a), Confirmation Ladders (§3b), LEAP Attractiveness Score (§8a), Market Structure Report (§13c), Personalized Portfolio Report (§13d).*

*Tutorial v2.4 reflects engine state as of 2026-03-03. Added: P-BEAR Signal Layer: Bearish Top Detection (§19), Portfolio Defensive Posture / P-BEAR Phase 2 (§20).*

*Tutorial v2.5 reflects engine state as of 2026-03-04. Added: Liquidity Regime and Timeframe Signal Weighting (§21) — vol-adaptive LOI thresholds, liquidity cycle × TF accuracy, CONTRACTING regime deployment rules. UNVALIDATED — 15-month dataset; re-validate at 24+ months.*
