#!/usr/bin/env python3
"""
daily_analysis_cycle.py — Multi-Agent Daily Analysis Pipeline (Task 5)

Flow:
  1. Load latest DB data and compute data payloads per analyst domain
  2. Call mstr-macro, mstr-technical, mstr-options, mstr-sri (Haiku/Sonnet/Haiku/Haiku)
  3. Validate all 4 responses
  4. Call CIO synthesis (Opus) with all 4 reports
  5. Write 5 rows to analysis table
  6. morning_brief.py reads CIO synthesis from analysis table

Cron: 10 12 * * 1-5  (10:10 AM ET = 12:10 UTC, after daily_engine_run.py)
"""

import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

DB_PATH = "/mnt/mstr-data/mstr.db"

# Add scripts directory to path
for p in ["/mnt/mstr-scripts", "/home/openclaw/mstr-engine/scripts"]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ── Model assignments ─────────────────────────────────────────────────────────
MODELS = {
    "mstr-macro":     "claude-haiku-4-5-20251001",
    "mstr-technical": "claude-haiku-4-5-20251001",
    "mstr-options":   "claude-sonnet-4-6",
    "mstr-sri":       "claude-haiku-4-5-20251001",
    "mstr-cio":       "claude-opus-4-6",
}

# Thinking budgets — disabled for sub-agents (structured JSON; thinking adds cost, not quality)
THINKING_CONFIG = {
    "mstr-macro":     None,                                       # disabled
    "mstr-technical": None,                                       # disabled
    "mstr-options":   None,                                       # disabled
    "mstr-sri":       None,                                       # disabled
    "mstr-cio":       {"type": "enabled", "budget_tokens": 5000}, # medium thinking
}

MAX_TOKENS = {
    "mstr-macro":     4096,
    "mstr-technical": 4096,
    "mstr-options":   6144,
    "mstr-sri":       4096,
    "mstr-cio":       8192,
}

WORKSPACE_ROOT = "/home/openclaw/.openclaw"


def log(msg: str):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}] {msg}")


def get_client():
    from api_utils import get_anthropic_client
    return get_anthropic_client()


JSON_ONLY_INSTRUCTION = """

---
## OUTPUT FORMAT — CRITICAL
Respond ONLY with a single valid JSON object.
- No markdown code fences (no ```json)
- No preamble, commentary, or explanation before or after the JSON
- No trailing text after the closing }
- The very first character of your response must be {
- The very last character of your response must be }
"""

def load_agent_prompt(agent_id: str) -> str:
    """Load AGENTS.md for a sub-agent and append JSON-only instruction."""
    path = Path(WORKSPACE_ROOT) / f"workspace-{agent_id}" / "AGENTS.md"
    if not path.exists():
        raise FileNotFoundError(f"AGENTS.md not found: {path}")
    return path.read_text() + JSON_ONLY_INSTRUCTION


def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


# ══════════════════════════════════════════════════════════════════════════════
# DATA PAYLOAD BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def build_macro_payload(conn: sqlite3.Connection) -> str:
    """Package macro/BTC/GLI data for mstr-macro."""
    now = datetime.now(timezone.utc)

    # Latest GLI proxy
    gli = conn.execute(
        "SELECT * FROM gli_proxy ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    gli_data = dict(gli) if gli else {}

    # FRED data (latest values for key series)
    fred_rows = conn.execute(
        """SELECT series_id, value, timestamp FROM fred
           WHERE timestamp >= date('now', '-5 days')
           ORDER BY series_id, timestamp DESC"""
    ).fetchall()
    fred_latest: dict = {}
    for row in fred_rows:
        sid = row["series_id"]
        if sid not in fred_latest:
            fred_latest[sid] = {"value": row["value"], "timestamp": row["timestamp"]}

    # Glassnode BTC metrics
    glass_rows = conn.execute(
        """SELECT metric_name, value, timestamp FROM glassnode
           WHERE timestamp >= date('now', '-3 days')
           ORDER BY metric_name, timestamp DESC"""
    ).fetchall()
    glass_latest: dict = {}
    for row in glass_rows:
        mn = row["metric_name"]
        if mn not in glass_latest:
            glass_latest[mn] = {"value": row["value"], "timestamp": row["timestamp"]}

    # Recent EDGAR filings
    edgar_rows = conn.execute(
        """SELECT timestamp, filing_type, title, btc_purchased, is_convertible_note, summary
           FROM edgar ORDER BY timestamp DESC LIMIT 5"""
    ).fetchall()
    edgar_list = [dict(r) for r in edgar_rows]

    # BTC price
    btc = conn.execute(
        "SELECT price_usd as price, timestamp FROM btc_price ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    btc_data = dict(btc) if btc else {}

    # Howell phase
    howell = conn.execute(
        """SELECT phase, confidence, score_turbulence, score_speculation, score_calm, score_rebound,
                  timestamp as updated_at
           FROM howell_phase_state WHERE id=1"""
    ).fetchone()
    howell_data = dict(howell) if howell else {}

    payload = {
        "analysis_date": now.strftime("%Y-%m-%d %H:%M UTC"),
        "btc_price": btc_data,
        "gli_proxy": gli_data,
        "fred_indicators": fred_latest,
        "btc_onchain": glass_latest,
        "edgar_recent_filings": edgar_list,
        "howell_phase_current": howell_data,
        "request": (
            "Analyze the macro environment, BTC on-chain health, GLI proxy, Howell phase, "
            "preferred share signals (check strc_spread and preferred_ohlcv tables if available), "
            "and any MSTR catalysts. Compute liquidity regime. Produce your full JSON output."
        ),
    }
    return json.dumps(payload, indent=2, default=str)


def build_technical_payload(conn: sqlite3.Connection) -> str:
    """Package MSTR OHLCV + volume for mstr-technical."""
    # 60 bars of daily OHLCV
    ohlcv = conn.execute(
        """SELECT timestamp, open, high, low, close, volume
           FROM ohlcv WHERE timeframe='1D'
           ORDER BY timestamp DESC LIMIT 60"""
    ).fetchall()
    ohlcv_list = [dict(r) for r in ohlcv]

    # Latest SRI for key levels reference
    sri_latest = conn.execute(
        """SELECT timestamp, timeframe, fast_tl, slow_tl, support, resistance, robust_fit,
                  volume_vs_20d_adv, volume_spike, consecutive_red_bars
           FROM sri_indicators WHERE timeframe='LT'
           ORDER BY timestamp DESC LIMIT 1"""
    ).fetchone()
    sri_data = dict(sri_latest) if sri_latest else {}

    # Recent intraday for same-day context
    intraday = conn.execute(
        """SELECT timestamp, open, high, low, close, volume
           FROM ohlcv_intraday ORDER BY timestamp DESC LIMIT 20"""
    ).fetchall()
    intraday_list = [dict(r) for r in intraday]

    payload = {
        "analysis_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "ohlcv_daily_60bars": ohlcv_list[::-1],  # chronological
        "sri_key_levels": sri_data,
        "intraday_recent": intraday_list[::-1],
        "request": (
            "Analyze MSTR price structure. Identify all key support and resistance levels "
            "with exact prices and reasons. Assess trend, momentum, volume vs ADV, "
            "and any active patterns. Produce your full JSON output. "
            "Focus on levels that would be useful for strike placement."
        ),
    }
    return json.dumps(payload, indent=2, default=str)


def build_options_payload(conn: sqlite3.Connection) -> str:
    """Package IV/options/flow data for mstr-options."""
    # ORATS core — latest
    orats = conn.execute(
        "SELECT * FROM orats_core ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    orats_data = dict(orats) if orats else {}

    # Options skew
    skew = conn.execute(
        "SELECT * FROM options_skew ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    skew_data = dict(skew) if skew else {}

    # Latest options chain (sample — near-term strikes within 20% of current price)
    chain = conn.execute(
        """SELECT expiry, strike, option_type, bid, ask, iv, delta, gamma, theta, vega, volume, open_interest
           FROM options_chain
           WHERE timestamp >= datetime('now', '-1 day')
           ORDER BY expiry, strike LIMIT 100"""
    ).fetchall()
    chain_list = [dict(r) for r in chain]

    # Flow (unusual whales — last 24h)
    flow = conn.execute(
        """SELECT timestamp, expiry, strike, option_type, sentiment, premium, volume, is_unusual
           FROM flow WHERE timestamp >= datetime('now', '-24 hours')
           ORDER BY premium DESC LIMIT 30"""
    ).fetchall()
    flow_list = [dict(r) for r in flow]

    # Current AB2 gate states from DB
    gates = conn.execute(
        """SELECT asset, gate_state, loi, ct_tier, context, max_delta, updated_at
           FROM pmcc_gate_state
           ORDER BY updated_at DESC LIMIT 20"""
    ).fetchall()
    gates_list = [dict(r) for r in gates]

    # Prior TA output for strike anchoring
    ta_output = conn.execute(
        """SELECT output_json FROM analysis
           WHERE agent_id='mstr-technical'
           ORDER BY timestamp DESC LIMIT 1"""
    ).fetchone()
    ta_data = json.loads(ta_output["output_json"]) if ta_output else {}

    # Current MSTR price
    price = conn.execute(
        "SELECT close FROM ohlcv WHERE timeframe='1D' ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    current_price = price["close"] if price else None

    # mNAV latest
    mnav = conn.execute(
        "SELECT mnav_ratio, premium_pct, btc_price, mstr_price, timestamp FROM mnav ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    mnav_data = dict(mnav) if mnav else {}

    payload = {
        "analysis_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "current_mstr_price": current_price,
        "mnav": mnav_data,
        "orats_core": orats_data,
        "options_skew": skew_data,
        "options_chain_sample": chain_list,
        "unusual_flow_24h": flow_list,
        "ab2_gate_states": gates_list,
        "ta_support_resistance": ta_data,
        "request": (
            "Analyze the IV environment, assess the current AB2 PMCC gate state for MSTR, "
            "and produce 2-3 trade ideas if conditions are favorable. "
            "Check all IV regime rules, mNAV ratio, hurdle rate (0.83%/month), "
            "and flow bias. Produce your full JSON output."
        ),
    }
    return json.dumps(payload, indent=2, default=str)


def build_sri_payload(conn: sqlite3.Connection) -> str:
    """Package SRI indicator data for mstr-sri."""
    # SRI indicators across all 4 TFs (last 5 bars each for trend context)
    sri_all = conn.execute(
        """SELECT timestamp, timeframe, fast_tl, fast_tl_color, slow_tl, slow_tl_color,
                  slow_tl_slope, slow_tl_slope_roc, sribi_score, sribi_score_v2,
                  sth_mvrv, sth_mvrv_zone, support, robust_fit, resistance,
                  volume_vs_20d_adv, volume_spike, consecutive_red_bars, stage_boolean
           FROM sri_indicators
           WHERE timestamp >= datetime('now', '-10 days')
           ORDER BY timeframe, timestamp DESC"""
    ).fetchall()

    # Organize by TF
    by_tf: dict = {}
    for row in sri_all:
        tf = row["timeframe"]
        if tf not in by_tf:
            by_tf[tf] = []
        if len(by_tf[tf]) < 5:
            by_tf[tf].append(dict(row))

    # Recent SRI signals (confirmed stage + transition probabilities)
    sri_signals = conn.execute(
        """SELECT timestamp, confirmed_stage, momentum_score, transition_prob_5d,
                  transition_prob_10d, transition_prob_20d, composite_signal,
                  mvrv, sribi, gli_zscore, close_price
           FROM sri_signals ORDER BY timestamp DESC LIMIT 10"""
    ).fetchall()
    signals_list = [dict(r) for r in sri_signals]

    # Howell phase for Gate Zero check
    howell = conn.execute(
        "SELECT phase, confidence, score_turbulence FROM howell_phase_state WHERE id=1"
    ).fetchone()
    howell_data = dict(howell) if howell else {}

    # GLI score (from gli_proxy table — gli_score is the Z-score equivalent)
    gli = conn.execute(
        "SELECT gli_score, gli_trend, grid_regime, macro_score FROM gli_proxy ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    gli_data = dict(gli) if gli else {}

    # Prior macro output for GLI meta-filter
    macro_output = conn.execute(
        """SELECT output_json FROM analysis
           WHERE agent_id='mstr-macro'
           ORDER BY timestamp DESC LIMIT 1"""
    ).fetchone()
    macro_data = json.loads(macro_output["output_json"]) if macro_output else {}

    payload = {
        "analysis_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "sri_indicators_by_tf": by_tf,
        "recent_transition_signals": signals_list,
        "howell_phase": howell_data,
        "gli_meta_filter": gli_data,
        "macro_context": {
            "regime": macro_data.get("macro_regime", "unknown"),
            "gli_score": (macro_data.get("gli_proxy", {}) or {}).get("z_score")
                         or gli_data.get("gli_score"),
            "liquidity_regime": macro_data.get("liquidity_regime", "unknown"),
        },
        "request": (
            "Analyze the SRI indicators across all timeframes. Apply all validated signal filters "
            "(volume confirmation, 3-consecutive-red-bars, SRIBI magnitude ±30, MVRV 5-bar validation). "
            "Apply GLI meta-filter from macro context. "
            "Designate the current stage using the 10-state taxonomy. "
            "Assess any active transition signals. Produce your full JSON output."
        ),
    }
    return json.dumps(payload, indent=2, default=str)


# ══════════════════════════════════════════════════════════════════════════════
# SUB-AGENT CALLS
# ══════════════════════════════════════════════════════════════════════════════

def call_sub_agent(client, agent_id: str, payload: str) -> Optional[dict]:
    """Call a sub-agent with its domain payload. Returns parsed JSON or None."""
    from api_utils import call_claude, get_response_text

    model = MODELS[agent_id]
    system_prompt = load_agent_prompt(agent_id)
    thinking = THINKING_CONFIG.get(agent_id)
    max_tokens = MAX_TOKENS[agent_id]

    log(f"Calling {agent_id} ({model}, max_tokens={max_tokens})...")
    start = time.time()

    response = call_claude(
        client=client,
        model=model,
        system=system_prompt,
        messages=[{"role": "user", "content": payload}],
        max_tokens=max_tokens,
        script_name=f"daily_analysis_cycle/{agent_id}",
        thinking=thinking,
    )

    elapsed = int((time.time() - start) * 1000)
    text = get_response_text(response)
    log(f"  {agent_id} responded in {elapsed}ms — {response.usage.input_tokens}in/{response.usage.output_tokens}out tokens")

    # Extract JSON from response
    json_text = text
    # Try to find JSON block
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if json_match:
        json_text = json_match.group(1)
    else:
        # Try to find raw JSON object
        json_start = text.find("{")
        json_end = text.rfind("}")
        if json_start >= 0 and json_end > json_start:
            json_text = text[json_start:json_end + 1]

    try:
        result = json.loads(json_text)
        return result
    except json.JSONDecodeError as e:
        log(f"  ⚠️ {agent_id} JSON parse error: {e} — storing raw text")
        return {"raw_text": text, "_parse_error": str(e)}


# ══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

REQUIRED_FIELDS = {
    "mstr-macro": ["macro_regime", "btc_directional_bias", "gli_proxy"],
    "mstr-technical": ["support_levels", "resistance_levels", "trend"],
    "mstr-options": ["iv_environment"],
    "mstr-sri": ["current_stage", "confidence"],
}


def validate_response(agent_id: str, result: dict) -> tuple[bool, list[str]]:
    """Validate sub-agent response has required fields."""
    if result is None:
        return False, ["null response"]
    if "_parse_error" in result:
        return False, [f"JSON parse error: {result['_parse_error']}"]

    required = REQUIRED_FIELDS.get(agent_id, [])
    missing = [f for f in required if f not in result]
    if missing:
        return False, [f"Missing required fields: {missing}"]
    return True, []


# ══════════════════════════════════════════════════════════════════════════════
# CIO SYNTHESIS
# ══════════════════════════════════════════════════════════════════════════════

def build_synthesis_prompt(reports: dict) -> str:
    """Build CIO synthesis prompt from all 4 analyst reports."""
    report_sections = []
    for agent_id, data in reports.items():
        section = f"### {agent_id.upper()} REPORT\n```json\n{json.dumps(data, indent=2, default=str)[:3000]}\n```"
        report_sections.append(section)

    return f"""You have received analysis from all four specialist agents. 

{chr(10).join(report_sections)}

Your task:
1. Identify any contradictions between analyst reports. Name them explicitly (e.g., "Macro says Risk-On but SRI says Stage 4 continuation — investigate this tension"). Do NOT average conflicting signals.
2. Determine the root cause of any contradiction and make a judgment call with explicit reasoning.
3. Synthesize a unified market view: current stage + confidence, macro regime, IV posture, key levels for strike placement.
4. Produce 2-3 actionable trade recommendations with full hypothesis blocks (minimum 3 hypotheses per trade, one labeled [Primary], each with data source tag, and a KILL CONDITION).
5. State portfolio management actions for existing positions.
6. State the key watch levels and triggers for the next 24-48 hours.
7. Log the signal_scores INSERT statement for today's stage call.

Apply all 8 permanent rules (GLI meta-filter, Saylor Event Discount Rule, Liquidity Regime TF Weighting, Vol-Adaptive LOI Threshold, AB4 deployment hurdle, etc.).

Format your response as a comprehensive morning brief that morning_brief.py can read from the analysis table.
"""


def call_cio_synthesis(client, reports: dict) -> Optional[str]:
    """Call CIO (Opus) with all 4 analyst reports for synthesis."""
    from api_utils import call_claude, get_response_text

    model = MODELS["mstr-cio"]
    thinking = THINKING_CONFIG["mstr-cio"]
    max_tokens = MAX_TOKENS["mstr-cio"]

    # Load CIO system prompt
    cio_system_path = Path(WORKSPACE_ROOT) / "workspace-mstr-cio" / "AGENTS.md"
    if cio_system_path.exists():
        system_prompt = cio_system_path.read_text()
    else:
        system_prompt = "You are the CIO for the MSTR Options Engine. Synthesize analyst reports into actionable recommendations."

    synthesis_payload = build_synthesis_prompt(reports)

    log(f"Calling CIO synthesis ({model}, max_tokens={max_tokens}, thinking=medium)...")
    start = time.time()

    response = call_claude(
        client=client,
        model=model,
        system=system_prompt,
        messages=[{"role": "user", "content": synthesis_payload}],
        max_tokens=max_tokens,
        script_name="daily_analysis_cycle/mstr-cio-synthesis",
        thinking=thinking,
    )

    elapsed = int((time.time() - start) * 1000)
    text = get_response_text(response)
    log(f"  CIO synthesis complete in {elapsed}ms ({elapsed//1000}s) — "
        f"{response.usage.input_tokens}in/{response.usage.output_tokens}out tokens")

    if elapsed > 180_000:  # > 3 minutes
        log("  ⚠️ Opus latency exceeded 3 minutes — consider falling back to Sonnet for cron cycles")

    return text


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE WRITES
# ══════════════════════════════════════════════════════════════════════════════

def write_to_analysis(conn: sqlite3.Connection, agent_id: str, analysis_type: str, output: dict | str):
    """Write agent output to analysis table."""
    if isinstance(output, str):
        output_json = json.dumps({"text": output})
    else:
        output_json = json.dumps(output, default=str)

    conn.execute(
        """INSERT OR REPLACE INTO analysis (timestamp, agent_id, analysis_type, output_json)
           VALUES (datetime('now'), ?, ?, ?)""",
        (agent_id, analysis_type, output_json),
    )
    conn.commit()
    log(f"  Wrote {agent_id}/{analysis_type} to analysis table ({len(output_json)} bytes)")


def log_signal_score(conn: sqlite3.Connection, stage: str, confidence: float):
    """Log today's stage call to signal_scores."""
    try:
        conn.execute(
            """INSERT INTO signal_scores (timestamp, agent_id, signal_type, prediction, confidence_at_call)
               VALUES (datetime('now'), 'mstr-sri', 'stage_call', ?, ?)""",
            (stage, confidence),
        )
        conn.commit()
        log(f"  Logged signal_score: stage_call={stage} confidence={confidence}")
    except Exception as e:
        log(f"  Warning: could not log signal_score: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    start_total = time.time()
    log("=" * 60)
    log("Daily Analysis Cycle — Starting")
    log("=" * 60)

    client = get_client()
    conn = db_connect()
    reports: dict = {}
    validation_errors: dict = {}

    # ── Phase 1: Sub-agent calls (sequential) ─────────────────────────────────
    agent_payloads = {
        "mstr-macro":     build_macro_payload(conn),
        "mstr-technical": build_technical_payload(conn),
        "mstr-options":   build_options_payload(conn),
        "mstr-sri":       build_sri_payload(conn),
    }

    for agent_id, payload in agent_payloads.items():
        log(f"\n── {agent_id} ──")
        try:
            result = call_sub_agent(client, agent_id, payload)
            valid, errors = validate_response(agent_id, result)
            if not valid:
                log(f"  ⚠️ Validation issues: {errors}")
                validation_errors[agent_id] = errors
            else:
                log(f"  ✅ Valid response")

            reports[agent_id] = result or {}
            write_to_analysis(conn, agent_id, "daily_analysis", result or {})

        except Exception as e:
            log(f"  ❌ {agent_id} failed: {e}")
            import traceback
            traceback.print_exc()
            reports[agent_id] = {"_error": str(e)}
            validation_errors[agent_id] = [str(e)]

    # ── Phase 2: Check we have enough to synthesize ────────────────────────────
    failed_agents = [a for a, r in reports.items() if "_error" in r]
    if len(failed_agents) >= 3:
        log(f"\n❌ Too many agent failures ({failed_agents}) — aborting synthesis")
        sys.exit(1)
    elif failed_agents:
        log(f"\n⚠️ {len(failed_agents)} agents failed ({failed_agents}) — proceeding with partial data")

    # ── Phase 3: CIO synthesis ────────────────────────────────────────────────
    log(f"\n── CIO Synthesis ──")
    try:
        synthesis = call_cio_synthesis(client, reports)
        write_to_analysis(conn, "mstr-cio", "daily_synthesis", {"text": synthesis})

        # Extract and log stage call from synthesis
        stage_match = re.search(r'Stage\s+([1-4][a-zA-Z_]*)', synthesis or "")
        conf_match = re.search(r'confidence[:\s]+(\d+)', synthesis or "", re.IGNORECASE)
        if stage_match:
            stage = stage_match.group(0)
            confidence = float(conf_match.group(1)) if conf_match else 70.0
            log_signal_score(conn, stage, confidence)

    except Exception as e:
        log(f"❌ CIO synthesis failed: {e}")
        import traceback
        traceback.print_exc()
        write_to_analysis(conn, "mstr-cio", "daily_synthesis", {"_error": str(e)})

    # ── Summary ───────────────────────────────────────────────────────────────
    elapsed_total = int((time.time() - start_total))
    log(f"\n{'='*60}")
    log(f"Analysis Cycle Complete in {elapsed_total}s ({elapsed_total//60}m {elapsed_total%60}s)")
    for agent_id in list(agent_payloads.keys()) + ["mstr-cio"]:
        status = "❌" if agent_id in failed_agents or agent_id in validation_errors else "✅"
        log(f"  {status} {agent_id}")
    if validation_errors:
        log(f"\nValidation warnings: {validation_errors}")
    log(f"{'='*60}")

    conn.close()

    # Write timing to cron_state
    try:
        conn2 = db_connect()
        conn2.execute(
            """INSERT OR REPLACE INTO cron_state (script_name, last_success, last_attempt, consecutive_failures)
               VALUES ('daily_analysis_cycle', datetime('now'), datetime('now'), 0)"""
        )
        conn2.commit()
        conn2.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()
