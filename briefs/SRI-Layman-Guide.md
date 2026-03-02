# SRI Options Engine — Layman's Guide
**Version 1.0 | March 5, 2026**
**Audience: Greg, Gavin, Gary**

---

## What This Is

This document explains *why* the MSTR Options Engine works the way it does — in plain language, without the code. Think of it as the pilot's briefing before the instrument panel.

The engine is not a stock-picking system. It's a **capital discipline framework**. It tells you when to be in, how much to put in, how to earn income while you wait, and when to get out. Every dollar you own is accounted for at every moment.

---

## The Four Buckets

Every dollar lives in exactly one of four buckets at all times. There is no gray area.

### 🟡 AB4 — The Waiting Room

This is where your money lives when it's not deployed. But unlike a regular savings account or money market fund, it actually pays you well: roughly **0.83% per month (~10% per year)** via STRC preferred stock — Saylor's preferred equity, senior to the common.

Think of AB4 as your *high-yield holding pen*. Capital doesn't leave here unless the trade you're entering is expected to beat that 0.83% monthly return. If nothing clears that bar, you stay put. You're not losing; you're earning.

**The rules:**
- A hard floor of **10% of the portfolio stays here as true cash, always.** This is sacred. It never moves, regardless of how good the signal looks.
- The soft ceiling is **25%**. If AB4 climbs above 25%, you have too much idle money — look harder for qualifying entries.
- Being 100% in AB4 is perfectly fine. We do not deploy capital just to feel busy.
- All preferred stocks (STRC, STRK, STRF) count as AB4. But only true cash (not preferreds) satisfies the 10% floor.

> **Analogy:** AB4 is like a hotel lobby — comfortable, productive, and you're earning while you wait. But the 10% hard floor is the emergency exit that never gets blocked. Ever.

---

### 🔵 AB3 — The Core Position

AB3 is the **long-term thesis bet**. When the system detects that an asset has become structurally cheap — not just down, but *deeply* below fair value — it signals an entry. You buy 2-year call options (called LEAPs — Long-term Equity AnticiPation Securities) when the market looks its worst and hold them through the full recovery cycle.

This is not a trade. This is a **position**. You hold through the noise, through the volatility, through the weeks when it doesn't look like it's working. Then you trim gradually as the market recovers, selling in four tranches: 25% at a time.

- **Baseline allocation: 50% of portfolio**
- Entries require a confirmed "Stage 2" bottom signal (more on this below)
- You don't diversify for diversification's sake. If the best signal is in MSTR and MSTR alone, that's where it goes.

> **Analogy:** AB3 is like buying a beach house when the news says a hurricane just left and everyone's scared. You paid a low price because others were panicking. You hold it until the neighborhood recovers, then sell pieces as the value climbs back.

---

### 🟢 AB1 — The Short-Term Bet

AB1 captures **breakout momentum**. When the system sees a pre-breakout setup — the asset is building pressure and multiple timeframe signals are aligning — it signals a short-term LEAP entry. You hold days to 90 days and ride the move.

- **Baseline allocation: 25% of portfolio**
- If the breakout doesn't materialize, the position doesn't get forced out. It simply gets reclassified as AB3 and held for the longer cycle.

> **Analogy:** AB1 is like betting on a horse that the pace figures say is primed to run. If it doesn't break, you don't shoot the horse — you just update your expectations.

---

### 🟠 AB2 — The Passive Income Layer

AB2 requires **no new capital**. It runs on top of your AB3 LEAPs.

Once you own the LEAPs, you can sell short-dated call options against them — 30 to 45 days out — collecting premium each month. This is called a **Poor Man's Covered Call (PMCC)**, essentially renting out your position to someone who wants to cap your upside temporarily in exchange for cash.

The target is **2–5% per month** of your LEAP cost basis. But — critically — the system only lets you do this when the timing is right. If we're still in accumulation mode, you don't sell calls. You preserve the upside. The gate only opens when the LOI (explained below) says conditions permit.

---

## The Signal Ladder — How We Decide When to Buy

The engine uses four stacked layers of analysis. Each layer must give the green light before the next one matters.

### Layer 0 — Global Liquidity (The Weather)

Is the global central bank environment expanding or contracting? Think of this as checking whether it's sunny or raining for risk assets worldwide. When the Fed, European Central Bank, and China's central bank are all printing and expanding their balance sheets, risk assets tend to rally. When they're tightening, the opposite.

A positive Global Liquidity Index (GLI) delays our exit signals — rallies tend to run further in good weather. A negative GLI makes us more cautious on new entries.

### Layer 1 — Regime (The Road Conditions)

Eight market inputs — including Bitcoin, interest rates, the dollar, credit spreads, and volatility — combine into a single **Regime Score** from -7 to +7. This tells us whether the overall market environment is risk-on, neutral, or risk-off.

- **Regime ≤ -2: No new positions. Period.** It doesn't matter what the other signals say.
- The regime score also picks the vehicle: MSTR vs. IBIT (a Bitcoin ETF), based on which is showing better momentum relative to BTC at any given time.

### Layer 2 — Signals (The Actual Buy/Sell Decisions)

The primary entry signal is the **LOI (LEAP Opportunity Index)** — think of it as a "structural cheapness" gauge. When it's deeply negative, the asset is cheap and it's time to accumulate. When it's highly positive, it's time to trim.

| LOI Reading | What It Means | Action |
|---|---|---|
| Below -45 (Momentum assets) | Deep value — accumulation zone | Stage 1 watch; prepare STRC for liquidation |
| Below -40 (mean-reversion assets) | Deep value — accumulation zone | Stage 1 watch |
| Above -20 | Recovery underway | Call-writing gate opens |
| Above +40 (Momentum: MSTR/TSLA) | Rich — trim zone | Sell closer-to-money calls; sell LEAP tranches |
| Above +20 (MR assets: SPY/QQQ) | Rich — trim zone | Sell closer-to-money calls; sell LEAP tranches |

Supporting the LOI is the **SRIBI** (Structural Regime Indicator — Breadth Index), which measures trend across four timeframes: very short-term, short-term, long-term, and very long-term (VST/ST/LT/VLT). The **CT Tier** (Conviction Tier, 0–4) counts how many of those four timeframes are trending positively. CT3/CT4 = high conviction.

### Layer 3 — Allocation (The Sizing)

Once the signal clears, the engine determines which bucket receives the capital and how much. In normal mode, no single asset gets more than 20% of the total portfolio. That soft cap lifts when AB4 is above 25% — because at that point you have too much idle cash and the better risk is being too conservative, not too concentrated.

---

## STRC: More Than Just a Parking Spot

STRC preferred stock is the **benchmark and staging area**. If a trade can't beat 0.83%/month, you shouldn't make it — you'd be better off doing nothing.

When the system moves to Stage 1 (accumulation zone detected), you begin **gradually** selling STRC to free up capital for the upcoming LEAP buy. You don't liquidate all at once — preferred stocks can be thinly traded intraday, and a forced liquidation on a Stage 2 signal would be clumsy and costly. The preparation happens slowly. The execution happens swiftly.

STRC also serves as a **health indicator**: if STRC's price drops below $97, it signals stress in Saylor's capital structure — and typically precedes weakness in MSTR. Your cash is doing double duty.

---

## The Full Cycle — Start to Finish

| Step | What Happens | Your Action |
|---|---|---|
| 1 | Cash earns ~10%/year in STRC | Hold, watch |
| 2 | LOI drops below -45/-40 (Stage 1) | Start gradually selling STRC |
| 3 | LOI confirms 2-bar bounce (Stage 2) | 🎯 **Buy 2-year LEAPs** |
| 4 | Hold through the recovery | No calls yet — preserve upside |
| 5 | LOI crosses -20 | 🟢 **Gate opens — start selling monthly calls** |
| 6 | LOI climbs to +40 (Momentum) or +20 (MR) | 🟠 **Sell closer calls, trim exposure** |
| 7 | LOI hits first trim threshold | ⚠️ **Sell 25% of LEAP position** |
| 8 | Continue through TRIM_50%, TRIM_75%, EXIT_100% | Sell in tranches |
| 9 | Proceeds return to STRC | Cycle complete — wait for next entry |

---

## What the Discord Alerts Mean

| Alert | Meaning |
|---|---|
| 🎯 AB3 Buy | Stage 2 bottom confirmed. Buy LEAPs now. |
| 🚀 AB1 Entry | Pre-breakout confirmed. Buy short-term LEAP. |
| 🟢 PMCC Gate Open | LOI crossed -20. You can start selling calls. |
| 🟠 Delta Management | LOI hit the high threshold. Closer-to-money calls permitted. |
| ⚠️ AB3 Trim | LOI hit a trim level. Sell 25% of LEAP position. |
| 🔴 Gate Closed | LOI dropped back into accumulation. Stop writing calls. |
| ⏸️ AB1 Pause | Breakout signal active. Call selling paused on this asset. |
| ▶️ AB1 Resumed | Breakout done. Calls can resume. |

---

## Quick Reference Numbers

| Metric | Value | What It Means |
|---|---|---|
| STRC yield | ~0.83%/month | The hurdle rate. Beat this or stay in STRC. |
| LOI entry (Momentum assets) | < -45 | Accumulation zone open for MSTR, TSLA, IBIT |
| LOI entry (MR assets) | < -40 | Accumulation zone open for SPY, QQQ, GLD, IWM |
| LOI call gate | > -20 | Call-writing permitted |
| LOI trim zone (Momentum) | > +40 | Closer-to-money calls OK; begin trimming |
| LOI trim zone (MR) | > +20 | Closer-to-money calls OK; begin trimming |
| AB4 hard floor | 10% | Always in true cash. Non-negotiable. |
| AB4 soft ceiling | 25% | Above this, look harder for entries |
| Max OTM call delta | 0.25 | Standard income mode |
| Max ATM call delta | 0.40 | Trim/delta management mode |
| AB3 target allocation | 50% | Core position |
| AB1 target allocation | 25% | Short-term tactical |
| Per-asset soft cap | 20% | Lifts when AB4 > 25% |

---

## Frequently Asked Questions

**"Why aren't we buying anything right now?"**
Because nothing is cheap enough. MSTR's LOI bottomed at -52 in February 2026 — that was the entry window. It's now recovered to around -30. We're in the hold zone: not cheap enough to add, not rich enough to trim. The right posture is STRC + patience. The next entry comes when a new pullback brings LOI below -45 for a Momentum asset.

**"What's the point of sitting in STRC?"**
Two things. First, it pays you 0.83%/month — 10%/year — which is a genuinely good risk-free return from Saylor's preferred equity. Second, STRC price acts as an early warning system. If it drops below $97, that's stress in the Saylor capital structure showing up before MSTR does. Your cash is both earning and watching.

**"When do we ignore the 20% per-asset cap?"**
When AB4 is above 25% (too much idle cash) and the best available signal is concentrated in one asset. Concentration is not a problem when the entry is disciplined. If MSTR is the only thing with a confirmed Stage 2 bounce, that's where the money goes. The 10% hard floor is the only rule that never bends.

**"What does this engine NOT do?"**
- It does not guarantee profits
- It does not give specific price targets
- It does not execute trades automatically
- It does not trade BTC directly (BTC is a regime input, not a trading asset)
- It does not override Greg's final judgment on any trade

The engine is a decision-support tool. The humans decide.

---

*SRI Options Engine — Internal Reference Document. Not investment advice.*
