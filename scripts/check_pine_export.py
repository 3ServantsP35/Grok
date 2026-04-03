#!/usr/bin/env python3
"""
check_pine_export.py
====================

Lightweight post-update Pine export checker for P-TVI.
Current purpose:
- compare a CSV export against the schema contract scaffold
- catch obvious breakage after Pine changes
- verify minimum rows and required columns

This is intentionally a lightweight first implementation, not the final full regression harness.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import pandas as pd

CONTRACT_PATH = Path(__file__).resolve().parents[1] / "config" / "pine_schema_contract.json"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def check_export(csv_path: str | Path, family: str = "240") -> dict:
    csv_path = Path(csv_path)
    contract = load_contract()
    required = contract.get("core_required_columns", [])
    min_rows = int(contract.get("timeframe_min_rows", {}).get(family, 0))

    result = {
        "path": str(csv_path),
        "family": family,
        "ok": True,
        "row_count": 0,
        "missing_required_columns": [],
        "warnings": []
    }

    if not csv_path.exists():
        result["ok"] = False
        result["warnings"].append("file_missing")
        return result

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        result["ok"] = False
        result["warnings"].append(f"read_error:{e}")
        return result

    if "time" in df.columns:
        df = df[df["time"].astype(str) != "time"]

    result["row_count"] = len(df)
    if len(df) < min_rows:
        result["ok"] = False
        result["warnings"].append(f"row_count_below_min:{len(df)}<{min_rows}")

    missing = [c for c in required if c not in df.columns]
    result["missing_required_columns"] = missing
    if missing:
        result["ok"] = False

    if "time" in df.columns:
        try:
            ts = pd.to_numeric(df["time"], errors="coerce")
            if ts.isna().any():
                result["warnings"].append("time_non_numeric")
            elif not ts.is_monotonic_increasing:
                result["warnings"].append("time_not_monotonic")
        except Exception as e:
            result["warnings"].append(f"time_validation_error:{e}")

    return result


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Check a Pine CSV export against the current schema contract scaffold")
    parser.add_argument("csv_path")
    parser.add_argument("--family", default="240")
    args = parser.parse_args()

    result = check_export(args.csv_path, args.family)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
