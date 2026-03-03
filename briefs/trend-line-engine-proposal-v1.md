# Trend Line Engine — Proposed Approach v1.0
**Date:** 2026-03-03
**Status:** Proposal — awaiting Gavin scope confirmation
**Author:** CIO

---

## Unified Requirement (CIO's interpretation)

The Trend Line Engine serves two coupled functions:
1. **Infrastructure:** The CIO can mathematically reference key trend lines as linear equations derived from anchor points on price data — giving the engine "eyes" on structural price levels the way it currently has eyes on SRI signals.
2. **Signal:** The engine uses those equations to detect proximity events, confirmed breaks, and bounces, integrating them into stage state analysis and morning briefs to improve entry timing and exit confirmation.

The desired outcome — higher win rates and better identification of trend breaks and continuations — flows directly from coupling the infrastructure to the signal layer.

---

## Gap Assessment — What the Engine Currently Cannot Do

| Capability | Current state | Gap |
|---|---|---|
| Read LOI signals | ✅ Full | None |
| Read Howell sector signals | ✅ Full | None |
| Know price is at a key SRI level (FTL/STL) | ✅ Partial — uses calculated levels | Lacks visual trend lines |
| Know price is approaching a major trend line | ❌ None | **Critical gap** |
| Confirm a trend line break | ❌ None | **Critical gap** |
| Distinguish trend line bounce from break | ❌ None | **High priority** |
| Know whether current price is above or below a trend line | ❌ None | **Critical gap** |
| Contextualize an LOI signal with trend structure | ❌ None | **High priority** |

**The practical consequence:** The engine can say "LOI crossed −45, Watch declared" but it cannot say "Watch declared, AND price is sitting at a 12-month downtrend line — a break of this line would confirm the Stage 1 initiation." That second part is where significant win-rate improvement lives.

---

## Proposed Architecture: Hybrid (Option C)

Three-tier architecture combining Gavin's visual judgment with algorithmic detection:

```
Tier 1: Gavin-Validated Major Lines
    → Gavin identifies significant multi-month trend lines in TradingView
    → Commits them to GitHub as structured data
    → CIO reads and monitors these with highest priority

Tier 2: Algorithmically Detected Minor Lines
    → Python engine detects pivot highs/lows from OHLC data
    → Fits candidate trend lines to significant pivot sequences
    → Outputs as lower-confidence signals; Gavin can promote to Tier 1

Tier 3: Dynamic Support/Resistance (derived from SRI levels)
    → FTL/STL levels from existing SRI data (already partially built)
    → Extended into the future as flat or slightly sloping levels
    → No new data required; already in the engine
```

**Why hybrid:** Gavin's ability to identify truly significant trend lines (the ones markets actually react to) is superior to any algorithm on major lines. Algorithmic detection adds breadth coverage for minor lines and removes the manual bottleneck for shorter-term analysis.

---

## Data Specification

### Tier 1 — Gavin-Defined Lines

**File format:** `trend-lines/{ASSET}-trend-lines.json` in GitHub repo, updated by Gavin as needed.

```json
{
  "asset": "MSTR",
  "updated": "2026-03-03",
  "lines": [
    {
      "id": "MSTR-TL-001",
      "label": "Post-ATH downtrend",
      "type": "resistance",
      "direction": "descending",
      "anchor1": {"date": "2024-11-21", "price": 543.00},
      "anchor2": {"date": "2025-01-22", "price": 380.00},
      "significance": "major",
      "notes": "Connects Nov 2024 ATH to Jan 2025 lower high"
    },
    {
      "id": "MSTR-TL-002",
      "label": "Feb 2026 base support",
      "type": "support",
      "direction": "flat",
      "anchor1": {"date": "2026-02-05", "price": 120.00},
      "anchor2": {"date": "2026-02-28", "price": 120.00},
      "significance": "major",
      "notes": "Double-bottom support zone"
    }
  ]
}
```

**From these two points, the engine computes for any date:**
```
price_on_line(date) = anchor1_price + slope × (date - anchor1_date)
slope = (anchor2_price - anchor1_price) / (anchor2_date - anchor1_date)
distance_pct = (current_price - price_on_line) / price_on_line × 100
```

### Tier 2 — Algorithmically Detected Lines

**Detection method:** Zigzag pivot detection → connect sequential pivot highs (resistance lines) and sequential pivot lows (support lines) → filter by minimum length (≥ 3 anchor points), minimum significance (touches > 2), and R² fit quality.

**Algorithm:**
```python
def detect_trend_lines(ohlc_df, min_touches=2, min_length_bars=20, r2_threshold=0.90):
    # 1. Find pivot highs/lows using local max/min over N-bar window
    # 2. For each sequence of 3+ pivots, fit a linear regression
    # 3. Filter by R² (line quality) and touch count
    # 4. Return lines sorted by significance (length × touches × R²)
```

Output format identical to Tier 1 but with `significance: "minor"` and `confidence: r2_value`.

---

## Signal Integration

### Three signal types generated per trend line:

**1. Proximity Alert** (Layer 2, `TRENDLINE_PROXIMITY`)
- Trigger: Price within 2% of trend line price for the current bar
- Output: "MSTR approaching major downtrend resistance at $148.20 (current: $145.80, 1.6% gap)"
- Use: Prepare for potential test; watch next session closely

**2. Test Detection** (Layer 2, `TRENDLINE_TEST`)
- Trigger: Price touches within 0.5% of trend line (intrabar)
- Output: "MSTR testing major downtrend resistance at $148.20 — watch for break or rejection"
- Use: High-alert mode; break or rejection determines stage implication

**3. Break Confirmation** (Layer 2, `TRENDLINE_BREAK`)
- Trigger: Closing price beyond trend line by > 0.5% AND volume ≥ 1.5x ADV
- Output: "MSTR confirmed break ABOVE major downtrend resistance at $148.20 with volume 2.1x ADV"
- Use: Stage State implication applied (see below)

---

## Stage State Integration

The most valuable application: trend line events contextualize stage state transitions.

| Trend Line Event | Stage State Context | Combined Signal | Win Rate Implication |
|---|---|---|---|
| Break ABOVE descending resistance | S4→1 Forming → S1→2 Watch | Pre-breakout confirmed — strongest AB1 entry signal | Materially higher than stage signal alone |
| Break ABOVE descending resistance | S2C Forming | Continuation confirmed — add to AB3 | Higher confidence on continuation |
| Break BELOW ascending support | S2→3 Watch | Distribution confirmed — accelerate trim schedule | Reduces false S2→3 alerts |
| Break BELOW ascending support | S2C Watch | S2C invalidated — reclassify as S2→3 Watch | Prevents bad addition to position |
| Bounce off ascending support | S4→1 Forming | VLT Clock context improved — bounce at structural level | Improves clock interpretation |
| Price trapped between resistance above + support below | Any stage | Range-bound: reduce signal confidence | Prevents entries into low-probability setups |

---

## Morning Brief Integration

When any tracked asset has an active trend line within 5% of current price, the morning brief includes a trend line block:

```
📐 TREND LINE WATCH — MSTR
Major resistance: $148.20 (Post-ATH downtrend) — 10.2% above current
Major support:    $120.00 (Feb 2026 base) — 10.8% below current
Current position: In range — no immediate test
Context: A break of $148.20 with volume would be the S1→2 Watch trigger.
         A break of $120.00 would invalidate S4→1 Forming — re-enter Watch.
```

---

## Win Rate Improvement — Mechanism

The win rate improvement comes from three specific scenarios:

**1. Entry filtering:** Avoid entries when price is approaching resistance immediately after Watch is declared. An LOI Watch signal into the bottom of a range is a better entry than the same signal with overhead resistance 3% above. The engine currently cannot distinguish these.

**2. Exit confirmation:** A trend line break below support confirms S2→3 faster and more precisely than SRI alone. SRI takes 2–3 bars to confirm a Slow Trackline red sequence; a trend line break is confirmed on the close. Faster exit = better P&L on distribution entries.

**3. Breakout targeting:** AB1 entries (pre-breakout) are currently triggered by LOI signal alone. Adding "AND price approaching major resistance" makes the AB1 signal considerably more precise — you're entering specifically because a trend line break is imminent, not just because the SRI says so.

---

## Implementation Plan

**Phase 1 — Infrastructure (Tier 1 only):**
- Build `TrendLineEngine` class in `sri_engine.py`
- Read Tier 1 JSON files from GitHub repo
- Calculate current price-on-line for all active trend lines
- Generate proximity, test, and break events
- Add to morning brief trend line block

**Phase 2 — Signal Integration:**
- Wire `TRENDLINE_PROXIMITY`, `TRENDLINE_TEST`, `TRENDLINE_BREAK` into `pmcc_alerts.py`
- Integrate into Stage State confirmation ladder (break above resistance = S1→2 Watch trigger)
- Add to MSR key triggers section

**Phase 3 — Algorithmic Detection (Tier 2):**
- Build zigzag pivot detector
- Build line fitting algorithm with R² quality filter
- Generate candidate lines for Gavin review
- Promote validated candidates to Tier 1 JSON

---

## What I Need From Gavin

**To start Phase 1 immediately:**
1. Confirm the JSON format above is acceptable for Tier 1 input (or propose changes)
2. Commit an initial `trend-lines/MSTR-trend-lines.json` file to GitHub with the 2–4 most significant MSTR trend lines you currently have drawn in TradingView (just the anchor points — date and price for each endpoint)

**For Phase 3 scope:**
3. Confirm whether algorithmic detection (Tier 2) is in scope for this project, or if Tier 1 human-defined lines are sufficient for now

---

## Proposed Outcome Metrics

We'll know the Trend Line Engine is working when:
- Win rate on AB1 entries improves measurably when trend line break is the entry trigger vs. LOI signal alone
- False S2→3 alerts (and premature exits) decrease as trend line support holds
- Morning brief trend line blocks referenced in post-mortems as a contributing factor in successful entries

These metrics will be tracked via the Signal Accuracy Tracking system (backlog #8) once the Trade Recommendation Engine is live.

---

*Next step: Gavin reviews → confirms format → commits first MSTR trend lines JSON → Phase 1 built in first sprint after crontab install*
