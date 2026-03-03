# Stage 2 Continuation Classifier — v1.1
**Date:** 2026-03-02 | **Revised:** 2026-03-02 (v1.1 — Gate Zero added)
**Author:** CIO  
**Status:** Production — Gate Zero integrated, Howell Phase Engine live  
**Dataset:** 221 labeled correction episodes, 7 assets (MSTR/TSLA/IBIT/SPY/QQQ/GLD/IWM), 2022–2026

---

## The Problem

When LOI crosses the accumulation threshold (-45 for Momentum, -40 for MR), the system fires an AB3 watch signal. Two scenarios are indistinguishable at the trough:

- **Stage 2 Continuation:** Temporary correction within an intact bull trend. Price recovers and sets new highs. AB3 LEAP entry here produces outsized gains.
- **Stage 3/4 Reversal:** Structural breakdown beginning. Lower prices ahead. AB3 entry here causes early capital deployment into a declining asset.

The current framework handles this by requiring a "Stage 2 bounce confirmation" before entering — but this sacrifices significant entry quality (often 10–25% off the trough before confirmation fires).

**This classifier identifies high-probability continuations earlier, enabling better LEAP entry pricing.**

---

## Key Findings

### Finding 1: Single Features Are Weak (Expected)
No individual feature at the LOI trough has correlation > |0.15| with the continuation/reversal label across the full multi-asset dataset. The trough-bar snapshot alone does not contain sufficient information.

**Why:** The data spans multiple macro regimes (2022 bear, 2023–2024 recovery, 2024–2026 bull). A feature that signals continuation in a bull regime signals reversal in a bear regime. A regime-agnostic classifier is inherently limited.

---

### Finding 2: The Dominant Signal Is VLT Recovery Speed (Not Trough Features)

The single most powerful predictor is **how fast VLT recovers above zero after the trough** — measured at +6, +12, and +20 bars.

| Bars After Trough | CONTINUATION | REVERSAL | Gap |
|---|---|---|---|
| +6 bars: VLT > 0 | 52% | 42% | +10% |
| +12 bars: VLT > 0 | 82% | 58% | +24% |
| +20 bars: VLT > 0 | **100%** | 94% | +6% |

**Critical insight:**
- **100% of labeled continuation episodes** had VLT recover above zero within 40 bars (median: **6 bars = 1.5 trading days**)
- 8 reversal episodes never crossed zero in 40 bars
- At +12 bars, VLT>0 creates a 82% vs 58% split — **the operationally actionable gate**

**Operational rule:** When LOI crosses -45, start a 12-bar VLT clock. VLT>0 at ≤6 bars = strong continuation. VLT still negative at 12+ bars = increasing reversal probability. Still negative at 20 bars = abort.

---

### Finding 3: Counterintuitive — Strong Prior Bull = Lower Continuation Probability

Tested: Does a strong prior VLT context (structural VLT avg from 120 to 60 bars before trough) predict continuation?

| Prior Structural VLT | Continuation Rate |
|---|---|
| Bear context (< -10) | 45% |
| Weak negative (-10 to 0) | **52%** ← Best zone |
| Weak positive (0 to +10) | 40% |
| Strong bull (> +10) | 37% ← Worst zone |

**Counter-intuitive finding:** Corrections that occur after a strong sustained bull (high structural VLT) have the LOWEST continuation rate. This is the late-cycle signal: elevated structural VLT means the asset has already run far and is more vulnerable to a genuine stage turn.

**Implication:** Don't deploy early into "obvious" bull market corrections on momentum assets that have been running hard for 3+ months. That is precisely when Stage 3 distributions masquerade as corrections.

---

### Finding 4: Episode Type Has Asset-Specific Patterns

**Transient (1–3 bars below threshold) vs Structural (4–15 bars) vs Extended (>15 bars):**

| Episode Type | Overall | MSTR | TSLA | SPY | QQQ |
|---|---|---|---|---|---|
| Transient (1–3 bars) | 41% | **60%** | **57%** | 26% | 30% |
| Structural (4–15 bars) | **50%** | 50% | 42% | **71%** | 50% |
| Extended (>15 bars) | 39% | 33% | 50% | 40% | **75%** |

**Pattern by asset class:**

- **Momentum assets (MSTR, TSLA, IBIT):** Transient spikes are the PRIMARY entry signal (57–60%). These are BTC-acceleration-driven LOI spikes that self-correct quickly when BTC stabilizes. Structural episodes carry lower conviction unless confirmed by CPS ≥ 50.

- **Mean-reverting assets (SPY, QQQ):** Transient spikes are NOISE (26–30%). The primary signal is the Structural episode — a genuine oversold condition (71% for SPY). For QQQ, extended episodes are even better (75%, though n=4).

---

### Finding 5: CPS ≥ 50 + Structural Episode = 62.5% Continuation

Combining the Structural episode filter (4–15 bars) with CPS ≥ 50 gives the best pre-confirmation signal across all assets: **62.5% continuation rate** (n=16, all assets combined).

This is the only combination that meaningfully clears the 56% "always predict reversal" baseline.

---

## The Classifier Framework

### Gate Zero: Howell Phase + IWM Breadth Filter

**This gate runs BEFORE CPS, episode typing, or VLT clock. A failed Gate Zero hard-blocks entry regardless of how favorable downstream signals appear.**

Gate Zero answers a single question: *Is this asset class currently "in season" per the Howell liquidity cycle?*

#### Step 1 — Howell Phase Check

| Asset | Phase eligibility for AB3 entry |
|---|---|
| MSTR / IBIT (Beta/Risk On) | Rebound ✅ Full · Calm ✅ Full · Speculation ⚠️ 50% max · Turbulence ❌ Wait |
| SPY / QQQ (Equities) | Rebound ✅ · Calm ✅ · Speculation ❌ Block · Turbulence ✅ Flush entries only |
| TSLA / IWM (Cyclicals) | Rebound ✅ · Calm ✅ · Speculation ❌ Block · Turbulence ❌ Wait |
| GLD (Commodities) | Rebound ❌ · Calm ✅ · Speculation ✅ (approaching peak) · Turbulence ❌ Exiting |

**Current phase (live, 2026-03-02): 🌧️ TURBULENCE**
- MSTR/IBIT: ❌ Blocked (phase 0% multiplier) — wait for Rebound signal
- TSLA: ❌ Blocked (Cyclicals blocked in Turbulence)
- SPY/QQQ: ✅ Eligible (Turbulence flush — but IWM Breadth Gate required, see Step 2)
- GLD: ❌ Exiting phase — no new AB3

**Phase transition as early Rebound signal:** When MSTR/IBIT LOI begins recovering from deeply negative territory while phase is still Turbulence, this is the first leading indicator of a Turbulence→Rebound transition. The Howell Phase Engine fires a `HOWELL_PHASE_TRANSITION` Discord alert the moment the phase shifts. That alert is the primary AB3 entry trigger for Beta assets.

#### Step 2 — IWM Breadth Gate (SPY/QQQ only)

This gate applies exclusively when SPY or QQQ LOI crosses the -40 accumulation threshold. It determines whether the correction is a broad-market flush (entry eligible) or a narrow/concentrated sell (skip entirely).

**IWM state at the SPY/QQQ LOI trough (AT the trough bar, not prior trend):**

| IWM State | Breadth Signal | Entry Decision |
|---|---|---|
| IWM headwind (LT<0 AND VLT<0) | Broad flush — capital leaving all segments | ✅ Proceed to CPS + episode type |
| IWM neutral or bull | Narrow/isolated correction — Howell Speculation top signal | ❌ Hard block — do not enter |

**Why this matters:** When SPY/QQQ corrects while IWM holds firm, capital has rotated from cyclicals to mega-cap tech/quality equity (Howell Speculation phase breadth divergence). The index appears to correct but the broad market has already rolled over. Backtested continuation rate in this configuration: **10–13%**. Not a buying opportunity — it is the beginning of structural breakdown in SPY itself.

When IWM is also weak at the SPY trough (broad flush): **51–63% continuation rate** in Structural episodes. The only actionable SPY/QQQ AB3 setup.

**This signal is named `BREADTH_DIVERGENCE` in the system.** It fires when IWM LOI > 0 AND SPY LOI < -20 simultaneously.

#### Gate Zero Decision Tree

```
LOI crosses accumulation threshold
         │
         ▼
  Check Howell Phase
  ┌──────┴──────────┐
  │                 │
Asset in season?   Asset out of season?
  │                        │
  ▼                        ▼
For SPY/QQQ:          ❌ BLOCKED
  Check IWM state          (even if CPS=80, VLT recovers fast)
  │
  ├─ IWM headwind → ✅ Proceed to CPS + Episode Type → VLT Clock
  └─ IWM strong   → ❌ BLOCKED (BREADTH_DIVERGENCE)
```

---

### Three-Stage Gate System (Stages A–C, run only after Gate Zero passes)

**STAGE A — Episode Typing (real-time, as LOI drops below threshold)**

Monitor episode duration as it unfolds. Do not wait for the trough to be confirmed — classify in real time.

```
TRANSIENT (LOI < threshold, ≤3 bars):
  → Momentum assets (MSTR/TSLA/IBIT): HIGH alert — enter 25% position on next 4H bar
  → MR assets (SPY/QQQ/GLD/IWM): LOW alert — do not enter, wait for Structural confirmation
  
STRUCTURAL (LOI < threshold, 4-15 bars):
  → All assets: MEDIUM alert — enter 25% position at trough, scale on VLT recovery
  → If CPS ≥ 50: upgrade to HIGH alert — enter 50% position

EXTENDED (LOI < threshold, >15 bars):
  → All assets: HOLD — reversal probability rising
  → Enter ONLY if VLT makes meaningful recovery while still in zone (rare)
  → Best strategy: wait for full VLT recovery then enter at better price
```

**STAGE B — VLT Recovery Clock (starts at LOI trough bar)**

Track VLT value at each subsequent 4H bar. This is the operational entry gate.

```
VLT > 0 within ≤6 bars of trough:
  → STRONG CONTINUATION SIGNAL
  → Scale to full position (add remaining allocation)
  → Start tracking: AB3 LEAP at this entry price

VLT > 0 within 7–12 bars of trough:
  → MODERATE CONTINUATION SIGNAL  
  → Scale to 75% position — less conviction but directionally valid

VLT still negative at 12 bars:
  → WARNING — reversal probability now dominant
  → Reduce to 25% position or hold cash

VLT still negative at 20 bars:
  → ABORT — full reversal pattern
  → Close or reduce any existing position
  → Wait for full VLT recovery before reassessing
```

**STAGE C — CPS Score (computed at trough bar, before Stage B fires)**

The CPS informs initial sizing at Stage A/B, not the go/no-go decision (which belongs to VLT recovery).

```
CPS = weighted composite of 4 inputs (0–100 scale):

C1: Structural VLT context (120–60 bars prior)      Weight: 35%
    < -10 (bear context):     40 pts
    -10 to 0 (recovery phase): 65 pts  ← best zone
    0 to +10 (mild bull):     55 pts
    > +10 (elevated bull):    30 pts   ← late-cycle warning

C2: VLT depth at trough                              Weight: 25%
    VLT > -15 (shallow):      60 pts
    VLT -15 to -25:           50 pts
    VLT -25 to -40:           40 pts
    VLT < -40 (deep):         25 pts

C3: VLT vs LT spread at trough                       Weight: 25%
    (VLT - LT) > +10:         65 pts  ← structural support intact
    (VLT - LT) 0 to +10:     55 pts
    (VLT - LT) -10 to 0:     45 pts
    (VLT - LT) < -10:         35 pts  ← both TFs collapsing together

C4: Recent VLT momentum (prior 60-bar avg)           Weight: 15%
    avg > +15:                50 pts
    avg +5 to +15:            55 pts
    avg -5 to +5:             50 pts
    avg < -5:                 40 pts
```

**CPS interpretation:**

| CPS | Implication | Sizing at Stage A |
|---|---|---|
| ≥ 55 | Favorable structural context | 50% initial position |
| 50–54 | Neutral-favorable | 25% initial position |
| 45–49 | Neutral | 15% initial position — wait for Stage B |
| < 45 | Unfavorable context | No initial position — wait for Stage B only |

---

## Asset-Specific Entry Rules

### Momentum Assets: MSTR, TSLA, IBIT

**Gate Zero note — TSLA is a Cyclical in the Howell framework.** While MSTR/IBIT are Beta/Risk On assets eligible in Rebound and Calm, TSLA follows the Cyclicals path: blocked in both Speculation and Turbulence phases. In the current Turbulence phase, TSLA AB3 entry is hard-blocked at Gate Zero regardless of LOI depth or CPS score. Resume entry eligibility when phase shifts to Rebound.

**Primary pattern:** Transient LOI spike (1–3 bars) during a period when BTC/market is stabilizing. These are mechanical acceleration-driven spikes, not structural breakdowns.

**Entry sequence:**
1. LOI crosses -45 → check episode type in real time
2. If Transient + VLT > -20 (shallow): enter 25% immediately — no waiting
3. VLT clock: VLT > 0 within 6 bars → scale to full position
4. If Structural (4–15 bars): wait for VLT clock; enter 25% at trough, scale at VLT > 0
5. If Extended (>15 bars): hold; enter on VLT recovery while LOI still compressed

**CPS special note for MSTR:** When BTC is in a confirmed Stage 2 (LOI > 0 on BTC charts) and MSTR LOI spikes below -45, the continuation rate is expected to be materially higher than the historical 52–60% average. The BTC structural context functions as an implicit CPS booster — treat any MSTR LOI spike during BTC Stage 2 as HIGH priority regardless of the standalone CPS reading.

### Mean-Reverting Assets: SPY, QQQ, GLD, IWM

**Primary pattern:** Structural episodes (4–15 bars) represent genuine oversold conditions that tend to resolve higher.

**Gate Zero applies first — SPY/QQQ require BOTH Howell phase eligibility AND IWM breadth gate.**

**Entry sequence:**
1. **Gate Zero:** Howell phase must allow equity entries (Rebound/Calm/Turbulence flush). In Speculation, hard block regardless of LOI depth.
2. **Gate Zero (SPY/QQQ only):** Check IWM state AT the LOI trough. IWM headwind (LT<0 AND VLT<0) required. IWM neutral or bullish = BREADTH_DIVERGENCE = skip entirely.
3. LOI crosses threshold → DO NOT enter on transient spike (26–30% continuation rate; only Structural episodes in MR assets)
4. Monitor: if episode extends to 4+ bars → elevate to MEDIUM alert
5. CPS ≥ 50: enter 25% at trough
6. VLT clock: VLT > 0 within 6 bars → scale to full position
7. Transient spikes < 4 bars: ignore unless they cluster (3+ within 30 bars = accumulation pressure)

---

## What This Changes in the Framework

### Current AB3 protocol (pre-classifier):
- Wait for LOI < accumulation threshold
- Wait for Stage 2 bounce confirmation (price recovers, VLT turns positive)
- Enter LEAP on bounce confirmation
- Miss: Entry is 10–25% above the actual trough price

### New AB3 protocol (with classifier + Gate Zero):
- **Gate Zero:** Howell Phase check → phase-eligible or blocked. IWM breadth check for SPY/QQQ.
- LOI crosses threshold (only if Gate Zero passes) → immediate episode-type classification
- **Momentum + Transient spike:** 25% position immediately; scale on VLT>0 at ≤6 bars
- **All assets + Structural + CPS≥50:** 25% position at trough; scale on VLT>0
- **Extended episode:** Hold; enter on VLT recovery while still compressed
- Miss: Eliminated for Transient entries; reduced from 10–25% to 5–10% for Structural entries

**Key insight Gate Zero provides:** The 13% SPY/QQQ continuation rate on IWM-isolated spikes is explained entirely by the Howell Speculation phase. Those signals were not broken — they were correctly identifying that SPY was at a structural Speculation-phase top, not a buying opportunity. Gate Zero prevents deploying capital into this configuration.

### Capital deployment impact:
The classifier enables partial deployment (~25%) at the trough price on high-confidence signals, before the full Stage 2 bounce confirmation. The remaining 75% deploys on VLT recovery (Stage B gate). This preserves the structural safety of Stage 2 confirmation for the majority of the position while capturing superior pricing on the initial tranche.

---

## What the Classifier Does NOT Solve

1. **Bear market entries:** The classifier was trained including 2022 bear market data. Many "continuation" signals in that data ultimately failed at 6-month horizons. The GLI Z-score and macro regime must remain as an external override — if GLI Z < -1.0, downgrade all CPS readings by 15 points.

2. **Extended episodes in bear/neutral regime:** If the macro regime is Neutral or Bearish and the episode extends beyond 15 bars, the classifier has limited ability to distinguish a "violent but temporary" drop from a structural collapse. In these cases, default to standard Stage 2 bounce protocol (wait for full confirmation).

3. **Single-asset idiosyncratic risk:** The classifier uses SRI/LOI signals which are price-action derived. It cannot detect company-specific events (TSLA Musk controversy, MSTR BTC accounting issues) that can cause structural selling the SRI doesn't anticipate. Fundamental monitoring remains essential.

---

## Calibration Notes

The current classifier is calibrated on 221 episodes spanning 2022–2026. The best validated accuracy is:
- **Structural + CPS ≥ 50 → 62.5% continuation** (n=16, small but consistent with per-asset patterns)
- **Transient + Momentum assets → 57–60% continuation** (n=22 combined MSTR+TSLA)
- **VLT > 0 at ≤12 bars → 82% continuation** (n=80, strongest signal, lagging)

The classifier should be re-run quarterly as new bars are added. The calibration thresholds (CPS weights, VLT clock bars) should be reviewed after each major market cycle.

---

## Application: TSLA as of 2026-03-02

| Input | Value | CPS Component |
|---|---|---|
| Structural VLT prior (120–60 bars): | ~+8 (mild bull) | C1 = 55 pts |
| VLT at last trough bar (3/2 18:30): | -10 (shallow) | C2 = 60 pts |
| VLT-LT spread: | +10 (VLT less negative) | C3 = 65 pts |
| Prior 60-bar VLT avg: | ~+5 | C4 = 55 pts |
| **CPS** | | **≈ 57** |

LOI = -35 (10 pts from -45 threshold). Episode not yet active.

**Projection:** If LOI crosses -45 in the next 1–2 sessions:
- VLT currently at -10 → likely Transient or early Structural episode
- CPS ≈ 57 (borderline favorable)
- Momentum asset → apply Momentum entry rules
- **Action:** 25% LEAP position at first LOI < -45 bar; scale to full on VLT > 0 within 6 bars
- **Kill:** VLT still negative at 12 bars → hold at 25% only; VLT negative at 20 bars → close and wait

Price entry estimate: $370–$395 if LOI reaches -45 at current trajectory.

---

## Next Steps

1. **Add VLT Recovery Clock to `pmcc_alerts.py`** — alert when VLT crosses zero after a LOI trough event *(pending)*
2. **Add episode-type classifier to `sri_engine.py`** — real-time Transient/Structural/Extended label in scan output *(pending)*
3. **Add CPS computation to `daily_engine_run.py`** — publish CPS in morning brief when any asset is in LOI watch zone *(pending)*
4. **Backtest improvement:** Re-label using "new price high within 120 bars" instead of "+5% at 60 bars" to reduce false negatives on slow-recovery continuations *(pending)*
5. **Regime conditioning:** Separate analysis for GLI > 0 vs GLI < 0 subsets — expected to materially improve all accuracy metrics *(pending)*
6. **Monthly recalibration:** Run as part of monthly review when new CSV data arrives *(ongoing)*

### Completed (v1.1)
- ✅ **Gate Zero — Howell Phase Engine** live in `sri_engine.py` (Layer 0.5, commit `df64b23c`)
- ✅ **Gate Zero — IWM Breadth Filter** documented and integrated into SPY/QQQ entry rules
- ✅ **BREADTH_DIVERGENCE signal** named; fires when IWM LOI > 0 AND SPY LOI < -20
- ✅ **HOWELL_PHASE_TRANSITION alert** in `pmcc_alerts.py` — fires on every phase change to Discord
- ✅ **TSLA Cyclical classification** — hard-blocked in Turbulence and Speculation phases
- ✅ **DB tables** `howell_phase_state` + `howell_phase_transitions` seeded and live

---

*Brief v1.1. Gate Zero is production. "What the Classifier Does NOT Solve" section remains valid — recommend re-reading with Howell phase context in mind.*
