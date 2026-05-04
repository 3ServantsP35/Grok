# P-SRI-V3.2.2 — Architecture Upgrade Acceptance Report (2026-05-04, v1)

**Project:** P-SRI-V3.2.2-BUILD-ACCEPTANCE  
**Date:** 2026-05-04  
**Status:** Test plan executed, production acceptance review complete  
**Author:** Cyler  
**Reference plan:** `briefs/p-sri-v322-architecture-upgrade-test-plan-v1.md`

---

## 1. Executive verdict

**Verdict: NOT READY FOR PRODUCTION**

Archie’s upgrade work contains several real architectural wins, but the current live state fails multiple **Category A** acceptance gates.

The most important blockers are:

1. **The scheduled production path is polling `mstr_suite` only**, even though the accepted config now includes enabled `visser` and `mr_assets` themes.
2. **The broader TV theme scope is materially incomplete in live warehouse coverage.**
3. **The live TradingView capture path is not yet data-trustworthy.** Multiple distinct instruments are returning the same latest OHLCV bar, which is a production blocker.
4. **Docs and code still conflict on “one theme vs all in-scope themes” runtime behavior.**

Because of those failures, this upgrade cannot yet be accepted as satisfactory for production.

---

## 2. What was tested

I worked the acceptance plan across these areas:

- architecture artifact presence
- DB schema presence and seed state
- Howell freshness/schema fixes
- doctrine landing in operator docs
- TV theme config completeness
- LaunchAgent / scheduler wiring
- TV warehouse outputs (`tv_state.md`, `tv_history_index.md`)
- query helper usability
- resolver usability
- live data-integrity spot tests using the TradingView CLI path
- logs and recent run behavior

I did **not** attempt to fix the issues in this pass. This is an acceptance review, not a remediation pass.

---

## 3. High-level outcome summary

## 3.1 Areas that passed or substantially passed

### A. Core v3.2.2 schema exists
Confirmed in `mstr.db`:
- `ab_profile_selection`
- `ab4_benchmark`
- `ab4_tolerance_bands`
- `ab3_deviation_log`
- `tv_price_bars`
- `tv_indicator_values`
- `tv_ingest_runs`
- `howell_phase_state`

### B. Howell schema expansion landed
Confirmed additional `howell_phase_state` columns exist:
- `vt_sribi`
- `vt_signal`
- `dbc_sribi`
- `dbc_signal`

### C. AB profile seeds landed
Observed:
- `ab_profile_selection`: **5 rows**
- `ab4_benchmark`: **128 rows**
- `ab4_tolerance_bands`: **5 rows**
- `ab3_deviation_log`: **32 rows**

### D. Resolver exists and is functionally usable
`ab_profile_resolver.py` runs and produced a coherent dry-run result for `greg` using:
- profile = `RAWHybrid`
- phase = `Turbulence`
- per-sleeve benchmark vs actual rollup
- tiered deviations

This is meaningful progress and one of the stronger completed pieces.

### E. Cyler-facing warehouse outputs exist
Confirmed present and auto-generated:
- `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_state.md`
- `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_history_index.md`

### F. Query helper is usable
`tv_query.py --list-tickers` returned warehouse coverage and is operational.

### G. Operator docs were partially updated correctly
`Grok/AGENTS.md` now references:
- `tv_state.md`
- `tv_history_index.md`
- TV warehouse usage

That lockstep rewrite appears materially improved versus the older state.

---

## 3.2 Areas that failed acceptance

### A. Scheduler/runtime scope does not match accepted theme scope
The accepted live config now includes three enabled themes:
- `mstr_suite` — **16 tickers**
- `visser` — **43 tickers**
- `mr_assets` — **35 tickers**

But `~/Library/LaunchAgents/com.mstr.tv-feed.plist` is still hard-wired to:

```text
/Users/vera/mstr-engine/.venv/bin/python3
/Users/vera/mstr-engine/scripts/tv_poll.py
--theme
mstr_suite
```

So the scheduled production path is **not** polling all accepted in-scope themes.

This is a direct **Category A blocker**.

### B. Live warehouse coverage is materially incomplete outside `mstr_suite`
Observed 4H theme coverage in `tv_price_bars`:
- `mstr_suite`: **16 distinct tickers** loaded
- `visser`: **5 distinct tickers** loaded
- `mr_assets`: **11 distinct tickers** loaded

Relative to configured scope:
- `mstr_suite`: **16 / 16 = 100%**
- `visser`: **5 / 43 = 11.6%**
- `mr_assets`: **11 / 35 = 31.4%**

`tv_history_index.md` confirms many configured tickers still show:
- earliest bar = `—`
- latest bar = `—`
- bar count = `0`

Examples from `visser` with zero coverage:
- `TSM`, `AVGO`, `MRVL`, `GOOGL`, `VST`, `CEG`, `ETN`, `VRT`, `ANET`, `GLW`, `CDNS`, `SNPS`, `MU`, `LLY`, `COHR`, `AMD`, `ARM`, `QCOM`, `AAPL`, `ORCL`, `NOW`, `SAP`, all relative charts, and most of the frontier/material/software set

Examples from `mr_assets` with zero coverage:
- `US02Y`, `US10Y`, `ETHUSD`, `TOTAL`, `TOTAL2`, `BTC_D`, `ETH_D`, `HG1`, `SI1`, `CL1`, `NG1`, `FCX`, `SLV`, `IWM_SPY`, `QQQ_SPY`, `BTC_QQQ`, and others

This is a direct **scope completeness failure**.

### C. `visser` and `mr_assets` are stale, not live
Theme max timestamps in warehouse:
- `mstr_suite`: latest through **2026-05-02 / 2026-05-01** depending on ticker
- `visser`: latest **2026-04-17T17:30:00+00:00**
- `mr_assets`: many latest bars also **2026-04-17T17:30:00+00:00**

So even where nonzero coverage exists, much of it is **stale**.

This means the broader architecture is not functioning as a live production feed.

### D. Critical data-integrity failure: repeated OHLCV across distinct symbols
This is the most serious functional blocker.

Evidence from `tv_state.md` and logs showed that multiple different instruments were sharing the same latest OHLCV bar and volume. Example from the 2026-05-04 09:30 PT scheduled poll:

- `SPY`: open `722.96`, high `723.22`, low `720.47`, close `720.67`, volume `11,092,985`
- `GLD`: open `722.96`, high `723.22`, low `720.47`, close `720.67`, volume `11,092,985`
- `IWM`: open `722.96`, high `723.22`, low `720.47`, close `720.67`, volume `11,092,985`

The log confirms the same latest close repeated across the run:
- `MSTR` → close `720.67`
- `IBIT` → close `720.67`
- `BTCUSD` → close `720.67`
- `STRC` → close `720.67`
- `SPY` → close `720.67`
- `GLD` → close `720.67`
- `IWM` → close `720.67`
- `DXY` → close `720.67`
- ratio charts also reporting the same close

I then manually spot-tested the live TradingView CLI path directly:

### Manual symbol-switch spot test
Commands executed sequentially for:
- `AMEX:GLD`
- `AMEX:IWM`
- `AMEX:SPY`

Each returned the same latest 4H bar:
- time `1777656600`
- open `722.96`
- high `723.22`
- low `720.47`
- close `720.67`
- volume `11092985`

So this is not just a markdown-rendering problem. The capture path itself is not reliably switching symbols before reading data.

This is an automatic **Category A production blocker**.

### E. `tv_poll.py` docs vs runtime behavior are inconsistent
`tv_poll.py` module docstring says:

> “For each in-scope theme...”

But the actual implementation takes **one theme per run** and defaults to:
- `--theme mstr_suite`

The LaunchAgent likewise invokes only `mstr_suite`.

So the runtime behavior does not match the operational story implied by the docs.

This is a significant architecture/documentation mismatch.

---

## 4. Detailed test results by acceptance area

## 4.1 Phase 1 — Claim audit

### Result: PARTIAL PASS
Archie’s claims can be reconciled only if interpreted narrowly:
- the **core warehouse scaffolding** exists
- the **broad multi-theme productionization** is **not actually complete**

The phrase “architecture upgrades are done” is too strong for the current live state.

---

## 4.2 Phase 2 — Static completeness audit

### Required artifact presence
**Result: PASS**

The main scripts, docs, migration files, and config artifacts exist.

### Doctrine landing audit
**Result: PARTIAL PASS**

Good:
- AGENTS references rev7 warehouse files
- v3.2.2 doctrine docs are present

Open concern:
- legacy `AllocationEngine` remains in `sri_engine.py`
- stale legacy script copies remain in workspace/Grok paths

I do **not** treat the mere existence of legacy code as a blocker by itself, but it increases confusion risk.

### Howell freshness bug audit
**Result: MIXED**

Good:
- no `WHERE id=1` stale-read hits were found in `~/mstr-engine/scripts`

Concern:
- stale `WHERE id=1` references still exist in `Grok/scripts/daily_analysis_cycle.py`

Interpretation:
- **deployed MSTR engine path appears clean** on this specific issue
- **workspace copies are still stale** and should be cleaned or clearly retired

This is **not my top blocker**, but it is still worth fixing.

### Howell schema completeness audit
**Result: PASS**

`VT` / `DBC` fields exist as planned.

### TV theme completeness audit
**Result: FAIL**

Themes exist in YAML, but live coverage and scheduler behavior do not match accepted scope.

### TradingView symbol correctness audit
**Result: FAIL**

Even apart from zero-coverage tickers, the live symbol-switch path is not trustworthy. Data integrity fails before full symbol validation can be considered complete.

### Layout/watchlist completeness audit
**Result: FAIL**

The warehouse evidence strongly suggests the TV account / layout / switching path is not yet aligned with the intended full-scope themes.

### Workspace path audit
**Result: PASS**

The summary files and paths exist where Cyler expects them.

---

## 4.3 Phase 3 — Functional audit

### DB migration integrity
**Result: PASS**

Core schema present and queryable.

### Single-theme poll functional test (`mstr_suite`)
**Result: FAIL (integrity)**

The poll completes mechanically, but the **captured data is not trustworthy** because multiple symbols resolve to the same latest bar.

A run that “succeeds” while ingesting bad market identity is **not** a real success.

### Multi-theme poll functional state
**Result: FAIL**

The broader themes are neither fully loaded nor kept fresh by the scheduler.

### Summary-writer functional test
**Result: PASS WITH CAVEAT**

`tv_state.md` and `tv_history_index.md` do regenerate.

Caveat:
- they are accurately summarizing a **partially stale / partially incorrect** warehouse
- so the file generation works, but the underlying data quality is not production-safe

### Query helper functional test
**Result: PASS**

The helper works against the warehouse and is useful.

### Resolver functional separation test
**Result: PARTIAL PASS**

Good:
- `ab_profile_resolver.py` exists and works
- benchmark tables are populated
- deviation log exists and has data

Open concern:
- only two portfolios appear in `ab3_deviation_log` so far (`greg`, `gavin`)
- legacy `AllocationEngine` still exists in `sri_engine.py`
- integration of resolver into broader live automation should be reviewed further after TV issues are fixed

This is **not currently the primary blocker**.

### Idempotency / repeatability
**Result: NOT FULLY CLEARED**

The table design appears idempotent by key, but because the symbol-switch/data-integrity layer is failing, I do not consider repeatability truly validated yet.

---

## 4.4 Phase 4 — Operational audit

### LaunchAgent readiness
**Result: PARTIAL FAIL**

Good:
- plist exists
- scheduled times are correctly defined
- logs are writable
- scheduled run happened on 2026-05-04 09:30 PT

Fail:
- the scheduled path runs only `mstr_suite`
- not all accepted live themes

### Short soak test
**Result: NOT PASSED**

A soak window cannot count as passed while:
- the scheduler ignores two enabled themes
- broader theme coverage is stale/incomplete
- symbol identity is corrupted in the capture path

### Data-quality spot audit
**Result: FAIL**

The repeated-bar issue is disqualifying.

### Failure-path behavior
**Result: NOT FULLY TESTED / DEFERRED**

No further failure-path probing was needed after the Category A blockers surfaced.

---

## 5. Category A blockers

These blockers prevent production acceptance right now.

### Blocker 1 — Scheduler only polls `mstr_suite`
Accepted scope and live schedule do not match.

### Blocker 2 — `visser` theme coverage is only 5/43 tickers
This is far below acceptable completeness.

### Blocker 3 — `mr_assets` theme coverage is only 11/35 tickers
Also below acceptable completeness.

### Blocker 4 — `visser` and `mr_assets` data are stale
Much of the nonzero data tops out on **2026-04-17**.

### Blocker 5 — Symbol/data identity failure in live capture
Distinct symbols return the same OHLCV bars. This is the most serious blocker.

### Blocker 6 — Docs imply broader runtime scope than code actually runs
Operational story and production behavior diverge.

---

## 6. Non-blocking or secondary issues

These matter, but they are not the main reason for rejection.

### Secondary 1 — Legacy stale-read copies remain in Grok workspace scripts
Observed in `Grok/scripts/daily_analysis_cycle.py`:
- still reading `howell_phase_state WHERE id=1`

This appears outside the deployed `mstr-engine` runtime, but it should still be cleaned up or retired clearly.

### Secondary 2 — Legacy allocation engine still exists in `sri_engine.py`
Not a blocker by itself if retired in practice, but it increases operator confusion risk.

### Secondary 3 — Only two portfolios have persisted deviation-log evidence so far
Not fatal, but worth extending once the ingest layer is trustworthy.

---

## 7. Positive findings worth preserving

To be clear, this is not a zero-value build. Several pieces are good and should be preserved:

1. **Warehouse schema shape is sound**
2. **Resolver architecture is real and usable**
3. **Cyler-facing summary outputs are the right pattern**
4. **AGENTS / docs have moved materially closer to the right rev7 model**
5. **The theme-based config model is directionally correct**

The issue is not that nothing was built. The issue is that the live operational path still fails essential completeness and integrity bars.

---

## 8. What must be true before re-test

Before I would re-run acceptance, Archie should at minimum close these:

### Required before re-test
1. **Fix symbol-switch / chart-read integrity** so different symbols stop returning the same bar
2. **Make scheduler/runtime actually poll the full accepted theme scope**, not just `mstr_suite`
3. **Populate and verify full theme coverage** for `visser` and `mr_assets`
4. **Refresh stale broader-theme data** so warehouse timestamps are current
5. **Align code and docs** on whether poll runs one theme or all enabled themes per scheduled execution

### Strongly recommended before re-test
6. clean stale workspace copies of old Howell-read logic
7. document clearly which theme set is accepted v1 scope vs follow-on scope
8. produce one clean evidence artifact showing per-theme coverage = expected configured tickers

---

## 9. Final recommendation

My recommendation is:

> **Do not accept the architecture upgrades as production-ready yet.**

Instead:
- treat the current state as **substantial but incomplete**
- fix the TV runtime/data-integrity blockers first
- then re-run this acceptance plan

The strongest concise summary is:

> The scaffolding is real, the resolver side is promising, and the workspace-output pattern is good, but the live TradingView production path is still incomplete and not yet trustworthy enough for production acceptance.

---

## 10. Key evidence points

### Theme counts from config
- `mstr_suite`: 16 tickers
- `visser`: 43 tickers
- `mr_assets`: 35 tickers

### Distinct 4H tickers actually present in warehouse
- `mstr_suite`: 16
- `visser`: 5
- `mr_assets`: 11

### Max timestamps by theme in warehouse
- `mstr_suite`: current into 2026-05-01 / 2026-05-02
- `visser`: 2026-04-17
- `mr_assets`: mostly 2026-04-17

### LaunchAgent invocation
- `tv_poll.py --theme mstr_suite`

### Repeated-bar spot test
`AMEX:GLD`, `AMEX:IWM`, and `AMEX:SPY` all returned:
- open `722.96`
- high `723.22`
- low `720.47`
- close `720.67`
- volume `11092985`

That single finding alone is enough to block production.
