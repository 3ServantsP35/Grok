#!/usr/bin/env python3
"""
liquidity_roc_draft.py
======================

First-pass weekly liquidity ROC proxy engine.

Purpose:
- provide a testable quantitative draft now
- emphasize rate-of-change over absolute level
- translate liquidity-style macro inputs into BTC / MSTR / IBIT context

This is intentionally a proxy model, not a final Michael Howell replica.
It uses available local TradingView-exported series already in the repo.

Inputs (current draft):
- INDEX_BTCUSD, 240_*.csv
- BATS_IBIT, 240_*.csv
- BATS_MSTR, 240_*.csv
- TVC_DXY, 240_*.csv
- TVC_VIX, 240_*.csv
- BATS_HYG, 240_*.csv
- BATS_LQD, 240_*.csv
- BATS_TLT, 240_*.csv
- CRYPTOCAP_STABLE.C.D, 240_*.csv
- BATS_STRF_BATS_LQD, 240_*.csv
- BATS_STRD_BATS_HYG, 240_*.csv

Draft philosophy:
- Liquidity ROC > absolute liquidity level
- Falling DXY / VIX / stablecoin dominance are liquidity-supportive
- Rising HYG/LQD, STRF/LQD, STRD/HYG, TLT are treated as supportive proxies
- Score is a weighted composite of standardized short-term ROC values
"""

from __future__ import annotations

import glob
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]

SERIES_MAP = {
    "BTC": "INDEX_BTCUSD, 240_*.csv",
    "IBIT": "BATS_IBIT, 240_*.csv",
    "MSTR": "BATS_MSTR, 240_*.csv",
    "DXY": "TVC_DXY, 240_*.csv",
    "VIX": "TVC_VIX, 240_*.csv",
    "HYG": "BATS_HYG, 240_*.csv",
    "LQD": "BATS_LQD, 240_*.csv",
    "TLT": "BATS_TLT, 240_*.csv",
    "STABLE_D": "CRYPTOCAP_STABLE.C.D, 240_*.csv",
    "STRF_LQD": "BATS_STRF_BATS_LQD, 240_*.csv",
    "STRD_HYG": "BATS_STRD_BATS_HYG, 240_*.csv",
}

WEIGHTS = {
    "DXY": -0.20,
    "VIX": -0.15,
    "STABLE_D": -0.15,
    "HYG": 0.10,
    "LQD": 0.05,
    "TLT": 0.05,
    "STRF_LQD": 0.15,
    "STRD_HYG": 0.15,
}


@dataclass
class SeriesSnapshot:
    name: str
    path: str | None
    last_close: float | None
    roc_5: float | None
    roc_10: float | None
    roc_20: float | None


@dataclass
class LiquidityROCReport:
    liquidity_roc_score: float
    liquidity_roc_regime: str
    liquidity_roc_acceleration: str
    btc_alignment: str
    mstr_alignment: str
    ibit_alignment: str
    top_positive_drivers: list[str]
    top_negative_drivers: list[str]
    series: dict[str, dict[str, Any]]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


def latest_match(pattern: str) -> Path | None:
    matches = [Path(p) for p in glob.glob(str(REPO_ROOT / pattern))]
    if not matches:
        return None
    matches.sort(key=lambda p: p.stat().st_mtime)
    return matches[-1]


def load_close_series(path: Path) -> pd.Series:
    df = pd.read_csv(path, low_memory=False)
    if "time" in df.columns:
        df = df[df["time"] != "time"].reset_index(drop=True)
    close = pd.to_numeric(df["close"], errors="coerce").dropna().reset_index(drop=True)
    return close


def pct_change_n(s: pd.Series, n: int) -> float | None:
    if len(s) <= n:
        return None
    prev = float(s.iloc[-1 - n])
    curr = float(s.iloc[-1])
    if prev == 0:
        return None
    return ((curr / prev) - 1.0) * 100.0


def classify_regime(score: float) -> str:
    if score >= 0.75:
        return "STRONGLY SUPPORTIVE"
    if score >= 0.25:
        return "SUPPORTIVE"
    if score > -0.25:
        return "NEUTRAL / TRANSITIONAL"
    if score > -0.75:
        return "RESTRICTIVE"
    return "STRONGLY RESTRICTIVE"


def classify_alignment(asset_roc: float | None, liq_score: float) -> str:
    if asset_roc is None:
        return "UNKNOWN"
    if liq_score > 0.25 and asset_roc > 0:
        return "ALIGNED BULLISH"
    if liq_score < -0.25 and asset_roc < 0:
        return "ALIGNED BEARISH"
    if liq_score > 0.25 and asset_roc <= 0:
        return "LAGGING LIQUIDITY"
    if liq_score < -0.25 and asset_roc >= 0:
        return "OUTRUNNING LIQUIDITY"
    return "MIXED"


def build_report() -> LiquidityROCReport:
    series_snapshots: dict[str, SeriesSnapshot] = {}
    driver_scores: dict[str, float] = {}

    for name, pattern in SERIES_MAP.items():
        path = latest_match(pattern)
        if not path:
            series_snapshots[name] = SeriesSnapshot(name, None, None, None, None, None)
            continue
        close = load_close_series(path)
        snap = SeriesSnapshot(
            name=name,
            path=str(path.name),
            last_close=float(close.iloc[-1]) if len(close) else None,
            roc_5=pct_change_n(close, 5),
            roc_10=pct_change_n(close, 10),
            roc_20=pct_change_n(close, 20),
        )
        series_snapshots[name] = snap
        if name in WEIGHTS and snap.roc_5 is not None:
            driver_scores[name] = WEIGHTS[name] * snap.roc_5

    liquidity_roc_score = sum(driver_scores.values())

    # Acceleration = compare shorter ROC composite to medium ROC composite
    accel_short = 0.0
    accel_med = 0.0
    for name, weight in WEIGHTS.items():
        snap = series_snapshots.get(name)
        if not snap:
            continue
        if snap.roc_5 is not None:
            accel_short += weight * snap.roc_5
        if snap.roc_10 is not None:
            accel_med += weight * snap.roc_10
    if accel_short > accel_med + 0.10:
        acceleration = "IMPROVING"
    elif accel_short < accel_med - 0.10:
        acceleration = "DETERIORATING"
    else:
        acceleration = "STABLE / MIXED"

    positives = sorted(driver_scores.items(), key=lambda kv: kv[1], reverse=True)
    negatives = sorted(driver_scores.items(), key=lambda kv: kv[1])

    btc_roc = series_snapshots["BTC"].roc_5
    mstr_roc = series_snapshots["MSTR"].roc_5
    ibit_roc = series_snapshots["IBIT"].roc_5

    return LiquidityROCReport(
        liquidity_roc_score=round(liquidity_roc_score, 3),
        liquidity_roc_regime=classify_regime(liquidity_roc_score),
        liquidity_roc_acceleration=acceleration,
        btc_alignment=classify_alignment(btc_roc, liquidity_roc_score),
        mstr_alignment=classify_alignment(mstr_roc, liquidity_roc_score),
        ibit_alignment=classify_alignment(ibit_roc, liquidity_roc_score),
        top_positive_drivers=[f"{k} ({v:+.3f})" for k, v in positives[:3]],
        top_negative_drivers=[f"{k} ({v:+.3f})" for k, v in negatives[:3]],
        series={k: asdict(v) for k, v in series_snapshots.items()},
    )


def print_human(report: LiquidityROCReport) -> None:
    print("=" * 72)
    print("WEEKLY LIQUIDITY ROC DRAFT")
    print("=" * 72)
    print(f"Liquidity ROC Score: {report.liquidity_roc_score:+.3f}")
    print(f"Liquidity Regime:    {report.liquidity_roc_regime}")
    print(f"Acceleration:        {report.liquidity_roc_acceleration}")
    print()
    print(f"BTC alignment:       {report.btc_alignment}")
    print(f"MSTR alignment:      {report.mstr_alignment}")
    print(f"IBIT alignment:      {report.ibit_alignment}")
    print()
    print("Top positive drivers:")
    for item in report.top_positive_drivers:
        print(f"  + {item}")
    print("Top negative drivers:")
    for item in report.top_negative_drivers:
        print(f"  - {item}")
    print()
    print("Series snapshots:")
    for name, snap in report.series.items():
        print(
            f"  {name:10s} close={snap['last_close']} roc5={snap['roc_5']} roc10={snap['roc_10']} roc20={snap['roc_20']} file={snap['path']}"
        )
    print("=" * 72)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Draft weekly liquidity ROC proxy engine")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(report.to_json())
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
