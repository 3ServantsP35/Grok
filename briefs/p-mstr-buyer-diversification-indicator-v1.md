# P-MSTR-BUYER-DIVERSIFICATION — Buyer Diversification Indicator v1

**Project:** P-MSTR-BUYER-DIVERSIFICATION  
**Date:** 2026-05-17  
**Status:** Open  
**Author:** Cyler

---

## 1. Why this project exists

The current **Force Field / FF ROC** logic is valuable in part because **Strategy Inc** has functioned as the dominant and most legible transmission vehicle for bitcoin demand into the public equity / structured-credit complex.

That creates an important structural dependency:
- if Strategy remains the primary buyer and the primary monetizable public wrapper for bitcoin exposure, Force Field / FF ROC may continue to carry strong explanatory value
- if bitcoin buying becomes increasingly **diversified across multiple buyer cohorts**, the value of a strongly MSTR-centered force model may decline

This project exists to build a new indicator that tracks **buyer diversification** directly.

---

## 2. Core problem

The problem is not that Force Field is wrong.

The problem is that Force Field may become **less complete** if the market structure changes.

More specifically:
- today, MSTR-specific sponsorship and MSTR-linked transmission channels may explain an unusually large share of the action
- over time, that may weaken if bitcoin accumulation and related demand become more distributed across:
  - ETFs
  - treasury companies
  - corporates
  - sovereign or quasi-sovereign buyers
  - alternative public wrappers
  - broader ecosystem demand

If that happens, then **FF ROC deterioration may partly reflect declining MSTR centrality rather than straightforward deterioration in aggregate bitcoin demand quality**.

That distinction matters.

---

## 3. Core doctrine

The new buyer-diversification indicator should:
- be an **MSTR-theme structural context indicator**
- help interpret whether MSTR remains the dominant buyer-transmission vehicle
- help judge whether the current market is becoming more **MSTR-centric** or more **buyer-diversified**
- sit **alongside Force Field**, not replace it

That means the indicator’s job is not to answer:
- is MSTR bullish right now?

Its job is to answer:
- how concentrated is effective buyer power in the MSTR channel?
- is that concentration strengthening or weakening?
- is bitcoin demand becoming more diversified across competing channels?
- does FF ROC still deserve the same interpretive weight it had when MSTR dominance was greater?

---

## 4. Main project goal

This project should define a new indicator that helps answer:

> Is bitcoin demand still sufficiently concentrated through Strategy Inc and its related transmission channels that Force Field / FF ROC should remain a primary tactical read, or is buyer diversification increasing enough that the MSTR-centered model should be interpreted with more caution?

---

## 5. What the indicator should measure

At a high level, the buyer-diversification indicator should attempt to measure some combination of:

1. **MSTR buyer centrality**
   - how central Strategy remains as a monetizable public buyer / wrapper for BTC demand

2. **Alternative buyer breadth**
   - whether competing buyer cohorts are becoming more important

3. **Transmission dominance**
   - whether MSTR-linked instruments still dominate the public-market transmission of BTC demand

4. **Diversification trend**
   - whether the market is moving toward:
     - greater concentration in MSTR
     - or greater diversification across multiple buyer channels

5. **Interpretation impact on FF ROC**
   - whether Force Field / FF ROC should currently be trusted as a high-weight tactical read
   - or discounted somewhat because the market has become structurally less MSTR-centric

---

## 6. Working hypothesis

The working hypothesis is:

- **high MSTR buyer centrality** should increase the interpretive value of Force Field / FF ROC
- **high buyer diversification** should reduce the interpretive exclusivity of Force Field / FF ROC, even if FF ROC still contains useful information

This does **not** mean FF ROC becomes useless.

It means:
- the indicator may need a **weighting or confidence adjustment** based on how concentrated buyer power remains in MSTR

---

## 7. Candidate input categories

The new indicator will likely need a mix of proxies rather than a single clean series.

### 7.1 Strategy-specific demand proxies
Potential examples:
- MSTR relative strength versus BTC proxies
- MSTR relative strength versus IBIT or ETF complex
- MSTR financing / preferred / credit sponsorship state
- MSTR premium / wrapper-demand behavior

### 7.2 ETF and alternative public-wrapper proxies
Potential examples:
- ETF flows or ETF-relative strength proxies
- IBIT / BTC / MSTR relative relationships
- public wrapper dispersion beyond MSTR

### 7.3 Corporate / treasury buyer proxies
Potential examples:
- breadth of treasury-company participation
- new treasury-equity issuance or other monetizable BTC treasury expressions
- spread in performance between MSTR and alternative treasury vehicles

### 7.4 Ecosystem / broad market proxies
Potential examples:
- total crypto market breadth
- BTC dominance versus alt / ecosystem risk appetite
- whether BTC demand is broadening beyond MSTR-linked channels

### 7.5 Cross-ratio expressions
Likely useful category:
- ratio studies that tell us whether MSTR remains the preferred transmission vehicle or is losing relative centrality

---

## 8. What the indicator should output

A mature buyer-diversification indicator should likely produce outputs such as:

- **MSTR-dominant**
- **MSTR-led but broadening**
- **mixed transmission**
- **diversifying buyer base**
- **MSTR no longer dominant**

And possibly also:
- a confidence or interpretive-weight note for FF ROC, such as:
  - **FF ROC high relevance**
  - **FF ROC normal relevance**
  - **FF ROC discounted by buyer diversification**

That second output is especially important.

---

## 9. Role inside the MSTR theme architecture

The cleanest architectural role is likely:

- Force Field / FF ROC = still the primary **MSTR-centered tactical force read**
- Buyer Diversification Indicator = a **structural context / weighting read** that tells us whether MSTR remains central enough for FF ROC to deserve full interpretive weight

That means the new indicator probably belongs near the Force Field layer rather than deep inside macro or broad shared-theme work.

---

## 10. Important design constraint

This project should avoid a simplistic conclusion such as:
- more diversified buyers = bearish for MSTR

That is too crude.

The real issue is not directional by itself.

The real issue is:
- whether a more diversified buyer base makes the **MSTR-centered model less singularly explanatory**
- and therefore changes how we weight Force Field / FF ROC inside decision support

That is a more precise and useful framing.

---

## 11. Data and implementation questions

Open questions include:

1. Which parts of the needed buyer-diversification proxy set are already available in current live pulls?
2. Which required proxies would need new Archie-side data plumbing?
3. Can a useful v1 be built from existing ratios and public-wrapper comparisons alone?
4. Should the output be a discrete state engine, a continuous score, or both?
5. How should the indicator feed into MSTR Suite report wording and sleeve interpretation?

### Likely Archie dependency
If the current warehouse does not already contain the right public-wrapper, ETF-flow, treasury-breadth, or buyer-breadth proxies, this could become an **Archie-priority data-expansion task**, because it directly affects the future trustworthiness of the top-priority MSTR theme.

---

## 12. Immediate next steps

1. define the candidate proxy set for buyer concentration vs diversification
2. check which proxies are already present in the live warehouse or current themes
3. define the first-draft state outputs
4. define how the indicator should modify FF ROC interpretation
5. determine whether Archie-side data expansion is required for v1

---

## 13. Bottom line

The MSTR theme needs a new project because Force Field / FF ROC is strongest when MSTR remains the dominant buyer-transmission vehicle for bitcoin demand.

If that market structure changes, we need a way to track it directly.

This project therefore exists to build a **buyer diversification indicator** that tells us whether:
- MSTR remains central enough for FF ROC to keep full interpretive weight
- or whether growing diversification in bitcoin buying requires a more cautious reading of the MSTR-centered force model
