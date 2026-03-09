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

CREATE TABLE IF NOT EXISTS howell_phase_state (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT NOT NULL,
    phase       TEXT NOT NULL,
    confidence  REAL,
    score_rebound       REAL,
    score_calm          REAL,
    score_speculation   REAL,
    score_turbulence    REAL,
    xlk_sribi   REAL,   xlk_signal  TEXT,
    xly_sribi   REAL,   xly_signal  TEXT,
    xlf_sribi   REAL,   xlf_signal  TEXT,
    xle_sribi   REAL,   xle_signal  TEXT,
    xlp_sribi   REAL,   xlp_signal  TEXT,
    tlt_sribi   REAL,   tlt_signal  TEXT,
    gld_sribi   REAL,   gld_signal  TEXT,
    iwm_sribi   REAL,   iwm_signal  TEXT
);

CREATE TABLE IF NOT EXISTS howell_phase_transitions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT NOT NULL,
    from_phase  TEXT NOT NULL,
    to_phase    TEXT NOT NULL,
    confidence  REAL
);

CREATE TABLE IF NOT EXISTS pbear_state_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    asset           TEXT NOT NULL,
    state           TEXT NOT NULL,
    loi             REAL,
    signals_fired   TEXT,
    ab2_fast_gate   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS defensive_posture_log (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp            TEXT NOT NULL,
    posture              TEXT NOT NULL,
    forming_assets       TEXT,
    confirmed_assets     TEXT,
    ab4_floor            REAL,
    ab3_new_entries      INTEGER,
    expression3_eligible INTEGER,
    rationale            TEXT
);

CREATE TABLE IF NOT EXISTS expression3_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    level           TEXT NOT NULL,
    conditions_met  INTEGER,
    mnav            REAL,
    mstr_pbear      TEXT,
    howell_phase    TEXT,
    btc_lt_sribi    REAL,
    btc_lt_rolling  INTEGER
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

# P-BEAR alert codes
ALERT_PBEAR_WATCH       = "PBEAR_WATCH"        # LOI enters watch zone
ALERT_PBEAR_FORMING     = "PBEAR_FORMING"      # Primary bearish signal fires → AB2 pause
ALERT_PBEAR_CONFIRMED   = "PBEAR_CONFIRMED"    # Dual-TF confirmed → hedge entry zone
ALERT_PBEAR_INVALIDATED = "PBEAR_INVALIDATED"  # Thesis invalidated → resume normal

# DOI (Distribution Opportunity Index) alert codes — Momentum assets only
ALERT_DOI_T1_TRIM      = "DOI_T1_TRIM"       # LOI crosses +40 (25% trim — first signal)
ALERT_DOI_T2_TRIM      = "DOI_T2_TRIM"       # LOI crosses +60 (50% trim)
ALERT_DOI_T3_TRIM      = "DOI_T3_TRIM"       # LOI crosses +80 (75% trim)
ALERT_DOI_VLT_PEAK     = "DOI_VLT_PEAK"      # VLT SRI Bias crosses +20 — 100% exit WR
ALERT_DOI_LOI_ROLLOVER = "DOI_LOI_ROLLOVER"  # LOI rollover from peak — 89% exit WR

# Portfolio posture + Expression 3 alert codes
ALERT_PORTFOLIO_POSTURE_CHANGE = "PORTFOLIO_POSTURE_CHANGE"
ALERT_EXPRESSION3_SETUP        = "EXPRESSION3_SETUP"
ALERT_EXPRESSION3_ARMED        = "EXPRESSION3_ARMED"

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

    raw_color = alert.get("color", "blue")
    color = raw_color if isinstance(raw_color, int) else COLOR_MAP.get(raw_color, COLOR_MAP["blue"])
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

# ── Howell Phase helpers ──────────────────────────────────────────────────────

_PHASE_ACTION_LINES: Dict[str, str] = {
    'Rebound':     "**Action:** Full AB3 sizing on Beta (MSTR/IBIT) and Cyclicals (TSLA). AB2 call-writing active.",
    'Calm':        "**Action:** Maximum AB2 income activity. AB3 entries on all eligible assets.",
    'Speculation': "**Action:** Reduce equity/cyclical AB3 to 50% max. No new Beta calls until phase shifts. Energy/GLD favoured.",
    'Turbulence':  "**Action:** PAUSE AB2 call-writing. Hold existing LEAPs. Watch Beta assets for early Rebound signal. Preserve optionality.",
}

_TRANSITION_EMOJIS: Dict[str, str] = {
    ('Turbulence',   'Rebound'):    '🚀',
    ('Rebound',      'Calm'):       '☀️',
    ('Calm',         'Speculation'):'🍂',
    ('Speculation',  'Turbulence'): '🌧️',
    # Non-sequential transitions
    ('Turbulence',   'Calm'):       '🌤️',
    ('Rebound',      'Speculation'):'⚡',
}


def save_howell_state(conn: sqlite3.Connection, state) -> None:
    """Persist HowellPhaseState to DB."""
    ts = datetime.now(timezone.utc).isoformat()
    ps = state.phase_scores
    ss = state.sector_sribi
    sg = state.sector_signals
    conn.execute(
        """INSERT INTO howell_phase_state
           (timestamp, phase, confidence,
            score_rebound, score_calm, score_speculation, score_turbulence,
            xlk_sribi, xlk_signal, xly_sribi, xly_signal,
            xlf_sribi, xlf_signal, xle_sribi, xle_signal,
            xlp_sribi, xlp_signal, tlt_sribi, tlt_signal,
            gld_sribi, gld_signal, iwm_sribi, iwm_signal)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (ts, state.phase, state.confidence,
         ps.get('Rebound', 0), ps.get('Calm', 0),
         ps.get('Speculation', 0), ps.get('Turbulence', 0),
         ss.get('XLK', 0), sg.get('XLK', ''),
         ss.get('XLY', 0), sg.get('XLY', ''),
         ss.get('XLF', 0), sg.get('XLF', ''),
         ss.get('XLE', 0), sg.get('XLE', ''),
         ss.get('XLP', 0), sg.get('XLP', ''),
         ss.get('TLT', 0), sg.get('TLT', ''),
         ss.get('GLD', 0), sg.get('GLD', ''),
         ss.get('IWM', 0), sg.get('IWM', ''))
    )
    conn.commit()


def load_prev_howell_phase(conn: sqlite3.Connection) -> Optional[str]:
    """Return the most recently saved Howell phase label, or None."""
    row = conn.execute(
        "SELECT phase FROM howell_phase_state ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return row[0] if row else None


def detect_howell_transition(state, prev_phase: Optional[str]) -> Optional[Dict]:
    """
    Return an alert dict if the Howell phase has changed, else None.
    state: HowellPhaseState
    """
    if prev_phase is None or prev_phase == state.phase:
        return None

    key     = (prev_phase, state.phase)
    emoji   = _TRANSITION_EMOJIS.get(key, '🔄')
    action  = _PHASE_ACTION_LINES.get(state.phase, '')
    scores  = " | ".join(f"{p}: {v:+.0f}" for p, v in state.phase_scores.items())
    sectors = "\n".join(
        f"  {t}: `{state.sector_signals.get(t,'?')}` (LT={state.sector_sribi.get(t,0):+.0f})"
        for t in ['XLK','XLY','XLF','XLE','XLP','TLT','GLD','IWM']
    )

    body = (
        f"**Howell Macro Phase shifted:** `{prev_phase}` → `{state.phase}` {state.emoji}\n"
        f"**Confidence:** `{state.confidence:.0f}%`\n\n"
        f"**Phase scores:** {scores}\n\n"
        f"**Sector signals:**\n{sectors}\n\n"
        f"{action}"
    )

    return {
        "asset":      "MACRO",
        "alert_type": "HOWELL_PHASE_TRANSITION",
        "prev_state": prev_phase,
        "new_state":  state.phase,
        "color":      0x1DB954 if state.phase in ('Rebound', 'Calm') else (
                      0xD29922 if state.phase == 'Speculation' else 0xF85149),
        "emoji":      emoji,
        "title":      f"{emoji} Howell Phase: {prev_phase} → {state.phase}",
        "body":       body,
        "current":    {"phase": state.phase, "confidence": state.confidence},
    }


# ── P-BEAR state change detection ─────────────────────────────────────────────

def load_prev_pbear_states(conn: sqlite3.Connection) -> Dict[str, str]:
    """Load most recent P-BEAR state per asset from pbear_state_log."""
    rows = conn.execute(
        """SELECT asset, state FROM pbear_state_log
           WHERE id IN (
               SELECT MAX(id) FROM pbear_state_log GROUP BY asset
           )"""
    ).fetchall()
    return {r[0]: r[1] for r in rows}


def save_pbear_states(conn: sqlite3.Connection, pbear_sigs: Dict) -> None:
    """Persist current P-BEAR signals to pbear_state_log."""
    now = datetime.now(timezone.utc).isoformat()
    for asset, sig in pbear_sigs.items():
        try:
            conn.execute(
                """INSERT INTO pbear_state_log
                   (timestamp, asset, state, loi, signals_fired, ab2_fast_gate)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (now, asset, sig.state.name, sig.loi,
                 json.dumps(sig.signals_fired()), int(sig.ab2_fast_gate))
            )
        except Exception:
            pass
    conn.commit()


def save_defensive_posture(conn: sqlite3.Connection, state) -> None:
    """Persist defensive posture state to defensive_posture_log."""
    conn.execute("""
        INSERT INTO defensive_posture_log
        (timestamp, posture, forming_assets, confirmed_assets, ab4_floor,
         ab3_new_entries, expression3_eligible, rationale)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        state.posture.name,
        ','.join(state.forming_assets),
        ','.join(state.confirmed_assets),
        state.ab4_floor_override,
        int(state.ab3_new_entries),
        int(state.expression3_eligible),
        state.rationale,
    ))
    conn.commit()


def save_expression3(conn: sqlite3.Connection, state) -> None:
    """Persist Expression 3 trigger state to expression3_log."""
    conn.execute("""
        INSERT INTO expression3_log
        (timestamp, level, conditions_met, mnav, mstr_pbear,
         howell_phase, btc_lt_sribi, btc_lt_rolling)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        state.level, state.conditions_met, state.mnav,
        state.mstr_pbear, state.howell_phase, state.btc_lt_sribi,
        int(state.btc_lt_rolling),
    ))
    conn.commit()


def load_prev_defensive_posture(conn: sqlite3.Connection) -> str:
    """Return most recent posture name from DB, or 'NORMAL' if none."""
    row = conn.execute(
        "SELECT posture FROM defensive_posture_log ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return row[0] if row else 'NORMAL'


def load_prev_expression3_level(conn: sqlite3.Connection) -> str:
    """Return most recent Expression 3 level from DB, or 'INACTIVE' if none."""
    row = conn.execute(
        "SELECT level FROM expression3_log ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return row[0] if row else 'INACTIVE'


def detect_pbear_alerts(pbear_sigs: Dict, prev_pbear: Dict[str, str]) -> List[Dict]:
    """
    Detect P-BEAR state transitions and generate alerts.

    Alert hierarchy:
      INACTIVE/WATCH  → FORMING/+    → ALERT_PBEAR_FORMING
      FORMING/+       → CONFIRMED/+  → ALERT_PBEAR_CONFIRMED
      any             → WATCH        → ALERT_PBEAR_WATCH (first time watch)
      FORMING+/CONF+  → INVALIDATED  → ALERT_PBEAR_INVALIDATED
    """
    alerts = []
    _PBEAR_ORDER = ["INACTIVE", "WATCH", "FORMING", "FORMING_PLUS",
                    "CONFIRMED", "CONFIRMED_PLUS", "INVALIDATED"]
    _COLOR = {
        ALERT_PBEAR_WATCH:       "yellow",
        ALERT_PBEAR_FORMING:     "orange",
        ALERT_PBEAR_CONFIRMED:   "red",
        ALERT_PBEAR_INVALIDATED: "green",
    }
    _EMOJI = {
        ALERT_PBEAR_WATCH:       "👁",
        ALERT_PBEAR_FORMING:     "🟠",
        ALERT_PBEAR_CONFIRMED:   "🚨",
        ALERT_PBEAR_INVALIDATED: "✅",
    }

    for asset, sig in pbear_sigs.items():
        curr_state = sig.state.name
        prev_state = prev_pbear.get(asset, "INACTIVE")

        if curr_state == prev_state:
            continue

        loi    = sig.loi
        price  = sig.price
        sigs   = ", ".join(sig.signals_fired()) or "none"
        gate   = "🛑 AB2 PAUSED" if sig.ab2_fast_gate else "✅ AB2 OK"

        # Determine alert type
        alert_type = None
        if curr_state == "INVALIDATED":
            alert_type = ALERT_PBEAR_INVALIDATED
        elif curr_state in ("CONFIRMED", "CONFIRMED_PLUS"):
            alert_type = ALERT_PBEAR_CONFIRMED
        elif curr_state in ("FORMING", "FORMING_PLUS"):
            alert_type = ALERT_PBEAR_FORMING
        elif curr_state == "WATCH" and prev_state == "INACTIVE":
            alert_type = ALERT_PBEAR_WATCH

        if alert_type is None:
            continue

        title_map = {
            ALERT_PBEAR_WATCH:       f"P-BEAR Watch — {asset}",
            ALERT_PBEAR_FORMING:     f"P-BEAR FORMING — {asset} | AB2 Paused",
            ALERT_PBEAR_CONFIRMED:   f"🚨 P-BEAR CONFIRMED — {asset}",
            ALERT_PBEAR_INVALIDATED: f"P-BEAR Invalidated — {asset}",
        }
        body_map = {
            ALERT_PBEAR_WATCH: (
                f"**LOI entered bearish watch zone.**\n"
                f"LOI `{loi:+.1f}` | Price `${price:.2f}`\n"
                f"State: `{prev_state}` → `{curr_state}`\n"
                f"**Action:** Monitor for primary signal (MACD/RSI/OBV divergence)."
            ),
            ALERT_PBEAR_FORMING: (
                f"**Primary bearish signal fired — AB2 call-selling PAUSED.**\n"
                f"LOI `{loi:+.1f}` | Price `${price:.2f}`\n"
                f"State: `{prev_state}` → `{curr_state}`\n"
                f"Signals: `{sigs}`\n"
                f"Gate: {gate}\n"
                f"**Action:** Stop writing new short calls. Watch for CONFIRMED."
            ),
            ALERT_PBEAR_CONFIRMED: (
                f"**Dual-TF confirmation — distribution top likely.**\n"
                f"LOI `{loi:+.1f}` | Price `${price:.2f}`\n"
                f"State: `{prev_state}` → `{curr_state}`\n"
                f"Signals: `{sigs}`\n"
                f"Gate: {gate}\n"
                f"**Action:** Evaluate hedge entry. Consider defensive posture."
            ),
            ALERT_PBEAR_INVALIDATED: (
                f"**Bearish thesis invalidated — normal mode resumed.**\n"
                f"LOI `{loi:+.1f}` | Price `${price:.2f}`\n"
                f"State: `{prev_state}` → `{curr_state}`\n"
                f"**Action:** AB2 call-selling gate unlocked. Resume normal protocol."
            ),
        }

        alerts.append({
            "asset":      asset,
            "alert_type": alert_type,
            "prev_state": prev_state,
            "new_state":  curr_state,
            "color":      _COLOR[alert_type],
            "emoji":      _EMOJI[alert_type],
            "title":      title_map[alert_type],
            "body":       body_map[alert_type],
            "current":    {"loi": loi, "price": price},
        })

    return alerts


def detect_doi_alerts(prev_doi: Dict, curr_doi: Dict) -> list:
    """
    Detect DOI signal transitions for Momentum assets.
    Each alert fires once when a new signal appears (prev=False, curr=True).

    Args:
        prev_doi: {asset: DOISignal.to_dict()} from previous run (DB-backed)
        curr_doi: {asset: DOISignal} from current DOIEngine.compute_all()
    Returns:
        list of alert dicts
    """
    alerts = []
    emoji_map = {
        ALERT_DOI_T1_TRIM:      "⚠️",
        ALERT_DOI_T2_TRIM:      "🟠",
        ALERT_DOI_T3_TRIM:      "🔴",
        ALERT_DOI_VLT_PEAK:     "🌟",
        ALERT_DOI_LOI_ROLLOVER: "🚨",
    }
    color_map = {
        ALERT_DOI_T1_TRIM:      "orange",
        ALERT_DOI_T2_TRIM:      "orange",
        ALERT_DOI_T3_TRIM:      "red",
        ALERT_DOI_VLT_PEAK:     "red",
        ALERT_DOI_LOI_ROLLOVER: "red",
    }

    for asset, sig in curr_doi.items():
        prev = prev_doi.get(asset, {})
        loi  = sig.loi or 0
        vlt  = sig.vlt_bias or 0

        body_t1 = (f"**LOI T1 Trim \u2014 {asset}** | Sell 25% of LEAP position\n"
                   f"LOI `{loi:+.1f}` crossed above `+40`. Start first trim tranche.\n"
                   f"Sell 25% of AB3 LEAP. Tighten call strikes to OTM delta \u22640.25.")
        body_t2 = (f"**LOI T2 Trim \u2014 {asset}** | Sell 50% of remaining LEAP\n"
                   f"LOI `{loi:+.1f}` crossed above `+60`. Second trim tranche.\n"
                   f"Sell another 25% of AB3 LEAP (50% total now sold).")
        body_t3 = (f"**LOI T3 Trim \u2014 {asset}** | Sell 75% of original LEAP\n"
                   f"LOI `{loi:+.1f}` crossed above `+80`. Third trim tranche.\n"
                   f"Sell another 25% of AB3 LEAP (75% total now sold). Hold final 25% for exit.")
        body_vp = (f"\U0001f31f **VLT SRI Bias Peak \u2014 {asset}** | 100% Win Rate Exit Signal\n"
                   f"VLT SRI Bias `{vlt:+.1f}` crossed above `+20`.\n"
                   f"**Historical WR: 100% on MSTR.** Sell remaining AB3 LEAP. "
                   f"Close all open calls. Full exit.")
        body_lr = (f"\U0001f6a8 **LOI Rollover \u2014 {asset}** | 89% Win Rate Exit Signal\n"
                   f"LOI dropped 25+ pts from 20-bar peak (LOI now `{loi:+.1f}`).\n"
                   f"**Historical WR: 89% on MSTR.** Exit remaining LEAP position. "
                   f"Stop all call-writing. Cycle ending.")

        checks = [
            (ALERT_DOI_T1_TRIM,      sig.t1_active,      prev.get("t1_active", False),      body_t1),
            (ALERT_DOI_T2_TRIM,      sig.t2_active,      prev.get("t2_active", False),      body_t2),
            (ALERT_DOI_T3_TRIM,      sig.t3_active,      prev.get("t3_active", False),      body_t3),
            (ALERT_DOI_VLT_PEAK,     sig.vlt_peak,       prev.get("vlt_peak", False),       body_vp),
            (ALERT_DOI_LOI_ROLLOVER, sig.exit_rollover,  prev.get("exit_rollover", False),  body_lr),
        ]

        for alert_type, curr_val, prev_val, body in checks:
            if curr_val and not prev_val:
                # New signal — fire alert
                alerts.append({
                    "asset":      asset,
                    "alert_type": alert_type,
                    "emoji":      emoji_map[alert_type],
                    "color":      color_map[alert_type],
                    "title":      f"{emoji_map[alert_type]} DOI Signal — {asset}",
                    "body":       body,
                    "prev_state": "inactive",
                    "new_state":  alert_type.split("_", 1)[1] if "_" in alert_type else alert_type,
                    "current":    {"loi": loi, "price": 0},
                })

    return alerts


def load_prev_doi_states(conn: sqlite3.Connection) -> Dict:
    """Load previous DOI signal states from pmcc_alert_log (last fired alerts)."""
    prev = {}
    try:
        rows = conn.execute(
            """SELECT asset, alert_type FROM pmcc_alert_log
               WHERE alert_type LIKE 'DOI_%'
               AND id IN (SELECT MAX(id) FROM pmcc_alert_log
                          WHERE alert_type LIKE 'DOI_%' GROUP BY asset, alert_type)
               AND timestamp > datetime('now', '-2 days')"""
        ).fetchall()
        for asset, atype in rows:
            if asset not in prev:
                prev[asset] = {}
            if atype == ALERT_DOI_T1_TRIM:       prev[asset]["t1_active"] = True
            elif atype == ALERT_DOI_T2_TRIM:     prev[asset]["t2_active"] = True
            elif atype == ALERT_DOI_T3_TRIM:     prev[asset]["t3_active"] = True
            elif atype == ALERT_DOI_VLT_PEAK:    prev[asset]["vlt_peak"] = True
            elif atype == ALERT_DOI_LOI_ROLLOVER: prev[asset]["exit_rollover"] = True
    except Exception as e:
        pass  # Non-fatal — will just re-fire any active signals
    return prev


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

    # Howell phase — load prev, check transition, save current
    howell_state  = engine_result.get("howell")
    prev_phase    = load_prev_howell_phase(conn)
    howell_alert  = None
    if howell_state is not None:
        howell_alert = detect_howell_transition(howell_state, prev_phase)
        save_howell_state(conn, howell_state)

    # Load previous P-BEAR states and detect transitions
    prev_pbear    = load_prev_pbear_states(conn)
    pbear_signals = engine_result.get("pbear_signals", {})
    pbear_alerts  = detect_pbear_alerts(pbear_signals, prev_pbear) if pbear_signals else []
    if pbear_signals:
        save_pbear_states(conn, pbear_signals)

    # ── Defensive posture + Expression 3 ──────────────────────────────────────
    defensive_state = engine_result.get("defensive_posture")
    expr3_state     = engine_result.get("expression3")
    posture_alerts  = []

    if defensive_state is not None:
        prev_posture_str = load_prev_defensive_posture(conn)
        if defensive_state.posture.name != prev_posture_str:
            posture_color = (0xFF4444 if defensive_state.posture.value >= 2 else 0xFFAA00)
            posture_alerts.append({
                "asset":      "PORTFOLIO",
                "alert_type": ALERT_PORTFOLIO_POSTURE_CHANGE,
                "prev_state": prev_posture_str,
                "new_state":  defensive_state.posture.name,
                "color":      posture_color,
                "emoji":      defensive_state.emoji,
                "title":      f"🛡️ Portfolio Posture: {prev_posture_str} → {defensive_state.posture.name}",
                "body":       (
                    f"**{defensive_state.rationale}**\n"
                    f"AB4 floor: {defensive_state.ab4_floor_override:.0%} | "
                    f"AB3 new entries: {'✅' if defensive_state.ab3_new_entries else '🚫'} | "
                    f"Expr3 eligible: {'✅' if defensive_state.expression3_eligible else '⬜'}\n"
                    + (f"Forming: {', '.join(defensive_state.forming_assets)}\n"
                       if defensive_state.forming_assets else "")
                    + (f"Confirmed: {', '.join(defensive_state.confirmed_assets)}"
                       if defensive_state.confirmed_assets else "")
                ),
                "current":    {"loi": 0, "price": 0},
            })
        save_defensive_posture(conn, defensive_state)

    if expr3_state is not None:
        prev_e3_str = load_prev_expression3_level(conn)
        if expr3_state.level in ('SETUP', 'ARMED') and expr3_state.level != prev_e3_str:
            e3_code  = ALERT_EXPRESSION3_ARMED if expr3_state.level == 'ARMED' else ALERT_EXPRESSION3_SETUP
            e3_color = 0xFF0000 if expr3_state.level == 'ARMED' else 0xFF8800
            posture_alerts.append({
                "asset":      "MSTR",
                "alert_type": e3_code,
                "prev_state": prev_e3_str,
                "new_state":  expr3_state.level,
                "color":      e3_color,
                "emoji":      expr3_state.emoji,
                "title":      f"📐 Expression 3: {expr3_state.emoji} {expr3_state.level}",
                "body":       (
                    f"mNAV={expr3_state.mnav:.2f}x | MSTR P-BEAR={expr3_state.mstr_pbear} | "
                    f"Howell={expr3_state.howell_phase} | BTC LT rolling={expr3_state.btc_lt_rolling}\n"
                    f"Conditions met: {expr3_state.conditions_met}/4\n"
                    f"Structure: Long MSTR debit put spread (ATM/OTM 20-25%, 90-120 DTE) + Long IBIT"
                ),
                "current":    {"loi": 0, "price": 0},
            })
        save_expression3(conn, expr3_state)

    # Detect all alert types
    all_alerts = []
    all_alerts += detect_gate_transitions(prev_states, current_states)
    all_alerts += detect_ab3_watch(prev_states, current_states)   # Stage 1 zone entry
    all_alerts += detect_ab3_alerts(ab3_signals)                  # Stage 2 buy + trim
    all_alerts += detect_ab1_alerts(ab1_signals)
    all_alerts += pbear_alerts                                      # P-BEAR top detection

    # DOI distribution alerts (Momentum assets: MSTR/IBIT/TSLA)
    try:
        from doi_engine import DOIEngine
        _doi_engine  = DOIEngine()
        _doi_curr    = _doi_engine.compute_all()
        _doi_prev    = load_prev_doi_states(conn)
        _doi_alerts  = detect_doi_alerts(_doi_prev, _doi_curr)
        all_alerts  += _doi_alerts
    except Exception as _doi_err:
        print(f"  [pmcc_alerts] DOI alerts skipped: {_doi_err}")
    all_alerts += posture_alerts                                    # Portfolio posture + Expr3
    if howell_alert:
        all_alerts.insert(0, howell_alert)  # Phase transitions lead the alert queue

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
