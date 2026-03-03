# SRI Options Engine — Layman's Guide
**Version 1.1 | March 3, 2026**
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

### Layer 0.5 — Howell Phase (The Season)

Between the global weather and the road conditions, there's a question neither one answers on its own:

> *What time of year is it in the market?*

The **Howell Phase Engine** reads eight sector ETF trend signals — Tech (XLK), Cyclicals (XLY), Financials (XLF), Energy (XLE), Defensives (XLP), Bonds (TLT), Gold (GLD), and Small Caps (IWM) — and determines which of four macro seasons the market is currently in:

| Season | Phase | What's Working | What's Not |
|---|---|---|---|
| 🌱 Spring | **Rebound** | Equities, Tech, Cyclicals, Financials | Bonds, Energy, Defensives |
| ☀️ Summer | **Calm** | Everything — broad participation | Nothing yet fading |
| 🍂 Autumn | **Speculation** | Commodities, Energy, Defensives | Cyclicals rolling over; equity breadth narrowing |
| 🌧️ Winter | **Turbulence** | Bonds, Defensives | Almost everything else |

**Why this matters for us:** You don't plant crops in winter — and you don't buy TSLA or MSTR LEAPs when the season is wrong. In **Speculation**, Cyclicals (TSLA, small caps) are already rolling over — entering them feels like buying a dip but it's actually the beginning of a breakdown. In **Turbulence**, the correct trade for SPY is to wait for broad-flush conditions (small caps also down), not to buy when only the big names are selling off.

**The current season (2026-03-02): 🌧️ Turbulence**
- Meaning: Tech, Cyclicals, and Financials are all trending down. Bonds and Defensives are holding up. This is the late-cycle pattern.
- What we're doing: Preserving cash in STRC, pausing AB2 call-writing, watching MSTR and BTC for the first signs that Spring is beginning.
- The moment the phase shifts to Rebound, a Discord alert fires — that's the starting gun for AB3 LEAP deployment on Beta assets.

**The breadth signal:** There's one special rule inside this layer for SPY/QQQ. When small caps (IWM) are still strong while SPY is correcting, it means *only the big names are selling*. Capital has already rotated out of small caps into mega-cap quality earlier — and the index is beginning to roll over from the top, not bouncing from a healthy dip. Historical data: only 10–13% of SPY/QQQ corrections in this configuration continue higher. We skip those entirely. When small caps are *also* weak (everyone's selling), that's a real flush — and those have 51–63% continuation rates. Those we buy.

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
| 🌱 Howell Phase Transition | **The macro season just changed.** The most important alert in the system — especially Turbulence → Rebound, which is the starting gun for MSTR/IBIT AB3 deployment. |

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

## The Traffic Light System

The engine doesn't just say "buy" or "sell." It tells you **exactly where we are on the journey** — and how confident it is that we're about to turn the corner.

Think of it like a road trip with ten distinct mile markers. The classic map has four main stops: Accumulation (buying zone), Markup (going up), Distribution (topping out), and Markdown (going down). But the real world doesn't jump cleanly from one stop to the next. There are transition zones — that moment when you can see the engine struggling to pull the car uphill before it finally crests the ridge.

The engine now names those transition zones explicitly. Here are all ten:

| Where We Are | Engine Name | Plain Language |
|---|---|---|
| 🟢 The valley floor | **S4→1** | "We might be at the bottom. Watch carefully." |
| 🟢 Starting to climb | **S1** | "The climb has begun. Engine confirmed turning." |
| 🟢 Gaining speed | **S1→2** | "Breakout building. Pre-breakout entry window." |
| 🟢 Full acceleration | **S2** | "Full markup underway. Momentum is real." |
| 🟢 Cruising altitude | **S2C** | "The run is continuing. Hold your position." |
| 🟡 Warning signs | **S2→3** | "Starting to see cracks. First caution flags." |
| 🔴 Topping out | **S3** | "Distribution in progress. Reduce exposure." |
| 🔴 Losing altitude | **S3→4** | "Markdown beginning. Get lighter fast." |
| 🔴 Descending | **S4** | "Full downtrend. Don't buy the dip." |
| 🔴 Still descending | **S4C** | "Continues lower. No floor signal yet." |

**The key insight:** Most costly mistakes in this system happen at two points — at *S2→3* (holding too long because you think the run is continuing) and at *S4→1* (buying too early because you think the bottom is in). The engine's job is to tell you which one of those you're actually in, with specificity.

### The Confidence Ladder

Every transition also has a confidence level: **Watch → Forming → Confirmed**.

- **Watch** means "conditions are starting to look like a transition might be coming." The car is slowing down. You notice it. But you haven't confirmed the turn yet.
- **Forming** means "multiple conditions are now lining up." The speedometer is dropping, the road ahead is curving, your passenger is pointing left.
- **Confirmed** means "the turn has happened." The evidence is there. Now you act.

The most important confirmation is the **S4→1 Confirmed** signal — the engine's all-clear that a genuine bottom has been reached. Until that fires, you hold your cash in STRC and watch. When it fires, you act.


---

## The Readiness Score

Every week, the engine publishes a **0–10 Readiness Score** (technically called the LEAP Attractiveness Score) for each asset it tracks. Think of it like a weather forecast confidence rating:

- **10/10:** "Pack your umbrella, cancel your picnic — it's definitely raining." High confidence, high conviction. Full position entry authorized.
- **8–9/10:** "There's an 80% chance of rain." Strong conviction. Act now.
- **6–7/10:** "There's a chance — building but not certain yet." Conditions are developing. A small early position may make sense.
- **4–5/10:** "Clouds are forming, but it might blow over." Watch closely. Don't commit yet.
- **1–3/10:** "Not a cloud in the sky." No entry. Hold your cash.

### Where the Number Comes From

The score starts with where the asset is on the ten-step road map above. Being at **S4→1 Confirmed** (genuine bottom confirmed) starts you at a 10. Being in **S4 or S4C** (still falling, no floor) starts you at 0. The middle states get scores in between.

Then the engine applies adjustments based on the broader environment:

- Is the macro season wrong? (Turbulence phase — wrong time of year to plant) → score goes down
- Is global liquidity contracting? → score goes down slightly
- Is Bitcoin's bottom unconfirmed? (For MSTR and IBIT) → score goes down slightly
- Is MSTR trading at a discount to its Bitcoin holdings? → score goes up slightly
- Is the price near a major floor? → score goes up slightly

### Most Decisions Happen in the 6–8 Range

A perfect 10 is rare — it requires all the stars to align simultaneously. A 0 means "don't touch it." Most real decisions happen in the **6–8 range**, where conditions are building but not yet certain. That's normal. The engine is designed to make you act on evidence, not perfection.

### The Personal Income Angle

Here's something the shared score doesn't capture: **your specific situation matters.**

If your portfolio isn't generating the monthly income you need yet — say you haven't built up enough covered call income to hit your 2% monthly target — the engine recognizes that and adjusts when it makes sense to act a little earlier.

Think of it this way: if you're getting paid well while you wait (your income engine is working), you can afford to be patient and wait for a score of 8 before deploying. But if your income engine isn't built yet, waiting for that perfect 8 while sitting at a 6.5 has a real cost every month you delay. The engine accounts for this in your **private personal report** (more on that below).

This personal adjustment is **never shown in the shared report**. It's your information, for your situation, used only in your private channel.


---

## Your Personal Report

Once a week — or any time you ask — the engine generates a **Personal Report** just for you, delivered only in your private channel.

Here's what it does: it takes the shared market picture (the 0–10 scores, the stage states, the confirmation ladders) and translates it into:

> *"Here's what this means for your specific situation, your income needs, and your current positions."*

For example, the shared report might say MSTR is a 7/10. Your personal report might say: "Your income engine is currently generating 1.1%/month against your 2% target. Given that gap, this 7 becomes more actionable for you — here's a suggested approach at 25% of your normal sizing."

Or it might say: "You already have a large MSTR position from the February entry. Given your current exposure, the recommendation is to hold and not add at this level."

**What your personal report covers:**
- Your income gap (how far you are from your 2%/month target)
- Your current positions and how they relate to the current signals
- A specific action recommendation for the week — with sizing
- What to watch for that would change that recommendation

**Privacy rule:** Your personal report is never shared with other users, never posted to shared channels, and never committed to GitHub. It is yours and only yours.

To get your report, just ask in your private channel: *"Give me my personal report."*


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

*v1.1 additions: The Traffic Light System (10-state taxonomy), The Readiness Score (LEAP Attractiveness), Your Personal Report (PPR overview).*
