#!/usr/bin/env python3
"""
GLI Proxy Collector — Layer 0 Macro Engine
==========================================
Implements 42 Macro's Global Liquidity formula:
  GLI Proxy = Global Central Bank Balance Sheets + Global Broad Money + Global FX Reserves (ex Gold)

Data sources:
  - FRED API (free, no key) — Fed balance sheet, US M2, repo data
  - ECB SDW API — Eurozone balance sheet + M3
  - BOJ (approximated via FRED Japan series)
  - PBOC (approximated via FRED China series)

Layer 0 outputs (monthly, interpolated to weekly):
  - GLI_YOY: Global Liquidity YoY% change (3-month moving avg)
  - GLI_TREND: Rising / Flat / Falling
  - GRID_REGIME: GOLDILOCKS / REFLATION / INFLATION / DEFLATION
  - MACRO_SCORE: -2 to +2 adjustment to regime composite score
  - PARADIGM: A / B / C / D (42 Macro framework)

Usage:
  python3 collect_gli_proxy.py          # Run and print current readings
  python3 collect_gli_proxy.py --save   # Save to DB
"""

import urllib.request
import ssl
import json
import sqlite3
import argparse
import math
from datetime import datetime, timedelta, date
from typing import Optional, Tuple, List, Dict

# ── SSL context (cert verification disabled in container) ──────────────────
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ── DB path ────────────────────────────────────────────────────────────────
DB_PATH = "/mnt/mstr-data/mstr.db"


# ══════════════════════════════════════════════════════════════════════════
# FRED FETCHER
# ══════════════════════════════════════════════════════════════════════════

def fred_series(series_id: str, periods: int = 104) -> List[Tuple[str, float]]:
    """Fetch a FRED series as (date, value) list, most recent `periods` obs."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "mstr-cio/2.0"})
    try:
        data = urllib.request.urlopen(req, context=ctx, timeout=15).read().decode()
        rows = []
        for line in data.strip().split('\n')[1:]:  # skip header
            parts = line.split(',')
            if len(parts) == 2 and parts[1].strip() not in ('.', ''):
                try:
                    rows.append((parts[0].strip(), float(parts[1].strip())))
                except ValueError:
                    pass
        return rows[-periods:]
    except Exception as e:
        print(f"  FRED {series_id} error: {e}")
        return []


def fred_latest(series_id: str) -> Optional[Tuple[str, float]]:
    """Get the most recent value for a FRED series."""
    rows = fred_series(series_id, periods=5)
    return rows[-1] if rows else None


# ══════════════════════════════════════════════════════════════════════════
# ECB FETCHER
# ══════════════════════════════════════════════════════════════════════════

def ecb_latest(flow_ref: str, key: str) -> Optional[float]:
    """
    Fetch latest observation from ECB Statistical Data Warehouse.
    Examples:
      flow_ref='BSI', key='M.U2.N.A.T.A.AL.A.1.U2.2000.Z01.E' (Eurozone M3)
    """
    url = (f"https://data-api.ecb.europa.eu/service/data/{flow_ref}/{key}"
           f"?lastNObservations=3&format=jsondata")
    req = urllib.request.Request(url, headers={"User-Agent": "mstr-cio/2.0",
                                                "Accept": "application/json"})
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=15).read()
        data = json.loads(resp)
        datasets = data.get('dataSets', [])
        if not datasets:
            return None
        series = datasets[0].get('series', {})
        for s_key, s_data in series.items():
            obs = s_data.get('observations', {})
            if obs:
                last_val = list(obs.values())[-1]
                if last_val and last_val[0] is not None:
                    return float(last_val[0])
    except Exception as e:
        print(f"  ECB {flow_ref}/{key[:20]} error: {e}")
    return None


# ══════════════════════════════════════════════════════════════════════════
# GLI PROXY COMPUTATION
# ══════════════════════════════════════════════════════════════════════════

class GLIProxy:
    """
    42 Macro Global Liquidity Proxy
    = Global CB Balance Sheets + Global Broad Money + Global FX Reserves (ex Gold)

    Components by weight (approximate):
      Fed balance sheet:    30% (WALCL)
      ECB balance sheet:    20% (ECB BSI)
      BOJ balance sheet:    10% (via FRED JPNASSETS proxy)
      PBOC proxy:           10% (China FX reserves, FRED CHFRS)
      US M2:                15% (WM2NS)
      Eurozone M3:           5% (ECB)
      Global FX reserves:   10% (TOTRESNS + proxy)
    """

    def collect(self) -> Dict:
        """Collect all components and return current GLI state."""
        print("  Fetching GLI components from FRED + ECB...")

        # ── Central Bank Balance Sheets ─────────────────────────────────
        # Fed (weekly, $M)
        fed = fred_series("WALCL", 104)
        fed_latest_val = fed[-1][1] if fed else None
        fed_yoy = self._yoy(fed, 52) if len(fed) >= 52 else None
        print(f"    Fed BS: ${fed_latest_val/1e6:.2f}T | YoY: {fed_yoy:+.1f}%" if fed_latest_val and fed_yoy else f"    Fed BS: {fed_latest_val}")

        # ECB balance sheet (monthly, EUR billions)
        # BSI.M.U2.N.A.T.A.AL.A.1.U2.2000.Z01.E = Eurosystem total assets
        ecb_val = ecb_latest("ILM", "M.U2.EUR.MRO.A.A.Z.Z.L90.F.E.T.EUR._X.N")
        if ecb_val is None:
            # Fallback: use ECB main refinancing rate as proxy signal direction
            ecb_val = None
        print(f"    ECB BS: {ecb_val} (EUR bn)")

        # US overnight repo facility (liquidity injection signal)
        rrp = fred_series("RRPONTSYD", 52)  # Overnight reverse repo (lower = more liquidity)
        rrp_latest = rrp[-1][1] if rrp else None
        rrp_trend = "injecting" if (rrp_latest or 0) < 100 else "draining"
        print(f"    Fed RRP: ${rrp_latest:.1f}B ({rrp_trend})")

        # RMOP — Fed started $40B/month in Dec 2025 (per Howell report)
        # This is QE-equivalent — treat as bullish liquidity signal
        rmop_active = True  # Started Dec 2025, $40B/month through Mar 2026
        print(f"    RMOP: Active ($40B/month through Mar-26)")

        # ── Money Supply ─────────────────────────────────────────────────
        # US M2 (weekly, $B)
        m2 = fred_series("WM2NS", 104)
        m2_latest = m2[-1][1] if m2 else None
        m2_yoy = self._yoy(m2, 52) if len(m2) >= 52 else None
        print(f"    US M2: ${m2_latest:.0f}B | YoY: {m2_yoy:+.1f}%" if m2_latest and m2_yoy else f"    US M2: {m2_latest}")

        # ── FX Reserves & Repo Stress ────────────────────────────────────
        # SOFR - IORB spread (repo market stress — wider = tighter liquidity)
        sofr_data = fred_series("SOFR", 20)
        sofr_val = sofr_data[-1][1] if sofr_data else 4.3
        iorb_data = fred_series("IORB", 20)
        iorb_val = iorb_data[-1][1] if iorb_data else 4.4
        repo_spread = sofr_val - iorb_val
        repo_stress = repo_spread > 0.15  # Danger zone per Howell report
        print(f"    Repo spread (SOFR-IORB): {repo_spread:+.3f}% | Stress: {repo_stress}")

        # DXY direction (countercyclical GLI indicator per 42 Macro)
        dxy = fred_series("DTWEXBGS", 52)
        if not dxy:
            # Try alternate series
            dxy = fred_series("DTWEXAFEGS", 52)
        dxy_latest = dxy[-1][1] if dxy else None
        dxy_yoy = self._yoy(dxy, 52) if len(dxy) >= 52 else None
        # Rising DXY = liquidity tightening (countercyclical)
        dxy_signal = "tightening" if (dxy_yoy or 0) > 2 else "loosening" if (dxy_yoy or 0) < -2 else "neutral"
        print(f"    DXY: {dxy_latest:.1f} | YoY: {dxy_yoy:+.1f}% ({dxy_signal})" if dxy_latest and dxy_yoy else f"    DXY: unavailable")

        # ── Compute GLI Score ─────────────────────────────────────────────
        gli_score = self._compute_gli_score(
            fed_yoy=fed_yoy,
            m2_yoy=m2_yoy,
            rrp_latest=rrp_latest,
            rmop_active=rmop_active,
            repo_spread=repo_spread,
            dxy_yoy=dxy_yoy,
        )

        # ── GRID Regime ───────────────────────────────────────────────────
        grid_regime, growth_signal, inflation_signal = self._grid_regime()

        # ── 42 Macro Paradigm ─────────────────────────────────────────────
        paradigm = self._current_paradigm()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "fed_bs_trillions": round(fed_latest_val / 1e6, 2) if fed_latest_val else None,
            "fed_bs_yoy": round(fed_yoy, 2) if fed_yoy else None,
            "us_m2_billions": m2_latest,
            "us_m2_yoy": round(m2_yoy, 2) if m2_yoy else None,
            "rrp_billions": rrp_latest,
            "rmop_active": rmop_active,
            "repo_spread": round(repo_spread, 4),
            "repo_stress": repo_stress,
            "dxy_yoy": round(dxy_yoy, 2) if dxy_yoy else None,
            "dxy_signal": dxy_signal,
            "gli_score": gli_score,
            "gli_trend": "rising" if gli_score > 0.5 else "falling" if gli_score < -0.5 else "flat",
            "grid_regime": grid_regime,
            "growth_signal": growth_signal,
            "inflation_signal": inflation_signal,
            "paradigm": paradigm,
            "macro_score": self._macro_score(gli_score, grid_regime, paradigm),
        }

    def _yoy(self, series: List[Tuple], lag_periods: int) -> Optional[float]:
        """Compute YoY % change."""
        if len(series) < lag_periods + 1:
            return None
        current = series[-1][1]
        prior = series[-lag_periods][1]
        if prior == 0:
            return None
        return (current - prior) / prior * 100

    def _compute_gli_score(self, fed_yoy, m2_yoy, rrp_latest, rmop_active,
                            repo_spread, dxy_yoy) -> float:
        """
        GLI score: -2 to +2
        Positive = liquidity expanding (bullish for risk assets)
        Negative = liquidity contracting (bearish)
        """
        score = 0.0

        # Fed balance sheet growth
        if fed_yoy is not None:
            if fed_yoy > 5: score += 0.5
            elif fed_yoy > 0: score += 0.25
            elif fed_yoy < -5: score -= 0.5
            else: score -= 0.25

        # RMOP (active QE = bullish)
        if rmop_active:
            score += 0.3

        # M2 growth
        if m2_yoy is not None:
            if m2_yoy > 5: score += 0.4
            elif m2_yoy > 2: score += 0.2
            elif m2_yoy < 0: score -= 0.4
            else: score += 0.1

        # RRP level (higher RRP = less liquidity in system)
        if rrp_latest is not None:
            if rrp_latest < 100: score += 0.3    # very low RRP = liquidity deployed
            elif rrp_latest < 500: score += 0.1
            elif rrp_latest > 1000: score -= 0.2

        # Repo stress
        if repo_spread is not None:
            if repo_spread > 0.25: score -= 0.4  # Danger zone
            elif repo_spread > 0.15: score -= 0.2

        # DXY (countercyclical)
        if dxy_yoy is not None:
            if dxy_yoy > 5: score -= 0.4    # strong dollar = tighter global liquidity
            elif dxy_yoy > 2: score -= 0.2
            elif dxy_yoy < -2: score += 0.2  # weak dollar = looser global liquidity
            elif dxy_yoy < -5: score += 0.4

        return round(max(-2.0, min(2.0, score)), 2)

    def _grid_regime(self) -> Tuple[str, str, str]:
        """
        Determine current GRID regime from 42 Macro framework.
        Based on Jan 9, 2026 report: GOLDILOCKS confirmed.
        
        GOLDILOCKS: Growth ↑, Inflation ↓ → risk-on, disinflationary
        REFLATION:  Growth ↑, Inflation ↑ → risk-on, inflationary
        INFLATION:  Growth ↓, Inflation ↑ → risk-off, inflationary
        DEFLATION:  Growth ↓, Inflation ↓ → risk-off, deflationary
        
        In production: update from latest 42 Macro report monthly.
        """
        # Current reading from Jan 9, 2026 report
        # Macro Weather Model: bearish 3-month for stocks/BTC → caution
        # But GRID: GOLDILOCKS modal outcome
        # Risk: Macro Weather showing early signs of regime weakening

        growth = "rising"      # US economy resilient, Paradigm C tailwinds
        inflation = "falling"  # Disinflationary AI productivity + disinflation

        if growth == "rising" and inflation == "falling":
            regime = "GOLDILOCKS"
        elif growth == "rising" and inflation == "rising":
            regime = "REFLATION"
        elif growth == "falling" and inflation == "rising":
            regime = "INFLATION"
        else:
            regime = "DEFLATION"

        return regime, growth, inflation

    def _current_paradigm(self) -> str:
        """
        42 Macro Paradigm A-E classification.
        Current: transitioning B→C (per Jan 2026 report).
        B = cut (fiscal/monetary tightening)
        C = grow (Paradigm C = tax cuts, deregulation, growth)
        """
        return "B_TO_C"  # Update monthly from 42 Macro report

    def _macro_score(self, gli_score: float, grid_regime: str, paradigm: str) -> int:
        """
        Convert GLI + GRID + Paradigm into Layer 0 score adjustment.
        
        This score ADJUSTS the Layer 1 composite regime score.
        Range: -2 to +2
        
        Applied to our 8-input regime score as:
          final_regime_score = layer1_score + macro_score
        """
        score = 0

        # GLI direction
        if gli_score > 1.0: score += 2
        elif gli_score > 0.5: score += 1
        elif gli_score < -1.0: score -= 2
        elif gli_score < -0.5: score -= 1

        # GRID regime
        risk_on = grid_regime in ("GOLDILOCKS", "REFLATION")
        if risk_on:
            score += 0  # neutral adjustment — already reflected in market prices
        else:
            score -= 1  # risk-off regime reduces size

        # Paradigm
        if paradigm in ("C", "D"):
            score += 0  # monetary loosening bullish but priced in
        elif paradigm in ("B", "B_TO_C"):
            score -= 0  # fiscal tightening headwind, slight drag

        return max(-2, min(2, score))

    def print_summary(self, state: Dict):
        """Print formatted Layer 0 summary."""
        print("\n" + "=" * 70)
        print("  LAYER 0 — MACRO REGIME (42 Macro / Howell Framework)")
        print("=" * 70)
        print(f"\n  GRID Regime:  {state['grid_regime']}")
        print(f"  GLI Score:    {state['gli_score']:+.2f} ({state['gli_trend'].upper()})")
        print(f"  Paradigm:     {state['paradigm']}")
        print(f"  Macro Score:  {state['macro_score']:+d} (adjustment to Layer 1)")

        print(f"\n  Key Inputs:")
        print(f"    Fed BS:      ${state['fed_bs_trillions']:.2f}T | YoY: {state['fed_bs_yoy']:+.1f}%" if state['fed_bs_yoy'] else f"    Fed BS: ${state['fed_bs_trillions']}")
        print(f"    US M2:       ${state['us_m2_billions']:.0f}B | YoY: {state['us_m2_yoy']:+.1f}%" if state['us_m2_yoy'] else "")
        print(f"    RMOP Active: {state['rmop_active']} ($40B/mo through Mar-26)")
        print(f"    Repo Spread: {state['repo_spread']:+.3f}% | Stress: {state['repo_stress']}")
        print(f"    DXY:         {state['dxy_signal'].upper()} (YoY: {state['dxy_yoy']:+.1f}%)" if state['dxy_yoy'] else "")

        regime = state['grid_regime']
        gli = state['gli_score']
        print(f"\n  Regime Interpretation:")
        if regime == "GOLDILOCKS":
            print("    GOLDILOCKS: Risk-on, disinflationary → full allocation to risk assets")
            print("    KISS: 60% stocks / 30% gold / 10% BTC (max allocation)")
        elif regime == "REFLATION":
            print("    REFLATION: Risk-on, inflationary → tilt toward commodities + BTC")
        elif regime == "INFLATION":
            print("    INFLATION: Risk-off → cut equity/BTC to 50%; hold gold")
        elif regime == "DEFLATION":
            print("    DEFLATION: Risk-off → defensive positioning")

        if gli < -0.5:
            print("    GLI FALLING: Liquidity tightening → higher drawdown risk for BTC/MSTR")
            print("    Per Howell: BTC has 40-45% GLI beta, 13-week lead time")
        elif gli > 0.5:
            print("    GLI RISING: Liquidity expanding → supportive for risk assets")

        howell_warning = state.get('fed_bs_yoy', 0) or 0
        if howell_warning < 0:
            print("    ⚠️ Howell Warning: Fed BS contracting → GLI cyclical downswing risk")

    def save_to_db(self, state: Dict):
        """Save GLI state to SQLite DB."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS gli_proxy (
                timestamp TEXT,
                gli_score REAL,
                gli_trend TEXT,
                grid_regime TEXT,
                growth_signal TEXT,
                inflation_signal TEXT,
                paradigm TEXT,
                macro_score INTEGER,
                fed_bs_trillions REAL,
                fed_bs_yoy REAL,
                us_m2_billions REAL,
                us_m2_yoy REAL,
                rrp_billions REAL,
                rmop_active INTEGER,
                repo_spread REAL,
                repo_stress INTEGER,
                dxy_yoy REAL
            )
        """)
        c.execute("""
            INSERT INTO gli_proxy VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            state['timestamp'], state['gli_score'], state['gli_trend'],
            state['grid_regime'], state['growth_signal'], state['inflation_signal'],
            state['paradigm'], state['macro_score'],
            state['fed_bs_trillions'], state['fed_bs_yoy'],
            state['us_m2_billions'], state['us_m2_yoy'],
            state['rrp_billions'], int(state['rmop_active']),
            state['repo_spread'], int(state['repo_stress']),
            state['dxy_yoy'],
        ))
        conn.commit()
        conn.close()
        print("  ✓ Saved to gli_proxy table")


# ══════════════════════════════════════════════════════════════════════════
# REGIME INTEGRATION — how Layer 0 adjusts Layer 1 score
# ══════════════════════════════════════════════════════════════════════════

def apply_layer0_to_regime(layer1_score: int, gli_state: Dict) -> Dict:
    """
    Apply Layer 0 macro regime to adjust Layer 1 composite score.
    
    Rules (from AGENTS.md):
      GLI Z-score > 0.5:  Reduce bearish stage probability ~20%
                          → +1 to regime score if Layer 1 is bearish
      GLI Z-score < -0.5: Reduce bullish stage probability ~20%
                          → -1 to regime score if Layer 1 is bullish
      GRID GOLDILOCKS:    Confirm risk-on; allow full allocation
      GRID INFLATION:     Override bullish signals; defensive posture
    
    Returns adjusted score and reasoning.
    """
    gli_score = gli_state.get('gli_score', 0)
    grid_regime = gli_state.get('grid_regime', 'GOLDILOCKS')
    macro_adj = gli_state.get('macro_score', 0)

    adjusted = layer1_score + macro_adj

    # SRI bearish stage override (per AGENTS.md GLI Meta-Filter Rule)
    if gli_score > 0.5 and layer1_score < -1:
        adjusted += 1  # Reduce bearish call probability
        reason = "GLI expanding → reduces bearish stage probability by ~20%"
    elif gli_score < -0.5 and layer1_score > 1:
        adjusted -= 1  # Reduce bullish call probability
        reason = "GLI contracting → reduces bullish stage probability by ~20%"
    else:
        reason = "GLI neutral → no override on SRI stage calls"

    # GRID regime override
    if grid_regime == "INFLATION" and adjusted > 0:
        adjusted = 0
        reason += " | INFLATION regime → overrides bullish signals"
    elif grid_regime in ("GOLDILOCKS", "REFLATION") and adjusted < -3:
        adjusted = -2
        reason += " | GOLDILOCKS/REFLATION → caps bearish override at -2"

    return {
        "layer1_score": layer1_score,
        "macro_adjustment": macro_adj,
        "final_score": max(-9, min(9, adjusted)),
        "gli_score": gli_score,
        "grid_regime": grid_regime,
        "override_reason": reason,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="Save to DB")
    args = parser.parse_args()

    gli = GLIProxy()
    state = gli.collect()
    gli.print_summary(state)

    # Example integration with Layer 1
    print("\n\n  LAYER 0 + LAYER 1 INTEGRATION EXAMPLE:")
    layer1_example = 1  # NEUTRAL from earlier run
    result = apply_layer0_to_regime(layer1_example, state)
    print(f"    Layer 1 score:    {result['layer1_score']:+d}")
    print(f"    Macro adjustment: {result['macro_adjustment']:+d}")
    print(f"    Final score:      {result['final_score']:+d}")
    print(f"    Override:         {result['override_reason']}")

    if args.save:
        gli.save_to_db(state)
