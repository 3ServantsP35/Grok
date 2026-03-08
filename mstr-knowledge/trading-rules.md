# Trading Rules — AB Bucket Framework v4.0

**Last updated:** 2026-03-08
**Approved by:** Gavin (rizenshine5359) — equal co-owner
**Status:** Active

---

## Permanent Rules (Non-Negotiable)

1. **No naked short positions under any circumstances.** All short option legs must be part of a defined-risk spread structure. No exceptions, no approvals override this.
2. **AB4 hard floor: 10% true cash minimum.** Preferreds (STRC, STRK, STRF) count as AB4 but do not satisfy the floor. Never breached.
3. **STRC hurdle rate: 0.83%/month.** Every deployment must beat this rate. If no signal clears the bar, stay in STRC.
4. **No new naked short calls.** Even within a spread, the short leg must have a defined long leg at entry. Not post-entry.

---

## Bucket Definitions

### AB4 — Capital Reserve (unchanged)

- **Instrument:** STRC (primary), STRK, STRF, true cash
- **Floor:** 10% minimum true cash (hard floor — never breached)
- **Role:** Default staging for all undeployed capital. Earns ~0.83%/month as hurdle rate benchmark
- **Exit condition:** Capital leaves AB4 only when the target AB1/AB2/AB3 signal clears the STRC hurdle rate
- **In structural bear:** AB4 typically runs 30–40% of portfolio as AB1/AB2/AB3 remain under-deployed

---

### AB3 — Structural Accumulation (unchanged)

- **Instrument:** 2-year OTM LEAPs (calls) on in-scope momentum assets
- **Intent:** Capital appreciation over a full market cycle
- **Target allocation:** ~50% of total portfolio
- **Entry signal:** AB3 LOI < vol-adaptive threshold; Stage 2 bounce confirmation required
  - LOI threshold: -45 (Momentum assets: MSTR/TSLA/IBIT); -40 (MR assets: SPY/QQQ/GLD/IWM)
  - Vol-adaptive multiplier: high-vol entries dramatically outperform low-vol entries (+26% vs -27% median 60d return)
- **Exit:** Phased trim schedule — 25% at LOI +20 / 50% at LOI +40 / 75% at LOI +60 / final on 20pt rollover
- **Note:** The long LEAP leg of any PMCC is always classified as AB3 capital

---

### AB2 — Directional Conviction (v4.0 — revised)

- **Intent:** Delta-first. Take a directional position on a significant identified overextension or pre-breakout setup. Hold until the move completes or thesis fails.
- **Holding period:** 30 days minimum; 90+ days typical for LEAP structures
- **Capital:** ≤10% of total portfolio. No standalone capital requirement for PMCC short legs (those are AB1 or AB2 by intent, against AB3 capital)
- **Entry criteria:** Significant overextension signal required. Valid triggers:
  - Force Field BOUNCE EXHAUST (STRONG_BULL + structural gap — 93% bearish at +20d)
  - AB3 LOI at extreme distribution territory + Force Field bear zone
  - CT1/CT2 pre-breakout + Force Field EARLY RECOV
  - MOD_BEAR or STRONG_BEAR Force Field zone with directional confirmation

**Permitted structures (simple only — no more than 2 legs):**
1. **Long LEAP puts** — bearish overextension, highest conviction, defined risk (max loss = premium paid)
2. **Bear call spread** — bearish overextension, 30–90 DTE, strikes at +15% OTM minimum
3. **Bull put spread** — bullish underextension, 30–90 DTE, high-confidence signal required
4. **Long LEAP calls 60–120 DTE** — CT1/CT2 pre-breakout directional play

**PMCC short leg as AB2:** The short call leg of a PMCC is classified AB2 when it is directionally motivated (larger size, 30+ DTE, opened because of a specific directional view rather than routine income harvesting).

---

### AB1 — Theta Income (v4.0 — revised)

- **Intent:** Theta-first. Harvest time decay consistently. Higher volume of trades than AB2/AB3; smaller per-trade commitment.
- **Holding period:** 1 day to 2 weeks target; 30 DTE hard maximum
- **Capital:** ≤10% of total portfolio (excludes AB3 LEAP long leg in any PMCC)
- **Entry criteria:** CRS ≥ 7 (or ≥ 5 with explicit rationale); LOI in S1 CHOP (−45 to −20) or RECOVERY (−20 to 0); Exercise Risk LOW or MED
- **Income target:** Consistent quarterly income. Track cumulative monthly return vs. STRC hurdle

**Permitted structures:**
1. **Bull put spread** — income in LOI accumulation/S1 CHOP zone, 7–30 DTE
2. **Bear call spread** — income in LOI extended/distribution zone, 7–30 DTE
3. **PMCC short leg (theta-motivated)** — selling calls against AB3 LEAPs when income is the primary objective; classified AB1 regardless of DTE (see edge case note below)

**PMCC short leg as AB1:** The short call leg of a PMCC is classified AB1 when it is theta-motivated (opened to generate income against an existing AB3 LEAP, guided by CRS score, not a specific directional view). This is the default classification for PMCC income cycles.

---

## PMCC Classification Rules

The PMCC is a hybrid strategy. Capital is allocated as follows:

| Component | Bucket | Notes |
|---|---|---|
| Long LEAP leg | **AB3** | Always. This is structural accumulation capital. |
| Short call leg — theta-motivated | **AB1** | CRS-guided income cycle. Default classification. |
| Short call leg — directional conviction | **AB2** | Larger size or 30+ DTE, opened because of a directional view. Note the intent at entry. |

**Edge case:** A 45 DTE short call opened against an AB3 LEAP with CRS ≥ 7 in S1 CHOP stage is classified **AB1** even though it exceeds the 30 DTE target. Reason: intent is theta income, not directional conviction. Document the exception at time of entry in the trade log.

---

## Capital Allocation Summary

| Bucket | Target | Constraint |
|---|---|---|
| AB3 | ~50% | Vol-adaptive entry gates; Stage 2 required |
| AB2 | ≤10% | Independent capital for directional trades |
| AB1 | ≤10% | Excludes AB3 LEAP long leg |
| AB4 | ≥10% (floor); balance of undeployed | Hard floor = true cash only |

**Combined AB1 + AB2 ≤ 20% of total portfolio at any time.**

In a structural bear market, expect: AB3 ≈ 25–35%, AB1 ≈ 5%, AB2 ≈ 5%, AB4 ≈ 55–65%.

---

## Signal Routing

| Signal | Bucket | Default Structure |
|---|---|---|
| AB3 LOI < vol-adaptive threshold + Stage 2 bounce | AB3 | 2-year LEAP call |
| Force Field BOUNCE EXHAUST, high conviction | AB2 | Long LEAP puts OR bear call spread |
| CT1/CT2 pre-breakout + Force Field EARLY RECOV | AB2 | Long LEAP call 60–120 DTE |
| CRS ≥ 7, S1 CHOP/RECOVERY, ExRisk LOW/MED | AB1 | Short credit spread 7–30 DTE |
| PMCC income cycle (routine) | AB1 | Short call against AB3 LEAP |
| PMCC income cycle (directional conviction) | AB2 | Short call against AB3 LEAP — note at entry |

---

## IV Regime Rules (AB1/AB2 context)

- **Ultra-high IV (90th+):** Maximum AB1 aggression. LEAP entries (AB2/AB3) ideal on forward valuation.
- **High IV (70–90th):** Standard AB1 cycle. Full premium harvest; target 3–5%/month.
- **Normal IV (30–70th):** Conservative AB1. OTM only, skip if premium < 0.83%/month.
- **Low IV (<30th):** Pause AB1 income. Focus AB3 accumulation if LOI signals present.

---

## mNAV Ratio (MSTR-specific)

`mNAV = Market Cap / (BTC Holdings × BTC Price)`

- High (3.0x+): Overextended — sell calls (AB1), consider AB2 bear call spread
- Low (1.2x or below): Undervalued — sell puts or hold (AB1/AB2 bullish)
- Always cite current mNAV in trade recommendations

---

## Retired Structures (pending reactivation)

- Iron Condors — retired v2.0; not currently in scope
- Standalone bull put spreads as AB2 income (pre-v4.0 AB2 definition) — reclassified to AB1

---

*Framework v4.0 — supersedes all prior bucket definitions. AB1 and AB2 descriptions in any earlier documents are deprecated.*
