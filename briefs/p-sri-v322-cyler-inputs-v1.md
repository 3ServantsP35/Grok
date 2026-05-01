# P-SRI-v3.2.2 Build Inputs — Cyler Authored Seed Data v1
**Project:** P-SRI-V3.2.2-BUILD  
**Date:** 2026-05-01  
**Author:** Cyler (CIO)  
**Status:** Seed input for Archie implementation and v1 backtest

---

## Scope

This file answers three open items from `briefs/p-sri-v322-build-design-v1.md`:

1. **§7.1 AB4 benchmark seed weights**
2. **§7.2 AB3 Tier A/B/C/D placeholder thresholds**
3. **§7.5 RAW Hybrid AB3 doctrine (fast take)**

---

## One ambiguity to resolve explicitly

The biggest ambiguity is **Speculation**.

The Howell allocation tutorial contains both:
- **8.2 Speculation benchmark allocation (early / mid Speculation)**
- **8.3 Late Speculation benchmark allocation (transition risk rising)**

For the v1 resolver and `ab4_benchmark` seed table, I recommend:
- use **8.2 early / mid Speculation** as the canonical `phase='Speculation'` seed
- treat **late Speculation** as a later refinement, transition-state overlay, or v1.1 extension

Reason:
- the schema currently keys off the **four Howell phases**, not subphases
- seeding late Speculation directly into the single Speculation row would make the whole phase too defensive too early
- the more elegant long-term fix is either explicit subphase support or explicit transition portfolios, not silently collapsing late Spec into the canonical phase row

So the tables below use **early / mid Speculation**.

---

## Ask 1 — §7.1 AB4 benchmark seed weights

### Authoring rule
- **Rotational** = direct authored phase weights
- **All-Weather** = 50% compression toward the neutral/core baseline already defined in the Howell allocation tutorial
- **RAW Hybrid** = computed midpoint of Rotational and All-Weather, not authored here

### CSV-ready seed table

```csv
profile,phase,sleeve,sleeve_class,weight_pct
Rotational,Rebound,cash / equivalents,standard,5
Rotational,Rebound,short Treasuries,standard,5
Rotational,Rebound,long Treasuries,standard,0
Rotational,Rebound,investment-grade credit,standard,5
Rotational,Rebound,broad US equities,standard,15
Rotational,Rebound,defensive equities,standard,0
Rotational,Rebound,cyclical equities,standard,15
Rotational,Rebound,small caps,standard,10
Rotational,Rebound,commodities broad basket,standard,5
Rotational,Rebound,gold,standard,0
Rotational,Rebound,BTC proxy ETFs,special,10
Rotational,Rebound,international equities,standard,5
Rotational,Rebound,energy equities,standard,0
Rotational,Rebound,financials,standard,10
Rotational,Rebound,MSTR preferreds,special,5
Rotational,Rebound,MSTR common,special,10
Rotational,Calm,cash / equivalents,standard,5
Rotational,Calm,short Treasuries,standard,5
Rotational,Calm,long Treasuries,standard,0
Rotational,Calm,investment-grade credit,standard,10
Rotational,Calm,broad US equities,standard,15
Rotational,Calm,defensive equities,standard,5
Rotational,Calm,cyclical equities,standard,10
Rotational,Calm,small caps,standard,5
Rotational,Calm,commodities broad basket,standard,5
Rotational,Calm,gold,standard,5
Rotational,Calm,BTC proxy ETFs,special,5
Rotational,Calm,international equities,standard,5
Rotational,Calm,energy equities,standard,5
Rotational,Calm,financials,standard,10
Rotational,Calm,MSTR preferreds,special,5
Rotational,Calm,MSTR common,special,5
Rotational,Speculation,cash / equivalents,standard,10
Rotational,Speculation,short Treasuries,standard,5
Rotational,Speculation,long Treasuries,standard,0
Rotational,Speculation,investment-grade credit,standard,0
Rotational,Speculation,broad US equities,standard,10
Rotational,Speculation,defensive equities,standard,5
Rotational,Speculation,cyclical equities,standard,5
Rotational,Speculation,small caps,standard,0
Rotational,Speculation,commodities broad basket,standard,15
Rotational,Speculation,gold,standard,10
Rotational,Speculation,BTC proxy ETFs,special,10
Rotational,Speculation,international equities,standard,0
Rotational,Speculation,energy equities,standard,10
Rotational,Speculation,financials,standard,0
Rotational,Speculation,MSTR preferreds,special,10
Rotational,Speculation,MSTR common,special,10
Rotational,Turbulence,cash / equivalents,standard,20
Rotational,Turbulence,short Treasuries,standard,15
Rotational,Turbulence,long Treasuries,standard,15
Rotational,Turbulence,investment-grade credit,standard,5
Rotational,Turbulence,broad US equities,standard,0
Rotational,Turbulence,defensive equities,standard,10
Rotational,Turbulence,cyclical equities,standard,0
Rotational,Turbulence,small caps,standard,0
Rotational,Turbulence,commodities broad basket,standard,0
Rotational,Turbulence,gold,standard,15
Rotational,Turbulence,BTC proxy ETFs,special,0
Rotational,Turbulence,international equities,standard,0
Rotational,Turbulence,energy equities,standard,0
Rotational,Turbulence,financials,standard,0
Rotational,Turbulence,MSTR preferreds,special,15
Rotational,Turbulence,MSTR common,special,5
AllWeather,Rebound,cash / equivalents,standard,7.5
AllWeather,Rebound,short Treasuries,standard,7.5
AllWeather,Rebound,long Treasuries,standard,2.5
AllWeather,Rebound,investment-grade credit,standard,5
AllWeather,Rebound,broad US equities,standard,12.5
AllWeather,Rebound,defensive equities,standard,2.5
AllWeather,Rebound,cyclical equities,standard,10
AllWeather,Rebound,small caps,standard,7.5
AllWeather,Rebound,commodities broad basket,standard,5
AllWeather,Rebound,gold,standard,2.5
AllWeather,Rebound,BTC proxy ETFs,special,7.5
AllWeather,Rebound,international equities,standard,5
AllWeather,Rebound,energy equities,standard,2.5
AllWeather,Rebound,financials,standard,7.5
AllWeather,Rebound,MSTR preferreds,special,7.5
AllWeather,Rebound,MSTR common,special,7.5
AllWeather,Calm,cash / equivalents,standard,7.5
AllWeather,Calm,short Treasuries,standard,7.5
AllWeather,Calm,long Treasuries,standard,2.5
AllWeather,Calm,investment-grade credit,standard,7.5
AllWeather,Calm,broad US equities,standard,12.5
AllWeather,Calm,defensive equities,standard,5
AllWeather,Calm,cyclical equities,standard,7.5
AllWeather,Calm,small caps,standard,5
AllWeather,Calm,commodities broad basket,standard,5
AllWeather,Calm,gold,standard,5
AllWeather,Calm,BTC proxy ETFs,special,5
AllWeather,Calm,international equities,standard,5
AllWeather,Calm,energy equities,standard,5
AllWeather,Calm,financials,standard,7.5
AllWeather,Calm,MSTR preferreds,special,7.5
AllWeather,Calm,MSTR common,special,5
AllWeather,Speculation,cash / equivalents,standard,10
AllWeather,Speculation,short Treasuries,standard,7.5
AllWeather,Speculation,long Treasuries,standard,2.5
AllWeather,Speculation,investment-grade credit,standard,2.5
AllWeather,Speculation,broad US equities,standard,10
AllWeather,Speculation,defensive equities,standard,5
AllWeather,Speculation,cyclical equities,standard,5
AllWeather,Speculation,small caps,standard,2.5
AllWeather,Speculation,commodities broad basket,standard,10
AllWeather,Speculation,gold,standard,7.5
AllWeather,Speculation,BTC proxy ETFs,special,7.5
AllWeather,Speculation,international equities,standard,2.5
AllWeather,Speculation,energy equities,standard,7.5
AllWeather,Speculation,financials,standard,2.5
AllWeather,Speculation,MSTR preferreds,special,10
AllWeather,Speculation,MSTR common,special,7.5
AllWeather,Turbulence,cash / equivalents,standard,15
AllWeather,Turbulence,short Treasuries,standard,12.5
AllWeather,Turbulence,long Treasuries,standard,10
AllWeather,Turbulence,investment-grade credit,standard,5
AllWeather,Turbulence,broad US equities,standard,5
AllWeather,Turbulence,defensive equities,standard,7.5
AllWeather,Turbulence,cyclical equities,standard,2.5
AllWeather,Turbulence,small caps,standard,2.5
AllWeather,Turbulence,commodities broad basket,standard,2.5
AllWeather,Turbulence,gold,standard,10
AllWeather,Turbulence,BTC proxy ETFs,special,2.5
AllWeather,Turbulence,international equities,standard,2.5
AllWeather,Turbulence,energy equities,standard,2.5
AllWeather,Turbulence,financials,standard,2.5
AllWeather,Turbulence,MSTR preferreds,special,12.5
AllWeather,Turbulence,MSTR common,special,5
```

### Sum checks
Each `(profile, phase)` block sums to **100%**.

### Intent notes
- Rows with `0` are **intentional** and should remain explicit in the seed table.
- In Turbulence, **BTC proxy ETFs = 0** in Rotational is deliberate.
- In Turbulence, **MSTR common = 5** in both profiles is a deliberate residual-conviction allowance, not an accidental leftover.
- **MSTR preferreds** remain meaningfully funded in Speculation and Turbulence because they sit between ballast and conviction expression better than MSTR common.

---

## Ask 2 — §7.2 AB3 Tier A/B/C/D placeholder thresholds

These are **v1 operational thresholds** for the resolver, not final doctrine.

### Recommended interpretation rule
Measure tier size as:

> **absolute percentage-point deviation beyond the AB4 benchmark weight**

This is incremental overweight or underweight outside normal benchmark alignment / tolerance handling.

### Placeholder ladder by sleeve class

| Sleeve class | Tier A | Tier B | Tier C | Tier D |
|---|---:|---:|---:|---:|
| Standard diversified sleeves | > tolerance to 5pp | >5pp to 10pp | >10pp to 20pp | >20pp |
| Special sleeves | > tolerance to 3pp | >3pp to 6pp | >6pp to 12pp | >12pp |

### Resolver-friendly form

#### Standard diversified sleeves
- **Tier A:** deviation beyond tolerance, up to **5 percentage points**
- **Tier B:** **>5 to 10 percentage points**
- **Tier C:** **>10 to 20 percentage points**
- **Tier D:** **>20 percentage points**

#### Special sleeves
- **Tier A:** deviation beyond tolerance, up to **3 percentage points**
- **Tier B:** **>3 to 6 percentage points**
- **Tier C:** **>6 to 12 percentage points**
- **Tier D:** **>12 percentage points**

### Phase interpretation modifier
I would keep the resolver math simple in v1 and apply the phase nuance in **review language**, not in the numeric ladder yet.

That means:
- same numeric ladder in all phases for v1
- but **Turbulence** should narratively scrutinize a given tier more harshly
- and **Rebound** should narratively tolerate a given tier more easily

If you want a machine modifier later, I would add it in v2 rather than embed it into the first resolver release.

### Owner override handling
Tier D is where the system should most naturally escalate toward **owner override** language, especially for:
- special sleeves
- zero-benchmark sleeves
- Turbulence-phase offensive residuals

I would not automatically equate Tier D with owner override in code, but I would treat Tier D as the default place where the system asks:

> is this still framework-endorsed AB3, or has it become a knowingly non-framework position?

---

## Ask 3 — §7.5 RAW Hybrid AB3 doctrine (fast take)

RAW Hybrid AB3 deviations should be judged as a **true midpoint anchor with slight rhetorical lean toward Rotational discipline when conditions worsen**. In other words, it should not inherit Rotational’s full high-bar skepticism, but it also should not drift into All-Weather-style permissiveness just because the benchmark is smoother. The benchmark itself already softens the posture by construction, so AB3 review should remain meaningfully skeptical, especially in Speculation and Turbulence. My v2 doctrinal answer would be: **closer to midpoint in Rebound and Calm, closer to Rotational in Speculation and Turbulence**.

---

## Implementation notes for Archie

- Use the table above exactly for v1 seeding.
- Keep `Speculation` mapped to the **8.2 early/mid** row set for now.
- Treat **late Speculation** as a separate future enhancement, not silent v1 drift.
- Keep all zero rows explicit in `ab4_benchmark`.
- Let backtest tell us whether special-sleeve Tier C/D thresholds are still too wide.

---

## Recommended next refinement after v1 backtest

If the backtest is useful enough to justify v1.1 quickly, I would next add:
1. explicit **late Speculation** support or transition portfolios
2. phase-sensitive **Tier interpretation modifiers**
3. branch-specific special-sleeve overrides for:
   - BTC proxy ETFs
   - MSTR preferreds
   - MSTR common
