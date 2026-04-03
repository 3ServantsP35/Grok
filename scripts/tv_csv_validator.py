#!/usr/bin/env python3
"""
tv_csv_validator.py
===================

P-TVI scaffold for centralized TradingView CSV validation.
Current scope:
- load canonical_csvs.json
- resolve asset/family config
- fast-path validation for required columns + row count + monotonic time
- emit structured result dict for downstream consumers

This is intentionally a first implementation foothold, not the final full validator.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import pandas as pd

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "canonical_csvs.json"


@dataclass
class ValidationResult:
    ok: bool
    asset: str
    family: str
    path: str
    row_count: int = 0
    errors: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TVCSVValidator:
    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or CONFIG_PATH
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        return json.loads(Path(self.config_path).read_text())

    def get_asset_config(self, asset: str, family: str = "240") -> dict[str, Any]:
        return self.config["timeframe_families"][family]["assets"][asset]

    def validate_file(self, path: str | Path, asset: str, family: str = "240") -> ValidationResult:
        path = str(path)
        cfg = self.get_asset_config(asset, family)
        errors: list[str] = []

        csv_path = Path(path)
        if not csv_path.exists():
            return ValidationResult(False, asset, family, path, 0, ["file_missing"])

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            return ValidationResult(False, asset, family, path, 0, [f"read_error:{e}"])

        # strip duplicate header rows if present
        if "time" in df.columns:
            df = df[df["time"].astype(str) != "time"]

        row_count = len(df)
        if row_count < int(cfg.get("min_rows", 0)):
            errors.append(f"row_count_below_min:{row_count}<{cfg.get('min_rows')}")

        required_columns = cfg.get("required_columns", [])
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            errors.append(f"missing_columns:{','.join(missing)}")

        if "time" in df.columns:
            try:
                ts = pd.to_numeric(df["time"], errors="coerce")
                if ts.isna().any():
                    errors.append("time_non_numeric")
                elif not ts.is_monotonic_increasing:
                    errors.append("time_not_monotonic")
            except Exception as e:
                errors.append(f"time_validation_error:{e}")

        return ValidationResult(len(errors) == 0, asset, family, path, row_count, errors or [])


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Validate a TradingView CSV against canonical config")
    parser.add_argument("path")
    parser.add_argument("asset")
    parser.add_argument("--family", default="240")
    args = parser.parse_args()

    validator = TVCSVValidator()
    result = validator.validate_file(args.path, args.asset, args.family)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
