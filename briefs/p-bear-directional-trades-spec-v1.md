# P-BEAR Directional Bearish Trade Specifications — v1.0

**Date:** 2026-03-03  
**Status:** Active  
**Scope:** Non-MSTR assets (MSTR routed to Expression 3); all assets with P-BEAR CONFIRMED or above.

---

## 1. Universal Entry Rules

| Rule | Value |
|---|---|
| **Minimum state to enter** | P-BEAR **CONFIRMED** (state value ≥ 5) |
| **FORMING/FORMING_PLUS** | ❌ No entry — whipsaw risk; AB2 fast-gate only |
| **Max notional per position** | **5% of portfolio** (GLD: 3%) |
| **IV gate (at execution)** | >70th pctl → prefer spreads (sell premium); <30th pctl → prefer long puts |
| **Conflicting regime** | Check Howell phase before entry for TSLA (blocked in Turbulence) |
| **MSTR** | Routed to **Expression 3** — do not enter independently |

**Entry hierarchy:** CONFIRMED → trade eligible. CONFIRMED_PLUS → elevated conviction, same instrument, potentially larger notional (within 5% cap).

---

## 2. Per-Asset-Class Playbook

| Asset Class | Assets | Instrument | Duration (DTE) | Structure | Max Notional | Key Gate |
|---|---|---|---|---|---|---|
| **MOMENTUM** | TSLA | Debit put spread | 45–60 | ATM / OTM-10% put spread | 5% | Howell ≠ Turbulence |
| **BTC_CORRELATED** | IBIT | Long put LEAP | 90–120 | OTM 10-15% put | 5% | OBV primary bearish div |
| **MR** | SPY, QQQ, IWM | Debit put spread | 45–60 | OTM 5-10% put spread | 5% | RSI4H + RSI_D + OBV triple |
| **TRENDING** | GLD | Short-duration puts | 30–45 | OTM 5-8% puts | **3%** | Supertrend flip confirmation |

### Asset-class notes

**MOMENTUM (TSLA)**  
- Instrument: Debit put spread (ATM / OTM-10%).  
- TSLA is a **Cyclical** asset — blocked entirely in Howell Turbulence phase.  
- Confirm Howell gate before any entry. Do not enter a TSLA bearish position if Howell = Turbulence.  
- 45-60 DTE preferred: enough theta buffer; not so long that reversals erase premium.

**BTC_CORRELATED (IBIT)**  
- Instrument: Long put LEAP (90-120 DTE).  
- AB1-style sizing applies — treat as a tactical LEAP entry in bearish direction.  
- IBIT options have wider bid/ask spreads than SPY — factor spread cost into break-even calculation.  
- Entry only when OBV primary shows bearish divergence (BTC-correlated top confirmation).

**MR (SPY, QQQ, IWM)**  
- Instrument: Debit put spread (OTM 5-10%).  
- Requires triple confirmation: RSI 4H bearish div + RSI Daily bearish div + OBV bearish div.  
- IV gate interaction: if IV > 70th pctl, tighten the spread (sell premium closer to ATM); if IV < 30th pctl, widen the long put wing.

**TRENDING (GLD)**  
- Instrument: Short-duration puts (30-45 DTE).  
- GLD is a mean-reverting trend asset — tops are typically followed by sharp reversals.  
- Smaller notional (3%) reflects faster mean-reversion risk.  
- Enter only after Supertrend has confirmed a BEAR flip on the daily chart.

---

## 3. Integration with Expression 3 (MSTR)

**MSTR is not traded directly through the P-BEAR directional playbook.** When MSTR reaches P-BEAR CONFIRMED, the signal feeds into Expression 3 eligibility scoring:

| Expression 3 Condition | Source |
|---|---|
| mNAV > 2.0x | mNAV engine |
| MSTR P-BEAR FORMING+ | P-BEAR engine (this layer) |
| Howell = Speculation or Turbulence | Howell phase DB |

Expression 3 structure: **debit put spread + long IBIT put LEAP** (mNAV contraction trade).  
Activation requires ≥ 3 of 4 conditions armed (4th condition is defensive posture override).

When MSTR P-BEAR fires CONFIRMED but Expression 3 is not yet armed (e.g., mNAV < 2.0x), the CIO should:
- Note the signal in the morning brief
- Monitor for Expression 3 arm-up
- **Do not open an independent MSTR put position** outside Expression 3 structure

---

## 4. TSLA Howell Gate — Reminder

TSLA is classified as **Cyclical-Momentum**. The Howell liquidity phase gates TSLA directional trades in both directions:

| Howell Phase | TSLA Bearish Trade |
|---|---|
| Expansion | ✅ Eligible (P-BEAR CONFIRMED required) |
| Slowdown | ✅ Eligible — heightened conviction |
| Contraction | ✅ Eligible — heightened conviction |
| **Turbulence** | ❌ **BLOCKED** — forced liquidation risk |

In Turbulence, macro tail risk dominates sector signals. TSLA can spike violently in either direction on liquidity events. Do not open bearish positions in Turbulence even with P-BEAR CONFIRMED.

---

## 5. IV Regime Interaction

The IV gate is applied **at execution time**, not at signal time. P-BEAR CONFIRMED is the entry permission; IV regime determines the instrument structure.

| IV Regime | Instrument Preference | Rationale |
|---|---|---|
| Ultra-high (90th+) | Spreads — sell OTM put against long | Premium rich; recoup cost selling near wing |
| High (70–90th) | Spreads — standard debit spread | Standard vol environment |
| Normal (30–70th) | Debit spreads (standard) | Minor premium cost |
| Low (<30th) | Long puts / LEAPs only | Cheap premium — pay up for convexity; avoid selling vol |

**GLD exception:** GLD put duration is already compressed (30-45 DTE) to account for mean-reversion. IV gate still applies to structure, but do not extend duration chasing premium.

**IBIT exception:** LEAP structure (90-120 DTE) is fixed regardless of IV. At high IV, cost will be elevated — accept or scale notional down to remain within 5% cap.

---

## 6. Signal Output Fields (bearish_trade_spec() return)

When P-BEAR >= CONFIRMED, `PBearSignal.bearish_trade_spec()` returns:

```python
{
    'asset':               str,   # e.g. 'QQQ'
    'instrument':          str,   # e.g. 'Debit put spread'
    'duration_dte':        str,   # e.g. '45-60'
    'structure':           str,   # Entry structure description
    'max_notional_pct':   float,  # 0.05 or 0.03 for GLD
    'notes':               str,   # Per-asset-class guidance
    'pbear_state':         str,   # e.g. 'CONFIRMED' or 'CONFIRMED_PLUS'
    'signals_confirmed':  List[str],  # Individual signals that fired
    'ab2_fast_gate_active': bool,  # Always True at CONFIRMED+
}
```

Returns `None` for states below CONFIRMED (INACTIVE, WATCH, FORMING, FORMING_PLUS).

---

## 7. Morning Brief Integration

The morning brief includes a **⚠️ Bearish Trade Opportunities** block when any asset reaches CONFIRMED or above. This block appears within the Portfolio Defensive Posture section (section 8.5), below the confirmed-assets list.

Format:
```
⚠️ Bearish Trade Opportunities (P-BEAR CONFIRMED)
• QQQ [CONFIRMED]: Debit put spread 45-60 DTE | OTM 5-10% put spread; RSI4H + RSI_D + OBV triple confirmation
  Max notional: 5% | IV gate: >70th pctl → tighter spread (sell premium); <30th → wider long put.
```

If no assets are at CONFIRMED or above, the block is suppressed entirely.

---

## 8. Change Log

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-03-03 | Initial spec — per-asset-class playbook, IV gate, Expression 3 routing, Howell gate |
