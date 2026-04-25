# P-MCP-CSV Phase 0 Preliminary Design — MSTR 4H Golden Path
**Project:** P-MCP-CSV  
**Date:** 2026-04-25  
**Author:** Archie  
**Status:** Ready for implementation

---

## Executive Summary

This document translates the approved Phase 0 standardization spec into a preliminary design for implementation.

The design goal is straightforward:

- standardize one deterministic TradingView export workflow for **MSTR 4H** on the **Mac Studio**
- validate it strictly
- publish a normalized repo copy as `MSTR_4H.csv`
- fail closed on any invalid or incomplete run
- preserve the current downstream MSTR Suite workflow

This is intentionally **not** a full automation design for the entire export suite.

It is a controlled Phase 0 design for one golden path that can later be expanded safely.

---

## 1. Design Objective

Implement a local Phase 0 workflow on the Mac Studio that:

1. receives a raw TradingView CSV download for the canonical MSTR 4H chart
2. validates file identity, schema, historical depth, and freshness
3. writes a manifest and validation log
4. copies the validated file into the `Grok` repo root as `MSTR_4H.csv`
5. commits and pushes the result
6. confirms downstream compatibility via smoke test
7. reports success or failure to local logs and Discord

---

## 2. Design Principles

### 2.1 Contract before automation
The validator and file-handling contract are primary.

Automation must conform to the contract, not redefine it.

### 2.2 Fail closed
If the export is missing, stale, malformed, or incompatible, the run must stop before publication.

### 2.3 Preserve raw artifacts
The original TradingView download remains intact for traceability and recovery.

### 2.4 Normalize only at publish boundary
The raw file may vary in suffix, but the published repo copy must always be:
- `MSTR_4H.csv`

### 2.5 Downstream compatibility over elegance
The system should preserve the current downstream model, including duplicate columns and TradingView-specific quirks.

---

## 3. Scope

### 3.1 In scope
- one-symbol, one-timeframe Phase 0 flow for **MSTR 4H**
- Mac Studio local intake, staging, validation, publish, and reporting flow
- manual export initiation from TradingView
- manifest/logging support
- GitHub publish support
- downstream smoke-test gate

### 3.2 Out of scope
- browser automation of TradingView export
- support for the full MSTR Suite export set
- redesign of downstream analytics
- replacement market data source
- database-backed orchestration
- weekly timeframe support

---

## 4. Proposed System Boundary

### 4.1 Human-operated boundary
Phase 0 assumes the operator performs the TradingView download manually from the canonical saved chart on the Mac Studio.

### 4.2 Machine-operated boundary
Once the raw file lands in the intake location, the system handles:
- discovery
- validation
- manifest creation
- staging
- publish copy
- commit/push
- smoke test
- reporting

### 4.3 Automation boundary recommendation
The right boundary for later automation remains:
- **one chart = one export contract = one validation path**

That keeps drift detection and failure diagnosis tractable.

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
1. operator downloads the canonical MSTR 4H CSV from TradingView
2. raw file lands in `~/Downloads/tradingview-intake/`
3. runner identifies the candidate file for the requested run type
4. runner copies raw file into run staging
5. validator checks identity, header contract, historical depth, freshness, and file integrity
6. validator computes schema fingerprint and writes validation result
7. runner writes manifest
8. if validation passes, runner copies file into repo root as `MSTR_4H.csv`
9. runner commits and pushes
10. runner executes downstream smoke test
11. runner reports success or failure

### 6.3 Publish gate
No publish step occurs unless all validation gates pass.

### 6.4 Smoke-test gate
A run is not fully successful until the downstream smoke test passes.

---

## 7. Data Contract Handling

### 7.1 Canonical input contract
The canonical source object is:
- `BATS_MSTR, 240_57f94.csv`

It defines:
- symbol/timeframe intent
- expected header list
- duplicate header behavior
- minimum historical window

### 7.2 Canonical published artifact
The repo-facing published artifact must always be:
- `MSTR_4H.csv`

### 7.3 Raw file retention
The original TradingView filename must be retained in intake/staging and referenced in the manifest.

---

## 8. Validation Design

### 8.1 Validation stages
Validation should run in this order:

1. file presence check
2. parseability check
3. file identity check
4. schema/header check
5. historical depth check
6. freshness check
7. publish-precondition check
8. downstream smoke-test gate after publish

### 8.2 File presence check
Confirm exactly one intended candidate file has been selected for the run.

Fail if:
- no candidate file is found
- candidate selection is ambiguous

### 8.3 Parseability check
Confirm the file can be parsed as CSV without mutating duplicate headers.

Implementation requirement:
- parser must preserve duplicate column names exactly as ordered

### 8.4 File identity check
Phase 0 should verify the file is the intended MSTR 4H export artifact.

Recommended rule set:
- raw filename contains `MSTR`
- raw filename contains the TradingView 4H interval marker equivalent to `240`
- file is created or copied within the active run window
- file path corresponds to the intake location or staging copy of that intake artifact

### 8.5 Schema validation
Validation must confirm:
- exact column count
- exact column order
- exact column labels
- exact duplicate preservation

No normalization, deduplication, or header cleanup is allowed.

### 8.6 Canonical header fingerprint
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

### 8.7 Historical depth validation
Validation must confirm:
- at least three years of history are present
- oldest and newest timestamps are recorded in the manifest

Open item:
- numeric row-count floor still to be calibrated with Cyler

### 8.8 Freshness validation
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

## 9. Manifest Design

### 9.1 Required manifest fields
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

### 9.2 Manifest format
Recommended format:
- YAML or JSON

My recommendation:
- **JSON** for machine processing
- optional human-readable summary log alongside it

### 9.3 Manifest retention
Keep manifests for all runs, including failures.

---

## 10. Logging Design

### 10.1 Local logs
Each run should produce:
- a machine-readable manifest
- a human-readable validation log

### 10.2 Logging content
Minimum logging content:
- run id
- run type
- selected file
- validation checks executed
- pass/fail result per check
- final publish status
- commit SHA if published
- smoke-test result

### 10.3 Reporting destinations
Phase 0 reporting destinations:
- local log on Mac Studio
- Discord

### 10.4 Discord reporting recommendation
Recommended message format:
- run type
- status
- published filename
- commit SHA or “not published”
- failure reason if applicable

---

## 11. Publish Design

### 11.1 Publish action
Publish is a **copy** action from validated staging artifact into the repo root.

### 11.2 Publish target
- `<grok_repo>/MSTR_4H.csv`

### 11.3 Git flow
Recommended Phase 0 git sequence:
1. ensure repo is available
2. copy validated file into repo root
3. `git add MSTR_4H.csv`
4. commit with deterministic message
5. push

### 11.4 Commit message recommendation
Example:

```text
data: publish MSTR_4H.csv for 2026-04-25 midday run
```

### 11.5 Publish safety
Fail before commit if:
- validation failed
- repo path unavailable
- output copy failed

---

## 12. Downstream Smoke Test Design

### 12.1 Purpose
The smoke test confirms that the existing MSTR Suite reporting flow can still consume the published file.

### 12.2 Minimum requirement
The smoke test should verify that:
- the downstream process loads the published CSV successfully
- no schema compatibility failure occurs
- expected report-generation entry point still runs

### 12.3 Preliminary implementation approach
The exact smoke-test command is still open.

Recommended Phase 0 pattern:
- use the lightest existing downstream invocation that proves compatibility
- treat any exception, parse failure, or missing-field failure as a hard fail

---

## 13. Failure and Recovery Model

### 13.1 Hard-fail conditions
Hard fail if any of the following occurs:
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

### 13.2 Retry model
For automated runs:
- retry once
- if retry fails, report and stop

### 13.3 Recovery support
Failed runs should leave behind:
- raw staged artifact
- validation log
- manifest
- failure reason

This is enough for manual rerun or diagnosis.

---

## 14. Proposed Implementation Shape

### 14.1 Primary runner
A single local runner script is sufficient for Phase 0.

Responsibilities:
- identify run type
- select candidate file
- orchestrate validation
- write manifest/logs
- publish file
- invoke git steps
- invoke smoke test
- report result

### 14.2 Validator module
Validation should be implemented as explicit independent checks, not one opaque pass/fail block.

Recommended checks:
- `check_presence()`
- `check_identity()`
- `check_schema()`
- `check_fingerprint()`
- `check_history_depth()`
- `check_freshness()`
- `check_publish_ready()`

### 14.3 Config inputs
Recommended configuration values:
- repo path
- intake path
- staging path
- manifest path
- log path
- expected published filename
- expected schema fingerprint
- freshness window definitions
- smoke-test command
- Discord reporting target

---

## 15. Operational Procedure for Phase 0

### 15.1 Midday or close run
1. open canonical MSTR 4H chart on Mac Studio
2. confirm chart state
3. download CSV from TradingView
4. run Phase 0 runner with intended run type
5. inspect success/failure output
6. confirm GitHub publish if successful

### 15.2 Manual test run
For testing, operator may use `manual-test` mode.

This should still:
- validate strictly
- write manifests/logs
- avoid weakening production checks

---

## 16. Open Decisions

These do not block implementation start, but must be resolved before Phase 0 acceptance testing is finalized.

### 16.1 Row-count floor
Status: **open — pending Cyler calibration**

Three-year window rule is locked. Cyler to confirm whether a hard numeric row-count minimum (e.g., 2,000 rows) should be enforced in addition. Working assumption: no hard floor until Cyler specifies one.

### 16.2 Freshness tolerances
Status: **resolved — defaults locked in Section 8.8**

Defaults may be tightened during implementation calibration but not widened.

### 16.3 Smoke-test command
Status: **open — pending identification of the downstream MSTR Suite entry point**

The smoke test should use the lightest existing invocation that proves the published CSV loads and passes schema checks in the downstream reporting flow. Exact command to be confirmed during implementation.

### 16.4 Discord reporting destination
Status: **open — pending routing decision**

Recommended destination: MSTR `alerts` webhook. Confirm with Gavin before implementation.

---

## 17. Recommendation

Proceed with implementation of Phase 0 using this design.

The design is intentionally modest and correct:
- manual TradingView export
- strict validator
- deterministic publish artifact
- explicit manifest and logs
- fail-closed behavior
- smoke-tested downstream compatibility

That is the right foundation before broader suite expansion or browser automation.

---

## 18. Next Step

The next document should be an **implementation plan** that converts this preliminary design into:
- concrete file locations
- exact fingerprint algorithm specification
- exact freshness windows
- exact smoke-test command
- script/module breakdown
- operator runbook

---

## Bottom Line

Yes, the revised spec was sufficient.

This preliminary design gives the team a workable Phase 0 architecture for standardizing the **MSTR 4H** TradingView export on the **Mac Studio** without disturbing the current downstream reporting model.

It is ready to use as the basis for the next implementation-planning step.
