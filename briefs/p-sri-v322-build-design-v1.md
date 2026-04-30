# P-SRI-V3.2.2: Build Design — Howell Phasing, AB4 Profiles, AB3 Ruleset

**Project:** P-SRI-V3.2.2-BUILD
**Version:** v1 — Draft for Greg + Gavin review
**Date:** 2026-04-30 (revised same day — added RAW Hybrid profile)
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

This document defines the build that closes the gap. It assumes the existing `HowellPhaseEngine` is reused and bug-fixed; it adds new tables, modules, and a backtest harness; it migrates Cyler off manual GitHub-CSV uploads onto a Camel-Engine-fed workspace data feed; it rewrites `AGENTS.md` to match v3.2.2 doctrine.

It does **not** ship until backtest validates the classifier and the new ruleset.

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
| D7 | **Migrate Cyler off GitHub-CSV via Camel-Engine workspace feed**, not via a synchronous CE endpoint. | Yesterday's "convenience + operational continuity" answer. CE writes CSVs into `~/.openclaw-mstr/workspace-mstr-cio/data-feed/` on cron; Cyler reads files unchanged. |
| D8 | **AGENTS.md is rewritten in lockstep**, both Grok-canonical and workspace-local. | Without this, Cyler keeps reasoning from old doctrine after we ship. |
| D9 | **Backtest is a gate.** No flip to v3.2.2 enforcement until backtest passes a pre-declared bar. | Per Gavin's instruction. |
| D10 | **RAW Hybrid is a *derived* profile, not a *seeded* one.** Weights are computed at lookup time as `(Rotational + All-Weather) / 2` per (phase, sleeve). No separate rows in `ab4_benchmark`. | Keeps the midpoint definition canonical — if Rotational or All-Weather weights are tuned, RAW Hybrid auto-updates. Eliminates drift between three parallel weight tables. |
| D11 | **Tolerance bands for RAW Hybrid use the default §9.3 table unmodified.** | AB3 ruleset §9.5 currently differentiates Rotational (default) from All-Weather (slightly more generous in interpretation, default formal base). RAW Hybrid sits between, but the default table is already the formal base for both — no adjustment needed in v1. Tighten in v2 if backtest reveals asymmetry. |

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

### 5.5 Camel Engine → workspace data feed

Per yesterday's decision: CE writes CSVs into `~/.openclaw-mstr/workspace-mstr-cio/data-feed/` on a daily cron. Filenames mirror the existing TradingView export pattern (`BATS_<ticker>, <interval>_<hash>.csv`) so Cyler's read paths don't change.

- New CE LaunchAgent: `com.camel.tv-feed-mstr.plist`. Daily 08:00 PT (after market open + Pine indicator settle).
- CE's TV ingest service (Camel Phase 3) provides the data; the workspace-feed writer is a thin shim.
- Daily smoke test: count files written, post to `system_log` Discord webhook on miss.
- After 1 week of clean parallel runs (CE feed + manual upload both populating workspace), retire the manual upload + the cron entry that pulls Grok into the workspace.

### 5.6 P-TVI retirement

Once §5.5 has soaked, decommission the broken P-TVI pipeline (broken since 2026-04-08 per `project_ptvi_chart_access.md`):
- Remove its cron entry.
- Archive its scripts under `~/Archive/p-tvi-retired-YYYY-MM-DD/`.
- Note in `lessons_workspace_architecture.md` that P-TVI was retired, replaced by CE feed.

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
- **Update** the Real-Time Data Protocol to reference the new CE workspace feed path.

### 5.8 Cyler workspace knowledge files

Net-new under `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/`:
- `ab_profile.md` — declares the active AB4 profile per portfolio (mirrored from `ab_profile_selection` table).
- `phase_state.md` — auto-generated daily from `howell_phase_state`. Latest phase, confidence, sector signals.
- `ppr_template.md` — the PPR output template referenced in AB3 ruleset §13 step 5.

`active-tasks.md` updated to show v3.2.2 build complete and to drop the stale 2026-03-15 sprint entries that no longer apply.

---

## 6. Effort estimate

| Step | Type | Estimate |
|---|---|---|
| 5.1 reconcile + fix bugs | Code + migration | 0.5 day |
| 5.2 schema | SQL + seed | 0.5 day |
| 5.3 resolver module | Python | 1.5 days |
| 5.4 backtest harness | Python + analysis | 2 days |
| 5.5 CE → workspace feed | Camel Engine work | 1 day (assumes Camel Phase 3 TV ingest already shipped — open item §7.4) |
| 5.6 P-TVI retirement | Cron + archive | 0.5 day |
| 5.7 AGENTS.md rewrite | Doctrine | 1 day (Cyler review loop) |
| 5.8 workspace knowledge | Markdown templates | 0.5 day |
| **Total** | | **~7.5 days of focused work** + backtest soak window |

This is "asap" pace, not staged-rollout pace. Steps 5.1–5.4 can compress to 3 days if backtest tooling reuses existing scaffolding in `backtest_btc_mstr_v2.py` and `backtest_indicators_v2.py`.

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

### 7.4 Camel Phase 3 TV ingest readiness

CLAUDE.md describes Camel Phase 3 (TradingView MCP) as the "next planned addition." If it's not yet shipped, §5.5 grows. Recommend Greg confirm whether the CE TV ingest exists in any form today, or whether §5.5 becomes "build CE TV ingest *and* the workspace shim."

**Owner:** Greg. **Required by:** §5.5 start.

### 7.5 AB3 ruleset needs a §8.3 for RAW Hybrid

AB3 ruleset v1 has §8.1 (AB3 logic if benchmark = Rotational) and §8.2 (AB3 logic if benchmark = All-Weather). It does not yet have a §8.3 for RAW Hybrid. The resolver in v1 will use the default tolerance table for RAW Hybrid per D11; what is missing is the *qualitative* doctrine on whether RAW Hybrid AB3 deviations should be judged closer to Rotational's high-bar stance or All-Weather's "more conceptual room" stance.

**Owner:** Cyler. **Required by:** v2 of AB3 ruleset, not v1 of resolver. v1 resolver works without it; the doctrine fills in over time.

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
| Camel Phase 3 TV ingest is more work than expected | §5.5 slips. Manual GitHub-CSV continues to work as fallback for the duration. No critical path break. |
| Schema changes to `howell_phase_state` break existing readers | ADD COLUMN is backward-compatible; existing readers don't touch the new columns. |
| Engine-file drift turns out to mean local has divergent fixes that need preservation | §5.1 starts with a real diff, not an overwrite. |

---

## 9. Out of scope (explicit)

- Chart-reading / visual chart access for Cyler — deferred per Gavin's 2026-04-30 instruction.
- Pine indicator port to Python (SRI Bias Oscillator, Stage & Reversal, STH MVRV Replica) — separate work-stream.
- AB1 / AB2 logic changes — both keep their current definitions in v3.2.2; this build does not touch them.
- APE → SRI Layer 0.75 ingest contract — separate work-stream (per session memory `project_sri_engine_integration_topology.md`).
- Renaming MSTR Engine to SRI Engine across paths/configs — deferred per session memory `project_sri_engine_rename.md`.
- Personal-portfolio data appearing in Grok — strict GitHub privacy rule remains in force.

---

## 10. Sign-off

| Owner | Role | Decision needed | Status |
|---|---|---|---|
| Gavin | MSTR Engine co-lead | Approve sequence + acceptance bars in §5.4 | ☐ |
| Greg | AI Portfolio Engine + Camel co-lead | Confirm Camel Phase 3 readiness for §5.5 (open item §7.4) | ☐ |
| Cyler | CIO doctrine author | Author AB4 benchmark weights (open item §7.1) and Tier thresholds (§7.2) | ☐ |

Once all three sign-offs are in, Archie executes §5.1 same-day.

---

## Appendix A — File-level deltas planned by this build

```
NEW:
  ~/mstr-engine/scripts/ab_profile_resolver.py
  ~/mstr-engine/scripts/backtest_v322.py
  ~/mstr-engine/scripts/migrations/2026-04-30_ab_framework_v322.sql
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/ab_profile.md
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/phase_state.md
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/ppr_template.md
  ~/Library/LaunchAgents/com.camel.tv-feed-mstr.plist
  ~/.openclaw-mstr/workspace-mstr-cio/data-feed/                (directory)

MODIFIED:
  ~/mstr-engine/scripts/sri_engine.py                          (reconcile drift only)
  ~/mstr-engine/scripts/daily_analysis_cycle.py                (latest-row reads)
  ~/mstr-engine/scripts/morning_brief.py                       (latest-row reads)
  ~/mstr-engine/scripts/pmcc_alerts.py                         (latest-row reads)
  ~/.openclaw-mstr/workspace-mstr-cio/AGENTS.md                (doctrine rewrite)
  ~/.openclaw-mstr/workspace-mstr-cio/Grok/AGENTS.md           (canonical mirror)
  ~/.openclaw-mstr/workspace-mstr-cio/active-tasks.md          (drop 2026-03-15 sprint entries; add v3.2.2 status)
  mstr.db schema                                               (4 new tables, 4 new columns)
  crontab                                                      (add CE feed; later remove P-TVI)

ARCHIVED (after §5.6 soak):
  ~/Archive/p-tvi-retired-YYYY-MM-DD/                          (P-TVI scripts + last logs)
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
