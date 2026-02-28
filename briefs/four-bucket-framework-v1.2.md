# Four-Bucket Investment Framework
**Version:** 1.2.1 | **Date:** 2026-02-26
**Authors:** Gavin (SRI methodology, indicator architecture, RORO concept), CIO (backtesting, options structure)
**Status:** Draft v1.2.1 — Added RORO × BTC Cycle anchored allocation map, P1+C1 trap rule

---

## Executive Summary

This framework organizes all capital into four buckets with distinct time horizons, instruments, and signal sources. Three key innovations:

1. **Asymmetric signal architecture:** Bullish and bearish signals use different indicator systems
2. **RORO Capital Rotation Framework:** Cross-asset SRI breadth determines which phase of the capital rotation cycle we're in — and which buckets to emphasize
3. **STRC as cost-of-capital benchmark:** Every Bucket 1 and 2 trade must clear STRC's yield (~10% annualized) to justify deploying capital

```
┌──────────────────────────────────────────────────────────────────┐
│                    SIGNAL ARCHITECTURE                            │
│                                                                  │
│  BULLISH ENGINE: SRI Confirmation Ladder                         │
│  (FTL/STL crossover → robust fit speed → retest → red cross)    │
│                                                                  │
│  BEARISH ENGINE: SOPR + STRS                                     │
│  (SOPR < -0.2 trigger + STRS falling fast confirmation)          │
│                                                                  │
│  REGIME ENGINE: RORO Capital Rotation                            │
│  (Cross-asset SRI breadth → 5-phase rotation → bucket emphasis)  │
│                                                                  │
│  COST-OF-CAPITAL: STRC Benchmark                                 │
│  (Every trade must beat ~0.83%/month or capital stays in STRC)   │
├────────────┬───────────────┬──────────────┬──────────────────────┤
│  BUCKET 1  │   BUCKET 2    │   BUCKET 3   │    BUCKET 4          │
│ Directional│ Spread Income │    LEAPs     │ Cash (STRC) & Alts   │
│ Days-Weeks │  Quarterly    │  6-18 Mo     │ Always Active         │
│ IBIT       │  MSTR         │  MSTR/IBIT   │ STRC + Alternatives  │
└────────────┴───────────────┴──────────────┴──────────────────────┘
```

---

## Part 1: The Signal Layer

### 1A. Bullish Engine — SRI Confirmation Ladder

The SRI framework is structurally biased toward identifying bullish setups. This is by design — it detects Wyckoff accumulation-to-markup transitions. Backtested across 1,300 daily rows and 1,247 4H rows of MSTR, plus 1,650 daily rows of BTC.

**The 7-Step Confirmation Ladder:**

| Step | Event | Avg Timing | Significance |
|---|---|---|---|
| 1 | Green resistance line gaps / FTL approaches STL | Day 0 | First reversal attempt |
| 2 | Price overtakes STL | Day 0-3 | Price leads indicators |
| 3 | FTL turns green, slopes up | Day 1-5 | Momentum shifting |
| 4 | **FTL crosses above STL** | Day 3-10 | **Primary signal — start the clock** |
| 5 | **Price retests STL as support** | Day 5-13 | **Retest: hold/fail determines everything** |
| 6 | **Robust fit crosses STL** | Day 7-20 | **Speed = signal quality** |
| 7 | Red support line overtakes STL | Day 15-40+ | **Take-profit signal** |

**The Three Discriminators (backtested):**

**1. Robust Fit Speed — THE primary discriminator**

| Speed | Classification | 4H: 20d Avg Return | Win Rate | Action |
|---|---|---|---|---|
| ≤5 days | FAST — genuine | +16.6% to +36.7% | 63-80% | Go long |
| 5-10 days | MODERATE | +10-15% | ~55% | Reduce bearish, wait |
| >10 days | SLOW — trap | -6% to -12% | <50% | Sell the rip |

**2. Retest Outcome (4H data, n=10)**

| Result | 20d Avg Return | Action |
|---|---|---|
| **Held** (within 3% of STL) | **+36.7%** | Confirm longs |
| **Failed** (closes >3% below) | **-6.2%** | Close longs, treat as trap |

**3. Red Line Cross = Exit Signal (daily data)**

Average price move at red cross: **+13.6%** (range -6% to +28%). After the red cross, returns flatten or reverse.

**MVRV Quality Filter:**

| MVRV at Cross | Quality | Evidence |
|---|---|---|
| < 1.0 | **Highest** | Jan 2023 +44%, Sep 2024 +158% |
| 1.0 - 1.5 | Good | Standard recovery |
| 1.5 - 2.0 | Caution | Could be bear rally |
| > 2.0 | **Dangerous** | Apr 2021 MVRV 2.57 → -45% in 30d |

**Current MVRV: 0.50 — the most favorable in the entire dataset.**

**VL Timeframe Rule:**
- At extreme readings (record Stage 4, deep MVRV): shorter TFs lead, VL lags by definition
- Buckets 1 and 2 do NOT require VL confirmation
- Bucket 3 (LEAPs) requires either VL confirmation OR P1_EARLY + MVRV < 0.8 (see revised LEAP triggers)

### 1B. Bearish Engine — SOPR + STRS

The SRI does not reliably identify bearish setups. FTL crossing *below* STL is actually a contra-indicator (price goes UP 67% of the time at 5 days). The bearish engine uses different indicators.

**Primary Trigger: STH-SOPR (Mirrored) < -0.2**

| Horizon | Avg Return | Bear Win Rate | Sample |
|---|---|---|---|
| 5 days | **-10.7%** | **100% (7/7)** | MSTR Daily |
| 10 days | -12.6% | 71% | |
| 20 days | -13.2% | 71% | |
| 30 days | **-14.8%** | **86%** | |

**Confirmation: STRS (Short-Term Risk Score) Falling Fast**

STRS dropping >0.10 in 5 days: 83% bear at 20d (n=6).

**STRS Context (regime indicator):**

| STRS Level | Interpretation |
|---|---|
| > 0.55 | Overheated — vulnerable to shock |
| 0.35 - 0.50 | Healthy — normal risk environment |
| 0.25 - 0.35 | Cooling — declining risk appetite |
| < 0.25 | Exhausted — selloff late-stage, look elsewhere |

**Bearish Signal Tiers:**

| Tier | Conditions | Action |
|---|---|---|
| **1 — Full Bearish** | SOPR < -0.2 + STRS was >0.45 recently & falling + MVRV >1.5 | Buy IBIT puts |
| **2 — Defensive** | SOPR < -0.1 + STRS declining from >0.40 | Close bullish spreads, tighten stops |
| **3 — Watch** | Risk Osc < -0.15 on BTC | Flag but don't trade |

### 1C. Preferred Stock Integration (All Signals)

| Signal | Meaning | Action |
|---|---|---|
| STRC > $97, STRF > $97 | Credit healthy | Bullish signals confirmed |
| STRC < $97 | Credit stress | **Close all bullish positions** |
| STRF < $97 | Severe stress | **Close all positions + add puts** |
| STRK > $85 with volume | Recovery priced | Stage 1 confirmation candidate |
| Credit healthy + equity falling | Bullish divergence | Tier 1 long signal |

**SCHI Composite:** (STRF premium × 0.4) + (STRC premium × 0.3) + (STRK premium × 0.3)

---

## Part 2: RORO Capital Rotation Framework

### 2A. The Core Concept

Capital does not flip binary between "risk-on" and "risk-off." It flows through asset classes in a **sequence** driven by investor risk appetite. The RORO framework uses SRI breadth across 13 assets to detect which phase of this rotation we're in — and which buckets to emphasize.

This is Howell's liquidity cycle research translated into SRI language: liquidity enters safety assets first, then flows progressively down the risk curve.

### 2B. Asset Tiers

Assets are organized into four tiers reflecting their position in the capital rotation sequence:

| Tier | Assets | Role in Rotation |
|---|---|---|
| **T1 — Safety** | TLT, GLD, BIL | First to receive capital in risk-off; first to lose it in risk-on |
| **T2 — Quality** | SPY, QQQ, XLP | Second wave — capital broadens into large-cap equity |
| **T3 — Risk** | BTC, IBIT, XLY | Third wave — risk appetite expanding to volatile assets |
| **T4 — Speculative** | MSTR, TSLA | Last to receive capital; highest beta, highest reward |

### 2C. The Five Rotation Phases

Each phase is defined by the SRI state (SRIBI) of Safety and Risk tiers:

| Phase | Safety SRIBI | Quality SRIBI | Risk SRIBI | Meaning |
|---|---|---|---|---|
| **P1 — EARLY CYCLE** | ✅ Bullish (>+10) | Mixed | ❌ Bearish (<-10) | Capital hiding in safety. Risk assets bottoming. |
| **P2 — BROADENING** | ✅ Bullish | ✅ Bullish | Weak/Mixed | Capital moving out the risk curve |
| **P3 — RISK-ON** | Any | ✅ Bullish | ✅ Bullish | Full risk appetite. Best BTC/MSTR returns. |
| **P4 — LATE CYCLE** | ❌ Bearish | Any | ✅ Bullish | Safety leaving; risk still euphoric. Distribution. |
| **P5 — FULL RISK-OFF** | ❌ Bearish | Any | ❌ Bearish | Everything hit. Maximum fear. |

**P0 — MIXED:** When conditions don't cleanly fit a phase. ~53% of days. No rotation signal.

### 2D. RORO Backtest Results (3,728 days, 2011–2026)

**Phase Distribution:**

| Phase | Days | % of Total |
|---|---|---|
| P0 Mixed | 1,898 | 53.1% |
| P1 Early | 257 | 7.2% |
| P2 Broadening | 148 | 4.1% |
| P3 Risk-On | 1,029 | 28.8% |
| P4 Late | 96 | 2.7% |
| P5 Full Risk-Off | 148 | 4.1% |

**BTC Forward Returns by Phase:**

| Phase | 5d | 20d | 40d | 60d | 60d Bull% |
|---|---|---|---|---|---|
| P1 Early | -0.2% | -0.3% | +2.8% | +7.7% | 60% |
| P2 Broadening | +0.8% | +2.4% | +7.8% | +10.0% | 61% |
| **P3 Risk-On** | **+3.0%** | **+13.1%** | **+24.5%** | **+35.2%** | **59%** |
| P4 Late | +2.0% | +9.5% | +23.6% | +35.4% | 63% |
| P5 Full Risk-Off | -0.6% | -0.2% | +5.3% | +9.2% | 57% |

**MSTR Forward Returns by Phase (note the difference):**

| Phase | 10d | 20d | 40d | 40d Bull% |
|---|---|---|---|---|
| **P1 Early** | **+2.3%** | **+4.6%** | **+8.1%** | **68%** |
| P2 Broadening | -0.8% | +1.8% | +17.5% | 51% |
| P3 Risk-On | +2.3% | +3.5% | +5.6% | 44% |
| P5 Full Risk-Off | +2.7% | +5.6% | +9.8% | 68% |

**Key insight: MSTR mean-reverts in P1_EARLY and P5_RISK_OFF.** Its beta works in reverse — oversold MSTR in fearful regimes snaps back harder than BTC. This confirms MSTR as a Bucket 2 (spread) vehicle, not Bucket 1 (directional).

### 2E. The P1_EARLY + BTC Bottoming Combo

When P1_EARLY coincides with deeply negative BTC SRIBI (< -40), we are in historically significant bottoming zones. **44 instances in the dataset.**

Notable instances: Jan 2015 ($182-$288), Nov 2018 ($3,349-$4,544), Mar 2020 ($6,406-$7,933), Nov 2022 ($15,761-$16,992), **Feb 2026 ($64,081-$67,636 — current).**

| Horizon | Avg Return | Bull% | Worst | Best |
|---|---|---|---|---|
| 5d | -2.9% | 48% | -34.9% | +18.8% |
| 20d | +0.04% | 49% | -26.3% | +25.3% |
| 40d | +2.6% | 57% | -19.1% | +48.9% |
| 60d | +6.4% | 62% | -26.5% | +57.6% |

**Interpretation:** Near-term is choppy and unreliable (coin flip at 5-20d). But the 40-60d horizon turns meaningfully positive. This is the accumulation zone — not the deployment zone for short-term directional.

### 2F. SRIBI Breadth Composite (Continuous RORO Score)

In addition to the discrete 5-phase classification, we compute a continuous RORO score:

**RORO Score = Risk-On avg SRIBI − Risk-Off avg SRIBI**

| Percentile | Score | Regime |
|---|---|---|
| < 20th | < -14.8 | Strong Risk-Off |
| 20th-40th | -14.8 to +0.5 | Lean Risk-Off |
| 40th-60th | +0.5 to +10.5 | Neutral |
| 60th-80th | +10.5 to +20.8 | Lean Risk-On |
| > 80th | > +20.8 | Strong Risk-On |

**BTC 20d forward by RORO quintile (monotonic edge):**

| Quintile | Avg Return | Bull% |
|---|---|---|
| Q1 (Strong RF) | +0.9% | 52% |
| Q2 (Lean RF) | +2.1% | 51% |
| Q3 (Neutral) | +3.6% | 54% |
| Q4 (Lean RO) | +9.8% | 60% |
| **Q5 (Strong RO)** | **+12.6%** | **62%** |

Q5 vs Q1 spread at 20d: **+11.7%.** This is a tradeable edge.

### 2G. Phase Transition Sequencing

P1_EARLY historically transitions to:
- P0_MIXED (most common — rotation stalls or reverses)
- P5_FULL_RISK_OFF (risk-off deepens — the "it gets worse" scenario)
- P2_BROADENING (capital starts flowing to quality — the bullish resolution)

**The trigger to watch:** Quality tier (SPY/QQQ) SRIBI turning bullish while Safety remains bullish. That's the P1→P2 transition — the signal that capital is moving down the risk curve.

### 2H. RORO × BTC Cycle Anchored Map

BTC's SRI stage transitions don't fire reliably in the data (the indicator was calibrated for equities). Instead, we define BTC cycle phases using FTL/STL position + SRIBI:

| BTC Cycle Phase | Definition | % of Days |
|---|---|---|
| **C4_MARKDOWN** | FTL < STL, SRIBI < -20 | 14% |
| **C4→1_ACCUM** | FTL < STL, SRIBI ≥ -20 and < +10 | 14% |
| **C1_EARLY_MARKUP** | FTL > STL, SRIBI < +10 | 22% |
| **C2_MARKUP** | FTL > STL, SRIBI ≥ +10, rising | 23% |
| **C2_MATURE** | FTL > STL, SRIBI ≥ +10, fading | 14% |
| **C3_DISTRIBUTION** | FTL < STL, SRIBI ≥ +10 | 13% |

**Co-occurrence: RORO Phase → Most Likely BTC Cycle**

| RORO Phase | BTC Cycle (dominant) | BTC FTL>STL |
|---|---|---|
| P5 Full Risk-Off | C4 Markdown (52%) | 27% |
| P1 Early | C4 Markdown (44%) + C1 Early (37%) — **bifurcated** | 37% |
| P2 Broadening | C1 Early Markup (49%) | 66% |
| P3 Risk-On | C2 Markup (48%) + C2 Mature (26%) | 79% |
| P4 Late | C2 Markup (60%) + C2 Mature (23%) | 84% |

**The Expected Cycle Progression:**

```
P1 + C4_MARKDOWN   ←— WE ARE HERE
  ↓ SRIBI improves toward 0
P1 + C4→1_ACCUM    (40d: +13.3% — best P1 state. Scale Bucket 3 Path B.)
  ↓ FTL crosses STL
P1 + C1_EARLY      (40d: -4.2% — ⚠️ TRAP ZONE. Do NOT deploy Bucket 1.)
  ↓ Quality SRIBI crosses +10
P2 + C1_EARLY      (40d: +8.2% — Broadening confirmed. Bucket 1 pilot.)
  ↓ BTC SRIBI turns positive
P3 + C2_MARKUP     (40d: +35.4% — THE MONEY ZONE. Maximum deployment.)
  ↓ Safety SRIBI turns negative
P4 + C2_MARKUP     (40d: +31.9% — Late but still good. Start taking profits.)
  ↓ BTC FTL crosses below STL
P4 + C3_DISTRIB    (40d: -14.2% — EXIT SIGNAL. Close everything.)
  ↓ Everything sells
P5 + C4_MARKDOWN   (Full risk-off. Cycle resets.)
```

### 2I. Anchored Allocation Table: RORO × BTC Cycle → Buckets

This is the master allocation table. It replaces the single-axis stage-based allocations with a two-dimensional map anchored to both cross-asset rotation (RORO) and individual asset cycle position (BTC Cycle).

| RORO | BTC Cycle | B1 Direct. | B2 Spreads | B3 LEAPs | B4 STRC | Key Rule |
|---|---|---|---|---|---|---|
| **P1** | **C4 Markdown** | **0%** | **15-20%** | **5-8%** | **72-80%** | **← CURRENT POSITION** |
| P1 | C4→1 Accum | 0% | 15-20% | 8-12% | 68-77% | SRIBI improving → scale B3 |
| P1 | C1 Early | **0%** | 15-20% | hold | hold | **⚠️ TRAP — do NOT add B1** |
| P2 | C4→1 Accum | 5-10% | 15-20% | 12-18% | 52-68% | Pilot B1, scale B3 |
| P2 | C1 Early | 10-15% | 15-20% | 15-20% | 45-60% | Broadening confirmed |
| **P3** | **C2 Markup** | **15-20%** | **20-25%** | **25-35%** | **20-40%** | **MAXIMUM DEPLOYMENT** |
| P3 | C2 Mature | 10-15% | 20-25% | 25-30% | 30-45% | Hold, tighten stops |
| P3 | C3 Distrib. | 5% (puts) | 10-15% | close 50% | 30-80% | Begin exit |
| P4 | C2 Markup | 5-10% | 15-20% | take profits | 55-70% | Late — harvest |
| **P4** | **C3 Distrib.** | **10-15% (puts)** | **5-10%** | **close all** | **65-80%** | **EXIT SIGNAL** |
| P5 | C4 Markdown | 0% | 5-10% | 0% | 85-95% | Maximum STRC |

### 2J. The P1+C1 Trap Rule (CRITICAL)

**Never deploy Bucket 1 directional when RORO and BTC cycle disagree.**

When BTC's FTL crosses above STL (C1_EARLY_MARKUP) but RORO is still P1_EARLY, the 40-day forward return is **-4.2%** (n=92). The bullish SRI signals are real accumulation signals — they are correct about the *condition* but wrong about the *timing*. The markup doesn't begin until capital flows down the risk curve (RORO P2→P3).

**What survives the trap:**
- Bucket 3 Path B LEAPs (12-18mo DTE) — long enough to ride through chop
- Bucket 2 spreads — MSTR mean-reversion works in P1
- STRC — 10% yield while waiting

**What gets killed:**
- Bucket 1 short-dated calls (30-45 DTE) — directional into P1+C1 is where capital dies

**The gate for Bucket 1:** RORO Phase ≥ P2 (Quality SRIBI > +10 while Safety stays bullish). This single rule avoids every false start in the dataset.

---

## Part 3: STRC Cost-of-Capital Benchmark

### 3A. The Principle

**STRC is the risk-free rate for this portfolio.**

Strategy's 10% coupon preferred stock (STRC), trading near par ($100), yields approximately **0.83% per month** with near-zero principal risk when held above par. Every trade in Buckets 1 and 2 must offer higher expected monthly return than STRC to justify deploying the capital.

If a trade can't beat STRC, the capital stays in STRC. This is not conservative — it's rational. STRC sets the floor.

### 3B. Expected Monthly Yield Hurdle

For any Bucket 1 or Bucket 2 trade, compute:

```
Expected Monthly Yield = (Probability of Profit × Avg Win − Probability of Loss × Avg Loss) / Capital at Risk / Holding Period in Months

Trade clears hurdle if: Expected Monthly Yield > 0.83%
```

**Example — Bull Put Spread:**
- Max profit: $2,900 (BPS $110/$100 @ $2.90 credit)
- Max loss: $7,100
- PoP: 75%
- Avg holding period: 30 days (1 month)
- Expected monthly yield: (0.75 × $2,900 − 0.25 × $7,100) / $7,100 = **+0.56%/month**
- **Verdict: Does NOT clear STRC hurdle.** Capital stays in STRC unless PoP improves or strike selection improves the R/R.

**Example — Iron Condor:**
- Max profit: $4,630 (IC $95/$105P + $145/$155C @ $4.63)
- Max loss: $5,370
- PoP: 72%
- Expected monthly yield: (0.72 × $4,630 − 0.28 × $5,370) / $5,370 / 1.5mo = **+12.6%/month**
- **Verdict: Clears hurdle decisively.** Deploy.

### 3C. When STRC Itself Becomes a Signal

STRC trading below par ($100) means the market is pricing credit risk into Strategy's preferred stock. This is itself a macro signal:

| STRC Price | Interpretation | Action |
|---|---|---|
| > $100 | Premium — credit healthy, yield < 10% | Normal benchmark |
| $97-$100 | Par — standard yield ~10% | Normal benchmark |
| < $97 | **Credit stress signal** | **Close all bullish positions per 1C** |
| < $93 | **Severe stress** | **STRC loses benchmark status — move to BIL/T-bills** |

If STRC breaks below $93, it is no longer a risk-free instrument and should not be used as the cost-of-capital benchmark. Substitute BIL or 3-month T-bills (~4.5-5% annualized, ~0.4%/month).

### 3D. Bucket 3 Exclusion

Bucket 3 (LEAPs) is explicitly excluded from the STRC yield comparison. LEAPs target long-term capital appreciation on regime transitions — a fundamentally different objective than monthly income. Comparing a 12-month LEAP to a monthly STRC yield is a category error.

Bucket 3 is evaluated on its own terms: asymmetric risk/reward at SRI inflection points, not monthly carry.

---

## Part 4: The Four Buckets

### BUCKET 1 — Short-Term Directional (Days to Weeks)

**Purpose:** Capture 5-30 day directional moves at SRI inflection points.

**Default vehicle: IBIT** (calls and puts)
**High-conviction override: MSTR** (calls only, Tier 1 with MVRV < 1.0)

**STRC hurdle applies:** Expected monthly yield must exceed 0.83%.

**Why IBIT over MSTR for Bucket 1:**
- Risk-adjusted returns favor IBIT at 20d+ (0.92 vs 0.75 at 60d)
- Bid-ask spreads 5-10x tighter
- Lower beta = tighter stops = larger sizing for same dollar risk
- Win rates identical (80% at 20d)

#### Bullish Entries (Long IBIT Calls)

**Tier 1 — Highest Conviction (all conditions):**
- [ ] FTL crosses above STL
- [ ] Robust fit crosses STL within 5 days (FAST)
- [ ] Price retests STL and holds (within 3%)
- [ ] MVRV < 1.5
- [ ] SRIBI positive or crossing zero
- [ ] Preferred credit healthy (STRC > $97)
- *Backtest: 20d avg +36.7%, 80% win rate*
- **For MVRV < 1.0: consider MSTR calls for leveraged beta**

**Tier 2 — Moderate (two of first three):**
- *Backtest: 20d avg +16.6%, 63% win rate*

**Tier 3 — No Entry:**
Robust fit > 10 days and/or retest fails → bear trap

#### Bearish Entries (Long IBIT Puts)

**Tier 1 — Full Bearish (all conditions):**
- [ ] STH-SOPR crosses below -0.2
- [ ] STRS was > 0.45 within last 10 days AND now declining
- [ ] MVRV > 1.5
- [ ] STRC < $97
- *Backtest: 5d avg -10.7%, 100% bear win rate (n=7)*

**Tier 2 — Defensive:**
- [ ] SOPR < -0.1 + STRS declining from > 0.40
- Action: Close bullish spreads, tighten stops — don't initiate puts

#### Position Structure

| Element | Specification |
|---|---|
| Strike | ATM to 5% OTM |
| DTE | 30-45 days |
| Size | Per RORO-adjusted allocation model (Part 5) |
| Entry timing | Day 2-5 after signal — **never chase Day 1** (avg -2.7%) |

#### Exit Rules

| Trigger | Action |
|---|---|
| Red line crosses STL (Step 7) | Close 50-75% |
| 50% profit | Close 50%, trail remainder |
| Robust fit stalls > 10 days | Close — reclassify as trap |
| Retest fails (>3% below STL) | Close immediately |
| Time stop: 21 DTE remaining | Close or roll |
| STRC breaks $97 | Close all bullish positions |
| SOPR recovers above 0 (for puts) | Close bearish positions |

---

### BUCKET 2 — Spread Income (Quarterly Premium Selling)

**Purpose:** Generate consistent income by selling premium at SRI-defined levels.

**Vehicle: MSTR** (IV30 83rd pctile — richer premium than IBIT)

**STRC hurdle applies:** Expected monthly yield must exceed 0.83%.

#### Stage-Based Strategy Selection

| SRI Stage | Primary Strategy |
|---|---|
| **Stage 4** | IC + BPS + BCS at SRI levels |
| **Stage 4→1** | Close BCS, widen BPS |
| **Stage 1** | Aggressive BPS; cash-secured puts |
| **Stage 2** | Covered calls + BCS on rallies |
| **Stage 3** | Buy put spreads, sell call spreads |

#### RORO Phase Overlay for Bucket 2

| RORO Phase | Bucket 2 Emphasis |
|---|---|
| **P1 Early** | **Primary bucket.** MSTR mean-reverts (+4.6% at 20d, 66% bull). Sell puts aggressively into fear. |
| P2 Broadening | Continue spreads. Begin shifting to bullish bias. |
| P3 Risk-On | Standard spreads. Covered calls if holding shares. |
| P4 Late | Shift bearish — BCS over BPS. Tighten stops. |
| P5 Full Risk-Off | Reduce size. Only highest-PoP condors. Capital migrates to STRC. |

#### Position Structure

| Element | Specification |
|---|---|
| Width | $10 standard |
| DTE | 30-60 days |
| Max risk | $50K per position, 8 positions max |
| Min R/R | Must clear STRC hurdle (0.83%/month expected yield) |
| Min PoP | 65% |

#### SRI-Driven Management

| SRI Event | Spread Action |
|---|---|
| FTL crosses above STL | Close all BCS within 2 days |
| Fast robust (≤5d) | Shift entire portfolio bullish |
| Retest holds | Add BPS at new STL support |
| Retest fails | Close BPS, add BCS |
| Red line crosses STL | Take 50-75% profit on BPS |
| STRC < $97 | Close all BPS immediately |
| STRK > $85 with volume | Maximum BPS allocation |

---

### BUCKET 3 — LEAPs (Long-Term Leveraged Positioning)

**Purpose:** Maximize long-term capital appreciation via leveraged delta during confirmed regime transitions.

**Vehicle: MSTR** (2-3x BTC beta is the point) or **IBIT** (for lower-risk LEAP exposure)

**STRC hurdle does NOT apply.** Bucket 3 is evaluated on asymmetric capital appreciation, not monthly yield.

#### Entry Triggers — REVISED v1.2

Bucket 3 has two entry paths:

**Path A — Classic (Stage 1 Confirmation):**
Need 2-3 of 4 primary triggers:
- [ ] SRI confirms Stage 1 on daily (5+ consecutive days)
- [ ] GLI Z-score > -0.5
- [ ] IV30 < 60%
- [ ] BTC breaks 200-day MA with volume

**Path B — Early Accumulation (P1_EARLY + Deep Discount):** *(New in v1.2)*
- [ ] RORO Phase = P1_EARLY (Safety bullish, Risk bearish)
- [ ] BTC STH-MVRV < 0.8
- [ ] Preferred credit healthy (STRC > $97)
- [ ] DTE ≥ 12 months (must be true LEAPs — long enough to survive chop)

**Why Path B exists:** P1_EARLY with deep discount MVRV identifies historically significant bottoming zones (Jan 2015, Nov 2018, Mar 2020, Nov 2022). The 60d forward return is +10.9% with 68% bull rate (n=84). The near-term is choppy, so only long-dated instruments survive the volatility. This is the asymmetric bet on rotation completing.

**Path B constraints:**
- Maximum 50% of LEAP budget via Path B (reserve the other 50% for Path A scaling)
- Wider strikes (10-20% OTM) to reduce premium at risk
- Accept mark-to-market drawdowns — the thesis is 6-12 months, not 6 weeks

#### Scaling Schedule

| Trigger | Allocation |
|---|---|
| Path B (P1_EARLY + MVRV < 0.8) | Up to 25% of LEAP budget |
| Path A: First cluster (2/4 primary) | +25% (50% total) |
| Stage 1 confirmed | +25% (75% total) |
| Stage 2 confirmed | +25% (100% total) |

#### LEAP Management

| Event | Action |
|---|---|
| Stage 2→3 begins | Close 50%, convert to spreads |
| Stage 3 confirmed | Close all |
| IV > 70th pctile at entry | Do NOT buy — sell premium instead |
| BTC breaks 200-day MA down | Close 50% of Path A, reassess |
| RORO transitions to P5 | Close 50% of Path B (thesis weakening) |
| STRC breaks $97 | Close all LEAPs |

---

### BUCKET 4 — STRC + Alternatives (Always Active)

**Purpose:** Preserve and grow capital when BTC/MSTR signals don't justify deployment. Generate baseline income via STRC. Opportunistically capture returns in non-correlated assets during BTC/MSTR regime exhaustion.

**This is not a residual bucket.** STRC is the default deployment of all capital not actively earning higher returns in Buckets 1-3.

#### 4A. STRC as Default Position

All uninvested capital sits in STRC (Strategy 10% Coupon Preferred Stock, ~$100/share).

| Attribute | Value |
|---|---|
| Ticker | STRC |
| Coupon | 10% annual (~0.83%/month) |
| Par value | $100 |
| Current price | ~$100 (at par) |
| Risk | Credit risk to Strategy Inc. Mitigated by STRC > $97 monitoring. |
| Liquidity | Daily — can be sold to fund Bucket 1-3 entries |

**STRC serves three functions simultaneously:**
1. **Income generation:** 10% annual yield covers living expense draw ($500K/yr from ~$5M = exact match at full STRC deployment)
2. **Cost-of-capital benchmark:** Every Bucket 1/2 trade must beat 0.83%/month to justify capital deployment
3. **Credit health signal:** STRC price < $97 triggers defensive posture across all buckets

#### 4B. Living Expense Draw

With $5M portfolio and $500K/yr target:
- Full STRC allocation at $5M × 10% = $500K/yr — **exactly covers the draw**
- As capital deploys to Buckets 1-3, STRC income declines proportionally
- Bucket 2 spread income must compensate for the yield reduction on deployed capital
- In P3_RISK_ON (most capital deployed), living draw comes from a mix of STRC yield on remaining cash + Bucket 2 income + periodic Bucket 1 profit-taking

#### 4C. Alternative Assets

When RORO indicates capital is flowing to specific asset classes, Bucket 4 can deploy to alternatives — but only when the alternative's own SRI signals confirm.

**Candidate Vehicles:**

| Asset | Ticker | Use Case | SRI Data Available |
|---|---|---|---|
| Gold | GLD | Risk-off hedge, liquidity cycle play | ✅ 3,668 rows |
| Long-term Treasuries | TLT | Flight to safety, rate cuts | ✅ 5,935 rows |
| Nasdaq 100 | QQQ | Growth when tech leads | ✅ 3,832 rows |
| Silver | SLV | Commodity cycle | ✅ 3,468 rows |
| Energy | XLE | Inflation hedge | ✅ 5,786 rows |
| Consumer Staples | XLP | Defensive rotation | ✅ 3,728 rows |
| Tesla | TSLA | High-beta tech, event-driven | ✅ 1,593 rows |

**RORO Phase → Alternative Emphasis:**

| RORO Phase | Alternative Opportunity |
|---|---|
| **P1 Early** | Safety assets (GLD, TLT) already bullish — ride existing trend. NOT new entries (they've already moved). |
| **P2 Broadening** | Quality assets turning (QQQ, XLP). Consider directional if their SRI confirms. |
| **P3 Risk-On** | No alternatives needed — capital belongs in Buckets 1-3 on BTC/MSTR. |
| **P4 Late** | Begin rotating profits to GLD/TLT as safety play. |
| **P5 Full Risk-Off** | Maximum alternative allocation. GLD/TLT if their SRI is bullish. Otherwise pure STRC. |

#### 4D. Bucket 4 Rules

1. **Uninvested capital defaults to STRC.** Not cash, not money market — STRC. Exception: if STRC < $93, substitute BIL.
2. **STRC hurdle applies to Buckets 1 and 2.** If a trade's expected monthly yield < 0.83%, capital stays in STRC.
3. **Alternative positions use Bucket 1 framework** applied to that asset's SRI data — same entry/exit discipline, same tier structure.
4. **Total alternative allocation capped at 20%** until individual SRI frameworks are backtested.
5. **BTC/MSTR signals always take priority.** If a Bucket 1/2/3 signal fires while capital is in alternatives, close alternatives and redeploy.
6. **Never go below 10% STRC.** Minimum cash equivalent at all times.

---

## Part 5: RORO-Integrated Allocation Model

### 5A. The Core Principle

**Allocation is driven by two axes: SRI Stage (individual asset signal) and RORO Phase (cross-asset rotation).**

SRI Stage tells you *what* to trade. RORO Phase tells you *how much* and *where in the capital stack*.

### 5B. Allocation Matrix: SRI Stage × RORO Phase

**Bucket 1 — Directional (% of portfolio)**

| | P1 Early | P2 Broad. | P3 Risk-On | P4 Late | P5 Risk-Off |
|---|---|---|---|---|---|
| Stage 4, no signal | 0% | 0% | 0% | 0% | 0% |
| Stage 4, FTL Tier 1 | 5-10% | 15-20% | 15-20% | 5-10% | 0% |
| Stage 4, FTL Tier 2 | 0-5% | 5-10% | 10-15% | 0% | 0% |
| Stage 1 Confirmed | 5-10% | 10-15% | 15-20% | 5-10% | 0% |
| Stage 3, SOPR Tier 1 | 10-15% (puts) | 10-15% (puts) | 15-20% (puts) | 15-20% (puts) | 10-15% (puts) |

**Bucket 2 — Spreads (% of portfolio)**

| | P1 Early | P2 Broad. | P3 Risk-On | P4 Late | P5 Risk-Off |
|---|---|---|---|---|---|
| Stage 4 | **15-25%** | 15-20% | 10-15% | 10-15% | 5-10% |
| Stage 1 | 20-25% | 20-25% | 20-25% | 15-20% | 10-15% |
| Stage 2 | 15-20% | 15-20% | 20-25% | 15-20% | 10-15% |
| Stage 3 | 10-15% | 10-15% | 10-15% | 5-10% | 5-10% |

*P1_EARLY is the highest Bucket 2 allocation because MSTR mean-reversion is strongest in this phase.*

**Bucket 3 — LEAPs (% of portfolio)**

| | P1 Early | P2 Broad. | P3 Risk-On | P4 Late | P5 Risk-Off |
|---|---|---|---|---|---|
| No triggers | 0% | 0% | 0% | 0% | 0% |
| Path B qualified | **5-10%** | 5-10% | N/A | 0% | 0% |
| Path A: 2/4 triggers | 10-15% | 15-20% | 15-20% | 5-10% | 0% |
| Stage 1 confirmed | 15-20% | 20-25% | 25-30% | 10-15% | 0% |
| Stage 2 confirmed | 20-25% | 25-30% | **30-40%** | 15-20% | 0% |

**Bucket 4 — STRC + Alternatives (remainder)**

Bucket 4 = 100% minus (Bucket 1 + Bucket 2 + Bucket 3). Minimum 10%.

### 5C. The STRC Yield Adjustment

When calculating how much Bucket 2 income is needed:

```
Required Bucket 2 monthly income = 
  Living expense draw per month ($41,667 at $500K/yr)
  − STRC monthly income (Bucket 4 STRC balance × 0.83%)

If STRC covers the full draw → Bucket 2 trades are purely for growth (higher hurdle, more selective)
If STRC partially covers → Bucket 2 has an income mandate (lower hurdle, more active)
```

**Current state ($4.6M in STRC):** STRC generates ~$38K/month. Living draw is ~$42K/month. Gap is only ~$4K/month — Bucket 2 has minimal income mandate. This means we can be highly selective, only taking spreads that significantly exceed the STRC hurdle.

### 5D. Allocation Decision Tree (RORO-Integrated)

```
1. What RORO Phase are we in?
   → Sets the column in the allocation matrix

2. What SRI Stage are we in?
   → Sets the row in the allocation matrix
   → Cross-reference: read target allocation for each bucket

3. Is a Bucket 1 signal active?
   → If yes: What tier? Apply the phase-adjusted allocation
   → If no: Bucket 1 = 0%

4. Are Bucket 3 LEAP triggers met?
   → Path A or Path B? Scale per schedule
   → Apply RORO phase adjustment

5. Compute Bucket 2 income mandate
   → STRC covers draw? Be selective (high hurdle)
   → STRC short of draw? Be active (standard hurdle)

6. Apply STRC hurdle to every Bucket 1 and Bucket 2 trade
   → Expected monthly yield > 0.83%? Deploy.
   → Below hurdle? Capital stays in STRC.

7. Remaining capital → STRC
   → If STRC < $93: substitute BIL
   → Scan alternatives per RORO phase guidance

8. Verify constraints
   → Bucket 4 ≥ 10% always
   → No single position > $50K risk
   → No more than 8 concurrent Bucket 2 positions
   → Bucket 3 scales per schedule, never lump-sum
   → Total alternatives ≤ 20%
```

---

## Part 6: Cross-Bucket Coordination

### Signal Cascade

**When Bucket 1 bullish signal fires:**
1. Bucket 1: Enter IBIT calls (Day 2-5)
2. Bucket 2: Close all BCS within 2 days; shift spread portfolio bullish
3. Bucket 3: If Path B LEAPs open, hold — signal confirms thesis
4. Bucket 4: Sell STRC to fund Bucket 1 entry; reduce alternative positions

**When Bucket 1 bullish signal fails:**
1. Bucket 1: Close longs; enter IBIT puts if SOPR confirms
2. Bucket 2: Maintain/increase BCS; close aggressive BPS
3. Bucket 3: If Path B LEAPs open, reassess at next RORO phase check
4. Bucket 4: Buy back STRC; scan alternatives

**When Bucket 1 bearish signal fires (SOPR < -0.2):**
1. Bucket 1: Enter IBIT puts
2. Bucket 2: Close all BPS; add BCS
3. Bucket 3: Close any LEAPs if STRC < $97
4. Bucket 4: Maximum STRC allocation; consider TLT if its SRI confirms

**When RORO phase transitions (e.g., P1→P2):**
1. Recalculate all bucket allocations using new column
2. Bucket 1: If transitioning to P3, prepare for higher directional allocation
3. Bucket 2: Adjust spread bias per phase overlay table
4. Bucket 3: Path B LEAPs benefit from rotation confirmation — hold or add
5. Bucket 4: Reduce STRC allocation as capital deploys; reduce alternatives as BTC/MSTR signals strengthen

### Priority Rule

**BTC/MSTR signals always take priority over alternatives.** If a Bucket 1/2/3 signal fires while capital is deployed in alternatives, close alternatives, buy STRC temporarily, then deploy from STRC to the signaled bucket.

---

## Part 7: Daily Operating Routine

### Pre-Market (8:00 AM ET)

1. **Real-Time Data Pull** (mandatory): `date -u`, Yahoo MSTR quote, OKX BTC quote
2. **RORO Phase Check:** Compute tier SRIBIs → classify phase → compare to yesterday
3. **RORO Score:** Continuous score + percentile rank + 5-day trend
4. **SRI Ladder Status:** Where are we in Steps 1-7?
5. **Bearish Engine Check:** SOPR, STRS level and 5d slope
6. **Preferred Spread:** STRC price (benchmark health), STRF, STRK, SCHI
7. **STRC Income Computation:** Current Bucket 4 STRC balance × 0.83% = monthly income. Gap to living draw?
8. **Allocation Check:** Current allocation vs RORO-adjusted target. Any rebalancing needed?
9. **Trigger Proximity:** Is any bucket entry/exit approaching?
10. **Alternative Scan:** If RORO phase indicates alternative opportunity, check asset SRI status

### Intraday Checkpoints

| Time | Check |
|---|---|
| 9:45 AM ET | Opening range — STL hold? Reprice pending orders. STRC price check. |
| 12:00 PM ET | Midday — robust fit, retest status, SOPR |
| 3:30 PM ET | Power hour — SRI breaks? Position management? |

### Post-Market (4:30 PM ET)

1. Update SRI ladder progress
2. Score open trades by step
3. Update RORO phase and score
4. Check preferred stock closes — STRC benchmark health
5. Update allocation vs target — any drift from RORO-adjusted targets?
6. Compute actual vs expected monthly yield per Bucket 2 position
7. If red line crossed STL → Bucket 1 exit process
8. If SOPR crossed -0.2 → alert for morning bearish entry
9. Write EOD recap including RORO phase + STRC income status

---

## Part 8: Current State (Feb 26, 2026)

### Market Snapshot

| Element | Value | Implication |
|---|---|---|
| MSTR | ~$135 | At $135 gate |
| BTC | ~$67,600 | Recovery from $62.5K low |
| SRI Stage | 4 (Day 187+) | Longest in dataset |
| MVRV | 0.50 | Most favorable ever |
| BTC SRIBI | -65 | Deeply negative |
| IV30 | ~80% (83rd pctile) | Rich — good for selling |
| STRS | 0.28 | Low, building from depleted |
| SOPR | ~-0.13 | Negative, above -0.2 |
| STRC | ~$100 | At par — benchmark healthy |

### RORO State

| Element | Value |
|---|---|
| **Phase** | **P1_EARLY** |
| RORO Score | -35.2 (4th percentile) |
| Safety SRIBI | +25.0 (TLT, GLD, BIL bullish) |
| Quality SRIBI | +3.3 (SPY, QQQ mixed) |
| Risk SRIBI | -42.5 (BTC, IBIT deeply bearish) |
| Speculative SRIBI | -15.0 (MSTR, TSLA bearish) |
| 5-day trend | Deteriorating (-28.6 → -35.2) |
| Phase duration | 10+ consecutive days in P1 |

### Current vs Target Allocation (RORO-Adjusted)

**Phase: P1_EARLY. Stage: 4, no confirmed signal.**

| Bucket | RORO Target | Current (Greg) | Status |
|---|---|---|---|
| 1 — Directional | 0% | 0% | ✅ Aligned |
| 2 — Spreads | 15-25% | ~8% | ⚠️ Room for more if trades clear STRC hurdle |
| 3 — LEAPs (Path B) | 5-10% if MVRV < 0.8 | 0% | 🔍 **Path B qualified** — MVRV 0.50, STRC healthy |
| 4 — STRC + Alts | 65-85% | ~92% (cash) | ⚠️ Convert cash to STRC for 10% yield |

### Key Actions Implied

1. **Convert idle cash to STRC** — $4.6M sitting at ~0% when STRC yields 10%. Immediate ~$38K/month income.
2. **Bucket 3 Path B is live** — P1_EARLY + MVRV 0.50 qualifies. Consider 5-10% ($250-500K) in 12-18 month MSTR or IBIT LEAPs, 10-20% OTM.
3. **Bucket 2 active** — MSTR mean-reverts hard in P1_EARLY. Sell puts into fear. But every trade must clear 0.83%/month.
4. **Watch for P1→P2 transition** — Quality SRIBI at +3.3, barely positive. If SPY/QQQ SRIBI firms above +10, we're broadening.

### Five-Trigger System for Stage 1

| # | Trigger | Status |
|---|---|---|
| 1 | MSTR > $135 w/ volume | ⚠️ AT THE LINE |
| 2 | STRK > $85 | ❌ $80.87 |
| 3 | SRIBI crosses zero | ❌ -65 |
| 4 | GLI Z > -0.7 | ❌ -1.01 |
| 5 | BTC > $72K | ❌ $67,600 |

**0 of 5 confirmed. 1 approaching.**

---

## Part 9: Risk Parameters

| Parameter | Limit |
|---|---|
| Max concurrent positions | 8 |
| Max risk per position | $50,000 |
| Min PoP (Bucket 2) | 65% |
| STRC yield hurdle (Buckets 1 & 2) | 0.83%/month expected yield |
| Take-profit target | 50% of max profit |
| Time stop | 21 DTE |
| Portfolio delta limit | ±50 net delta |
| Portfolio vega limit | -200 net vega |
| Loss halt | $50K unrealized portfolio loss |
| Min Bucket 4 (STRC) | 10% always |
| Max alternative allocation | 20% until frameworks validated |
| STRC health floor | $97 — below this, close all bullish |
| STRC benchmark floor | $93 — below this, substitute BIL |
| No naked short calls | Without Greg's approval |
| No earnings week trades | Without discussion |

---

## Part 10: Backtesting Appendix

### Data Sources
- Gavin's TradingView SRI exports: github.com/3ServantsP35/Grok
- MSTR daily: 5,012 rows (2006–2026)
- MSTR 4H: 1,247 rows (Jul 2023 – Jan 2026)
- BTC daily: 4,816 rows (2012–2026)
- IBIT daily: 510 rows (Jan 2024 – Jan 2026)
- SPY: 6,616 rows, QQQ: 3,832 rows, TLT: 5,935 rows, GLD: 3,668 rows
- Plus: XLY, XLK, XLP, XLE, XLF, HYG, LQD, BIL, SLV, DBC, TSLA, DXY, Copper/Gold, Stable Coin Dom

### RORO Rotation Backtest (3,728 days, 2011–2026)
- **P3_RISK_ON → BTC 20d:** +13.1% avg (vs +3.5% baseline). Strongest phase for directional.
- **P1_EARLY → MSTR 20d:** +4.6%, 66% bull. Mean-reversion premium strongest here.
- **P1_EARLY + BTC SRIBI < -40 (n=44):** 60d +6.4%, 62% bull. Historically significant bottoming zones.
- **P1_EARLY + MVRV < 0.8 (n=84):** 60d +10.9%, 68% bull. LEAP entry qualifier.

### Bullish: FTL Crosses Above STL
- **MSTR 4H** — Fast robust ≤5d (n=8): 20d +16.6%, 63% win. Retest held (n=5): 20d +36.7%
- **BTC Daily** — 20d +6.8%, 83% win. 60d +20.7%, 83% win
- **IBIT vs MSTR** — Risk-adjusted: IBIT 0.92 vs MSTR 0.75 at 60d.

### Bearish: STH-SOPR < -0.2
- **MSTR Daily** (7 instances): 5d -10.7% (100% bear), 30d -14.8% (86% bear)

### SRIBI Breadth Composite (Continuous RORO)
- **Q5 (Strong RO) vs Q1 (Strong RF) at BTC 20d:** +12.6% vs +0.9%. Spread: +11.7%.
- **Monotonic across all quintiles and horizons.** Signal quality confirmed.

---

## Revision History

| Date | Version | Changes |
|---|---|---|
| 2026-02-25 | 1.0 | Initial three-bucket framework |
| 2026-02-25 | 1.1 | Added Bucket 4, allocation model, decision tree |
| 2026-02-26 | 1.2 | RORO Capital Rotation Framework (5-phase, 13-asset, 3,728d backtest). STRC as cost-of-capital benchmark and default cash position. Revised LEAP triggers (Path B: P1_EARLY + MVRV < 0.8). RORO × SRI Stage allocation matrix. STRC yield hurdle for Buckets 1/2. Living expense draw model. Bucket 4 restructured around STRC. |
| 2026-02-26 | **1.2.1** | **RORO × BTC Cycle anchored allocation map. BTC cycle phases (C4→C1→C2→C3) defined via FTL/STL + SRIBI. Co-occurrence analysis (3,728d). Expected cycle progression sequence. P1+C1 Trap Rule: never deploy Bucket 1 when RORO and BTC cycle disagree (-4.2% at 40d, n=92). Master allocation table keyed to both RORO phase and BTC cycle.** |

---

*Framework by Gavin (rizenshine5359) & CIO. Subject to revision as more signal events accumulate and alternative asset frameworks are validated.*
