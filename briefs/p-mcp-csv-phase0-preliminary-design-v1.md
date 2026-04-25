# P-MCP-CSV Phase 0 Preliminary Design — MSTR 4H Golden Path
**Project:** P-MCP-CSV  
**Date:** 2026-04-25  
**Author:** Archie  
**Status:** Revised preliminary design with TradingView access automation

---

## Executive Summary

This document translates the approved Phase 0 standardization spec into a preliminary design for implementation.

The design goal is straightforward:

- automate acquisition of one deterministic TradingView export workflow for **MSTR 4H** on the **Mac Studio**
- enforce **4H** as a hard chart and indicator calibration rule
- validate the acquired export strictly
- publish a normalized repo copy as `MSTR_4H.csv`
- fail closed on any invalid or incomplete run
- preserve the current downstream MSTR Suite workflow

This is still intentionally limited to one golden path, but it now includes the missing acquisition layer: how the system gets the TradingView export in the first place.

---

## 1. Design Objective

Implement a local Phase 0 workflow on the Mac Studio that:

1. accesses TradingView through a persistent authenticated browser session
2. opens the canonical MSTR 4H chart
3. verifies **4H** timeframe state before export
4. triggers the TradingView CSV download
5. validates file identity, schema, historical depth, and freshness
6. writes a manifest and validation log
7. copies the validated file into the `Grok` repo root as `MSTR_4H.csv`
8. commits and pushes the result
9. confirms downstream compatibility via smoke test
10. reports success or failure to local logs and Discord

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

---

## 3. Scope

### 3.1 In scope
- one-symbol, one-timeframe Phase 0 flow for **MSTR 4H**
- Mac Studio local browser-based TradingView access and export automation
- Mac Studio local intake, staging, validation, publish, and reporting flow
- manifest/logging support
- GitHub publish support
- downstream smoke-test gate

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
- publish copy
- commit/push
- smoke test
- reporting

### 4.3 Boundary recommendation
The right boundary remains:
- **one chart = one export contract = one validation path**

The difference is that the export action itself is now inside the automated system boundary.

### 4.4 Why this boundary is correct
This preserves TradingView as the source of truth while still allowing the system to acquire the data directly.

It also keeps the calibrated chart state, including **4H**, inside the controlled contract instead of treating it as a human prerequisite.

---

## 5. Proposed Local Architecture

### 5.1 Directories
Recommended paths on the Mac Studio:

- `~/Downloads/tradingview-intake/`
  - raw TradingView downloads
- `~/tradingview-sync/staging/`
  - per-run staging work
- `~/tradingview-sync/logs/`
  - validation logs and run summaries
- `~/tradingview-sync/manifests/`
  - machine-readable run manifests
- local `Grok` repo working copy
  - validated publish target

### 5.2 Staging layout
Recommended per-run structure:

```text
~/tradingview-sync/staging/
  <run_id>/
    raw/
    validation/
    publish/
```

Example:

```text
~/tradingview-sync/staging/20260425T113000-ct-midday/
```

### 5.3 Why this layout
This provides:
- run isolation
- reproducibility
- easier debugging
- durable audit trail
- clean support for failed-run inspection

---

## 6. Proposed Runtime Flow

### 6.1 Run types
Supported Phase 0 run types:
- `midday`
- `close`
- `manual-test`

### 6.2 Sequence
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
11. if validation passes, runner copies file into repo root as `MSTR_4H.csv`
12. runner commits and pushes
13. runner executes downstream smoke test
14. runner reports success or failure

### 6.3 Acquisition gate
No validation begins until the system has confirmed that a fresh download was successfully triggered and observed.

### 6.4 Publish gate
No publish step occurs unless all access and validation gates pass.

### 6.5 Smoke-test gate
A run is not fully successful until the downstream smoke test passes.

---

## 7. TradingView Access Design

### 7.1 Access model
The preferred acquisition path is **browser-driven TradingView export automation** on the Mac Studio.

This means the system should use a persistent browser session that is already authenticated to TradingView and capable of opening the canonical saved chart.

### 7.2 Why browser-driven export is the right Phase 0 path
This is the right initial path because it:
- preserves TradingView as source of truth
- preserves the exact chart-state contract
- preserves indicator fidelity
- avoids premature reconstruction of TradingView outputs from alternative data sources

### 7.3 Session model
Recommended model:
- dedicated browser profile for TradingView automation
- persistent authenticated session maintained on the Mac Studio
- fail closed if the session is logged out or requires unexpected human re-authentication

### 7.4 Chart navigation model
The system should navigate to one canonical saved chart for MSTR.

That chart must be treated as a configuration object, not just a visual destination.

### 7.5 4H timeframe standardization policy
**4H is mandatory.**

The automation must verify that the active TradingView chart is set to **4H** before any export action is attempted.

A chart discovered in any other timeframe must fail immediately.

This rule exists because the MSTR indicators are tuned and calibrated to 4H, and future indicators are expected to follow the same standard unless explicitly overridden.

### 7.6 Export trigger model
The automation must invoke the normal TradingView CSV export path, not a substitute data retrieval method, during this phase.

### 7.7 Download detection model
After export is triggered, the system should watch the intake directory for the new file associated with the current run.

Failure to observe a fresh file inside the configured wait window is a hard failure.

### 7.8 Access-layer failure cases
Hard fail if:
- TradingView session is not authenticated
- canonical chart cannot be opened
- symbol does not match the target chart
- timeframe is not **4H**
- export action cannot be triggered
- download artifact does not appear in the intake path
- TradingView UI drift prevents reliable export

---

## 8. Data Contract Handling

### 8.1 Canonical input contract
The canonical source object is:
- `BATS_MSTR, 240_57f94.csv`

It defines:
- symbol/timeframe intent
- expected header list
- duplicate header behavior
- minimum historical window

### 8.2 Canonical published artifact
The repo-facing published artifact must always be:
- `MSTR_4H.csv`

### 8.3 Raw file retention
The original TradingView filename must be retained in intake/staging and referenced in the manifest.

---

## 9. Validation Design

### 9.1 Validation stages
Validation should run in this order:

1. file presence check
2. parseability check
3. file identity check
4. schema/header check
5. historical depth check
6. freshness check
7. publish-precondition check
8. downstream smoke-test gate after publish

### 9.2 File presence check
Confirm exactly one intended candidate file has been selected for the run.

Fail if:
- no candidate file is found
- candidate selection is ambiguous

### 9.3 Parseability check
Confirm the file can be parsed as CSV without mutating duplicate headers.

Implementation requirement:
- parser must preserve duplicate column names exactly as ordered

### 9.4 File identity check
Phase 0 should verify the file is the intended MSTR 4H export artifact.

Recommended rule set:
- raw filename contains `MSTR`
- raw filename contains the TradingView 4H interval marker equivalent to `240`
- file is created or copied within the active run window
- file path corresponds to the intake location or staging copy of that intake artifact
- the access layer recorded a successful export event for this run before the file appeared

### 9.5 Schema validation
Validation must confirm:
- exact column count
- exact column order
- exact column labels
- exact duplicate preservation

No normalization, deduplication, or header cleanup is allowed.

### 9.6 Canonical header fingerprint
Implementation:
- take the ordered header row exactly as exported
- serialize as comma-joined UTF-8 string, no trailing newline
- compute **SHA-256** over that representation

Fingerprint rule:
- one canonical stored fingerprint for the approved MSTR 4H sample
- each run computes its own fingerprint
- mismatch = hard fail

**Canonical MSTR 4H fingerprint (113 columns):**
```
sha256: c37c5b63111674f556e086c2f1ce2eb936362791350e4446360958e2ebc70a53
```

Derived from the exact ordered header of `BATS_MSTR, 240_57f94.csv`. This value is the schema contract. It must be stored in config, not hardcoded in the validator.

### 9.7 Historical depth validation
Validation must confirm:
- at least three years of history are present
- oldest and newest timestamps are recorded in the manifest

Open item:
- numeric row-count floor still to be calibrated with Cyler

### 9.8 Freshness validation
The system does not require real-time data.

**Two-gate freshness check:**

Gate 1 — file age (mtime-based):
- file mtime must fall within the configured execution window
- a file from a prior run window is stale and must fail

Gate 2 — data age (newest-row timestamp):
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
- if a file passes schema/depth but its mtime predates the current run window, reject it — do not silently republish yesterday's export

These tolerances are defaults. The implementation may tighten the mtime window during calibration, but should not widen it.

---

## 10. Manifest Design

### 10.1 Required manifest fields
Recommended manifest schema:

```yaml
run_id:
run_type:                  # midday | close | manual-test
started_at:
completed_at:
source_download_filename:
source_download_path:
staged_raw_path:
published_filename:        # MSTR_4H.csv
published_repo_path:
schema_fingerprint:
expected_schema_fingerprint:
row_count:
oldest_timestamp:
newest_timestamp:
validation_status:
validation_errors:
commit_sha:
push_status:
downstream_smoke_test_status:
report_status:
```

### 10.2 Manifest format
Recommended format:
- YAML or JSON

My recommendation:
- **JSON** for machine processing
- optional human-readable summary log alongside it

### 10.3 Manifest retention
Keep manifests for all runs, including failures.

---

## 11. Logging Design

### 11.1 Local logs
Each run should produce:
- a machine-readable manifest
- a human-readable validation log

### 11.2 Logging content
Minimum logging content:
- run id
- run type
- selected file
- validation checks executed
- pass/fail result per check
- final publish status
- commit SHA if published
- smoke-test result

### 11.3 Reporting destinations
Phase 0 reporting destinations:
- local log on Mac Studio
- Discord

### 11.4 Discord reporting recommendation
Recommended message format:
- run type
- status
- published filename
- commit SHA or “not published”
- failure reason if applicable

---

## 12. Publish Design

### 12.1 Publish action
Publish is a **copy** action from validated staging artifact into the repo root.

### 12.2 Publish target
- `<grok_repo>/MSTR_4H.csv`

### 12.3 Git flow
Recommended Phase 0 git sequence:
1. ensure repo is available
2. copy validated file into repo root
3. `git add MSTR_4H.csv`
4. commit with deterministic message
5. push

### 12.4 Commit message recommendation
Example:

```text
data: publish MSTR_4H.csv for 2026-04-25 midday run
```

### 12.5 Publish safety
Fail before commit if:
- validation failed
- repo path unavailable
- output copy failed

---

## 13. Downstream Smoke Test Design

### 13.1 Purpose
The smoke test confirms that the existing MSTR Suite reporting flow can still consume the published file.

### 13.2 Minimum requirement
The smoke test should verify that:
- the downstream process loads the published CSV successfully
- no schema compatibility failure occurs
- expected report-generation entry point still runs

### 13.3 Preliminary implementation approach
The exact smoke-test command is still open.

Recommended Phase 0 pattern:
- use the lightest existing downstream invocation that proves compatibility
- treat any exception, parse failure, or missing-field failure as a hard fail

---

## 14. Failure and Recovery Model

### 14.1 Hard-fail conditions
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
- publish copy failure
- git commit or push failure
- downstream smoke test failure

### 14.2 Retry model
For automated runs:
- retry once
- if retry fails, report and stop

### 14.3 Recovery support
Failed runs should leave behind:
- raw staged artifact
- validation log
- manifest
- failure reason

This is enough for manual rerun or diagnosis.

---

## 15. Proposed Implementation Shape

### 15.1 Primary runner
A single local runner script is sufficient for Phase 0.

Responsibilities:
- identify run type
- attach to or launch TradingView browser session
- open canonical chart
- verify **4H** timeframe state
- trigger export and detect fresh download
- select candidate file
- orchestrate validation
- write manifest/logs
- publish file
- invoke git steps
- invoke smoke test
- report result

### 15.2 Access and validator modules
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

### 15.3 Config inputs
Recommended configuration values:
- repo path
- intake path
- staging path
- manifest path
- log path
- TradingView chart URL or saved-chart locator
- dedicated browser profile/session locator
- expected symbol
- enforced timeframe (`4H`)
- expected published filename
- expected schema fingerprint
- freshness window definitions
- smoke-test command
- Discord reporting target

---

## 16. Operational Procedure for Phase 0

### 16.1 Midday or close run
1. invoke the Phase 0 runner with intended run type
2. runner opens the canonical TradingView chart on Mac Studio
3. runner verifies symbol and **4H** state
4. runner triggers CSV download from TradingView
5. runner validates the resulting artifact
6. inspect success/failure output
7. confirm GitHub publish if successful

### 16.2 Manual test run
For testing, operator may use `manual-test` mode.

This should still:
- use the same TradingView access path when possible
- validate strictly
- write manifests/logs
- avoid weakening production checks

---

## 17. Open Decisions

These do not block implementation start, but must be resolved before Phase 0 acceptance testing is finalized.

### 17.1 Row-count floor
Status: **open — pending Cyler calibration**

Three-year window rule is locked. Cyler to confirm whether a hard numeric row-count minimum (e.g., 2,000 rows) should be enforced in addition. Working assumption: no hard floor until Cyler specifies one.

### 17.2 Freshness tolerances
Status: **resolved — defaults locked in Section 9.8**

Defaults may be tightened during implementation calibration but not widened.

### 17.3 Smoke-test command
Status: **open — pending identification of the downstream MSTR Suite entry point**

The smoke test should use the lightest existing invocation that proves the published CSV loads and passes schema checks in the downstream reporting flow. Exact command to be confirmed during implementation.

### 17.4 Discord reporting destination
Status: **open — pending routing decision**

Recommended destination: MSTR `alerts` webhook. Confirm with Gavin before implementation.

### 17.5 TradingView session maintenance
Status: **open — pending operational decision**

Need to decide how the dedicated browser session is maintained on the Mac Studio and how re-authentication is handled when TradingView expires the session.

### 17.6 Browser control method
Status: **open — pending implementation choice**

Need to decide the concrete browser automation/control method used to drive TradingView export on the Mac Studio.

---

## 18. Recommendation

Proceed with implementation of Phase 0 using this revised design.

The design is intentionally narrow but now complete enough at the system boundary:
- browser-driven TradingView export acquisition
- strict **4H** enforcement
- strict validator
- deterministic publish artifact
- explicit manifest and logs
- fail-closed behavior
- smoke-tested downstream compatibility

That is the right foundation before broader suite expansion.

---

## 19. Next Step

The next document should be an **implementation plan** that converts this preliminary design into:
- concrete browser/session control method
- concrete file locations
- exact fingerprint algorithm specification
- exact freshness windows
- exact smoke-test command
- script/module breakdown
- operator runbook

---

## Bottom Line

Yes, the revised spec was sufficient, but only after clarifying that the system itself must acquire the TradingView export.

This revised preliminary design gives the team a workable Phase 0 architecture for:
- directly accessing TradingView on the **Mac Studio**
- enforcing **4H** as a hard chart-state rule
- acquiring the export automatically
- validating and publishing it without disturbing the current downstream reporting model

It is now ready to use as the basis for the next implementation-planning step.
