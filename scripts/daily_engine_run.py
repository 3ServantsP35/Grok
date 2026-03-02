#!/usr/bin/env python3
"""
Daily Engine Run — P12 Phase 3
================================
Pulls 16 canonical CSVs from GitHub, runs the 4-layer SRI engine,
regenerates the dashboard, and posts a regime + signal summary to Discord.

Schedule (crontab suggestion):
  30 14 * * 1-5  /usr/bin/python3 /mnt/mstr-scripts/daily_engine_run.py >> /mnt/mstr-logs/daily_engine.log 2>&1

That fires at 10:30 AM ET (14:30 UTC) — after Gavin's daily morning push.
A second run at 21:00 UTC (5 PM ET) catches any late updates.

Author: CIO Engine  |  Version: 1.0  |  2026-03-05
"""

import os, sys, ssl, json, urllib.request, urllib.error, urllib.parse
import subprocess, time, traceback
from datetime import datetime, timezone
from pathlib import Path

# Load .env manually (no dotenv dependency)
_ENV_PATH = Path("/mnt/mstr-config/.env")
if _ENV_PATH.exists():
    for _line in _ENV_PATH.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

# ── Config ──────────────────────────────────────────────────────
GH_TOKEN   = os.environ.get("GITHUB_TOKEN", "")  # Set in /mnt/mstr-config/.env
REPO       = "3ServantsP35/Grok"
DATA_DIR   = Path("/mnt/mstr-data")
LOG_TAG    = "[DAILY-RUN]"

WEBHOOK_ALERTS = os.environ.get("DISCORD_WEBHOOK_ALERTS", "")

# ── The 16 canonical CSVs (filename on GitHub → local save name) ─
CANONICAL_CSVS = {
    # Trading assets
    "BATS_MSTR, 240_7f820.csv":                    "BATS_MSTR, 240_7f820.csv",
    "BATS_IBIT, 240_ccca2.csv":                    "BATS_IBIT, 240_ccca2.csv",
    "BATS_SPY, 240_981cd.csv":                     "BATS_SPY, 240_981cd.csv",
    "BATS_QQQ, 240_21e37.csv":                     "BATS_QQQ, 240_21e37.csv",
    "BATS_GLD, 240_bfd71.csv":                     "BATS_GLD, 240_bfd71.csv",
    "BATS_IWM, 240_cfcaf.csv":                     "BATS_IWM, 240_cfcaf.csv",
    "BATS_TSLA, 240_bdcd2.csv":                    "BATS_TSLA, 240_bdcd2.csv",
    "BATS_PURR, 240_1fcfd.csv":                    "BATS_PURR, 240_1fcfd.csv",
    # Regime inputs
    "BITSTAMP_BTCUSD, 240_fe30c.csv":              "BITSTAMP_BTCUSD, 240_fe30c.csv",
    "BATS_MSTR_BATS_IBIT, 240_0ae35.csv":          "BATS_MSTR_BATS_IBIT, 240_0ae35.csv",
    "CRYPTOCAP_STABLE.C.D, 240_7a290.csv":         "CRYPTOCAP_STABLE.C.D, 240_7a290.csv",
    "BATS_STRC, 240_9969c.csv":                    "BATS_STRC, 240_9969c.csv",
    "BATS_TLT, 240_c5a3d.csv":                     "BATS_TLT, 240_c5a3d.csv",
    "TVC_DXY, 240_b3956.csv":                      "TVC_DXY, 240_b3956.csv",
    "BATS_HYG, 240_ab482.csv":                     "BATS_HYG, 240_ab482.csv",
    "TVC_VIX, 240_7b6d0.csv":                      "TVC_VIX, 240_7b6d0.csv",
}

# ── SSL context ──────────────────────────────────────────────────
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "Authorization": f"token {GH_TOKEN}",
    "User-Agent":    "mstr-cio/1.0",
}


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"{LOG_TAG} {ts}  {msg}", flush=True)


def gh_get_meta(filename: str) -> dict:
    """Fetch file metadata (sha, download_url, size) from GitHub."""
    encoded = urllib.parse.quote(filename, safe="")
    url = f"https://api.github.com/repos/{REPO}/contents/{encoded}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        return json.loads(r.read())


def gh_download(download_url: str, dest: Path) -> bool:
    """Download raw file from raw.githubusercontent.com."""
    req = urllib.request.Request(download_url, headers={"User-Agent": "mstr-cio/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            data = r.read()
        dest.write_bytes(data)
        return True
    except Exception as e:
        log(f"  ERROR downloading {dest.name}: {e}")
        return False


def needs_update(filename: str, local_path: Path) -> tuple[bool, str]:
    """Check if remote file differs from local by comparing sha."""
    if not local_path.exists():
        return True, "missing"
    try:
        meta = gh_get_meta(filename)
        remote_sha = meta.get("sha", "")
        # Compute local git blob sha (git uses length-prefixed content)
        local_data = local_path.read_bytes()
        import hashlib
        header = f"blob {len(local_data)}\0".encode()
        local_sha = hashlib.sha1(header + local_data).hexdigest()
        if local_sha != remote_sha:
            return True, meta.get("download_url", "")
        return False, ""
    except Exception as e:
        log(f"  sha check failed for {filename}: {e}")
        return True, ""  # Pull anyway on error


def pull_csvs() -> tuple[int, int]:
    """Pull all 16 CSVs. Returns (updated, skipped)."""
    import urllib.parse
    updated = 0
    skipped = 0
    for gh_name, local_name in CANONICAL_CSVS.items():
        local_path = DATA_DIR / local_name
        needs, download_url = needs_update(gh_name, local_path)
        if not needs:
            log(f"  ✓ {local_name[:40]:40s} (unchanged)")
            skipped += 1
            continue
        if not download_url:
            # Fetch meta to get download_url
            try:
                meta = gh_get_meta(gh_name)
                download_url = meta.get("download_url", "")
            except Exception as e:
                log(f"  ✗ {local_name[:40]:40s} (meta fetch failed: {e})")
                continue
        log(f"  ↓ {local_name[:40]:40s} pulling...")
        ok = gh_download(download_url, local_path)
        if ok:
            size_kb = local_path.stat().st_size // 1024
            log(f"    saved {size_kb:,} KB")
            updated += 1
        time.sleep(0.3)  # Gentle on GitHub rate limits
    return updated, skipped


def run_engine() -> dict | None:
    """Run the SRI engine and return full result dict."""
    sys.path.insert(0, "/mnt/mstr-scripts")
    os.environ.setdefault("FRED_API_KEY", "8ee8d7967be4aab0fdc7565e85676260")
    try:
        from sri_engine import SRIEngineV2
        engine = SRIEngineV2()
        result = engine.run_all(verbose=False)
        log("  Engine run complete")
        return result
    except Exception as e:
        log(f"  ENGINE ERROR: {e}")
        traceback.print_exc()
        return None


def regen_dashboard() -> bool:
    """Regenerate the HTML dashboard."""
    try:
        result = subprocess.run(
            [sys.executable, "/mnt/mstr-scripts/generate_dashboard.py",
             "--output", str(DATA_DIR / "dashboard.html")],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            log("  Dashboard regenerated")
            return True
        log(f"  Dashboard error: {result.stderr[:200]}")
        return False
    except Exception as e:
        log(f"  Dashboard exception: {e}")
        return False


# ── Discord formatting ────────────────────────────────────────────

def regime_emoji(score: int) -> str:
    if score >= 3:  return "🟢"
    if score >= 1:  return "🟡"
    if score >= -1: return "⚪"
    return "🔴"

def ctx_emoji(ctx_str: str) -> str:
    return {"TAILWIND": "🟢", "MIXED": "🟡", "HEADWIND": "🔴"}.get(ctx_str, "⚪")

def loi_emoji(loi: float, mode: str = "Momentum") -> str:
    thresh = -60 if mode == "Momentum" else -40
    if loi < -80: return "🔴🔴"
    if loi < thresh: return "🔴"
    if loi > 60: return "🟢"
    if loi > 40: return "🟡"
    return "⚪"

def build_discord_payload(result: dict) -> dict:
    """Build rich Discord embed from engine result."""
    reg   = result["regime"]
    state = result["current_state"]
    ab1   = result["ab1_signals"]
    ab2   = result["ab2_signals"]

    eff   = reg.effective_score
    ve    = reg.vehicle
    vix   = reg.vix_level
    ts    = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    re_em = regime_emoji(eff)

    # GLI line
    gli = reg.gli_state
    gli_line = ""
    if gli and gli.error is None:
        gz = gli.gli_zscore
        gc = gli.gegi.composite
        gli_line = f"**Layer 0 — GLI:** Z={gz:+.3f} | GEGI={gc:+.3f} | adj={gli.score_adjustment:+d}\n"

    # Regime line
    adj_label = reg.adjusted_regime_label or reg.regime_label
    regime_line = f"**Layer 1 — Regime:** {re_em} **{eff:+d}/7** {adj_label} | Vehicle: **{ve}** | VIX={vix:.1f}\n"

    # PMCC gate states (from ab2 results)
    pmcc_gates = {}
    for asset, ab2 in ab2.items():
        if isinstance(ab2, dict) and "current" in ab2:
            pmcc_gates[asset] = ab2["current"].get("gate_state", "")

    def gate_emoji(gs: str) -> str:
        return {"NO_CALLS": "🔴", "OTM_INCOME": "🟢", "DELTA_MGMT": "🟠",
                "PAUSED_AB1": "⏸️", "NO_POSITION": "⬜"}.get(gs, "❓")

    # Asset table
    asset_lines = []
    for asset, s in state.items():
        ctx  = s["context"]
        loi  = s["loi"]
        mode = s["mode"]
        ce   = ctx_emoji(ctx)
        le   = loi_emoji(loi, mode)
        price = s["price"]
        sribi = s["sribi"]
        gs   = pmcc_gates.get(asset, "")
        ge   = gate_emoji(gs)
        gs_short = gs.replace("_", "")[:9] if gs else "  ?"
        asset_lines.append(
            f"`{asset:4s}` ${price:>7.2f} {ce}{ctx[:4]:4s}  LOI={loi:+5.1f}{le}  "
            f"S={sribi['st']:+.0f} L={sribi['lt']:+.0f} VL={sribi['vlt']:+.0f}  "
            f"{ge}{gs_short}"
        )

    # AB1 active signals
    ab1_active = []
    for asset, sigs in ab1.items():
        if sigs:
            last = sigs[-1]
            if hasattr(last, "timestamp"):
                conf = getattr(last, "confidence", 0)
                ab1_active.append(f"{asset} ({conf:.0%} conf)")

    # AB2 open positions
    ab2_open = []
    for asset, sigs in ab2.items():
        opens = [x for x in sigs if isinstance(x, dict) and x.get("status") == "OPEN"]
        for p in opens:
            bh = p.get("bars_held", 0)
            days = round(bh / 6, 0)
            ab2_open.append(f"{asset} ({days:.0f}d)")

    # Build embed
    asset_block = "\n".join(asset_lines)
    ab1_str = ", ".join(ab1_active) if ab1_active else "None"
    ab2_str = ", ".join(ab2_open)   if ab2_open   else "None"

    description = (
        gli_line +
        regime_line +
        "\n```\n" + asset_block + "\n```\n"
        f"**AB1 Signals:** {ab1_str}\n"
        f"**AB2 Open:** {ab2_str}\n"
        f"\n-# {ts}"
    )

    return {
        "username": "SRI Engine",
        "embeds": [{
            "title": "🤖 Daily Engine Run",
            "description": description,
            "color": 0x238636 if eff >= 2 else (0xD29922 if eff >= 0 else 0xF85149),
        }]
    }


def post_discord(payload: dict, webhook_url: str) -> bool:
    """POST embed to Discord webhook."""
    if not webhook_url:
        log("  No webhook URL — skipping Discord post")
        return False
    body = json.dumps(payload).encode()
    req  = urllib.request.Request(webhook_url, data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "mstr-cio/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            log(f"  Discord → HTTP {r.status}")
            return r.status in (200, 204)
    except urllib.error.HTTPError as e:
        log(f"  Discord HTTP error: {e.code} {e.read()[:200]}")
        return False


# ── Main ─────────────────────────────────────────────────────────

def main():
    start = time.time()
    log("=" * 60)
    log("Daily engine run starting")

    # 1. Pull CSVs
    log("Step 1/4 — Syncing CSVs from GitHub...")
    updated, skipped = pull_csvs()
    log(f"  Summary: {updated} updated, {skipped} unchanged")

    # 2. Run engine
    log("Step 2/4 — Running SRI Engine (4 layers)...")
    result = run_engine()
    if result is None:
        log("FATAL: Engine failed. Aborting.")
        return 1

    # 3. Regenerate dashboard
    log("Step 3/4 — Regenerating dashboard...")
    regen_dashboard()

    # 4. Post to Discord
    log("Step 4/5 — Posting to Discord...")
    if result:
        payload = build_discord_payload(result)
        post_discord(payload, WEBHOOK_ALERTS)

    # 5. PMCC gate transition alerts
    log("Step 5/5 — PMCC gate transition alerts...")
    if result:
        try:
            sys.path.insert(0, "/mnt/mstr-scripts")
            import pmcc_alerts
            n_sent = pmcc_alerts.run(result, WEBHOOK_ALERTS)
            log(f"  PMCC alerts: {n_sent} sent")
        except Exception as e:
            log(f"  PMCC alerts error: {e}")
            import traceback
            traceback.print_exc()

    elapsed = time.time() - start
    log(f"Done in {elapsed:.1f}s")
    log("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
