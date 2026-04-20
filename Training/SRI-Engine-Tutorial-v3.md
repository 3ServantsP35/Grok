# SRI Decision Engine — Complete Methodology Tutorial
**Version 3.1 DRAFT | Date: 2026-04-20 | Author: CIO Engine**

---

## Purpose of v3.1

Version 3.1 refines the v3 architecture in three important ways:

1. **Layer 0.75 is clarified as a theme-routing and deployment layer** rather than a single universal thesis engine.
2. **TSLA is no longer treated as a separate top-level theme.** It is now treated as an optional security or narrative expression within the Visser theme.
3. **Layer 0.5 (Howell Phase Engine) is upgraded conceptually** from a simple phase label into a more decision-useful macro allocator that should ultimately track:
   - phase label
   - factor preference
   - deployment posture

This draft intentionally uses a **placeholder** for the Visser Theme integration work that must be completed collaboratively with Greg. That work is deferred to **v3.2**.

**What remains materially unchanged in v3.1:**
- **Layer 0** (GLI Engine)
- core **MSTR Force Field branch**
- shared **Layer 1** default assumption
- downstream **Layers 2–3** as the main signal/allocation scaffold

This document remains a **methodology + architecture spec hybrid**.

---

## Table of Contents

1. Architecture Overview (v3.1)
2. Key Design Principles
3. Layer 0 — GLI Engine (unchanged)
4. Layer 0.5 — Howell Phase Engine (refined)
5. Layer 0.75 — Theme Routing Layer (refined)
6. Theme Allocation Framework
7. MSTR Theme Engine — Force Field Branch
8. Visser Theme — Placeholder for v3.2 integration
9. All-Weather Engine — Proposed v0.1
10. Layer 1 — Shared Regime Engine
11. Layers 2–3 — Signal and Allocation Continuity
12. AB Bucket Interpretation in v3.1
13. Personalized Portfolio Report Integration
14. Human Technical Overlay
15. Open Questions and Next Iteration Targets

---

## 1. Architecture Overview (v3.1)

The engine is now organized around a shared macro scaffold followed by theme-specific routing.

```text
┌──────────────────────────────────────────────────────────────┐
│ LAYER 0: GLI ENGINE                                         │
│ Macro liquidity / growth regime                             │
│ Output: GLI Z-score, GEGI, paradigm label                   │
│ Function: probability and macro weighting                   │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 0.5: HOWELL PHASE ENGINE                              │
│ Phase + factor preference + deployment posture              │
│ Output: phase, cyc/def pref, growth/value pref, posture     │
│ Function: gate zero, macro phase conditioning               │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 0.75: THEME ROUTING LAYER                             │
│ Portfolio-owner allocation activates route branches         │
│ Branches: MSTR | Visser | All-Weather                       │
│ Output: theme guidance + deployment intensity               │
│ Function: route activation + sleeve deployment              │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 1: SHARED REGIME ENGINE                               │
│ Common structural / regime interpretation                   │
│ Output: regime state, risk posture, shared context          │
│ Function: common downstream conditioning                    │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 2: SIGNAL LAYER                                       │
│ AB1 / AB2 / AB3 logic inside active theme sleeves           │
│ Output: entry / hold / trim / income / accumulation states  │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 3: ALLOCATION ENGINE                                  │
│ Bucket accounting + sleeve deployment + Global AB4          │
│ Output: portfolio-aware capital posture                     │
└──────────────────────────────────────────────────────────────┘
```

### Core v3.1 idea
The system no longer assumes one universal directional engine for all investment ideas.

Instead:
- **MSTR** uses a thesis engine built around **Strategy / BTC demand mechanics**.
- **Visser** is reserved as a top-level theme, but its detailed integration is deferred to **v3.2**.
- **All-Weather** uses a thesis engine built around **risk-balanced multi-asset allocation**.

### Important v3.1 simplification
**TSLA is not a separate top-level route.**
It should instead be treated as an optional security, sub-narrative, or expression **inside the Visser theme**.

---

## 2. Key Design Principles

### 2.1 Shared macro, theme-specific drivers
The top of the stack remains shared.
Theme-specific differentiation begins at **Layer 0.75**.

### 2.2 Multiple theme sleeves can coexist
A portfolio owner can allocate capital to one, several, or all active top-level themes simultaneously.

### 2.3 Engines are mutually exclusive by top-level theme
The engines themselves are not interchangeable.

Examples:
- Force Field is relevant to **MSTR**.
- All-Weather logic is relevant to **All-Weather**.
- TSLA-specific expression belongs **inside Visser**, not as a standalone top-level route in v3.1.

### 2.4 Portfolio-owner allocation activates the route
A theme engine is only active if the portfolio owner has assigned capital to that theme.

### 2.5 Global AB4 remains global
AB4 remains a **global portfolio reserve / ballast sleeve**.
It is not independently duplicated inside each theme sleeve.

### 2.6 Theme-first, AB-second
In v3.1, the intended portfolio logic is:
1. assign capital at the **theme** level
2. use AB1 / AB2 / AB3 / AB4 as the **execution and posture framework** around those themes

This means top-level portfolio construction should be thought of as **theme-led**, while AB buckets describe how capital is deployed, defended, or harvested.

---

## 3. Layer 0 — GLI Engine (unchanged)

No methodological change in v3.1.

Layer 0 continues to provide:
- global liquidity context
- macro growth context
- broad probability adjustment
- top-down backdrop for all downstream logic

### Role in v3.1
Layer 0 still conditions:
- whether macro is broadly supportive or restrictive
- whether a theme should be interpreted in a risk-on or risk-off environment
- how aggressively downstream sleeves should deploy

**Important:** Layer 0 does **not** choose the theme. It conditions the theme.

---

## 4. Layer 0.5 — Howell Phase Engine (refined)

Version 3.1 preserves the Layer 0.5 location in the stack but **upgrades its conceptual role**.

### 4.1 Prior framing
In earlier drafts, Layer 0.5 was treated mainly as:
- a phase classifier
- an “in-season / out-of-season” gate
- a macro cycle conditioner

### 4.2 v3.1 framing
Layer 0.5 should ultimately provide **three outputs**:

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

### 4.3 Key Howell refinement
The Howell framework implies that:
- **liquidity level vs average** is most useful for determining **cyclical vs defensive** preference
- **liquidity direction / first difference** is most useful for determining **growth vs value** preference

This is a meaningful refinement and should be preserved for implementation.

### 4.4 Current strategic interpretation
Based on the latest Howell work, the current macro interpretation is best framed as:

> **late-cycle Speculation, not Turbulence yet**

This implies:
- narrower leadership
- more respect for value / scarcity / cyclicals
- less complacency toward broad passive growth exposure
- preparation for eventual Turbulence rather than immediate full risk-off positioning

### 4.5 Role in v3.1
Layer 0.5 should influence:
- sleeve activation intensity
- factor tilt inside sleeves
- whether posture should be offensive, selective, or defensive
- how much ballast emphasis the portfolio should carry

**Important:** Layer 0.5 still does **not** choose the theme. It conditions the theme and the form of deployment.

---

## 5. Layer 0.75 — Theme Routing Layer (refined)

This remains the central architectural change introduced in v3, but v3.1 clarifies it.

### 5.1 Purpose
Layer 0.75 now has two jobs:

1. **Routing**
   - determine which top-level theme engines are active for a given portfolio owner
   - based on the owner’s declared allocation percentages

2. **Deployment Intensity**
   - determine how aggressively each active theme sleeve should be deployed
   - based on macro context plus the theme engine’s own state

### 5.2 Inputs
- portfolio owner theme allocation
- Layer 0 output
- Layer 0.5 output
- theme-specific driver data
- optional human technical overlay when chart structure matters

### 5.3 Outputs
For each active theme sleeve:
- theme state
- theme confidence
- deployment intensity
- preferred exposure style
- route-specific warnings / invalidations

### 5.4 Routing rule
If portfolio owner allocation to a theme is:
- **0%** → theme engine is moot
- **> 0%** → theme engine is active

### 5.5 Default top-level theme allocation
Default portfolio template for v3.1:
- **34% MSTR**
- **33% Visser**
- **33% All-Weather**

Portfolio owners may adjust from that baseline.

### 5.6 Important v3.1 note on Visser
Visser remains a top-level route for allocation purposes, but the detailed engine integration work is deferred to **v3.2**. In v3.1, Visser should remain a placeholder sleeve in the architecture.

---

## 6. Theme Allocation Framework

### 6.1 Strategic theme allocation
The portfolio owner determines strategic sleeve weights.

This is a **mandate-level decision**, not a market-timing decision.

Examples:
- one owner may prefer a higher **MSTR** concentration
- another may prefer a larger **Visser** sleeve
- another may prefer heavier **All-Weather** ballast and lower thematic concentration

### 6.2 Tactical deployment within sleeve
Once a sleeve exists, the theme engine decides:
- whether to deploy now
- how much of the sleeve to deploy
- whether to prefer shares or options
- when to slow, pause, or increase deployment

### 6.3 Theme allocation rubric (planned)
A later iteration should create a simple user-facing rubric that helps portfolio owners answer:
- how much capital should be dedicated to each top-level theme
- how concentrated or diversified they want to be
- whether they prefer offensive, balanced, or defensive deployment

### 6.4 Future design question
A later iteration may allow a portfolio engine to recommend allocations **across themes**, but in v3.1 this remains a portfolio-owner decision.

---

## 7. MSTR Theme Engine — Force Field Branch

### 7.1 Status
This is the most fully developed theme engine in the current architecture.

### 7.2 Thesis premise
MSTR is not just “BTC beta.”
Its valuation and price action are driven by a specific reflexive flywheel:
- Strategy capital raising
- preferred / credit conditions
- BTC demand absorption
- premium expansion / compression
- stablecoin and liquidity backdrop
- relative expression vs IBIT

### 7.3 Core driver set
The existing Force Field logic should remain the MSTR branch under Layer 0.75.

Primary current inputs include:
- STRF/LQD
- MSTR/IBIT
- STRC
- stablecoin dominance
- MSTR self-state

### 7.4 Output role
The MSTR theme engine should continue to output:
- directional force
- bounce exhaustion / continuation risk
- deployment intensity for MSTR sleeve
- guidance for whether AB1 / AB2 / AB3 should be active

### 7.5 v3.1 interpretation
No major conceptual change except this:
- Force Field is now **one route**, not the universal thesis engine for the entire architecture

---

## 8. Visser Theme — Placeholder for v3.2 integration

### 8.1 Status
This section is intentionally a **placeholder** in v3.1.

The detailed Visser Theme architecture and its collaborative integration work with Greg will be incorporated in **v3.2**.

### 8.2 What is locked in already
Even though the full integration is deferred, the following should be treated as agreed:
- Visser remains a **top-level theme** in the allocation architecture
- TSLA is **not** a separate top-level theme in v3.1
- TSLA may appear inside Visser as an optional security, sub-theme, or narrative expression
- v3.2 must define the actual Visser engine contract, drivers, and interaction with Layer 0.75

### 8.3 What v3.1 should assume operationally
Until v3.2 is completed, the Visser sleeve should be treated as:
- allocation-aware
- present in PPRs and portfolio construction
- descriptively acknowledged in architecture
- not yet fully systematized in this document

### 8.4 v3.2 target
The next version should formalize:
- the Visser engine integration approach
- required inputs and outputs
- sub-theme handling
- tension resolution between thematic thesis and technical structure

---

## 9. All-Weather Engine — Proposed v0.1

### 9.1 Thesis premise
This route represents a **Ray Dalio-style risk-balanced allocation model**, not a thematic directional sleeve.

### 9.2 Function
In v3.1, All-Weather should be understood as potentially serving three roles:
- a strategic theme sleeve in its own right
- a portfolio benchmark / comparator
- a major contributor to Global AB4 ballast posture

### 9.3 Proposed asset families
Initial candidates:
- equities (broad beta)
- duration (TLT or equivalent)
- inflation / real assets (GLD, commodities)
- cash / preferred reserve instruments where appropriate

### 9.4 Proposed engine outputs
- **Growth State**
- **Inflation State**
- **Rate State**
- **Risk-Balance Posture**
- **Deployment Intensity** within all-weather sleeve
- **Preferred tilt** toward growth, duration, real assets, or reserve

### 9.5 TLT note for strategic context
Human technical analysis currently suggests:
- **TLT is deep in Stage 1**
- a likely **Stage 2 breakout may emerge in 2H26**

This should not be hard-coded as a system output yet, but it is an example of how human chart insight can refine timing around the All-Weather / duration sleeve.

---

## 10. Layer 1 — Shared Regime Engine

### 10.1 Current decision
Layer 1 remains shared across all top-level themes.

### 10.2 Why keep it shared for now
The shared regime layer still provides portfolio-wide context such as:
- broad risk-on / risk-off state
- market stress / calm condition
- common structural context

### 10.3 Warning
This assumption should be revisited during later iteration.
It may eventually prove that some routes need route-specific regime overlays.

For v3.1:
- **shared Layer 1 remains the default**

---

## 11. Layers 2–3 — Signal and Allocation Continuity

### 11.1 Layer 2 still governs AB1 / AB2 / AB3
The tactical and strategic signal layer remains intact conceptually.

### 11.2 Layer 3 still governs bucket accounting
The allocation engine remains intact conceptually, but its semantics widen because multiple theme sleeves can now exist.

### 11.3 New interpretation in v3.1
- **AB1 / AB2 / AB3** operate inside active theme sleeves
- **AB4** remains global

### 11.4 Practical meaning
If MSTR sleeve is active:
- AB1 / AB2 / AB3 may be used inside the MSTR sleeve according to Force Field + shared layer logic

If Visser sleeve is active:
- v3.1 architecture acknowledges the sleeve, but the detailed engine and signal mapping are deferred to v3.2

If All-Weather sleeve is active:
- deployment may look more allocation-oriented and less options-centric

---

## 12. AB Bucket Interpretation in v3.1

### 12.1 Theme-first allocation logic
The intended top-down sequence is:
1. set theme allocations
2. let Layer 0 / 0.5 condition risk posture
3. use AB buckets as the execution and posture framework

### 12.2 AB1
AB1 is a short-duration income / theta sleeve.
It is likely to remain relatively small and personalized.

### 12.3 AB2
AB2 is a higher-risk / reward directional sleeve for short- to medium-term delta-oriented positioning.
It should remain opportunistic rather than dominant.

### 12.4 AB3
AB3 should be treated as the core appreciation sleeve.
It may include:
- shares
- LEAPs
- long-duration thesis holdings

It is not “set and forget,” but neither is it intended as the most tactical trading sleeve.

### 12.5 AB4
AB4 remains the global ballast / reserve / income sleeve.
Its widening scope may include:
- cash
- preferreds
- duration
- all-weather style reserve posture

### 12.6 Practical sizing implication
AB1 + AB2 combined should generally be thought of as relatively modest in total portfolio weight, while AB3 and AB4 carry the more durable capital structure.

---

## 13. Personalized Portfolio Report Integration

### 13.1 PPR must become theme-aware
Each PPR should reflect the portfolio owner’s declared theme allocation.

### 13.2 Proposed PPR logic
For each owner:
1. read theme allocation percentages
2. activate only the relevant theme engines
3. report sleeve-level state
4. report deployment intensity for each active sleeve
5. summarize portfolio-level AB posture
6. highlight major macro conditioning from Layers 0 and 0.5

### 13.3 Example
If an owner allocates:
- 50% MSTR
- 20% Visser
- 30% All-Weather

Then the PPR should include:
- MSTR sleeve state and deployment intensity
- Visser sleeve placeholder state in v3.1
- All-Weather sleeve state and deployment intensity
- one unified Global AB4 posture

---

## 14. Human Technical Overlay

### 14.1 Why this section exists
The current system is strong in macro and structured inference, but human chart-reading can still add important edge, especially around:
- stage transitions
- breakout timing
- structural invalidations
- multi-timeframe nuance not yet fully systematized

### 14.2 Workflow rule
When technical structure materially affects the quality of the analysis, the workflow should explicitly request chart-based input from the portfolio owner or analyst.

### 14.3 Practical examples
The system should proactively request chart views for cases like:
- TLT setup confirmation
- suspected Stage 1 to Stage 2 transitions
- conflicting macro and technical signals
- high-conviction deployment timing decisions

### 14.4 Role in the architecture
This is not a replacement for the engine.
It is a **human technical overlay** that can improve decisions while the charting layer continues to mature.

---

## 15. Open Questions and Next Iteration Targets

### 15.1 v3.2 must complete Visser integration
Immediate next version should define:
- Visser engine structure
- its Layer 0.75 contract
- sub-theme handling
- internal treatment of TSLA and related expressions

### 15.2 Need a formal theme allocation rubric
The system still needs a simple rubric that helps owners choose theme allocations.

### 15.3 Need to pressure-test shared Layer 1 assumption
Keep current assumption, but revisit often.

### 15.4 Need formal route-to-bucket rules
Later iteration should define exactly:
- when shares are preferred vs options
- how sleeve deployment maps into AB1 / AB2 / AB3
- how global AB4 reserve interacts with active sleeve deployment

### 15.5 Need to operationalize Layer 0.5 outputs
The refined Howell logic should eventually be made explicit in system outputs:
- phase label
- factor preference
- deployment posture

---

## v3.1 Draft Summary

Version 3.1 keeps the multi-theme architecture introduced in v3, but makes it materially more coherent.

The defining characteristics of v3.1 are:
- shared macro scaffold
- refined Howell Phase logic at Layer 0.5
- theme routing at Layer 0.75
- TSLA removed as a standalone top-level theme
- Visser preserved as a top-level placeholder for v3.2
- multiple active sleeves in one portfolio
- global AB4 reserve retained
- stronger theme-first / AB-second framing
- explicit human technical overlay in the workflow

This draft should be treated as the v3.1 review base before implementation and before the fuller Visser collaboration work is incorporated in v3.2.
