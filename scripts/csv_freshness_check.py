#!/usr/bin/env python3
"""
csv_freshness_check.py — GitHub CSV freshness monitor (Task 8)

Checks last-commit timestamps for CANONICAL_CSVS on GitHub.
Flags files > 48h old (> 24h for MSTR).
Sends Gavin reminder if P-MSTR-SUITE CSVs are stale on Friday.

Usage:
  python3 csv_freshness_check.py              # full check
  python3 csv_freshness_check.py --suite-reminder   # Friday suite reminder only
"""

import json
import os
import sys
import ssl
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# ── Config ────────────────────────────────────────────────────────────────────
GITHUB_REPO = "3ServantsP35/Grok"
GITHUB_RAW_CONTENTS_URL = f"https://api.github.com/repos/{GITHUB_REPO}/commits"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

STALE_THRESHOLD_DEFAULT = timedelta(hours=48)
STALE_THRESHOLD_MSTR = timedelta(hours=24)

CANONICAL_CSVS = {
    "BATS_MSTR, 240_7b1cc.csv":               "MSTR (4H)",
    "BATS_IBIT, 240_7654d.csv":               "IBIT (4H)",
    "BATS_SPY, 240_8f6d8.csv":                "SPY (4H)",
    "BATS_QQQ, 240_5de53.csv":                "QQQ (4H)",
    "BATS_GLD, 240_41f2b.csv":                "GLD (4H)",
    "BATS_IWM, 240_9624e.csv":                "IWM (4H)",
    "BATS_TSLA, 240_b8831.csv":               "TSLA (4H)",
    "BATS_PURR, 240_0bdda.csv":               "PURR (4H)",
    "BATS_XLK, 240_e62e8.csv":                "XLK/Howell (4H)",
    "BATS_XLY, 240_73218.csv":                "XLY/Howell (4H)",
    "BATS_XLF, 240_e9161.csv":                "XLF/Howell (4H)",
    "BATS_XLE, 240_e801d.csv":                "XLE/Howell (4H)",
    "BATS_XLP, 240_3a323.csv":                "XLP/Howell (4H)",
    "INDEX_BTCUSD, 240_6739b.csv":            "BTC (4H)",
    "BATS_MSTR_BATS_IBIT, 240_05486.csv":     "MSTR/IBIT ratio (4H)",
    "CRYPTOCAP_STABLE.C.D, 240_7a8a0.csv":    "StabDom (4H)",
    "BATS_STRC, 240_5320c.csv":               "STRC (4H)",
    "BATS_TLT, 240_f930d.csv":                "TLT (4H)",
    "TVC_DXY, 240_d7e33.csv":                 "DXY (4H)",
    "BATS_HYG, 240_03e84.csv":                "HYG (4H)",
    "TVC_VIX, 240_5ff5f.csv":                 "VIX (4H)",
    "BATS_VT, 240_05664.csv":                 "VT/Global (4H)",
    "BATS_DBC, 240_5aa4d.csv":                "DBC/Commodities (4H)",
    "BATS_LQD, 240_1778d.csv":                "LQD (4H)",
}

# P-MSTR-SUITE subset (Gavin pushes these Fridays)
SUITE_CSVS = {
    "BATS_MSTR, 240_7b1cc.csv":               "MSTR LT",
    "BATS_STRC, 240_9969c.csv":               "STRC LT",
    "CRYPTOCAP_STABLE.C.D, 240_7a8a0.csv":    "StabDom",
    "BATS_STRF_BATS_LQD, 240_40822.csv":      "STRF/LQD",
    "BATS_MSTR_BATS_IBIT, 240_0ae35.csv":     "MSTR/IBIT",
}


def load_github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        for p in ["/mnt/mstr-data/.env_tokens",
                  "/home/openclaw/mstr-engine/data/.env_tokens"]:
            if os.path.exists(p):
                with open(p) as f:
                    for line in f:
                        if line.strip().startswith("GITHUB_TOKEN="):
                            token = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                            break
    return token


def get_last_commit_date(filename: str, token: str) -> datetime | None:
    """Query GitHub API for last commit date of a specific file."""
    # GitHub contents API: get commits for a specific path
    # We need to search within the repo for the file
    path = f"tradingview-exports/{filename}"
    url = f"{GITHUB_RAW_CONTENTS_URL}?path={urllib.parse.quote(path)}&per_page=1"

    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
            data = json.loads(resp.read())
            if data and len(data) > 0:
                date_str = data[0]["commit"]["committer"]["date"]
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        pass
    return None


def check_freshness(csv_dict: dict, token: str, mstr_threshold: bool = True) -> list:
    """
    Check freshness for all CSVs in dict.
    Returns list of dicts: {filename, label, last_commit, age_hours, stale, threshold_hours}
    """
    import urllib.parse
    results = []
    now = datetime.now(timezone.utc)

    for filename, label in csv_dict.items():
        threshold = (STALE_THRESHOLD_MSTR if "MSTR" in filename and mstr_threshold
                     else STALE_THRESHOLD_DEFAULT)

        last_commit = get_last_commit_date(filename, token)
        if last_commit:
            age = now - last_commit
            age_hours = age.total_seconds() / 3600
            stale = age > threshold
        else:
            age_hours = None
            stale = True  # Can't verify = assume stale

        results.append({
            "filename": filename,
            "label": label,
            "last_commit": last_commit.isoformat() if last_commit else "unknown",
            "age_hours": round(age_hours, 1) if age_hours else None,
            "stale": stale,
            "threshold_hours": threshold.total_seconds() / 3600,
        })

    return results


def load_discord_webhook(key: str) -> str:
    for p in ["/mnt/mstr-config/.env", "/home/openclaw/mstr-engine/config/.env"]:
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    if line.strip().startswith(f"{key}="):
                        return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def send_discord(webhook_url: str, message: str):
    if not webhook_url:
        print(f"[freshness] No webhook URL — message: {message[:100]}")
        return
    import urllib.parse
    payload = json.dumps({"content": message}).encode()
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            pass
    except Exception as e:
        print(f"[freshness] Discord send error: {e}")


def suite_reminder_mode():
    """Friday 2 PM ET reminder — check if suite CSVs are stale, ping Gavin."""
    token = load_github_token()
    results = check_freshness(SUITE_CSVS, token, mstr_threshold=True)

    stale = [r for r in results if r["stale"]]
    fresh = [r for r in results if not r["stale"]]

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if stale:
        stale_list = "\n".join(
            "  ❌ {} — {} (max {}h)".format(
                r['label'],
                "unknown age" if r['age_hours'] is None else f"{r['age_hours']:.0f}h old",
                int(r['threshold_hours'])
            )
            for r in stale
        )
        msg = (
            f"⚠️ **P-MSTR-SUITE: {len(stale)}/{len(results)} CSVs ARE STALE**\n"
            f"As of {now_str}\n\n"
            f"**Stale files:**\n{stale_list}\n\n"
            f"📋 Export from TradingView and push to GitHub by 4:00 PM ET.\n"
            f"Suite report runs at 4:30 PM ET. Stale data → report shows ⚠️ UNRELIABLE.\n"
            f"<@rizenshine5359>"
        )
    else:
        fresh_list = "\n".join(
            f"  ✅ {r['label']} — {r['age_hours']:.0f}h old"
            for r in fresh
        )
        msg = (
            f"✅ **P-MSTR-SUITE: All {len(results)} CSVs fresh**\n"
            f"As of {now_str}\n{fresh_list}\n"
            f"Suite report on track for 4:30 PM ET."
        )

    webhook = load_discord_webhook("DISCORD_WEBHOOK_ALERTS")
    send_discord(webhook, msg)
    print(msg)


def full_check_mode():
    """Full freshness check for all CANONICAL_CSVS. Returns summary."""
    token = load_github_token()
    print(f"Checking {len(CANONICAL_CSVS)} CSVs on GitHub...")
    results = check_freshness(CANONICAL_CSVS, token)

    stale = [r for r in results if r["stale"]]
    fresh = [r for r in results if not r["stale"]]

    print(f"\n{'CSV File':<50} {'Label':<25} {'Age':>8} {'Status'}")
    print("-" * 100)
    for r in sorted(results, key=lambda x: (x["stale"], -(x["age_hours"] or 9999))):
        age_str = f"{r['age_hours']:.0f}h" if r["age_hours"] else "unknown"
        status = "❌ STALE" if r["stale"] else "✅ OK"
        print(f"{r['filename']:<50} {r['label']:<25} {age_str:>8} {status}")

    print(f"\nSummary: {len(fresh)}/{len(results)} fresh, {len(stale)}/{len(results)} stale")

    if stale:
        print("\n⚠️ STALE FILES:")
        for r in stale:
            print(f"  {r['label']}: {r['filename']}")

    return {"fresh": len(fresh), "stale": len(stale), "total": len(results), "details": results}


def get_suite_freshness_status() -> dict:
    """Called by mstr_suite_report.py — returns stale status for suite CSVs."""
    token = load_github_token()
    results = check_freshness(SUITE_CSVS, token)
    stale = [r for r in results if r["stale"]]
    return {
        "all_fresh": len(stale) == 0,
        "stale_count": len(stale),
        "total": len(results),
        "stale_files": [r["label"] for r in stale],
        "details": results,
    }


if __name__ == "__main__":
    import urllib.parse  # needed in subfunctions

    if "--suite-reminder" in sys.argv:
        suite_reminder_mode()
    else:
        full_check_mode()
