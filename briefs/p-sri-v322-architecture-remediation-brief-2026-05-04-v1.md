# P-SRI-V3.2.2 — Architecture Remediation Brief for Archie (2026-05-04, v1)

**Project:** P-SRI-V3.2.2-BUILD-REMEDIATION  
**Date:** 2026-05-04  
**Status:** Action brief derived from Cyler acceptance review  
**Author:** Cyler  
**Primary source:** `briefs/p-sri-v322-architecture-upgrade-acceptance-report-2026-05-04-v1.md`

---

## 1. Purpose

This brief converts the acceptance-review failures into a clean remediation sequence for Archie.

The goal is not to debate whether meaningful work was done. It was.
The goal is to close the remaining gaps that currently prevent production acceptance.

The order below is intentional.

**Fix these in order.** Do not skip ahead to polish while the ingest path itself is still untrustworthy.

---

## 2. Current production verdict

As of Cyler’s 2026-05-04 acceptance run, the architecture is:

## **NOT READY FOR PRODUCTION**

The two core reasons are:
1. **scope incompleteness** outside `mstr_suite`
2. **data-integrity failure** in the TradingView capture path

Everything below is organized around eliminating those blockers first.

---

## 3. Priority order

## Priority 0 — Restore trust in symbol identity and market data capture

This is the single highest-priority issue.

### Problem
Distinct symbols are returning the same latest OHLCV bar through the live TradingView ingest path.

Confirmed examples during acceptance:
- `AMEX:SPY`
- `AMEX:GLD`
- `AMEX:IWM`

All returned the same latest bar values.

The scheduled poll logs also showed the same close repeating across many different tickers during the `mstr_suite` run.

### Why this is a hard blocker
If symbol switching is not actually taking effect before bar reads, then:
- warehouse rows are untrustworthy
- `tv_state.md` is untrustworthy
- downstream analysis is untrustworthy
- completeness of ticker scope becomes secondary, because bad data at scale is worse than incomplete data

### Required remediation
Archie should produce a root-cause fix for symbol identity, not a cosmetic patch.

That means explicitly verifying:
1. `set_symbol()` is truly switching the active chart symbol in TradingView before `ohlcv()` is called
2. the chart is actually ready after symbol switch, not merely returning CLI success
3. the returned OHLCV belongs to the intended symbol, not the previously loaded symbol or a cached chart state
4. ratio charts and ordinary symbols both pass the same identity checks

### Expected evidence for closure
Before asking for re-acceptance, Archie should provide:
- a short evidence log showing **at least 5 materially different symbols** returning differentiated bars after switching
- at least one test each for:
  - equity
  - ETF
  - ratio chart
  - crypto proxy
  - macro index
- proof that `chart_ready: false` is no longer being treated as acceptable if it correlates with bad data identity

### Suggested implementation direction
Possible areas to inspect:
- insufficient wait / readiness gating after symbol switch
- `tv` CLI returning success before chart state updates
- need for an explicit `chart_state()` confirmation loop after `set_symbol()`
- stale chart window / wrong panel / wrong tab assumptions
- direct-bars call reading from the current loaded series before symbol change settles

Do not move on until this is fixed.

---

## Priority 1 — Make the scheduler actually run the accepted scope

### Problem
The live LaunchAgent is still hard-wired to:
- `tv_poll.py --theme mstr_suite`

But the accepted config now includes enabled themes:
- `mstr_suite`
- `visser`
- `mr_assets`

### Why this is a blocker
The accepted architecture cannot claim multi-theme production coverage if the scheduled runtime only executes one theme.

### Required remediation
Archie needs to choose and implement one explicit runtime model:

### Option A — one scheduled run iterates all enabled themes
Preferred if operationally reliable.

### Option B — one scheduled job per theme
Also acceptable if explicit and well documented.

### Non-acceptable state
- docs imply broad scope
- YAML enables broad scope
- scheduler actually runs `mstr_suite` only

### Expected evidence for closure
- updated LaunchAgent or job set
- logs from scheduled execution proving all accepted themes actually ran
- documentation updated to match the real runtime model exactly

---

## Priority 2 — Bring `visser` and `mr_assets` to real scope completeness

### Problem
Current warehouse 4H coverage observed during acceptance:
- `mstr_suite`: 16/16 tickers present
- `visser`: 5/43 tickers present
- `mr_assets`: 11/35 tickers present

This is materially incomplete.

### Why this matters
Even after the scheduler is fixed, production cannot be accepted unless the intended scope actually resolves, loads, and writes.

### Required remediation
For both `visser` and `mr_assets`, Archie should produce a true completeness pass:

1. verify every configured ticker exists in the intended TradingView layout/watchlist environment
2. verify every configured ticker symbol resolves correctly
3. verify every configured ticker produces nonzero warehouse coverage
4. explicitly classify any ticker that is removed or deferred rather than silently leaving it at zero coverage

### Expected evidence for closure
Provide a per-theme matrix with columns:
- ticker id
- configured TV symbol
- loads in TV? (yes/no)
- writes bars? (yes/no)
- writes indicators? (yes/no)
- latest timestamp
- disposition (`pass`, `fixed`, `deferred`, `removed-from-scope`)

No hidden zero-coverage leftovers.

---

## Priority 3 — Refresh stale broader-theme data

### Problem
Even where `visser` and `mr_assets` have nonzero coverage, much of it tops out around:
- `2026-04-17`

That means the broader themes are not live.

### Required remediation
After fixing:
- symbol identity
- scheduler scope
- ticker completeness

Archie must run fresh ingest so all accepted live themes have current timestamps.

### Expected evidence for closure
For each accepted theme, provide:
- min latest timestamp
- max latest timestamp
- number of tickers whose latest bar is within expected freshness window

Target for closure:
- all accepted tickers should have recent latest bars appropriate to instrument/session timing
- no large stale subpopulation should remain unexplained

---

## Priority 4 — Align docs with actual runtime behavior

### Problem
Current docs and code are telling different stories.

Examples:
- `tv_poll.py` docstring implies a broader “for each in-scope theme” operational model
- the LaunchAgent currently runs only `mstr_suite`
- broader themes are enabled in YAML but not actually production-polled

### Why this matters
Operator confusion is not a cosmetic issue here. It leads directly to false confidence and missed blind spots.

### Required remediation
Archie should update all operator-facing docs so that they accurately describe:
- what themes are currently accepted live scope
- how scheduled polling actually works
- whether a single scheduled run processes one theme or all enabled themes
- what “enabled: true” means operationally
- what counts as draft / partial / active / accepted

### Expected evidence for closure
Updated consistency across:
- `tv_poll.py` docstring
- `tv-ingest-runbook.md`
- build brief where relevant
- any AGENTS / operational docs that mention the polling model

---

## Priority 5 — Cleanly separate accepted scope from follow-on scope

### Problem
The build drifted from:
- rev7 saying v1 ships `mstr_suite` only

to:
- YAML now containing enabled `visser` and `mr_assets`

That is fine if intentional, but it must be governed cleanly.

### Required remediation
Archie should explicitly state one of the following:

### Path 1 — expanded v1
`mstr_suite + visser + mr_assets` are now all accepted v1 scope and must all meet production bars.

### Path 2 — phased acceptance
Only `mstr_suite` is production v1; `visser` and `mr_assets` are staging themes pending later acceptance.

### Important note
Given current YAML and current expectations, Cyler assumes **Path 1** unless Archie and Gavin intentionally re-scope it.

### Expected evidence for closure
A short scope declaration committed in repo, not just chat.

---

## Priority 6 — Clean stale workspace/script copies that still encode old bugs

### Problem
Cyler’s acceptance pass still found stale `WHERE id=1` logic in:
- `Grok/scripts/daily_analysis_cycle.py`

The deployed `~/mstr-engine/scripts` path appears cleaner on this issue, but stale workspace copies still create confusion and future regression risk.

### Required remediation
Archie should either:
1. update the stale copies, or
2. clearly retire them so nobody mistakes them for live runtime sources

### Expected evidence for closure
- grep-clean evidence for stale-read bug across relevant live and mirrored codepaths, or
- explicit archival/retirement note if some copies are intentionally non-live

---

## Priority 7 — Clarify legacy `AllocationEngine` status

### Problem
The new resolver is real and useful, but legacy allocation code still exists in `sri_engine.py`.

That alone is not a production blocker, but it increases ambiguity about what truly governs live behavior.

### Required remediation
Archie should make the status explicit:
- still used somewhere live? or
- legacy only / retained for backward compatibility?

If legacy only, mark it clearly and ensure no key workflow still depends on it.

### Expected evidence for closure
- grep-based usage note
- short architecture note on which path is authoritative for v3.2.2 posture logic

---

## 4. What Archie should deliver back before re-test

Before Cyler re-runs acceptance, Archie should publish a short remediation package containing:

### Required artifacts
1. **Root-cause note** for the repeated-bar/symbol-identity bug
2. **Scheduler/runtime note** describing how all accepted themes are polled
3. **Per-theme completeness matrix** for `mstr_suite`, `visser`, `mr_assets`
4. **Fresh coverage evidence** showing accepted themes are current
5. **Doc-alignment note** describing what was updated

### Strongly preferred
6. one concise “ready for re-acceptance” note with:
- accepted scope
- known limitations
- anything intentionally deferred

---

## 5. Re-acceptance bars

Cyler should not re-run full acceptance until Archie can reasonably claim all of the following:

1. **different symbols produce different bars reliably**
2. **all accepted themes are actually polled in scheduled production path**
3. **all accepted-scope tickers either load successfully or are explicitly removed/deferred**
4. **broader themes are fresh, not stale April leftovers**
5. **runtime docs match reality**

Only then is a second acceptance run likely to be worth the time.

---

## 6. Bottom line for Archie

The main message is:

> The architecture is not being rejected because nothing was built. It is being held back because the live TradingView production path is still incomplete and not yet trustworthy.

So the remediation focus should be:
1. **fix trust in the data path**
2. **make runtime scope match accepted scope**
3. **complete and refresh the broader theme coverage**
4. **clean up the story the docs are telling**

That is the shortest path to production acceptance.
