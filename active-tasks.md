# Active Tasks — Updated 2026-03-01 (end of session)

## Status: P12 Phase 3 Complete — Needs Greg to Add GITHUB_TOKEN to .env

### Completed This Session

| Item | Status | Commit/File |
|---|---|---|
| Web Dashboard generator (`generate_dashboard.py`) | ✅ Done | `fb599f35` |
| MSTR Concordance backtest brief | ✅ Done | `306d2477` |
| P1 v2.0 brief (full allocation framework) | ✅ Done | `fa1550c9` |
| GLI Forecaster (13w model, peak/trough, BTC signal) | ✅ Done | `47c9e02c` |
| AB1 C6 filter (LOI≥8 at signal time) | ✅ Done | `5bcee532` |
| Daily engine run script (`daily_engine_run.py`) | ✅ Done | `c00caab8` |
| Crontab entries (2 new — morning + EOD run) | ✅ Done | `crontab.txt` |

### Blocked — Greg Required

**Action required: Add `GITHUB_TOKEN` to `/mnt/mstr-config/.env` on the host.**

```
GITHUB_TOKEN=<token from Greg's password manager — same token used by the engine>
```

Once added, the daily cron can pull CSVs from GitHub automatically.
Greg also needs to add the two new cron entries from `crontab.txt`.

Also needed (existing blockers):
- `DISCORD_WEBHOOK_GREG` — not yet in .env (Greg's portfolio channel)

### Next Up (Gavin Decision)

1. **P6 TSLA concordance backtest** — CSV available, just needs run
2. **P14 sequencing** — Gavin decides when to start Bearish Bias Suite backtest
3. **P1 v2.0 sign-off** — Greg + Gavin review `four-bucket-framework-v2.0.md`
4. **Morning Brief wiring** — connect existing `morning_brief.py` to new engine output
5. **GLI Forecast calibration** — resolve slope vs trough detection contradiction

### Key Findings This Session

- **AB1 C6 filter**: LOI≥8 at signal time removes both historical MSTR false signals (Jan 2022 bear, Oct 2025 down-trend). Live regime gate handles this in production — the historical scan shows 75% raw, live regime gate pushes effective rate to ~87-100%.
- **AB3 debounce already working**: State machine generates 21 MSTR signals over 4 years (not 600+). Old AB3LOIEngine was the bug — already fixed.
- **Daily pipeline tested**: Full run in 16.4 seconds — CSV sync, engine, dashboard, Discord post.

### Current Engine State (from last run)

- Regime: score=+1, NEUTRAL, vehicle=IBIT, VIX=19.85
- GLI: Z=+0.104, NEUTRAL, GEGI=+0.20
- GLI Forecast: TROUGH DETECTED (5w ago), BTC signal=BULLISH (13w), next inflection ~2026-07
- Dashboard: `/mnt/mstr-data/dashboard.html` (auto-refreshes every 5 minutes)
