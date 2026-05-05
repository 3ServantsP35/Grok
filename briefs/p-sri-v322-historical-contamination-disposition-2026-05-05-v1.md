# P-SRI-V3.2.2 — Historical Contamination Disposition (2026-05-05, v1)

**Project:** P-SRI-V3.2.2
**Date:** 2026-05-05
**Status:** Quarantined — batch cleanup deferred to remediation closeout
**Source:** P0 fix validation pass, 2026-05-05

---

## 1. What was found

The post-fix contamination check on `tv_price_bars` surfaced rows where
two tickers share an identical close value at the same timestamp:

| Window | Tickers | Rows | Hypothesis |
|---|---|---|---|
| 2026-04-20 → 2026-04-28 (5 trading days × 2 4H bars + 4 partial) | `SPY`, `IWM` | 14 | IWM rows have SPY's prices. Pre-rev7-p0fix-v3 stale-session bug. |
| 2013-03-22 (single 4H bar) | `SPY`, `GLD` | 1 | Likely Grok-CSV seed pollution; could also be a legitimate price-overlap coincidence. |
| 2026-05-02 → 2026-05-05 16:00 UTC (forensic pending) | `STABLE_C_D` (any wrong-symbol bars) | unknown | Pre-yaml-fix may have written wrong-ticker bars under `STABLE_C_D`'s PK. |

Full list: `~/mstr-engine/data/data_corruption_log.md` (append-only).

## 2. Disposition: quarantined, NOT cleaned

Per Gavin's directive (2026-05-05): **do not fix piecemeal.** During an
active remediation effort, more findings are likely to surface; per-row
cleanup is wasteful, and bar-by-bar deletion creates uneven gap
geometry. Batch cleanup at remediation closeout, with `Grok-CSV
re-fetch` as the leading approach (clean OHLCV + volume, no surgical
gaps).

The findings are recorded in `data_corruption_log.md` so they can't be
re-discovered as "new" in subsequent audits.

## 3. Implication for soak validation

**Critical separation:** these are **pre-fix bad rows.** They are NOT
evidence of post-fix contamination, and they are NOT counted against
the soak.

- The soak success cross-ticker contamination check
  (soak-success-criteria-v1 §2 Criterion C) explicitly filters
  `ts >= <SOAK_DAY_1>`. Historical rows with `ts < SOAK_DAY_1` are out
  of scope.
- Any contamination detected on rows where `ts >= 2026-05-05` IS
  evidence of post-fix regression and **must escalate immediately**.
  The pre-fix rows are quarantined; the post-fix window must stay
  clean.

## 4. Cleanup checklist (deferred)

When the batch cleanup pass runs (estimated post-soak):

1. Final pass through `data_corruption_log.md` — confirm no new
   findings have appeared since 2026-05-05.
2. For each contaminated window, decide between:
   - **Grok-CSV re-fetch** (preferred per Gavin 2026-05-05): pull
     clean CSVs from Grok for the affected ticker × ts range, replace
     bad rows via UPSERT.
   - **Surgical deletion** (fallback): delete known-bad rows, accept
     the gap. Use only when re-fetch is impractical.
3. After cleanup, re-run the cross-ticker check against the full
   `tv_price_bars` table (no `ts` filter) — should return zero rows
   (modulo any retained legitimate price-overlaps like the 2013
   SPY/GLD case if validated as coincidence).
4. Mark each finding in `data_corruption_log.md` as `cleaned`,
   `accepted`, or `superseded`.

## 5. Forensic check pending

Specifically for `STABLE_C_D`: the YAML fix landed 2026-05-05. Any
warehouse rows written between rev7 launch (2026-05-02) and the YAML
fix (2026-05-05 ~16:30 UTC) under `theme='mstr_suite' AND
ticker='STABLE_C_D'` may contain wrong-symbol data (TV would have
canonicalized to `CRYPTOCAP:STABLE.C.D` while the config said
`STABLE.C.D`).

```sql
SELECT ts, close
FROM tv_price_bars
WHERE theme = 'mstr_suite'
  AND ticker = 'STABLE_C_D'
  AND ingested_at >= '2026-05-02'
  AND ingested_at < '2026-05-05T16:30:00';
-- Sanity check: closes should be in the ~10–13 range (stablecoin
-- dominance index), not equity-like prices.
```

If any rows fail the sanity check, add to `data_corruption_log.md`.
This forensic is bundled into the Fix C drafting work.
