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

## 5.1 Two practical questions the indicator must answer

The v1 framework should be built around two practical questions:

1. **Which channel is currently carrying marginal BTC demand?**
2. **How concentrated is that demand in MSTR versus outside Strategy?**

These are more useful than trying to identify exact buyers with false precision.

The project should therefore be framed as a **buyer transmission and diversification indicator**, not a literal buyer-identity detector.

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

### 7.1 Strategy / MSTR channel proxies
Potential examples:
- `MSTR / BTC`
- `MSTR / IBIT`
- `MSTR / SPY`
- `STRF / LQD`
- `STRD / HYG`
- MSTR premium / wrapper-demand behavior

What these help answer:
- is Strategy still the preferred public transmission vehicle for BTC demand?
- is MSTR-specific sponsorship still dominant?

### 7.2 ETF channel proxies
Potential examples:
- `IBIT / BTC`
- `IBIT` versus `MSTR`
- ETF flow data, if accessible later
- BTC strength occurring without corresponding MSTR outperformance

What these help answer:
- is BTC demand increasingly being expressed through ETF channels instead of MSTR?

### 7.3 Other treasury / corporate channel proxies
Potential examples:
- breadth of treasury-company participation
- new treasury-equity issuance or other monetizable BTC treasury expressions
- spread in performance between MSTR and alternative treasury vehicles

What these help answer:
- is Strategy still unique, or is treasury-style BTC demand broadening into a wider corporate cohort?

### 7.4 Broad crypto-native channel proxies
Potential examples:
- `BTCUSD`
- `TOTAL`
- `TOTAL2`
- `BTC_D`
- `ETHUSD`
- `ETH_D`
- `STABLE_C_D`

What these help answer:
- is buying broadening across the crypto ecosystem rather than staying concentrated in MSTR-specific wrappers?

### 7.5 Macro / passive risk-on channel proxies
Potential examples:
- `SPY`
- `QQQ`
- `IWM`
- `BTC / QQQ` style comparisons where useful
- credit / dollar / vol context

What these help answer:
- is the move really BTC-specific, or is it being driven by broader macro beta and liquidity appetite?

### 7.6 Cross-ratio expressions
Likely useful category:
- ratio studies that tell us whether MSTR remains the preferred transmission vehicle or is losing relative centrality

This category likely becomes one of the most important because it converts raw price behavior into transmission-competition behavior.

---

## 8. What the indicator should output

A mature buyer-diversification indicator should likely produce outputs such as:

- **MSTR-dominant**
- **MSTR-led but broadening**
- **balanced transmission**
- **ETF-led**
- **broad crypto-led**
- **macro-risk-on-led**
- **MSTR no longer dominant**

And also a diversification state such as:
- **highly concentrated in MSTR**
- **moderately concentrated**
- **mixed**
- **broadly diversified**
- **MSTR losing centrality**

And possibly also:
- a confidence or interpretive-weight note for FF ROC, such as:
  - **FF ROC high relevance**
  - **FF ROC normal relevance**
  - **FF ROC reduced weight**
  - **FF ROC discounted by buyer diversification**

That third output is especially important because it converts the indicator into a practical decision-support tool.

## 8.1 Preferred v1 output structure

The v1 framework should likely produce three outputs:

### Output A — Buyer leadership state
Who appears to be leading marginal BTC demand?
- MSTR
- ETF
- broad crypto
- macro beta
- mixed

### Output B — Diversification state
How concentrated is buyer power?
- highly concentrated in MSTR
- moderately concentrated in MSTR
- mixed transmission
- broadly diversified outside MSTR
- MSTR no longer dominant

### Output C — FF relevance adjustment
How much interpretive weight should FF ROC receive right now?
- full weight
- normal weight
- reduced weight
- low exclusivity / discounted

This three-output structure is likely clearer than a single mystery score.

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

## 12. First-draft v1 framework

The v1 framework should be built as a **state engine first**, not a faux-precise score first.

### 12.1 Core logic

The engine should try to answer:
- is BTC demand currently being transmitted primarily through MSTR?
- through ETFs?
- through broad crypto participation?
- or through general macro beta / liquidity conditions?

And separately:
- is transmission becoming more concentrated in MSTR?
- or more diversified away from MSTR?

### 12.2 Minimal viable proxy stack

A sensible v1 starting stack would likely include:
- `MSTR / BTC`
- `MSTR / IBIT`
- `MSTR / SPY`
- `IBIT / BTC`
- `BTCUSD`
- `TOTAL`
- `TOTAL2`
- `BTC_D`
- `ETHUSD`
- `STABLE_C_D`
- `STRF / LQD`
- `STRD / HYG`
- `SPY`
- `QQQ`

This is not the final stack, but it is probably enough to begin classifying transmission leadership and diversification trend.

### 12.3 First-draft interpretation logic

Examples:

#### MSTR-dominant regime
Use when:
- BTC is strong
- MSTR is outperforming BTC and IBIT
- MSTR wrapper / credit proxies are supportive
- broader crypto breadth is not the main leader

#### ETF-led diversification regime
Use when:
- BTC is strong
- ETF proxies are improving
- MSTR is not uniquely outperforming
- public-market BTC demand appears to be broadening beyond MSTR

#### Broad crypto-led diversification regime
Use when:
- BTC is strong
- `TOTAL`, `TOTAL2`, `ETH`, and broader breadth are improving
- MSTR is no longer uniquely leading the move

#### Macro-risk-on-led regime
Use when:
- BTC strength is riding alongside broad risk-on assets
- macro beta appears to be carrying much of the move
- MSTR-specific dominance is weak or ambiguous

### 12.4 Practical use inside the MSTR theme

The main practical use of the v1 framework should be:
- preserve high confidence in FF ROC when MSTR remains central
- reduce FF ROC exclusivity when diversified transmission is increasing
- explain whether FF ROC deterioration reflects:
  - true deterioration in BTC demand quality
  - or a structural broadening of buyer channels away from MSTR dominance

## 13. Immediate next steps

1. check which v1 proxies are already present in the live warehouse or current themes
2. identify missing proxies that would require Archie-side expansion
3. define the threshold logic for the first discrete state engine
4. define how the MSTR Suite report should present buyer-transmission state
5. decide whether v1 should stop at state outputs or also publish a continuous score

---

## 14. Bottom line

The MSTR theme needs a new project because Force Field / FF ROC is strongest when MSTR remains the dominant buyer-transmission vehicle for bitcoin demand.

If that market structure changes, we need a way to track it directly.

This project therefore exists to build a **buyer diversification indicator** that tells us whether:
- MSTR remains central enough for FF ROC to keep full interpretive weight
- or whether growing diversification in bitcoin buying requires a more cautious reading of the MSTR-centered force model

The v1 framework should therefore focus less on literal buyer identity and more on two practical questions:
- **Which channel is currently carrying marginal BTC demand?**
- **How concentrated is that demand in MSTR versus outside Strategy?**