# P-AB3 Ruleset v1
**Project:** P-AB3-RULESET  
**Date:** 2026-04-28  
**Author:** Cyler (CIO)  
**Status:** Draft for Gavin + Greg review

---

## Executive Summary

AB3 is the system’s **intentional overexposure and leverage layer**.

It exists to let the portfolio deviate from the selected **AB4 benchmark profile** when evidence, timing, and asymmetry justify doing so.

That means AB3 is **not** an independent benchmark and it is **not** the default posture.

AB4 defines the benchmark anchor.
AB3 defines the acceptable ways to go beyond that anchor.

---

## 1. Core AB3 Purpose

AB3 exists to pursue **outsized appreciation** when:
- the macro backdrop is supportive enough,
- the specific opportunity is strong enough,
- and the benchmark alone is too conservative to fully express the opportunity.

In practical terms, AB3 allows two broad forms of deviation:

1. **Leverage through LEAPs**
2. **Share-based overweights relative to AB4 benchmark weight**

AB3 should always be understood as a **deviation layer on top of AB4**, not a replacement for AB4.

---

## 2. Relationship to AB4

AB4 now has:
- a **Rotational profile**
- an **All-Weather profile**

The user’s selected AB4 profile becomes the benchmark anchor used by PPR.

AB3 is evaluated **relative to that chosen benchmark**, not relative to a universal static portfolio.

### Core dependency
Before AB3 can be judged, the system must know:
1. the current Howell phase or transition state
2. the current AB4 benchmark allocation for the chosen profile
3. the user’s actual portfolio allocation

Only after those are known can the system classify a position as:
- benchmark-aligned
- within AB4 tolerance
- AB3 overexposure
- owner override

---

## 3. AB3 Objective Hierarchy

AB3 should optimize for the following objectives in order:

1. **Preserve the usefulness of AB4 as the benchmark anchor**
2. **Express high-conviction asymmetry where benchmark sizing is insufficient**
3. **Use leverage only when time horizon and setup quality justify it**
4. **Avoid turning the total portfolio into a hidden single-name bet**
5. **Remain explainable in PPR**

AB3 is therefore aggressive, but it is not supposed to be reckless.

---

## 4. What Counts as AB3

A position should be classified as AB3 when it does any of the following:

### 4.1 LEAP-based exposure
- long-dated calls used to create leveraged upside exposure
- PMCC base LEAPs when held as strategic appreciation exposure
- other long-duration option structures explicitly intended to amplify participation

### 4.2 Share-based overexposure
- common-share exposure above the chosen AB4 benchmark weight
- preferred-share exposure above the chosen AB4 benchmark weight when the excess is being used as a deliberate conviction position rather than benchmark alignment
- concentrated special-sleeve exposure that goes materially beyond benchmark posture

### 4.3 Reclassified benchmark residuals
A position may begin as benchmark-aligned but become AB3 if:
- benchmark weight is reduced and the owner keeps the larger position,
- a special sleeve remains oversized after the phase shifts,
- or a benchmark-consistent entry grows into a material overweight that the owner elects not to trim.

---

## 5. AB3 Instruments

### Allowed core AB3 instruments
- long-dated calls / LEAPs
- common shares
- in some cases, preferred shares when used as deliberate overweight rather than benchmark ballast

### Not preferred for AB3 by default
- short-duration options used primarily for trading noise
- complex multi-leg leverage structures unless later explicitly approved
- instruments that make PPR explanation materially harder without adding proportional edge

Default bias:
- **shares first when the thesis is strong but leverage is not required**
- **LEAPs when asymmetry and time horizon justify leverage**

---

## 6. LEAPs vs Shares Decision Rules

This is the core AB3 implementation choice.

### Use shares when
- the owner wants durable overweight exposure without expiry pressure
- the benchmark already allows meaningful exposure and AB3 is only adding moderate size
- volatility is high enough that LEAP pricing is unattractive
- the thesis is strong, but the timing window is wide and not especially convex
- the asset is better expressed as a persistent holding than as a leveraged timing bet

### Use LEAPs when
- the thesis is high-conviction and upside convexity matters
- the setup is time-sensitive enough that leverage meaningfully improves expected outcome
- the owner explicitly wants capped premium risk rather than larger share notional
- the phase backdrop and technical timing are aligned enough to support leveraged expression
- the opportunity is strong, but the owner does not want to commit full share capital

### Prefer shares over LEAPs when
- the Howell phase is hostile or unstable for new leveraged exposure
- the security is already a large portfolio concentration
- option pricing is too expensive relative to expected edge
- the thesis depends more on long persistence than on fast convex payoff

### Prefer LEAPs over shares when
- the entry window is unusually attractive
- the benchmark is underexpressing a highly asymmetric setup
- the owner wants upside participation with predefined premium at risk

---

## 7. AB3 Macro Conditioning by Howell Phase

AB3 should not be equally active in every phase.

### 7.1 Rebound
**AB3 posture:** most permissive

Why:
- recovery asymmetry is often strongest
- benchmark may still be too conservative for best opportunities
- leveraged upside can be highly rewarding when stress is unwinding

AB3 in Rebound may allow:
- new LEAP entries
- meaningful share overweights
- concentrated special-sleeve expression where evidence is strong

### 7.2 Calm
**AB3 posture:** selective but still constructive

Why:
- upside still exists
- broad benchmark already carries healthy risk exposure
- overexposure should become more selective, not automatic

AB3 in Calm may allow:
- targeted LEAP entries
- moderate share overweights
- preference for strongest relative opportunities rather than broad aggression

### 7.3 Speculation
**AB3 posture:** selective and narrower

Why:
- opportunity still exists, but quality narrows
- broad late-cycle leverage becomes more dangerous
- benchmark special sleeves may already be elevated

AB3 in Speculation should favor:
- narrower, high-conviction positions
- tighter explanation requirements
- lower tolerance for casual overexposure

### 7.4 Turbulence
**AB3 posture:** highly restricted

Why:
- capital preservation dominates
- benchmark is intentionally defensive
- new leveraged overexposure is hardest to justify here

AB3 in Turbulence should generally:
- block most new LEAP entries
- sharply reduce tolerance for new share overweights
- allow only exceptional residual conviction or early transition setups

---

## 8. AB3 by Benchmark Profile

Because AB4 now has two profiles, AB3 should also be judged differently depending on the selected anchor.

### 8.1 If benchmark profile = Rotational
Implication:
- benchmark already expresses the phase aggressively
- it takes a stronger case to justify additional AB3 overexposure

So under Rotational:
- fewer deviations should qualify as AB3-appropriate
- share overweights should be smaller and rarer
- LEAP use should require unusually strong asymmetry

### 8.2 If benchmark profile = All-Weather
Implication:
- benchmark is intentionally smoother and less aggressive
- there is more conceptual room for AB3 to add conviction expression

So under All-Weather:
- moderate AB3 overweights are easier to justify
- LEAPs may be used to reintroduce convexity that the profile intentionally suppresses
- PPR should be careful not to confuse deliberate AB3 with simple benchmark mismatch

---

## 9. AB4 Tolerance Band Framework

Before a position is classified as AB3, the system should first ask whether it is still inside a reasonable **AB4 tolerance band**.

The purpose of the tolerance band is to separate:
- normal implementation drift,
- intentional but still benchmark-adjacent positioning,
- and true AB3 overexposure.

### 9.1 Core principle
A position should only be called AB3 once it is **meaningfully outside** the allowed AB4 tolerance band for that sleeve.

That means the classification sequence is:
1. benchmark-aligned
2. within AB4 tolerance band
3. AB3 deviation
4. owner override

### 9.2 Sleeve classes for tolerance purposes
Use two sleeve classes:

#### Standard diversified sleeves
- cash / equivalents
- short Treasuries
- long Treasuries
- investment-grade credit
- broad US equities
- defensive equities
- cyclical equities
- small caps
- commodities broad basket
- gold
- international equities
- energy equities
- financials

#### Special sleeves
- BTC proxy ETFs
- MSTR preferreds
- MSTR common

Special sleeves get tighter tolerance because they are more concentrated, more regime-sensitive, and more likely to turn quiet drift into hidden conviction risk.

### 9.3 Default AB4 tolerance bands
These are default absolute percentage-point bands around benchmark weight.

| Benchmark sleeve weight | Standard diversified sleeve | Special sleeve |
|---|---:|---:|
| 0% | +2% max residual | +1% max residual |
| >0% to 5% | ±2% | ±1.5% |
| >5% to 10% | ±3% | ±2% |
| >10% to 20% | ±4% | ±3% |
| >20% | ±5% | ±4% |

### 9.4 Zero-weight rule
A sleeve with a **0% benchmark weight** should be treated more strictly than an active benchmark sleeve.

That means:
- a standard diversified sleeve may still carry a small residual position up to **2%** and remain AB4-adjacent
- a special sleeve may carry at most **1%** residual and remain AB4-adjacent
- above those levels, the position is no longer just implementation drift and should be classified as AB3 or owner override

This matters most in Turbulence and in transition periods where benchmark posture intentionally turns certain sleeves off.

### 9.5 Profile modifier
Tolerance should be slightly conditioned by the chosen AB4 profile.

#### Rotational benchmark anchor
- use the default tolerance table as written
- benchmark is already active and phase-expressive
- extra drift should be treated more skeptically

#### All-Weather benchmark anchor
- tolerance may be interpreted slightly more generously in discussion
- but the default table should still remain the formal base rule
- the real difference should usually be handled through benchmark choice itself, not by making tolerance excessively loose

In other words: profile choice is the main driver, not wide tolerance inflation.

### 9.6 Phase modifier
Tolerance interpretation should tighten when the phase is more defensive.

#### Rebound
- most tolerant of benchmark-adjacent offensive drift

#### Calm
- still reasonably tolerant, but less permissive than Rebound

#### Speculation
- tolerance should be interpreted more narrowly for broad risk and special-sleeve overweights

#### Turbulence
- tightest interpretation
- drift above benchmark should be reviewed aggressively, especially for risk sleeves at or near zero benchmark weight

### 9.7 Practical classification examples

#### Example A: benchmark weight 10%, actual 12%
If the sleeve is standard diversified, that is still within the **±3%** tolerance band.
Result: **within AB4 tolerance**, not AB3.

#### Example B: benchmark weight 10%, actual 14%
If the sleeve is standard diversified, this is outside the **±3%** tolerance band.
Result: likely **AB3 deviation**.

#### Example C: benchmark weight 5%, actual 6%
If the sleeve is a special sleeve, this is still inside the **±1.5%** tolerance band.
Result: still **AB4-adjacent**.

#### Example D: benchmark weight 0%, actual 3% in MSTR common
Special sleeve, zero benchmark, residual limit is **1%**.
Result: this is clearly **AB3 or owner override**, not simple tolerance drift.

### 9.8 Why the tolerance layer matters
Without tolerance bands, every small deviation becomes noisy and every meaningful deviation becomes hard to classify cleanly.

The tolerance layer keeps AB4 usable as a benchmark while preserving AB3 as a real category rather than a catch-all label.

---

## 10. AB3 Deviation Tiers

PPR should classify AB3 deviations in tiers.

### Tier A: Acceptable AB3 deviation
Characteristics:
- clearly tied to a specific thesis
- size is moderate relative to total portfolio
- consistent with phase posture
- easy to explain relative to benchmark

### Tier B: High-conviction AB3 deviation
Characteristics:
- deliberate concentrated expression
- still phase-aware
- stronger sizing than normal benchmark drift
- requires explicit rationale and ongoing review

### Tier C: Exceptional AB3 deviation
Characteristics:
- unusually large overweight or leverage
- only acceptable when evidence is unusually strong
- should be treated almost like a special approval state inside PPR

### Tier D: Owner override
Characteristics:
- position is knowingly beyond what the framework would endorse
- system records it, explains the mismatch, and stops pretending it is benchmark-consistent

---

## 11. Conceptual Size Constraints

Exact percentages can be finalized later, but the ruleset should already define the shape of the constraints.

### 11.1 Benchmark-first principle
AB4 benchmark weight is the starting point.
AB3 size is measured as **incremental exposure beyond benchmark**, not in isolation.

### 11.2 Special-sleeve caution
For special sleeves such as:
- BTC proxy ETFs
- MSTR preferreds
- MSTR common

AB3 overweights should be treated more carefully than broad diversified sleeves.

### 11.3 Concentration doctrine
AB3 can create concentration, but should not create **unexamined concentration**.

Any AB3 position should be judged by:
- total portfolio look-through exposure
- correlation to existing special sleeves
- macro phase compatibility
- whether the benchmark already carries the same theme

### 11.4 Phase-dependent tolerance
Tolerance for AB3 overexposure should be:
- highest in **Rebound**
- still meaningful in **Calm**
- narrower in **Speculation**
- minimal in **Turbulence**

---

## 12. PPR Workflow for AB3

AB3 should be handled through a repeatable PPR sequence.

### Step 1. Identify benchmark anchor
Determine:
- current Howell phase
- current AB4 profile selected by the user
- resulting benchmark allocation

### Step 2. Compare actual portfolio to benchmark
For each sleeve or security, determine whether the actual position is:
- benchmark-aligned
- within AB4 tolerance
- AB3 overweight
- owner override

### Step 3. Evaluate AB3 justification
If the position is AB3, ask:
- what is the thesis?
- why is benchmark weight insufficient?
- why shares vs LEAPs?
- is the phase supportive enough?
- is the concentration acceptable?

### Step 4. Classify AB3 intensity
Classify as:
- acceptable AB3 deviation
- high-conviction AB3 deviation
- exceptional AB3 deviation
- owner override

### Step 5. Produce explicit output
PPR should output:
- benchmark weight
- actual weight
- AB3 incremental overweight
- justification summary
- risk warning
- review / trim conditions

---

## 13. AB3 Review and Exit Logic

AB3 positions should not be immortal just because they were once justified.

They should be re-reviewed when:
- the Howell phase changes
- the AB4 benchmark profile changes
- the benchmark sleeve weight changes materially
- a technical deterioration invalidates the original timing thesis
- the position grows into a much larger concentration than originally intended

### Exit / reduction reasons
AB3 should usually be reduced when:
- the benchmark catches up and the excess is no longer needed
- the phase becomes less supportive
- the position shifts from asymmetry to mere stubbornness
- the leverage no longer justifies the risk
- the owner still wants to keep it, but only as a transparent override

---

## 14. Working Examples

### Example A: All-Weather user, wants more MSTR upside in Rebound
- benchmark MSTR common weight under All-Weather is moderate
- user wants materially more upside exposure
- phase is supportive
- LEAPs may be justified as AB3 because benchmark intentionally compresses risk

### Example B: Rotational user already has large MSTR benchmark weight in Speculation
- benchmark is already aggressive
- additional common-share overweight needs a much stronger case
- LEAPs should face a high bar because the benchmark already expresses the thesis strongly

### Example C: Turbulence user wants new large risk-asset LEAP position
- benchmark is defensive
- phase is hostile
- this is likely not acceptable AB3
- if retained anyway, it should likely be classified as owner override

---

## 15. Immediate Implications for Related Projects

### For P-SOUNDBOARD
Need a consistent template that shows:
- chosen AB4 profile
- benchmark weight
- actual weight
- AB3 incremental size
- rationale
- classification

### For P-REPORTING
Reports should distinguish:
- benchmark exposure
- AB3 excess exposure
- owner overrides

### For AB2 logic
If AB2 remains a PMCC income overlay on AB3 LEAPs, then AB2 eligibility depends on an already-approved AB3 base position. That means AB3 approval logic must come first.

---

## 16. Open Items for v2

Still to formalize:
- exact AB4 tolerance bands before AB3 classification begins
- exact AB3 tier thresholds by percentage and by sleeve type
- technical timing requirements for LEAP approval
- branch-specific AB3 rules for MSTR, BTC proxy, and other sleeves
- whether preferred-share overweights should always count as AB3 or sometimes remain benchmark-adjacent

---

## Bottom Line

AB4 is the benchmark.
AB3 is the controlled deviation layer.

The system should first decide:
- the phase,
- the benchmark profile,
- and the benchmark allocation.

Only then should it decide whether a larger position is:
- still benchmark-consistent,
- acceptable AB3,
- exceptional AB3,
- or simply owner override.

That keeps AB3 aggressive without letting it become undefined.