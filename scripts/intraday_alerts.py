#!/usr/bin/env python3
"""
Intraday Alert Triggers — MSTR Options Engine
Runs every 5 min during market hours. Cooldown-based dedup per alert type.
"""

import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone, timedelta

DB_PATH = "/mnt/mstr-data/mstr.db"
STATE_FILE = "/home/openclaw/mstr-engine/logs/alert_state.json"
if not os.path.exists("/home/openclaw/mstr-engine/logs"):
    STATE_FILE = "/mnt/mstr-logs/alert_state.json"

sys.path.insert(0, "/mnt/mstr-scripts")
sys.path.insert(0, "/home/openclaw/mstr-engine/scripts")
from send_alert import send_alert

# Cooldown periods in minutes per alert type
COOLDOWNS = {
    "stage_transition": 240,   # 4 hours
    "sribi_cross": 1440,       # Once per direction per day
    "volume_spike": 120,       # 2 hours
    "price_level": 60,         # 1 hour per level
    "iv_spike": 240,           # 4 hours
    "flow_spike": 60,          # 1 hour
    "kill_condition": 30,      # 30 min (escalating)
    "edgar_filing": 999999,    # Once per filing URL
}


def load_state():
    """Load alert state. Reset date tracking daily but keep cooldown timestamps."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
        if state.get("date") != today:
            # New day: clear cooldowns but keep edgar URLs seen
            edgar_seen = state.get("edgar_seen", [])
            return {"date": today, "cooldowns": {}, "edgar_seen": edgar_seen}
        return state
    except (FileNotFoundError, json.JSONDecodeError):
        return {"date": today, "cooldowns": {}, "edgar_seen": []}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def can_fire(state, key, cooldown_type):
    """Check if alert can fire based on cooldown."""
    cooldowns = state.get("cooldowns", {})
    last_fired = cooldowns.get(key)
    if not last_fired:
        return True
    last_time = datetime.fromisoformat(last_fired)
    now = datetime.now(timezone.utc)
    minutes_since = (now - last_time).total_seconds() / 60
    return minutes_since >= COOLDOWNS.get(cooldown_type, 60)


def mark_fired(state, key):
    state.setdefault("cooldowns", {})[key] = datetime.now(timezone.utc).isoformat()


def check_stage_transition(conn, state):
    """Alert if any stage score crosses threshold. 4-hour cooldown."""
    alerts = 0
    sri = conn.execute(
        "SELECT stage_boolean, sth_mvrv, sth_mvrv_zone, sribi_score, "
        "fast_tl_color, slow_tl_color, slow_tl_slope_roc, consecutive_red_bars "
        "FROM sri_indicators ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    if not sri or not sri[0]:
        return alerts

    raw_scores = json.loads(sri[0])
    # Filter to numeric stage keys only (skip _confirmed, _raw, _regime etc.)
    scores = {k: v for k, v in raw_scores.items() if not k.startswith('_')}
    if not scores:
        return alerts
    current_stage = max(scores, key=scores.get)

    for stage_num, score in scores.items():
        if stage_num == current_stage:
            continue

        # Tiered thresholds
        for threshold in [60, 75, 90]:
            if score < threshold:
                continue
            key = f"stage_{current_stage}_to_{stage_num}_t{threshold}"
            if not can_fire(state, key, "stage_transition"):
                continue

            mark_fired(state, key)
            urgency = "⚡" if threshold == 60 else "🔥" if threshold == 75 else "🚨"
            send_alert(
                f"{urgency} Stage {current_stage}→{stage_num} Signal (score: {score})",
                f"Stage {stage_num} score hit **{score}** (threshold: {threshold})\n\n"
                f"Current: Stage {current_stage} ({scores[current_stage]})\n"
                f"MVRV: {sri[1]:.4f} ({sri[2]})\n"
                f"SRIBI: {sri[3]:.1f}\n"
                f"Fast TL: {sri[4]} | Slow TL: {sri[5]}\n"
                f"Red bars: {sri[7]}",
                "yellow" if threshold == 60 else "red",
            )
            alerts += 1
            print(f"  🔔 Stage {current_stage}→{stage_num} (score={score}, t={threshold})")

    # SRIBI zero-cross
    sri_prev = conn.execute(
        "SELECT sribi_score FROM sri_indicators ORDER BY timestamp DESC LIMIT 1 OFFSET 1"
    ).fetchone()
    if sri_prev and sri_prev[0] is not None and sri[3] is not None:
        prev_sribi = sri_prev[0]
        curr_sribi = sri[3]
        if prev_sribi < 0 and curr_sribi >= 0:
            key = "sribi_cross_bull"
            if can_fire(state, key, "sribi_cross"):
                mark_fired(state, key)
                mag = abs(prev_sribi)
                send_alert(
                    "⚡ SRIBI Zero-Cross (Bullish)",
                    f"SRIBI: {prev_sribi:.1f} → {curr_sribi:.1f}\n"
                    f"Magnitude: {mag:.1f} {'✅ above ±30 threshold' if mag >= 30 else '⚠️ below ±30 — low confidence'}",
                    "green" if mag >= 30 else "yellow",
                )
                alerts += 1
        elif prev_sribi >= 0 and curr_sribi < 0:
            key = "sribi_cross_bear"
            if can_fire(state, key, "sribi_cross"):
                mark_fired(state, key)
                send_alert(
                    "⚡ SRIBI Zero-Cross (Bearish)",
                    f"SRIBI: {prev_sribi:.1f} → {curr_sribi:.1f}",
                    "red" if abs(prev_sribi) >= 30 else "yellow",
                )
                alerts += 1

    return alerts


def check_volume_spike(conn, state):
    """Alert at 2.5x and escalate at 3.5x, 5x. 2-hour cooldown per tier."""
    alerts = 0
    latest = conn.execute(
        "SELECT timestamp, volume FROM ohlcv ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    if not latest:
        return alerts

    adv_row = conn.execute(
        "SELECT AVG(volume) FROM (SELECT volume FROM ohlcv ORDER BY timestamp DESC LIMIT 20)"
    ).fetchone()
    if not adv_row or not adv_row[0]:
        return alerts

    adv = adv_row[0]
    vol = latest[1]
    ratio = vol / adv if adv > 0 else 0

    for threshold, label in [(2.5, "Volume Spike"), (3.5, "Heavy Volume"), (5.0, "EXTREME Volume")]:
        if ratio < threshold:
            continue
        key = f"volume_{threshold}x"
        if not can_fire(state, key, "volume_spike"):
            continue

        mark_fired(state, key)
        color = "yellow" if threshold == 2.5 else "red"
        send_alert(
            f"🔺 {label}: {ratio:.1f}x ADV",
            f"Volume: **{vol:,.0f}** vs 20d ADV {adv:,.0f}\n"
            f"Ratio: **{ratio:.1f}x** (threshold: {threshold}x)\n\n"
            f"*{'Required for Stage 4→1 transition' if threshold == 2.5 else 'Possible capitulation event'}*",
            color,
        )
        alerts += 1
        print(f"  🔔 Volume {ratio:.1f}x ADV (threshold {threshold}x)")

    return alerts


def check_price_levels(conn, state):
    """Alert when price touches key levels. 1-hour cooldown per level."""
    alerts = 0
    latest = conn.execute(
        "SELECT close FROM ohlcv ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    if not latest:
        return alerts
    price = latest[0]

    sri = conn.execute(
        "SELECT fast_tl, slow_tl, support, resistance, robust_fit "
        "FROM sri_indicators ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    if not sri:
        return alerts

    levels = {
        "fast_tl": ("Fast TL", sri[0]),
        "slow_tl": ("Slow TL", sri[1]),
        "support": ("Support", sri[2]),
        "resistance": ("Resistance", sri[3]),
        "robust_fit": ("Robust Fit", sri[4]),
    }

    for lkey, (name, level) in levels.items():
        if not level:
            continue

        pct_dist = abs(price - level) / level
        if pct_dist > 0.01:
            continue

        key = f"level_{lkey}"
        if not can_fire(state, key, "price_level"):
            continue

        mark_fired(state, key)
        direction = "testing from below" if price < level else "testing from above"
        color = "yellow"
        if lkey == "support" and price <= level:
            color = "red"
        elif lkey == "resistance" and price >= level:
            color = "green"
        elif lkey == "slow_tl" and price >= level:
            color = "green"

        send_alert(
            f"📍 Price at {name}: ${level:.2f}",
            f"MSTR **${price:.2f}** — {direction} ({pct_dist:.1%} away)\n\n"
            f"Resistance: ${levels['resistance'][1]:.2f}\n"
            f"Slow TL: ${levels['slow_tl'][1]:.2f}\n"
            f"Robust Fit: ${levels['robust_fit'][1]:.2f}\n"
            f"Fast TL: ${levels['fast_tl'][1]:.2f}\n"
            f"Support: ${levels['support'][1]:.2f}",
            color,
        )
        alerts += 1
        print(f"  🔔 Price at {name}: ${level:.2f}")

    return alerts


def check_iv_spike(conn, state):
    """Alert if IV jumps ≥10pp. 4-hour cooldown."""
    alerts = 0
    rows = conn.execute(
        "SELECT timestamp, iv_30day FROM orats_core ORDER BY timestamp DESC LIMIT 2"
    ).fetchall()
    if len(rows) < 2 or not rows[0][1] or not rows[1][1]:
        return alerts

    curr_iv = rows[0][1]
    prev_iv = rows[1][1]
    change = (curr_iv - prev_iv) * 100

    for threshold in [10, 20]:
        if abs(change) < threshold:
            continue
        key = f"iv_spike_{threshold}"
        if not can_fire(state, key, "iv_spike"):
            continue

        mark_fired(state, key)
        direction = "SURGED" if change > 0 else "COLLAPSED"
        send_alert(
            f"📉 IV {direction}: {change:+.1f}pp",
            f"IV30: {prev_iv*100:.1f}% → {curr_iv*100:.1f}%\n"
            f"Change: **{change:+.1f}pp**\n\n"
            f"*{'Favor selling premium — wide spreads' if change > 0 else 'Reduce short vol exposure immediately'}*",
            "yellow" if change > 0 else "red",
        )
        alerts += 1
        print(f"  🔔 IV spike: {change:+.1f}pp")

    return alerts


def check_unusual_flow(conn, state):
    """Alert if net premium exceeds $5M. 1-hour cooldown. Escalate at $10M, $20M."""
    alerts = 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Use latest flow date if today has no data
    flow_date = conn.execute(
        "SELECT MAX(timestamp) FROM flow WHERE trade_type != 'dark_pool'"
    ).fetchone()[0]
    if not flow_date:
        return alerts
    # Skip if flow data is stale (>3 days — subscription canceled)
    flow_age = (datetime.now(timezone.utc).date() - datetime.strptime(str(flow_date)[:10], "%Y-%m-%d").date()).days
    if flow_age > 3:
        return alerts

    flow = conn.execute(
        "SELECT "
        "SUM(CASE WHEN sentiment='bullish' THEN premium ELSE 0 END), "
        "SUM(CASE WHEN sentiment='bearish' THEN premium ELSE 0 END) "
        "FROM flow WHERE timestamp=? AND trade_type != 'dark_pool'",
        (flow_date,),
    ).fetchone()

    if not flow or (not flow[0] and not flow[1]):
        return alerts

    bull = flow[0] or 0
    bear = flow[1] or 0
    net = bull - bear

    for threshold_m in [5, 10, 20]:
        threshold = threshold_m * 1_000_000
        if abs(net) < threshold:
            continue
        key = f"flow_{threshold_m}m"
        if not can_fire(state, key, "flow_spike"):
            continue

        mark_fired(state, key)
        direction = "BULLISH" if net > 0 else "BEARISH"
        urgency = "🐋" if threshold_m == 5 else "🐋🐋" if threshold_m == 10 else "🚨🐋🐋🐋"
        send_alert(
            f"{urgency} ${threshold_m}M+ Net {direction} Flow",
            f"Net Premium: **${net:+,.0f}**\n"
            f"Bull: ${bull:,.0f} | Bear: ${bear:,.0f}\n\n"
            f"*{'Major institutional bullish bet' if net > 0 else 'Major institutional bearish bet'}*",
            "green" if net > 0 else "red",
        )
        alerts += 1
        print(f"  🔔 Flow: ${net/1e6:+.1f}M (threshold ${threshold_m}M)")

    return alerts


def check_kill_conditions(conn, state):
    """Escalating alerts as price approaches kill level: 3%, 1.5%, <1%."""
    alerts = 0
    positions = conn.execute(
        "SELECT id, strategy, kill_condition, strikes "
        "FROM trade_log WHERE status='executed' AND kill_condition IS NOT NULL"
    ).fetchall()

    if not positions:
        return alerts

    latest = conn.execute(
        "SELECT close FROM ohlcv ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    if not latest:
        return alerts
    price = latest[0]

    for pos in positions:
        tid, strat, kill_cond, strikes = pos

        price_match = re.search(r'\$?([\d,]+(?:\.\d+)?)', kill_cond)
        if not price_match:
            continue

        kill_price = float(price_match.group(1).replace(",", ""))
        distance_pct = abs(price - kill_price) / kill_price if kill_price > 0 else 999

        # Escalating tiers
        tiers = [
            (0.03, "⚠️", "APPROACHING", "yellow"),
            (0.015, "🚨", "CLOSE TO", "red"),
            (0.01, "🔴🔴🔴", "IMMINENT —", "red"),
        ]

        for threshold, emoji, label, color in tiers:
            if distance_pct > threshold:
                continue
            key = f"kill_{tid}_{threshold}"
            if not can_fire(state, key, "kill_condition"):
                continue

            mark_fired(state, key)
            send_alert(
                f"{emoji} KILL {label} Trade #{tid}",
                f"**{strat}** | {strikes}\n\n"
                f"Kill: {kill_cond}\n"
                f"Price: **${price:.2f}** | Kill level: **${kill_price:.2f}**\n"
                f"Distance: **{distance_pct:.1%}**\n\n"
                f"{'⚠️ Review position.' if threshold == 0.03 else '🚨 **ACT NOW.**'}",
                color,
            )
            alerts += 1
            print(f"  {'⚠️' if threshold == 0.03 else '🚨'} Kill condition #{tid}: {distance_pct:.1%} away")

    return alerts


def check_edgar_new(conn, state):
    """Alert on new flagged filings. Once per unique filing URL."""
    alerts = 0
    edgar_seen = set(state.get("edgar_seen", []))

    filings = conn.execute(
        "SELECT timestamp, filing_type, summary, url FROM edgar "
        "WHERE (summary LIKE '%BTC PURCHASE%' OR summary LIKE '%ATM%' OR summary LIKE '%Convertible%') "
        "AND timestamp >= date('now', '-2 days') "
        "ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()

    for f in filings:
        url = f[3] or f"{f[0]}_{f[1]}"
        if url in edgar_seen:
            continue

        edgar_seen.add(url)
        is_purchase = "BTC PURCHASE" in (f[2] or "")

        title = "📋 "
        if is_purchase:
            title += "BTC Purchase Filing Detected"
        elif "ATM" in (f[2] or ""):
            title += "ATM/Offering Filing"
        else:
            title += "Convertible Note Filing"

        send_alert(
            title,
            f"**{f[1]}** — {f[0]}\n\n{f[2]}\n\n"
            f"*Saylor Event Discount Rule: discount Stage 3 signals during active purchase cycles.*",
            "green" if is_purchase else "blue",
        )
        alerts += 1
        print(f"  🔔 EDGAR: {f[1]} {f[0]}")

    state["edgar_seen"] = list(edgar_seen)[-100:]  # Keep last 100
    return alerts


DELTA_STATE_FILE = "/home/openclaw/mstr-engine/logs/alert_delta.json"
if not os.path.exists("/home/openclaw/mstr-engine/logs"):
    DELTA_STATE_FILE = "/mnt/mstr-logs/alert_delta.json"


def compute_current_snapshot(conn) -> dict:
    """Lightweight snapshot of key indicators for delta comparison.
    Fast: only 3 small queries. Used as pre-filter before full threshold checks."""
    snap = {}
    try:
        row = conn.execute(
            """SELECT sribi_score, fast_tl, slow_tl, sth_mvrv, stage_boolean,
                      consecutive_red_bars, volume_vs_20d_adv
               FROM sri_indicators WHERE timeframe='LT'
               ORDER BY timestamp DESC LIMIT 1"""
        ).fetchone()
        if row:
            raw = json.loads(row[4]) if row[4] else {}
            scores = {k: v for k, v in raw.items() if not k.startswith('_') and isinstance(v, (int, float))}
            stage = max(scores, key=scores.get) if scores else "unknown"
            snap["stage"] = stage
            snap["sribi"] = row[0] or 0
            snap["fast_tl"] = row[1] or 0
            snap["consecutive_red_bars"] = row[6] or 0
    except Exception:
        pass

    try:
        row = conn.execute(
            "SELECT close FROM ohlcv WHERE timeframe='1D' ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        if row:
            snap["price"] = row[0]
    except Exception:
        pass

    try:
        row = conn.execute(
            "SELECT iv_rank, iv_percentile FROM orats_core ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        if row:
            snap["iv_rank"] = row[0] or 0
    except Exception:
        pass

    try:
        row = conn.execute(
            "SELECT gate_state, loi FROM pmcc_gate_state WHERE asset='MSTR' ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        if row:
            snap["gate_state"] = row[0]
            snap["loi"] = row[1] or 0
    except Exception:
        pass

    return snap


def load_delta_state() -> dict:
    try:
        with open(DELTA_STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_delta_state(snap: dict):
    os.makedirs(os.path.dirname(DELTA_STATE_FILE), exist_ok=True)
    with open(DELTA_STATE_FILE, "w") as f:
        json.dump(snap, f)


def is_meaningful_change(curr: dict, prev: dict) -> tuple[bool, str]:
    """Check if any metric changed enough to warrant running full threshold checks.
    Returns (changed: bool, reason: str)."""
    if not prev:
        return True, "first_run"

    # Price moved >0.5%
    curr_price = curr.get("price", 0)
    prev_price = prev.get("price", 1)
    if prev_price and abs(curr_price - prev_price) / max(prev_price, 1) > 0.005:
        return True, f"price_move {prev_price:.2f}→{curr_price:.2f}"

    # LOI moved >2 points
    if abs(curr.get("loi", 0) - prev.get("loi", 0)) > 2.0:
        return True, f"loi_move {prev.get('loi', 0):.1f}→{curr.get('loi', 0):.1f}"

    # Stage changed
    if curr.get("stage") != prev.get("stage") and curr.get("stage"):
        return True, f"stage_change {prev.get('stage')}→{curr.get('stage')}"

    # Gate state changed
    if curr.get("gate_state") != prev.get("gate_state") and curr.get("gate_state"):
        return True, f"gate_change {prev.get('gate_state')}→{curr.get('gate_state')}"

    # SRIBI moved >5 points
    if abs(curr.get("sribi", 0) - prev.get("sribi", 0)) > 5.0:
        return True, f"sribi_move {prev.get('sribi', 0):.1f}→{curr.get('sribi', 0):.1f}"

    # IV rank moved >3 points
    if abs(curr.get("iv_rank", 0) - prev.get("iv_rank", 0)) > 3.0:
        return True, f"iv_rank_move {prev.get('iv_rank', 0):.0f}→{curr.get('iv_rank', 0):.0f}"

    # New consecutive red bars
    if curr.get("consecutive_red_bars", 0) != prev.get("consecutive_red_bars", 0):
        return True, f"red_bars {prev.get('consecutive_red_bars',0)}→{curr.get('consecutive_red_bars',0)}"

    # Force re-check every 30 minutes regardless
    last_check = prev.get("_timestamp")
    if last_check:
        try:
            last_dt = datetime.fromisoformat(last_check)
            if (datetime.now(timezone.utc) - last_dt) > timedelta(minutes=30):
                return True, "forced_30min"
        except Exception:
            pass

    return False, "no_meaningful_change"


def main():
    start = time.time()
    now_str = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    print(f"=== Intraday Alerts — {now_str} ===")

    # ── Delta pre-filter ──────────────────────────────────────────────────────
    # Quick snapshot before opening full connection to all tables.
    # Skips full threshold checks (7 DB queries) if nothing meaningful changed.
    conn_quick = sqlite3.connect(DB_PATH)
    conn_quick.execute("PRAGMA busy_timeout=3000")
    curr_snap = compute_current_snapshot(conn_quick)
    conn_quick.close()

    prev_snap = load_delta_state()
    changed, reason = is_meaningful_change(curr_snap, prev_snap)

    if not changed:
        elapsed_skip = int((time.time() - start) * 1000)
        print(f"  ⏭️  Skipped (delta: {reason}) | {elapsed_skip}ms")
        return

    print(f"  🔍 Running checks (delta: {reason})")

    # Update delta state with timestamp
    curr_snap["_timestamp"] = datetime.now(timezone.utc).isoformat()
    save_delta_state(curr_snap)

    state = load_state()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")

    total = 0
    total += check_stage_transition(conn, state)
    total += check_volume_spike(conn, state)
    total += check_price_levels(conn, state)
    total += check_iv_spike(conn, state)
    total += check_unusual_flow(conn, state)
    total += check_kill_conditions(conn, state)
    total += check_edgar_new(conn, state)

    save_state(state)

    elapsed = int((time.time() - start) * 1000)
    cooldown_count = len(state.get("cooldowns", {}))
    print(f"  Checks: 7 | Alerts fired: {total} | Active cooldowns: {cooldown_count} | {elapsed}ms")

    if total > 0:
        conn.execute(
            """INSERT INTO debug_log (timestamp, script_name, level, message, duration_ms)
               VALUES (?, 'intraday_alerts', 'INFO', ?, ?)""",
            (datetime.now(timezone.utc).isoformat(), f"{total} alerts fired", elapsed),
        )
        conn.commit()

    conn.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test-volume-spike":
        print("=== SIMULATING VOLUME SPIKE ===")
        send_alert(
            "🔺 Volume Spike: 3.2x ADV",
            "Volume: **52,500,000** vs 20d ADV 16,400,000\n"
            "Ratio: **3.2x** (threshold: 2.5x)\n\n"
            "*Required for Stage 4→1 transition*",
            "yellow",
        )
        print("  🔔 Simulated volume spike sent")
    else:
        main()
