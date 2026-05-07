# Gavin Personalized Layer 2-3 Report — v2

**Project:** P-REPORTING / Personalized portfolio implementation  
**Architecture:** SRI v3.2.2  
**Date:** 2026-05-07  
**Status:** Draft for review  
**Author:** Cyler

---

## 1. Purpose

This v2 report is meant to make the personalized portfolio reporting framework actually actionable.

Compared with v1, this version is designed to be more operational by making four things explicit:

1. the **shared-layer context** that gates downstream decisions
2. the **AB4 benchmark allocation** being prescribed
3. the **actual current portfolio vs benchmark**
4. the **specific adjustment ladder** most consistent with Gavin’s objectives and constraints

This is still based on the validated screenshot portfolio rather than a broker export, so the numbers should be treated as **decision-useful but provisional** until broker-export math and Greeks are added.

---

## 2. Personalized doctrine and constraints

## 2.1 Profile
- **AB4 profile:** Rotational AB4
- **Primary objective:** appreciation
- **Income role:** supported by `STRC` / yield-maxing and opportunistic trades, but not required to fully fund lifestyle income on a rigid schedule

## 2.2 Core MSTR doctrine
- default target is an **always-maxed 40% MSTR sleeve**
- the 40% can include both **bullish and bearish** expressions
- the sleeve can temporarily deviate from 40% when chart ambiguity is high enough to justify standing aside
- the sleeve can exceed 40% only when asymmetry is unusually attractive

## 2.3 Risk style
- highly aggressive, but focused on **risk-reward asymmetry**
- prefers **aggressive and smart rotation** rather than passive holding
- wants the system to rotate from long-delta conviction toward reduced delta, then negative delta, as tops form and confirm

## 2.4 Hard constraints
- maintain a combined **cash + cash-equivalent floor including `STRC` of $240,000**
- **no forced reduction of MSTR below 40%** as a default rule
- **no leverage other than LEAPs**

## 2.5 Bucket time horizons
| Bucket | Time horizon |
|---|---|
| AB4 | 2 years+, with bias toward 3-5 years, while maintaining 1 year of reserve |
| AB3 | about 1 year |
| AB2 | less than 1 year |
| AB1 | less than 30 days |

## 2.6 Reporting preference
The personalized report should emphasize:
- profit capture
- risk control
- benchmark deviation
- bucket opportunity by asset
- execution sequencing
- concentration control
- income support
- educational explanation

Decision framing should be:
- **benchmark recommendation**
- **acceptable deviation**
- **owner override**
with **ranked options**.

---

## 3. Shared context summary, Layers 0-1

## 3.1 Layer 0 — Economic backdrop
**Current read:** constructive enough to keep offensive opportunity alive.

### Implication
- macro is not imposing a hard risk-off regime
- offensive opportunity exists
- but macro alone is not enough to justify blind expansion of risk

## 3.2 Layer 0.5 — Howell phase
**Current read:** `Turbulence`, with early constructive pressure but not full confirmation.

### Implication
- broad participation is not yet fully trusted
- deployment should remain selective and staged
- chart structure still matters a lot

## 3.3 Layer 0.75 — Theme routing
**Current read:** MSTR remains the valid core sleeve, but internal positioning should adapt.

### Implication
- do not abandon the sleeve casually
- manage the sleeve through delta, overlays, and hedge posture
- this strongly supports the rotational AB4 concept

## 3.4 Layer 1 — Shared regime
**Current read:** selective constructive caution.

### Implication
- downstream signal trust should be selective, not automatic
- cleaner setups can be acted on
- ambiguous setups justify patience, lighter exposure, or more defensive overlays

## 3.5 Shared-layer bottom line
The shared stack does **not** support indiscriminate expansion.

But it **does** support maintaining the MSTR sleeve concept and managing that sleeve actively according to technical structure.

That is the foundation for the personalized Layer 2-3 recommendations below.

---

## 4. Portfolio extraction used in this report

This report uses the corrected screenshot interpretation below.

| Holding | Qty | Last price | Market value | Personalized role |
|---|---:|---:|---:|---|
| Cash | — | — | $2,214,955.47 | AB4 reserve |
| STRC | 3002 | 99.9697 | $300,109.04 | AB4 reserve / yield sleeve |
| MSTR common | 4 | 185.34 | $741.36 | negligible direct sleeve |
| MSTR Jun 05 '26 $190 Call | -117 | 11.29-11.82 | -~$143,325 | AB2 short-call overlay |
| MSTR Jun 18 '26 $190 Call | -55 | 15.35 | -$85,662.50 | AB2 short-call overlay |
| MSTR Jan 15 '27 $170 Call | 200 | 53.50 | $1,074,500.00 | AB3 core conviction |
| MSTR Jan 15 '27 $170 Put | 22 | 34.35 | $75,020.00 | hedge / risk-shaping sleeve |
| MSTR Jan 21 '28 $130 Call | 17 | 100.01 | $166,472.50 | AB3 core conviction |

### Portfolio NAV used
- **NAV:** `$3,602,810.87`

### Data note
A later production version should replace screenshot-derived estimates with:
- broker-export positions
- clean leg-by-leg pricing
- Greeks
- notional / delta conventions

---

## 5. AB4 benchmark prescription

## 5.1 Core benchmark
Given the profile and constraints, the cleanest benchmark is:

- **40.0% net MSTR sleeve**
- **minimum $240,000 in cash/cash-equivalents including `STRC`**
- remaining capital held in reserve unless stronger asymmetry justifies deployment

Using current NAV:

- **40.0% MSTR sleeve target = $1,441,124**
- **reserve floor = $240,000**

## 5.2 Benchmark allocation by asset class / role

| Asset class / role | Benchmark target | Notes |
|---|---:|---|
| Net MSTR sleeve | 40.0% | can include bullish and bearish structures |
| Cash-equivalent / reserve floor | 6.7% minimum | hard floor, can be above this |
| Additional reserve / staging capital | 53.3% flexible | undeployed capital until asymmetry improves |

This is intentionally simple because the doctrine is centered on a rotational MSTR sleeve, not a multi-theme benchmark.

---

## 6. Actual portfolio vs benchmark

## 6.1 Net MSTR sleeve math
Using the corrected signs:

- MSTR common: `$741`
- Jun 05 '26 $190 short calls: `-$143,325`
- Jun 18 '26 $190 short calls: `-$85,662`
- Jan 15 '27 $170 calls: `$1,074,500`
- Jan 15 '27 $170 puts: `$75,020`
- Jan 21 '28 $130 calls: `$166,472`

### Current estimated net MSTR sleeve
**~$1,087,746**

### Current estimated sleeve weight
**~30.2% of NAV**

### Gap vs benchmark
- **Target:** `$1,441,124`
- **Current:** `~$1,087,746`
- **Shortfall:** `~$353,378`
- **Shortfall as % of NAV:** `~9.81%`

## 6.2 Reserve posture
- Cash: `$2.215M`
- STRC: `$300K`
- Cash + STRC: `~$2.515M`
- Reserve floor required: `$240K`

### Reserve conclusion
The portfolio is massively above its minimum reserve floor.

That means:
- there is no liquidity pressure forcing defensiveness
- any current MSTR underweight is a **deliberate posture choice**, not a funding constraint

## 6.3 Benchmark vs actual table

| Role | Benchmark | Actual estimate | Deviation | Interpretation |
|---|---:|---:|---:|---|
| Net MSTR sleeve | 40.0% / $1,441,124 | ~30.2% / ~$1,087,746 | -9.81% / -$353,378 | materially underweight unless intentionally defensive |
| Cash/STRC floor | 6.7% / $240,000 min | ~69.8% / ~$2.515M | +63.1% / +$2.275M | enormous reserve surplus |
| AB3 core conviction | not fixed, subordinate to 40% net sleeve | ~34.5% / ~$1.2417M | n/a | large core already in place |
| AB2 overlays | tactical | ~-6.4% net market value effect | n/a | short-call overlays are the main suppressor of net sleeve exposure |
| Hedge | tactical / protective | ~2.1% / ~$75K | n/a | useful, but not the main driver of benchmark gap |

---

## 7. Personalized Layer 2 diagnosis

## 7.1 Core Layer 2 question
Relative to the AB4 benchmark, what is the real opportunity right now?

## 7.2 Correct current answer
The corrected answer is:

> **The portfolio is materially underweight the 40% benchmark, and the first decision is whether that underweight is an intentional defensive deviation or an unintended suppression caused by the short-call overlays.**

This is the key diagnosis.

## 7.3 Implication by chart state

### If charts are ambiguous
Then the current ~30.2% sleeve may be acceptable as a **temporary defensive deviation**.

### If charts are constructive
Then the sleeve is too far below benchmark and should be repaired.

### If charts are rolling over
Then the underweight is not a bug, it is part of the intended defensive posture, and the overlays may even need to become more defensive.

## 7.4 Most important Layer 2 conclusion
The current portfolio should **not** be described as "slightly underweight".

It should be described as:
- structurally underweight benchmark
- with the underweight caused largely by the **two short-call overlays**
- therefore the first live levers are overlay adjustments, not immediate core-LEAP surgery

---

## 8. Personalized Layer 3 prescription

## 8.1 Benchmark recommendation
The benchmark recommendation remains:
- **40.0% net MSTR sleeve**
- **$240K minimum reserve floor**
- use overlays and delta rotation to manage the sleeve rather than abandoning the sleeve concept

## 8.2 Acceptable deviation
The acceptable deviation is:
- temporary underweight when charts are ambiguous
- temporary overweight when asymmetry is unusually attractive

But the current underweight is large enough that it should only be tolerated if the chart read really justifies it.

## 8.3 Owner override
The owner override remains:
- stay sidelined / underweight if structure is too ambiguous
- exceed 40% only when asymmetry clearly warrants it

---

## 9. Recommended allocation posture now

This section answers the practical question: what allocation is being prescribed?

## 9.1 Prescribed posture if charts are still ambiguous

| Sleeve / role | Suggested posture now |
|---|---|
| AB4 reserve | keep fully intact |
| AB3 core | keep intact |
| Jun 05 short calls | maintain current size |
| Jun 18 short calls | maintain current size |
| Jan '27 puts | maintain current size |
| Net MSTR sleeve | allow temporary underweight near current level |

### Interpretation
This is a cautious rotational posture. It only makes sense if the chart read is genuinely ambiguous.

## 9.2 Prescribed posture if charts are constructive

| Sleeve / role | Suggested posture now |
|---|---|
| AB4 reserve | still intact, no reserve problem |
| AB3 core | preserve, add only if still needed after overlay repair |
| Jun 05 short calls | reduce first |
| Jun 18 short calls | reduce second |
| Jan '27 puts | keep unless bullish repair becomes strong enough to de-emphasize them |
| Net MSTR sleeve | move back toward 40% |

### Interpretation
If charts are constructive, the portfolio should be repaired toward benchmark, beginning with the overlay layer.

---

## 10. Adjustment priority order

This is the clean execution sequence.

1. **Jun 05 '26 $190 short calls**
2. **Jun 18 '26 $190 short calls**
3. **Jan 15 '27 $170 puts**
4. **Jan 15 '27 / Jan 21 '28 long calls**

### Why this order
- the benchmark gap is being created mainly by the short-call overlays
- overlays are the cleanest place to rotate delta first
- AB3 core should be the last thing touched unless the goal is explicit benchmark rebuilding through long-duration exposure

---

## 11. Contract-adjustment ladder

The right recommendation depends on chart state, so the cleanest operational format is a conditional ladder.

## 11.1 State A — Ambiguous / selective caution

### Recommendation
- keep **-117 Jun 05 short calls**
- keep **-55 Jun 18 short calls**
- keep **+22 Jan '27 puts**
- keep AB3 core unchanged
- accept ~30.2% as a temporary defensive underweight

### Meaning
This is valid only if the charts truly justify caution.

## 11.2 State B — Constructive upside confirmation

### Preferred repair sequence

#### Step 1: cover part of the Jun 05 shorts
- cover **50-75** contracts
- estimated sleeve restoration: about **$56K-$85K**

#### Step 2: cover part of the Jun 18 shorts
- cover **20-30** contracts
- estimated sleeve restoration: about **$31K-$46K**

#### Step 3: decide whether benchmark is repaired enough
If still meaningfully underweight, then use AB3 adds.

#### Step 4: add AB3 only if still needed
Approximate one-step repair equivalents:
- **66 Jan 15 '27 $170 calls** ≈ **$353K**
- **35 Jan 21 '28 $130 calls** ≈ **$350K**

### Interpretation
This is the cleanest constructive path because it first removes the suppressors before adding more long-duration size.

## 11.3 State C — Early rollover / diminishing upside

### Recommendation
- keep the **-117 Jun 05 short calls**
- consider increasing the **-55 Jun 18 short calls** to **-65 or -75**
- keep AB3 core intact
- keep puts intact

### Interpretation
This is the ideal diminishing-delta transition path described in the intake.

## 11.4 State D — Top largely confirmed, pre-drop

### Recommendation
- lean more defensive through the overlay layer first
- hold or modestly increase puts if needed
- only then consider trimming **10-20** Jan '27 $170 calls if you want to deepen defense further

### Interpretation
Use the overlay layer first, then hedge layer, then core if necessary.

---

## 12. Ranked recommendation set

## Rank 1 — Most important current read
### **Decide whether the current ~30.2% sleeve is an intentional defensive deviation or a benchmark error that now needs repair.**

That is the real decision.

## Rank 2 — Best constructive action path
### **If charts are constructive, reduce the Jun 05 shorts first, then the Jun 18 shorts, before adding fresh AB3 size.**

## Rank 3 — Best defensive action path
### **If charts are rolling over, keep the Jun 05 shorts, add more Jun 18 short-call pressure, and leave the AB3 core mostly intact.**

---

## 13. What is still missing for production quality

To make later versions materially better, the report should add:

### 13.1 Quant appendix
- broker-export positions
- exact leg values
- delta / gamma / theta by sleeve
- explicit net sleeve methodology

### 13.2 Chart appendix
- MSTR price-structure chart
- LOI / CPS panel
- VLT panel
- Force Field / FF ROC panel
- sleeve-composition chart
- adjustment table tied to chart states

### 13.3 Reporting artifact improvement
The recurring personalized report format should always include:
1. shared-layer summary
2. benchmark table
3. actual-vs-benchmark table
4. contract-adjustment ladder
5. action state: constructive / ambiguous / rollover / confirmed top

---

## 14. Bottom line

The most important quantitative conclusion is:

- **Target MSTR sleeve:** `$1.441M` = **40.0% of NAV**
- **Current estimated net MSTR sleeve:** `~$1.088M` = **30.2% of NAV**
- **Current shortfall:** `~$353.4K` = **9.81% of NAV**

The most important strategic conclusion is:

> **The current portfolio is materially underweight the rotational AB4 benchmark. That underweight is acceptable only if the chart read is intentionally cautious. If the chart is constructive enough, the first repair action should be reducing short-call suppression, starting with the Jun 05 line, before deciding whether additional AB3 size is still needed.**

The most important execution conclusion is:

> **Adjust overlays first, hedges second, and AB3 core last.**
