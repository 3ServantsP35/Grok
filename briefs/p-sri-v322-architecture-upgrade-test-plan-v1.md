# P-SRI-V3.2.2 — Architecture Upgrade Production Acceptance Test Plan (v1)

**Project:** P-SRI-V3.2.2-BUILD-ACCEPTANCE  
**Date:** 2026-05-04  
**Status:** Draft for Gavin review, not yet executed  
**Author:** Cyler  

---

## 1. Purpose

This document defines the test plan I will use to determine whether Archie's v3.2.2 architecture upgrades are complete enough to accept for production.

This is **not** the execution report. It is the **acceptance plan only**.

The goal is to answer one question cleanly:

> Are the upgrades complete, correctly wired, and operationally reliable enough that MSTR can treat them as production-ready rather than “mostly built”?

The plan is intentionally broader than a code check. It tests five things:

1. **Scope completeness** — was the promised architecture actually built?
2. **Configuration completeness** — are the right tickers, layouts, symbols, schedules, and docs present?
3. **Functional correctness** — do the scripts, DB writes, summaries, and resolver behaviors work as claimed?
4. **Operational readiness** — can the system run repeatedly without manual babysitting?
5. **Doctrine correctness** — did the build actually land the v3.2.2 mental model, rather than just add new files beside old logic?

---

## 2. What this plan is testing

This acceptance plan covers the architecture-upgrade claims that matter for production:

### 2.1 Core build areas in scope
- v3.2.2 doctrine integration
- AB4 benchmark architecture
- AB3 deviation architecture
- Howell state freshness and schema correctness
- TV ingest architecture owned by MSTR Engine
- TradingView theme/layout/ticker completeness
- warehouse writes into `mstr.db`
- workspace outputs for Cyler (`tv_state.md`, `tv_history_index.md`, query helper)
- cron / LaunchAgent operational readiness
- documentation / runbook accuracy
- retirement-readiness of the old manual CSV workflow

### 2.2 Explicit high-risk items to test
These are the areas most likely to look “done” while still being operationally incomplete:

- missing tickers in TradingView layouts or YAML config
- invalid TV symbols or exchange prefixes
- layouts existing locally but not matching the intended watchlist/chart scope
- partial DB schema completion with stale consumer reads still alive elsewhere
- new resolver code existing, but old allocation logic still driving outputs
- workspace docs claiming a flow that does not match the live paths
- poll success on a smoke run, but not on repeated runs
- summary files or query tools missing, stale, or pointing to wrong locations
- architecture documents updated, but AGENTS / operator docs still teaching obsolete doctrine

---

## 3. Evidence standard

The build is only accepted if each major area produces **observable evidence**, not just claims.

Accepted evidence forms:
- exact file paths present in repo or deployed paths
- exact config entries present
- exact SQL rows / counts / timestamps in `mstr.db`
- exact CLI outputs
- exact generated markdown outputs
- exact log lines from scheduled or manual runs
- exact diff proof when replacing old behaviors

Not sufficient by itself:
- “script exists”
- “dry run looked okay”
- “first smoke test passed once”
- “layout exists in TradingView”
- “it should work because YAML includes it”

---

## 4. Acceptance structure

I will score the build in three buckets:

### 4.1 Category A — Must-pass before production
If any Category A test fails, the architecture is **not production-ready**.

### 4.2 Category B — Can ship with explicit known limitation
These may be accepted if:
- the limitation is documented,
- the system still functions safely,
- the limitation does not corrupt downstream analysis,
- and Gavin explicitly accepts it.

### 4.3 Category C — Nice-to-have / future hardening
These do not block production, but they should be logged.

---

## 5. Acceptance gates

Production acceptance requires **all** of the following:

1. **All Category A tests pass**
2. **No hidden doctrine conflicts remain** between old and new architecture
3. **TV scope is complete for the accepted v1 theme set**
4. **The warehouse path is operationally stable**
5. **Cyler-facing outputs are present and usable**
6. **Known limitations are explicit and bounded**
7. **At least one short soak window passes** after Archie declares the build complete

If any of those are not true, the answer is “not ready yet.”

---

## 6. Test phases

The execution plan will run in this order.

### Phase 1 — Claim audit
Objective: establish exactly what Archie claimed is complete.

Outputs:
- list of claimed deliverables
- list of claimed non-goals / descopes
- list of known limitations Archie already documented
- list of areas where the build doc and live config disagree

### Phase 2 — Static completeness audit
Objective: verify files, configs, docs, schema, and doctrine landed where they should.

Outputs:
- completeness matrix
- missing artifact list
- stale-artifact list
- doctrine conflict list

### Phase 3 — Functional test
Objective: verify the main scripts and data paths behave correctly.

Outputs:
- script pass/fail table
- DB evidence snapshots
- output-file verification
- mismatch/bug list

### Phase 4 — Operational test
Objective: verify the system can run like production, not just manually.

Outputs:
- poll reliability observations
- summary freshness observations
- LaunchAgent / log observations
- manual-intervention count

### Phase 5 — Production-readiness decision
Objective: classify the architecture as:
- **Accept for production**
- **Accept with explicit limitations**
- **Not ready**

Outputs:
- final verdict
- blocking defects
- non-blocking defects
- sign-off recommendation

---

## 7. Detailed test matrix

## 7.1 Phase 1 — Claim audit

### Test A1 — Build-scope reconciliation
**Question:** What exactly is Archie claiming is done?  
**Method:** Compare the build-design brief, runbook, live config, and latest upgrade notes.  
**Pass condition:** A single reconciled scope statement can be written without contradiction.  
**Fail condition:** Major ambiguity remains about what v1 includes versus what was deferred.

### Test A2 — De-scope reconciliation
**Question:** Are all descoped items clearly marked as descoped rather than silently missing?  
**Examples:** deep history backfill, indicator-history seeding, Camel decommission, future themes, extended multi-cycle backtest depth.  
**Pass condition:** Each missing behavior is either implemented or explicitly documented as deferred.  
**Fail condition:** Missing work is only discoverable by accident.

---

## 7.2 Phase 2 — Static completeness audit

### Test B1 — Required artifact presence
Verify presence of all required files, including at minimum:
- build design brief
- relevant doctrine briefs
- TV ingest runbook
- `tv_themes.yaml`
- `tv_ingest.py`
- `tv_poll.py`
- `tv_seed.py`
- `tv_warehouse.py`
- `tv_state_writer.py`
- `tv_query.py`
- migration SQL for `tv_*` tables
- resolver-related scripts introduced by the architecture work

**Pass:** All required artifacts exist in expected paths.  
**Fail:** Missing scripts, wrong paths, or placeholder stubs.

### Test B2 — Doctrine landing audit
Check whether the repo’s operator-facing docs now teach:
- AB4 as benchmark anchor
- AB3 as deviation layer
- RAW Hybrid as derived midpoint profile
- Howell as regime anchor
- no persistence of legacy “AB1/AB2/AB3/AB4 as static capital buckets” language where it would mislead live operation

**Pass:** operator docs and live doctrine docs are aligned enough for production.  
**Fail:** Cyler-facing docs still materially teach the wrong mental model.

### Test B3 — Howell freshness bug audit
Check that all known stale-read consumers were actually fixed:
- no `WHERE id=1` stale-read logic remaining in live consumers
- latest-row selection by timestamp or descending id now used consistently

**Pass:** no stale-read path remains in live workflows.  
**Fail:** even one live consumer still reading frozen historical Howell state.

### Test B4 — Howell schema completeness audit
Verify `howell_phase_state` landed the additional fields needed for:
- `VT`
- `DBC`

**Pass:** schema exists and consumer writes succeed.  
**Fail:** fields still missing or populated nowhere.

### Test B5 — TV theme completeness audit
This is one of the highest-priority checks.

Verify the accepted v1 theme set is fully represented in config, including:
- `mstr_suite`
- `visser`
- `mr_assets`

For each theme, verify:
- layout name exists
- theme enabled/disabled status is intentional
- ticker list is complete relative to the agreed target scope
- duplicates are intentionally deduped, not accidentally omitted
- comments do not conflict with live behavior

**Pass:** the config exactly matches the intended scope.  
**Fail:** theme omissions, incomplete ticker coverage, or undocumented scope drift.

### Test B6 — TradingView symbol correctness audit
For every configured ticker, verify symbol validity and exchange correctness.

This specifically targets errors like:
- wrong exchange prefix
- unsupported ratio expression
- symbol accepted by YAML but rejected by TV
- alternate symbol used in layout vs config mismatch

**Pass:** every configured ticker resolves correctly in TradingView.  
**Fail:** any broken symbol remains in the accepted scope.

### Test B7 — Layout/watchlist completeness audit
This is distinct from YAML.

Verify the actual TradingView account layouts/watchlists contain the intended assets needed for live use, not just the config file.

Questions:
- Are all expected tickers actually present in the relevant TV layouts/watchlists?
- Do the chart layouts correspond to the theme definitions?
- Are required indicators present on those layouts?
- Are there silent omissions that would cause partial ingestion or blind spots?

**Pass:** the actual TV account state is complete enough to support the architecture.  
**Fail:** YAML says yes, but TV account state says no.

### Test B8 — Workspace path audit
Verify the Cyler-facing output paths are correct and consistent with docs:
- `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_state.md`
- `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_history_index.md`
- query helper path and usage

**Pass:** docs and live outputs match.  
**Fail:** documented outputs missing, stale, or written somewhere else.

---

## 7.3 Phase 3 — Functional test

### Test C1 — DB migration integrity
Verify the new tables exist and are queryable:
- `tv_price_bars`
- `tv_indicator_values`
- `tv_ingest_runs`
- resolver-related tables introduced by the upgrade

**Pass:** schema exists with expected keys/indexes and no obvious migration damage.  
**Fail:** missing tables, wrong columns, or unusable schema.

### Test C2 — Single-theme poll functional test
Run poll against `mstr_suite` and confirm:
- layout switch works
- each ticker iterates correctly
- OHLCV rows write
- indicator values write
- ingest run row writes
- no ticker aliasing problem (same ticker data repeated under multiple ids)

**Pass:** one clean run with correct row distribution.  
**Fail:** silent ticker-switch failure, repeated bars, or partial writes.

### Test C3 — Multi-theme poll functional test
Run the same verification for:
- `visser`
- `mr_assets`

This is where completeness pressure rises, because broader theme sets are more likely to hide symbol, ratio, and layout issues.

**Pass:** each enabled theme completes with expected success/failure profile.  
**Fail:** themes exist on paper but not in a usable live state.

### Test C4 — Summary-writer functional test
Verify that after poll completion:
- `tv_state.md` regenerates
- `tv_history_index.md` regenerates
- content is current and internally consistent with warehouse contents

**Pass:** summaries match live warehouse state.  
**Fail:** summaries absent, stale, or inconsistent.

### Test C5 — Query helper functional test
Verify `tv_query.py` can:
- list available tickers
- return history for a valid ticker
- return indicators when requested
- behave correctly for ratio series and unusual symbols

**Pass:** query helper is genuinely usable by Cyler.  
**Fail:** exists but not operational.

### Test C6 — Resolver functional separation test
Verify that the new architecture actually routes posture through the v3.2.2 resolver rather than old allocation logic.

Questions:
- Is the old `AllocationEngine` still accidentally driving anything important?
- Are AB3 deviations being computed from benchmark vs actual, not from old bucket metaphors?
- Are RAW Hybrid weights truly derived, not manually duplicated?

**Pass:** live posture logic aligns with v3.2.2 architecture.  
**Fail:** new code exists but old logic still governs outputs.

### Test C7 — Idempotency / repeatability test
Re-run the same ingest path and verify:
- duplicate rows are not created improperly
- reruns refresh where expected
- previously written bars remain stable

**Pass:** reruns are safe.  
**Fail:** duplicate or corrupt writes appear.

---

## 7.4 Phase 4 — Operational test

### Test D1 — LaunchAgent readiness
Verify that the scheduled operational surface is actually ready:
- plist present
- bootstrap path valid
- logs writable
- scheduled environment resolves dependencies

**Pass:** system can run in scheduled context.  
**Fail:** only manual shell execution works.

### Test D2 — Short soak test
After Archie declares upgrades complete, require a short soak window.

Recommended minimum for acceptance:
- **3 consecutive trading days clean** for provisional acceptance
- **7 consecutive trading days clean** for full operational confidence

Observe:
- run success rate
- failed-ticker count
- summary-file freshness
- manual interventions required
- any “layout changed under us” failures

**Pass:** stability is demonstrated.  
**Fail:** repeated babysitting or unexplained drift.

### Test D3 — Data quality spot audit
Spot-check representative assets across all themes:
- ordinary equity
- ETF
- ratio chart
- crypto proxy
- macro index / yield
- commodity future

For each, confirm:
- latest bar timestamp is plausible
- OHLCV looks instrument-appropriate
- indicator count is plausible for that layout

**Pass:** sampled data looks real and differentiated.  
**Fail:** stale, duplicated, or instrument-inappropriate data.

### Test D4 — Failure-path behavior audit
Force or inspect representative failures:
- invalid ticker
- TV not connected
- missing layout
- one ticker fails inside otherwise-good run

**Pass:** failure is visible, bounded, and non-catastrophic.  
**Fail:** silent failure or corrupted downstream state.

---

## 7.5 Phase 5 — Production decision

### Test E1 — Blocking-defect review
List all remaining defects and classify each as:
- production blocker
- ship-with-limitation
- non-blocking cleanup

### Test E2 — Readiness verdict
The final verdict will be one of:

#### Accept for production
Use only if:
- all Category A tests pass
- no material doctrine conflict remains
- all accepted themes and tickers are complete
- operational surface is stable enough for unattended use

#### Accept with explicit limitations
Use only if:
- all critical functionality works
- remaining gaps are narrow and documented
- those gaps do not create blind spots or corrupt decisions

#### Not ready
Use if:
- any accepted scope area is materially incomplete
- any live consumer still reads stale/incorrect state
- TV layout/watchlist incompleteness creates ingestion blind spots
- scheduler path is unreliable
- operator docs remain materially misleading

---

## 8. Category A blockers

The following are automatic blockers for production acceptance.

### A-blocker 1 — Theme/ticker incompleteness
If the accepted TradingView theme set is missing required tickers in either:
- YAML config, or
- actual TV layouts/watchlists,

then the architecture is **not complete**.

### A-blocker 2 — Broken symbol resolution
Any accepted-scope ticker that cannot load correctly in TV is a blocker until either:
- fixed, or
- explicitly removed from accepted scope.

### A-blocker 3 — Stale live Howell consumer
Any live workflow still reading stale `howell_phase_state` is a blocker.

### A-blocker 4 — Old doctrine still driving live outputs
If old AB bucket logic is still operationally in charge, the upgrade is not accepted.

### A-blocker 5 — Missing Cyler-facing outputs
If `tv_state.md`, `tv_history_index.md`, or query access are not live and usable, the warehouse path is not production-ready for Cyler.

### A-blocker 6 — Scheduled path unreliable
If only manual runs work, acceptance is blocked.

### A-blocker 7 — Docs materially misstate live architecture
If operator docs tell the wrong story strongly enough to cause live misuse, that is a blocker.

---

## 9. Category B acceptable known limitations

These are potentially acceptable **only if explicit**.

### B1 — Deep OHLCV history not fully backfilled
Potentially acceptable if:
- current working coverage is sufficient for the immediate use case,
- the limitation is documented,
- no workflow silently assumes deeper history than exists.

### B2 — Indicator history is forward-only
Potentially acceptable if:
- documented clearly,
- no backtest or consumer claims otherwise.

### B3 — Future themes not yet accepted into v1
Potentially acceptable if:
- v1 accepted scope is explicit,
- missing themes are clearly out of scope rather than “supposedly done.”

---

## 10. Execution artifacts I will produce when we run this

When Archie finishes and we execute this plan, I will produce:

1. **Acceptance checklist** — one line per test with pass/fail/blocker
2. **Gap log** — every defect or mismatch found
3. **Evidence appendix** — commands, row counts, paths, timestamps, screenshots if needed
4. **Readiness memo** — production verdict with exact blockers or sign-off recommendation

---

## 11. Recommended immediate use of this plan

Before running the plan, Archie should use it as a punch list.

Most likely trouble areas, in order, are:
1. actual TV layout/watchlist completeness versus YAML intent
2. symbol correctness across broad Visser/MR Assets scope
3. Cyler-facing summary/output freshness
4. doctrine drift in operator docs
5. scheduled-context reliability versus one-off manual success

That is where I would expect the real gaps to surface first.

---

## 12. Bottom line

The standard for acceptance should not be “the scripts exist” or “the smoke test passed once.”

The standard should be:

> the promised v3.2.2 architecture is complete in scope, correct in doctrine, operational in TradingView and `mstr.db`, usable by Cyler through workspace outputs, and stable enough to run without hidden blind spots.

This test plan is designed to answer that precisely when Archie says he is ready.
