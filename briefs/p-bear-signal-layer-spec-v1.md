# P-BEAR Signal Layer — Specification v1.0

**Date:** 2026-03-03  
**Author:** CIO Engine (subagent — P-BEAR Phase 1)  
**Status:** Implemented (Phase 1)  
**Repo:** `3ServantsP35/Grok` → `scripts/sri_engine.py`, `scripts/pmcc_alerts.py`, `scripts/morning_brief.py`

---

## Purpose & Scope

P-BEAR is the bearish top-detection layer for the MSTR/Crypto Options Engine. It detects distribution-phase transitions (markup → distribution → markdown) across all trading assets before they inflict damage on open AB2 (PMCC) call-writing positions.

**Core function:** When P-BEAR state reaches `FORMING` or above, AB2 call-selling is immediately gated (`ab2_fast_gate = True`). This protects short calls from being assigned or deep ITM as the underlying reverses.

**Phase 1 scope (this spec):**
- Per-asset bearish signal ladder (7 states)
- Integration into `SRIEngineV2.run_all()` output
- AB2 fast-gate override in `AB2PMCCEngine.gate_state()`
- Discord alerts on P-BEAR state transitions
- Morning brief P-BEAR column

**Phase 2 (future):** Portfolio-level defensive posture, Expression 3 hedge trigger, cross-asset contagion scoring.

---

## State Machine

### `PBearState` (7 states)

| Value | State | Description |
|-------|-------|-------------|
| 0 | `INACTIVE` | LOI below watch threshold — no monitoring |
| 1 | `WATCH` | LOI entered elevated zone — divergence monitoring active |
| 2 | `FORMING` | Primary bearish signal fires (per asset class) |
| 3 | `FORMING_PLUS` | Secondary signal also confirms |
| 4 | `CONFIRMED` | Dual-timeframe confirmation + LOI rolling — AB2 pause recommended |
| 5 | `CONFIRMED_PLUS` | Tertiary confirmation (strongest — use for hedge entry) |
| 6 | `INVALIDATED` | Bearish thesis invalidated — monitoring resets |

**AB2 Fast-Gate threshold:** State ≥ `FORMING` (value ≥ 2) → `ab2_fast_gate = True` → `PMCCGateState.NO_CALLS`

---

## Per-Asset-Class Confirmation Ladders

### MOMENTUM (MSTR, TSLA)
```
WATCH        → LOI > +40  (Momentum DELTA_MGMT threshold = watch start)
FORMING      → MACD_hist < 0  AND  LOI > +20
FORMING+     → RSI 4H bearish divergence confirmed
CONFIRMED    → RSI Daily divergence  +  LOI rolling over (−2pts from recent peak)
CONFIRMED+   → OBV divergence (tertiary — strongest signal)
INVALIDATION → MACD_hist > 0  AND  price within 0.2% of 20-bar high
```

### BTC_CORRELATED (IBIT)
```
WATCH        → LOI > +20
FORMING      → OBV divergence (OBV < OBV_SMA20  or  OBV < peak OBV)
FORMING+     → RSI 4H divergence also fires
CONFIRMED    → RSI Daily also diverging
INVALIDATION → OBV recovers above SMA20
```

### MR — Mean Reverting (SPY, QQQ, IWM)
```
WATCH        → LOI > +20
FORMING      → RSI 4H bearish divergence
FORMING+     → OBV < OBV_SMA20 (volume confirmation)
CONFIRMED    → RSI Daily divergence also fires
INVALIDATION → RSI 4H recovers  +  price within 0.2% of 20-bar high
```

### TRENDING (GLD)
```
WATCH        → LOI > +20
FORMING      → OBV divergence  AND  RSI 4H divergence  (simultaneous)
CONFIRMED    → Supertrend flips BEAR
INVALIDATION → Supertrend flips back BULL
```

---

## Column Mapping Table (TradingView CSV format — Track B confirmed)

| Engine Field | CSV Column Name | Notes |
|---|---|---|
| RSI 4H | `MTF RSI` | Updates every 4H bar close |
| RSI Daily | `MTF RSI.1` | Forward-filled; updates on daily close only |
| MACD histogram | `Histogram` | Standard MACD(12,26,9) histogram |
| OBV | `OnBalanceVolume` | On-Balance Volume |
| Supertrend BULL | `Up Trend` | notna = BULL active |
| Supertrend BEAR | `Down Trend` | notna = BEAR active |
| LOI | `LOI` | LEAP Opportunity Index (custom) |
| Weekly StochRSI | `%K` / `%D` | Secondary only; long warmup needed |
| Close price | `close` | Standard OHLCV |

**Divergence detection parameters:**
- Lookback window: 20 bars (4H × 20 ≈ 3.5 trading days)
- Price near peak: within 5% of local high
- RSI min gap: current RSI must be ≥ 2 pts below peak RSI
- LOI rollover: current LOI must be ≥ 2 pts below recent 5-bar peak

---

## AB2 Fast-Gate Override Rule

When `PBearSignal.ab2_fast_gate == True` (state ≥ FORMING):

```python
# In AB2PMCCEngine.gate_state():
if pbear_forming:
    return PMCCGateState.NO_CALLS  # P-BEAR fast-gate: distribution top forming
```

Rationale string: `"P-BEAR fast-gate: distribution forming ({asset})"`

**This overrides the normal LOI-based gate logic.** Even if LOI is in `OTM_INCOME` or `DELTA_MGMT` range, call-selling stops when P-BEAR detects active distribution.

The `pbear_forming` parameter must be explicitly passed into `gate_state()` and `_rationale()` by the caller. The `SRIEngineV2.run_all()` output includes `pbear_signals` dict for downstream use.

---

## Alert Code Definitions

| Code | Trigger | Color | Action Required |
|---|---|---|---|
| `PBEAR_WATCH` | INACTIVE → WATCH (LOI crosses into watch zone) | Yellow 🟡 | Monitor; no action yet |
| `PBEAR_FORMING` | any → FORMING or FORMING_PLUS | Orange 🟠 | **Stop writing new short calls immediately** |
| `PBEAR_CONFIRMED` | any → CONFIRMED or CONFIRMED_PLUS | Red 🔴 | **Evaluate hedge entry; close existing short calls** |
| `PBEAR_INVALIDATED` | FORMING+/CONF+ → INVALIDATED | Green ✅ | Resume normal AB2 protocol |

Alerts fire on **state transitions only** (not repeated on same state). State is persisted to `pbear_state_log` in `mstr.db`.

### DB Schema: `pbear_state_log`
```sql
CREATE TABLE IF NOT EXISTS pbear_state_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    asset           TEXT NOT NULL,
    state           TEXT NOT NULL,
    loi             REAL,
    signals_fired   TEXT,    -- JSON array of signal names
    ab2_fast_gate   INTEGER DEFAULT 0
);
```

---

## Current State Snapshot (2026-03-03)

| Asset | Class | P-BEAR State | LOI | Signals Active | AB2 Gated? |
|-------|-------|-------------|-----|----------------|-----------|
| MSTR | MOMENTUM | ⚪ INACTIVE | −30.5 | none | No |
| TSLA | MOMENTUM | ⚪ INACTIVE | −6.1 | MACD<0, LOI_ROLL, ST_BEAR | No |
| IBIT | BTC_CORRELATED | ⚪ INACTIVE | −20.0 | none | No |
| GLD | TRENDING | 👁 WATCH | +23.3 | none | No |
| SPY | MR | ⚪ INACTIVE | +17.4 | none | No |
| QQQ | MR | ⚪ INACTIVE | +2.2 | MACD<0, RSI4H_DIV, RSI_D_DIV, OBV_DIV, ST_BEAR | No |
| IWM | MR | ⚪ INACTIVE | +5.0 | none | No |

**Notes on current snapshot:**
- **GLD** is the only asset in WATCH zone (LOI=23.3 > 20 threshold). No divergence signals yet — monitoring active.
- **QQQ** has multiple bearish signals firing but LOI=+2.2 is below the +20 watch threshold. INACTIVE per protocol. Signals are tracked but not actionable until LOI enters watch zone.
- **TSLA** has MACD<0, LOI_ROLL, ST_BEAR but LOI=−6.1 well below MOMENTUM watch threshold (+40). Not in watch zone.
- All MSTR/BTC assets in accumulation zone — P-BEAR irrelevant. AB3 accumulation phase active for those.

---

## Implementation Details

### Files Modified
1. **`scripts/sri_engine.py`** — Added `PBearState` (Enum), `PBearSignal` (dataclass), `PBearEngine` (class); integrated into `SRIEngineV2` via `run_pbear()` and `run_all()`; updated `AB2PMCCEngine.gate_state()` and `_rationale()` with `pbear_forming` parameter.

2. **`scripts/pmcc_alerts.py`** — Added `pbear_state_log` DB schema; added alert code constants; added `load_prev_pbear_states()`, `save_pbear_states()`, `detect_pbear_alerts()` functions; integrated P-BEAR detection into `run()` pipeline.

3. **`scripts/morning_brief.py`** — Added P-BEAR column to AB2 PMCC gate state table; imports `PBearEngine`; reads from `pbear_state_log` DB first, falls back to live compute.

### Key Design Decisions
- **DB-first for morning brief**: The `pbear_state_log` table holds state between runs. Morning brief reads from DB (faster, consistent with alerts). Falls back to live compute if DB empty.
- **Signals tracked even when INACTIVE**: All individual signal flags (`macd_neg`, `rsi4h_div`, etc.) are computed regardless of state. This allows inspection of "what would fire if LOI moved into watch zone."
- **LOI as prerequisite, not signal**: LOI crossing the watch threshold is a prerequisite for P-BEAR to activate. Below the threshold, no alert fires even if all other signals are present. This prevents noise during accumulation phases.
- **Divergence lookback = 20 bars (4H)**: Covers ~3.5 trading days, sufficient to identify local tops without false positives from intraday noise.

---

## Next Steps — Phase 2

### Phase 2A: Portfolio-Level Defensive Posture
- Define `PBearPortfolioState`: aggregate signal across all assets
- Trigger portfolio-level alert when ≥2 assets in FORMING or above simultaneously
- Adjust `AllocationEngine` output to reduce AB3 deployment rate during multi-asset BEAR

### Phase 2B: Expression 3 Trigger (Hedge Entry)
- Define `Expression3Signal`: fires when any asset reaches `CONFIRMED_PLUS`
- Expression 3 = buy protective puts (or put spreads) on MSTR/IBIT as hedge
- Sizing: 5% of AB3 LEAP notional value; max 15% portfolio hedge cost basis
- Exit trigger: P-BEAR state → INVALIDATED

### Phase 2C: Cross-Asset Contagion Score
- If IBIT enters CONFIRMED while MSTR is WATCH or FORMING → escalate MSTR to FORMING immediately (BTC leads MSTR)
- If SPY+QQQ both enter CONFIRMED → flag broad market distribution; apply to all assets

### Phase 2D: Backtesting
- Validate ladder thresholds against 2021 MSTR top, 2024 BTC halving cycle top
- Measure false positive rate: how often CONFIRMED fires without >15% subsequent drawdown
- Calibrate `PRICE_NEAR_PEAK` (5%) and `RSI_DIV_MIN_GAP` (2pts) from backtesting data
