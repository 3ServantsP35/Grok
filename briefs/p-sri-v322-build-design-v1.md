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

**Operational shift baked into this build (added 2026-04-30):** TV ingest is owned by MSTR Engine, not Camel Engine. Camel's cycle indicators get rebuilt as Pine in Gavin's TradingView account and flow to Cyler through the same MSTR ingest pipeline as everything else. Camel Engine itself is on a decommission track gated on (a) Greg's explicit sign-off and (b) a Pine fidelity audit confirming DCL/WCL/YCL classification ports cleanly. Until both gates pass, Camel keeps running unmodified. See §5.9 for the decommission plan.

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
| D13 | **Camel Engine is on a decommission track.** Cycle indicators (DCL/WCL/YCL) get rebuilt as Pine in Gavin's TradingView account; their outputs flow to Cyler through MSTR Engine's TV ingest like any other indicator. Camel Engine itself — the codebase, the SQLCipher DB, the 9 LaunchAgents, the camel-engine vault remote — gets archived. **Gated on Greg sign-off and Pine fidelity audit.** See §5.9. | Honors v3.2.2's own framing that "Camel is a sourced indicator, not an architecture layer." The engine wrapper was always doing more than the methodology required. Removing it shrinks the operational surface (3 engines → 2), simplifies the Discord topology, and removes a SQLCipher DB and a vault repo from rotation. |

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

### 5.5 MSTR Engine TV ingest → workspace data feed

MSTR Engine writes CSVs into `~/.openclaw-mstr/workspace-mstr-cio/data-feed/` on a daily cron. Filenames mirror the existing TradingView export pattern (`BATS_<ticker>, <interval>_<hash>.csv`) so Cyler's read paths don't change.

- **Net-new in MSTR Engine:** `~/mstr-engine/scripts/tv_ingest.py` — wraps an unofficial TV client (`tvdatafeed`-style or community MCP). Uses Gavin's TV session cookie stored at `~/mstr-engine/.secrets/tv_session_cookie` (600 perms).
- **Workspace shim:** `~/mstr-engine/scripts/tv_feed_writer.py` — invokes `tv_ingest.py` for the canonical ticker × interval list and writes results to the data-feed dir with the BATS filename pattern.
- **New LaunchAgent:** `com.mstr.tv-feed.plist`. Daily 08:00 PT (after market open + Pine indicator settle).
- **Daily smoke test:** count files written, validate row counts within ±20% of yesterday's per-ticker counts, post to `system_log` Discord webhook on miss or anomaly.
- **Auth rotation:** monthly cookie refresh procedure documented in `~/mstr-engine/docs/tv-ingest-runbook.md`.
- **Soak window:** after 1 week of clean parallel runs (new MSTR feed + manual upload both populating workspace), retire the manual upload + the cron entry that pulls Grok into the workspace.

This step is **independent of the Camel decommission gate (§5.9).** MSTR Engine TV ingest ships regardless of whether Camel decommission is approved — the only thing the decommission decides is whether Camel keeps running its current Pine pipeline alongside, or hands over to Pine-in-Gavin's-TV-account.

### 5.6 P-TVI retirement

Once §5.5 has soaked, decommission the broken P-TVI pipeline (broken since 2026-04-08 per `project_ptvi_chart_access.md`):
- Remove its cron entry.
- Archive its scripts under `~/Archive/p-tvi-retired-YYYY-MM-DD/`.
- Note in `lessons_workspace_architecture.md` that P-TVI was retired, replaced by MSTR Engine TV feed.

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
- **Update** the Real-Time Data Protocol to reference the new MSTR Engine workspace feed path (replaces the GitHub-CSV upload pattern; replaces any reference to a Camel-served feed).

### 5.8 Cyler workspace knowledge files

Net-new under `~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/`:
- `ab_profile.md` — declares the active AB4 profile per portfolio (mirrored from `ab_profile_selection` table).
- `phase_state.md` — auto-generated daily from `howell_phase_state`. Latest phase, confidence, sector signals.
- `ppr_template.md` — the PPR output template referenced in AB3 ruleset §13 step 5.

`active-tasks.md` updated to show v3.2.2 build complete and to drop the stale 2026-03-15 sprint entries that no longer apply.

### 5.9 Camel Engine decommission (parallel track, gated)

This track runs in parallel with §5.1–§5.8 but does not block them. Nothing destructive happens until **both gates** pass:

- **Gate A — Greg's explicit sign-off.** Greg built Camel Engine. Decommissioning is his call, not Gavin's alone. Sign-off required even though Gavin and Greg are equal co-principals on this machine.
- **Gate B — Pine fidelity audit.** Archie reads `~/camel-engine/pipeline/` and confirms whether DCL/WCL/YCL classification logic ports cleanly to Pine. If something doesn't port (Python-only logic Pine cannot express), three options: accept the loss, port it to Python *inside* MSTR Engine, or keep that one piece of Camel running. Gate cleared either by green audit or by an explicit decision on a non-portable piece.

**Sequence after both gates pass:**

1. **Pine port.** Gavin recreates Camel's cycle indicators in his TradingView account. Verified outputs match `~/camel-engine/data/camel.db` historical cycle outputs to within an agreed tolerance over a 90-day window.
2. **Wire to MSTR ingest.** Pine outputs included in the canonical ticker × interval list in `tv_feed_writer.py` (§5.5).
3. **Cyler workspace doc.** Add a `cycle_state.md` file to `mstr-knowledge/` parallel to `phase_state.md`; populated daily from the new ingest. Update AGENTS.md session-start load list.
4. **Soak window.** 2 weeks of parallel running (Camel still up, new Pine pipeline running). Compare daily outputs. Discrepancy >5% on any cycle classification = stop, investigate.
5. **Camel quiet-down.** Disable LaunchAgents one at a time over a week (`com.camel.tv` → `com.camel.cross-system-signal` last). After each, verify nothing downstream broke. Discord webhooks (`cross_signals`, `system_log`, `briefing`, `alerts`, `trades`, `research` on Camel) marked deprecated; Cyler is told not to subscribe.
6. **Preservation, not deletion.**
   - `~/camel-engine/data/camel.db` — final SQLCipher snapshot to `~/Archive/camel-engine-decom-YYYY-MM-DD/data/`. Preserve key.
   - `~/camel-engine/data/backups/` — copy in the same archive.
   - `~/camel-engine/.secrets/` — copy in the same archive (preserve sqlcipher key + any TV session cookie).
   - `~/camel-engine/` codebase — final commit + tag `decommissioned-YYYY-MM-DD` on the GitHub remote, then archive locally.
   - `~/vault-cycle-trading/` — keep on disk and on GitHub indefinitely (it's methodology, not just code).
7. **LaunchAgent cleanup.** All 9 `com.camel.*` plists moved to `~/Archive/camel-engine-decom-YYYY-MM-DD/LaunchAgents/`.
8. **Crontab cleanup.** Remove any `~/camel-engine/` entries from crontab (none expected — Camel uses LaunchAgents — but verify).
9. **CLAUDE.md rewrite.** Drop the Camel Engine section. Update the "three engines" framing to "two engines + MSTR-owned cycle indicators." Update the Discord webhook topology table (rows for Camel-only channels become "[archived]"). Update the Backup section if it references `camel.db`. Update the rclone backup filters to stop covering `~/camel-engine/`.
10. **Memory updates.** Update `project_camel_engine.md` (mark superseded with archive pointer). Update `project_sri_engine_integration_topology.md` (Camel-as-engine reference becomes Camel-as-Pine-indicator-output; Layer 2 placement preserved).
11. **rclone backup filter update.** Remove `~/camel-engine/` from offsite backup, since the archive captures it once.

**Rollback path.** Until step 7 (LaunchAgent move), the decommission is fully reversible — re-enable the LaunchAgents and Camel resumes. After step 7 + a full backup cycle, rollback requires restoring from the archive bundle.

**Out-of-scope for v1 of this build:** the AI Portfolio Engine equivalent of this question (does APE eventually need its own TV ingest, and if so, do we extract a shared library between MSTR and APE?). Punt to a future doc.

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
| 5.1 reconcile + fix bugs | ~1.5 hours | 0.5 day (waits on Gavin to pick reconciliation direction) |
| 5.2 schema | ~45 min | 0.5 day (excludes Cyler authoring §7.1 weights — separately blocking) |
| 5.3 resolver module | ~3 hours | 1–1.5 days (Cyler review on edge cases + tier rules) |
| 5.4 backtest harness | ~4–6 hours pure exec; result interpretation can extend | 2–3 days (results may require seed re-tuning + re-run) |
| 5.5 MSTR TV ingest + feed | ~4 hours + open-ended cookie/2FA debugging | 1–2 days (Gavin sets cookie, validates first feed against manual upload) |
| 5.6 P-TVI retirement | ~30 min | 0.5 day after §5.5 1-week soak |
| 5.7 AGENTS.md rewrite | ~2 hours | 1–2 days (Cyler review loop) |
| 5.8 workspace knowledge | ~1 hour | 0.5 day |
| 5.9 Camel decommission (parallel, gated) | ~6–8 hours total Archie execution, spread out | **~3–4 weeks** (dominated by 2-week parallel soak in §5.9 step 4; Pine port time on Gavin separate) |
| **Total — primary track (§5.1–§5.8)** | **~22–25 hours of Archie execution** | **~9 days** + backtest soak window |
| **Total — incl. Camel decommission** | primary + ~6–8 hours | primary + 3–4 weeks parallel, mostly soak/safety windows |

### Compression levers

- Steps 5.1–5.4 can compress to ~3 calendar days if backtest tooling reuses existing scaffolding in `backtest_btc_mstr_v2.py` and `backtest_indicators_v2.py`.
- The §5.9 calendar column is conservative on purpose. If Greg sign-off is fast and the Pine port works first try, decommission can compress to ~2 weeks. The 2-week soak in step 4 is a hard floor — shortening it trades safety for speed and is not recommended.
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

### 7.4 Camel decommission gates

This open item replaces the previous "Camel Phase 3 readiness" question, which is now moot. The decommission requires:

- **(a) Greg's explicit sign-off.** Greg built Camel; the call is his. Gavin and Greg are equal co-principals on this machine in general, but the decommission of an engine one of them built specifically should be confirmed by the builder.
- **(b) Pine fidelity audit.** Archie reads `~/camel-engine/pipeline/` to confirm DCL/WCL/YCL classification logic ports cleanly to Pine. Audit produces a written report listing each piece of cycle logic and verdict (ports / lossy port / does not port). Anything that doesn't port gets a separate decision: accept loss, port to Python in MSTR Engine, or keep that piece of Camel running.

**Owners:** Greg (gate a), Archie (gate b). **Required by:** §5.9 step 1. The rest of the build (§5.1–§5.8) does not block on this; it ships either way.

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
| MSTR Engine TV ingest takes longer than 2.5 days | §5.5 slips. Manual GitHub-CSV continues to work as fallback for the duration. No critical path break. |
| Schema changes to `howell_phase_state` break existing readers | ADD COLUMN is backward-compatible; existing readers don't touch the new columns. |
| Engine-file drift turns out to mean local has divergent fixes that need preservation | §5.1 starts with a real diff, not an overwrite. |
| **Camel decommission:** Pine fidelity audit reveals cycle logic that doesn't port to Pine | §5.9 gate B fails. Either accept loss, port that piece to Python in MSTR Engine, or keep just that one Camel cron running. The audit catches this before any LaunchAgent gets disabled. |
| **Camel decommission:** something we don't know about depends on a Camel Discord webhook or signal | Soak window in §5.9 step 4 surfaces this before destructive steps. Disabling LaunchAgents one at a time in step 5 preserves rollback. |
| **Camel decommission:** TradingView session cookie auth proves brittle (account lockout, frequent breakage) | Mitigation already planned in §5.5 (monthly rotation, smoke test). Worst case: fall back to Pine alert webhooks for the most critical signals while we figure out a better auth path. |
| Greg sign-off on Camel decommission lags behind primary build | Primary build (§5.1–§5.8) ships independently. Camel keeps running unmodified. No delivery dependency. |

---

## 9. Out of scope (explicit)

- Chart-reading / visual chart access for Cyler — deferred per Gavin's 2026-04-30 instruction.
- Pine indicator port to Python (SRI Bias Oscillator, Stage & Reversal, STH MVRV Replica) — separate work-stream.
- AB1 / AB2 logic changes — both keep their current definitions in v3.2.2; this build does not touch them.
- APE → SRI Layer 0.75 ingest contract — separate work-stream (per session memory `project_sri_engine_integration_topology.md`).
- Renaming MSTR Engine to SRI Engine across paths/configs — deferred per session memory `project_sri_engine_rename.md`.
- Personal-portfolio data appearing in Grok — strict GitHub privacy rule remains in force.
- Extracting a shared TV-ingest library between MSTR Engine and AI Portfolio Engine — deferred. APE doesn't currently need TV data; if it does later, that's a future refactor decision, not a v1 question.

---

## 10. Sign-off

| Owner | Role | Decision needed | Status |
|---|---|---|---|
| Gavin | Trading systems owner | Approve sequence + §5.4 acceptance bars; approve §5.9 Camel decommission (subject to Pine fidelity audit gate B) | ☒ **2026-05-01** |
| Greg | (transferred) | Ownership of trading systems transferred to Gavin 2026-05-01; sign-off no longer required. Courtesy heads-up before §5.9 destructive steps still recommended. | n/a |
| Cyler | CIO doctrine author | Author AB4 benchmark weights (open item §7.1) and Tier thresholds (§7.2) | ☐ |

**Status note (2026-05-01, end of day):** §5.1–§5.4 complete and verified.

- **§5.1** — sri_engine.py drift resolved, VT/DBC columns added, stale `id=1` reads removed, Howell rows fresh.
- **§5.2** — `ab_profile_selection` (5 portfolios, all RAWHybrid), `ab4_benchmark` (128 rows, Cyler §7.1), `ab4_tolerance_bands` (5 rows, §9.3), `ab3_deviation_log` indexed. Two unplanned additions to support §5.3: `ab3_tier_thresholds` (Cyler §7.2 ladder, A/B/C/D × standard/special) and `sleeve_map` (Cyler sleeve-map-v1, 59 rows covering all 16 sleeves).
- **§5.3** — `~/mstr-engine/scripts/ab_profile_resolver.py` shipped. Resolves Rotational/AllWeather/RAWHybrid; rolls up positions through `sleeve_map`; logs + drops unmapped or missing-data positions; persists to `ab3_deviation_log`. CLI: `--portfolio --as-of --emit json|table --dry-run`. Tested live against `greg`.
- **§5.4** — `~/mstr-engine/scripts/backtest_v322.py` shipped. 17,520 sleeve-bars across 73 phase rows × 5 portfolios × 3 profiles. Acceptance bars: bar 1 PASS (240/240 groups consistent), bar 2 PASS (2.08% churn at ±20% bands), bar 3 SKIP (single-phase history — all rows Turbulence), bar 4 PASS (RAW Hybrid math exact across all 64 (phase, sleeve) checks). Reports written to `~/mstr-engine/data/backtests/`.
- **Position-data gap surfaced during §5.3** — Greg's options/spread rows (id=2, 3, 4, 5, 6) have NULL notional/delta and id=2/3 are past expiry. Cyler authored a reconciliation artifact (`briefs/p-sri-v322-positions-reconcile-greg-v1.md`) with explicit BROKER INPUT REQUIRED markers. SQL not yet applied; pending broker data from Gavin. The §5.4 backtest was run shares-only per Gavin's 2026-05-01 instruction (infrastructure validation, not strategy validation).
- **§5.5–§5.9** — TV ingest, P-TVI retire, AGENTS.md rewrite, workspace knowledge files, Camel decommission — all not yet started. §5.9 gating note in §10 above remains: Pine fidelity audit (gate B) is the only remaining gate; Greg sign-off (former gate A) is moot per ownership transfer.

---

## Appendix A — File-level deltas planned by this build

```
PRIMARY TRACK (§5.1–§5.8)

NEW:
  ~/mstr-engine/scripts/ab_profile_resolver.py
  ~/mstr-engine/scripts/backtest_v322.py
  ~/mstr-engine/scripts/tv_ingest.py                           (TV client wrapper)
  ~/mstr-engine/scripts/tv_feed_writer.py                      (workspace-feed shim)
  ~/mstr-engine/scripts/migrations/2026-04-30_ab_framework_v322.sql
  ~/mstr-engine/.secrets/tv_session_cookie                     (600 perms, gitignored)
  ~/mstr-engine/docs/tv-ingest-runbook.md                      (auth rotation procedure)
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/ab_profile.md
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/phase_state.md
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/ppr_template.md
  ~/Library/LaunchAgents/com.mstr.tv-feed.plist
  ~/.openclaw-mstr/workspace-mstr-cio/data-feed/               (directory)

MODIFIED:
  ~/mstr-engine/scripts/sri_engine.py                          (reconcile drift only)
  ~/mstr-engine/scripts/daily_analysis_cycle.py                (latest-row reads)
  ~/mstr-engine/scripts/morning_brief.py                       (latest-row reads)
  ~/mstr-engine/scripts/pmcc_alerts.py                         (latest-row reads)
  ~/.openclaw-mstr/workspace-mstr-cio/AGENTS.md                (doctrine rewrite)
  ~/.openclaw-mstr/workspace-mstr-cio/Grok/AGENTS.md           (canonical mirror)
  ~/.openclaw-mstr/workspace-mstr-cio/active-tasks.md          (drop 2026-03-15 sprint entries; add v3.2.2 status)
  mstr.db schema                                               (4 new tables, 4 new columns)
  crontab                                                      (add MSTR TV feed; later remove P-TVI)

ARCHIVED (after §5.6 soak):
  ~/Archive/p-tvi-retired-YYYY-MM-DD/                          (P-TVI scripts + last logs)


CAMEL DECOMMISSION TRACK (§5.9 — gated on Greg sign-off + Pine fidelity audit)

NEW:
  ~/.openclaw-mstr/workspace-mstr-cio/mstr-knowledge/cycle_state.md
  ~/mstr-engine/docs/camel-decom-pine-fidelity-audit.md        (audit report — gate B output)

MODIFIED (post-decommission):
  ~/.claude/CLAUDE.md                                          (drop Camel Engine section, update three-engines framing, update Discord topology table, update Backups section)
  ~/scripts/rclone-backup.sh + rclone-backup-filters.txt       (drop ~/camel-engine/ from offsite scope)
  ~/.claude/projects/-Users-vera/memory/project_camel_engine.md          (mark superseded, link to archive)
  ~/.claude/projects/-Users-vera/memory/project_sri_engine_integration_topology.md  (Camel-as-engine → Camel-as-Pine-output)

ARCHIVED (after §5.9 step 6):
  ~/Archive/camel-engine-decom-YYYY-MM-DD/data/                (final camel.db SQLCipher snapshot + backups/)
  ~/Archive/camel-engine-decom-YYYY-MM-DD/.secrets/            (sqlcipher key + session cookies)
  ~/Archive/camel-engine-decom-YYYY-MM-DD/LaunchAgents/        (all 9 com.camel.* plists)
  ~/Archive/camel-engine-decom-YYYY-MM-DD/codebase/            (final ~/camel-engine/ snapshot)

PRESERVED ON DISK + GITHUB (not archived):
  ~/vault-cycle-trading/                                       (methodology, kept indefinitely)
  3ServantsP35/Grok briefs/ Camel-related docs                 (kept for historical reference)
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
