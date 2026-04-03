#!/usr/bin/env python3
"""
P10 Trend Line Engine v3.0  —  Final production version
========================================================
Provides algorithmic trend line identification + SRI-derived structural levels
for MSTR and in-scope assets. Outputs ordered, distance-filtered lines suitable
for morning brief, MSR reports, and DB persistence.

Two source types are merged into a unified output:
  1. SRI-derived levels — named levels already computed in the indicator CSV
     (Fast TL, Slow TL, Reversal Support/Resistance for each TF)
  2. Swing-based lines — computed from major + intermediate zig-zag pivot detection
     with quality scoring (touches, span, R², recency)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import sqlite3, json, sys, os

# ─── Configuration ────────────────────────────────────────────────────────────

ASSET_ZZ_CONFIG = {
    # asset → (major_pct, intermediate_pct)  for zig-zag thresholds
    "MSTR":  (15.0,  7.0),
    "BTC":   (12.0,  6.0),
    "TSLA":  (15.0,  7.0),
    "IBIT":  (12.0,  6.0),
    "SPY":   ( 7.0,  3.5),
    "QQQ":   ( 7.0,  3.5),
    "GLD":   ( 6.0,  3.0),
    "IWM":   ( 8.0,  4.0),
}

# Lines are classified as NEAR (shown in brief) vs FAR (context only)
NEAR_RESISTANCE_PCT = 0.45   # show resistance up to 45% above price
NEAR_SUPPORT_PCT    = 0.40   # show support down to 40% below price
DB_PATH = os.environ.get("MSTR_DB_PATH", "/mnt/mstr-data/mstr.db")

# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class TrendLine:
    source: str              # 'SRI' or 'SWING'
    line_type: str           # 'resistance' or 'support'
    label: str               # human-readable name
    proj_now: float          # projected price at current date
    slope: float             # $/day (0.0 for horizontal SRI levels)
    anchor_date: str         # first anchor point date
    anchor_price: float
    end_date: Optional[str]  # second anchor point (SWING only)
    end_price: Optional[float]
    touches: int             # number of price contacts (SWING) or 0 (SRI)
    span_days: int           # span of the line in days
    r_squared: float         # 0.0–1.0 fit quality (SWING) or 1.0 (SRI exact)
    quality: int             # 0–100 composite score
    broken: bool             # True if price has closed through this line
    distance_pct: float      # % from current price; negative = above (resistance), positive = support above price
    proj_30d: float
    proj_60d: float
    tf_label: Optional[str]  # 'VLT'/'LT'/'ST'/'VST' for SRI lines

    @property
    def emoji(self) -> str:
        if self.broken:
            return "⚪"
        if self.line_type == "resistance":
            return "🔴" if self.touches >= 3 else "🟠"
        return "🟢" if self.touches >= 3 else "🔵"

    def brief_str(self, current_price: float) -> str:
        """Single-line format for morning brief / Discord."""
        dist_str = f"+{self.distance_pct:.1f}%" if self.distance_pct >= 0 else f"{self.distance_pct:.1f}%"
        slope_str = f" slope:{self.slope:+.2f}/d" if abs(self.slope) > 0.01 else ""
        touch_str = f" {self.touches}T" if self.touches > 0 else ""
        q_str = f" Q{self.quality}" if self.source == "SWING" else ""
        proj_str = ""
        if self.slope != 0.0:
            proj_str = f" | 30d:${self.proj_30d:.0f} 60d:${self.proj_60d:.0f}"
        return (f"  ${self.proj_now:<8.2f} {dist_str:>7}  {self.label:<30}"
                f"{slope_str}{touch_str}{q_str}{proj_str}")


@dataclass
class TrendLineResult:
    asset: str
    current_price: float
    as_of_date: str
    near_resistance: List[TrendLine]       # within NEAR_RESISTANCE_PCT above
    near_support: List[TrendLine]          # within NEAR_SUPPORT_PCT below
    former_res_now_support: List[TrendLine]  # broken resistance now below price
    former_sup_now_resistance: List[TrendLine]  # broken support now above price
    far_resistance: List[TrendLine]        # beyond threshold
    far_support: List[TrendLine]

    def to_brief_str(self, max_resistance: int = 8, max_support: int = 6) -> str:
        """Formatted block for Discord morning brief. Shows nearest lines first, capped at max_N."""
        lines = [f"📐 **KEY TREND LINES — {self.asset}** (${self.current_price:.2f} as of {self.as_of_date})"]

        # Resistance — prefer SRI-named levels + highest-touch SWING lines, nearest first
        res_show = self._priority_select(self.near_resistance, max_resistance)
        if res_show:
            lines.append("  **RESISTANCE** (nearest → furthest):")
            for l in res_show:
                dist = abs(l.distance_pct)
                lines.append(f"  🔴 ${l.proj_now:<8.2f} +{dist:.1f}% above  {l.label}" +
                             (f"  slope:{l.slope:+.2f}/d  30d:${l.proj_30d:.0f}" if abs(l.slope) > 0.05 else ""))
        else:
            lines.append("  *No resistance within 45%*")

        # Support — prefer SRI-named levels + highest-touch SWING lines, nearest first
        sup_show = self._priority_select(self.near_support, max_support)
        if sup_show:
            lines.append("  **SUPPORT** (nearest → furthest):")
            for l in sup_show:
                dist = abs(l.distance_pct)
                pos_str = "at/above" if l.distance_pct <= 0 else f"{dist:.1f}% below"
                lines.append(f"  🟢 ${l.proj_now:<8.2f} {pos_str:>12}  {l.label}" +
                             (f"  slope:{l.slope:+.2f}/d  30d:${l.proj_30d:.0f}" if abs(l.slope) > 0.05 else ""))
        else:
            lines.append("  *No support within 40%*")

        # Former levels (converted role) — max 3
        converted = (self.former_res_now_support + self.former_sup_now_resistance)[:3]
        if converted:
            lines.append("  **CONVERTED LEVELS** (former role reversed):")
            for l in converted:
                role = "res→support" if l in self.former_res_now_support else "sup→resistance"
                dist = abs((self.current_price - l.proj_now) / self.current_price * 100)
                lines.append(f"  ⚪ ${l.proj_now:.2f}  [{role}]  {dist:.1f}% away  {l.label[:40]}  {l.touches}T")

        return "\n".join(lines)

    def _priority_select(self, line_list: List["TrendLine"], max_n: int) -> List["TrendLine"]:
        """Select up to max_n lines: SRI-named lines always included; SWING lines by quality then proximity."""
        sri  = [l for l in line_list if l.source == "SRI"]
        swing = sorted([l for l in line_list if l.source == "SWING"],
                       key=lambda x: (-x.touches, -x.quality, abs(x.distance_pct)))
        result = sri[:max_n]
        remaining = max_n - len(result)
        result += swing[:remaining]
        # Re-sort by distance (nearest first for resistance = smallest proj_now; support = largest)
        result.sort(key=lambda x: x.proj_now if line_list and line_list[0].line_type == "resistance"
                    else -x.proj_now)
        return result

    def to_msr_str(self) -> str:
        """Formatted block for Market Structure Reports."""
        lines = [f"### Trend Line Structure ({self.asset} — {self.as_of_date})",
                 f"Current: ${self.current_price:.2f}", ""]

        lines.append("**Active Resistance (nearest first):**")
        for l in self.near_resistance[:6]:
            lines.append(f"- ${l.proj_now:.2f} (+{l.distance_pct:.1f}%) — {l.label}"
                         + (f" | slope ${l.slope:+.2f}/d, projects to ${l.proj_30d:.0f} in 30d" if l.slope != 0 else ""))

        lines.append("\n**Active Support (nearest first):**")
        for l in self.near_support[:6]:
            lines.append(f"- ${l.proj_now:.2f} ({l.distance_pct:.1f}%) — {l.label}"
                         + (f" | slope ${l.slope:+.2f}/d, projects to ${l.proj_30d:.0f} in 30d" if l.slope != 0 else ""))

        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Serializable dict for DB storage."""
        def line_to_dict(l: TrendLine):
            return {
                "source": l.source, "type": l.line_type, "label": l.label,
                "proj_now": l.proj_now, "slope": l.slope, "anchor_date": l.anchor_date,
                "anchor_price": l.anchor_price, "touches": l.touches,
                "span_days": l.span_days, "r_squared": l.r_squared,
                "quality": l.quality, "broken": l.broken, "distance_pct": l.distance_pct,
                "proj_30d": l.proj_30d, "proj_60d": l.proj_60d,
            }
        return {
            "asset": self.asset,
            "current_price": self.current_price,
            "as_of_date": self.as_of_date,
            "near_resistance": [line_to_dict(l) for l in self.near_resistance],
            "near_support": [line_to_dict(l) for l in self.near_support],
            "former_res_now_support": [line_to_dict(l) for l in self.former_res_now_support],
        }

# ─── Core Engine ──────────────────────────────────────────────────────────────

class TrendLineEngine:
    """
    Unified trend line engine.  Call analyze(df, asset) to get TrendLineResult.
    df must have columns: time (unix), open, high, low, close, and optionally
    SRI columns (e.g. 'LT Fast Trackline', 'VLT Slow Trackline', etc.)
    """

    def analyze(self, df: pd.DataFrame, asset: str,
                start_date: str = "2024-01-01") -> TrendLineResult:
        df = self._prepare_df(df, start_date)
        if df is None or len(df) < 30:
            return self._empty_result(asset)

        current_price = float(df["close"].iloc[-1])
        as_of = df["date"].iloc[-1].strftime("%Y-%m-%d")
        today_dt = df["date"].iloc[-1]
        d30 = (today_dt + timedelta(days=30)).strftime("%Y-%m-%d")
        d60 = (today_dt + timedelta(days=60)).strftime("%Y-%m-%d")

        lines: List[TrendLine] = []

        # 1. SRI-derived named levels (flat + slope from TL series)
        lines += self._extract_sri_lines(df, current_price, as_of, d30, d60)

        # 2. Swing-based trend lines (major + intermediate tiers)
        major_pct, inter_pct = ASSET_ZZ_CONFIG.get(asset.upper(), (12.0, 6.0))
        lines += self._compute_swing_lines(df, asset, current_price, as_of, d30, d60,
                                           major_pct, inter_pct)

        # 3. Deduplicate (collapse within 0.5% + 3 days)
        lines = self._deduplicate(lines, current_price)

        # 4. Classify into buckets
        return self._classify(lines, asset, current_price, as_of)

    # ── DataFrame preparation ────────────────────────────────────────────────

    def _prepare_df(self, df: pd.DataFrame, start_date: str) -> Optional[pd.DataFrame]:
        try:
            df = df.copy()
            df["date"] = pd.to_datetime(df["time"], unit="s", utc=True)
            # Keep only OHLC + named SRI columns
            keep = ["date", "time", "open", "high", "low", "close"]
            sri_cols = [c for c in df.columns if any(k in c for k in
                        ["Trackline", "Reversal Support", "Reversal Resistance",
                         "Reversal Robust Fit"])]
            df = df[keep + sri_cols].sort_values("date").reset_index(drop=True)
            cutoff = pd.Timestamp(start_date, tz="UTC")
            df = df[df["date"] >= cutoff].reset_index(drop=True)
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            df["high"]  = pd.to_numeric(df["high"],  errors="coerce")
            df["low"]   = pd.to_numeric(df["low"],   errors="coerce")
            return df if len(df) >= 30 else None
        except Exception as e:
            print(f"[TrendLineEngine] _prepare_df error: {e}")
            return None

    # ── SRI-derived levels ───────────────────────────────────────────────────

    def _extract_sri_lines(self, df, current_price, as_of, d30, d60) -> List[TrendLine]:
        """Extract named SRI levels: Fast/Slow Tracklines + Reversal bands per TF."""
        lines = []
        last = df.iloc[-1]
        today_dt = df["date"].iloc[-1]

        # Map column → (label, tf_label, line_type_hint)
        SRI_MAP = {
            "VLT Fast Trackline": ("VLT Fast TL",       "VLT", None),
            "VLT Slow Trackline": ("VLT Slow TL",       "VLT", None),
            "LT Fast Trackline":  ("LT Fast TL",        "LT",  None),
            "LT Slow Trackline":  ("LT Slow TL",        "LT",  None),
            "ST Fast Trackline":  ("ST Fast TL",        "ST",  None),
            "ST Slow Trackline":  ("ST Slow TL",        "ST",  None),
            "VST Fast Trackline": ("VST Fast TL",       "VST", None),
            "VST Slow Trackline": ("VST Slow TL",       "VST", None),
            "VLT Reversal Support":    ("VLT Rev Support",    "VLT", "support"),
            "VLT Reversal Resistance": ("VLT Rev Resistance", "VLT", "resistance"),
            "LT Reversal Support":     ("LT Rev Support",     "LT",  "support"),
            "LT Reversal Resistance":  ("LT Rev Resistance",  "LT",  "resistance"),
            "ST Reversal Support":     ("ST Rev Support",     "ST",  "support"),
            "ST Reversal Resistance":  ("ST Rev Resistance",  "ST",  "resistance"),
        }

        for col, (label, tf, type_hint) in SRI_MAP.items():
            if col not in df.columns:
                continue
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            if series.empty:
                continue

            val_now = float(last[col]) if pd.notna(last[col]) else float(series.iloc[-1])
            if val_now <= 0:
                continue

            # Compute slope from last 20 bars to assess direction
            if len(series) >= 20:
                slope_20 = (float(series.iloc[-1]) - float(series.iloc[-21])) / 20.0
            else:
                slope_20 = 0.0

            # Project 30/60d: SRI tracklines move approximately at their current slope
            val_30 = val_now + slope_20 * 30
            val_60 = val_now + slope_20 * 60

            # Determine line_type from position if not specified
            if type_hint:
                lt = type_hint
            else:
                lt = "support" if val_now <= current_price else "resistance"
                # Handle cases where TL crosses current price
                if abs(val_now - current_price) / current_price < 0.005:
                    lt = "support"  # At-the-money → treat as support

            dist = (current_price - val_now) / current_price * 100  # pos = below price (support)
            if lt == "resistance":
                dist = -dist  # Make resistance negative

            broken = False
            if lt == "resistance" and current_price > val_now * 1.01:
                broken = True
            elif lt == "support" and current_price < val_now * 0.99:
                broken = True

            lines.append(TrendLine(
                source="SRI", line_type=lt, label=label,
                proj_now=round(val_now, 2), slope=round(slope_20, 4),
                anchor_date=as_of, anchor_price=round(val_now, 2),
                end_date=None, end_price=None,
                touches=0, span_days=0, r_squared=1.0, quality=85,
                broken=broken, distance_pct=round(dist, 2),
                proj_30d=round(val_30, 2), proj_60d=round(val_60, 2),
                tf_label=tf,
            ))

        return lines

    # ── Swing detection ──────────────────────────────────────────────────────

    def _zigzag(self, df: pd.DataFrame, min_pct: float) -> List[Tuple]:
        """Percentage-based zig-zag. Returns list of (idx, date, price, 'H'|'L')."""
        swings = []
        if len(df) < 5:
            return swings
        direction = 1
        lh_idx, lh_p = 0, float(df["high"].iloc[0])
        ll_idx, ll_p = 0, float(df["low"].iloc[0])
        thresh = min_pct / 100.0

        for i in range(1, len(df)):
            hi = float(df["high"].iloc[i])
            lo = float(df["low"].iloc[i])
            if direction == 1:
                if hi > lh_p:
                    lh_p, lh_idx = hi, i
                elif lh_p > 0 and (lh_p - lo) / lh_p >= thresh:
                    swings.append((lh_idx, df["date"].iloc[lh_idx], lh_p, "H"))
                    direction = -1
                    ll_p, ll_idx = lo, i
            else:
                if lo < ll_p:
                    ll_p, ll_idx = lo, i
                elif ll_p > 0 and (hi - ll_p) / ll_p >= thresh:
                    swings.append((ll_idx, df["date"].iloc[ll_idx], ll_p, "L"))
                    direction = 1
                    lh_p, lh_idx = hi, i

        if direction == 1:
            swings.append((lh_idx, df["date"].iloc[lh_idx], lh_p, "H"))
        else:
            swings.append((ll_idx, df["date"].iloc[ll_idx], ll_p, "L"))
        return swings

    def _count_touches(self, df, anchor_dt, anchor_p, slope, line_type,
                       tol_pct=2.5) -> Tuple[int, float]:
        """Count bars touching this line. Returns (touches, R²)."""
        touch_residuals = []
        price_col = "high" if line_type == "resistance" else "low"
        for i in range(len(df)):
            dk = df["date"].iloc[i]
            days = (dk - anchor_dt).days
            expected = anchor_p + slope * days
            if expected <= 0:
                continue
            tol = expected * tol_pct / 100
            bar_price = float(df[price_col].iloc[i])
            if abs(bar_price - expected) <= tol:
                # Ensure we're approaching from the right side
                close_i = float(df["close"].iloc[i])
                if line_type == "resistance" and close_i <= expected * 1.015:
                    touch_residuals.append(bar_price - expected)
                elif line_type == "support" and close_i >= expected * 0.985:
                    touch_residuals.append(bar_price - expected)

        if len(touch_residuals) < 2:
            return len(touch_residuals), 0.0

        # R²: variance explained vs mean line price
        mean_touch = np.mean(touch_residuals)
        ss_res = sum((r - 0) ** 2 for r in touch_residuals)  # residuals from line (0 = perfect)
        ss_tot = sum((r - mean_touch) ** 2 for r in touch_residuals)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 1e-9 else 1.0
        return len(touch_residuals), max(0.0, round(r2, 3))

    def _quality_score(self, touches, span_days, r_squared, broken,
                       recency_days) -> int:
        """Composite quality 0–100."""
        touch_s  = min(touches * 8, 32)           # max 32 — touches
        span_s   = min(span_days / 6, 25)          # max 25 — longevity
        r2_s     = round(r_squared * 20, 0)        # max 20 — fit quality
        intact_s = 0 if broken else 18             # max 18 — still valid
        recency_s = max(0, 5 - recency_days // 30) # max 5 — recent confirmation
        return int(min(100, touch_s + span_s + r2_s + intact_s + recency_s))

    def _project(self, anchor_dt, anchor_p, slope, target_str) -> float:
        target_dt = datetime.strptime(target_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if hasattr(anchor_dt, 'tzinfo') and anchor_dt.tzinfo:
            days = (target_dt - anchor_dt).days
        else:
            days = (target_dt - anchor_dt.replace(tzinfo=timezone.utc)).days
        return round(anchor_p + slope * days, 2)

    def _compute_swing_lines(self, df, asset, current_price, as_of,
                             d30, d60, major_pct, inter_pct) -> List[TrendLine]:
        """Compute trend lines from major and intermediate swing points."""
        lines = []
        today_dt = df["date"].iloc[-1]

        for pct, tier in [(major_pct, "Major"), (inter_pct, "Inter")]:
            swings = self._zigzag(df, pct)
            highs = [(s[0], s[1], s[2]) for s in swings if s[3] == "H"]
            lows  = [(s[0], s[1], s[2]) for s in swings if s[3] == "L"]

            for point_list, lt in [(highs, "resistance"), (lows, "support")]:
                for i in range(len(point_list)):
                    for j in range(i + 1, len(point_list)):
                        idx1, d1, p1 = point_list[i]
                        idx2, d2, p2 = point_list[j]
                        span = (d2 - d1).days
                        if span < 14:
                            continue
                        slope = (p2 - p1) / span

                        # Enforce directional validity:
                        # Resistance lines: price should approach from BELOW
                        # Support lines: price should approach from ABOVE
                        # Allow slight slope variation but filter extreme reversals
                        if lt == "resistance" and slope > current_price * 0.01:
                            # Steeply rising resistance — skip (just a rising market)
                            pass  # keep, still valid
                        if lt == "support" and slope > current_price * 0.005:
                            pass  # rising support is valid

                        proj_now = p1 + slope * (today_dt - d1).days
                        if proj_now <= 0:
                            continue

                        # Distance filter: skip lines wildly far from price
                        dist_ratio = abs(proj_now - current_price) / current_price
                        if dist_ratio > 0.90:  # > 90% away → skip entirely
                            continue

                        touches, r2 = self._count_touches(df, d1, p1, slope, lt)
                        if touches < 2:
                            continue

                        broken = (lt == "resistance" and current_price > proj_now * 1.02) or \
                                 (lt == "support"    and current_price < proj_now * 0.98)

                        recency = (today_dt - d2).days
                        quality = self._quality_score(touches, span, r2, broken, recency)

                        proj_30 = self._project(d1, p1, slope, d30)
                        proj_60 = self._project(d1, p1, slope, d60)

                        dist = (current_price - proj_now) / current_price * 100
                        if lt == "resistance":
                            dist = -dist

                        anchor_str = d1.strftime("%Y-%m-%d")
                        end_str    = d2.strftime("%Y-%m-%d")
                        label = f"{tier} {lt[:3].title()}: {anchor_str}→{end_str}"

                        lines.append(TrendLine(
                            source="SWING", line_type=lt, label=label,
                            proj_now=round(proj_now, 2), slope=round(slope, 4),
                            anchor_date=anchor_str, anchor_price=round(p1, 2),
                            end_date=end_str, end_price=round(p2, 2),
                            touches=touches, span_days=span, r_squared=r2,
                            quality=quality, broken=broken,
                            distance_pct=round(dist, 2),
                            proj_30d=proj_30, proj_60d=proj_60,
                            tf_label=None,
                        ))

        return lines

    # ── Deduplication ────────────────────────────────────────────────────────

    def _deduplicate(self, lines: List[TrendLine],
                     current_price: float) -> List[TrendLine]:
        """Merge lines within 2.0% of each other (same type). Keep highest quality."""
        threshold = current_price * 0.020
        seen: List[TrendLine] = []
        for l in sorted(lines, key=lambda x: -x.quality):
            duplicate = False
            for s in seen:
                if s.line_type == l.line_type and abs(s.proj_now - l.proj_now) < threshold:
                    duplicate = True
                    break
            if not duplicate:
                seen.append(l)
        return seen

    # ── Classification ───────────────────────────────────────────────────────

    def _classify(self, lines: List[TrendLine], asset: str,
                  current_price: float, as_of: str) -> TrendLineResult:
        near_res, near_sup = [], []
        former_res_sup, former_sup_res = [], []
        far_res, far_sup = [], []

        for l in sorted(lines, key=lambda x: x.proj_now):
            if l.line_type == "resistance":
                if l.broken:
                    # Resistance broken = price above it → now acts as support if close
                    dist_below = (current_price - l.proj_now) / current_price
                    if 0 < dist_below <= NEAR_SUPPORT_PCT:
                        former_res_sup.append(l)
                else:
                    dist_above = (l.proj_now - current_price) / current_price
                    if dist_above <= NEAR_RESISTANCE_PCT:
                        near_res.append(l)
                    else:
                        far_res.append(l)
            else:  # support
                if l.broken:
                    # Support broken = price below it → now acts as resistance if close
                    dist_above = (l.proj_now - current_price) / current_price
                    if 0 < dist_above <= NEAR_RESISTANCE_PCT:
                        former_sup_res.append(l)
                else:
                    dist_below = (current_price - l.proj_now) / current_price
                    if dist_below <= NEAR_SUPPORT_PCT:
                        near_sup.append(l)
                    else:
                        far_sup.append(l)

        # Sort near lists by distance from price (closest first)
        near_res.sort(key=lambda x: x.proj_now)   # lowest first (nearest resistance)
        near_sup.sort(key=lambda x: -x.proj_now)   # highest first (nearest support)
        former_res_sup.sort(key=lambda x: -x.proj_now)
        former_sup_res.sort(key=lambda x: x.proj_now)

        return TrendLineResult(
            asset=asset, current_price=current_price, as_of_date=as_of,
            near_resistance=near_res, near_support=near_sup,
            former_res_now_support=former_res_sup,
            former_sup_now_resistance=former_sup_res,
            far_resistance=far_res, far_support=far_sup,
        )

    def _empty_result(self, asset: str) -> TrendLineResult:
        return TrendLineResult(
            asset=asset, current_price=0.0, as_of_date="N/A",
            near_resistance=[], near_support=[],
            former_res_now_support=[], former_sup_now_resistance=[],
            far_resistance=[], far_support=[],
        )

    # ── DB persistence ───────────────────────────────────────────────────────

    def save_to_db(self, result: TrendLineResult, db_path: str = DB_PATH):
        """Persist trend line snapshot to SQLite."""
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trend_line_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    asset TEXT NOT NULL,
                    as_of_date TEXT NOT NULL,
                    current_price REAL,
                    data_json TEXT NOT NULL
                )""")
            conn.execute("""
                DELETE FROM trend_line_cache
                WHERE asset = ? AND as_of_date = ?""", (result.asset, result.as_of_date))
            conn.execute("""
                INSERT INTO trend_line_cache (timestamp, asset, as_of_date, current_price, data_json)
                VALUES (?, ?, ?, ?, ?)""",
                (datetime.now(timezone.utc).isoformat(), result.asset,
                 result.as_of_date, result.current_price,
                 json.dumps(result.to_dict())))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[TrendLineEngine] DB save error: {e}")


# ─── Convenience function for morning brief ───────────────────────────────────

def get_trend_lines_for_brief(asset: str, csv_path: str,
                               start_date: str = "2024-01-01") -> str:
    """Load CSV, run engine, return formatted brief string. Never raises."""
    try:
        df = pd.read_csv(csv_path)
        eng = TrendLineEngine()
        result = eng.analyze(df, asset, start_date)
        # Optionally persist
        try:
            eng.save_to_db(result)
        except Exception:
            pass
        return result.to_brief_str()
    except Exception as e:
        return f"📐 Trend line analysis unavailable for {asset}: {e}"


def get_trend_lines_for_msr(asset: str, csv_path: str,
                             start_date: str = "2024-01-01") -> str:
    """Load CSV, run engine, return formatted MSR string. Never raises."""
    try:
        df = pd.read_csv(csv_path)
        eng = TrendLineEngine()
        result = eng.analyze(df, asset, start_date)
        # Optionally persist
        try:
            eng.save_to_db(result)
        except Exception:
            pass
        return result.to_msr_str()
    except Exception as e:
        return f"### Trend Line Structure ({asset})\n*Unavailable: {e}*"


# ─── CLI ──────────────────────────────────────────────────────────────────────

ASSET_PATHS = {
    "MSTR": "/mnt/mstr-data/BATS_MSTR_1D_91973.csv",
    "BTC":  "/mnt/mstr-data/INDEX_BTCUSD_1D_39f9f.csv",
    "TSLA": "/mnt/mstr-data/BATS_TSLA_1D_b4331.csv",
    "SPY":  "/mnt/mstr-data/BATS_SPY_1D_f2caa.csv",
    "QQQ":  "/mnt/mstr-data/BATS_QQQ_1D_d7851.csv",
    "GLD":  "/mnt/mstr-data/BATS_GLD_1D_20455.csv",
    "IWM":  "/mnt/mstr-data/BATS_IWM_240_8af1a.csv",
}

if __name__ == "__main__":
    target = sys.argv[1].upper() if len(sys.argv) > 1 else "MSTR"
    targets = list(ASSET_PATHS.keys()) if target == "ALL" else [target]

    for asset in targets:
        path = ASSET_PATHS.get(asset)
        if not path or not os.path.exists(path):
            print(f"[{asset}] CSV not found: {path}")
            continue
        output = get_trend_lines_for_brief(asset, path)
        print(output)
        print()
