# P-TVI — Discovery / Current-State Audit v1

**Status:** Initial audit  
**Related:** `briefs/p-tradingview-integration-brief-v1.md`  
**Related:** `briefs/p-tradingview-integration-backlog-v1.md`

---

## 1. Purpose

Document the current TradingView workflow as it exists today so P-TVI can be implemented against reality rather than assumptions.

This audit focuses on:
- current CSV/export flow
- current ingestion behavior
- current script inventory
- current chart/export dependencies
- current known friction points and risks

---

## 2. Current Operating Model — High Level

The current system already uses TradingView as a meaningful sensor layer, but the workflow is hybrid and only partially automated.

### Existing reality
TradingView currently feeds the system through exported CSV files, which are then consumed by Python scripts for:
- SRI engine calculations
- suite reporting
- DOI processing
- morning brief context
- daily engine runs
- freshness monitoring / reminders

### Important observation
P-TVI is not starting from zero.
There is already a substantial CSV-dependent TradingView architecture in place.

The project is therefore an **operational integration upgrade**, not a greenfield build.

---

## 3. Current CSV / Data Workflow

## 3.1 Current practical flow

The current pattern appears to be:

1. TradingView indicators/scripts are loaded and maintained manually.
2. CSV exports are generated from TradingView charts.
3. CSVs are placed into GitHub-tracked repo paths and/or mounted data paths.
4. Python scripts resolve latest files using filename-pattern matching.
5. Downstream analysis scripts consume those CSVs.
6. Separate freshness/reminder scripts monitor whether uploads appear current.

---

## 3.2 Evidence of current automation support already present

The repo already contains automation/support scripts related to TradingView CSV operations:

### Existing support scripts
- `scripts/csv_freshness_check.py`
- `scripts/suite_upload_alert.py`
- `scripts/daily_engine_run.py`
- `scripts/mstr_suite_engine.py`
- `scripts/mstr_suite_report.py`
- `scripts/doi_engine.py`
- `scripts/sri_engine.py`

### Existing cron references
`scripts/crontab_updated.txt` shows:
- freshness checks
- suite upload detector cadence
- reminder logic

This means the current system already has:
- freshness monitoring
- upload reminder concepts
- latest-file resolution logic
- downstream parsing behavior

But it still lacks a complete low-touch end-to-end TradingView integration layer.

---

## 3.3 Current ingestion style

The ingestion approach is currently mixed.

### Pattern A — mounted data directory
Many scripts read from:
- `/mnt/mstr-data`

### Pattern B — local repo fallback
Some scripts also read from:
- `/Users/vera/.openclaw-mstr/workspace-mstr-cio/Grok`

### Pattern C — GitHub/raw fetch path
Some logic, especially the suite engine, can fetch CSV content from GitHub using tokenized access and cache locally.

### Conclusion
The system already behaves like a **hybrid ingestion model**:
- mounted/local data for operational consumption
- GitHub as a source/canonical transfer layer in some paths
- local repo copies as fallback or working copies

This strongly supports using a **hybrid architecture** as the first P-TVI design candidate.

---

## 4. Current validation/freshness behavior

## 4.1 Current strengths

The current codebase already contains some important robustness features:
- latest-file pattern resolution using sorted hash-suffixed names
- duplicate/repeated header handling in some CSV readers
- freshness checks via dedicated script(s)
- suite upload detection logic
- family-aware file handling in several places

## 4.2 Current weaknesses

Validation is not yet unified into one canonical TradingView-integration layer.

Problems still likely include:
- validation logic spread across multiple scripts
- file expectations hard-coded in multiple places
- inconsistent source-of-truth assumptions between scripts
- human still needed for some handoff/notification steps
- truncation/integrity checks not yet centralized into a single enforceable gate

---

## 5. Current Pine / script inventory

## 5.1 Pine assets discovered in repo

Current `pine/` inventory includes:

### Core SRI/SRIBI family
- `pine/SRI_LT.pine`
- `pine/SRI_ST.pine`
- `pine/SRI_VLT.pine`
- `pine/SRI_VST.pine`
- `pine/SRIBI_LT.pine`
- `pine/SRIBI_ST.pine`
- `pine/SRIBI_VLT.pine`
- `pine/SRIBI_VST.pine`

### Forecast / action layer
- `pine/SRI_Forecast_AB1.pine`
- `pine/SRI_Forecast_AB2.pine`
- `pine/SRI_Forecast_AB3.pine`
- `pine/SRI_Forecast_DOI.pine`
- `pine/AB2_CRS.pine`

### MSTR-specific / suite / experimental
- `pine/SRI_AB1-2_Top_Formation_MSTR.pine`
- `pine/MSTR_Suite_Force_Field.pine`
- `pine/MSTR Suite — Force Field ROC`
- `pine/MSTR_Yellow_Prototype.pine`
- `pine/MSTR_B_Prototype.pine`
- `pine/MSTR Perpetual Call Valuation Indicator`

### Ratio / auxiliary
- `pine/STRF_LQD_Ratio.pine`
- `pine/INDICATOR-GUIDE.md`

---

## 5.2 Initial script classification

### Tier 1 — export-critical / production-critical candidates
These are likely first-tier for P-TVI testing and validation:
- core SRI exports used by `sri_engine.py`
- `pine/MSTR_Suite_Force_Field.pine`
- `pine/STRF_LQD_Ratio.pine`
- ratio/macro scripts whose outputs feed production reports or engines

### Tier 2 — production-adjacent research scripts
- `pine/SRI_Forecast_AB1.pine`
- `pine/SRI_Forecast_AB2.pine`
- `pine/SRI_Forecast_AB3.pine`
- `pine/SRI_Forecast_DOI.pine`
- `pine/AB2_CRS.pine`

### Tier 3 — experimental / prototype
- `pine/MSTR_Yellow_Prototype.pine`
- `pine/MSTR_B_Prototype.pine`

This tiering should be formalized in the next revision.

---

## 6. Current chart/export data universe observed

Observed current CSV universe in repo includes, among others:

### Core trading assets
- MSTR
- IBIT
- SPY
- QQQ
- GLD
- IWM
- TSLA
- PURR

### Macro / regime / ratio inputs
- BTC (`INDEX_BTCUSD`)
- MSTR/IBIT
- MSTR/SPY
- STABLE.C.D
- STRC
- STRF
- STRF/LQD
- TLT
- DXY
- VIX
- HYG
- LQD
- VT
- DBC
- sector ETFs (XLK, XLY, XLF, XLE, XLP)

### Additional observed files
- 1D and 240 families coexist for several assets
- some additional exploratory/universe files also exist

### Conclusion
TradingView is already serving not just price-charting needs but also:
- macro/regime sensing
- ratio analysis
- preferred/credit context
- cross-asset contextualization

That materially validates the macro-sourcing goal of P-TVI.

---

## 7. Current workflow strengths

The current TradingView stack already demonstrates:
- broad asset/risk-factor coverage
- established file naming conventions
- practical reliance on TradingView for both tactical and macro inputs
- downstream Python consumers already in production-like use
- some freshness alerting / reminder infrastructure
- some pattern-based latest-file resolution discipline

This is a strong base to build on.

---

## 8. Current workflow pain points / risks

## 8.1 Manual export/handoff friction
Still appears to require human participation for:
- export generation
- upload confidence
- data-availability signaling

## 8.2 Validation fragmentation
Different scripts each implement parts of:
- file selection
- cleaning
- freshness handling
- source fallback

This creates drift risk.

## 8.3 Hard-coded filenames / assumptions
Several scripts reference specific hashed filenames or fixed expected files.
This makes the system less elegant and more brittle than it should be.

## 8.4 Multiple source paths
The coexistence of:
- `/mnt/mstr-data`
- local repo CSVs
- GitHub download logic

is operationally useful, but currently too implicit.
It should become explicit policy.

## 8.5 Pine stale-instance risk
Prior lessons already show that TradingView script instances can become stale or misleading after updates.
This needs to be part of the formal deployment/testing workflow.

## 8.6 Chart visibility gap
The CIO still does not have a fully standardized direct chart-access workflow.
This remains one of the clearest P-TVI opportunities.

---

## 9. Early recommendations from discovery

## Recommendation 1 — Use a hybrid ingestion model
Do not force a false binary between GitHub and direct ingestion yet.

Best candidate architecture for v1:
- direct/local ingestion path for operational speed
- GitHub-tracked source remains canonical where versioning/reproducibility matters
- explicit freshness/status layer reports what source is being used

---

## Recommendation 2 — Centralize TradingView CSV validation
Instead of each consumer implementing its own partial checks, create a shared validator/resolver layer that handles:
- family resolution
- freshness
- schema checks
- truncation checks
- duplicate header cleanup policy

---

## Recommendation 3 — Formalize Pine script tiers
Not all Pine assets need the same automation/testing burden.

Create at least three tiers:
- production/export-critical
- production-adjacent research
- experimental

Then automate testing in that order.

---

## Recommendation 4 — Treat direct chart access as a first-class deliverable
This should not be postponed behind all ingestion work.
A proof of concept for direct chart access is high leverage and aligns directly with Gavin’s must-haves.

---

## Recommendation 5 — Make source policy explicit
Each downstream system should know whether it is reading from:
- mounted operational data
- repo-local fallback
- GitHub fetch/cache path

This should be a visible policy, not an accidental behavior.

---

## 10. Suggested immediate next actions

### A. Phase A follow-through
- formalize script inventory into tiers
- formalize chart/layout inventory
- identify first chart-access POC path

### B. Phase B kickoff
- design shared CSV validator/resolver module
- map current consumers that should use it first

### C. Phase C kickoff
- define practical method for chart access without manual screenshot upload

---

## 11. Bottom line

P-TVI is justified by the current system state.

The repo confirms that TradingView is already deeply embedded in:
- signal generation
- CSV-based ingestion
- macro/regime sensing
- suite/report workflows
- Pine research iteration

What is missing is not relevance.
What is missing is:
- a unified ingestion/validation layer
- a standardized direct chart-access workflow
- a formal Pine deployment/testing loop
- a cleaner explicit architecture tying all of that together

That means the project direction is correct, and the next step should be execution against this real current-state map.
