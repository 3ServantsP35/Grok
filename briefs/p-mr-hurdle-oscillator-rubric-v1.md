---
title: P-MR-HURDLE-OSCILLATOR-RUBRIC
date: 2026-05-30
status: Draft v1
---

# P-MR-HURDLE-OSCILLATOR-RUBRIC

## Purpose
Create a manual scoring rubric that determines whether **SPY** offers a better risk-adjusted opportunity than **STRC** as the hurdle rate.

This rubric is the decision template that should exist before any TradingView oscillator is coded.

## Core question

> Does SPY deserve incremental capital over STRC right now on a regime-aware, risk-adjusted basis?

This rubric answers only that question.

It does **not** answer:
- whether the expression should be shares vs LEAPs
- whether AB3 SPY call LEAPs are eligible
- whether CiovaccoCapital agrees

Those are downstream questions.

## Independence rule
This rubric must remain fully independent of:
- CiovaccoCapital
- discretionary commentary inputs
- any external channel that may become unavailable

It should rely only on directly sourced market / architecture inputs.

## Scoring framework
Use a 5-block scoring model.

Each block scores from **-2 to +2**:
- **+2** strongly favors SPY over STRC
- **+1** moderately favors SPY over STRC
- **0** neutral / no edge
- **-1** moderately favors STRC over SPY
- **-2** strongly favors STRC over SPY

Total score range: **-10 to +10**.

---

## Block 1 — Macro compatibility
### Question
Does the current macro backdrop support broad-equity sponsorship strongly enough to let SPY clear a defensive hurdle?

### Inputs
- Layer 0 liquidity posture
- Layer 0.5 Howell phase posture
- growth posture
- whether the backdrop is broadening or still restrictive/selective

### Scoring guide
- **+2** Layer 0 constructive and Layer 0.5 supportive of broader risk sponsorship
- **+1** Layer 0 constructive but Layer 0.5 still selective, with improvement building
- **0** mixed cross-layer read, no strong edge either way
- **-1** restrictive / selective backdrop with incomplete confirmation
- **-2** clearly risk-constraining / defensive macro state

### Interpretation note
This block should prevent SPY from scoring too high in a regime where broad beta is still structurally unsupported.

---

## Block 2 — SPY trend quality
### Question
Is SPY structurally healthy enough to justify clearing the STRC hurdle?

### Inputs
- long-term trend direction
- trend persistence
- position vs major moving/trend anchors
- absence or presence of structural damage

### Scoring guide
- **+2** strong persistent uptrend with clean structural confirmation
- **+1** constructive trend with minor imperfections
- **0** mixed trend / range / uncertain trend quality
- **-1** weak or deteriorating trend quality
- **-2** broken / clearly adverse broad-equity structure

### Interpretation note
This is about structure, not short-term enthusiasm.

---

## Block 3 — Breadth and participation quality
### Question
Is SPY being supported by broad participation, or only by a narrow leadership group?

### Inputs
- equal-weight confirmation
- small-cap / cyclical participation
- sector breadth
- breadth persistence vs one-cluster leadership

### Scoring guide
- **+2** broad and durable participation
- **+1** decent participation with some concentration risk
- **0** mixed / unclear breadth picture
- **-1** narrow leadership, weak confirmation
- **-2** highly concentrated advance or clearly defensive internal structure

### Interpretation note
This block matters because SPY should not beat STRC by default if the advance is too narrow and fragile.

---

## Block 4 — Relative opportunity vs STRC
### Question
Does SPY offer enough expected upside and structural quality to beat STRC on a risk-adjusted basis?

### Inputs
- STRC carry / hurdle attractiveness
- expected SPY upside vs hurdle return
- likely path quality / path risk
- asymmetry of upside relative to downside

### Scoring guide
- **+2** SPY clearly offers superior risk-adjusted opportunity to STRC
- **+1** SPY modestly clears the hurdle
- **0** no meaningful edge over STRC
- **-1** STRC compares favorably on risk-adjusted basis
- **-2** STRC is clearly the better hurdle asset

### Interpretation note
This is the core block. Even if SPY looks decent, STRC may still be the better capital destination on a hurdle-adjusted basis.

---

## Block 5 — Volatility and downside asymmetry
### Question
Is the volatility / drawdown environment good enough to prefer SPY over STRC?

### Inputs
- realized volatility
- market stress / downside pressure
- fragility of recent advance
- drawdown asymmetry

### Scoring guide
- **+2** benign volatility backdrop with favorable downside asymmetry
- **+1** acceptable volatility backdrop for equity exposure
- **0** neutral / mixed volatility conditions
- **-1** elevated fragility or poor asymmetry
- **-2** hostile volatility / drawdown environment

### Interpretation note
This block is important because STRC’s hurdle role becomes more attractive when path risk rises.

---

## Total score interpretation
### Score bands
- **+7 to +10** → **SPY clearly preferred over STRC**
- **+3 to +6** → **SPY modestly preferred over STRC**
- **-2 to +2** → **No strong edge / neutral**
- **-6 to -3** → **STRC modestly preferred over SPY**
- **-10 to -7** → **STRC clearly preferred over SPY**

## Output posture classes
The rubric should output one of four postures:

1. **STRC preferred**
- keep hurdle discipline high
- do not force broad-equity preference

2. **Neutral / no edge**
- no strong rotation pressure either way
- avoid aggressive expression choice

3. **SPY shares preferred**
- broad equities clear the hurdle
- stock allocation can expand ahead of aggressive convex expression

4. **SPY aggressive expression eligible**
- this is only a provisional posture class
- it still requires a separate AB3 gate before LEAPs are allowed

## Separate AB3 gate reminder
Even a very high rubric score does **not** automatically authorize SPY call LEAPs.

A separate AB3 expression gate must still assess:
- phase suitability
- timing quality
- volatility suitability
- downside asymmetry
- tactical expression quality

## Recommended first manual workflow
For the next few runs:
1. score each block manually
2. write a one-line reason for each score
3. total the score
4. assign posture class
5. separately decide whether AB3 expression is justified

## Next step after rubric approval
Once this rubric is accepted:
- convert the block logic into a smaller feature set
- determine which inputs are directly available in TradingView / warehouse
- then draft the Pine implementation spec
