# AB4 Gate Entry Doctrine v1

**Status:** v1 — 2026-07-13  
**Owner:** Cyler  
**Purpose:** Define how the AB4 Gate should be interpreted, reported, and alerted across asset classes. This doctrine ensures messaging reflects observed signal behavior rather than treating all assets identically.

---

## 1. Core Principle

The AB4 Gate identifies **recovery windows**, not precision entry points.

**Policy:** When the gate is open → phase in on any executable cadence → hold through.  
No mechanical closer has proven reliable. The gate is a **state**, not an event.

---

## 2. Asset Classification

Assets are grouped by observed AB4 signal frequency and behavior on daily charts.

### Tier 1 — Core Equity/MR (Preferred)
**Assets:** QQQ, SPY, IWM, GLD, XLE, XLP

- Signal rate: Very low (typically 2–5%)
- Window character: Infrequent, relatively durable clusters
- PMCC suitability: **High** — aligns well with “phase in and hold”
- Alerting tone: Clean, high-conviction windows. Minimal caveats required.

### Tier 2 — Higher-Frequency Growth (Use with Caution)
**Assets:** TSLA, NVDA, AVGO, MU, MRVL

- Signal rate: Moderate to high (8–18%)
- Window character: Frequent openings and closings; shorter duration
- PMCC suitability: **Marginal** — windows are noisier; higher risk of over-deployment
- Alerting tone: Must flag higher frequency. Recommend more conservative phasing or smaller initial size.

### Tier 3 — Acceptable with Caveats
**Assets:** AMZN, TSM, LLY, CEG, ETN, VST

- Signal rate: Low to moderate
- Window character: Generally acceptable, but less clean than Tier 1
- PMCC suitability: Acceptable with monitoring
- Alerting tone: Standard messaging with light context if needed.

### Tier 4 — Not Recommended
**Assets:** MSTR, BTC, and any other high-volatility or structurally different names

- These assets do not reliably produce the intended recovery-window behavior under current parameters.
- MSTR remains on the SRI engine. BTC and pure momentum names are out of scope for this gate.

---

## 3. Alerting & Reporting Rules

When generating AB4 Window reports or alerts, messaging must reflect the asset’s tier:

- **Tier 1 assets**: Standard “AB4 WINDOW OPEN — Phase & Hold” language is sufficient.
- **Tier 2 assets**: Add a short qualifier, e.g.:
  - “AB4 WINDOW OPEN (higher-frequency name — consider conservative sizing)”
- **Tier 3 assets**: Standard language unless recent behavior deviates.
- **Tier 4 assets**: Do not include in AB4 Gate reporting.

Reports should include:
- Current state (OPEN / CLOSED)
- Days window has been open (if applicable)
- Tier classification (for context)
- One-line note only when the asset is Tier 2

---

## 4. Parameter Notes

The current parameters (Price < 200wMA + RSI(14) < 35 + 200wMA 52w slope > 0) were calibrated primarily on Tier 1 assets.

- Tier 2 names may benefit from future tightening (e.g., RSI < 30 or steeper slope requirement).
- No parameter changes are approved at this time. Any tuning must be proposed, tested, and approved before implementation.

---

## 5. Relationship to Broader Doctrine

- This file is subordinate to `trading-rules.md` (AB4 window policy — HOLD THROUGH).
- It is also subordinate to the General Law recorded in `lessons-active.md`:
  > Any rule keyed to confirmed momentum or regime fires at the wrong moment because confirmation is only available after the move it would have you act on.

The AB4 Gate is intentionally kept as a **slow, state-based** condition. Additional layers (SRI Differential, regime exits, drawdown stops, etc.) have been tested and falsified.

---

## 6. Update Criteria

This doctrine should be reviewed when:
- New assets are added to the reporting list
- Significant changes in signal behavior are observed on existing assets
- A parameter change is proposed for any tier

**Last reviewed:** 2026-07-13 (initial version)