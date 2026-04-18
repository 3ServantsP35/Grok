# SRI Decision Engine — Complete Methodology Tutorial
**Version 3.0 DRAFT | Date: 2026-04-18 | Author: CIO Engine**

---

## Purpose of v3

Version 3 introduces a major architectural change while preserving the existing macro and regime scaffold.

**What changes in v3:**
- Layer **0.75** is no longer a single universal Force Field Engine.
- Layer **0.75** becomes a **Thesis Routing Layer**.
- The routing layer activates one or more thesis-specific engines based on the portfolio owner's declared thesis allocation.

**What does not materially change in v3:**
- **Layer 0** (GLI Engine)
- **Layer 0.5** (Howell Phase Engine)
- **Layer 1** (shared regime layer, pending future review)
- **Layers 2–3** remain structurally similar, though their downstream interpretation widens to support multiple thesis sleeves.

This document is a **methodology + architecture spec hybrid**. It explains both how the system should work conceptually and how it should be implemented.

---

## Table of Contents

1. Architecture Overview (v3)
2. Key Design Principles
3. Layer 0 — GLI Engine (unchanged)
4. Layer 0.5 — Howell Phase Engine (unchanged)
5. Layer 0.75 — Thesis Routing Layer (new)
6. Thesis Allocation Framework
7. MSTR Thesis Engine — Force Field Branch
8. TSLA Thesis Engine — Proposed v0.1
9. Visser Thesis Engine — Proposed v0.1
10. All-Weather Engine — Proposed v0.1
11. Layer 1 — Shared Regime Engine
12. Layers 2–3 — Signal and Allocation Continuity
13. Planned Changes to AB3 and AB4
14. Personalized Portfolio Report Integration
15. Open Questions and Next Iteration Targets

---

## 1. Architecture Overview (v3)

The engine is now organized around a shared macro scaffold followed by thesis-specific routing.

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
│ Sector / macro phase classification                         │
│ Output: phase, confidence, seasonal “in-season” context     │
│ Function: gate zero, macro phase conditioning               │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 0.75: THESIS ROUTING LAYER                            │
│ Portfolio-owner thesis allocation activates route branches  │
│ Branches: MSTR | TSLA | Visser | All-Weather                │
│ Output: thesis-specific guidance + deployment intensity     │
│ Function: thesis selection + sleeve activation              │
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
│ AB1 / AB2 / AB3 signal logic inside active thesis sleeves   │
│ Output: entry / hold / trim / income / accumulation states  │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ LAYER 3: ALLOCATION ENGINE                                  │
│ Bucket accounting + sleeve deployment + Global AB4          │
│ Output: portfolio-aware capital posture                     │
└──────────────────────────────────────────────────────────────┘
```

### Core v3 idea
The system no longer assumes one universal directional engine for all investment ideas.

Instead:
- **MSTR** uses a thesis engine built around **Strategy / BTC demand mechanics**.
- **TSLA** uses a thesis engine built around **Tesla-specific value drivers**.
- **Visser** uses a thesis engine built around **AI / macro / innovation-cycle logic**.
- **All-Weather** uses a thesis engine built around **risk-balanced multi-asset allocation**.

---

## 2. Key Design Principles

### 2.1 Shared macro, thesis-specific drivers
The top of the stack remains shared.
The thesis-specific differentiation begins at **Layer 0.75**.

### 2.2 Multiple thesis sleeves can coexist
A portfolio owner can allocate capital to one, several, or all four theses simultaneously.

### 2.3 Engines are mutually exclusive by thesis
The engines themselves are not interchangeable.

Examples:
- Force Field is relevant to **MSTR**.
- Force Field is **not** relevant to **TSLA**.
- A TSLA engine should model **TSLA’s real drivers**, not borrow MSTR logic.

### 2.4 Portfolio-owner allocation activates the route
A thesis engine is only active if the portfolio owner has assigned capital to that thesis.

### 2.5 Global AB4 remains global
AB4 is still a **global portfolio reserve / defensive sleeve**.
It is not split separately inside each thesis sleeve.

---

## 3. Layer 0 — GLI Engine (unchanged)

No methodological change in v3.

Layer 0 continues to provide:
- global liquidity context
- macro growth context
- broad probability adjustment
- top-down backdrop for all downstream logic

### Role in v3
Layer 0 still conditions:
- whether macro is broadly supportive or restrictive
- whether a thesis should be interpreted in a risk-on or risk-off environment
- how aggressively downstream sleeves should deploy

**Important:** Layer 0 does **not** choose the thesis. It conditions the thesis.

---

## 4. Layer 0.5 — Howell Phase Engine (unchanged)

No methodological change in v3.

Layer 0.5 continues to provide:
- phase classification
- “in-season” vs “out-of-season” structure
- macro cycle context between GLI and per-thesis deployment

### Role in v3
Layer 0.5 should remain a shared phase conditioner that helps determine:
- whether a thesis sleeve should be defensive, opportunistic, or aggressive
- whether macro context supports trend continuation, rebound, speculation, or turbulence

**Important:** Layer 0.5 does **not** choose the thesis. It conditions the thesis.

---

## 5. Layer 0.75 — Thesis Routing Layer (new)

This is the central architectural change in v3.

### 5.1 Purpose
Layer 0.75 now has two jobs:

1. **Routing**
   - determine which thesis engines are active for a given portfolio owner
   - based on the owner's declared thesis allocation percentages

2. **Deployment Intensity**
   - determine how aggressively each active thesis sleeve should be deployed
   - based on macro context plus the thesis engine’s own state

### 5.2 Inputs
- portfolio owner thesis allocation
- Layer 0 output
- Layer 0.5 output
- thesis-specific driver data

### 5.3 Outputs
For each active thesis sleeve:
- thesis state
- thesis confidence
- deployment intensity
- preferred exposure style (shares, options, or defensive hold)
- route-specific warnings / invalidations

### 5.4 Routing rule
If portfolio owner allocation to a thesis is:
- **0%** → thesis engine is moot
- **> 0%** → thesis engine is active

### 5.5 Default thesis allocation
Default portfolio template:
- **25% MSTR**
- **25% TSLA**
- **25% Visser**
- **25% All-Weather**

Portfolio owners may adjust from that baseline.

### 5.6 Deployment intensity
Each thesis engine should output both:
- **thesis-specific guidance**
- **capital deployment intensity**

Example:
- TSLA thesis active at 25% strategic sleeve
- TSLA thesis engine currently says “deploy 40% of sleeve”
- therefore only part of that 25% sleeve is actively deployed into AB1/2/3, while remaining capital stays in the global reserve framework

---

## 6. Thesis Allocation Framework

### 6.1 Strategic thesis allocation
The portfolio owner determines strategic sleeve weights.

This is a **mandate-level decision**, not a market-timing decision.

Examples:
- Greg may choose a higher TSLA sleeve
- Gavin may prefer a higher MSTR sleeve
- Kathryn may prefer higher All-Weather and lower thematic concentration

### 6.2 Tactical deployment within sleeve
Once a sleeve exists, the thesis engine decides:
- whether to deploy now
- how much of the sleeve to deploy
- whether to prefer shares or options
- when to slow, pause, or increase deployment

### 6.3 Thesis allocation rubric (planned)
A later iteration should create a simple user-facing rubric that helps portfolio owners answer:
- how much of their capital should be dedicated to each thesis
- how concentrated or diversified they want to be
- whether they prefer offensive, balanced, or defensive deployment

---

## 7. MSTR Thesis Engine — Force Field Branch

### 7.1 Status
This is the only fully developed thesis engine at present.

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
- Stablecoin dominance
- MSTR self-state

### 7.4 Output role
The MSTR thesis engine should continue to output:
- directional force
- bounce exhaustion / continuation risk
- deployment intensity for MSTR sleeve
- guidance for whether AB1/AB2/AB3 should be active

### 7.5 v3 interpretation
No major conceptual change except this:
- Force Field is now **one route**, not the universal thesis engine for the entire architecture

---

## 8. TSLA Thesis Engine — Proposed v0.1

### 8.1 Status
This is a proposed engine, not settled doctrine.
It should be treated as a review framework for Greg.

### 8.2 Thesis premise
TSLA should be modeled through the primary drivers of its value and price action, using a blend of leading and lagging indicators.

The engine should answer:
- is TSLA acting like a high-beta momentum vehicle?
- is it in a narrative re-rating regime?
- is it being supported by macro/liquidity?
- are core company-specific drivers strengthening or weakening?

### 8.3 Proposed TSLA driver families

#### A. Structural price / trend state
- SRI stage state across ST / LT / VLT
- trackline posture
- reversal support / resistance geometry
- LOI / SRIBI progression

#### B. Growth / innovation premium state
Possible proxies:
- QQQ relative behavior
- TSLA / QQQ ratio
- TSLA / SPY ratio
- AI / growth cohort relative strength

#### C. Consumer / cyclicality state
Possible proxies:
- XLY
- IWM
- consumer discretionary breadth
- rates sensitivity via TLT / DXY context

#### D. Company-specific thesis state
Proposed qualitative or semi-quantitative buckets:
- autonomy / FSD optimism regime
- energy / storage narrative support
- margin / delivery narrative stress
- execution confidence regime

These may initially need manual or semi-manual interpretation before becoming fully systematic.

### 8.4 Proposed TSLA engine output
The TSLA thesis engine should produce:
- **Thesis State:** weak / mixed / strong
- **Narrative State:** de-rating / neutral / re-rating
- **Structure State:** Stage 2 continuation / Stage 3 risk / Stage 4 reset / Stage 4→1 rebound
- **Deployment Intensity:** 0–100% of TSLA sleeve
- **Preferred Expression:** shares / calls / LEAPs / low deployment

### 8.5 First-pass deployment logic
Example conceptual outputs:
- **Strong thesis + strong structure + favorable macro:** deploy heavily
- **Strong structure but weak narrative / macro:** partial deployment only
- **Narrative strong but structure broken:** watch / defer
- **Stage 3 risk or failed breakout:** reduce deployment intensity

### 8.6 Immediate next step
The next iteration should propose a **Greg review table**:
- candidate TSLA drivers
- why they matter
- whether they are leading / coincident / lagging
- whether they are measurable from available datasets

---

## 9. Visser Thesis Engine — Proposed v0.1

### 9.1 Status
This is also a proposal, not settled doctrine.

### 9.2 Thesis premise
The Visser route should represent an **AI Macro Nexis** framework, where the core investment thesis is based on innovation-cycle leadership, macro regime, and thematic capital concentration.

### 9.3 Proposed driver families

#### A. Innovation leadership breadth
Potential proxies:
- QQQ
- XLK
- NVDA
- MSFT
- AMZN
- PLTR
- semis / AI leadership basket behavior

#### B. Macro liquidity support
Shared top-down inputs:
- GLI
- Howell phase
- DXY
- VIX
- TLT

#### C. Narrative concentration / speculation state
Potential proxies:
- relative performance of AI leaders vs broad market
- extreme breadth narrowing vs broad participation
- gold/BTC / risk comparison as speculative regime tell

#### D. Risk appetite / duration preference
Potential proxies:
- QQQ / IWM
- growth / value spread
- TLT and real-rate sensitivity

### 9.4 Proposed Visser engine output
The engine should produce:
- **Innovation Cycle State:** early / broadening / concentrated / exhausted
- **Macro Support State:** supportive / mixed / restrictive
- **Speculation State:** healthy / frothy / exhausted
- **Deployment Intensity:** 0–100% of Visser sleeve
- **Preferred Expression:** leaders / baskets / options / lower-risk posture

### 9.5 Immediate next step
Create a first review memo mapping:
- Jordy Visser conceptual pillars
- candidate measurable inputs
- what can be automated now vs what stays interpretive

---

## 10. All-Weather Engine — Proposed v0.1

### 10.1 Thesis premise
This route represents a **Ray Dalio-style risk-balanced allocation model**, not a thematic directional sleeve.

### 10.2 Function
This is both:
- a strategic thesis sleeve in its own right
- and the conceptual anchor for a broadened global AB4 posture

### 10.3 Proposed asset families
Initial candidates:
- equities (broad beta, e.g. VT / SPY)
- duration (TLT or equivalent)
- inflation / real assets (GLD, DBC)
- cash / preferred reserve instruments where appropriate

### 10.4 Proposed engine outputs
- **Growth State**
- **Inflation State**
- **Rate State**
- **Risk-Balance Posture**
- **Deployment Intensity** within all-weather sleeve
- **Preferred tilt** toward growth, duration, real assets, or reserve

### 10.5 Role relative to AB4
Important distinction:
- the **All-Weather thesis** is a route
- **Global AB4** is the portfolio reserve bucket

The two are related but not identical.

A portfolio owner may:
- allocate capital strategically to the All-Weather thesis
- and still maintain a separate global AB4 reserve posture

---

## 11. Layer 1 — Shared Regime Engine

### 11.1 Current decision
Layer 1 remains shared across all theses.

### 11.2 Why keep it shared for now
The shared regime layer still provides portfolio-wide context such as:
- broad risk-on / risk-off state
- market stress / calm condition
- common structural context

### 11.3 Warning
This assumption should be revisited during iteration.
It may eventually prove that some routes need route-specific regime interpretation overlays.

For now:
- **shared Layer 1 remains the default**

---

## 12. Layers 2–3 — Signal and Allocation Continuity

### 12.1 Layer 2 still governs AB1 / AB2 / AB3
The tactical and strategic signal layer remains intact conceptually.

### 12.2 Layer 3 still governs bucket accounting
The allocation engine remains intact conceptually, but its downstream semantics widen because multiple thesis sleeves now exist.

### 12.3 New interpretation in v3
- **AB1 / AB2 / AB3** should now operate inside an active thesis sleeve
- **AB4** remains global

### 12.4 Practical meaning
If TSLA thesis sleeve is active:
- AB1 / AB2 / AB3 may be used inside TSLA sleeve according to that thesis engine

If MSTR sleeve is active:
- AB1 / AB2 / AB3 may be used inside MSTR sleeve according to Force Field + shared layer logic

If All-Weather sleeve is active:
- deployment may look more allocation-oriented and less options-centric

---

## 13. Planned Changes to AB3 and AB4

These are intentional changes already identified for later incorporation.

### 13.1 AB3 widening
Current / old framing:
- AB3 primarily treated as **call LEAP accumulation**

Planned v3 adjustment:
- AB3 should allow **shares or call LEAPs**
- instrument choice should depend on thesis, volatility, and deployment logic

### 13.2 AB4 widening
Current / old framing:
- AB4 primarily associated with cash / STRC reserve logic

Planned v3 adjustment:
- AB4 remains global
- but its scope widens to include **all-weather reserve / allocation options**, not only cash and STRC

---

## 14. Personalized Portfolio Report Integration

### 14.1 PPR must become thesis-aware
Each PPR should reflect the portfolio owner’s declared thesis allocation.

### 14.2 Proposed PPR logic
For each owner:
1. read thesis allocation percentages
2. activate only the relevant thesis engines
3. report sleeve-level state
4. report deployment intensity for each active sleeve
5. summarize portfolio-level AB posture

### 14.3 Example
If Greg allocates:
- 40% MSTR
- 20% TSLA
- 20% Visser
- 20% All-Weather

Then PPR should include:
- MSTR sleeve state and deployment intensity
- TSLA sleeve state and deployment intensity
- Visser sleeve state and deployment intensity
- All-Weather sleeve state and deployment intensity
- one unified Global AB4 posture

---

## 15. Open Questions and Next Iteration Targets

### 15.1 Need to define TSLA engine drivers with Greg
Immediate next step:
- propose TSLA driver table for Greg review

### 15.2 Need to define Visser engine drivers more precisely
Immediate next step:
- propose AI Macro Nexis driver table for review

### 15.3 Need thesis allocation rubric
The system still needs a simple rubric that helps owners choose thesis allocations.

### 15.4 Need to pressure-test shared Layer 1 assumption
Keep current assumption, but revisit often.

### 15.5 Need formal route-to-bucket rules
Later iteration should define exactly:
- when shares are preferred vs options
- how sleeve deployment maps into AB1 / AB2 / AB3
- how global AB4 reserve interacts with active sleeve deployment

---

## v3 Draft Summary

Version 3 changes the architecture from a **single-thesis directional engine with universal Force Field logic** into a **multi-thesis routing framework**.

The defining characteristics of v3 are:
- shared macro scaffold
- thesis-specific routing at Layer 0.75
- portfolio-owner allocation activation
- multiple active thesis sleeves in one portfolio
- mutually exclusive thesis engines by sleeve
- global AB4 reserve retained
- widened AB3 and AB4 design goals

This draft should be treated as the new base document for review before implementation.
