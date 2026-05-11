# P-MSTR-SLEEVE — MSTR Sleeve Refinement v1

**Project:** P-MSTR-SLEEVE  
**Date:** 2026-05-07  
**Status:** Open  
**Author:** Cyler

---

## 1. Why this project exists

The MSTR sleeve should not be treated as a simplistic long-only expression whose main premise is that price rises over time.

The actual edge is more specific:

> The sleeve is valuable because it can be managed as an **aggregate delta engine** across multiple stages, allowing the portfolio to profit through changing conditions rather than only through passive upside ownership.

This project exists to refine that doctrine and translate it into reporting outputs that are genuinely useful to users.

---

## 2. Product principle

The guiding principle for this project is:

> **The real deliverable is not “good analysis.” It is decision-ready clarity.**

Analysis matters only insofar as it supports the clarity being offered.

That means future Layer reports and PPR outputs should be judged by whether they help a user answer practical questions like:
- what posture should I be in now?
- what aggregate delta should I be targeting?
- what structures should I use to express that posture?
- what should I adjust first if the chart state changes?

---

## 3. Core thesis

## 3.1 MSTR sleeve doctrine
The MSTR sleeve is a specialized volatility-management sleeve.

It should be understood as:
- a persistent strategic sleeve
- with stage-dependent internal structure
- managed through aggregate delta, convexity, and overlays
- using long calls, short calls, puts, and other approved structures to adapt posture

## 3.2 Strategic claim
A large concentrated sleeve, such as **40%**, is justified only if the system can manage that sleeve intelligently across multiple conditions.

That means the sleeve must be designed to:
- preserve long-term upside participation
- monetize stall / chop / mean reversion
- reduce or reverse net delta during topping / drawdown phases
- re-expand intelligently when favorable structure returns

---

## 4. Project goals

This project should produce doctrine and reporting conventions for:

1. **Stage-aware aggregate delta management** across stages 1-4
2. A canonical vocabulary for:
   - sleeve posture
   - target aggregate delta
   - acceptable deviation
   - adjustment sequence
3. A repeatable translation from:
   - chart state
   - shared-layer context
   - personalized benchmark
   - actual held structure
   into a clear recommended sleeve posture
4. A PPR / personalized reporting format that gives users:
   - benchmark
   - actual posture
   - target posture
   - adjustment ladder
   - decision-ready recommendation

---

## 5. Draft stage-based sleeve framework

This section is the first working draft of the stage-based aggregate-delta framework.

It is not final doctrine yet. The exact ranges should later be pressure-tested and refined through backtesting.

## 5.1 High-level shape

The user-proposed and provisionally accepted shape is:
- **Stage 1:** aggregate delta mean-reverts toward `0` around the natural center of the stage
- **Stage 2:** aggregate delta expands to **greater than 1** depending on leverage and positional bets
- **Stage 3:** aggregate delta migrates back toward `0`
- **Stage 4:** aggregate delta likely lives in the **-0.5 to -1.0** range because markdown volatility becomes extreme

This shape makes conceptual sense.

The key idea is:

> the sleeve should not target one static delta posture. It should rotate through stage-dependent delta regimes in order to extract volatility-adjusted returns across the full cycle.

## 5.2 Stage 1 draft

### Operational meaning
Stage 1 is the early / damaged / unresolved zone where the sleeve should be cautious about assuming immediate trend continuation.

### User framing worth preserving
- delta should **mean-revert toward 0** at the natural center of the stage
- doctrine should reference a **stage center of mass** concept, not fixed cycle-specific price points as permanent anchors
- cycle-specific price examples are acceptable only when explicitly labeled as time-bound examples

### Draft posture implication
- Stage 1 should not be treated as inherently neutral in all cases
- when price is relatively close to the stage center of mass, the sleeve should usually stay near neutral rather than strongly offensive
- when price moves far outside the center of mass and asymmetry becomes extreme, Stage 1 can justify a sharp increase in positive delta, potentially even **> 1**, especially when reserve capital is available

### Draft target zone
Provisional target:
- **within roughly 20% of the stage center of mass:** keep posture relatively close to neutral, roughly in a **+0.5 to -0.5** style zone
- **far outside the center of mass with strong asymmetry:** allow Stage 1 to stretch materially more positive, potentially **> 1 delta**

These are still draft declarations and should be validated through backtesting.

### Rotational view of delta
Stage 1 should also be understood rotationally.

If the sleeve is emerging from Stage 4 and the system gains confidence that markdown is ending and transition is underway, delta should **migrate upward** from negative posture toward neutral and then constructive posture rather than jumping all at once.

### Structural expression
Often best expressed through:
- preserved long-duration call core
- active short-call overlays
- selective put LEAPs or protective structures
- opportunistic re-expansion of bullish exposure when deep oversold asymmetry becomes unusually favorable

## 5.3 Stage 2 draft

### Operational meaning
Stage 2 is the expansion / favorable thrust zone where offensive posture should dominate.

### Draft posture implication
- this is where the sleeve earns the right to carry **greater than 1 delta**
- leverage and positional bets become a feature, not a bug, if structure and context support them

### Draft target zone
Provisional target: **> 1 delta**, scaled by:
- user leverage preference
- structure quality
- shared-layer support
- concentration tolerance

### Structural expression
Often best expressed through:
- dominant long call exposure
- reduced suppressive overlays
- less emphasis on defensive puts unless retained for tail-risk reasons

## 5.4 Stage 3 draft

### Operational meaning
Stage 3 is the cooling / topping / transition zone where the sleeve should stop behaving like a pure expansion engine.

### Draft posture implication
- delta should begin migrating back toward **0**
- the goal is to monetize stall, deterioration, and failed continuation while still preserving the possibility of re-acceleration if the market proves stronger than expected
- Stage 3 should be understood as a **rotational migration zone**, not only as a static target zone

### Draft target zone
Provisional target: **declining toward 0**, potentially moving from clearly positive to flat depending on timing quality.

These declarations should be backtested rather than treated as final doctrine.

### Rotational view of delta
If the sleeve is coming out of a strong Stage 2 markup posture, Stage 3 is where delta should usually **step down progressively** from `1+` rather than collapsing abruptly, unless chart deterioration becomes severe enough to justify faster defensive rotation.

### Structural expression
Often best expressed through:
- keeping long-duration core
- adding or tightening short calls
- introducing or increasing put exposure
- using overlays first before cutting structural core

## 5.5 Stage 4 draft

### Operational meaning
Stage 4 is the markdown / panic / volatility-expansion-to-the-downside zone.

### Draft posture implication
- the sleeve should stop trying to act like a merely de-risked bull position
- it should be capable of carrying meaningfully negative net exposure to survive and profit during violent markdowns

### Draft target zone
Provisional target: **-0.5 to -1.0 delta**.

This is a strong claim and will need backtest pressure-testing, but conceptually it fits the user’s doctrine.

### Structural expression
Often best expressed through:
- heavy short-call suppression
- substantial put or downside participation
- selective trimming of core longs if needed
- explicit focus on surviving volatility expansion, not just softening the blow

## 5.6 Design questions still open

This draft immediately raises several questions that the project must answer:
- how do we define the stage boundaries operationally enough for the system to recommend target delta confidently?
- how should the framework translate from **gross delta** to **net sleeve delta** in mixed structures?
- when should the sleeve prefer more short-call pressure versus more put exposure?
- how much user personalization should be allowed around the default target zones?
- when does a stage change justify touching AB3 core rather than only the overlay layer?

## 5.7 Chart-reading architecture question

The user explicitly raised whether we need to build **chart-reading capabilities into the architecture with Archie’s help**.

That question is now part of this project.

The core issue is simple:
- if target delta is stage-dependent
- and stage classification depends materially on chart structure, FF ROC behavior, and ST/LT SRI patterns
- then the system may need a stronger, more explicit chart-state interpretation layer than the current reporting flow provides

Working question:

> Do we need a formal machine-assisted chart-state interpreter in the architecture so the sleeve can map charts into target-delta posture more reliably?

This should be treated as an open architecture task, not a side note.

## 5.8 Stage classification and target-zone table (draft)

The next step is to turn the stage concept into a usable operating table.

This table is still provisional and should later be refined through backtesting and live review.

| Stage | Operational description | Draft target aggregate delta | Preferred structural expression | Main reporting question |
|---|---|---:|---|---|
| **Stage 1** | damaged / unresolved / early rebuilding zone, with price likely pulled toward a stage center | mean-revert toward `0` near the stage center, but can stretch materially positive when price is far outside the center and asymmetry is strong | keep long-duration core, use short calls and selective puts near the center, then re-expand bullish posture when deep oversold asymmetry becomes compelling | are we close enough to the stage center to stay near neutral, or far enough away that asymmetry justifies re-levering? |
| **Stage 2** | expansion / favorable thrust / offensive regime | `> 1` when supported by structure, leverage preference, and concentration tolerance | dominant long call posture, reduced suppressive overlays, lighter defensive posture unless needed for tail risk | how much offensive leverage is justified here, and what is the best way to express it? |
| **Stage 3** | cooling / topping / deterioration / transition | rotational migration back toward `0` from clearly positive posture | preserve core, tighten short calls, introduce or increase puts, use overlays before touching structural core | how fast should the sleeve rotate down from Stage 2 posture, and when is the top credible enough to push through flat? |
| **Stage 4** | markdown / panic / violent downside volatility | `-0.5` to `-1.0`, subject to backtest refinement | heavy short-call suppression, substantial downside participation, selective core trimming if needed | how negative should the sleeve get, and how quickly should it move there? |

## 5.9 Stage classification rule set (draft)

For reporting purposes, the system should not merely label a stage. It should explain **why** it thinks the stage applies.

A usable stage-classification rule set will likely need at least these inputs:
- **price structure**
  - higher highs / lower highs
  - support / resistance behavior
  - stage center or center-of-mass estimate
- **FF ROC behavior**
  - accelerating, decelerating, deteriorating, or recovering thrust
- **ST vs LT SRI pattern alignment**
  - alignment
  - divergence
  - breakdown of ST first with LT holding
- **shared-layer context**
  - whether Layers 0-1 are supportive enough to let the sleeve stay offensive

### Draft classification logic by stage

#### Stage 1
Likely when:
- damage has occurred or the structure is unresolved
- price is not yet in clean offensive expansion
- the system expects mean reversion toward a stage center
- FF ROC is not showing trustworthy upside thrust

#### Stage 2
Likely when:
- price structure is constructive and follow-through is working
- FF ROC supports continuing thrust
- ST and LT SRI patterns are aligned constructively
- shared layers are supportive enough to trust expansion

#### Stage 3
Likely when:
- price is cooling after an offensive phase
- FF ROC is decelerating or deteriorating
- ST pattern weakens before LT fully breaks
- failed pushes, lower highs, or topping behavior begin to appear

#### Stage 4
Likely when:
- markdown / downside volatility becomes dominant
- FF ROC and structure both confirm deterioration
- the market is no longer merely topping but actively breaking down
- defensive or negative-delta posture is required for survival and profit capture

## 5.10 Operational posture table (draft)

The framework now needs a more explicit operating table so it can drive PPR outcomes.

This is still draft doctrine and should later be refined through backtesting.

| Stage | Default delta band (draft) | Acceptable deviation logic | Preferred structures | First rotation lever | Escalation trigger |
|---|---:|---|---|---|---|
| **Stage 1** | near-neutral by default when price is near stage center, roughly **+0.5 to -0.5** | may stretch materially more positive when price is far outside the stage center and asymmetry becomes compelling | long-duration call core, selective short calls, selective put protection, opportunistic bullish re-expansion when deeply oversold | overlays first, then opportunistic long re-expansion | strong asymmetry away from stage center, improving structure, and evidence transition from Stage 4 into Stage 1 is maturing |
| **Stage 2** | **> 1** when structure and leverage tolerance support it | can stay below max offense if shared layers are only partially supportive or concentration tolerance is lower | dominant long call posture, reduced suppressive short calls, lighter protective structures | release suppressive overlays first | deterioration in FF ROC, failed pushes, ST weakness, or loss of clean expansion quality |
| **Stage 3** | migrate from clearly positive toward **0** | can remain somewhat positive if deterioration is mild; can push through flat faster if top evidence strengthens | preserve long core, tighten or add short calls, increase puts, use overlays before trimming structural core | short-call tightening first | repeated failed continuation, worsening FF ROC, ST/LT divergence, lower highs, or clearer transition into markdown risk |
| **Stage 4** | **-0.5 to -1.0** | can be less negative if downside volatility is moderating or transition into Stage 1 is beginning | heavy short-call suppression, substantial put participation, selective core trimming if needed | defensive overlays and put layer first | stabilization, exhaustion, improving FF ROC, and increasing evidence markdown is ending |

## 5.11 Rotational migration rules (draft)

The stage model should not be treated as four isolated static boxes. The real edge comes from **rotational migration of aggregate delta** as evidence changes.

### Stage 4 -> Stage 1 migration
- begin raising delta from strongly negative posture as markdown exhaustion and rebuilding evidence accumulate
- first remove the most suppressive defensive overlays
- then reduce excess put pressure
- re-expand bullish posture only as transition confidence improves

### Stage 1 -> Stage 2 migration
- move from near-neutral / asymmetry-sensitive posture into offensive posture only when constructive follow-through is proving itself
- release suppressive overlays first
- let long-duration bullish structures reclaim leadership
- do not force `> 1` delta until expansion quality is actually present

### Stage 2 -> Stage 3 migration
- rotate down from `1+` progressively rather than waiting for full breakdown confirmation
- begin with tighter short calls and added protection
- preserve the structural core unless deterioration becomes strong enough to justify deeper cuts
- recognize Stage 3 as the zone where failure to rotate early can give back a large amount of prior edge

### Stage 3 -> Stage 4 migration
- when topping behavior becomes markdown behavior, stop acting like a softened bull book
- push toward genuinely defensive or negative-delta posture
- let overlays and put structures do the first heavy lifting
- trim structural core only if needed to survive volatility expansion or improve expected payoff

## 5.12 Observable transition triggers (draft)

The system should later formalize these as explicit signals, but the early draft is:

### Transition toward more offensive posture
Triggered by combinations of:
- improving price structure
- FF ROC recovery or acceleration
- ST/LT SRI alignment improving
- higher confidence that a damaged/rebuilding zone is becoming true expansion

### Transition toward more neutral posture
Triggered by combinations of:
- price nearing stage center / fair-value area within the stage
- weakening asymmetry
- reduced edge from prior extreme positioning
- uncertainty rising without clear continuation signal

### Transition toward more defensive posture
Triggered by combinations of:
- FF ROC deterioration
- failed pushes and lower highs
- ST weakness appearing ahead of LT weakness
- markdown risk becoming more credible than continued markup

### Transition toward strongly negative posture
Triggered by combinations of:
- confirmed structural deterioration
- markdown volatility expansion
- poor rebound quality
- evidence that the market is no longer merely topping but actively breaking down

## 5.13 Implementation matrix by sleeve component (draft)

This section translates the stage framework into how the major sleeve components should usually behave.

This is still draft doctrine and should later be tightened with backtesting and portfolio review.

| Stage | Long call core | Short-call layer | Put layer | Reserve / deployment posture | First thing to change when rotating |
|---|---|---|---|---|---|
| **Stage 1** | keep strategic long core intact; expand only when asymmetry is unusually compelling | use selectively to keep posture near neutral when price is near stage center; reduce suppression if deep oversold asymmetry becomes compelling | keep selective protection; size up only if rebuild remains uncertain | keep reserve available because Stage 1 often rewards patience and selective redeployment | short-call suppression first, then opportunistic long re-expansion |
| **Stage 2** | let long call core dominate; this is the main offensive engine | reduce suppressive short-call pressure unless needed for user-specific risk constraints | keep light unless needed for tail risk or portfolio-specific protection | deploy more aggressively when expansion quality is confirmed | release short-call suppression first |
| **Stage 3** | preserve core initially; avoid cutting it too early unless deterioration becomes severe | tighten, add, or roll short calls more actively to bleed off delta from Stage 2 posture | begin increasing put participation as topping risk grows | slow fresh deployment; emphasize rotation over new offense | short-call layer first, then put layer, core last |
| **Stage 4** | trim selectively if needed, but not automatically; core is subordinate to survival and markdown profit capture | use heavy suppression to prevent the sleeve from behaving like a softened bull book | make the put layer substantial enough to matter in true markdown conditions | keep reserve strong and flexible for later re-entry | defensive overlays and put layer first, then selective core trimming if needed |

### Implementation logic notes
- The **long call core** is usually the last structural layer to be touched, except when markdown conditions become severe enough that survival and expected payoff justify direct cuts.
- The **short-call layer** is the main rotation lever for most transitions because it changes delta efficiently without forcing immediate abandonment of the strategic core.
- The **put layer** is the main bridge between merely defensive posture and truly negative posture.
- **Reserve posture** is not passive cash management. It is part of the sleeve’s optionality engine and should be reported as such.

## 5.14 Position-management playbook (draft)

This section turns the stage framework into action sequencing.

The purpose is not to prescribe one rigid move in every circumstance. The purpose is to define the **default order of operations** when the sleeve’s current aggregate delta differs from the target posture.

## 5.14.1 If target delta is higher than current delta

### Default order of operations
1. **reduce suppressive short-call pressure first**
2. **reduce excess put pressure second**
3. **expand long-duration bullish exposure third**
4. **deploy additional reserve capital last, only if needed after the first three steps**

### Rationale
- short calls are usually the cheapest and cleanest first lever for restoring upside participation
- puts may still be useful, so they should not always be removed before short-call normalization is tested
- expanding the long core should usually come after overlays are no longer suppressing the sleeve excessively

## 5.14.2 If target delta is lower than current delta

### Default order of operations
1. **tighten or add short-call pressure first**
2. **increase put participation second**
3. **trim long-duration bullish exposure third**
4. **increase reserve posture only as a consequence of prior reductions, not as the primary first lever**

### Rationale
- short calls are the main efficient rotation tool for shedding delta without immediately abandoning structural upside
- puts are the main bridge from moderately defensive posture into more explicitly negative posture
- trimming the core should usually come after overlays and puts have already done as much work as they reasonably can

## 5.14.3 When to prefer short calls over puts

Prefer more short-call pressure when:
- the goal is to reduce delta without fully abandoning the strategic core
- the likely path is chop, stall, failed continuation, or moderate downside
- premium harvest matters
- the user wants a rotational rather than outright bearish expression

## 5.14.4 When to prefer puts over more short calls

Prefer more put exposure when:
- the downside move is expected to be faster or more violent
- negative convexity from the core needs to be offset more directly
- the sleeve needs to move from defensive to meaningfully negative posture
- the user wants more direct participation in markdown rather than primarily suppressing upside

## 5.14.5 When to trim core longs

Trim core longs only after serious consideration of whether overlays and puts can achieve the needed posture first.

Core trimming becomes more justified when:
- markdown conditions are severe
- expected payoff improves materially from direct reduction rather than overlay management alone
- concentration or risk constraints require it
- the system concludes that survival and future redeployment flexibility matter more than holding maximum structural upside exposure through the current phase

## 5.14.6 When to redeploy reserve

Reserve should be redeployed when:
- asymmetry becomes unusually attractive
- the stage framework supports more offensive posture
- overlays are no longer suppressing the sleeve excessively
- the expected incremental payoff from redeployment is superior to simply normalizing existing structures

Reserve should not be treated as idle capital. It is part of the sleeve’s optionality engine.

## 5.15 Reporting integration
Define how Layer reports and PPRs should express sleeve recommendations so users are not left extracting clarity manually.

At minimum, outputs should clearly answer:
- what stage does the system think we are in?
- why does it think that stage applies?
- what is the target aggregate delta for that stage?
- what is the current estimated aggregate delta?
- is the sleeve inside or outside the default band?
- what deviation is acceptable and why?
- how should the long call core be treated?
- how should the short-call layer be treated?
- how should the put layer be treated?
- which positions should change first?
- what is the recommended adjustment ladder?

### Greeks communication rule
Option recommendations should begin layering in Greeks as an **explanation layer**, not as a full independent analysis block by default.

User-facing communication should focus primarily on:
- **delta** when explaining posture migration, targeted exposure changes, or why a structure better fits the current opportunity
- **theta** when explaining income generation, premium harvest, or why a short-option layer is being emphasized

Other Greeks may still inform internal calibration and assessment, but ordinarily should not dominate the user-facing explanation unless they become unusually important to the recommendation.

The user should not have to infer the posture from the analysis. The report should say the posture plainly.

---

## 6. Intended deliverables

## 6.1 Doctrine deliverable
A canonical sleeve doctrine brief covering:
- purpose of the MSTR sleeve
- stage-aware posture logic
- target delta philosophy
- role of core longs vs overlays vs hedge layer

## 6.2 Reporting deliverable
A reporting specification that adds to PPR outputs:
- target aggregate delta zone
- current estimated delta posture
- current benchmark vs actual sleeve exposure
- recommended structure by chart state
- first / second / third adjustment priority
- brief Greeks explanation focused mainly on **delta migration** and **theta-income intent** where relevant

## 6.3 Quant/chart deliverable
A list of minimum required quantitative and chart inputs for production-grade sleeve guidance, likely including:
- price structure
- FF ROC
- ST/LT SRI pattern state
- delta / gamma / theta summary by sleeve
- composition chart for current vs target sleeve

---

## 5.16 Implementation decision tree (draft)

This is the first draft of the sleeve decision tree.

It is meant to bridge the gap between stage doctrine and actual user-facing guidance.

## 5.16.1 Step 1 — Determine current stage and transition risk
The system should first answer:
- what stage are we most likely in now?
- how confident is that stage call?
- is the market stable within that stage, or transitioning toward the next one?

This matters because transition risk often matters more than the static stage label.

## 5.16.2 Step 2 — Estimate current aggregate delta versus target band
The system should then answer:
- what is the current estimated aggregate delta of the sleeve?
- what is the default target band for the current stage?
- is the current posture inside the target band, above it, or below it?

## 5.16.3 Step 3 — If current delta is above target
### Default sequence
1. tighten or add **short-call pressure**
2. increase **put participation**
3. trim **core longs** only if overlays and puts are insufficient

### Skip-ahead condition
If markdown risk is accelerating quickly, the system may move faster toward puts or selective core trimming rather than waiting for a slow overlay-only adjustment.

## 5.16.4 Step 4 — If current delta is below target
### Default sequence
1. reduce **short-call suppression**
2. reduce excess **put pressure**
3. expand **long-duration bullish exposure**
4. redeploy **reserve** only if the first steps are insufficient

### Skip-ahead condition
If asymmetry is unusually strong and reserve is abundant, the system may justify faster direct long re-expansion.

## 5.16.5 Step 5 — If current delta is inside the target band
If the sleeve is already inside the target band, the system should usually avoid unnecessary change.

The main question then becomes:
- should posture be held steady?
- or is transition evidence growing strong enough that the system should proactively rotate before the band itself changes?

## 5.16.6 Step 6 — Prioritize rotational levers by situation
### Prefer short calls first when:
- the goal is incremental delta reduction
- the likely path is stall, chop, or moderate downside
- the user wants income and rotational flexibility

### Prefer puts first when:
- downside acceleration risk is higher
- the sleeve needs to move from defensive to truly negative posture
- direct downside participation matters more than simple upside suppression

### Prefer core-long changes first only when:
- the current structure is badly mismatched to stage
- overlays and puts cannot solve the posture problem cleanly enough
- concentration / survival / payoff concerns justify direct structural change

## 5.16.7 Step 7 — Output decision-ready recommendation
The reporting layer should then produce a clear recommendation in this order:
1. **current stage + confidence**
2. **target delta band**
3. **current estimated delta posture**
4. **gap versus target**
5. **first rotation lever**
6. **second rotation lever**
7. **owner override / acceptable deviation logic**

That structure should become the backbone of personalized sleeve recommendations and PPR outputs.

---

## 7. Immediate next steps

1. pressure-test and refine the **stage-by-stage aggregate delta framework** for stages 1-4
2. refine the **stage classification rule set** into explicit observable conditions
3. refine the **default delta bands**, acceptable deviation bands, and migration thresholds for each stage
4. refine the **implementation decision tree** into a more explicit production decision flow
5. define the **current-state reporting template** for personalized sleeve recommendations
6. define the minimum chart/quant appendix needed to support decision-ready clarity
7. determine whether a formal **chart-reading capability** should be added to the architecture with Archie’s help
8. revise PPR reporting so the user sees a recommended posture first, with analysis supporting it rather than replacing it

---

## 8. Bottom line

This project is about turning the MSTR sleeve into a fully articulated operating doctrine rather than a vague conviction trade.

The north star is not analysis for its own sake.

The north star is:

> **decision-ready clarity about how the sleeve should be positioned, why, and what to change next.**
