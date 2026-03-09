#!/usr/bin/env python3
"""
doi_engine.py — Distribution Opportunity Index (DOI) Engine
============================================================
Reads pre-computed DOI columns from TradingView CSV exports.
Valid for Momentum assets only: MSTR, IBIT, TSLA.

Outputs:
  - DOI Score (0-10): distribution pressure gauge
  - VLT SRI Bias: secondary exit signal line
  - T1/T2/T3 trim signals (LOI +40 / +60 / +80)
  - VLT Peak ★: VLT SRI Bias crosses +20 (100% WR exit)
  - EXIT — LOI Rollover ✕: LOI drops 25pts from 20-bar peak (89% WR)
  - CT4 Distribution: all TFs positive + VLT > +20

Architecture: P-DOI, Layer 2 Signal Engine.
Scope: Momentum assets only (MSTR, IBIT, TSLA).
       MR assets (SPY/QQQ/GLD/IWM) not supported — distribution WR < 60%.

Column mapping (force_<ASSET>.csv):
  'DOI Score (0-10)'     → doi_score
  'VLT SRI Bias'         → vlt_bias
  'T1 Trim 25%'          → t1_signal (notna = active)
  'T2 Trim 50%'          → t2_signal
  'T3 Trim 75%'          → t3_signal
  'VLT Peak'             → vlt_peak_signal (notna = active)
  'EXIT — LOI Rollover'  → exit_rollover (notna = active)
  'CT4 Distribution'     → ct4_dist (notna = active)
  'LOI'                  → loi (last column occurrence)
"""

import csv
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
CSV_DIR   = Path("/tmp")
CSV_MAP   = {
    "MSTR": "force_MSTR.csv",
    "IBIT": "force_MSTR_IBIT.csv",   # MSTR/IBIT ratio CSV; IBIT uses same file
    "TSLA": "force_MSTR.csv",         # TSLA uses dedicated file if available
}

# Per-asset CSV overrides
# Try TSLA-specific CSV first; fall back to None (TSLA not in force_*.csv exports yet)
def _build_asset_csv_map(csv_dir: Path) -> dict:
    tsla_csv = csv_dir / "force_TSLA.csv"
    return {
        "MSTR": csv_dir / "force_MSTR.csv",
        "IBIT": csv_dir / "force_MSTR_IBIT.csv",
        "TSLA": tsla_csv if tsla_csv.exists() else None,
    }

CSV_ASSET_MAP = _build_asset_csv_map(CSV_DIR)

MOMENTUM_ASSETS = {"MSTR", "IBIT", "TSLA"}

VLT_PEAK_THRESHOLD = 20.0   # VLT SRI Bias above this → 100% exit signal
T1_LOI = 40.0
T2_LOI = 60.0
T3_LOI = 80.0

# ── DOISignal dataclass-equivalent ────────────────────────────────────────────

class DOISignal:
    def __init__(
        self,
        asset: str,
        loi: Optional[float],
        doi_score: Optional[float],
        vlt_bias: Optional[float],
        t1_active: bool,
        t2_active: bool,
        t3_active: bool,
        vlt_peak: bool,
        exit_rollover: bool,
        ct4_dist: bool,
        timestamp: Optional[str] = None,
        data_age_bars: int = 0,
    ):
        self.asset         = asset
        self.loi           = loi
        self.doi_score     = doi_score
        self.vlt_bias      = vlt_bias
        self.t1_active     = t1_active
        self.t2_active     = t2_active
        self.t3_active     = t3_active
        self.vlt_peak      = vlt_peak
        self.exit_rollover = exit_rollover
        self.ct4_dist      = ct4_dist
        self.timestamp     = timestamp
        self.data_age_bars = data_age_bars

    @property
    def any_trim(self) -> bool:
        return self.t1_active or self.t2_active or self.t3_active

    @property
    def high_conviction_exit(self) -> bool:
        return self.vlt_peak or self.exit_rollover

    @property
    def active_trim_level(self) -> Optional[str]:
        if self.t3_active: return "T3 (75%)"
        if self.t2_active: return "T2 (50%)"
        if self.t1_active: return "T1 (25%)"
        return None

    @property
    def distribution_zone(self) -> bool:
        """LOI above T1 threshold — distribution mode active."""
        return (self.loi or 0) >= T1_LOI

    def to_dict(self) -> dict:
        return {
            "asset":         self.asset,
            "loi":           self.loi,
            "doi_score":     self.doi_score,
            "vlt_bias":      self.vlt_bias,
            "t1_active":     self.t1_active,
            "t2_active":     self.t2_active,
            "t3_active":     self.t3_active,
            "vlt_peak":      self.vlt_peak,
            "exit_rollover": self.exit_rollover,
            "ct4_dist":      self.ct4_dist,
            "timestamp":     self.timestamp,
            "data_age_bars": self.data_age_bars,
        }


class DOIEngine:
    """
    Reads DOI data from TradingView CSV exports and returns DOISignal objects.
    Supports MSTR, IBIT, TSLA (Momentum assets only).
    """

    def __init__(self, csv_dir: Optional[Path] = None):
        self.csv_dir = csv_dir or CSV_DIR

    def _load_csv_rows(self, asset: str) -> Optional[list[dict]]:
        """Load CSV rows for asset. Returns list of dicts or None."""
        asset_map = _build_asset_csv_map(self.csv_dir)
        csv_file = asset_map.get(asset)
        if csv_file is None:
            log.debug(f"DOI: no CSV configured for {asset}")
            return None
        if not csv_file.exists():
            log.warning(f"DOI CSV not found for {asset}: {csv_file}")
            return None

        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [r for r in reader]
            return rows if rows else None
        except Exception as e:
            log.error(f"DOI CSV load error ({asset}): {e}")
            return None

    @staticmethod
    def _safe_float(val: Optional[str]) -> Optional[float]:
        try:
            if val is None or str(val).strip() in ("", "NaN", "nan", "null"):
                return None
            return float(val)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _notna(val: Optional[str]) -> bool:
        """Returns True if value is a non-zero numeric (binary signal active)."""
        try:
            if val is None or str(val).strip() in ("", "NaN", "nan", "null"):
                return False
            return float(val) != 0
        except (ValueError, TypeError):
            return False

    def compute(self, asset: str) -> Optional[DOISignal]:
        """
        Compute DOI state for a single asset.
        Returns None if data unavailable or asset not Momentum.
        """
        asset = asset.upper()
        if asset not in MOMENTUM_ASSETS:
            log.debug(f"DOI: {asset} is not a Momentum asset — skipping")
            return None

        rows = self._load_csv_rows(asset)
        if not rows:
            return None

        # Use last row (most recent bar)
        last = rows[-1]

        # ── Find LOI (last occurrence of 'LOI' key in CSV) ──────────────────
        # DictReader may suffix duplicate keys — find the DOI LOI column
        # The DOI LOI appears after 'DOI Score (0-10)' in column order
        loi = self._safe_float(last.get("LOI.1") or last.get("LOI"))
        doi_score = self._safe_float(last.get("DOI Score (0-10)"))
        vlt_bias = self._safe_float(last.get("VLT SRI Bias"))

        # Trim signals — notna = active on that bar
        t1 = self._notna(last.get("T1 Trim 25%"))
        t2 = self._notna(last.get("T2 Trim 50%"))
        t3 = self._notna(last.get("T3 Trim 75%"))
        vlt_peak = self._notna(last.get("VLT Peak"))
        exit_roll = self._notna(last.get("EXIT — LOI Rollover"))
        ct4_dist = self._notna(last.get("CT4 Distribution"))

        ts = last.get("time", "")

        return DOISignal(
            asset=asset,
            loi=loi,
            doi_score=doi_score,
            vlt_bias=vlt_bias,
            t1_active=t1,
            t2_active=t2,
            t3_active=t3,
            vlt_peak=vlt_peak,
            exit_rollover=exit_roll,
            ct4_dist=ct4_dist,
            timestamp=ts,
        )

    def compute_all(self) -> dict[str, DOISignal]:
        """Compute DOI state for all Momentum assets."""
        results = {}
        for asset in MOMENTUM_ASSETS:
            sig = self.compute(asset)
            if sig:
                results[asset] = sig
        return results

    def format_brief_block(self, signals: dict[str, DOISignal]) -> str:
        """
        Format DOI section for morning_brief.py.
        Returns a Discord-markdown formatted block.
        """
        if not signals:
            return "**📊 DOI — Distribution Signals**\n*No data available*"

        lines = ["**📊 DOI — Distribution Opportunity Index**"]
        lines.append("*Momentum assets only. LOI > +40 = distribution zone. MR assets not applicable.*\n")
        lines.append("```")
        lines.append(f"{'Asset':<6} {'LOI':>7}  {'DOI':>4}  {'VLT Bias':>9}  {'Signals'}")
        lines.append("─" * 58)

        for asset in ["MSTR", "IBIT", "TSLA"]:
            sig = signals.get(asset)
            if not sig:
                lines.append(f"{asset:<6} {'—':>7}  {'—':>4}  {'—':>9}  no data")
                continue

            loi_str   = f"{sig.loi:+.1f}" if sig.loi is not None else "—"
            doi_str   = f"{sig.doi_score:.1f}" if sig.doi_score is not None else "—"
            vlt_str   = f"{sig.vlt_bias:+.1f}" if sig.vlt_bias is not None else "—"

            signal_parts = []
            if sig.t3_active:        signal_parts.append("T3⚠")
            elif sig.t2_active:      signal_parts.append("T2⚠")
            elif sig.t1_active:      signal_parts.append("T1⚠")
            if sig.vlt_peak:         signal_parts.append("VLT★")
            if sig.exit_rollover:    signal_parts.append("EXIT✕")
            if sig.ct4_dist:         signal_parts.append("CT4")
            sig_str = " ".join(signal_parts) if signal_parts else "—"

            lines.append(f"{asset:<6} {loi_str:>7}  {doi_str:>4}  {vlt_str:>9}  {sig_str}")

        lines.append("```")
        lines.append("T1=+40 (25% trim) | T2=+60 (50%) | T3=+80 (75%) | "
                     "VLT★=100% exit | EXIT✕=89% rollover")

        # High-conviction callout
        for asset, sig in signals.items():
            if sig.high_conviction_exit:
                lines.append(f"\n🚨 **{asset}**: High-conviction exit signal — "
                              f"{'VLT Peak ★ (100% WR)' if sig.vlt_peak else 'LOI Rollover ✕ (89% WR)'}")
            elif sig.any_trim and not sig.high_conviction_exit:
                lines.append(f"\n⚠️ **{asset}**: {sig.active_trim_level} trim level active")

        return "\n".join(lines)


# ── Standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = DOIEngine()
    signals = engine.compute_all()
    for asset, sig in signals.items():
        print(f"\n{asset}:")
        print(f"  LOI={sig.loi}, DOI Score={sig.doi_score}, VLT Bias={sig.vlt_bias}")
        print(f"  T1={sig.t1_active}, T2={sig.t2_active}, T3={sig.t3_active}")
        print(f"  VLT Peak={sig.vlt_peak}, Exit Rollover={sig.exit_rollover}")
    if signals:
        engine2 = DOIEngine()
        print("\n" + engine2.format_brief_block(signals))
