# SRI-Based Trading Framework
**Version:** 1.0 | **Date:** 2026-02-25 | **Authors:** Gavin (SRI methodology), CIO (backtesting & options structure)
**Status:** Active — backtested against 5yr daily + 2.5yr 4H MSTR data

---

## Architecture

This framework nests three strategy buckets within a unified SRI signal layer. Each bucket has its own entry/exit triggers, position sizing, and time horizon — but all share the same underlying SRI confirmation ladder.

```
┌─────────────────────────────────────────────────────┐
│              SRI CONFIRMATION LADDER                  │
│   (FTL/STL crossover → robust fit → retest → red)   │
├──────────────┬──────────────────┬────────────────────┤
│  BUCKET 1    │    BUCKET 2      │     BUCKET 3       │
│  Short-Term  │    Spreads       │     LEAPs          │
│  Calls/Puts  │    Income        │     Long-Term      │
│  Days-Weeks  │    Quarterly     │     6-12+ Months   │
├──────────────┼──────────────────┼────────────────────┤
│  Directional │  Premium Selling │  Leveraged Delta   │
│  ATM/OTM     │  At Reversals    │  Deep ITM/ATM      │
│  30-45 DTE   │  30-60 DTE       │  180-365 DTE       │
│  High gamma  │  High theta      │  High vega         │
└──────────────┴──────────────────┴────────────────────┘
```

---

## The SRI Confirmation Ladder

### The Sequence (backtested)

| Step | Event | Avg Timing (from Step 1) | What It Means |
|---|---|---|---|
| 1 | Green resistance line gaps / FTL approaches STL | Day 0 | First sign of reversal attempt |
| 2 | Price overtakes STL | Day 0-3 | Price leads the indicators |
| 3 | FTL turns green and slopes up | Day 1-5 | Momentum shifting |
| 4 | **FTL crosses above STL** | Day 3-10 | **Primary signal — start the clock** |
| 5 | Price retests STL as support | Day 5-13 (avg 2d after Step 4) | **Critical validation — hold/fail determines everything** |
| 6 | Robust fit line crosses STL | Day 7-20 (avg 5d after Step 4) | **Speed determines signal quality** |
| 7 | Red support line overtakes STL / STL turns up | Day 15-40+ | **Take-profit signal — most of the move is done** |

### The Speed Rule (backtested, n=19 across daily + 4H)

**The speed at which the ladder completes predicts whether the signal is real.**

| Robust Fit Timing | Classification | Avg 20d Return | Win Rate | Action |
|---|---|---|---|---|
| ≤5 days after FTL cross | **FAST — genuine transition** | +16.6% to +36.7% | 63-80% | Go long |
| 5-10 days | **MODERATE — possible** | +10-15% | ~55% | Reduce bearish, wait |
| >10 days | **SLOW — likely bear trap** | -6% to -12% | <50% | Sell the rip |
| Never (>50 days) | **FAILED** | -25% to -68% | ~20% | Full defensive |

### The Retest Rule (backtested, 4H data, n=10)

Every FTL/STL crossover produces a retest within ~2 days. The outcome:

| Retest Result | Avg 20d Return | Action |
|---|---|---|
| **Held** (price stays within 3% of STL) | **+36.7%** | Confirm long positions |
| **Failed** (price closes >3% below STL) | **-6.2%** | Close longs, treat as trap |

### The Red Cross = Exit Signal (backtested, daily data)

- Avg price move at time of red line crossing STL: **+13.6%**
- Range: -6% to +28%
- After red cross, returns flatten or reverse
- **The red cross marks the peak of the initial thrust, not the beginning**

### MVRV Filter (backtested)

| MVRV at Crossover | Signal Quality |
|---|---|
| < 1.0 | Highest quality — deep discount, spring-loaded (Jan 2023 +44%, Sep 2024 +158%) |
| 1.0 - 1.5 | Good — standard recovery signals |
| 1.5 - 2.0 | Caution — mid-cycle, could be bear rally |
| > 2.0 | Dangerous — overextended (Apr 2021 at 2.57 → -45% in 30d) |

**Current MVRV: 0.50 — the most favorable in the entire dataset.**

### VL Timeframe Override Rule

At extreme readings (record Stage 4, MVRV deep discount):
- **VL (2D) SRI lags by definition** — it cannot confirm until the move is 30-50% complete
- Shorter TFs (4H, 1D) lead at cycle bottoms
- Do NOT require VL confirmation for Bucket 1 or 2 entries
- VL confirmation triggers Bucket 3 (LEAP) entries

---

## BUCKET 1: Short-Term Directional (Calls/Puts)

### Purpose
Capture 5-30 day directional moves at SRI inflection points using long calls or puts.

### Entry Triggers

#### LONG CALLS — Bullish Inflection

**Tier 1 Entry (highest conviction):**
All conditions met:
- [ ] FTL crosses above STL (Step 4)
- [ ] Robust fit crosses STL within 5 days (Step 6 — FAST)
- [ ] Price retests STL and holds (Step 5 — HELD)
- [ ] MVRV < 1.5
- [ ] SRIBI positive or crossing zero
- [ ] Preferred credit healthy (STRC > $97, STRF > $97)

*Backtest: 20d avg +36.7%, 80% win rate*

**Tier 2 Entry (moderate conviction):**
Two of first three conditions met:
- [ ] FTL crosses above STL
- [ ] Robust fit crosses within 5 days OR retest holds (not both)
- [ ] SRIBI improving (trending toward zero from below)

*Backtest: 20d avg +16.6%, 63% win rate*

**Tier 3 — NO ENTRY:**
Robust fit takes >10 days and/or retest fails → bear trap

#### LONG PUTS — Bearish Inflection (USE WITH CAUTION)

**Backtested finding: Bearish FTL/STL crosses are unreliable for MSTR puts.**
- 12 significant bear crosses: only 33% produced downside at 5d, 42% at 20d
- MSTR's structural upward bias (BTC + Saylor) creates frequent bear traps
- Avg return 5d after bear cross: +7.1% (price goes UP)

**Only enter puts when ALL of the following are met:**
- [ ] FTL crosses below STL from above
- [ ] MVRV > 2.0 (overextended — only bear crosses above 2.0 produced sustained declines)
- [ ] STRC < $97 (credit stress confirming — structural, not just technical)
- [ ] GLI Z-score < -0.5 (macro headwind)
- [ ] Robust fit crosses below STL within 5 days

**Preferred use of bear crosses:** Close Bucket 1 longs, add/maintain Bucket 2 BCS. NOT as triggers for long puts.

### BTC Cross-Validation (backtested, n=6)

BTC bullish FTL/STL crosses show **higher win rates but smaller moves** vs MSTR:
- 20d: avg +6.8%, 83% win rate (vs MSTR +15.2%, 44%)
- 60d: avg +20.7%, 83% win rate (vs MSTR +7.4%, 33%)
- BTC signals are more reliable; MSTR signals have more noise from beta amplification
- Use BTC crossover as **confirmation** for MSTR entries: both crossing = highest conviction

### Position Structure

| Element | Specification |
|---|---|
| **Instrument** | Long calls or puts (not spreads) |
| **Strike** | ATM to 5% OTM |
| **DTE** | 30-45 days (enough time for the move, limits theta burn) |
| **Size** | 2-5% of portfolio per trade |
| **Entry timing** | Day 2-5 after FTL cross, AFTER retest — never chase the cross itself |

### Exit Rules

| Trigger | Action |
|---|---|
| **Red line crosses STL** (Step 7) | Close 50-75% of position |
| **50% profit** | Close 50%, trail remainder |
| **Robust fit stalls** (>10 days, no cross) | Close entire position — reclassify as trap |
| **Retest fails** (price closes >3% below STL) | Close immediately — stop loss |
| **Time stop: 21 DTE remaining** | Close or roll if thesis intact |
| **STRC breaks $97** | Close all bullish positions regardless |

### Day-of Execution Timing (from 4H backtest)

| Day After Cross | Avg Return | Action |
|---|---|---|
| Day 1 | -2.7% | **Do not enter.** Shakeout / gap fill common. |
| Day 2 | +1.4% | Retest typically begins. Watch for hold. |
| Day 3-5 | +3.6% | **Entry zone** — if robust crossed and retest held |
| Day 10 | +5.9% | Move accelerating — too late for initial entry |
| Day 20 | +15.2% | Approaching red cross exit zone |

---

## BUCKET 2: Spread Income (Quarterly Premium Selling)

### Purpose
Generate consistent income by selling premium at key SRI reversal points, primarily through credit spreads (bull put spreads, bear call spreads, iron condors). Target: capture theta decay during range-bound or trending periods identified by SRI stage.

### Stage-Based Strategy Selection

| SRI Stage | Primary Strategy | Rationale |
|---|---|---|
| **Stage 4 (Markdown)** | Sell bull put spreads + bear call spreads / iron condors | Sell into fear; elevated put skew pays outsized premium |
| **Stage 4→1 Transition** | Shift from neutral to bullish spreads; close BCS, widen BPS | Transition emerging; reduce bearish exposure |
| **Stage 1 (Accumulation)** | Aggressive bull put spreads; sell cash-secured puts | Bottoming confirmed; collect premium while building share position |
| **Stage 2 (Markup)** | Sell covered calls + bear call spreads on rallies | Ride the trend; sell premium on overextensions |
| **Stage 3 (Distribution)** | Shift to protective; buy put spreads, sell call spreads | Topping signals; reduce bullish exposure |

### Entry Triggers — Spreads at Reversals

**Bull Put Spreads (selling puts below support):**
- [ ] SRI Stage 4 with SELL_PUT window OPEN
- [ ] Put skew > 70th percentile (rich premium)
- [ ] Short strike below key SRI support level (Fast TL or tested support)
- [ ] mNAV < 1.3x (discount regime)
- [ ] Preferred credit healthy (STRC > $97)
- [ ] **Enhanced entry:** FTL approaching STL from below (pre-crossover) + credit divergence

**Bear Call Spreads (selling calls above resistance):**
- [ ] SRI Stage 4 or Stage 3 with declining STL
- [ ] Short strike above STL or declining resistance level
- [ ] All MAs bearishly aligned (death cross active)
- [ ] GLI Z-score < -0.5 (macro headwind)

**Iron Condors (selling both sides):**
- [ ] Stage 4 range-bound consolidation
- [ ] IV > 70th percentile (rich premium both sides)
- [ ] Put wing below FTL/support, call wing above STL/resistance
- [ ] Width = SRI-defined support-to-resistance range

### Position Structure

| Element | Specification |
|---|---|
| **Instrument** | Credit spreads ($10 wide standard) |
| **DTE** | 30-60 days (sweet spot for theta/gamma balance) |
| **Size** | Max $50K risk per position, 8 positions max |
| **Minimum R/R** | 25% for single spreads, 50%+ for iron condors |
| **Minimum PoP** | 65% (from ORATS or estimated) |

### SRI-Enhanced Spread Management

| SRI Event | Spread Action |
|---|---|
| **FTL crosses above STL (Step 4)** | Close all bear call spreads within 2 days |
| **Robust fit crosses within 5d (FAST)** | Close remaining BCS, shift to BPS |
| **Retest holds** | Add BPS at new STL support level |
| **Retest fails** | Close BPS, add BCS — reversal failed |
| **Red line crosses STL** | Take profit on BPS (50-75% of remaining) |
| **STRC < $97** | Close all BPS immediately — credit stress |
| **STRK > $85 with volume** | Stage 1 candidate — maximum BPS allocation |
| **Stage transition confirmed** | Rotate entire spread portfolio to new stage strategy |

### Quarterly Income Cycle

| Month of Quarter | Action |
|---|---|
| Month 1 | Open new spread positions at SRI levels. Target 4-6 positions. |
| Month 2 | Manage: take profits at 50%, roll winners, close losers at stop |
| Month 3 | Expiration management: close, roll, or let expire. Prepare next quarter's levels. |

### Kill Conditions (Spread-Specific)

| Condition | Action |
|---|---|
| Portfolio loss > $50K unrealized | Close weakest 2 positions |
| Any single position at max loss | Close, do not add |
| BTC < $60K (current cycle) | Close all put spreads |
| MSTR gap > 10% against position | Reassess; close if SRI confirms direction |
| IV crush > 20 vol pts | Re-evaluate all positions for reduced premium |

---

## BUCKET 3: LEAPs (Long-Term Leveraged Positioning)

### Purpose
Maximize long-term capital appreciation through leveraged delta exposure during confirmed Stage 1→2 transitions. LEAPs provide 3-5x notional leverage with defined risk and no margin calls.

### Entry Triggers — ALL REQUIRED (2-3 of 4 minimum)

LEAPs are the highest-conviction, largest-capital deployment. Entry requires multi-timeframe + macro + credit confirmation.

**Primary Triggers (need 2-3):**
- [ ] SRI confirms Stage 1 on daily TF (5+ consecutive days)
- [ ] GLI Z-score > -0.5 (macro headwind removed)
- [ ] IV30 < 60% (cheap options — don't buy rich LEAPs)
- [ ] BTC breaks 200-day MA with volume

**Confirmation Triggers (strengthen conviction):**
- [ ] VL (2D) SRI begins cupping — VL confirmation is the LEAP signal (unlike Bucket 1/2 where VL lags)
- [ ] STRK > $85 with sustained volume (equity market pricing recovery)
- [ ] MVRV crosses above 1.0 (hard gate cleared)
- [ ] SRIBI > +20 on daily and 2D timeframes
- [ ] MSTR/BTC/STRC ratio breaks above 0.22 (cup & handle breakout)
- [ ] GLI Z-score > 0 (macro tailwind)

**Current status: 0 of 4 primary triggers met. $0 LEAP allocation.**

### Why VL Confirmation Matters Here

For Bucket 1 (short-term), we proved VL lags at bottoms — waiting for VL costs you the first 30-50% of the move. But for LEAPs:
- You're deploying large capital ($500K-$1M)
- 6-12 month time horizon means you need the *trend*, not the *turn*
- VL confirmation means the trend has been established, reducing risk of a bear trap
- Missing the first 30% of the move is acceptable when you're leveraged 3-5x on the remaining 70%

### Position Structure

| Element | Specification |
|---|---|
| **Instrument** | Long calls, deep ITM to ATM |
| **Strike** | ATM or up to 20% ITM (delta 0.60-0.80) |
| **DTE** | 180-365 days (minimum 180) |
| **Size** | Up to $1M total allocation (Greg); up to $200K (Gavin) |
| **Scaling** | 25% at first trigger cluster, 25% at Stage 1 confirmation, 50% at Stage 2 confirmation |

### LEAP Entry Timing Relative to SRI Ladder

```
Stage 4 ──────────────────────── Stage 1 ──────── Stage 2
    │                                │                │
    │  Bucket 1: Enter here          │                │
    │  (FTL cross, Day 2-5)          │                │
    │                                │                │
    │  Bucket 2: Active throughout   │  Shift to      │  Sell covered
    │  (spreads at SRI levels)       │  bullish BPS   │  calls on LEAPs
    │                                │                │
    │                                │  Bucket 3:     │  Bucket 3:
    │                                │  25% entry     │  Add 50%
    │                                │  (Stage 1      │  (Stage 2
    │                                │  confirmed)    │  confirmed)
```

### LEAP Management

| Event | Action |
|---|---|
| **Stage 1 confirmed (5+ days)** | Enter first 25% tranche |
| **Stage 2 confirmed** | Add 50% tranche; begin selling covered calls against LEAPs |
| **GLI Z-score crosses above 0** | Add final 25% — macro tailwind confirmed |
| **Stage 2→3 transition begins** | Close 50% of LEAPs; convert remainder to spreads |
| **Stage 3 confirmed** | Close all LEAPs |
| **IV spike > 90th percentile** | Do NOT buy LEAPs — wait for IV normalization |
| **STRC < $97 during hold** | Hedge with protective puts, do not close LEAPs yet |
| **BTC breaks below 200-day MA** | Close 50% LEAPs, reassess |

### LEAP Strike Selection by IV Regime

| IV30 Percentile | Strike Guidance |
|---|---|
| < 30th | Buy ATM or slightly OTM — cheap vol, maximize leverage |
| 30th-50th | Buy ATM — balanced cost/leverage |
| 50th-70th | Buy 10-20% ITM — reduce vega exposure |
| > 70th | **Do not buy LEAPs** — sell premium instead (Bucket 2) |

---

## Cross-Bucket Coordination

### Capital Allocation by Stage

| Stage | Bucket 1 (Directional) | Bucket 2 (Spreads) | Bucket 3 (LEAPs) | Cash |
|---|---|---|---|---|
| **Stage 4 (current)** | 0-5% | 10-20% | 0% | 75-90% |
| **Stage 4→1 Transition** | 5-10% | 15-25% | 0% | 65-80% |
| **Stage 1 Confirmed** | 5-10% | 20-30% | 10-25% | 35-65% |
| **Stage 2 Confirmed** | 0-5% | 20-30% | 25-50% | 15-55% |
| **Stage 3 (Distribution)** | 5-10% (puts) | 15-25% (bearish) | 0% (closed) | 65-80% |

### Signal Cascade

When a Bucket 1 signal fires (FTL cross → fast robust → retest held):
1. **Bucket 1:** Enter directional calls immediately (Day 2-5)
2. **Bucket 2:** Close all bear call spreads within 2 days; shift spread portfolio bullish
3. **Bucket 3:** Begin monitoring LEAP triggers — no action yet until Stage 1 confirmed

When a Bucket 1 signal fails (slow robust / retest failure):
1. **Bucket 1:** Close directional longs, enter puts if breakdown confirmed
2. **Bucket 2:** Maintain or increase bear call spreads; close aggressive BPS
3. **Bucket 3:** No change — LEAP triggers remain unmet

### Preferred Stock Integration (All Buckets)

| Preferred Signal | Bucket 1 | Bucket 2 | Bucket 3 |
|---|---|---|---|
| STRC < $97 | Close all longs | Close all BPS | Do not enter LEAPs |
| STRF < $97 | Close all longs + add puts | Close all BPS + add BCS | Close any existing LEAPs |
| STRK > $85 w/vol | Add to longs | Maximum BPS allocation | Stage 1 confirmation candidate |
| Credit divergence (credit healthy + equity falling) | Tier 1 long signal | Aggressive BPS entry | Monitor — not yet |

---

## Monitoring & Daily Routine

### Pre-Market (8:00 AM ET)

1. Check SRI ladder status: Where are we in Steps 1-7?
2. Check preferred spread: STRC, STRF, STRK levels
3. Check MVRV, SRIBI, GLI Z-score
4. Identify: Is any bucket trigger approaching?
5. If FTL cross is active: count days since cross, check robust fit progress

### Intraday Checkpoints

| Time | Check |
|---|---|
| 9:45 AM ET | Opening range — did STL hold as support/resistance? |
| 12:00 PM ET | Midday — robust fit progress, retest status |
| 3:30 PM ET | Power hour — any SRI level breaks? Closing positions? |

### Post-Market (4:30 PM ET)

1. Update SRI ladder progress
2. Score any active Bucket 1 trades: which step are we on?
3. Check preferred stock closing levels
4. Update hypothesis tracking on all open positions
5. If red line crossed STL today → trigger Bucket 1 exit process

---

## Current State (Feb 25, 2026)

| Element | Status |
|---|---|
| **SRI Stage** | 4 (Day 187, record) |
| **MVRV** | 0.50 (deep discount — most favorable in dataset) |
| **FTL vs STL** | FTL approaching STL from below on 8H — cross imminent |
| **Robust fit** | Below STL — clock not started |
| **SRIBI** | -49.86 (negative, not yet crossing zero) |
| **GLI Z-score** | -1.01 (macro headwind active) |
| **Preferred** | STRC $99.67, STRF $100.35 — credit healthy |
| **STRK** | $78.82 — equity recovery not priced |
| **IV30** | 80.6% (83rd pctile) — too rich for LEAPs |

### Active Bucket Status

| Bucket | Status | Next Trigger |
|---|---|---|
| **1 (Directional)** | **Watching** — FTL approaching STL on 8H | FTL crosses STL → start clock |
| **2 (Spreads)** | **Active** — IC Apr 17 $105/$95P + $145/$155C executing | Manage at SRI levels |
| **3 (LEAPs)** | **Inactive** — 0 of 4 primary triggers met | Stage 1 confirmation + IV < 60% |

---

## Backtesting Appendix

### Daily Data (MSTR, Nov 2020 – Jan 2026, n=1,300)

**Significant FTL > STL crossovers (20+ days below): 9 instances**
- Fast robust (≤10d): avg 20d return varies; best trades had robust ≤7d
- Slow robust (>10d): avg 20d returns negative
- Red line cross avg timing: 26 days after FTL cross
- Price move at red cross: avg +13.6%, range -6% to +28%

### 4H Data (MSTR, Jul 2023 – Jan 2026, n=1,247)

**Significant FTL > STL crossovers (5+ days below): 10 instances**
- Fast robust (≤5d): n=8, avg 5d +7.1%, 10d +10.4%, 20d +16.6%
- Slow robust (>5d): n=2, avg 5d -10.7%, 10d -12.0%
- Retest held: n=5, avg 20d +36.7%
- Retest failed: n=5, avg 20d -6.2%
- All crossovers had a retest within avg 2 days
- Day 1 after cross avg -2.7% (don't chase)
- Optimal entry: Day 2-5 after cross, post-retest confirmation

### Source Data
- Gavin's TradingView Pine Script SRI indicators exported via GitHub (github.com/3ServantsP35/Grok)
- MSTR daily: `BATS_MSTR, 1D_d2e5e.csv` (1,300 rows)
- MSTR 4H: `BATS_MSTR, 240_2de8a.csv` (1,247 rows), `BATS_MSTR, 240_b91b5.csv` (2,401 rows)

---

*Framework by Gavin (rizenshine5359) & CIO. Backtested against 5+ years of MSTR data with Gavin's SRI indicator values. Subject to revision as more crossover events are observed.*
