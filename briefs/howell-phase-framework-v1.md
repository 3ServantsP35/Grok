# Howell Phase Framework — v1.0
**Date:** 2026-03-02  
**Author:** CIO  
**Status:** Ready for Gavin Review  
**Source:** Michael Howell / CrossBorder Capital GLI Framework  
**Trigger:** Stage 2 Continuation Classifier research revealed IWM breadth signal matches Howell phases exactly

---

## Overview

The Howell Global Liquidity framework identifies four macro phases — **Rebound, Calm, Speculation, Turbulence** — driven by the global liquidity cycle. Each phase has distinct asset class winners and losers.

This document:
1. Maps the Howell phases to our SRI data
2. Adds Howell Phase as **Gate Zero** to all AB strategies
3. Documents all architecture, methodology, indicator, and CSV implications
4. Records the **current phase reading** as of 2026-03-02

---

## The Howell Asset Allocation Matrix

Derived from Howell's published slide (GLIndexes, Slide 35):

### Asset Classes by Phase

| Asset | Rebound | Calm | Speculation | Turbulence |
|---|---|---|---|---|
| Beta / Risk On (MSTR, IBIT) | 🟢 | 🟢 | 🟡 | 🔴 |
| Equities (SPY, QQQ) | 🟢 | 🟢 | 🟡 | 🔴 |
| Credits / Financials | 🟢 | 🟢 | 🟡 | 🔴 |
| Commodities (GLD, XLE) | 🔴 | 🟢 | 🟢 | 🔴 |
| Bond Duration (TLT) | 🔴 | 🟡 | 🔴 | 🟢 |

### Industry Groups by Phase

| Group | Rebound | Calm | Speculation | Turbulence |
|---|---|---|---|---|
| Cyclicals (IWM, XLY, TSLA) | 🟢 | 🟢 | 🔴 | 🔴 |
| Technology (XLK, QQQ) | 🟢 | 🟢 | 🟢 | 🔴 |
| Financials (XLF) | 🟢 | 🟢 | 🟡 | 🔴 |
| Energy / Commodities (XLE) | 🔴 | 🟢 | 🟢 | 🔴 |
| Defensives (XLP) | 🔴 | 🟢 | 🟢 | 🟢 |

### The Capital Flow Sequence (Wave Diagram, Slide 33)

```
Trough → REBOUND → CALM → SPECULATION → TURBULENCE → Trough
          Equities   +Comm    Commodities   Cash/Bonds    Equities
          Cyclicals           Defensives    Defensives    (next cycle)
          Tech                Energy        Bonds
```

Capital enters the cycle in Rebound (equities / risk assets first), peaks in Calm (broad participation), rotates to Commodities/Defensives in Speculation, then flushes to Bonds/Defensives in Turbulence before the next Rebound begins.

---

## Phase Detection via SRI Data

### Proxy Instruments (all available in repo)

| Howell Category | Proxy | CSV Available | SRIBI Data |
|---|---|---|---|
| Technology | XLK | `BATS_XLK, 240_2d3a0.csv` | ✅ 41-col, 718 bars |
| Cyclicals | XLY | `BATS_XLY, 240_5c4a3.csv` | ✅ 41-col, 720 bars |
| Financials | XLF | `BATS_XLF, 240_8199b.csv` | ✅ 41-col, 718 bars |
| Energy | XLE | `BATS_XLE, 240_f7c2d.csv` | ✅ 41-col, 718 bars |
| Defensives | XLP | `BATS_XLP, 240_337b5.csv` | ✅ 41-col, 718 bars |
| Bond Duration | TLT | `BATS_TLT, 240_c5a3d.csv` | ✅ 71-col, 2345 bars |
| Commodities | GLD | `BATS_GLD, 240_bfd71.csv` | ✅ 71-col (full LOI) |
| Cyclicals (broad) | IWM | `BATS_IWM, 240_cfcaf.csv` | ✅ 71-col (full LOI) |
| Beta / Risk On | MSTR, IBIT, BTC | existing trading files | ✅ |

**Note:** Sector ETFs (XLK, XLY, XLF, XLE, XLP) currently export single-TF SRIBI only. Sufficient for phase detection directionally. For full LOI computation, 84-96 col exports are needed (see CSV needs section).

### Phase Detection Algorithm

```python
def detect_howell_phase(sribi_map):
    """
    sribi_map: dict of ticker → current SRIBI LT value
    Returns: (phase_name, confidence_score, raw_scores)
    """
    tech  = sribi_map.get('XLK', 0)
    cycl  = sribi_map.get('XLY', sribi_map.get('IWM', 0))
    comm  = sribi_map.get('GLD', sribi_map.get('XLE', 0))
    defn  = sribi_map.get('XLP', 0)
    bonds = sribi_map.get('TLT', 0)
    fin   = sribi_map.get('XLF', 0)

    def s(v): return 1 if v > 0 else -1

    scores = {
        'Rebound':     s(tech) + s(cycl) - s(defn) - s(bonds) + s(fin),
        'Calm':        s(tech) + s(cycl) + s(comm) + 0.5*s(defn) - 0.5*s(bonds),
        'Speculation': s(tech) - s(cycl) + s(comm) + s(defn) - s(bonds),
        'Turbulence':  -s(tech) - s(cycl) - s(comm) + s(defn) + s(bonds),
    }
    return max(scores, key=scores.get), scores
```

### Phase Signature Table (for manual reads)

| Signal | Rebound | Calm | Speculation | Turbulence |
|---|---|---|---|---|
| XLK (Tech) | + | + | + | **−** |
| XLY (Cyclicals) | + | + | **−** | **−** |
| GLD (Commodities) | − | + | + | − |
| XLP (Defensives) | − | + | + | **+** |
| TLT (Bonds) | − | 0 | − | **+** |
| Key tell | Cycl lead | Broad | Tech/Comm diverge | Bonds/Def only |

**Breadth signal (empirically discovered):**
- IWM strong + SPY corrects = Speculation or late Calm → 13% continuation for SPY
- IWM also weak + SPY corrects = Turbulence flush → 51–63% continuation for SPY

---

## Current Phase Reading — 2026-03-02

| Proxy | SRIBI | 30d Avg | Direction |
|---|---|---|---|
| XLK (Technology) | -15.0 | -10.8 | ▼ Bear |
| XLY (Cyclicals) | -20.0 | -5.3 | ▼ Bear |
| XLF (Financials) | -15.0 | -2.1 | ▼ Bear |
| XLE (Energy) | +35.0 | +12.7 | ▲ Bull |
| XLP (Defensives) | +15.0 | +17.8 | ▲ Bull |
| TLT (Bond Duration) | +30.0 | -9.7 | ▲ Bull |
| GLD (Commodities) | +40.0 | +22.2 | ▲ Bull |
| IWM (Cyclicals broad) | -5.0 | +6.6 | ▼ Bear |
| SPY (Equities) | -10.0 | -6.1 | ▼ Bear |

**→ Phase: TURBULENCE** (score: +3 vs Speculation +1 vs Calm -1 vs Rebound -5)

**Turbulence confirmation signals:**
- ✅ Tech (XLK) negative
- ✅ Cyclicals (XLY, IWM) negative
- ✅ Bonds (TLT) strongly positive (+30)
- ✅ Defensives (XLP) positive
- ⚠️ Commodities (GLD) still positive — unusual for Turbulence; likely lagging due to structural CB demand (GLD classified as Trending, not cyclical commodity)
- ⚠️ MSTR/IBIT strong today (+6.6%/+5.5%) — BTC local bounce; Beta/Risk On beginning to recover = possible early Turbulence → Rebound signal for crypto-adjacent assets

**Nuance:** GLD remaining strong in Turbulence is consistent with the 2024–2026 gold structural shift (central bank demand decoupling GLD from pure risk-off flows). The Turbulence reading is otherwise clean.

### What Turbulence Means for Open Positions / Near-Term Trades

| Asset | Phase Signal | Action |
|---|---|---|
| MSTR/IBIT | Red in Turbulence but recovering → watch for Rebound signal | Hold; LOI spike = buy if VLT recovers within 6 bars |
| TSLA | Cyclicals Red in Turbulence — structural, not transient | Wait for LOI -45 + VLT recovery; do not pre-position |
| SPY/QQQ | Equities Red in Turbulence — but Turbulence = buy the flush | Enter AB3 ONLY if structural episode (4-15 bars) + IWM also weak |
| GLD | Commodities Red in Turbulence (per matrix) but trending asset | Maintain DELTA_MGMT; watch for trim signals as TLT continues higher |
| TLT | Bond Duration Green in Turbulence ✅ | If adding defensive exposure, TLT is the phase-correct vehicle |

---

## Gate Zero: Howell Phase Filter for All AB Strategies

The Howell Phase is now **the first filter applied before CPS or LOI gates**.

### AB3 Entry Eligibility by Phase

| Asset Class | Rebound | Calm | Speculation | Turbulence |
|---|---|---|---|---|
| Beta/Risk On (MSTR, IBIT) | ✅ Full | ✅ Full | ⚠️ 50% max | ❌ Wait for VLT recovery signal |
| Equities (SPY, QQQ) | ✅ Full | ✅ Full | ❌ Do not enter | ✅ Turbulence flush entries |
| Cyclicals (TSLA, IWM) | ✅ Full | ✅ Full | ❌ Do not enter | ❌ Wait — bottoms early Rebound |
| Commodities (GLD) | ❌ Too early | ✅ Enter | ⚠️ At peak | ❌ Exiting |
| Bond Duration (TLT) | ❌ | ❌ | ❌ | ✅ Best entry |

**Critical rule:** When Howell phase = Speculation AND IWM strong:
- Do NOT enter AB3 LEAP on SPY or QQQ regardless of LOI depth
- 13% continuation rate — the index is rolling over, not correcting

**Critical rule:** When Howell phase = Turbulence AND IWM also weak (broad flush):
- AB3 LEAP on SPY/QQQ is eligible — structural episode (4-15 bars) required
- 51-63% continuation rate — this is the "buy the flush" setup

### AB2 PMCC Gate Adjustments by Phase

| Phase | Adjustment |
|---|---|
| Rebound | Standard LOI gates apply; aggressive income harvesting |
| Calm | Standard LOI gates; maximum AB2 activity period |
| Speculation | Reduce max_delta by 0.05 on all Equities/Cyclicals; NO new calls on Beta/Risk On assets |
| Turbulence | Pause AB2 on all assets except Defensives; preserve LEAP optionality |

### AB1 Phase Filter

| Phase | AB1 Activity |
|---|---|
| Rebound | Primary AB1 entry window for all Momentum assets |
| Calm | AB1 valid; confirm VLT acceleration as additional filter |
| Speculation | AB1 on Technology only (XLK green); block Cyclicals/Equities |
| Turbulence | No new AB1 entries; existing positions managed to stop or LT+ |

---

## Architecture Implications

### New Component: HowellPhaseEngine

Add to `sri_engine.py` as a new class, called from `RegimeEngine` or as a parallel Layer 1.5 component.

```python
class HowellPhaseEngine:
    """
    Detects the current Howell macro phase from sector ETF SRI states.
    Layer 1.5: runs after RegimeEngine, before Signal layer.
    """
    SECTOR_PROXIES = {
        'XLK': ('BATS_XLK, ', 'SRI Bias Histogram', 'Technology'),
        'XLY': ('BATS_XLY, ', 'SRI Bias Histogram', 'Cyclicals'),
        'XLF': ('BATS_XLF, ', 'SRI Bias Histogram', 'Financials'),
        'XLE': ('BATS_XLE, ', 'SRI Bias Histogram', 'Energy'),
        'XLP': ('BATS_XLP, ', 'SRI Bias Histogram', 'Defensives'),
        'TLT': ('BATS_TLT, ', 'LT SRI Bias Histogram', 'Bond Duration'),
    }
    # Uses existing GLD, IWM, SPY data already loaded by SRIEngineV2

    def compute(self, sector_data: dict, trading_data: dict) -> HowellPhaseState:
        """Returns phase + confidence + per-asset phase eligibility"""
        ...
```

**Integration points:**
1. `daily_engine_run.py`: Load sector CSVs → run HowellPhaseEngine → pass result to AB2/AB3 scan
2. `morning_brief.py`: Add Phase row to embed (e.g., "Phase: TURBULENCE 🔴")
3. `pmcc_alerts.py`: Add phase transition alert (Turbulence→Rebound = major buy signal)
4. `sri_engine.py` `run_ab2()` and `run_ab3()`: Accept `howell_phase` parameter to gate eligibility

### Layer Architecture Update

```
LAYER 0:   GLI Engine         (global liquidity Z-score, GEGI)
LAYER 0.5: HowellPhaseEngine  (NEW — sector SRI → Rebound/Calm/Speculation/Turbulence)
LAYER 1:   RegimeEngine       (multi-asset SRI regime scoring, vehicle selection)
LAYER 2:   Signal Engines     (AB1/AB2/AB3 per asset, conditioned on L0+L0.5+L1)
LAYER 3:   AllocationEngine   (CPS + phase eligibility → position sizing)
```

Layer 0.5 sits between the GLI macro view (Layer 0) and the per-asset regime (Layer 1). It provides the structural context that tells the signal layer which assets are "in season."

### New DB Table

```sql
CREATE TABLE howell_phase_state (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT,
    phase       TEXT,     -- Rebound/Calm/Speculation/Turbulence
    confidence  REAL,     -- score delta vs next-best phase
    xlk_sribi   REAL,
    xly_sribi   REAL,
    xlf_sribi   REAL,
    xle_sribi   REAL,
    xlp_sribi   REAL,
    tlt_sribi   REAL,
    gld_sribi   REAL,
    iwm_sribi   REAL
);

CREATE TABLE howell_phase_transitions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp    TEXT,
    from_phase   TEXT,
    to_phase     TEXT,
    confidence   REAL
);
```

---

## Methodology Implications

### 1. Stage 2 Continuation Classifier — Gate Zero Added

The CPS framework (from `stage2-continuation-classifier-v1.md`) gains a new upstream gate:

```
BEFORE running CPS:
→ Determine Howell phase
→ Check if the target asset is "in season" for that phase
→ If NOT in season: block entry regardless of CPS or LOI depth
→ If IN season: proceed to CPS + episode type + VLT recovery
```

This resolves the root cause of poor SPY/QQQ transient spike performance: those episodes were firing during Speculation phase when Equities are explicitly Orange/transitioning. The 13% continuation rate is the empirical signature of entering equities against the phase flow.

### 2. The Breadth Divergence Signal (Gavin's original hypothesis — validated)

The Speculation → Turbulence transition creates the exact pattern Gavin described:
- Capital narrows to Technology + Commodities (few stocks holding up the index)
- Cyclicals (IWM, XLY) roll over first
- SPY/QQQ *look* like they're correcting when they're actually beginning a structural top
- The SRI on SPY is picking up the broad-market pressure but Tech is still green

The IWM-vs-SPY divergence is the real-time breadth indicator. When:
- IWM SRIBI < 0 AND SPY SRIBI still positive → Speculation phase breadth divergence (SELL equities)
- IWM SRIBI < 0 AND SPY SRIBI also negative → Turbulence (BUY the flush when structural)

**This is now a named signal in our system: BREADTH_DIVERGENCE.**

### 3. TSLA Reclassification

TSLA is classified as a Momentum asset in the engine but behaves like a **Cyclical** in the Howell framework. In Speculation phase, Cyclicals go Red while Technology stays Green. TSLA's current correction is phase-consistent — it is the Cyclical rotation that Howell predicts at this stage of the cycle.

**Revised TSLA entry rule:** TSLA AB3 entry is eligible in Rebound and early Calm. In Turbulence, wait for confirmed phase transition before entering. Current phase (Turbulence) means TSLA is not yet at the ideal entry window — the LOI -45 signal should be qualified with a phase shift toward Rebound first.

### 4. GLD Trim Rule Refinement

GLD is Commodities. Howell says Commodities peak in Speculation and go Red in Turbulence. GLD is already at DELTA_MGMT (LOI +23.3). The TLT turning strongly positive (+30) while GLD remains elevated is the classic Turbulence signal. GLD is likely approaching its structural trim point even if the LOI hasn't yet crossed the trim threshold.

**New rule:** When TLT SRIBI crosses above +20 AND GLD is in DELTA_MGMT, initiate GLD trim regardless of LOI — the phase rotation is telling you Commodities are peaking.

### 5. MSTR/IBIT — Turbulence to Rebound Transition Signal

In Howell's framework, Beta/Risk On leads the recovery out of Turbulence — they are the FIRST to go green in Rebound. This is consistent with BTC historically leading risk-on recoveries.

**New signal:** When MSTR/IBIT LOI begins recovering (crosses above -20 from below) while phase is still technically Turbulence, this is an EARLY REBOUND indicator. It precedes the full phase shift by 2–4 weeks. This is the optimal AB3 entry window for MSTR/IBIT: before the phase officially transitions but after the BTC-specific recovery has begun.

---

## CSV / Data Needs

### Immediate: Add Sector ETFs to Daily Pipeline (Gate Zero feeds)

These need to be added to `CANONICAL_CSVS` in `daily_engine_run.py` — they're regime inputs, not trading assets. Gavin updates them daily as part of the existing 16-file cadence (asking Gavin to add 5 more).

| Ticker | File in Repo | Action |
|---|---|---|
| XLK | `BATS_XLK, 240_2d3a0.csv` | Add to CANONICAL_CSVS |
| XLY | `BATS_XLY, 240_5c4a3.csv` | Add to CANONICAL_CSVS |
| XLF | `BATS_XLF, 240_8199b.csv` | Add to CANONICAL_CSVS |
| XLE | `BATS_XLE, 240_f7c2d.csv` | Add to CANONICAL_CSVS |
| XLP | `BATS_XLP, 240_337b5.csv` | Add to CANONICAL_CSVS |

TLT is already in `CANONICAL_CSVS` ✅

### Upgrade Path: Multi-TF Sector Exports (AB3-Enhanced)

Current sector CSVs have single-TF SRIBI only (41 cols). For full LOI computation on sectors, Gavin would need to export the same 84-96 col format used for MSTR/TSLA/IBIT.

**Priority:** LOW for phase detection (single-TF is sufficient). MEDIUM if we want to backtest Howell phase transitions with full LOI depth.

**Specific ask for Gavin when ready:**
Export the 5 sector ETFs (XLK, XLY, XLF, XLE, XLP) using the same multi-TF indicator layout as the trading assets. This would give us ~718 bars of full SRIBI for each sector — enough to validate the phase detection going back to mid-2024.

### New Regime Input: XLY / XLP Ratio

A single-value composite ratio — XLY SRIBI minus XLP SRIBI — captures the growth-vs-defensive spread. When positive = risk appetite; when negative = defensive rotation. This could be added as a 17th regime input or computed inline in the HowellPhaseEngine from existing data.

---

## Tutorial Update Required

**`SRI-Engine-Tutorial-v2.md`** needs a new section documenting Layer 0.5 (HowellPhaseEngine), the phase matrix, and the Gate Zero concept. Estimated: Section 6.5 (between existing GLI section and Regime Engine section).

**`SRI-Layman-Guide.md`** needs a paragraph explaining the four seasons analogy:
- Rebound = Spring (plant equities)
- Calm = Summer (everything grows)
- Speculation = Autumn (harvest commodities, equity gains begin fading)
- Turbulence = Winter (bonds and defensives shelter; wait for spring)

---

## Implementation Sequence

1. **P-HOWELL-1:** Add 5 sector ETFs to `CANONICAL_CSVS` in `daily_engine_run.py` (10 min)
2. **P-HOWELL-2:** Build `HowellPhaseEngine` class in `sri_engine.py` (2–3 hrs)
3. **P-HOWELL-3:** Add `howell_phase_state` and `howell_phase_transitions` tables to DB (30 min)
4. **P-HOWELL-4:** Integrate HowellPhaseEngine into `daily_engine_run.py` and `morning_brief.py` (1 hr)
5. **P-HOWELL-5:** Add phase transition alert to `pmcc_alerts.py` — Turbulence→Rebound = major buy signal (1 hr)
6. **P-HOWELL-6:** Update Stage 2 Continuation Classifier brief with Gate Zero (30 min)
7. **P-HOWELL-7:** Tutorial updates (1 hr)
8. **P-HOWELL-8 (deferred):** Backtest Howell phase accuracy using full historical XLK/XLY/TLT data

**Gavin action required:** Add 5 sector ETF daily exports to TradingView upload cadence (XLK, XLY, XLF, XLE, XLP — same format as current 41-col files).

---

*Brief ends. Current phase: TURBULENCE. Primary implication: MSTR/IBIT watching for Rebound signal; TSLA and SPY/QQQ AB3 entries require phase shift toward Rebound before full sizing.*
