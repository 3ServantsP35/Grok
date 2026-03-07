#!/usr/bin/env python3
"""
ppr_generator.py — Personalized Portfolio Report generator
Runs after morning_brief.py (14:30 UTC / 10:30 AM ET on trading days).

Reads CIO daily synthesis from the analysis table and generates three
personalized Discord reports:
  - Greg  (#mstr-greg):  Action-oriented, bottom-line-first, no dollar amounts
  - Gavin (#mstr-gavin): Deep technical, paper portfolio, full indicator depth
  - Gary  (#mstr-gary):  Educational, plain language, rotating learning moments

Cost model: Pure Python formatting from existing synthesis — ZERO additional
Claude calls. The delegation cycle already did the analysis.
"""

import json
import os
import re
import sqlite3
import ssl
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
DB_PATH          = os.environ.get("DB_PATH", "/mnt/mstr-data/mstr.db")
CONFIG_ENV_PATH  = os.environ.get("CONFIG_ENV_PATH", "/mnt/mstr-config/.env")
WORKSPACE_ROOT   = Path(os.environ.get("WORKSPACE_ROOT", "/home/openclaw/.openclaw/workspace-mstr-cio"))
KNOWLEDGE_DIR    = WORKSPACE_ROOT / "mstr-knowledge"
LOG_PATH         = "/mnt/mstr-logs/ppr.log"

# ── Discord embed color constants ───────────────────────────────────────────
COLOR_STAGE_1 = 0x27AE60  # green
COLOR_STAGE_2 = 0x2ECC71  # light green
COLOR_STAGE_3 = 0xF39C12  # orange
COLOR_STAGE_4 = 0xC0392B  # red
COLOR_DEFAULT = 0x3498DB  # blue

STAGE_COLOR_MAP = {
    "S1": COLOR_STAGE_1, "S1_TO_S2": COLOR_STAGE_1,
    "S2": COLOR_STAGE_2, "S2_CONT": COLOR_STAGE_2, "S2_CONS": COLOR_STAGE_2,
    "S2_TO_S3": COLOR_STAGE_3,
    "S3": COLOR_STAGE_3,
    "S4": COLOR_STAGE_4, "S4_CONS": COLOR_STAGE_4, "S4_TO_S1": COLOR_STAGE_4,
}

# ── Logging ─────────────────────────────────────────────────────────────────
def log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ── Environment ──────────────────────────────────────────────────────────────
def load_env() -> dict:
    env = {}
    for p in [CONFIG_ENV_PATH, "/mnt/mstr-data/.env_tokens"]:
        try:
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
        except FileNotFoundError:
            pass
    return env


# ── Database ──────────────────────────────────────────────────────────────────
def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def load_latest_synthesis(conn: sqlite3.Connection) -> dict:
    """Load the most recent CIO daily synthesis from the analysis table."""
    row = conn.execute(
        """SELECT analysis, timestamp FROM analysis
           WHERE agent_id = 'mstr-cio' AND analysis_type = 'daily_synthesis'
           ORDER BY timestamp DESC LIMIT 1"""
    ).fetchone()
    if not row:
        return {}
    try:
        return json.loads(row["analysis"])
    except (json.JSONDecodeError, TypeError):
        return {"raw_text": row["analysis"], "timestamp": row["timestamp"]}


def load_latest_sri(conn: sqlite3.Connection) -> dict:
    """Pull current stage + LOI data for direct DB reference."""
    row = conn.execute(
        """SELECT confirmed_stage, momentum_score, transition_prob_5d,
                  transition_prob_10d, transition_prob_20d
           FROM sri_signals ORDER BY timestamp DESC LIMIT 1"""
    ).fetchone()
    return dict(row) if row else {}


def load_mnav(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        "SELECT mnav_ratio, premium_pct, mstr_price, btc_price FROM mnav ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    return dict(row) if row else {}


def load_pmcc_gate(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        "SELECT gate_state, loi, ct_tier, max_delta FROM pmcc_gate_state WHERE asset='MSTR' ORDER BY updated_at DESC LIMIT 1"
    ).fetchone()
    return dict(row) if row else {}


def load_portfolio_state(filename: str) -> str:
    path = KNOWLEDGE_DIR / filename
    try:
        return path.read_text()
    except FileNotFoundError:
        return f"[{filename} not found]"


def load_gary_topic_queue() -> str:
    """Extract next topic from gary-profile.md topic queue."""
    profile = load_portfolio_state("gary-profile.md")
    # Find first uncovered topic (first entry with "—" date)
    in_queue = False
    for line in profile.split("\n"):
        if "Topics to Cover Next" in line:
            in_queue = True
        if in_queue and line.strip().startswith("1."):
            return line.strip()[2:].strip()
    return "The 4-stage SRI cycle"


# ── Synthesis extraction helpers ───────────────────────────────────────────
def extract_field(synthesis: dict, *keys, default="N/A"):
    """Safely traverse nested synthesis dict."""
    obj = synthesis
    for k in keys:
        if not isinstance(obj, dict):
            return default
        obj = obj.get(k, default)
    return obj if obj not in (None, "", {}, []) else default


def get_stage_color(stage_str: str) -> int:
    if not stage_str:
        return COLOR_DEFAULT
    for k, v in STAGE_COLOR_MAP.items():
        if k in str(stage_str).upper():
            return v
    return COLOR_DEFAULT


def fmt_pct(val) -> str:
    try:
        return f"{float(val):.1f}%"
    except (TypeError, ValueError):
        return str(val)


def fmt_price(val) -> str:
    try:
        return f"${float(val):,.2f}"
    except (TypeError, ValueError):
        return str(val)


# ── PPR Generators ─────────────────────────────────────────────────────────

def generate_greg_ppr(synthesis: dict, sri: dict, mnav: dict, gate: dict) -> str:
    """
    Greg's report: bottom-line first, action-oriented.
    No dollar amounts — percentages and allocation categories only.
    """
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    stage      = extract_field(synthesis, "stage_call", default=sri.get("confirmed_stage", "Unknown"))
    confidence = extract_field(synthesis, "stage_confidence", default="—")
    action     = extract_field(synthesis, "recommended_action", default="Hold current posture. No changes today.")
    thesis     = extract_field(synthesis, "primary_thesis", default="")

    mstr_price = fmt_price(mnav.get("mstr_price"))
    btc_price  = fmt_price(mnav.get("btc_price"))
    mnav_ratio = f"{float(mnav.get('mnav_ratio', 0)):.2f}x" if mnav.get("mnav_ratio") else "N/A"

    loi        = gate.get("loi", "N/A")
    gate_state = gate.get("gate_state", "N/A")
    ct_tier    = gate.get("ct_tier", "N/A")

    trade_ideas = extract_field(synthesis, "trade_ideas", default=[])
    if isinstance(trade_ideas, str):
        trade_ideas_text = trade_ideas[:800]
    elif isinstance(trade_ideas, list) and trade_ideas:
        lines = []
        for i, idea in enumerate(trade_ideas[:3], 1):
            if isinstance(idea, dict):
                s = idea.get("strategy", idea.get("description", str(idea)))
                lines.append(f"  {i}. {s}")
            else:
                lines.append(f"  {i}. {idea}")
        trade_ideas_text = "\n".join(lines)
    else:
        trade_ideas_text = "No actionable trades today."

    kill = extract_field(synthesis, "kill_condition", default="")
    howell = extract_field(synthesis, "howell_phase", default="Unknown")
    pbear  = extract_field(synthesis, "pbear_status", default="Normal")

    report = f"""**📊 {today} — Personal Brief**

**STAGE & ACTION**
Stage: **{stage}** | Confidence: {confidence}
{f"> {thesis}" if thesis and thesis != "N/A" else ""}
**Today:** {action}

**PORTFOLIO SNAPSHOT**
Deployment: ~7.8% (target 50/25/25 — AB3/AB1/AB4)
AB2 Gate: {gate_state} | LOI: {loi} | CT Tier: {ct_tier}
AB4 Cash Floor: ✅ Above 10% minimum

**MARKET LEVELS**
MSTR: {mstr_price} | BTC: {btc_price}
mNAV: {mnav_ratio} ({'sell calls' if mnav.get('mnav_ratio', 0) and float(mnav.get('mnav_ratio', 0)) >= 3.0 else 'neutral' if float(mnav.get('mnav_ratio', 0)) > 1.2 else 'sell puts'})

**TRADE IDEAS**
{trade_ideas_text}
{f"> Kill: {kill}" if kill and kill != "N/A" else ""}

**RISK MONITOR**
Howell Phase: {howell} | P-BEAR: {pbear}"""

    return report.strip()


def generate_gavin_ppr(synthesis: dict, sri: dict, mnav: dict, gate: dict,
                       portfolio_state: str) -> str:
    """
    Gavin's report: deep technical, full indicator depth, paper portfolio context.
    """
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    stage      = extract_field(synthesis, "stage_call", default=sri.get("confirmed_stage", "Unknown"))
    confidence = extract_field(synthesis, "stage_confidence", default="—")
    thesis     = extract_field(synthesis, "primary_thesis", default="")

    # Pull TF readings from synthesis if present
    tf_readings    = extract_field(synthesis, "tf_readings", default={})
    transition_w   = extract_field(synthesis, "transition_watch", default="")
    agent_tensions = extract_field(synthesis, "agent_tensions", default="None flagged")

    mnav_ratio = f"{float(mnav.get('mnav_ratio', 0)):.3f}x" if mnav.get("mnav_ratio") else "N/A"
    premium    = fmt_pct(mnav.get("premium_pct"))
    loi        = gate.get("loi", "N/A")
    gate_state = gate.get("gate_state", "N/A")
    ct_tier    = gate.get("ct_tier", "N/A")
    max_delta  = gate.get("max_delta", "N/A")

    macro_regime = extract_field(synthesis, "macro_regime", default="Unknown")
    gli_score    = extract_field(synthesis, "gli_score", default="N/A")
    howell       = extract_field(synthesis, "howell_phase", default="Unknown")
    liq_regime   = extract_field(synthesis, "liquidity_regime", default="Unknown")

    iv_env   = extract_field(synthesis, "iv_environment", default="Unknown")
    flow_sum = extract_field(synthesis, "flow_summary", default="")

    trade_ideas = extract_field(synthesis, "trade_ideas", default=[])
    if isinstance(trade_ideas, list) and trade_ideas:
        idea_lines = []
        for i, idea in enumerate(trade_ideas[:3], 1):
            if isinstance(idea, dict):
                idea_lines.append(f"**{i}.** {json.dumps(idea, default=str)[:300]}")
            else:
                idea_lines.append(f"**{i}.** {str(idea)[:300]}")
        trade_text = "\n".join(idea_lines)
    else:
        trade_text = str(trade_ideas)[:500] if trade_ideas else "None."

    conflicts = extract_field(synthesis, "analyst_conflicts", default="None.")

    report = f"""**📊 {today} — Technical Brief**

**STAGE ASSESSMENT**
Stage: **{stage}** (confidence: {confidence})
{f"> {thesis}" if thesis and thesis != "N/A" else ""}
Transition Watch: {transition_w if transition_w and transition_w != "N/A" else "None active"}

**LAYER 0–1 REGIME**
Macro: {macro_regime} | GLI Score: {gli_score}
Howell: {howell} | Liquidity: {liq_regime}

**INDICATOR DASHBOARD**
LOI: {loi} | Gate: {gate_state} | CT: {ct_tier} | Max Δ: {max_delta}
mNAV: {mnav_ratio} (premium {premium})
IV Env: {iv_env}
{f"Flow: {flow_sum[:200]}" if flow_sum and flow_sum != "N/A" else ""}

**TF READINGS**
{json.dumps(tf_readings, indent=2, default=str)[:500] if tf_readings and tf_readings != "N/A" else "See morning brief for full TF detail."}

**TRADE IDEAS (paper)**
{trade_text}

**ANALYST CROSS-CHECK**
Conflicts: {conflicts if isinstance(conflicts, str) else json.dumps(conflicts, default=str)[:200]}
Agent tensions: {agent_tensions}

**PAPER PORTFOLIO**
All cash. No open positions. Next entry: Stage 1 confirmation or AB1 CT2+."""

    return report.strip()


def generate_gary_ppr(synthesis: dict, sri: dict, mnav: dict) -> str:
    """
    Gary's report: educational, plain language, one rotating learning moment.
    """
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    stage     = extract_field(synthesis, "stage_call", default=sri.get("confirmed_stage", "Stage 4"))
    mstr_price = fmt_price(mnav.get("mstr_price"))
    btc_price  = fmt_price(mnav.get("btc_price"))
    mnav_ratio = float(mnav.get("mnav_ratio", 1.5)) if mnav.get("mnav_ratio") else 1.5

    # Plain-language stage descriptions
    stage_plain = {
        "S1":       "**Accumulation** — the bottom of the cycle. Smart money is quietly buying. This is historically the best time to build positions, but it requires patience.",
        "S1_TO_S2": "**Transition: Accumulation → Recovery** — early signs of a bottom. Indicators are starting to turn positive. Still cautious but watching closely.",
        "S2":       "**Recovery** — the cycle is turning up. Momentum is building. This is where most of the framework's entries happen.",
        "S2_CONT":  "**Recovery (Continuation)** — the uptrend is in force. Momentum is strong. Holding existing positions; watching for signs of the next peak.",
        "S2_CONS":  "**Recovery (Consolidation)** — a pause within the uptrend. Normal healthy rest before the next leg up.",
        "S2_TO_S3": "**Transition: Recovery → Distribution** — early warning that the cycle may be peaking. Time to start trimming.",
        "S3":       "**Distribution** — the top of the cycle. Prices look high, sentiment is euphoric. The framework is reducing exposure here.",
        "S4":       "**Correction** — the cycle is coming down. Capital preservation mode. Think of this as winter — we're waiting for spring.",
        "S4_CONS":  "**Correction (Consolidation)** — a pause within the downtrend. Could be a base forming, or just a rest before lower prices.",
        "S4_TO_S1": "**Transition: Correction → Accumulation** — signs of a potential bottom. Not confirmed yet, but worth watching closely.",
    }
    stage_key = str(stage).upper()
    stage_description = stage_plain.get(stage_key, f"**{stage}** — the framework is monitoring current conditions carefully.")

    # Watch levels from synthesis
    support    = extract_field(synthesis, "key_support", default="check morning brief")
    resistance = extract_field(synthesis, "key_resistance", default="check morning brief")

    # One-line mNAV explanation
    if mnav_ratio >= 3.0:
        mnav_plain = f"MSTR is trading at {mnav_ratio:.2f}× its Bitcoin value — relatively expensive historically."
    elif mnav_ratio <= 1.2:
        mnav_plain = f"MSTR is trading at {mnav_ratio:.2f}× its Bitcoin value — relatively cheap historically."
    else:
        mnav_plain = f"MSTR is trading at {mnav_ratio:.2f}× its Bitcoin value — in a normal range."

    # Rotating learning moment — next topic in queue
    next_topic = load_gary_topic_queue()

    # Learning content — simple templates
    learning_map = {
        "the 4-stage cycle":            "The SRI framework divides the market into four seasons: Accumulation (bottom), Recovery (uptrend), Distribution (top), and Correction (downtrend). Right now we're in the {stage} phase. Each phase calls for a different action — buy at the bottom, hold through recovery, sell near the top, protect capital during correction.",
        "what is mstr":                 "MicroStrategy (MSTR) is a company that holds Bitcoin as its primary asset. When Bitcoin rises 10%, MSTR often rises 15-20% — it's an amplified Bitcoin bet. The 'mNAV ratio' tells us how much of a premium investors are paying for that amplification.",
        "what is mnav":                 "mNAV stands for 'Market-to-Net Asset Value.' If MSTR's Bitcoin is worth $50B but MSTR's market cap is $100B, mNAV = 2.0. You're paying 2× for Bitcoin exposure. At 3× or higher, it's historically expensive. At 1.2× or below, historically cheap.",
        "what is a leap option":        "A LEAP is a long-dated options contract — typically 1-2 years until expiration. Instead of buying 100 shares of MSTR at $133 each ($13,300), you might pay $3,000 for the right to buy at $150 in 2 years. If MSTR hits $200, your $3,000 grows to ~$5,000+ while tying up far less capital.",
    }

    topic_lower = next_topic.lower()
    learning_content = None
    for key, val in learning_map.items():
        if key in topic_lower:
            learning_content = val.format(stage=stage)
            break
    if not learning_content:
        learning_content = f"Today's topic: **{next_topic}**\nWatch for a deeper explanation in tomorrow's brief as the CIO builds out the learning curriculum."

    report = f"""**📚 {today} — Daily Learning Brief**

**TODAY IN ONE PARAGRAPH**
We're currently in {stage_description}

**KEY NUMBERS**
MSTR: {mstr_price} | BTC: {btc_price}
{mnav_plain}

**WHAT TO WATCH TODAY**
• Support: {support} — if MSTR closes above this, the trend is intact
• Resistance: {resistance} — a close above here would be a bullish signal

**📖 LEARNING MOMENT: {next_topic.title()}**
{learning_content}"""

    return report.strip()


# ── Discord Delivery ─────────────────────────────────────────────────────────

def split_for_discord(text: str, limit: int = 4000) -> list:
    """Split text into chunks that fit Discord embed description limit."""
    if len(text) <= limit:
        return [text]
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > limit:
            if current:
                chunks.append(current.strip())
            current = line + "\n"
        else:
            current += line + "\n"
    if current:
        chunks.append(current.strip())
    return chunks


def send_ppr(webhook_url: str, user_name: str, ppr_content: str,
             stage: str, today: str) -> int:
    """Send PPR to a Discord channel via webhook embed."""
    if not webhook_url:
        log(f"  ⚠️  No webhook for {user_name} — skipping")
        return 0

    color = get_stage_color(stage)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    chunks = split_for_discord(ppr_content, limit=4000)
    success = 0

    for i, chunk in enumerate(chunks):
        title = f"📊 {user_name} — Personal Brief | {today}" if i == 0 else f"📊 {user_name} — (continued)"
        payload = json.dumps({
            "embeds": [{
                "title": title,
                "description": chunk,
                "color": color,
                "footer": {"text": f"MSTR Engine PPR | Automated | Part {i+1}/{len(chunks)}"}
            }]
        }).encode()
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                log(f"  ✅ {user_name} part {i+1}: HTTP {r.status}")
                success += 1
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:120]
            log(f"  ❌ {user_name} part {i+1}: HTTP {e.code} — {body}")
        except Exception as ex:
            log(f"  ❌ {user_name} part {i+1}: {ex}")

    return success


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    log("=" * 60)
    log("PPR Generator — starting")
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    env  = load_env()
    conn = db_connect()

    # Load data
    log("Loading CIO synthesis from analysis table...")
    synthesis = load_latest_synthesis(conn)
    if not synthesis:
        log("ERROR: No CIO synthesis found in analysis table. Has daily_analysis_cycle.py run today?")
        sys.exit(1)

    synthesis_ts = synthesis.get("timestamp", "unknown")
    log(f"Synthesis loaded (timestamp: {synthesis_ts})")

    sri   = load_latest_sri(conn)
    mnav  = load_mnav(conn)
    gate  = load_pmcc_gate(conn)
    stage = synthesis.get("stage_call", sri.get("confirmed_stage", "Unknown"))

    conn.close()

    portfolio_gavin = load_portfolio_state("gavin-portfolio-state.md")

    # Generate reports
    log("Generating Greg PPR...")
    greg_ppr = generate_greg_ppr(synthesis, sri, mnav, gate)

    log("Generating Gavin PPR...")
    gavin_ppr = generate_gavin_ppr(synthesis, sri, mnav, gate, portfolio_gavin)

    log("Generating Gary PPR...")
    gary_ppr = generate_gary_ppr(synthesis, sri, mnav)

    # Deliver
    log("Sending PPRs via webhooks...")
    results = {}

    greg_webhook  = env.get("DISCORD_WEBHOOK_GREG", "")
    gavin_webhook = env.get("DISCORD_WEBHOOK_GAVIN", "")
    gary_webhook  = env.get("DISCORD_WEBHOOK_GARY", "")

    results["Greg"]  = send_ppr(greg_webhook,  "Greg",  greg_ppr,  stage, today)
    results["Gavin"] = send_ppr(gavin_webhook, "Gavin", gavin_ppr, stage, today)
    results["Gary"]  = send_ppr(gary_webhook,  "Gary",  gary_ppr,  stage, today)

    # Summary
    log("-" * 40)
    for user, sent in results.items():
        icon = "✅" if sent > 0 else "❌"
        log(f"  {icon} {user}: {sent} embed(s) sent")

    # Fail loudly if all three failed (likely missing webhooks, not a bug)
    if all(v == 0 for v in results.values()):
        log("WARNING: All PPRs failed to deliver. Verify webhook URLs in .env.")
        sys.exit(1)

    log("PPR Generator — complete")


if __name__ == "__main__":
    main()
