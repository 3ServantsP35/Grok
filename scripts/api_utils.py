#!/usr/bin/env python3
"""
api_utils.py — Shared Claude API wrapper with cost tracking.
All scripts that call Claude should use call_claude() from this module.

Usage:
    from api_utils import call_claude, get_anthropic_client, query_api_costs

Cost tracking: Every call logged to debug_log with token counts + duration.
Cost rates ($/M tokens):
    claude-opus-4-6:      $15.00 input / $75.00 output
    claude-sonnet-4-6:    $3.00 input  / $15.00 output
    claude-haiku-4-5:     $0.80 input  / $4.00 output
"""

import os
import sqlite3
import time
from datetime import datetime, timezone, timedelta
from typing import Optional

DB_PATH = "/mnt/mstr-data/mstr.db"

# Cost rates per million tokens
COST_RATES = {
    # Opus
    "claude-opus-4-6":              {"input": 15.00, "output": 75.00},
    "claude-opus-4-6-20250929":     {"input": 15.00, "output": 75.00},
    # Sonnet
    "claude-sonnet-4-6":            {"input": 3.00,  "output": 15.00},
    "claude-sonnet-4-6-20250929":   {"input": 3.00,  "output": 15.00},
    # Haiku
    "claude-haiku-4-5":             {"input": 0.80,  "output": 4.00},
    "claude-haiku-4-5-20251001":    {"input": 0.80,  "output": 4.00},
}

DEFAULT_RATE = {"input": 3.00, "output": 15.00}  # Sonnet as fallback


def get_anthropic_client():
    """Return a configured Anthropic client using env or .env file."""
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Try loading from .env files
        for env_path in ["/mnt/mstr-config/.env", "/home/openclaw/mstr-engine/config/.env"]:
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ANTHROPIC_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            os.environ["ANTHROPIC_API_KEY"] = api_key
                            break
                if api_key:
                    break

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment or .env files")

    return anthropic.Anthropic(api_key=api_key)


def call_claude(
    client,
    model: str,
    system: str,
    messages: list,
    max_tokens: int = 4096,
    script_name: str = "unknown",
    thinking: Optional[dict] = None,
    db_path: str = DB_PATH,
) -> object:
    """
    Call Claude API and log token usage + cost to debug_log.

    Args:
        client: anthropic.Anthropic instance
        model: Model ID (e.g., 'claude-sonnet-4-6-20250929')
        system: System prompt string
        messages: List of message dicts
        max_tokens: Max output tokens
        script_name: Name of calling script (for cost tracking)
        thinking: Optional thinking config dict, e.g. {"type": "enabled", "budget_tokens": 5000}
        db_path: SQLite DB path

    Returns:
        anthropic.types.Message response object
    """
    start = time.time()

    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": messages,
    }
    if thinking:
        kwargs["thinking"] = thinking

    response = client.messages.create(**kwargs)
    duration_ms = int((time.time() - start) * 1000)

    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    # Calculate cost
    rates = COST_RATES.get(model, DEFAULT_RATE)
    cost_usd = (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000

    # Log to DB
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA busy_timeout=3000")
        conn.execute(
            """INSERT INTO debug_log
               (timestamp, script_name, level, message,
                prompt_tokens, completion_tokens, model, duration_ms)
               VALUES (?, ?, 'API_CALL', ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                script_name,
                f"in={input_tokens} out={output_tokens} cost=${cost_usd:.4f}",
                input_tokens,
                output_tokens,
                model,
                duration_ms,
            ),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[api_utils] Warning: could not log to debug_log: {e}")

    return response


def get_response_text(response) -> str:
    """Extract text content from a Claude response, skipping thinking blocks."""
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "\n".join(parts).strip()


def compute_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Compute USD cost for a given token usage."""
    rates = COST_RATES.get(model, DEFAULT_RATE)
    return (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000


def query_api_costs(days: int = 1, db_path: str = DB_PATH) -> dict:
    """
    Query debug_log for API cost summary.

    Returns dict with:
        total_cost_usd: float
        total_input_tokens: int
        total_total_tokens: int (input + output)
        calls: int
        by_script: list of {script, calls, input, output, cost}
        by_model: list of {model, calls, input, output, cost}
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        rows = conn.execute(
            """SELECT script_name, model,
                      COALESCE(prompt_tokens, 0) as input_tok,
                      COALESCE(completion_tokens, 0) as output_tok
               FROM debug_log
               WHERE level = 'API_CALL'
                 AND timestamp >= ?
                 AND prompt_tokens IS NOT NULL""",
            (since,),
        ).fetchall()
        conn.close()

        total_cost = 0.0
        total_input = 0
        total_output = 0
        by_script: dict = {}
        by_model: dict = {}

        for row in rows:
            in_tok = row["input_tok"]
            out_tok = row["output_tok"]
            model = row["model"] or "unknown"
            script = row["script_name"] or "unknown"
            cost = compute_cost(in_tok, out_tok, model)

            total_cost += cost
            total_input += in_tok
            total_output += out_tok

            s = by_script.setdefault(script, {"calls": 0, "input": 0, "output": 0, "cost": 0.0})
            s["calls"] += 1
            s["input"] += in_tok
            s["output"] += out_tok
            s["cost"] += cost

            m = by_model.setdefault(model, {"calls": 0, "input": 0, "output": 0, "cost": 0.0})
            m["calls"] += 1
            m["input"] += in_tok
            m["output"] += out_tok
            m["cost"] += cost

        by_script_list = sorted(
            [{"script": k, **v} for k, v in by_script.items()],
            key=lambda x: x["cost"],
            reverse=True,
        )
        by_model_list = sorted(
            [{"model": k, **v} for k, v in by_model.items()],
            key=lambda x: x["cost"],
            reverse=True,
        )

        return {
            "total_cost_usd": total_cost,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_input + total_output,
            "calls": len(rows),
            "days": days,
            "by_script": by_script_list,
            "by_model": by_model_list,
        }

    except Exception as e:
        return {"error": str(e), "total_cost_usd": 0.0, "calls": 0}


def format_cost_section(yesterday_data: dict, week_data: dict) -> str:
    """Format API cost section for morning brief."""
    lines = ["**💰 API Cost Tracker**"]

    if "error" in yesterday_data:
        lines.append(f"  ⚠️ Error: {yesterday_data['error']}")
        return "\n".join(lines)

    y_cost = yesterday_data.get("total_cost_usd", 0)
    w_cost = week_data.get("total_cost_usd", 0)
    w_avg = w_cost / 7 if w_cost else 0
    y_calls = yesterday_data.get("calls", 0)

    lines.append(f"  Yesterday: **${y_cost:.2f}** ({y_calls} API calls)")
    lines.append(f"  7d average: **${w_avg:.2f}/day** (total ${w_cost:.2f})")

    if y_cost > 30:
        lines.append(f"  ⚠️ **COST ALERT: ${y_cost:.2f} exceeds $30/day threshold**")

    top_scripts = yesterday_data.get("by_script", [])[:5]
    if top_scripts:
        lines.append("  **By script (yesterday):**")
        for s in top_scripts:
            lines.append(f"    {s['script']:<35} ${s['cost']:.3f}  ({s['calls']} calls)")

    top_models = yesterday_data.get("by_model", [])[:4]
    if top_models:
        lines.append("  **By model (yesterday):**")
        for m in top_models:
            lines.append(
                f"    {m['model']:<35} ${m['cost']:.3f}  "
                f"(in={m['input']:,} out={m['output']:,})"
            )

    return "\n".join(lines)


if __name__ == "__main__":
    # Quick test / cost report CLI
    print("=== API Cost Report ===")
    for days in [1, 7]:
        data = query_api_costs(days=days)
        if "error" in data:
            print(f"  {days}d: Error — {data['error']}")
        else:
            print(f"  {days}d: ${data['total_cost_usd']:.4f} | {data['calls']} calls | "
                  f"{data['total_tokens']:,} tokens")
            for s in data["by_script"][:5]:
                print(f"    {s['script']:<35} ${s['cost']:.4f}")
