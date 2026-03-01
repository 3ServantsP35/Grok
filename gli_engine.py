#!/usr/bin/env python3
"""
GLI Engine — Layer 0
====================
Global Liquidity Index proxy from public FRED data.

Methodology (Howell / CrossBorder Capital adapted):
  Global Liquidity = aggregate central bank balance sheet expansion.
  GLI leads BTC price by ~13 weeks (ρ=0.58).
  GLI leads global equities by ~6 months.

Components:
  US Block  (65%):
    WALCL   — Fed balance sheet (weekly, millions USD)          [40%]
    WM2NS   — M2 money supply (weekly, billions USD)            [15%]
    WRESBAL — Bank reserves (weekly, millions USD)              [05%]
    WTREGEN — Treasury General Account inverse (weekly, mn USD) [05%]
  International Block (35%):
    ECBASSETSW — ECB balance sheet (weekly, millions EUR)       [20%]
    JPNASSETS  — BOJ balance sheet (monthly, millions JPY)      [15%]
  PBoC: excluded (no reliable recent FRED data; revisit quarterly)

GEGI — Global Economic Growth Index:
  Monetary  (30%): FEDFUNDS direction (cutting=+1, hiking=-1)
  Fiscal    (40%): Federal deficit direction (expanding=+1)
  External  (30%): Chicago Fed NFCI (accommodative=+1)

Output: GLIState used by RegimeEngine as probability adjuster.

Author: CIO Engine
Date: 2026-03-05
"""

import os
import json
import ssl
import math
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict


# ═══════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════

@dataclass
class GLIComponentState:
    """State of a single GLI component"""
    series_id: str
    label: str
    latest_date: str
    latest_value: float
    roc_26w: float        # 26-week % change
    roc_direction: str    # UP / DOWN / FLAT
    weight: float


@dataclass
class GEGIState:
    """Global Economic Growth Index components"""
    monetary_score: float    # -1 to +1  (FEDFUNDS direction)
    fiscal_score: float      # -1 to +1  (deficit direction)
    external_score: float    # -1 to +1  (NFCI)
    composite: float         # -1 to +1  weighted average
    label: str               # EXPANSIONARY / NEUTRAL / CONTRACTIONARY


@dataclass
class GLIState:
    """
    Full Layer 0 state — output of GLIEngine.compute().
    Passed into RegimeEngine.compute() to adjust Layer 1 probabilities.
    """
    timestamp: datetime
    # GLI scores
    gli_zscore: float            # Z-score vs 2-year rolling window
    gli_trend: str               # EXPANDING / NEUTRAL / CONTRACTING
    gli_momentum: float          # 13-week momentum of composite ROC
    gli_composite_roc: float     # Current weighted ROC across components
    # Stress indicator
    sofr_iorb_spread_bps: float  # SOFR - IORB in basis points (>20bp = stress)
    # GEGI
    gegi: GEGIState
    # Components (for reporting)
    components: List[GLIComponentState] = field(default_factory=list)
    # Derived output for RegimeEngine
    probability_adjustment: float = 0.0   # -0.2 to +0.2
    score_adjustment: int = 0             # -2 to +2  (integer adjustment to composite score)
    label: str = "NEUTRAL"
    interpretation: str = ""
    error: Optional[str] = None           # Non-None if data fetch failed


# ═══════════════════════════════════════════════════════════════
# GLI ENGINE
# ═══════════════════════════════════════════════════════════════

class GLIEngine:
    """
    Computes GLI Z-score and GEGI from public FRED data.

    Usage:
        engine = GLIEngine()
        state = engine.compute()
        print(state.gli_zscore, state.gegi.composite)
    """

    FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

    # GLI components: (series_id, label, weight, invert)
    # invert=True means higher value = less liquidity (TGA draw = inject when TGA falls)
    GLI_COMPONENTS = [
        ("WALCL",      "Fed Balance Sheet",    0.40, False),
        ("WM2NS",      "US M2 Money Supply",   0.15, False),
        ("WRESBAL",    "Bank Reserves",        0.05, False),
        ("WTREGEN",    "Treasury Gen Account", 0.05, True),   # inverted: TGA fall = injection
        ("ECBASSETSW", "ECB Balance Sheet",    0.20, False),
        ("JPNASSETS",  "BOJ Balance Sheet",    0.15, False),
    ]

    # GEGI series
    GEGI_SERIES = {
        "FEDFUNDS":      "Fed Funds Rate",
        "MTSDS133FMS":   "Federal Surplus/Deficit",
        "NFCI":          "Chicago Fed Financial Conditions",
    }

    # Repo stress
    STRESS_SERIES = ["SOFR", "IORB"]

    def __init__(self, fred_key: str = None):
        self.fred_key = fred_key or os.getenv("FRED_API_KEY", "8ee8d7967be4aab0fdc7565e85676260")
        self._ctx = ssl.create_default_context()
        self._ctx.check_hostname = False
        self._ctx.verify_mode = ssl.CERT_NONE
        self._cache: Dict[str, List[Tuple[str, float]]] = {}

    # ─────────────────────────────────────────────────────────
    # DATA FETCHING
    # ─────────────────────────────────────────────────────────

    def _fetch(self, series_id: str, limit: int = 130) -> List[Tuple[str, float]]:
        """Fetch FRED series observations, newest first. Returns list of (date, value)."""
        if series_id in self._cache:
            return self._cache[series_id]

        url = (f"{self.FRED_BASE}?series_id={series_id}"
               f"&api_key={self.fred_key}&file_type=json"
               f"&sort_order=desc&limit={limit}")
        req = urllib.request.Request(url, headers={"User-Agent": "mstr-cio/1.0"})
        try:
            with urllib.request.urlopen(req, context=self._ctx, timeout=15) as r:
                data = json.loads(r.read())
            obs = [(o["date"], float(o["value"]))
                   for o in data.get("observations", [])
                   if o["value"] not in (".", "")]
            self._cache[series_id] = obs
            return obs
        except Exception as e:
            print(f"  [GLI] FRED fetch error {series_id}: {e}")
            return []

    def _latest(self, series_id: str) -> Optional[float]:
        obs = self._fetch(series_id, limit=10)
        return obs[0][1] if obs else None

    def _roc(self, obs: List[Tuple[str, float]], periods: int = 26) -> Optional[float]:
        """
        % change over N observations (newest first list).
        For monthly series, 6 periods ≈ 6 months.
        For weekly series, 26 periods ≈ 6 months.
        """
        if len(obs) < periods + 1:
            return None
        current = obs[0][1]
        prior = obs[periods][1]
        if prior == 0:
            return None
        return (current - prior) / abs(prior) * 100

    def _roc_series(self, obs: List[Tuple[str, float]], periods: int = 26) -> List[float]:
        """Return full ROC series for Z-score calculation (newest first)."""
        result = []
        for i in range(len(obs) - periods):
            current = obs[i][1]
            prior = obs[i + periods][1]
            if prior != 0:
                result.append((current - prior) / abs(prior) * 100)
            else:
                result.append(0.0)
        return result  # newest first

    def _zscore(self, series: List[float], window: int = 104) -> Optional[float]:
        """
        Z-score of latest value vs rolling window.
        Series is newest-first.
        """
        if len(series) < 2:
            return None
        working = series[:window]
        if len(working) < 4:
            return None
        mean = sum(working) / len(working)
        variance = sum((x - mean) ** 2 for x in working) / len(working)
        std = math.sqrt(variance) if variance > 0 else 1.0
        return (series[0] - mean) / std

    # ─────────────────────────────────────────────────────────
    # GLI COMPUTATION
    # ─────────────────────────────────────────────────────────

    def _compute_gli(self) -> Tuple[float, float, str, float, List[GLIComponentState]]:
        """
        Returns (composite_roc, zscore, trend, momentum_13w, components).
        composite_roc = weighted sum of 26-week ROC across all components.
        """
        components = []
        weighted_roc_series: List[List[float]] = []
        weights = []

        for series_id, label, weight, invert in self.GLI_COMPONENTS:
            # Use shorter lookback for monthly series (BOJ)
            limit = 52 if series_id == "JPNASSETS" else 160
            periods = 6 if series_id == "JPNASSETS" else 26   # 6 months for monthly

            obs = self._fetch(series_id, limit=limit)
            if not obs:
                continue

            roc_s = self._roc_series(obs, periods=periods)
            if not roc_s:
                continue

            # Invert if needed (e.g. TGA: falling TGA = more reserves = bullish)
            if invert:
                roc_s = [-x for x in roc_s]

            current_roc = roc_s[0]
            direction = "UP" if current_roc > 0.5 else ("DOWN" if current_roc < -0.5 else "FLAT")

            components.append(GLIComponentState(
                series_id=series_id,
                label=label,
                latest_date=obs[0][0],
                latest_value=obs[0][1],
                roc_26w=current_roc,
                roc_direction=direction,
                weight=weight,
            ))
            weighted_roc_series.append([x * weight for x in roc_s])
            weights.append(weight)

        if not weighted_roc_series:
            return 0.0, 0.0, "NEUTRAL", 0.0, []

        # Align all series to same length (minimum)
        min_len = min(len(s) for s in weighted_roc_series)
        composite_series = [
            sum(series[i] for series in weighted_roc_series)
            for i in range(min_len)
        ]

        composite_roc = composite_series[0]
        zscore = self._zscore(composite_series, window=104) or 0.0

        # 13-week momentum: change in composite_roc over last 13 periods
        momentum = (composite_series[0] - composite_series[min(13, min_len - 1)]) if min_len > 13 else 0.0

        # Trend determination
        if zscore > 0.5:
            trend = "EXPANDING"
        elif zscore < -0.5:
            trend = "CONTRACTING"
        else:
            trend = "NEUTRAL"

        return composite_roc, zscore, trend, momentum, components

    # ─────────────────────────────────────────────────────────
    # GEGI COMPUTATION
    # ─────────────────────────────────────────────────────────

    def _compute_gegi(self) -> GEGIState:
        """
        Compute Global Economic Growth Index.
        Returns scores from -1.0 to +1.0 per component and composite.
        """
        # ── Monetary (30%): FEDFUNDS direction ──────────────────
        monetary = 0.0
        fedfunds = self._fetch("FEDFUNDS", limit=12)
        if len(fedfunds) >= 7:
            current_rate = fedfunds[0][1]
            prior_6m = fedfunds[6][1]
            delta = current_rate - prior_6m
            if delta <= -0.25:
                monetary = 1.0    # Cutting — accommodative
            elif delta >= 0.25:
                monetary = -1.0   # Hiking — restrictive
            else:
                # Normalize small changes
                monetary = max(-1.0, min(1.0, -delta / 0.25))

        # ── Fiscal (40%): Federal deficit direction ──────────────
        fiscal = 0.0
        deficit = self._fetch("MTSDS133FMS", limit=24)
        if len(deficit) >= 18:
            # 12-month rolling sum (monthly data, newest first)
            roll_now = sum(obs[1] for obs in deficit[:12])
            roll_6m = sum(obs[1] for obs in deficit[6:18])
            delta_roll = roll_now - roll_6m
            # Expanding deficit (more negative) = fiscal stimulus = positive for growth
            # delta_roll negative means deficit expanded → bullish
            if delta_roll < -20000:     # $20B threshold
                fiscal = 1.0
            elif delta_roll > 20000:    # deficit shrinking = fiscal drag
                fiscal = -1.0
            else:
                fiscal = max(-1.0, min(1.0, -delta_roll / 20000))

        # ── External (30%): Chicago Fed Financial Conditions ──────
        external = 0.0
        nfci = self._fetch("NFCI", limit=10)
        if nfci:
            nfci_val = nfci[0][1]
            # NFCI < -0.3 = accommodative (positive) → external = +1
            # NFCI > +0.3 = tightening (negative) → external = -1
            if nfci_val < -0.3:
                external = 1.0
            elif nfci_val > 0.3:
                external = -1.0
            else:
                external = max(-1.0, min(1.0, -nfci_val / 0.3))

        composite = (monetary * 0.30) + (fiscal * 0.40) + (external * 0.30)

        if composite > 0.3:
            label = "EXPANSIONARY"
        elif composite < -0.3:
            label = "CONTRACTIONARY"
        else:
            label = "NEUTRAL"

        return GEGIState(
            monetary_score=round(monetary, 3),
            fiscal_score=round(fiscal, 3),
            external_score=round(external, 3),
            composite=round(composite, 3),
            label=label,
        )

    # ─────────────────────────────────────────────────────────
    # REPO STRESS
    # ─────────────────────────────────────────────────────────

    def _compute_sofr_iorb(self) -> float:
        """Returns SOFR - IORB spread in basis points."""
        sofr = self._latest("SOFR")
        iorb = self._latest("IORB")
        if sofr is None or iorb is None:
            return 0.0
        return round((sofr - iorb) * 100, 1)  # convert % to bps

    # ─────────────────────────────────────────────────────────
    # PROBABILITY ADJUSTMENT
    # ─────────────────────────────────────────────────────────

    def _derive_adjustment(self, zscore: float, gegi: GEGIState) -> Tuple[float, int, str, str]:
        """
        Convert GLI Z-score + GEGI into probability_adjustment and score_adjustment.

        Returns (prob_adj, score_adj, label, interpretation)
        prob_adj: -0.2 to +0.2 (fractional probability shift)
        score_adj: -2 to +2 (integer to add to Layer 1 composite score)
        """
        # Base adjustment from GLI Z-score
        if zscore >= 1.5:
            prob_adj = 0.20
            score_adj = 2
            label = "STRONG TAILWIND"
            interp = f"GLI Z={zscore:.2f} — strong liquidity expansion. Bearish signals are likely false. Stage 4 = consolidation."
        elif zscore >= 0.5:
            prob_adj = 0.10
            score_adj = 1
            label = "TAILWIND"
            interp = f"GLI Z={zscore:.2f} — liquidity expanding. Reduce bearish probability ~20%. Stage 1 signals credible."
        elif zscore <= -1.5:
            prob_adj = -0.20
            score_adj = -2
            label = "STRONG HEADWIND"
            interp = f"GLI Z={zscore:.2f} — strong liquidity contraction. Bullish signals are likely false. Stage 1 = false bottom."
        elif zscore <= -0.5:
            prob_adj = -0.10
            score_adj = -1
            label = "HEADWIND"
            interp = f"GLI Z={zscore:.2f} — liquidity contracting. Reduce bullish probability ~20%. Stage 1 signals need extra confirmation."
        else:
            prob_adj = 0.0
            score_adj = 0
            label = "NEUTRAL"
            interp = f"GLI Z={zscore:.2f} — neutral liquidity. No probability adjustment."

        # GEGI amplification
        if gegi.composite > 1.0:
            score_adj = min(score_adj + 1, 2)
            prob_adj = min(prob_adj + 0.05, 0.20)
            interp += f" GEGI={gegi.composite:.2f} amplifying bullish override."
        elif gegi.composite < 0.0:
            score_adj = max(score_adj - 1, -2)
            prob_adj = max(prob_adj - 0.05, -0.20)
            interp += f" GEGI={gegi.composite:.2f} amplifying bearish override."

        return round(prob_adj, 3), int(score_adj), label, interp

    # ─────────────────────────────────────────────────────────
    # MAIN ENTRY POINT
    # ─────────────────────────────────────────────────────────

    def compute(self) -> GLIState:
        """Full Layer 0 computation. Returns GLIState."""
        try:
            composite_roc, zscore, trend, momentum, components = self._compute_gli()
            gegi = self._compute_gegi()
            sofr_iorb = self._compute_sofr_iorb()
            prob_adj, score_adj, label, interpretation = self._derive_adjustment(zscore, gegi)

            return GLIState(
                timestamp=datetime.utcnow(),
                gli_zscore=round(zscore, 3),
                gli_trend=trend,
                gli_momentum=round(momentum, 3),
                gli_composite_roc=round(composite_roc, 3),
                sofr_iorb_spread_bps=sofr_iorb,
                gegi=gegi,
                components=components,
                probability_adjustment=prob_adj,
                score_adjustment=score_adj,
                label=label,
                interpretation=interpretation,
                error=None,
            )

        except Exception as e:
            return GLIState(
                timestamp=datetime.utcnow(),
                gli_zscore=0.0,
                gli_trend="NEUTRAL",
                gli_momentum=0.0,
                gli_composite_roc=0.0,
                sofr_iorb_spread_bps=0.0,
                gegi=GEGIState(0, 0, 0, 0, "NEUTRAL"),
                label="NEUTRAL",
                interpretation="GLI data unavailable — no adjustment applied",
                error=str(e),
            )

    def print_report(self, state: GLIState) -> None:
        """Print formatted Layer 0 report."""
        print("\n" + "═" * 60)
        print("LAYER 0: GLI ENGINE — Global Liquidity")
        print("═" * 60)
        if state.error:
            print(f"  ⚠ Error: {state.error}")
            return

        print(f"  GLI Z-Score:   {state.gli_zscore:+.3f}  [{state.gli_trend}]")
        print(f"  GLI Momentum:  {state.gli_momentum:+.3f}  (13w trend)")
        print(f"  SOFR-IORB:     {state.sofr_iorb_spread_bps:+.1f} bps  {'⚠ STRESS' if state.sofr_iorb_spread_bps > 20 else 'normal'}")
        print()
        print(f"  GEGI:          {state.gegi.composite:+.3f}  [{state.gegi.label}]")
        print(f"    Monetary:    {state.gegi.monetary_score:+.3f}  (FEDFUNDS direction)")
        print(f"    Fiscal:      {state.gegi.fiscal_score:+.3f}  (deficit direction)")
        print(f"    External:    {state.gegi.external_score:+.3f}  (NFCI)")
        print()
        print(f"  Adjustment:    {state.label}")
        print(f"  Score Δ:       {state.score_adjustment:+d}  (applied to Layer 1 composite)")
        print(f"  Prob Δ:        {state.probability_adjustment:+.1%}")
        print()
        print(f"  Interpretation: {state.interpretation}")
        print()
        print("  Components:")
        for c in state.components:
            arrow = "↑" if c.roc_direction == "UP" else ("↓" if c.roc_direction == "DOWN" else "→")
            print(f"    {c.series_id:15s} {arrow}  ROC26={c.roc_26w:+.2f}%  wt={c.weight:.0%}  [{c.latest_date}]")
        print("═" * 60)


# ═══════════════════════════════════════════════════════════════
# STANDALONE TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Running GLI Engine — Layer 0 test...")
    engine = GLIEngine()
    state = engine.compute()
    engine.print_report(state)
    print(f"\nScore adjustment to pass to RegimeEngine: {state.score_adjustment:+d}")
    print(f"Probability adjustment:                   {state.probability_adjustment:+.1%}")
