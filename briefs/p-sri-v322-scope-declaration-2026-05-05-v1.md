# P-SRI-V3.2.2 — Scope Declaration (2026-05-05, v1)

**Project:** P-SRI-V3.2.2
**Date:** 2026-05-05
**Status:** Active — formalizes Path 2 governance per Cyler's remediation brief §5
**Authority:** Gavin (operator), confirmed by Cyler (architect) 2026-05-05
**Source brief:** `p-sri-v322-architecture-remediation-brief-2026-05-04-v1.md` §5

---

## 1. Production v1 scope

| Theme | Status | Tickers | Timeframe | Scheduler |
|---|---|---|---|---|
| `mstr_suite` | **Accepted v1 production** | 16 | 4H | `com.mstr.tv-feed` LaunchAgent, twice daily Mon–Fri |

### `mstr_suite` ticker set

```
MSTR, IBIT, BTCUSD, STRC, STABLE_C_D, STRF, STRD, SPY, GLD, IWM, DXY,
MSTR_IBIT, STRF_LQD, STRD_HYG, BTC_GOLD, MSTR_SPY
```

This is the only theme that the production cron polls. Bars and indicators
written under `theme='mstr_suite'` are governed by the soak/acceptance
criteria in `p-sri-v322-soak-success-criteria-2026-05-05-v1.md`.

## 2. Staging scope

| Theme | Status | Tickers | Timeframe | Scheduler |
|---|---|---|---|---|
| `visser` | Staging | 35 | 4H, 1D | None (Grok-CSV seed-and-replay only) |
| `mr_assets` | Staging | 15 | 4H, 1D | None (Grok-CSV seed-and-replay only) |
| `grok_backfill` | Staging utility bucket | 9 | 4H, 1D | None (Grok-CSV seeds) |

Staging themes have warehouse data populated via manual Grok-CSV historical
backfill runs (`tv_ingest_runs.run_kind='seed'`). They are NOT polled by the
production scheduler. Their `enabled: true` flag in `config/tv_themes.yaml`
indicates "ready to be promoted," not "currently in production."

## 3. Promotion criteria

A staging theme can be promoted to production after ALL of:

1. Production v1 (`mstr_suite`) soak passes (per soak-success-criteria brief).
2. The theme's tickers all resolve correctly via the rev7-p0fix-v3 patched
   `set_symbol()` (no `quote_symbol != requested` mismatches).
3. A theme-specific soak — minimum 3 trading days of clean scheduled polls
   with the same pass criteria as `mstr_suite` v1.
4. Cyler architecture sign-off + Gavin operator sign-off.

## 4. Phased promotion plan (post-mstr_suite-soak)

Recommended ordering:

1. **`visser` first.** Larger ticker count and deeper history makes it a
   better stress test for the patched scheduler. Symbol resolution edge
   cases (e.g., `STABLE_C_D`-class canonicalization) more likely to
   surface here than in `mr_assets`.
2. **`mr_assets` second**, after one clean trading day of `visser` polling.
3. **`grok_backfill`** stays a utility bucket; not currently planned for
   cron promotion.

LaunchAgent design for staged promotion is not committed yet. Two options
on the table:
- **Option A:** one cron job per theme (`com.mstr.tv-feed-visser`,
  `com.mstr.tv-feed-mr-assets`).
- **Option B:** single cron job iterates all enabled themes
  (`tv_poll.py --all-enabled`).

Decision deferred until post-soak.

## 5. Out of scope for v1

- Indicator history extraction (TV CLI does not expose; warehouse
  accumulates forward from each poll).
- Sub-4H timeframes for `mstr_suite` tickers (1D/2H entries exist for some
  tickers via legacy paths but are not in the v1 acceptance scope).
- Any theme not enumerated in this document.

## 6. Authoritative source

This document is the canonical scope reference. Where it conflicts with
`config/tv_themes.yaml` (`enabled: true` flags), this document governs;
the YAML's `enabled: true` is operationally permissive but does not imply
production status.

When this document changes, update via a versioned successor
(`p-sri-v322-scope-declaration-YYYY-MM-DD-vN.md`) rather than editing in
place. Append-only history makes scope drift visible.
