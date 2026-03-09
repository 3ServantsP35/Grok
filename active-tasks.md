# Active Tasks
**Last Updated:** 2026-03-09 03:15 UTC

---

## Sprint Complete ✅ (2026-03-09 session)

| Task | Status | SHA/Notes |
|---|---|---|
| AB Bucket v4.0 framework | ✅ | `7441461f` (trading-rules.md), `a49079d1` (AGENTS.md) |
| Training/ folder created on GitHub | ✅ | SRI-Layman-Guide `a723c39c`, Tutorial `db41500f` |
| 52 stale CSVs deleted from GitHub root | ✅ | — |
| Force Field → morning_brief.py Section 4.75 | ✅ | `7b3bfa41` |
| Force Field store → daily_analysis_cycle.py Phase 4 | ✅ | `12978ad1` |
| doi_engine.py built | ✅ | `1af93ec0` |
| DOI → morning_brief.py Section 4.8 | ✅ | `d536bd96` |
| DOI 5 alert types → pmcc_alerts.py | ✅ | `a7877ba8` |
| P10 trend_line_engine.py committed | ✅ | `a3319787` |
| SRI_Forecast_AB1.pine → v7.1 (v4.0 routing notes) | ✅ | `823a65ff` |
| P-BEAR Phase 1 confirmed live | ✅ | PBearEngine in sri_engine.py |
| Greg channel bindings + gateway restart | ✅ | Verified in openclaw.json |
| suite_upload_alert.py crontab install | ✅ | Gavin installed 2026-03-09 |
| DISCORD webhooks (GREG/GAVIN/GARY) | ✅ | All verified set |

---

## Pending — Gavin

- [ ] **STRC/STRF ticker prefixes** — Open Force Field Pine indicator in TradingView;
      confirm STRC and STRF info table rows show non-na values. If na, swap NASDAQ: → BATS: in inputs.
- [ ] **Tutorial v2.5 review** — Training/SRI-Engine-Tutorial-v2.md and Training/SRI-Layman-Guide.md on GitHub

---

## Pending — Greg

- [ ] **#all-alerts channel** — create in Discord + provide webhook URL;
      add DISCORD_WEBHOOK_ALL_ALERTS to .env

---

## 6-Month Checkpoint — Gavin (2026-09-08)

Run on or after 2026-09-08:
  docker exec openclaw-sbx-agent-mstr-cio-7db631bb \
    python3 /mnt/mstr-scripts/mstr_suite_engine.py --calibrate 10 --zone STRONG_BULL

If WR >= 70%:
  sqlite3 /root/mstr-engine/data/mstr.db \
    "INSERT OR REPLACE INTO engine_config VALUES ('suite_bull_graduated','1');"

This graduates STRONG_BULL from PROVISIONAL to HIGH confidence and enables full sizing.

---

## Standing Rules
- sri_engine.py frozen — new engines in separate files
- All Claude calls via api_utils.call_claude()
- Opus only in daily_analysis_cycle.py Python calls
- GitHub: no personal data, P&L, or position sizes ever
- NO NAKED SHORTS — permanent rule, no exceptions
- Pine v6: multi-line ternaries in parens; color(na) not bare na in color chains
