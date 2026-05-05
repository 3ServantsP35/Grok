# P-SRI-V3.2.2 — P0 Closure Note (2026-05-05, v1)

**Project:** P-SRI-V3.2.2
**Date:** 2026-05-05
**Status:** P0 closed pending soak confirmation
**Source brief:** `p-sri-v322-architecture-remediation-brief-2026-05-04-v1.md` §3 Priority 0

---

## 1. Root-cause summary

**Symptom (Cyler 2026-05-04):** distinct symbols (`AMEX:SPY`, `AMEX:GLD`,
`AMEX:IWM`) returned the same latest OHLCV bar through the live TV ingest
path. Warehouse rows untrustworthy.

**Root cause (Archie 2026-05-05):** TradingView Desktop process (PID 81617,
alive since 2026-04-30 17:00 PT) had lost its live data subscription. The
CDP API layer continued to accept and acknowledge `tv symbol XXX` commands
— `chart_state.symbol` updated immediately — but the underlying chart's
data window was frozen on a cached series. `ohlcv` and `quote` returned
the frozen bars regardless of which symbol was nominally active. The bug
class is **stale data subscription, not symbol-switch race.**

## 2. Why initial fix attempts were insufficient

### v1 — `chart_state` polling
Polled `chart_state()` after `set_symbol()` until `state["symbol"] ==
requested`. Insufficient: `chart_state` reports the requested symbol
immediately even when no data has loaded. The polling loop exited
"successfully" while ohlcv continued returning frozen bars.

### v2 — `chart_ready` + freshness gate
Polled `tv symbol`'s `chart_ready` field plus a quote freshness check.
**`chart_ready` empirically unreliable:** TV's CLI returns
`chart_ready: false` persistently even on a healthy chart that has loaded
fresh data. Confirmed post-restart: `tv symbol "NASDAQ:MSTR"` →
`chart_ready: false`, but `tv quote` returned `time=1777987800` with
`close=186.77` (correct fresh MSTR price). Treating `chart_ready` as a
strict gate fail-closed against working TV.

### v3 (current) — `tv quote` round-trip gate
Polls `tv symbol` (idempotent) then `tv quote` until ALL of:
- `quote.success == true`
- `quote.symbol == requested_symbol`
- `quote.time` within `DATA_FRESHNESS_MAX_AGE_HOURS` (72h) of now

This passes against healthy TV (quote returns the just-switched symbol's
real fresh data) and fail-closes against stale TV (quote returns the
prior frozen series, so `quote.symbol != requested` until the chart
actually switches and `quote.time` exceeds the threshold).

## 3. Implementation

- `~/mstr-engine/scripts/tv_ingest.py` — `set_symbol()` rewritten;
  module docstring includes iteration history; `_run()` now treats
  `success: false` from the CLI as a failure.
- `~/mstr-engine/scripts/tv_poll.py` — `poll_ticker()` adds a post-read
  drift guard (Layer 3) that re-checks `chart_state.symbol` after `ohlcv`
  + indicator reads. `_alert()` now sends an explicit User-Agent header
  to bypass Cloudflare CF1010 blocking of default Python urllib UA.

## 4. Operational recovery (one-time)

Stale TV process recycled via:

```bash
launchctl kickstart -k gui/$(id -u)/com.camel.tradingview
```

Old PID 81617 → new PID 5572. Data subscription restored.

This is the standard recovery pattern documented in
`~/.claude/projects/-Users-vera/memory/lessons_tradingview_cdp.md`.
The new patch causes any future stale-session event to fail-closed
loudly (Discord alerts) rather than silently writing corrupt data, but
recovery still requires this kick.

## 5. Status

**P0 closed pending soak confirmation.**

- Patch landed, validated against both the broken (frozen TV) and the
  fixed (post-kick TV) states.
- All four re-acceptance bars from the remediation brief satisfied —
  see soak-success-criteria brief for the reproducible queries.
- `com.mstr.tv-feed` re-bootstrapped 2026-05-05 ~16:30 UTC.
- Soak day 1 = first successful scheduled poll on/after re-bootstrap.

P0 will be marked **closed** once the soak passes (target ~2026-05-13).
Until then, treat as "remediated, awaiting field validation."

## 6. Architectural lesson for the record

When verifying a CDP-fronted system's state, **don't trust the API's
self-report; verify via the actual data path.** TV's `chart_state` and
`chart_ready` both reported things that didn't match the chart's
behavior. The reliable signal was downstream — `tv quote`'s round-trip
of symbol + time fields.

This generalizes: any system where a control plane and a data plane can
disagree (especially if the data plane has its own caching, async
loading, or external subscriptions), gate on the data plane, not the
control plane.
