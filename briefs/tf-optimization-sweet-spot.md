# Timeframe Optimization — The Sweet Spot

**Date:** 2026-03-01  
**Purpose:** Find optimal entry timing × exit rule × profitability across the full TF spectrum  
**Method:** 14 entry gates × 12 exit rules × 8 assets = 1,344 combinations tested

---

## The Core Discovery

**The lagging indicator that's too late for ENTRY is perfect for EXIT.**

Enter when VST turns bullish while LT+VLT are still bearish (catching the inflection). Exit when LT finally confirms positive (the trend is now priced in). The LT confirmation signal we were using as an entry trigger becomes the exit trigger instead.

---

## Entry Gate Results — The Spectrum

Tested every combination from "VST only" (fastest, noisiest) to "All 4 bullish" (most confirmed, most late). Clear gradient emerges:

### MSTR (Momentum)
| Gate | n | 20d Win% | 20d Median | Assessment |
|---|---|---|---|---|
| VST+ only | 1,106 | 55% | +5.2% | Too noisy, coin flip |
| **VST+ / LT- VLT-** | **52** | **81%** | **+22.8%** | **◆ SWEET SPOT** |
| VST+ ST+ / LT- VLT- | 19 | 83% | +18.4% | Slightly better win%, fewer fires |
| VST+ ST+ LT+ | 714 | 50% | -0.1% | Too late, move already priced |
| All 4 bullish | 707 | 50% | -0.1% | Dead — same as random |
| LT+ only | 1,116 | 46% | -2.4% | **Anti-signal** — current AB1 basis |

**The gradient is stark:** Going from "VST+ / LT- VLT-" (81% win) to "All 4 bullish" (50% win) — adding LT+VLT confirmation DESTROYS the signal. The edge IS the divergence between leading and lagging TFs.

### Cross-Asset Sweet Spot: "VST+ / LT- VLT-"

| Asset | Mode | n | 20d Win% | 20d Median |
|---|---|---|---|---|
| **GLD** | Trending | 33 | **91%** | **+9.5%** |
| **MSTR** | Momentum | 52 | **81%** | **+22.8%** |
| **QQQ** | Mean-Rev | 31 | **73%** | **+6.2%** |
| **IWM** | Mean-Rev | 28 | **71%** | **+9.3%** |
| TSLA | Momentum | 48 | 59% | +4.6% |
| BLOK | Momentum | 28 | 46% | -10.4% |
| BTC | Momentum | 287 | 30% | -4.1% |
| TLT | Mean-Rev | 40 | 16% | -4.5% |

**Works on 4/8 assets at >70% win rate.** TSLA benefits from the tighter "VST+ ST+ / LT- VLT-" gate (86%, +19.6%). BTC and TLT are broken regardless of gate — the SRI framework doesn't predict them.

### Why "VST+ ST+ / LT-" is the BLOK Winner (and IWM)
For some assets, requiring ST confirmation (not just VST) eliminates false starts without adding too much lag. The IWM result is striking: VST+ST+/LT-VLT- = 93% win at 20-bar time stop, 86% at 10% trail.

---

## Exit Rule Results — Two Regimes

### Regime 1: "LT Confirms" Exit (Momentum Assets)

For MSTR and BLOK, the best structural exit is **"LT turns positive"**:

| Asset | Win% | Median P&L | Mean P&L | Median Hold |
|---|---|---|---|---|
| MSTR | **73%** | **+10.3%** | +5.4% | 20 bars (3.3d) |
| IWM | **93%** | **+2.6%** | +3.3% | 6 bars (1d) |
| BLOK | **75%** | **+2.4%** | +1.4% | 19 bars (3.2d) |
| QQQ | **84%** | **+2.1%** | +1.7% | 15 bars (2.5d) |
| GLD | **91%** | **+1.5%** | +1.5% | 11 bars (1.8d) |

**This is the elegant solution:** The LT SRIBI turning positive means the structural trend has caught up with the leading VST signal. The trade thesis (early entry before LT confirms) has played out. Take profit.

Tight hold times (6-20 bars = 1-3 days). High win rates. Modest but consistent P&L. This is an **AB2 spread entry** — sell puts when VST leads, close when LT catches up.

### Regime 2: Trailing Stop Exit (Trending Assets)

For GLD and IWM, a **10% trailing stop** dramatically outperforms:

| Asset | Win% | Median P&L | Mean P&L | Median Hold |
|---|---|---|---|---|
| GLD | **91%** | **+21.4%** | **+19.6%** | 360 bars (60d) |
| IWM | **86%** | **+20.0%** | **+19.1%** | 294 bars (49d) |
| QQQ | 65% | +1.2% | +6.3% | 162 bars (27d) |

GLD at 91% win and +21.4% median — this is an **AB1/AB3 entry** signal. Buy when VST leads into a structural divergence, ride the trend with a wide stop.

### Why TF-Based Exits Beat Fixed Time Stops

Time stops (20/40/60 bars) work OK, but they leave money on the table on trending moves and hold too long on failed signals. "LT turns pos" captures the exact moment the structural shift is confirmed — typically 1-3 days on momentum assets. The trailing stop does the same for trending assets but adapts to move magnitude.

---

## The Redesigned Signal Architecture

### AB1 v4: "Structural Divergence Entry"

**Entry:** VST SRIBI crosses positive while LT + VLT SRIBI remain negative  
(For TSLA/IWM: require ST also positive)

**Exit:**  
- Momentum assets (MSTR, TSLA, BLOK): Exit when **LT SRIBI turns positive**
- Trending assets (GLD): Exit on **10% trailing stop from peak**
- MR assets (QQQ, IWM): Exit when **LT SRIBI turns positive** OR 5% trailing stop

**Excluded:** BTC (30% win), TLT (16% win) — SRI doesn't work on these

### AB2 v3: "Divergence Spread"

Same entry as AB1, but the trade is a **credit spread** instead of directional:
- Sell bull put spread when VST+/LT-VLT- fires
- Close spread when LT turns positive (profit capture)
- The 1-3 day average hold with 73-93% win rate is IDEAL for short-dated credit spreads
- This IS the AB2 redesign — stop trying to find "support" and instead sell premium into the structural divergence

### Why This Works (The Theory)

The SRI's four timeframes form a **cascade**: VST leads → ST confirms → LT follows → VLT anchors.

At bottoms: VST flips first while LT/VLT are still bearish. This creates a *structural tension* — the short-term has turned but the long-term hasn't caught up. Price typically resolves this tension upward (73-91% of the time).

At tops: the reverse cascade happens, but we already know from prior backtests that SRI is structurally bullish-biased. Bearish cascades are unreliable as sell signals (they're actually contrarian buys on GLD/QQQ).

The old AB1 waited for the cascade to COMPLETE before entering. The new AB1 enters when the cascade STARTS.

---

## Data Request

The current data is sufficient for the entry/exit redesign. However, to validate the **"LT turns pos" exit timing** more precisely, it would help to have:

1. **SPY 4H export** with the same indicator set — we have QQQ but SPY is the primary MR benchmark
2. **Longer BTC history** — current BTC file only covers Dec 2024-Feb 2026 (14 months). Need 3+ years to determine if the BTC failure is structural or sample-dependent
3. **IBIT 4H export** — our designated AB1 vehicle for BTC exposure; may behave differently than spot BTC

For script implementation: no additional data needed. I can build AB1 v4 and AB2 v3 from the existing SRIBI columns in the CSV exports.

---

## Summary

| Question | Old Answer | New Answer |
|---|---|---|
| When to enter? | After LT confirms (lagging) | When VST leads while LT disagrees (leading) |
| When to exit? | Fixed time / FTL cross | When LT catches up (momentum) or 10% trail (trending) |
| What makes a good signal? | More confirmation = better | **Divergence** between TFs = better |
| Why did AB1 fail? | Wrong parameters | Wrong architecture — confirmation destroys the edge |
| Where does AB2 fit? | Sell puts near "support" (STL) | Sell puts into structural divergence, close on LT confirm |
