---
title: P-MR-HURDLE-OSCILLATOR
date: 2026-05-30
status: Draft v1
---

# P-MR-HURDLE-OSCILLATOR

## Purpose
Design an oscillator that helps determine whether MR Assets, especially **SPY**, offers a better risk-adjusted opportunity than **STRC** as the hurdle rate.

## Core decision
This indicator must be **completely independent of CiovaccoCapital**.

It should rely only on native market data and architecture inputs that the system can source directly.

## Strategic question
The oscillator should answer:

> Does broad-equity exposure, especially SPY, deserve incremental capital over STRC on a regime-aware and risk-adjusted basis?

That is the right upstream question.

The downstream question:

> Should that preference be expressed through shares, cash reduction, or AB3 SPY call LEAPs?

must remain a **separate gate**.

## Architecture placement
Best fit:
- **Layer 0.75 / MR Assets relative-attractiveness tool**
- supports **AB4 stock-vs-STRC intensity judgment**
- can inform **AB3 SPY expression eligibility**, but does not decide it alone

## What it should not do
The oscillator should **not**:
- depend on CiovaccoCapital
- override Layer 0 or Layer 0.5
- serve as a direct LEAP trigger by itself
- collapse benchmark choice and expression choice into one signal

## Candidate input families
Initial research set:

1. **SPY trend quality**
- long-term trend direction
- trend persistence
- distance vs key trend anchors

2. **Breadth / participation quality**
- large-cap only vs broad participation
- equal-weight confirmation
- small-cap / cyclical confirmation

3. **Volatility / drawdown pressure**
- realized-vol context
- implied stress proxies if available
- downside asymmetry / recent damage

4. **Relative strength / opportunity quality**
- SPY vs STRC total-return behavior
- SPY vs defensive assets
- SPY vs quality / cyclicals split if useful

5. **Macro compatibility**
- Layer 0 liquidity compatibility
- Layer 0.5 phase compatibility
- whether macro allows broader equity sponsorship

6. **Hurdle economics**
- STRC carry / hurdle attractiveness
- whether SPY offers enough expected upside and quality to beat that hurdle on a risk-adjusted basis

## Proposed outputs
The first version should ideally produce:
- **relative attractiveness score**
- **confidence bucket**
- **preferred capital posture**

Suggested posture classes:
- STRC preferred
- neutral / no edge
- SPY shares preferred
- SPY aggressive expression eligible

## Separate AB3 gate
Even if the oscillator favors SPY over STRC, AB3 SPY LEAPs should still require:
- acceptable phase backdrop
- sufficient trend quality
- acceptable volatility setup
- acceptable downside asymmetry
- non-fragile breadth confirmation

So the flow is:
1. oscillator says whether SPY clears STRC
2. separate AB3 gate says whether LEAPs are the right expression

## Recommended build sequence
### Phase 1 — Manual scoring rubric
Draft a non-code rubric that scores SPY vs STRC across the candidate input families.

### Phase 2 — Feature selection
Reduce the rubric to the smallest set of high-signal inputs that can be sourced reliably.

### Phase 3 — Pine prototype
Build a TradingView oscillator prototype using only native / directly sourced inputs.

### Phase 4 — Validation
Check whether high oscillator states actually align with better forward SPY opportunity relative to STRC, and separately test whether they improve AB3 SPY LEAP timing.

## Immediate next step
Draft the Phase 1 manual rubric before writing Pine code. The rubric should define:
- score buckets
- exact input list
- interpretation rules
- output posture classes
