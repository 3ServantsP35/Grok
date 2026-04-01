# P-TVI — TradingView Integration Claude Code Handoff Brief v1

**Status:** Handoff brief for engineering planning  
**Audience:** Claude Code / engineering implementation workflow  
**Project:** P-TVI — TradingView Integration  
**Priority:** 🔴 High

---

## 1. Executive Summary

This project is an infrastructure and workflow upgrade for the MSTR Engine system.

The goal is to transform TradingView from a partially manual charting/export surface into a first-class operational tool inside the system.

Today, TradingView is already deeply embedded in the workflow through Pine scripts and CSV exports that feed Python engines, reports, and regime analysis. But the workflow still depends too much on manual effort, especially around CSV exports, data freshness/truncation checks, chart visibility, and Pine-update testing.

The desired result is a system where TradingView becomes:
- a more automated data source
- a direct chart-analysis surface for the CIO
- a cleaner Pine-development environment
- a lower-touch testing loop after script changes
- a viable source of macro/regime data

This is not a request for a vague “integration.”
It is a concrete effort to improve how chart data, chart state, Pine development, and TradingView-native macro data flow through the larger MSTR Engine system.

---

## 2. What the user is trying to accomplish

The user wants to achieve five must-have outcomes in the context of TradingView as a tool inside the broader system.

### Must-have #1 — Automate the current CSV workflow
Current manual steps include:
- downloading TradingView CSVs manually
- checking them for truncation / incomplete history manually
- posting them to the GitHub repo manually
- notifying the CIO that fresh data is available

The user wants this process automated or materially reduced.

### Must-have #2 — Provide direct chart access
The CIO should be able to inspect current charts directly rather than depending on manually uploaded screenshots/images.

### Must-have #3 — Support continued Pine iteration
The system should make it easier to continue evolving Pine scripts over time.

### Must-have #4 — Support post-update testing without manual intervention
After Pine script updates, the system should support testing/validation without requiring a fully manual QA handoff loop.

### Must-have #5 — Source macro data directly from TradingView
TradingView should become a useful macro/regime data source, not just a price-charting tool.

---

## 3. Why this project matters

Right now the system loses time and reliability because:
- chart-derived data still requires manual bridging
- chart-state visibility for the CIO is too indirect
- Pine iteration is possible but not operationally smooth
- validation logic is fragmented across multiple scripts
- TradingView-native macro coverage is underused

If solved well, this project should:
- reduce human handoff friction
- improve data freshness confidence
- shorten the path from chart state to analysis
- improve engineering speed for Pine changes
- make the whole system less operationally brittle

This is a high-leverage infrastructure project because it affects data acquisition, research speed, reporting quality, and chart-side observability at once.

---

## 4. Important context: this is not a greenfield project

Claude Code should assume that TradingView is **already deeply integrated** into the current system.

This project is not about inventing a relationship with TradingView from scratch.
It is about upgrading an already-real dependency into a cleaner, more explicit, more automated architecture.

### Existing reality
TradingView currently feeds the system through CSV exports used by Python scripts for:
- SRI engine calculations
- daily engine runs
- suite report generation
- DOI processing
- morning brief context
- freshness/reminder logic

### Practical implication
The implementation plan should start with current system reality, not a theoretical fresh redesign.

---

## 5. Current repo/workspace artifacts already created for this project

Claude Code should read these first:

### Primary docs
- `briefs/p-tradingview-integration-brief-v1.md`
- `briefs/p-tradingview-integration-backlog-v1.md`
- `briefs/p-tradingview-integration-discovery-v1.md`
- `briefs/p-tradingview-integration-standards-v1.md`

### Project/task tracking
- `active-tasks.md`

These documents already capture:
- project goals
- workstreams
- current-state audit
- Pine/script tiering
- chart-view standardization ideas
- phased backlog

Claude Code should build from those documents, not ignore them.

---

## 6. Current system behavior Claude Code needs to understand

## 6.1 TradingView already acts as a sensor layer
There is already a documented architecture pattern in the system:

> TradingView (sensor) → CSV → Engine (brain) → Alerts/Reports

This project should refine and operationalize that pattern, not replace the Python decision engine.

### Design rule
TradingView is a **sensor/tool layer**, not the final decision engine.
Python remains the main interpretation/aggregation layer.

---

## 6.2 Current ingestion behavior is hybrid already
The current system reads TradingView data through a mix of:
- mounted operational data paths (for example `/mnt/mstr-data`)
- local repo/workspace fallback paths
- GitHub/raw-fetch style paths in some components

This means the current system already behaves like a **hybrid ingestion model**.

### Important implication
Claude Code should not assume the architecture must choose a pure GitHub-only or pure direct-ingestion model.
A hybrid design is currently the most realistic candidate.

---

## 6.3 Current validation logic is fragmented
There are already pieces of validation and freshness logic in the codebase, but they are spread across multiple scripts.

This means the project should likely centralize:
- schema checks
- freshness checks
- latest-file resolution
- truncation/integrity checks
- family handling (e.g. 240 vs 1D)
- source/fallback policy

### Important implication
One probable high-value engineering outcome is a shared TradingView CSV validator/resolver module used by multiple consumers.

---

## 7. Existing scripts/features Claude Code should inspect

The following existing scripts are directly relevant and should be reviewed before proposing an engineering plan.

### Current CSV/freshness/upload-related scripts
- `scripts/csv_freshness_check.py`
- `scripts/suite_upload_alert.py`
- `scripts/daily_engine_run.py`
- `scripts/mstr_suite_report.py`
- `scripts/mstr_suite_engine.py`
- `scripts/doi_engine.py`
- `scripts/sri_engine.py`
- `scripts/morning_brief.py`

### Why they matter
These scripts already implement parts of:
- file discovery
- filename assumptions
- CSV parsing
- latest-file resolution
- fallback behavior
- freshness signaling
- downstream dependency expectations

The engineering plan should account for existing behavior rather than duplicating or breaking it.

---

## 8. Existing Pine/script inventory Claude Code should understand

The current `pine/` inventory includes at least the following categories:

### Core SRI/SRIBI family
- `pine/SRI_VST.pine`
- `pine/SRI_ST.pine`
- `pine/SRI_LT.pine`
- `pine/SRI_VLT.pine`
- `pine/SRIBI_VST.pine`
- `pine/SRIBI_ST.pine`
- `pine/SRIBI_LT.pine`
- `pine/SRIBI_VLT.pine`

### Forecast/action layer
- `pine/SRI_Forecast_AB1.pine`
- `pine/SRI_Forecast_AB2.pine`
- `pine/SRI_Forecast_AB3.pine`
- `pine/SRI_Forecast_DOI.pine`
- `pine/AB2_CRS.pine`

### Regime/suite/MSTR-specific
- `pine/MSTR_Suite_Force_Field.pine`
- `pine/STRF_LQD_Ratio.pine`
- `pine/SRI_AB1-2_Top_Formation_MSTR.pine`
- `pine/MSTR Suite — Force Field ROC`
- `pine/MSTR Perpetual Call Valuation Indicator`

### Experimental/prototype
- `pine/MSTR_Yellow_Prototype.pine`
- `pine/MSTR_B_Prototype.pine`

Claude Code should treat these as different operational tiers, not as one flat list.

---

## 9. Script tiering assumptions already proposed

A tiering model has already been proposed.

### Tier 1 — Production/export-critical
Likely includes:
- core SRI overlays
- core SRIBI oscillators
- `pine/MSTR_Suite_Force_Field.pine`
- `pine/STRF_LQD_Ratio.pine`
- other scripts whose exported fields feed live engine/report behavior

### Tier 2 — Production-adjacent / research-critical
Likely includes:
- forecast scripts
- tactical research scripts
- MSTR-specific operational overlays that matter but are not the highest-risk export dependencies

### Tier 3 — Experimental/prototype
Likely includes:
- Yellow/B prototype scripts

### Important implication
Automation/testing should be prioritized in this order:
- Tier 1 first
- Tier 2 second
- Tier 3 last

---

## 10. Chart-view standardization assumptions already proposed

The project already has a proposed view model.

### Proposed standard views
1. **Universal Export / Download View**
2. **Pine Development / Testing View**
3. **Macro / Regime View**
4. **MSTR Theta / PMCC Management View**
5. **BTC / IBIT Directional Research View**

### Important implication
Claude Code should think in terms of standard operating views/layouts, not one giant overloaded TradingView workspace.

---

## 11. Constraints / rules Claude Code must preserve

### 11.1 GitHub-tracked files are canonical for source edits
The user explicitly wants GitHub-tracked files patched directly.

### 11.2 Do not break existing production consumers casually
Any plan should identify which scripts currently depend on which file patterns or schema assumptions.

### 11.3 Preserve family discipline
Asset/pair + timeframe families matter.
Examples:
- `240` and `1D` are distinct families
- latest-file logic should not collapse distinct families into one

### 11.4 Avoid fragile over-automation too early
The user wants meaningful progress, not flashy automation that becomes brittle.

### 11.5 Preserve the architecture split
TradingView should improve the system, but should not replace the Python engine as the main interpretation layer.

### 11.6 Prototype branches are not equal priority
The failed MSTR Yellow/B branch should not quietly consume Tier 1 automation effort.

---

## 12. Known technical details from the current codebase

Claude Code should be aware of the following observations from the current audit.

### 12.1 Filename/hash pattern behavior already exists
Multiple scripts use filename matching patterns like:
- `BATS_MSTR, 240_*.csv`
- `CRYPTOCAP_STABLE.C.D, 240_*.csv`
- `INDEX_BTCUSD, 240_*.csv`

Several resolvers rely on:
- sorted matches
- lexicographically latest hash-suffixed filename selection

### 12.2 Duplicate header rows are already a known issue
Some CSV loaders explicitly strip repeated header rows from TradingView exports.

### 12.3 There are both local and mounted data paths
Examples in current code include:
- `/mnt/mstr-data`
- local workspace/repo CSVs
- suite-engine GitHub fetch/cache logic

### 12.4 Cron-based freshness/upload support already exists
There are existing cron references for:
- CSV freshness checks
- suite upload alerts/reminders

### 12.5 TradingView stale-instance behavior is already a known lesson
There is prior project knowledge that TradingView script instances can become stale/misleading after updates and may need recreation.

### Important implication
The deployment/testing plan should explicitly account for stale-instance mitigation.

---

## 13. Suggested engineering framing for Claude Code

Claude Code should treat this project as five linked engineering problems:

### A. Data acquisition/integration
How should TradingView-derived data enter the system with minimal manual friction?

### B. Validation/integrity
How do we ensure exports are current, complete, family-correct, and schema-valid?

### C. Direct chart visibility
How can the CIO access charts directly without manual screenshot handoff?

### D. Pine iteration/testing
How do we create a low-touch workflow from Pine edit → deployed chart state → validated output?

### E. Macro/regime sourcing
How should TradingView-native macro series be incorporated without creating sprawl or duplicated source confusion?

---

## 14. What Claude Code should produce

The user intends to work with Claude Code to create an engineering plan.

The most useful Claude Code output would be:

### 14.1 A concrete engineering plan
Including:
- architecture decision(s)
- phased implementation plan
- proposed modules/components
- explicit first sprint
- dependency/risk analysis

### 14.2 A proposed system architecture
Especially for:
- ingestion layer
- validator/resolver layer
- chart-access path
- Pine deployment/testing flow
- reporting/freshness signaling integration

### 14.3 A migration strategy
How to move from today’s mixed/fragmented reality to a cleaner system without breaking current production workflows.

### 14.4 A list of unknowns requiring user input
The user explicitly wants Claude Code to advance the work as far as possible, but any true blockers or ambiguous policy choices should be surfaced clearly.

---

## 15. Recommended starting point for Claude Code

Claude Code should begin by reading, in order:

1. `briefs/p-tradingview-integration-brief-v1.md`
2. `briefs/p-tradingview-integration-backlog-v1.md`
3. `briefs/p-tradingview-integration-discovery-v1.md`
4. `briefs/p-tradingview-integration-standards-v1.md`
5. `active-tasks.md`
6. the relevant existing scripts listed above

Then Claude Code should produce an implementation-ready engineering plan.

---

## 16. Best current architecture recommendation

Based on the current audit, the best starting recommendation is:

### **Use a hybrid ingestion model**
Meaning:
- local/direct ingestion path for operational speed where feasible
- GitHub-tracked files remain canonical where versioning/reproducibility matter
- explicit validator/resolver layer determines freshness/quality/source status
- downstream consumers become less dependent on bespoke per-script file discovery logic over time

This recommendation should be challenged if Claude Code finds a better approach, but it is the best current candidate.

---

## 17. Bottom line

The user is trying to make TradingView a first-class operational tool inside the MSTR Engine system.

Success means:
- less manual CSV handoff
- direct chart access for analysis
- easier Pine innovation
- low-touch post-update testing
- meaningful TradingView-native macro sourcing
- a cleaner architecture connecting chart state to Python-side interpretation

Claude Code should treat this as a serious systems-integration project with existing production context, not as a narrow convenience automation request.
