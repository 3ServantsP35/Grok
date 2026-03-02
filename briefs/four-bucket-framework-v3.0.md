# Four-Bucket Allocation Framework — v3.0
**Date: 2026-03-02 | Author: CIO | Status: ✅ Approved**

---

## What Changed from v2.0

v2.0 treated AB2 as an independent credit spread pool (Bull Put Spreads) with its own capital allocation and entry gates. That design produced a persistent blocking problem: the MIXED context + LOI filter kept AB2 closed during exactly the periods when AB3 was accumulating. The result was idle capital earning nothing when IV was highest.

v3.0 restructures AB2 as a **PMCC income engine running on top of AB3 LEAPs** rather than an independent position. AB3 provides the long exposure via 2-year LEAPs; AB2 monetizes that exposure continuously by selling short-duration calls against it. The two buckets become linked — AB2 is a strategy layer on AB3, not a separate pool.

AB1 and AB4 are unchanged.

---

## The Four Buckets

| Bucket | Instrument | Time Horizon | Role | Baseline | Floor | Ceiling |
|---|---|---|---|---|---|---|
| **AB1** | OTM LEAPs | 1 week – 90 days | Opportunistic breakout trades | 25% | — | — |
| **AB2** | Short calls vs. AB3 LEAPs | < 90 days | Income overlay on AB3 | — | — | — |
| **AB3** | 2-year LEAPs | Months – cycle | Core long exposure | 50% | — | **35%** |
| **AB4** | Cash / STRC | Permanent | Liquidity reserve | 25% | **10%** | — |

> **Note on AB2 allocation:** AB2 no longer consumes independent capital. Short calls sold against AB3 LEAPs are collateralized by the LEAP itself — no additional margin required. AB2's 25% baseline from v2.0 is absorbed into AB3 (now 50% baseline). AB2 performance is measured as monthly income generated per LEAP unit, not as a % of portfolio capital.

---

## AB3 — 2-Year LEAP Accumulation (Core Bucket)

### Purpose
Build concentrated long exposure to in-scope assets at deep structural discounts. The 2-year duration provides time for the SRI cycle to complete without expiry pressure.

### Asset Pool
All 8 trading assets eligible: MSTR, IBIT, TSLA, SPY, QQQ, GLD, IWM, PURR*.  
*PURR: observation mode until ~500 bars (~Jun 2026). Track only, no AB3 entries.

### Entry Gate — LOI Deep Accumulation

| Asset Mode | Accumulation (Stage 1) | Deep Accumulation (Stage 2 required) |
|---|---|---|
| Momentum (MSTR, IBIT, TSLA, PURR) | LOI < -45 | LOI < -65 (bounce confirmation) |
| Mean-Reverting (SPY, QQQ, IWM) | LOI < -40 | LOI < -60 |
| Trending (GLD) | LOI < -45 | LOI < -65 |

**Two-stage signal system:**
- **Stage 1 (Awareness):** LOI crosses below accumulation threshold → triangle marker. Start monitoring.
- **Stage 2 (Actionable):** 2-bar confirmed LOI bounce + depth filter (LOI must have reached bounce_depth before recovery) → circle marker. This is the actual entry trigger.

**Additional gates:**
- GLI Z-score < -1.0: raise accumulation threshold by 20 pts (false bottom risk elevated)
- Regime score: no gate on entry — AB3 entries are regime-agnostic. Existing positions never force-closed.

### LEAP Selection
- **Duration:** 2 years DTE at entry (not shorter — time is the edge in structural recovery)
- **Strike:** 5–15% OTM at entry
- **Delta:** 0.30–0.45 at entry
- **Sizing:** Position sized to AB3 allocation; never exceed 35% of portfolio mark-to-market

### Exit — Phased Trims via LOI
| Signal | Trim | Rationale |
|---|---|---|
| LOI > +40 (MR: +10) | 25% | First trim — recovery confirmed |
| LOI > +60 (MR: +30) | 25% | Second trim — distribution building |
| LOI > +80 (MR: +50) | 25% | Third trim — overextension |
| LOI rollover (−20 from peak) | Final 25% | Full exit on structural turn |

**AB3 Ceiling (35%):** If AB3 mark-to-market exceeds 35% of portfolio, engine alerts. No auto-trim — owner decides. When AB3 is over ceiling and a new signal fires, alert before entry.

---

## AB2 — Short Call Income Overlay

### Purpose
Generate 2–5% monthly income (measured against AB3 LEAP cost basis) by selling short-duration calls against existing AB3 LEAP positions. This is a Poor Man's Covered Call (PMCC) structure. AB3 LEAP = synthetic long stock; AB2 short call = covered call equivalent.

### Asset Pool
All assets where AB3 LEAPs are held. No separate pool or capital required.  
**IBIT re-enabled** — the prior IBIT restriction applied to Bull Put Spreads only (MIXED context timing). PMCC structure is context-independent.

### How It Works
For each AB3 LEAP position, the engine evaluates whether to sell a short call based on:
1. The current LOI/CT tier state (see Call-Selling Gate below)
2. IV level and available premium
3. Target delta for the short call (set by LOI/CT state)

The short call premium collected reduces the net cost basis of the AB3 LEAP over time. A LEAP bought at $25 and offset by $3/month in call premium has an effective cost basis of $7 after 6 months.

### Call-Selling Gate — LOI/CT State Controls Strike Aggressiveness

| LOI Zone | CT Tier | Call Action | Max Delta | Rationale |
|---|---|---|---|---|
| LOI < -20 + CT1 | Accumulation | **No calls** | — | Let LEAP ride; upside needed most here |
| LOI -20 to +20 + CT2-CT3 | Neutral / Recovery | OTM calls | ≤ 0.25 | Income mode; preserve upside |
| LOI > +20 + CT3-CT4 | Approaching trim | ATM/ITM calls | ≤ 0.40 | Delta reduction as trim mechanism |
| AB1 signal active on asset | Any | **Pause** | — | AB1 expects fast move; don't cap it |

> **Upside protection rule:** In LOI -20 to +20 zone, never sell calls within 20% of current price. This prevents capping MSTR's momentum moves (40–60% monthly possible during Saylor cycles).

### Call Duration
- Target: 30–45 DTE (theta sweet spot)
- Range: 7–90 DTE depending on opportunity and market conditions
- Roll: when 7–10 DTE remain and the call is OTM, roll forward to next cycle

### Income Target
- **2–5% monthly** of AB3 LEAP cost basis — expressed as a cycle average, not a monthly floor
- When VIX > 25: target top of range (IV elevated, premium rich)
- When VIX < 18: target bottom of range or skip; do not sell closer-to-the-money to compensate

### Direction / Delta Management
Selling ITM or near-ATM calls (delta > 0.30) is permitted in the LOI > +20 / CT3-CT4 zone as a deliberate delta reduction mechanism — when the AB3 position is maturing and you want to reduce net long exposure without closing the LEAP. This is **delta management**, not a directional bet. The distinction matters: delta management is driven by the AB3 position lifecycle, not by conviction on near-term price direction.

### What PMCC Changes vs. v2.0 Credit Spreads

| Factor | v2.0 Bull Put Spreads | v3.0 PMCC |
|---|---|---|
| Entry gate | LOI > -30 + MIXED + LT+ | LEAP exists + LOI/CT state |
| Capital consumed | Margin for spread | None (LEAP is collateral) |
| Max loss | Defined (spread width) | LEAP premium minus calls collected |
| Upside cap | None | Yes — managed by gate |
| Blocked during accumulation? | Yes (entire Feb 2026) | No |
| IBIT eligible? | No | Yes |
| Complexity | Medium | Higher (two instruments) |

---

## AB1 — Opportunistic Breakout LEAPs

### Purpose
High-conviction, shorter-hold LEAP trades initiated around confirmed breakout conditions. Not a structural accumulation vehicle — the edge is timing the breakout, not catching the bottom.

### Asset Pool
All 8 trading assets eligible. PURR excluded until ~500 bars.

### Entry Gate — CT Signal at Pre-Breakout
AB1 entries require a Concordance Tier 1 signal:

| CT Level | Condition | AB1 Eligible? |
|---|---|---|
| CT1 | VST+ in MIXED context | ✅ Core entry |
| CT2 | VST+LT aligned, VLT > -20 | ✅ Highest conviction |
| CT3 | All TFs positive | ❌ Too late |
| CT4 | All TFs + strong VLT | ❌ Distribution — exit |

**Additional gates:**
- LOI anchor: asset touched accumulation threshold within last 120 bars
- Stage 4→1 transition: FTL crossed above STL within last 30 bars
- Regime score ≥ -1
- GLI Z-score > -0.5 (or LOI < -80 for deep accumulation override)
- C6 filter: LOI recovery ≥ 8 pts above anchor at signal time

### LEAP Selection
- **Duration:** OTM LEAPs, 60–120 DTE (shorter than AB3 — tactical, not structural)
- **Strike:** 5–15% OTM
- **Delta:** 0.30–0.45

### Exit Rules
1. **LT turns positive** (primary) — structural catch-up complete
2. **90-day max** — time stop
3. **Failure → AB3 reclassification** — if ST turns negative within 40 bars AND price gain < 5%, reclassify to AB3 (no forced close)

### AB1 / AB2 Interaction
When an AB1 signal fires on an asset where an AB3 LEAP is also held:  
→ **Suspend AB2 call selling on that asset** until the AB1 trade completes.  
The expected breakout move from AB1 must not be capped by a short call.

---

## AB4 — Cash & STRC Reserve

### Purpose
Liquidity reserve. Earns STRC yield (~10% annual / 0.83%/month) while awaiting opportunity.

### Floor (10%)
Never depleted regardless of opportunity. If fully deployed, the next trade waits for an exit.

### STRC as Hurdle Rate
Every AB1 LEAP trade must have an expected return exceeding 0.83%/month. If not, capital stays in AB4.  
AB2 income (short call premium) is measured against this hurdle — if premium available is < 0.83%/month of LEAP cost, skip the cycle.

### STRC as Regime Signal
- STRC ≥ $97: Saylor engine healthy — full deployment eligible
- STRC $90–97: Stress building — reduce new AB3 entries
- STRC < $90: Flywheel impaired — defensive posture, max AB4

---

## Allocation Mechanics

### Capital Flow
```
Total Portfolio (e.g., $5M)
  │
  ├── AB4 floor (≥10% = $500K) — protected first
  │
  ├── AB3 LEAP purchases (baseline 50% = $2.5M)
  │     └── AB2 short calls written against AB3 (no additional capital)
  │
  └── AB1 opportunistic LEAPs (baseline 25% = $1.25M)
        └── Residual to AB4 if no AB1 signals
```

### AB3 Ceiling Logic
- If AB3 mark-to-market > 35%: alert, no auto-trim, no new AB3 entries until resolved
- When AB3 over ceiling and AB1 signal fires: pause AB1 until AB3 resolves (AB3 compresses the AB1 budget first)
- AB2 call selling continues regardless of AB3 ceiling breach (it's income optimization, not new capital)

### Regime Gates
| Regime Score | AB1 | AB2 (call sales) | AB3 new entries | AB4 |
|---|---|---|---|---|
| +4 to +7 (RISK-ON) | Full | Full | Full | 10% |
| +2 to +3 (BULL) | Full | Full | Full | Normal |
| 0 to +1 (NEUTRAL) | 75% size | Full | Full | Normal |
| -1 (CAUTIOUS BEAR) | 50% size | OTM only (δ ≤ 0.20) | Pause new | Add to AB4 |
| ≤ -2 (RISK-OFF) | No new | Pause | Existing only | Max |

AB3 existing positions are never force-closed by regime. Only new entries are gated.

---

## Asset Competition Rules

### AB3 (Multiple LOI signals)
All valid signals enter simultaneously if allocation allows. If AB3 would breach 35%, alert owner before proceeding. Strongest Stage 2 signal (deepest confirmed bounce from anchor) gets priority if forced to choose.

### AB1 (Multiple CT1 signals)
Priority:
1. Deepest LOI anchor (most negative = strongest structural bottom)
2. Higher CT confidence score
3. GLI Z-score alignment

### AB2 (Multiple PMCC candidates)
All AB3 positions are candidates. Sort by:
1. Highest IV / premium available
2. Position in LOI zone (neutral zone > accumulation zone for call writing)
3. Avoid writing calls during AB1 signal window

---

## Portfolio Independence
| Portfolio | Owner | Capital | Mode |
|---|---|---|---|
| Greg | Greg McKelvey | $5M live | Full execution |
| Gavin | Gavin | $1M | Paper |
| Gary | Gary | TBD | Educational |

Each portfolio runs the full allocation engine independently.

---

## Sign-off Status

| Decision | Owner | Status |
|---|---|---|
| AB2 restructured as PMCC income overlay | Gavin | ✅ |
| AB3 broadened to 2-year LEAPs, multi-asset | Gavin | ✅ |
| Call-selling gate (LOI/CT state controls delta) | Gavin | ✅ |
| AB1/AB2 pause interaction | Gavin | ✅ |
| IBIT re-enabled for AB2 (PMCC) | Gavin | ✅ |
| AB3 baseline raised to 50% (absorbs AB2 allocation) | Gavin | ✅ |
| AB3 35% ceiling (alert, not auto-trim) | Gavin | ✅ |
| AB4 10% floor | Gavin | ✅ |
| 25% equal trim tranches | Gavin | ✅ |
| Multi-asset competition rules | Gavin | ✅ |
| STRC hurdle rate (0.83%/month) | Gavin | ✅ |

---

*Supersedes: four-bucket-framework-v2.0.md. Cross-reference: SRI-Engine-Tutorial-v2.md Sections 9–13.*
