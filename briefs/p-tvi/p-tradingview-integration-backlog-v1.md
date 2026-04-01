# P-TVI — TradingView Integration Backlog v1

**Status:** Draft for review / execution  
**Priority:** 🔴 High  
**Parent brief:** `briefs/p-tradingview-integration-brief-v1.md`

---

## 1. Purpose

Translate the P-TVI brief into a concrete implementation backlog with clear sequencing.

The goal is to begin with the highest-leverage operational wins:
1. eliminate manual CSV handoff friction
2. give the CIO direct chart visibility
3. create a low-touch Pine update + testing loop
4. expand TradingView as a macro/regime sensor

---

## 2. Recommended execution order

### Phase A — Workflow discovery and current-state mapping
Do first. Avoid building blind.

### Phase B — CSV automation + validation pipeline
Highest immediate leverage.

### Phase C — Direct chart access proof of concept
Second-highest leverage.

### Phase D — Pine update + low-touch testing workflow
Needed for sustainable iteration.

### Phase E — TradingView macro/regime integration
Valuable expansion after the core workflow is stable.

---

## 3. Backlog

## A. Discovery / current-state audit

### A1. Document current TradingView workflow end-to-end
**Priority:** P0  
**Outcome:** exact current-state map

Tasks:
- document how CSVs are currently exported
- document where they land locally
- document how they are validated for truncation/history depth
- document how they are uploaded to GitHub
- document how availability is currently communicated to the CIO
- document current pain points / failure modes

Deliverable:
- current-state workflow note appended or linked from the main brief

---

### A2. Inventory current Pine/script/chart assets
**Priority:** P0  
**Outcome:** authoritative scope inventory

Tasks:
- list core Pine scripts currently in active use
- classify each as: production / experimental / legacy / macro / export-critical
- identify which scripts must be in the first testing tier
- identify which scripts currently feed CSV-dependent workflows

Deliverable:
- script inventory table

---

### A3. Inventory current chart views/layouts
**Priority:** P1  
**Outcome:** understand what must be standardized

Tasks:
- identify current TradingView layouts/views
- identify which are export views vs analysis views
- identify which views are overloaded / fragile / redundant
- identify where one universal download view is sufficient vs where multiple standard views are needed

Deliverable:
- layout inventory + standardization candidates

---

## B. CSV automation + validation pipeline

### B1. Define canonical ingestion architecture
**Priority:** P0  
**Outcome:** one agreed transfer model

Decision to make:
- GitHub as canonical handoff layer
- direct local watch-folder ingestion
- hybrid model (preferred candidate until proven otherwise)

Recommendation:
- start with a **hybrid model**:
  - local/watch-folder style ingestion for operational speed
  - GitHub-tracked files remain canonical source for versioned script/data workflow where appropriate

Deliverable:
- architecture decision note

---

### B2. Build CSV validation utility
**Priority:** P0  
**Outcome:** automatic detection of bad TradingView exports

Validation checks:
- file exists
- schema/expected columns present
- minimum history depth satisfied
- latest timestamp is recent enough
- no obvious truncation pattern
- duplicate header-row contamination handled
- asset/pair + timeframe-family naming rules respected

Deliverable:
- Python validator script/module

---

### B3. Build latest-file resolver / family governance
**Priority:** P0  
**Outcome:** clean interpretation of most recent valid files

Tasks:
- preserve distinct families like `240` vs `1D`
- reject stale duplicates where appropriate
- define priority rules across local vs GitHub copies
- emit explicit freshness/status output

Deliverable:
- reusable resolver logic + conventions doc

---

### B4. Build ingestion/status reporting
**Priority:** P1  
**Outcome:** CIO no longer waits for manual “data is ready” message

Tasks:
- emit machine-readable status for data freshness
- surface validation failures clearly
- optionally send Discord/system message when new valid data is available
- optionally update DB/config state for `last_upload_ts` / freshness markers

Deliverable:
- availability/status reporting mechanism

---

### B5. Define failure policy
**Priority:** P1  
**Outcome:** predictable behavior on bad exports

Decisions needed:
- when to hard-fail
- when to warn and proceed
- when to fall back to previous good file
- when to block report generation entirely

Deliverable:
- failure-policy rules

---

## C. Direct chart access

### C1. Evaluate chart access options
**Priority:** P0  
**Outcome:** pick a reliable chart-visibility method

Options to evaluate:
- browser-controlled TradingView access
- standardized chart URLs/layouts
- internal snapshot workflow
- image/screenshot capture only as fallback

Deliverable:
- chart-access recommendation

---

### C2. Build chart-access proof of concept
**Priority:** P0  
**Outcome:** CIO can inspect current chart state directly

Success criteria:
- chart can be opened consistently
- indicators/layout load correctly
- current state is visually inspectable without manual screenshot upload
- workflow is stable enough for repeated use

Deliverable:
- working POC with usage notes

---

### C3. Define standard chart views
**Priority:** P1  
**Outcome:** reduce layout chaos

Initial candidate views:
- universal download/export view
- MSTR theta-management view
- BTC / IBIT directional research view
- macro/regime view
- development/testing view for Pine iteration

Deliverable:
- standard view set

---

## D. Pine update + testing loop

### D1. Define Pine deployment/update workflow
**Priority:** P0  
**Outcome:** explicit process from file edit to chart/test state

Tasks:
- define source-of-truth path for Pine files
- define how chart-side updates are applied
- define how stale-instance risk is detected/mitigated
- define what counts as “deployed” vs “edited only”

Deliverable:
- Pine deployment workflow note

---

### D2. Build post-update validation checklist
**Priority:** P0  
**Outcome:** no manual babysitting required for basic QA

Checks:
- expected columns exported
- no silent schema drift
- current bars present
- downstream parser still works
- output behavior is plausible on known reference cases

Deliverable:
- regression/sanity checklist

---

### D3. Build automated export-schema tests for top-tier scripts
**Priority:** P1  
**Outcome:** script changes break loudly instead of silently

Top-tier scripts should likely include:
- core SRI export scripts
- suite-critical TradingView exports
- MSTR/IBIT ratio script(s)
- macro/regime export scripts used by the engine

Deliverable:
- automated schema tests for first-tier scripts

---

### D4. Build parser-compatibility tests
**Priority:** P1  
**Outcome:** Pine changes don’t silently break Python consumption

Tasks:
- run updated exports through current parser logic
- detect rename/missing-column issues quickly
- identify where parser assumptions are too brittle

Deliverable:
- parser-compatibility test harness

---

## E. TradingView macro/regime integration

### E1. Build candidate series list
**Priority:** P1  
**Outcome:** prioritized macro integration universe

Candidate categories:
- DXY / rates / yields
- HYG / credit / liquidity proxies
- VIX / vol structures
- stablecoin dominance
- BTC-relative structures
- preferreds / spreads / ETF relationships
- breadth / internal market measures

Deliverable:
- ranked candidate list with rationale

---

### E2. Classify macro series by use type
**Priority:** P1  
**Outcome:** avoid undisciplined macro sprawl

Classification:
- regime-critical
- corroborative only
- exploratory only
- visual/context only

Deliverable:
- macro series classification table

---

### E3. Pilot first macro ingestion set
**Priority:** P2  
**Outcome:** prove macro sourcing works in practice

Suggested first pilot set:
- DXY
- HYG or credit proxy
- VIX / vol proxy
- stablecoin dominance
- one preferred/relative structure if available and useful

Deliverable:
- first TradingView macro pilot integration

---

## F. Reporting / alert integration

### F1. Expose data-freshness state in reports
**Priority:** P1  
**Outcome:** analysis consumers know whether chart data is current

Tasks:
- optionally annotate morning brief / suite report with chart-data freshness
- surface stale/truncated warnings clearly

Deliverable:
- freshness indicator in reporting flow

---

### F2. Evaluate TradingView alert-routing opportunities
**Priority:** P2  
**Outcome:** reduce missed/high-friction signals

Tasks:
- identify alert types worth routing
- classify by urgency and usefulness
- determine whether alerts should hit Discord directly or feed a parser first

Deliverable:
- alert-routing sub-plan

---

## 4. Suggested first implementation sprint

### Sprint 1 objective
Deliver the highest-leverage operational base for P-TVI.

### Sprint 1 scope
1. document current workflow
2. decide ingestion architecture
3. build CSV validator
4. build latest-file/freshness resolver
5. produce chart-access recommendation / POC path
6. define Pine deployment + post-update validation workflow

### Sprint 1 success condition
By end of Sprint 1, the team should know:
- how TradingView data enters the system
- how bad exports are caught automatically
- how the CIO will access charts directly
- how Pine changes will be validated with low touch

---

## 5. Dependencies / risks

### Risks
- TradingView UI/browser automation may be brittle if over-scoped early
- local/export paths may vary by machine or workflow
- stale-instance Pine behavior can create false confidence
- macro series availability/consistency may differ from dedicated sources
- over-automation too early could create a fragile maintenance burden

### Mitigations
- start with simple stable workflows
- prefer validation and observability before heavy automation
- keep GitHub-tracked source canonical
- treat browser automation as a tool, not the architecture

---

## 6. Recommendation

Start P-TVI with a practical systems-engineering mindset:
- workflow mapping first
- CSV integrity automation second
- direct chart access third
- Pine testing loop fourth
- macro expansion fifth

That sequence maximizes practical payoff while minimizing fragile overbuild.
