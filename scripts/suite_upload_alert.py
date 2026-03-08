#!/usr/bin/env python3
"""
suite_upload_alert.py — P-MSTR-SUITE CSV Upload Detector & Alerter
====================================================================
Runs daily (suggested: 09:00 UTC and 15:00 UTC). Checks GitHub for
new Suite CSV commits. If any Suite CSV was updated since last check,
runs the force engine and sends channel-appropriate alerts to:

  #mstr-gavin  — full engine signal + component breakdown
  #mstr-greg   — bottom-line direction + gate status (no dollar amounts)
  #mstr-gary   — plain English + one observable thing to watch

Usage:
  python3 suite_upload_alert.py             # check and alert if new
  python3 suite_upload_alert.py --force     # alert regardless of freshness
  python3 suite_upload_alert.py --dry-run   # compute + print, no send
"""

import json
import os
import sys
import ssl
import sqlite3
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
DB_PATH    = Path("/mnt/mstr-data/mstr.db")
CONFIG_ENV = Path("/mnt/mstr-config/.env")
TOKEN_ENV  = Path("/mnt/mstr-data/.env_tokens")

GITHUB_REPO   = "3ServantsP35/Grok"
GITHUB_BRANCH = "main"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode    = ssl.CERT_NONE

# ── Suite CSV filenames (confirmed working 2026-03-08) ────────────────────────
SUITE_CSVS = {
    "BATS_MSTR, 240_8ee08.csv":              "MSTR",
    "INDEX_BTCUSD, 240_29008.csv":           "BTC",
    "CRYPTOCAP_STABLE.C.D, 240_cbdd5.csv":   "STABLE.D",
    "BATS_STRC, 240_92d2f.csv":              "STRC",
    "BATS_STRF_BATS_LQD, 240_22e21.csv":    "STRF/LQD",
    "BATS_MSTR_BATS_IBIT, 240_56652.csv":   "MSTR/IBIT",
}

# ── Env loader ────────────────────────────────────────────────────────────────
def load_env() -> dict:
    env = {}
    for path in [CONFIG_ENV, TOKEN_ENV]:
        if path.exists():
            for line in path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip().strip('"').strip("'")
    env.update(os.environ)
    return env

# ── GitHub helpers ────────────────────────────────────────────────────────────
def github_request(url: str, token: str) -> dict | list | None:
    headers = {
        "Accept":        "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[suite_alert] GitHub request failed: {e}")
        return None

def get_latest_commit_date(filename: str, token: str) -> datetime | None:
    """Return UTC datetime of the most recent commit touching this file."""
    url = (f"https://api.github.com/repos/{GITHUB_REPO}/commits"
           f"?path={urllib.parse.quote(filename)}&per_page=1&sha={GITHUB_BRANCH}")
    data = github_request(url, token)
    if data and len(data) > 0:
        date_str = data[0]["commit"]["committer"]["date"]
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return None

# ── DB helpers ────────────────────────────────────────────────────────────────
def get_last_seen_ts(conn: sqlite3.Connection) -> datetime | None:
    try:
        row = conn.execute(
            "SELECT value FROM engine_config WHERE key='suite_last_upload_ts'"
        ).fetchone()
        if row:
            return datetime.fromisoformat(row[0])
    except Exception:
        pass
    return None

def set_last_seen_ts(conn: sqlite3.Connection, ts: datetime):
    conn.execute("""
        INSERT OR REPLACE INTO engine_config (key, value)
        VALUES ('suite_last_upload_ts', ?)
    """, (ts.isoformat(),))
    conn.commit()

def ensure_engine_config(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS engine_config
        (key TEXT PRIMARY KEY, value TEXT)
    """)
    conn.commit()

# ── Discord sender ────────────────────────────────────────────────────────────
def send_discord(webhook_url: str, message: str, dry_run: bool = False):
    if dry_run:
        print(f"\n{'─'*60}\n{message}\n{'─'*60}")
        return
    if not webhook_url:
        print(f"[suite_alert] No webhook — skipping: {message[:80]}")
        return
    payload = json.dumps({"content": message}).encode()
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            code = resp.getcode()
            if code not in (200, 204):
                print(f"[suite_alert] Discord HTTP {code}")
    except Exception as e:
        print(f"[suite_alert] Discord send error: {e}")

# ── Message formatters ────────────────────────────────────────────────────────
def format_gavin(signal: dict, updated_files: list, ts_str: str) -> str:
    """Full technical depth for #mstr-gavin."""
    zone  = signal["zone"].replace("_", " ")
    conf  = "✅ HIGH" if signal["confidence"] == "HIGH" else "⚠️ PROVISIONAL"
    dir_icon = {"BULLISH": "📈", "BEARISH": "📉", "NONE": "➡️"}.get(signal["direction"], "")
    trend_icon = {"RISING": "↗", "FALLING": "↘", "FLAT": "→"}.get(signal["f_trend"], "")
    structs = " / ".join(signal["trade_structures"])
    updated_str = ", ".join(updated_files) if updated_files else "all"

    lines = [
        f"📊 **MSTR Suite — Fresh CSV Package Detected** ({ts_str})",
        f"Updated: `{updated_str}`",
        f"",
        f"**🧲 Force Signal**",
        f"Zone: {dir_icon} **{zone}** | Confidence: {conf}",
        f"F_net: `{signal['f_net']:+.4f}` | Trend: {trend_icon} {signal['f_trend']} "
        f"(`{'→'.join(str(v) for v in signal['f_net_3bar'])}`)",
        f"",
        f"**Components:**",
        f"• Primary STRF/LQD: `{signal['f_primary']:+.4f}` ← {signal['strf_lt_state']}",
        f"• Multiplier MIBIT LT: `{signal['multiplier']:.3f}` ← {signal['mibit_lt_state']}",
        f"• Credit STRC: `{signal['f_credit']:+.4f}` ← {signal['strc_st_state']}",
        f"• Liquidity STABLE.D: `{signal['f_friction']:+.4f}` ← {signal['stable_lt_state']}",
        f"• MSTR LT: {signal['mstr_lt_state']}",
        f"",
        f"**Trade:** {signal['direction']} | {structs} | DTE {signal['dte_range']}",
        f"**Sizing:** {signal['sizing']}",
    ]
    if signal["gate"] != "None — validated signal":
        lines.append(f"**Gate:** {signal['gate']}")
    return "\n".join(lines)


def format_greg(signal: dict, ts_str: str) -> str:
    """Bottom-line for #mstr-greg. No dollar amounts. Action first."""
    zone = signal["zone"].replace("_", " ")
    dir_icon = {"BULLISH": "📈", "BEARISH": "📉", "NONE": "➡️"}.get(signal["direction"], "")
    conf_tag = "" if signal["confidence"] == "HIGH" else " (provisional)"

    # Gate met?
    gate_met = signal["mibit_lt_state"] == "MOMENTUM_BULL"
    gate_str = "✅ Gate met — entry eligible" if gate_met else "⛔ Gate not met — hold"

    action = signal["direction"]
    if signal["confidence"] == "PROVISIONAL" and not gate_met:
        action_str = "No action — gate not met"
    elif signal["direction"] == "NONE":
        action_str = "AB2 income only — no directional trades"
    elif signal["direction"] == "BEARISH":
        action_str = f"Bearish{conf_tag} — {', '.join(signal['trade_structures'][:2])} | {signal['dte_range']} DTE | Full sizing"
    else:
        action_str = f"Bullish{conf_tag} — {', '.join(signal['trade_structures'][:2])} | {signal['dte_range']} DTE | Half sizing"

    lines = [
        f"📊 **Suite Update** ({ts_str})",
        f"",
        f"**{dir_icon} {zone}** | F_net: `{signal['f_net']:+.4f}` | {signal['f_trend']}",
        f"**Action:** {action_str}",
        f"**MSTR/IBIT LT:** {signal['mibit_lt_state']} — {gate_str}",
        f"**STRF/LQD LT:** {signal['strf_lt_state']}",
        f"**STRC:** {signal['strc_st_state']} | **STABLE.D:** {signal['stable_lt_state']}",
    ]
    return "\n".join(lines)


def format_gary(signal: dict, ts_str: str) -> str:
    """Plain English for #mstr-gary. Define terms. One observable."""
    zone  = signal["zone"]
    f_net = signal["f_net"]

    # Plain English zone descriptions
    zone_plain = {
        "STRONG_BULL": "early signs of a potential rally — not confirmed yet",
        "MOD_BULL":    "slightly favorable conditions — wait for confirmation",
        "NEUTRAL":     "no clear direction — forces are balanced",
        "MOD_BEAR":    "unfavorable conditions — downward pressure building",
        "STRONG_BEAR": "significant downward pressure — caution warranted",
    }.get(zone, "uncertain")

    # Instrument state in plain English
    strf_state = signal["strf_lt_state"]
    mibit_state = signal["mibit_lt_state"]

    strf_plain = {
        "MOMENTUM_BULL": "MicroStrategy's fundraising power is expanding (bullish)",
        "DECEL_BULL":    "MicroStrategy's fundraising power is starting to slow (early warning)",
        "MOMENTUM_BEAR": "MicroStrategy's fundraising power is contracting (bearish)",
        "DECEL_BEAR":    "Downward pressure on fundraising is easing (possible turn)",
        "TRANSITION":    "MicroStrategy's fundraising capacity is neutral — no clear trend",
        "CROSS_BULL":    "MicroStrategy's fundraising just turned bullish",
        "CROSS_BEAR":    "MicroStrategy's fundraising just turned bearish",
    }.get(strf_state, strf_state)

    # One thing to watch
    if mibit_state == "TRANSITION" and zone in ("STRONG_BULL", "MOD_BULL"):
        watch = ("Watch the MSTR/IBIT ratio (how much premium investors pay for MSTR over "
                 "just holding Bitcoin directly). When it starts rising consistently, that's "
                 "the green light for this bullish signal.")
    elif zone in ("MOD_BEAR", "STRONG_BEAR"):
        watch = ("Watch for MSTR to hold above its recent support levels. If it starts "
                 "making lower lows on high volume, that confirms the bearish reading.")
    elif zone == "NEUTRAL":
        watch = ("Watch for any of the six indicators to break out of their current "
                 "neutral state. The first to move usually sets the direction for the others.")
    else:
        watch = ("Watch MicroStrategy's preferred stock (STRC) — if it stays above $99, "
                 "credit conditions remain healthy and support any upside move.")

    lines = [
        f"📊 **Weekly Data Update** ({ts_str})",
        f"",
        f"Fresh data is in. Here's what the system is seeing:",
        f"",
        f"**Current reading:** {zone_plain}",
        f"*(Think of this like a weather forecast — it tells us the likely conditions "
        f"over the next 1-4 weeks, not a guarantee.)*",
        f"",
        f"**The key signal right now:**",
        f"{strf_plain}",
        f"",
        f"**One thing to watch this week:**",
        f"{watch}",
    ]
    return "\n".join(lines)

# ── Main logic ────────────────────────────────────────────────────────────────
def main():
    force   = "--force"   in sys.argv
    dry_run = "--dry-run" in sys.argv

    env   = load_env()
    token = env.get("GITHUB_TOKEN") or env.get("GH_TOKEN", "")
    if not token:
        print("[suite_alert] No GitHub token found — exiting")
        sys.exit(1)

    # Open DB
    conn = sqlite3.connect(DB_PATH)
    ensure_engine_config(conn)
    last_seen = get_last_seen_ts(conn)
    now = datetime.now(tz=timezone.utc)

    print(f"[suite_alert] Checking GitHub for new Suite CSVs... (last seen: {last_seen})")

    # Check each CSV for latest commit date
    latest_overall = None
    updated_files  = []

    for filename, label in SUITE_CSVS.items():
        commit_dt = get_latest_commit_date(filename, token)
        if commit_dt is None:
            print(f"  {label}: could not fetch")
            continue
        print(f"  {label}: last commit {commit_dt.strftime('%Y-%m-%d %H:%M UTC')}")
        if latest_overall is None or commit_dt > latest_overall:
            latest_overall = commit_dt
        if last_seen is None or commit_dt > last_seen:
            updated_files.append(label)

    if not force and not updated_files:
        print("[suite_alert] No new uploads detected. Nothing to send.")
        conn.close()
        return

    if force and not updated_files:
        updated_files = list(SUITE_CSVS.values())

    print(f"[suite_alert] New/updated: {updated_files}")

    # Run the force engine
    try:
        from mstr_suite_engine import MSTRSuiteEngine
        engine = MSTRSuiteEngine(force_refresh=True)
        signal = engine.compute_current_signal()
        engine.store_signal(signal)
        print(f"[suite_alert] Engine signal: zone={signal['zone']} f_net={signal['f_net']:+.4f}")
    except Exception as e:
        print(f"[suite_alert] Engine error: {e}")
        signal = None

    ts_str = now.strftime("%Y-%m-%d %H:%M UTC")

    # Send to all three channels
    webhook_gavin = env.get("DISCORD_WEBHOOK_GAVIN", "")
    webhook_greg  = env.get("DISCORD_WEBHOOK_GREG", "")
    webhook_gary  = env.get("DISCORD_WEBHOOK_GARY", "")

    if signal:
        msg_gavin = format_gavin(signal, updated_files, ts_str)
        msg_greg  = format_greg(signal, ts_str)
        msg_gary  = format_gary(signal, ts_str)
    else:
        # Engine failed — send minimal alert
        msg_gavin = f"📊 **Suite CSVs updated** ({ts_str}) — engine error, check logs."
        msg_greg  = f"📊 **Suite update** ({ts_str}) — data refreshed, engine error."
        msg_gary  = f"📊 **Weekly data update received** ({ts_str}). Analysis pending."

    print("[suite_alert] Sending alerts...")
    send_discord(webhook_gavin, msg_gavin, dry_run)
    send_discord(webhook_greg,  msg_greg,  dry_run)
    send_discord(webhook_gary,  msg_gary,  dry_run)

    # Update last-seen timestamp
    if not dry_run and latest_overall:
        set_last_seen_ts(conn, latest_overall)
        print(f"[suite_alert] Updated last-seen to {latest_overall.isoformat()}")

    conn.close()
    print("[suite_alert] Done.")


if __name__ == "__main__":
    main()
