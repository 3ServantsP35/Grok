#!/usr/bin/env python3
"""
Morning Brief — MSTR Options Engine
Generates pre-market briefing from all data sources.
Sends to Discord and saves to ~/mstr-engine/logs/briefs/
"""

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone

DB_PATH = "/mnt/mstr-data/mstr.db"
BRIEFS_DIR = "/home/openclaw/mstr-engine/logs/briefs"
# Container fallback
if not os.path.exists("/home/openclaw/mstr-engine/logs"):
    BRIEFS_DIR = "/mnt/mstr-logs/briefs"

sys.path.insert(0, "/mnt/mstr-scripts")
sys.path.insert(0, "/home/openclaw/mstr-engine/scripts")

from send_alert import send_alert, load_webhook, SSL_CTX, COLORS
import urllib.request


def send_long_brief(title, sections, color="blue"):
    """Send a multi-embed brief to Discord (bypasses 4096 char limit)."""
    webhook_url = load_webhook()
    now = datetime.now(timezone.utc).isoformat()
    color_int = COLORS.get(color, COLORS["blue"])

    embeds = []

    # Title embed
    embeds.append({
        "title": title,
        "description": sections[0] if sections else "",
        "color": color_int,
        "timestamp": now,
    })

    # Additional sections as separate embeds (Discord limit: 10 embeds per message)
    for section in sections[1:10]:
        embeds.append({
            "description": section,
            "color": color_int,
        })

    payload = json.dumps({"embeds": embeds}).encode("utf-8")

    for attempt in range(2):
        try:
            req = urllib.request.Request(
                webhook_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (compatible; MSTREngine/1.0)",
                },
                method="POST",
            )
            resp = urllib.request.urlopen(req, context=SSL_CTX, timeout=15)
            if resp.status in (200, 204):
                return True
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
            else:
                print(f"Brief send failed: {e}", file=sys.stderr)
                return False
    return False


def build_brief():
    """Query all data sources and build the morning brief."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sections = []

    # ============================================
    # 1. PRICE & MVRV
    # ============================================
    ohlcv = conn.execute(
        "SELECT timestamp, open, high, low, close, volume FROM ohlcv ORDER BY timestamp DESC LIMIT 5"
    ).fetchall()

    sri = conn.execute(
        "SELECT timestamp, sth_mvrv, sth_mvrv_zone, fast_tl, fast_tl_color, slow_tl, "
        "slow_tl_color, slow_tl_slope, slow_tl_slope_roc, sribi_score, sribi_score_v2, "
        "volume_vs_20d_adv, volume_spike, consecutive_red_bars, stage_boolean, "
        "support, robust_fit, resistance "
        "FROM sri_indicators ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()

    if ohlcv:
        last = ohlcv[0]
        prev = ohlcv[1] if len(ohlcv) > 1 else None
        close = last[4]
        prev_close = prev[4] if prev else close
        change = close - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0
        vol = last[5]

        arrow = "🟢" if change >= 0 else "🔴"

        mvrv = sri[1] if sri else 0
        mvrv_zone = sri[2] if sri else "unknown"

        section = f"{arrow} **MSTR ${close:.2f}** ({change:+.2f} / {change_pct:+.1f}%)\n"
        section += f"📊 Range: ${last[3]:.2f} – ${last[2]:.2f} | Vol: {vol:,.0f}\n"
        section += f"📈 **STH-MVRV: {mvrv:.4f}** ({mvrv_zone.replace('_', ' ')})"

        sections.append(section)

    # ============================================
    # 2. mNAV & BTC-MSTR RELATIONSHIP (TOP INDICATOR)
    # ============================================
    mnav_row = conn.execute(
        "SELECT mnav_ratio, premium_pct, btc_price, mstr_price, btc_per_share, implied_btc_price "
        "FROM mnav ORDER BY date DESC LIMIT 1"
    ).fetchone()
    
    mnav_hist = conn.execute(
        "SELECT AVG(mnav_ratio), MIN(mnav_ratio), MAX(mnav_ratio) FROM mnav"
    ).fetchone()
    
    # Fear & Greed
    fng = conn.execute(
        "SELECT value, classification FROM sentiment WHERE source='fear_greed' ORDER BY date DESC LIMIT 1"
    ).fetchone()
    
    # BTC derivatives
    funding = conn.execute(
        "SELECT value, json_extract(detail_json, '$.annualized_pct') FROM btc_derivatives "
        "WHERE metric='funding_rate' ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    
    # Skew
    skew_row = conn.execute(
        "SELECT skew_regime, put_call_skew_30d, skew_25d_30, iv_5d_put, iv_atm FROM options_skew "
        "ORDER BY date DESC LIMIT 1"
    ).fetchone()
    
    if mnav_row:
        mnav_val = mnav_row[0]
        mnav_z = (mnav_val - 1.596) / 0.412  # Historical mean/std from backtest
        btc_price_val = mnav_row[2]
        implied_btc = mnav_row[5]
        
        # Regime
        if mnav_z < -1.5:
            mnav_regime = "🔥 EXTREME DISCOUNT — Maximum accumulation zone"
        elif mnav_z < -0.5:
            mnav_regime = "🟢 DISCOUNT — Favorable for share buying + put selling"
        elif mnav_z < 0.5:
            mnav_regime = "⚪ FAIR VALUE — Balanced approach"
        elif mnav_z < 1.5:
            mnav_regime = "🟡 PREMIUM — Favor call selling"
        else:
            mnav_regime = "🔴 EXTREME PREMIUM — Aggressively sell calls, reduce shares"
        
        # Mean reversion potential
        reversion_pct = ((1.596 / mnav_val) - 1) * 100 if mnav_val > 0 else 0
        
        section = "**📊 mNAV & BTC-MSTR DASHBOARD**\n"
        section += f"```\n"
        section += f"mNAV:      {mnav_val:.3f}x  (Z={mnav_z:+.2f})\n"
        section += f"Premium:   {mnav_row[1]:+.1f}%\n"
        section += f"BTC:       ${btc_price_val:,.0f}\n"
        section += f"Implied:   ${implied_btc:,.0f}  ({'above' if implied_btc > btc_price_val else 'below'} spot)\n"
        section += f"BTC/Share: {mnav_row[4]:.6f}\n"
        section += f"Beta:      1.39x (up: 1.86x / down: 1.02x)\n"
        if mnav_hist:
            section += f"Range:     {mnav_hist[1]:.3f}x — {mnav_hist[2]:.3f}x (avg {mnav_hist[0]:.3f}x)\n"
        section += f"Reversion: {reversion_pct:+.0f}% to mean\n"
        section += f"```\n"
        section += f"{mnav_regime}\n"
        
        # BTC sentiment row
        sentiment_parts = []
        if fng:
            emoji = "😱" if fng[0] < 25 else "😰" if fng[0] < 40 else "😐" if fng[0] < 60 else "😊" if fng[0] < 75 else "🤑"
            sentiment_parts.append(f"{emoji} Fear/Greed: {fng[0]:.0f} ({fng[1]})")
        if funding:
            sentiment_parts.append(f"Funding: {funding[1]:.1f}% ann." if funding[1] else f"Funding: {funding[0]:.6f}")
        if skew_row:
            sentiment_parts.append(f"Skew: {skew_row[0]}")
        
        if sentiment_parts:
            section += "\n" + " | ".join(sentiment_parts)
        
        sections.append(section)
    
    # ============================================
    # 3. SRI STAGE DESIGNATION
    # ============================================
    if sri:
        scores_raw = json.loads(sri[14]) if sri[14] else {}
        scores = {k: v for k, v in scores_raw.items() if k.isdigit()}
        stage = max(scores, key=scores.get) if scores else "?"
        best_score = scores.get(stage, 0)
        second_best = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0
        confidence = min(0.95, 0.4 + ((best_score - second_best) / best_score * 0.55)) if best_score > 0 else 0

        # Sub-stage
        sub = ""
        if stage == "4" and sri[8] and sri[8] > 0:  # slow_tl_slope_roc > 0
            sub = "C"
        elif stage == "2" and sri[8] and sri[8] < 0:
            sub = "C"

        fast_color_emoji = {"green": "🟢", "red": "🔴", "orange": "🟡"}.get(sri[4], "⚪")
        slow_color_emoji = {"green": "🟢", "red": "🔴", "orange": "🟡"}.get(sri[6], "⚪")

        section = f"**🎯 STAGE {stage}{sub}** (confidence: {confidence:.0%})\n"
        section += f"```\nScore: S1={scores.get('1',0)} | S2={scores.get('2',0)} | S3={scores.get('3',0)} | S4={scores.get('4',0)}\n```\n"
        section += f"{fast_color_emoji} Fast TL: ${sri[3]:.2f} ({sri[4]})\n"
        section += f"{slow_color_emoji} Slow TL: ${sri[5]:.2f} ({sri[6]}) — {sri[13]} consecutive red bars\n"
        section += f"Slow TL Slope RoC: {sri[8]:+.4f}"

        if sri[8] and sri[8] > 0 and sri[6] == "red":
            section += " ⚠️ **Decline decelerating**"

        section += f"\nSRIBI: {sri[9]:.1f} (v2: {sri[10]:.1f})\n"
        section += f"Vol/ADV: {sri[11]:.2f}x {'🔺 SPIKE' if sri[12] else ''}"

        # Transition signals
        transitions = []
        if stage == "4" and sri[8] and sri[8] > 0:
            transitions.append("✋ Slow TL deceleration (4→1 precursor)")
        if stage == "4" and sri[4] == "green":
            transitions.append("✋ Fast TL turned green")
        if mvrv < 0.5:
            transitions.append("✋ MVRV in deep discount — bottoming zone")
        if sri[11] and sri[11] >= 2.5:
            transitions.append("🚨 Volume capitulation detected (>2.5x ADV)")

        if transitions:
            section += "\n\n**Transition Signals:**\n" + "\n".join(transitions)

        sections.append(section)

    # ============================================
    # 3. KEY LEVELS
    # ============================================
    if sri:
        sup = sri[15]
        rob = sri[16]
        res = sri[17]
        fast = sri[3]
        slow = sri[5]

        section = "**📍 Key Levels**\n"
        section += f"```\n"
        section += f"Resistance:  ${res:.2f}\n"
        section += f"Slow TL:     ${slow:.2f}\n"
        section += f"Robust Fit:  ${rob:.2f}\n"
        section += f"Fast TL:     ${fast:.2f}\n"
        section += f"Support:     ${sup:.2f}\n"
        section += f"```"
        sections.append(section)

    # ============================================
    # 4. GLI & MACRO
    # ============================================
    gli = conn.execute(
        "SELECT timestamp, fed_bs_trillions, gli_score, macro_score, "
        "grid_regime, paradigm, gli_trend FROM gli_proxy ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()

    fred_latest = {}
    for series in ["DGS10", "DGS2", "DFEDTARU", "DTWEXBGS"]:
        r = conn.execute(
            "SELECT value FROM fred WHERE series_id=? ORDER BY timestamp DESC LIMIT 1",
            (series,),
        ).fetchone()
        if r:
            fred_latest[series] = r[0]

    if gli:
        fed_bs   = gli[1] or 0.0   # Fed balance sheet $T
        zscore   = gli[2] or 0.0   # GLI Z-score
        macro_sc = gli[3] or 0      # macro_score (+1/-1/0)
        grid     = gli[4] or ""
        paradigm = gli[5] or ""
        trend    = gli[6] or ""

        if zscore > 0.5:
            regime = "🟢 EXPANSIONARY"
        elif zscore < -0.5:
            regime = "🔴 CONTRACTIONARY"
        else:
            regime = "🟡 NEUTRAL"

        section = f"**🌍 Global Liquidity**\n"
        section += f"Fed BS: ${fed_bs:.2f}T | Z-Score: **{zscore:+.3f}** | Macro: {macro_sc:+d}\n"
        section += f"Regime: {regime} | GRID: {grid} | Paradigm: {paradigm} | Trend: {trend}\n\n"

        # Macro
        dgs10 = fred_latest.get("DGS10", 0)
        dgs2 = fred_latest.get("DGS2", 0)
        spread = dgs10 - dgs2 if dgs10 and dgs2 else 0
        section += f"**Macro:** 10Y: {dgs10}% | 2Y: {dgs2}% | 2s10s: {spread:+.2f}bp\n"
        section += f"Fed Funds: {fred_latest.get('DFEDTARU', '?')}% | DXY: {fred_latest.get('DTWEXBGS', '?')}"

        sections.append(section)

    # ============================================
    # 4.5 HOWELL PHASE (Layer 0.5)
    # ============================================
    try:
        sys.path.insert(0, "/mnt/mstr-scripts")
        from sri_engine import HowellPhaseEngine
        howell_eng   = HowellPhaseEngine()
        howell_state = howell_eng.compute()

        ph   = howell_state.phase
        conf = howell_state.confidence
        em   = howell_state.emoji
        scores_str = "  ".join(
            f"{p[:4]}:{v:+.0f}" for p, v in howell_state.phase_scores.items()
        )
        # Sector signal table
        signal_rows = ""
        signal_map  = {"BULL": "▲", "BEAR": "▼", "NEUTRAL": "─"}
        for ticker in ["XLK", "XLY", "XLF", "XLE", "XLP", "TLT", "GLD", "IWM", "VT"]:
            sig   = howell_state.sector_signals.get(ticker, "?")
            lt    = howell_state.sector_sribi.get(ticker, 0)
            arrow = signal_map.get(sig, "?")
            signal_rows += f"{ticker:4s} {arrow} {lt:+.0f}\n"

        # AB strategy guidance
        ab3_note = ""
        if ph == "Turbulence":
            ab3_note = "⚠️ AB3 Beta (MSTR/IBIT): wait for Rebound signal | AB2: PAUSED"
        elif ph == "Speculation":
            ab3_note = "⚠️ AB3 Beta: 50% max sizing | AB3 Cyclicals (TSLA): BLOCKED"
        elif ph in ("Rebound", "Calm"):
            ab3_note = "✅ AB3 all asset classes eligible | AB2 fully active"

        section  = f"**🌍 Howell Phase: {em} {ph}** (conf={conf:.0f}%)\n"
        section += f"```\nPhase scores: {scores_str}\n\n"
        section += f"Sector signals (LT SRIBI):\n{signal_rows}```\n"
        section += ab3_note
        sections.append(section)
    except Exception as _hpe:
        sections.append(f"**🌍 Howell Phase**\n*Unavailable: {type(_hpe).__name__}: {str(_hpe)[:100]}*")

    # ============================================
    # 4.6 LIQUIDITY REGIME × SIGNAL WEIGHTING (2026-03-03 insight)
    # ============================================
    try:
        from sri_engine import AdaptiveLOIEngine

        # Determine liquidity regime from HYG SRIBI + VIX LOI proxy
        # HYG ST SRIBI and VIX LOI are stored in gli_proxy or regime tables
        _hyg_sribi = None
        _vix_loi   = None
        try:
            _hyg_row = conn.execute(
                "SELECT gli_score FROM gli_proxy ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
            # Try dedicated regime columns if available
            _reg_row = conn.execute(
                "SELECT hyg_sribi, vix_loi FROM regime_state ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
            if _reg_row:
                _hyg_sribi = _reg_row[0]
                _vix_loi   = _reg_row[1]
        except Exception:
            pass

        # Classify liquidity regime
        if _hyg_sribi is not None and _vix_loi is not None:
            if _hyg_sribi > 0 and _vix_loi < 0:
                _liq_regime = "EXPANDING"
                _tf_guidance = "Short TF signals (VST/ST) elevated weight. Momentum sustains."
            elif _hyg_sribi < 0 and _vix_loi > 0:
                _liq_regime = "CONTRACTING"
                _tf_guidance = "LT/VLT confirmation required for AB3 deployment. ST for monitoring."
            else:
                _liq_regime = "NEUTRAL"
                _tf_guidance = "Balanced TF weighting. No adjustment."
        else:
            # Fallback: use gli_score as proxy (positive = expanding, negative = contracting)
            _gli_z = gli[2] if gli else 0.0
            if _gli_z > 0.3:
                _liq_regime = "EXPANDING"
                _tf_guidance = "Short TF signals (VST/ST) elevated weight. Momentum sustains."
            elif _gli_z < -0.3:
                _liq_regime = "CONTRACTING"
                _tf_guidance = "LT/VLT confirmation required for AB3 deployment. ST for monitoring."
            else:
                _liq_regime = "NEUTRAL"
                _tf_guidance = "Balanced TF weighting. No adjustment."

        # Pull adaptive LOI thresholds from AdaptiveLOIEngine for primary assets
        DATA_DIR = "/mnt/mstr-data"
        _adaptive_assets = {
            "MSTR": f"{DATA_DIR}/BATS_MSTR, 240_7b1cc.csv",
            "TSLA": f"{DATA_DIR}/BATS_TSLA, 240_b8831.csv",
            "IBIT": f"{DATA_DIR}/BATS_IBIT, 240_7654d.csv",
        }
        import pandas as pd, os as _os

        _adaptive_rows = []
        for _sym, _csv in _adaptive_assets.items():
            # Try to find CSV by prefix if exact path missing
            if not _os.path.exists(_csv):
                _prefix = f"BATS_{_sym}, 240_"
                _candidates = [
                    f for f in _os.listdir(DATA_DIR) if f.startswith(_prefix) and f.endswith(".csv")
                ]
                _csv = f"{DATA_DIR}/{_candidates[0]}" if _candidates else None

            if _csv and _os.path.exists(_csv):
                try:
                    _df = pd.read_csv(_csv)
                    _eng = AdaptiveLOIEngine(asset=_sym, asset_class="MOMENTUM")
                    _result = _eng.compute(_df)
                    _vol_regime = _result.vol_regime
                    _adaptive_thresh = _result.adaptive_threshold
                    _base_thresh     = _result.base_threshold
                    _loi_val         = _result.current_loi
                    _below           = "✅ YES" if _loi_val <= _adaptive_thresh else "No"
                    _adaptive_rows.append(
                        f"{_sym:<4} vol:{_vol_regime:<7} | Adaptive thresh: {_adaptive_thresh:+.1f}"
                        f" (base:{_base_thresh:+.1f}) | LOI:{_loi_val:+.1f} → below? {_below}"
                    )
                except Exception as _ae:
                    _adaptive_rows.append(f"{_sym:<4} adaptive threshold unavailable ({type(_ae).__name__})")
            else:
                _adaptive_rows.append(f"{_sym:<4} CSV not found — adaptive threshold skipped")

        _liq_emoji = {"EXPANDING": "🟢", "CONTRACTING": "🔴", "NEUTRAL": "🟡"}.get(_liq_regime, "⚪")
        _liq_section  = "```\n"
        _liq_section += "── Liquidity Regime Signal Weights ──────────────────────────\n"
        _liq_section += f"Liquidity: {_liq_emoji} {_liq_regime} | {_tf_guidance}\n"
        for _row in _adaptive_rows:
            _liq_section += _row + "\n"
        _liq_section += "─────────────────────────────────────────────────────────────\n"
        _liq_section += "```"
        # Append as sub-section tag to previous GLI/Howell section
        if sections:
            sections[-1] = sections[-1] + "\n\n" + _liq_section
        else:
            sections.append(_liq_section)

    except ImportError:
        # AdaptiveLOIEngine not yet available — skip gracefully
        pass
    except Exception as _liq_err:
        # Non-fatal — append a minimal note to the prior section
        if sections:
            sections[-1] = sections[-1] + f"\n\n*Liquidity regime weights unavailable: {type(_liq_err).__name__}: {str(_liq_err)[:80]}*"

    # ============================================
    # 5. IV REGIME
    # ============================================
    orats = conn.execute(
        "SELECT timestamp, iv_30day, iv_60day, iv_90day, hv_30day, iv_rank, iv_percentile, "
        "put_call_ratio, skew_index, term_structure_slope FROM orats_core ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()

    if orats:
        iv30 = orats[1] or 0
        hv30 = orats[4] or 0
        iv_rank = orats[5]
        iv_pctl = orats[6]
        pcr = orats[7] or 0
        skew = orats[8] or 0
        term_slope = orats[9] or 0

        iv_premium = ((iv30 - hv30) / hv30 * 100) if hv30 > 0 else 0

        section = f"**📉 IV Regime** ({orats[0]})\n"
        section += f"```\n"
        section += f"IV30:   {iv30*100:.1f}%    HV30: {hv30*100:.1f}%    Premium: {iv_premium:+.1f}%\n"
        section += f"IV60:   {(orats[2] or 0)*100:.1f}%    IV90: {(orats[3] or 0)*100:.1f}%\n"
        if iv_rank is not None:
            section += f"Rank:   {iv_rank:.0%}     Pctl: {iv_pctl:.0%}\n"
        section += f"P/C:    {pcr:.2f}      Skew: {skew:.2f}      Term: {term_slope:+.3f}\n"
        section += f"```\n"

        # Regime classification
        if iv_pctl and iv_pctl >= 0.9:
            section += "🔥 **ULTRA-HIGH IV** — Aggressively sell premium"
        elif iv_pctl and iv_pctl >= 0.7:
            section += "📈 **HIGH IV** — Standard credit selling"
        elif iv_pctl and iv_pctl >= 0.3:
            section += "📊 **NORMAL IV** — Selective, calendars/diagonals"
        elif iv_pctl is not None:
            section += "📉 **LOW IV** — Buy protection, minimize selling"
        else:
            section += f"IV regime: computing (need more data for rank/percentile)"

        if term_slope > 0.05:
            section += "\n📐 Contango — front vol cheap vs back"
        elif term_slope < -0.05:
            section += "\n📐 Backwardation — front vol elevated (event risk?)"

        sections.append(section)

    # ============================================
    # 6. EDGAR FILINGS
    # ============================================
    filings = conn.execute(
        "SELECT timestamp, filing_type, summary FROM edgar "
        "WHERE timestamp >= date((SELECT MAX(timestamp) FROM ohlcv), '-3 days') "
        "AND summary IS NOT NULL "
        "ORDER BY timestamp DESC LIMIT 5"
    ).fetchall()

    if filings:
        section = "**📋 Recent SEC Filings**\n"
        for f in filings:
            section += f"• {f[0]} | {f[1]} — {f[2][:80]}\n"
        sections.append(section)
    else:
        # Check for any recent filing
        any_filing = conn.execute(
            "SELECT timestamp, filing_type FROM edgar ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        if any_filing:
            sections.append(f"**📋 SEC Filings**\nNo new flagged filings. Last: {any_filing[0]} ({any_filing[1]})")

    # ============================================
    # 7. FLOW SUMMARY
    # ============================================
    flow_date = conn.execute(
        "SELECT MAX(timestamp) FROM flow WHERE trade_type != 'dark_pool'"
    ).fetchone()[0]

    # Skip flow section if data is stale (>2 trading days old)
    if flow_date:
        from datetime import timedelta
        flow_age = (datetime.now(timezone.utc) - datetime.fromisoformat(flow_date.replace('Z', '+00:00') if 'Z' in str(flow_date) else flow_date + 'T00:00:00+00:00')).days if 'T' in str(flow_date) else (datetime.now(timezone.utc).date() - datetime.strptime(flow_date, "%Y-%m-%d").date()).days
        if flow_age > 3:
            flow_date = None  # Stale — skip section

    if flow_date:
        flow = conn.execute(
            "SELECT COUNT(*), "
            "SUM(CASE WHEN is_unusual=1 THEN 1 ELSE 0 END), "
            "SUM(CASE WHEN sentiment='bullish' THEN premium ELSE 0 END), "
            "SUM(CASE WHEN sentiment='bearish' THEN premium ELSE 0 END), "
            "SUM(CASE WHEN trade_type='sweep' THEN premium ELSE 0 END) "
            "FROM flow WHERE timestamp=? AND trade_type != 'dark_pool'",
            (flow_date,),
        ).fetchone()

        dp = conn.execute(
            "SELECT COUNT(*), SUM(premium), "
            "SUM(CASE WHEN sentiment='bullish' THEN premium ELSE 0 END), "
            "SUM(CASE WHEN sentiment='bearish' THEN premium ELSE 0 END) "
            "FROM flow WHERE timestamp=? AND trade_type='dark_pool'",
            (flow_date,),
        ).fetchone()

        total_contracts = flow[0] or 0
        unusual = flow[1] or 0
        bull_prem = flow[2] or 0
        bear_prem = flow[3] or 0
        sweep_prem = flow[4] or 0
        net_prem = bull_prem - bear_prem

        dp_count = dp[0] or 0
        dp_total = dp[1] or 0
        dp_bull = dp[2] or 0
        dp_bear = dp[3] or 0

        section = f"**🐋 Flow Summary** ({flow_date})\n"
        section += f"```\n"
        section += f"Contracts: {total_contracts:,}  |  Unusual: {unusual:,}\n"
        section += f"Bull Prem: ${bull_prem:,.0f}\n"
        section += f"Bear Prem: ${bear_prem:,.0f}\n"
        section += f"Net:       ${net_prem:+,.0f} {'(bullish)' if net_prem > 0 else '(bearish)'}\n"
        section += f"Sweeps:    ${sweep_prem:,.0f}\n"
        section += f"\n"
        section += f"Dark Pool: {dp_count:,} prints | ${dp_total:,.0f} total\n"
        section += f"  Bull: ${dp_bull:,.0f} | Bear: ${dp_bear:,.0f}\n"
        section += f"```"

        sections.append(section)

    # ============================================
    # 8. AB2 PMCC — GATE STATES & OPEN CALLS
    # ============================================
    try:
        import pandas as pd
        from sri_engine import AB2PMCCEngine, PMCCGateState, PBearEngine

        # CSV paths for each asset (84-col AB3-enhanced preferred; 71-col fallback)
        DATA_DIR = "/mnt/mstr-data"
        PMCC_CSVS = {
            "MSTR": [f"{DATA_DIR}/BATS_MSTR, 240_7b1cc.csv"],   # v2 bearish indicators
            "IBIT": [f"{DATA_DIR}/BATS_IBIT, 240_7654d.csv"],
            "TSLA": [f"{DATA_DIR}/BATS_TSLA, 240_b8831.csv"],
            "SPY":  [f"{DATA_DIR}/BATS_SPY, 240_8f6d8.csv"],
            "QQQ":  [f"{DATA_DIR}/BATS_QQQ, 240_5de53.csv"],
            "GLD":  [f"{DATA_DIR}/BATS_GLD, 240_41f2b.csv"],
            "IWM":  [f"{DATA_DIR}/BATS_IWM, 240_9624e.csv"],
        }

        # Load GLI for threshold adjustment (gli_proxy table; no gegi column — use 0.0)
        gli_row = conn.execute(
            "SELECT gli_score FROM gli_proxy ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        gli_z   = float(gli_row[0]) if gli_row else 0.0
        gegi    = 0.0   # gegi not stored in gli_proxy; GLI Z-score is the primary adjuster

        pmcc_eng  = AB2PMCCEngine()
        gate_rows = []
        has_any   = False

        # Load P-BEAR states from DB (most recent per asset); fallback to live compute
        _pbear_db = {}
        try:
            _pb_rows = conn.execute(
                """SELECT asset, state FROM pbear_state_log
                   WHERE id IN (SELECT MAX(id) FROM pbear_state_log GROUP BY asset)"""
            ).fetchall()
            _pbear_db = {r[0]: r[1] for r in _pb_rows}
        except Exception:
            pass

        for asset, paths in PMCC_CSVS.items():
            df = None
            for p in paths:
                if os.path.exists(p):
                    try:
                        df = pd.read_csv(p)
                        break
                    except Exception:
                        continue
            if df is None or len(df) == 0:
                continue

            sig = pmcc_eng.current_signal(df, asset, gli_z=gli_z, gegi=gegi)
            state   = sig['gate_state']
            loi     = sig['loi']
            ct      = sig['ct_tier']
            ctx     = sig['context'][:4]           # TAIL/HEAD/MIXE
            thresh  = sig['trim_threshold']
            cls     = sig['asset_class'][:3]       # Mom/MR
            delta   = sig['max_delta']
            price   = sig['price']

            # Gate emoji
            gate_emoji = {
                'NO_CALLS':    '🔴',
                'OTM_INCOME':  '🟢',
                'DELTA_MGMT':  '🟠',
                'PAUSED_AB1':  '⏸️',
                'NO_POSITION': '⬜',
            }.get(state, '❓')

            # P-BEAR state: use DB if available, else compute live
            pbear_state_name = _pbear_db.get(asset)
            pbear_emoji      = '⚪'
            if pbear_state_name is None and df is not None:
                try:
                    _pb_eng  = PBearEngine(asset)
                    _pb_sig  = _pb_eng.compute(df)
                    pbear_state_name = _pb_sig.state.name
                    pbear_emoji      = _pb_sig.emoji
                except Exception:
                    pbear_state_name = 'N/A'
            else:
                _pbear_emoji_map = {
                    'INACTIVE': '⚪', 'WATCH': '👁', 'FORMING': '🟡',
                    'FORMING_PLUS': '🟠', 'CONFIRMED': '🔴',
                    'CONFIRMED_PLUS': '🚨', 'INVALIDATED': '✅',
                }
                pbear_emoji = _pbear_emoji_map.get(pbear_state_name or '', '⚪')

            gate_rows.append((asset, gate_emoji, state, loi, ct, ctx, delta, thresh, cls, price,
                               pbear_emoji, pbear_state_name or 'N/A'))
            has_any = True

        if has_any:
            section  = "**📝 AB2 PMCC — Gate States**\n"
            section += f"*GLI Z={gli_z:+.3f} | GEGI={gegi:+.3f}*\n"
            section += "```\n"
            section += f"{'Asset':<6} {'Gate':<13} {'LOI':>6}  {'CT':>3}  {'Ctx':>4}  {'δ max':>5}  {'Thresh':>6}  {'P-BEAR':<14}\n"
            section += "─" * 68 + "\n"
            for asset, em, state, loi, ct, ctx, delta, thresh, cls, price, pb_em, pb_st in gate_rows:
                state_short  = state.replace('_', ' ')[:12]
                pb_st_short  = (pb_st or 'N/A').replace('_', ' ')[:13]
                section += (f"{asset:<6} {em}{state_short:<12} {loi:>+6.1f}  CT{ct}  "
                            f"{ctx:<4}  {delta:>5.2f}  {thresh:>+6.0f}  {pb_em}{pb_st_short}\n")
            section += "```\n"

            # Momentum vs MR legend
            section += "🔴 NO\\_CALLS = accumulate | 🟢 OTM = δ≤0.25 | 🟠 DELTA\\_MGMT = δ≤0.40\n"
            section += "⚪=Inactive 👁=Watch 🟡=Forming 🟠=Forming+ 🔴=Confirmed 🚨=Conf+ ✅=Invalidated\n"
            section += f"*Momentum (MSTR/TSLA/IBIT) DELTA\\_MGMT threshold: LOI>+40 | MR: LOI>+20*\n\n"

            # ── Cross-Asset Accumulation Count (multi-asset deployment signal) ──────
            # Per backtest 2026-03-05: 3+ assets LOI<-20 simultaneously = max AB4 deploy
            acc_count = sum(1 for _, _, _, loi_v, *_ in gate_rows if loi_v < -20)
            _acc_emoji = "🟢" if acc_count <= 1 else ("🟡" if acc_count == 2 else "🔴")
            _acc_note  = ("Normal" if acc_count <= 1
                          else "Elevated — consider adding positions" if acc_count == 2
                          else "⚠ MAXIMUM DEPLOYMENT SIGNAL — 3+ assets accumulating")
            section += f"{_acc_emoji} **Cross-Asset Accumulation: {acc_count}/7 assets LOI<−20** — {_acc_note}\n\n"

            # ── Per-asset entry calibration notes (cross-asset LEAP backtest 2026-03-05) ──
            calib_notes = []
            for asset, _, _, loi_v, ct_v, ctx_v, *_ in gate_rows:
                if asset == "TSLA":
                    # Inverted concordance: 0 TFs+ = 78% WR; 3 TFs+ = 24% WR
                    tf_count = ct_v  # ct_tier ≈ TF concordance level
                    if tf_count >= 3:
                        calib_notes.append(f"⚠ **TSLA**: CT{tf_count} — inverted concordance; 24% 180d WR at full alignment. Entry quality degraded.")
                    elif loi_v < -20:
                        calib_notes.append(f"✓ **TSLA**: LOI={loi_v:+.1f}, CT{tf_count} — acc zone + low concordance = optimal entry setup (77%+ WR).")
                elif asset == "GLD":
                    # SMA200 structural filter: +30pp WR difference
                    try:
                        import glob
                        _gld_files = sorted(glob.glob("/mnt/mstr-data/BATS_GLD, 240_*.csv"))
                        if _gld_files:
                            _gdf = pd.read_csv(_gld_files[-1])
                            _gclose = float(_gdf.iloc[-1]["close"])
                            _gsma200 = float(_gdf["close"].tail(1200).mean()) if len(_gdf) >= 200 else None
                            if _gsma200:
                                if _gclose > _gsma200:
                                    calib_notes.append(f"✓ **GLD**: Above SMA200 (${_gclose:.2f} > ${_gsma200:.2f}) — structural entry gate OPEN (69% WR).")
                                else:
                                    calib_notes.append(f"⚠ **GLD**: Below SMA200 (${_gclose:.2f} < ${_gsma200:.2f}) — structural entry gate CLOSED (38% WR). Do not open new LEAPs.")
                    except Exception:
                        pass
                elif asset == "QQQ":
                    # Mixed context is counter-signal for QQQ (13.9% WR)
                    if ctx_v.startswith("MIXE"):
                        calib_notes.append(f"⚠ **QQQ**: Mixed context detected — COUNTER-SIGNAL (13.9% 180d WR). Do not enter. Requires VLT+ alignment.")
            if calib_notes:
                section += "**Entry Calibration:**\n"
                for note in calib_notes:
                    section += f"  {note}\n"
                section += "\n"

            # Open short calls from trade_log
            open_calls = conn.execute(
                """SELECT asset, strategy, strikes, expiry, entry_price, status
                   FROM trade_log
                   WHERE status = 'OPEN'
                     AND strategy LIKE '%PMCC%' OR strategy LIKE '%CC%' OR strategy LIKE '%Call%'
                   ORDER BY expiry ASC LIMIT 10"""
            ).fetchall()

            if open_calls:
                section += "**Open Short Calls:**\n```\n"
                for oc in open_calls:
                    section += f"{oc[0]:<6} {oc[1]:<12} {str(oc[2]):<12} exp:{oc[3]}  entry:{oc[4]}\n"
                section += "```"
            else:
                # Fall back to checking for any legacy short calls
                section += "*(No PMCC short calls in trade\\_log — legacy Mar 20 calls tracked manually)*"

            sections.append(section)

    except Exception as _pmcc_err:
        sections.append(f"**📝 AB2 PMCC**\n*Gate states unavailable: {type(_pmcc_err).__name__}: {str(_pmcc_err)[:120]}*")

    # ============================================
    # 8.5 PORTFOLIO DEFENSIVE POSTURE (P-BEAR Phase 2)
    # ============================================
    try:
        from sri_engine import (SRIEngineV2, DefensivePostureEngine,
                                Expression3Engine, PortfolioPosture)
        _eng = SRIEngineV2()
        _eng.load_all()

        # Run just P-BEAR + posture engines (skip GLI + full regime for speed)
        _pbear_sigs = _eng.run_pbear()

        _def_eng  = DefensivePostureEngine()
        _def_state = _def_eng.compute(_pbear_sigs)

        # mNAV live compute
        _mnav = 0.0
        try:
            _mnav_row = conn.execute(
                "SELECT mnav_ratio FROM mnav ORDER BY date DESC LIMIT 1"
            ).fetchone()
            if _mnav_row:
                _mnav = float(_mnav_row[0])
        except Exception:
            pass

        # Howell from DB
        _howell_db = conn.execute(
            "SELECT phase FROM howell_phase_state ORDER BY id DESC LIMIT 1"
        ).fetchone()
        _howell_phase = _howell_db[0] if _howell_db else 'Unknown'

        # Build posture section
        dp = _def_state
        posture_section  = f"**🛡️ Portfolio Defensive Posture: {dp.emoji} {dp.posture.name}**\n"
        posture_section += f"_{dp.rationale}_\n"
        posture_section += (f"AB4 floor: **{dp.ab4_floor_override:.0%}** | "
                            f"AB3 new entries: {'✅ yes' if dp.ab3_new_entries else '🚫 halted'} | "
                            f"Expr3 eligible: {'✅ yes' if dp.expression3_eligible else '⬜ no'}\n")

        if dp.posture != PortfolioPosture.NORMAL:
            if dp.forming_assets:
                posture_section += "\n**Forming assets (AB2 paused):**\n"
                for _a in dp.forming_assets:
                    _s = _pbear_sigs.get(_a)
                    _st = _s.state.name if _s else 'UNKNOWN'
                    _em = _s.emoji if _s else '⚪'
                    posture_section += f"  • {_a}: {_em} {_st}\n"
            if dp.confirmed_assets:
                posture_section += "\n**Confirmed assets (hedge zone):**\n"
                for _a in dp.confirmed_assets:
                    _s = _pbear_sigs.get(_a)
                    _st = _s.state.name if _s else 'UNKNOWN'
                    _em = _s.emoji if _s else '⚪'
                    posture_section += f"  • {_a}: {_em} {_st}\n"

        # Bearish Trade Opportunities — only when any asset is P-BEAR CONFIRMED or above
        _confirmed_trades = []
        for _asset, _sig in _pbear_sigs.items():
            _trade = _sig.bearish_trade_spec()
            if _trade:
                _confirmed_trades.append(_trade)

        if _confirmed_trades:
            posture_section += "\n**⚠️ Bearish Trade Opportunities (P-BEAR CONFIRMED)**\n"
            for _t in _confirmed_trades:
                posture_section += (
                    f"• **{_t['asset']}** [{_t['pbear_state']}]: {_t['instrument']} "
                    f"{_t['duration_dte']} DTE | {_t['structure']}\n"
                    f"  Max notional: {_t['max_notional_pct']:.0%} | {_t['notes']}\n"
                )

        # Expression 3 status
        _e3_bearish_phases = {'Speculation', 'Turbulence'}
        _mnav_ok   = _mnav > 2.0
        _pbear_ok  = 'MSTR' in (dp.forming_assets + dp.confirmed_assets)
        _howell_ok = _howell_phase in _e3_bearish_phases
        _e3_count  = sum([_mnav_ok, _pbear_ok, _howell_ok])
        _e3_levels = {4: '🚨 ARMED', 3: '🟠 SETUP', 2: '👁 WATCH', 1: '⚪ INACTIVE', 0: '⚪ INACTIVE'}
        _e3_label  = _e3_levels.get(_e3_count, '⚪ INACTIVE')
        posture_section += (f"\n**Expression 3:** {_e3_label} ({_e3_count}/4 conditions) | "
                            f"mNAV={_mnav:.2f}x [threshold: 2.0x]")

        sections.append(posture_section)

    except Exception as _dp_err:
        sections.append(f"**🛡️ Portfolio Posture**\n*Unavailable: {type(_dp_err).__name__}: {str(_dp_err)[:120]}*")

    # ============================================
    # 9. BOTTOM LINE
    # ============================================
    if sri and gli:
        _sc = {k: v for k, v in json.loads(sri[14]).items() if k.isdigit()} if sri[14] else {}
        stage_str = f"Stage {max(_sc, key=_sc.get)}" if _sc else "?"
        zscore = gli[2]
        
        # Get mNAV for bottom line
        mnav_bl = conn.execute("SELECT mnav_ratio FROM mnav ORDER BY date DESC LIMIT 1").fetchone()
        mnav_v = mnav_bl[0] if mnav_bl else None
        mnav_z_bl = ((mnav_v - 1.596) / 0.412) if mnav_v else None

        section = "**💡 Bottom Line**\n"

        if "4" in stage_str:
            if sri[8] and sri[8] > 0:
                section += "Stage 4 decline is decelerating — watch for 4→1 transition signals. "
                section += "Not there yet: need volume capitulation (>2.5x ADV) and MVRV recovery toward 1.0. "
            else:
                section += "Stage 4 downtrend intact. No transition signals. "

            if zscore < -0.5:
                section += "GLI contractionary adds macro headwind. "
            
            if mnav_z_bl is not None and mnav_z_bl < -1:
                section += f"\n\n🔑 **mNAV at {mnav_v:.3f}x (Z={mnav_z_bl:.2f}) — deep discount.** "
                section += f"Mean reversion to 1.6x = +{((1.596/mnav_v)-1)*100:.0f}% upside in MSTR relative to BTC. "
                section += "Accumulate shares. Sell puts into fear. "

            section += "\n\n**Posture: Accumulate on weakness. Sell premium aggressively at these IV levels.**"

        elif "1" in stage_str:
            section += "Stage 1 accumulation. Early bullish but unconfirmed. "
            if mnav_z_bl is not None and mnav_z_bl < -0.5:
                section += f"mNAV at discount ({mnav_v:.3f}x) — favors aggressive LEAP deployment. "
            section += "**Posture: Buy shares + LEAPs. Selective bull put spreads with wide margins.**"

        elif "2" in stage_str:
            section += "Stage 2 markup. Trend is your friend. "
            if mnav_z_bl is not None and mnav_z_bl > 1:
                section += f"mNAV premium expanding ({mnav_v:.3f}x) — start selling calls. "
            section += "**Posture: Hold shares, sell puts at support, covered calls for income.**"

        elif "3" in stage_str:
            section += "Stage 3 distribution. Topping signals present. "
            if mnav_z_bl is not None and mnav_z_bl > 1.5:
                section += f"mNAV at extreme premium ({mnav_v:.3f}x) — aggressively reduce. "
            section += "**Posture: Sell calls at resistance, reduce shares, buy protection.**"

        sections.append(section)

    conn.close()
    return sections


def main():
    start = time.time()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"=== Morning Brief — {today} ===\n")

    sections = build_brief()

    # Print to console
    for s in sections:
        print(s)
        print()

    # Save to file
    os.makedirs(BRIEFS_DIR, exist_ok=True)
    brief_path = os.path.join(BRIEFS_DIR, f"morning_{today}.md")
    with open(brief_path, "w") as f:
        f.write(f"# Morning Brief — {today}\n\n")
        for s in sections:
            f.write(s + "\n\n---\n\n")
    print(f"Brief saved to {brief_path}")

    # Send to Discord
    title = f"☀️ Morning Brief — {today}"
    ok = send_long_brief(title, sections, "blue")
    print(f"Discord: {'✓ Sent' if ok else '✗ Failed'}")

    elapsed = int((time.time() - start) * 1000)
    print(f"Duration: {elapsed}ms")

    # Log
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO debug_log (timestamp, script_name, level, message, duration_ms)
           VALUES (?, 'morning_brief', 'INFO', ?, ?)""",
        (datetime.now(timezone.utc).isoformat(), f"Brief generated: {len(sections)} sections", elapsed),
    )
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO cron_state (script_name, last_success, last_attempt,
           consecutive_failures, last_error)
           VALUES ('morning_brief', ?, ?, 0, NULL)
           ON CONFLICT(script_name) DO UPDATE SET
           last_success=?, last_attempt=?, consecutive_failures=0, last_error=NULL""",
        (now, now, now, now),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
