#!/usr/bin/env python3
"""
weekly_liquidity_report.py

Downscoped weekly liquidity report generator.
Focus: weekly report only, no TradingView indicator work.

Current version:
- pulls the latest proxy series already available in the repo
- computes a simple liquidity ROC composite
- translates that into BTC / MSTR / IBIT framing
- prints a Discord-friendly report

This is intentionally iterative, not a final production engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from typing import Optional

import requests

from liquidity_roc_draft import build_report


@dataclass
class WeeklyView:
    score: float
    regime: str
    acceleration: str
    btc_alignment: str
    mstr_alignment: str
    ibit_alignment: str
    top_positive: list[str]
    top_negative: list[str]
    btc_roc5: Optional[float]
    mstr_roc5: Optional[float]
    ibit_roc5: Optional[float]


def _fmt_pct(v: Optional[float]) -> str:
    return "n/a" if v is None else f"{v:+.2f}%"


def _date_label(now: Optional[datetime] = None) -> str:
    now = now or datetime.now()
    return now.strftime("%A, %B %d, %Y")


def _view() -> WeeklyView:
    r = build_report()
    s = r.series
    return WeeklyView(
        score=r.liquidity_roc_score,
        regime=r.liquidity_roc_regime,
        acceleration=r.liquidity_roc_acceleration,
        btc_alignment=r.btc_alignment,
        mstr_alignment=r.mstr_alignment,
        ibit_alignment=r.ibit_alignment,
        top_positive=r.top_positive_drivers,
        top_negative=r.top_negative_drivers,
        btc_roc5=s.get("BTC", {}).get("roc_5"),
        mstr_roc5=s.get("MSTR", {}).get("roc_5"),
        ibit_roc5=s.get("IBIT", {}).get("roc_5"),
    )


def _implication(view: WeeklyView) -> str:
    if view.score >= 0.25 and view.acceleration == "IMPROVING":
        return "Liquidity is supportive and improving. That favors cleaner upside continuation in BTC and a stronger reflexive response in MSTR."
    if view.score >= 0.25 and view.acceleration != "IMPROVING":
        return "Liquidity is still supportive, but momentum is no longer strengthening. That argues for tactical upside with a higher risk of stalling or chop."
    if view.score <= -0.25 and view.acceleration == "DETERIORATING":
        return "Liquidity is restrictive and worsening. That raises downside risk for BTC and makes MSTR more vulnerable to underperformance and failed rallies."
    if view.score <= -0.25:
        return "Liquidity is restrictive, though not clearly worsening. That keeps the macro backdrop cautious and limits confidence in sustained upside." 
    return "Liquidity is transitional. The backdrop does not strongly confirm either a durable breakout or a major breakdown, so price action and force should carry more weight tactically."


def render_discord() -> str:
    v = _view()
    lines: list[str] = []
    lines.append("🌐 **Weekly Liquidity Report**")
    lines.append(_date_label())
    lines.append("")
    lines.append(f"**Liquidity ROC score:** {v.score:+.3f}")
    lines.append(f"**Regime:** {v.regime}")
    lines.append(f"**Acceleration:** {v.acceleration}")
    lines.append("")
    lines.append("**Asset alignment**")
    lines.append(f"- BTC: {v.btc_alignment} ({_fmt_pct(v.btc_roc5)} 5-bar)")
    lines.append(f"- MSTR: {v.mstr_alignment} ({_fmt_pct(v.mstr_roc5)} 5-bar)")
    lines.append(f"- IBIT: {v.ibit_alignment} ({_fmt_pct(v.ibit_roc5)} 5-bar)")
    lines.append("")
    lines.append("**Top positive drivers**")
    for item in v.top_positive:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("**Top negative drivers**")
    for item in v.top_negative:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("**Implication for BTC and MSTR**")
    lines.append(_implication(v))
    return "\n".join(lines)


ENV_PATHS = [Path("/mnt/mstr-config/.env"), Path("/Users/vera/mstr-engine/config/.env")]
MAX_DISCORD_LEN = 1900


def _load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for path in ENV_PATHS:
        if path.exists():
            for line in path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
            break
    for key, val in os.environ.items():
        env.setdefault(key, val)
    return env


def _split_message(text: str) -> list[str]:
    if len(text) <= MAX_DISCORD_LEN:
        return [text]
    chunks: list[str] = []
    current = ""
    for line in text.split("\n"):
        candidate = current + "\n" + line if current else line
        if len(candidate) > MAX_DISCORD_LEN:
            if current:
                chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def post_discord(webhook_key: str = "DISCORD_WEBHOOK_ALERTS") -> int:
    env = _load_env()
    webhook = env.get(webhook_key, "")
    if not webhook:
        print(f"[ERROR] {webhook_key} not configured")
        return 1
    text = render_discord()
    for chunk in _split_message(text):
        r = requests.post(
            webhook,
            json={"content": chunk},
            headers={"User-Agent": "mstr-cio/1.0"},
            timeout=10,
        )
        r.raise_for_status()
    print(f"[INFO] Posted weekly liquidity report via {webhook_key}")
    return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Generate weekly liquidity report")
    parser.add_argument("--post", action="store_true", help="Post report to Discord webhook")
    parser.add_argument("--webhook-key", default="DISCORD_WEBHOOK_ALERTS", help="Webhook env key to use when posting")
    args = parser.parse_args()

    if args.post:
        return post_discord(args.webhook_key)

    print(render_discord())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
