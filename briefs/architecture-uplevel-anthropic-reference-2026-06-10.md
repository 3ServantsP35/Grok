# MSTR Engine Architecture Uplevel Brief
**Anthropic Financial Services Reference Assessment + Proposed Skills System**

**Prepared for**: Gavin, Greg, Archie  
**Date**: 2026-06-10  
**Author**: Cyler (CIO)  
**Purpose**: Evaluate whether adopting patterns from Anthropic’s public financial-services agent repository justifies the engineering effort for the MSTR Engine.

---

## 1. Executive Summary

The Anthropic `financial-services` GitHub repo + associated 2025/2026 releases represent the strongest public reference architecture for multi-agent finance/quant systems currently available. It emphasizes **modular skills**, named end-to-end agents, governed connectors, sub-agent orchestration, and validation tooling.

**Recommendation**: The core ideas are worth adopting selectively. A full lift-and-shift is not justified, but a targeted `skills/` system with sync/validation tooling would meaningfully improve maintainability, reduce prompt drift, and make future specialization easier — especially as the rule set and agent count grow.

**Juice vs. Squeeze verdict**: Worth doing in phases, starting with the highest-leverage pieces (skills modularity + validation scripts). Expected net positive within 4–6 weeks if scoped tightly.

---

## 2. Assessment of Anthropic Materials

**Key Artifacts Reviewed**
- GitHub: `anthropics/financial-services` (reference agents, skills, connectors, managed-agent cookbooks)
- Anthropic announcements: “Claude for Financial Services” (2025) and “Agents for financial services” (May 2026)
- Keynote framing: Positioned as “closest thing to a real quant research desk”

**Strengths of Their Approach**
- Clean separation between **skills** (domain knowledge + methods) and **agents** (workflow ownership).
- Skills are small, versionable, and bundled rather than duplicated.
- Explicit sub-agent delegation patterns and orchestration examples (`orchestrate.py`, leaf-worker subagents).
- Strong emphasis on auditability, human sign-off, and validation scripts (`check.py`, `sync-agent-skills.py`).
- Connector abstraction (MCP) for data sources.
- Reference templates designed to be customized, not used as-is.

**Limitations for Our Use Case**
- Generalist FSI focus (IB, PE, fund admin, wealth). Our domain is highly specialized (SRI stages, AB-framework v3.2.2, MSTR reflexivity, GLI meta-filter, STRC hurdle, etc.).
- Their doctrine layer is weaker than ours.
- Heavy reliance on commercial data platforms; our connectors are mostly custom.
- Platform-specific (Claude Cowork / Managed Agents) vs. our OpenClaw + sessions_spawn flexibility.

**Bottom line**: Excellent reference for *plumbing and modularity*. Does not replace our methodology or CIO synthesis role.

---

## 3. Current MSTR Engine State vs. Reference

| Dimension              | Current MSTR Engine                          | Anthropic Reference                     | Gap / Opportunity                     |
|------------------------|----------------------------------------------|-----------------------------------------|---------------------------------------|
| Prompt Structure       | Monolithic AGENTS.md + trading-rules.md     | Modular skills + bundled agents        | High – drift risk, hard to maintain  |
| Agent Specialization   | 4 analysts + CIO                             | Named end-to-end agents                | Medium – we are already close        |
| Sub-agent Handoffs     | sessions_spawn + custom delegation           | Explicit leaf workers + steering       | Medium – can improve                 |
| Data Layer             | Custom scripts                               | MCP connectors + manifest              | Medium – formalize as connectors     |
| Validation & Sync      | Manual                                       | check.py / sync-agent-skills.py        | High – add this                      |
| Auditability           | Strong (Hypothesis Blocks, signal_scores)    | Strong (logs, permissions, sign-off)   | Low – already good                   |
| Doctrine Strength      | Very strong (9 permanent rules, AB spine)    | Weak                                   | We are ahead                         |

---

## 4. Proposed Skills System (Draft for Review)

**Goal**: Move from monolithic prompt files to a maintainable, versioned skills library while preserving all existing doctrine and output formats.

**Proposed Directory Structure**

```
mstr-engine/
├── skills/
│   ├── core/                    # Shared across all agents & CIO
│   │   ├── hypothesis-block.md
│   │   ├── data-freshness.md
│   │   ├── ab-framework-overview.md
│   │   ├── permanent-rules.md   # The 9 rules, one file or split
│   │   ├── output-formats.md    # Morning Brief, trade rec, council verdict
│   │   └── self-check.md
│   ├── sri/
│   │   ├── stage-logic.md
│   │   ├── srbi-mvrv-rules.md
│   │   ├── asset-specific.md
│   │   └── ...
│   ├── macro/
│   │   ├── gli-gegi-filter.md
│   │   ├── howell-phase.md
│   │   ├── btc-sma50.md
│   │   └── ...
│   ├── technical/
│   ├── options/
│   ├── cio/
│   │   ├── synthesis-protocol.md
│   │   ├── council-verdict.md
│   │   └── delegation-rules.md
│   ├── connectors/
│   │   └── manifest.yaml        # Data sources + freshness requirements
│   └── scripts/
│       ├── sync-agent-skills.py
│       ├── validate.py
│       └── check.py
│
├── agents/                      # Future: named agent definitions
│   ├── mstr-sri-agent.md
│   ├── mstr-macro-agent.md
│   └── ...
└── ...
```

**Example Skill File Format** (`skills/sri/stage-logic.md`)

```markdown
---
skill_id: sri-stage-logic
version: 1.3
owner: mstr-sri
last_updated: 2026-06-09
dependencies: [core/ab-framework-overview, core/permanent-rules]
used_by: [mstr-sri-agent, cio-synthesis-agent]
tags: [stage, sri, core]
---

# SRI Stage Logic (10-State Model)

## Purpose
Define the exact criteria and thresholds for assigning one of the 10 SRI stages to MSTR and related assets.

## Inputs
- SRIBI value + components
- STH-MVRV
- Price action relative to key levels
- Liquidity regime (HYG SRIBI, VIX LOI)
- GLI Z-score (via meta-filter)

## Process
1. Calculate base stage from SRIBI + MVRV thresholds.
2. Apply Rule 1 (GLI Meta-Filter) probability adjustment.
3. Apply Rule 2 (Saylor Event Discount) if active.
4. Apply Rule 3 (Liquidity Regime TF Weighting).
5. Apply Rule 9 (BTC 50-Day SMA) defensive overlay if triggered.
6. Resolve conflicts using governance spine priority.

## Output Format
Return: Stage X (name), confidence, key drivers, and any active rule adjustments.

## Constraints & Rules
- Never override AB4 or AB3 tier math.
- Must state data freshness + timestamp.
- Stage 4 with Rule 9 trigger → maximum defensive posture.

## Examples
[Include 2–3 concrete historical examples with dates]

## Change Log
- v1.3: Added Rule 9 integration (2026-06-09)
```

This format makes skills self-documenting, versioned, and easy to sync/validate.

---

## 5. Recommendations & Prioritization

**Phase 1 (High ROI, Low Risk) – 2–3 weeks**
- Extract 4–6 core skills (Hypothesis Block, Data Freshness, Permanent Rules, SRI Stage Logic, AB Framework overview).
- Implement basic `sync-agent-skills.py` + `validate.py`.
- Test bundling into existing sub-agents.

**Phase 2 (Medium) – 3–5 weeks**
- Add connectors manifest.
- Create named agent definition files.
- Improve sub-agent handoff patterns based on their orchestration examples.

**Phase 3 (Optional)**
- Full migration of all rules and analyst instructions.
- Evaluation harness for agent output quality.

**Do Not Do**
- Move to their platform or Managed Agents (we have better flexibility with OpenClaw).
- Over-generalize skills at the expense of our specialized doctrine.

---

## 6. Effort vs. Benefit Analysis (“Juice Worth the Squeeze?”)

| Area                        | Effort | Benefit                          | Net | Notes |
|----------------------------|--------|----------------------------------|-----|-------|
| Skills modularity          | Medium | High (maintainability, less drift) | +   | Core win |
| Validation & sync scripts  | Low    | High (reliability)               | ++  | Quick win |
| Connectors abstraction     | Medium | Medium                           | +   | Helpful long-term |
| Sub-agent orchestration    | Medium | Medium                           | +   | Incremental improvement |
| Full agent re-architecture | High   | Medium                           | -   | Not worth it now |

**Overall**: The modular skills + validation layer is worth the effort. It directly addresses growing complexity and makes the system more robust as we add more rules and agents. The specialized nature of our domain means we should treat their repo as a strong reference, not a template to copy wholesale.

---

## 7. Next Steps

1. Archie to review this brief + proposed `skills/` structure and example.
2. Decision call (Gavin + Greg + Cyler + Archie) on Phase 1 scope.
3. If approved, Cyler to lead initial skill extraction with Archie on tooling.

---

**Status**: Draft for review. Ready for Archie evaluation and discussion with Greg.