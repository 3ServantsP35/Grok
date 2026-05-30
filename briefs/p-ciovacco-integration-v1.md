---
title: P-CIOVACCO-INTEGRATION
date: 2026-05-30
status: Draft v1
---

# P-CIOVACCO-INTEGRATION

## Purpose
Define how CiovaccoCapital should inform the architecture without becoming a dependency for core decisions.

## Core decision
CiovaccoCapital is an **advisory input only**.

It may improve interpretation when available, but the architecture must remain fully operable when it is absent.

## Non-dependency rule
- No Layer 0, 0.5, AB4, AB3, or PPR decision may require CiovaccoCapital to be available.
- No signal, gate, or allocation state should fail open or fail closed because a Ciovacco input is missing.
- If the source is unavailable, the decision stack proceeds using native architecture inputs only.

## Correct placement
CiovaccoCapital fits best as:
- **Layer 0.75 advisory intelligence**
- **MR Assets supplementary context**
- **AB4 stock-allocation supplement**, not benchmark authority

It does **not** replace:
- Layer 0 liquidity authority
- Layer 0.5 Howell phase authority
- AB4 benchmark construction
- AB3 deviation gates

## Best use cases
Use Ciovacco-style work to inform:
- long-horizon broad-equity trend quality
- breadth durability and participation quality
- rare historical analog setups
- whether SPY / broad equities appear structurally attractive enough to clear a higher hurdle versus defensive alternatives
- whether risk appetite is broadening in a way that supports more stock exposure inside MR Assets or AB4

## Not appropriate for
Do not use CiovaccoCapital as:
- a macro-liquidity substitute for Howell
- a direct trade trigger
- a required condition for AB3 LEAP deployment
- a benchmark override

## Operational rule
When CiovaccoCapital provides useful information:
1. extract the relevant market-structure insight
2. translate it into MR Assets / AB4 context language
3. state clearly that it is **supplementary** rather than authoritative
4. preserve a clean fallback path when the source is absent

## Reporting guidance
When included in reports, language should be framed like:
- "supplementary broad-equity structure input"
- "advisory market-structure context"
- "non-blocking external confirmation"

Avoid language implying the architecture depends on it.

## Immediate next step
Use CiovaccoCapital in manual review mode first. Do not wire automation or required report fields until repeated value is demonstrated.
