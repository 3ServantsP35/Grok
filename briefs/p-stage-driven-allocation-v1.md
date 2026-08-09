# P-Stage-Driven Allocation — v1

**Author:** Archie (documenting), architecture by **Gavin**
**Date:** 2026-08-09
**Status:** **REFERENCE DOCUMENT — no build authorized.** Captures the architecture as specified
2026-08-09. Nothing in §9 is a work order.
**Rev 2 (2026-08-09):** direction endorsed by Gavin. §7.2 replaced with measured ORATS data +
IV-sensitivity analysis; §7.4/§5.1 capital-structure monitoring elevated to a hard requirement;
§7.5 All-Weather given a specified behavioral check; §10.7 and §11.5 added.
**Source:** Gavin's allocation table (private Google Sheet, single tab), read 2026-08-09 after three
in-session revisions.
**Supersedes in scope:** most of `briefs/`-adjacent work queued under the Grok Proposal
(see §9). Does not supersede `decision-hardening-doctrine.md`.

---

## §0 Purpose

This describes a fundamental change in how capital allocation is decided across the whole
framework. It is not an incremental adjustment to an existing engine. Read §1 and §4 before
touching any project listed in §9.

Sample portfolio figures from the source table are deliberately omitted. All prescriptions here
are percentages; dollar specifics live outside tracked files per CLAUDE.md.

---

## §1 What changed

**Before:** each theme reasoned about its own allocation. Regime context flowed top-down through
the layer stack, with Howell phase driving the AB4 benchmark directly. Themes were parallel
consumers of shared context.

**After:** **MSTR's stage is the master switch.** One classification (S1–S4) drives the allocation
vector across every sleeve simultaneously. Everything upstream exists to sharpen and confirm that
one call.

The causal claim underneath it:

> Global liquidity growth drives MSTR. MSTR's observable stage is therefore a readable proxy for
> where liquidity is in its cycle. Stage → allocation across all themes.

**The four-year cycle is a communication device, not a load-bearing assumption.** Gavin's position
(2026-08-09): it does not matter whether the four-year periodicity holds, because its purpose is to
make the strategy explicable. The mechanism — liquidity drives MSTR — is the part that must hold.
See §5 and §6 for how each is treated differently.

**Primary goal:** substantial continuous income, with portfolio growth taken in waves when
liquidity surges. Income is the constant; growth is episodic.

---

## §2 The allocation prescription

Identical in both four-year blocks (2026–2029 and 2030–2033). The second block is the same
prescription against a compounded base, not a different strategy.

| Sleeve | Asset / expression | S1 | S2 | S3 | S4 |
|---|---|---:|---:|---:|---:|
| MSTR | MSTR covered-call strategy | 40 | 40 | 20 | 10 |
| Visser | XLK covered calls *(or Visser cherry-picking)* | 20 | 20 | 10 | 0 |
| Gold | GLD covered-call strategy | 10 | 10 | 10 | 20 |
| All Weather | BIGY & STRC | 10 | 10 | 20 | 20 |
| All Weather | ALLW | 10 | 10 | 20 | 20 |
| All Weather | Cash | 10 | 10 | 20 | 30 |
| | **Total** | 100 | 100 | 100 | 100 |

**Stage economics** (as specified; direction, not doctrine):

| | S1 | S2 | S3 | S4 |
|---|---:|---:|---:|---:|
| Stage Yr Appr (annual) | 0% | 100% | 10% | 0% |
| Stage Mo Yield (monthly) | 4% | 2% | 3% | 2% |

Income is computed on the **running balance**, so a full cycle compounds the base by
1.0 × 2.0 × 1.1 = **2.2×**, which is exactly the ratio between the first and second block's
income rows. The model is internally consistent on that point.

Per-asset appreciation assumptions retained in the source table: MSTR 30%, Visser 15%, Gold 8%,
BIGY & STRC 10%, ALLW 0%, Cash 0% — blending to 16.8% at S1 weights. **Open:** whether this column
is now reference-only, since it disagrees with `Stage Yr Appr` S1 = 0% (§10.1).

---

## §3 Stage semantics — the two levers

The stage sets **two** things. Weights are the smaller lever.

### 3.1 Allocation (the visible lever)

Risk-on in S1/S2; de-risk through S3; maximum defense in S4. Cash and Gold absorb what MSTR and
Visser give up. Straightforward.

### 3.2 Call-overlay intensity (the larger lever)

**S1 and S2 hold identical weights.** The entire difference between them is how hard short calls
are written — and call aggression runs *inverse* to expected appreciation:

- **S1 — accumulation.** No appreciation expected, so upside is sold hard (4%/mo). Simultaneously
  the cheapest point to accumulate AB3 call LEAPs ahead of the S2 wave. S1 is not the dull stage;
  it does two jobs at once.
- **S2 — stand down.** Call writing drops to 2%/mo deliberately, so the 100% appreciation year is
  not capped. This is the discipline most covered-call programs lack — they write through the rally
  that was supposed to pay for everything.
- **S3 — re-harvest.** Appreciation decays to 10%; writing goes back up to 3%/mo.
- **S4 — defense.** Least exposure to write against; 2%/mo.

**Consequence:** a stage engine that only resolves weights is insufficient. The S1/S2 boundary is
invisible in the allocation table and carries the majority of the economic outcome. See §7.1.

---

## §4 The architecture

### 4.1 Layer stack and authority

| Layer | Role | Authority |
|---|---|---|
| 0.5 / 0.75 (liquidity-bearing) | Confirm the stage — Howell phase, GLI, Capital Wars | **Confidence, not label** |
| 0.75 (thesis-bearing) | APE / company-level advisory | Advisory only |
| **Stage engine** | Declares S1–S4 from MSTR's own structure | **Sole owner of the label** |
| AB4 | Sleeve weights (§2) | Prescribed by stage |
| AB1 | Call overlay intensity | Prescribed by stage |
| AB3 | Optional overallocation / leverage | Recommended, not prescribed |
| AB2 | User-designated side bets | Discretionary |

**The key separation — label vs. confidence vs. action:**

- **Label** comes from MSTR's own structure (price, MVRV, super-long-timeframe SRI). Mechanical,
  hardened, single source. Upstream layers never override it.
- **Confidence** comes from upstream. Does the liquidity picture corroborate the stage MSTR is
  printing? Since the baseline assumption is that liquidity *drives* MSTR, liquidity is the
  mechanism and MSTR price structure is the observable — corroboration is meaningful evidence,
  not decoration.
- **Action** is gated by confidence, not by label alone. A low-confidence S2 declaration throttles
  the call overlay partway and sizes AB3 small rather than committing the full posture.

This is the operational meaning of "influential and informative, not authoritative" (Gavin,
2026-08-09). Given the low tolerance for a wrong stage call, confidence-gating is where that low
tolerance gets expressed.

### 4.2 The AB mapping

The allocation table **is AB4** — the prescribed baseline, *not* a cash bucket. This matches live
doctrine (`trading-rules.md:117`: AB4 is "a baseline, not a cash bucket"). Everything else layers
on top of it.

- **AB4** — hold the prescribed weights. Instrument-agnostic: you are AB4 whether you hold shares
  or express the weight otherwise, as long as you do not exceed the prescription.
- **AB1** — the covered-call overlay. **The short calls *are* the delta/theta bets**; there is no
  separate theta program by default. Written against **both** the share base **and** AB3 LEAPs.
  Additional theta structures exist only if the user explicitly designates side bets.
- **AB3** — overallocation and leverage; exposure *beyond* the prescribed weight. LEAPs are the
  instrument. **Not prescribed, but recommended as a consideration:**
  - **S1** — accumulate call LEAPs cheaply ahead of the S2 wave.
  - **S3–S4** — put LEAPs as bearish transition bets.
  This is an activation of existing doctrine, not a new concept: `trading-rules.md:117` already
  specifies the MSTR sleeve carries "bullish + bearish expressions" and instructs to "manage
  aggregate delta across stages, not long-only."
- **AB2** — user-designated side bets. Discretionary, outside the prescription.

**Measurement consequence.** Under `notional_delta_convention.md`, AB3 footprint is
**underlying-equivalent notional**, not premium paid. A cheap S1 LEAP is small in dollars out the
door and large in AB3 terms. That is the correct treatment, but it means "accumulated cheaply"
will read as expensive to the deviation tiers — **the AB3 tier thresholds likely need
stage-awareness rather than being absolute** (§10.5).

**Existing governance slots on unmodified:** tier A/B/C/D deviation, Tier D → owner override,
single-name > 5pp → PPR concentration review, `ab_profile_resolver.py`, `ab3_deviation_log`.
Stage-driven allocation simply gives that machinery a benchmark that moves. Integration cost is
low — materially lower than the Grok proposal, which required new plumbing throughout.

### 4.3 Transition mechanics

- **User-driven**, not system-executed. The system declares the stage and specifies the target
  vector; it does not time or execute the glide.
- Pre- and post-transition targets are set by the user.
- Realistic horizon ≈ **3 months** for a transition to play out.

---

## §5 Baseline assumptions and their monitors

### 5.1 "MSTR is driven by global liquidity growth and will not decouple"

**Treatment:** assume it holds; build a standing method to retest whether it ever breaks down.
It is an assumption under monitoring, not a belief.

**Unification worth noting:** persistent disagreement between MSTR's declared stage and the
liquidity layer *is* the decoupling test failing. The confirmation mechanism of §4.1 and the
decoupling monitor are **the same instrument read at two horizons** — short disagreement means low
confidence; sustained disagreement means the baseline assumption is failing. One build serves both.

**The monitor MUST watch capital structure, not only price correlation** — mNAV, convert issuance,
the preferred stack. Elevated to a hard requirement by Gavin 2026-08-09 ("correct and
non-negotiable"). MSTR can print a stage for reasons that have nothing to do with global liquidity,
and price correlation alone will not separate those cases. See §7.4.

### 5.2 "The liquidity cycle is four years"

**Treatment:** explicitly *not* load-bearing. Retained because it makes the strategy explicable.
No validation effort should be spent defending the periodicity. See §6.

---

## §6 Validation methodology

Governed by the E1–E7 Rules of Evidence (`briefs/p-indicator-methodology-v1.md`).

**The constraint, stated plainly:** a four-year-cycle stage model **cannot be validated on available
history.** BTC offers roughly three cycles; MSTR-as-proxy perhaps one and a half. Three observations
will not support a confidence claim about anything. Pretending otherwise repeats the error class
that produced four false "no signal" results before 2026-08-03.

**Therefore validate below the cycle horizon.** The testable claim is not "the four-year cycle is
real." It is:

> In the N months following a declared stage transition, the prescribed posture outperforms the
> prior posture.

That claim has dozens of observations across assets rather than three, it is the thing actually
acted upon, and it is falsifiable. Same correction that reclassified the earlier null results as
measurement error: right objective, right horizon.

**Every driver and gate must carry objective + horizon + n** before it is allowed to influence a
stage call (E1/E2/E4). Unsourced percentages are demoted to priors.

**Audit instrument:** `scripts/posthoc_review.py` fits directly as the post-hoc review mechanism
for stage calls.

---

## §7 Risks and open design issues

### 7.1 The S1→S2 boundary carries nearly all the economic weight — and the weights don't mark it

S1 and S2 are allocated identically. The only thing that changes is call aggression, and it changes
across the year that produces essentially all of the appreciation.

- **Late into S2:** calls written into the rip; the wave the entire four-year thesis depends on gets
  capped.
- **Early into S2:** income forfeited for nothing.

**Implication for the work plan:** stage-accuracy effort should be weighted specifically at the
S1→S2 transition, not spread evenly across all four boundaries. This is where the super-long-timeframe
SRI should be pointed first.

### 7.2 The 4% S1 yield is achievable at current IV, with essentially no margin

**Measured against live ORATS data** (snapshot 2026-08-07 21:00 UTC; MSTR spot $100.02;
surface IV ≈ 0.71). Call premium as % of spot:

| Strike | 28 DTE | 35 DTE | Delta (35d) |
|---|---:|---:|---:|
| 100 (ATM) | 7.93% | **8.86%** | 0.547 |
| 105 (+5%) | 5.85% | 6.83% | 0.460 |
| 110 (+10%) | 4.32% | 5.15% | 0.380 |

At S1 weights the other sleeves contribute roughly **0.51%/mo** to the portfolio (Visser ~1.25%,
Gold ~1%, BIGY & STRC ~1%, ALLW ~0.25%, cash ~0.35%, at their respective weights). Clearing 4%
therefore requires **~8.7%/mo from the MSTR sleeve**.

**8.7% required vs. 8.86% available at 35-DTE ATM.** The target is not merely "aggressive" — it is
calibrated to full at-the-money writing on essentially the entire sleeve, at ~35 days, with roughly
2% headroom. Writing 5% OTM instead yields 6.83%, which drops the portfolio to ~3.2%/mo.

**Delta consequence:** ATM delta is 0.547, so the sleeve retains only ~45% of MSTR's upside at all
times while the program runs. In S1 that is the intended trade. But it means the book is already
half-capped continuously, *before* any late-S2 error — so §7.1 compounds from a worse starting
point than originally stated.

**IV sensitivity — the structural tension.** Near-ATM IV (delta 0.45–0.60, 21–42 DTE) across the
full ORATS history:

| | Feb | Mar | Apr | May | Jun | Jul | Aug |
|---|---|---|---|---|---|---|---|
| avg IV | 0.79 | 0.73 | 0.73 | **0.67** | 0.82 | 0.87 | 0.73 |
| range | .69–.91 | .65–.90 | .64–.88 | **.50**–.79 | .65–**1.18** | .60–1.09 | .62–.80 |

Premium scales roughly with IV, so the achievable portfolio yield maps to:

- **IV 0.50** (observed floor) → ~6.3% ATM → **~3.0%/mo** — misses by a quarter
- **IV 0.71** (current) → 8.86% → **~4.05%/mo** — clears
- **IV 0.87** (July avg) → ~10.9% → **~4.9%/mo** — comfortable

**Hypothesis, NOT a finding:** S1 is defined as the flat, basing stage, and flat regimes typically
compress IV. If that holds for MSTR, the income target is highest in exactly the stage where the
premium funding it is thinnest. **This is currently untestable** — ORATS history begins 2026-02-20,
six months, spanning at most one stage. Per E1/E2/E4 it is recorded as an open question (§10.7),
not asserted. What the data *does* establish: a 2:1 IV range inside six months moves achievable
yield from 3.0% to 4.9%, so the 4% carries real sensitivity regardless.

Still worth reconciling the full 4/2/3/2 row against `briefs/pmcc-findings-v1.md` before the
numbers harden; only the S1 leg has been measured here.

### 7.3 The known S1 ladder defect maps onto the most expensive available error

`project_mstr_stage_indicator` records an open defect: the S1 ladder's trailing-Fit mislabels
declines as basing. Under this architecture, a false S1 during a downtrend simultaneously:

1. moves AB4 to 40% MSTR,
2. starts AB3 LEAP accumulation into a falling knife,
3. turns on 4%/mo call writing.

Previously that defect produced a bad *analysis*. Now it moves the whole portfolio three ways at
once. **Recommend treating it as a ship-blocker rather than parallel work.**

### 7.4 The defensive sleeve holds Strategy credit

**STRC is MicroStrategy preferred.** In S4 the book is 10% MSTR equity plus 20% BIGY & STRC — so
the diversifier is correlated to the thing it is diversifying against, specifically in the scenario
that matters (an MSTR credit event). That is also precisely the scenario the §5.1 decoupling
assumption exists to monitor.

**REQUIREMENT (Gavin, 2026-08-09 — "correct and non-negotiable"): the decoupling monitor must
watch MSTR capital structure — mNAV, the preferred stack, convert dynamics — and the STRC leg, not
only price correlation.** MSTR can print a stage for reasons that have nothing to do with global
liquidity, and price correlation alone will not distinguish those. (BIGY's composition is
unconfirmed — §10.4.)

### 7.5 All Weather is the largest defensive allocation and the least analytically supported

In S3/S4, All Weather is 40–70% of the book across three rows. It has no indicators, no gates, and
no warehouse coverage — and the redefinition (§8.3) removes sector rotation to simplify further.
The largest allocation in the stages where capital preservation matters most would run on
essentially no signal.

**Specified minimum (Gavin, 2026-08-09):** ballast should not be over-engineered, but the sleeve
needs a *behavioral* check — "is the defensive sleeve still behaving like a defensive sleeve?" This
is a test, not a forecasting model, and requires no new indicators:

1. **Rolling correlation** of the All-Weather sleeve to the MSTR sleeve — expected low or negative.
2. **Drawdown participation** — during MSTR drawdowns, does All Weather hold up, or come along?

**This check and the §7.4 capital-structure monitor are largely the same instrument**, because STRC
sits inside All Weather. Strategy preferred behaving like Strategy equity rather than like ballast
*is* the credit-event signature. One test covers both, and it fails loudly rather than silently.

### 7.6 This descopes Visser

If XLK covered calls are an acceptable default for a sleeve that peaks at 20% and goes to 0% in S4,
then the cherry-picking apparatus — the ranker, LOI, the gate-conditional acceptance test that
returned INCONCLUSIVE on 2026-08-04, the AB4 gate that fires on only 1.6% of ticker-bars — becomes
optional infrastructure. The architecture is arguably indicating: default to XLK, stop spending
there. See §9.

---

## §8 Doctrine changes required

### 8.1 The locked ordering collides with this design

`trading-rules.md:113` currently locks: **Howell phase (regime) → AB4 (benchmark) → AB3
(deviation/governance) → APE/Visser (advisory).** Howell sits at the top and drives AB4 directly.

This design routes it differently: **MSTR stage → AB4**, with Howell *confirming the stage*.

This is the concrete instance of "upstream currently has too much authority." Note the change is a
demotion in **routing** and a promotion in **causal role** — Howell stops setting weights and starts
validating the mechanism that sets them. It is not a downgrade of the liquidity work.

### 8.2 The AB framework line in CLAUDE.md is stale

CLAUDE.md states "AB4 (cash/defensive) → AB3 (core equity) → AB2 (high-conviction directional) →
AB1 (income generation)." This contradicts both live doctrine files:

- `trading-rules.md:117` — AB4 is "a baseline, **not a cash bucket**"; AB3 is the deviation layer.
- `recovered-trading-doctrine.md:25` — "AB3 = core long-exposure decisions (add LEAPs / hold /
  unwind)."

**Recommend correcting the CLAUDE.md line.** It reproduces this exact misreading in every fresh
session.

### 8.3 The AllWeather profile is redefined, not renamed

`ab_profile_selection` carries a live `AllWeather` profile. This design **replaces** its approach —
sector rotation comes out in favor of simplicity. All five operators currently default to RAWHybrid,
so blast radius is presently low, but this is a redefinition of a live profile and needs a migration
decision.

### 8.4 Delivery constraint

Any doctrine landing from this must reach a `session_start[]`-reachable file or it is inert
(`lessons_doctrine_index_unreachable`). Twelve `mstr-knowledge/` files already breach the
12,000-byte inject guard (`project_doctrine_file_grooming`), so grooming becomes a prerequisite
rather than an optional cleanup.

---

## §9 Project impact

| Project | Effect |
|---|---|
| **MSTR Stage indicator** | **Promoted to critical path.** S1 ladder defect (§7.3) first; then transition-accuracy measurement weighted to S1→S2. |
| **Liquidity path** (Howell phase, GLI, Capital Wars ingest) | **Rises in importance** — now load-bearing for stage confidence. |
| **APE / RIS broken route** | **Priority drops.** Company-thesis content stays advisory. Note the split is by *content*, not layer number: liquidity-bearing inputs rise, thesis-bearing inputs do not. |
| **Visser Uplift** | Descoped toward an XLK default (§7.6). The five 4H CSV exports previously requested drop in priority unless cherry-picking is retained. |
| **Grok Proposal v1.1** | **Largely superseded — this is the simplification.** What survives is narrow: driver categories as evidence feeding stage determination and the decoupling monitor. Most of the seven queued fixes become moot. |
| **Indicator methodology (E1–E7)** | Becomes the governing standard for stage validation (§6). |
| **Decision hardening / `posthoc_review.py`** | Fits cleanly as the audit instrument for stage calls. No conflict — this design prescribes allocation from a classification; it does not generate picks. |
| **Doctrine grooming** | Now a prerequisite (§8.4), not optional. |
| **Alerting framework** | Stage-transition alerts become the highest-value alert class in the system. |
| **CLAUDE.md** | AB framework line needs correcting (§8.2). |

---

## §10 Open questions

1. **Is the per-asset `Apprec` column now reference-only?** It blends to 16.8% at S1 weights while
   `Stage Yr Appr` says S1 = 0%. Read as different concepts (long-run per-asset assumption vs.
   stage-realized), but unconfirmed.
2. **Does the system prescribe the call overlay, or only the stage?** If stage drives call
   aggression, the natural output is a target — delta band, DTE, percentage of position written, per
   sleeve per stage. That is an output class not produced today.
3. **Does the system need to output time-in-stage?** Position sizing and the 3-month transition both
   depend on whether you are early or late within a stage, not merely which stage it is.
4. **What is BIGY?** Composition unconfirmed; needed to assess the §7.4 correlation risk on that leg.
5. **Should AB3 deviation tiers become stage-aware?** Cheap S1 LEAPs carry large underlying-equivalent
   notional and will trip absolute thresholds (§4.2).
6. **Super-long-timeframe SRI — warehouse or chart-only?** Named as a primary stage-confirmation
   enabler. The warehouse is 4H and indicators accumulate forward only, so a very long timeframe will
   have few closed observations — the same n-problem that rendered VST unusable at 87 bars. Its actual
   observation count must be established before it is leaned on.
7. **Does MSTR's IV systematically compress in S1?** If it does, the 4%/mo target is highest in the
   stage where the funding premium is thinnest (§7.2). Not answerable today — ORATS history begins
   2026-02-20 and spans at most one stage. Becomes testable by joining IV history to stage labels
   once enough stage transitions are on record. Until then the 4% should be treated as
   IV-regime-dependent, not fixed.

---

## §11 Recommended sequence (not authorized)

1. **Quantify how much authority Layers 0.5/0.75 currently carry** against historical stage calls.
   Cheapest of the open studies, both series exist, and it settles the authority question with
   evidence rather than judgment.
2. **Establish whether liquidity phase leads or merely coincides with MSTR stage transitions, and by
   how long.** This sets how much weight confirmation deserves and is the foundation of both the
   confidence model (§4.1) and the decoupling monitor (§5.1).
3. **Fix the S1 ladder defect** (§7.3) — ship-blocker.
4. **Establish the super-long-timeframe SRI's observation count** (§10.6) before designing around it.
5. **Build the All-Weather behavioral check** (§7.5) — cheapest item on this list, needs no new
   indicators, and doubles as the STRC leg of the capital-structure monitor (§7.4).
6. **Reconcile the remaining 2/3/2 legs against `pmcc-findings-v1.md`** — the S1 leg is measured
   (§7.2); S2–S4 are not.

---

## Appendix — provenance

Architecture specified by Gavin in session 2026-08-09. Source table revised three times during that
session: the competing per-asset `Mo. Yield` column was removed (leaving `Stage Mo Yield` as the
single income source), PMCC references were replaced with covered-call language to reflect the AB4/AB3
separation, and the `Stage Yr Yield` label was corrected to `Stage Mo Yield`.

Related: `briefs/p-indicator-methodology-v1.md`, `briefs/p-visser-layered-logic-v1.md`,
`briefs/pmcc-findings-v1.md`, `mstr-knowledge/decision-hardening-doctrine.md`,
`mstr-knowledge/notional_delta_convention.md`, `mstr-knowledge/trading-rules.md`.
Memory: `project_grok_proposal`, `project_mstr_stage_indicator`, `project_indicator_methodology`,
`project_visser_uplift`, `project_doctrine_file_grooming`.
