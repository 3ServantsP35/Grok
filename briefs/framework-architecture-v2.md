# MSTR Engine Architecture v1.0
**Date:** February 27, 2026  
**Authors:** Gavin (framework lead) + CIO  
**Status:** APPROVED

---

## Three-Layer Architecture

### Layer 1: REGIME ENGINE — "Where are we?"

The Regime Engine defines the economic and market environment. It constrains everything downstream — no signal or allocation decision happens without regime context.

#### 1A. Macro Regime (Howell Framework)

Four macro drivers, following Howell's framework for what drives asset prices:

| Driver | What It Measures | Primary Data | Howell Label |
|---|---|---|---|
| **Global Liquidity** | Net central bank balance sheet expansion/contraction + private credit | GLI proxy (4-bank → 28-bank target), M2, Fed/ECB/BOJ balances | "Liquidity Cycle" |
| **Global Economic Growth** | Real economic momentum | GEGI estimate, PMIs, employment, earnings revisions | "Growth Cycle" |
| **Inflation** | Price level trajectory | CPI, breakevens, commodity indices (DBC), Copper/Gold ratio | "Inflation Cycle" |
| **Interest Rates / Monetary Policy** | Cost of capital, yield curve shape | Fed Funds, 2Y/10Y Treasury, yield curve spread | "Monetary Cycle" |

**Howell's key insight we adopt:** These four cycles don't move in lockstep. They lead/lag each other in a sequence:

```
Liquidity leads → Growth follows → Inflation lags → Rates respond
   (6-12mo)         (3-6mo)          (6-12mo)         (reactive)
```

Each driver has three states:

| State | Liquidity | Growth | Inflation | Rates |
|---|---|---|---|---|
| **Expanding / Rising** | GLI Z > +0.5 | GEGI > 1.0 | CPI accelerating | Hiking / hawkish |
| **Neutral / Transitioning** | GLI Z: -0.5 to +0.5 | GEGI: 0 to 1.0 | CPI stable | Pausing |
| **Contracting / Falling** | GLI Z < -0.5 | GEGI < 0 | CPI decelerating | Cutting / dovish |

**Macro Regime output:** A 4-factor state vector.  
Example: `Liquidity: Contracting (Z=-1.01) | Growth: Neutral (GEGI=0.3) | Inflation: Falling | Rates: Cutting`

#### 1B. Asset Attractiveness (Howell-Aligned)

From the macro regime, Howell derives which asset classes are attractive. We adopt his framework:

| Macro Condition | Favored Assets | Howell Term |
|---|---|---|
| Liquidity expanding + Rates falling | **Hard assets, BTC, Gold, Risk-on equities** | "Liquidity Boom" |
| Liquidity expanding + Growth rising | **Equities, credit, cyclicals** | "Goldilocks" |
| Liquidity contracting + Inflation rising | **Commodities, TIPS, real assets** | "Stagflation" |
| Liquidity contracting + Growth falling | **Treasuries, cash, defensives** | "Deflation Risk" |
| Liquidity neutral + Rates falling | **Duration (TLT), quality growth** | "Easing Cycle" |

**For BTC specifically (Howell's thesis):** BTC is primarily driven by liquidity + risk appetite. Not growth, not inflation directly. This means:
- Liquidity expanding = BTC tailwind regardless of growth
- Liquidity contracting = BTC headwind even if growth is fine
- Risk appetite (our RORO) is the second driver — amplifies or dampens the liquidity signal

**For alternatives (why we need all four drivers):** Gold responds to real rates + inflation. TLT responds to rate expectations. Commodities respond to growth + inflation. If we only track liquidity and risk, we'll miss rotation opportunities in Bucket 4 alternatives.

#### 1C. Risk Phase (RORO) — renamed from "RORO Phase"

Risk appetite as measured by SRI breadth across asset tiers. Uses Howell's concept of risk appetite as a cycle that overlays the liquidity cycle.

| Phase | Definition | Howell Analog |
|---|---|---|
| **RP1 Early** | Safety bullish (>+10), Risk bearish (<-10) | "Risk Aversion" — capital fleeing to safety |
| **RP2 Broadening** | Safety + Quality bullish, Risk not yet | "Risk Appetite Recovery" — tentative return |
| **RP3 Risk-On** | Quality + Risk bullish | "Risk Seeking" — full deployment phase |
| **RP4 Late** | Risk bullish, Safety bearish | "Risk Euphoria" — late cycle, caution |
| **RP5 Risk-Off** | Both bearish | "Risk Panic" — capital destruction phase |

#### 1D. Bitcoin Cycle Phase

BTC-specific cycle position derived from FTL/STL + SRIBI:

| Phase | Definition |
|---|---|
| **BC1 Markdown** | FTL < STL, SRIBI < -20 |
| **BC2 Accumulation** | FTL < STL, SRIBI ≥ -20 and < +10 |
| **BC3 Early Markup** | FTL > STL, SRIBI < +10 |
| **BC4 Markup** | FTL > STL, SRIBI ≥ +10, rising |
| **BC5 Mature** | FTL > STL, SRIBI ≥ +10, fading |
| **BC6 Distribution** | FTL < STL, SRIBI ≥ +10 |

*(Renumbered from C4→C1→C2→C3 to sequential BC1→BC6 for clarity)*

#### 1E. Full Regime State

**Combined output:** `Macro Regime × Risk Phase × Bitcoin Cycle`

Example (current): 
```
MACRO: Liquidity Contracting (Z=-1.01, stabilizing) | Growth Neutral | Inflation Falling | Rates Cutting
RISK PHASE: RP1 Early (Safety bullish, Risk bearish)
BTC CYCLE: BC1 Markdown (FTL<STL, SRIBI=-65)
ASSET ATTRACTIVENESS: Favors Treasuries, Gold, Cash. BTC headwind but approaching cycle turn.
```

---

### Layer 2: SIGNAL LAYER — "What's firing?"

Signals are gated by regime. The same signal produces different actions depending on regime state.

#### 2A. Concordance Tier (Bullish Entry Timing)

Multi-TF SRIBI alignment — determines WHEN to enter and at WHAT size.

| Tier | Definition | Win% 20d | Use |
|---|---|---|---|
| **CT1 Scout** | VST > 0 + LT rising + VLT rising | 50% | Watch only. Path B LEAPs at minimum size. |
| **CT2 Early** | VST > 0 + LT > 0 + VLT > -20 | 55% | Entry gate for AB2 spreads. Small AB1 if regime allows. |
| **CT3 Confirmed** | All TFs > 0 | 57% | Full AB2. AB1 if regime ≥ RP3. |
| **CT4 High Conviction** | All > 0 + VLT > +20 | 63% | Full size all buckets per regime allocation. |

**Regime gating rules:**

| Concordance Tier | RP1 | RP2 | RP3+ |
|---|---|---|---|
| CT1 | AB3 Path B only | AB3 Path B only | AB2 small + AB3 |
| CT2 | AB2 spreads | AB2 + small AB1 | AB1 + AB2 + AB3 |
| CT3 | AB2 full | AB1 + AB2 + AB3 | Full deployment |
| CT4 | AB2 full + AB3 add | Full deployment | Full deployment, max size |

#### 2B. Bear Trigger (Bearish/Exit Signals)

| Trigger | Definition | Action |
|---|---|---|
| **BT1 Warning** | SOPR < -0.2 + SRIBI mixed or positive | Distribution alert — tighten stops |
| **BT2 Confirmed** | SOPR < -0.2 + STRS > 0.45 falling + MVRV > 1.5 | Close AB1 directional. Tighten AB2. |
| **BT3 Capitulation** | SOPR < -0.2 + ALL SRIBI negative | Capitulation BUY signal (+3.81% at 20d) |

Note: BT3 is counterintuitively a buy. When SOPR shows heavy losses AND all TFs are bearish, that's seller exhaustion — where bottoms form.

#### 2C. Preferred Signal (SCHI)

Leading indicator from Strategy preferred shares:
- STRC < $97: Credit stress — reduce bullish exposure
- STRF < $97: Severe stress — close all bullish
- STRK > $85 with volume: Recovery signal — Stage 1 confirmation candidate
- SCHI composite for aggregate read

#### 2D. Stage Transitions

VLT/LT stage transitions are rare and high-signal. VST transitions are frequent and noisy.
- **VLT or LT Stage 3→4:** Major bottom marker (only 2 BTC instances ever)
- **VLT or LT Stage 4→1:** Confirmed cycle turn
- **VST Stage transitions:** Precision entry timing within an already-confirmed direction (per Gavin's tutorial)

---

### Layer 3: ALLOCATION ENGINE — "How much, where?"

#### 3A. Allocation Buckets (AB1–AB4)

| Bucket | Purpose | Vehicle | When Active |
|---|---|---|---|
| **AB1 Directional** | Trend capture | IBIT (default), MSTR calls (high conviction only) | CT2+ AND RP2+ |
| **AB2 Spreads** | Income + defined risk | MSTR options spreads | CT2+ any RP |
| **AB3 LEAPs** | Long-term appreciation | MSTR LEAPs | Path B: RP1+MVRV<0.8. Otherwise CT3+ |
| **AB4 Cash & Alts** | Capital preservation + rotation | STRC (cash), alternatives per macro regime | Always |

#### 3B. STRC Hurdle

Every AB1 and AB2 trade must exceed STRC's expected monthly yield (0.83%/month at par) or capital stays in STRC. AB3 is exempt (different objective).

#### 3C. Regime Allocation Map

Pre-defined allocation targets for each RP × BC combination:

| State | AB1 | AB2 | AB3 | AB4 |
|---|---|---|---|---|
| RP1 × BC1 (current) | 0% | 15-20% | 5-8% (Path B) | 72-80% |
| RP1 × BC2 | 0% | 15-20% | 10-15% | 65-75% |
| RP2 × BC3 | 10-15% | 15-20% | 15-20% | 45-60% |
| RP3 × BC4 (money zone) | 15-20% | 20-25% | 25-35% | 20-40% |
| RP4 × BC5 | 5-10% | 10-15% | reduce | 65-80% |
| RP4 × BC6 (exit) | 10-15% puts | 5-10% | close | 65-80% |

*(Full 30-cell matrix to be built when all combinations are backtested)*

#### 3D. Position Sizing

- Max 8 concurrent positions
- Max $50K risk per position
- Min 65% PoP on AB2 spreads
- Portfolio Greeks: ±50 delta, -200 vega
- Kelly criterion informs sizing within these limits

---

### Decision Flow

```
REGIME ENGINE (Layer 1)
  Macro (Liquidity×Growth×Inflation×Rates)
  + Risk Phase (RP1–RP5)
  + Bitcoin Cycle (BC1–BC6)
  + Asset Attractiveness (Howell overlay)
         │
         ▼
SIGNAL LAYER (Layer 2) — gated by regime
  Concordance Tier (CT1–CT4)
  × Bear Triggers (BT1–BT3)
  × Preferred Signal (SCHI)
  × Stage Transitions (VST/ST/LT/VLT)
         │
         ▼
ALLOCATION ENGINE (Layer 3)
  Regime Allocation Map → Bucket targets
  + STRC Hurdle → trade qualification
  + Position Sizing → specific recommendation
         │
         ▼
  → TRADE RECOMMENDATION
```

---

### Complete Naming Reference

| Abbreviation | Full Name | Values |
|---|---|---|
| **RP** | Risk Phase | RP1 Early → RP5 Risk-Off |
| **BC** | Bitcoin Cycle | BC1 Markdown → BC6 Distribution |
| **CT** | Concordance Tier | CT1 Scout → CT4 High Conviction |
| **BT** | Bear Trigger | BT1 Warning, BT2 Confirmed, BT3 Capitulation |
| **AB** | Allocation Bucket | AB1 Directional → AB4 Cash & Alts |
| **SRI Stage** | Stage + Timeframe | Stage 1–4 × VST/ST/LT/VLT |

---

### What's New vs v0 Draft

1. **Layer 1 expanded with Howell macro drivers** — Liquidity, Growth, Inflation, Rates as independent cycles with lead/lag sequence
2. **Asset Attractiveness layer added** — maps macro conditions to favored asset classes (enables Bucket 4 rotation beyond BTC/MSTR)
3. **RP# replaces P#** for Risk Phases — no confusion with project numbers
4. **BC# replaces C#** for Bitcoin Cycle — sequential numbering (BC1–BC6)
5. **CT# for Concordance Tiers** — clean abbreviation
6. **BT# for Bear Triggers** — consistent with CT#
7. **"Regime Allocation Map" replaces "Anchored Table"**
8. **Regime gating matrix added** — explicit rules for which CT×RP combos unlock which buckets

---

### Open Items

1. **Macro data pipeline gaps:** We have GLI proxy (crude 4-bank), Fed Funds, 2Y/10Y, DXY, VIX. We're missing: PMIs, CPI/breakevens, credit spreads (HYG-BIL), earnings revisions. Need to expand FRED collection or find sources.
2. **Howell's 28-bank GLI:** Our 4-bank proxy is rough. Better data = better liquidity cycle reads.
3. **Macro regime classification rules:** Thresholds for Expanding/Neutral/Contracting on each driver need backtesting. Current GLI Z-score thresholds (±0.5) are preliminary.
4. **Full RP×BC matrix:** 30 cells, many will have sparse data. Need to identify which combos actually occur and which are theoretical.
5. **Asset attractiveness backtesting:** Howell's framework is theory — need to validate which macro conditions actually predict asset class returns with our data.
