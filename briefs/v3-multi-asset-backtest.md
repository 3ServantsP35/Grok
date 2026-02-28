# V3 Multi-Asset Indicator Backtest

**Date:** 2026-02-28  
**Assets:** MSTR, BTC, TSLA, QQQ, GLD, TLT, IWM, BLOK (8 assets)  
**Timeframe:** 4H bars, ~2021-2026 (2,325-2,545 bars per asset)  
**Scripts:** AB1 v3, AB2 v2, AB3 v3

---

## AB1 — Directional Signals (Sequential Staging)

### Cross-Asset Summary @ 20d Forward

| Asset | Mode | Signal | n | Win% | Median | Verdict |
|---|---|---|---|---|---|---|
| **TSLA** | Momentum | Strong Bull | 4 | **100%** | **+36.8%** | ✅ Best performer |
| **BLOK** | Momentum | Strong Bull | 6 | **83%** | **+18.8%** | ✅ Strong |
| **GLD** | Trending | Strong Bull | 6 | **100%** | **+6.7%** | ✅ Reliable |
| **IWM** | Mean-Rev | Strong Bull | 6 | 67% | +1.3% | ⚠️ Marginal |
| **QQQ** | Mean-Rev | Strong Bull | 2 | 50% | -2.0% | ❌ Too few fires |
| **MSTR** | Momentum | Strong Bull | 3 | 33% | -4.4% | ❌ Anti-signal |
| **BTC** | Momentum | Strong Bull | 1 | 0% | -3.5% | ❌ Single fire, loser |
| **TLT** | Mean-Rev | Strong Bull | 10 | **30%** | **-3.4%** | ❌ Anti-signal |

**Bearish Signals (MR assets auto-enabled):**

| Asset | Mode | Signal | n | Win% | Median | Verdict |
|---|---|---|---|---|---|---|
| **QQQ** | Mean-Rev | Strong Bear | 7 | **86%** | **+7.1%** | ❌ INVERTED — bears are bullish! |
| **GLD** | Trending | Strong Bear | 8 | **88%** | **+7.6%** | ❌ INVERTED |
| **IWM** | Mean-Rev | Strong Bear | 5 | 60% | +4.9% | ❌ INVERTED |
| **TLT** | Mean-Rev | Strong Bear | 7 | 14% | -3.1% | ✅ Only correct bear signal |
| **BLOK** | Momentum | Strong Bear | 10 | 40% | -2.8% | ⚠️ Weak signal |

### Key Findings

1. **AB1 Strong Bull works on TSLA (100%, +36.8%), BLOK (83%, +18.8%), GLD (100%, +6.7%)** — sequential staging captures genuine momentum shifts on these assets
2. **AB1 Strong Bull FAILS on MSTR and BTC** — the two assets we care most about. Sequential staging still catches early rallies that fail. Need additional filter (LOI < -20? MVRV < 0.8?)
3. **AB1 Strong Bull FAILS on TLT** — 30% win rate. Bond dynamics don't fit the FTL/STL framework
4. **ALL bearish signals on MR assets are INVERTED** — when the system says "short," price goes UP (QQQ 86%, GLD 88%). This confirms: SRI is structurally bullish. Bearish FTL crosses on non-TLT assets are contrarian buy signals, not sell signals
5. **Exception: TLT bear signals work** (14% win = 86% correct as bearish). TLT is the only asset where bearish AB1 has edge

### AB1 Recommendation
- **Enable:** TSLA, BLOK, GLD (strong bull only)
- **Disable or add deep-value filter:** MSTR, BTC
- **Disable entirely:** TLT (bull side broken), QQQ (too few bull fires)
- **KILL all bearish signals except TLT** — they are contra-indicators. Consider: flip bear signals to BUY on QQQ/GLD/IWM

---

## AB2 — Spread Signals

### Bull Put Results

| Asset | n | STL Hold 30d | 20d Win% | 20d Median | Verdict |
|---|---|---|---|---|---|
| QQQ | 1 | **100%** | 100% | +11.7% | ✅ But n=1 |
| GLD | 4 | 0% | **100%** | **+24.8%** | ⚠️ Profitable but breaches STL |
| TLT | 3 | 0% | 67% | +2.0% | ⚠️ Thin edge |
| MSTR | 5 | 0% | 60% | +4.5% | ❌ All breach STL |
| TSLA | 2 | 0% | 50% | +32.1% | ❌ Small sample |
| IWM | 3 | 0% | 33% | -1.3% | ❌ Negative |
| BLOK | 2 | 50% | 50% | -13.7% | ❌ Negative |

### Iron Condor Results (MR assets + BLOK leaked through)

| Asset | n | STL Hold | 20d Win% | 20d Median | Verdict |
|---|---|---|---|---|---|
| GLD | 77 | 26% | **68%** | **+5.2%** | ✅ Best IC asset |
| BLOK | 72 | 14% | **68%** | **+11.0%** | ✅ Strong (but momentum — shouldn't fire) |
| QQQ | 82 | 13% | 64% | +4.2% | ⚠️ STL breaches too frequent |
| IWM | 87 | 13% | 62% | +2.9% | ⚠️ Marginal |
| TLT | 104 | **1%** | **35%** | **-2.7%** | ❌ Disaster — 99% breach STL |

### Key Findings

1. **Bull Put STL hold rate is 0% across almost all assets** — the triple filter is selecting bars near STL where breach is imminent. The filter catches support tests that fail, not ones that hold. Need to INVERT: fire when price bounces OFF STL (close > STL after testing it), not when approaching it
2. **Iron Condors fire prolifically** on MR assets (77-104 times). Win rates are decent (62-68%) but STL hold is terrible (1-26%). The directional component loses even though the overall position may profit from theta
3. **TLT Iron Condors are catastrophic** — 1% STL hold, 35% win. TLT trends too much for condors
4. **BLOK Iron Condors shouldn't be firing** — BLOK is classified as Momentum but ICs appeared (72 fires). The auto-detect may be misclassifying BLOK, or the IC filter doesn't check mode
5. **GLD is the best spread asset** — both bull puts (100% win) and ICs (68% win, 26% hold) work

### AB2 Recommendation
- **Bull Put needs fundamental redesign**: Fire on bounce-from-STL, not approach-to-STL
- **Iron Condor**: Keep for GLD, QQQ. Disable for TLT (trending disaster). Fix BLOK classification leak
- **Bear Call suppression confirmed working** — 0 fires on all momentum assets ✅

---

## AB3 — LOI / LEAP Signals

### Trim Signal Quality

| Asset | Trim 25% n | 60d Win% | 60d Median | Assessment |
|---|---|---|---|---|
| **BLOK** | 11 | **80%** | **+32.6%** | ✅ Trims work — still more upside after |
| **MSTR** | 5 | 60% | +95.8% | ✅ Massive upside continues post-trim |
| **GLD** | 5 | 60% | +9.5% | ⚠️ Modest |
| **QQQ** | 4 | 75% | +10.3% | ⚠️ Decent |
| **TSLA** | 4 | 33% | -11.8% | ❌ Trims too early (price keeps falling) |
| **IWM** | 5 | 60% | +4.7% | ⚠️ Marginal |
| **TLT** | 9 | **12%** | **-11.1%** | ❌ Anti-signal — trim means more downside |

### Key Findings

1. **MSTR + BLOK trim signals are healthy** — price continues higher after trim. The shifted thresholds (40/60/80 for momentum) are working. Trimming 25% at LOI=40 while retaining 75% through further upside is correct portfolio management
2. **TLT trims are catastrophic** — 12% win at 60d, -11.1% median. When LOI reaches +10-18 on TLT, it's a SELL signal, not a trim. This confirms TLT is fundamentally different: the SRI framework detects "bullish structure" but TLT then reverts. **TLT should not use AB3 at all, or the thresholds need complete recalibration**
3. **TSLA trims too early** — only 33% win at 60d. The 40/60/80 thresholds may be too low for TSLA (LOI range -55 to +75 vs MSTR -72 to +100)
4. **LOI ranges differ wildly by asset** — BTC barely reaches ±43, QQQ ±28, while MSTR hits ±100 and BLOK ±48. Fixed thresholds can't work across all assets

### AB3 Recommendation
- **MSTR and BLOK**: Working as designed. Keep 40/60/80 trims
- **TLT**: Remove from AB3 entirely (LOI trims are anti-signal)
- **TSLA**: Widen trim thresholds (50/70/90) — current 40 is too early
- **QQQ/IWM**: MR thresholds (10/30/50) may be too tight for the narrow LOI range. Consider percentile-based adaptive thresholds
- **BTC**: LOI never reaches trim levels — AB3 is accumulation-only for BTC

---

## Asset-Level Verdicts

| Asset | AB1 | AB2 | AB3 | Overall |
|---|---|---|---|---|
| **TSLA** | ✅ Bull 100% | ⚠️ Too few | ⚠️ Trims early | Strong on AB1 |
| **BLOK** | ✅ Bull 83% | ⚠️ IC leak | ✅ Trims work | Best all-around |
| **GLD** | ✅ Bull 100% | ✅ Best spreads | ⚠️ Modest | Best for AB2 |
| **QQQ** | ❌ Too few | ⚠️ IC decent | ⚠️ Narrow range | Needs more data |
| **IWM** | ⚠️ 67% bull | ⚠️ IC marginal | ⚠️ Marginal | Mediocre across board |
| **MSTR** | ❌ 33% bull | ❌ 0% STL hold | ✅ Trims work | AB3 only |
| **BTC** | ❌ Single fire | — No fires | — No fires | Insufficient signal |
| **TLT** | ❌ Both broken | ❌ IC disaster | ❌ Anti-signal | **Remove from all AB scripts** |

---

## Critical Action Items

1. **KILL TLT from AB framework** — every indicator is broken or inverted on TLT. Bond dynamics fundamentally don't fit SRI's equity/crypto momentum framework
2. **FLIP bearish signals to BUY on QQQ/GLD/IWM** — or just disable bearish entirely (current state is dangerous: a user following "Strong Bear" on QQQ would short into +7% rallies)
3. **Redesign AB2 Bull Put trigger** — fire on bounce-from-STL, not approach-to-STL
4. **Fix BLOK IC leak** — momentum asset shouldn't get Iron Condors
5. **Add percentile-based AB3 thresholds** — LOI ranges differ 3x across assets; fixed thresholds don't generalize
6. **Add MSTR/BTC-specific AB1 filter** — require LOI < -20 or deep discount condition to prevent catching early-stage rallies in structural bear markets
