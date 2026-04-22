# SRI Decision Engine — Complete Methodology Tutorial
**Version 3.2.1 DRAFT | Date: 2026-04-22 | Author: CIO Engine**

---

## Purpose of v3.2.1

Version 3.2.1 preserves the v3.2 branch architecture while materially upgrading the Howell Phase Engine design.

The most important changes in v3.2.1 are:

1. **Layer 0.5 is upgraded** from a phase labeler into a fuller transition framework modeled more explicitly on how SRI handles stage transitions.
2. **Liquidity Destination / Absorption State** is added so the engine can distinguish between liquidity supporting financial assets and liquidity being absorbed by the real economy.
3. **A Howell evidence stack** is formalized to support phase designation with a more disciplined and auditable input set.
4. **Phase Transition Percentage** is introduced so the framework can represent transition formation with a style that is consistent with the existing stage framework.
5. **The cascade from Layer 0.5 into downstream layers is clarified** so phase outputs more directly influence deployment intensity, timing, and allocation posture.

This document remains a **methodology + architecture spec hybrid**.

---

## Table of Contents

1. Architecture Overview (v3.2.1)
2. Key Design Principles
3. Layer 0 — GLI Engine
4. Layer 0.5 — Howell Phase Engine
5. Layer 0.75 — Theme Routing and Ingest Layer
6. Theme Allocation Framework
7. MSTR Theme Engine — Force Field Branch
8. Visser Theme Engine — APE Integration Branch
9. All-Weather Engine
10. Layer 1 — Shared Regime Engine
11. Layer 2 — Signal Layer
12. Layer 3 — Allocation Engine
13. AB Bucket Framework in v3.2
14. Personalized Portfolio Report Integration
15. Human Technical Overlay
16. Open Questions and Next Iteration Targets

---

## 1. Architecture Overview (v3.2.1)

The engine is now organized around a shared macro scaffold, a theme routing and ingest layer, and a portfolio execution framework.

```text
┌──────────────────────────────────────────────────────────────┐
│ LAYER 0: GLI ENGINE                                         │
│ Macro liquidity / growth regime                             │
│ Output: GLI Z-score, GEGI, paradigm label                   │
│ Function: This layer measures the global liquidity backdrop │
│ and establishes the top-down macro conditions that shape    │
│ risk appetite for every downstream decision.                │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 0.5: HOWELL PHASE ENGINE                              │
│ Phase + factor preference + deployment posture              │
│ Output: phase, cyc/def pref, growth/value pref, posture     │
│ Function: This layer translates liquidity structure into a  │
│ usable market phase, factor preference, and deployment      │
│ posture so the system can anticipate transitions instead of │
│ reacting to them too late.                                  │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 0.75: THEME ROUTING AND INGEST LAYER                  │
│ Activates branches and ingests branch-native outputs        │
│ Branches: MSTR | Visser/APE | All-Weather                   │
│ Output: branch state + deployment intensity + warnings      │
│ Function: This layer activates the relevant top-level theme │
│ sleeves, ingests external or native branch intelligence,    │
│ and merges that with macro context before capital is put to │
│ work.                                                       │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 1: SHARED REGIME ENGINE                               │
│ Common structural / regime interpretation                   │
│ Output: regime state, risk posture, shared context          │
│ Function: This layer converts broad market structure into a │
│ shared risk framework that all active sleeves can use for   │
│ consistent downstream signal interpretation.                │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 2: SIGNAL LAYER                                       │
│ AB1 / AB2 / AB3 logic inside active theme sleeves           │
│ Output: entry / hold / trim / income / accumulation states  │
│ Function: This layer converts theme, regime, and timing     │
│ context into actionable trade and position-management       │
│ signals for the active sleeves.                             │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 3: ALLOCATION ENGINE                                  │
│ Security selection + rebalancing + theme rotation + Global  │
│ AB4                                                        │
│ Output: portfolio-aware capital posture                     │
│ Function: This layer converts active signals into actual    │
│ portfolio deployment, sizing, reserve posture, security     │
│ choices, and cross-theme capital rotation.                  │
└──────────────────────────────────────────────────────────────┘
```

### Core v3.2.1 idea
The system no longer assumes that every theme must be internally created the same way.

Instead:
- **MSTR** is a native SRI branch built around Strategy / BTC mechanics.
- **Visser** is an externally constructed strategy branch owned by **APE**, then ingested into the SRI workflow.
- **All-Weather** is a portfolio-balancing branch focused on durability, diversification, and reserve posture.

### Important simplification carried forward
**TSLA is not a separate top-level route.**
It may appear within Visser as an optional security, high-conviction expression, or sub-theme.

---

## 2. Key Design Principles

### 2.1 Shared macro, branch-specific intelligence
The top of the stack remains shared.
Branch-specific differentiation begins at **Layer 0.75**.

### 2.2 Multiple sleeves can coexist
A portfolio owner can allocate capital to one, several, or all top-level branches simultaneously.

### 2.3 External engines are allowed
Not every branch has to be built natively inside SRI.
If a branch already has a valid strategy engine, SRI should ingest it rather than needlessly recreate it.

### 2.4 SRI informs, it does not erase branch ownership
If an external branch such as APE already owns:
- thesis construction
- watchlist management
- internal security selection
- internal risk management

then SRI should preserve that ownership and add:
- macro conditioning
- portfolio integration
- TA timing overlays
- cross-theme capital allocation context

### 2.5 Theme-first, AB-second
In v3.2 the intended portfolio logic is:
1. assign capital at the **theme / branch** level
2. condition that capital through Layers 0, 0.5, and 1
3. deploy and manage it through AB buckets and allocation logic

### 2.6 Global AB4 remains global
AB4 remains a global capital layer, even though branch-level decisions may influence how much of the total portfolio stays there.

---

## 3. Layer 0 — GLI Engine

No methodological change in v3.2.

Layer 0 continues to provide:
- global liquidity context
- macro growth context
- broad probability adjustment
- top-down backdrop for all downstream logic

### Role in v3.2
Layer 0 still conditions:
- whether macro is broadly supportive or restrictive
- whether a branch should be interpreted in a risk-on or risk-off environment
- how aggressively downstream sleeves should deploy

**Important:** Layer 0 does **not** choose the branch. It conditions the branch.

---

## 4. Layer 0.5 — Howell Phase Engine

Layer 0.5 remains the macro transition engine, but v3.2.1 makes it much more structurally similar to the way SRI handles stage designation and stage transitions.

### 4.1 Design goal
The Howell framework should not merely say, “we are in Rebound, Calm, Speculation, or Turbulence.”

It should do the equivalent of the SRI stage framework by:
- identifying the current phase
- identifying whether the phase is strengthening or weakening
- defining recognizable transition markers
- estimating how close the system is to the next phase
- cascading those outputs into deployment and allocation decisions downstream

### 4.2 Core outputs
Layer 0.5 should now provide five durable outputs:

1. **Phase Label**
   - Rebound
   - Calm
   - Speculation
   - Turbulence

2. **Factor Preference**
   - cyclical vs defensive
   - growth vs value

3. **Deployment Posture**
   - offensive
   - selective
   - defensive
   - ballast-building

4. **Liquidity Destination / Absorption State**
   - financial-market supportive
   - mixed / contested
   - real-economy absorptive

5. **Phase Transition Percentage**
   - an estimate of how far the system has progressed from the current phase toward the next one
   - intended to mirror the style of the existing stage framework more than a generic “risk score”

### 4.3 Key Howell refinements
The Howell framework implies that:
- **liquidity level vs average** is most useful for determining **cyclical vs defensive** preference
- **liquidity direction / first difference** is most useful for determining **growth vs value** preference
- strong real-economy conditions can coincide with weakening support for financial assets
- late-cycle strength can therefore be dangerous for risk assets rather than automatically bullish

### 4.4 Liquidity destination state
This is a critical new output.

The Phase Engine should distinguish between:
- liquidity that is still available to support asset prices, refinancing capacity, and financial-market balance sheets
- liquidity that is increasingly being absorbed by the real economy through working capital, capex, inventory, or other non-asset-price-inducing uses

This matters because risk assets can weaken even when the economy still appears robust.

### 4.5 Howell phase transition framework
The architecture should formalize Howell phases in a way that is analogous to SRI stage handling.

That means defining:
- phase continuation markers
- phase transition markers
- confirmation thresholds
- invalidation criteria
- a transition percentage that rises as evidence for the next phase accumulates

The system should therefore become capable of saying things like:
- current phase remains intact
- transition pressure is building
- transition is likely but not confirmed
- new phase is confirmed

### 4.6 Evidence stack for phase designation
The following evidence stack should be treated as a formal input set into phase designation:
- cyclicals vs defensives
- growth vs value leadership
- yield-curve direction and inflection behavior
- commodity leadership and late-cycle resource behavior
- market internals / risk appetite measures
- survey-vs-market divergence where observable
- liquidity destination / absorption behavior

This evidence stack is valuable because it helps identify not just whether there is “strength,” but what kind of strength it is and what part of the liquidity cycle it most resembles.

### 4.7 Lead-lag principle
The architecture should explicitly assume that:
- liquidity cycle leads
- business cycle lags
- risk appetite and market internals often turn before surveys confirm the transition

This means Layer 0.5 should be optimized for identifying **transition formation**, not merely **transition confirmation**.

### 4.8 Intended use of the framework
The purpose of this layer is not to hard-code the market’s current state into the architecture document.

Instead, it should provide a durable framework for identifying:
- where the market is within the liquidity cycle
- which factor preferences are favored in that phase
- whether liquidity is supporting financial assets or being absorbed elsewhere
- what kind of deployment posture is appropriate as transitions begin to form
- how close the system likely is to the next phase

### 4.9 Relationship to branch-native frameworks
Howell Phase is a **macro capital-flow framework**.
It may align or conflict with branch-native strategic frameworks, especially Visser eras.
That tension is expected and should be handled explicitly rather than treated as a bug.

### 4.10 Cascade into downstream layers
Layer 0.5 outputs should not remain descriptive only.
They should cascade downstream as follows:
- **Layer 0.75**: branch deployment intensity and caution flags
- **Layer 1**: common risk posture and regime interpretation
- **Layer 2**: aggressiveness of timing signals and preferred structure selection
- **Layer 3**: sizing, reserve posture, security selection pacing, and theme rotation

### 4.11 Strong economy, weak risk-asset liquidity rule
The architecture should explicitly support the possibility that:
- the business cycle appears strong
- but financial-market liquidity support is deteriorating

When that happens, the system should not interpret strong macro by itself as a broad risk-on green light.
Instead, it should treat the combination as potentially late-cycle and increasingly hostile to indiscriminate risk deployment.

---

## 5. Layer 0.75 — Theme Routing and Ingest Layer

This is the defining architectural upgrade in v3.2.

### 5.1 Purpose
Layer 0.75 now has three jobs:

1. **Routing**
   - determine which top-level branches are active for a given portfolio owner
   - based on declared allocation percentages

2. **Ingest**
   - accept branch-native outputs from either internal or external engines
   - preserve branch-specific intelligence rather than flattening everything into one generic model

3. **Deployment Conditioning**
   - determine how aggressively each active sleeve should be deployed
   - based on macro context, branch-native state, and timing overlays

### 5.2 Inputs
- portfolio owner branch allocation
- Layer 0 output
- Layer 0.5 output
- branch-specific driver data
- external branch outputs where applicable
- optional human technical overlay when structure materially affects timing

### 5.3 Outputs
For each active branch:
- branch state
- branch confidence
- deployment intensity
- preferred exposure style
- route-specific warnings / invalidations
- distinction between **systematic branch read** and **human-adjusted deployment read** when relevant

### 5.4 Routing rule
If portfolio owner allocation to a branch is:
- **0%** → branch is moot
- **> 0%** → branch is active

### 5.5 Default top-level branch allocation
Default portfolio template remains illustrative only.
Portfolio owners may adjust branch weights based on mandate, risk tolerance, conviction, and diversification goals.

### 5.6 Human intervention at Layer 0.75
Human chart analysis can intervene at Layer 0.75 when route activation or deployment intensity depends on structure that is not yet reliably inferable from the systematic stack alone.

This intervention should work as follows:
- the engine produces its best route-level read from Layers 0, 0.5, and branch inputs
- if deployment timing depends on unresolved chart structure, the workflow explicitly requests a human chart view
- the human input is treated as an overlay on timing, exposure style, or caution flags, not as a replacement for the branch itself
- final branch output should distinguish between **branch-native strategic view**, **SRI systematic overlay**, and **human timing overlay** when more than one is present

### 5.7 Conflict-resolution rule
When branch-native conviction and SRI overlays disagree, the system should not collapse the conflict into a false single answer.
It should instead surface the disagreement explicitly.

Examples:
- **strong thesis, weak timing** → deploy less, stage entries, or prefer shares over leverage
- **good timing, weak thesis** → treat as tactical only, not strategic accumulation
- **macro headwind, branch conviction intact** → reduce sleeve size rather than forcing zero allocation
- **owner override** → allowed, but must be visibly recorded as an override rather than an engine recommendation

---

## 6. Theme Allocation Framework

### 6.1 Strategic branch allocation
The portfolio owner determines strategic sleeve weights.
This is a mandate-level decision, not a pure market-timing decision.

### 6.2 Tactical deployment within sleeve
Once a sleeve exists, the branch plus SRI overlay decide:
- whether to deploy now
- how much of the sleeve to deploy
- whether to prefer shares, options, or reserve posture
- when to slow, pause, or increase deployment

### 6.3 Future allocation sophistication
Later versions may allow a portfolio engine to recommend allocations across branches, but owner control remains primary.

### 6.4 Branch allocation vs branch composition
A critical distinction in v3.2:
- **branch allocation** = how much capital the overall portfolio gives a branch
- **branch composition** = how the branch internally allocates capital across securities

For Visser, branch composition is primarily owned by **APE**.
For MSTR and All-Weather, branch composition is native to SRI.

---

## 7. MSTR Theme Engine — Force Field Branch

### 7.1 Status
This remains the most fully developed native branch in the architecture.

### 7.2 Thesis premise
MSTR is not just BTC beta.
Its valuation and price action are driven by a specific reflexive flywheel:
- Strategy capital raising
- preferred / credit conditions
- BTC demand absorption
- premium expansion / compression
- stablecoin and liquidity backdrop
- relative expression vs IBIT

### 7.3 Core driver set
Primary current inputs include:
- STRF/LQD
- MSTR/IBIT
- STRC
- stablecoin dominance
- MSTR self-state

### 7.4 Output role
The MSTR branch should continue to output:
- directional force
- bounce exhaustion / continuation risk
- deployment intensity for the MSTR sleeve
- guidance for whether AB1 / AB2 / AB3 should be active

### 7.5 Relationship to portfolio workflow
MSTR remains a native route, but it is now clearly only one branch of the larger portfolio engine.

---

## 8. Visser Theme Engine — APE Integration Branch

### 8.1 Status
Visser is now defined as a real branch in v3.2.

However, it is **not** re-created inside SRI.
It is ingested from an external strategy engine referred to operationally as **APE**.

### 8.2 Ownership boundary
APE should own the internal Visser strategy logic, including where applicable:
- thesis construction
- era logic
- watchlist management
- KPI-based promotions / demotions
- internal security selection
- internal allocation and risk management
- hedge-fund style synthesis specific to the Visser process

SRI should own:
- macro conditioning
- phase-aware interpretation
- timing overlays
- deployment intensity at the branch level
- cross-theme portfolio allocation context
- reporting and portfolio integration

### 8.3 Conceptual model
The cleanest mental model is:

> **APE builds the ETF; SRI decides how much ETF, when, and under what macro and timing conditions.**

That is not literally an ETF structure, but it is the correct architectural analogy.

### 8.4 Required ingest contract from APE
APE should ideally provide a structured payload into Layer 0.75 containing:
- **Era State**
- **Thesis State**
- **Security Universe / Sleeve Composition**
- **Target Weights**
- **Internal Conviction / Confidence**
- **Watchlist Promotion / Demotion Signals**
- **Strategic Warnings / Cautions**

### 8.5 Required SRI overlay outputs on top of APE
Once APE output is ingested, SRI should add:
- macro conditioning
- Howell phase influence
- TA timing caution or confirmation
- deployment intensity for the Visser sleeve
- portfolio-level allocation recommendation
- warnings when structure and thesis disagree

### 8.6 Visser eras
Visser eras are a strategic narrative framework.
They are **not the same thing** as Howell phases.

Visser eras should be treated as:
- internally valid strategic states for the AI / infrastructure / downstream opportunity arc
- longer-horizon narrative phases
- capable of being accelerated, delayed, or stressed by macro and liquidity conditions

### 8.7 Relationship between Visser eras and Howell phase
The relationship should be explicitly monitored rather than assumed.

Examples:
- a Visser era transition may align with favorable macro and phase conditions
- a Visser era may remain strategically valid while Howell turns less supportive
- a macro shock may slow the pace of a Visser era transition without invalidating the long-term thesis

### 8.8 Internal sub-theme handling
Visser may contain multiple sub-themes or internal strategic clusters.
Examples may include:
- infrastructure build-out
- semis / picks and shovels
- hyperscalers
- future AI downstream opportunity sets
- optional TSLA exposure when justified by the branch’s own logic

v3.2 should therefore treat Visser as a **containerized strategic sleeve**, not a flat ticker basket.

### 8.9 Conflict handling for Visser
The most important conflicts to surface are:
- APE says add, TA says overextended
- APE says a name is strategically favored, macro says lower branch size overall
- APE favors a future era beneficiary, TA says it is too early
- owner wants a conviction expression not currently favored by APE

The engine should handle these via sizing, timing, and warnings, not by pretending the conflict does not exist.

---

## 9. All-Weather Engine

### 9.1 Thesis premise
This branch represents a risk-balanced allocation model, not a single directional thematic bet.

### 9.2 Function
All-Weather may serve three roles:
- a strategic branch in its own right
- a benchmark / comparator
- a contributor to Global AB4 ballast posture

### 9.3 Proposed asset families
Initial candidates:
- equities
- duration
- inflation / real assets
- cash / preferred reserve instruments where appropriate

### 9.4 Proposed engine outputs
- Growth State
- Inflation State
- Rate State
- Risk-Balance Posture
- Deployment Intensity
- Preferred tilt toward growth, duration, real assets, or reserve

### 9.5 Technical overlay relevance
Duration-heavy decisions inside All-Weather may require human chart confirmation when stage structure or breakout timing matters more than macro allocation logic alone.

That human input should refine:
- timing of adds
- preferred instrument choice
- caution around false breakouts
- confidence in Stage transitions

---

## 10. Layer 1 — Shared Regime Engine

### 10.1 Current decision
Layer 1 remains shared across all top-level branches.

### 10.2 Why keep it shared
The shared regime layer still provides portfolio-wide context such as:
- broad risk-on / risk-off state
- market stress / calm condition
- common structural context

### 10.3 Warning
This assumption should be revisited during later iteration.
It may eventually prove that some routes need route-specific regime overlays.

---

## 11. Layer 2 — Signal Layer

### 11.1 Core role
Layer 2 converts branch state plus regime context into actual execution signals.

### 11.2 Scope
AB1 / AB2 / AB3 operate inside active branches.
AB4 remains global.

### 11.3 Practical meaning
If MSTR is active:
- Layer 2 uses Force Field + regime + structure to produce timing and expression guidance

If Visser is active:
- Layer 2 uses APE strategic output plus SRI timing overlays to determine whether the branch should deploy now, scale in, pause, or express through lower-risk structures

If All-Weather is active:
- Layer 2 may be more allocation-oriented and less options-centric

---

## 12. Layer 3 — Allocation Engine

Layer 3 is more than bucket accounting.
In v3.2 it should explicitly manage three distinct decision types.

### 12.1 Security selection
Examples:
- replacing one Visser holding with another
- changing the preferred security inside a branch
- promoting a watchlist name into active capital

### 12.2 Rebalancing
Examples:
- trimming winners back toward target
- adding to laggards still favored by the branch
- reducing concentration after strong relative moves

### 12.3 Theme rotation
Examples:
- reducing one branch and increasing another
- cutting overall Visser allocation while maintaining internal conviction on certain names
- shifting more capital into All-Weather or reserve posture

### 12.4 Why this separation matters
Security selection, rebalancing, and theme rotation are not the same decision.
The document should treat them separately so the engine does not confuse internal branch management with portfolio-level capital rotation.

---

## 13. AB Bucket Framework in v3.2

The call made it clear that the older framing of AB buckets was too blunt.

### 13.1 AB4
AB4 should be understood as the **base capital layer**.
It may include:
- core long-duration holdings
- cash
- preferreds
- all-weather allocations
- baseline branch allocations intended to be durable rather than highly tactical

### 13.2 AB3
AB3 should be understood as **positioning deviation / oversized conviction / leverage relative to baseline**.

Examples:
- going above baseline branch allocation because the setup is unusually favorable
- expressing high conviction through LEAPs instead of shares
- temporarily oversizing a position beyond strategic target

### 13.3 AB2
AB2 remains the **short- to medium-term directional / delta expression layer**.
It is more tactical than AB3 and usually shorter in duration.

### 13.4 AB1
AB1 remains the **short-duration theta / income expression layer**.

### 13.5 Gray area between AB1 and AB2
AB1 and AB2 are differentiated mainly by emphasis and risk character, not by a perfectly clean boundary.
That is acceptable, as long as the system uses them to represent:
- type of risk
- duration of exposure
- required attention level

### 13.6 Why this matters
This framing better reflects how real portfolios are run:
- AB4 = durable base capital
- AB3 = deliberate deviations from that base
- AB2 = tactical directional overlays
- AB1 = short-duration income overlays

---

## 14. Personalized Portfolio Report Integration

### 14.1 PPR must become branch-aware
Each PPR should reflect the portfolio owner’s declared branch allocation.

### 14.2 Proposed PPR logic
For each owner:
1. read branch allocation percentages
2. activate only the relevant branches
3. ingest branch-native outputs where applicable
4. report sleeve-level state
5. report deployment intensity for each active sleeve
6. summarize portfolio-level AB posture
7. highlight major macro conditioning from Layers 0 and 0.5
8. explicitly surface conflicts between strategic thesis and timing when present

### 14.3 Visser-specific PPR requirement
When Visser is active, the PPR should distinguish:
- what came from **APE strategic output**
- what came from **SRI macro / timing overlay**
- what was adjusted by **human technical intervention** if any

---

## 15. Human Technical Overlay

### 15.1 Why this section exists
The current system is strong in macro and structured inference, but human chart-reading can still add important edge, especially around:
- stage transitions
- breakout timing
- structural invalidations
- multi-timeframe nuance not yet fully systematized
- conflicts between macro posture and chart structure

### 15.2 Workflow rule
When technical structure materially affects the quality of the analysis, the workflow should explicitly request chart-based input rather than silently assuming the systematic read is sufficient.

### 15.3 Trigger conditions for requesting human chart input
The system should proactively request chart views when:
- stage designation materially changes deployment timing
- breakout or breakdown timing is central to the decision
- macro and technical signals appear to conflict
- a high-conviction add, trim, or risk reduction depends on chart structure
- the system has low confidence in its own structural read

### 15.4 How the intervention should work
Recommended sequence:
1. the engine forms its systematic view
2. the engine identifies unresolved chart uncertainty
3. the workflow asks for the specific chart view needed
4. the human provides a structure read, stage read, or transition view
5. final deployment guidance records whether human chart input altered the recommendation

### 15.5 Role in the architecture
This is not a replacement for the engine.
It is a structured overlay that refines timing, confidence, and exposure style while the charting layer continues to mature.

---

## 16. Open Questions and Next Iteration Targets

### 16.1 Formal APE data contract
The branch contract for Visser should be made more concrete in implementation terms.

### 16.2 Era-to-phase monitoring
Later versions should formalize how Visser eras are monitored against Howell phase shifts without forcing a false one-to-one mapping.

### 16.2a Howell transition markers
Later versions should define explicit transition markers, confirmation rules, and invalidation rules for each Howell phase so the system can mirror the discipline of the existing stage framework more closely.

### 16.3 Shared vs branch-specific regime overlays
Keep shared Layer 1 for now, but revisit whether some branches need more bespoke regime handling.

### 16.4 Route-to-bucket rules
Later versions should define in more implementation detail:
- when shares are preferred vs options
- when AB3 should be used as sizing deviation vs leverage
- how AB4 reserve interacts with active branch deployment

### 16.5 Commodities / metals branch question
The architecture appears intentionally extensible enough to support future branches such as commodities or metals.
That remains an open but likely future path.

---

## v3.2.1 Draft Summary

Version 3.2.1 keeps the v3.2 branch architecture but materially strengthens the Phase Engine.

The defining characteristics of v3.2.1 are:
- shared macro scaffold
- refined Howell logic at Layer 0.5
- Theme Routing and Ingest at Layer 0.75
- Visser defined as an external APE-fed branch
- explicit Visser era handling
- clear separation between branch composition and branch allocation
- Layer 3 separated into security selection, rebalancing, and theme rotation
- AB4 treated as base capital and AB3 as conviction deviation / leverage layer
- explicit conflict handling between strategic thesis, macro context, and timing
- structured human technical overlay
- Liquidity Destination / Absorption State in Layer 0.5
- Howell evidence stack for phase designation
- Phase Transition Percentage modeled in the spirit of the stage framework
- explicit downstream cascade from the Phase Engine

This draft should be treated as the v3.2.1 review base before implementation.
