#!/usr/bin/env python3
"""
tv_rpa_export.py
================

First scaffold for the bounded TradingView RPA export layer.
This is intentionally conservative and documents the exact operating rules
we are adopting in P-TVI:
- two export windows per day only
- in-scope assets only
- fixed approved views only
- mandatory 60-second dwell before triggering each download
- stop on any anomaly
- manual fallback always preserved

Current scope:
- load canonical config
- expose the approved asset/view list for export
- provide a bounded execution skeleton with dwell + logging
- provide a Playwright-based execution path when runtime dependencies are available
- fail explicitly with actionable preflight messages when runtime dependencies are missing
"""

from __future__ import annotations

import json
import os
import sys
import time
import importlib.util
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "canonical_csvs.json"


@dataclass
class ExportTask:
    asset: str
    family: str
    pattern: str
    export_view_url: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TVRPAExport:
    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or CONFIG_PATH
        self.config = self._load_config()
        self.dwell_seconds = int(self.config.get("rpa_export", {}).get("dwell_seconds", 60))
        self.download_timeout_seconds = int(self.config.get("rpa_export", {}).get("download_timeout_seconds", 120))
        self.staging_directory = self.config.get("rpa_export", {}).get("staging_directory", "/mnt/mstr-data/.staging/")

    def preflight(self) -> tuple[bool, list[str]]:
        problems: list[str] = []
        if not importlib.util.find_spec("playwright"):
            problems.append("missing_python_package:playwright")
        if not os.environ.get("TV_USERNAME"):
            problems.append("missing_env:TV_USERNAME")
        if not os.environ.get("TV_PASSWORD"):
            problems.append("missing_env:TV_PASSWORD")
        return (len(problems) == 0, problems)

    def _load_config(self) -> dict[str, Any]:
        return json.loads(Path(self.config_path).read_text())

    def build_export_tasks(self, family: str = "240") -> list[ExportTask]:
        cfg_family = self.config["timeframe_families"][family]
        tasks: list[ExportTask] = []
        for asset, meta in cfg_family["assets"].items():
            tasks.append(
                ExportTask(
                    asset=asset,
                    family=family,
                    pattern=meta["pattern"],
                    export_view_url=meta.get("export_view_url"),
                )
            )
        return tasks

    def log(self, msg: str) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[TV-RPA] {ts}  {msg}", flush=True)

    def enforce_manual_fallback_rule(self) -> None:
        self.log("Manual fallback remains valid. Any anomaly should stop automation and defer to manual export.")

    def dwell_before_download(self, asset: str) -> None:
        self.log(f"{asset}: chart/export view loaded; waiting mandatory {self.dwell_seconds}s before download")
        time.sleep(self.dwell_seconds)

    def run_dry(self, family: str = "240") -> list[dict[str, Any]]:
        tasks = self.build_export_tasks(family)
        self.log(f"Loaded {len(tasks)} approved export tasks from canonical config")
        self.enforce_manual_fallback_rule()
        rendered = [t.to_dict() for t in tasks]
        for t in tasks:
            self.log(f"Approved task: {t.asset} | family={t.family} | pattern={t.pattern} | view={t.export_view_url or 'UNSET'}")
        return rendered

    def run_real(self, family: str = "240") -> int:
        ok, problems = self.preflight()
        if not ok:
            self.log("RPA preflight failed: " + ", ".join(problems))
            self.log("Manual fallback should be used until runtime dependencies are installed/configured.")
            return 2

        from playwright.sync_api import sync_playwright  # type: ignore

        tasks = self.build_export_tasks(family)
        self.log(f"Starting bounded RPA run for {len(tasks)} approved tasks")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            # Placeholder login path; explicit until layout/view details are configured.
            self.log("Playwright runtime available. Concrete login/export selectors still need to be configured.")
            self.log("Stopping here intentionally rather than faking export completion.")

            context.close()
            browser.close()
            return 0


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Bounded TradingView RPA export scaffold")
    parser.add_argument("--family", default="240")
    parser.add_argument("--mode", choices=["dry", "real"], default="dry")
    args = parser.parse_args()

    runner = TVRPAExport()
    if args.mode == "real":
        return runner.run_real(args.family)
    tasks = runner.run_dry(args.family)
    print(json.dumps(tasks, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
