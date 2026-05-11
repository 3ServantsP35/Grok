# P-MSTR-SUITE-REPORT — New MSTR Suite Report v1

**Project:** P-MSTR-SUITE-REPORT  
**Date:** 2026-05-11  
**Status:** Open  
**Author:** Cyler

---

## 1. Why this project exists

The legacy MSTR Suite reporting path that relies on CSV exports is now deprecated.

The reason is straightforward:
- the legacy CSV-driven generator can produce stale or contradictory output
- that output can conflict with the current live suite state
- this creates false analytical confidence and is not acceptable for production reporting

This project exists to replace that legacy path with a **new MSTR Suite report** built on the live source-of-truth path.

---

## 2. Core doctrine

The new MSTR Suite report should be built around the principle that:

> live source-of-truth inputs are authoritative, and stale legacy export paths must not be allowed to silently generate misleading analysis.

The old CSV path should therefore be treated as:
- deprecated for production use
- usable only as historical reference or archived logic source until explicitly retired

---

## 3. Project goals

This project should deliver:

1. a **new MSTR Suite report path** built around current live suite inputs
2. fail-closed validation that prevents stale or contradictory input states from producing a report
3. a clearer output structure that fits the current architecture and reporting standards
4. a suite report that can serve as a trustworthy input into Layer 2-3 and PPR interpretation

---

## 4. Preferred source-of-truth direction

The likely primary source path is:
- `mstr-knowledge/tv_state.md`

Potential supporting artifacts may include:
- `mstr-knowledge/phase_state.md`
- `mstr-knowledge/cycle_state.md` (only if fresh enough)
- options-state artifacts where needed for delta/theta-aware interpretation

The project should explicitly decide which artifacts are authoritative and in what order.

---

## 5. Required hardening behaviors

The new suite report should:
- fail closed when source data is stale
- validate recency/freshness before generating a report
- validate key values against the live source path
- clearly distinguish:
  - valid report
  - stale source
  - contradictory source state
  - missing source state

The system should prefer no report over a misleading report.

---

## 6. Draft report requirements

The new suite report should likely include:
- structural state
- force diagnostics
- trend / transition interpretation
- scenario framing
- bucket translation
- clear CIO conclusion

It should also align with the newer product/reporting principle:

> the real deliverable is decision-ready clarity, not just rational analysis.

---

## 7. Open design questions

1. Should the new suite report be generated directly from `tv_state.md`, or should there be a purpose-built intermediate state artifact?
2. How much of the old suite logic is worth preserving versus rewriting?
3. What are the minimum freshness and contradiction checks required before report generation?
4. Should the new suite report become the canonical chart-state input for Layer 2-3 and PPR workflows?
5. How should Archie’s report-path fix interact with this broader replacement effort?

---

## 8. Immediate next steps

1. define the canonical source-of-truth inputs for the new suite report
2. define the required fail-closed checks
3. define the new report structure
4. determine whether the legacy generator should be archived or retained only for reference
5. connect the new suite report to the broader PPR / Layer 2-3 workflow

---

## 9. Bottom line

This is not just a bug fix.

It is a report-path replacement project.

The goal is to build a **new MSTR Suite report** that is live-source-driven, fail-closed, and trustworthy enough to support downstream portfolio and sleeve decisions.
