#!/usr/bin/env python3
"""
SRI Engine Dashboard Generator
===============================
Runs the full 4-layer engine and renders a self-contained HTML dashboard.

Usage:
    python3 generate_dashboard.py [--output /path/to/dashboard.html]

Output: Single HTML file with embedded CSS/JS. No external dependencies.
Intended to be refreshed by cron on the same cadence as daily CSV ingestion.

Author: CIO Engine
Date: 2026-03-05
"""

import sys
import os
import json
import argparse
from datetime import datetime

sys.path.insert(0, "/mnt/mstr-scripts")
os.environ.setdefault("FRED_API_KEY", "8ee8d7967be4aab0fdc7565e85676260")

from sri_engine import SRIEngineV2, Context


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def ctx_class(ctx_str):
    if ctx_str == "TAILWIND": return "green"
    if ctx_str == "MIXED":    return "yellow"
    return "red"

def score_class(s):
    if s >= 2:  return "green"
    if s >= 0:  return "yellow"
    return "red"

def loi_class(loi, mode="Momentum"):
    thresh = -60 if mode == "Momentum" else -40
    if loi < thresh:     return "red"
    if loi > 40:         return "green"
    return "neutral"

def loi_label(loi, mode="Momentum"):
    thresh = -60 if mode == "Momentum" else -40
    deep   = -80 if mode == "Momentum" else -60
    if loi < deep:   return "🔴 DEEP ACC"
    if loi < thresh: return "🟠 ACC"
    if loi > 80:     return "🟢 DIST+"
    if loi > 60:     return "🟢 DIST"
    if loi > 40:     return "🟡 TRIM"
    return "⚪ HOLD"

def ab3_last(sigs):
    if not sigs: return "—"
    last = sigs[-1]
    sig_type = last[0] if isinstance(last, tuple) else str(last)
    return sig_type.replace("AB3_", "").replace("_", " ")

def fmt_pct(v): return f"{v:+.1f}%"
def fmt_score(v): return f"{v:+d}"
def esc(s): return str(s).replace("<","&lt;").replace(">","&gt;")


# ═══════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════════════════════════════

CSS = """
:root {
  --bg: #0d1117; --bg2: #161b22; --bg3: #21262d;
  --border: #30363d; --text: #c9d1d9; --muted: #8b949e;
  --green: #3fb950; --yellow: #d29922; --red: #f85149;
  --blue: #58a6ff; --purple: #bc8cff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: 'SF Mono', 'Fira Code', monospace; font-size: 13px; line-height: 1.5; }
h1 { font-size: 18px; color: var(--blue); }
h2 { font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
.header { padding: 16px 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
.ts { color: var(--muted); font-size: 11px; }
.layout { display: grid; grid-template-columns: 320px 1fr; gap: 12px; padding: 12px; }
.left-col { display: flex; flex-direction: column; gap: 12px; }
.right-col { display: flex; flex-direction: column; gap: 12px; }
.panel { background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 14px; }
.panel-title { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }
table { width: 100%; border-collapse: collapse; }
th { color: var(--muted); font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; padding: 4px 6px; text-align: left; border-bottom: 1px solid var(--border); }
td { padding: 5px 6px; border-bottom: 1px solid var(--bg3); }
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--bg3); }
.green  { color: var(--green); }
.yellow { color: var(--yellow); }
.red    { color: var(--red); }
.blue   { color: var(--blue); }
.purple { color: var(--purple); }
.neutral { color: var(--muted); }
.bold   { font-weight: bold; }
.score-big { font-size: 28px; font-weight: bold; text-align: center; padding: 8px 0; }
.score-label { text-align: center; font-size: 11px; color: var(--muted); margin-bottom: 12px; }
.kv { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid var(--bg3); }
.kv:last-child { border-bottom: none; }
.kv-key { color: var(--muted); }
.kv-val { font-weight: bold; }
.tag { display: inline-block; padding: 1px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
.tag-green  { background: #1a3a1f; color: var(--green); }
.tag-yellow { background: #3a2f0a; color: var(--yellow); }
.tag-red    { background: #3a0f0f; color: var(--red); }
.tag-blue   { background: #0d2a4a; color: var(--blue); }
.tag-neutral{ background: var(--bg3); color: var(--muted); }
.signal-dot { font-size: 10px; margin-right: 2px; }
.component-bar { height: 4px; background: var(--bg3); border-radius: 2px; margin-top: 2px; }
.component-fill { height: 4px; border-radius: 2px; }
.bar-pos { background: var(--green); }
.bar-neg { background: var(--red); }
.bar-neu { background: var(--muted); }
.full-width { grid-column: 1 / -1; }
@media (max-width: 900px) { .layout { grid-template-columns: 1fr; } .left-col, .right-col { } }
"""

def build_html(reg, state, ab1_sigs, ab2_sigs, ab3_sigs, generated_at):
    gli = reg.gli_state
    eff = reg.effective_score
    raw = reg.composite_score
    adj = reg.adjusted_score

    # ── Score gauge colour ───────────────────────────────────────
    sc = score_class(eff)

    # ── GLI panel ────────────────────────────────────────────────
    gli_html = ""
    if gli and gli.error is None:
        gz = gli.gli_zscore
        gz_cls = "green" if gz > 0.5 else ("red" if gz < -0.5 else "neutral")
        gc = gli.gegi.composite
        gc_cls = "green" if gc > 0.3 else ("red" if gc < -0.3 else "neutral")
        sofr = gli.sofr_iorb_spread_bps
        sofr_cls = "red" if sofr > 20 else "neutral"

        comp_rows = ""
        for c in gli.components:
            roc = c.roc_26w
            bar_cls = "bar-pos" if roc > 0 else ("bar-neg" if roc < 0 else "bar-neu")
            bar_w = min(100, abs(roc) * 5)
            arrow = "↑" if c.roc_direction == "UP" else ("↓" if c.roc_direction == "DOWN" else "→")
            roc_cls = "green" if roc > 0 else ("red" if roc < 0 else "neutral")
            comp_rows += f"""
            <tr>
              <td>{esc(c.series_id)}</td>
              <td style="color:var(--muted);font-size:10px">{int(c.weight*100)}%</td>
              <td class="{roc_cls}">{arrow} {roc:+.1f}%</td>
              <td style="color:var(--muted);font-size:10px">{c.latest_date}</td>
            </tr>"""

        adj_tag = f'<span class="tag tag-{gz_cls}">{gli.label} ({gli.score_adjustment:+d})</span>'
        gli_html = f"""
        <div class="panel">
          <div class="panel-title">Layer 0 — GLI Engine</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px">
            <div>
              <div style="font-size:10px;color:var(--muted)">GLI Z-Score</div>
              <div style="font-size:22px;font-weight:bold" class="{gz_cls}">{gz:+.3f}</div>
              <div style="font-size:10px;color:var(--muted)">{gli.gli_trend} | mom {gli.gli_momentum:+.2f}</div>
            </div>
            <div>
              <div style="font-size:10px;color:var(--muted)">GEGI</div>
              <div style="font-size:22px;font-weight:bold" class="{gc_cls}">{gc:+.3f}</div>
              <div style="font-size:10px;color:var(--muted)">{gli.gegi.label}</div>
            </div>
          </div>
          <div class="kv"><span class="kv-key">SOFR-IORB</span><span class="kv-val {sofr_cls}">{sofr:+.0f} bps {'⚠' if sofr > 20 else '✓'}</span></div>
          <div class="kv"><span class="kv-key">Monetary</span><span class="kv-val {'green' if gli.gegi.monetary_score > 0 else 'red' if gli.gegi.monetary_score < 0 else 'neutral'}">{gli.gegi.monetary_score:+.2f}</span></div>
          <div class="kv"><span class="kv-key">Fiscal</span><span class="kv-val {'green' if gli.gegi.fiscal_score > 0 else 'red' if gli.gegi.fiscal_score < 0 else 'neutral'}">{gli.gegi.fiscal_score:+.2f}</span></div>
          <div class="kv" style="margin-bottom:12px"><span class="kv-key">External (NFCI)</span><span class="kv-val {'green' if gli.gegi.external_score > 0 else 'red' if gli.gegi.external_score < 0 else 'neutral'}">{gli.gegi.external_score:+.2f}</span></div>
          <div style="margin-bottom:8px">{adj_tag}</div>
          <table>
            <tr><th>Series</th><th>Wt</th><th>ROC 26w</th><th>As of</th></tr>
            {comp_rows}
          </table>
        </div>"""
    else:
        gli_html = '<div class="panel"><div class="panel-title">Layer 0 — GLI Engine</div><div class="neutral">Unavailable</div></div>'

    # ── Regime panel ─────────────────────────────────────────────
    regime_rows = ""
    for name, inp in reg.inputs.items():
        ic = "green" if inp.score > 0 else ("red" if inp.score < 0 else "neutral")
        regime_rows += f"""
        <tr>
          <td class="bold">{esc(name)}</td>
          <td class="{ic}">{fmt_score(inp.score)}</td>
          <td style="color:var(--muted);font-size:11px">{esc(inp.interpretation)}</td>
        </tr>"""

    adj_note = ""
    if gli and gli.score_adjustment != 0:
        adj_note = f'<div style="font-size:11px;color:var(--muted);margin-top:4px">Raw: {raw:+d} → GLI adj: {adj:+d}</div>'

    regime_html = f"""
    <div class="panel">
      <div class="panel-title">Layer 1 — Regime Engine</div>
      <div class="score-big {sc}">{eff:+d}<span style="font-size:14px;color:var(--muted)">/7</span></div>
      <div class="score-label">{esc(reg.adjusted_regime_label or reg.regime_label)}</div>
      {adj_note}
      <div class="kv"><span class="kv-key">Vehicle</span><span class="kv-val blue">{esc(reg.vehicle)}</span></div>
      <div class="kv" style="margin-bottom:12px"><span class="kv-key">VIX</span><span class="kv-val {'yellow' if reg.vix_level > 25 else 'neutral'}">{reg.vix_level:.1f}</span></div>
      <table>
        <tr><th>Input</th><th>Δ</th><th>Interpretation</th></tr>
        {regime_rows}
      </table>
    </div>"""

    # ── Asset grid ───────────────────────────────────────────────
    asset_rows = ""
    for asset, s in state.items():
        sr = s['sribi']
        ctx = s['context']
        loi = s['loi']
        mode = s['mode']
        ctx_c = ctx_class(ctx)
        loi_c = loi_class(loi, mode)
        loi_lbl = loi_label(loi, mode)

        # AB3 last signal
        ab3_s = ab3_sigs.get(asset, [])
        ab3_lbl = "—"
        if ab3_s:
            last_sig = ab3_s[-1]
            if isinstance(last_sig, tuple) and len(last_sig) >= 2:
                sig_name = str(last_sig[0]).replace("AB3_","").replace("_"," ")
                sig_date = str(last_sig[1])[:10] if last_sig[1] else ""
                ab3_lbl = f"{sig_name} {sig_date}"

        # AB1 recent signal
        ab1_s = ab1_sigs.get(asset, [])
        ab1_lbl = "—"
        if ab1_s:
            last = ab1_s[-1]
            ts = str(last.timestamp)[:10] if hasattr(last, 'timestamp') else "?"
            conf = f"{last.confidence:.0%}" if hasattr(last, 'confidence') else ""
            ab1_lbl = f"{ts} {conf}"

        # AB2 open
        ab2_s = ab2_sigs.get(asset, [])
        ab2_open = [x for x in ab2_s if isinstance(x, dict) and x.get('status') == 'OPEN']
        ab2_lbl = "—"
        if ab2_open:
            p = ab2_open[-1]
            ed = str(p.get('entry_date',''))[:10]
            bh = p.get('bars_held', 0)
            ab2_lbl = f"🟢 {ed} ({bh}b)"

        sribi_fmt = f"{sr['vst']:+.0f}/{sr['st']:+.0f}/{sr['lt']:+.0f}/{sr['vlt']:+.0f}"

        asset_rows += f"""
        <tr>
          <td class="bold">{esc(asset)}</td>
          <td>${s['price']:.2f}</td>
          <td><span class="tag tag-{ctx_c}">{esc(ctx)}</span></td>
          <td style="font-size:11px;color:var(--muted)">{sribi_fmt}</td>
          <td class="{loi_c}">{loi:+.1f}</td>
          <td>{loi_lbl}</td>
          <td style="font-size:11px;color:var(--muted)">{esc(ab3_lbl)}</td>
          <td style="font-size:11px;color:var(--muted)">{esc(ab1_lbl)}</td>
          <td style="font-size:11px;color:var(--muted)">{esc(ab2_lbl)}</td>
        </tr>"""

    asset_grid = f"""
    <div class="panel">
      <div class="panel-title">Layer 2 — Asset State (all 8)</div>
      <table>
        <tr>
          <th>Asset</th><th>Price</th><th>Context</th>
          <th>SRIBI V/S/L/VL</th><th>LOI</th><th>Zone</th>
          <th>AB3 Last</th><th>AB1 Last</th><th>AB2 Open</th>
        </tr>
        {asset_rows}
      </table>
    </div>"""

    # ── AB2 open positions detail ────────────────────────────────
    ab2_detail_rows = ""
    for asset, sigs in ab2_sigs.items():
        opens = [x for x in sigs if isinstance(x, dict) and x.get('status') == 'OPEN']
        for p in opens:
            ed = str(p.get('entry_date',''))[:10]
            entry_px = p.get('entry', 0)
            bh = p.get('bars_held', 0)
            days = round(bh / 6, 1)
            ctx_val = p.get('context', '?')
            ab2_detail_rows += f"""
            <tr>
              <td class="bold">{esc(asset)}</td>
              <td>{ed}</td>
              <td>${entry_px:.2f}</td>
              <td><span class="tag tag-{ctx_class(ctx_val)}">{esc(ctx_val)}</span></td>
              <td>{bh}b ({days}d)</td>
              <td class="yellow">OPEN</td>
            </tr>"""

    ab2_panel = f"""
    <div class="panel">
      <div class="panel-title">AB2 — Open Spreads</div>
      {'<div class="neutral" style="font-size:12px">No open positions</div>' if not ab2_detail_rows else f"""
      <table>
        <tr><th>Asset</th><th>Entry</th><th>Price</th><th>Context</th><th>Held</th><th>Status</th></tr>
        {ab2_detail_rows}
      </table>"""}
    </div>"""

    # ── AB1 recent signals ───────────────────────────────────────
    ab1_rows = ""
    for asset, sigs in ab1_sigs.items():
        for s in (sigs[-2:] if sigs else []):
            ts = str(s.timestamp)[:10] if hasattr(s, 'timestamp') else "?"
            price = f"${s.price:.2f}" if hasattr(s, 'price') else "?"
            conf = f"{s.confidence:.0%}" if hasattr(s, 'confidence') else "?"
            loi_v = s.metadata.get('loi', 0) if hasattr(s, 'metadata') else 0
            conf_cls = "green" if getattr(s, 'confidence', 0) >= 0.8 else "yellow"
            ab1_rows += f"""
            <tr>
              <td class="bold">{esc(asset)}</td>
              <td>{ts}</td>
              <td>{price}</td>
              <td class="{conf_cls}">{conf}</td>
              <td class="neutral">{loi_v:+.1f}</td>
            </tr>"""

    ab1_panel = f"""
    <div class="panel">
      <div class="panel-title">AB1 — Pre-Breakout Signals (recent)</div>
      {'<div class="neutral" style="font-size:12px">No recent signals</div>' if not ab1_rows else f"""
      <table>
        <tr><th>Asset</th><th>Date</th><th>Price</th><th>Conf</th><th>LOI</th></tr>
        {ab1_rows}
      </table>"""}
    </div>"""

    # ── Footer ───────────────────────────────────────────────────
    footer = f"""
    <div style="padding:12px 20px;border-top:1px solid var(--border);color:var(--muted);font-size:11px;text-align:center">
      Generated {generated_at} UTC &nbsp;|&nbsp; SRI Engine v2.1 &nbsp;|&nbsp; Data: last CSV push
    </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="300">
  <title>SRI Engine Dashboard</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>SRI Engine Dashboard</h1>
      <div class="ts">4-Layer Architecture: GLI → Regime → Signal → Allocation</div>
    </div>
    <div class="ts" style="text-align:right">
      Last updated: {generated_at} UTC<br>
      Regime: <span class="{sc}">{eff:+d}/7</span> &nbsp; Vehicle: <span class="blue">{esc(reg.vehicle)}</span> &nbsp; VIX: {reg.vix_level:.1f}
    </div>
  </div>

  <div class="layout">
    <div class="left-col">
      {gli_html}
      {regime_html}
    </div>
    <div class="right-col">
      {asset_grid}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        {ab2_panel}
        {ab1_panel}
      </div>
    </div>
  </div>
  {footer}
</body>
</html>"""

    return html


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/mnt/mstr-data/dashboard.html")
    parser.add_argument("--no-gli", action="store_true")
    args = parser.parse_args()

    print(f"[Dashboard] Running engine...")
    engine = SRIEngineV2()
    result = engine.run_all(verbose=False, skip_gli=args.no_gli)

    reg      = result["regime"]
    state    = result["current_state"]
    ab1_sigs = result["ab1_signals"]
    ab2_sigs = result["ab2_signals"]
    ab3_sigs = result["ab3_signals"]

    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    html = build_html(reg, state, ab1_sigs, ab2_sigs, ab3_sigs, generated_at)

    with open(args.output, "w") as f:
        f.write(html)
    print(f"[Dashboard] Written → {args.output}  ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
