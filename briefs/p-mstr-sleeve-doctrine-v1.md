# P-MSTR-SLEEVE — MSTR Sleeve Doctrine v1

**Owner:** Cyler (CIO)  
**Last Updated:** 2026-06-06  
**Status:** Draft for review & lock

---

## 1. Theme Identity & Scope

MSTR Sleeve Doctrine defines how the mandatory 40% MSTR allocation is expressed rotationally across market stages using aggregate delta management rather than passive long-only ownership. The sleeve is explicitly exempt from the 20% per-asset soft cap while the mandate remains active.

This brief covers only the MSTR rotational sleeve. It does not replace AB4 benchmark setting, AB3 deviation rules, or the core SRI stage machine.

## 2. Problem Statement (Fixed)

Is the MSTR sleeve currently positioned for optimal risk-adjusted appreciation versus STRC within the 40% always-maxed mandate, and how should aggregate delta be adjusted as SRI stage and liquidity regime change?

## 3. Integration Contract (Fixed)

- **Data sources:** tv_state.md (primary), mstr-knowledge/*, on-chain (Strategy holdings), mNAV, OKX BTC-USDT. All references include exact pull timestamp.
- **Fail-closed:** If tv_state or required indicators are >1 trading day stale, default to neutral delta posture and flag for immediate review.
- **Outputs:** Stage-by-stage delta target, expression mix (bullish calls / short calls / put LEAPs), PPR-ready recommendation, morning brief section.
- **Privacy:** No personal balances, P&L, or cost basis. Generic sleeve posture only.
- **Human-in-the-loop:** All sleeve changes require operator confirmation before execution.

## 4. Indicator Consumption Contract

1. **Indicator surface:** Primary = SRI_VLT + SRIBI_VLT + LOI (adaptive). Secondary = VST/ST for tactical delta adjustments, mNAV for call/put gates.
2. **TF weighting:** Follows Rule 3 exactly. EXPANDING regime → elevate VST/ST influence on delta targets. CONTRACTING regime → require LT/VLT confirmation before material delta increase.
3. **Theme-specific extensions:** Aggregate delta calculation (long LEAP delta + short call delta + put LEAP delta). mNAV-based call selling gate (high mNAV → sell calls; low mNAV → sell puts). Stage-specific expression mix.
4. **Confirmation ladder usage:** Uses standard Watch/Forming/Confirmed/Invalidated on the MSTR SRI stage transition. Delta changes are gated on Confirmed or higher unless in S1 chop (where income expressions are prioritized).
5. **Fail-closed on indicator data:** If LOI or VLT is stale, hold existing delta posture and escalate to Cyler for manual override.

## 5. Theme-Specific Engine (MSTR Sleeve Uniqueness)

**Core principle:** Manage aggregate notional delta across stages 1–4 rather than maintaining static long exposure. The sleeve is always 40% of portfolio but the *expression* rotates.

**Stage-by-stage posture (starting point for testing):**

- **Stage 1 (Chop):** Income-max expression. PMCC short calls 0.20–0.25Δ / 7–14 DTE. Reduced long delta. Target aggregate delta 0.30–0.50.
- **Stage 2 (Recovery/Std):** Core bullish expression. Long LEAPs (AB3) + opportunistic short calls. Target aggregate delta 0.70–0.90.
- **Stage 3 (Trim Approach):** Delta reduction. Increase short calls, reduce new long LEAPs. Target aggregate delta 0.50–0.70.
- **Stage 4 (Decline):** Defensive expression. Put LEAPs or Expression 3 routing. Target aggregate delta 0.20–0.40.

**mNAV overlay:** High mNAV (≥3.0x) increases short-call priority. Low mNAV (≤1.2x) favors put selling or LEAP additions.

**Liquidity regime modifier:** In CONTRACTING regimes, require LT/VLT confirmation before any delta increase above 0.60.

**Saylor event discount:** During active convertible/note windows, treat Stage 3 signals as lower conviction.

## 6. Decision Framework & Output Contract

**Bottom line format:**  
"MSTR sleeve recommended aggregate delta: X.XX | Primary expression: [Long LEAPs / PMCC / Put LEAPs] | Rationale: [stage + regime + mNAV] | Trigger to change: [specific level or stage transition]"

All recommendations include the exact level that would invalidate the current posture.

## 7. Dependencies & Open Items

- Requires live tv_state.md and mNAV feed.
- Needs backtest validation of stage-by-stage delta targets (proposed R4 after current v3.2.2 work).
- Must be reconciled with P-MSTR-SUITE-REPORT confirmation ladder once both are live.

---

**Next:** Review & test this draft together. Once locked, it becomes the reference for all subsequent theme briefs.