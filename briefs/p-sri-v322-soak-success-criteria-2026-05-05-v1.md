# P-SRI-V3.2.2 — Soak Success Criteria (2026-05-05, v1)

**Project:** P-SRI-V3.2.2
**Date:** 2026-05-05
**Status:** Active — defines reproducible pass criteria for P0 soak
**Source brief:** `p-sri-v322-architecture-remediation-brief-2026-05-04-v1.md` §5
**Companion:** `p-sri-v322-p0-closure-note-2026-05-05-v1.md`

---

## 1. Soak window

- **Soak day 1:** date of the first successful scheduled poll on or after
  2026-05-05 16:30 UTC (when `com.mstr.tv-feed` was re-bootstrapped).
- **Soak end target:** ~2026-05-13 (the seventh trading-day's 13:00 PT poll).
- **Required runs:** 13 polls (= 7 trading days × 2 polls/day, minus the
  first day's morning poll if re-bootstrap was after 09:30 PT).
- **Theme in scope:** `mstr_suite` only (per scope-declaration-v1).

## 2. Pass criteria

All FOUR conditions must hold:

### Criterion A — Poll count

≥13 rows in `tv_ingest_runs` with `run_kind='poll'`, `theme='mstr_suite'`,
and `started_at >= '<soak day 1>'`.

```sql
SELECT COUNT(*) AS poll_count
FROM tv_ingest_runs
WHERE run_kind = 'poll'
  AND theme = 'mstr_suite'
  AND started_at >= '<SOAK_DAY_1>';
-- Pass: poll_count >= 13
```

### Criterion B — Zero failures

No poll runs with `tickers_fail > 0`.

```sql
SELECT COUNT(*) AS failed_runs
FROM tv_ingest_runs
WHERE run_kind = 'poll'
  AND theme = 'mstr_suite'
  AND started_at >= '<SOAK_DAY_1>'
  AND tickers_fail > 0;
-- Pass: failed_runs = 0
```

If `failed_runs > 0`, list them:

```sql
SELECT id, started_at, tickers_ok, tickers_fail, notes
FROM tv_ingest_runs
WHERE run_kind = 'poll'
  AND theme = 'mstr_suite'
  AND started_at >= '<SOAK_DAY_1>'
  AND tickers_fail > 0
ORDER BY started_at;
```

### Criterion C — No cross-ticker close-equality contamination

Within the soak window, no two tickers in `mstr_suite` write the same
close value at the same `ts`.

```sql
SELECT ts, close, GROUP_CONCAT(ticker) AS tickers, COUNT(*) AS n
FROM tv_price_bars
WHERE theme = 'mstr_suite'
  AND timeframe = '4H'
  AND ts >= '<SOAK_DAY_1>'
GROUP BY ts, close
HAVING n > 1
ORDER BY ts DESC;
-- Pass: zero rows
```

**Note:** This check applies ONLY to bars with `ts >= <SOAK_DAY_1>`.
Pre-soak rows may show contamination from the historical SPY/IWM bug
(see `~/mstr-engine/data/data_corruption_log.md`); those are
quarantined and out of scope for soak validation. See historical-
contamination-disposition brief.

### Criterion D — Indicator pipeline staying live

`tv_state.md` and `tv_history_index.md` mtimes stay current through the
window — should refresh after each successful poll.

```bash
WS=~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge
stat -f '%Sm %N' "$WS/tv_state.md" "$WS/tv_history_index.md"
# Pass: both files have mtime within 4h of the most recent poll's
# `finished_at`.
```

## 3. Reproducible end-of-soak script

```bash
#!/usr/bin/env bash
# Run this on or after 2026-05-13 to evaluate the soak.
SOAK_DAY_1='2026-05-05'   # set to the actual first-poll date once observed
DB=~/mstr-engine/data/mstr.db

echo "=== Criterion A — Poll count (target ≥13) ==="
sqlite3 "$DB" "
SELECT COUNT(*) AS poll_count
FROM tv_ingest_runs
WHERE run_kind = 'poll'
  AND theme = 'mstr_suite'
  AND started_at >= '$SOAK_DAY_1';
"

echo "=== Criterion B — Failed runs (target 0) ==="
sqlite3 "$DB" "
SELECT COUNT(*) AS failed_runs
FROM tv_ingest_runs
WHERE run_kind = 'poll'
  AND theme = 'mstr_suite'
  AND started_at >= '$SOAK_DAY_1'
  AND tickers_fail > 0;
"

echo "=== Criterion C — Cross-ticker contamination in soak window (target 0) ==="
sqlite3 "$DB" "
SELECT ts, close, GROUP_CONCAT(ticker) AS tickers, COUNT(*) AS n
FROM tv_price_bars
WHERE theme = 'mstr_suite'
  AND timeframe = '4H'
  AND ts >= '$SOAK_DAY_1'
GROUP BY ts, close
HAVING n > 1
ORDER BY ts DESC;
"

echo "=== Criterion D — workspace summary file freshness ==="
stat -f '%Sm %N' \
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_state.md \
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_history_index.md
```

## 4. Daily health snapshot (during soak)

Once per day during the soak window, post a short status to Cyler with:

```sql
-- Today's polls (count, fail count, bars/values written)
SELECT COUNT(*) AS polls_today,
       SUM(tickers_fail) AS total_failures,
       SUM(bars_written) AS bars_written,
       SUM(values_written) AS values_written
FROM tv_ingest_runs
WHERE run_kind = 'poll'
  AND theme = 'mstr_suite'
  AND date(started_at) = date('now');

-- Cross-ticker contamination check for today's bars
SELECT ts, close, GROUP_CONCAT(ticker) AS tickers
FROM tv_price_bars
WHERE theme = 'mstr_suite'
  AND timeframe = '4H'
  AND date(ts) = date('now')
GROUP BY ts, close
HAVING COUNT(*) > 1;
```

If any check shows drift, escalate immediately — soak signal is
broken; do not wait for end of window.

## 5. Pass / fail decision

- **All four criteria pass** → P0 marked closed, §5.6 P-TVI retirement
  cleared to execute, staging themes can begin promotion per
  scope-declaration-v1 §3.
- **Any criterion fails** → soak does NOT pass. Diagnose the failure,
  fix root cause, restart soak clock from day 1. Do not partial-credit.
