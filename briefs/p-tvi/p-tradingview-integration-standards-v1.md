# P-TVI — Script Tiering and Chart-View Standards v1

**Status:** Draft for review / execution  
**Related:** `briefs/p-tradingview-integration-brief-v1.md`  
**Related:** `briefs/p-tradingview-integration-backlog-v1.md`  
**Related:** `briefs/p-tradingview-integration-discovery-v1.md`

---

## 1. Purpose

Define two foundational standards for P-TVI:

1. **Pine/script tiering** — which scripts deserve the highest automation, testing, and operational protection
2. **Chart-view standards** — which TradingView layouts/views should be standardized first

This is needed so P-TVI does not treat every script and every chart as equally important.

---

## 2. Script tiering framework

Scripts should be grouped by operational criticality, not by age or personal preference.

### Tier 1 — Production / export-critical
These scripts directly support live engine workflows, CSV-derived analysis, or production-grade context generation.

### Tier 2 — Production-adjacent / research-critical
These scripts materially affect decision support or research velocity, but are not the most fragile production dependencies.

### Tier 3 — Experimental / prototype / optional
These scripts are useful for exploration, but should not receive the same operational burden as live dependencies.

---

## 3. Proposed script tiers

## Tier 1 — Production / export-critical

### Core SRI price overlays
- `pine/SRI_VST.pine`
- `pine/SRI_ST.pine`
- `pine/SRI_LT.pine`
- `pine/SRI_VLT.pine`

### Core SRIBI oscillators
- `pine/SRIBI_VST.pine`
- `pine/SRIBI_ST.pine`
- `pine/SRIBI_LT.pine`
- `pine/SRIBI_VLT.pine`

### Regime / suite-critical scripts
- `pine/MSTR_Suite_Force_Field.pine`
- `pine/STRF_LQD_Ratio.pine`

### Tier 1 rationale
These scripts should be treated as first-tier because they are closest to:
- production CSV exports
- engine consumption
- regime/state interpretation
- suite/report workflows
- architecture-critical context

### Tier 1 requirements
Tier 1 scripts should ultimately have:
- strongest schema validation
- strongest freshness/history checks
- explicit deployment/update workflow
- strongest stale-instance mitigation procedures
- first-priority parser compatibility testing

---

## Tier 2 — Production-adjacent / research-critical

### Forecast / bucket / tactical scripts
- `pine/SRI_Forecast_AB1.pine`
- `pine/SRI_Forecast_AB2.pine`
- `pine/SRI_Forecast_AB3.pine`
- `pine/SRI_Forecast_DOI.pine`
- `pine/AB2_CRS.pine`

### MSTR-specific operational research scripts
- `pine/SRI_AB1-2_Top_Formation_MSTR.pine`
- `pine/MSTR Suite — Force Field ROC`
- `pine/MSTR Perpetual Call Valuation Indicator`

### Tier 2 rationale
These scripts matter operationally, but they should come after Tier 1 for automation hardening.
They are important for:
- tactical guidance
- research acceleration
- strategy refinement
- MSTR-specific overlay logic

### Tier 2 requirements
Tier 2 scripts should eventually have:
- post-update schema/sanity checks where they export CSV-relevant columns
- defined deployment workflow
- known-reference behavior checks
- compatibility review when downstream logic depends on them

---

## Tier 3 — Experimental / prototype

### Prototype scripts
- `pine/MSTR_Yellow_Prototype.pine`
- `pine/MSTR_B_Prototype.pine`

### Tier 3 rationale
These scripts are useful as research artifacts, but they are not entitled to first-tier integration effort.
They should remain available for experimentation while being explicitly excluded from the highest-priority automation burden.

### Tier 3 requirements
- no production dependency assumptions
- clearly labeled experimental status
- no automation priority unless promoted by new evidence

---

## 4. Tiering notes / governance rules

### Rule 1 — Promotion requires evidence
A Tier 3 or Tier 2 script should only be promoted if it becomes:
- operationally necessary
- repeatedly used in production decisions
- a direct upstream dependency of engine/report logic

### Rule 2 — Automation priority follows tier
If automation capacity is limited:
- Tier 1 first
- Tier 2 second
- Tier 3 last

### Rule 3 — Export-critical status matters more than visual appeal
A script with hidden export fields that feeds the engine deserves more protection than a visually useful but non-exported overlay.

### Rule 4 — Failed branches stay de-prioritized
Previously failed branches like the MSTR Yellow/B prototype line should remain outside the core automation burden unless new evidence justifies revival.

---

## 5. Chart-view standards

P-TVI should not assume one giant overloaded TradingView layout is the right long-term solution.

Instead, use standardized views by operational purpose.

---

## View 1 — Universal Export / Download View

**Priority:** Highest  
**Purpose:** produce the canonical export set with minimal ambiguity

### Required characteristics
- contains the export-critical Tier 1 scripts needed for CSV production
- optimized for consistent export, not visual elegance
- minimized indicator overload
- stable naming discipline
- suitable for repeatable batch export workflow

### Notes
This view is the first target for:
- CSV automation
- truncation/freshness checks
- export validation

---

## View 2 — MSTR Theta / PMCC Management View

**Priority:** High  
**Purpose:** support MSTR-specific tactical management and premium-harvest context

### Likely components
- core SRI overlays relevant for MSTR structure
- MSTR suite / force context where useful
- MSTR-specific operational overlays
- valuation / PMCC context tools where appropriate

### Notes
This view is for operational trading interpretation, not necessarily CSV export.

---

## View 3 — BTC / IBIT Directional Research View

**Priority:** High  
**Purpose:** support cleaner directional delta-expression research outside the MSTR-only lane

### Likely components
- core SRI/SRIBI context for BTC / IBIT
- ratio views
- directional/tactical research overlays
- future AB2 directional research indicators

### Notes
This view reflects the architecture decision that BTC / IBIT should carry more of the directional research burden.

---

## View 4 — Macro / Regime View

**Priority:** High  
**Purpose:** use TradingView as a macro/regime sensor layer

### Likely components
- DXY
- HYG / LQD / credit proxies
- VIX
- stablecoin dominance
- BTC-relative structures
- preferred/relative instruments where useful
- sector/risk-cycle charts if they remain framework-relevant

### Notes
This view is a direct foundation for the macro-sourcing must-have in P-TVI.

---

## View 5 — Pine Development / Testing View

**Priority:** High  
**Purpose:** support script iteration, debugging, and post-update verification

### Likely components
- script-under-test
- expected export fields / hidden plots where relevant
- comparison/reference scripts if needed
- clean environment for stale-instance checks and validation

### Notes
This view exists to reduce iteration friction and isolate testing from production chart clutter.

---

## 6. Initial standardization order

If view standardization must be sequenced, use this order:

### 1. Universal Export / Download View
because CSV automation depends on it

### 2. Pine Development / Testing View
because script iteration/testing is one of Gavin’s must-haves

### 3. Macro / Regime View
because macro sourcing is a must-have and a likely force multiplier

### 4. MSTR Theta / PMCC Management View
because it supports live tactical decision-making

### 5. BTC / IBIT Directional Research View
because it will matter more as directional work migrates there

---

## 7. Immediate implications for P-TVI

This standards document implies the next practical build priorities are:

1. build the CSV validator around **Tier 1** scripts and the **Universal Export View**
2. define a **Pine Development / Testing View** so post-update verification is clean
3. define a **Macro / Regime View** as the first direct-chart-access proof of concept candidate
4. keep Tier 3 prototype work outside the initial automation burden

---

## 8. Recommended next step

The next execution step after this standards file should be:

### Ingestion architecture decision
Decide whether P-TVI v1 should formally adopt:
- GitHub handoff
- direct local ingestion
- hybrid ingestion

### Current recommendation
Use a **hybrid ingestion model** initially, because the discovery audit shows the current system already behaves that way.

---

## 9. Bottom line

P-TVI should automate and protect the parts of TradingView that matter most.

That means:
- Tier 1 scripts first
- Universal Export View first
- direct chart access built around standard views
- Pine testing built around a dedicated dev/test view
- prototypes kept deliberately out of the initial heavy automation path
