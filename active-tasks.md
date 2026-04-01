# Active Tasks
**Last Updated:** 2026-03-15 00:30 UTC

---

## Sprint Complete ✅

All 13 architecture optimization tasks done. See memory/2026-03-07.md.

---

## Infrastructure — ✅ CONFIRMED OPERATIONAL (2026-03-15)

Verified by system admin. All prior "Greg Actions Required" items were already resolved.

- [x] **Crontab** — 52 active entries confirmed installed ✅
- [x] **Discord webhooks** — GREG (Spidey Bot), GAVIN (Gav MSTR bot), GARY (Captain Hook), ALERTS, ALL_ALERTS — all returning 200 ✅
- [x] **Channel bindings** — #mstr-cio, #mstr-greg, #mstr-gavin, #mstr-gary all bound ✅
- [x] **Bind mounts** — /Users/vera/mstr-engine/data, /Users/vera/mstr-engine/scripts, /Users/vera/mstr-engine/config, /Users/vera/mstr-engine/logs live ✅
- [x] **PBearEngine** — class in sri_engine.py line 3635; pbear_state_log 21 records through 2026-03-13 ✅
- [x] **engine_config** — suite_bull_graduated (false) + suite_last_upload_ts seeded ✅
- [x] **Gateway** — running via systemd openclaw-mstr.service, port 18789, Discord connected ✅

---

## Phase: P-MSTR-SUITE — Magnetic Force Engine

### Status: Engine built, integrated, verification/monitoring closeout

**Engine:** /Users/vera/mstr-engine/scripts/mstr_suite_engine.py (written 2026-03-08)

**What's done:**
- [x] Pass 1 backtesting — lead/lag analysis, 12 input/TF combinations
- [x] Pass 2 backtesting — F_net composite model, zone WR validation
- [x] Force model architecture confirmed (physics-based, not scoring)
- [x] mstr_suite_engine.py built — full force computation, zone classification, confidence tiers, DB storage, brief formatter, calibrate() method
- [x] Bearish signal side validated: MOD/STRONG BEAR → 75-91% WR at +10-30d (N=29-36)
- [x] Bullish signal side: PROVISIONAL pending 6-month live calibration
- [x] engine_config table seeded: suite_bull_graduated=false, suite_last_upload_ts ✅

**Closeout completed:**
- [x] Engine built and committed in GitHub-tracked files
- [x] Wired into `morning_brief.py` via `engine.format_brief_block(signal)` section insertion
- [x] Wired into `daily_analysis_cycle.py` via `engine.store_signal(signal)` after CIO synthesis
- [x] Fixed integration method mismatch (`compute_signal()` → `compute_current_signal()`) in commit `5898a4f`
- [x] Optional scenario/fib/deeper-reset context already incorporated in `mstr_suite_report.py`

**Remaining posture:**
- [ ] Next live/runtime pass should confirm brief rendering and signal storage in the production path
- [ ] Continue normal validation/monitoring against realized path; no major build work remains

**6-Month Calibration Checkpoint — Gavin action:**
- Date: 2026-09-08 (6 months from engine deployment)
- Action: Run python3 /Users/vera/mstr-engine/scripts/mstr_suite_engine.py --calibrate 10 --zone STRONG_BULL
- Decision rule: If WR >= 70% on STRONG_BULL, upgrade to HIGH confidence and enable full sizing.
- Owner: Gavin (rizenshine5359)

---

## Pending — CIO Work Items

- [ ] Observe/confirm next live production run for suite brief rendering + DB storage
- [ ] Gavin: review Tutorial v2.5 and SRI-Layman-Guide.md

---

## Recent Project Updates (2026-03-29 to 2026-03-30)

### P-MSTR Theta / Delta Split — ✅ Architecture decided
- [x] Concluded that **MSTR** should be treated primarily as the **theta / PMCC / premium-harvest vehicle**
- [x] Concluded that **BTC / IBIT** should be treated as the cleaner **directional delta-expression layer**
- [x] Updated tracked specs/docs to reflect this split
- [x] Updated AB1 / AB2 Pine messaging to match the new architecture
- [ ] Future follow-through: directional AB2 signal development should migrate toward BTC / IBIT research instead of forcing MSTR to carry that role

### P-AB1-2 MSTR Topping Work — ✅ Branch closed, lessons extracted
- [x] Completed multiple calibration passes on Green / Yellow / Red / B logic
- [x] Established that **Green** is the only stable MSTR signal from that branch
- [x] Established that Yellow/B logic did **not** validate for their intended MSTR roles
- [x] Created standalone `MSTR_Yellow_Prototype.pine` and `MSTR_B_Prototype.pine`
- [x] Confirmed B prototype behaved more promisingly on BTC than on MSTR, reinforcing the new architecture
- [ ] Do not continue tuning the retired MSTR Yellow/B branch unless a new feature-family design is explicitly approved

### P-CSV Hygiene / TradingView Ops — ✅ improved
- [x] Reduced TradingView indicator load by clarifying keep/drop priorities
- [x] Agreed one universal download view is workable after indicator reduction
- [x] Cleaned stale CSV uploads from GitHub root and local workspace
- [ ] Optional later cleanup: rename ambiguous custom/prototype export titles if CSV interpretation becomes a bottleneck again

---

## High-Priority Next Steps

### 1. P-MSTR-SUITE — Production closeout / operationalization ✅ NEAR-CLOSED
- [x] Repair integration method mismatch and push fix
- [x] Suite output wired into `morning_brief.py`
- [x] Suite output persistence wired into `daily_analysis_cycle.py`
- [x] Final generic engine artifacts committed/pushed
- [ ] Confirm next live production pass, then treat project as fully closed

### 2. P-TRADINGVIEW-INTEGRATION 🔴 HIGH
- [x] Define a dedicated TradingView integration project inspired by the referenced x.com workflow
- [x] Determine desired scope: indicator orchestration, export/download workflow, alert routing, signal packaging, and chart automation requirements
- [x] Map which parts should live in Pine, which in Python, and which in the Discord/reporting layer
- [x] Produce a concrete implementation brief and prioritized build plan
- [x] Execute Phase A discovery/current-state audit (`briefs/p-tradingview-integration-discovery-v1.md`)
- [x] Formalize Pine/script tiering and chart-view standards (`briefs/p-tradingview-integration-standards-v1.md`)
- [ ] Decide canonical ingestion architecture (GitHub vs direct vs hybrid)
- [ ] Build shared CSV validation + freshness pipeline
- [ ] Build direct chart-access proof of concept
- [ ] Define Pine deployment/update + low-touch testing workflow

### 3. BTC / IBIT AB2 Directional Research Track 🔴 HIGH
- [ ] Formalize a BTC / IBIT-specific AB2 research brief/spec
- [ ] Decide preferred directional structures for IBIT (long calls vs call debit spreads vs other delta-heavy structures)
- [ ] Build/test first BTC / IBIT directional signal prototype with the new architecture in mind
- [ ] Keep this work separate from MSTR theta-management logic

### 4. MSTR Theta / PMCC Management Refinement 🔴 HIGH
- [ ] Freeze Green conceptually as the maintain/farm signal
- [ ] Decide whether any further MSTR indicator work is needed purely for theta-management wording or posture guidance
- [ ] Avoid re-opening the failed Yellow/B directional-timing branch unless a new hypothesis is defined first

### 4. P-DOI / Existing Production Integrations 🟡 MEDIUM
- [ ] Confirm DOI/morning brief/alerts are fully live and documented in current workflow

### 5. QQQ / Cross-Asset Pine Cleanup 🟡 MEDIUM
- [ ] Revisit the deferred SRI AB1 Pine rebuild for QQQ only after the higher-priority suite and BTC/IBIT directional work is underway

---

## Standing Rules
- sri_engine.py frozen — new engines in separate files
- All Claude calls via api_utils.call_claude()
- Opus only in daily_analysis_cycle.py Python calls
- PPR generator: zero API calls
- GitHub: no personal data, P&L, or position sizes ever
