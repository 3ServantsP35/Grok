# Indicators

## MR Hurdle Oscillator v1

File:
- `mr_hurdle_oscillator_v1.pine`

### Purpose
Estimate whether **SPY** deserves incremental capital over **STRC** on a regime-aware, risk-adjusted basis.

### Important limitation
This is **not** an AB3 SPY call LEAP trigger.

It only answers the upstream question:
- does SPY clear STRC?

Expression choice remains separate.

### Symbols used by default
- `AMEX:SPY`
- `AMEX:RSP`
- `AMEX:IWM`
- `AMEX:HYG`
- `NASDAQ:IEF`
- `CBOE:VIX`

### User input to review carefully
- `STRC Annual Hurdle (decimal)`

Default is `0.08` for now.
This is a placeholder assumption and should be reviewed by the user.

### What it scores
1. Macro proxy
2. SPY trend quality
3. Breadth / participation quality
4. Relative opportunity vs STRC hurdle
5. Volatility / downside asymmetry

### Output bands
- `<= -3` → STRC preferred
- `-3 to +3` → Neutral / no edge
- `>= +3` → SPY shares preferred
- `>= +7` → SPY aggressive expression eligible

### First testing goal
Check whether the indicator behaves directionally as expected on:
- daily timeframe
- weekly timeframe
- recent periods where broad-equity internals clearly improved or deteriorated

### Specific review questions
1. Do the posture shifts look broadly sensible?
2. Is the breadth block helping, or overpowering the composite?
3. Is the STRC hurdle input set at a sensible placeholder level?
4. Should macro be proxied differently before v2?
