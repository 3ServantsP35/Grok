# Stage Designation Backtest v1 — Reliability Analysis Across All Four Timeframes

> **Generated:** 2026-03-04 | **Data:** 4H OHLCV + SRI Indicators | **Assets:** MSTR, TSLA, IBIT, SPY, QQQ, IWM, GLD

---
## Section 1: Executive Summary

### Key Findings

- **Most Accurate Overall Approach (Bullish, at longest window):** LOI Trough — avg 56.4% accuracy across all assets
- **Best Single-TF Bullish Signal:** LT Only — avg 46.1% accuracy
- **Best Single-TF Bearish Signal:** VST Only — avg 100.0% accuracy

### Single-TF Accuracy Rankings (Cross-Asset Average, Longest Window, Bullish)

| Rank | TF | Avg Accuracy | Assets w/ n≥5 |
|------|-----|-------------|--------------|
| 1 | LT Only | 46.1% | 7/7 |
| 2 | ST Only | 45.7% | 7/7 |
| 3 | VST Only | 45.1% | 7/7 |
| 4 | VLT Only | 43.8% | 7/7 |

### All-Approach Rankings (Bullish, Longest Window)

| Rank | Approach | Avg Accuracy |
|------|---------|-------------|
| 1 | LOI Trough | 56.4% |
| 2 | LT Only | 46.1% |
| 3 | ST Only | 45.7% |
| 4 | All-4 Agree | 45.7% |
| 5 | VST Only | 45.1% |
| 6 | VLT Only | 43.8% |
| 7 | VST+ST Combined | 42.2% |
| 8 | LT+VLT Combined | 38.7% |
| 9 | ST+LT Combined | 30.2% |

---
## Section 2: Per-Asset Results

### MSTR (MOMENTUM)

- **Bars:** 645 | **Period:** 2024-11-11 → 2026-03-03
- **Windows:** [30, 60, 120] bars | **Bull threshold:** 15% | **Bear threshold:** -15%
- **LOI threshold used:** -45

**Stage Distribution:**
  - MIXED: 225 bars (34.9%)
  - S2: 116 bars (18.0%)
  - S2_early: 4 bars (0.6%)
  - S2_to_3: 8 bars (1.2%)
  - S3_to_4: 19 bars (2.9%)
  - S4: 250 bars (38.8%)
  - S4_to_1: 23 bars (3.6%)

#### Bullish Signal Accuracy

| # | Approach | N | Acc@30b | MAE@30b | Acc@60b | MAE@60b | Acc@120b | MAE@120b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 31 | 25.8%±15.4% (n=31) | -11.8% | 35.5%±16.8% (n=31) | -20.0% | 38.7%±17.1% (n=31) | -30.1% |
| 2. ST Only | 23 | 21.7%±16.9% (n=23) | -10.6% | 30.4%±18.8% (n=23) | -22.9% | 47.8%±20.4% (n=23) | -30.1% |
| 3. LT Only | 17 | 23.5%±20.2% (n=17) | -17.5% | 35.3%±22.7% (n=17) | -20.0% | 41.2%±23.4% (n=17) | -29.7% |
| 4. VLT Only | 30 | 23.3%±15.1% (n=30) | -10.7% | 30.0%±16.4% (n=30) | -18.0% | 43.3%±17.7% (n=30) | -30.2% |
| 5. VST+ST | 13 | **38.5%±26.4%** (n=13) | -8.0% | 38.5%±26.4% (n=13) | -15.4% | 53.8%±27.1% (n=13) | -24.5% |
| 6. ST+LT | 7 | 28.6%±33.5% ⚠️LOW (n=7) | -20.2% | **42.9%±36.7% ⚠️LOW** (n=7) | -25.0% | **57.1%±36.7% ⚠️LOW** (n=7) | -29.1% |
| 7. LT+VLT | 9 | 22.2%±27.2% ⚠️LOW (n=9) | -10.8% | 33.3%±30.8% ⚠️LOW (n=9) | -17.8% | 44.4%±32.5% ⚠️LOW (n=9) | -24.5% |
| 8. All-4 Agree | 20 | 20.0%±17.5% (n=20) | -13.5% | 30.0%±20.1% (n=20) | -22.0% | 35.0%±20.9% (n=20) | -26.9% |
| 9. MIXED (Gavin's) | 1 | 0.0%±0.0% ⚠️INSUF (n=1) | -10.9% | 0.0%±0.0% ⚠️INSUF (n=1) | -16.2% | 0.0%±0.0% ⚠️INSUF (n=1) | -51.5% |
| 10. LOI Threshold | 2 | 0.0%±0.0% ⚠️INSUF (n=2) | -12.8% | 0.0%±0.0% ⚠️INSUF (n=2) | -18.3% | 0.0%±0.0% ⚠️INSUF (n=2) | -42.5% |
| 11. LOI Trough | 48 | 25.0%±12.2% (n=48) | -12.1% | 37.5%±13.7% (n=48) | -19.2% | 56.2%±14.0% (n=48) | -29.3% |

#### Bearish Signal Accuracy

| # | Approach | N | Acc@30b | MAE@30b | Acc@60b | MAE@60b | Acc@120b | MAE@120b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 31 | **100.0%±0.0%** (n=31) | 5.0% | **100.0%±0.0%** (n=31) | 9.7% | **100.0%±0.0%** (n=31) | 16.8% |
| 2. ST Only | 22 | **100.0%±0.0%** (n=22) | 6.4% | **100.0%±0.0%** (n=22) | 10.1% | **100.0%±0.0%** (n=22) | 20.2% |
| 3. LT Only | 19 | **100.0%±0.0%** (n=19) | 8.5% | **100.0%±0.0%** (n=19) | 13.0% | **100.0%±0.0%** (n=19) | 15.7% |
| 4. VLT Only | 32 | **100.0%±0.0%** (n=32) | 7.1% | **100.0%±0.0%** (n=32) | 8.9% | **100.0%±0.0%** (n=32) | 17.9% |
| 5. VST+ST | 17 | **100.0%±0.0%** (n=17) | 7.7% | **100.0%±0.0%** (n=17) | 13.0% | **100.0%±0.0%** (n=17) | 21.0% |
| 6. ST+LT | 6 | **100.0%±0.0% ⚠️LOW** (n=6) | 10.6% | **100.0%±0.0% ⚠️LOW** (n=6) | 14.0% | **100.0%±0.0% ⚠️LOW** (n=6) | 14.0% |
| 7. LT+VLT | 11 | **100.0%±0.0%** (n=11) | 17.0% | **100.0%±0.0%** (n=11) | 17.0% | **100.0%±0.0%** (n=11) | 17.0% |
| 8. All-4 Agree | 28 | **100.0%±0.0%** (n=28) | 5.0% | **100.0%±0.0%** (n=28) | 6.5% | **100.0%±0.0%** (n=28) | 16.4% |

### TSLA (MOMENTUM)

- **Bars:** 632 | **Period:** 2024-11-20 → 2026-03-03
- **Windows:** [30, 60, 120] bars | **Bull threshold:** 15% | **Bear threshold:** -15%
- **LOI threshold used:** -45

**Stage Distribution:**
  - MIXED: 250 bars (39.6%)
  - S2: 175 bars (27.7%)
  - S2_early: 1 bars (0.2%)
  - S2_to_3: 16 bars (2.5%)
  - S3: 1 bars (0.2%)
  - S3_to_4: 9 bars (1.4%)
  - S4: 149 bars (23.6%)
  - S4_to_1: 31 bars (4.9%)

#### Bullish Signal Accuracy

| # | Approach | N | Acc@30b | MAE@30b | Acc@60b | MAE@60b | Acc@120b | MAE@120b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 32 | 31.2%±16.1% (n=32) | -8.3% | 37.5%±16.8% (n=32) | -11.1% | 53.1%±17.3% (n=32) | -11.4% |
| 2. ST Only | 20 | 30.0%±20.1% (n=20) | -5.1% | 50.0%±21.9% (n=20) | -5.1% | 70.0%±20.1% (n=20) | -7.4% |
| 3. LT Only | 15 | 33.3%±23.9% (n=15) | -5.6% | 33.3%±23.9% (n=15) | -7.7% | 60.0%±24.8% (n=15) | -7.7% |
| 4. VLT Only | 26 | 19.2%±15.1% (n=26) | -6.7% | 46.2%±19.2% (n=26) | -7.3% | 65.4%±18.3% (n=26) | -8.3% |
| 5. VST+ST | 11 | 27.3%±26.3% (n=11) | -5.8% | 54.5%±29.4% (n=11) | -9.2% | 63.6%±28.4% (n=11) | -9.6% |
| 6. ST+LT | 4 | 25.0%±42.4% ⚠️INSUF (n=4) | -9.1% | 25.0%±42.4% ⚠️INSUF (n=4) | -10.0% | 25.0%±42.4% ⚠️INSUF (n=4) | -10.8% |
| 7. LT+VLT | 5 | 0.0%±0.0% ⚠️LOW (n=5) | -5.5% | 0.0%±0.0% ⚠️LOW (n=5) | -5.6% | 40.0%±42.9% ⚠️LOW (n=5) | -5.6% |
| 8. All-4 Agree | 18 | **50.0%±23.1%** (n=18) | -4.7% | **61.1%±22.5%** (n=18) | -4.7% | **77.8%±19.2%** (n=18) | -5.2% |
| 9. MIXED (Gavin's) | 2 | 50.0%±69.3% ⚠️INSUF (n=2) | -15.2% | 100.0%±0.0% ⚠️INSUF (n=2) | -15.2% | 100.0%±0.0% ⚠️INSUF (n=2) | -15.2% |
| 10. LOI Threshold | 1 | 100.0%±0.0% ⚠️INSUF (n=1) | -2.2% | 100.0%±0.0% ⚠️INSUF (n=1) | -3.8% | 100.0%±0.0% ⚠️INSUF (n=1) | -3.8% |
| 11. LOI Trough | 43 | 37.2%±14.4% (n=43) | -1.1% | 48.8%±14.9% (n=43) | -5.4% | 69.8%±13.7% (n=43) | -5.4% |

#### Bearish Signal Accuracy

| # | Approach | N | Acc@30b | MAE@30b | Acc@60b | MAE@60b | Acc@120b | MAE@120b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 36 | **100.0%±0.0%** (n=36) | 7.6% | **100.0%±0.0%** (n=36) | 10.2% | **100.0%±0.0%** (n=36) | 16.3% |
| 2. ST Only | 19 | **100.0%±0.0%** (n=19) | 8.0% | **100.0%±0.0%** (n=19) | 11.1% | **100.0%±0.0%** (n=19) | 17.5% |
| 3. LT Only | 16 | **100.0%±0.0%** (n=16) | 14.5% | **100.0%±0.0%** (n=16) | 17.7% | **100.0%±0.0%** (n=16) | 23.9% |
| 4. VLT Only | 26 | **100.0%±0.0%** (n=26) | 7.7% | **100.0%±0.0%** (n=26) | 10.5% | **100.0%±0.0%** (n=26) | 15.6% |
| 5. VST+ST | 13 | **100.0%±0.0%** (n=13) | 10.0% | **100.0%±0.0%** (n=13) | 11.3% | **100.0%±0.0%** (n=13) | 17.5% |
| 6. ST+LT | 7 | **100.0%±0.0% ⚠️LOW** (n=7) | 13.2% | **100.0%±0.0% ⚠️LOW** (n=7) | 15.3% | **100.0%±0.0% ⚠️LOW** (n=7) | 15.3% |
| 7. LT+VLT | 6 | **100.0%±0.0% ⚠️LOW** (n=6) | 5.9% | **100.0%±0.0% ⚠️LOW** (n=6) | 9.1% | **100.0%±0.0% ⚠️LOW** (n=6) | 12.3% |
| 8. All-4 Agree | 16 | **100.0%±0.0%** (n=16) | 4.6% | **100.0%±0.0%** (n=16) | 14.3% | **100.0%±0.0%** (n=16) | 14.9% |

### IBIT (BTC_CORRELATED)

- **Bars:** 634 | **Period:** 2024-11-19 → 2026-03-03
- **Windows:** [30, 60, 120] bars | **Bull threshold:** 12% | **Bear threshold:** -12%
- **LOI threshold used:** -40

**Stage Distribution:**
  - MIXED: 292 bars (46.1%)
  - S2: 122 bars (19.2%)
  - S2_to_3: 5 bars (0.8%)
  - S3: 1 bars (0.2%)
  - S3_to_4: 6 bars (0.9%)
  - S4: 197 bars (31.1%)
  - S4_to_1: 11 bars (1.7%)

#### Bullish Signal Accuracy

| # | Approach | N | Acc@30b | MAE@30b | Acc@60b | MAE@60b | Acc@120b | MAE@120b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 46 | 8.7%±8.1% (n=46) | -5.7% | 19.6%±11.5% (n=46) | -8.0% | 30.4%±13.3% (n=46) | -17.5% |
| 2. ST Only | 26 | 11.5%±12.3% (n=26) | -7.2% | 15.4%±13.9% (n=26) | -8.4% | 19.2%±15.1% (n=26) | -22.0% |
| 3. LT Only | 23 | **43.5%±20.3%** (n=23) | -2.4% | **60.9%±19.9%** (n=23) | -2.8% | 60.9%±19.9% (n=23) | -2.8% |
| 4. VLT Only | 26 | 3.8%±7.4% (n=26) | -6.5% | 11.5%±12.3% (n=26) | -8.2% | 19.2%±15.1% (n=26) | -21.8% |
| 5. VST+ST | 22 | 4.5%±8.7% (n=22) | -7.7% | 9.1%±12.0% (n=22) | -9.0% | 13.6%±14.3% (n=22) | -22.5% |
| 6. ST+LT | 5 | 0.0%±0.0% ⚠️LOW (n=5) | -7.2% | 0.0%±0.0% ⚠️LOW (n=5) | -7.4% | 0.0%±0.0% ⚠️LOW (n=5) | -20.2% |
| 7. LT+VLT | 7 | 0.0%±0.0% ⚠️LOW (n=7) | -4.8% | 14.3%±25.9% ⚠️LOW (n=7) | -7.3% | 28.6%±33.5% ⚠️LOW (n=7) | -9.9% |
| 8. All-4 Agree | 27 | 18.5%±14.7% (n=27) | -4.8% | 29.6%±17.2% (n=27) | -7.9% | 33.3%±17.8% (n=27) | -9.9% |
| 11. LOI Trough | 37 | 27.0%±14.3% (n=37) | -4.8% | 54.1%±16.1% (n=37) | -6.2% | **67.6%±15.1%** (n=37) | -8.9% |

#### Bearish Signal Accuracy

| # | Approach | N | Acc@30b | MAE@30b | Acc@60b | MAE@60b | Acc@120b | MAE@120b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 49 | **100.0%±0.0%** (n=49) | 5.2% | **100.0%±0.0%** (n=49) | 9.4% | **100.0%±0.0%** (n=49) | 10.5% |
| 2. ST Only | 33 | **100.0%±0.0%** (n=33) | 4.8% | **100.0%±0.0%** (n=33) | 6.0% | **100.0%±0.0%** (n=33) | 8.5% |
| 3. LT Only | 21 | **100.0%±0.0%** (n=21) | 8.0% | **100.0%±0.0%** (n=21) | 13.8% | **100.0%±0.0%** (n=21) | 16.9% |
| 4. VLT Only | 36 | **100.0%±0.0%** (n=36) | 4.2% | **100.0%±0.0%** (n=36) | 5.9% | **100.0%±0.0%** (n=36) | 8.8% |
| 5. VST+ST | 26 | **100.0%±0.0%** (n=26) | 4.5% | **100.0%±0.0%** (n=26) | 5.0% | **100.0%±0.0%** (n=26) | 7.8% |
| 6. ST+LT | 9 | **100.0%±0.0% ⚠️LOW** (n=9) | 3.7% | **100.0%±0.0% ⚠️LOW** (n=9) | 5.3% | **100.0%±0.0% ⚠️LOW** (n=9) | 11.6% |
| 7. LT+VLT | 12 | **100.0%±0.0%** (n=12) | 4.8% | **100.0%±0.0%** (n=12) | 9.0% | **100.0%±0.0%** (n=12) | 10.5% |
| 8. All-4 Agree | 28 | **100.0%±0.0%** (n=28) | 4.2% | **100.0%±0.0%** (n=28) | 5.5% | **100.0%±0.0%** (n=28) | 11.4% |

### SPY (MR)

- **Bars:** 634 | **Period:** 2024-11-19 → 2026-03-03
- **Windows:** [20, 40, 80] bars | **Bull threshold:** 6% | **Bear threshold:** -6%
- **LOI threshold used:** -40

**Stage Distribution:**
  - MIXED: 270 bars (42.6%)
  - S2: 192 bars (30.3%)
  - S2_to_3: 12 bars (1.9%)
  - S3_to_4: 6 bars (0.9%)
  - S4: 139 bars (21.9%)
  - S4_to_1: 15 bars (2.4%)

#### Bullish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 43 | 0.0%±0.0% (n=43) | -1.1% | 4.7%±6.3% (n=43) | -1.7% | 23.3%±12.6% (n=43) | -2.5% |
| 2. ST Only | 37 | 2.7%±5.2% (n=37) | -0.7% | 8.1%±8.8% (n=37) | -1.3% | 27.0%±14.3% (n=37) | -1.5% |
| 3. LT Only | 15 | 0.0%±0.0% (n=15) | -1.3% | 6.7%±12.6% (n=15) | -1.8% | 20.0%±20.2% (n=15) | -2.1% |
| 4. VLT Only | 38 | 2.6%±5.1% (n=38) | -0.4% | 7.9%±8.6% (n=38) | -1.0% | 21.1%±13.0% (n=38) | -1.1% |
| 5. VST+ST | 24 | 0.0%±0.0% (n=24) | -1.1% | 4.2%±8.0% (n=24) | -1.4% | 16.7%±14.9% (n=24) | -2.3% |
| 6. ST+LT | 7 | 0.0%±0.0% ⚠️LOW (n=7) | -1.0% | **14.3%±25.9% ⚠️LOW** (n=7) | -1.3% | **28.6%±33.5% ⚠️LOW** (n=7) | -1.5% |
| 7. LT+VLT | 6 | 0.0%±0.0% ⚠️LOW (n=6) | -0.2% | 0.0%±0.0% ⚠️LOW (n=6) | -1.1% | 16.7%±29.8% ⚠️LOW (n=6) | -1.9% |
| 8. All-4 Agree | 34 | 0.0%±0.0% (n=34) | -1.1% | 2.9%±5.7% (n=34) | -1.4% | 14.7%±11.9% (n=34) | -1.5% |
| 11. LOI Trough | 40 | **5.0%±6.8%** (n=40) | -0.4% | 7.5%±8.2% (n=40) | -0.4% | 25.0%±13.4% (n=40) | -1.5% |

#### Bearish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 41 | **100.0%±0.0%** (n=41) | 1.7% | **100.0%±0.0%** (n=41) | 2.8% | **100.0%±0.0%** (n=41) | 4.1% |
| 2. ST Only | 29 | **100.0%±0.0%** (n=29) | 1.7% | **100.0%±0.0%** (n=29) | 2.8% | **100.0%±0.0%** (n=29) | 4.6% |
| 3. LT Only | 13 | **100.0%±0.0%** (n=13) | 1.1% | **100.0%±0.0%** (n=13) | 2.2% | **100.0%±0.0%** (n=13) | 2.2% |
| 4. VLT Only | 26 | **100.0%±0.0%** (n=26) | 2.0% | **100.0%±0.0%** (n=26) | 2.8% | **100.0%±0.0%** (n=26) | 4.0% |
| 5. VST+ST | 22 | **100.0%±0.0%** (n=22) | 1.6% | **100.0%±0.0%** (n=22) | 2.6% | **100.0%±0.0%** (n=22) | 4.6% |
| 6. ST+LT | 4 | 100.0%±0.0% ⚠️INSUF (n=4) | 2.5% | 100.0%±0.0% ⚠️INSUF (n=4) | 2.9% | 100.0%±0.0% ⚠️INSUF (n=4) | 4.5% |
| 7. LT+VLT | 7 | **100.0%±0.0% ⚠️LOW** (n=7) | 1.5% | **100.0%±0.0% ⚠️LOW** (n=7) | 2.2% | **100.0%±0.0% ⚠️LOW** (n=7) | 2.4% |
| 8. All-4 Agree | 22 | **100.0%±0.0%** (n=22) | 2.5% | **100.0%±0.0%** (n=22) | 3.1% | **100.0%±0.0%** (n=22) | 3.8% |

### QQQ (MR)

- **Bars:** 634 | **Period:** 2024-11-19 → 2026-03-03
- **Windows:** [20, 40, 80] bars | **Bull threshold:** 6% | **Bear threshold:** -6%
- **LOI threshold used:** -40

**Stage Distribution:**
  - MIXED: 243 bars (38.3%)
  - S2: 207 bars (32.6%)
  - S2_early: 1 bars (0.2%)
  - S2_to_3: 12 bars (1.9%)
  - S3: 2 bars (0.3%)
  - S3_to_4: 14 bars (2.2%)
  - S4: 144 bars (22.7%)
  - S4_to_1: 11 bars (1.7%)

#### Bullish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 37 | 5.4%±7.3% (n=37) | -1.1% | 13.5%±11.0% (n=37) | -1.5% | **51.4%±16.1%** (n=37) | -1.9% |
| 2. ST Only | 33 | 3.0%±5.8% (n=33) | -0.9% | 6.1%±8.1% (n=33) | -1.5% | 39.4%±16.7% (n=33) | -1.9% |
| 3. LT Only | 18 | **11.1%±14.5%** (n=18) | -2.2% | **22.2%±19.2%** (n=18) | -3.8% | 27.8%±20.7% (n=18) | -4.7% |
| 4. VLT Only | 41 | 2.4%±4.7% (n=41) | -0.9% | 9.8%±9.1% (n=41) | -1.5% | 41.5%±15.1% (n=41) | -1.6% |
| 5. VST+ST | 22 | 0.0%±0.0% (n=22) | -1.5% | 4.5%±8.7% (n=22) | -1.8% | 31.8%±19.5% (n=22) | -2.3% |
| 6. ST+LT | 7 | 0.0%±0.0% ⚠️LOW (n=7) | -2.1% | 0.0%±0.0% ⚠️LOW (n=7) | -5.1% | 0.0%±0.0% ⚠️LOW (n=7) | -10.7% |
| 7. LT+VLT | 7 | 0.0%±0.0% ⚠️LOW (n=7) | -0.9% | 14.3%±25.9% ⚠️LOW (n=7) | -0.9% | 28.6%±33.5% ⚠️LOW (n=7) | -2.6% |
| 8. All-4 Agree | 37 | 5.4%±7.3% (n=37) | -1.3% | 5.4%±7.3% (n=37) | -1.5% | 35.1%±15.4% (n=37) | -1.6% |
| 11. LOI Trough | 54 | 5.6%±6.1% (n=54) | -1.2% | 16.7%±9.9% (n=54) | -1.5% | 42.6%±13.2% (n=54) | -2.4% |

#### Bearish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 35 | **100.0%±0.0%** (n=35) | 3.4% | **100.0%±0.0%** (n=35) | 3.4% | **100.0%±0.0%** (n=35) | 5.6% |
| 2. ST Only | 34 | **100.0%±0.0%** (n=34) | 2.1% | **100.0%±0.0%** (n=34) | 3.2% | **100.0%±0.0%** (n=34) | 5.6% |
| 3. LT Only | 20 | **100.0%±0.0%** (n=20) | 2.4% | **100.0%±0.0%** (n=20) | 3.2% | **100.0%±0.0%** (n=20) | 4.0% |
| 4. VLT Only | 38 | **100.0%±0.0%** (n=38) | 2.5% | **100.0%±0.0%** (n=38) | 3.3% | **100.0%±0.0%** (n=38) | 5.4% |
| 5. VST+ST | 18 | **100.0%±0.0%** (n=18) | 2.3% | **100.0%±0.0%** (n=18) | 2.9% | **100.0%±0.0%** (n=18) | 5.2% |
| 6. ST+LT | 8 | **100.0%±0.0% ⚠️LOW** (n=8) | 1.6% | **100.0%±0.0% ⚠️LOW** (n=8) | 2.7% | **100.0%±0.0% ⚠️LOW** (n=8) | 2.7% |
| 7. LT+VLT | 12 | **100.0%±0.0%** (n=12) | 2.6% | **100.0%±0.0%** (n=12) | 3.2% | **100.0%±0.0%** (n=12) | 3.7% |
| 8. All-4 Agree | 25 | **100.0%±0.0%** (n=25) | 3.1% | **100.0%±0.0%** (n=25) | 3.4% | **100.0%±0.0%** (n=25) | 4.7% |

### IWM (MR)

- **Bars:** 634 | **Period:** 2024-11-19 → 2026-03-03
- **Windows:** [20, 40, 80] bars | **Bull threshold:** 6% | **Bear threshold:** -6%
- **LOI threshold used:** -40

**Stage Distribution:**
  - MIXED: 261 bars (41.2%)
  - S2: 189 bars (29.8%)
  - S2_to_3: 10 bars (1.6%)
  - S3_to_4: 6 bars (0.9%)
  - S4: 149 bars (23.5%)
  - S4_to_1: 19 bars (3.0%)

#### Bullish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 35 | 2.9%±5.5% (n=35) | -1.5% | 28.6%±15.0% (n=35) | -2.5% | 54.3%±16.5% (n=35) | -3.8% |
| 2. ST Only | 34 | 8.8%±9.5% (n=34) | -2.3% | 20.6%±13.6% (n=34) | -3.2% | 52.9%±16.8% (n=34) | -4.0% |
| 3. LT Only | 29 | 10.3%±11.1% (n=29) | -1.7% | 27.6%±16.3% (n=29) | -2.1% | 55.2%±18.1% (n=29) | -2.1% |
| 4. VLT Only | 35 | 5.7%±7.7% (n=35) | -2.0% | 17.1%±12.5% (n=35) | -3.6% | 48.6%±16.6% (n=35) | -5.1% |
| 5. VST+ST | 21 | 4.8%±9.1% (n=21) | -2.8% | 14.3%±15.0% (n=21) | -3.8% | 52.4%±21.4% (n=21) | -3.8% |
| 6. ST+LT | 11 | 0.0%±0.0% (n=11) | -2.0% | 27.3%±26.3% (n=11) | -2.1% | 45.5%±29.4% (n=11) | -5.9% |
| 7. LT+VLT | 8 | 0.0%±0.0% ⚠️LOW (n=8) | -1.7% | 12.5%±22.9% ⚠️LOW (n=8) | -1.7% | **62.5%±33.5% ⚠️LOW** (n=8) | -1.7% |
| 8. All-4 Agree | 36 | 2.8%±5.4% (n=36) | -1.6% | 13.9%±11.3% (n=36) | -2.1% | 61.1%±15.9% (n=36) | -2.1% |
| 9. MIXED (Gavin's) | 4 | 25.0%±42.4% ⚠️INSUF (n=4) | -1.8% | 75.0%±42.4% ⚠️INSUF (n=4) | -1.8% | 75.0%±42.4% ⚠️INSUF (n=4) | -1.8% |
| 11. LOI Trough | 43 | **14.0%±10.4%** (n=43) | -1.8% | **34.9%±14.2%** (n=43) | -2.8% | 51.2%±14.9% (n=43) | -3.3% |

#### Bearish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 38 | **100.0%±0.0%** (n=38) | 2.4% | **100.0%±0.0%** (n=38) | 4.2% | **100.0%±0.0%** (n=38) | 7.2% |
| 2. ST Only | 34 | **100.0%±0.0%** (n=34) | 2.1% | **100.0%±0.0%** (n=34) | 3.8% | **100.0%±0.0%** (n=34) | 7.5% |
| 3. LT Only | 25 | **100.0%±0.0%** (n=25) | 2.2% | **100.0%±0.0%** (n=25) | 2.5% | **100.0%±0.0%** (n=25) | 4.4% |
| 4. VLT Only | 35 | **100.0%±0.0%** (n=35) | 2.4% | **100.0%±0.0%** (n=35) | 3.2% | **100.0%±0.0%** (n=35) | 5.4% |
| 5. VST+ST | 23 | **100.0%±0.0%** (n=23) | 2.0% | **100.0%±0.0%** (n=23) | 4.1% | **100.0%±0.0%** (n=23) | 6.6% |
| 6. ST+LT | 10 | **100.0%±0.0%** (n=10) | 2.4% | **100.0%±0.0%** (n=10) | 2.8% | **100.0%±0.0%** (n=10) | 5.1% |
| 7. LT+VLT | 10 | **100.0%±0.0%** (n=10) | 2.4% | **100.0%±0.0%** (n=10) | 2.8% | **100.0%±0.0%** (n=10) | 5.1% |
| 8. All-4 Agree | 26 | **100.0%±0.0%** (n=26) | 2.0% | **100.0%±0.0%** (n=26) | 2.4% | **100.0%±0.0%** (n=26) | 4.7% |

### GLD (TRENDING)

- **Bars:** 634 | **Period:** 2024-11-19 → 2026-03-03
- **Windows:** [20, 40, 80] bars | **Bull threshold:** 8% | **Bear threshold:** -8%
- **LOI threshold used:** -40

**Stage Distribution:**
  - MIXED: 248 bars (39.1%)
  - S2: 256 bars (40.4%)
  - S2_to_3: 10 bars (1.6%)
  - S3: 3 bars (0.5%)
  - S3_to_4: 8 bars (1.3%)
  - S4: 99 bars (15.6%)
  - S4_to_1: 10 bars (1.6%)

#### Bullish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 37 | 2.7%±5.2% (n=37) | -1.3% | 24.3%±13.8% (n=37) | -1.3% | 64.9%±15.4% (n=37) | -1.3% |
| 2. ST Only | 30 | 3.3%±6.4% (n=30) | -1.6% | 23.3%±15.1% (n=30) | -2.1% | 63.3%±17.2% (n=30) | -2.2% |
| 3. LT Only | 33 | 6.1%±8.1% (n=33) | -1.2% | 18.2%±13.2% (n=33) | -1.3% | 57.6%±16.9% (n=33) | -1.4% |
| 4. VLT Only | 34 | 2.9%±5.7% (n=34) | -1.3% | 29.4%±15.3% (n=34) | -2.1% | 67.6%±15.7% (n=34) | -2.2% |
| 5. VST+ST | 22 | 4.5%±8.7% (n=22) | -1.3% | 18.2%±16.1% (n=22) | -1.7% | 63.6%±20.1% (n=22) | -1.8% |
| 6. ST+LT | 14 | 0.0%±0.0% (n=14) | -0.5% | 14.3%±18.3% (n=14) | -1.7% | 50.0%±26.2% (n=14) | -1.7% |
| 7. LT+VLT | 16 | **6.2%±11.9%** (n=16) | -2.5% | 25.0%±21.2% (n=16) | -3.0% | 50.0%±24.5% (n=16) | -3.0% |
| 8. All-4 Agree | 32 | 3.1%±6.0% (n=32) | -2.3% | 21.9%±14.3% (n=32) | -2.7% | 62.5%±16.8% (n=32) | -2.9% |
| 11. LOI Trough | 45 | 2.2%±4.3% (n=45) | -0.4% | **31.1%±13.5%** (n=45) | -0.4% | **82.2%±11.2%** (n=45) | -0.6% |

#### Bearish Signal Accuracy

| # | Approach | N | Acc@20b | MAE@20b | Acc@40b | MAE@40b | Acc@80b | MAE@80b |
|---|---------|---|---|---|---|---|---|---|
| 1. VST Only | 34 | **100.0%±0.0%** (n=34) | 3.3% | **100.0%±0.0%** (n=34) | 4.2% | **100.0%±0.0%** (n=34) | 10.3% |
| 2. ST Only | 27 | **100.0%±0.0%** (n=27) | 2.3% | **100.0%±0.0%** (n=27) | 3.9% | **100.0%±0.0%** (n=27) | 10.6% |
| 3. LT Only | 23 | **100.0%±0.0%** (n=23) | 4.2% | **100.0%±0.0%** (n=23) | 6.2% | **100.0%±0.0%** (n=23) | 8.3% |
| 4. VLT Only | 33 | **100.0%±0.0%** (n=33) | 2.8% | **100.0%±0.0%** (n=33) | 4.9% | **100.0%±0.0%** (n=33) | 10.6% |
| 5. VST+ST | 19 | **100.0%±0.0%** (n=19) | 3.4% | **100.0%±0.0%** (n=19) | 6.2% | **100.0%±0.0%** (n=19) | 13.1% |
| 6. ST+LT | 11 | **100.0%±0.0%** (n=11) | 3.7% | **100.0%±0.0%** (n=11) | 4.2% | **100.0%±0.0%** (n=11) | 6.1% |
| 7. LT+VLT | 12 | **100.0%±0.0%** (n=12) | 2.8% | **100.0%±0.0%** (n=12) | 4.4% | **100.0%±0.0%** (n=12) | 10.0% |
| 8. All-4 Agree | 25 | **100.0%±0.0%** (n=25) | 3.4% | **100.0%±0.0%** (n=25) | 4.5% | **100.0%±0.0%** (n=25) | 9.4% |

---
## Section 3: Cross-Asset Signal Comparison

### Bullish Signal Rankings — Cross-Asset Average Accuracy (All Windows)

| Approach | W1 Avg | W2 Avg | W3 Avg | Overall | Assets (n≥5) |
|---------|--------|--------|--------|---------|-------------|
| 11. LOI Trough | 16.6% | 32.9% | 56.4% | **35.3%** | 7/7 |
| 3. LT Only | 18.3% | 29.2% | 46.1% | **31.2%** | 7/7 |
| 8. All-4 Agree | 14.3% | 23.6% | 45.7% | **27.8%** | 7/7 |
| 1. VST Only | 11.0% | 23.4% | 45.1% | **26.5%** | 7/7 |
| 2. ST Only | 11.6% | 22.0% | 45.7% | **26.4%** | 7/7 |
| 4. VLT Only | 8.6% | 21.7% | 43.8% | **24.7%** | 7/7 |
| 5. VST+ST | 11.4% | 20.5% | 42.2% | **24.7%** | 7/7 |
| 7. LT+VLT | 4.1% | 14.2% | 38.7% | **19.0%** | 7/7 |
| 6. ST+LT | 4.8% | 16.5% | 30.2% | **17.1%** | 6/7 |
| 9. MIXED (Gavin's) | N/A | N/A | N/A | **nan%** | 0/7 |
| 10. LOI Threshold | N/A | N/A | N/A | **nan%** | 0/7 |

### Interpretation

**Top 3 Bullish Approaches by Cross-Asset Average Accuracy:**
1. **11. LOI Trough** (35.3% avg) — works across 7/7 assets with sufficient sample size
2. **3. LT Only** (31.2% avg) — works across 7/7 assets with sufficient sample size
3. **8. All-4 Agree** (27.8% avg) — works across 7/7 assets with sufficient sample size

### Single-TF Deep Dive

| TF | Avg Bull Acc | Avg Bear Acc | Signal Frequency | Notes |
|-----|------------|------------|-----------------|-------|
| VST | 45.1% | 100.0% | 5.9% of bars | Highest frequency, noisiest |
| ST | 45.7% | 100.0% | 4.6% of bars | Balanced frequency/accuracy |
| LT | 46.1% | 100.0% | 3.4% of bars | Lower freq, higher accuracy |
| VLT | 43.8% | 100.0% | 5.2% of bars | Slowest signal, highest conviction |

---
## Section 4: Stage Transition Timing Analysis

Lead time = bars from TF zero-crossing to actual price trough/peak.
Positive = signal fired **before** the price turning point (early/correct).
Negative = signal fired **after** the turning point (late/lagging).

### Bottom Transition (S4→1): Lead Times by TF

| Asset | VST Lead | ST Lead | LT Lead | VLT Lead | Best TF |
|-------|---------|--------|--------|---------|--------|
| MSTR | -10.0b | -20.0b | -20.0b | -24.0b | **VST** |
| TSLA | -17.0b | -23.0b | -26.0b | -19.0b | **VST** |
| IBIT | -16.5b | -16.5b | -26.0b | -16.5b | **VST** |
| SPY | -18.5b | -22.5b | -19.0b | -22.5b | **VST** |
| QQQ | -19.0b | -17.0b | -26.0b | -17.0b | **ST** |
| IWM | -25.0b | -25.0b | -25.0b | -19.0b | **VLT** |
| GLD | -28.0b | -28.0b | -18.5b | -25.5b | **LT** |

### Top Transition (S2→3): Lead Times by TF

| Asset | VST Lead | ST Lead | LT Lead | VLT Lead | Best TF |
|-------|---------|--------|--------|---------|--------|
| MSTR | -18.0b | -19.0b | -4.0b | -22.0b | **LT** |
| TSLA | -29.0b | -11.0b | -11.0b | -22.0b | **ST** |
| IBIT | -27.0b | -27.0b | -15.0b | -27.0b | **LT** |
| SPY | -22.0b | -22.0b | -9.0b | -22.0b | **LT** |
| QQQ | -21.0b | -16.0b | -9.0b | -19.0b | **LT** |
| IWM | -24.0b | -29.0b | -29.5b | -29.0b | **VST** |
| GLD | -25.0b | -24.0b | -22.0b | -25.0b | **LT** |

### Average Stage Duration by Asset Class

| Asset | S4 Avg (bars) | S1 Avg (bars) | S2 Avg (bars) | S3 Avg (bars) | MIXED % |
|-------|-------------|-------------|-------------|-------------|--------|
| MSTR | 273 (42.3%) | 0 (0.0%) | 120 (18.6%) | 27 (4.2%) | 34.9% |
| TSLA | 180 (28.5%) | 0 (0.0%) | 176 (27.8%) | 26 (4.1%) | 39.6% |
| IBIT | 208 (32.8%) | 0 (0.0%) | 122 (19.2%) | 12 (1.9%) | 46.1% |
| SPY | 154 (24.3%) | 0 (0.0%) | 192 (30.3%) | 18 (2.8%) | 42.6% |
| QQQ | 155 (24.4%) | 0 (0.0%) | 208 (32.8%) | 28 (4.4%) | 38.3% |
| IWM | 168 (26.5%) | 0 (0.0%) | 189 (29.8%) | 16 (2.5%) | 41.2% |
| GLD | 109 (17.2%) | 0 (0.0%) | 256 (40.4%) | 21 (3.3%) | 39.1% |

---
## Section 5: LOI vs Composite Analysis

LOI = VLT_SRIBI×40% + VLT_acceleration×30% + LT_SRIBI×15% + Concordance×15%
Design goal: detect deep oversold bottoms for AB3 LEAP entry.

### LOI Threshold Performance vs Single TF (Bullish Accuracy at Longest Window)

| Asset | Class | LOI Thr | LOI Acc | VST Acc | ST Acc | LT Acc | VLT Acc | LOI vs Best-TF |
|-------|-------|---------|--------|--------|--------|--------|--------|--------------|
| MSTR | MOMENTUM | -45 | N/A | 38.7% | 47.8% | 41.2% | 43.3% | — |
| TSLA | MOMENTUM | -45 | 100.0% (n=1) | 53.1% | 70.0% | 60.0% | 65.4% | +30.0% 🟢 |
| IBIT | BTC_CORRELATED | -40 | N/A | 30.4% | 19.2% | 60.9% | 19.2% | No signals |
| SPY | MR | -40 | N/A | 23.3% | 27.0% | 20.0% | 21.1% | No signals |
| QQQ | MR | -40 | N/A | 51.4% | 39.4% | 27.8% | 41.5% | No signals |
| IWM | MR | -40 | N/A | 54.3% | 52.9% | 55.2% | 48.6% | No signals |
| GLD | TRENDING | -40 | N/A | 64.9% | 63.3% | 57.6% | 67.6% | No signals |

### LOI Trough vs LOI Threshold

| Asset | Trough Acc | Trough n | Threshold Acc | Threshold n | Winner |
|-------|-----------|---------|-------------|-----------|--------|
| MSTR | N/A (n=0) | 0 | 0.0% (n=2) | 2 | — |
| TSLA | N/A (n=0) | 0 | 100.0% (n=1) | 1 | **Threshold** (no trough signals) |
| IBIT | N/A (n=0) | 0 | N/A (n=0) | 0 | — |
| SPY | N/A (n=0) | 0 | N/A (n=0) | 0 | — |
| QQQ | N/A (n=0) | 0 | N/A (n=0) | 0 | — |
| IWM | N/A (n=0) | 0 | N/A (n=0) | 0 | — |
| GLD | N/A (n=0) | 0 | N/A (n=0) | 0 | — |

### Optimal LOI Threshold Analysis

For MOMENTUM assets (MSTR/TSLA), current threshold = -45.
For MR/TRENDING/BTC_CORRELATED assets, current threshold = -40.

**MSTR:** LOI<-45 → 0.0% (n=2) | LOI<-40 → 0.0% (n=2)
**TSLA:** LOI<-45 → 100.0% (n=1) | LOI<-40 → 100.0% (n=1)

---
## Section 6: Failure Mode Analysis

### False Positive Rates by TF and Asset

*(False positive = price moved >5% against signal direction within the window)*

| Asset | VST FPR | ST FPR | LT FPR | VLT FPR | MIXED FPR | LOI FPR |
|-------|--------|--------|--------|--------|----------|--------|
| MSTR | 96.8% | 95.7% | 94.1% | 96.7% | 100.0% | 100.0% |
| TSLA | 81.2% | 60.0% | 66.7% | 69.2% | 100.0% | 0.0% |
| IBIT | 82.6% | 88.5% | 43.5% | 84.6% | N/A | N/A |
| SPY | 25.6% | 21.6% | 20.0% | 18.4% | N/A | N/A |
| QQQ | 24.3% | 21.2% | 50.0% | 17.1% | N/A | N/A |
| IWM | 48.6% | 47.1% | 37.9% | 51.4% | 25.0% | N/A |
| GLD | 0.0% | 3.3% | 3.0% | 2.9% | N/A | N/A |

### Key Failure Patterns

**VST Failure Modes:**
- High chop rate: VST crosses zero dozens of times per year, most are noise
- Whipsaws in range-bound markets cause serial false signals
- VST alone has no regime filter — fires regardless of LT/VLT context

**ST Failure Modes:**
- Counter-trend rallies in Stage 4 generate bullish ST crosses that fail
- Bear market bounces: ST+ while LT/VLT still negative often revert

**LT Failure Modes:**
- Late signals: LT crosses well after price has already moved
- Confirms direction but misses optimal entry by many bars

**VLT Failure Modes:**
- Extremely lagged: by the time VLT crosses, much of the move is done
- Low signal frequency limits statistical reliability

**MIXED Context Failure Modes:**
- Can persist for extended periods during prolonged Stage 4 recovery
- Does not filter for depth of oversold condition (no LOI floor)
- ST/VST can turn positive on weak bounces before real recovery

**LOI Failure Modes:**
- LOI formula is VLT-heavy (40%+30%=70% VLT components)
- In fast crashes, VLT doesn't have time to get deeply negative before bounce
- Threshold may be too deep (-45) for shorter-cycle assets

**Stage Machine Failures:**
- MIXED classification is ambiguous — not actionable
- S2_to_3 and S3_to_4 transition states overlap
- VLT neutrality (±5 band) causes state instability at boundaries

---
## Section 7: CIO Insights & Improvement Recommendations

### R1: TF Reweighting in LOI Formula

**Current:** LOI = VLT×40% + VLT_accel×30% + LT×15% + Concordance×15%
**Finding:** LT+VLT combined signals show strong accuracy but LOI over-weights VLT.
- VLT is a 70% component (direct + acceleration). This creates extreme lag in fast markets.
- ST component is completely absent from LOI formula despite strong single-TF accuracy.

**Recommendation:** Add ST component. Proposed: LOI_v2 = VLT×35% + VLT_accel×25% + LT×20% + ST×10% + Concordance×10%
  - LT+VLT combined accuracy: 38.7% avg across assets

### R2: MIXED Context as Complementary (Not Replacement) Signal

**Recommendation:** Use MIXED Context as Stage 1 watch trigger with LOI as final deployment gate.

### R3: Optimal AB3 Threshold Calibration

**Current thresholds:** MOMENTUM: -45 | MR: -40

**Analysis:**
- MSTR (MOMENTUM): 2 signals at current threshold, acc=0.0%
- TSLA (MOMENTUM): 1 signals at current threshold, acc=100.0%

**Recommendation:**
- If MOMENTUM signals are too infrequent (n<4 per year), lower threshold to -40
- If MOMENTUM signals have high accuracy (>70%) but low frequency, consider maintaining -45 as the main AB3 gate but using MIXED context for AB1/early accumulation
- MR assets: -40 appears appropriate given smaller amplitude moves
- TRENDING (GLD): consider -35 given more consistent trending behavior and smaller vol swings

### R4: False Positive Reduction

**Highest-impact filters to add:**

1. **Volume confirmation:** Require above-average volume on ST/VST cross bars
   - Rationale: False crosses in low-volume consolidation are systematic noise

2. **VLT trend filter:** For all bullish signals, require VLT > prior bar VLT (momentum improving)
   - Reduces false positives from dead-cat bounces where VLT is still accelerating down

3. **Minimum VST/ST spread:** Require VST > 5 AND ST > 0 (not just crossed zero)
   - Eliminates borderline crosses that quickly revert

4. **LOI momentum gate:** Only enter when LOI is rising (current bar LOI > prior bar LOI)
   - A LOI trough is more reliable when slope has turned positive

### R5: P-BEAR Signal Calibration

**Bear signal accuracy findings:**
- VST bearish crosses: high frequency, low accuracy — too noisy for short positioning
- LT/VLT bearish crosses: higher accuracy but significant lag (price already down 10-20%)
- S2_to_3 stage transition: best early warning, but confirmation requires full S3 state

**Recommendation for P-BEAR design:**
- Primary trigger: VST < 0 AND ST < 0 AND LT still > 0 (early distribution detection)
- Confirmation: LT turns negative (S3→S4 confirmed)
- Target instruments: Bear spreads with 60-90 DTE (not VLT lagged)
- Kill condition: any return to MIXED context after S3 designation

- For PMCC (AB2) short calls: S2_to_3 state should trigger max call-selling delta (≥0.35)
- Stage 3 confirmed: may warrant initiating bear put spreads (P-BEAR AB1 equivalent)

### R6: Stage Machine Enhancement Proposals

**1. Replace binary stage with confidence score:**
   Instead of hard sign(x) classification, use weighted score:
   `stage_strength = (VST×0.1 + ST×0.2 + LT×0.3 + VLT×0.4) / max_possible`
   - Smooths boundary instability
   - Enables graduated position sizing (larger at higher confidence)

**2. Add minimum duration filter:**
   Require stage designation to persist ≥3 bars before acting
   - Eliminates many VST-driven false transitions

**3. MIXED state clarification:**
   Sub-classify MIXED into:
   - MIXED_BULLISH: VST+ST positive, LT/VLT recovering (Gavin's MIXED entry)
   - MIXED_BEARISH: VST+ST negative, LT/VLT still positive
   - MIXED_CONFUSED: random sign pattern, no actionable bias

**4. Asset-class-specific neutral bands:**
   Current ±5 band applies to all assets equally.
   Proposal: MOMENTUM ±8, MR ±3, TRENDING ±5
   - Reduces noise signals for high-volatility MOMENTUM names
   - Increases sensitivity for low-volatility MR names

---
## Appendix: Statistical Notes

- All accuracy figures use maximum-gain-within-window methodology
  (i.e., did price hit the threshold AT ANY POINT in the window, not just at end)
- This is appropriate for options traders who can take profits at any point
- False positive rate defined as: price moved >5% against signal within window
- CI = 95% binomial confidence interval = ±1.96√(p(1-p)/n)
- Results with n<10 flagged LOW SAMPLE; n<5 flagged INSUFFICIENT DATA

---
*Report generated by Stage Designation Backtest Engine v1 | 2026-03-04*