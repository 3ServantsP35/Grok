# Active Tasks — Updated 2026-03-08

## Completed This Session (2026-03-08)

| Item | Status | Ref |
|---|---|---|
| AB Bucket Framework v4.0 | ✅ Done | `mstr-knowledge/trading-rules.md` |
| Force Field Pine indicator (Layer 0.75) | ✅ Done | `pine/MSTR_Suite_Force_Field.pine` SHA `60b7b013` |
| Force Field structural gap gate (BOUNCE EXHAUST) | ✅ Done | SHA `60b7b013` — 93% bearish +20d when SB + struct gap |
| INDICATOR-GUIDE.md updated | ✅ Done | Force Field + STRF/LQD sections added SHA `9813597c` |
| AGENTS.md Strategy Library updated to v4.0 | ✅ Done | |
| suite_upload_alert.py built + committed | ✅ Done | SHA `1d1b7963` |

## Blocked — Gavin Required

- **Install updated crontab**: `cd ~/Grok && git pull && cp scripts/suite_upload_alert.py ~/mstr-engine/scripts/ && cp scripts/crontab_updated.txt ~/mstr-engine/scripts/ && crontab -u openclaw ~/mstr-engine/scripts/crontab_updated.txt`
- **Verify STRC/STRF ticker prefixes** in Force Field indicator (NASDAQ: vs BATS: — check if na in TV)
- **6-month checkpoint (2026-09-08)**: Run `mstr_suite_engine.py --calibrate 10 --zone STRONG_BULL`; graduate if WR ≥70%

## Blocked — Greg Required

- Add 3 channel bindings to `openclaw.json` + gateway restart
- Create #mstr-gary webhook → add `DISCORD_WEBHOOK_GARY` to `.env`
- Install updated crontab: `crontab -u openclaw ~/mstr-engine/scripts/crontab_updated.txt`
- Verify `DISCORD_WEBHOOK_GREG` and `DISCORD_WEBHOOK_GAVIN` still valid
- Create #all-alerts channel → provide `DISCORD_WEBHOOK_ALL_ALERTS`

## In Progress / Next Up

- **Wire `mstr_suite_engine.py` into `morning_brief.py`** — Section 4 force signal block
- **Wire `--store` into `daily_analysis_cycle.py`** — auto-persist signals each cycle
- **P-DOI integration** — add DOI block to `morning_brief.py` + 5 alert events
- **SRI AB1 Pine rebuild for QQQ** — `lt_flip_with_st_pos` as primary entry
- **Commit P10 files to GitHub** — `trend_line_engine.py` + updated `morning_brief.py`
- **Tutorial v2.5 review** — Gavin to review `SRI-Engine-Tutorial-v2.md`

## Key Decisions Locked

- **No naked shorts** — permanent rule, no exceptions, no approval overrides
- **AB4 hard floor 10% true cash** — unchanged
- **PMCC classification by intent**: long leg = AB3; short leg = AB1 (theta) or AB2 (directional)
- **AB1 + AB2 combined ≤ 20%** of total portfolio
- **Force Field BOUNCE EXHAUST** = STRONG_BULL + price >10% below LT Slow TL = 93% bearish +20d
- **Bull zones PROVISIONAL** until 2026-09-08 checkpoint

