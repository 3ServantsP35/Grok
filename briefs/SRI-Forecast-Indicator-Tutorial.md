# SRI Forecast Indicators — Tutorial & Reference Guide
**Version:** 1.0 | **Date:** 2026-02-28
**Authors:** CIO + Gavin (RizenShine)
**Audience:** Greg, Gary, Gavin

---

## Overview

We have three Pine Script indicators that work together to cover the full investment decision spectrum. Each is a separate script on TradingView — load them independently based on what you're analyzing.

| Indicator | What It Does | Where It Lives |
|-----------|-------------|----------------|
| **SRI Forecast AB1** | Directional signals — when to buy | Price chart overlay |
| **SRI Forecast AB2** | Spread guidance — where to sell premium | Price chart overlay |
| **SRI Forecast AB3** | LEAP timing — when to accumulate/distribute long-dated options | Separate oscillator pane |

All three are built on the same SRI (Stochastic Regime Indicator) engine that Gavin designed. They read the same SRIBI (SRI Bias Index) data across 4 timeframes. They just interpret it differently for different trading strategies.

---

## Quick Start

### Loading the Scripts
1. Open TradingView on any chart (BTC, MSTR, SPY, etc.)
2. Click "Indicators" → "Invite-only scripts" or paste from Pine Editor
3. The scripts are in the GitHub repo: `3ServantsP35/Grok` under `pine/`
4. AB1 and AB2 go on the **price chart** (overlay=true)
5. AB3 goes in a **separate pane below** (overlay=false, it's an oscillator)

### What You'll See Immediately
- **AB1:** Green triangles (buy signals) and a forecast ribbon projecting 20 days forward
- **AB2:** Colored slow trackline (STL) showing spread safety zones, plus small diamonds for spread opportunities
- **AB3:** An oscillator line (the LOI) with green/red zones showing LEAP accumulation/distribution windows

---

## SRI Forecast AB1 — Directional Signals

### Purpose
Tells you **when to enter a directional position** (buy IBIT, buy MSTR shares, etc.). This is your Allocation Bucket 1 tool.

### How It Works
The indicator watches for two specific patterns that have backtested edge:

**Signal 1: FTL Cross Above STL** (fluorescent green triangle ▲)
- The LT Fast Trackline crosses above the LT Slow Trackline
- This is a structural trend change — the medium-term trend is turning bullish
- Backtest: 67% win rate, +9.1% median return at 20 days
- Fires ~4 times per year on BTC

**Signal 2: CT3+ Pullback Entry** (smaller green triangle)
- Price pulls back to the STL while 3+ of 4 timeframes are bullish
- This is buying the dip in a confirmed uptrend
- Backtest: 74% win rate, +6.1% median return at 20 days
- Fires ~3 times per year on BTC

### The Forecast Ribbon
The shaded ribbon projecting forward from the current bar shows **backtested percentile ranges** for the next 20 days based on the current SRIBI zone:

- **Upper dashed line:** 75th percentile outcome (bullish scenario)
- **Solid center line:** Median (50th percentile) expected path
- **Lower dashed line:** 25th percentile outcome (bearish scenario)

The color tells you the current regime:
- 🟢 Green = Very Bullish (SRIBI avg > +25): median +2.78% at 20d
- 🔵 Teal = Bullish (+5 to +25): median +0.10%
- ⚪ Gray = Neutral (-5 to +5): median -1.21%
- 🟠 Orange = Bearish (-25 to -5): median -0.58%
- 🔴 Red = Very Bearish (< -25): median +1.29% ← *contrarian bullish!*

**Key insight for Greg and Gary:** The Very Bearish zone actually has *positive* expected returns. This is the capitulation zone — everyone is selling, but historically that's where bottoms form. This is NOT a signal to sell.

### The Info Table (bottom right)
Shows at a glance:
- Current SRIBI zone and name
- Concordance tier (CT0-CT4) — how many timeframes agree
- Individual SRIBI readings for VST, ST, LT, VLT (● = bullish, ○ = bearish)
- 20-day median forecast
- Active AB1 signal (if any)

### Bearish Signals
Currently **scaffolded but disabled** for BTC. Our backtest found zero reliable bearish directional signals on BTC — every combination tested was 53% or worse (coin flip). The bearish signal architecture exists in the code for future use on other assets (SPY bearish signals are untested but theoretically should work given SPY's mean-reverting nature).

### What To Do With AB1 Signals
1. Green triangle appears → **check the forecast ribbon**. Is the median path positive?
2. Check the concordance tier in the table. CT4 (all timeframes bullish) is highest conviction.
3. If signal + ribbon + concordance align → consider a directional position (buy IBIT for BTC exposure, or MSTR shares)
4. Position size based on CT tier: CT2 = small, CT3 = standard, CT4 = full

---

## SRI Forecast AB2 — Spread Guidance

### Purpose
Tells you **where and when to sell option premium** (bull put spreads, bear call spreads, iron condors). This is your Allocation Bucket 2 tool.

### The Colored STL (Slow Trackline)
The thick line on the chart is the LT Slow Trackline — the structural support/resistance level. Its color tells you how safe it is to sell spreads near that level:

| Color | Zone | Distance from STL | Risk | Action | Backtest Hold Rate |
|-------|------|-------------------|------|--------|-------------------|
| 🟢 **Green** | Overweight | < 3%, LOW risk | Safe + profitable | Full size spreads | 81% |
| 💚 **Light Green** | Standard | < 3%, MEDIUM risk | Safe | Standard size | 84% |
| 🟡 **Yellow** | Conservative | 3-8% from STL | Moderate | Half size | 74% |
| ⚪ **Gray** | STRC | > 8% from STL | Low but unprofitable | Don't bother — put capital in STRC instead | 93% safe but thin premium |
| 🔴 **Red** | Avoid | < 3%, HIGH risk | Dangerous | No new spreads | 27% hold (73% breach) |

**The key insight:** Gray doesn't mean dangerous — it means the premium isn't worth it. You're too far from STL for spreads to generate meaningful income. Park that capital in STRC (~10% annual) instead.

**Red means get out.** When the STL turns red, price is near it AND the risk factors (FTL structure, concordance, momentum) all point to a breach. 73% of the time, price breaks through.

### AB2 Spread Detection Markers
Small diamonds appear on the chart when specific spread opportunities are detected:

- 🟢 **Green diamond below bar:** Bull Put Spread — price near STL support, green/light green zone, bearish SRIBI (contrarian). Strike your put AT the STL.
- 🔴 **Red diamond above bar:** Bear Call Spread — price extended above FTL, bullish SRIBI, limited upside per forecast
- 🟣 **Purple diamond:** Iron Condor — neutral zone, narrow forecast ribbon
- 🟡 **Yellow circle:** Conservative spread — yellow zone, half size

### Breach Risk Scoring
The indicator calculates a composite breach risk score using 3 factors:
1. **FTL vs STL structure:** FTL below STL = bearish structure (+3 risk). FTL above = support confirmed (-2 risk).
2. **SRIBI concordance:** All timeframes bearish at support = counterintuitively SAFE (capitulation, -3 risk). All bullish = complacency (+2 risk).
3. **Momentum:** 5-day rate of change. Falling fast = risk. Stable/rising = support.

The composite maps to LOW / MEDIUM / HIGH risk, which drives the STL color.

### The Forecast Ribbon (same as AB1)
Same 20-day projection. In AB2 context, use it to:
- Set your **short strike** at the p25 level (75% chance price stays above)
- Set your **spread width** based on ribbon width (wider ribbon = wider spread needed)
- Avoid bear call spreads when ribbon is strongly bullish (p75 > 10%)

### What To Do With AB2
1. Look at the STL color — that's your primary decision
2. If Green/Light Green: look for the green diamond (bull put spread signal)
3. Strike the short put AT or slightly below the STL level (it's your structural support)
4. Use the forecast ribbon p25 as your downside scenario
5. If Gray: don't force it. STRC at 10% annual is your risk-free alternative
6. If Red: close existing spreads near that level. Do not open new ones.

---

## SRI Forecast AB3 — LEAP Opportunity Index (LOI)

### Purpose
Tells you **when to buy and sell LEAPs** (long-dated call options, 6-12+ months to expiry). This is your Allocation Bucket 3 tool. LEAPs are about buying long-duration optionality at extreme dislocations — not short-term trading.

### The LOI Oscillator
A single line oscillating between roughly -100 and +100. It combines 4 components:

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| VLT SRIBI | 40% | Structural trend (the LEAP timeframe) |
| VLT Acceleration | 30% | How fast the structural trend is changing |
| LT SRIBI | 15% | Medium-term confirmation |
| Concordance | 15% | Cross-timeframe agreement (0/4 to 4/4 bullish) |

The weighting is backtested across 6 assets (BTC, MSTR, SPY, QQQ, TSLA, TLT) from 2015-2026.

### Zone Interpretation

**Accumulation zones (green background) — BUY LEAPs:**

| LOI Level | Zone | Action | Backtest (BTC) |
|-----------|------|--------|----------------|
| < -80 | DEEP ACCUMULATION | Back up the truck. Rare, generational. | Only fired twice: FTX bottom (Nov 2022), current cycle (Feb 2026) |
| -80 to -60 | ACCUMULATION | Scale into LEAPs | 70% win at 60d, +12.4% median |
| -60 to -20 | Mild Opportunity | Hold, watch for deeper entry | Mild positive edge |

**Neutral zone (no background):**

| LOI Level | Zone | Action |
|-----------|------|--------|
| -20 to +20 | Neutral | Hold existing LEAPs. No new action. |

**Distribution zones (amber/red background) — TRIM LEAPs:**

| LOI Level | Zone | Action |
|-----------|------|--------|
| +20 to +40 | Mild Caution | First trim level (25%) |
| +40 to +60 | Elevated | Second/third trim |
| > +60 | Distribution | Late-stage trimming |

### The Phased Trim Schedule

**This is the key innovation.** LEAPs should NOT be sold all at once. The indicator manages a 4-phase exit:

| Phase | Trigger | Action | Cumulative Sold |
|-------|---------|--------|----------------|
| Trim 1 | LOI crosses above +20 | Sell 25% of LEAP position | 25% |
| Trim 2 | LOI crosses above +40 | Sell another 25% | 50% |
| Trim 3 | LOI crosses above +60 | Sell another 25% | 75% |
| Final | LOI peaks above +60 then drops 20 points | Close remaining 25% | 100% |
| Reset | LOI drops below -20 | New cycle — back to 0% trimmed | 0% |

Each trim fires **once per cycle**. You'll see triangle-down markers (▼) with "25%", "50%", "75%" labels, and an "EXIT" marker for the final close.

**Why phased?** Because we can't call tops. Our backtest proved that LOI > 60 on BTC keeps running 50% of the time. By trimming in phases, you capture most of the move if it continues, but you've already banked 50-75% if it reverses.

### Auto-Detect: Momentum vs Mean-Reverting

The indicator automatically detects what kind of asset you're viewing and adjusts ALL thresholds:

**Momentum mode** (BTC, MSTR, TSLA, IBIT, crypto):
- Accumulate at LOI < -60, deep at < -80
- Trim at +20 / +40 / +60
- Trends persist → hold longer, trim later

**Mean-Reverting mode** (SPY, QQQ, TLT, everything else):
- Accumulate at LOI < -40, deep at < -60
- Trim at +10 / +30 / +50
- Extremes revert → buy earlier, trim earlier

The table header shows `[TR]⚡` (momentum, auto-detected) or `[MR]⚡` (mean-reverting, auto-detected). You can override this in settings if needed.

### Position Management Panel

Enter your LEAP details in the settings to see real-time position info:

1. **Strike Price** → Shows ITM/OTM, moneyness %, intrinsic value per contract
2. **Entry Cost** → Shows per-contract P&L and % return
3. **Number of Contracts** → Shows total dollar P&L

This turns the indicator from an analytical tool into a **position management dashboard**. At each trim marker, you can see exactly what you're locking in.

### What To Do With AB3
1. **New LEAP position:** Wait for LOI to drop below accumulation threshold (green zone). Buy calls 6-12 months out, strikes near or slightly OTM.
2. **Existing position:** Enter your strike/cost/qty in settings. Watch the trim phases.
3. **Trim marker appears:** Execute the trim — sell the indicated percentage of your LEAP position at market.
4. **Cycle completes:** LOI drops below reset → you're back to 0% trimmed, ready for the next accumulation.

---

## How The Three Scripts Work Together

```
┌─────────────────────────────────────────────┐
│               PRICE CHART                    │
│                                              │
│   AB1: Forecast ribbon + buy signals         │
│   AB2: Colored STL + spread diamonds         │
│                                              │
├─────────────────────────────────────────────┤
│           OSCILLATOR PANE                    │
│                                              │
│   AB3: LOI line + accumulation/trim zones    │
│                                              │
└─────────────────────────────────────────────┘
```

**Typical workflow:**

1. **Check AB3 first** — Where are we in the LEAP cycle? Accumulating, holding, or distributing?
2. **Check AB2 on the price chart** — What color is the STL? Are we near support? Any spread opportunities?
3. **Check AB1** — Any directional signals firing? What does the forecast ribbon say?
4. **Cross-reference** — All three reading bullish? High conviction. Mixed signals? Reduce size or wait.

### Signal Hierarchy
- AB3 (LEAPs) operates on the **longest timeframe** — structural cycle positioning
- AB1 (directional) is **medium-term** — trend entries and exits
- AB2 (spreads) is **shortest** — premium collection at specific price levels

When they conflict, the longer timeframe wins. If AB3 is in deep accumulation but AB1 hasn't triggered a buy signal yet, it means the structural setup is there but the timing isn't ripe. Wait for AB1 confirmation before sizing up directional.

---

## Key Concepts Reference

### SRIBI (SRI Bias Index)
The difference between the Fast Trackline (FTL) and Slow Trackline (STL) as a percentage. Positive = FTL above STL = bullish structure. Negative = bearish.

### Timeframes
| Abbreviation | Reversal Band | Fast Trackline | Slow Trackline |
|---|---|---|---|
| VST (Very Short) | 2H | 2H | 1D |
| ST (Short) | 4H | 2H | 1D |
| LT (Long) | 1D | 4H | 1W |
| VLT (Very Long) | 2D | 8H | 2W |

### Concordance Tiers
- **CT0:** 0/4 timeframes bullish — full bearish (capitulation zone — contrarian bullish!)
- **CT1:** 1/4 bullish — early signs, not reliable
- **CT2:** 2/4 bullish — split market, the "breadth trap" (worst zone: -1.31% at 20d)
- **CT3:** 3/4 bullish — confirmed trend, quality asset entry
- **CT4:** 4/4 bullish — full conviction, all timeframes aligned

### STRC Hurdle
STRC (Strategy's preferred stock) yields ~10% annually (~0.83%/month). Any trade in AB1, AB2, or AB3 must have expected returns exceeding STRC, or the capital should stay parked there. STRC is the risk-free rate of this system.

---

## Settings Reference

### AB1 Settings
| Setting | Default | Description |
|---------|---------|-------------|
| Trackline ATR Period | 14 | Core SRI parameter — don't change unless Gavin says to |
| Trackline ATR Coefficient | 1.0 | Core SRI parameter |
| Show Forecast Ribbon | On | The 20-day projection |
| Show AB1 Signals | On | Buy signal markers |
| Show Stage Background | On | Green/red tint for LT bull/bear |

### AB2 Settings
| Setting | Default | Description |
|---------|---------|-------------|
| Near STL % | 3.0 | Threshold for "near" zone (green/light green/red) |
| Mid STL % | 8.0 | Threshold for "mid" zone (yellow) |
| Show Forecast Ribbon | On | Same 20-day projection |
| Show AB2 Spread Markers | On | Diamond markers for spread opportunities |
| Show Info Table | On | Bottom-right data panel |

### AB3 Settings
| Setting | Default | Description |
|---------|---------|-------------|
| Asset Behavior | Auto-Detect | Momentum (BTC/MSTR/TSLA) or Mean-Reverting (SPY/QQQ) |
| LOI Weights | 40/30/15/15 | VLT / Acceleration / LT / Concordance — backtested defaults |
| Use Custom Trim Levels | Off | Enable to override mode defaults |
| LEAP Strike Price | 0 | Your average call strike — enables position tracking |
| Entry Cost Per Contract | 0 | Premium paid × 100 — enables P&L display |
| Number of Contracts | 0 | For total dollar P&L |

---

## FAQ

**Q: Do I need all three scripts loaded at once?**
A: No. Load what's relevant to your current analysis. AB2 is the most commonly used (spread management). AB3 is for when you're specifically managing LEAPs. AB1 is for timing entries.

**Q: The forecast ribbon shows negative median — does that mean sell?**
A: Not necessarily. The ribbon shows probability distributions, not recommendations. A negative median in the Very Bearish zone is historically where bottoms form. Context matters.

**Q: Why can't I see buy signals on SPY?**
A: Bearish AB1 signals are disabled by default. Bullish signals work the same on all assets. We're planning to enable MR-specific signals in a future update once SPY bearish signals are backtested.

**Q: The LOI says "ACCUMULATE" but price keeps falling — is it wrong?**
A: No. Accumulation zones ARE when price is falling. That's the point — you're buying when others are panic selling. The 70% win rate means 30% of the time it keeps falling further. This is why you scale in (don't go all-in on the first accumulation signal).

**Q: What's the ⚡ in the AB3 table header?**
A: It means the mode (Momentum or Mean-Reverting) was auto-detected from the symbol, not manually set. If you override it in settings, the ⚡ disappears.

**Q: Can I use these on stocks other than BTC/MSTR/SPY?**
A: Yes. The SRI engine works on any liquid asset. The SRIBI readings and concordance tiers are universal. The mode toggle (Momentum vs MR) adjusts thresholds appropriately. Just know that backtesting was done on BTC, SPY, QQQ, GLD, TLT, and TSLA — other assets are extrapolated.

---

*For questions, ask in #mstr-cio. For bugs or feature requests, tag CIO.*
