# P-MSTR-SLEEVE — MSTR Sleeve Doctrine v1

**Owner:** Cyler (CIO)  
**Last Updated:** 2026-06-06  
**Status:** Draft for review & lock (Benchmark Version)

---

## 1. Theme Identity & Scope

MSTR Sleeve Doctrine defines how the default 40% MSTR allocation (adjustable by owner directive) is expressed rotationally across market stages using aggregate delta management rather than passive long-only ownership. The sleeve is explicitly exempt from the 20% per-asset soft cap while the default allocation remains active.

This brief covers only the MSTR rotational sleeve. It does not replace AB4 benchmark setting, AB3 deviation rules, or the core SRI stage machine.

## 2. Theme Objective (Fixed)

The MSTR sleeve exists to generate risk-adjusted alpha and income inside the default 40% allocation by rotationally expressing bullish, neutral, and defensive postures across SRI stages through aggregate delta management and options overlays — always clearing the STRC hurdle rate.

## 3. Integration Contract (Fixed)

**Purpose of this section:** Define exactly how upstream doctrine and data sources constrain and inform the MSTR sleeve, and what happens when required inputs are missing or stale.

**Requirements for completeness:**
- Must describe how Howell phase, GLI Z-score, liquidity regime (Rule 3), AB4 benchmark, and AB3 tier rules shape sleeve posture.
- Must list primary data sources and explain *how each is used* in the decision process.
- Must define clear fail-closed conditions tied to those sources.

**Upstream Layer Impact:**
- **Howell Phase & GLI:** Sets the macro regime bias. In Turbulence or GLI contraction (Z < -0.5), the sleeve defaults to more defensive aggregate delta targets unless VLT confirmation is strong.
- **Liquidity Regime (Rule 3):** In EXPANDING regimes (HYG SRIBI > 0, VIX LOI < 0), VST/ST signals receive elevated weight for tactical delta adjustments. In CONTRACTING regimes, LT/VLT confirmation is required before any material increase in aggregate delta.
- **AB4 / STRC Hurdle:** Every sleeve expression must clear the 0.83%/month STRC yield. No new capital deployment is permitted if the expected return does not exceed this hurdle.
- **AB3 Tier Rules:** Sleeve delta increases are gated by AB3 tier thresholds. Tier D changes require owner override.

**Primary Data Sources & Usage:**
- `tv_state.md` (SRI_VLT, SRIBI_VLT, LOI, VST/ST indicators) — Primary source for stage classification and delta target calculation.
- mNAV (Market Cap / BTC holdings × BTC price) — Determines call vs put selling priority.
- On-chain Strategy holdings + convertible note calendar — Applies Saylor Event Discount during active issuance windows.
- OKX BTC-USDT ticker — Real-time BTC price for mNAV and delta calculations.

**Fail-Closed Rules:**
- If `tv_state.md` or required indicators are >1 trading day stale → default to neutral aggregate delta (0.50–0.60) and flag for immediate Cyler review.
- If mNAV data is unavailable → default to neutral call selling (0.20–0.25Δ) regardless of stage.

## 4. Indicator Consumption Contract

**Purpose of this section:** Specify exactly which indicators are used, why they matter to this theme, and the concrete signals that drive buy, sell, hedge, and income decisions.

**Requirements for completeness:**
- Must name specific indicators/TFs and explain their importance to the MSTR sleeve.
- Must describe the signals they generate and the precise conditions under which those signals trigger action (buy/sell/hedge/income).

**Indicators Used & Rationale:**

1. **SRI_VLT + SRIBI_VLT + Adaptive LOI (Primary)**  
   - Why important: These form the core stage classification and momentum signal for the MSTR sleeve. VLT is the all-weather timeframe; LOI provides the depth-of-trough signal that historically precedes the strongest risk-adjusted moves.
   - Key signals & conditions:
     - LOI < adaptive threshold (-43.6 for MSTR) + Stage 2 breakout → Primary trigger for AB3 call LEAP purchases.
     - LOI < -45 in Stage 1 chop → Income-max expression (PMCC short calls prioritized).
     - VLT crossing from negative to positive after deep trough → Confirmation for increasing aggregate delta.

2. **VST / ST (Tactical)**  
   - Why important: Used for short-term delta adjustments in EXPANDING liquidity regimes (Rule 3).
   - Key signals & conditions:
     - VST momentum thrust in Stage 2 → Tactical long delta increase (up to +0.10 aggregate).
     - VST reversal in Stage 3 → Early delta reduction signal.

3. **mNAV**  
   - Why important: Determines the relative attractiveness of call selling vs put selling.
   - Key signals & conditions:
     - mNAV ≥ 3.0x → Increase short-call priority (sell calls against existing long LEAPs).
     - mNAV ≤ 1.2x → Favor put selling or new LEAP additions.

4. **Confirmation Ladder (Watch / Forming / Confirmed / Invalidated)**  
   - Why important: Gates material changes in aggregate delta. Confirmed or higher is required for AB3-sized moves unless in Stage 1 chop.

**Concrete Decision Examples:**
- AB3 call LEAP purchase is triggered when LOI fires below adaptive threshold *and* either (a) Stage 2 breakout is Confirmed, or (b) deep discount occurs in Stage 1 with VLT turning positive.
- Short call income is increased when LOI is in the -45 to -20 zone in Stage 1 or when mNAV is elevated in Stage 3.
- Defensive put LEAPs or Expression 3 routing is activated when VLT remains negative for 5+ bars in Stage 4 or during active Saylor issuance windows.

## 5. Theme-Specific Engine (MSTR Sleeve Uniqueness)

**Purpose of this section:** Contain the unique rotation logic and aggregate delta targets for the MSTR sleeve.

**Stage-by-Stage Aggregate Delta Targets (starting benchmark):**

- **Stage 1 (Chop):** Target aggregate delta 0.30–0.50. Primary expression = PMCC short calls (0.20–0.25Δ, 7–14 DTE). Reduced long delta. Income is the priority.
- **Stage 2 (Recovery / Std):** Target aggregate delta 0.70–0.90. Primary expression = Long LEAPs (AB3) + opportunistic short calls. Bullish rotation.
- **Stage 3 (Trim Approach):** Target aggregate delta 0.50–0.70. Primary expression = Reduce new long LEAPs, increase short calls. Delta compression.
- **Stage 4 (Decline):** Target aggregate delta 0.20–0.40. Primary expression = Put LEAPs or Expression 3 routing. Defensive posture.

**Additional Modifiers:**
- Liquidity regime (Rule 3), mNAV overlay, and Saylor event discount are applied on top of the stage targets.
- All targets are subject to the STRC hurdle test before deployment.

## 6. Decision Framework & Output Contract (Fixed)

**Purpose of this section:** Define the exact output format and the specific triggers that would change the recommendation.

**Output Format (for PPR and morning brief):**
"MSTR sleeve recommended aggregate delta: X.XX | Primary expression: [Long LEAPs / PMCC / Put LEAPs] | Key drivers: [stage + regime + mNAV + LOI status] | Invalidation trigger: [specific level or stage transition]"

**Invalidation / Change Triggers (examples):**
- LOI crosses above adaptive threshold while in Stage 2 → Consider increasing long delta.
- VLT remains negative for 5+ bars in Stage 3 → Reduce aggregate delta.
- Active convertible note window + Stage 3 signal → Apply Saylor Event Discount (lower conviction).

## 7. Dependencies & Open Items

- Requires live `tv_state.md` and mNAV feed.
- Needs backtest validation of stage-by-stage delta targets (proposed R4).
- Must be reconciled with P-MSTR-SUITE-REPORT confirmation ladder once both are live.

---

**This version is now substantially more complete and can serve as the benchmark for other theme operating briefs.**