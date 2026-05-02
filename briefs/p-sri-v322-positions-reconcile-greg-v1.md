# P-SRI-v3.2.2 Positions Reconcile — Greg v1
**Project:** P-SRI-V3.2.2-BUILD  
**Date:** 2026-05-01  
**Author:** Cyler (CIO)  
**Status:** **DEFERRED 2026-05-02** — see status note below.

---

## Status note (2026-05-02, Gavin)

This artifact is **deferred indefinitely**, pending broker-data reconciliation that would have required Greg-portfolio operator input. Per the 2026-05-01 ownership transfer, day-to-day operation of the trading systems sits with Gavin alone; Gavin's call (2026-05-02) is to leave Greg's stale option/spread rows as-is for now and not block the rev7 build on this reconciliation.

What this means in practice:

- The convention work in §1 (notional / delta doctrine) **stands** and is canonical for any new position rows.
- The §5.4 backtest continues to run shares-only on Greg's portfolio per the 2026-05-01 instruction; the options exposure understated/dropped per §1 is a known gap, not a fixable defect, until and unless we revive this reconciliation.
- The SQL in this brief has **not been applied** and is not currently scheduled to be applied. The required `BROKER INPUT REQUIRED` markers were never filled in.
- `portfolio_positions` does not exist as a separate table in `mstr.db`; positions live in the existing `positions` table where the stale rows sit.

If we ever revive this work — broker data appears, or a Greg-portfolio refresh becomes worth the effort — this brief is the starting point. Until then, it's archival reference.

---

## Why this exists

The resolver is now live, but Greg's current positions table is not usable for a fair options-aware rollup because multiple open option / spread rows are missing the fields that drive actual exposure math:
- `strikes`
- `expiry`
- `avg_cost`
- `current_price`
- `notional`
- `delta`

If we backtest or run portfolio-resolution logic against this state, the system will systematically understate or drop options exposure.

My recommendation is:
- fix the **convention** first
- reconcile the **stale rows** second
- only then run the backtest

---

# 1. Notional and delta convention table

This is the convention I am willing to defend in PPRs.

## Core doctrine

### Principle A, notional should represent capital-relevant sleeve exposure
Notional is not just a brokerage bookkeeping field. In this framework it should answer:

> how much sleeve-level exposure is this position expressing right now?

For cash equities, that is simple mark value.
For options, the cleanest v1 answer is **underlying-equivalent exposure**, not premium paid and not max-loss bookkeeping alone.

### Principle B, delta should represent signed effective directional exposure per unit underlying
The delta column should be signed so the resolver can aggregate exposure naturally.

### Principle C, spreads should use net-spread delta, not legless placeholders
Any options spread held in the book should eventually have enough structure stored to derive **net spread delta**.

---

## Convention table

| instrument_type | notional convention | delta convention | Notes |
|---|---|---|---|
| `shares` | `abs(qty) × current_price` | `+1.0` for long shares, `-1.0` for short shares | Resolver applies sign via `qty` or signed delta handling |
| `cash` | `cash balance` | `NULL` | No directional delta |
| `short_call` | `abs(qty) × 100 × underlying_price` | `signed option delta × abs(qty) × 100`, negative for short calls | Use current underlying-equivalent exposure, not strike notional or premium |
| `leap_call` | `abs(qty) × 100 × underlying_price` | `signed option delta × abs(qty) × 100` | Long bullish call LEAP |
| `put_leap` | `abs(qty) × 100 × underlying_price` | `signed option delta × abs(qty) × 100`, normally negative | Bearish defined-risk expression |
| `bull_put_spread` | `abs(qty) × 100 × underlying_price` | `net spread delta × abs(qty) × 100` | Use live net delta of short put minus long put |
| `bear_call_spread` | `abs(qty) × 100 × underlying_price` | `net spread delta × abs(qty) × 100`, normally negative | Use live net delta of short call minus long call |
| `strc` / `strk` / `strf` / `strd` shares | `abs(qty) × current_price` | `+1.0` | Preferred shares are cash securities, not option greeks objects |

---

## Why I prefer this convention

### Options notional
I do **not** want options notional defined as:
- premium paid
- strike × contracts
- max loss on spread

for sleeve rollup purposes.

Why:
- premium paid understates economic exposure
- strike notional is too static and can misstate live exposure badly
- max-loss framing is useful for risk controls, but not for benchmark sleeve comparison

For sleeve-level benchmark resolution, what matters is:

> how much underlying sleeve exposure is this option structure currently creating?

That is best approximated by **underlying price × contracts × 100**, paired with a signed delta measure.

### Delta field
Store delta as:

> **signed aggregate contract delta**, not per-contract raw delta only

So for a short call position of `-20` contracts with option delta `0.32`, the stored aggregate delta should be:

`-20 × 100 × 0.32 = -640`

That makes portfolio aggregation much cleaner.

If the schema insists on storing per-contract delta instead, then the resolver must multiply by `qty × 100` consistently. My preference is to store **aggregate signed delta** directly.

---

## Recommended v1 formula summary for implementation

If Archie wants a compact implementation rule for `mstr-knowledge/notional_delta_convention.md`, I would write it this way:

### Shares
- `notional = abs(qty) * current_price`
- `delta = 1.0` for long shares, `-1.0` for short shares

### Cash
- `notional = balance`
- `delta = NULL`

### Single-leg options
- `notional = abs(qty) * 100 * underlying_price`
- `delta = signed option_delta * abs(qty) * 100`

### Option spreads
- `notional = abs(qty) * 100 * underlying_price`
- `delta = signed net_spread_delta * abs(qty) * 100`

### Preferred shares
- `notional = abs(qty) * current_price`
- `delta = 1.0`

---

# 2. Reconciliation actions for stale rows

## General posture

I do **not** think Cyler should fabricate missing options data from doctrine alone.

For backtest integrity, the system needs either:
- broker statement / fill history
- or source-of-truth position journal / trade log

Without that, we should not invent expiries, premiums, strikes, or realized PnL.

So my rule is:
- close only what can be closed safely
- backfill only what can be derived credibly
- otherwise mark as **BROKER INPUT REQUIRED**

---

## Row id=2

### Current row
- `id=2`
- `asset=MSTR`
- `instrument_type=short_call`
- `qty=-20`
- `strikes=140C`
- `expiry=2026-03-20`
- `avg_cost=NULL`
- `current_price=NULL`
- `notional=NULL`
- `delta=NULL`

### Decision
**Mark for manual reconciliation, then close.**

Reason:
- expiry date is known
- but we do **not** know whether this expired worthless, was bought back, was rolled, or was assigned
- we also lack premium / cost basis needed for realized PnL

### BROKER INPUT REQUIRED
- opening trade date
- opening credit / `avg_cost`
- whether the contract expired worthless, was closed early, was rolled, or was assigned
- actual exit date
- actual exit price / debit-to-close if any
- realized PnL
- underlying reference used by broker if assigned

### SQL guidance
```sql
-- id=2 BROKER INPUT REQUIRED before safe closure
-- Required fields: open_date, avg_cost, exit_date, exit_price, exit_reason,
-- realized_pnl, assignment_flag_or_roll_flag
```

### If broker confirms expired worthless
```sql
UPDATE positions
SET status = 'CLOSED',
    exit_date = '2026-03-20',
    exit_price = 0,
    current_price = 0,
    notional = 0,
    delta = 0,
    exit_reason = 'EXPIRED_WORTHLESS',
    realized_pnl = (ABS(qty) * 100 * avg_cost)
WHERE id = 2;
```

---

## Row id=3

### Current row
- `id=3`
- `asset=MSTR`
- `instrument_type=short_call`
- `qty=-10`
- `strikes=150C`
- `expiry=2026-03-20`
- `avg_cost=NULL`
- `current_price=NULL`
- `notional=NULL`
- `delta=NULL`

### Decision
**Mark for manual reconciliation, then close.**

Reason is the same as id=2.

### BROKER INPUT REQUIRED
- opening trade date
- opening credit / `avg_cost`
- whether expired worthless, was closed, rolled, or assigned
- actual exit date
- actual exit price
- realized PnL

### SQL guidance
```sql
-- id=3 BROKER INPUT REQUIRED before safe closure
-- Required fields: open_date, avg_cost, exit_date, exit_price, exit_reason,
-- realized_pnl, assignment_flag_or_roll_flag
```

### If broker confirms expired worthless
```sql
UPDATE positions
SET status = 'CLOSED',
    exit_date = '2026-03-20',
    exit_price = 0,
    current_price = 0,
    notional = 0,
    delta = 0,
    exit_reason = 'EXPIRED_WORTHLESS',
    realized_pnl = (ABS(qty) * 100 * avg_cost)
WHERE id = 3;
```

---

## Row id=4

### Current row
- `id=4`
- `asset=TSLA`
- `instrument_type=bull_put_spread`
- `qty=-1`
- strikes / expiry / avg_cost / current_price / notional / delta all missing

### Decision
**Mark for manual reconciliation. Do not keep as open until backfilled.**

Reason:
- for a spread, missing strikes means we do not even know the structure width
- missing expiry means we do not know whether it is stale, live, or already dead
- missing current delta means the resolver has no exposure basis at all

### BROKER INPUT REQUIRED
- short strike
- long strike
- expiry
- open date
- opening net credit / debit
- current mark
- current net delta or enough leg detail to calculate it
- status, if already closed
- exit date / exit price / realized PnL if closed

### SQL guidance
```sql
-- id=4 BROKER INPUT REQUIRED
-- Required fields: short_strike, long_strike, expiry, open_date, avg_cost,
-- current_price, delta, status, exit_date, exit_price, realized_pnl
```

### If still open after broker input
```sql
UPDATE positions
SET strikes = '<short_put>/<long_put>',
    expiry = '<YYYY-MM-DD>',
    avg_cost = <open_net_credit_or_debit>,
    current_price = <current_mark>,
    notional = ABS(qty) * 100 * <underlying_price>,
    delta = <signed_net_spread_delta_times_100>,
    status = 'OPEN'
WHERE id = 4;
```

### If broker shows it is already closed
```sql
UPDATE positions
SET status = 'CLOSED',
    strikes = '<short_put>/<long_put>',
    expiry = '<YYYY-MM-DD>',
    avg_cost = <open_net_credit_or_debit>,
    exit_date = '<YYYY-MM-DD>',
    exit_price = <close_mark>,
    current_price = 0,
    notional = 0,
    delta = 0,
    exit_reason = '<EXPIRED|CLOSED_EARLY|ASSIGNED>',
    realized_pnl = <realized_pnl>
WHERE id = 4;
```

---

## Row id=5

### Current row
- `id=5`
- `asset=SPY`
- `instrument_type=bull_put_spread`
- `qty=-1`
- strikes / expiry / avg_cost / current_price / notional / delta all missing

### Decision
**Mark for manual reconciliation.**

### BROKER INPUT REQUIRED
- short strike
- long strike
- expiry
- open date
- opening net credit / debit
- current mark
- current net delta or sufficient leg data
- status if already closed
- exit fields if closed

### SQL guidance
```sql
-- id=5 BROKER INPUT REQUIRED
-- Required fields: short_strike, long_strike, expiry, open_date, avg_cost,
-- current_price, delta, status, exit_date, exit_price, realized_pnl
```

### If still open after broker input
```sql
UPDATE positions
SET strikes = '<short_put>/<long_put>',
    expiry = '<YYYY-MM-DD>',
    avg_cost = <open_net_credit_or_debit>,
    current_price = <current_mark>,
    notional = ABS(qty) * 100 * <underlying_price>,
    delta = <signed_net_spread_delta_times_100>,
    status = 'OPEN'
WHERE id = 5;
```

### If already closed
```sql
UPDATE positions
SET status = 'CLOSED',
    strikes = '<short_put>/<long_put>',
    expiry = '<YYYY-MM-DD>',
    avg_cost = <open_net_credit_or_debit>,
    exit_date = '<YYYY-MM-DD>',
    exit_price = <close_mark>,
    current_price = 0,
    notional = 0,
    delta = 0,
    exit_reason = '<EXPIRED|CLOSED_EARLY|ASSIGNED>',
    realized_pnl = <realized_pnl>
WHERE id = 5;
```

---

## Row id=6

### Current row
- `id=6`
- `asset=QQQ`
- `instrument_type=bull_put_spread`
- `qty=-1`
- strikes / expiry / avg_cost / current_price / notional / delta all missing

### Decision
**Mark for manual reconciliation.**

### BROKER INPUT REQUIRED
- short strike
- long strike
- expiry
- open date
- opening net credit / debit
- current mark
- current net delta or sufficient leg data
- status if already closed
- exit fields if closed

### SQL guidance
```sql
-- id=6 BROKER INPUT REQUIRED
-- Required fields: short_strike, long_strike, expiry, open_date, avg_cost,
-- current_price, delta, status, exit_date, exit_price, realized_pnl
```

### If still open after broker input
```sql
UPDATE positions
SET strikes = '<short_put>/<long_put>',
    expiry = '<YYYY-MM-DD>',
    avg_cost = <open_net_credit_or_debit>,
    current_price = <current_mark>,
    notional = ABS(qty) * 100 * <underlying_price>,
    delta = <signed_net_spread_delta_times_100>,
    status = 'OPEN'
WHERE id = 6;
```

### If already closed
```sql
UPDATE positions
SET status = 'CLOSED',
    strikes = '<short_put>/<long_put>',
    expiry = '<YYYY-MM-DD>',
    avg_cost = <open_net_credit_or_debit>,
    exit_date = '<YYYY-MM-DD>',
    exit_price = <close_mark>,
    current_price = 0,
    notional = 0,
    delta = 0,
    exit_reason = '<EXPIRED|CLOSED_EARLY|ASSIGNED>',
    realized_pnl = <realized_pnl>
WHERE id = 6;
```

---

# 3. Forward-looking hygiene guard

Add a daily reconciliation check that runs before resolver / backtest jobs and flags any `positions.status='OPEN'` row that has one of the following problems: `expiry < today`, `current_price IS NULL`, `notional IS NULL`, `delta IS NULL` for any non-cash option structure, or missing `strikes` on any spread type. On hit, the job should post a compact alert to the `system_log` Discord webhook listing `id, asset, instrument_type, expiry, missing_fields`, and optionally set a `data_quality_flag='RECON_REQUIRED'` field if such a field exists. The key is that unresolved exposure rows should fail loud before they distort benchmark rollups or backtests.

---

# 4. Other data-quality gaps spotted

## A. positions schema appears under-specified for spreads
For spreads, a single `strikes` text field is survivable, but not ideal. Long term I would prefer explicit fields:
- `short_strike`
- `long_strike`
- `option_type`
- `contracts`
- `multiplier`

That makes net-delta and max-risk auditing much cleaner.

## B. Missing trade-log linkage
These reconciliation requests would be much easier if every position row were linked to:
- open trade id
- fill history
- close / roll / assignment events

Right now too much lifecycle state is apparently trapped outside the DB.

## C. Expired options should not remain silently OPEN
An expired contract left open in the table is more than cosmetic. It corrupts actual exposure reporting and makes the resolver look wrong when the real issue is stale portfolio data.

## D. Current position snapshot is insufficient for backtest-grade options history
For options-aware backtesting, positions snapshots alone are not enough. You eventually need either:
- historical trade-log events, or
- periodic marks with delta snapshots

Otherwise the system can classify sleeve intent but not reproduce true live exposure through time.

---

## Bottom line

What is safe today:
- adopt the convention table immediately
- close id=2 and id=3 **only after** broker confirms their actual expiry outcome / realized PnL
- hold id=4,5,6 as **manual reconciliation required** until broker fields are backfilled

What is not safe today:
- pretending the missing spread rows have valid exposure
- running the options-aware backtest as if these NULLs were harmless
