#!/usr/bin/env python3
"""
PMCC Alerts — Gate transition detection and option action alerts.

Runs as Step 5 of daily_engine_run.py after the SRI engine produces results.
Compares current PMCC gate states against stored previous states and fires
Discord alerts on any transition.

Alert triggers:
  GATE_OPEN      : NO_CALLS → OTM_INCOME   — call-writing window opens
  GATE_CLOSE     : OTM_INCOME/DELTA_MGMT → NO_CALLS — accumulation, stop writing
  GATE_UPGRADE   : OTM_INCOME → DELTA_MGMT — ATM calls now permitted
  GATE_DOWNGRADE : DELTA_MGMT → OTM_INCOME — back to OTM-only mode
  AB1_PAUSE      : any → PAUSED_AB1        — breakout active, calls paused
  AB1_RESUME     : PAUSED_AB1 → any        — breakout done, calls resume
  AB3_BUY        : Stage 2 bounce signal fires (new within 24h)
  AB3_TRIM       : LOI trim level crossed (new within 24h)
  AB1_ENTRY      : New AB1 pre-breakout signal fires

State persistence: mstr.db table `pmcc_gate_state`
"""

import json
import os
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple

DB_PATH = "/mnt/mstr-data/mstr.db"

# ── DB schema ─────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS pmcc_gate_state (
    asset           TEXT PRIMARY KEY,
    gate_state      TEXT NOT NULL,
    loi             REAL,
    ct_tier         INTEGER,
    context         TEXT,
    max_delta       REAL,
    trim_threshold  REAL,
    price           REAL,
    lt_roc_state    TEXT,
    vlt_roc_state   TEXT,
    asset_class     TEXT,
    updated_at      TEXT
);

CREATE TABLE IF NOT EXISTS pmcc_alert_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT NOT NULL,
    asset       TEXT NOT NULL,
    alert_type  TEXT NOT NULL,
    prev_state  TEXT,
    new_state   TEXT,
    loi         REAL,
    price       REAL,
    message     TEXT,
    sent        INTEGER DEFAULT 0
);
"""

# ── Transition config ─────────────────────────────────────────────────────────

# (prev, new) → (alert_type, color, emoji, title_template, body_template)
TRANSITIONS: Dict[Tuple[str, str], Dict] = {
    ("NO_CALLS",   "OTM_INCOME"):  {
        "type": "GATE_OPEN", "color": "green", "emoji": "🟢",
        "title": "PMCC Gate OPEN — {asset}",
        "body": (
            "**Call-writing window is now open.**\n"
            "LOI `{loi:+.1f}` crossed above `-20` threshold.\n"
            "**Max delta:** `{max_delta:.2f}` (OTM only — never within 20% of spot)\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Scan for 30–45 DTE OTM calls on existing AB3 LEAP."
        ),
    },
    ("OTM_INCOME", "DELTA_MGMT"): {
        "type": "GATE_UPGRADE", "color": "orange", "emoji": "🟠",
        "title": "PMCC Delta Management — {asset}",
        "body": (
            "**LOI above DELTA_MGMT threshold — ATM/ITM calls permitted.**\n"
            "LOI `{loi:+.1f}` ≥ `{trim_threshold:+.0f}` (asset-class threshold).\n"
            "**Max delta:** `{max_delta:.2f}` — delta reduction mode active\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Can move short call closer to money. Use intentionally "
            "to reduce LEAP delta as position matures."
        ),
    },
    ("NO_CALLS",   "DELTA_MGMT"): {
        "type": "GATE_UPGRADE", "color": "orange", "emoji": "🟠",
        "title": "PMCC Delta Management (direct) — {asset}",
        "body": (
            "**LOI jumped directly to DELTA_MGMT — fast move.**\n"
            "LOI `{loi:+.1f}` ≥ `{trim_threshold:+.0f}`.\n"
            "**Max delta:** `{max_delta:.2f}`\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Evaluate ATM calls. Confirm AB3 trim schedule."
        ),
    },
    ("OTM_INCOME", "NO_CALLS"):   {
        "type": "GATE_CLOSE", "color": "red", "emoji": "🔴",
        "title": "PMCC Gate CLOSED — {asset}",
        "body": (
            "**LOI dropped back below `-20` — stop writing new calls.**\n"
            "LOI `{loi:+.1f}` | Previously in OTM_INCOME.\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Do not open new short calls. Manage/close existing "
            "short calls opportunistically. LEAP upside must be preserved."
        ),
    },
    ("DELTA_MGMT", "NO_CALLS"):   {
        "type": "GATE_CLOSE", "color": "red", "emoji": "🔴",
        "title": "PMCC Gate CLOSED (from DELTA_MGMT) — {asset}",
        "body": (
            "**Sharp LOI reversal — DELTA_MGMT → NO_CALLS.**\n"
            "LOI `{loi:+.1f}` | This is a fast correction signal.\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Close short calls immediately. Protect LEAP delta."
        ),
    },
    ("DELTA_MGMT", "OTM_INCOME"): {
        "type": "GATE_DOWNGRADE", "color": "yellow", "emoji": "🟡",
        "title": "PMCC Downgraded to OTM — {asset}",
        "body": (
            "**LOI fell below DELTA_MGMT threshold — return to OTM-only mode.**\n"
            "LOI `{loi:+.1f}` | Delta ≤ `{max_delta:.2f}` now.\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Roll any ATM/ITM calls back to OTM if practical. "
            "Tighten delta on next cycle."
        ),
    },
    ("OTM_INCOME", "PAUSED_AB1"): {
        "type": "AB1_PAUSE", "color": "yellow", "emoji": "⏸️",
        "title": "PMCC Paused — AB1 Active on {asset}",
        "body": (
            "**AB1 breakout signal active — call selling PAUSED.**\n"
            "Do not sell new calls while AB1 is live. Don't cap the move.\n"
            "Price: `${price:.2f}` | LOI `{loi:+.1f}`\n"
            "**Action:** Hold existing short calls. Do not open new ones until "
            "AB1 completes (LT turns positive or 90-bar time stop)."
        ),
    },
    ("DELTA_MGMT", "PAUSED_AB1"): {
        "type": "AB1_PAUSE", "color": "yellow", "emoji": "⏸️",
        "title": "PMCC Paused — AB1 Active on {asset}",
        "body": (
            "**AB1 breakout signal active — call selling PAUSED (was in DELTA_MGMT).**\n"
            "Breakout in progress — protect the upside.\n"
            "Price: `${price:.2f}` | LOI `{loi:+.1f}`\n"
            "**Action:** Consider closing current short calls to free delta. "
            "Watch for LT turn-positive as AB1 exit signal."
        ),
    },
    ("NO_CALLS",   "PAUSED_AB1"): {
        "type": "AB1_PAUSE", "color": "yellow", "emoji": "⏸️",
        "title": "AB1 Active (no calls open) — {asset}",
        "body": (
            "**AB1 pre-breakout signal active.** Gate was already NO_CALLS.\n"
            "Price: `${price:.2f}` | LOI `{loi:+.1f}`\n"
            "**Action:** Monitor AB1 LEAP entry. No short call action needed "
            "(gate was closed)."
        ),
    },
    ("PAUSED_AB1", "OTM_INCOME"): {
        "type": "AB1_RESUME", "color": "green", "emoji": "▶️",
        "title": "PMCC Resumed — AB1 Complete on {asset}",
        "body": (
            "**AB1 signal cleared — call selling RESUMED.**\n"
            "LOI `{loi:+.1f}` | Gate: OTM_INCOME | Max delta: `{max_delta:.2f}`\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Evaluate re-opening short call position."
        ),
    },
    ("PAUSED_AB1", "DELTA_MGMT"): {
        "type": "AB1_RESUME", "color": "orange", "emoji": "▶️",
        "title": "PMCC Resumed at DELTA_MGMT — {asset}",
        "body": (
            "**AB1 complete — resumed directly into DELTA_MGMT.**\n"
            "LOI `{loi:+.1f}` ≥ `{trim_threshold:+.0f}` | Max delta: `{max_delta:.2f}`\n"
            "**CT{ct_tier}** | {context} | Price: `${price:.2f}`\n"
            "**Action:** Review AB3 trim phase. ATM calls permitted."
        ),
    },
    ("PAUSED_AB1", "NO_CALLS"):   {
        "type": "AB1_RESUME", "color": "red", "emoji": "▶️",
        "title": "AB1 Complete — Gate Closed on {asset}",
        "body": (
            "**AB1 signal cleared but LOI dropped below gate floor.**\n"
            "LOI `{loi:+.1f}` | Returned to accumulation zone.\n"
            "Price: `${price:.2f}` | **No calls — preserve LEAP upside.**\n"
            "**Action:** AB1 may have failed → reclassify as AB3 if applicable."
        ),
    },
}

# AB3 signal types that trigger alerts
AB3_WATCH_SIGNALS = {"ACC_ENTER", "STAGE1_ENTER", "WATCH"}    # Stage 1: zone entered — prepare STRC
AB3_BUY_SIGNALS   = {"ACCUMULATE", "DEEP_ACCUMULATE", "STAGE2_BOUNCE", "BOUNCE"}  # Stage 2: act now
AB3_TRIM_SIGNALS  = {"TRIM_25", "TRIM_50", "TRIM_75", "EXIT_100", "DISTRIBUTE"}

# AB3_WATCH: LOI threshold per asset class (same as AB3 entry thresholds from AGENTS.md)
AB3_WATCH_THRESHOLD = {
    "MSTR": -45.0, "TSLA": -45.0, "IBIT": -45.0, "PURR": -45.0,  # Momentum
    "SPY":  -40.0, "QQQ":  -40.0, "GLD":  -40.0, "IWM":  -40.0,  # MR
}

COLOR_MAP = {"green": 0x238636, "orange": 0xE3B341, "red": 0xF85149,
             "yellow": 0xD29922, "blue": 0x1F6FEB}


# ── DB helpers ────────────────────────────────────────────────────────────────

def ensure_schema(conn: sqlite3.Connection) -> None:
    for stmt in SCHEMA.strip().split(";"):
        s = stmt.strip()
        if s:
            conn.execute(s)
    conn.commit()


def load_prev_states(conn: sqlite3.Connection) -> Dict[str, Dict]:
    rows = conn.execute(
        "SELECT asset, gate_state, loi, ct_tier, context, max_delta, "
        "trim_threshold, price, lt_roc_state, vlt_roc_state, asset_class "
        "FROM pmcc_gate_state"
    ).fetchall()
    return {
        r[0]: {
            "gate_state": r[1], "loi": r[2], "ct_tier": r[3],
            "context": r[4], "max_delta": r[5], "trim_threshold": r[6],
            "price": r[7], "lt_roc_state": r[8], "vlt_roc_state": r[9],
            "asset_class": r[10],
        }
        for r in rows
    }


def save_states(conn: sqlite3.Connection, states: Dict[str, Dict]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    for asset, s in states.items():
        conn.execute(
            """INSERT INTO pmcc_gate_state
               (asset, gate_state, loi, ct_tier, context, max_delta,
                trim_threshold, price, lt_roc_state, vlt_roc_state,
                asset_class, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(asset) DO UPDATE SET
                 gate_state=excluded.gate_state,
                 loi=excluded.loi,
                 ct_tier=excluded.ct_tier,
                 context=excluded.context,
                 max_delta=excluded.max_delta,
                 trim_threshold=excluded.trim_threshold,
                 price=excluded.price,
                 lt_roc_state=excluded.lt_roc_state,
                 vlt_roc_state=excluded.vlt_roc_state,
                 asset_class=excluded.asset_class,
                 updated_at=excluded.updated_at""",
            (asset,
             s.get("gate_state", ""),
             s.get("loi"), s.get("ct_tier"),
             s.get("context"), s.get("max_delta"),
             s.get("trim_threshold"), s.get("price"),
             s.get("lt_roc_state"), s.get("vlt_roc_state"),
             s.get("asset_class"), now)
        )
    conn.commit()


def log_alert(conn: sqlite3.Connection, asset: str, alert_type: str,
              prev: str, new: str, loi: float, price: float,
              message: str, sent: bool) -> None:
    conn.execute(
        """INSERT INTO pmcc_alert_log
           (timestamp, asset, alert_type, prev_state, new_state, loi, price, message, sent)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (datetime.now(timezone.utc).isoformat(), asset, alert_type,
         prev, new, loi, price, message, int(sent))
    )
    conn.commit()


# ── Transition detection ──────────────────────────────────────────────────────

def detect_gate_transitions(
    prev_states: Dict[str, Dict],
    current_states: Dict[str, Dict],
) -> List[Dict]:
    """
    Compare current vs previous gate states.
    Returns list of alert dicts for any changed asset.
    """
    alerts = []
    for asset, curr in current_states.items():
        prev     = prev_states.get(asset, {})
        prev_gs  = prev.get("gate_state", "")
        curr_gs  = curr.get("gate_state", "")

        if not prev_gs:
            # First time seeing this asset — record state, no alert
            continue

        if prev_gs == curr_gs:
            continue  # No change

        key = (prev_gs, curr_gs)
        if key not in TRANSITIONS:
            # Catch-all for any unexpected transition
            alerts.append({
                "asset":      asset,
                "alert_type": "GATE_CHANGE",
                "prev_state": prev_gs,
                "new_state":  curr_gs,
                "color":      "blue",
                "emoji":      "🔄",
                "title":      f"PMCC State Change — {asset}",
                "body":       (
                    f"`{prev_gs}` → `{curr_gs}`\n"
                    f"LOI `{curr.get('loi', 0):+.1f}` | "
                    f"CT{curr.get('ct_tier', 0)} | "
                    f"Price: `${curr.get('price', 0):.2f}`"
                ),
                "current":    curr,
            })
            continue

        cfg    = TRANSITIONS[key]
        loi    = curr.get("loi", 0) or 0
        ct     = curr.get("ct_tier", 0) or 0
        ctx    = curr.get("context", "") or ""
        price  = curr.get("price", 0) or 0
        delta  = curr.get("max_delta", 0) or 0
        thresh = curr.get("trim_threshold", 0) or 0

        body = cfg["body"].format(
            asset=asset, loi=loi, ct_tier=ct, context=ctx,
            price=price, max_delta=delta, trim_threshold=thresh,
        )
        alerts.append({
            "asset":      asset,
            "alert_type": cfg["type"],
            "prev_state": prev_gs,
            "new_state":  curr_gs,
            "color":      cfg["color"],
            "emoji":      cfg["emoji"],
            "title":      cfg["title"].format(asset=asset),
            "body":       body,
            "current":    curr,
        })

    return alerts


def detect_ab3_watch(
    prev_states: Dict[str, Dict],
    current_states: Dict[str, Dict],
) -> List[Dict]:
    """
    Detect when LOI first crosses below the AB3 accumulation threshold (Stage 1).
    Fires AB3_WATCH alert: "zone entered — begin sizing out of STRC gradually."

    Thresholds: Momentum assets (MSTR/TSLA/IBIT/PURR) = -45; MR (SPY/QQQ/GLD/IWM) = -40.
    Only fires on the crossing bar (prev ≥ threshold AND current < threshold).
    """
    alerts = []
    for asset, curr in current_states.items():
        prev     = prev_states.get(asset, {})
        curr_loi = curr.get("loi", 0) or 0.0
        prev_loi = prev.get("loi")
        threshold = AB3_WATCH_THRESHOLD.get(asset.upper(), -45.0)

        # Need previous LOI to detect crossing
        if prev_loi is None:
            continue

        prev_loi = float(prev_loi)

        # Only fire on the crossing: prev was above (or at) threshold, now below
        if prev_loi >= threshold and curr_loi < threshold:
            price = curr.get("price", 0) or 0
            ctx   = curr.get("context", "") or ""
            ct    = curr.get("ct_tier", 0) or 0
            depth = threshold - curr_loi   # how far below threshold

            alerts.append({
                "asset":      asset,
                "alert_type": "AB3_WATCH",
                "prev_state": f"LOI {prev_loi:+.1f}",
                "new_state":  f"LOI {curr_loi:+.1f} (below {threshold:+.0f})",
                "color":      "orange",
                "emoji":      "🔶",
                "title":      f"AB3 Stage 1 Watch — {asset}",
                "body": (
                    f"**LOI entered accumulation zone — Stage 1 active.**\n"
                    f"LOI `{curr_loi:+.1f}` crossed below `{threshold:+.0f}` threshold "
                    f"({depth:.1f} pts below).\n"
                    f"**CT{ct}** | {ctx} | Price: `${price:.2f}`\n\n"
                    f"**Action:** Begin gradually reducing STRC exposure. "
                    f"Do not wait for Stage 2 — preferred stocks can be thin intraday.\n"
                    f"**Watch for:** 2-bar confirmed LOI bounce from this level = 🎯 AB3_BUY signal."
                ),
                "current": curr,
            })

    return alerts


def detect_ab3_alerts(ab3_signals: Dict[str, List]) -> List[Dict]:
    """
    Scan today's AB3 signals for buy/trim events.
    Only alerts on signals with timestamp within last 48h (avoids re-alerting).
    """
    alerts = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

    for asset, sigs in ab3_signals.items():
        for sig in (sigs or []):
            # sig is a tuple from AB3LOIEngine — (signal_type, loi, price, date, ...)
            try:
                if isinstance(sig, (tuple, list)):
                    sig_type = str(sig[0]).upper() if sig else ""
                    loi      = float(sig[1]) if len(sig) > 1 else 0.0
                    price    = float(sig[2]) if len(sig) > 2 else 0.0
                    sig_date = sig[3] if len(sig) > 3 else None
                elif isinstance(sig, dict):
                    sig_type = str(sig.get("signal_type", "")).upper()
                    loi      = float(sig.get("loi", 0))
                    price    = float(sig.get("price", 0))
                    sig_date = sig.get("date") or sig.get("timestamp")
                else:
                    continue

                # Freshness check
                if sig_date is not None:
                    try:
                        if isinstance(sig_date, str):
                            ts = datetime.fromisoformat(sig_date.replace("Z", "+00:00"))
                        else:
                            ts = sig_date
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=timezone.utc)
                        if ts < cutoff:
                            continue
                    except Exception:
                        pass  # Can't parse date — include it

                if sig_type in AB3_WATCH_SIGNALS:
                    alerts.append({
                        "asset":      asset,
                        "alert_type": "AB3_WATCH",
                        "prev_state": "",
                        "new_state":  sig_type,
                        "color":      "orange",
                        "emoji":      "🔶",
                        "title":      f"AB3 Stage 1 Watch — {asset}",
                        "body": (
                            f"**Accumulation zone entered — Stage 1 active.**\n"
                            f"Signal: `{sig_type}` | LOI `{loi:+.1f}` | Price: `${price:.2f}`\n"
                            f"**Action:** Begin gradual STRC reduction. "
                            f"Watch for Stage 2 bounce confirmation → 🎯 AB3_BUY."
                        ),
                        "current": {"loi": loi, "price": price},
                    })

                elif sig_type in AB3_BUY_SIGNALS:
                    alerts.append({
                        "asset":      asset,
                        "alert_type": "AB3_BUY",
                        "prev_state": "",
                        "new_state":  sig_type,
                        "color":      "green",
                        "emoji":      "🎯",
                        "title":      f"AB3 BUY — Stage 2 Confirmed: {asset}",
                        "body": (
                            f"**Stage 2 bottom confirmed — actionable LEAP entry.**\n"
                            f"Signal: `{sig_type}` | LOI `{loi:+.1f}` | Price: `${price:.2f}`\n"
                            f"**Action:** Scale into 2-year OTM LEAPs per AB3 sizing rules. "
                            f"Confirm depth filter (LOI must have reached accumulation floor)."
                        ),
                        "current": {"loi": loi, "price": price},
                    })

                elif sig_type in AB3_TRIM_SIGNALS:
                    trim_map = {
                        "TRIM_25": ("25%", "orange"), "TRIM_50": ("50%", "orange"),
                        "TRIM_75": ("75%", "red"),    "EXIT_100": ("100% — EXIT", "red"),
                        "DISTRIBUTE": ("distribute", "red"),
                    }
                    pct, clr = trim_map.get(sig_type, (sig_type, "orange"))
                    alerts.append({
                        "asset":      asset,
                        "alert_type": "AB3_TRIM",
                        "prev_state": "",
                        "new_state":  sig_type,
                        "color":      clr,
                        "emoji":      "⚠️",
                        "title":      f"AB3 TRIM {pct} — {asset}",
                        "body": (
                            f"**LOI trim level crossed — reduce AB3 position {pct}.**\n"
                            f"Signal: `{sig_type}` | LOI `{loi:+.1f}` | Price: `${price:.2f}`\n"
                            f"**Action:** Sell {pct} of 2-year LEAP position. "
                            f"Review PMCC short calls — may need to close/roll before trimming LEAP."
                        ),
                        "current": {"loi": loi, "price": price},
                    })

            except Exception:
                continue

    return alerts


def detect_ab1_alerts(ab1_signals: Dict[str, List]) -> List[Dict]:
    """Alert on new AB1 pre-breakout signals (within 48h)."""
    alerts = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

    for asset, sigs in ab1_signals.items():
        for sig in (sigs or []):
            try:
                ts = getattr(sig, "timestamp", None)
                if ts:
                    if hasattr(ts, "tzinfo") and ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    if ts < cutoff:
                        continue
                conf   = getattr(sig, "confidence",  0.0)
                price  = getattr(sig, "price",        0.0)
                ct     = str(getattr(sig, "ct_level", ""))
                ctx    = str(getattr(sig, "context",  ""))
                loi    = float(getattr(sig, "metadata", {}).get("loi", 0) if hasattr(sig, "metadata") else 0)

                alerts.append({
                    "asset":      asset,
                    "alert_type": "AB1_ENTRY",
                    "prev_state": "",
                    "new_state":  "AB1_ACTIVE",
                    "color":      "blue",
                    "emoji":      "🚀",
                    "title":      f"AB1 Pre-Breakout Signal — {asset}",
                    "body": (
                        f"**Pre-breakout LEAP entry signal.**\n"
                        f"CT{ct} | {ctx} | Confidence: `{conf:.0%}`\n"
                        f"Price: `${price:.2f}` | LOI `{loi:+.1f}`\n"
                        f"**Action:** Buy OTM LEAP 60–120 DTE. "
                        f"Exit: LT turns positive OR 90-bar time stop. "
                        f"Target: 10%+ underlying move."
                    ),
                    "current": {"loi": loi, "price": price, "ct_tier": ct, "context": ctx},
                })
            except Exception:
                continue

    return alerts


# ── Discord send ──────────────────────────────────────────────────────────────

def send_alert_discord(alert: Dict, webhook_url: str) -> bool:
    """Send a single alert embed to Discord."""
    import urllib.request
    import ssl

    if not webhook_url:
        return False

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE

    color = COLOR_MAP.get(alert.get("color", "blue"), COLOR_MAP["blue"])
    ts    = datetime.now(timezone.utc).isoformat()

    # ROC context footer if available
    curr       = alert.get("current", {})
    lt_roc     = curr.get("lt_roc_state", "")
    vlt_roc    = curr.get("vlt_roc_state", "")
    roc_footer = ""
    if lt_roc or vlt_roc:
        roc_footer = f"\n-# LT ROC: {lt_roc}  |  VLT ROC: {vlt_roc}"

    description = alert["body"] + roc_footer + f"\n-# {ts}"

    payload = json.dumps({
        "username": "SRI Engine",
        "embeds": [{
            "title":       f"{alert['emoji']} {alert['title']}",
            "description": description,
            "color":       color,
            "timestamp":   ts,
        }]
    }).encode()

    req = urllib.request.Request(
        webhook_url, data=payload, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "mstr-cio/1.0"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            return r.status in (200, 204)
    except Exception as e:
        print(f"  [pmcc_alerts] Discord send failed for {alert['asset']}: {e}")
        return False


# ── Main entry point ──────────────────────────────────────────────────────────

def run(engine_result: Dict, webhook_url: str, db_path: str = DB_PATH) -> int:
    """
    Main entry point called from daily_engine_run.py after engine runs.

    Args:
        engine_result : dict returned by SRIEngineV2.run_all()
        webhook_url   : Discord webhook URL for alerts
        db_path       : path to mstr.db

    Returns:
        int: number of alerts sent
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    ensure_schema(conn)

    # Load previous gate states from DB
    prev_states = load_prev_states(conn)

    # Extract current PMCC states from engine result
    ab2_results   = engine_result.get("ab2_signals", {})
    ab3_signals   = engine_result.get("ab3_signals", {})
    ab1_signals   = engine_result.get("ab1_signals", {})
    current_states: Dict[str, Dict] = {}

    for asset, ab2 in ab2_results.items():
        curr = ab2.get("current", {}) if isinstance(ab2, dict) else {}
        if curr:
            current_states[asset] = curr

    # Detect all alert types
    all_alerts = []
    all_alerts += detect_gate_transitions(prev_states, current_states)
    all_alerts += detect_ab3_watch(prev_states, current_states)   # Stage 1 zone entry
    all_alerts += detect_ab3_alerts(ab3_signals)                  # Stage 2 buy + trim
    all_alerts += detect_ab1_alerts(ab1_signals)

    # Send alerts and log
    sent = 0
    for alert in all_alerts:
        ok = send_alert_discord(alert, webhook_url)
        log_alert(
            conn,
            asset      = alert["asset"],
            alert_type = alert["alert_type"],
            prev       = alert.get("prev_state", ""),
            new        = alert.get("new_state", ""),
            loi        = alert.get("current", {}).get("loi", 0),
            price      = alert.get("current", {}).get("price", 0),
            message    = alert["body"][:500],
            sent       = ok,
        )
        status = "✅" if ok else "❌"
        print(f"  [pmcc_alerts] {status} {alert['emoji']} {alert['alert_type']} — {alert['asset']} "
              f"({alert.get('prev_state', '')} → {alert.get('new_state', '')})")
        if ok:
            sent += 1

    # Save new gate states (even if no transitions — keeps DB fresh)
    if current_states:
        save_states(conn, current_states)

    conn.close()
    return sent


# ── Standalone run ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    """
    Standalone: initialize gate states without sending alerts.
    Run once after first deployment to seed the DB with current states.

    Usage: python3 pmcc_alerts.py --seed
    """
    import sys
    sys.path.insert(0, "/mnt/mstr-scripts")
    os.environ.setdefault("FRED_API_KEY", "8ee8d7967be4aab0fdc7565e85676260")

    seed_mode = "--seed" in sys.argv

    from sri_engine import SRIEngineV2
    engine  = SRIEngineV2()
    result  = engine.run_all(verbose=False)
    ab2     = result.get("ab2_signals", {})

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    ensure_schema(conn)

    current: Dict[str, Dict] = {}
    for asset, data in ab2.items():
        curr = data.get("current", {}) if isinstance(data, dict) else {}
        if curr:
            current[asset] = curr

    if seed_mode:
        save_states(conn, current)
        print(f"Seeded {len(current)} gate states into DB (no alerts sent).")
        for asset, s in current.items():
            print(f"  {asset:6s} → {s.get('gate_state'):15s}  LOI={s.get('loi', 0):+.1f}")
    else:
        prev = load_prev_states(conn)
        print(f"Previous states: {len(prev)} | Current: {len(current)}")
        transitions = detect_gate_transitions(prev, current)
        ab3_alerts  = detect_ab3_alerts(result.get("ab3_signals", {}))
        ab1_alerts  = detect_ab1_alerts(result.get("ab1_signals", {}))
        all_a = transitions + ab3_alerts + ab1_alerts
        print(f"Detected {len(all_a)} alerts (dry run — not sent):")
        for a in all_a:
            print(f"  {a['emoji']} {a['alert_type']} — {a['asset']}: "
                  f"{a.get('prev_state','')} → {a.get('new_state','')}")

    conn.close()
