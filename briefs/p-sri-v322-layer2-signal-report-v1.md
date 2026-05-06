# Layer 2 Signal Report — v1

**Project:** P-REPORTING / P-LAYER-ARCH  
**Architecture:** SRI v3.2.2  
**Date:** 2026-05-06  
**Status:** Draft for Gavin review  
**Author:** Cyler

---

## 1. Purpose

This document is the first actual draft of the **Layer 2 Signal Report** for the v3.2.2 architecture.

The purpose of the report is to make Layer 2 legible to users by reporting:
- what signal state is active inside each relevant branch
- how Layer 2 applies to each asset currently in the user’s portfolio relative to the chosen AB4 profile
- whether AB1, AB2, or AB3 conditions are firing, forming, blocked, or invalidated
- how much confidence to place in the current signal state
- what timing structure is driving the signal view
- what evidence supports the signal call
- whether there is an opportunity to capture more profit through other buckets relative to the AB4 baseline
- what this should imply for Layer 3 allocation decisions

Like the Layer 0 through Layer 1 reports, this report should stay **pure in authority** while becoming highly useful in implication.

That means it should:
- report signal-layer state accurately
- explain whether timing and structure are actionable, forming, blocked, or broken
- distinguish among AB1, AB2, and AB3 rather than flattening them together
- show the evidence behind the signal call instead of reducing everything to prose

It should **not**:
- replace Layer 0 macro authority
- replace Layer 0.5 phase authority
- replace Layer 0.75 branch-routing authority
- replace Layer 1 shared regime authority
- decide final portfolio sizing by itself

---

## 2. Core reporting framework

The Layer 2 report should be organized around ten durable reporting fields.

1. **Signal state**
2. **Signal direction / timing posture**
3. **Confidence**
4. **AB4-relative opportunity context**
5. **AB1 state**
6. **AB2 state**
7. **AB3 state**
8. **Blocking / invalidation state**
9. **Warnings / tensions**
10. **Evidence package**

These fields reflect what Layer 2 actually owns in the architecture: converting branch state plus regime context into actual execution signals.

### 2.1 What Layer 2 owns

Layer 2 is the **signal layer**.

Its job is to convert:
- branch state
- macro and phase context
- regime posture
- structure and timing evidence

into actual signal states such as:
- watch
- forming
- confirmed
- invalidated
- blocked
- no edge

This means Layer 2 is the architecture’s **timing and actionability interpreter**.
It is where structure becomes signal, but not yet final sizing.

### 2.2 Scope of Layer 2

In v3.2.2:
- **AB1 / AB2 / AB3** operate inside active branches
- **AB4** remains global and is not a Layer 2 signal bucket

That means the report should treat Layer 2 primarily as:
- a signal-state and timing report
- a bucket-translation report for AB1 / AB2 / AB3
- an **AB4-relative opportunity report** for assets already in the portfolio or under active consideration
- a bridge from structural context to allocation readiness

### 2.3 Confidence-factor framework

Confidence at Layer 2 should answer:

> How actionable and trustworthy is the current signal state?

A simple v1 scale is enough:
- **High confidence** = structure, timing, and upstream layers all align cleanly
- **Moderate confidence** = the signal is usable, but gating or crosscurrents remain
- **Low confidence** = evidence is mixed, early, blocked, or too fragile for strong trust

Layer 2 confidence should be influenced by:
- coherence with Layers 0 through 1
- stage / ladder progression
- CPS or equivalent classifier support where available
- VLT clock or similar timing confirmation
- breadth and gate-state alignment
- whether the signal is blocked by phase or structural rules

### 2.4 Signal-state framework

The report should classify the current signal state clearly.

A simple v1 ladder:
- **Blocked**
- **Watch**
- **Forming**
- **Confirmed**
- **Invalidated**
- **No edge**

This matters because a good Layer 2 report should tell users not just what direction might matter, but how close the system is to actual actionability.

---

## 3. Current Layer 2 report

## 3.1 Executive conclusion

Layer 2 should currently be interpreted as the architecture’s **state-to-signal conversion layer**, where the central question is not just “is the thesis good?” but “is the structure actionable now, and is there an AB1 / AB2 / AB3 opportunity relative to the user’s chosen AB4 baseline?”

The present top-level interpretation is:
- Layer 2 inherits caution from Layer 0.5 and selectivity from Layer 1
- branch-level contradictions from Layer 0.75 still matter materially
- therefore Layer 2 should emphasize **signal quality, gating, and timing confirmation** over raw strategic enthusiasm

This is a **signal-discipline layer**, not a thesis layer.

## 3.2 Current doctrine-based conclusion

My base-case draft for Layer 2 is:

## **Signal opportunity should be treated as selective, ladder-based, gate-conditioned, and explicitly measured relative to the chosen AB4 baseline rather than continuously “on.”**

That is the most important behavior the report should communicate.

---

## 4. Current Layer 2 summary line

The published summary line for Layer 2 should look like this:

- **Layer 2:** `signal regime | timing posture | confidence | AB4-relative opportunity | AB1 state | AB2 state | AB3 state | major block / tension`

Current draft doctrine line:

- **Layer 2:** `Selective signal opportunity | Watch/forming/confirmed ladder, not binary timing | Moderate confidence | Asset-level opportunities must be judged relative to AB4 baseline | AB1 tactical / conditional | AB2 directional or income state conditional | AB3 structural / staged | Gated by phase, breadth, and structural confirmation`

This gives users one compact line and then a fuller signal interpretation below it.

---

## 5. Signal-state block

## 5.1 Current signal interpretation

- **Signal state:** `Selective, ladder-based actionability`
- **Signal direction / timing posture:** `Action depends on watch → forming → confirmed progression, not one-step binary triggers`
- **Confidence:** `Moderate`

## 5.2 Why this is the signal-layer call

Layer 2 exists because the architecture needs something more precise than:
- macro backdrop
- phase label
- branch thesis
- shared regime posture

It needs to know when structure is:
- merely interesting
- becoming actionable
- fully actionable
- broken or invalid

The alert and classifier doctrine already shows that Layer 2 is built around:
- confirmation ladders
- stage-state transitions
- CPS thresholds
- VLT recovery clocks
- breadth divergence logic
- invalidation conditions

That means the cleanest Layer 2 identity is:

## **A ladder-based signal engine with explicit gates and invalidations**

## 5.3 Why confidence is moderate

The confidence is best described as:

## **Confidence = Moderate**

because:
- the signal architecture is strong conceptually
- but many signals still depend on asset-specific context, gating, and confirmation quality
- the system is intentionally selective and does not treat every structural move as tradable

This is a good kind of moderation. It reflects discipline, not weakness.

---

## 6. AB4-relative opportunity block

## 6.1 Why this block is necessary

This is the missing practical bridge in the earlier draft.

Layer 2 is not just answering whether a signal exists in the abstract. It is answering:

> Relative to the user’s chosen AB4 profile and current holdings, is there an opportunity to capture additional profit or improve expression through AB1, AB2, or AB3?

That means Layer 2 has to become explicitly **asset-in-portfolio aware**.

It should evaluate each relevant asset through three lenses:
- current portfolio role under AB4 baseline
- current technical/chart signal opportunity
- whether another bucket offers a superior profit-capture expression right now

## 6.2 What the report should publish for each asset

For each asset currently held, watched, or benchmark-relevant, the report should publish:
- current AB4 baseline role
- whether AB1 opportunity exists
- whether AB2 opportunity exists
- whether AB3 opportunity exists
- whether no incremental bucket opportunity exists relative to simply holding baseline exposure
- what chart / timing evidence is driving that conclusion

## 6.3 Core Layer 2 question by asset

For each asset, Layer 2 should answer:

- should this remain just AB4 baseline exposure?
- is there a tactical AB1 opportunity here?
- is there an AB2 directional or income opportunity here?
- is there an AB3 structural overexposure / deviation opportunity here?
- or is the right answer still **do nothing beyond baseline**?

That is the asset-level application logic that makes Layer 2 genuinely portfolio-relevant.

## 6.4 Reporting principle

The report should not assume every asset deserves an active bucket opportunity.

A very important valid Layer 2 output is:

- **No incremental bucket opportunity relative to AB4 baseline**

That is just as important as identifying an active opportunity.

## 6.5 Suggested per-asset report row

The eventual published Layer 2 report should include an asset-by-asset table or section like:

| Asset | AB4 baseline role | AB1 | AB2 | AB3 | Best current opportunity | Why |
|---|---|---|---|---|---|---|
| MSTR | active / overweight candidate / baseline absent / etc. | ... | ... | ... | ... | ... |

This is probably the single most important practical addition to the report.

---

## 7. AB1 state block

## 6.1 What AB1 owns

AB1 is the short-duration theta / income or tactical opportunity layer.

Depending on the branch and asset, it may function as:
- premium-sale favorable
- breakout-opportunity favorable
- neutral
- avoid

## 6.2 Current doctrine-based AB1 interpretation

AB1 should be treated as:
- the most tactical bucket
- highly timing-sensitive
- often more sensitive to early structural deterioration or acceleration than AB2

For MSTR-related work, recent doctrine also implies:
- AB1 should increasingly act as a **theta-management / premium-sale layer** rather than a pure directional oracle
- AB1 may turn cautious or bearish-active before broader bullish structure fully breaks when topping evidence clusters

## 6.3 Reporting format for AB1

The report should publish AB1 as one of:
- **Favorable theta window**
- **Tactical directional favorable**
- **Neutral**
- **Avoid**
- **Blocked**

That is a better user-facing output than raw indicator fragments.

---

## 8. AB2 state block

## 7.1 What AB2 owns

AB2 is the short- to medium-term directional or income-expression layer.

Its exact implementation can vary by architecture branch, but it generally answers:
- is there a directional opportunity here?
- should an income overlay be active?
- should delta be reduced or preserved?

## 7.2 Important current doctrine

AB2 already has important architecture-specific rules worth preserving:
- in the PMCC framework, AB2 can function as an **income overlay on AB3 LEAPs**, not necessarily an independent capital bucket
- AB2 state is strongly shaped by LOI / CT conditions
- AB2 should pause when AB1 expects a fast move that should not be capped
- AB2 may shift into delta-management mode when the AB3 lifecycle matures

## 7.3 Reporting format for AB2

The report should publish AB2 as one of:
- **Bullish directional**
- **Bearish directional**
- **Income favorable**
- **Delta-management favorable**
- **No AB2 edge**
- **Blocked**

This is one of the most practically useful outputs of Layer 2.

---

## 9. AB3 state block

## 8.1 What AB3 owns

AB3 is the structural deployment / longer-horizon conviction layer relative to baseline.

It should answer:
- is structural accumulation beginning?
- is partial deployment justified at the trough?
- is this a stage-1 watch, a stage-2 actionable setup, or a broken thesis?

## 8.2 Important current doctrine

The current AB3 architecture already includes critical signal rules worth preserving:
- **Gate Zero applies first**
- LOI threshold crossings create awareness, not automatic deployment
- classifier and episode-type logic help distinguish Transient vs Structural vs Extended episodes
- CPS can justify a 25% anticipatory tranche at the trough in the right conditions
- VLT recovery clock governs scale-up vs caution vs abort
- breadth divergence can hard-block certain MR entries

## 8.3 Reporting format for AB3

The report should publish AB3 as one of:
- **Add**
- **Watch**
- **Wait**
- **Hold**
- **De-risk**
- **Blocked**

This translates the structural signal state into something users can actually understand.

---

## 10. Blocking / invalidation block

## 9.1 Why this block is essential

Layer 2 is where the architecture becomes dangerous if it does not explicitly publish why something is **not** actionable.

The report should surface blocks like:
- Howell phase ineligible
- IWM breadth divergence active
- VLT clock unresolved or aborted
- CPS below threshold
- signal invalidated after forming
- tactical opportunity present but branch deployment not supportive

## 9.2 Most likely interpretation philosophy

My current base-case view is:
- Layer 2 should earn trust by being willing to say **no**, **not yet**, and **wait for confirmation**
- a large part of its value is not finding more signals, but filtering out lower-quality ones

That means the report should make blocked and invalidated states as visible as confirmed ones.

---

## 11. Warnings / tensions block

## 10.1 Why this block is essential

Layer 2 is where timing tension becomes operational.

The report should surface tensions like:
- strategic thesis intact, but timing poor
- signal forming, but gate state still selective
- macro improving, but breadth still blocks entry
- branch conviction strong, but ladder not yet confirmed
- tactical topping evidence active before broader trend fully breaks

## 10.2 Most likely interpretation

My current base-case interpretation is:
- Layer 2 should usually resolve tensions through **staging**, **partial deployment**, **wait states**, or **blocking logic**
- it should rarely pretend a conflicted setup is fully clean just because one part of the stack looks attractive

That is exactly what makes it a real signal layer instead of a hype amplifier.

---

## 12. Evidence package

The report should not stop at signal labels. It should show the evidence behind them.

### 11.1 Required evidence categories

The Layer 2 evidence package should include as much of the following as is available:

1. **Upstream context evidence**
   - latest Layer 0 conclusion
   - latest Layer 0.5 phase state
   - latest Layer 0.75 deployment-conditioning state
   - latest Layer 1 gate-state environment

2. **Ladder / stage evidence**
   - watch, forming, confirmed, invalidated state
   - number of rungs cleared where applicable

3. **Classifier / timing evidence**
   - CPS level where applicable
   - VLT recovery clock state
   - stage-transition status

4. **Gate / block evidence**
   - Howell Gate Zero status
   - breadth gate status
   - branch-level deployment constraints

5. **Bucket-translation evidence**
   - why AB1 is favorable/avoid
   - why AB2 is directional/income/no-edge
   - why AB3 is add/watch/wait/blocked

6. **Invalidation evidence**
   - what would break the setup
   - what would move it from watch to forming or forming to confirmed

### 11.2 Current doctrine-backed evidence examples

The current signal doctrine already gives strong evidence examples the report should reuse:
- `STAGE_WATCH_DECLARED`
- `STAGE_FORMING_DECLARED`
- `STAGE_CONFIRMED`
- `STAGE_INVALIDATED`
- `VLT_CLOCK_START`
- `VLT_CLOCK_RESOLVED`
- `VLT_CLOCK_WARNING`
- `VLT_CLOCK_ABORT`
- `BREADTH_DIVERGENCE`
- `CPS_THRESHOLD`

These are exactly the kinds of state changes that should populate the report’s evidence package.

### 11.3 Reporting principle

If the signal evidence is incomplete, the report should say so directly.

That means Layer 2 should be allowed to publish states like:
- watch only
- forming but blocked
- structurally attractive, tactically unresolved
- tactical edge present, strategic support weak

That honesty is one of the main quality controls of the whole architecture.

---

## 13. Combined Layer 2 synthesis

## 12.1 Current combined read

The current combined Layer 2 state should be summarized as:
- signals must clear gates, not just exist
- timing must progress through a ladder, not merely flash once
- bucket translation matters as much as signal direction
- upstream caution should still shape actionability materially

### Combined Layer 2 conclusion:
## **Signal opportunity exists, but it must earn actionability through gates, ladder progression, and timing confirmation**

### Combined confidence:
## **Moderate confidence**

The Layer 2 architecture is strong precisely because it resists premature action.

## 12.2 Plain-English takeaway

The right user takeaway is:
- Layer 2 is where the architecture decides whether a setup is actually tradeable
- not every interesting move is actionable
- good Layer 2 states should become clearer, not noisier, as confirmation builds

---

## 14. Downstream impact by layer

## 13.1 Impact on Layer 3 — Allocation Engine

Layer 3 should use Layer 2 to decide:
- whether an allocation action exists at all
- whether a tranche should be anticipatory, partial, full, reduced, or paused
- whether the opportunity belongs in AB1, AB2, or AB3 expression

Current implication:
- Layer 3 should not infer action from thesis alone
- it should wait for Layer 2 to clarify bucket translation and actionability state

---

## 15. Recommended published report format

For each recurring Layer 2 report, the published format should begin with one summary line and then expand by bucket and active setup.

### Layer 2 line
- **Layer 2:** `signal regime | timing posture | confidence | AB4-relative opportunity | AB1 state | AB2 state | AB3 state | major block / tension`

Example:
- **Layer 2:** `Selective signal opportunity | Ladder-based timing with explicit gates | Moderate confidence | Only some assets justify bucket activity beyond AB4 baseline | AB1 tactical / conditional | AB2 state context-dependent | AB3 staged structural opportunity | Gate Zero + breadth + VLT confirmation matter`

### Required asset-application block
After the summary line, the report should publish an asset-by-asset application block containing:
- asset
- current AB4 baseline role
- current AB1 / AB2 / AB3 opportunity states
- best current bucket opportunity relative to baseline
- key chart / signal evidence
- current block / invalidation if any

### Required evidence block
The report should also publish a compact evidence block containing:
- latest upstream layer conclusions
- current ladder / stage state
- current CPS / VLT clock or equivalent timing evidence
- current blocks / invalidations
- rationale for AB1 / AB2 / AB3 translation

That makes the report compact at the top, but still auditable and tactically useful below.

---

## 16. Chart package for the published version

Charts are not embedded in this chat workflow, but the eventual published report should include them.

### Required chart set

1. **Signal ladder tracker**
   - watch / forming / confirmed / invalidated over time

2. **VLT recovery clock panel**
   - start, elapsed bars, resolved / warning / abort status

3. **CPS / classifier panel**
   - threshold crossings
   - episode classification where available

4. **Gate-state map**
   - Howell Gate Zero
   - breadth gate
   - branch deployment constraints

5. **Bucket-translation panel**
   - AB1 / AB2 / AB3 current state by active asset or branch

6. **Invalidation / resolution panel**
   - what would confirm, downgrade, or kill the setup

---

## 17. Draft labeling rules to preserve

The following reporting pattern should be preserved going forward:

- report the current **signal state**
- call the **signal direction / timing posture** clearly
- assign one **confidence factor**
- publish the current **AB4-relative opportunity context**
- publish the current **AB1 state**
- publish the current **AB2 state**
- publish the current **AB3 state**
- apply Layer 2 explicitly **asset by asset** for the user’s portfolio or active watch universe
- publish the current **blocking / invalidation state**
- publish the current **warnings / tensions**
- publish an **evidence package**
- synthesize what the combined Layer 2 backdrop implies for Layer 3
- explicitly surface important divergence rather than flattening it
- state the **most likely interpretation** when tensions matter

---

## 18. Bottom line

The Layer 2 report should evolve from vague signal talk into a disciplined actionability report with repeatable fields.

The best v1 reporting structure is:
- **signal state**
- **signal direction / timing posture**
- **confidence**
- **AB4-relative opportunity context**
- **AB1 state**
- **AB2 state**
- **AB3 state**
- **blocking / invalidation state**
- **warnings / tensions**
- **evidence package**
- **combined Layer 2 conclusion**
- **downstream implications for Layer 3**
- **chart package in the published version**

Current draft doctrine call:

- **Layer 2:** `Selective signal opportunity | Watch/forming/confirmed ladder, not binary timing | Moderate confidence | Asset-level opportunities must be judged relative to AB4 baseline | AB1 tactical / conditional | AB2 directional or income state conditional | AB3 structural / staged | Gated by phase, breadth, and structural confirmation`
- **Layer 2 Conclusion:** `Signal opportunity exists, but it must earn actionability through gates, ladder progression, timing confirmation, and asset-level comparison to the chosen AB4 baseline`
- **Combined Confidence:** `Moderate`

That gives users a clean answer to both questions that matter:

1. **What is Layer 2 saying?**
2. **What is actually actionable now, and in which bucket?**
