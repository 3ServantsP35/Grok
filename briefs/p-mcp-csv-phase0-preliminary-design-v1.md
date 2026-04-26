# P-MCP-CSV Phase 0 Preliminary Design — MSTR 4H Golden Path
**Project:** P-MCP-CSV  
**Date:** 2026-04-26  
**Author:** Archie  
**Status:** Revised preliminary design with implementation plan and production-risk controls

---

## Executive Summary

This document translates the approved Phase 0 standardization spec into a preliminary design and implementation plan.

The design goal is to:

- automate acquisition of one deterministic TradingView export workflow for **MSTR 4H** on the **Mac Studio**
- enforce **4H** as a hard chart and indicator calibration rule
- validate the acquired export strictly
- publish a normalized repo copy as `MSTR_4H.csv`
- fail closed on any invalid or incomplete run
- preserve the current downstream MSTR Suite workflow
- **nearly eliminate risk to the current engines and production environment**

The most important risk is not simple implementation failure. The most important risk is **silently publishing a bad CSV into production and contaminating downstream reporting**.

Because of that, this design now includes a **production-safety architecture**, a **risk-mitigation plan**, and an **implementation plan** that requires shadow mode and guarded rollout before any production cutover.

---

## 1. Design Objective

Implement a local Phase 0 workflow on the Mac Studio that:

1. accesses TradingView through a persistent authenticated browser session
2. opens the canonical MSTR 4H chart
3. verifies **4H** timeframe state before export
4. triggers the TradingView CSV download
5. validates file identity, schema, historical depth, and freshness
6. writes a manifest and validation log
7. initially publishes only to **non-production shadow destinations**
8. confirms downstream compatibility via smoke test
9. only after repeated successful shadow runs, copies the validated file into the `Grok` repo root as `MSTR_4H.csv`
10. commits and pushes the result
11. reports success or failure to local logs and Discord

---

## 2. Design Principles

### 2.1 Contract before automation
The validator and file-handling contract are primary.

Automation must conform to the contract, not redefine it.

### 2.2 Fail closed
If the export is missing, stale, malformed, or incompatible, the run must stop before publication.

### 2.3 Preserve raw artifacts
The original TradingView download remains intact for traceability and recovery.

### 2.4 4H is a hard rule
The chart timeframe must be **4H**.

This is not just a data preference. It is part of the calibrated indicator environment and therefore part of the export contract.

Any non-4H chart state is an automatic failure.

### 2.5 Normalize only at publish boundary
The raw file may vary in suffix, but the published repo copy must always be:
- `MSTR_4H.csv`

### 2.6 Downstream compatibility over elegance
The system should preserve the current downstream model, including duplicate columns and TradingView-specific quirks.

### 2.7 Production safety over speed
No implementation convenience should be allowed to risk the current engines.

A slower rollout with shadow mode, backups, and rollback protection is preferable to a faster rollout that can alter live production inputs prematurely.

---

## 3. Scope

### 3.1 In scope
- one-symbol, one-timeframe Phase 0 flow for **MSTR 4H**
- Mac Studio local browser-based TradingView access and export automation
- Mac Studio local intake, staging, validation, publish, and reporting flow
- shadow-mode and guarded production rollout
- manifest/logging support
- GitHub publish support
- downstream smoke-test gate
- rollback and backup protections

### 3.2 Out of scope
- support for the full MSTR Suite export set
- redesign of downstream analytics
- replacement market data source
- database-backed orchestration
- weekly timeframe support
- broad multi-chart orchestration beyond the single MSTR 4H golden path

---

## 4. Revised System Boundary

### 4.1 Access layer
The system is responsible for obtaining the export from TradingView.

That means the automated boundary now begins before file intake and includes:
- opening the TradingView session on the Mac Studio
- navigating to the canonical saved MSTR chart
- verifying the chart is in **4H**
- triggering the CSV export
- waiting for the download artifact to appear in intake

### 4.2 Processing layer
Once the raw file lands in the intake location, the system handles:
- discovery
- validation
- manifest creation
- staging
- shadow publish
- smoke test
- optional guarded production publish
- commit/push
- reporting

### 4.3 Boundary recommendation
The right boundary remains:
- **one chart = one export contract = one validation path**

The difference is that the export action itself is now inside the automated system boundary.

### 4.4 Why this boundary is correct
This preserves TradingView as the source of truth while still allowing the system to acquire the data directly.

It also keeps the calibrated chart state, including **4H**, inside the controlled contract instead of treating it as a human prerequisite.

---

## 5. Production-Safety Architecture

### 5.1 Core production concern
The main production risk is:
- a stale, malformed, wrong-chart, or wrong-timeframe CSV being published into the live path and consumed by current engines

### 5.2 Safety model
To nearly eliminate that risk, the system should operate in three modes:

1. **Dry-run mode**
   - acquires export
   - validates
   - writes logs/manifests
   - does not publish anywhere used by production

2. **Shadow mode**
   - acquires export
   - validates
   - writes logs/manifests
   - publishes only to a non-production destination
   - runs smoke tests
   - does not replace the live production artifact

3. **Production mode**
   - allowed only after shadow success criteria are met
   - writes backup of the current live artifact first
   - replaces production artifact only after all gates pass

### 5.3 Required safety barriers
Before any live publish is allowed, the system must support:
- dry-run mode
- shadow mode
- production mode flag separation
- backup of prior production artifact
- rollback command or script
- smoke test gate
- fail-closed default behavior
- explicit publish target separation

### 5.4 Production-separation rule
The new automation must not initially write to the same destination relied on by the current engines.

The current engines should continue consuming the existing path until shadow validation has proven stable.

---

## 6. Proposed Local Architecture

### 6.1 Directories
Recommended paths on the Mac Studio:

- `~/Downloads/tradingview-intake/`
  - raw TradingView downloads
- `~/tradingview-sync/staging/`
  - per-run staging work
- `~/tradingview-sync/logs/`
  - validation logs and run summaries
- `~/tradingview-sync/manifests/`
  - machine-readable run manifests
- `~/tradingview-sync/shadow-publish/`
  - non-production published artifacts for validation
- local `Grok` repo working copy
  - guarded production publish target

### 6.2 Staging layout
Recommended per-run structure:

```text
~/tradingview-sync/staging/
  <run_id>/
    raw/
    validation/
    shadow/
    publish/
```

Example:

```text
~/tradingview-sync/staging/20260426T113000-ct-midday/
```

### 6.3 Production backup layout
Recommended backup path:

```text
~/tradingview-sync/backups/
  MSTR_4H/
    2026-04-26T113000-ct-midday.csv
```

### 6.4 Why this layout
This provides:
- run isolation
- reproducibility
- easier debugging
- durable audit trail
- non-production verification area
- recoverable live publish rollback

---

## 7. Proposed Runtime Flow

### 7.1 Run types
Supported Phase 0 run types:
- `midday`
- `close`
- `manual-test`

### 7.2 Operating modes
Supported execution modes:
- `dry-run`
- `shadow`
- `production`

### 7.3 Sequence
1. runner launches or attaches to the dedicated authenticated TradingView browser session on the Mac Studio
2. runner opens the canonical saved MSTR chart
3. runner verifies symbol and **4H** timeframe state
4. runner triggers the TradingView CSV export
5. raw file lands in `~/Downloads/tradingview-intake/`
6. runner identifies the candidate file for the requested run type
7. runner copies raw file into run staging
8. validator checks identity, header contract, historical depth, freshness, and file integrity
9. validator computes schema fingerprint and writes validation result
10. runner writes manifest
11. if mode is `dry-run`, stop after validation and reporting
12. if mode is `shadow`, copy validated file to shadow destination and run smoke tests
13. if mode is `production`, first verify production gating eligibility, then back up the live artifact, then publish to repo root as `MSTR_4H.csv`
14. runner commits and pushes when production publish is enabled
15. runner reports success or failure

### 7.4 Acquisition gate
No validation begins until the system has confirmed that a fresh download was successfully triggered and observed.

### 7.5 Shadow gate
No production publish may occur unless shadow behavior has already been proven in repeated successful runs.

### 7.6 Publish gate
No publish step occurs unless all access and validation gates pass.

### 7.7 Smoke-test gate
A run is not fully successful until the downstream smoke test passes.

---

## 8. TradingView Access Design

### 8.1 Access model
The preferred acquisition path is **browser-driven TradingView export automation** on the Mac Studio.

This means the system should use a persistent browser session that is already authenticated to TradingView and capable of opening the canonical saved chart.

### 8.2 Why browser-driven export is the right Phase 0 path
This is the right initial path because it:
- preserves TradingView as source of truth
- preserves the exact chart-state contract
- preserves indicator fidelity
- avoids premature reconstruction of TradingView outputs from alternative data sources

### 8.3 Session model
Recommended model:
- dedicated browser profile for TradingView automation
- persistent authenticated session maintained on the Mac Studio
- fail closed if the session is logged out or requires unexpected human re-authentication

### 8.4 Chart navigation model
The system should navigate to one canonical saved chart for MSTR.

That chart must be treated as a configuration object, not just a visual destination.

### 8.5 4H timeframe standardization policy
**4H is mandatory.**

The automation must verify that the active TradingView chart is set to **4H** before any export action is attempted.

A chart discovered in any other timeframe must fail immediately.

This rule exists because the MSTR indicators are tuned and calibrated to 4H, and future indicators are expected to follow the same standard unless explicitly overridden.

### 8.6 Export trigger model
The automation must invoke the normal TradingView CSV export path, not a substitute data retrieval method, during this phase.

### 8.7 Download detection model
After export is triggered, the system should watch the intake directory for the new file associated with the current run.

Failure to observe a fresh file inside the configured wait window is a hard failure.

### 8.8 Access-layer failure cases
Hard fail if:
- TradingView session is not authenticated
- canonical chart cannot be opened
- symbol does not match the target chart
- timeframe is not **4H**
- export action cannot be triggered
- download artifact does not appear in the intake path
- TradingView UI drift prevents reliable export

---

## 9. Data Contract Handling

### 9.1 Canonical input contract
The canonical source object is:
- `BATS_MSTR, 240_57f94.csv`

It defines:
- symbol/timeframe intent
- expected header list
- duplicate header behavior
- minimum historical window

### 9.2 Canonical published artifact
The repo-facing published artifact must always be:
- `MSTR_4H.csv`

### 9.3 Raw file retention
The original TradingView filename must be retained in intake/staging and referenced in the manifest.

### 9.4 Shadow artifact
Recommended shadow-published filename:
- `MSTR_4H.shadow.csv`

This allows repeated comparisons and smoke testing without touching live production inputs.

---

## 10. Validation Design

### 10.1 Validation stages
Validation should run in this order:

1. file presence check
2. parseability check
3. file identity check
4. schema/header check
5. historical depth check
6. freshness check
7. publish-precondition check
8. smoke-test gate after shadow or production publish

### 10.2 File presence check
Confirm exactly one intended candidate file has been selected for the run.

Fail if:
- no candidate file is found
- candidate selection is ambiguous

### 10.3 Parseability check
Confirm the file can be parsed as CSV without mutating duplicate headers.

Implementation requirement:
- parser must preserve duplicate column names exactly as ordered

### 10.4 File identity check
Phase 0 should verify the file is the intended MSTR 4H export artifact.

Recommended rule set:
- raw filename contains `MSTR`
- raw filename contains the TradingView 4H interval marker equivalent to `240`
- file is created or copied within the active run window
- file path corresponds to the intake location or staging copy of that intake artifact
- the access layer recorded a successful export event for this run before the file appeared

### 10.5 Schema validation
Validation must confirm:
- exact column count
- exact column order
- exact column labels
- exact duplicate preservation

No normalization, deduplication, or header cleanup is allowed.

### 10.6 Canonical header fingerprint
Implementation:
- take the ordered header row exactly as exported
- serialize as comma-joined UTF-8 string, no trailing newline
- compute **SHA-256** over that representation

Fingerprint rule:
- one canonical stored fingerprint for the approved MSTR 4H sample
- each run computes its own fingerprint
- mismatch = hard fail

**Canonical MSTR 4H fingerprint (113 columns):**
```text
sha256: c37c5b63111674f556e086c2f1ce2eb936362791350e4446360958e2ebc70a53
```

Derived from the exact ordered header of `BATS_MSTR, 240_57f94.csv`. This value is the schema contract. It must be stored in config, not hardcoded in the validator.

### 10.7 Historical depth validation
Validation must confirm:
- at least three years of history are present
- oldest and newest timestamps are recorded in the manifest

Open item:
- numeric row-count floor still to be calibrated with Cyler

### 10.8 Freshness validation
The system does not require real-time data.

**Two-gate freshness check:**

Gate 1, file age (mtime-based):
- file mtime must fall within the configured execution window
- a file from a prior run window is stale and must fail

Gate 2, data age (newest-row timestamp):
- computed as the maximum unix timestamp in the `time` column
- compared against a per-run-type floor

**Midday run** (11:30am CT / 12:30pm ET trigger):
- mtime window: 10:00–13:00 CT today
- newest row floor: market open of the **current or prior** trading session (≥ T-1 09:30 ET)
- rationale: 4H bars make same-day intraday rows unlikely before noon; prior-session close is valid

**Close run** (3:00pm CT / 4:00pm ET trigger):
- mtime window: 14:30–18:00 CT today
- newest row floor: today at 13:30 ET (ensures at least one same-day 4H bar is present)
- rationale: first full same-day 4H bar closes at 13:30 ET; anything older is a stale re-use

**Stale leftover rule:**
- if a file passes schema/depth but its mtime predates the current run window, reject it, do not silently republish an earlier export

These tolerances are defaults. The implementation may tighten the mtime window during calibration, but should not widen it.

### 10.9 Production publish validation
Production publish adds extra required checks:
- production mode explicitly requested
- shadow acceptance threshold already met
- backup write succeeds before replacement
- live target path is reachable
- rollback pointer is recorded in manifest

---

## 11. Manifest Design

### 11.1 Required manifest fields
Recommended manifest schema:

```yaml
run_id:
run_type:                        # midday | close | manual-test
mode:                            # dry-run | shadow | production
started_at:
completed_at:
source_download_filename:
source_download_path:
staged_raw_path:
shadow_published_path:
published_filename:              # MSTR_4H.csv
published_repo_path:
production_backup_path:
schema_fingerprint:
expected_schema_fingerprint:
row_count:
oldest_timestamp:
newest_timestamp:
validation_status:
validation_errors:
shadow_status:
production_publish_status:
commit_sha:
push_status:
downstream_smoke_test_status:
rollback_ready:
report_status:
```

### 11.2 Manifest format
Recommended format:
- **JSON** for machine processing
- optional human-readable summary log alongside it

### 11.3 Manifest retention
Keep manifests for all runs, including failures and dry-runs.

---

## 12. Logging Design

### 12.1 Local logs
Each run should produce:
- a machine-readable manifest
- a human-readable validation log

### 12.2 Logging content
Minimum logging content:
- run id
- run type
- mode
- selected file
- validation checks executed
- pass/fail result per check
- shadow publish status
- final production publish status
- commit SHA if published
- smoke-test result
- rollback target if production was touched

### 12.3 Reporting destinations
Phase 0 reporting destinations:
- local log on Mac Studio
- Discord

### 12.4 Discord reporting recommendation
Recommended message format:
- run type
- mode
- status
- published filename or shadow artifact name
- commit SHA or “not published”
- failure reason if applicable

---

## 13. Publish Design

### 13.1 Shadow publish action
Shadow publish is a **copy** action from validated staging artifact into a non-production destination.

### 13.2 Shadow publish target
Recommended:
- `~/tradingview-sync/shadow-publish/MSTR_4H.shadow.csv`

### 13.3 Production publish action
Production publish is a **copy** action from validated staging artifact into the repo root.

### 13.4 Production publish target
- `<grok_repo>/MSTR_4H.csv`

### 13.5 Git flow
Recommended Phase 0 production git sequence:
1. ensure repo is available
2. back up current `MSTR_4H.csv` if it exists
3. copy validated file into repo root
4. `git add MSTR_4H.csv`
5. commit with deterministic message
6. push

### 13.6 Commit message recommendation
Example:

```text
data: publish MSTR_4H.csv for 2026-04-26 midday run
```

### 13.7 Publish safety
Fail before production commit if:
- validation failed
- repo path unavailable
- output copy failed
- backup failed
- smoke-test gate failed

---

## 14. Downstream Smoke Test Design

### 14.1 Purpose
The smoke test confirms that the existing MSTR Suite reporting flow can still consume the published file.

### 14.2 Minimum requirement
The smoke test should verify that:
- the downstream process loads the published CSV successfully
- no schema compatibility failure occurs
- expected report-generation entry point still runs

### 14.3 Preliminary implementation approach
The exact smoke-test command is still open.

Recommended Phase 0 pattern:
- use the lightest existing downstream invocation that proves compatibility
- run it first against the shadow artifact during rollout
- treat any exception, parse failure, or missing-field failure as a hard fail

---

## 15. Failure and Recovery Model

### 15.1 Hard-fail conditions
Hard fail if any of the following occurs:
- TradingView session unavailable or unauthenticated
- canonical chart cannot be opened
- chart timeframe is not **4H**
- export action fails
- no candidate file found
- ambiguous candidate file selection
- CSV parse failure
- schema mismatch
- fingerprint mismatch
- insufficient historical depth
- stale file detected
- shadow publish failure
- backup failure
- production publish copy failure
- git commit or push failure
- downstream smoke test failure

### 15.2 Retry model
For automated runs:
- retry once on access/download failure if safe
- do not retry publish after partial production mutation without human review
- if retry fails, report and stop

### 15.3 Recovery support
Failed runs should leave behind:
- raw staged artifact
- validation log
- manifest
- failure reason
- backup artifact if production had been touched

This is enough for manual rerun or diagnosis.

### 15.4 Rollback model
If production mode has replaced the live artifact and a post-publish failure is detected, the system should support immediate rollback using the most recent backup.

Rollback should be simple, explicit, and documented.

---

## 16. Risk Assessment and Mitigation Plan

### 16.1 Primary risks
The major risks are:

1. **Silent bad-data publish**
   - wrong chart
   - wrong timeframe
   - stale file
   - schema drift
   - TradingView UI drift leading to unexpected output

2. **Collision with current production engines**
   - overwriting a live production file too early
   - changing timing assumptions
   - causing downstream jobs to consume new automation output before trust is established

3. **Session and browser fragility**
   - authentication expiry
   - unexpected modal dialogs
   - saved-chart drift
   - downloads landing in unexpected paths

4. **Operational noise**
   - false alarms
   - duplicate runs
   - confusing failure states

### 16.2 Mitigation strategy
The required mitigation strategy is:
- default to dry-run or shadow mode
- separate non-production and production destinations
- require repeated successful shadow runs before live cutover
- back up the live artifact before replacement
- fail closed on all access, validation, and smoke-test errors
- keep rollback fast and explicit
- keep the manual process available during rollout

### 16.3 Shadow acceptance threshold
Recommended threshold before enabling production mode:
- at least **5 successful shadow runs**
- covering both **midday** and **close** windows
- no schema mismatches
- no freshness misses
- no smoke-test failures
- no unexplained divergence from expected output

This threshold can be raised if the team wants even tighter risk control.

### 16.4 Production cutover rule
Production mode should not be enabled merely because the code exists.

Production mode should be enabled only after:
- shadow threshold is met
- manual review confirms output quality
- rollback path is tested
- team approves production cutover explicitly

### 16.5 Manual fallback rule
If production mode is unstable, the team must be able to revert immediately to the existing manual workflow.

The new automation must not remove or block that fallback path.

---

## 17. Proposed Implementation Shape

### 17.1 Primary runner
A single local runner script is sufficient for Phase 0.

Responsibilities:
- identify run type
- identify execution mode
- attach to or launch TradingView browser session
- open canonical chart
- verify **4H** timeframe state
- trigger export and detect fresh download
- select candidate file
- orchestrate validation
- write manifest/logs
- shadow publish or production publish
- invoke backup/rollback helpers
- invoke smoke test
- report result

### 17.2 Access and validator modules
The acquisition layer and validation layer should be implemented as explicit independent checks, not one opaque pass/fail block.

Recommended access checks:
- `check_session()`
- `open_chart()`
- `check_symbol()`
- `check_timeframe_4h()`
- `trigger_export()`
- `wait_for_download()`

Recommended validation checks:
- `check_presence()`
- `check_identity()`
- `check_schema()`
- `check_fingerprint()`
- `check_history_depth()`
- `check_freshness()`
- `check_publish_ready()`
- `check_shadow_eligibility()`
- `check_production_eligibility()`

### 17.3 Config inputs
Recommended configuration values:
- repo path
- intake path
- staging path
- manifest path
- log path
- shadow publish path
- backup path
- TradingView chart URL or saved-chart locator
- dedicated browser profile/session locator
- expected symbol
- enforced timeframe (`4H`)
- expected published filename
- expected shadow filename
- expected schema fingerprint
- freshness window definitions
- smoke-test command
- Discord reporting target
- shadow acceptance threshold

---

## 18. Implementation Plan

### 18.1 Phase A, non-invasive setup
Build only the following first:
- dedicated TradingView browser profile
- intake/staging/log/manifest directories
- config file
- fingerprint storage
- runner skeleton

Constraint:
- no production publish support enabled yet

### 18.2 Phase B, access-layer proof
Implement and test:
- session attach/launch
- chart open
- symbol verification
- **4H** verification
- export trigger
- download detection

Deliverable:
- reliable acquisition of a fresh raw export into intake

Constraint:
- dry-run only

### 18.3 Phase C, validator proof
Implement and test:
- CSV parsing preserving duplicate headers
- fingerprint check
- freshness checks
- historical depth checks
- manifest writing
- structured failure reporting

Deliverable:
- deterministic validation outcome

Constraint:
- dry-run only

### 18.4 Phase D, shadow-mode rollout
Implement and test:
- shadow publish path
- smoke-test invocation against shadow output
- Discord and local logging
- repeated scheduled runs in shadow mode

Success criteria:
- meet the shadow acceptance threshold
- observe no production interference

Constraint:
- production publish disabled

### 18.5 Phase E, rollback and backup controls
Implement and test:
- live artifact backup
- rollback helper
- production eligibility gate
- manifest rollback recording

Deliverable:
- proven recovery path before any live cutover

Constraint:
- still no production cutover until explicitly approved

### 18.6 Phase F, guarded production cutover
Enable production mode only after:
- shadow threshold satisfied
- rollback tested successfully
- smoke-test command confirmed
- team approves production use

First production rollout should be:
- one supervised run
- backup verified beforehand
- manual fallback standing by

### 18.7 Phase G, post-cutover observation
After first live cutover:
- monitor initial production runs closely
- keep manual fallback available
- keep rollback ready
- do not expand scope until stability is demonstrated

---

## 19. Operational Procedure for Phase 0

### 19.1 Midday or close run
1. invoke the runner with intended run type and mode
2. runner opens the canonical TradingView chart on Mac Studio
3. runner verifies symbol and **4H** state
4. runner triggers CSV download from TradingView
5. runner validates the resulting artifact
6. if in shadow mode, publish only to shadow destination and run smoke test
7. if in production mode, back up current live artifact before any replacement
8. inspect success/failure output
9. confirm GitHub publish only if production mode was allowed and passed all gates

### 19.2 Manual test run
For testing, operator may use `manual-test` mode.

This should still:
- use the same TradingView access path when possible
- validate strictly
- write manifests/logs
- avoid weakening production checks
- default to dry-run unless specifically overridden

---

## 20. Open Decisions

These do not block implementation start, but must be resolved before Phase 0 acceptance testing is finalized.

### 20.1 Row-count floor
Status: **open — pending Cyler calibration**

Three-year window rule is locked. Cyler to confirm whether a hard numeric row-count minimum should be enforced in addition.

### 20.2 Freshness tolerances
Status: **resolved — defaults locked in Section 10.8**

Defaults may be tightened during implementation calibration but not widened.

### 20.3 Smoke-test command
Status: **open — pending identification of the downstream MSTR Suite entry point**

The smoke test should use the lightest existing invocation that proves the published CSV loads and passes schema checks in the downstream reporting flow.

### 20.4 Discord reporting destination
Status: **open — pending routing decision**

Recommended destination: MSTR alerts endpoint or equivalent ops channel.

### 20.5 TradingView session maintenance
Status: **open — pending operational decision**

Need to decide how the dedicated browser session is maintained on the Mac Studio and how re-authentication is handled when TradingView expires the session.

### 20.6 Browser control method
Status: **open — pending implementation choice**

Need to decide the concrete browser automation/control method used to drive TradingView export on the Mac Studio.

### 20.7 Shadow acceptance threshold
Status: **proposed — pending team confirmation**

Current recommendation: minimum 5 successful shadow runs across both run windows before production cutover.

---

## 21. Recommendation

Proceed with implementation of Phase 0 using this revised design and implementation plan.

The design is intentionally narrow but now complete enough at the system boundary and much safer for existing production:
- browser-driven TradingView export acquisition
- strict **4H** enforcement
- strict validator
- shadow-first rollout
- deterministic publish artifact
- explicit manifest and logs
- backup and rollback controls
- fail-closed behavior
- smoke-tested downstream compatibility

That is the right foundation before broader suite expansion.

---

## Bottom Line

This revised design is meant to do more than automate a download.

It is meant to automate the MSTR 4H TradingView export path **without hindering the current engines and production environment**.

The main way it does that is by refusing to treat production publish as the first success condition.

Instead, it requires:
- dry-run capability
- shadow-mode proof
- explicit production gating
- backup before replacement
- rollback readiness
- manual fallback during rollout

That is the safest way to move forward while still making real progress.
