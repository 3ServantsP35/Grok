#!/usr/bin/env python3
"""
tv_rpa_export.py
================

Bounded TradingView RPA export layer for P-TVI.

Current implemented scope:
- load canonical config
- build approved export task list
- explicit preflight checks
- Playwright runtime path
- authenticated login flow scaffold
- bounded per-asset navigation flow
- mandatory 60-second dwell before download trigger
- explicit stop-on-anomaly behavior

Important:
- This script is intentionally narrow and failure-intolerant.
- It does not implement broad browser automation.
- It is designed around fixed views, in-scope assets, and manual fallback.
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
DEFAULT_LOGIN_URL = "https://www.tradingview.com/accounts/signin/"
DEFAULT_HOME_URL = "https://www.tradingview.com/"


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
        self.tv_username = os.environ.get("TV_USERNAME", "")
        self.tv_password = os.environ.get("TV_PASSWORD", "")

    def _load_config(self) -> dict[str, Any]:
        return json.loads(Path(self.config_path).read_text())

    def preflight(self) -> tuple[bool, list[str]]:
        problems: list[str] = []
        if not importlib.util.find_spec("playwright"):
            problems.append("missing_python_package:playwright")
        if not self.tv_username:
            problems.append("missing_env:TV_USERNAME")
        if not self.tv_password:
            problems.append("missing_env:TV_PASSWORD")
        return (len(problems) == 0, problems)

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

    def fail(self, msg: str, code: int = 2) -> int:
        self.log(f"FAIL: {msg}")
        self.log("Manual fallback should be used until this anomaly is resolved.")
        return code

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

    def _login(self, page) -> None:
        self.log("Opening TradingView login page")
        page.goto(DEFAULT_LOGIN_URL, wait_until="domcontentloaded", timeout=60000)

        # Conservative selector strategy; fail fast if the login form is not found.
        email_candidates = [
            'input[name="username"]',
            'input[name="email"]',
            'input[type="email"]'
        ]
        password_candidates = [
            'input[name="password"]',
            'input[type="password"]'
        ]
        submit_candidates = [
            'button[type="submit"]',
            'button:has-text("Sign in")',
            'button:has-text("Log in")'
        ]

        email_locator = None
        for sel in email_candidates:
            loc = page.locator(sel)
            if loc.count() > 0:
                email_locator = loc.first
                break
        if email_locator is None:
            raise RuntimeError("login_email_field_not_found")

        password_locator = None
        for sel in password_candidates:
            loc = page.locator(sel)
            if loc.count() > 0:
                password_locator = loc.first
                break
        if password_locator is None:
            raise RuntimeError("login_password_field_not_found")

        submit_locator = None
        for sel in submit_candidates:
            loc = page.locator(sel)
            if loc.count() > 0:
                submit_locator = loc.first
                break
        if submit_locator is None:
            raise RuntimeError("login_submit_button_not_found")

        email_locator.fill(self.tv_username)
        password_locator.fill(self.tv_password)
        submit_locator.click()
        page.wait_for_load_state("domcontentloaded", timeout=60000)
        self.log("Login flow submitted")

    def _open_export_view(self, page, task: ExportTask) -> None:
        if not task.export_view_url:
            raise RuntimeError(f"missing_export_view_url:{task.asset}")
        self.log(f"Opening export view for {task.asset}: {task.export_view_url}")
        page.goto(task.export_view_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_load_state("networkidle", timeout=60000)

    def _download_csv_placeholder(self, page, task: ExportTask) -> None:
        # This is the remaining page-specific step. We intentionally stop here
        # rather than faking completion without real selectors.
        self.dwell_before_download(task.asset)
        raise RuntimeError(f"download_selectors_not_implemented:{task.asset}")

    def run_real(self, family: str = "240") -> int:
        ok, problems = self.preflight()
        if not ok:
            return self.fail("RPA preflight failed: " + ", ".join(problems))

        from playwright.sync_api import sync_playwright  # type: ignore

        tasks = self.build_export_tasks(family)
        self.log(f"Starting bounded RPA run for {len(tasks)} approved tasks")
        self.enforce_manual_fallback_rule()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            try:
                self._login(page)
                for task in tasks:
                    self._open_export_view(page, task)
                    self._download_csv_placeholder(page, task)
            except Exception as e:
                context.close()
                browser.close()
                return self.fail(str(e))

            context.close()
            browser.close()
            self.log("RPA run completed")
            return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Bounded TradingView RPA export")
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
