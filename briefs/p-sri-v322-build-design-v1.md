# P-SRI-V3.2.2: Build Design — Howell Phasing, AB4 Profiles, AB3 Ruleset

**Project:** P-SRI-V3.2.2-BUILD
**Version:** v1 — Draft for Greg + Gavin review
**Date:** 2026-04-30
**Revision history:**
- rev1 — initial draft, two AB4 profiles, Camel-served TV feed
- rev2 — added RAW Hybrid profile (third AB4 profile, computed midpoint)
- rev3 — redirected TV ingest to MSTR Engine, added §5.9 Camel decommission track, recast §6 effort estimate with explicit units (Archie execution time vs calendar time)
- rev4 (2026-05-01) — Gavin signed off on §5.4 acceptance bars and overall sequence. Greg sign-off no longer required (full ownership of trading systems transferred to Gavin same day). §5.9 Camel decommission now gated on Gavin alone + Pine fidelity audit. §5.1 schema/bug-fix work was already executed 2026-04-30 and is reflected in current `mstr.db` state — see Status note in §10. Primary track unblocked pending Cyler's §7.1 weights.
- rev5 (2026-05-01) — §5.1–§5.4 all complete. Cyler authored §7.1 weights, §7.2 tier ladder, §7.5 RAW Hybrid doctrine (`briefs/p-sri-v322-cyler-inputs-v1.md`), and the canonical sleeve_map (`briefs/p-sri-v322-sleeve-map-v1.md`). Two unplanned additions: `ab3_tier_thresholds` table (not originally in §5.2; tier ladder needed an auditable home) and `sleeve_map` table (not originally in design — discovered as a gap during §5.3 implementation). Positions reconciliation artifact authored (`briefs/p-sri-v322-positions-reconcile-greg-v1.md`); SQL not yet applied — pending broker data input from Gavin. §5.4 backtest passes infrastructure bars (1, 2, 4); bar 3 skipped on single-phase history (all rows Turbulence). Portfolio scope expanded to all five operators (Gavin/Greg/Gary/Kathryn/Ali), all defaulting to RAWHybrid.
- rev6 (2026-05-02) — **Camel Engine decommission de-scoped per Gavin.** Build now stops at "MSTR Engine writes the workspace data feed that replaces Cyler's manual GitHub-CSV upload." Camel Engine continues running unmodified — no Pine port, no LaunchAgent disable, no codebase archive, no two-engine reframing of CLAUDE.md. §5.9, the §6 Camel-decom row, §7.4, the §8 Camel-decom risk rows, the §10 Greg-sign-off entry, and the Camel-decom block in Appendix A are all retired. D13 is withdrawn. The CSV-decom functionality inside MSTR Engine (§5.5 + §5.6) is unchanged and remains the active deliverable.
- rev7 (2026-05-02) — **§5.5 reframed from CSV snapshot feed to price+indicator timeseries warehouse.** Per Gavin: ticker is the organizing unit, theme determines the TV layout that defines the indicator stack, and `mstr.db` is the canonical warehouse of OHLCV + indicator history per (ticker, timeframe). v1 ships the **MSTR Suite** theme only — 16 tickers (incl. 5 ratio charts and STABLE.C.D dominance series) under the `MSTR Suite - Download` layout. Single timeframe **4H**. History seeded back to **March 2009** where available, **3y minimum** otherwise. Recurring cadence: twice daily Mon–Fri at **11:30 CT** and **15:00 CT** (incl. Bitcoin). Cyler reads workspace summary files (`tv_state.md`, `tv_history_index.md`) plus a SQL helper (`tv_query.py`) for ad-hoc deep dives — not a flat-file data-feed dir. The earlier session-cookie auth assumption is also retired: implementation reuses Camel's CDP attach to TV Desktop on `127.0.0.1:9222`, no cookie. Adds D14–D17, expands §5.2 schema with `tv_price_bars` / `tv_indicator_values` / `tv_ingest_runs`, fully rewrites §5.5, retires the data-feed dir and the manual cookie-rotation procedure. MR Assets and Visser themes deferred to a follow-on rev once their layouts and ticker scopes are confirmed.
**Author:** Archie (on behalf of Gavin + Greg)
**Source briefs:**
- `briefs/howell-phase-allocation-tutorial-v1.md` (Cyler, 2026-04-27)
- `briefs/p-ab3-ruleset-v1.md` (Cyler, 2026-04-28)
- `briefs/SRI-Engine-Tutorial-v3.md` (v3.2.2 DRAFT, Cyler, 2026-04-22)

---

## 1. Executive summary

v3.2.2 reframes the AB framework. **AB4 is the benchmark anchor** with three profiles (Rotational, All-Weather, RAW Hybrid), sized by Howell phase. **AB3 is the deviation layer** atop the chosen benchmark, scrutinised by phase, profile, and a tolerance band before being classified as a real deviation. The existing engine partially implements the inputs (Howell phase classifier, sector SRIBI ingest, GLI proxy) but the AB3/AB4 enforcement layer encodes an older mental model and must be rebuilt.

**Profile definitions:**
- **Rotational** — aggressively avoids bearish positions; phase-expressive, leans most into offensive sleeves when phase is supportive and most defensive when it is not.
- **All-Weather** — intentionally smoother, less aggressive; carries balanced exposure across phases.
- **RAW Hybrid** (Rotational-All-Weather Hybrid) — derived profile. Per-sleeve weight is the **arithmetic midpoint** of Rotational and All-Weather weights for the same (phase, sleeve). Architectural consequence: RAW Hybrid does not inherit Rotational's bearish-avoidance *stance* — it dilutes it by 50%. A sleeve that Rotational holds at 0% in Turbulence and All-Weather holds at 5% will appear in RAW Hybrid at 2.5%. This is the intended semantic of "midpoint of the difference"; flagging it explicitly so Cyler can confirm.

This document defines the build that closes the gap. It assumes the existing `HowellPhaseEngine` is reused and bug-fixed; it adds new tables, modules, and a backtest harness; it migrates Cyler off manual GitHub-CSV uploads onto an MSTR-Engine-fed workspace data feed; it rewrites `AGENTS.md` to match v3.2.2 doctrine.

It does **not** ship until backtest validates the classifier and the new ruleset.

**Operational shift baked into this build (rev7, 2026-05-02):** TV ingest is owned by MSTR Engine, not Camel Engine. §5.5 builds an **OHLCV + indicator timeseries warehouse** in `mstr.db`, fed by twice-daily polls of TradingView Desktop (Mon–Fri at 11:30 CT and 15:00 CT, including Bitcoin). The organizing unit is the **theme**: each theme has a named TV layout that already has the right indicator stack applied (e.g., `MSTR Suite - Download` for MSTR Suite tickers; `MR Assets - Download` for sector / macro / regime tickers; future themes — Visser etc. — get their own layouts). v1 ships the **MSTR Suite** theme only: 16 tickers including 5 ratio charts and the STABLE.C.D stablecoin-dominance series, single 4H timeframe, history seeded back to March 2009 where available. The MSTR-Engine-owned warehouse is the replacement for Cyler's manual GitHub-CSV upload pattern. Camel Engine itself stays running unchanged — no decommission, no Pine port of cycle indicators, no operational surface reduction in this build (per rev6 descope, retained in rev7).

---

## 2. Current state — what exists, what's stale

### 2.1 Engine code

| Component | File / line | Status |
|---|---|---|
| `HowellPhaseEngine` | `sri_engine.py:1298` | **Reuse with fixes.** Implements the full Rebound/Calm/Speculation/Turbulence signature matrix across XLK, XLY, XLF, XLE, XLP, TLT, GLD, IWM, VT, DBC. Live. |
| `HowellPhaseState` | `sri_engine.py:1225` | Reuse. Properties (`ab3_beta_eligible`, `ab3_size_multiplier`, etc.) encode an older AB3 model and must be **deprecated** once the new resolver is in place. |
| `AB3StateMachine` | `sri_engine.py:1990` | **Legacy.** Encodes AB3 = LEAP accumulation via LOI thresholds (NEUTRAL → ACCUMULATING → HOLDING → TRIMMING). Keep as a *signal source* feeding the new resolver; do not let it drive bucket classification. |
| `AllocationEngine` | `sri_engine.py:2130` | **Legacy.** Default 25/25/25/25 baseline. Incompatible with v3.2.2 (benchmark depends on profile × phase). Stop using once new resolver is in place. |
| `gli_engine.py` | Grok root, 763 lines | Reuse. GLI is a Howell signal input. |
| `collect_gli_proxy.py` | Grok root, 503 lines | Reuse. Daily GLI proxy collection. |

`sri_engine.py` is frozen by standing rule (active-tasks.md). All new work goes in new files.

### 2.2 Database

| Table | Rows | Status |
|---|---:|---|
| `howell_phase_state` | 71 (2026-03-03 → 2026-04-30) | Active. **Schema gap:** lacks columns for VT and DBC SRIBI/signals (the engine computes them; the table drops them). |
| `howell_phase_transitions` | (small) | Active. |
| `portfolio_aggregate`, `portfolio_config`, `portfolio_marks` | live | Reuse for actual-portfolio inputs to the resolver. |
| `ab_profile_selection`, `ab4_benchmark_*`, `ab4_tolerance_bands`, `ab3_deviation_log` | (none) | **Net new.** §6 specifies. |

Latest phase as of 2026-04-30 14:00 UTC: **Turbulence, confidence 20** (read directly from `mstr.db`).

### 2.3 Doctrine drift — three layered generations on disk

| Source | AB3 means | AB allocation baseline | Recency |
|---|---|---|---|
| `AGENTS.md` (Grok + workspace) | Structural accumulation via LEAPs | 50/25/25/0 | 2026-03-08 / 2026-03-31 |
| `AllocationEngine` Python | LEAP accumulation bucket | 25/25/25/25 | 2026-03-16 |
| **v3.2.2 + AB3 ruleset** | **Deviation layer atop AB4 benchmark** | Profile (Rotational \| All-Weather) × phase | **2026-04-22+** |

Cyler currently operates on the older mental model. v3.2.2 sits unintegrated in `briefs/`. **Doctrine reframing in `AGENTS.md` is part of this build, not a follow-up.**

### 2.4 Cyler workspace

`~/.openclaw-mstr/workspace-mstr-cio/Grok/` is a local checkout of `3ServantsP35/Grok`, refreshed daily (last 2026-04-30 06:07). Cyler's "read CSVs from Main" is a local-filesystem read against this checkout, not a GitHub API call. The migration target is therefore writing CSVs into a workspace-readable directory rather than serving them from a remote endpoint.

---

## 3. Findings from audit — three latent bugs

These were discovered during code review on 2026-04-30. None are blocking the build; all get fixed inside it.

### 3.1 Stale-read bug (P0 once exposed)
`scripts/daily_analysis_cycle.py` reads `howell_phase_state WHERE id=1` at lines **257** and **464**. Row id=1 is from **2026-03-03**, ~58 days stale. Cyler's morning brief has been reading a frozen value. Hidden by luck because the phase classifier output has been Turbulence both then and now. If the classifier had transitioned, Cyler would never have seen it. Same pattern likely in `scripts/morning_brief.py` and `scripts/pmcc_alerts.py` (both grep-positive for `howell_phase_state`).

**Fix:** read by `MAX(timestamp)` or `ORDER BY id DESC LIMIT 1` in step §5.1.

### 3.2 Schema drift in `howell_phase_state`
Python `HowellPhaseEngine` computes signals for 10 sectors (XLK, XLY, XLF, XLE, XLP, TLT, GLD, IWM, VT, DBC). The DB table has columns for only 8 (lacks VT, DBC). VT and DBC values are silently dropped before persistence.

**Fix:** ADD COLUMN migration in step §5.1. Backfill from re-running classifier over recent CSVs is optional (the live values aren't load-bearing for the existing classifier *score*, only for forensic review).

### 3.3 Engine-file drift
Local `~/mstr-engine/scripts/sri_engine.py` is dated **2026-03-16**, 56 bytes smaller than the canonical Grok copy (pulled today). Cron paths run the local file, so the **deployed engine is behind the GitHub canonical version**.

**Action:** before any new work, `diff` the two and reconcile. Either pull GitHub down, or push local up — but stop the divergence. Step §5.1.

---

## 4. Architecture decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | **Reuse `HowellPhaseEngine`**, do not rewrite. | Already implements signature matrix, already writing daily rows. Rewriting buys nothing. |
| D2 | **AB4 profile selection is per-portfolio**, stored in `ab_profile_selection`. Three profiles available: Rotational, All-Weather, RAW Hybrid. | Each tracked portfolio (Greg / Gavin / Kathryn / Ali / mock) can run a different profile. |
| D3 | **Howell phase governs AB4 benchmark sizing**, via lookup tables (one per profile) keyed on `(profile, phase, sleeve)`. | Per Cyler's Howell brief: phase drives AB4 weights for the chosen profile. |
| D4 | **Tolerance bands from AB3 ruleset §9.3 are seeded as the v1 numbers**; backtest tunes them. | The brief gives concrete starting values. |
| D5 | **AB3 is computed, not stored as a portfolio target.** | AB3 deviation is a *classification* of actual positions vs benchmark, not a separate bucket with its own target. The AllocationEngine 25/25/25/25 model is wrong. |
| D6 | **Frozen `sri_engine.py` stays frozen.** All new logic goes in new modules under `~/mstr-engine/scripts/`. Bug fixes (§3.1, §3.2) are the only sri_engine touch points. | Standing rule from `active-tasks.md`. |
| D7 | **Migrate Cyler off GitHub-CSV via MSTR Engine workspace feed**, not via a synchronous endpoint. | "Convenience + operational continuity" answer. MSTR Engine writes CSVs into `~/.openclaw-mstr/workspace-mstr-cio/data-feed/` on cron; Cyler reads files unchanged. *Originally drafted as a Camel-served feed; redirected to MSTR Engine same day per D12.* |
| D8 | **AGENTS.md is rewritten in lockstep**, both Grok-canonical and workspace-local. | Without this, Cyler keeps reasoning from old doctrine after we ship. |
| D9 | **Backtest is a gate.** No flip to v3.2.2 enforcement until backtest passes a pre-declared bar. | Per Gavin's instruction. |
| D10 | **RAW Hybrid is a *derived* profile, not a *seeded* one.** Weights are computed at lookup time as `(Rotational + All-Weather) / 2` per (phase, sleeve). No separate rows in `ab4_benchmark`. | Keeps the midpoint definition canonical — if Rotational or All-Weather weights are tuned, RAW Hybrid auto-updates. Eliminates drift between three parallel weight tables. |
| D11 | **Tolerance bands for RAW Hybrid use the default §9.3 table unmodified.** | AB3 ruleset §9.5 currently differentiates Rotational (default) from All-Weather (slightly more generous in interpretation, default formal base). RAW Hybrid sits between, but the default table is already the formal base for both — no adjustment needed in v1. Tighten in v2 if backtest reveals asymmetry. |
| D12 | **MSTR Engine owns its TV ingest.** No dependency on Camel Engine for data plumbing. Future engines (APE, etc.) build or share separately when they need TV data; not solved at this layer in v1. | Camel is currently producing errors. Routing Cyler's data dependency through an unstable engine violates the "engines stay separated at the data layer" doctrine in CLAUDE.md. Also: Camel Phase 3 TV ingest was never built — "reuse" was always going to mean "build it, then couple to it." Same total work, more coupling. |
| ~~D13~~ | ~~Camel Engine is on a decommission track…~~ **Withdrawn 2026-05-02 (rev6).** Camel Engine stays running unmodified. This build's only operational reduction is replacing Cyler's manual GitHub-CSV upload with the MSTR-owned workspace data feed (§5.5–§5.6). Camel decommission, if it happens, is a future decision outside this build. | n/a |
| D14 | **Theme is the organizing unit; each theme maps to one named TV layout.** v1 ships **MSTR Suite** only (`MSTR Suite - Download` layout, 16 tickers). Future themes — MR Assets (`MR Assets - Download`), Visser, etc. — are scoped per layout when their tickers and indicators are confirmed. Each theme's layout has the correct indicator stack pre-applied; the agent does not manage indicators programmatically. | Mirrors how Gavin already organizes TV. Indicators-per-ticker is implicit in the layout — we don't have to maintain a separate "which indicator on which ticker" config. Adding a theme is adding one YAML block + one already-existing TV layout. |
| D15 | **Single timeframe baseline: 4H.** Single history-seed target: **March 2009** where the asset has it; **3y minimum** acceptable. Both are configurable in the theme YAML; defaults until changed. | 4H matches the natural cadence Gavin wants for SRI Engine consumption. March 2009 is the post-GFC anchor, common for regime work. 3y minimum guarantees enough bars for indicator warm-up and short-history backtest comparisons even on recent issues like STRC/STRD/STRF. |
| D16 | **`mstr.db` is the canonical warehouse for raw history.** Cyler does **not** load history from a markdown file; he reads workspace summary files (`tv_state.md`, `tv_history_index.md`) for at-a-glance state and uses a SQL helper (`tv_query.py`) for deep dives. | Putting multi-year 4H history into a markdown file would inflate Cyler's session-start to megabytes of CSV-in-markdown and bury the actual summary signal. The DB is the right shape for history; markdown is the right shape for one-page session-start context. |
| D17 | **Recurring poll runs Mon–Fri at 11:30 CT (mid-day) and 15:00 CT (end-of-day), including Bitcoin.** Weekend poll skipped even though BTC trades 24/7. | Matches Gavin's instruction. The 4H bars TV produces are calendar-aligned (00/04/08/12/16/20 UTC); the two daily polls reliably capture the most recent closed bars during US trading hours. Off-hours weekend BTC bars are picked up on Monday's poll. |

---

## 5. Build sequence

Each step is a discrete unit of work. Steps 5.1–5.4 have minimal dependencies and can run loosely in parallel; 5.5 depends on 5.4; 5.6–5.8 depend on 5.5.

### 5.1 Reconcile and fix the existing engine

- `diff` local `~/mstr-engine/scripts/sri_engine.py` against canonical Grok copy. Resolve drift in one direction.
- Add columns to `howell_phase_state`: `vt_sribi REAL, vt_signal TEXT, dbc_sribi REAL, dbc_signal TEXT`. Migration script in `scripts/migrations/`.
- Fix all `WHERE id=1` reads on `howell_phase_state` in `daily_analysis_cycle.py`, `morning_brief.py`, `pmcc_alerts.py`. Replace with latest-row-by-timestamp.
- Add unit test that the brief reads a row whose timestamp is within 24h of `now()`.

**Acceptance:** classifier output is current, complete, and read freshly by every consumer.

### 5.2 New schema for AB framework

```sql
-- Profile selection per portfolio
-- RAWHybrid (Rotational-All-Weather Hybrid) is a derived profile; weights are
-- computed at lookup time as the arithmetic midpoint of Rotational and AllWeather.
-- It is a valid selection here, but does NOT receive its own rows in ab4_benchmark.
CREATE TABLE ab_profile_selection (
  portfolio_id   TEXT PRIMARY KEY,
  profile        TEXT NOT NULL CHECK (profile IN ('Rotational', 'AllWeather', 'RAWHybrid')),
  selected_at    TEXT NOT NULL,
  selected_by    TEXT NOT NULL,
  notes          TEXT
);

-- Benchmark sleeve weights per (profile, phase).
-- Only seeded for Rotational and AllWeather. RAWHybrid is computed in code.
CREATE TABLE ab4_benchmark (
  profile        TEXT NOT NULL CHECK (profile IN ('Rotational', 'AllWeather')),
  phase          TEXT NOT NULL,
  sleeve         TEXT NOT NULL,
  sleeve_class   TEXT NOT NULL CHECK (sleeve_class IN ('standard', 'special')),
  weight_pct     REAL NOT NULL,
  PRIMARY KEY (profile, phase, sleeve)
);

-- Tolerance bands (AB3 ruleset §9.3) — seeded, tunable
CREATE TABLE ab4_tolerance_bands (
  benchmark_band       TEXT PRIMARY KEY,    -- '0', '0_to_5', '5_to_10', '10_to_20', 'over_20'
  standard_band_pct    REAL NOT NULL,
  special_band_pct     REAL NOT NULL,
  zero_residual_std    REAL,
  zero_residual_spec   REAL
);

-- Deviation log — one row per resolver run per portfolio per sleeve where status != benchmark_aligned
CREATE TABLE ab3_deviation_log (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp       TEXT NOT NULL,
  portfolio_id    TEXT NOT NULL,
  profile         TEXT NOT NULL,
  phase           TEXT NOT NULL,
  sleeve          TEXT NOT NULL,
  benchmark_pct   REAL NOT NULL,
  actual_pct      REAL NOT NULL,
  delta_pct       REAL NOT NULL,
  status          TEXT NOT NULL,   -- benchmark_aligned | within_tolerance | ab3_deviation | owner_override
  tier            TEXT,            -- A | B | C | D (null when not ab3)
  rationale_md    TEXT
);
CREATE INDEX idx_ab3_dev_pf_ts ON ab3_deviation_log (portfolio_id, timestamp);
```

Seed `ab4_tolerance_bands` directly from AB3 ruleset §9.3. Seed `ab4_benchmark` for **Rotational and AllWeather** × four phases × the standard/special sleeves listed in §9.2 — initial weights TBD by Cyler (open item §7.1). RAW Hybrid is *not* seeded here; it is computed at lookup time per D10.

**Added rev7 — TV timeseries warehouse tables (per D14–D17, used by §5.5):**

```sql
-- One row per (ticker, timeframe, bar timestamp). Idempotent upsert keyed on PK.
-- `theme` denormalized for easy filtering; not part of the natural key (the same
-- ticker can in principle belong to multiple themes — current layout matters for
-- indicators, not for OHLCV).
CREATE TABLE tv_price_bars (
  ticker        TEXT NOT NULL,
  timeframe     TEXT NOT NULL,            -- '4H' for v1
  ts            TEXT NOT NULL,            -- ISO8601 UTC, bar OPEN time
  open          REAL NOT NULL,
  high          REAL NOT NULL,
  low           REAL NOT NULL,
  close         REAL NOT NULL,
  volume        REAL,                     -- nullable for ratio/index series
  theme         TEXT NOT NULL,            -- 'mstr_suite' for v1
  ingested_at   TEXT NOT NULL,
  PRIMARY KEY (ticker, timeframe, ts)
);
CREATE INDEX idx_tv_bars_theme_ts ON tv_price_bars (theme, ts);

-- Long-format indicator values. Each (ticker, timeframe, ts, indicator_id, value_key)
-- holds one numeric reading. Long-format keeps schema flexible across studies that
-- emit varying value keys (oscillators with multiple plots, multi-line indicators, etc.).
CREATE TABLE tv_indicator_values (
  ticker        TEXT NOT NULL,
  timeframe     TEXT NOT NULL,
  ts            TEXT NOT NULL,
  indicator_id  TEXT NOT NULL,            -- normalized study id, e.g. 'sri_bias'
  value_key     TEXT NOT NULL,            -- 'bias', 'oscillator', 'signal', etc.
  value_num     REAL,                     -- nullable when study returned non-numeric / no signal
  value_text    TEXT,                     -- only used for state/signal indicators that return strings
  theme         TEXT NOT NULL,
  ingested_at   TEXT NOT NULL,
  PRIMARY KEY (ticker, timeframe, ts, indicator_id, value_key)
);
CREATE INDEX idx_tv_ind_ind_ts ON tv_indicator_values (indicator_id, ts);
CREATE INDEX idx_tv_ind_theme_ts ON tv_indicator_values (theme, ts);

-- One row per recurring-poll run. Used for the smoke-test deltas and for the
-- workspace-summary generator to know "when did we last successfully ingest."
CREATE TABLE tv_ingest_runs (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  run_kind      TEXT NOT NULL CHECK (run_kind IN ('seed', 'poll')),
  theme         TEXT NOT NULL,
  started_at    TEXT NOT NULL,
  finished_at   TEXT,
  tickers_ok    INTEGER DEFAULT 0,
  tickers_fail  INTEGER DEFAULT 0,
  bars_written  INTEGER DEFAULT 0,
  values_written INTEGER DEFAULT 0,
  notes         TEXT
);
CREATE INDEX idx_tv_runs_theme_started ON tv_ingest_runs (theme, started_at);
```

The PRIMARY KEYs make `INSERT … ON CONFLICT DO UPDATE` (SQLite UPSERT) idempotent — re-running a poll for a candle that's already in the warehouse just refreshes `ingested_at` plus any value that changed mid-bar (TV occasionally restates the most recent unclosed bar). The most recent bar's row is intentionally allowed to update; older rows should never change in practice but the same UPSERT path handles both.

### 5.3 New module: `ab_profile_resolver.py`

Path: `~/mstr-engine/scripts/ab_profile_resolver.py`. Single responsibility: given (portfolio_id, latest Howell phase, actual portfolio marks), produce one row per sleeve in `ab3_deviation_log` plus a structured PPR payload matching AB3 ruleset §13 step 5.

Algorithm:
1. Look up `profile = ab_profile_selection[portfolio_id]`.
2. **Resolve benchmark weights for each sleeve:**
   - If `profile in ('Rotational', 'AllWeather')`: direct lookup in `ab4_benchmark[(profile, phase, sleeve)]`.
   - If `profile == 'RAWHybrid'`: lookup both `ab4_benchmark[('Rotational', phase, sleeve)]` and `ab4_benchmark[('AllWeather', phase, sleeve)]` and return `(rot + aw) / 2`. If either side is missing for a sleeve, treat the missing side as 0 and emit a warning to the deviation log so Cyler sees it during review.
3. Compute `actual = portfolio_aggregate` rolled up to sleeve.
4. For each sleeve: classify per AB3 ruleset §13 (benchmark-aligned / within-tolerance / AB3 / owner-override) using the tolerance band table. Tolerance bands apply uniformly across all three profiles per D11.
5. For AB3 status, classify into Tier A/B/C/D using rules from AB3 ruleset §10 (Tier definitions are *qualitative* in v1 — open item §7.2).
6. Persist to `ab3_deviation_log`. Always log the *effective* benchmark weight used (the resolved or computed value), not just the profile + phase, so the resolver run is reproducible after-the-fact.
7. Return PPR payload.

CLI: `python ab_profile_resolver.py --portfolio gavin --as-of 2026-04-30 --emit json`. Same module is callable as a Python import from `daily_analysis_cycle.py`.

### 5.4 Backtest harness: `scripts/backtest_v322.py`

Replays historical Howell phase output × historical portfolio marks × the new resolver. Outputs:
- Time series of (phase, profile, sleeve_status) per portfolio
- Histogram of how often each sleeve sits in each status (benchmark / tolerance / AB3 / override)
- Sensitivity sweep: tolerance band ±20% to find brittleness
- Phase-conditional AB3 hit rate vs forward portfolio return (uses `portfolio_marks` for ground truth on actual past portfolios; mock portfolios for hypothetical Rotational-vs-All-Weather comparisons)

**Pre-declared backtest bar (Gavin/Greg to confirm before §5.5):**
- ≥ 95% of bars classified into a single status per sleeve (i.e., the resolver doesn't flip-flop within a phase)
- Tolerance band sensitivity ≤ 30% status churn at ±20% bands (i.e., the bands aren't pathologically tight or loose)
- AB3 deviations in Turbulence are <50% as frequent as in Rebound on the mock Rotational portfolio (sanity check that phase-conditioning works)
- **RAW Hybrid sanity check:** for any (phase, sleeve), `RAWHybrid_weight ≈ (Rotational_weight + AllWeather_weight) / 2` to within 0.01 percentage points (tests the derivation is correct and stable across re-runs).

**Backtest fails → tune §5.2 seeds → re-run.** Do not ship to live until all three bars pass.

### 5.5 TV timeseries warehouse (rev7 — replaces the prior CSV-feed §5.5)

The replacement for Cyler's manual GitHub-CSV upload is **a price+indicator timeseries warehouse in `mstr.db`**, polled twice daily Mon–Fri from TradingView Desktop. v1 ships the **MSTR Suite** theme only; future themes follow the same pattern but are out of scope for this build.

#### 5.5.1 TV CLI wrapper extensions (`tv_ingest.py`)

The current `tv_ingest.py` only wraps `status / set_symbol / set_timeframe / values`. Extend it with thin functions over additional `tv` CLI commands the implementation already exposes:

- `ohlcv(symbol, timeframe, bars=N) → list[Bar]` — wraps `tv ohlcv`. Returns rows from the chart's currently-loaded view. Caller is responsible for ensuring enough history is loaded (see seed below).
- `indicator_history(symbol, timeframe, study_filter, bars=N) → list[IndicatorReading]` — wraps `tv data indicator`. Returns historical indicator values aligned to bar timestamps.
- `layout_switch(layout_name)` — wraps `tv layout switch`.
- `chart_state() → dict` — wraps `tv state`. Used to confirm symbol/timeframe took effect after `set_symbol` + `set_timeframe`.
- `scroll_back_to(symbol, timeframe, target_date)` — helper that drives the chart's history-load by combining `tv scroll` and `tv range`. Used only by the seed script. May require multiple iterations with brief sleeps between calls; TV's history paginates and the chart needs to render before bars become readable.

The **CDP attach** model from the existing `tv_ingest.py` stays — no session cookie. The earlier mention of `~/mstr-engine/.secrets/tv_session_cookie` is retired (was always wrong; rev7 corrects the doc to match the implementation).

#### 5.5.2 Theme YAML config

Path: `~/mstr-engine/config/tv_themes.yaml`. Replaces `tv_feed.yaml` (which targeted the old CSV-snapshot model and is no longer used).

```yaml
defaults:
  timeframes: ["4H"]
  history_seed_target: "2009-03-01"   # March 2009; assets without that depth fall back to as-far-back-as-they-go
  history_seed_minimum_years: 3        # below this, treat the seed as failed for that ticker

themes:
  - id: mstr_suite
    layout: "MSTR Suite - Download"
    tickers:
      - { id: MSTR,         tv_symbol: "NASDAQ:MSTR" }
      - { id: IBIT,         tv_symbol: "NASDAQ:IBIT" }
      - { id: BTCUSD,       tv_symbol: "INDEX:BTCUSD" }   # confirm against layout
      - { id: STRC,         tv_symbol: "NASDAQ:STRC" }
      - { id: STABLE_C_D,   tv_symbol: "STABLE.C.D" }     # stablecoin dominance — verbatim
      - { id: MSTR_IBIT,    tv_symbol: "NASDAQ:MSTR/NASDAQ:IBIT" }
      - { id: STRF_LQD,     tv_symbol: "NASDAQ:STRF/NASDAQ:LQD" }
      - { id: STRD_HYG,     tv_symbol: "NASDAQ:STRD/NASDAQ:HYG" }
      - { id: BTC_GOLD,     tv_symbol: "INDEX:BTCUSD/AMEX:GLD" }
      - { id: STRF,         tv_symbol: "NASDAQ:STRF" }
      - { id: STRD,         tv_symbol: "NASDAQ:STRD" }
      - { id: MSTR_SPY,     tv_symbol: "NASDAQ:MSTR/AMEX:SPY" }
      - { id: SPY,          tv_symbol: "AMEX:SPY" }
      - { id: GLD,          tv_symbol: "AMEX:GLD" }
      - { id: IWM,          tv_symbol: "AMEX:IWM" }
      - { id: DXY,          tv_symbol: "TVC:DXY" }

  # MR Assets, Visser, etc. — out of scope for v1 (see §9). Add as separate theme blocks
  # once their layouts and ticker scopes are confirmed.

poll_schedule:
  # Two daily polls Mon–Fri; including BTC. Times in America/Chicago for clarity;
  # plist actually runs in machine-local PT.
  cdt_poll_times: ["11:30", "15:00"]

smoke_test:
  bars_per_run_min: 1                   # at minimum, the just-closed 4H bar
  bars_per_run_max: 6                   # if a poll catches up after a missed run
  alert_webhook_env: DISCORD_WEBHOOK_ALERTS
```

#### 5.5.3 One-time history seed: `~/mstr-engine/scripts/tv_seed.py`

Backfills `tv_price_bars` and `tv_indicator_values` for every (ticker, timeframe) in the chosen theme(s), back to the configured `history_seed_target` or as far as TV provides.

CLI: `python tv_seed.py --theme mstr_suite [--ticker MSTR] [--dry-run]`. `--ticker` is a single-ticker mode useful for re-seeding one symbol after fixing config. `--dry-run` exercises the seed loop without writing to `mstr.db`.

Sequence per ticker:

1. `layout_switch` to the theme's layout (once at start).
2. `set_symbol` + `set_timeframe`.
3. `scroll_back_to(target_date)` — drives the chart to load history. Iterate `tv scroll` + a short sleep until the leftmost loaded bar is at-or-before the target, or until `tv ohlcv` reports no further history (TV's natural left edge).
4. Read `ohlcv` page-by-page; UPSERT into `tv_price_bars`.
5. Read `indicator_history` for every study in the data window (one pass per study, all bars of the loaded range); UPSERT into `tv_indicator_values`.
6. Append a row to `tv_ingest_runs` with `run_kind='seed'` and counts.

**Acceptance for the seed:** for each ticker, either (a) the warehouse holds a continuous bar history from the configured target through the most recent closed 4H bar, or (b) the warehouse holds the maximum available history from TV and the gap from `history_seed_minimum_years` is logged as a known-short ticker (e.g. STRC/STRD/STRF). No partial seeds: a ticker either makes the bar or is logged as an exception.

#### 5.5.4 Recurring twice-daily poller: `~/mstr-engine/scripts/tv_poll.py`

The forward-going equivalent of `tv_seed.py`, run by the LaunchAgent. Same pipeline, but for each ticker reads only the last N bars (default 6 — enough to recover from one missed poll) and UPSERTs them. The PRIMARY KEYs on `tv_price_bars` and `tv_indicator_values` make this idempotent.

Pipeline sketch (per run):

1. `layout_switch` to `MSTR Suite - Download`.
2. For each ticker in the theme:
   - `set_symbol` + `set_timeframe`.
   - `ohlcv(bars=6)` → UPSERT.
   - `indicator_history(bars=6)` → UPSERT for every study in the data window.
3. Append a `tv_ingest_runs` row.
4. Trigger the workspace summary generator (§5.5.5).
5. Smoke test: if `bars_written` for a ticker is 0 across 2 consecutive runs (and the day is a normal trading day), post to the alerts webhook.

**Replaces the existing `tv_feed_writer.py`.** That file was scoped to the CSV-snapshot model; rev7 retires it.

#### 5.5.5 Workspace summary generator: `~/mstr-engine/scripts/tv_state_writer.py`

Runs at the end of every poll. Writes two files into the workspace `mstr-knowledge/` dir:

- **`tv_state.md`** — one-page table per theme showing, per ticker: latest bar (ts, close, % vs prior close), latest indicator readings (one row per indicator with its primary value key), data freshness ("last bar age" relative to expected). Cyler loads this at session-start for "what's the world look like right now."
- **`tv_history_index.md`** — listing of which tickers have how much history in the warehouse (earliest bar, bar count) and a short snippet showing how to query `tv_query.py` for deeper history.

Both files are derived; never hand-edited.

#### 5.5.6 SQL helper: `~/mstr-engine/scripts/tv_query.py`

Thin wrapper for ad-hoc deep-dives. Cyler invokes it when he needs more than the latest values.

CLI: `python tv_query.py --ticker MSTR [--from 2024-01-01] [--to 2024-12-31] [--include-indicators] [--emit table|json|csv]`. Default emits a markdown table (LLM-friendly).

#### 5.5.7 LaunchAgent

Replace the existing `com.mstr.tv-feed.plist` (single daily run at 08:00 PT, scoped to the CSV writer) with a new plist running `tv_poll.py` twice daily Mon–Fri:

- 09:30 PT (= 11:30 CT)
- 13:00 PT (= 15:00 CT)

Use `StartCalendarInterval` with an array of two dicts. Restrict to weekdays via `Weekday` keys (1–5).

The seed (`tv_seed.py`) is **not** scheduled — it's a one-time manual run before the poller goes live. Subsequent re-seeds (e.g., after schema changes) are also manual.

#### 5.5.8 Acceptance bars (rev7 §5.5 ship gate)

- **Bar 1 — seed completeness:** every MSTR Suite ticker has either (a) bars from `history_seed_target` to within one 4H bar of "now," or (b) a logged short-history exception with a documented earliest bar.
- **Bar 2 — recurring idempotency:** running `tv_poll.py` twice in succession produces zero net new rows on the second call.
- **Bar 3 — poll coverage:** after 7 consecutive trading days, every ticker shows at least 1 new bar from each daily poll on each day, with no missed runs.
- **Bar 4 — Cyler readability:** Cyler-as-an-LLM-agent can correctly answer "what was MSTR's last 4H close?" from `tv_state.md` alone, and "what was MSTR's close on 2024-06-01?" from `tv_query.py` alone, without needing other context.

### 5.6 P-TVI retirement

Once §5.5 has soaked — i.e., **all four §5.5.8 acceptance bars pass and 7 consecutive trading days of clean polls land in the warehouse** — decommission the broken P-TVI pipeline (broken since 2026-04-08 per `project_ptvi_chart_access.md`):

- Remove its cron entry.
- Archive its scripts under `~/Archive/p-tvi-retired-YYYY-MM-DD/`.
- Note in `lessons_workspace_architecture.md` that P-TVI was retired, replaced by the MSTR Engine TV warehouse.

### 5.7 AGENTS.md rewrite (lockstep)

Two files, kept in sync:
- `~/.openclaw-mstr/workspace-mstr-cio/AGENTS.md` (workspace-local, what Cyler actually loads)
- `~/.openclaw-mstr/workspace-mstr-cio/Grok/AGENTS.md` (canonical, pushed to GitHub)

Changes:
- **Strategy Library:** rewrite AB3 from "Structural Accumulation via LEAPs" to "Controlled deviation layer atop AB4 benchmark, classified per AB3 ruleset v1."
- **Capital Deployment Ruleset:** replace 50/25/25/0 baseline with profile-conditional benchmark + tolerance + deviation model.
- **Cross-references** to `briefs/p-ab3-ruleset-v1.md`, `briefs/howell-phase-allocation-tutorial-v1.md`, and the v3.2.2 tutorial.
- **Remove** the ByteRover paragraph (ByteRover removed from OpenClaw 2026-04-15).
- **Add** `mstr-knowledge/ab_profile.md` to the session-start load list — this file states the active portfolio's selected profile.
- **Add** `mstr-knowledge/tv_state.md` and `mstr-knowledge/tv_history_index.md` to the session-start load list (rev7) — current per-ticker bar + indicator state, plus history-index pointer to `tv_query.py`.
- **Update** the Real-Time Data Protocol to describe the warehouse model (rev7): raw history lives in `mstr.db` tables (`tv_price_bars`, `tv_indicator_values`); session-start summary lives in `tv_state.md`; deep history queries go through `tv_query.py`. This replaces the GitHub-CSV upload pattern, the prior `data-feed/` CSV-snapshot dir, and any reference to a Camel-served feed.

### 5.8 Cyler workspace knowledge files

Net-new under `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/`:
- `ab_profile.md` — declares the active AB4 profile per portfolio (mirrored from `ab_profile_selection` table).
- `phase_state.md` — auto-generated daily from `howell_phase_state`. Latest phase, confidence, sector signals. **Stays scoped to phase summary in rev7** — does NOT dump TV history.
- `ppr_template.md` — the PPR output template referenced in AB3 ruleset §13 step 5.
- **`tv_state.md` (rev7)** — auto-generated by `tv_state_writer.py` at the end of every TV poll. Per-theme table of latest 4H bar + latest indicator readings per ticker, plus data-freshness annotation.
- **`tv_history_index.md` (rev7)** — auto-generated alongside `tv_state.md`. Lists each ticker's earliest bar in the warehouse + bar count, plus a copy-paste `tv_query.py` snippet for fetching history.

`active-tasks.md` updated to show v3.2.2 build complete and to drop the stale 2026-03-15 sprint entries that no longer apply.

### 5.9 Camel Engine decommission — **DESCOPED 2026-05-02 (rev6)**

Per Gavin: this build only needs to deliver the MSTR-side functionality required to retire the manual GitHub-CSV process — **not** to actually decommission Camel Engine. The functional replacement for the manual CSV upload is §5.5 (MSTR TV ingest writes to `~/.openclaw-mstr/workspace-mstr-cio/data-feed/`) plus §5.6 (P-TVI retirement once §5.5 has soaked one week). Both remain in scope and unchanged.

What is **out of scope** as of rev6:

- Pine port of Camel cycle indicators (DCL/WCL/YCL) into Gavin's TradingView account.
- `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/cycle_state.md` (would have been populated from the Pine port).
- `~/mstr-engine/docs/camel-decom-pine-fidelity-audit.md` (gate B output — gate withdrawn).
- 2-week parallel soak comparing Camel vs Pine outputs.
- Sequential disable of the 9 `com.camel.*` LaunchAgents.
- Archive of `~/camel-engine/` codebase, `camel.db`, `~/camel-engine/.secrets/`, and the LaunchAgent plists.
- CLAUDE.md rewrite from "three engines" to "two engines + MSTR-owned cycle indicators."
- rclone backup filter changes for `~/camel-engine/`.
- Memory updates to `project_camel_engine.md` and `project_sri_engine_integration_topology.md` related to a Camel-as-output reframing.

Camel Engine continues running unmodified. Its LaunchAgents stay loaded, its cron-equivalents stay live, its Discord webhooks stay subscribed, its SQLCipher DB and vault stay in rotation. If a future decision revives the decommission, this section is the starting point — but it is no longer part of v3.2.2 ship.

**Out-of-scope for v1 of this build (carried over):** the AI Portfolio Engine equivalent of this question (does APE eventually need its own TV ingest, and if so, do we extract a shared library between MSTR and APE?). Punt to a future doc.

---

## 6. Effort estimate

### Units key (added rev3)

Earlier revisions of this doc reported a single fuzzy "days" column that conflated Archie's execution time on this machine with calendar time including human review. That was a sloppy unit. This revision splits it.

- **Archie execution time** — wall-clock time *I* (the Claude Code agent on the Mac Studio) need to do the work, assuming Gavin or Greg are reachable for go/no-go decisions but not co-authoring. Mostly tool-execution time + my own thinking. Numbers are honest best-guesses; padded for unknowns where I haven't yet validated environment behaviour (e.g., TV cookie auth flow against Gavin's account).
- **Calendar time** — realistic elapsed time accounting for normal review-feedback loops with Gavin / Greg / Cyler, time waiting for sign-offs, and parallel work. This is what to plan around.
- **Numbers diverge** by 2–6× on most rows. That divergence is *normal*, not waste — the calendar column reflects deliberate human-in-the-loop checkpoints, not idle time.

### Estimate

| Step | Archie execution | Calendar (with review loop) |
|---|---|---|
| 5.1 reconcile + fix bugs | ~1.5 hours | **DONE** (rev5) |
| 5.2 AB schema | ~45 min | **DONE** (rev5) |
| 5.2 TV warehouse schema additions (rev7) | ~1 hour | 0.5 day |
| 5.3 resolver module | ~3 hours | **DONE** (rev5) |
| 5.4 backtest harness | ~4–6 hours | **DONE** (rev5; bar 3 deferred on single-phase history) |
| 5.5.1 tv_ingest.py CLI extensions | ~2 hours | 0.5 day |
| 5.5.2 theme YAML config | ~1 hour | 0.5 day (Gavin confirms ratio + STABLE.C.D symbols against the live layout) |
| 5.5.3 tv_seed.py + first MSTR Suite seed run | ~6–10 hours exec; seed itself runs ~1–3 hours wall time per ticker on deep history | 2–3 days (one ticker fails → diagnose → re-seed; expect 1–2 surprises across 16 tickers) |
| 5.5.4 tv_poll.py + idempotency tests | ~3 hours | 1 day |
| 5.5.5 tv_state_writer.py | ~2 hours | 0.5 day |
| 5.5.6 tv_query.py | ~1.5 hours | 0.5 day |
| 5.5.7 LaunchAgent (twice-daily Mon–Fri) | ~30 min | 0.25 day |
| 5.5.8 7-day soak | — (passive) | **7 trading days** of wall clock |
| 5.6 P-TVI retirement | ~30 min | 0.25 day after soak |
| 5.7 AGENTS.md rewrite | ~2 hours partial | partial done (workspace), pending lockstep mirror to `Grok/AGENTS.md` (~1 hour) — and rev7 additions of `tv_state.md` / `tv_history_index.md` to load list |
| 5.8 workspace knowledge files (incl. rev7 additions) | ~1 hour | 0.5 day |
| 5.9 Camel decommission | — | **DESCOPED rev6** — not in this build. |
| **Total — remaining work after rev5/rev6** | **~22–28 hours of Archie execution** | **~9 calendar days + 7-day trading soak** |
| **Total — original primary track (§5.1–§5.4 done)** | (already shipped) | (already shipped) |

### Compression levers

- The seed run (5.5.3) is the dominant calendar item beyond the 7-day soak. If TV's history loads quickly across all 16 MSTR Suite tickers, this collapses to 1 day. If multiple tickers need re-seed cycles (history holes, indicator value-key mismatches, ratio-chart edge cases), it can stretch.
- 5.5.4 can run in parallel with 5.5.5 / 5.5.6 since they're independent modules sharing only the schema.
- The biggest variable I can't model from here is **how often Gavin's at the keyboard.** If you're reviewing in real time as I work, calendar shrinks toward Archie-execution time. If you're checking in once a day, it stretches toward the calendar column. The doc's calendar numbers assume the once-a-day pattern.

---

## 7. Open items requiring Cyler / Gavin / Greg input

These are cited per Gavin's instruction (2026-04-30) — ship the design doc with the gaps explicit, resolve in parallel.

### 7.1 Initial AB4 benchmark weights (Rotational × phase × sleeve, AllWeather × phase × sleeve)

The AB3 ruleset §9.2 lists sleeves but doesn't give weights. Cyler's Howell tutorial gives the framework but not the table. **Cyler needs to author the seed weights for Rotational and All-Weather across all four phases** — RAW Hybrid is computed from these two per D10, so it does not need its own seed table. This is the input that makes the resolver run. Without it, backtest is blocked.

**Owner:** Cyler. **Required by:** §5.4 start.

### 7.2 AB3 Tier A/B/C thresholds (exact percentages)

AB3 ruleset §10 defines tiers qualitatively. §17 lists "exact AB3 tier thresholds by percentage and by sleeve type" as open. v1 will encode tiers using a placeholder ladder; backtest output will help calibrate.

**Owner:** Cyler + Gavin. **Required by:** §5.4 mid.

### 7.3 LEAP technical timing requirement

AB3 ruleset §17 lists "technical timing requirements for LEAP approval" as open. Without this, the resolver can classify LEAP positions as AB3 but cannot opine on whether the *timing* of a new LEAP entry meets the bar. Recommend deferring to v2 of the resolver.

**Owner:** Cyler. **Required by:** v2, not v1.

### 7.4 ~~Camel decommission gates~~ — **CLOSED 2026-05-02 (rev6)**

Per Gavin's descope, Camel decommission is no longer in scope. Both gates (Greg sign-off; Pine fidelity audit) are retired. Camel Engine remains a running engine.

### 7.5 AB3 ruleset needs a §8.3 for RAW Hybrid

AB3 ruleset v1 has §8.1 (AB3 logic if benchmark = Rotational) and §8.2 (AB3 logic if benchmark = All-Weather). It does not yet have a §8.3 for RAW Hybrid. The resolver in v1 will use the default tolerance table for RAW Hybrid per D11; what is missing is the *qualitative* doctrine on whether RAW Hybrid AB3 deviations should be judged closer to Rotational's high-bar stance or All-Weather's "more conceptual room" stance.

**Owner:** Cyler. **Required by:** v2 of AB3 ruleset, not v1 of resolver. v1 resolver works without it; the doctrine fills in over time.

### 7.7 (rev7) Non-MSTR-Suite themes — ticker lists + layouts

v1 ships only the **MSTR Suite** theme. The follow-on themes need confirmed inputs before we add them:

- **MR Assets** — layout name confirmed as `MR Assets - Download`. Ticker scope **TBD by Gavin.** Best-guess starting point: the 10 Howell sectors (XLK XLY XLF XLE XLP TLT GLD IWM VT DBC) + macro names (SPX/NDX/VIX/DXY/TNX) — but do not encode without confirmation.
- **Visser** — layout does not yet exist. Out of scope until Gavin authors the layout in TV and provides the ticker scope.
- **Future themes** — same pattern (one TV layout per theme; ticker list per theme; everything else inherited from `defaults`).

**Owner:** Gavin (ticker lists, layout creation). **Required by:** when each theme is requested for build. Each is a low-coupling addition — one YAML block, one seed run, no schema changes.

### 7.6 Howell signal inputs not yet verified in `mstr.db`

The Howell brief references inputs whose presence I have not yet verified end-to-end:
- GLI cycle index (Howell's primary)
- GEGI (Global Excess Growth Indicator)
- USD-cycle proxy
- BTC on-chain liquidity proxy

`gli_engine.py` and `collect_gli_proxy.py` exist in Grok root, suggesting GLI is partially wired. Verification pass needed before §5.4 backtest can use them.

**Owner:** Archie. **Required by:** §5.4 start. (Will be resolved during step §5.1 audit work.)

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| Cyler ships a brief from old doctrine while the build is in flight | Communicate freeze on AB3 doctrine reasoning until 5.7 ships. Cyler reads from briefs; if the briefs are right, the reasoning is right. |
| Backtest fails the §5.4 bar | That's the bar working. Tune §5.2 seeds, re-run. Do not ship around the bar. |
| MSTR Engine TV ingest takes longer than 2.5 days | §5.5 slips. Manual GitHub-CSV continues to work as fallback for the duration. No critical path break. |
| Schema changes to `howell_phase_state` break existing readers | ADD COLUMN is backward-compatible; existing readers don't touch the new columns. |
| Engine-file drift turns out to mean local has divergent fixes that need preservation | §5.1 starts with a real diff, not an overwrite. |
| TV session cookie auth proves brittle (account lockout, frequent breakage) | Mitigation already planned in §5.5 (monthly rotation, smoke test). Manual GitHub-CSV upload remains a fallback throughout the §5.5 1-week soak. |

---

## 9. Out of scope (explicit)

- Chart-reading / visual chart access for Cyler — deferred per Gavin's 2026-04-30 instruction.
- Pine indicator port to Python (SRI Bias Oscillator, Stage & Reversal, STH MVRV Replica) — separate work-stream.
- AB1 / AB2 logic changes — both keep their current definitions in v3.2.2; this build does not touch them.
- APE → SRI Layer 0.75 ingest contract — separate work-stream (per session memory `project_sri_engine_integration_topology.md`).
- Renaming MSTR Engine to SRI Engine across paths/configs — deferred per session memory `project_sri_engine_rename.md`.
- Personal-portfolio data appearing in Grok — strict GitHub privacy rule remains in force.
- Extracting a shared TV-ingest library between MSTR Engine and AI Portfolio Engine — deferred. APE doesn't currently need TV data; if it does later, that's a future refactor decision, not a v1 question.
- **Camel Engine decommission** — descoped 2026-05-02 (rev6). This build delivers the MSTR-side functionality that retires the manual CSV upload, but it does **not** decommission Camel. Camel keeps running unmodified. See §5.9 for what was removed from scope.
- **MR Assets, Visser, and any other non-MSTR-Suite themes** — out of scope for v1 of rev7 (2026-05-02). The architecture (theme YAML + named TV layout + uniform schema) supports them as additive blocks, but no theme other than MSTR Suite ships in this build. See §7.7.
- **Multiple timeframes** — single 4H baseline only in rev7. Adding 1D / 1W is a future config change, not v1 work.
- **Indicator-as-Pine-port-to-Python work** — already out of scope above; reaffirmed: the warehouse stores whatever TV emits in the data window. Computing indicators in MSTR Engine code is not in this build.

---

## 10. Sign-off

| Owner | Role | Decision needed | Status |
|---|---|---|---|
| Gavin | Trading systems owner | (rev4) Approve sequence + §5.4 acceptance bars. (rev6) Descope §5.9 Camel decommission; build only the MSTR-side CSV-replacement functionality. | ☒ **rev4 2026-05-01 / rev6 2026-05-02** |
| Greg | (transferred) | Ownership of trading systems transferred to Gavin 2026-05-01; sign-off no longer required. Camel decommission descoped rev6, so the prior "courtesy heads-up before destructive steps" note is also retired. | n/a |
| Cyler | CIO doctrine author | Author AB4 benchmark weights (open item §7.1) and Tier thresholds (§7.2) | ☒ **2026-05-01** (`p-sri-v322-cyler-inputs-v1.md`) |

**Status note (2026-05-01, end of day):** §5.1–§5.4 complete and verified.

- **§5.1** — sri_engine.py drift resolved, VT/DBC columns added, stale `id=1` reads removed, Howell rows fresh.
- **§5.2** — `ab_profile_selection` (5 portfolios, all RAWHybrid), `ab4_benchmark` (128 rows, Cyler §7.1), `ab4_tolerance_bands` (5 rows, §9.3), `ab3_deviation_log` indexed. Two unplanned additions to support §5.3: `ab3_tier_thresholds` (Cyler §7.2 ladder, A/B/C/D × standard/special) and `sleeve_map` (Cyler sleeve-map-v1, 59 rows covering all 16 sleeves).
- **§5.3** — `~/mstr-engine/scripts/ab_profile_resolver.py` shipped. Resolves Rotational/AllWeather/RAWHybrid; rolls up positions through `sleeve_map`; logs + drops unmapped or missing-data positions; persists to `ab3_deviation_log`. CLI: `--portfolio --as-of --emit json|table --dry-run`. Tested live against `greg`.
- **§5.4** — `~/mstr-engine/scripts/backtest_v322.py` shipped. 17,520 sleeve-bars across 73 phase rows × 5 portfolios × 3 profiles. Acceptance bars: bar 1 PASS (240/240 groups consistent), bar 2 PASS (2.08% churn at ±20% bands), bar 3 SKIP (single-phase history — all rows Turbulence), bar 4 PASS (RAW Hybrid math exact across all 64 (phase, sleeve) checks). Reports written to `~/mstr-engine/data/backtests/`.
- **Position-data gap surfaced during §5.3** — Greg's options/spread rows (id=2, 3, 4, 5, 6) have NULL notional/delta and id=2/3 are past expiry. Cyler authored a reconciliation artifact (`briefs/p-sri-v322-positions-reconcile-greg-v1.md`) with explicit BROKER INPUT REQUIRED markers. SQL not yet applied; pending broker data from Gavin. The §5.4 backtest was run shares-only per Gavin's 2026-05-01 instruction (infrastructure validation, not strategy validation).
- **§5.5–§5.8** — TV ingest scaffolding staged for the **prior** CSV-snapshot model (scripts + plist + runbook present). Per **rev7 (2026-05-02)** the model changed to a timeseries warehouse — the existing `tv_feed_writer.py` and `tv_feed.yaml.example` are retired; `tv_ingest.py` is extended (not replaced). New scripts to build: `tv_seed.py`, `tv_poll.py`, `tv_state_writer.py`, `tv_query.py`. New config: `tv_themes.yaml`. New plist schedule: twice daily Mon–Fri (replaces the daily-08:00-PT plist). P-TVI retire pending §5.5 7-day soak post-cutover. Workspace AGENTS.md rewritten 2026-05-01; canonical `Grok/AGENTS.md` mirror still pre-rewrite (D8 lockstep open) and now also needs rev7 additions for `tv_state.md` / `tv_history_index.md`. Existing workspace knowledge files (`ab_profile.md`, `phase_state.md`, `ppr_template.md`) present; rev7 adds two new ones (`tv_state.md`, `tv_history_index.md`).
- **§5.9 Camel decommission — DESCOPED rev6 (2026-05-02).** Removed from this build. Camel Engine continues running unmodified.

---

## Appendix A — File-level deltas planned by this build

```
PRIMARY TRACK — combined view through rev7

NEW (rev1–rev6, already shipped):
  ~/mstr-engine/scripts/ab_profile_resolver.py                 (rev5 — shipped)
  ~/mstr-engine/scripts/backtest_v322.py                       (rev5 — shipped)
  ~/mstr-engine/scripts/tv_ingest.py                           (rev5 — shipped, kept and extended in rev7)
  ~/mstr-engine/scripts/migrations/2026-04-30_ab_framework_v322.sql   (rev5 — applied)
  ~/mstr-engine/scripts/migrations/2026-04-30_howell_vtdbc_columns.sql (rev5 — applied)
  ~/mstr-engine/scripts/migrations/2026-05-01_tier_ladder_fix_and_sleeve_map.sql (rev5 — applied)
  ~/mstr-engine/docs/tv-ingest-runbook.md                      (rev5 — needs rev7 rewrite per CDP / no cookie)
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/ab_profile.md       (rev5)
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/phase_state.md      (rev5)
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/ppr_template.md     (rev5)

NEW (rev7 — to be built):
  ~/mstr-engine/scripts/tv_seed.py                             (one-time backfill)
  ~/mstr-engine/scripts/tv_poll.py                             (twice-daily poller, replaces tv_feed_writer.py)
  ~/mstr-engine/scripts/tv_state_writer.py                     (workspace summary generator)
  ~/mstr-engine/scripts/tv_query.py                            (Cyler's history helper)
  ~/mstr-engine/config/tv_themes.yaml                          (replaces tv_feed.yaml.example)
  ~/mstr-engine/scripts/migrations/2026-05-02_tv_warehouse.sql (tv_price_bars, tv_indicator_values, tv_ingest_runs)
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_state.md         (auto-generated)
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/tv_history_index.md (auto-generated)

MODIFIED:
  ~/mstr-engine/scripts/sri_engine.py                          (rev5 — reconcile drift, done)
  ~/mstr-engine/scripts/daily_analysis_cycle.py                (rev5 — latest-row reads, done)
  ~/mstr-engine/scripts/morning_brief.py                       (rev5 — latest-row reads, done)
  ~/mstr-engine/scripts/pmcc_alerts.py                         (rev5 — latest-row reads, done)
  ~/mstr-engine/scripts/tv_ingest.py                           (rev7 — add ohlcv/indicator_history/layout_switch/scroll_back_to)
  ~/Library/LaunchAgents/com.mstr.tv-feed.plist                (rev7 — schedule changes from daily 08:00 PT to twice-daily Mon–Fri 09:30 + 13:00 PT; ProgramArguments points to tv_poll.py)
  ~/.openclaw-mstr/workspace-mstr-cio/AGENTS.md                (workspace doctrine rewrite, partial done — rev7 adds tv_state.md/tv_history_index.md to load list)
  ~/.openclaw-mstr/workspace-mstr-cio/Grok/AGENTS.md           (canonical mirror — pending; D8 lockstep open)
  ~/.openclaw-mstr/workspace-mstr-cio/active-tasks.md          (drop 2026-03-15 sprint entries; add v3.2.2 status)
  mstr.db schema                                               (cumulative: 7 net-new tables, 4 added columns)
  crontab                                                      (no change in rev7 — TV poll runs via LaunchAgent, not cron)

RETIRED (rev7):
  ~/mstr-engine/scripts/tv_feed_writer.py                      (CSV-snapshot model — replaced by tv_poll.py; deleted)
  ~/mstr-engine/config/tv_feed.yaml.example                    (replaced by tv_themes.yaml)
  ~/mstr-engine/.secrets/tv_session_cookie                     (never created — session cookie was never the auth model; doc-only retirement)
  ~/.openclaw-mstr/workspace-mstr-cio/data-feed/               (CSV-snapshot dir — never created on disk in current state; remove from any AGENTS.md references)

ARCHIVED (after §5.5 7-day soak passes, then §5.6 fires):
  ~/Archive/p-tvi-retired-YYYY-MM-DD/                          (P-TVI scripts + last logs)


CAMEL DECOMMISSION TRACK — REMOVED rev6 (2026-05-02). See §5.9.
```

---

## Appendix B — Open questions for v2 (post-ship)

These are not blockers for v1 ship but are worth tracking:

- Should the resolver also classify AB1 (theta) and AB2 (directional conviction) deviations? Current scope is AB3 deviation classification only.
- AGENTS.md "Strategy Library v4.0 (2026-03-08)" should likely become v5.0 with this rewrite — version it.
- ByteRover removal (already done in OpenClaw runtime per memory) needs a corresponding cleanup pass on `mstr-knowledge/system-learnings.md` and any `brv` references in helper scripts.
- The `kathryn-portfolio-state.md` and `ali-portfolio-state.md` files in `mstr-knowledge/` — should those portfolios get v3.2.2 profile selections too, or are they intentionally outside this framework?

---

*End of document.*
