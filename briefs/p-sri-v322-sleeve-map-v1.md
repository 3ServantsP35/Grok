# P-SRI-v3.2.2 Sleeve Map v1
**Project:** P-SRI-V3.2.2-BUILD  
**Date:** 2026-05-01  
**Author:** Cyler (CIO)  
**Status:** Seed input for Archie resolver implementation

---

## Purpose

This file defines the canonical mapping from:

> **(asset, instrument_type) → sleeve / sleeve_class / rollup_basis**

for the v3.2.2 resolver.

The resolver needs this table to roll actual positions into the 16 AB4 sleeves before comparing them to benchmark posture.

---

## Core mapping doctrine

### 1. Sleeves are economic exposure buckets, not security-type buckets
The map should answer:

> what sleeve is this position economically expressing?

not merely:

> what wrapper is it?

That means:
- `SPY shares` and `SPY bull_put_spread` both roll to **broad US equities**
- `MSTR shares`, `MSTR leap_call`, and `MSTR short_call` all roll to **MSTR common**
- `IBIT shares` and `BITB shares` both roll to **BTC proxy ETFs**

### 2. Default rollup basis
Use these defaults:
- **shares / ETFs / cash** → `notional`
- **options / option spreads / short calls / LEAPs** → `delta_adjusted_notional`
- **cash-like wrappers intentionally treated as operational cash** → `cash_equivalent`

### 3. Negative-delta options should reduce the sleeve they are written against
Examples:
- `MSTR short_call` reduces effective **MSTR common** exposure
- `SPY bear_call_spread` reduces effective **broad US equities** exposure
- `MSTR put_leap` is a bearish expression on **MSTR common**, so it rolls to that sleeve with negative delta-adjusted exposure

### 4. Resolver behavior for unmapped positions
I agree with Archie's proposed default:
- **log a warning**
- **drop the position from the sleeve rollup**
- **surface it clearly in resolver output**

That is better than silently guessing and polluting benchmark-vs-actual calculations.

---

## Important clarifications / ambiguities resolved

### A. MSTR shares
**Resolution:** `MSTR shares` roll to **MSTR common**, not broad US equities.

Reason:
- MSTR common is already an explicit **special sleeve** in the framework
- treating it as broad US equities would hide the exact concentration the doctrine is trying to isolate

### B. QQQ
**Resolution:** `QQQ` rolls to **broad US equities** in v1.

Reason:
- there is no dedicated technology sleeve in the 16-sleeve framework
- QQQ is concentrated, but it is still being used here as a broad US growth-beta proxy rather than a standalone special sleeve

### C. TSLA
**Resolution:** `TSLA` rolls to **broad US equities** in v1.

Reason:
- TSLA is not an explicit AB4 sleeve
- tactical TSLA expressions need a rollup home for resolver math
- if TSLA becomes a recurring strategic overweight that the doctrine wants isolated, that is a **v2 sleeve-design question**, not a v1 mapping question

### D. SGOV / BIL / SHV overlap
**Resolution:**
- `CASH cash`, `SGOV shares`, and `BIL shares` should default to **cash / equivalents**
- `SHY shares`, `VGSH shares`, `SCHO shares` should default to **short Treasuries**
- `SHV shares` is genuinely ambiguous because it often behaves like an operational cash sleeve; for v1 I would map `SHV shares` to **cash / equivalents** unless the portfolio intentionally treats it as a duration sleeve

This is the one place where operational usage matters more than the ticker family.

---

## CSV-ready sleeve map seed

```csv
asset,instrument_type,sleeve,sleeve_class,rollup_basis,notes
CASH,cash,cash / equivalents,standard,notional,Base cash balance
SGOV,shares,cash / equivalents,standard,cash_equivalent,Operational cash proxy
BIL,shares,cash / equivalents,standard,cash_equivalent,Operational cash proxy
SHV,shares,cash / equivalents,standard,cash_equivalent,Treat as cash-like unless explicitly designated as short-duration sleeve
SHY,shares,short Treasuries,standard,notional,Short-duration Treasury sleeve
VGSH,shares,short Treasuries,standard,notional,Short-duration Treasury sleeve
SCHO,shares,short Treasuries,standard,notional,Short-duration Treasury sleeve
TLT,shares,long Treasuries,standard,notional,Long-duration Treasury sleeve
IEF,shares,long Treasuries,standard,notional,Intermediate-to-long Treasury duration expression
LQD,shares,investment-grade credit,standard,notional,IG credit sleeve
SPY,shares,broad US equities,standard,notional,Canonical broad US equity wrapper
VTI,shares,broad US equities,standard,notional,Canonical broad US equity wrapper
QQQ,shares,broad US equities,standard,notional,Treated as broad US growth-beta proxy in v1
SPY,bull_put_spread,broad US equities,standard,delta_adjusted_notional,Income strategy with bullish SPY exposure
SPY,bear_call_spread,broad US equities,standard,delta_adjusted_notional,Bearish or defensive equity expression
SPY,leap_call,broad US equities,standard,delta_adjusted_notional,Leveraged bullish broad equity exposure
SPY,put_leap,broad US equities,standard,delta_adjusted_notional,Bearish broad equity expression
QQQ,bull_put_spread,broad US equities,standard,delta_adjusted_notional,Income strategy with bullish QQQ exposure
QQQ,bear_call_spread,broad US equities,standard,delta_adjusted_notional,Bearish or defensive QQQ expression
QQQ,leap_call,broad US equities,standard,delta_adjusted_notional,Leveraged bullish QQQ exposure
QQQ,put_leap,broad US equities,standard,delta_adjusted_notional,Bearish QQQ expression
XLP,shares,defensive equities,standard,notional,Canonical defensive equity wrapper
XLV,shares,defensive equities,standard,notional,Healthcare as defensive equity sleeve
XLU,shares,defensive equities,standard,notional,Utilities as defensive equity sleeve
XLY,shares,cyclical equities,standard,notional,Canonical cyclical equity wrapper
XLI,shares,cyclical equities,standard,notional,Industrial cyclical expression
XLB,shares,cyclical equities,standard,notional,Materials cyclical expression
IWM,shares,small caps,standard,notional,Canonical small-cap wrapper
IWM,bull_put_spread,small caps,standard,delta_adjusted_notional,Income strategy with bullish small-cap exposure
IWM,bear_call_spread,small caps,standard,delta_adjusted_notional,Bearish or defensive small-cap expression
DBC,shares,commodities broad basket,standard,notional,Canonical broad commodities wrapper
PDBC,shares,commodities broad basket,standard,notional,Alternative broad commodities wrapper
GLD,shares,gold,standard,notional,Canonical gold sleeve
IAU,shares,gold,standard,notional,Alternative gold wrapper
IBIT,shares,BTC proxy ETFs,special,notional,Canonical BTC proxy ETF
BITB,shares,BTC proxy ETFs,special,notional,Alternative BTC proxy ETF
FBTC,shares,BTC proxy ETFs,special,notional,Alternative BTC proxy ETF
IBIT,bull_put_spread,BTC proxy ETFs,special,delta_adjusted_notional,Bullish income expression on BTC proxy sleeve
IBIT,bear_call_spread,BTC proxy ETFs,special,delta_adjusted_notional,Bearish BTC proxy expression
IBIT,leap_call,BTC proxy ETFs,special,delta_adjusted_notional,Leveraged bullish BTC proxy expression
IBIT,put_leap,BTC proxy ETFs,special,delta_adjusted_notional,Bearish BTC proxy expression
VEA,shares,international equities,standard,notional,Developed international equities wrapper
VXUS,shares,international equities,standard,notional,Broad international equities wrapper
VT,shares,international equities,standard,notional,Treated as international sleeve proxy in v1 Howell context
XLE,shares,energy equities,standard,notional,Canonical energy equity wrapper
XLF,shares,financials,standard,notional,Canonical financials wrapper
MSTR,shares,MSTR common,special,notional,Direct MSTR common exposure
MSTR,leap_call,MSTR common,special,delta_adjusted_notional,Leveraged bullish MSTR common exposure
MSTR,put_leap,MSTR common,special,delta_adjusted_notional,Bearish MSTR common expression
MSTR,short_call,MSTR common,special,delta_adjusted_notional,Negative-delta short calls reduce MSTR common exposure
MSTR,bull_put_spread,MSTR common,special,delta_adjusted_notional,Bullish income expression on MSTR common sleeve
MSTR,bear_call_spread,MSTR common,special,delta_adjusted_notional,Bearish or defensive MSTR common expression
STRC,shares,MSTR preferreds,special,notional,Primary MSTR preferred sleeve
STRK,shares,MSTR preferreds,special,notional,MSTR preferred sleeve
STRF,shares,MSTR preferreds,special,notional,MSTR preferred sleeve
STRD,shares,MSTR preferreds,special,notional,MSTR preferred sleeve
TSLA,shares,broad US equities,standard,notional,Tactical single-name growth exposure mapped to broad US equities in v1
TSLA,bull_put_spread,broad US equities,standard,delta_adjusted_notional,Tactical bullish TSLA exposure mapped to broad US equities in v1
TSLA,bear_call_spread,broad US equities,standard,delta_adjusted_notional,Tactical bearish TSLA exposure mapped to broad US equities in v1
```

---

## Per-sleeve canonical summary

### cash / equivalents
Canonical rows:
- `CASH cash`
- `SGOV shares`
- `BIL shares`
- `SHV shares` (cash-like by default in v1)

### short Treasuries
Canonical rows:
- `SHY shares`
- `VGSH shares`
- `SCHO shares`

### long Treasuries
Canonical rows:
- `TLT shares`
- `IEF shares`

### investment-grade credit
Canonical rows:
- `LQD shares`

### broad US equities
Canonical rows:
- `SPY shares`
- `VTI shares`
- `QQQ shares`
- `SPY/QQQ` option structures
- `TSLA` tactical expressions in v1

### defensive equities
Canonical rows:
- `XLP shares`
- `XLV shares`
- `XLU shares`

### cyclical equities
Canonical rows:
- `XLY shares`
- `XLI shares`
- `XLB shares`

### small caps
Canonical rows:
- `IWM shares`
- `IWM` option structures

### commodities broad basket
Canonical rows:
- `DBC shares`
- `PDBC shares`

### gold
Canonical rows:
- `GLD shares`
- `IAU shares`

### BTC proxy ETFs
Canonical rows:
- `IBIT shares`
- `BITB shares`
- `FBTC shares`
- `IBIT` option structures

### international equities
Canonical rows:
- `VEA shares`
- `VXUS shares`
- `VT shares` in v1 Howell context

### energy equities
Canonical rows:
- `XLE shares`

### financials
Canonical rows:
- `XLF shares`

### MSTR preferreds
Canonical rows:
- `STRC shares`
- `STRK shares`
- `STRF shares`
- `STRD shares`

### MSTR common
Canonical rows:
- `MSTR shares`
- `MSTR leap_call`
- `MSTR put_leap`
- `MSTR short_call`
- `MSTR bull_put_spread`
- `MSTR bear_call_spread`

---

## Notes for Archie / resolver behavior

### 1. Instrument-type vocabulary
If the DB or positions table currently uses a different options vocabulary, normalize before join if needed.

Preferred v1 vocabulary:
- `cash`
- `shares`
- `leap_call`
- `put_leap`
- `short_call`
- `bull_put_spread`
- `bear_call_spread`

If an existing row comes in as generic `leap`, I would interpret it as **bullish call LEAP** unless another field distinguishes put vs call.

### 2. Unknown position handling
Recommended v1 behavior:
- leave the benchmark math untouched
- emit a **resolver warning** with `(asset, instrument_type, market_value)`
- show a list of dropped positions in the report output

### 3. Why preferred shares use `notional`
Even though the prompt floated delta relevance for `strc/strk/strf`, I do **not** want preferred shares treated as `delta_adjusted_notional` by default.

Reason:
- they are cash securities, not option wrappers
- their doctrinal role is sleeve-level capital allocation, not option convexity
- delta-adjusting them would understate real committed capital in the MSTR preferred sleeve

So for:
- `STRC shares`
- `STRK shares`
- `STRF shares`
- `STRD shares`

use **`notional`**.

---

## v2 questions, not v1 blockers

These are real questions, but they should not block resolver work today:
- whether `QQQ` deserves its own sleeve later instead of broad US equities
- whether `TSLA` should eventually become an explicit special sleeve if it becomes durable doctrine
- whether `VT` should remain in international equities or become a split-weight global wrapper treatment
- whether certain ultra-short Treasury wrappers should be portfolio-configurable between `cash / equivalents` and `short Treasuries`
