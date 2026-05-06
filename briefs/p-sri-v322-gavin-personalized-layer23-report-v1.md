# Gavin Personalized Layer 2-3 Report — v1

**Project:** P-REPORTING / Personalized portfolio implementation  
**Architecture:** SRI v3.2.2  
**Date:** 2026-05-06  
**Status:** Draft for Gavin review  
**Author:** Cyler

---

## 1. Scope and limitations

This report is an updated **personalized Layer 2-3 report** for Gavin’s portfolio.

It is designed to do three things more explicitly than the first draft:

1. summarize **Layers 0-1** so the later recommendations are clearly grounded
2. translate the portfolio into a **quantified AB4 benchmark vs current-state comparison**
3. prescribe more concrete **Layer 2-3 adjustments** at the contract / sleeve level

### Important limitation
This report is more quantitative than the Discord draft, but it is still working from:
- a validated portfolio screenshot
- shared-layer architecture reports
- stated portfolio objectives and constraints

It is **not yet** working from:
- a broker export / CSV position file
- live Greeks
- chart screenshots for each current structure
- current LOI / CPS / VLT / FF ROC readouts tied directly to each held asset/contract

So the numbers below should be treated as **provisional but decision-useful**.

---

## 2. Personalized inputs now locked

## 2.1 AB4 profile
- **Profile:** Rotational AB4
- **Core doctrine:** maintain an **always-maxed MSTR sleeve of 40%** by portfolio value, using both bullish and bearish positioning when needed
- **Important exception:** if charts are sufficiently ambiguous, standing aside from the 40% rule is acceptable

## 2.2 Objective
- **Primary objective:** appreciation
- Income can come from:
  - `STRC` / yield-maxing
  - opportunistic trades
- No requirement to generate the full **$30K lifestyle income** consistently from the portfolio on a fixed schedule

## 2.3 Risk style
- **Highly aggressive**, but intelligent about **risk-reward asymmetry**
- Comfortable going beyond the 40% MSTR rule when asymmetry is unusually attractive

## 2.4 Hard constraints
- maintain a cash / cash-equivalent floor including `STRC` of **$240,000**
- **no forced reduction of MSTR below 40%** as a normal rule
- **no leverage other than LEAPs**

## 2.5 Time horizons by bucket
- **AB4:** 2 years+, with bias toward 3-5 years, while always maintaining 1 year of cash/cash-equivalent reserve including `STRC`
- **AB3:** 1 year
- **AB2:** less than 1 year
- **AB1:** less than 30 days

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

The report should frame decisions as:
- **benchmark recommendation**
- **acceptable deviation**
- **owner override**
with **ranked options**.

---

## 3. Shared context summary, Layers 0-1

## 3.1 Layer 0 — Economic backdrop
**Current read:** constructive liquidity backdrop, not a hard macro headwind.

Implication:
- macro is supportive enough to keep offensive opportunity alive
- broad bearishness should be moderated
- this supports maintaining an offensive-capable stance, but not blind risk expansion

## 3.2 Layer 0.5 — Howell phase
**Current read:** `Turbulence`, with early constructive pressure worth watching.

Implication:
- broad participation is still not fully trusted
- deployment should remain selective and staged
- the system should respect caution until transition becomes more confirmed

## 3.3 Layer 0.75 — Theme routing
**Current read:** MSTR sleeve remains valid, but deployment should be conditioned rather than forced.

Implication:
- the sleeve stays central
- contradiction should be resolved through **positioning mix**, **delta**, **income overlay**, and **hedge posture**
- this is highly compatible with the rotational AB4 concept

## 3.4 Layer 1 — Shared regime
**Current read:** selective constructive caution.

Implication:
- the environment is better than hard risk-off
- but downstream trust still has to be earned
- strong setups deserve action; weak or ambiguous setups deserve patience or tighter management

## 3.5 Bottom-line shared context
The shared stack says:

> stay committed to the MSTR sleeve concept, but let **technical structure and stage** determine how aggressively that sleeve should be expressed.

That is the bridge into the personalized Layer 2-3 recommendations below.

---

## 4. Portfolio extraction used for this report

This report uses the validated screenshot interpretation below.

| Holding | Qty | Last price | Market value | Current role |
|---|---:|---:|---:|---|
| Cash | — | — | $2,214,955.47 | AB4 baseline reserve |
| STRC | 3002 | 99.9697 | $300,109.04 | AB4 baseline yield/cash-equivalent reserve |
| MSTR common | 4 | 185.34 | $741.36 | negligible direct MSTR sleeve exposure |
| MSTR Jun 05 '26 $190 Call | -117 | 11.29-11.82 (OCR range) | -~$132K to -$143K | AB2 short-call income / negative-delta overlay |
| MSTR Jun 18 '26 $190 Call | -55 | 15.35 | -$85,662.50 | AB2 short-call overlay |
| MSTR Jan 15 '27 $170 Call | 200 | 53.50 | $1,074,500.00 | core AB3 conviction exposure |
| MSTR Jan 15 '27 $170 Put | 22 | 34.35 | $75,020.00 | hedge / risk-shaping sleeve |
| MSTR Jan 21 '28 $130 Call | 17 | 100.01 | $166,472.50 | longer-dated AB3 conviction exposure |

### Total assets used
- **Portfolio NAV:** `$3,602,810.87`

### Important data note
The screenshot total-position line and some OCR-derived row values are not perfectly clean. For allocation percentages and adjustment sizing, the report uses the validated holdings table above and treats exact option valuations as **provisional** until a broker export is available.

---

## 5. AB4 benchmark prescription, quantified

## 5.1 Core benchmark
Given the profile inputs, the cleanest benchmark is:

### AB4 benchmark
- **MSTR sleeve target:** **40.0%** of NAV
- **Cash / cash-equivalent floor:** **$240,000 minimum** including `STRC`
- **Remaining capital:** rotational reserve and opportunity capital until a better non-MSTR sleeve or a stronger MSTR asymmetry justifies deployment

Using current NAV of `$3,602,810.87`:

- **40.0% MSTR sleeve target = $1,441,124**
- **Cash/STRC floor = $240,000**

## 5.2 Benchmark by asset class (current recommended AB4 frame)

Because the current portfolio is effectively a one-theme architecture centered on MSTR, the benchmark should currently be described by **asset class / role** rather than by many sleeves.

| Asset class / role | Benchmark target | Notes |
|---|---:|---|
| MSTR sleeve (net, bullish + bearish) | 40.0% | Core rotational sleeve, can be expressed through common, LEAPs, short calls, puts |
| STRC / cash-equivalent reserve floor | 6.7% minimum | Hard floor, can be above this |
| Additional cash / reserve / staging capital | 53.3% flexible | Default home for undeployed capital until asymmetry justifies action |

This is the cleanest benchmark expression from the inputs given so far.

---

## 6. Current portfolio vs benchmark

## 6.1 Current MSTR sleeve estimate
Using the corrected holdings table above, the current **net MSTR sleeve market value** is approximately:

- MSTR common: `$741`
- Jun 05 '26 $190 calls: `-~$143,325`
- Jun 18 '26 $190 short calls: `-$85,662`
- Jan 15 '27 $170 calls: `$1,074,500`
- Jan 15 '27 $170 puts: `$75,020`
- Jan 21 '28 $130 calls: `$166,472`

### Estimated net MSTR sleeve
**~$1.088M**

### Estimated sleeve weight
**~30.2% of NAV**

### Gap vs 40% target
- **Target:** `$1,441,124`
- **Current estimate:** `~$1,087,746`
- **Shortfall:** `~$353,378`
- **Shortfall as % of NAV:** `~9.81%`

## 6.2 Current reserve posture
- Cash: `$2.215M`
- STRC: `$300K`
- Combined reserve-like sleeve: `~$2.515M`

This is **far above** the hard floor of `$240K`.

That means the portfolio currently has:
- ample reserve
- meaningful optionality
- enough liquidity to repair a benchmark underweight if charts justify it

## 6.3 Current bucket interpretation

| Bucket / role | Current estimate | Comment |
|---|---:|---|
| AB4 reserve | very high | far above hard floor, gives exceptional flexibility |
| AB3 core conviction | ~34.5% of NAV | Jan '27 + Jan '28 longs + negligible common |
| AB2 overlay | ~-6.4% of NAV net market value effect | two short-call overlays are materially suppressing net sleeve exposure |
| Hedge | ~2.1% of NAV | long Jan '27 puts |

---

## 7. Personalized Layer 2 diagnosis

## 7.1 Core Layer 2 question
Relative to the AB4 benchmark, where is the best opportunity to capture more profit or improve risk control?

## 7.2 Current answer
The corrected answer is:

### **The portfolio is materially underweight the 40% MSTR benchmark unless chart ambiguity is high enough to justify standing aside.**

Instead of a slight underweight, the current portfolio is:
- **~30.2% net MSTR sleeve exposure**
- **~9.8% of NAV below benchmark**
- carrying a large negative overlay from the two short-call positions

That changes the interpretation materially.

## 7.3 Why
Because the current stack says:
- Layer 0 supportive
- Layer 0.5 still cautious
- Layer 1 selective
- and your own override rule says chart ambiguity is a valid reason to abandon the 40% rule temporarily

Therefore the best current Layer 2 read is:

> **If the chart is ambiguous, the current underweight can be tolerated as a temporary defensive deviation. If the chart is not ambiguous, the current sleeve is too far below benchmark and should be repaired first through overlay reduction, then through AB3 re-expansion if needed.**

---

## 8. Personalized Layer 3 prescription, quantified

This section is the actual portfolio prescription.

## 8.1 Benchmark recommendation

### Benchmark recommendation now
1. **Preserve the reserve floor** without question
2. **Preserve the 40% MSTR sleeve doctrine** as the default benchmark
3. Recognize that the portfolio is currently **materially underweight** that benchmark
4. Use the **short-call overlays** as the first repair lever before touching AB3 core

That means the portfolio should currently be run with this priority order:

### Adjustment priority order
1. **Jun 05 '26 $190 short calls**
2. **Jun 18 '26 $190 short calls**
3. **Jan 15 '27 $170 puts**
4. **Jan 15 '27 / Jan 21 '28 long calls** (AB3 core, touch last unless you are deliberately rebuilding toward benchmark)

This is the most important sequencing recommendation in the whole report.

---

## 8.2 Most critical adjustments to make now

Given the current shared-layer backdrop and your objectives, the most critical current adjustments are:

### Adjustment 1 — Recognize the underweight correctly
The portfolio is not slightly underweight. It is **~$353K below** the 40% sleeve target.

That means the real question is not whether to ignore a small gap. The real question is:
- is the chart ambiguous enough to justify staying this far underweight?
- or should the sleeve be rebuilt closer to benchmark?

### Adjustment 2 — Treat the Jun 05 short calls as the first active repair lever
Because the Jun 05 calls are **short**, not long, they should be interpreted as a meaningful suppressor of net MSTR sleeve exposure.

That means the first live decision is whether to:
- maintain them if your chart read is cautious
- partially cover them if your chart read is improving
- fully cover them if your chart read turns clearly constructive

### Adjustment 3 — Protect the AB3 core unless you are deliberately re-optimizing the benchmark sleeve
For now, treat the **Jan '27 $170 calls** and **Jan '28 $130 calls** as the protected structural core.

That means:
- do **not** trim AB3 first just because the short-term tape gets messy
- use overlays first
- only add to AB3 if you decide the underweight should be repaired through longer-duration exposure rather than through short-covering alone

---

## 8.3 Contract-level recommendation ladder

Because chart precision is still missing from this report, the cleanest way to be precise is through a **conditional recommendation ladder**.

### State A — Current base case: ambiguous / selective caution
**This is only appropriate if your chart read is genuinely ambiguous.**

Recommended posture:
- **AB3 core:** no change
- **Jun 05 '26 $190 short calls:** maintain current `-117`
- **Jun 18 '26 $190 short calls:** maintain current `-55`
- **Jan '27 puts:** maintain current `+22`
- **MSTR sleeve target:** accept current `~30.2%` only as a temporary defensive underweight

Interpretation:
- benchmark says 40%
- current evidence would have to be ambiguous enough to justify staying ~9.8% underweight

### State B — Constructive upside confirmation
If the charts become materially constructive again, the cleanest way to restore the sleeve toward 40% is to reduce the short overlays first.

#### Preferred refill options
**Option B1:** cover **50-75** of the `-117` Jun 05 short calls
- estimated sleeve restoration: `~$56K-$85K`
- first repair step because it removes the nearest suppressor of upside expression

**Option B2:** cover **20-30** of the `-55` Jun 18 short calls
- estimated sleeve restoration: `~$31K-$46K`
- good second repair step if you want a more gradual rebuild

**Option B3:** if you want to restore benchmark through AB3 instead of short-covering, add **66 Jan 15 '27 $170 calls**
- estimated added market value: `~$353,100`
- this is the cleanest direct one-step restoration of the benchmark gap using current prices

**Option B4:** alternatively add **35 Jan 21 '28 $130 calls**
- estimated added market value: `~$350,035`
- slightly underfills the full gap but keeps the add very long-duration

**Option B5:** full overlay normalization path
- cover **all 117** Jun 05 shorts and **all 55** Jun 18 shorts
- then add roughly **23 Jan '27 $170 calls** or **12 Jan '28 $130 calls** to finish the move toward 40%

### State C — Early rollover / diminishing upside
If MSTR starts rolling over but the top is not yet fully confirmed:

#### Preferred adjustments
**Option C1:** keep the `-117` Jun 05 shorts in place
- they are already doing useful defensive and income work

**Option C2:** increase Jun 18 short calls from `-55` to **-65 or -75**
- adds income
- reduces delta progressively
- best aligns with your stated rotational style

**Option C3:** keep AB3 core intact at this stage
- do not start cutting Jan '27 / Jan '28 core too early

### State D — Top largely confirmed, but before the drop
If the chart moves from “rollover risk” to “top largely confirmed”:

#### Preferred adjustments
**Option D1:** increase short calls from `-117 / -55` toward a more defensive overlay mix first
- the exact ratio depends on where you want net delta to land

**Option D2:** hold or modestly increase the `+22` Jan '27 puts if you want cleaner negative-delta protection

**Option D3:** trim **10-20** of the Jan 15 '27 $170 calls only after the overlay layer has already been optimized
- use AB3 trimming as a second-order lever, not first response

---

## 9. Ranked recommendation set

## Rank 1 — Best fit right now
### **Reclassify the portfolio as materially underweight benchmark, and let chart clarity decide whether to keep that underweight or repair it first through short-call reduction.**

Why this ranks first:
- it reflects the corrected asset sign
- it matches your rotational process better
- it identifies the right first levers
- it prevents false comfort from the earlier understated underweight

## Rank 2
### **If constructive confirmation appears, cover part of the Jun 05 shorts first, then part of the Jun 18 shorts, before adding fresh AB3 size.**

Why this ranks second:
- cleaner than immediately buying more long exposure
- preserves your existing structure
- restores benchmark in the order most consistent with your style

## Rank 3
### **If rollover strengthens, keep the Jun 05 shorts, add more Jun 18 short-call pressure, and leave the AB3 core mostly intact.**

Why this ranks third:
- aligns directly with your stated rotational process
- uses overlays first
- preserves optionality for deeper defensive rotation later

---

## 10. What is still missing for a production-grade version

You were right that Discord naturally pulled the first version toward prose.

The next production-grade version should incorporate:

### 10.1 Exact broker-export math
- clean contract values
- net delta / gamma / theta by sleeve
- exact net MSTR sleeve measurement by strategy leg

### 10.2 Required chart package
For GitHub review and later personalized-channel delivery, the report should include:

1. **MSTR price structure chart**
   - stage / price-action context
   - local trend line / breakdown / breakout status

2. **LOI + CPS panel**
   - where AB3 structural opportunity sits
   - whether stage is watch / forming / confirmed

3. **VLT recovery / deterioration panel**
   - confirms or weakens timing quality

4. **Force Field + FF ROC panel**
   - for tactical deterioration / exhaustion / acceleration

5. **MSTR sleeve composition chart**
   - AB4 reserve
   - AB3 core
   - AB2 overlay
   - hedge
   - current vs benchmark

6. **Contract-adjustment table**
   - exact contract counts to add / trim / cover under each chart state

### 10.3 Quantitative ruleset upgrade
The later version should explicitly calculate:
- benchmark MSTR sleeve target in dollars
- actual sleeve exposure in dollars and %
- contract-count changes needed to restore / reduce / neutralize sleeve posture
- projected delta change from each recommended adjustment

---

## 11. Bottom line

The most important quantitative conclusion in this report is:

- **Target MSTR sleeve:** `$1.441M` (40.0% of NAV)
- **Current estimated MSTR sleeve:** `~$1.088M` (30.2% of NAV)
- **Shortfall vs target:** `~$353.4K` (9.81% of NAV)

The most important strategic conclusion is:

> **The corrected portfolio is materially underweight the 40% MSTR benchmark. If the chart is ambiguous, that underweight can be tolerated temporarily. If the chart is constructive enough, the first repair action should be covering short-call overlays, starting with the Jun 05 line, before deciding whether new AB3 size is still needed.**

The most important sequencing conclusion is:

> **First adjust the Jun 05 shorts and the Jun 18 short calls. Touch the Jan '27 and Jan '28 core only after the overlay layer has already been used or if you explicitly choose to rebuild benchmark exposure through longer-duration longs.**

That is the corrected current Layer 2-3 prescription I can give from the available data.
