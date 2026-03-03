# #mstr-cio Project Tracker
**Managed by:** Gavin (rizenshine5359) — Project Manager
**Updated:** 2026-03-03

---

## Project Status Summary

| Project | Name | Status | Owner |
|---|---|---|---|
| P1 | Allocation Bucket Framework (AB1/AB2/AB3/AB4) | ✅ v3.0 Complete | CIO |
| P2 | Bear Indicators | ⏸️ Deferred | Gavin |
| P4 | RORO / Howell Phase Engine | ✅ Complete | CIO |
| P5 | Daily Alerts & Automation | 🔴 Blocked — crontab | Greg |
| P6 | Multi-TF SRI / Concordance (LOI) | ✅ Complete | CIO |
| P7 | Framework Architecture | ✅ Complete — Approved | Gavin |
| P8 | Pine Scripts — Mirror Layer | ✅ Pivoted & Stable | Gavin |
| P9 | MSTR/IBIT Pair Trade | ⏸️ Deferred | Gavin |
| P10 | Trend Line Engine | ⏸️ Deferred | Greg + Gavin |
| P11 | STRC Spread Monitor | 🟡 Needs cron | Greg |
| P12 | Python Decision Engine | ✅ Phase 1+2 Complete | CIO |
| P13 | Trade Journal | 🟡 Schema defined — queued | CIO |
| P14 | Bearish Bias Indicator Suite | ⏸️ Deferred | Gavin |
| P-HOWELL | Howell Phase Engine | ✅ Complete — Live | CIO |
| P-CLASSIFIER | Stage 2 Continuation Classifier | ✅ v1.1 — Pending Gavin review | Gavin |
| P-GLI | GLI Engine (Layer 0) | ✅ Complete — Live | CIO |
| P-MSR | Market Structure Reports | ✅ Framework + Prototype complete | CIO |
| P-PPR | Personalized Portfolio Report | ✅ Workflow validated | CIO |
| P-MOCK | Weekly Generic Portfolio Brief | ✅ Live | CIO |
| P-TUTORIALS | Tutorial v2.2 + Layman's Guide | 🔵 Pending Gavin review | Gavin |
| P-UAA | Updated Alert Approach | 🟡 Scope TBD | Gavin |

---

## Active Projects

---

### P5: Daily Alerts & Engine Automation
**Status:** 🔴 Blocked — awaiting crontab install
**Lead:** CIO | **Approver:** Greg

The automation layer is built. All scripts exist and have been tested. Nothing fires automatically until the cron schedule is installed on the host.

| Milestone | Status |
|---|---|
| Morning Brief generator | ✅ Built |
| EOD Recap automation | ✅ Built |
| PMCC gate alerts (7 types) | ✅ Built |
| Howell phase transition alert | ✅ Built |
| Discord routing (alerts, Gavin, Gary channels) | ✅ Built |
| Stage 2 Classifier Gate Zero integration | ✅ Built |
| **Crontab install** | 🔴 Blocked — Greg must run install script |
| **DISCORD_WEBHOOK_GREG** | 🔴 Blocked — Greg must verify/recreate webhook |
| Greg channel automated output | ⬜ Pending webhook |

**Greg action required:**
```bash
sudo -u openclaw bash /home/openclaw/mstr-engine/scripts/install_crontab.sh
```
Then verify: `sudo -u openclaw crontab -l`

---

### P-HOWELL: Howell Phase Engine (Layer 0.5)
**Status:** ✅ Complete — Live
**Lead:** CIO | **Approver:** Gavin

Classifies the current macro cycle phase (Rebound / Calm / Speculation / Turbulence) using 8 sector ETFs. Phase determines Gate Zero eligibility for all AB3 entry decisions. Discord alert fires on every phase transition. Morning brief includes §4.5 Howell phase block.

**Current phase:** 🌧️ TURBULENCE (score T=+3, conf 12.5% — Turbulence/Speculation boundary)

| Milestone | Status | Commit |
|---|---|---|
| Sector ETFs added to CANONICAL_CSVS | ✅ | `2ebe963f` |
| HowellPhaseEngine + HowellPhaseState in sri_engine.py | ✅ | `df64b23c` |
| DB tables (howell_phase_state + howell_phase_transitions) | ✅ | `0febb3b1` |
| DB seeded with first live state | ✅ | — |
| Daily Discord embed — phase line in morning brief | ✅ | `4a83ba10` |
| Morning brief §4.5 (phase scores, sector table, AB guidance) | ✅ | `09f662f1` |
| HOWELL_PHASE_TRANSITION alert in pmcc_alerts.py | ✅ | `0febb3b1` |
| Gate Zero integrated into Stage 2 Classifier v1.1 | ✅ | `4ae16835` |
| Layer 0.5 section in Tutorial v2.2 | ✅ | `3bbb7e18` |
| Seasons analogy in Layman's Guide | ✅ | `d7e6cb2e` |

**Howell Asset Allocation Matrix:**

| Asset Class | Rebound | Calm | Speculation | Turbulence |
|---|---|---|---|---|
| Equities / Tech | 🟢 | 🟢 | 🟠 | 🔴 |
| Cyclicals | 🟢 | 🟢 | 🔴 | 🔴 |
| Commodities | 🔴 | 🟢 | 🟢 | 🔴 |
| Bond Duration | 🔴 | 🟠 | 🟠 | 🟢 |
| Defensives | 🔴 | 🟢 | 🟢 | 🟢 |

---

### P-CLASSIFIER: Stage 2 Continuation Classifier v1.1
**Status:** ✅ Research complete | 🔵 Pending Gavin review before live wiring
**Lead:** CIO | **Approver:** Gavin
**Brief:** `briefs/stage2-continuation-classifier-v1.md`

Distinguishes mid-bull corrections (buy the dip — Stage 2 Continuation) from genuine Stage 3/4 distribution tops. Uses CPS composite score (4 VLT/LT factors) plus Gate Zero (Howell phase + IWM breadth).

**Key finding:** When IWM is strong while SPY/QQQ corrects, continuation rate is only 10–13% — skip entirely. When IWM also shows headwind at the trough, continuation rises to 62.5% — valid entry zone.

| Milestone | Status | Commit |
|---|---|---|
| 221-episode dataset labeled | ✅ | — |
| CPS composite formula validated | ✅ | — |
| IWM breadth gate research (74 SPY/QQQ episodes) | ✅ | — |
| v1.1 brief with Gate Zero section | ✅ | `4ae16835` |
| Gavin review of "What It Doesn't Solve" section | 🔵 Pending | — |
| CPS wired into live AB3 entry triggers | ⬜ After Gavin approval | — |

---

### P-MSR: Market Structure Report Framework
**Status:** ✅ Framework v1.1 complete | Prototype (MSTR) built
**Lead:** CIO | **Approver:** Gavin
**Framework:** `briefs/stage-state-framework-v1.md`
**Reports:** `market-structure-reports/`

Standardized weekly report for every tracked asset. Declares Stage State (10-state taxonomy), Confirmation Ladder progress (Watch/Forming/Confirmed/Invalidated), LEAP Attractiveness Score (objective, 0–10), upstream macro context (GLI, RORO, Howell), and key transition triggers.

**The 10 Stage States:**
S1 (Accumulation) → S1→2 (Breakout Formation) → S2 (Markup) → S2C (Stage 2 Continuation) → S2→3 (Distribution Warning) → S3 (Distribution) → S3→4 (Markdown Initiation) → S4 (Markdown) → S4C (Stage 4 Continuation) → S4→1 (Bottom Formation)

**MSTR current state:** S4→1 Forming | Score: 6/10 | See latest MSR for full analysis.

| Milestone | Status |
|---|---|
| 10-state taxonomy defined | ✅ |
| Confirmation ladders (Watch/Forming/Confirmed/Invalidated) per key transition | ✅ |
| LEAP Attractiveness Score 0–10 with modifier set | ✅ |
| Risk/Reward modifier (mNAV, floor proximity, cycle asymmetry) | ✅ |
| Platform Value modifier spec (in PPR — see below) | ✅ |
| Anticipatory Tranche rules | ✅ |
| Portfolio implications table by stage | ✅ |
| MSTR prototype report | ✅ |
| Weekly automation (cron, all assets) | ⬜ Post crontab install |
| MR vs Momentum threshold differentiation (backtest) | ⬜ Queued |

---

### P-PPR: Personalized Portfolio Report
**Status:** ✅ Workflow validated by Gavin 2026-03-03
**Lead:** CIO | **Approver:** Gavin

Per-user report generated on-demand in each user's dedicated channel only. Translates the shared MSR into a personalized recommendation applying the user's income profile, LEAP coverage, Platform Value modifier, and personal deploy gate.

**Privacy: Non-negotiable.** PPR is never committed to GitHub, never shared cross-channel. Lives in Discord and the private database only.

| Milestone | Status |
|---|---|
| Platform Value modifier formula | ✅ |
| User profile schema (income target, gates, risk posture) | ✅ |
| PPR structure defined (7 sections) | ✅ |
| Gavin workflow validated (#mstr-gavin) | ✅ |
| Standardized code pipeline | ⬜ Queued |

**Default income profile:** Target 2%/month | Acceptable range 0–5% | High volatility tolerance | 10% hard cash floor always maintained | STRC counts as current income at 0.83%/month

---

### P-UAA: Updated Alert Approach
**Status:** 🟡 New project — scope TBD
**Lead:** Gavin (scope) → CIO (build)

Redesign the alert system to incorporate the new Stage State taxonomy. Current alerts cover PMCC gate changes and Howell phase transitions. The new framework requires a richer event vocabulary: confirmation ladder rung events (Watch/Forming/Confirmed/Invalidated), LEAP Attractiveness Score changes, anticipatory tranche triggers, PPR-relevant signals.

| Milestone | Status |
|---|---|
| Gavin defines alert event vocabulary and routing | 🔴 Pending Gavin |
| Design spec | ⬜ After scope definition |
| Build in pmcc_alerts.py | ⬜ After spec |

---

### P-TUTORIALS: Tutorial v2.2 + Layman's Guide Layer 0.5
**Status:** 🔵 Built — Pending Gavin review
**Lead:** CIO | **Approver:** Gavin

Full 4-layer architecture documentation for Greg (technical) and Gary (educational). Includes GLI Engine, Howell Phase "four seasons" analogy, and all signal layer updates.

| Document | Status |
|---|---|
| SRI-Engine-Tutorial-v2.md (v2.2) — technical | ✅ On GitHub (`3bbb7e18`) |
| SRI-Layman-Guide.md — Layer 0.5 section | ✅ On GitHub (`d7e6cb2e`) |
| Gavin review of both | 🔵 Pending |

---

### P-MOCK: Weekly Generic Portfolio Brief
**Status:** ✅ Live
**Lead:** CIO | Privacy rule: permanent

Generic $1M model portfolio brief published weekly to GitHub `mock-portfolios/` folder. Greg, Gavin, and Gary calibrate their personal portfolios privately against the model.

**Privacy rule (non-negotiable):** Only generic model content goes to GitHub. No personal account balances, position sizes, P&L, or identifying information — ever.

| Milestone | Status |
|---|---|
| mock-portfolios/ folder created | ✅ `570ab663` |
| First brief (2026-03-02) | ✅ `d9499da8` |
| Second brief due | ⬜ 2026-03-09 |

---

## Completed Projects

---

### P1: Allocation Bucket Framework — AB1/AB2/AB3/AB4
**Status:** ✅ v3.0 Complete
**Final architecture:**
- **AB3 (Core):** 2-year OTM LEAPs at deep LOI accumulation. Momentum threshold: LOI ≤ -45. MR threshold: LOI ≤ -40.
- **AB2 (Income Overlay):** PMCC — sell short calls (<90 DTE) against AB3 LEAPs. LOI gate controlled (NO_CALLS / OTM_INCOME / DELTA_MGMT).
- **AB1 (Tactical):** OTM LEAPs 60–120 DTE at CT1/CT2 pre-breakout signals. S1→2 Watch window.
- **AB4 (Cash Reserve):** STRC as default staging vehicle. Hard floor 10% true cash. Soft ceiling 25%. STRC yield (0.83%/month) is the universal hurdle rate.
- **Baseline allocation:** AB3=50% | AB1=25% | AB4=25% | AB2=income overlay only

---

### P4: RORO / Regime Engine (Layer 1)
**Status:** ✅ Complete — integrated into Python engine
- 5-phase capital rotation model built and backtested
- SRIBI breadth composite operational
- Howell phase engine (P-HOWELL) built on top of this work
- Regime Engine live in sri_engine.py

---

### P6: Multi-TF SRI / Concordance → LOI (Leap Opportunity Index)
**Status:** ✅ Complete
- LOI = composite oscillator: VLT SRIBI (40%) + VLT Acceleration (30%) + LT SRIBI (15%) + Concordance (15%)
- MR vs Momentum asset classification complete (BTC/MSTR/TSLA = Momentum; SPY/QQQ = MR; GLD = Trending)
- Phased trim schedule: 25% at LOI +20 / 50% at +40 / 75% at +60 / final on 20pt rollover
- AB3 Pine Script v5 confirmed by Gavin 2026-03-02

---

### P7: Framework Architecture
**Status:** ✅ Approved by Gavin 2026-03-05
**Final 4-layer architecture:**
```
Layer 0    — GLI Engine           (global liquidity — FRED proxy + GEGI)
Layer 0.5  — Howell Phase Engine  (macro cycle phase — Rebound/Calm/Speculation/Turbulence)
Layer 1    — Regime Engine        (asset-level regime — LOI gate states)
Layer 2    — Signal Engine        (LOI, CPS, VLT Recovery Clock, episode type)
Layer 3    — Allocation Engine    (AB1/AB2/AB3/AB4 capital deployment)
```
Gavin: *"Consider the architecture reviewed. The big missing piece has been filled (GLI/GEGI)."*

---

### P8: Pine Scripts — Mirror Layer
**Status:** ✅ Pivoted and stable
Pine scripts are visual coaching tools for Gavin only. All signal logic lives in Python. Pine scripts never diverge from engine state. AB3 Pine v5 confirmed accurate 2026-03-02.

---

### P-GLI: GLI Engine (Layer 0)
**Status:** ✅ Complete — Live
- FRED-based 6-component global liquidity proxy
- GEGI (ratio) computed alongside Z-score
- Z-score applied as ~20% probability modifier on all stage calls
- GLI Full = $189.2T (record level; rate-of-change peaked Q3 2025)
- Current Z-score: negative (contraction)
- Commit: `47c9e02c`

---

### P12: Python Decision Engine
**Status:** ✅ Phase 1 + Phase 2 Complete
- **Phase 1:** Full 4-layer engine. CSV ingest, SRIBI parser, Regime Engine, AB1/AB2/AB3 state machines, Allocation Engine, GLI Engine, Howell Phase Engine. All running end-to-end.
- **Phase 2:** Web dashboard (`generate_dashboard.py`). Self-contained HTML, all 4 layers visualized.
- 16 canonical CSVs: 8 trading assets (MSTR, IBIT, SPY, QQQ, GLD, IWM, TSLA, PURR) + 8 regime inputs (BTC, MSTR/IBIT ratio, Stablecoin Dom, STRC, TLT, DXY, HYG, VIX)
- Phase 3 (cron automation): pending Greg crontab install

---

## Deferred Projects

| Project | Objective | Trigger to Reactivate | Owner |
|---|---|---|---|
| **P2 — Bear Indicators** | Short-side signal generation for bear market opportunities | Gavin decides | Gavin |
| **P9 — MSTR/IBIT Pair Trade** | Systematic pair trading on relative SRI divergence | Gavin decides | Gavin |
| **P10 — Trend Line Engine** | CIO reads trend lines as linear equations on date/price coordinates | Greg + Gavin align on format spec | Greg + Gavin |
| **P14 — Bearish Bias Indicator Suite** | Symmetric bearish framework (DOI) with same rigor as SRI | Gavin decides | Gavin |
| **PURR Asset** | Full trading signals when bar count is sufficient | Auto-activates at 500+ bars | CIO (auto) |
| **Howell T1/T2/T3 Wave Mapping** | Map Howell capital flow wave structure onto IWM breadth findings | Gavin commits Howell Asset Alloc images to GitHub briefs/ | Gavin |

---

## Post-Launch Build Queue

| # | Project | Objective | Priority | Blocker |
|---|---|---|---|---|
| 1 | VLT Recovery Clock Alert | Alert when VLT crosses zero post-trough — the AB3 scaling gate | 🔴 HIGH | Crontab (Greg) |
| 2 | Episode-Type Classifier | Real-time Transient/Structural/Extended label + CPS in daily scan | 🔴 HIGH | Crontab (Greg) |
| 3 | CPS in Morning Brief | Early warning when any asset within 10 pts of threshold | 🔴 HIGH | #2 first |
| 4 | MSR Weekly Automation | Auto-generate MSRs every Monday AM for all assets | 🔴 HIGH | Crontab (Greg) |
| 5 | PPR Code Pipeline | Standardize intake + generation per user profile | 🔴 HIGH | None |
| 6 | Updated Alert Approach | Redesign alerts around Stage State events + ladder rung changes | 🔴 HIGH | **Gavin defines scope** |
| 7 | Trade Recommendation Engine | Structured executable trade recs with ORATS PoP, Greeks, hypothesis blocks, trade_log writes | 🟡 MED | PPR pipeline |
| 8 | Signal Accuracy Tracking | Measure signal prediction accuracy; weight by track record | 🟡 MED | None |
| 9 | Post-Mortem Process | Score closed trade hypotheses; extract structured lessons | 🟡 MED | #7 first |
| 10 | MR vs Momentum Threshold Differentiation | Backtest confirmation ladder thresholds by asset class | 🟡 MED | None |
| 11 | Classifier Dataset Re-labeling | Fix false negatives using "new high within 120 bars" metric | 🔵 LOW | None |
| 12 | Regime-Conditioned Classifier | Separate CPS models for GLI Z>0 vs Z<0 | 🔵 LOW | #11 first |
| 13 | Intraday Alert Frequency | Tune alert cadence for live trading hours | 🔵 LOW | Greg/Gavin requirements |
| 14 | Multi-Agent Sub-Analyst System | Activate mstr-macro/technical/options/sri as independent domain specialists | 🔵 LOW | None |

---

## Blocked Items

| Item | Needed | Owner |
|---|---|---|
| **Crontab install** | `sudo -u openclaw bash /home/openclaw/mstr-engine/scripts/install_crontab.sh` | **Greg** |
| **DISCORD_WEBHOOK_GREG** | Verify/recreate webhook in #mstr-greg; update config .env on host | **Greg** |
| **Tutorial v2.2 review** | Review both documents on GitHub | **Gavin** |
| **Stage 2 Classifier "What It Doesn't Solve"** | Sign-off before CPS wired into live entries | **Gavin** |
| **P-UAA scope definition** | Define alert event vocabulary before build begins | **Gavin** |
| **Howell images** | Commit Howell Asset Alloc.png + Howell Asset Alloc2.png to GitHub briefs/ | **Gavin** |

---

## Project Dependencies

```
P-GLI (Layer 0)
    └──→ P-HOWELL (Layer 0.5)
              └──→ P-CLASSIFIER (Gate Zero)
                        └──→ P-MSR (stage declarations)
                                  └──→ P-PPR (personalized layer)
                                  └──→ P-UAA (alert redesign)

P12 (Python Engine)
    └──→ P5 (Alerts — needs crontab)
    └──→ P-HOWELL (runs inside engine)
    └──→ VLT Recovery Clock (post-launch #1)
    └──→ Episode Classifier (post-launch #2)
    └──→ Trade Rec Engine (post-launch #7)

P6 (LOI) ──→ P1 (AB framework) ──→ P-MSR (score inputs)
```

**Critical path to full live operation:** Greg installs crontab → all automation starts → post-launch build queue opens

---

*Last updated: 2026-03-03 by CIO. Gavin manages priorities and sequencing.*
*Privacy rule: This tracker contains no personal portfolio data. Personal trade history, P&L, and positions live exclusively in the private database.*
