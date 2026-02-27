# Framework Architecture Consolidation — CIO Recommendation
**Date:** February 27, 2026  
**Requested by:** Gavin  
**Status:** DRAFT — awaiting Gavin review

---

## The Problem

We've built powerful analytical frameworks, but they've emerged organically over 10 days. The naming is inconsistent, the relationships between frameworks aren't formalized, and a new reader (or Gary) would struggle to understand how they fit together. We need a clean architecture before we codify further.

**Current inventory of frameworks:**
1. RORO (5-phase capital rotation)
2. Four-Bucket Investment Framework (allocation structure)
3. SRI 4-Stage (Wyckoff cycle — the foundation Gavin built)
4. 4-Tier Entry System (SRIBI concordance timing — new today)
5. BTC Cycle Phases (C4→C1→C2→C3)
6. Three-Tier FTL/STL Framework (crossover classification)
7. Bearish Signal Tiers (SOPR/STRS distribution detection)
8. STRC Cost-of-Capital Benchmark
9. Preferred Stock Signal Layer (SCHI composite)
10. GLI Meta-Filter

That's 10 frameworks. Some are nested. Some overlap. Some are decision layers and some are signal layers. Here's my recommendation for organizing them.

---

## Proposed Architecture: Three Layers

### Layer 1: REGIME (Where are we?)
Answers: "What phase of the cycle are we in? What's the macro environment?"

| Component | What It Does | Output |
|---|---|---|
| **SRI Stage** (4-Stage) | Wyckoff cycle position per asset, per timeframe | Stage 1/2/3/4 × VST/ST/LT/VLT |
| **RORO Phase** (5-Phase) | Cross-asset risk appetite | P1→P5 |
| **BTC Cycle** (6-Phase) | BTC-specific position in markup/markdown | C4→C4to1→C1→C2→C2m→C3 |
| **GLI Regime** | Global liquidity direction | Expanding / Contracting / Z-score |

**Proposed name:** **Regime Engine**  
**Output:** A single regime state: `RORO Phase × BTC Cycle × GLI Direction`  
Example: `P1_EARLY × C4_MARKDOWN × GLI_Stabilizing`

This is the "dashboard" layer. It doesn't tell you what to trade — it tells you what *kind* of environment you're in, which constrains everything downstream.

### Layer 2: SIGNAL (What's the trade?)
Answers: "Given this regime, what specific entry/exit signals are firing?"

| Component | What It Does | Output |
|---|---|---|
| **SRIBI Concordance** (4-Tier) | Multi-TF SRIBI alignment for entry timing | T1 Scout → T4 High Conviction |
| **Bearish Triggers** | SOPR/STRS distribution detection | Bear Tier 1/2/3 |
| **FTL/STL Crossover** | Trend confirmation per TF | Bull cross / Bear cross × TF |
| **Preferred Stock Signals** (SCHI) | Leading indicator from credit markets | STRC/STRF/STRK stress levels |
| **Stage Transitions** | Structural shift detection | 4→1, 1→2, 2→3, 3→4 × TF |

**Proposed name:** **Signal Layer**  
**Output:** Signal type + tier + direction + confidence  
Example: `SRIBI T2_EARLY (bullish, 55% win rate)`

Signals are GATED by regime. A T2 bullish signal in P1_EARLY doesn't trigger Bucket 1 (regime gate blocks it). The same signal in P3_RISK_ON triggers full Bucket 1 deployment.

### Layer 3: ALLOCATION (How much, where?)
Answers: "Given regime + signal, what do we actually do with capital?"

| Component | What It Does | Output |
|---|---|---|
| **Four-Bucket Framework** | Capital allocation structure | % to Bucket 1/2/3/4 |
| **STRC Hurdle** | Minimum return threshold | Trade clears 0.83%/mo or stays in STRC |
| **Anchored Allocation Table** | RORO × BTC Cycle → bucket targets | Specific % ranges per state |
| **Position Sizing** | Kelly-informed, max risk per trade | Dollar amount per position |

**Proposed name:** **Allocation Engine**  
**Output:** Specific trade recommendation with size, vehicle, structure  
Example: `Bucket 2: MSTR BPS Apr17 $110/$100, 2% of portfolio`

---

## The Decision Flow

```
┌─────────────────────────────────────────────┐
│           REGIME ENGINE (Layer 1)            │
│                                              │
│  SRI Stage × RORO Phase × BTC Cycle × GLI   │
│                                              │
│  Output: P1_EARLY × C4_MARKDOWN × GLI_Stab  │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           SIGNAL LAYER (Layer 2)             │
│                                              │
│  SRIBI Concordance Tier │ Bearish Triggers   │
│  FTL/STL Crossovers     │ SCHI Preferred     │
│  Stage Transitions       │                   │
│                                              │
│  Regime GATES which signals are actionable   │
│  Output: T2_EARLY bullish (gated → B2 only)  │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         ALLOCATION ENGINE (Layer 3)          │
│                                              │
│  Four Buckets │ STRC Hurdle │ Anchored Table │
│  Position Sizing │ Risk Limits               │
│                                              │
│  Output: Specific trade rec with size        │
└─────────────────────────────────────────────┘
```

---

## Naming Cleanup

### Current → Proposed

| Current Name | Problem | Proposed Name |
|---|---|---|
| "4-Stage" / "SRI Stage" | Ambiguous — which TF? | **SRI Stage [TF]** (always specify: "SRI Stage LT") |
| "RORO" | Good, keep it | **RORO Phase** (P1–P5) |
| "BTC Cycle" | Could mean anything | **BTC Cycle Phase** (C4, C4to1, C1, C2, C2m, C3) |
| "4-Tier Entry" | Confusable with "4-Stage" | **Concordance Tier** (T1–T4) |
| "Four-Bucket Framework" | Fine but wordy | **Bucket Allocation** (B1–B4) |
| "Three-Tier FTL/STL" | Overlaps with Concordance Tiers | **RETIRE** — subsume into Concordance Tier system |
| "Bearish Signal Tiers" | Fine | **Bear Trigger** (BT1–BT3) |
| "STRC Benchmark" | Fine | **STRC Hurdle** |
| "SCHI" | Fine | **Preferred Signal** (SCHI composite) |
| "GLI Meta-Filter" | Fine | **GLI Regime** |

### Biggest Cleanup: Merge Three-Tier FTL/STL into Concordance Tiers

The old Three-Tier FTL/STL framework (Tier 1 Aggressive Long, Tier 2 Moderate Long, Tier 3 Trap) was built on single-TF data. The new 4-Tier Concordance system supersedes it entirely — it captures the same crossover dynamics but across all timeframes with better precision. The "trap" finding (1/3 breadth) is now embedded in Concordance Tier logic.

**Recommendation:** Archive Three-Tier FTL/STL. Reference it as historical predecessor. Use Concordance Tiers going forward.

---

## Sequencing: What Gets Built First

| Priority | Component | Why | Status |
|---|---|---|---|
| 1 | Regime Engine definitions | Everything else depends on knowing the regime | 80% done — needs formal spec |
| 2 | Concordance Tier definitions (BTC) | Today's finding — needs codification | Backtested, needs spec |
| 3 | Regime × Signal gating rules | Which signals are actionable in which regimes | Partially in v1.2.1 |
| 4 | Allocation Engine tables | Bucket targets per regime state | Done in v1.2.1 anchored table |
| 5 | Bear Trigger expansion | More bearish indicators on BTC data | P2 ongoing |
| 6 | Alt asset signal calibration | Different weights for SPY-like vs BTC-like | New project (P6) |

---

## What This Changes in Practice

**Morning Brief structure would become:**

```
REGIME: P1_EARLY × C4_MARKDOWN × GLI_Stabilizing
CONCORDANCE: Pre-T1 (all SRIBI negative, no TF bullish)
ALLOCATION: B1=0% | B2=15-20% | B3=5-8% (Path B) | B4=72-80% (STRC)
BEAR WATCH: No BT triggers active
PREFERRED: STRC $100 (healthy), SCHI neutral

→ RECOMMENDATION: Hold current positions. No new entries until 
  Concordance reaches T1 (VST crosses zero). Accumulate LEAPs 
  only on Path B qualification.
```

Clean. Readable. Every framework has one job. No overlaps.

---

## Open Questions for Gavin

1. Does this three-layer architecture match your mental model?
2. The naming — does "Concordance Tier" feel right, or do you have a better term for the multi-TF SRIBI alignment concept?
3. Do you agree the Three-Tier FTL/STL should be retired in favor of Concordance Tiers?
4. Should we version this architecture (e.g., "MSTR Engine Architecture v1.0") for reference?
