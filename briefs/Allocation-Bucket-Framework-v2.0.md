# Allocation Bucket Framework v2.0 — Multi-Asset Rotation
**Date:** February 27, 2026  
**Authors:** Gavin (framework lead) + CIO  
**Status:** APPROVED by Gavin — awaiting Greg review  
**Supersedes:** Four-Bucket Framework v1.2.1  
**Architecture Reference:** MSTR Engine Architecture v1.0

---

## What Changed from v1.x

v1.x treated AB1-3 as MSTR/IBIT buckets with alternatives confined to AB4. Backtesting revealed this leaves capital idle 88% of the time (MSTR CT4 = 247 of 2,096 days).

**v2.0 principle: Every asset competes for every bucket based on Concordance Tier signal quality.** The best signal wins the allocation. This increases:
- **Coverage:** 12% → 73-80% of trading days have an actionable signal
- **Win rate:** 56% → 64% blended (quality assets pull up the average)
- **Consistency:** Always deployed somewhere rather than waiting for one asset

---

## The Four Allocation Buckets

### AB1 — Directional (Trend Capture)

**Objective:** Capture sustained moves in trending assets.  
**Risk profile:** Highest. Full directional exposure. Sized for drawdowns.

| Asset Pool | CT Gate | Instrument | Why This Gate |
|---|---|---|---|
| BTC (via IBIT) | CT4 | Shares, calls | 64% win, +8.94% avg, 2.16x skew |
| MSTR | CT4 | Shares, calls | 58% win, +17.22% avg (post-BTC strategy) |
| TSLA | CT4 | Shares, calls | 60% win, +7.32% avg |
| SPY | CT3+ | Shares, calls | 70% win, +0.73% avg |
| QQQ | CT3+ | Shares, calls | 67% win, +1.08% avg |
| GLD | CT3+ | Shares, calls | 62% win, +1.58% avg |

**Why two tiers of gates:**
- Risk assets (BTC, MSTR, TSLA) require CT4 because their win rates at CT3 are ~55% — too close to coin flip for directional risk.
- Quality assets (SPY, QQQ, GLD) sustain 62-70% win rates at CT3+ — acceptable for directional with smaller sizing.

**Vehicle selection within MSTR/IBIT:**
- Default: IBIT (better risk-adjusted at 60d historically)
- Switch to MSTR calls when: MSTR/IBIT ratio VST AND ST are bullish (premium expanding)

**Regime gate:** AB1 requires RP2+ for risk assets (BTC, MSTR, TSLA). Quality assets (SPY, QQQ, GLD) may enter AB1 in RP1 if at CT3+ — their structural win rates (62-70%) justify deployment without regime confirmation.

**Current state:** GLD is CT4 (+41 SRIBI) — eligible for AB1 as a quality asset even in RP1. TLT is CT4 but AB4-only (negative directional EV).

### AB2 — Spreads (Income + Defined Risk)

**Objective:** Generate consistent income through premium selling with defined max loss.  
**Risk profile:** Moderate. Capped upside, capped downside. Win rate is the key metric.

| Direction | Asset Pool | Signal Gate | Strategy |
|---|---|---|---|
| **Bull put spreads** | MSTR | CT2+ (any state — mean-reversion) | Sell OTM puts, buy further OTM |
| **Bull put spreads** | SPY, QQQ | CT3+ | Sell OTM puts |
| **Bear call spreads** | MSTR, IBIT | BT-Distribution, BT-Trap, BT-BC6 | Sell OTM calls |
| **Iron condors** | MSTR | CT2+ AND no BT active | Both sides |

**MSTR-specific rule (CODIFIED):** MSTR delivers +6.94% at 20d even when all SRIBI are negative (post-BTC strategy). AB2 bull put spreads on MSTR are valid in ANY concordance state. The mean-reversion is structural.

**Bear spread triggers (from backtest):**

| Trigger | Signal | MSTR 20d | Bear% | DTE |
|---|---|---|---|---|
| BT-Distribution | SOPR<-0.2 + SRIBI mixed/pos + STRS>0.35 | -4.10% | 60% | 21-30 |
| BT-Trap | 1/4 or 3/4 breadth + SOPR<0 | -2.53% | 61% | 14-21 |
| BT-BC6 | FTL<STL + SRIBI≥10 + STRS falling | -11.55% (40d) | 53% | 45-60 |

**BT3 Capitulation Override:** When ALL SRIBI are negative, all bear signals are BLOCKED. That's a buy, not a sell.

**Regime considerations:**
- RP1: Bull put spreads only (bearish regime → don't sell calls unless BT triggered)
- RP3+: Full condor eligible
- RP4×BC6: Bear call spreads primary (exit signal confirmed)

### AB3 — LEAPs (Long-Term Appreciation)

**Objective:** Leveraged long-term exposure at structurally attractive entry points.  
**Risk profile:** High notional, long duration. Requires patience.

| Asset Pool | Entry Gate | Instrument |
|---|---|---|
| MSTR | Path B: RP1 + MVRV < 0.8 + STRC > $97 + DTE ≥ 12mo | Deep OTM calls, 10-20% OTM |
| MSTR | Standard: CT3+ AND RP3+ | ATM-10% calls, 9-18mo |
| TSLA | CT4 AND RP3+ | ATM-10% calls |
| BTC (via IBIT options) | CT4 AND RP3+ | ATM calls |

**Path B (current — active):** RP1 + MVRV at 0.50 (deepest ever) + STRC $100 (healthy). Small position sizing (25% of LEAP budget), wide strikes.

**Standard path:** Wait for CT3+ AND RP3+. This is the high-confidence LEAP entry.

### AB4 — Cash & Rotation (Capital Preservation)

**Objective:** Preserve capital and earn risk-free yield while waiting for signals.  
**Risk profile:** Lowest. Capital preservation is primary.

| Instrument | When | Yield |
|---|---|---|
| **STRC** | Default cash position | ~10% annual (0.83%/month) |
| **GLD** | CT3+ in any RP (macro hedge) | Variable |
| **TLT** | Rates falling + CT3+ | Variable |

**STRC is the cash default.** Idle capital earns 0.83%/month. Every AB1/AB2 trade must exceed this hurdle or capital stays in STRC.

**TLT exclusion from AB1-3:** TLT at CT4 delivers -0.08% at 20d with 41% win rate. It does NOT belong in directional or spread buckets. Its role is AB4 only — macro hedge when rates are falling.

---

## Multi-Asset Rotation Rules

### Daily Process

1. **Compute CT for every asset** in the pool (BTC, MSTR, SPY, QQQ, GLD, TSLA)
2. **Check regime** (RP phase, BC phase)
3. **Apply gates:** Which assets qualify for which buckets?
4. **Rank qualified assets** by SRIBI avg (highest conviction first)
5. **Allocate** per Regime Allocation Map, filling from highest-rank down
6. **Check STRC hurdle:** Does expected return exceed 0.83%/month?
7. **Check bear triggers:** Any BT signals active? Override accordingly.

### Asset Selection Priority

When multiple assets qualify for the same bucket:

**AB1 (directional):** Pick the highest SRIBI avg among qualified assets. Higher SRIBI = stronger trend = better directional entry.

**AB2 (spreads):** MSTR is always the primary AB2 vehicle (highest IV = richest premiums, strongest mean-reversion). SPY/QQQ are secondary when MSTR IV is at 30th percentile or below.

**AB3 (LEAPs):** Only enter when Path B or Standard gate is met. No rotation — this is a strategic position, not tactical.

**AB4 (cash):** STRC default. Rotate to GLD/TLT only with explicit CT signal.

### What This Means Today (Feb 27, 2026)

| Asset | CT | SRIBI Avg | Eligible Buckets |
|---|---|---|---|
| **GLD** | **CT4** | **+41** | AB4 (macro hedge). AB1 blocked by RP1 gate — *pending Gavin decision* |
| **TLT** | CT4 | +38 | AB4 only (negative directional EV) |
| MSTR | CT0 | -5 | AB2 bull puts (mean-reversion rule), AB3 Path B |
| SPY | CT0 | -11 | None |
| QQQ | CT0 | -12 | None |
| TSLA | CT0 | -15 | None |
| BTC | CT0 | -48 | None |

**Active trades available today:**
1. **AB2:** MSTR bull put spreads (structural mean-reversion, any CT state)
2. **AB3:** MSTR LEAPs via Path B (RP1 + MVRV 0.50 + STRC healthy)
3. **AB4:** STRC (cash), GLD (CT4 macro hedge)

---

## Regime Allocation Map v2.0

Allocations now reflect multi-asset rotation. "AB1 15%" means 15% to the best-signal directional asset, not necessarily MSTR.

| RP × BC | AB1 | AB2 | AB3 | AB4 |
|---|---|---|---|---|
| **RP1 × BC1** (current) | 0% | 15-20% (MSTR puts) | 5-8% (Path B) | 72-80% (STRC + GLD) |
| RP1 × BC2 | 0% | 15-20% | 10-15% | 65-75% |
| RP2 × BC3 | 10-15% (best CT3+) | 15-20% | 15-20% | 45-60% |
| **RP3 × BC4** | **15-20%** (best CT4) | **20-25%** | **25-35%** | 20-40% |
| RP4 × BC5 | 5-10% | 10-15% | reduce | 65-80% |
| **RP4 × BC6** | 10-15% **bear spreads** | 5-10% | **close** | 65-80% |

---

## Performance Benchmarks

| Strategy | Trading Days | Win% | EV/20d | vs STRC |
|---|---|---|---|---|
| MSTR-only CT4 (v1.x) | 247 (12%) | 56% | +14.96% | ✅ but rarely active |
| Best CT3+ rotation | 1,676 (80%) | 63% | +3.95% | ✅ and almost always active |
| Tiered rotation (quality CT3+, risk CT4) | 1,527 (73%) | **64%** | +3.44% | ✅ best risk-adjusted |
| STRC (cash baseline) | 2,096 (100%) | 100% | +0.83% | — (is the hurdle) |

**Tiered rotation is the recommended default.** 64% win rate, active 73% of days, every trade clears STRC hurdle. When risk assets hit CT4 (BTC, MSTR, TSLA), the system naturally concentrates into higher-return opportunities.

---

## Key Rules Summary

1. **Every asset competes for every bucket.** Best CT signal wins the allocation.
2. **Two-tier CT gates:** Quality assets (SPY, QQQ, GLD) enter at CT3+. Risk assets (BTC, MSTR, TSLA) enter at CT4.
3. **AB1 regime gate is tiered:** Risk assets (BTC, MSTR, TSLA) require RP2+. Quality assets (SPY, QQQ, GLD) can enter AB1 in any RP at CT3+.
4. **MSTR AB2 is always on** — mean-reversion is structural, any CT state.
5. **BT3 Capitulation overrides all bear signals** — when all SRIBI negative, it's a buy.
6. **STRC is the cash default.** Every trade must clear the **2%/month yield objective.** STRC at 0.83%/month is the floor, not the target.
7. **TLT is AB4 only** — negative directional EV despite CT signals.
8. **MSTR/IBIT vehicle selection** by ratio VST/ST: bullish ratio → MSTR, bearish → IBIT.

---

## Decisions (Closed — Feb 27, 2026)

1. **RP1 gate for quality assets:** ✅ APPROVED. GLD (and SPY, QQQ) at CT3+ are eligible for AB1 in any RP, including RP1. The RP gate only applies to risk assets (BTC, MSTR, TSLA).

2. **Position sizing:** The objective is **highest annual return while meeting a minimum 2% monthly yield threshold.** This is the codified investment objective. Position sizing should optimize for this target, not equal-weight. The 2% threshold may be revised. *(Note: replaces the prior STRC hurdle of 0.83%/month — the bar is now higher.)*

3. **Correlation management:** Guideline (not rule): **no single investment should represent more than 5% of total portfolio.** Acknowledged this may not always be achievable, but it's the design target.

4. **AB2 bear spread program:** ✅ APPROVED. ~6x/year is sufficient given STRC as the parking lot between signals. Cash earns the hurdle rate while waiting.

5. **Sector ETF expansion:** **NOT NOW.** Prove this setup works with the current 7-asset pool first. Expansion is a future consideration, not a priority.
