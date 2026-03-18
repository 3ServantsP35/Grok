# #mstr-cio Project Tracker
**Managed by:** Gavin (rizenshine5359) — Project Manager
**Updated:** 2026-03-18

---

## Project Status Summary

| Project | Name | Status | Owner |
|---|---|---|---|
| P1 | Allocation Bucket Framework (AB1/AB2/AB3/AB4) | ✅ v3.0 Complete | CIO |
| P2 | Bear Indicators | ✅ Closed — delivered by P-BEAR | CIO |
| P4 | RORO / Howell Phase Engine | ✅ Complete | CIO |
| P5 | Alerts & Automation (incl. UAA) | 🔴 Blocked — crontab + scope | Greg/Gavin |
| P6 | Multi-TF SRI / Concordance (LOI) | ✅ Complete | CIO |
| P7 | Framework Architecture | ✅ Complete — Approved | Gavin |
| P8 | Pine Scripts — Mirror Layer | ✅ Pivoted & Stable | Gavin |
| P9 | MSTR/IBIT Pair Trade | ⏸️ Deferred | Gavin |
| P10 | Trend Line Engine | 🟡 Live prototype tested; resistance-line analysis now in active use | CIO |
| P11 | STRC Spread Monitor | 🟡 Needs cron | Greg |
| P12 | Python Decision Engine | ✅ Phase 1+2 Complete | CIO |
| P13 | Trade Journal | 🟡 Schema defined — queued | CIO |
| P14 | Bearish Bias Indicator Suite | ✅ Retired — scope superseded by P-DOI | Gavin |
| P-BEAR | Bearish Signal & Adjustment Architecture | ✅ All phases complete | CIO |
| P-HOWELL | Howell Phase Engine | ✅ Complete — Live | CIO |
| P-CLASSIFIER | Stage 2 Continuation Classifier | ✅ v1.1 — Pending Gavin review | Gavin |
| P-GLI | GLI Engine (Layer 0) | ✅ Complete — Live | CIO |
| P-MSR | Market Structure Reports | ✅ All 7 assets updated 2026-03-04 | CIO |
| P-PPR | Personalized Portfolio Report | ✅ Workflow validated | CIO |
| P-MOCK | Weekly Generic Portfolio Brief | ✅ Live | CIO |
| P-TUTORIALS | Tutorial v2.5 + Layman's Guide | 🔵 Pending Gavin review | Gavin |
| P-CRS | AB2 Call Ripeness Score v2 | ✅ Complete — Pine v6 | CIO |
| P-PINE-GUIDE | Pine Indicator Tutorial Guide | ✅ Complete | CIO |
| P-BACKTEST | Stage Designation + Vol-Adaptive Research | ✅ Complete — R1/R2/R3 implemented | CIO |
| P-PINE-V6 | Pine v6 Migration | ✅ All 12 scripts on v6 | CIO |
| P-DOI | Distribution Signal Layer (Momentum assets) | 🔴 HIGH — Pine v1 live; CRS integration queued | CIO |
| P-MR-ENTRY | Cross-Asset LEAP Opportunity Framework (all in-scope assets) | 🟡 MED — Phase 1 research complete; calibrations live | CIO |
| P-MSTR-SUITE | MSTR Chart Suite — 5-chart weekly confirmation ladder | 🔴 HIGH — Active build + live discretionary use | Gavin/CIO |
| P-FF | Force Field / Force Field ROC | 🟡 FF live; FF ROC live; docs + CSV exports updated | CIO |

---

## Active Projects

---

### P5: Alerts & Automation *(merged with P-UAA)*
**Status:** 🔴 Blocked — crontab (Greg) + alert event vocabulary (Gavin)
**Lead:** CIO | **Approver:** Greg + Gavin

Two distinct blockers. The automation plumbing is fully built and tested. Nothing fires until Greg installs crontab. In parallel, the alert event vocabulary must be redesigned around the Stage State taxonomy — that design work (owned by Gavin) can proceed independently of the cron install.

**P-UAA merger rationale:** P5 (plumbing) and P-UAA (vocabulary redesign) are the same system. Maintaining them separately created false separation. Combined scope: build the right alerts *and* make them run automatically.

**Phase 1 — Plumbing (built, blocked on crontab):**

| Milestone | Status |
|---|---|
| Morning Brief generator | ✅ Built |
| EOD Recap automation | ✅ Built |
| PMCC gate alerts (7 types) | ✅ Built |
| Howell phase transition alert | ✅ Built |
| Discord routing (alerts, Gavin, Gary channels) | ✅ Built |
| Stage 2 Classifier Gate Zero integration | ✅ Built |
| Section 4.6 Liquidity Regime × TF Weighting in morning brief | ✅ Built (`9d3de58e`) |
| Section 8.5 P-BEAR bearish trade block in morning brief | ✅ Built (`57ed37fe`) |
| **Crontab install** | 🔴 Blocked — Greg must run install script |
| **DISCORD_WEBHOOK_GREG** | 🔴 Blocked — Greg must verify/recreate webhook |
| Greg channel automated output | ⬜ Pending webhook |

**Phase 2 — Alert Vocabulary Redesign (P-UAA scope, pending Gavin):**

Current alerts cover PMCC gate changes and Howell phase transitions. The Stage State taxonomy introduced a richer event vocabulary that the alert system doesn't yet surface. Gavin must define the event list before build begins.

| Milestone | Status |
|---|---|
| Gavin defines alert event vocabulary | 🔴 Pending Gavin |
| Confirmation ladder rung events (Watch/Forming/Confirmed/Invalidated) | ⬜ After vocab defined |
| LEAP Attractiveness Score change alerts | ⬜ After vocab defined |
| Anticipatory tranche trigger alerts | ⬜ After vocab defined |
| PPR-relevant signal routing | ⬜ After vocab defined |
| Integrate Stage State events into `pmcc_alerts.py` | ⬜ After vocab defined |

**Greg action required (Phase 1):**
```bash
sudo -u openclaw bash /home/openclaw/mstr-engine/scripts/install_crontab.sh
```
Then verify: `sudo -u openclaw crontab -l`

---

### P10: Trend Line Engine
**Status:** 🟡 Live prototype tested — now actively used in discretionary MSTR resistance/support analysis; not yet wired into pipeline
**Lead:** CIO | **Approver:** Greg + Gavin

Objective: CIO reads key trend lines as linear equations on date/price coordinates — visible in analysis without requiring TradingView.

**2026-03-04 live test:** Ran successfully against MSTR and BTC 4H CSV data. Swing high detection, two-point and multi-point linear regression, and forward projection all working. Key outputs demonstrated:
- MSTR post-ATH descending resistance TL (R²=0.968): anchored Jul-16/Aug-11/Oct-6 highs; current projection $203, slope -$4.70/day
- BTC Jan–Feb descending resistance TL: confirmed breakout today ($5,820 above projected level)
- Near-term resistance TL anchored on January swing highs

**Next step:** Formalize as a reusable function in `sri_engine.py`; integrate into morning brief and MSR generation.

| Milestone | Status |
|---|---|
| Swing high/low detection algorithm | ✅ Tested live |
| Two-point and multi-point linear regression | ✅ Tested live |
| Forward projection (N-day) | ✅ Tested live |
| R² confidence scoring | ✅ Tested live |
| TrendLine class in sri_engine.py | ⬜ Queued |
| Integration into morning brief | ⬜ After class build |
| Integration into MSR generation | ⬜ After class build |

---

### P-TUTORIALS: Tutorial v2.5 + Layman's Guide
**Status:** 🔵 Built — Pending Gavin review
**Lead:** CIO | **Approver:** Gavin

Full 4-layer architecture documentation for Greg (technical) and Gary (educational). Current version: v2.5.

| Document | Version | Status | Commit |
|---|---|---|---|
| SRI-Engine-Tutorial-v2.md | v2.5 | ✅ On GitHub | `cd2efd94` |
| SRI-Layman-Guide.md | Current | ✅ On GitHub | `d2b4b758` |
| Gavin review of both | — | 🔵 Pending | — |

**v2.5 additions over v2.2 (last reviewed):**
- §19: P-BEAR Signal Layer (7-state machine, per-asset ladders, AB2 fast-gate)
- §20: Portfolio Defensive Posture (4 levels, Expression 3 trigger spec)
- §21: Liquidity Regime × TF Weighting (Pearson r evidence, vol-adaptive formula, CONTRACTING/EXPANDING rules)
- Layman's Guide: "Weather Warnings" P-BEAR barometer analogy

---

### P-MSR: Market Structure Reports
**Status:** ✅ Framework v1.1 complete | Actively used for GLD/GLDM proxy work and ongoing MSTR structure reviews
**Lead:** CIO | **Approver:** Gavin
**Framework:** `briefs/stage-state-framework-v1.md`
**Reports:** `market-structure-reports/`

Standardized weekly report for every tracked asset. Declares Stage State (10-state taxonomy), Confirmation Ladder progress (Watch/Forming/Confirmed/Invalidated), LEAP Attractiveness Score (objective, 0–10), upstream macro context (GLI, RORO, Howell), and key transition triggers.

**Current MSR scores (2026-03-04):**

| Asset | Score | Stage | Key Note |
|---|---|---|---|
| MSTR | 6.5/10 | S2_early → S2 CONFIRMED | VLT turned positive 2026-03-04; all TFs now positive |
| IBIT | 4.0/10 | S4→1 | LOI surging +13.8/5bars; MIXED_BULLISH pattern |
| GLD | 2.0/10 | S2 w/ P-BEAR watch | 5/6 P-BEAR signals active; Supertrend watch $469.69 |
| SPY | 1.0/10 | MIXED_BEARISH | 6/7 P-BEAR signals; LOI collapsing -15/5bars |
| QQQ | 1.0/10 | S4 | 5/7 P-BEAR signals |
| IWM | 1.0/10 | S4 | 4/7 P-BEAR signals |
| TSLA | 1.0/10 | S4 | All TFs deeply negative |
| PURR | Stub | <500 bars | Observation mode — not yet created |

**Note on MSTR re: 2026-03-04 session:** VLT SRI Bias flipped to +20 on today's close. This upgrades MSTR from S2_early to S2 CONFIRMED (all four timeframes now positive). MSR score likely moves to 7.5–8.0 when re-run with current data. LOI at -14.2, projected to cross zero within 1 trading day.

| Milestone | Status |
|---|---|
| 10-state taxonomy defined | ✅ |
| Confirmation ladders per key transition | ✅ |
| LEAP Attractiveness Score 0–10 | ✅ |
| Risk/Reward modifier | ✅ |
| Platform Value modifier spec (in PPR) | ✅ |
| Anticipatory Tranche rules | ✅ |
| All 7 asset MSRs updated 2026-03-04 | ✅ |
| Push MSRs to GitHub | 🔵 Pending Gavin clearance |
| Weekly automation (cron, all assets) | ⬜ Post crontab install |
| PURR MSR stub | ⬜ Queued |

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

---

### P-DOI: Distribution Signal Layer *(Momentum assets only)*
**Status:** 🔴 HIGH — Pine v1 built; CRS integration queued
**Lead:** CIO | **Approver:** Gavin

**Origin:** P14 (Bearish Bias Indicator Suite) retired. The original "symmetric DOI with same rigor as SRI across all assets" scope was invalidated by the SPY/QQQ AB1 signal research, which found `loi_rollover` reaches only 54.8% win rate on MR assets — below the 60% threshold. P2 (Bear Indicators) was fully delivered by P-BEAR. P-DOI is the remaining gap: **a purpose-built Pine distribution indicator for Momentum assets**, where the signals are empirically validated.

**Research finding that scopes this project:**
- MSTR `loi_rollover`: **89% win rate** at 3% drawdown / 60 bars ✅
- MSTR `vlt_above_20`: **100%** ✅
- QQQ/SPY `loi_rollover`: **54.8%** ❌ — excluded from scope
- MR assets: distribution signals do not clear threshold — explicitly out of scope

**In scope (Momentum: MSTR, IBIT, TSLA):**

| Milestone | Status |
|---|---|
| Formalize `loi_rollover` as validated distribution marker (MSTR/IBIT/TSLA) | ✅ Implemented in DOI v1 |
| Formalize `vlt_above_20` as trim/exit signal | ✅ Implemented in DOI v1 |
| STRF/LQD topping divergence as credit-side distribution confirmation | ✅ Engine block 6b live |
| Build Pine distribution indicator (DOI oscillator — Momentum assets only) | ✅ `pine/SRI_Forecast_DOI.pine` (`411044f7`) |
| Wire into CRS and AB2 trim-zone precision | ⬜ Next step |

**Explicitly excluded:** SPY, QQQ, IWM, GLD — distribution signals unreliable on MR assets; CRS handles trim-zone guidance adequately for those.

---

### P-MR-ENTRY: Cross-Asset LEAP Opportunity Framework
**Status:** 🟡 MED — Research in progress (`cross-asset-leap-research-v1.md` running)
**Lead:** CIO | **Approver:** Gavin

**Strategic problem:**
The portfolio is over-indexed on MSTR being right. MSTR signal quality is ~92% (mixed_context win rate); all other in-scope assets are 38-55%. That gap means income generation is MSTR-dependent. The framework needs validated, high-confidence entry signals across the full asset universe so income can be generated from other assets when MSTR is range-bound, unfavorable for new entry, or simply needs to be left alone.

**Scope (expanded from original P-MR-ENTRY):**
All in-scope assets — MSTR, IBIT, SPY, QQQ, GLD, IWM, TSLA. For each asset: find the specific conditions that produce **≥70% win rate at 180-day horizon with N ≥ 10** (the "very high confidence" threshold for LEAP call entry). Each asset class requires a different signal stack:

| Asset | Class | Primary Entry Hypothesis | Current Signal Quality |
|---|---|---|---|
| MSTR | Momentum | LOI depth + stage transition | ✅ 92% (mixed_context) |
| IBIT | BTC-Proxy | Similar to MSTR, less volatile | 🟡 Untested — expect similar |
| TSLA | Business Momentum | Howell Speculation entry | 🟡 Untested |
| GLD | Trending | Dollar cycle + GLI + structural trend | 🟡 Untested |
| SPY | MR-Large | Episode Type × macro dislocation | ❌ 38-55% on current signals |
| QQQ | MR-Large | Same as SPY, slightly higher beta | ❌ 38-55% on current signals |
| IWM | MR-Small | GLI expansion + small-cap breadth cycle | 🟡 Untested |

**Core research hypothesis:**
Each asset class has a *different* high-confidence entry signal. The mistake was applying MSTR's LOI-depth framework universally. The research goal is to find each asset's native "very high confidence window" — not force a single framework onto all assets.

SPY/QQQ archetype: April/May 2025 tariff dislocation = transient macro shock on constructive regime → LEAP entries highly profitable. This is one instance of the broader pattern: **exogenous shock, regime intact, VIX elevated, LOI turning from trough**. Must generalize beyond any single event type.

**Research milestones:**

| Milestone | Status |
|---|---|
| Cross-asset backtest: win rates by condition for all 7 assets | ✅ `briefs/cross-asset-leap-research-v1.md` (`a1ad4139`) |
| Identify best condition combination per asset (≥70% / N≥10) | ✅ See signal stack table in brief |
| Cross-asset opportunity windows (when do multiple assets align?) | ✅ 3+ assets LOI<-20 = max deploy (~8% of days) |
| VIX proxy for Howell Phase in backtest | ✅ Complete (period-biased — extend VIX history) |
| Indicator calibration from findings | ✅ AB3 Pine + morning brief updated (`c3fa2585`, `c0698ceb`) |
| system-learnings.md — 4 cross-agent insights | ✅ Complete (docs sub-agent) |
| INDICATOR-GUIDE per-asset calibration warnings | ✅ Complete (docs sub-agent) |
| Episode taxonomy formalization (Transient / Structural / Extended) | ⬜ After Episode Classifier |
| Asset-specific signal specs (one per asset, validated) | ⬜ After Stage 4→1 rerun at 4H |
| Stage 4→1 rerun at 4H resolution (methodology gap fix) | ⬜ Priority research |
| Extend VIX history to 2019 (de-bias VIX-crossed signals) | ⬜ Data acquisition |
| Episode Type Classifier build | ⬜ Post-launch #3 |
| Wire into morning brief: multi-asset high-confidence window alerts | ✅ Cross-asset accumulation count live |
| Pine indicator: asset-specific entry signals | ⬜ After Stage 4→1 research |

**Dependencies:**

| Dependency | Project | Status |
|---|---|---|
| Cross-asset backtest brief | This project | 🔄 Running |
| Episode Type Classifier | Post-launch build #3 | ⬜ Not yet built |
| Trend Line Engine (price anchors) | P10 | 🟡 Prototype tested |
| GLI + Howell | P-GLI, P-HOWELL | ✅ Live |

---

## Recently Completed Projects

---

### P-BEAR: Bearish Signal & Adjustment Architecture
**Status:** ✅ All phases complete
**Lead:** CIO | **Approver:** Gavin

Full bearish signal framework layered on top of the existing SRI engine. Covers signal detection, portfolio posture escalation, and directional trade expression.

| Item | Description | Status | Commit |
|---|---|---|---|
| 1 | P-BEAR signal engine (7-state machine, per-asset ladders) | ✅ | `adecb607` |
| 2 | Directional bearish trade logic (`bearish_trade_spec()`) | ✅ | `57ed37fe` |
| 3 | WeeklyStochRSI → CONFIRMED_PLUS gate | ✅ | `adecb607` |
| 4 | Morning brief §8.5 bearish trade block | ✅ | `57ed37fe` |
| 5 | Tutorial v2.4 §19–20 + Layman's Guide "Weather Warnings" | ✅ | `caec2180` / `d2b4b758` |

**Portfolio Defensive Posture Matrix:**

| Level | Trigger | AB4 Floor | AB3 New | AB2 | Expr3 |
|---|---|---|---|---|---|
| 🟢 NORMAL | No signals | 10% | ✅ | Normal | — |
| 🟡 CAUTIOUS | 1 FORMING | 10% | ✅ | Paused on asset | — |
| 🟠 DEFENSIVE | 2 FORMING or 1 CONFIRMED | 15% | ❌ | Under review | — |
| 🔴 MAX DEFENSIVE | 2 CONFIRMED or CONF+ | 20% | ❌ | Close calls | Eligible |

**Per-asset bearish playbook:** SPY/QQQ/IWM = debit put spread 45–60 DTE; IBIT = long put LEAP 90–120 DTE; GLD = OTM puts 30–45 DTE (3% notional max); TSLA = put spread gated by Howell ≠ Turbulence; MSTR = Expression 3 routing only.

**Spec doc:** `briefs/p-bear-directional-trades-spec-v1.md`

---

### P-CRS: AB2 Call Ripeness Score v2
**Status:** ✅ Complete — Pine v6
**Lead:** CIO | **Approver:** Gavin
**File:** `pine/AB2_CRS.pine` | **Final commit:** `591cdc84`

Full rewrite of the AB2 call-selling indicator with corrected philosophy: Stage 1 chop is the **primary income window**, not a no-call zone. Three objective outputs — no portfolio-specific logic (STRC hurdle and contract sizing belong in PPR).

**Architecture:**
- **Income Score (0–10):** IV premium (0–4) + Stage alignment (0–4) + Chop confirmation (0–2) + modifiers (Howell phase, liquidity regime)
- **Strike Width (%):** Stage-adaptive baseline; VST momentum direction adjusts ±3–5%
- **Exercise Risk (LOW/MED/HIGH):** Based on VST SRI Bias Histogram slope

**Stage baselines:**

| LOI Zone | Stage | Strike Width |
|---|---|---|
| < −45 | DECLINE | NO CALLS |
| −45 to −20 | S1 CHOP ★ | +12% OTM |
| −20 to 0 | RECOVERY | +17% OTM |
| 0 to +20 | S2 STD | +10% OTM |
| +20 to +40 | TRIM APPROACH | +5% OTM |
| > +40 | DELTA_MGMT | +1% ATM/ITM |

**Backtest validation:** 80% call success at +10% OTM in S1 chop zone (LOI −45 to −20); 96% at +20% OTM. Prior hard gate at LOI < −20 was blocking calls exactly when they worked best — removed.

**Pine v6 fixes applied:** Multi-line expression collapse (2 instances); `request.security` tuple pattern; type annotation removal from destructuring; `lookahead` parameter removed (v6 default).

---

### P-PINE-GUIDE: Pine Indicator Tutorial Guide
**Status:** ✅ Complete — updated with Force Field vs Force Field ROC interpretation rule
**Lead:** CIO
**File:** [`pine/INDICATOR-GUIDE.md`](https://github.com/3ServantsP35/Grok/blob/main/pine/INDICATOR-GUIDE.md) | **Commit:** `044c4130`

Comprehensive tutorial for all 12 Pine Script indicators. Covers all four families: SRI Price Overlays (4), SRIBI Oscillators (4), SRI Forecast Strategy Monitors (3), and AB2 CRS (1). Each indicator includes: what it shows, inputs/settings table, how to use it, key signals, framework connection, common mistakes. Includes "Putting It All Together" section with 4-chart setup and decision hierarchy.

**Direct links by family:**

| Family | Scripts |
|---|---|
| SRI Price Overlays | SRI_VST, SRI_ST, SRI_LT, SRI_VLT |
| SRIBI Oscillators | SRIBI_VST, SRIBI_ST, SRIBI_LT, SRIBI_VLT |
| SRI Forecast | SRI_Forecast_AB1, SRI_Forecast_AB2, SRI_Forecast_AB3 |
| Income Tools | AB2_CRS v2 |

---

### P-PINE-V6: Pine v6 Migration
**Status:** ✅ Complete — all core scripts on Pine v6; recent Force Field / FF ROC parser fixes pushed live

---

### P-FF: Force Field / Force Field ROC
**Status:** 🟡 Active — both indicators live; FF ROC promoted to primary analytical read
**Lead:** CIO

**Current state:**
- Original Force Field remains the base regime/state indicator
- Force Field ROC is now the primary tactical / decision-support indicator
- FF ROC is live on GitHub and documented in `pine/INDICATOR-GUIDE.md`
- CSV export fields now include:
  - `F_net ROC 1`
  - `F_net ROC 3`
  - `F_net ROC 5`
  - `F_net Acceleration`
- Pine parser/formatting fixes were pushed directly to GitHub from the Mac mini runtime
- Legacy Force Field display/marker behavior is still usable, but marker rendering remains visually suboptimal when enabled

**Canonical interpretation rule:**
- Original FF answers: **what regime/state are we in?**
- FF ROC answers: **is that regime strengthening, weakening, accelerating, or exhausting?**
- Operational hierarchy: read original FF first for structural zone, then FF ROC for timing/quality of force

**Infrastructure note:**
- CIO/Cyler is now running natively on the **Mac mini**, not the stale VPS sandbox
- Direct local repo read/write plus GitHub commit/push capability has been restored and verified
- Indicator edits should now be made **repo-first** in GitHub-tracked files to avoid copy/paste drift

**Next step:**
- Validate FF ROC versus live MSTR continuation/rejection behavior over the next 2–4 weeks
- Decide later whether the legacy FF should remain fully parallel or be demoted to a background-only indicator

---

All Pine scripts in the repo are now on `@version=6`. CRS was the only script created under v5; migrated in the same session it was built.

**Pine v6 rules (permanent, all future scripts):**
1. `@version=6` header on all new scripts
2. Multi-line expressions must be inside `()` or collapsed to one line — no implicit continuation
3. `request.security()` tuple pattern: `[a, b] = request.security(sym, tf, [expr1, expr2])` — no type annotations in brackets
4. `lookahead` parameter omitted (v6 defaults to `barmerge.lookahead_off`)

---

### P-BACKTEST: Stage Designation + Vol-Adaptive LOI Research
**Status:** ✅ Complete — R1/R2/R3 implemented in `sri_engine.py`
**Lead:** CIO | **Approver:** Gavin
**Reports:** `briefs/stage-designation-backtest-v1.md` | `briefs/loi-vol-adaptation-research-v1.md`
**Engine commit:** `7ee6dafb`

**Key findings:**

**Stage Designation Backtest (`e6ce2e4f`):**
- LOI Trough = most accurate bullish signal (56.4% cross-asset avg)
- LOI threshold (−45) virtually never fires — miscalibrated; only 2 signals on MSTR in 15 months
- Stage 1 never fires — classification logic gap (S4→1 short-circuits S1 condition)
- MIXED bars = 35–46% of all bars — stage machine ambiguous half the time

**Vol-Adaptive LOI Research (`fbc03fff`):**
- H1: Direction inverted — HIGH vol → MORE negative LOI troughs (not less); LOW vol entries are the poison (−26.8% median vs HIGH vol +26.3%)
- H2: CONTRACTING regime → LT/VLT more reliable; EXPANDING → VST/ST elevated; ST is all-weather
- Adaptive formula validated: `threshold = base × (median_ATR_ratio / current_ATR_ratio)`

**R1/R2/R3 implemented (`7ee6dafb`):**

| Item | Change | Detail |
|---|---|---|
| R1 | `AdaptiveLOIEngine` | MOMENTUM/BTC_CORRELATED: adaptive (base −45); MR/TRENDING: flat −40; capped base×0.6/base×1.3 |
| R2 | `classify_mixed_context()` | MIXED_BULLISH / MIXED_BEARISH / MIXED_CONFUSED sub-classification |
| R3 | `classify_stage()` + `promote_stage1()` | S4→1 → S1 after VST positive ≥5 consecutive bars |

**Current adaptive thresholds:** MSTR=−43.6 | TSLA=−50.2 | IBIT=−41.5 | MR/TRENDING: −40 flat

**System learnings promoted:** `mstr-knowledge/system-learnings.md` (`35416f46`) — two ACTIVE entries (liquidity-TF weighting + vol-adaptive LOI)

---

## Completed Projects (Legacy)

---

### P1: Allocation Bucket Framework — AB1/AB2/AB3/AB4
**Status:** ✅ v3.0 Complete
- **AB3 (Core):** 2-year OTM LEAPs at deep LOI accumulation. Vol-adaptive threshold (MOMENTUM/BTC_CORRELATED base −45; MR/TRENDING −40).
- **AB2 (Income Overlay):** PMCC — sell short calls (<90 DTE) against AB3 LEAPs. Stage-adaptive CRS (S1 chop = primary income window).
- **AB1 (Tactical):** OTM LEAPs 60–120 DTE at CT1/CT2 pre-breakout signals. S1→2 Watch window.
- **AB4 (Cash Reserve):** STRC as default staging vehicle. Hard floor 10% true cash. Soft ceiling 25%. STRC yield (0.83%/month) is the universal hurdle rate.
- **Baseline allocation:** AB3=50% | AB1=25% | AB4=25% | AB2=income overlay only

---

### P4: RORO / Regime Engine (Layer 1)
**Status:** ✅ Complete — integrated into Python engine

---

### P6: Multi-TF SRI / Concordance → LOI
**Status:** ✅ Complete
- LOI = VLT SRIBI (40%) + VLT Acceleration (30%) + LT SRIBI (15%) + Concordance (15%)
- MR vs Momentum classification: BTC/MSTR/TSLA = Momentum; SPY/QQQ = MR; GLD = Trending
- Vol-adaptive thresholds integrated (R1)

---

### P7: Framework Architecture
**Status:** ✅ Approved by Gavin 2026-03-05
```
Layer 0    — GLI Engine           (global liquidity — FRED proxy + GEGI)
Layer 0.5  — Howell Phase Engine  (macro cycle phase)
Layer 1    — Regime Engine        (asset-level regime)
Layer 2    — Signal Engine        (LOI, CPS, VLT Recovery Clock)
Layer 3    — Allocation Engine    (AB1/AB2/AB3/AB4 capital deployment)
```

---

### P8: Pine Scripts — Mirror Layer
**Status:** ✅ Pivoted and stable. All 12 scripts on Pine v6.

---

### P-HOWELL: Howell Phase Engine (Layer 0.5)
**Status:** ✅ Complete — Live
**Current phase:** 🌧️ TURBULENCE

| Milestone | Status | Commit |
|---|---|---|
| HowellPhaseEngine + HowellPhaseState in sri_engine.py | ✅ | `df64b23c` |
| DB tables + seeded | ✅ | `0febb3b1` |
| Morning brief §4.5 | ✅ | `09f662f1` |
| HOWELL_PHASE_TRANSITION alert | ✅ | `0febb3b1` |
| Gate Zero in Stage 2 Classifier v1.1 | ✅ | `4ae16835` |

---

### P-CLASSIFIER: Stage 2 Continuation Classifier v1.1
**Status:** ✅ Research complete | 🔵 Pending Gavin review before live wiring
**Brief:** `briefs/stage2-continuation-classifier-v1.md`

IWM breadth gate key finding: IWM strong while SPY/QQQ corrects → continuation rate 10–13% (skip). IWM also showing headwind at trough → 62.5% continuation (valid entry zone).

---

### P-GLI: GLI Engine (Layer 0)
**Status:** ✅ Complete — Live. Current Z-score: negative (contraction).

---

### P12: Python Decision Engine
**Status:** ✅ Phase 1+2 Complete. Phase 3 (cron) pending Greg crontab install.

---

### P-MOCK: Weekly Generic Portfolio Brief
**Status:** ✅ Live
- First brief: 2026-03-02 | Next due: 2026-03-09 (Monday)
- **Privacy rule (non-negotiable):** Only generic model content goes to GitHub. No personal account balances, position sizes, P&L, or identifying information — ever.

---

## Deferred Projects

| Project | Objective | Trigger to Reactivate | Owner |
|---|---|---|---|
| **P9 — MSTR/IBIT Pair Trade** | Systematic pair trading on relative SRI divergence | Gavin decides | Gavin |
| **PURR Asset** | Full trading signals when bar count is sufficient | Auto-activates at 500+ bars | CIO (auto) |
| **Howell T1/T2/T3 Wave Mapping** | Map Howell capital flow wave structure onto IWM breadth findings | Gavin commits Howell Asset Alloc images to GitHub briefs/ | Gavin |

---

## Post-Launch Build Queue

| # | Project | Objective | Priority | Blocker |
|---|---|---|---|---|
| 1 | VLT Recovery Clock Alert | Alert when VLT crosses zero post-trough — the AB3 scaling gate | 🔴 HIGH | Crontab (Greg) |
| 2 | Trend Line Engine (P10) | Formalize TrendLine class in `sri_engine.py`; wire into morning brief + MSR | 🔴 HIGH | None — prototype proven |
| 3 | Episode-Type Classifier | Real-time Transient/Structural/Extended label + CPS in daily scan | 🔴 HIGH | Crontab (Greg) |
| 4 | CPS in Morning Brief | Early warning when any asset within 10 pts of threshold | 🔴 HIGH | #3 first |
| 5 | MSR Weekly Automation | Auto-generate MSRs every Monday AM for all assets | 🔴 HIGH | Crontab (Greg) |
| 6 | PPR Code Pipeline | Standardize intake + generation per user profile | 🔴 HIGH | None |
| 7 | P5 Phase 2 — Alert Vocabulary Redesign | Stage State events, ladder rung changes, LAS alerts, PPR routing (P-UAA merged into P5) | 🔴 HIGH | **Gavin defines vocab** |
| 8 | classify_stage() Bug Fix | Returns MIXED_CONFUSED for MSTR (should be S2_early/S2); fix condition sequencing | 🟡 MED | None |
| 9 | Trade Recommendation Engine | Structured executable trade recs with ORATS PoP, Greeks, hypothesis blocks, trade_log writes | 🟡 MED | PPR pipeline |
| 10 | Signal Accuracy Tracking | Measure signal prediction accuracy; weight by track record | 🟡 MED | None |
| 11 | Post-Mortem Process | Score closed trade hypotheses; extract structured lessons | 🟡 MED | #9 first |
| 12 | PURR MSR Stub | Create observation-mode stub MSR for PURR | 🟡 MED | None |
| 13 | MR vs Momentum Threshold Differentiation | Backtest confirmation ladder thresholds by asset class | 🟡 MED | None |
| 13b | P-DOI: Distribution Signal Layer | Pine DOI oscillator for MSTR/IBIT/TSLA; `loi_rollover` + `vlt_above_20` formalized; STRF/LQD divergence layer already live | 🔴 HIGH | None |
| 13c | P-MR-ENTRY: Cross-Asset LEAP Opportunity | Find ≥70% win-rate entry conditions for ALL in-scope assets; each asset gets its own validated signal; portfolio income not dependent on MSTR alone | 🟡 MED | Episode Type Classifier (#3), P10 |
| 14 | Re-run Vol-Adaptive + Stage Backtest | Increase confidence at 24+ months data | 🔵 LOW | Time |
| 15 | Classifier Dataset Re-labeling | Fix false negatives using "new high within 120 bars" metric | 🔵 LOW | None |
| 16 | Regime-Conditioned Classifier | Separate CPS models for GLI Z>0 vs Z<0 | 🔵 LOW | #15 first |
| 17 | Multi-Agent Sub-Analyst System | Activate mstr-macro/technical/options/sri as independent domain specialists | 🔵 LOW | None |

---

## Blocked Items

| Item | Needed | Owner |
|---|---|---|
| **Crontab install** | `sudo -u openclaw bash /home/openclaw/mstr-engine/scripts/install_crontab.sh` | **Greg** |
| **DISCORD_WEBHOOK_GREG** | Verify/recreate webhook in #mstr-greg; update config .env on host | **Greg** |
| **Tutorial v2.5 review** | Review SRI-Engine-Tutorial-v2.md (v2.5) and SRI-Layman-Guide.md on GitHub | **Gavin** |
| **Stage 2 Classifier "What It Doesn't Solve"** | Sign-off before CPS wired into live entries | **Gavin** |
| **MSR push to GitHub** | Open questions cleared before publishing MSRs | **Gavin** |
| **P5 Phase 2 — Alert vocabulary** | Define Stage State event vocabulary before redesign builds (P-UAA merged into P5) | **Gavin** |
| **Howell images** | Commit Howell Asset Alloc.png + Howell Asset Alloc2.png to GitHub briefs/ | **Gavin** |

---

## Project Dependencies

```
P-GLI (Layer 0)
    └──→ P-HOWELL (Layer 0.5)
              └──→ P-CLASSIFIER (Gate Zero)
                        └──→ P-MSR (stage declarations)
                                  └──→ P-PPR (personalized layer)
                                  └──→ P5 Phase 2 (alert redesign — P-UAA merged)

P12 (Python Engine)
    └──→ P5 (Alerts — needs crontab)
    └──→ P-HOWELL (runs inside engine)
    └──→ P-BACKTEST R1/R2/R3 (integrated)
    └──→ VLT Recovery Clock (post-launch #1)
    └──→ P10 Trend Line Engine (post-launch #2)
    └──→ Episode Classifier (post-launch #3)
    └──→ Trade Rec Engine (post-launch #9)

P6 (LOI) ──→ P1 (AB framework) ──→ P-MSR (score inputs)
P-CRS (AB2 CRS v2) ──→ P-PPR (strike width inputs)
P-BEAR (signal engine) ──→ P-DOI (Pine distribution layer — MSTR/IBIT/TSLA only)

Episode Classifier (post-launch #3)
    └──→ P-MR-ENTRY (primary gate for SPY/QQQ AB3 entries)
              └──→ P10 Trend Lines (price anchor layer for MR entries)
P-PINE-GUIDE ──→ Greg + Gary onboarding
```

**Critical path to full live operation:** Greg installs crontab → all automation starts → post-launch build queue opens

**Runtime / repo status (2026-03-18):** Native Mac mini runtime confirmed; local repo read/write and direct GitHub push capability restored.

---

## P-MSTR-SUITE — MSTR Chart Suite

**Owner:** Gavin (methodology), CIO (build)  
**Initiated:** 2026-03-05  
**Priority:** HIGH — Weekend advisory tool for Greg, Gavin, Gary

### Hypothesis
5 SRI charts (MSTR LT, STRC LT, Stablecoin Dom LT, STRF/LQD LT, MSTR/IBIT LT) form a confirmation ladder that can assess MSTR's 30–60 day directional outlook with high confidence when 4+ signals align.

### Deliverables
| Item | Status |
|------|--------|
| Phase 1: Hypothesis document | ✅ `briefs/mstr-chart-suite-hypothesis-v1.md` |
| Report script `mstr_suite_report.py` | 🔄 Building |
| Cron: Friday 3:30 PM ET reminder | ⬜ Pending crontab install |
| Cron: Friday 4:30 PM ET report | ⬜ Pending crontab install |
| Phase 2: Quantitative backtest | ⬜ After Phase 1 validated |
| Phase 3: Composite score validation | ⬜ After Phase 2 |
| Optional: Add BTC SRI LT as Chart 6 | ⬜ Proposed for Phase 2 |

### CSV Mapping (Friday push required)
| Chart | CSV Pattern |
|-------|------------|
| MSTR SRI LT | `BATS_MSTR, 240_*.csv` |
| STRC SRI LT | `BATS_STRC, 240_*.csv` |
| Stablecoin Dom SRI LT | `CRYPTOCAP_STABLE.C.D, 240_*.csv` |
| STRF/LQD SRI LT | `BATS_STRF_BATS_LQD, 240_*.csv` |
| MSTR/IBIT SRI LT | `BATS_MSTR_BATS_IBIT, 240_*.csv` |

### Cron Schedule (to be added to host crontab)
```cron
# MSTR Chart Suite — Friday CSV reminder (3:30 PM ET = 20:30 UTC)
30 20 * * 5 /usr/bin/python3 /mnt/mstr-scripts/mstr_suite_report.py reminder >> /mnt/mstr-logs/suite_report.log 2>&1

# MSTR Chart Suite — Friday weekly report (4:30 PM ET = 21:30 UTC)
30 21 * * 5 /usr/bin/python3 /mnt/mstr-scripts/mstr_suite_report.py report >> /mnt/mstr-logs/suite_report.log 2>&1
```

---

*Last updated: 2026-03-18 by CIO. Gavin manages priorities and sequencing.*
*Privacy rule: This tracker contains no personal portfolio data. Personal trade history, P&L, and positions live exclusively in the private database.*
