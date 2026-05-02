# P-SRI-V3.2.2 — Visser Operational Spec Request (v1)

**Project:** P-SRI-V3.2.2-VISSER-OPERATIONAL  
**Date:** 2026-05-02  
**Status:** Request for Cyler — operational v2 spec for the Visser Theme  
**Author:** Archie  
**Reads from:** `briefs/p-sri-v322-visser-theme-grounding-v1.md` (Cyler, 2026-05-02)  
**Triggered by:** §11.1 of the grounding brief (`The next artifact should likely be a shorter operational brief that defines: exact section structure for the Visser Theme output, allowed statuses, sleeve-family mapping, contradiction / caution language, PPR integration points`)

---

## 1. Why this exists

The grounding brief is doctrinally complete and load-bearing. It tells me *what* Visser is, what role it plays, and what it must not do. It explicitly defers the operational layer to a follow-on artifact.

This request enumerates the **five concrete gaps** I need Cyler to fill before I can implement Visser end-to-end in the rev7 architecture. Each gap maps to a specific build decision; without resolution, that piece of the implementation is blocked or has to ship a placeholder.

I structured the request as direct questions with the build-side options I see, so Cyler can answer in his pen against a known surface.

---

## 2. Already settled (no action needed)

- **Layer placement:** Layer 0.75 advisory intelligence. Confirmed.
- **Doctrine constraint:** does NOT override Howell, AB4, AB3. Confirmed.
- **Output posture:** textual statuses, not bull/bear tags. Confirmed.
- **Six durable themes inventory** (§4 of grounding). Useful as content reference.
- **Conflict resolution order:** regime/benchmark first, deviation second, Visser third. Confirmed.

These are landed in `AGENTS.md` and mirrored to `Grok/AGENTS.md`. The Visser doctrine statement from §10 of the grounding brief is the canonical anchor.

---

## 3. Open operational questions (requested in priority order)

### Q1 — Visser-relevance filter on the APE side

**Build context:** the existing publisher (`scripts/publish_mstr_ape_digest.py` in AI Portfolio Engine) emits ALL routed items above conviction 50, no Visser-specific filter. Today's RIS items carry `frameworks: [...]` tags (e.g. "Whole Rack", "AI Drug Discovery") but no item is tagged `"Visser"` directly.

**The question:** how does the publisher know an item is Visser-relevant?

**Options I see:**
- **(a) APE adds a tag at routing time.** A new `theme: "visser"` field on each item, or `frameworks: [..., "Visser"]`. Requires a routing-side change (separate work-stream).
- **(b) Publisher implements a content classifier.** Match against the six themes from §4 of the grounding brief (physical AI bottlenecks, agentic demand, software moat compression, era compounding, ROI timing, financial-rail rebuild) using keyword / framework / source-family heuristics.
- **(c) All APE intel is implicitly Visser-flavored.** Since APE's whole canon is Greg's Visser-derived stack, every routed item is by definition Visser-relevant. No filter; the publisher just renders an aggregate Visser status from the full set.

**My recommendation if you're undecided:** option (c) for v2, because it's the simplest, matches the grounding brief's framing that APE *is* the Visser research stack, and avoids depending on a separate APE-routing change. We can move to (a) or (b) later if false positives become an issue.

---

### Q2 — Output section structure for `ape_intel.md`

**Build context:** the publisher already emits `## Visser Status` with placeholder content (status taxonomy + doctrine reminder). The grounding brief proposes five status words: `reinforcing` / `challenging-but-not-invalidating` / `timing-caution` / `concentration-caution` / `watchlist-support-only`.

**The questions:**
- **Q2a — One overall status, or per-theme statuses?** One row that says "Visser is currently `timing-caution`," or six rows (one per durable theme — physical AI bottlenecks, agentic demand, etc.) each with their own status?
- **Q2b — How is the status computed?** Counting reinforcing vs challenging items in the routed set? Rule-based mapping from the route taxonomy (THESIS_REINFORCE → reinforcing, THESIS_CHALLENGE → challenging, etc.)? Heuristic from conviction-weighted item direction?
- **Q2c — Should the section show the underlying items, or just the rolled-up status?** I lean toward both: status at top, contributing items as a small table below.

**Specifically, what I'd build with a clear answer:** a 10-line Python function that takes `items` and returns one of the five status strings (or a dict of theme→status if per-theme), plus a renderer that formats the section. Either shape is ~30 min of work; I just need the rule.

---

### Q3 — Sleeve-family mapping

**Build context:** §7 of the grounding brief lists Visser-relevant sleeve families ("AI infrastructure / power / thermal / industrial enablers", "compute / accelerator / fabrication chokepoints", etc.). The existing `sleeve_map` table in `mstr.db` has 59 rows mapping concrete `(asset, instrument_type) → sleeve` tuples. None are tagged Visser today.

**The question:** how does the resolver / PPR generator know which sleeves are in scope when Visser intelligence applies?

**Options I see:**
- **(a) Add a `visser_relevant BOOLEAN` column to `sleeve_map`.** Cyler authors per-sleeve assignments (you'd send me a list — or update the canonical sleeve_map brief — of sleeve_ids that are Visser-relevant). Smallest schema change; clear lookup at resolver time.
- **(b) Define Visser-touched sleeves via `frameworks` in the Visser items themselves.** When an item carries `frameworks: ["Power Grid", ...]`, the publisher rolls up which sleeve_classes those frameworks map to (via a frameworks-to-sleeves table or hard-coded mapping). Indirect; depends on item-level framework tagging being clean.
- **(c) Don't represent Visser scope structurally.** Cyler reads `ape_intel.md` and `ab3_deviation_log` side-by-side and decides which deviations to read with Visser color. No new schema. Trades reproducibility for flexibility.

**My recommendation if you're undecided:** option (a). Concrete, small, auditable, and the assignment is a one-time human authoring task. Sends a clean signal to the resolver: this deviation lands in a Visser-flagged sleeve, so its tier escalation should consider current Visser status.

---

### Q4 — PPR integration

**Build context:** the existing `ppr_template.md` is the v1 PPR template per the AB3 ruleset §13. Visser's role per the grounding brief: PPR narrative, concentration review, AB3 escalation context, sleeve add/trim staging, watchlist promotion/deferral, warning banners.

**The questions:**
- **Q4a — New section in `ppr_template.md`?** A "Visser status & implications" section between the existing deviation summary and the recommended actions? Or interleaved into the existing sections (e.g. status banner at the top; per-deviation Visser color in the per-sleeve breakdown)?
- **Q4b — Does the resolver consume Visser status?** Two paths:
  - Resolver reads current Visser status and stamps a `visser_color` field on each `ab3_deviation_log` row. Resolver math is unchanged but downstream consumers (PPR generator, Cyler) see the Visser overlay structurally.
  - Resolver stays Visser-blind; Cyler reads `ape_intel.md` and the deviation log separately and applies Visser color in the PPR text he writes.
- **Q4c — Are there hard-rule integration points** (e.g. "if Visser is `concentration-caution` AND the deviation is over X% in a Visser-flagged sleeve, escalate the tier") or is everything textual interpretation?

**My recommendation if you're undecided:** Cyler-driven (Q4b path 2) for v2; structural (path 1) for a future v3 once the operational pattern stabilizes. PPR template gets a new section per Q4a (cleaner than interleaving); no hard rules in v2 (Q4c).

---

### Q5 — TV warehouse: does Visser need its own price ingest?

**Build context:** as of 2026-05-02, Gavin has provided ticker scope for three new themes (`ai_infra`, `visser_macro_regime`, `frontier_optionality` — drafted in `tv_themes.yaml` with `enabled: false` until layouts exist). These will populate the price+indicator warehouse alongside `mstr_suite`.

**The question is implicit but worth confirming:** the Visser Theme as defined in the grounding brief is *advisory thematic intelligence* (read from APE). The three new YAML themes are *price+indicator data feeds*. Are they the same Visser, or two different things flying under the same banner?

**My read:** they're complementary, not the same.
- The **APE-driven Visser status** (this spec) is qualitative and sits in `ape_intel.md`.
- The **TV warehouse Visser-related themes** are quantitative and sit in `tv_price_bars` / `tv_indicator_values`. They give Cyler price+indicator history for the names that the qualitative status applies to.

**Confirm or correct:** if the brief intends Visser to be purely intelligence-driven with no separate price ingest, I'll mark the three TV themes accordingly. If Visser includes a structural price-data presence (which the AI Infra / Macro Regime / Frontier ticker scopes suggest), then both surfaces co-exist and Q3 (sleeve mapping) gets a parallel "ticker → Visser-theme" mapping question.

---

## 4. What I'm building in parallel (no Cyler input needed)

These don't require Q1–Q5 answers and are safe to ship now:

- **Visser doctrine statement** in `AGENTS.md` (rev7.3 doctrine block; landed 2026-05-02).
- **`## Visser Status` placeholder section** in `ape_intel.md` (publisher pre-wired with the section structure; content rule slots in once Q1+Q2 settle).
- **Three draft themes** in `tv_themes.yaml` (`enabled: false`; flips on once Gavin's layouts exist).
- **Skip-disabled-theme logic** in `tv_poll.py` and `tv_seed.py` (added 2026-05-02).
- **Operational spec request** (this brief).

---

## 5. Suggested operational spec deliverable

A concrete operational v2 brief from Cyler addressing:

1. Q1 answer + reasoning
2. Q2a/Q2b/Q2c — section structure, computation rule, sample output
3. Q3 answer + (if option a) initial Visser-relevant sleeve list
4. Q4a/Q4b/Q4c — PPR integration shape
5. Q5 confirmation + (if both surfaces) ticker→Visser-theme mapping for `ai_infra`, `visser_macro_regime`, `frontier_optionality`
6. A status template for `## Visser Status` showing what a real digest entry should look like in three illustrative cases (reinforcing / timing-caution / no-routed-evidence)

If the operational spec lands, I can implement Q1–Q4 in ~4 hours of work and push to all repos in a single rev7.4 wave.

---

## 6. Out of scope for this request

- Reframing Visser doctrine (the grounding brief is canonical)
- Adding Visser to AB4 benchmark math (explicitly out of scope per grounding §5.3)
- Auto-trading on Visser signals (explicitly out of scope per grounding §3.3, §11.2)
- Bidirectional MSTR↔APE control loop (deferred to v3 per APE ingest contract §12.2)
