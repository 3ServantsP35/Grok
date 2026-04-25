# P-TVI — Architecture Decisions v1

**Status:** Decided  
**Date:** 2026-04-25  
**Decisions recorded from:** #infra-ops conversation, Gavin + Archie  
**Context:** These decisions update and supersede any implicit Phase 0 assumptions in the handoff brief that described CSV downloads as a manual step.

---

## AD-1 — TradingView Data Access: Use tradingview-mcp CDP approach (not Playwright web)

### Decision
MSTR Engine's TradingView data acquisition will use the `tradingview-mcp` CLI via Chrome DevTools Protocol (CDP) to control TradingView Desktop — the same architecture the Camel Engine already uses in production.

This replaces/supersedes the earlier Phase 0 assumption that CSVs would come from "normal TradingView downloads" performed manually by Gavin.

### Architecture
```
mstr_tv_reader.py → tradingview-mcp CLI → CDP port 9222 → TradingView Desktop
```

Camel Engine reference implementation: `~/camel-engine/pipeline/tv_reader.py`  
CLI location: `~/tradingview-mcp/src/cli/index.js`

### What this enables
- Automated symbol switching
- Automated timeframe verification and setting
- Automated CSV export or indicator value reads
- No manual download step required

### What this does NOT do
- It does not replace the Python engine as the decision/interpretation layer
- TradingView remains a sensor layer; Python remains the brain

### Rationale
The Camel Engine proved this pattern works in production. Reusing the same toolchain avoids building a parallel access mechanism and keeps infrastructure consolidated on a single CDP approach.

---

## AD-2 — 4H Timeframe is Canonical for All MSTR Indicators

### Decision
All MSTR Engine indicators are calibrated and tuned to the 4-hour (4H) timeframe. This is non-negotiable and permanent, not a default that can drift.

The automation must:
1. **Verify** the active chart timeframe is `4H` before any CSV export or indicator read
2. **Set** the timeframe to `4H` if it is not already set
3. **Never** read data on any other timeframe

This applies to all current and future MSTR indicators added to the pipeline.

### Why enforcement matters
TradingView can silently revert to a different timeframe after symbol switches, chart reloads, or manual user interaction between automated runs. Reading data on the wrong timeframe would produce corrupt results without any explicit error — the data would look valid but be meaningless against MSTR Engine calibration.

### Implementation requirement
The MSTR `tv_reader.py` equivalent must include a `verify_and_set_timeframe("4H")` step as a hard precondition before any data read. This step must not be skippable via config or argument.

---

## Open Questions (not yet decided)

These remain from the broader P-TVI backlog:

1. **CSV vs. indicator-table reads** — Will the MCP path export CSVs (CDP-driven download) or read indicator values directly from the chart panel? Camel Engine reads indicator tables directly; MSTR may need CSVs for engine compatibility. Needs a concrete proof of concept to decide.

2. **Canonical ingestion architecture** — GitHub-tracked vs. direct local path vs. hybrid. Still open per `active-tasks.md`.

3. **Shared validator module** — Whether to build a shared CSV validator/resolver usable by both the tradingview-mcp path and any manual fallback path.
