# MSTR/IBIT Pair Trade — Proposed Approach v1.0
**Date:** 2026-03-03
**Status:** Proposal — awaiting Gavin review
**Author:** CIO

---

## The Core Insight

MSTR and IBIT both provide BTC exposure, but through structurally different instruments. IBIT is direct BTC in ETF form — it trades at essentially no premium or discount to BTC NAV. MSTR is a leveraged BTC proxy with embedded optionality: Saylor's ability to issue debt and equity to buy more BTC, the corporate structure, and market sentiment all create a premium (or discount) to the underlying BTC NAV.

That premium — the mNAV ratio — has a predictable cycle that maps to the SRI stage framework:

| Stage | Historical mNAV behavior |
|---|---|
| S4 / S4→1 | mNAV compresses toward or below 1.0x (discount to BTC) |
| S1 / S1→2 | mNAV bottoms and begins recovering toward 1.5x–2.0x |
| S2 (early) | mNAV normalizes toward 2.0x–3.0x |
| S2 (late) / S2→3 | mNAV expands to 3.0x–5.0x (euphoria premium) |
| S3 / S4 | mNAV contracts sharply as premium unwinds |

**Current reading: 0.916x** — MSTR trading below its BTC holdings. Historically, this represents the maximum premium compression. The pair trade opportunity arises because the mNAV mean-reverts toward historical norms (1.5x–3.0x) over every complete cycle.

---

## The Two Trade Expressions

### Expression 1: Relative Allocation (Simpler, Portfolio-Level)

Rather than a simultaneous long/short, adjust the relative weighting between MSTR and IBIT based on mNAV:

| mNAV | MSTR/IBIT relative weight | Rationale |
|---|---|---|
| < 1.0x (current: 0.916x) | MSTR heavily overweight vs IBIT | MSTR cheap on BTC-adjusted basis; mNAV expansion expected |
| 1.0x–1.5x | MSTR moderately overweight | Recovery phase; MSTR still lagging historical premium |
| 1.5x–2.5x | Equal weight | Normalized; no structural edge either way |
| 2.5x–3.5x | IBIT moderately overweight | Premium elevated; IBIT safer BTC expression |
| > 3.5x | IBIT heavily overweight / MSTR underweight | Euphoria premium; mean-reversion risk high |

This is the simplest implementation — it lives entirely within the existing AB3 capital allocation rules. No new instruments needed. Just a signal that says: "at this mNAV level, prefer MSTR over IBIT for BTC exposure."

### Expression 2: Options Spread Pair (More Complex, Higher Upside Capture)

Structured as a directional relative-value spread when mNAV is at extremes:

**At sub-1.0x mNAV (current condition):**
- Long MSTR 2-year LEAPs (deep accumulation + premium recovery)
- Short/underweight IBIT LEAPs or reduce IBIT exposure
- Thesis: MSTR captures BTC appreciation PLUS mNAV recovery from 0.9x → 2.0x+ = compounded return
- Quantified edge: if BTC goes from $68K to $200K and mNAV goes from 0.9x to 2.0x simultaneously, MSTR goes from $134 to ~$790 (+489%), while IBIT would go from $38.72 to ~$114 (+194%) — the premium recovery adds 295 percentage points of outperformance

**At 3.5x+ mNAV (distribution phase):**
- Reduce MSTR; hold IBIT or lean to cash
- Or: buy IBIT LEAPs (simpler BTC play without premium contraction risk)
- Thesis: mNAV mean-reversion from 3.5x → 1.5x at flat BTC price = 57% MSTR decline while IBIT is flat

---

## The SRI Overlay

The ratio itself (MSTR price / IBIT price × IBIT_shares_per_BTC) tracks mNAV and can be analyzed with SRI methods.

**Ratio SRI signals:**
- When ratio LOI is deeply negative (ratio oversold) = premium compressed = MSTR is cheap relative to IBIT = Expression 1/2 buy signal
- When ratio LOI is highly positive (ratio overbought) = premium elevated = trim MSTR relative to IBIT

This is the analytical gap the engine currently has: we have LOI for each asset independently but not for the ratio itself. The pair trade implementation requires adding the MSTR/IBIT ratio as a tracked instrument.

**Inputs needed:**
- MSTR/IBIT ratio CSV from Gavin (same 4H format as other assets)
- mNAV calculation running in the engine (already partially built — uses BTC price + MSTR shares + BTC holdings)

---

## Stage Integration

The pair trade signal integrates cleanly into the existing Stage framework:

| Condition | Pair Trade Implication |
|---|---|
| MSTR S4→1 Forming + mNAV < 1.0x | Maximum MSTR overweight signal. Both the stage and the premium compressed simultaneously. Highest-conviction MSTR entry vs IBIT. |
| MSTR S2→3 Watch + mNAV > 3.0x | Both signals align bearish on MSTR. Shift to IBIT for any remaining BTC exposure. |
| MSTR S2C Confirmed + mNAV 1.5x–2.5x | Neutral pair — no relative trade signal. Hold MSTR if in position; no preference between MSTR and IBIT for new exposure. |
| MSTR S4→1 Confirmed + mNAV < 1.5x | Full MSTR entry. Both premium expansion AND stage recovery playing simultaneously. AB3 entry preferred in MSTR over IBIT. |

---

## mNAV Constants (for engine use)

```python
MSTR_BTC_HOLDINGS = 717_130          # BTC
MSTR_SHARES_OUTSTANDING = 333_750_000  # shares
MSTR_DEBT = 8.19e9                    # $ — adjusts net NAV
MSTR_PREFERRED = 6.92e9              # $ — adjusts net NAV
MSTR_CASH = 2.30e9                   # $ — adjusts net NAV

# Net BTC NAV per share = (BTC_holdings × BTC_price) / shares_outstanding
# mNAV = MSTR_market_cap / Net_BTC_NAV
# Simple mNAV = (MSTR_price × shares) / (BTC_holdings × BTC_price)
```

---

## Implementation Plan

**Phase 1 (Immediate — no new data required):**
- Add mNAV to every MSTR MSR and morning brief (already partially done)
- Define mNAV thresholds in the Stage State Framework as formal MSTR/IBIT weighting signals
- Document the mNAV cycle map (stage → expected mNAV range)

**Phase 2 (Next sprint — requires MSTR/IBIT ratio CSV):**
- Ask Gavin to export MSTR/IBIT ratio CSV (4H, same format)
- Add ratio as a tracked regime input in the engine
- Run LOI on the ratio to generate formal pair trade LOI signals

**Phase 3 (Production — after Phase 2 validated):**
- Pair trade recommendations included in MSR: "MSTR vs IBIT relative weight: MSTR +2 overweight"
- PPR includes specific sizing guidance based on mNAV + ratio LOI + user portfolio state

---

## Key Risk

**The mNAV may not recover on the expected timeline.** If Saylor's capital-raise engine slows or if institutional appetite for leveraged BTC exposure wanes, the premium may remain compressed for longer than historical cycles suggest. This risk is partially mitigated by the fact that at 0.9x mNAV, MSTR is already trading below pure BTC value — the premium compression risk is largely priced in.

**The pair trade is not a hedge.** Both MSTR and IBIT are long BTC in different wrappers. A BTC crash hurts both. The pair trade only captures the relative premium, not the underlying direction.

---

## Pending Questions for Gavin

1. Is the relative allocation approach (Expression 1) sufficient for now, or should we also design the options spread structure (Expression 2)?
2. Can you export the MSTR/IBIT ratio as a 4H CSV from TradingView for Phase 2?
3. Are there additional mNAV data points (e.g., net asset value accounting for debt and preferred) you want incorporated into the ratio calculation?

---

*Next step: Gavin review → if approved, Phase 1 implemented immediately; Phase 2 depends on ratio CSV*
