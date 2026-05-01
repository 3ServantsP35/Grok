# ABFv2 Salvage Decisions v1
**Project:** Doctrine cleanup after v3.2.2 reframing  
**Date:** 2026-05-01  
**Author:** Cyler (CIO)  
**Status:** Salvage decision artifact for Archie validation / mechanical patching

---

## Scope

This artifact reviews `briefs/abfv2-uncommitted-salvage-source-2026-05-01.md` fragment-by-fragment and decides whether each substantive uncommitted edit should:
- **KEEP** and migrate verbatim,
- **REPHRASE** into current v3.2.2 doctrine vocabulary,
- or **ARCHIVE** as genuinely obsolete / contradicted.

Core standard used in this review:
- v3.2.2 is the active doctrine stack
- **AB4 is the benchmark anchor**
- **AB3 is the deviation layer atop AB4**
- technical trade-gating logic from ABFv2 should **not** be silently backported into benchmark / resolver doctrine unless it still makes sense there

---

## Salvage decision table

| Fragment | Verdict | Migrate to | Rationale |
|--------------------|---------------------------|----------------------------------|-----------|
| Status flip: `DRAFT` → `APPROVED by Gavin — awaiting Greg review` | ARCHIVE | n/a | This is file-status metadata on a superseded document, not live doctrine. Current authority should remain attached to the active v3.2.2 artifacts, not inherited from an archived ABFv2 file. |
| AB1 RP1 gate revision: quality assets (SPY, QQQ, GLD) may enter AB1 in RP1 while risk assets still require RP2+ | ARCHIVE | n/a | This is technical directional-entry gating from the old CT/RP execution model. It may still be useful later in an AB1/AB2 technical screener or execution ruleset, but it does not belong inside the current AB4 benchmark / AB3 deviation stack. |
| Current-state example: GLD CT4 eligible in RP1, TLT CT4 but AB4-only | ARCHIVE | n/a | Snapshot-specific operational commentary, not durable doctrine. It should remain historical context only. |
| Key-rule change: replace simple `AB1 requires RP2+` with a tiered regime gate | ARCHIVE | n/a | Same reason as above. This is part of the old tactical signal grammar, not the benchmark/deviation architecture. If revived, it should land in a future technical options-entry / AB1 rules doc, not the current resolver docs. |
| Yield objective change: replace 0.83% monthly hurdle with a codified **2%/month yield objective** | ARCHIVE | n/a | As written, this conflicts with the current architecture. In v3.2.2, STRC remains a benchmark / hurdle reference inside AB4, but not every trade or sleeve should be governed by a universal 2% monthly objective. This may still be a useful future target for income-oriented AB1/AB2 design, but it should not be migrated into the current benchmark resolver doctrine. |
| Heading change: `Open Questions` → `Decisions (Closed — Feb 27, 2026)` | ARCHIVE | n/a | Editorial / governance metadata on a superseded file. The individual decisions are reviewed below on their merits. |
| Closed decision: RP1 gate for quality assets approved | ARCHIVE | n/a | Same as the AB1 RP1 gate fragments above. Potentially reusable later, but not a fit for current v3.2.2 doctrine documents. |
| Closed decision: position sizing should optimize for highest annual return while meeting a minimum 2% monthly yield threshold | ARCHIVE | n/a | Too tightly tied to the old bucket-rotation framing. Under v3.2.2, benchmark posture, deviation logic, and sleeve-level concentration review come first; a universal 2% monthly target is not an appropriate global doctrine rule. |
| Closed decision: guideline that **no single investment should represent more than 5% of total portfolio** | REPHRASE | `briefs/p-ab3-ruleset-v1.md` §11.3 Concentration doctrine | The underlying concern remains valid, but the old wording cannot survive verbatim because the new framework explicitly allows benchmark sleeves above 5% and even meaningful concentration when warranted. What survives is a **soft scrutiny threshold** for concentrated AB3 deviations, especially in special sleeves. |
| Closed decision: **AB2 bear spread program approved** (~6x/year is enough because STRC is the parking lot between signals) | ARCHIVE | n/a | This is about AB2 program viability, not AB4 benchmark logic or AB3 deviation doctrine. It belongs, if anywhere, in a future AB1/AB2 trading brief or technical screener / execution doctrine. |
| Closed decision: **Sector ETF expansion NOT NOW**; prove the 7-asset pool first | ARCHIVE | n/a | Current v3.2.2 doctrine already assumes a broader sleeve universe and Howell sector structure. The old restriction is contradicted by the active architecture and should not be migrated. |

---

## REPHRASE decisions with ready-to-apply patches

## 1. Concentration guideline (`no single investment > 5%`) → REPHRASE

### Why this survives only in adapted form
The old version was:

> no single investment should represent more than 5% of total portfolio.

That cannot be migrated verbatim because the current framework explicitly allows:
- benchmark sleeve weights above 5%,
- special sleeves with meaningful benchmark allocations,
- and concentration when evidence is strong.

What *does* survive is the governance intent:
- concentration should not drift in unnoticed,
- especially in special sleeves,
- and a soft review threshold is useful.

### Rephrased text

> **Soft concentration review threshold:** absent explicit override, any single-name or special-sleeve **AB3 incremental deviation** greater than **5 percentage points of total portfolio** should trigger explicit concentration review in PPR. This is not a hard ban, but a scrutiny threshold intended to prevent hidden concentration from presenting itself as routine benchmark drift.

### Ready-to-apply patch

```markdown
*** Begin Patch
*** Update File: briefs/p-ab3-ruleset-v1.md
@@
 ### 11.3 Concentration doctrine
 AB3 can create concentration, but should not create **unexamined concentration**.
 
 Any AB3 position should be judged by:
 - total portfolio look-through exposure
 - correlation to existing special sleeves
 - macro phase compatibility
 - whether the benchmark already carries the same theme
+
+**Soft concentration review threshold:** absent explicit override, any single-name or special-sleeve **AB3 incremental deviation** greater than **5 percentage points of total portfolio** should trigger explicit concentration review in PPR. This is not a hard ban, but a scrutiny threshold intended to prevent hidden concentration from presenting itself as routine benchmark drift.
*** End Patch
```

---

## Archive notes for future doctrine authors

These fragments were **not** migrated into the current v3.2.2 stack, but they may still deserve a future home in non-resolver docs:

### Likely future-home candidates
- **AB1 RP1 gate for quality assets**
  - Possible future home: technical entry / screener doctrine for AB1 or options opportunity screening.
- **2% monthly yield objective**
  - Possible future home: AB1/AB2 income-program design doc, if Gavin wants a stronger explicit return target than the STRC hurdle.
- **AB2 bear spread program approval**
  - Possible future home: AB2 program brief or technical options screener / execution brief.

### Clearly obsolete under current doctrine
- sector ETF expansion deferral
- file status / editorial metadata
- snapshot-specific GLD / TLT commentary

---

## Bottom line

My salvage conclusion is intentionally narrow:
- **Most ABFv2 uncommitted edits should be archived**, not migrated, because they belong to the older CT/RP tactical bucket model.
- The one fragment that cleanly survives translation into current doctrine is the **concentration-governance instinct**, but only after being rewritten into **AB3 incremental deviation** language.
- Everything else should either remain archived or be revisited later in a dedicated **technical entry / AB1 / AB2 / screener** brief rather than polluting the current benchmark-resolver stack.
