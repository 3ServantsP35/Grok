# #mstr-cio Project Tracker
**Managed by:** Gavin (rizenshine5359) — Project Manager
**Updated:** 2026-03-01

---

## Active Projects

### P1: Allocation Bucket Framework (Multi-Asset Rotation)
**Status:** 🟡 v2.0 In Progress — Major architecture shift: multi-asset rotation
**Lead:** Gavin + CIO | **Approver:** Greg + Gavin
**Brief:** `briefs/four-bucket-framework-v1.2.md` (v1.x), v2.0 TBD
**Incorporates:** Former P3 (Alt Investment Framework) — consolidated Feb 27

| Milestone | Status | Date |
|---|---|---|
| Initial three-bucket framework (v1.0) | ✅ Complete | Feb 25 |
| RORO + STRC integration (v1.2.1) | ✅ Complete | Feb 26 |
| Architecture v1.0 approved (RP/BC/CT/AB naming) | ✅ Complete | Feb 27 |
| Multi-TF concordance validated (4 TFs) | ✅ Complete | Feb 27 |
| **Multi-asset rotation discovery** | ✅ Backtested | Feb 27 |
| All assets compete for AB1-3 by CT signal quality | ✅ Proven | Feb 27 |
| P3 (Alt Framework) consolidated into P1 | ✅ Done | Feb 27 |
| v2.0 brief: multi-asset rotation rules, asset pools per bucket | ✅ Written — four-bucket-framework-v2.0.md | Mar 5 |
| Tiered CT gates per asset class (quality CT3+, risk CT4) | ✅ Codified in v2.0 brief | Mar 5 |
| Greg + Gavin sign-off on v2.0 | ⬜ Pending review | — |
| Production integration (Morning Brief, alerts) | ⬜ Pending sign-off | — |

**Key decisions needed:**
- [ ] Greg/Gavin sign-off on multi-asset rotation (AB1-3 open to all assets)
- [ ] Asset pool per bucket (which assets eligible for AB1 vs AB2 vs AB3)
- [ ] Tiered CT gates: quality assets at CT3+, risk assets at CT4 only?
- [ ] Greg/Gavin sign-off on STRC hurdle + Path B LEAPs
- [ ] ~~20% cap on alternatives~~ → obsolete, all assets equal in rotation

---

### P2: Bear Trigger — Bearish Ruleset & Indicators
**Status:** 🟡 Active (Year-Long)
**Lead:** Gavin (indicators) + CIO (backtesting) | **Target:** Production-ready by Stage 3 of next cycle
**Brief:** Section 1B of Four-Bucket Framework + standalone brief TBD

| Milestone | Status | Date |
|---|---|---|
| SOPR < -0.2 backtested (MSTR daily) | ✅ Complete — 100% 5d bear, n=7 | Feb 25 |
| STRS regime backtest (MSTR daily) | ✅ Complete — falling fast 83% bear, n=6 | Feb 25 |
| Risk Oscillator backtest (BTC daily) | ✅ Complete — weak standalone signal | Feb 25 |
| SOPR/STRS backtest on BTC data | ⬜ Next | — |
| Gavin exports STRS-specific TradingView data | ⬜ Waiting on Gavin | — |
| Risk Oscillator combo signals (more data) | ⬜ Ongoing | — |
| Formalize bearish tier system (v1) | ✅ In framework v1.2 | Feb 25 |
| P4+C3 exit signal validated | ✅ -14.2% at 40d, n=15 | Feb 26 |
| Stage 2→3 transition detection | ⬜ Future | — |
| Standalone Bear Trigger brief | ⬜ Pending | — |

**Indicators in scope:**
- [x] STH-SOPR (Mirrored) — PRIMARY bearish trigger
- [x] STRS (Short-Term Risk Score) — confirmation + regime
- [x] Risk Oscillator — regime only, not directional
- [x] RORO P4+C3_DISTRIBUTION — EXIT signal (-14.2% at 40d)
- [ ] Additional indicators from Gavin (TBD)

---

### P3: ~~Alt Investment Framework~~ → CONSOLIDATED INTO P1
**Status:** 🔀 Merged into P1 (Multi-Asset Rotation)
**Reason:** Backtest proved AB1-3 should not be MSTR/IBIT-only. All assets compete for every bucket based on CT signal quality. "Alternatives" are just another asset in the rotation pool. Separate framework unnecessary.

---

### P4: RORO — Risk-On / Risk-Off Framework
**Status:** 🟢 Core Framework Complete — GLI Forecast Outstanding
**Lead:** Gavin (Howell research, RORO concept) + CIO (backtesting) | **Approver:** Greg + Gavin
**Brief:** Integrated into `briefs/four-bucket-framework-v1.2.md` (Parts 2A-2J)

| Milestone | Status | Date |
|---|---|---|
| **Deliverable A: RORO Capital Rotation** | | |
| 5-phase rotation model defined (13 assets, 4 tiers) | ✅ Complete | Feb 26 |
| RORO backtest (3,728 days, 2011-2026) | ✅ Complete | Feb 26 |
| SRIBI breadth composite (continuous RORO score) | ✅ Complete | Feb 26 |
| BTC forward returns by RORO quintile (monotonic edge confirmed) | ✅ Complete | Feb 26 |
| BTC cycle phases defined (C4→C1→C2→C3 via FTL/STL+SRIBI) | ✅ Complete | Feb 26 |
| RORO × BTC Cycle co-occurrence map | ✅ Complete | Feb 26 |
| P1+C1 trap rule identified and quantified (-4.2% at 40d, n=92) | ✅ Complete | Feb 26 |
| Anchored allocation table (RORO × BTC Cycle → Buckets) | ✅ Complete | Feb 26 |
| Expected cycle progression sequence | ✅ Complete | Feb 26 |
| RORO integrated with Four-Bucket Framework (v1.2) | ✅ Complete | Feb 26 |
| RORO daily automation (phase classification script) | ⬜ Pending | — |
| **Deliverable B: GLI Forecast** | | |
| GLI proxy validated (4-bank) | ✅ Built | Feb 22 |
| BTC-GLI lead/lag backtest (BTC leads 6mo) | ✅ Complete | Feb 25 |
| GLI forecast model (leading indicators → 13w horizon) | ✅ Built — GLIForecaster class | Mar 5 |
| GLI confidence bands (±1σ) | ✅ Built | Mar 5 |
| Peak/trough calling | ✅ Built (4w consecutive momentum) | Mar 5 |
| BTC 13w directional signal from GLI | ✅ Built | Mar 5 |
| Forecast slope/direction reconciliation | 🔄 Calibration needed | Mar 5 |
| **Deliverable C: Howell Integration** | | |
| Howell charts analyzed | ⬜ Blocked (image permissions) | — |
| Howell thesis vs our RORO findings comparison | ✅ Done — btc-outlook-30k-vs-55k.md | Mar 5 |

---

### P5: Daily Trading Alerts
**Status:** 🟡 Running but not fully automated
**Lead:** CIO | **Approver:** Greg (all trades)
**Brief:** Trading rules in `mstr-knowledge/trading-rules.md`

| Milestone | Status | Date |
|---|---|---|
| Morning Brief automation (cron) | ✅ Built, needs cron trigger | Feb 23 |
| EOD Recap automation | ✅ Built | Feb 23 |
| Intraday alerts (7 types) | ✅ Built | Feb 22 |
| T1 shares filled (3K @ $128.59) | ✅ Complete | Feb 24 |
| CCs executed (20x $140C + 10x $150C) | ✅ Complete | Feb 24 |
| IC Apr 17 execution | 🟡 Pending Greg fill | Feb 25 |
| RORO phase + BTC cycle in Morning Brief | ⬜ Pending P1 sign-off | — |
| STRC hurdle check on trade recs | ⬜ Pending P1 sign-off | — |
| Portfolio-specific routing (#mstr-greg) | ⬜ Pending webhook in .env | — |
| Preferred stock alerts (SCHI) | 🟡 Script ready, needs cron | Feb 25 |
| P1+C1 trap alert (warn against directional) | ⬜ Pending P1 sign-off | — |
| FTL/STL crossover monitoring in alerts | ⬜ Pending P1 sign-off | — |
| SOPR/STRS bearish alerts | ⬜ Pending P2 progress | — |

**Current positions (Greg):**
- 3,000 MSTR shares @ $128.59
- 20x $140C Mar 20 (sold), 10x $150C Mar 20 (sold)
- IC Apr 17 $105/$95P + $145/$155C (executing)
- ~$4.61M cash → **convert to STRC per v1.2**

---

## Project Dependencies

```
P4 (RORO) ──→ P1 (Bucket Framework) ──→ P5 (Daily Alerts)
                  │        ↑                     ↑
                  │    P6 (Concordance)      P2 (Bear Trigger)
                  │        ↑                     ↑
                  │    P7 (Architecture)     P14 (Bearish Suite) ←── structural context for P2
                  │    ↑── naming/structure for all
                  ↓
             P3 ─── CONSOLIDATED INTO P1
             P8 (TV Indicators) ←── HIGH PRI, needs P7+P6 first
             P9 (MSTR/IBIT Pair) ←── independent
             P10 (Momentum vs MR) ←── informs asset signal weights
             P14 (Bearish Suite) ──→ AB2 Bear Call enablement
                                 ──→ Iron Condor gating
                                 ──→ AB3 trim confirmation
```

**Critical path:** P7 (architecture) → P6 (codify concordance) → P1 (update framework) → P5 (production)
**Parallel work:** P2 (bearish events), P4-B (GLI forecast), P8 (asset behavior brief), P14 (bearish bias framework)

---

### P6: Multi-TF SRI Integration & Concordance System
**Status:** 🟡 Active — MSTR backtested, TSLA/GLD pending
**Lead:** Gavin + CIO | **Approver:** Gavin
**Brief:** `briefs/multi-tf-backtest-btc-spy.md`, `briefs/mstr-concordance-backtest.md`

| Milestone | Status | Date |
|---|---|---|
| Pine Scripts created (8 fixed-TF variants) | ✅ Complete | Feb 27 |
| Gavin exports new multi-TF CSVs (BTC, SPY) | ✅ Complete | Feb 27 |
| Multi-TF backtest (BTC + SPY) | ✅ Complete | Feb 27 |
| **4-Tier Concordance Entry System discovered** | ✅ Backtested | Feb 27 |
| BTC ST timeframe data gap identified | 🔴 Gavin investigating | Feb 27 |
| **MSTR concordance backtest** | ✅ Complete — CT1=78% bull regime | Mar 5 |
| Key finding: CT1 regime-dependent (0% bear, 95% bull) — GLI required | ✅ Documented | Mar 5 |
| Key finding: CT4 = distribution signal on MSTR (-32% at 20d, Dec 24) | ✅ Documented | Mar 5 |
| Codify Concordance Tiers into formal spec | 🔄 In progress — P1 v2.0 has CT gates | Mar 5 |
| TSLA concordance backtest | ⬜ Pending CSV | — |
| GLD concordance backtest | ⬜ Pending CSV | — |
| Rebuild RORO with multi-TF SRIBI | ⬜ Pending remaining exports | — |
| Retire Three-Tier FTL/STL framework | ⬜ Pending Gavin approval | — |

**Key findings (to codify):**
- T1 SCOUT (VST>0 + LT/VLT rising): 50% win, earliest entry, LEAP-only
- T2 EARLY (VST>0 + LT>0 + VLT>-20): 55% win, ~44 days before T3, sweet spot
- T3 CONFIRMED (all TFs > 0): 57% win, baseline
- T4 HIGH CONVICTION (all > 0 + VLT > +20): 63% win, full size
- 1/3 breadth trap: -1.31% at 20d (validates P1+C1 trap rule)
- VST is precision entry tool, NOT directional indicator (confirms Gavin's tutorial)
- SOPR < -0.2 only bullish when ALL SRIBI negative (capitulation vs distribution)

---

### P7: Framework Architecture Consolidation
**Status:** ✅ Architecture Approved — Mar 5, 2026
**Lead:** CIO (recommendation) + Gavin (approval) | **Approver:** Gavin
**Brief:** `briefs/SRI-Engine-Tutorial-v2.md` (v2.1 — canonical architecture document)

**Architecture (final, 4 layers):**
```
Layer 0: GLI Engine  →  global liquidity probability adjusters (FRED proxy + GEGI)
Layer 1: Regime Engine  →  8 market inputs → composite score + vehicle selection
Layer 2: Signal Layer  →  AB1 / AB2 / AB3 per asset
Layer 3: Allocation Engine  →  bucket tracking, floors, ceilings, transitions
```

Gavin review (Mar 5): *"Consider the architecture reviewed. The big missing piece has been filled (GLI/GEGI)."*

| Milestone | Status | Date |
|---|---|---|
| Inventory all frameworks (10 identified) | ✅ Complete | Feb 27 |
| Three-layer architecture proposed (Regime/Signal/Allocation) | ✅ Draft | Feb 27 |
| Naming cleanup table | ✅ Draft | Feb 27 |
| **Layer 0 (GLI/GEGI) identified as missing piece** | ✅ Built + wired | Mar 5 |
| **Gavin review & approval** | ✅ Approved | Mar 5 |
| Formal architecture spec — Tutorial v2.1 | ✅ Published | Mar 5 |
| Merge/retire redundant frameworks | ⬜ Ongoing | — |
| Morning Brief restructure to match 4-layer architecture | ⬜ Pending P5 | — |

---

### P8: TradingView Pine Scripts — Mirror / Visualization Layer
**Status:** 🟡 Pivoting — scripts become mirrors of Python engine (P12)
**Lead:** CIO (build) + Gavin (test/iterate) | **Approver:** Gavin
**Brief:** TBD

**Pivot (Mar 1):** Pine scripts no longer contain signal logic. They visualize what the Python engine sees — tracklines, SRIBI zones, context backgrounds, and engine-generated signal markers. This ensures Gavin can coach and diagnose from TradingView while the engine makes decisions.

| Milestone | Status | Date |
|---|---|---|
| AB1 v5 + AB2 v3 + AB3 v3 built (signal logic in Pine) | ✅ Complete but superseded | Feb 28 |
| **PIVOT: Signal logic moves to Python engine (P12)** | ✅ Decision | Mar 1 |
| "SRI Data Export" script (raw data for CSV export) | ⬜ Pending | — |
| "SRI Dashboard" mirror script (reflects engine state) | ⬜ Pending P12 Phase 2 | — |
| Gavin validation: can see what engine sees | ⬜ Pending | — |

---

### P9: MSTR/IBIT Pair Trading
**Status:** ⬜ Queued
**Lead:** Gavin + CIO | **Approver:** Gavin
**Brief:** TBD

| Milestone | Status | Date |
|---|---|---|
| MSTR/IBIT ratio SRI analysis | ✅ Preliminary (in Full Backtest v2) | Feb 27 |
| Pair trade strategy definition | ⬜ Pending | — |
| Backtest pair P&L | ⬜ Pending | — |
| Integration with AB system | ⬜ Pending | — |

**Context:** MSTR/IBIT ratio shows VST/ST bullish, LT/VLT bearish — premium expanding from shorter TFs up. Pair trading could capture MSTR's structural outperformance of BTC with hedged risk.

---

### P10: Trend Line Identification
**Status:** ⬜ Queued — awaiting Gavin detail
**Lead:** Gavin | **Approver:** Gavin
**Brief:** TBD

| Milestone | Status | Date |
|---|---|---|
| Gavin provides requirements/detail | ⬜ Pending | — |

---

### P12: Python Decision Engine + Web Dashboard + Automated Feed
**Status:** 🟢 Phase 1 complete. Phase 2 pivoted to web dashboard (Gavin approved Mar 5).
**Lead:** CIO | **Approver:** Gavin
**Brief:** TBD

**Architecture (revised):** TradingView = sensor. Python = brain. **Web dashboard** = primary mirror (all-asset view, all layers). Pine scripts = minimal chart overlays only (context shading, S/R, LOI panel).

| Milestone | Status | Date |
|---|---|---|
| **Phase 1: CSV Ingest + Full Engine** | | |
| CSV data spec defined | ✅ Complete | Mar 1 |
| Python CSV ingest + SRIBI parser | ✅ Complete | Mar 1 |
| ST-primary signal logic in Python | ✅ Complete | Mar 1 |
| Regime Engine (8 inputs, vehicle, VIX) | ✅ Complete | Mar 1 |
| AB1 Pre-Breakout Engine | ✅ Complete | Mar 1 |
| AB2 Credit Spread Engine (v2, MIXED gate) | ✅ Complete | Mar 3 |
| AB3 State Machine (NEUTRAL/ACC/HOLD/TRIM) | ✅ Complete | Mar 1 |
| Allocation Engine (25/25/25/25, floors/ceilings) | ✅ Complete | Mar 1 |
| GLI Engine Layer 0 (FRED proxy + GEGI) | ✅ Complete | Mar 5 |
| Layer 0 → Layer 1 wiring (RegimeEngine.compute) | ✅ Complete | Mar 5 |
| GLI Forecaster (13w horizon, peak/trough) | ✅ Complete | Mar 5 |
| All 4 layers running end-to-end | ✅ Tested | Mar 5 |
| **Phase 2: Web Dashboard (pivot from Pine mirror)** | | |
| Architecture decision: web > Pine for operational mirror | ✅ Gavin approved | Mar 5 |
| generate_dashboard.py — self-contained HTML generator | ✅ Built + tested | Mar 5 |
| Layer 0 panel (GLI Z, GEGI, components) | ✅ Complete | Mar 5 |
| Layer 1 panel (regime score, inputs, vehicle) | ✅ Complete | Mar 5 |
| Layer 2 asset grid (all 8, LOI, context, signals) | ✅ Complete | Mar 5 |
| AB1/AB2 signal detail panels | ✅ Complete | Mar 5 |
| Pine chart overlays (context shading, S/R, LOI panel) | ⬜ Pending — minimal scope | — |
| **Phase 3: Automated Feed** | | |
| Cron: daily CSV pull → engine → dashboard refresh | ⬜ Next | — |
| Discord post of regime + signals on daily run | ⬜ Pending | — |
| TradingView webhook (eliminate manual CSV) | ⬜ Research | — |

**CSV Requirements (Phase 1):**
- **Assets:** MSTR, BTC, SPY, QQQ, GLD, IWM, TSLA, IBIT (+ BLOK optional)
- **Timeframe:** 4H candles
- **Per asset:** OHLC + 4 TFs × (SRIBI, FTL, STL, RevSup, RevRes, RobustFit, 4 stage transitions) = ~44 columns
- **Delivery:** Daily push to GitHub repo root
- **No signal columns needed** — engine computes all signals

**Key Design Principles:**
1. Pine scripts mirror engine state for Gavin visibility — never diverge
2. All signal logic lives in Python — single source of truth
3. Every parameter change is instantly backtestable
4. Cross-asset context available for every decision
5. Portfolio state integrated into signal generation

---

### P14: Bearish Bias Indicator Suite — Distribution Detection Framework
**Status:** 🟡 Active — Research & Design Phase
**Lead:** Gavin (framework design) + CIO (backtesting/build) | **Approver:** Gavin
**Brief:** TBD — `briefs/bearish-indicator-suite-v1.md` (to be created)

**Purpose:**
The SRI framework is structurally bullish-biased — it was purpose-built as a Wyckoff accumulation detector. Bearish SRI crosses are unreliable as primary signals (38% accuracy in the Saylor/preferred era). This project builds a **symmetric bearish framework** with the same multi-timeframe rigor and backtesting discipline as SRI, but calibrated to identify distribution tops, markdown initiation, and structural bearish bias.

This is not P2 (Bear Trigger). P2 identifies specific bearish *events* (SOPR spikes, STRS deterioration). P14 builds a continuous bearish *bias* indicator — an oscillator that answers the same question SRI answers on the bull side: *"Is structural selling pressure building?"*

**Design Principles:**
1. **Mirror SRI's structure, not its signals.** Same multi-TF (VST/ST/LT/VLT) architecture, but calibrated for distribution detection. Stage 2→3→4 precision replaces Stage 4→1 as the primary detection target.
2. **Complement, not replace, SRI.** The two frameworks run simultaneously. SRI scores bullish bias; the new framework scores bearish bias. The spread between them is the signal.
3. **Asset-class aware.** Momentum assets (MSTR/BTC/TSLA) require different distribution signatures than mean-reverting assets (SPY/QQQ). Separate calibrations.
4. **Backtested to the same standard as SRI.** Every indicator must have quantified win rates, N counts, and forward return distributions before production.

**Candidate Indicators (to be researched and validated):**

| Indicator | Description | Priority |
|---|---|---|
| **Distribution Opportunity Index (DOI)** | Mirror of LOI — composite oscillator measuring distribution accumulation; VLT positive/decelerating + Stage 3→4 + breadth deterioration | P1 |
| **Stage 2→3 Transition Detector** | Precision detection of FTL→STL crossover from above, with confirmation filters to reduce false signals | P1 |
| **Multi-TF Bearish Breadth** | # of TFs showing negative SRIBI simultaneously, weighted by TF importance; inverse of Concordance | P1 |
| **Bearish Divergence Scanner** | Price making new highs while LT/VLT SRIBI making lower highs — classic distribution divergence | P2 |
| **Supply Absorption Oscillator** | Volume-weighted measure of selling pressure being absorbed vs overwhelmed at key price levels | P2 |
| **LOI Rollover Signal** | LOI crossing from above +60 back toward 0 with acceleration — existing AB3 trim signal, but formalized as a standalone bearish indicator | P3 |

**DOI Formula (proposed — to be validated):**
```
DOI = (VLT_SRIBI_normalized × 40) + (VLT_deceleration × 30) + (LT_SRIBI_normalized × 15) + (Bear_Breadth × 15)
```
*Note: VLT_deceleration = negative ROC on VLT SRIBI when VLT is positive (topping signal). Bear_Breadth = inverse concordance (% of TFs negative).*

Distribution zone: DOI > +60. Extreme distribution: DOI > +80.

**Integration Points:**
- **AB3 trim signals:** DOI > +60 could replace or confirm LOI-based trim thresholds
- **AB2 Bear Call enablement:** DOI > +60 on MR assets = conditions where Bear Call spreads become valid (currently disabled pending this framework)
- **Iron Condor gating:** DOI > +40 + LOI < -20 = IC setup (structural distribution AND accumulation simultaneously = range-bound)
- **P2 Bear Triggers:** DOI provides the structural context; SOPR/STRS provide the event trigger. High DOI + SOPR spike = highest-conviction bearish signal

**Open Research Questions:**
1. Does the same FTL/STL framework that detects accumulation reliably detect distribution, or does distribution have fundamentally different price mechanics?
2. Are Stage 2→3 transitions more or less reliable than Stage 4→1 as signals? (Hypothesis: less reliable on momentum assets due to Saylor effect)
3. What is the optimal VLT deceleration threshold for momentum vs MR assets?
4. Can DOI + LOI spread predict range-bound regimes better than either alone?

| Milestone | Status | Date |
|---|---|---|
| Project scoped and approved | ✅ Complete | Mar 5 |
| Literature review: Wyckoff distribution theory | ⬜ Pending | — |
| Stage 2→3 transition backtest (all 8 assets) | ⬜ Pending | — |
| Multi-TF bearish breadth backtest | ⬜ Pending | — |
| DOI formula design + initial backtest | ⬜ Pending | — |
| DOI vs LOI correlation analysis (are they independent?) | ⬜ Pending | — |
| Bearish divergence scanner backtest | ⬜ Pending | — |
| Supply absorption oscillator research | ⬜ Pending | — |
| Asset-specific calibration (Momentum vs MR vs Trending) | ⬜ Pending | — |
| Integration spec: how DOI wires into AB2/AB3/IC gating | ⬜ Pending | — |
| Pine script: DOI visualization for Gavin coaching | ⬜ Pending | — |
| Python engine: DOI class in `sri_engine.py` | ⬜ Pending | — |
| Production validation (paper trading period) | ⬜ Pending | — |
| Gavin/Greg sign-off for production deployment | ⬜ Pending | — |

**Key Dependencies:**
- P12 (Python engine) must be stable before DOI class is added
- P6 (Concordance system) — Bear Breadth is the inverse of Concordance; leverage existing logic
- P2 (Bear Trigger) — DOI provides structural context for P2 event signals; coordinate with Gavin

---

### P13: Discord Trade Journal — Automated Portfolio Tracking
**Status:** ⬜ Queued — Post-launch
**Lead:** CIO | **Approver:** Greg + Gavin
**Brief:** TBD

**Concept:** Greg, Gavin, and Gary each log trades via Discord messages in their respective channels (#mstr-greg, #mstr-gavin, #mstr-gary). The CIO engine parses these entries, tracks positions, computes P&L, and maintains each portfolio's trade journal automatically.

**Input format (proposed — simple Discord messages):**
```
BUY 100 MSTR @ $130.50
SELL 50 MSTR @ $145.20
OPEN BPS MSTR Apr 17 $120/$110 @ $3.40 x10
CLOSE BPS MSTR Apr 17 $120/$110 @ $0.80 x10
```

| Milestone | Status | Date |
|---|---|---|
| Define message parsing format (simple, typo-tolerant) | ⬜ Pending | — |
| Build Discord message listener for trade channels | ⬜ Pending | — |
| Trade log database tables (per user) | ⬜ Pending | — |
| Position tracker (open positions, avg cost, Greeks) | ⬜ Pending | — |
| P&L computation (realized, unrealized, by strategy) | ⬜ Pending | — |
| Daily/weekly portfolio summary auto-post | ⬜ Pending | — |
| Hypothesis linkage (connect trades to CIO recommendations) | ⬜ Pending | — |
| Confirmation flow (CIO echoes parsed trade for user to verify) | ⬜ Pending | — |
| **Greg portfolio** (#mstr-greg): $5M, live | ⬜ Pending | — |
| **Gavin portfolio** (#mstr-gavin): $1M paper | ⬜ Pending | — |
| **Gary portfolio** (#mstr-gary): TBD, educational | ⬜ Pending | — |

**Key Design Principles:**
1. Friction-free input — plain English in Discord, not forms or commands
2. CIO confirms every parsed trade back to the user before logging
3. Ties into hypothesis tracking — "this trade was recommended by AB1 signal on 03/01"
4. Each user sees only their own P&L; CIO sees all three for cross-portfolio analysis
5. Options P&L tracks both premium and underlying moves

---

### P11: BTC Momentum vs SPY Mean-Reversion — Asset Behavior Brief
**Status:** ⬜ Queued
**Lead:** CIO | **Approver:** Gavin
**Brief:** TBD

| Milestone | Status | Date |
|---|---|---|
| Deep-dive brief on momentum vs mean-reversion distinction | ⬜ Pending | — |
| Trading strategy implications per asset class | ⬜ Pending | — |
| Signal weight differentiation (BTC-linked vs SPY-linked) | ⬜ Pending | — |

**Context:** Multi-TF backtest showed BTC trends with SRIBI concordance (bull begets bull) while SPY mean-reverts (bearish SRIBI = best forward returns). Different signal weights needed for each. Gavin requested a detailed brief before any execution changes.

---

## Blocked Items (Need Greg)

| Item | What's Needed | Project |
|---|---|---|
| P1 sign-off on v1.2.1 | Review framework, approve STRC/Path B/trap rule | P1 → all |
| Image permissions cron | `* * * * * chmod -R o+r .../media/inbound/ 2>/dev/null` | P4-C |
| Preferred stock cron | Deploy `collect_preferred.py` to crontab | P5 |
| DISCORD_WEBHOOK_GREG in .env | `echo 'DISCORD_WEBHOOK_GREG=...' >> .env` | P5 |
| BTC $60K alert cron | Deploy `alert_btc_60k.py` | P5 |
| IC fill confirmation | Execute in brokerage, confirm fill | P5 |
| Convert cash to STRC | Brokerage order | P1 |

---

### P11: STRC Spread Monitor — Saylor Engine Fuel Gauge
**Status:** 🟢 Active — First reading collected
**Lead:** CIO | **Approver:** Gavin
**Script:** `/mnt/mstr-scripts/collect_strc_spread.py`
**Cadence:** Every 4 hours during market hours

**Thesis:** The spread between STRC's market yield (~10%) and the forward Fed Funds rate is a leading indicator for the Saylor BTC acquisition engine. Wide spread → more preferred share demand → more capital → more BTC buying.

**Current Reading (2026-02-28):**
- EFFR: 3.64% | 6m Forward: 3.37% | 12m Forward: 2.98%
- STRC Yield: 10.00% | 6m Spread: **664 bp** | 12m Spread: **702 bp**
- Engine Fuel: **FULL** — market pricing 75bp of cuts over 12 months, spread expanding

**Fuel Gauge:**
| Spread (6m fwd) | Level | Implication |
|---|---|---|
| ≥600 bp | FULL | Max capacity — strong issuance incentive |
| 500-599 bp | HIGH | Engine running strong |
| 400-499 bp | MODERATE | Slowing — watch for issuance pause |
| 300-399 bp | LOW | Narrowing — caution signal |
| <300 bp | CRITICAL | Engine may stall |

**Cron (Greg to add):**
```
0 */4 * * 1-5 cd /home/openclaw/mstr-engine && docker exec mstr-engine python3 /mnt/mstr-scripts/collect_strc_spread.py >> /mnt/mstr-logs/strc_spread.log 2>&1
```

---

### P10: SRI Forecast Indicator — Weekly Validation
**Status:** 🟢 Recurring
**Lead:** CIO | **Approver:** Gavin
**Script:** `pine/SRI_Forecast.pine` (repo) / `scripts/pine/SRI_Forecast.pine` (local)
**Cadence:** Weekly (every Monday, pre-market)

| Task | Frequency | Description |
|---|---|---|
| Backtest accuracy check | Weekly | Re-run breach risk scoring on latest BTC data. Compare predicted hold/breach vs actual outcomes for any STL approaches in the prior week. |
| Zone distribution audit | Weekly | Confirm time-in-zone percentages haven't drifted significantly from backtest baseline (gray ~69%, yellow ~22%, near ~9%). |
| AB2 signal review | Weekly | Check if any AB2 signals fired. Score outcome: did spread at STL hold? |
| Forecast ribbon accuracy | Monthly | Compare 20d forecast ribbon median vs actual 20d return for each zone. Flag any zone with >2σ deviation from backtest. |
| Optimization proposals | As needed | Propose threshold or factor weight changes based on accumulated data. Requires Gavin approval before implementation. |

**Baseline metrics (v4, BTC 2021-2026):**
- Classified accuracy: 79% (15/19)
- GREEN hold rate: 81% | LIGHT GREEN: 84% | YELLOW: 74% | RED breach: 73%
- Coverage: 68% of STL approaches classified (non-MEDIUM)

**Log:**
| Date | Result | Notes |
|---|---|---|
| 2026-02-28 | ✅ Baseline established | v4 deployed with 5-zone scheme |

---

---

## Today's Key Discoveries (Feb 27, 2026)

1. **4-Tier Concordance Entry System** — Multi-TF SRIBI alignment defines entry timing. T2 (VST>0 + LT>0 + VLT>-20) is the sweet spot: 55% win, 44 days earlier than full confirmation, +3.14% at 20d.
2. **1/3 Breadth Trap validated** — Independently confirms P1+C1 trap rule. Partial TF confirmation is worse than no confirmation (-1.31% at 20d).
3. **VST confirmed as precision entry, not directional** — Matches Gavin's Indicator Tutorial exactly. VST bullish flip with LT bearish = 44% win (noise).
4. **SOPR capitulation vs distribution** — SOPR < -0.2 is only bullish when ALL SRIBI negative. With SRIBI positive = distribution (-0.87%, 35% win).
5. **Risk-depleted + bearish SRIBI = highest-conviction accumulation** — RO < -0.3 + SRIBI avg < -20: 76% win, +7.2% at 20d, +15.6% at 40d.
6. **VLT Stage 3→4 fired Feb 1** — Only 2nd time ever (first was FTX bottom Nov 2022). Current analog: 100% win rate at 20d (n=5).
7. **BTC vs SPY behave opposite** — BTC trends with concordance, SPY mean-reverts. Different signal weights needed (P8 queued).
8. **Framework architecture consolidation proposed** — Three layers: Regime Engine → Signal Layer → Allocation Engine. 10 frameworks mapped. P7 brief delivered.

---

## Session Highlights — Mar 5, 2026

1. **Tutorial v2.1** — Section 6 (GLI Layer 0), 4-layer architecture. Commit `06b0dde4`.
2. **BTC Outlook Brief** — `btc-outlook-30k-vs-55k.md`. Commit `cf707a33`.
3. **P14 created** — Bearish Bias Indicator Suite. Design phase.
4. **GLI Engine** — `gli_engine.py`. FRED proxy (6 components), GEGI, SOFR-IORB. Commit `e31e17af`.
5. **Layer 0 wired** — `sri_engine.py` RegimeEngine.compute(gli_state=). Commit `879b2919`.
6. **P7 approved** — Gavin: *"The big missing piece has been filled."* 4-layer canonical.
7. **Web Dashboard** — `generate_dashboard.py`. Self-contained HTML, all 4 layers. Commit `fb599f35`.
8. **MSTR Concordance** — `mstr-concordance-backtest.md`. CT1=78% bull regime, 0% bear. GLI is non-optional filter. Commit `306d2477`.
9. **P1 v2.0 brief** — `four-bucket-framework-v2.0.md`. Multi-asset rotation, CT gates, all rules. Commit `fa1550c9`.
10. **GLI Forecaster** — `GLIForecaster` class in `gli_engine.py`. 13w horizon, peak/trough, BTC signal. Commit `47c9e02c`.

---

*Last updated: 2026-03-05 by CIO. Gavin manages priorities and sequencing.*
