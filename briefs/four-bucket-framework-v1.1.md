# Four-Bucket Investment Framework
**Version:** 1.1 | **Date:** 2026-02-25
**Authors:** Gavin (SRI methodology, indicator architecture), CIO (backtesting, options structure)
**Status:** Draft v1.1 — Added Bucket 4 (Cash & Alternatives), risk-adjusted allocation model

---

## Executive Summary

This framework organizes all capital into four buckets with distinct time horizons, instruments, and signal sources. Two key innovations:

1. **Asymmetric signal architecture:** Bullish and bearish signals use different indicator systems
2. **Allocation optimized for risk-adjusted return**, with income/safety needs as an adjustment overlay — not the driver

```
┌──────────────────────────────────────────────────────────────┐
│                    SIGNAL ARCHITECTURE                        │
│                                                              │
│  BULLISH ENGINE: SRI Confirmation Ladder                     │
│  (FTL/STL crossover → robust fit speed → retest → red cross)│
│                                                              │
│  BEARISH ENGINE: SOPR + STRS                                 │
│  (SOPR < -0.2 trigger + STRS falling fast confirmation)      │
│                                                              │
│  REGIME ENGINE: STRS + Risk Oscillator                       │
│  (Risk depleted → rotate to alternatives)                    │
├────────────┬───────────────┬──────────────┬──────────────────┤
│  BUCKET 1  │   BUCKET 2    │   BUCKET 3   │    BUCKET 4      │
│ Directional│ Spread Income │    LEAPs     │ Cash & Alts      │
│ Days-Weeks │  Quarterly    │  6-12+ Mo    │ Always Active     │
│ IBIT       │  MSTR         │  MSTR        │ Cash/GLD/QQQ/TLT │
└────────────┴───────────────┴──────────────┴──────────────────┘
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

Average price move at red cross: **+13.6%** (range -6% to +28%). After the red cross, returns flatten or reverse. This marks the peak of the initial thrust.

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
- Bucket 3 (LEAPs) DOES require VL confirmation — you need the trend, not just the turn

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

### 1C. Regime Engine — When to Rotate

When STRS and Risk Oscillator indicate depleted risk appetite in BTC/MSTR — no bullish edge, no bearish edge, just noise — the framework shifts capital to Bucket 4 (Cash & Alternatives).

Risk Oscillator is NOT a directional signal (BTC: 55% bear at 20d — coin flip). Its value is telling you: *this market has no tradeable signal right now.*

### 1D. Preferred Stock Integration (All Signals)

| Signal | Meaning | Action |
|---|---|---|
| STRC > $97, STRF > $97 | Credit healthy | Bullish signals confirmed |
| STRC < $97 | Credit stress | **Close all bullish positions** |
| STRF < $97 | Severe stress | **Close all positions + add puts** |
| STRK > $85 with volume | Recovery priced | Stage 1 confirmation candidate |
| Credit healthy + equity falling | Bullish divergence | Tier 1 long signal |

**SCHI Composite:** (STRF premium × 0.4) + (STRC premium × 0.3) + (STRK premium × 0.3)
Current SCHI: -5.43 (mild stress, STRK-driven — not credit)

---

## Part 2: The Four Buckets

### BUCKET 1 — Short-Term Directional (Days to Weeks)

**Purpose:** Capture 5-30 day directional moves at SRI inflection points.

**Default vehicle: IBIT** (calls and puts)
**High-conviction override: MSTR** (calls only, Tier 1 with MVRV < 1.0)

**Why IBIT over MSTR for Bucket 1:**
- Risk-adjusted returns favor IBIT at 20d+ (0.92 vs 0.75 at 60d)
- Bid-ask spreads 5-10x tighter — viable market orders
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
| Size | Per allocation model (Part 3) |
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

#### Stage-Based Strategy Selection

| SRI Stage | Primary Strategy |
|---|---|
| **Stage 4** | IC + BPS + BCS at SRI levels |
| **Stage 4→1** | Close BCS, widen BPS |
| **Stage 1** | Aggressive BPS; cash-secured puts |
| **Stage 2** | Covered calls + BCS on rallies |
| **Stage 3** | Buy put spreads, sell call spreads |

#### Position Structure

| Element | Specification |
|---|---|
| Width | $10 standard |
| DTE | 30-60 days |
| Max risk | $50K per position, 8 positions max |
| Min R/R | 25% single spreads, 50%+ iron condors |
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

**Purpose:** Maximize long-term capital appreciation via leveraged delta during confirmed Stage 1→2 transitions.

**Vehicle: MSTR** (2-3x BTC beta is the point)

#### Entry Triggers (need 2-3 of 4 primary)

- [ ] SRI confirms Stage 1 on daily (5+ consecutive days)
- [ ] GLI Z-score > -0.5
- [ ] IV30 < 60%
- [ ] BTC breaks 200-day MA with volume

**Confirmation:** VL (2D) SRI cupping, STRK > $85, MVRV > 1.0, SRIBI > +20

**Current status: 0 of 4 primary triggers. $0 LEAP allocation.**

#### Scaling Schedule

| Trigger | Allocation |
|---|---|
| First cluster (2/4 primary) | 25% of LEAP budget |
| Stage 1 confirmed | +25% (50% total) |
| Stage 2 confirmed | +50% (100% total) |

#### LEAP Management

| Event | Action |
|---|---|
| Stage 2→3 begins | Close 50%, convert to spreads |
| Stage 3 confirmed | Close all |
| IV > 70th pctile | Do NOT buy — sell premium instead |
| BTC breaks 200-day MA down | Close 50%, reassess |

---

### BUCKET 4 — Cash & Alternatives (Always Active)

**Purpose:** Preserve capital when BTC/MSTR regime offers no edge, and generate returns from non-correlated assets when SRI signals exist elsewhere.

**This is not a residual bucket.** Cash and alternatives are a deliberate, optimized allocation — not "whatever's left over."

#### Cash as a Position

Cash earns the risk-free rate (~4.5-5% currently in money market/T-bills). In Stage 4 with no active signals, cash is the **highest risk-adjusted return** available — zero drawdown, positive carry.

**Cash is the default allocation.** Capital moves OUT of cash into Buckets 1-3 only when signals justify the risk. Capital moves BACK to cash when signals expire or fail.

#### Alternative Assets

When the regime engine indicates depleted BTC/MSTR risk appetite (STRS exhausted, Risk Osc negative, SRI flat), Bucket 4 actively seeks returns in non-correlated assets.

**Candidate Vehicles:**

| Asset | Ticker | Correlation to BTC | Use Case |
|---|---|---|---|
| Gold | GLD | Low (~0.1) | Risk-off hedge, inflation protection |
| Nasdaq 100 | QQQ | Moderate (~0.5) | Growth when tech leads, BTC lags |
| Long-term Treasuries | TLT | Negative (~-0.3) | Flight to safety, rate cuts |
| Tesla | TSLA | Moderate (~0.4) | High-beta tech, event-driven |
| Energy | XLE | Low (~0.2) | Commodity cycle, inflation hedge |

**Signal Source:** Gavin's SRI indicator CSVs exist for QQQ, GLD, DXY on GitHub with full FTL/STL/SRIBI columns. Individual asset SRI frameworks will be built as these are backtested.

**Current status:** Frameworks not yet built. For now, Bucket 4 = cash + T-bills. Alternative asset allocation activates once individual SRI frameworks are validated.

#### Bucket 4 Strategy by Regime

| Regime | Bucket 4 Action |
|---|---|
| **Active BTC/MSTR signals (any bucket firing)** | Cash only — capital reserved for Buckets 1-3 |
| **No signals, STRS > 0.35** | Cash + T-bills — healthy regime but no entry point |
| **No signals, STRS < 0.25** | Scan alternatives — BTC/MSTR risk depleted, look elsewhere |
| **Confirmed Stage 4, no cross imminent** | Active alternative allocation — GLD/TLT if their SRI signals present |
| **Macro tailwind (GLI Z > 0) but BTC lagging** | QQQ/TSLA calls if their SRI confirms |

#### Bucket 4 Rules

1. **Never go 0% cash.** Minimum 10% cash at all times for liquidity and opportunity cost.
2. **Alternative positions use the same Bucket 1 framework** applied to that asset's SRI data — same entry/exit discipline, same tier structure.
3. **Alternatives are Bucket 1-style trades** (directional, 30-45 DTE). No spread selling on alternatives (insufficient IV edge outside MSTR). No LEAPs on alternatives (insufficient conviction without full framework validation).
4. **Total alternative allocation capped at 20% of portfolio** until individual frameworks are backtested.
5. **BTC/MSTR signals always take priority.** If a Bucket 1/2/3 signal fires while capital is in alternatives, close alternatives and redeploy.

---

## Part 3: Allocation Model — Optimized for Risk-Adjusted Return

### The Core Principle

**Allocation follows signal quality, not financial needs.**

The base allocation at each stage is determined by the risk-adjusted edge available in each bucket — measured by win rate, return magnitude, and variance from our backtests. Income needs and safety preferences are an *adjustment layer* applied on top.

### Base Allocations by Stage (Optimized for Risk-Adjusted Return)

These allocations represent where capital should be deployed to maximize risk-adjusted returns based on backtested signal quality at each stage.

| Stage | Bucket 1 (Directional) | Bucket 2 (Spreads) | Bucket 3 (LEAPs) | Bucket 4 (Cash & Alts) |
|---|---|---|---|---|
| **Stage 4, no signal** | 0% | 10-15% | 0% | **85-90%** |
| **Stage 4, FTL cross Tier 1** | **15-20%** | 10-15% | 0% | 65-75% |
| **Stage 4, FTL cross Tier 2** | 5-10% | 10-15% | 0% | 75-85% |
| **Stage 4→1 Transition** | 10-15% | 15-20% | 0% | 65-75% |
| **Stage 1 Confirmed** | 5-10% | 20-25% | **15-25%** | 40-60% |
| **Stage 2 Confirmed** | 0-5% | 20-25% | **30-40%** | 30-50% |
| **Stage 2 Mature** | 0% | 15-20% | **35-45%** | 35-50% |
| **Stage 3 (Distribution)** | 5-10% (puts) | 10-15% (bearish) | 0% (closed) | **75-85%** |
| **Stage 3, SOPR Tier 1** | **15-20% (puts)** | 5-10% (bearish) | 0% | 70-80% |

**How to read this table:** These are the risk-optimal allocations. A Tier 1 FTL cross in Stage 4 with MVRV < 1.0 is the highest-edge signal in our dataset (80% win, 36.7% avg 20d return). The framework allocates aggressively to that signal. Conversely, Stage 4 with no signal has zero edge in Buckets 1 and 3 — cash is the optimal position.

### Why These Allocations

**Stage 4, no signal (85-90% cash):**
No bullish signal active. Spreads earn modest income but Kelly criterion says the edge is thin — PoP is 65% but R/R on individual spreads is 25-50%, so the expected value per dollar risked is moderate. Cash at 4.5-5% risk-free rate is competitive. Hold capital for the high-edge signal.

**Stage 4, Tier 1 FTL cross (15-20% directional):**
This is the best risk-adjusted moment. Backtested: 80% win rate, 36.7% avg 20d return at MVRV < 1.0. Half-Kelly suggests ~36% allocation, but we cap at 20% because n=5 (small sample, need more data). As more crossovers are observed and framework is validated, this ceiling can rise.

**Stage 1-2 (LEAPs ramp to 35-45%):**
Once the trend is confirmed (VL cupping, 2+ primary triggers), MSTR LEAPs offer 3-5x leveraged exposure to a validated move. Historical Stage 1→2 moves: +100-300% on the stock, +300-1000% on ATM LEAPs. The Kelly edge is enormous but we scale in gradually (25/50/100%) to manage the risk of false Stage 1 calls.

**Stage 3, SOPR Tier 1 (15-20% puts):**
SOPR < -0.2 is our strongest bearish signal: 100% win at 5d, 86% at 30d. When it fires during confirmed Stage 3, the framework allocates aggressively to puts. This is the bearish equivalent of the Tier 1 FTL cross.

### Adjustment Layer: Income Needs

The base allocations optimize for total risk-adjusted return. When income is needed, the adjustment shifts capital toward Bucket 2 (spread income) and covered calls.

| Need | Adjustment |
|---|---|
| **No income need** | Use base allocations as-is |
| **Moderate income ($250-500K/yr)** | +5-10% to Bucket 2, -5-10% from Bucket 4 cash |
| **Heavy income ($500K+/yr)** | +10-15% to Bucket 2, shift Bucket 2 toward higher-frequency shorter-DTE spreads, prioritize covered calls on shares |

**Greg's current situation:** $500K/yr income target from $5M. Adjustment: +10% to Bucket 2 vs base. Front-load high-turnover strategies in 2026 to consume $750K short-term losses.

**Gavin's paper portfolio:** No income need. Use base allocations as-is.

### Adjustment Layer: Safety / Capital Preservation

When capital preservation is prioritized (approaching a major withdrawal, uncertain regime, personal risk tolerance shift):

| Need | Adjustment |
|---|---|
| **Standard** | Use base allocations |
| **Conservative** | +10-15% to Bucket 4 cash, reduce Bucket 1/3 sizing |
| **Defensive** | Cap Buckets 1-3 at 50% combined, minimum 50% cash |
| **Capital preservation mode** | Bucket 4 at 80%+, only Bucket 2 active (small, high-PoP spreads) |

### Allocation Decision Tree

```
1. What SRI Stage are we in?
   → Sets the base allocation row from the table above

2. Is a Bucket 1 signal active?
   → If yes: What tier? Adjust Bucket 1 allocation accordingly
   → If no: Bucket 1 = 0%, capital stays in Bucket 4

3. Are Bucket 3 LEAP triggers met?
   → If yes: How many? Scale per 25/50/100% schedule
   → If no: Bucket 3 = 0%

4. Apply income adjustment
   → Shift from Bucket 4 → Bucket 2 per need level

5. Apply safety adjustment
   → Shift from Buckets 1/3 → Bucket 4 per need level

6. Check Bucket 4 regime
   → Are alternative asset SRI signals present?
   → If yes and BTC/MSTR signals absent: allocate to alternatives
   → If no: hold cash/T-bills

7. Verify constraints
   → Bucket 4 ≥ 10% always
   → No single Bucket 1 trade > 5% of portfolio
   → No more than 8 concurrent Bucket 2 positions
   → Bucket 3 scales per schedule, never lump-sum
```

---

## Part 4: Cross-Bucket Coordination

### Signal Cascade

**When Bucket 1 bullish signal fires:**
1. Bucket 1: Enter IBIT calls (Day 2-5)
2. Bucket 2: Close all BCS within 2 days; shift spread portfolio bullish
3. Bucket 3: Begin monitoring LEAP triggers — no action yet
4. Bucket 4: Reduce cash allocation per stage table; close any alternative positions

**When Bucket 1 bullish signal fails:**
1. Bucket 1: Close longs; enter IBIT puts if SOPR confirms
2. Bucket 2: Maintain/increase BCS; close aggressive BPS
3. Bucket 3: No change
4. Bucket 4: Return capital to cash; scan alternatives

**When Bucket 1 bearish signal fires (SOPR < -0.2):**
1. Bucket 1: Enter IBIT puts
2. Bucket 2: Close all BPS; add BCS
3. Bucket 3: Close any LEAPs if STRC < $97
4. Bucket 4: Increase cash allocation; consider TLT (flight to safety)

**When regime indicates no edge:**
1. Buckets 1-3: Reduce to minimum or zero
2. Bucket 4: Maximum allocation — cash + scan for alternative SRI signals

### Priority Rule

**BTC/MSTR signals always take priority over alternatives.** If a Bucket 1/2/3 signal fires while capital is deployed in alternatives, close alternatives and redeploy. The BTC/MSTR framework is backtested; alternatives are not yet.

---

## Part 5: Daily Operating Routine

### Pre-Market (8:00 AM ET)

1. **Real-Time Data Pull** (mandatory): `date -u`, Yahoo MSTR quote, OKX BTC quote
2. **SRI Ladder Status:** Where are we in Steps 1-7?
3. **Bearish Engine Check:** SOPR, STRS level and 5d slope
4. **Preferred Spread:** STRC, STRF, STRK, SCHI
5. **Allocation Check:** Current allocation vs target for this stage. Any rebalancing needed?
6. **Trigger Proximity:** Is any bucket entry/exit approaching?
7. **Alternative Scan:** If Bucket 4 alternatives active, check their SRI status

### Intraday Checkpoints

| Time | Check |
|---|---|
| 9:45 AM ET | Opening range — STL hold? Reprice pending orders. |
| 12:00 PM ET | Midday — robust fit, retest status, SOPR |
| 3:30 PM ET | Power hour — SRI breaks? Position management? |

### Post-Market (4:30 PM ET)

1. Update SRI ladder progress
2. Score open trades by step
3. Check preferred stock closes, update SCHI
4. Update allocation vs target — any drift?
5. If red line crossed STL → Bucket 1 exit process
6. If SOPR crossed -0.2 → alert for morning bearish entry
7. Write EOD recap

---

## Part 6: Current State (Feb 25, 2026)

### Market Snapshot

| Element | Value | Implication |
|---|---|---|
| MSTR | $135.18 | Up from $124 yesterday |
| BTC | $68,534 | Recovery from $62.5K Sunday low |
| SRI Stage | 4 (Day 187) | Longest in dataset |
| MVRV | 0.50 | Most favorable ever |
| SRIBI | -49.86 | Negative, not crossing zero |
| FTL vs STL | Approaching (8H) | Cross imminent |
| IV30 | 80.6% (83rd pctile) | Rich — good for selling |
| GLI Z-score | -1.01 | Macro headwind |
| STRS | 0.28 | Low, building from depleted |
| SOPR | ~-0.13 | Negative, above -0.2 |
| Preferred | STRC $99.96, STRF $100.80, STRK $80.87 | Credit healthy |
| SCHI | -5.43 | Mild stress (STRK-driven) |

### Current Allocation vs Target

**Stage: 4, no confirmed signal. Base allocation: 85-90% cash.**
**Income adjustment: +10% to Bucket 2 (Greg's $500K/yr target).**

| Bucket | Target | Actual (Greg) | Status |
|---|---|---|---|
| 1 — Directional | 0% | 0% | ✅ Aligned |
| 2 — Spreads | 15-20% | ~8% ($385K shares + CCs + IC pending) | ⚠️ Below target — room for 1-2 more spreads |
| 3 — LEAPs | 0% | 0% | ✅ Aligned |
| 4 — Cash & Alts | 80-85% | ~92% ($4.61M cash) | ⚠️ Above target — could deploy more to Bucket 2 |

### Five-Trigger System for Stage 1

| # | Trigger | Status |
|---|---|---|
| 1 | MSTR > $135 w/ volume | ⚠️ AT THE LINE |
| 2 | STRK > $85 | ❌ $80.87 |
| 3 | SRIBI crosses zero | ❌ -49.86 |
| 4 | GLI Z > -0.7 | ❌ -1.01 |
| 5 | BTC > $72K | ❌ $68,534 |

**0 of 5 confirmed. 1 approaching.**

---

## Part 7: Risk Parameters

| Parameter | Limit |
|---|---|
| Max concurrent positions | 8 |
| Max risk per position | $50,000 |
| Min probability of profit | 65% |
| Take-profit target | 50% of max profit |
| Time stop | 21 DTE |
| Portfolio delta limit | ±50 net delta |
| Portfolio vega limit | -200 net vega |
| Loss halt | $50K unrealized portfolio loss |
| Min cash (Bucket 4) | 10% always |
| Max alternative allocation | 20% until frameworks validated |
| No naked short calls | Without Greg's approval |
| No earnings week trades | Without discussion |

---

## Part 8: Backtesting Appendix

### Data Sources
- Gavin's TradingView SRI exports: github.com/3ServantsP35/Grok
- MSTR daily: 1,300 rows (Nov 2020 – Jan 2026)
- MSTR 4H: 1,247 rows (Jul 2023 – Jan 2026)
- BTC daily: 1,650 rows (Jul 2021 – Jan 2026)
- IBIT daily: 510 rows (Jan 2024 – Jan 2026)
- Additional: QQQ, GLD, DXY CSVs available (not yet backtested)

### Bullish: FTL Crosses Above STL
- **MSTR 4H** — Fast robust ≤5d (n=8): 20d +16.6%, 63% win. Retest held (n=5): 20d +36.7%
- **BTC Daily** — 20d +6.8%, 83% win. 60d +20.7%, 83% win
- **IBIT vs MSTR** — Risk-adjusted: IBIT 0.92 vs MSTR 0.75 at 60d. Win rates identical.

### Bearish: FTL Crosses Below STL (Contra-Indicator)
- **MSTR Daily** (12 significant): 5d avg +7.1%. Do NOT use for bearish entries.

### Bearish: STH-SOPR < -0.2
- **MSTR Daily** (7 instances): 5d -10.7% (100% bear), 30d -14.8% (86% bear)

### Bearish Confirmation: STRS Falling Fast
- **MSTR Daily** (6 instances): 20d -4.9%, 83% bear

### Regime: Risk Oscillator
- **BTC Daily** (20 instances): 20d +0.7%, 55% bear — not a signal, regime context only

### Regime: STRS Level
- **MSTR Daily**: <0.25 → 20d -1.8% (depleted). 0.35-0.50 → 20d +10.7% (sweet spot). >0.65 → 20d +26.4% (rare euphoria)

---

## Part 9: Future Work

| Priority | Item | Status |
|---|---|---|
| 1 | **Alternative asset SRI frameworks** — Backtest QQQ, GLD, TLT, TSLA, XLE using GitHub CSVs. Build individual Bucket 1 frameworks per asset. | Backlog |
| 2 | **STRS regime rotation threshold** — Derive empirically: exact level + duration that triggers alternative scan. | Backlog |
| 3 | **Bearish engine hardening** — Year-long. More SOPR/STRS events. Target: production-ready by Stage 3. | Active |
| 4 | **Preferred stock pipeline** — `collect_preferred.py` ready. Needs cron deploy. | Ready |
| 5 | **FTL/STL production integration** — Crossover monitoring in Morning Brief automation. | In progress |
| 6 | **BTC SOPR/STRS validation** — Run bearish backtests on BTC (currently MSTR only). | Next |
| 7 | **IBIT options liquidity analysis** — Quantify execution edge vs MSTR. | Backlog |
| 8 | **Allocation model validation** — Paper trade the allocation targets for 1 quarter, compare to equal-weight baseline. | After launch |

---

## Revision History

| Date | Version | Changes |
|---|---|---|
| 2026-02-25 | 1.0 | Initial three-bucket framework |
| 2026-02-25 | 1.1 | Added Bucket 4 (Cash & Alternatives). Allocation model optimized for risk-adjusted return with income/safety as adjustment layers. Allocation decision tree. Current vs target tracking. |

---

*Framework by Gavin (rizenshine5359) & CIO. Subject to revision as more signal events accumulate and alternative asset frameworks are validated.*
