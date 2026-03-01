# Four-Bucket Allocation Framework — v2.0
**Date: 2026-03-05 | Author: CIO | Status: Awaiting Greg + Gavin sign-off**

---

## What Changed from v1.x

v1.x treated AB1–AB3 as MSTR/IBIT-centric with "alternatives" as a separate category. Backtesting invalidated that premise: **all assets compete for every bucket based on signal quality**. The framework now treats all 8 trading assets equally. The strongest signal wins the allocation.

v2.0 also formalizes the Concordance Tier (CT) gate per bucket — entry quality requirements differ by bucket because the risk/reward profiles differ.

---

## The Four Buckets

| Bucket | Instrument | Time Horizon | Signal Source | Baseline | Floor | Ceiling |
|---|---|---|---|---|---|---|
| **AB1** | OTM LEAPs | 1 week – 90 days | CT1 pre-breakout | 25% | — | — |
| **AB2** | Credit spreads | 1–3 weeks | ST cross+ in MIXED context | 25% | — | — |
| **AB3** | LEAPs | Months – cycle | LOI deep accumulation | 25% | — | **35%** |
| **AB4** | Cash / STRC | Permanent | Default | 25% | **10%** | — |

---

## AB1 — Tactical LEAP Bucket

### Asset Pool
All 8 trading assets are eligible: MSTR, IBIT, TSLA, SPY, QQQ, GLD, IWM, PURR*.  
*PURR: observation mode until 500 bars (~Jun 2026). Track only, no AB1 entries.

### Entry Gate — CT1 Signal Required
AB1 entries require a Concordance Tier 1 signal minimum:

| CT Level | Condition | AB1 Eligible? | Notes |
|---|---|---|---|
| CT1 | VST+ in MIXED context | ✅ Full size | Core entry — MIXED ctx required |
| CT2 | VST+LT aligned, VLT>-20 | ✅ Full size | Rare, ideal — higher confidence |
| CT3 | All TFs positive | ❌ No entry | Too late — structural catch-up complete |
| CT4 | All TFs + strong VLT | ❌ No entry | Distribution signal — exit existing |

**Additional gates (all must pass):**
- LOI anchor: asset must have touched accumulation threshold within last 120 bars (Momentum: LOI < -60; MR: < -40)
- Stage 4→1 transition: FTL crossed above STL within last 30 bars
- Regime score ≥ -1 (no new entries in risk-off)
- GLI Z-score > -0.5 (or LOI < -80 if GLI is in headwind — deep accumulation overrides)

### Exit Rules
1. **LT turns positive** (primary) — structural catch-up complete
2. **90-day max** — time stop regardless of position
3. **Failure → AB3 reclassification** — if ST cross negative within 40 bars AND price gain < 5%, reclassify as AB3 (no forced close)

### Sizing
- Base: 25% of portfolio target for AB1 bucket
- Reduce by 25% if regime score is 0 or -1 (cautious sizing)
- GLI headwind tag: reduce by additional 25%

---

## AB2 — Credit Spread Bucket

### Asset Pool
MSTR, TSLA, SPY, QQQ, GLD, IWM.  
**IBIT is disabled** — MIXED context doesn't predict reliable LT catch-up timing on crypto-adjacent assets.

### Entry Gate — MIXED Context + ST Cross
```
C1: ST crosses positive (ST SRIBI from ≤0 to >0)
C2: VST positive (VST SRIBI > 0)
C3: Context = MIXED (LT < 0 AND VLT > 0)
C4: Regime score ≥ -1
C5: VIX > 18 (premium worth selling)
```

No CT requirement — AB2 is a premium-capture strategy, not a directional bet. The MIXED context gate is the equivalent quality filter.

### Strategy — Bull Put Spread
Sell put at recent support, buy put further OTM. Width: 5–10% of underlying price.
PoP target: ≥65%.

**VIX sizing:**
- VIX > 25: +25% position size
- VIX 18–25: standard size
- VIX < 18: −50% size or skip

**Disabled strategies (pending P14 validation):**
- Bear Call spreads: disabled on all assets
- Iron Condors: disabled pending DOI (bearish bias indicator)

### Exit Rules
1. **LT turns positive** (primary, ~90% of exits)
2. **90-bar time stop** (~15 trading days)

---

## AB3 — Strategic LEAP Bucket

### Asset Pool
All 8 assets eligible. Asset enters AB3 via:
(a) LOI deep accumulation signal, or
(b) Failed AB1 reclassification

### Entry Gate — LOI Threshold
| Asset Mode | Accumulation | Deep Accumulation |
|---|---|---|
| Momentum | LOI < -60 | LOI < -80 |
| Mean-Reverting | LOI < -40 | LOI < -60 |
| Trending | LOI < -60 | LOI < -80 |

No CT gate required — AB3 entries are regime-agnostic. The LOI measures structural opportunity regardless of short-term momentum.

**Exception:** GLI Z < -1.0 raises accumulation threshold by 20 points (Stage 1 = likely false bottom). Require LOI < -80 (momentum) or < -60 (MR) before entering.

### Exit — Phased Trims
| Signal | Trim | Rationale |
|---|---|---|
| LOI > +40 (MR: +10) | 25% | First trim — recovery confirmed |
| LOI > +60 (MR: +30) | 25% | Second trim — distribution building |
| LOI > +80 (MR: +50) | 25% | Third trim — overextension |
| LOI rollover (−20 from peak) | Final 25% | Full exit on structural turn |

**AB3 Ceiling (35%):** If AB3 mark-to-market exceeds 35% of portfolio, engine alerts. No auto-trim — owner decides. When AB3 is over ceiling and a new AB3 signal fires, alert before entry.

### LEAP Selection
- Strike: 5–15% OTM at entry
- Expiry: 12–18 months DTE (strategic — not tactical)
- Delta: 0.30–0.45 at entry

---

## AB4 — Cash & STRC Reserve

### Purpose
Liquidity reserve. Earns STRC yield (~10% annual, 0.83%/month) while awaiting opportunity.

### Floor (10%)
Never depleted regardless of opportunity set. If portfolio is fully deployed, the next trade must wait for an exit to fund it.

### STRC as Hurdle Rate
Every AB1 and AB2 trade must have an expected return exceeding 0.83%/month. If not, capital stays in AB4.

### STRC as Regime Signal
- STRC ≥ $97: Saylor engine healthy — full deployment eligible
- STRC $90–97: Stress building — reduce new entries
- STRC < $90: Flywheel impaired — move to defensive posture

---

## Asset Competition Rules

When multiple assets simultaneously have valid signals for the same bucket:

**AB1 (multiple CT1 signals):**
Priority order:
1. Highest LOI anchor depth (most negative = strongest structural bottom)
2. Higher concordance confidence score
3. Deeper GLI Z-score alignment

**AB2 (multiple MIXED context crosses):**
Priority order:
1. Highest VIX-adjusted premium available
2. Strongest PoP at target strike
3. Asset with less recent AB2 activity (diversify)

**AB3 (multiple LOI signals):**
No priority — all valid signals enter simultaneously if allocation allows. If AB3 would breach 35%, alert owner before proceeding.

---

## Allocation Interaction Rules

### AB1 → AB3 Transition
1. ST turns negative within 40 bars of AB1 entry AND price gain < 5%
2. Reclassify LEAP from AB1 to AB3 (accounting only — LEAP stays open)
3. Reduce AB1 bucket %, increase AB3 bucket %
4. If AB3 would breach 35% ceiling, alert owner

### When AB3 Exceeds Ceiling
1. Engine alerts — does not auto-trim
2. No new AB3 entries until AB3 resolves below 35% or owner explicitly approves
3. If AB1 entry also pending: pause AB1 until AB3 resolves (AB1 compresses first)

### Priority of Capital
```
AB4 floor (10%) → protect first
AB3 ceiling (35%) → cap second
AB1 / AB2 → compete for remaining 55%
```

---

## Regime Gates on Allocation

| Regime Score | AB1 | AB2 | AB3 | AB4 |
|---|---|---|---|---|
| +4 to +7 (RISK-ON) | Full | Full | Full | 10% (floor) |
| +2 to +3 (BULL) | Full | Full | Full | Normal |
| 0 to +1 (NEUTRAL) | 75% size | Full | Full | Normal |
| -1 (CAUTIOUS BEAR) | 50% size | 50% size | Full | Add to AB4 |
| ≤ -2 (RISK-OFF) | No new | No new | Existing only | Max |

AB3 existing positions are never force-closed by regime. Only new entries are gated.

---

## Portfolio Independence

Three portfolios tracked separately. No cross-portfolio implications.

| Portfolio | Owner | Capital | Mode |
|---|---|---|---|
| Greg | Greg McKelvey | $5M | Live |
| Gavin | Gavin | $1M | Paper |
| Gary | Gary | TBD | Educational |

Each portfolio runs the full allocation engine independently. Signal quality is universal; sizing is portfolio-specific.

---

## CT Gate Summary (Cross-Bucket Reference)

| Tier | AB1 | AB2 | AB3 | Note |
|---|---|---|---|---|
| CT1 (VST+, MIXED) | ✅ Core | — | ✅ (via LOI) | Best entry for AB1 and AB3 |
| CT2 (VST+LT+, VLT>) | ✅ Ideal | — | ✅ | Rare; highest conviction |
| CT3 (all TFs+) | ❌ | — | ✅ (existing) | AB1 too late; AB3 holds |
| CT4 (all+ strong VLT) | ❌ | — | Trim signal | Overextension — reduce |
| MIXED + ST cross | — | ✅ | — | AB2 specific gate |

---

## Sign-off Required

| Decision | Owner | Status |
|---|---|---|
| Multi-asset rotation (all assets compete for AB1–3) | Greg + Gavin | ⬜ Pending |
| STRC hurdle rate (0.83%/month) | Greg + Gavin | ⬜ Pending |
| CT1 as AB1 entry gate (not CT3) | Gavin | ⬜ Pending |
| AB1 failure → AB3 (no forced close) | Greg | ⬜ Pending |
| IBIT disabled for AB2 | Gavin | ✅ Approved |
| 25% equal trim tranches | Gavin | ✅ Approved |
| AB3 35% ceiling (alert, not auto-trim) | Gavin | ✅ Approved |
| AB4 10% floor | Gavin | ✅ Approved |

---

*Supersedes: four-bucket-framework-v1.2.md. Cross-reference: SRI-Engine-Tutorial-v2.md Sections 9–13.*
