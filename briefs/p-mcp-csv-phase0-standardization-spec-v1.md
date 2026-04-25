# P-MCP-CSV Phase 0 Standardization Spec — MSTR 4H Golden Path
**Project:** P-MCP-CSV  
**Date:** 2026-04-25  
**Author:** Cyler (CIO), revised with Archie review  
**Status:** Draft revised after Archie review

---

## Executive Summary

P-MCP-CSV should not begin as a broad automation project.

It should begin as a **standardization project** whose job is to make the existing TradingView export workflow reproducible enough that later automation is safe.

The immediate target is a single **golden-path export contract** for **MSTR 4H** using the canonical TradingView sample:

- `BATS_MSTR, 240_57f94.csv`

Phase 0 is successful only if:
1. the export workflow is standardized on the **Mac mini**, and
2. one end-to-end **manual golden-path run** is proven for MSTR 4H using that standard.

This project deliberately preserves the current downstream analysis model. The goal is to eliminate manual CSV handoff over time, not redesign the MSTR Suite workflow during Phase 0.

The revised Phase 0 contract now also locks in:
- a **normalized published filename** for the repo copy
- a **canonical header fingerprint** for exact schema validation
- a **run manifest** for traceability and recovery
- explicit **mid-day** and **close-of-day** freshness windows
- explicit acceptance criteria for validation, publish, and downstream smoke testing

---

## 1. Objective

Create a stable, repeatable, fail-closed TradingView export workflow on the **Mac mini** that can later be automated without changing the downstream MSTR Suite analysis process.

### Immediate objective
Standardize one canonical export path for **MSTR 4H**.

### Broader project intent
Once the golden path is proven, extend the same standard to the full MSTR Suite export set and then automate the export, ingestion, and publish steps.

---

## 2. Core Constraints Locked in Conversation

### 2.1 Source of truth
TradingView remains the source of truth for:
- price data
- indicator outputs
- CSV structure used by current downstream analysis

### 2.2 Workflow boundary
The current downstream process should remain unchanged for now.

Phase 0 is not a redesign of analysis logic. It is a standardization step that makes later automation possible.

### 2.3 Host
The canonical automation host is the **Mac mini** that already hosts the rest of the infrastructure.

### 2.4 Export model
The CSVs come from **normal TradingView downloads**.

This project is not trying to replace those exports with a separate market-data source in Phase 0.

### 2.5 Failure policy
The system must be **fail-closed**.

If one required export fails or is missing:
- the whole run is blocked
- no partial publication occurs
- no downstream reporting should proceed on incomplete data

### 2.6 Trigger model
The long-term target is:
- scheduled runs at **11:30am CT** and **3:00pm CT**
- on-demand reruns for testing and production use

### 2.7 Freshness target
The business requirement is **not real-time data**.

The required freshness target is limited to:
- a valid **mid-day** export for the **11:30am CT** workflow, and
- a valid **close-of-day** export for the **3:00pm CT** workflow.

---

## 3. Why Phase 0 Exists

At the moment, the process is still too variable for safe unattended automation because:
- CSVs are currently downloaded manually from personal machines
- the Mac mini is not yet the standardized export origin
- the TradingView export routine is not yet defined as a stable contract
- filenames, paths, and recovery behavior need to be formalized

Phase 0 solves that problem by defining the export contract first.

**Guiding principle:**
> Define the contract before the mechanism.

---

## 4. Phase 0 Scope

### 4.1 In scope
- define the canonical MSTR 4H export contract
- standardize the export on the Mac mini
- define local intake, staging, and publish paths
- define validation and failure behavior
- define the canonical published filename
- define the canonical schema fingerprint rule
- define the run manifest structure
- manually prove one end-to-end MSTR 4H golden-path run

### 4.2 Out of scope
- full unattended export automation
- weekly timeframe support
- broader portfolio-wide ingestion beyond the MSTR Suite set
- database redesign
- analysis/reporting redesign
- replacement of TradingView export fidelity with external APIs

---

## 5. Phase 1 Export Set to Standardize After Golden Path

The broader MSTR Suite export set to be standardized after the golden-path MSTR 4H proof is:

- MSTR
- IBIT
- BTCUSD
- STRC
- STABLE.C.D
- MSTR/IBIT
- STRF/LQD
- STRD/HYG
- GOLD/BTCI
- STRF
- STRD
- MSTR/SPY

All are currently intended to standardize on **4H** for the first expansion phase.

---

## 6. Golden-Path Contract — MSTR 4H

### 6.1 Canonical sample
The canonical sample for the golden path is:
- `BATS_MSTR, 240_57f94.csv`

This file is the reference object for:
- raw export structure
- schema fidelity
- minimum historical depth
- downstream compatibility expectations
- canonical header fingerprint source material

### 6.2 Filename policy
Phase 0 will use **two filename forms**:

1. **Raw TradingView download name**
   - preserved unchanged in intake/staging for traceability
2. **Canonical published repo filename**
   - normalized to: `MSTR_4H.csv`

This removes dependency on TradingView suffix behavior while preserving the original download artifact.

### 6.3 Repo destination
The published file belongs in the repo **main/root folder**, consistent with current policy.

### 6.4 Publish method
The validated file must be **copied**, not moved, into the repo working tree root.

The raw TradingView file must remain available in intake/staging for audit and recovery.

### 6.5 Schema rule
The valid MSTR 4H export must preserve:
- **every column** present in the canonical sample
- **the exact canonical column order**
- **all duplicate column names exactly as exported**
- **at least three years of data**

### 6.6 Historical depth requirement
The canonical sample currently contains:
- **2,189 rows**
- first timestamp: `1638210600`
- last timestamp: `1776432600`

Phase 0 does not require the row count to remain frozen at 2,189.

Phase 0 does require:
- the same schema contract
- at least a three-year historical window
- a later row-count floor decision calibrated with Cyler before final automation acceptance language is locked

### 6.7 Acceptance rule for duplicates
The canonical sample contains repeated column labels, including examples such as:
- `LT Fast TL`
- `LT Slow TL`
- `Fast Trackline`
- `B Exhaust`
- `LOI`
- `Trim 25%`
- `Trim 50%`
- `Trim 75%`
- `F_net`
- `Primary (STRF/LQD)`
- `Credit (STRC x0.5)`
- `Friction (STABLE x0.4)`
- `Self (MSTR x0.3)`

That duplication is part of the real TradingView export contract and must not be “cleaned up” during Phase 0.

---

## 7. Canonical Schema Snapshot — MSTR 4H

The canonical sample contains **113 columns**.

### 7.1 Header snapshot
```text
time
open
high
low
close
LT Fast TL
LT Slow TL
BP Entry
MIXED Watch
LT Exit
Time Stop
IBIT Disabled
CT1 Cross
CT2 Cross
CT3 Cross
CT4 Distribution
IWM CT3 Warning
QQQ LT+ST Entry
QQQ LOI Caution
LT Fast TL
LT Slow TL
Fast Trackline
Slow Trackline
Green T
Yellow T
Red T
B Exhaust
Fast Trackline
B Exhaust
Fast Trackline
Yellow T
DOI Score (0-10)
LOI
VLT SRI Bias
T1 Trim 25%
T2 Trim 50%
T3 Trim 75%
VLT Peak
EXIT — LOI Rollover
CT4 Distribution
ATR
LOI
Acc
Deep Acc
Trim 25%
Trim 50%
Trim 75%
Acc Enter
Deep Enter
Acc Bounce
Deep Bounce
Trim 25%
Trim 50%
Trim 75%
Exit 100%
CT4 Dist
IWM Trim
VLT SRI Bias Histogram
ST SRI Bias Histogram
LT SRI Bias Histogram
F_net
Primary (STRF/LQD)
Credit (STRC x0.5)
Friction (STABLE x0.4)
Self (MSTR x0.3)
Multiplier
dF_net (ROC)
dF_net_5bar (momentum)
Into Bear
Into Bull
Into Strong Bear
Bounce Exhaustion
F_net
Primary (STRF/LQD)
Credit (STRC x0.5)
Friction (STABLE x0.4)
Self (MSTR x0.3)
Into Bear
Into Bull
Into Strong Bear
VLT Reversal Support
VLT Reversal Robust Fit
VLT Reversal Resistance
VLT Fast Trackline
VLT Slow Trackline
VLT Stage 4 to 1
VLT Stage 1 to 2
VLT Stage 2 to 3
VLT Stage 3 to 4
ST Reversal Support
ST Reversal Robust Fit
ST Reversal Resistance
ST Fast Trackline
ST Slow Trackline
ST Stage 4 to 1
ST Stage 1 to 2
ST Stage 2 to 3
ST Stage 3 to 4
LT Reversal Support
LT Reversal Robust Fit
LT Reversal Resistance
LT Fast Trackline
LT Slow Trackline
LT Stage 4 to 1
LT Stage 1 to 2
LT Stage 2 to 3
LT Stage 3 to 4
STH MVRV
MVRV SMA
%K
%D
MTF RSI
Short-Term Risk Score
```

### 7.2 Schema handling rule
For Phase 0, a valid export means:
- same column count
- same column order
- same column names, including duplicates
- no dropped fields
- no renamed fields
- canonical header fingerprint match

### 7.3 Canonical header fingerprint rule
The validation contract must include a **canonical header fingerprint** derived from the exact ordered header row of the canonical sample.

That fingerprint must be generated from:
- the full ordered header list
- original spelling
- original order
- duplicate labels preserved exactly

A Phase 0 export is schema-valid only if its derived header fingerprint matches the canonical fingerprint.

---

## 8. Recommended Local Path Architecture on Mac mini

The local path design should separate raw downloads from validated publishable files.

### 8.1 Recommended structure
- `~/Downloads/tradingview-intake/`
  - raw TradingView downloads land here
- `~/tradingview-sync/staging/`
  - validation and run-state processing happen here
- local working copy of the `Grok` repo
  - validated file is copied here before commit/push

### 8.2 Why this structure is recommended
This preserves:
- raw-file traceability
- simpler debugging
- clean failure handling
- lower risk of publishing bad files directly into the repo

### 8.3 Path rule
No file should enter the repo working tree until it passes validation.

### 8.4 Publish-name rule
The repo working tree should receive the normalized canonical file:
- `MSTR_4H.csv`

The raw TradingView download filename should remain preserved outside the repo publish destination.

---

## 9. Standardized Operator Workflow for the Golden Path

The manual Phase 0 golden-path run should follow this sequence:

1. open the saved **MSTR 4H** TradingView chart on the Mac mini
2. confirm the chart is the canonical export chart
3. perform the normal TradingView CSV download
4. ensure the raw file lands in the canonical intake location
5. validate filename identity, schema, history depth, and freshness window
6. write the run manifest and validation log
7. copy the validated file into the local repo working tree root as `MSTR_4H.csv`
8. commit and push the file to GitHub
9. confirm the published file is usable by the existing MSTR Suite reporting workflow

---

## 10. Required Chart-State Standardization

For MSTR 4H, the Mac mini must have one stable saved chart that preserves:
- the correct symbol
- the correct timeframe (**4H**)
- the required indicators
- the TradingView export path that produces the canonical schema

This chart is not merely a visual reference. It is the configuration object that defines the export contract.

If the chart state drifts, the exported file contract may drift with it.

One-chart-per-export is the intended automation boundary for Phase 0 and the next expansion phase.

---

## 11. Validation Rules

A valid Phase 0 golden-path MSTR 4H file must satisfy all of the following:

### 11.1 File identity validation
- raw file is traceable to the current MSTR 4H export run
- file is identifiable as the MSTR 4H export source artifact
- normalized published filename is `MSTR_4H.csv`

### 11.2 Schema validation
- header count matches the canonical sample
- header order matches the canonical sample
- duplicate columns remain intact
- canonical header fingerprint matches

### 11.3 Historical depth validation
- file contains at least three years of data
- row-count floor remains pending final calibration with Cyler

### 11.4 Freshness validation
A valid file does not need to be real-time.

A valid file must satisfy the intended run window:
- **mid-day run**: file is current enough for the scheduled **11:30am CT** workflow
- **close-of-day run**: file is current enough for the scheduled **3:00pm CT** workflow

Validation should confirm that:
- the newest row is appropriate for the intended run window, and
- the file is not a stale leftover from a prior run

### 11.5 Publish validation
- validated file is copied into the repo root successfully as `MSTR_4H.csv`
- commit succeeds
- push succeeds

### 11.6 Manifest and logging validation
- every run writes a local validation log
- every run writes a run manifest, whether the run passes or fails

### 11.7 Downstream compatibility validation
- existing MSTR Suite report generation still works from the published file
- downstream smoke test passes before the run is considered fully successful

---

## 12. Run Manifest Template

Each run should produce a manifest object with at least the following fields:

```yaml
run_id:
run_type:            # midday | close | manual-test
started_at:
completed_at:
source_download_filename:
source_download_path:
published_filename:  # MSTR_4H.csv
schema_fingerprint:
row_count:
oldest_timestamp:
newest_timestamp:
validation_status:
validation_errors:
commit_sha:
push_status:
downstream_smoke_test_status:
```

### 12.1 Manifest purpose
The run manifest exists to provide:
- traceability
- recovery support
- auditability
- easier debugging during Phase 0 and Phase 1

---

## 13. Failure Policy

### 13.1 Fail-closed rule
Any missing or invalid required file blocks the run.

No partial-success publication should occur.

### 13.2 Retry policy
For automated runs, the policy should be:
- **retry once**
- if still failing, alert and stop

### 13.3 Reporting policy
Success/failure should be reported to:
- **Discord**
- **local log** on the Mac mini

### 13.4 Recovery expectation
A failed run should leave enough evidence in the local log, manifest, and staging flow to support manual rerun and diagnosis.

---

## 14. Phase 0 Acceptance Test

Phase 0 is accepted when all of the following are true for the **MSTR 4H golden path**:

1. MSTR 4H is exported on the Mac mini from the canonical TradingView chart
2. the exported file preserves the canonical schema contract
3. the file passes the canonical header fingerprint check
4. the file contains at least three years of data
5. the file satisfies the intended freshness window for the run
6. the file lands in the local canonical path structure
7. the validated file is copied to the canonical GitHub repo location as `MSTR_4H.csv`
8. the run writes a local validation log and run manifest
9. downstream MSTR Suite reporting still works
10. the downstream smoke test passes

---

## 15. Recommended Next Milestones

### Milestone 1 — MSTR 4H chart contract
- create/confirm the canonical saved MSTR 4H chart on the Mac mini
- verify the export produces the expected schema contract
- generate and lock the canonical header fingerprint

### Milestone 2 — Local path and validation contract
- create the intake/staging path structure
- define the validation script requirements
- define the logging, manifest, and retry behavior
- define exact run-window freshness checks

### Milestone 3 — Manual golden-path proof
- run one documented end-to-end MSTR 4H export from the Mac mini
- validate and publish it to GitHub as `MSTR_4H.csv`
- confirm downstream report compatibility

### Milestone 4 — Archie review closure
- confirm the revised contract and path architecture
- confirm the automation boundary and acceptance logic

### Milestone 5 — Expansion planning
- extend the same standardization pattern to the rest of the MSTR Suite export set
- only then begin Phase 1 automation design

---

## 16. Phase 1 Preview

Once Phase 0 is accepted, Phase 1 should automate around this standardized contract in the following order:

1. intake detection
2. validation
3. staging
4. repo publish
5. reporting/logging
6. scheduled and on-demand execution

Only after that should the system automate the TradingView export action itself.

---

## 17. Questions for Archie Review

The intended Archie review should focus on:
- whether the Mac mini path architecture is the right one
- whether one-chart-per-export is the best automation boundary
- whether the validation rules are strict enough
- whether the retry/failure model is appropriate
- whether the golden-path MSTR 4H proof is the right MVP before expanding to the full suite

Those questions are now substantially answered in favor of:
- the proposed Mac mini path architecture
- one-chart-per-export as the preferred boundary
- stricter machine-testable validation rules
- copy-into-repo publish behavior
- golden-path-first scope before broader automation

---

## Bottom Line

P-MCP-CSV should begin by making **one TradingView export deterministic** before trying to automate twelve.

The approved Phase 0 golden path is:
- **MSTR**
- **4H**
- **normalized repo publish filename: `MSTR_4H.csv`**
- **raw TradingView filename preserved outside repo publish path**
- **repo root publish by copy**
- **full schema preservation**
- **canonical header fingerprint enforcement**
- **three-year minimum history**
- **mid-day and close-of-day freshness windows only**
- **fail-closed run behavior**
- **Discord + local log visibility**
- **run manifest + downstream smoke test requirements**

That is the correct revised contract for the next implementation step.
