# Three-Bucket Investment Framework
**Version:** 1.0 | **Date:** 2026-02-25
**Authors:** Gavin (SRI methodology, indicator architecture), CIO (backtesting, options structure)
**Status:** Draft for review — Greg and Gavin to iterate

---

## Executive Summary

This framework organizes all trading activity into three buckets with distinct time horizons, instruments, and signal sources. The key innovation: **bullish and bearish signals use different indicator systems**, and the framework recognizes when the BTC/MSTR regime offers no edge — triggering rotation to other assets.

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
│  (Risk depleted → rotate to non-correlated assets)           │
├──────────────┬──────────────────┬────────────────────────────┤
│  BUCKET 1    │    BUCKET 2      │     BUCKET 3               │
│  Directional │    Spread Income  │     LEAPs                  │
│  Days-Weeks  │    Quarterly      │     6-12+ Months           │
│  IBIT default│    MSTR           │     MSTR                   │
└──────────────┴──────────────────┴────────────────────────────┘
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

When short-term holders are realizing losses at this rate, the selloff has 5-30 more days to run. The only "failures" at 20d (Nov 2022, Dec 2022) occurred at the absolute cycle bottom — the signal correctly identified the final capitulation phase.

**Confirmation: STRS (Short-Term Risk Score) Falling Fast**

STRS dropping >0.10 in 5 days: 83% bear at 20d (n=6). STRS validates that risk appetite was elevated *before* the SOPR trigger — meaning there's fuel for the move down.

**STRS Context (regime, not signal):**

| STRS Level | Interpretation |
|---|---|
| > 0.55 | Overheated — risk appetite high, vulnerable to shock |
| 0.35 - 0.50 | Healthy — normal risk environment |
| 0.25 - 0.35 | Cooling — risk appetite declining |
| < 0.25 | Exhausted — selloff likely late-stage, limited further downside |

**Bearish Signal Tiers:**

| Tier | Conditions | Action |
|---|---|---|
| **1 — Full Bearish** | SOPR < -0.2 + STRS was >0.45 recently & now falling + MVRV >1.5 | Buy IBIT puts |
| **2 — Defensive** | SOPR < -0.1 + STRS declining from >0.40 | Close bullish spreads, tighten stops |
| **3 — Watch** | Risk Osc < -0.15 on BTC | Flag but don't trade |

### 1C. Regime Engine — When to Look Elsewhere

**Risk Oscillator is not a directional signal** (BTC: 20d bear rate 55% when crossing below -0.15 — coin flip). Its value is as a regime indicator.

When STRS and Risk Oscillator indicate depleted risk appetite in BTC/MSTR — meaning the SRI bullish engine has no signal and the bearish engine has exhausted its move — the framework rotates attention to non-correlated assets.

**Candidate rotation vehicles:** QQQ, GLD, TLT, TSLA, XLE
**Data available:** Gavin's GitHub has SRI indicator CSVs for QQQ, GLD, DXY with full FTL/STL/SRIBI columns
**Status:** Rotation thresholds will be derived empirically from STRS data. Individual asset frameworks to be built as a future project.

### 1D. Preferred Stock Integration (All Signals)

The preferred stocks (STRF, STRC, STRK) serve as a leading indicator layer across all signal types.

| Signal | Meaning | Action |
|---|---|---|
| STRC > $97, STRF > $97 | Credit healthy | Bullish signals confirmed |
| STRC < $97 | Credit stress | **Close all bullish positions** |
| STRF < $97 | Severe stress | **Close all positions + add puts** |
| STRK > $85 with volume | Equity market pricing recovery | Stage 1 confirmation candidate |
| Credit healthy + equity falling | Bullish divergence | Tier 1 long signal (divergence = market mispricing the risk) |

**Current preferred state:** STRC $99.96, STRF $100.80, STRK $80.87 — credit healthy, NOT confirming BTC weakness.

**SCHI Composite:** (STRF premium × 0.4) + (STRC premium × 0.3) + (STRK premium × 0.3)
Current SCHI: -5.43 (mild stress, driven by STRK equity discount — not credit stress)

---

## Part 2: The Three Buckets

### BUCKET 1 — Short-Term Directional (Days to Weeks)

**Purpose:** Capture 5-30 day directional moves at SRI inflection points.

**Default vehicle: IBIT** (calls and puts)
**High-conviction override: MSTR** (calls only, Tier 1 signals with MVRV < 1.0)

**Why IBIT over MSTR for Bucket 1:**
- Risk-adjusted returns favor IBIT at 20d+ (Sharpe-like: 0.75 vs 0.71 at 20d, 0.92 vs 0.75 at 60d)
- Bid-ask spreads 5-10x tighter — better fills, viable market orders
- Lower beta = tighter stops = larger position sizing for same dollar risk
- Win rates identical (80% at 20d on SRI signals)
- MSTR's 2-3x raw return advantage is offset by 2-3x drawdown risk

**BTC as cross-confirmation:** When both BTC and MSTR show FTL crossing STL within the same ±5 day window, conviction increases significantly.

#### Bullish Entries (Long IBIT Calls)

**Tier 1 — Highest Conviction (all conditions):**
- [ ] FTL crosses above STL
- [ ] Robust fit crosses STL within 5 days (FAST)
- [ ] Price retests STL and holds (within 3%)
- [ ] MVRV < 1.5
- [ ] SRIBI positive or crossing zero
- [ ] Preferred credit healthy (STRC > $97)
- *Backtest: 20d avg +36.7%, 80% win rate*
- **For MVRV < 1.0: consider MSTR calls instead of IBIT for leveraged beta**

**Tier 2 — Moderate (two of first three):**
- [ ] FTL cross + (robust fast OR retest holds)
- [ ] SRIBI improving toward zero
- *Backtest: 20d avg +16.6%, 63% win rate*

**Tier 3 — No Entry:**
Robust fit > 10 days and/or retest fails → bear trap

#### Bearish Entries (Long IBIT Puts)

**Tier 1 — Full Bearish:**
- [ ] STH-SOPR crosses below -0.2
- [ ] STRS was > 0.45 within last 10 days AND now declining
- [ ] MVRV > 1.5 (overextended)
- [ ] STRC < $97 (credit stress confirming)
- *Backtest: 5d avg -10.7%, 100% bear win rate (n=7)*

**Tier 2 — Defensive:**
- [ ] SOPR < -0.1 + STRS declining from > 0.40
- Action: Close bullish spreads, tighten stops — don't initiate puts

#### Position Structure

| Element | Specification |
|---|---|---|
| Strike | ATM to 5% OTM |
| DTE | 30-45 days |
| Size | 2-5% of portfolio per trade |
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

#### Execution Timing (from 4H backtest)

| Day After Signal | Avg Return | Action |
|---|---|---|
| Day 1 | -2.7% | **Do not enter** — shakeout common |
| Day 2-3 | +1.4% | Retest zone — watch for hold/fail |
| Day 3-5 | +3.6% | **Entry zone** — robust crossed, retest held |
| Day 10+ | +5.9% | Too late for initial entry |

---

### BUCKET 2 — Spread Income (Quarterly Premium Selling)

**Purpose:** Generate consistent income by selling premium at SRI-defined reversal levels.

**Vehicle: MSTR** (higher IV = fatter premiums)
- MSTR IV30 currently 80.6% (83rd percentile) vs IBIT ~50-55%
- Put skew at 98th percentile on MSTR — outsized premium for bull put spreads

#### Stage-Based Strategy Selection

| SRI Stage | Primary Strategy | Rationale |
|---|---|---|
| **Stage 4 (current)** | IC + BPS + BCS at SRI levels | Sell into fear; elevated skew pays |
| **Stage 4→1 Transition** | Close BCS, widen BPS | Transition emerging; shift bullish |
| **Stage 1** | Aggressive BPS; cash-secured puts | Confirmed bottom; collect while building |
| **Stage 2** | Covered calls + BCS on rallies | Ride trend; sell premium on extensions |
| **Stage 3** | Buy put spreads, sell call spreads | Topping; reduce bullish exposure |

#### Entry Triggers

**Bull Put Spreads:**
- [ ] SRI Stage 4 with put skew > 70th percentile
- [ ] Short strike below key SRI support (FTL or tested level)
- [ ] mNAV < 1.3x
- [ ] Preferred credit healthy
- [ ] Enhanced: FTL approaching STL from below + credit divergence

**Bear Call Spreads:**
- [ ] Stage 3 or 4 with declining STL
- [ ] Short strike above STL or resistance
- [ ] MAs bearishly aligned
- [ ] GLI Z-score < -0.5

**Iron Condors:**
- [ ] Stage 4 range-bound consolidation
- [ ] IV > 70th percentile
- [ ] Put wing below support, call wing above resistance
- [ ] Width = SRI support-to-resistance range

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
| Stage transition confirmed | Rotate to new stage strategy |

#### Kill Conditions

| Condition | Action |
|---|---|
| Portfolio loss > $50K unrealized | Close weakest 2 positions |
| BTC < $60K (current cycle) | Close all put spreads |
| MSTR gap > 10% against position | Reassess; close if SRI confirms |
| Any single position at max loss | Close, do not add |

---

### BUCKET 3 — LEAPs (Long-Term Leveraged Positioning)

**Purpose:** Maximize long-term capital appreciation through leveraged delta exposure during confirmed Stage 1→2 transitions.

**Vehicle: MSTR** (leveraged beta to BTC is the entire point — 2-3x amplification over 6-12 months)

#### Entry Triggers — High Bar (need 2-3 of 4 primary)

**Primary (2-3 required):**
- [ ] SRI confirms Stage 1 on daily TF (5+ consecutive days)
- [ ] GLI Z-score > -0.5 (macro headwind removed)
- [ ] IV30 < 60% (don't buy rich LEAPs)
- [ ] BTC breaks 200-day MA with volume

**Confirmation (strengthen conviction):**
- [ ] **VL (2D) SRI begins cupping** — this is THE LEAP signal
- [ ] STRK > $85 with sustained volume
- [ ] MVRV crosses above 1.0
- [ ] SRIBI > +20 on daily and 2D timeframes
- [ ] MSTR/BTC/STRC ratio breaks above 0.22 (cup & handle breakout)

**Why VL confirmation matters here (and not for Buckets 1-2):**
LEAPs deploy large capital ($500K-$1M) over 6-12 months. Missing the first 30% of the move is acceptable when you're leveraged 3-5x on the remaining 70%. VL confirmation means the *trend* is established, not just the *turn*. This reduces the risk of deploying large capital into a bear trap.

**Current status: 0 of 4 primary triggers met. $0 LEAP allocation.**

#### Position Structure

| Element | Greg ($5M) | Gavin ($1M paper) |
|---|---|---|
| Max allocation | $1M | $200K |
| Strike | ATM or up to 20% ITM (delta 0.60-0.80) |
| DTE | 180-365 days minimum |

#### Scaling Schedule

| Trigger | Allocation |
|---|---|
| First trigger cluster (2/4 primary met) | 25% of LEAP budget |
| Stage 1 confirmed (5+ days) | +25% (total 50%) |
| Stage 2 confirmed | +50% (total 100%) |

#### IV Regime for LEAP Strike Selection

| IV30 Percentile | Guidance |
|---|---|
| < 30th | Buy ATM or slightly OTM — cheap vol |
| 30th-50th | Buy ATM — balanced |
| 50th-70th | Buy 10-20% ITM — reduce vega |
| > 70th | **Do not buy LEAPs** — Bucket 2 instead |

#### LEAP Management

| Event | Action |
|---|---|
| Stage 2→3 begins | Close 50%, convert rest to spreads |
| Stage 3 confirmed | Close all LEAPs |
| IV spike > 90th pctile | Do NOT buy; wait for normalization |
| BTC breaks 200-day MA down | Close 50%, reassess |
| STRC < $97 during hold | Hedge with protective puts |

---

## Part 3: Cross-Bucket Coordination

### Capital Allocation by Stage

| Stage | Bucket 1 | Bucket 2 | Bucket 3 | Cash |
|---|---|---|---|---|
| **Stage 4 (current)** | 0-5% | 10-20% | 0% | 75-90% |
| **Stage 4→1 Transition** | 5-10% | 15-25% | 0% | 65-80% |
| **Stage 1 Confirmed** | 5-10% | 20-30% | 10-25% | 35-65% |
| **Stage 2 Confirmed** | 0-5% | 20-30% | 25-50% | 15-55% |
| **Stage 3 (Distribution)** | 5-10% (puts) | 15-25% (bearish) | 0% | 65-80% |

### Signal Cascade

**When Bucket 1 bullish signal fires:**
1. Bucket 1: Enter IBIT calls (Day 2-5)
2. Bucket 2: Close all BCS within 2 days; shift spread portfolio bullish
3. Bucket 3: Begin monitoring LEAP triggers — no action yet

**When Bucket 1 bullish signal fails (slow robust / retest failure):**
1. Bucket 1: Close longs; enter IBIT puts if SOPR confirms
2. Bucket 2: Maintain/increase BCS; close aggressive BPS
3. Bucket 3: No change

**When Bucket 1 bearish signal fires (SOPR < -0.2):**
1. Bucket 1: Enter IBIT puts
2. Bucket 2: Close all BPS; add BCS
3. Bucket 3: Close any existing LEAPs if STRC < $97

**When regime indicates no edge (STRS depleted, Risk Osc negative, SRI flat):**
1. All buckets: Reduce MSTR/BTC exposure to minimum
2. Bucket 1: Rotate attention to QQQ, GLD, TLT, TSLA, XLE
3. Bucket 2: Maintain existing positions only; no new entries
4. Bucket 3: No action

---

## Part 4: Daily Operating Routine

### Pre-Market (8:00 AM ET)

1. **Real-Time Data Pull** (mandatory): `date -u`, Yahoo MSTR quote, OKX BTC quote
2. **SRI Ladder Status:** Where are we in Steps 1-7? Days since last FTL cross?
3. **Bearish Engine Check:** Current SOPR, STRS level and 5d slope
4. **Preferred Spread:** STRC, STRF, STRK levels. SCHI composite.
5. **Trigger Proximity:** Is any bucket entry/exit trigger approaching?
6. **Open Position Check:** Update hypothesis tracking on all trades

### Intraday Checkpoints

| Time | Check |
|---|---|
| 9:45 AM ET | Opening range — did STL hold as support/resistance? Reprice any pending orders. |
| 12:00 PM ET | Midday — robust fit progress, retest status, SOPR intraday movement |
| 3:30 PM ET | Power hour — SRI level breaks? Position management before close? |

### Post-Market (4:30 PM ET)

1. Update SRI ladder progress for all timeframes
2. Score open Bucket 1 trades: which step are we on?
3. Check preferred stock closing levels, update SCHI
4. Update hypothesis tracking on all positions
5. **If red line crossed STL today** → trigger Bucket 1 exit process
6. **If SOPR crossed -0.2 today** → alert for next morning bearish entry
7. Write EOD recap

---

## Part 5: Current State (Feb 25, 2026)

### Market Snapshot

| Element | Value | Implication |
|---|---|---|
| MSTR | $135.18 | Up from $124 yesterday |
| BTC | $68,534 | Recovery from $62.5K Sunday low |
| SRI Stage | 4 (Day 187, record) | Longest Stage 4 in dataset |
| MVRV | 0.50 | Deep discount — most favorable ever |
| SRIBI | -49.86 | Negative, not yet crossing zero |
| FTL vs STL | Approaching from below (8H) | Cross imminent — watching |
| IV30 | 80.6% (83rd pctile) | Too rich for LEAPs; good for selling |
| GLI Z-score | -1.01 | Macro headwind active |
| STRS | 0.28 | Low — risk appetite building from depleted |
| SOPR | ~-0.13 | Negative but above -0.2 |
| STRC | $99.96 | At par — credit healthy |
| STRF | $100.80 | Above par — no fixed income stress |
| STRK | $80.87 | Deep discount — equity recovery not priced |
| SCHI | -5.43 | Mild stress (STRK-driven, not credit) |

### Active Bucket Status

| Bucket | Status | Next Trigger |
|---|---|---|
| **1 — Directional** | **WATCHING** — FTL approaching STL on 8H | FTL crosses STL → start robust fit clock |
| **2 — Spreads** | **ACTIVE** — IC Apr 17 executing; CCs on 3K shares | Manage at SRI levels |
| **3 — LEAPs** | **INACTIVE** — 0/4 primary triggers | Stage 1 confirmed + IV < 60% |

### Portfolio (Greg)

| Position | Details | Status |
|---|---|---|
| 3,000 MSTR shares | @ $128.59 ($385,770) | Holding |
| 20x $140C Mar 20 | Sold ~$5.25 | Winning (stock below strike) |
| 10x $150C Mar 20 | Sold ~$2.94 | Winning |
| IC Apr 17 $105/$95P + $145/$155C | Target $4.50 credit | Executing |
| Cash | ~$4.61M | Ready for deployment |

### Five-Trigger System for Stage 1

| # | Trigger | Status |
|---|---|---|
| 1 | MSTR > $135 with volume > 2x ADV | ⚠️ AT THE LINE ($135.18) |
| 2 | STRK > $85 | ❌ $80.87 |
| 3 | SRIBI crosses zero | ❌ -49.86 |
| 4 | GLI Z-score > -0.7 | ❌ -1.01 |
| 5 | BTC > $72K | ❌ $68,534 |

**0 of 5 confirmed. 1 approaching.**

---

## Part 6: Risk Parameters

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
| No naked short calls | Without Greg's explicit approval |
| No earnings week trades | Without discussion |

---

## Part 7: Backtesting Appendix

### Data Sources
- Gavin's TradingView SRI exports via GitHub (github.com/3ServantsP35/Grok)
- MSTR daily: 1,300 rows (Nov 2020 – Jan 2026)
- MSTR 4H: 1,247 rows (Jul 2023 – Jan 2026)
- BTC daily: 1,650 rows (Jul 2021 – Jan 2026)
- IBIT daily: 510 rows (Jan 2024 – Jan 2026)
- Additional: QQQ, GLD, DXY CSVs available (not yet backtested)

### Bullish Signal: FTL Crosses Above STL

**MSTR Daily (9 significant, 20+ days below):**
- Fast robust ≤10d: best trades, robust ≤7d especially strong
- Slow robust >10d: negative avg returns
- Red cross timing: avg 26d after FTL cross, avg +13.6% price move
- Bimodal robust distribution: ~7-11d (winners) or ~60-90d (losers)

**MSTR 4H (10 significant, 5+ days below):**
- Fast robust ≤5d (n=8): 5d +7.1%, 10d +10.4%, 20d +16.6%, 63% win
- Slow robust >5d (n=2): 5d -10.7%, 10d -12.0%
- Retest held (n=5): 20d +36.7%
- Retest failed (n=5): 20d -6.2%
- All retested within avg 2 days
- Day 1 avg -2.7% (don't chase)

**BTC Daily (6 significant, 15+ days below):**
- 20d avg +6.8%, win rate 83%
- 60d avg +20.7%, win rate 83%
- More reliable than MSTR but lower magnitude
- Fast robust less discriminating on BTC (slow robust still works)

**IBIT vs MSTR (5 crossovers during IBIT era):**
- MSTR raw: 20d avg +38.9%, 30d avg +48.9%
- IBIT raw: 20d avg +15.7%, 30d avg +13.9%
- IBIT risk-adjusted wins at 20d+ (0.75 vs 0.71, 0.92 vs 0.75 at 60d)
- Win rates identical: 80% at 20d

### Bearish Signal: FTL Crosses Below STL (Contra-Indicator)

**MSTR Daily (12 significant):**
- 5d avg **+7.1%** — price goes UP after bearish cross
- 67% bull win rate at 5d
- Confirms SRI bullish bias — do NOT use for bearish entries

### Bearish Signal: STH-SOPR < -0.2

**MSTR Daily (7 instances):**
- 5d: avg -10.7%, **100% bear (7/7)**
- 10d: avg -12.6%, 71% bear
- 20d: avg -13.2%, 71% bear
- 30d: avg -14.8%, 86% bear

### Bearish Confirmation: STRS Falling Fast (>0.10 in 5d)

**MSTR Daily (6 instances):**
- 20d: avg -4.9%, 83% bear

### Regime Indicator: Risk Oscillator

**BTC Daily (crossing below -0.15, 20 instances):**
- 20d: avg +0.7%, 55% bear — coin flip, NOT a directional signal
- Value: regime context only

### Regime Context: STRS Level

**MSTR Daily (1,300 rows):**
- < 0.25: 20d avg -1.8%, 58% bear — risk depleted, selloff late-stage
- 0.35-0.50: 20d avg +10.7%, 42% bear — healthy risk, sweet spot
- > 0.65: 20d avg +26.4%, 36% bear — euphoria, rare

---

## Part 8: Future Work (Backlog)

| Priority | Item | Status |
|---|---|---|
| 1 | **Multi-asset rotation framework** — Build SRI ladder for QQQ, GLD, TLT, TSLA, XLE using Gavin's GitHub CSVs. Triggered when STRS regime indicates depleted BTC/MSTR risk appetite. | Backlog |
| 2 | **Bearish engine hardening** — Year-long objective. Add more SOPR/STRS crossover events. Backtest Risk Oscillator with more data. Integrate STRS-specific exports from Gavin. Target: production-ready by Stage 3 of next cycle. | Active (ongoing) |
| 3 | **STRS regime rotation threshold** — Derive empirically from data (not estimated). Define exact STRS level + duration that triggers "look elsewhere." | Backlog |
| 4 | **Preferred stock data pipeline** — `collect_preferred.py` written and tested. Needs cron deployment by Greg. | Ready for deploy |
| 5 | **FTL/STL three-tier framework in production** — Integrate crossover monitoring, robust fit clock, retest detection into Morning Brief automation. | In progress |
| 6 | **Bearish side of BTC validation** — Run SOPR/STRS backtests on BTC data (currently done on MSTR only). | Next |
| 7 | **IBIT options liquidity analysis** — Compare actual bid-ask spreads, OI, volume vs MSTR at various strikes/DTEs. Quantify the execution edge. | Backlog |

---

## Revision History

| Date | Version | Changes |
|---|---|---|
| 2026-02-25 | 1.0 | Initial framework. Backtested bullish SRI ladder, bearish SOPR/STRS, IBIT vs MSTR, Risk Oscillator. Three buckets defined. |

---

*Framework by Gavin (rizenshine5359) & CIO. Subject to revision as more signal events accumulate and backtests expand to additional assets.*
