# AB1/AB2 Hypothesis Test — Root Cause & Redesign Path

**Date:** 2026-02-28  
**Purpose:** Diagnose why AB1 and AB2 underperform, test 7 hypotheses, identify the correct signal architecture

---

## The Diagnosis

**AB1 and AB2 fail because they use a lagging confirmation signal (LT FTL/STL cross) as an entry trigger.** The data shows a fundamentally better approach exists: **use VST as the entry signal while LT is still bearish** (catching the turn early).

---

## Hypothesis Results

### ✅ H4 — THE WINNER: "VST Bullish While LT Still Bearish"

This is the single strongest finding. Instead of waiting for LT to confirm (current AB1), enter when **VST+ST both turn positive while LT+VLT are still negative**:

| Asset | Mode | 20d Win% | 20d Median | n | vs Current AB1 |
|---|---|---|---|---|---|
| **TSLA** | Momentum | **86%** | **+19.6%** | 22 | ↑ from 100% but n=4 |
| **MSTR** | Momentum | **83%** | **+18.4%** | 12 | ↑↑ from 33% (was anti-signal!) |
| **BLOK** | Momentum | **75%** | **+6.2%** | 8 | ≈ 83% but lower median |
| **IWM** | Mean-Rev | **71%** | **+12.9%** | 14 | ↑ from 67% |
| **BTC** | Momentum | 57% | +5.9% | 7 | ↑ from 0% (single fire) |
| **QQQ** | Mean-Rev | 25% | -1.0% | 4 | ↓ (too few) |
| **TLT** | Mean-Rev | **21%** | **-3.3%** | 19 | Still broken |

**Why this works:** It catches the inflection point — shorter timeframes turn first at bottoms. By the time LT confirms, the easy money is made. The current AB1 waits for LT FTL>STL, then SRIBI confirmation, then pullback — that's 3 lagging filters stacked on each other.

**The simpler "VST cross+ while LT neg" version** also works broadly:
- MSTR: 68% win, +18.9% median (n=80) — excellent sample size
- QQQ: 76% win, +5.1% (n=55) — strong
- GLD: 74% win, +4.6% (n=82) — reliable
- IWM: 71% win, +5.1% (n=73) — solid
- BLOK: 61% win, +5.7% (n=71) — decent

### ✅ H5 — GLD Reversal Support is Real Support (83% hold)

| Asset | STL Hold | Rev Support Hold | Winner |
|---|---|---|---|
| GLD | 66% | **83%** | Rev Support |
| QQQ | 48% | **57%** | Rev Support |
| IWM | 45% | **52%** | Rev Support |
| TLT | 47% | 53% | Neither (both weak) |
| MSTR | 8% | 13% | Neither (both fail) |
| TSLA | 28% | 19% | Neither |

**Reversal Support is better than STL as support for MR assets**, especially GLD. But neither works for momentum assets — MSTR/TSLA/BLOK blow through both levels. This means **AB2 bull puts should only fire on GLD, QQQ, and IWM** where support actually holds.

### ✅ H6 — Flipped Bear Signals Work on QQQ and GLD

| Asset | 20d Win% | 30d Win% | 60d Win% | Verdict |
|---|---|---|---|---|
| QQQ | **86%** | **86%** | 71% | ✅ Flip to BUY |
| GLD | **88%** | **88%** | **88%** | ✅ Flip to BUY |
| IWM | 60% | 60% | 40% | ⚠️ Short-term only |
| TLT | 14% | 14% | 14% | ❌ Bear is correct here |

GLD "Strong Bear" flipped to buy: **88% win at every horizon through 60 days.** This is one of the strongest signals in the entire system. QQQ similar at 86%.

### ⚠️ H2 — SRIBI Divergence: Modest Edge

Bullish divergence (price at lows + SRIBI higher lows) shows:
- **GLD: 75% win at 20d** — useful
- **QQQ: 65% win at 20d** — decent  
- **MSTR: 57% win at 20d** — weak but positive
- **BTC/TLT: coin flip** — no edge

Not strong enough standalone, but useful as a confirmation filter.

### ⚠️ H3 — Reversal Band Touches: Asset-Dependent

LT Reversal Support touches:
- **GLD: 78% win** — excellent
- **QQQ: 70% win** — strong
- **IWM: 63% win** — decent
- **MSTR: 48%, BTC: 42%, TLT: 38%** — no edge on these

Same pattern: works on trending/MR assets, fails on momentum + bonds.

### ⚠️ H7 — Bounce vs Approach: Bounce is Marginally Better

Bounce (cross back above STL) vs Approach (within 3% of STL):
- Bounce has slightly higher win rates on momentum assets (TSLA 62% vs 53%, BLOK 70% vs 69%)
- But STL hold rates are terrible for both (<25% on most assets)
- **The STL itself is the problem, not the trigger logic**

### ❌ H1 — VST Stage Transitions: Too Few Fires

Stage 4→1 and 1→2 transitions fire only 2-6 times per asset over 5 years. Not enough for reliable signals. These are regime indicators, not trade triggers.

---

## The Redesigned Architecture

Based on these findings, here's what the data says AB1 and AB2 should be:

### AB1 v4 — "Early Turn" (Replaces Sequential Staging)

**Entry Signal:** VST SRIBI crosses positive while LT SRIBI is still negative.

**Filters (to reduce from n=80 to 1-2/month):**
1. VST+ST both positive (not just VST) — raises MSTR from 68% to 83% win
2. Price within 5% of LT Reversal Support (on assets where it works)
3. SRIBI divergence present (price near lows, VST SRIBI above its recent low)

**Asset-specific behavior:**
- **Momentum (MSTR, TSLA, BLOK):** VST+ST pos / LT+VLT neg = primary signal
- **MR (QQQ, IWM):** VST cross+ / LT neg = primary (broader filter OK, 71-76% win)
- **GLD:** Both bullish AND flipped-bear signals valid (74-88% win)
- **TLT:** EXCLUDE — nothing works
- **BTC:** Marginal (57%) — require additional filter (LOI < -30?)

**Exit:** Same as current (FTL cross or time stop) — these work fine

### AB2 v3 — "Support Bounce" (Replaces STL-Proximity)

**The problem:** STL is not support. It's a trailing stop that gets blown through.

**The fix:** Use **LT Reversal Support** as the support level instead of STL, and only on assets where support actually holds:

| Asset | Rev Support Hold Rate | Eligible? |
|---|---|---|
| GLD | 83% | ✅ Primary AB2 asset |
| QQQ | 57% | ✅ With caution |
| IWM | 52% | ⚠️ Marginal |
| All others | <35% | ❌ Exclude |

**Trigger:** Price bounces off LT Reversal Support (crosses back above after testing)

**Iron Condor:** Keep for GLD (68% win) and QQQ (64% win). The current design accidentally works because ICs are direction-neutral — the STL breach doesn't matter as much when you're selling both sides.

**Bear Call (MR only):** When LT Reversal Resistance is tested from below and rejected. Needs separate backtest.

### The "Flipped Bear" — New Signal Class

This is arguably the most important discovery. On QQQ and GLD, when the SRI system fires a bearish signal (FTL crosses below STL), **buy, don't sell.** This is the SRI's bullish bias working in reverse — the system's "bearish" detection is actually identifying oversold conditions on non-momentum assets.

**Implementation:** On GLD/QQQ, rename "Strong Bear" to "Contrarian Buy." Same signal, opposite interpretation. 86-88% win rate.

---

## Summary of Root Causes

| Problem | Root Cause | Fix |
|---|---|---|
| AB1 bull fails on MSTR | LT confirmation is too late — catches exhaustion | Enter on VST+ST turn while LT still bearish |
| AB1 bear inverted on QQQ/GLD | SRI is bullish detector; "bearish" = oversold | Flip to buy signal |
| AB2 bull put 0% STL hold | STL is not support — it's a trailing stop | Use Reversal Support; restrict to GLD/QQQ |
| TLT broken everywhere | Bond dynamics don't fit equity momentum framework | Remove from AB framework |
| AB1 works on TSLA/BLOK | These trend cleanly; LT confirmation aligns with real momentum | Keep but improve with VST early entry |

---

## Next Steps

1. **Implement AB1 v4** with VST+ST pos / LT+VLT neg entry on momentum assets
2. **Implement "Contrarian Buy"** signal on GLD/QQQ (flipped bear)
3. **Implement AB2 v3** using Reversal Support instead of STL, GLD/QQQ only
4. **Add TLT exclusion** to all three scripts
5. **Run validation backtest** on the new signals
6. Push updated scripts to repo
