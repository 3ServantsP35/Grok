# P-BEAR Phase 2 — Portfolio Defensive Posture Spec v1.0

**Date:** 2026-03-03  
**Author:** CIO Engine (subagent)  
**Status:** IMPLEMENTED — live in sri_engine.py / pmcc_alerts.py / morning_brief.py

---

## Purpose

Phase 1 detects distribution tops per-asset (PBearEngine → PBearSignal → PBearState).  
Phase 2 defines **what to DO** at the portfolio level when signals fire:

- Synthesise cross-asset P-BEAR signals into a single **PortfolioPosture**
- Wire the **AB2 fast-gate** so call-selling halts automatically on FORMING+ assets
- Monitor **Expression 3** (Bearish mNAV Contraction) trigger conditions
- Persist all state to DB and fire Discord alerts on transitions

---

## PortfolioPosture Levels

| Level | Ordinal | Trigger Condition | AB4 Floor | AB3 New | Expr3 |
|-------|---------|------------------|-----------|---------|-------|
| NORMAL | 0 | No asset FORMING+ | 10% | ✅ yes | ⬜ no |
| CAUTIOUS | 1 | 1+ asset FORMING | 10% | ✅ yes | ⬜ no |
| DEFENSIVE | 2 | 2+ assets FORMING OR 1+ CONFIRMED | 15% | 🚫 halt | ⬜ no |
| MAX_DEFENSIVE | 3 | 2+ CONFIRMED OR any CONFIRMED_PLUS | 20% | 🚫 halt | ✅ yes |

### Per-Level Actions

**NORMAL 🟢**
- Standard allocation. AB2 call-selling allowed per LOI gate.
- No distribution signals detected.

**CAUTIOUS 🟡**
- AB2 paused on affected asset(s) via fast-gate (`pbear_forming=True` propagated to `gate_state()`).
- No other restrictions — AB4 floor and AB3 unchanged.
- Log in morning brief with asset names.

**DEFENSIVE 🟠**
- AB4 floor rises to 15% hard (override AGENTS.md 10% default).
- No new AB3 entries on any asset regardless of LOI signal.
- Existing AB2 positions under review — do not roll/extend.

**MAX_DEFENSIVE 🔴**
- AB4 floor rises to 20% hard.
- Expression 3 trade entry eligible (all 4 conditions still required independently).
- Begin reducing AB3 positions on confirmed assets.
- No new AB3 or AB2 anywhere.

---

## AB4 Floor Overrides Per Posture

```
NORMAL        = 10%  (standard AGENTS.md floor)
CAUTIOUS      = 10%  (AB2 paused is sufficient; no capital reallocation needed)
DEFENSIVE     = 15%  (build dry powder for hedges and opportunistic re-entry)
MAX_DEFENSIVE = 20%  (hard capital preservation; Expression 3 sized from here)
```

These override the 10% hard floor defined in AGENTS.md for the duration of the elevated posture.  
The 10% true-cash-only requirement remains in force inside the override (i.e. at DEFENSIVE,  
15% total AB4 required with at minimum 10% in true cash).

---

## AB2 Fast-Gate Wiring

The AB2 fast-gate ensures that call-selling halts the moment a P-BEAR FORMING signal fires,  
without requiring a manual gate override.

### Data Flow

```
SRIEngineV2.run_all()
  │
  ├─ [Layer 2a] pbear_sigs = self.run_pbear()
  │             → Dict[asset → PBearSignal]
  │             → PBearSignal.ab2_fast_gate = True when state >= FORMING
  │
  ├─ [Layer 2b] defensive_state = DefensivePostureEngine.compute(pbear_sigs)
  │
  └─ ab2_sigs = self.run_ab2(reg, gli_state=gli_state, pbear_sigs=pbear_sigs)
                │
                └─ For each asset:
                     pbear_flag = pbear_sigs[asset].ab2_fast_gate  # True/False
                     pmcc.scan(df, asset, ..., pbear_forming=pbear_flag)
                     pmcc.current_signal(df, asset, ..., pbear_forming=pbear_flag)
                                │
                                └─ gate_state(..., pbear_forming=pbear_flag)
                                   → if pbear_forming: return PMCCGateState.NO_CALLS
```

### Key Code Change (run_ab2 signature)

```python
def run_ab2(self, regime=None, gli_state=None, pbear_sigs: Dict = None) -> Dict:
    ...
    pbear_forming_sig = (pbear_sigs or {}).get(asset, None)
    pbear_flag = pbear_forming_sig.ab2_fast_gate if pbear_forming_sig else False
    signals = pmcc.scan(df, asset, ..., pbear_forming=pbear_flag)
    current = pmcc.current_signal(df, asset, ..., pbear_forming=pbear_flag)
```

### Rationale String When Gated

```
"P-BEAR fast-gate: distribution forming (MSTR)"
```

This surfaces in the AB2 gate table in morning_brief.py so the analyst knows  
WHY the gate is closed, not just that it is.

---

## Expression 3 Trigger Conditions

**Trade Structure:**  
Long MSTR debit put spread (ATM/OTM 20-25%, 90-120 DTE) + Long IBIT  
Net: Long mNAV contraction — profits from MSTR premium compression regardless of BTC direction  
Sizing: MSTR put spread notional 1.5-2.0x IBIT dollar equivalent

**ALL 4 conditions required for ARMED status:**

| # | Condition | Threshold | Current (2026-03-03) |
|---|-----------|-----------|----------------------|
| 1 | mNAV > 2.0x | MSTR market cap / (717,130 BTC × BTC price) | 0.91x ❌ |
| 2 | MSTR P-BEAR >= FORMING | distribution signal active | INACTIVE ❌ |
| 3 | Howell Phase ∈ {Speculation, Turbulence} | GLI deteriorating | Turbulence ✅ |
| 4 | BTC LT SRIBI rolling over | current LT < max(prior 5 bars) - 5pt | True ✅ |

**Current status: 👁 WATCH (2/4 conditions)**

**Alert levels:**

| Conditions Met | Level | Alert Code |
|----------------|-------|-----------|
| 4/4 | ARMED 🚨 | EXPRESSION3_ARMED |
| 3/4 | SETUP 🟠 | EXPRESSION3_SETUP |
| 2/4 | WATCH 👁 | (no alert — informational only) |
| 0-1/4 | INACTIVE ⚪ | (no alert) |

> Alerts fire only on **level transitions** — not on every run.

---

## Alert Codes

| Code | Trigger | Color |
|------|---------|-------|
| `PORTFOLIO_POSTURE_CHANGE` | Any posture level transition | 🟡 0xFFAA00 (CAUTIOUS) / 🔴 0xFF4444 (DEFENSIVE+) |
| `EXPRESSION3_SETUP` | Expression 3 reaches 3/4 conditions | 🟠 0xFF8800 |
| `EXPRESSION3_ARMED` | Expression 3 reaches 4/4 conditions | 🔴 0xFF0000 |
| `PBEAR_FORMING` | Per-asset: primary bearish signal fires | (existing) |
| `PBEAR_CONFIRMED` | Per-asset: dual-TF confirmed | (existing) |

---

## DB Tables

### defensive_posture_log

```sql
CREATE TABLE IF NOT EXISTS defensive_posture_log (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp            TEXT NOT NULL,
    posture              TEXT NOT NULL,        -- NORMAL/CAUTIOUS/DEFENSIVE/MAX_DEFENSIVE
    forming_assets       TEXT,                 -- comma-separated
    confirmed_assets     TEXT,                 -- comma-separated
    ab4_floor            REAL,                 -- 0.10/0.10/0.15/0.20
    ab3_new_entries      INTEGER,              -- 1=yes, 0=halt
    expression3_eligible INTEGER,              -- 1=yes, 0=no
    rationale            TEXT
);
```

### expression3_log

```sql
CREATE TABLE IF NOT EXISTS expression3_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    level           TEXT NOT NULL,    -- INACTIVE/WATCH/SETUP/ARMED
    conditions_met  INTEGER,
    mnav            REAL,
    mstr_pbear      TEXT,
    howell_phase    TEXT,
    btc_lt_sribi    REAL,
    btc_lt_rolling  INTEGER           -- 1=rolling, 0=stable
);
```

---

## Current Portfolio Posture (2026-03-03 ~20:15 UTC)

```
Posture:         🟢 NORMAL
Rationale:       NORMAL: no distribution signals
AB4 floor:       10% (standard)
AB3 new entries: ✅ yes
Expr3 eligible:  ⬜ no

Per-asset P-BEAR states:
  MSTR  ⚪ INACTIVE  (LOI=-16.9, below WATCH threshold +40)
  IBIT  ⚪ INACTIVE  (LOI=-10.3, below WATCH threshold +20)
  TSLA  ⚪ INACTIVE  (LOI=-50.9, below WATCH threshold +40)
  SPY   ⚪ INACTIVE  (LOI=-26.2, below WATCH threshold +20)
  QQQ   ⚪ INACTIVE  (LOI=-32.8, below WATCH threshold +20)
  GLD   ⚪ WATCH     (LOI=+52.2 > +20 threshold) — monitoring divergence
  IWM   ⚪ INACTIVE  (LOI=-28.1, below WATCH threshold +20)

Expression 3:    👁 WATCH (2/4 conditions)
  ✅ Howell Turbulence | ✅ BTC LT SRIBI rolling over
  ❌ mNAV 0.91x (need >2.0x) | ❌ MSTR P-BEAR INACTIVE
```

> GLD at LOI=+52.2 is above the WATCH threshold (+20) but only at WATCH state —  
> no FORMING signals detected yet (OBV divergence AND RSI4H divergence both required  
> for GLD FORMING per TRENDING class ladder).

---

## Integration Notes

1. **Order dependency**: `run_pbear()` MUST complete before `run_ab2()` — enforced in `run_all()` since 2026-03-03.
2. **Lazy initialisation**: `DefensivePostureEngine` and `Expression3Engine` are instantiated on first `run_all()` call (None → class, since they're defined after `SRIEngineV2` in the file).
3. **Morning brief**: Section 8.5 computes posture independently (re-runs PBearEngine) rather than reading from result cache, ensuring the brief is always fresh even when called standalone.
4. **DB persistence**: Every `run()` call in pmcc_alerts.py saves posture + expr3 state. Alerts fire only on **transitions** — not on every save.
5. **BTC data for Expr3**: Uses `regime_engine._cache.get('BTC')` → falls back to `_load('BTC')`. If BTC CSV unavailable, `btc_lt_rolling=False` (condition 4 stays unmet — conservative default).
