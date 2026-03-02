# Portfolio State — Greg

**Last Updated:** 2026-03-05
**Framework Version:** v3.0 (PMCC income overlay on AB3 LEAPs)

---

## Account Summary

| Metric | Value |
|---|---|
| Starting Capital | $5,000,000 |
| Cash Available | ~$4,610,000 |
| Total Deployed | ~$390,000 |
| Deployed % | ~7.8% |
| AB3 Allocation | ~7.8% (target: 50%) |
| AB1 Allocation | 0% (target: 25%) |
| AB4 Reserve | ~92% cash (target floor: 25%) |

---

## AB3 — Core LEAP / Equity Positions

> Framework v3.0: 2-year OTM LEAPs at deep LOI accumulation. Short calls (AB2 PMCC) are sold against these positions.
> Current: MSTR held as shares (equiv. to delta-1 long). PMCC gate rules apply.

| # | Asset | Position | Qty | Avg Cost | Date Entered | LOI @ Entry | Stage @ Entry | Current LOI | PMCC Gate |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MSTR | Shares (equity proxy) | 3,000 sh | $128.59/sh | Feb 4–5, 2026 | ~-52 (deep acc) | Stage 1 Deep | -30.5 | NO_CALLS |

**AB3 Notes:**
- MSTR: Entered at deep accumulation (LOI ~-52, cycle bottom). Stage 2 bounce (confirmed LOI turn) since logged.
- LOI at -30.5 — 10.5 pts from opening OTM_INCOME gate (gate opens at LOI > -20).
- No adds below VLT Fast TL $133.84. No trims until LOI > +40 (Trim 25% phase).
- Next add signal: Stage 1 → Stage 2 re-entry if MSTR retests $107-$115 range.

---

## AB2 — PMCC Short Call Positions (Income Overlay)

> Short calls <90 DTE sold against AB3 LEAP/equity positions above.
> Gate state (per asset): NO_CALLS | OTM_INCOME | DELTA_MGMT | PAUSED_AB1

### Current Gate States (as of 2026-02-27 EOD)

| Asset | LOI | CT Tier | Context | Gate State | Max Delta | Threshold |
|---|---|---|---|---|---|---|
| MSTR | -30.5 | CT3 | MIXED | **NO_CALLS** | 0.00 | >-20 to open |
| IBIT | -20.5 | CT2 | HEADWIND | **NO_CALLS** | 0.00 | 0.5 pts from open |
| TSLA | -3.5 | CT0 | HEADWIND | OTM_INCOME | 0.25 | Gate open (caution: CT0) |
| SPY | +17.4 | CT3 | MIXED | OTM_INCOME | 0.25 | Gate open |
| QQQ | +2.5 | CT2 | MIXED | OTM_INCOME | 0.25 | Gate open |
| GLD | +23.3 | CT4 | TAILWIND | **DELTA_MGMT** | 0.40 | Active trim mode |
| IWM | +5.0 | CT3 | MIXED | OTM_INCOME | 0.25 | Gate open |

*Momentum threshold (MSTR/TSLA/IBIT): LOI > +40 for DELTA_MGMT*
*MR threshold (SPY/QQQ/GLD/IWM): LOI > +20 for DELTA_MGMT*

### Open Short Calls Against MSTR AB3

| # | Strike | Expiry | Contracts | Entry Credit | Entry Date | Entry Price | Delta @ Entry | Gate @ Entry | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | $140C | Mar 20, 2026 | -20 | — | ~Feb 23 | ~$130 | ~0.30 | — | OPEN (legacy) |
| 2 | $150C | Mar 20, 2026 | -10 | — | ~Feb 23 | ~$130 | ~0.20 | — | OPEN (legacy) |

**Notes on legacy calls:**
- Entered pre-v3.0. Gate state at entry not formally tracked.
- Both expire Mar 20. With MSTR at $129.63 and gate currently NO_CALLS, let these expire worthless or close near expiry.
- Do NOT roll into new short calls until PMCC gate opens (LOI > -20).

### AB2 PMCC — Tracking Template (for new positions)

When opening a new short call, log here:

```
| # | Asset | Strike | Expiry | Contracts | Entry Credit | Entry Date | MSTR/Asset Price | LOI @ Entry | Gate @ Entry | Delta @ Entry | Status |
```

**Rules:**
- Gate must be OTM_INCOME or DELTA_MGMT to open
- OTM_INCOME: delta ≤ 0.25, never within 20% of spot
- DELTA_MGMT: delta ≤ 0.40
- AB1 active on same asset → do not open; close existing short call if breakout confirmed
- Max DTE: 90 days. Target: 30–45 DTE for time decay sweet spot.
- Income target: 2–5%/month of LEAP cost basis (cycle average)

---

## AB2 Legacy — Bull Put Spreads (Retiring)

> Retired under framework v3.0. Manage to expiry. No new entries.

| # | Strategy | Asset | Strikes | Expiry | Contracts | Entry Credit | Entry Date | Breakeven | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Bull Put Spread | TSLA | — | — | — | — | Feb 13, 2026 | — | OPEN — manage to expiry |
| 2 | Bull Put Spread | SPY | — | — | Feb–Mar 2026 | — | Feb 9, 2026 | — | OPEN — manage to expiry |
| 3 | Bull Put Spread | QQQ | — | — | — | — | Feb 25, 2026 | — | OPEN — manage to expiry |

*Note: Exact strikes/credits not on file. Pull from brokerage. Log actuals when available.*

---

## AB1 — Tactical LEAP Positions

> OTM LEAPs 60–120 DTE at CT1/CT2 pre-breakout signals. Exit: LT turns positive or 90-day max.

| # | Asset | Strike | Expiry | Contracts | Entry Cost | Entry Date | LOI @ Entry | CT @ Entry | Status |
|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — | No open AB1 positions |

---

## AB4 — Cash Reserve

| Metric | Value |
|---|---|
| Cash | ~$4,610,000 |
| % of Portfolio | ~92% |
| Target Floor | 25% ($1,250,000) |
| Available to Deploy | ~$3,360,000 (above floor) |

**Deployment priority:**
1. AB3 MSTR — add on Stage 2 re-entry if retests $107-$115
2. AB3 multi-asset — open 2-year LEAPs on SPY/QQQ/GLD/IWM at next accumulation signals
3. AB1 — fire on next CT1/CT2 pre-breakout confirmation

---

## Greeks Summary (Open Positions)

| Position | Delta | Theta | Net |
|---|---|---|---|
| 3,000 MSTR shares | +3,000 | 0 | Long delta, no decay |
| -20x $140C Mar 20 | ~-30 (est.) | +est. | Short delta, theta positive |
| -10x $150C Mar 20 | ~-10 (est.) | +est. | Short delta, theta positive |
| **Net** | **~+2,960 MSTR delta** | **+theta** | Covered call overlay in place |

*Full Greeks: pull live from broker before any new position.*

---

## Watch Levels (MSTR)

| Level | Value | Significance |
|---|---|---|
| PMCC gate open | LOI > -20 | Can begin writing new short calls |
| VLT Fast TL resistance | $133.84 | No new AB3 adds above this |
| LT Fast TL support | $128.89 | Near-term support |
| Cycle bottom | $107 (Feb 5) | Deep accumulation reference |
| Trim 25% trigger | LOI > +40 | First AB3 trim tranche |
| DELTA_MGMT gate | LOI > +40 | ATM calls permitted (Momentum threshold) |

---

## Closed / Expired Positions

| # | Strategy | Asset | Result | Date Closed | Notes |
|---|---|---|---|---|---|
| — | Iron Condor | MSTR | — | — | Retired under v3.0 — do not reopen |
| — | Covered Calls (pre-v3.0) | MSTR | — | — | Mar 20 legacy calls — let expire |

---

## Session Log

| Date | Action | Notes |
|---|---|---|
| 2026-02-23/25 | AB3 entry | 3,000 MSTR shares @ $128.59 avg (Stage 1 deep acc, LOI ~-52) |
| 2026-02-23 | Legacy calls | -20x $140C Mar 20, -10x $150C Mar 20 sold |
| 2026-03-05 | Portfolio-state rewrite | Updated to v3.0 framework; PMCC tracking structure added |
