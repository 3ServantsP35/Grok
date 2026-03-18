#!/usr/bin/env python3
"""
MSTR Chart Suite — Weekly Report Generator
Reads 5 CSV files from /mnt/mstr-data/, analyzes signal ladders,
computes composite score, and posts a structured report to Discord.

Usage:
  python3 mstr_suite_report.py          # generate and post report
  python3 mstr_suite_report.py report   # same as above
  python3 mstr_suite_report.py reminder # send CSV update reminder

Set DRY_RUN = True to print to stdout instead of posting to Discord.
"""

import sys
import os
import glob
import traceback
from datetime import datetime, timezone, timedelta
from typing import Optional, Set

import pandas as pd
import requests
from trend_line_engine import TrendLineEngine
try:
    from dotenv import load_dotenv
except ImportError:
    # Fallback: parse .env manually if python-dotenv not installed
    def load_dotenv(path):
        try:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
        except Exception:
            pass

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

DRY_RUN = False  # Set True for local testing (suppresses Discord post)

ENV_PATHS = ["/mnt/mstr-config/.env", "/Users/vera/mstr-engine/config/.env"]
DATA_DIR   = "/mnt/mstr-data"
SCRIPTS_DIR = "/mnt/mstr-scripts"
LOCAL_REPO_DIR = "/Users/vera/.openclaw-mstr/workspace-mstr-cio/Grok"

SUITE_PATTERNS = {
    "MSTR_LT":   [f"{DATA_DIR}/BATS_MSTR, 240_*.csv", f"{LOCAL_REPO_DIR}/BATS_MSTR, 240_*.csv"],
    "STRC_LT":   [f"{DATA_DIR}/BATS_STRC, 240_*.csv", f"{LOCAL_REPO_DIR}/BATS_STRC, 240_*.csv"],
    "STAB_DOM":  [f"{DATA_DIR}/CRYPTOCAP_STABLE.C.D, 240_*.csv", f"{LOCAL_REPO_DIR}/CRYPTOCAP_STABLE.C.D, 240_*.csv"],
    "STRF_LQD":  [f"{DATA_DIR}/BATS_STRF_BATS_LQD, 240_*.csv", f"{LOCAL_REPO_DIR}/BATS_STRF_BATS_LQD, 240_*.csv"],
    "MSTR_IBIT": [f"{DATA_DIR}/BATS_MSTR_BATS_IBIT, 240_*.csv", f"{LOCAL_REPO_DIR}/BATS_MSTR_BATS_IBIT, 240_*.csv"],
}

MAX_DISCORD_LEN = 1900  # safe Discord message length


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def load_env():
    """Load .env and return dict of DISCORD webhook URLs."""
    for env_path in ENV_PATHS:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            break
    webhooks = {}
    for key in ("DISCORD_WEBHOOK_GAVIN", "DISCORD_WEBHOOK_GREG",
                "DISCORD_WEBHOOK_GARY", "DISCORD_WEBHOOK_CIO"):
        val = os.environ.get(key)
        if val:
            webhooks[key] = val
    return webhooks


def resolve_csv_path(key: str):
    """Resolve newest matching CSV from mounted data dir or local repo fallback."""
    patterns = SUITE_PATTERNS[key]
    matches = []
    for pat in patterns:
        matches.extend(glob.glob(pat))
    if not matches:
        return None
    matches = sorted(matches, key=lambda x: os.path.getmtime(x), reverse=True)
    return matches[0]


def load_csv(key: str):
    """Load and clean a suite CSV. Returns None on failure."""
    path = resolve_csv_path(key)
    try:
        if not path:
            raise FileNotFoundError(f"no matches for {key}")
        df = pd.read_csv(path, low_memory=False)
        # Drop repeated header rows (TradingView exports sometimes embed headers)
        df = df[df["time"] != "time"].reset_index(drop=True)
        df = df.apply(pd.to_numeric, errors="coerce")
        if len(df) < 6:
            print(f"[WARN] {key}: only {len(df)} rows after cleaning — too few for slope")
            return None
        return df
    except FileNotFoundError:
        print(f"[ERROR] {key}: file not found → {path}")
        return None
    except Exception as e:
        print(f"[ERROR] {key}: {e}")
        return None


def slope5(series: pd.Series) -> float:
    """Compute 5-bar slope: (last - 5th-from-last) / 5."""
    s = series.dropna()
    if len(s) < 6:
        return 0.0
    return (float(s.iloc[-1]) - float(s.iloc[-6])) / 5


def last(series: pd.Series, default=float("nan")) -> float:
    """Return last non-NaN value of a series."""
    s = series.dropna()
    return float(s.iloc[-1]) if len(s) > 0 else default


def fmt_score_bar(score: float, max_score: float = 5.0) -> str:
    """Return a filled bar like [████░░] scaled to max_score."""
    filled = round(score * 8 / max_score)
    bar = "█" * filled + "░" * (8 - filled)
    return f"[{bar}]"


def send_discord(webhooks: dict, message: str,
                 summary_only_keys: Optional[Set[str]] = None):
    """
    Post message to all webhooks.
    summary_only_keys: if set, those webhooks get only the first line (summary).
    Splits messages > MAX_DISCORD_LEN automatically.
    """
    if DRY_RUN:
        print("=" * 60)
        print("[DRY RUN — would post to Discord]")
        print(message)
        print("=" * 60)
        return

    chunks = split_message(message)

    for key, url in webhooks.items():
        try:
            if summary_only_keys and key in summary_only_keys:
                # Just send the first line as a summary
                summary_line = message.split("\n")[0]
                r = requests.post(url, json={"content": summary_line}, timeout=10)
                r.raise_for_status()
                print(f"[INFO] Summary sent to {key}")
            else:
                for i, chunk in enumerate(chunks):
                    r = requests.post(url, json={"content": chunk}, timeout=10)
                    r.raise_for_status()
                print(f"[INFO] Report sent to {key} ({len(chunks)} chunk(s))")
        except Exception as e:
            print(f"[ERROR] Failed to post to {key}: {e}")


def split_message(text: str) -> list[str]:
    """Split text into chunks ≤ MAX_DISCORD_LEN, breaking on newlines."""
    if len(text) <= MAX_DISCORD_LEN:
        return [text]
    chunks = []
    current = ""
    for line in text.split("\n"):
        candidate = current + "\n" + line if current else line
        if len(candidate) > MAX_DISCORD_LEN:
            if current:
                chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def et_now() -> datetime:
    """Return current US/Eastern time (handles EST/EDT automatically)."""
    utc_now = datetime.now(timezone.utc)
    # EST = UTC-5, EDT = UTC-4 (rough; no pytz required)
    # Use fixed EST for consistency; cron runs Friday 4:30 PM ET
    et = utc_now - timedelta(hours=5)
    return et


# ─────────────────────────────────────────────────────────────────────────────
# CHART ANALYZERS
# ─────────────────────────────────────────────────────────────────────────────

def analyze_mstr_lt(df: pd.DataFrame) -> dict:
    """Chart 1 — MSTR SRI LT with better structural classification."""
    try:
        price     = last(df["close"])
        lt_fast   = last(df["LT Fast Trackline"])
        lt_slow   = last(df["LT Slow Trackline"])
        vlt_fast  = last(df["VLT Fast Trackline"])
        vlt_slow  = last(df["VLT Slow Trackline"])
        lt_bias   = last(df["LT SRI Bias Histogram"])
        vlt_bias  = last(df["VLT SRI Bias Histogram"])
        st_bias   = last(df["ST SRI Bias Histogram"]) if "ST SRI Bias Histogram" in df.columns else float("nan")
        loi       = last(df["LOI"])

        lt_fast_slope = slope5(df["LT Fast Trackline"])
        lt_slow_slope = slope5(df["LT Slow Trackline"])
        vlt_fast_slope = slope5(df["VLT Fast Trackline"])

        above_lt_fast = price > lt_fast
        above_lt_slow = price > lt_slow
        above_vlt_fast = price > vlt_fast

        # Structural classification hierarchy
        if lt_bias > 0 and vlt_bias > 0 and above_vlt_fast and lt_fast_slope >= 0:
            status = "🟢 BULLISH"
            score = 1
        elif lt_bias > 0 and above_vlt_fast:
            status = "🟡 RECOVERING"
            score = 0.5
        elif lt_bias > 0 and vlt_bias <= 0:
            status = "🟡 MIXED"
            score = 0.5
        elif lt_bias <= 0 and vlt_bias <= 0 and not above_vlt_fast:
            status = "🔴 BEARISH"
            score = 0
        else:
            status = "🟡 TRANSITIONAL"
            score = 0.5

        if lt_bias > 0 and vlt_bias > 0:
            backdrop = "bullish structure active"
        elif lt_bias > 0 and vlt_bias <= 0:
            backdrop = "LT improved, VLT headwind still present"
        elif lt_bias <= 0 and vlt_bias > 0:
            backdrop = "VLT support intact, LT weakening"
        else:
            backdrop = "structural headwind active"

        level_note = (
            f"Price {'above' if above_vlt_fast else 'below'} VLT Fast TL | "
            f"LT slope {lt_fast_slope:+.2f}/bar | "
            f"LT Hist {lt_bias:+.0f} / VLT Hist {vlt_bias:+.0f}"
        )
        narrative = f"{backdrop} | {level_note}"

        return {
            "status": status,
            "score": score,
            "price": price,
            "lt_fast": lt_fast,
            "lt_slow": lt_slow,
            "vlt_fast": vlt_fast,
            "vlt_slow": vlt_slow,
            "lt_bias": lt_bias,
            "vlt_bias": vlt_bias,
            "st_bias": st_bias,
            "loi": loi,
            "lt_fast_slope": lt_fast_slope,
            "lt_slow_slope": lt_slow_slope,
            "vlt_fast_slope": vlt_fast_slope,
            "above_lt_fast": above_lt_fast,
            "above_lt_slow": above_lt_slow,
            "above_vlt_fast": above_vlt_fast,
            "narrative": narrative,
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_mstr_lt: {e}")
        return {"status": "⬜ DATA UNAVAILABLE", "score": 0, "error": str(e)}


def analyze_strc_lt(df: pd.DataFrame) -> dict:
    """Chart 2 — STRC SRI LT"""
    try:
        strc_price = last(df["close"])
        fast_tl    = last(df["ST Fast Trackline"]) if "ST Fast Trackline" in df.columns else last(df["Fast Trackline"])
        slow_tl    = last(df["ST Slow Trackline"]) if "ST Slow Trackline" in df.columns else last(df["Slow Trackline"])
        histogram  = last(df["ST SRI Bias Histogram"]) if "ST SRI Bias Histogram" in df.columns else last(df["SRI Bias Histogram"])
        gap        = fast_tl - slow_tl
        fast_slope = slope5(df["ST Fast Trackline"]) if "ST Fast Trackline" in df.columns else slope5(df["Fast Trackline"])

        # Stress classification
        if strc_price < 97 and fast_tl < slow_tl:
            status = "🔴 STRESS CONFIRMED"
            score  = 0
        elif 97 <= strc_price <= 99 and fast_slope < 0:
            status = "🟡 STRESS FORMING"
            score  = 0
        elif strc_price > 99 and fast_tl > slow_tl and histogram > 0:
            status = "🟢 NO STRESS"
            score  = 1
        else:
            status = "🟡 NEUTRAL"
            score  = 0

        narrative = (
            f"STRC {'above' if strc_price > 99 else 'below'} $99 par | "
            f"Fast TL {'>' if fast_tl > slow_tl else '<'} Slow TL | "
            f"slope {fast_slope:+.4f}/bar"
        )

        return {
            "status": status,
            "score":  score,
            "strc_price": strc_price,
            "fast_tl": fast_tl,
            "slow_tl": slow_tl,
            "gap":     gap,
            "histogram": histogram,
            "fast_slope": fast_slope,
            "narrative": narrative,
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_strc_lt: {e}")
        return {"status": "⬜ DATA UNAVAILABLE", "score": 0, "error": str(e)}


def analyze_stab_dom(df: pd.DataFrame) -> dict:
    """Chart 3 — Stablecoin Dominance SRI LT"""
    try:
        stab_price    = last(df["close"])
        lt_fast       = last(df["LT Fast Trackline"])
        lt_slow       = last(df["LT Slow Trackline"])
        lt_hist       = last(df["LT SRI Bias Histogram"])
        lt_fast_slope = slope5(df["LT Fast Trackline"])
        lt_hist_slope = slope5(df["LT SRI Bias Histogram"])

        # Signal from MSTR perspective (falling stab dom = bullish for MSTR)
        if lt_hist < 0 and lt_fast_slope < 0:
            status = "🟢 BULLISH"
            score  = 1
        elif stab_price < lt_fast and lt_fast_slope < 0:
            status = "🟢 CONFIRMING"
            score  = 1
        elif stab_price < lt_fast and lt_hist_slope < 0:
            status = "🟡 EARLY WARNING"
            score  = 0
        elif lt_hist > 20 and lt_fast_slope > 0:
            status = "🔴 BEARISH (crypto capital flight)"
            score  = 0
        else:
            status = "🟡 NEUTRAL"
            score  = 0

        direction = "declining" if lt_fast_slope < 0 else "rising"
        narrative = (
            f"Stab dom {direction} at LT level | "
            f"Dom {'<' if stab_price < lt_fast else '>'} Fast TL | "
            f"LT hist slope {lt_hist_slope:+.1f}/bar"
        )

        return {
            "status": status,
            "score":  score,
            "stab_price": stab_price,
            "lt_fast": lt_fast,
            "lt_slow": lt_slow,
            "lt_hist": lt_hist,
            "lt_fast_slope": lt_fast_slope,
            "lt_hist_slope": lt_hist_slope,
            "narrative": narrative,
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_stab_dom: {e}")
        return {"status": "⬜ DATA UNAVAILABLE", "score": 0, "error": str(e)}


def analyze_strf_lqd(df: pd.DataFrame) -> dict:
    """Chart 4 — STRF/LQD SRI LT"""
    try:
        ratio       = last(df["close"])
        fast_tl     = last(df["ST Fast Trackline"])
        slow_tl     = last(df["ST Slow Trackline"])
        loi         = last(df["LOI"])
        ratio_slope = slope5(df["close"])
        fast_slope  = slope5(df["ST Fast Trackline"])

        # Signal status
        if ratio > 1.0 and fast_tl > slow_tl and fast_slope > 0:
            status = "🟢 STRONG"
            score  = 1.0
        elif ratio < 1.0 and fast_tl > slow_tl and fast_slope > 0:
            status = "🟢 RECOVERING"
            score  = 0.5
        elif fast_tl < slow_tl or ratio_slope < -0.001:
            status = "🔴 STRESS"
            score  = 0
        elif fast_tl > slow_tl and ratio < 1.0:
            status = "🟡 NEUTRAL"
            score  = 0
        else:
            status = "🟡 NEUTRAL"
            score  = 0

        above_below = "ABOVE 1.0 (crypto premium)" if ratio > 1.0 else "BELOW 1.0 (residual stress)"
        score_display = "1" if score == 1.0 else ("½" if score == 0.5 else "0")

        narrative = (
            f"Ratio {above_below} | "
            f"Fast TL {'>' if fast_tl > slow_tl else '<'} Slow TL | "
            f"slope {fast_slope:+.5f}/bar"
        )

        return {
            "status": status,
            "score":  score,
            "score_display": score_display,
            "ratio":  ratio,
            "fast_tl": fast_tl,
            "slow_tl": slow_tl,
            "loi":    loi,
            "ratio_slope": ratio_slope,
            "fast_slope":  fast_slope,
            "above_below": above_below,
            "narrative": narrative,
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_strf_lqd: {e}")
        return {"status": "⬜ DATA UNAVAILABLE", "score": 0,
                "score_display": "0", "error": str(e)}


def analyze_mstr_ibit(df: pd.DataFrame) -> dict:
    """Chart 5 — MSTR/IBIT SRI LT"""
    try:
        ratio    = last(df["close"])
        vlt_hist = last(df["VLT SRI Bias Histogram"])
        lt_hist  = last(df["LT SRI Bias Histogram"])
        st_hist  = last(df["ST SRI Bias Histogram"])
        vst_hist = last(df["VST SRI Bias Histogram"]) if "VST SRI Bias Histogram" in df.columns else last(df["ST SRI Bias Histogram"])

        lt_slow_tl  = last(df["LT Slow Trackline"])
        vlt_slow_tl = last(df["VLT Slow Trackline"])

        hists = [vlt_hist, lt_hist, st_hist, vst_hist]
        tf_positive_count = sum(1 for h in hists if h > 0)

        # 5-bar trend check
        hists_5ago = [
            last(df["VLT SRI Bias Histogram"].iloc[:-5]) if len(df) >= 6 else vlt_hist,
            last(df["LT SRI Bias Histogram"].iloc[:-5])  if len(df) >= 6 else lt_hist,
            last(df["ST SRI Bias Histogram"].iloc[:-5])  if len(df) >= 6 else st_hist,
            (last(df["VST SRI Bias Histogram"].iloc[:-5]) if "VST SRI Bias Histogram" in df.columns else last(df["ST SRI Bias Histogram"].iloc[:-5])) if len(df) >= 6 else vst_hist,
        ]
        all_rising = all(h > h5 for h, h5 in zip(hists, hists_5ago))
        trending_up = lt_hist > hists_5ago[1] and st_hist > hists_5ago[2]

        if tf_positive_count >= 3:
            status = "🟢 ALPHA CYCLE"
            score  = 1
        elif lt_hist > 0 and st_hist > 0 and trending_up:
            status = "🟢 MOMENTUM"
            score  = 1
        elif lt_hist < 0 and vlt_hist < 0:
            status = "🔴 UNDERPERFORM (lagging BTC — potential entry or warning)"
            score  = 0
        else:
            status = "🟡 NEUTRAL"
            score  = 0

        tf_bar = f"VLT{vlt_hist:+.0f} LT{lt_hist:+.0f} ST{st_hist:+.0f} VST{vst_hist:+.0f}"
        narrative = (
            f"{tf_positive_count}/4 TFs positive | "
            f"{'All TFs rising' if all_rising else 'Mixed TF trend'} | "
            f"LT Slow TL: {lt_slow_tl:.4f}"
        )

        return {
            "status": status,
            "score":  score,
            "ratio":  ratio,
            "vlt_hist": vlt_hist,
            "lt_hist":  lt_hist,
            "st_hist":  st_hist,
            "vst_hist": vst_hist,
            "tf_positive_count": tf_positive_count,
            "all_rising": all_rising,
            "lt_slow_tl": lt_slow_tl,
            "vlt_slow_tl": vlt_slow_tl,
            "tf_bar": tf_bar,
            "narrative": narrative,
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_mstr_ibit: {e}")
        return {"status": "⬜ DATA UNAVAILABLE", "score": 0, "error": str(e)}




def analyze_st_progression(df: pd.DataFrame) -> dict:
    """ST companion view + ST/LT slow-trackline progression layer."""
    try:
        def get_optional(col, default=float("nan")):
            return last(df[col], default) if col in df.columns else default

        st_fast = get_optional("ST Fast Trackline")
        st_slow = get_optional("ST Slow Trackline")
        lt_fast = get_optional("LT Fast Trackline")
        lt_slow = get_optional("LT Slow Trackline")
        st_hist = get_optional("ST SRI Bias Histogram")
        lt_hist = get_optional("LT SRI Bias Histogram")
        vst_hist = get_optional("VST SRI Bias Histogram")
        vlt_hist = get_optional("VLT SRI Bias Histogram")

        st_slow_slope = slope5(df["ST Slow Trackline"]) if "ST Slow Trackline" in df.columns else 0.0
        lt_slow_slope = slope5(df["LT Slow Trackline"]) if "LT Slow Trackline" in df.columns else 0.0

        if pd.isna(st_slow) or pd.isna(lt_slow):
            return {
                "state": "⬜ DATA UNAVAILABLE",
                "cross_state": "unknown",
                "error": "missing ST/LT slow tracklines",
            }

        spread = st_slow - lt_slow
        prev_st = last(df["ST Slow Trackline"].iloc[:-1]) if "ST Slow Trackline" in df.columns and len(df) >= 2 else st_slow
        prev_lt = last(df["LT Slow Trackline"].iloc[:-1]) if "LT Slow Trackline" in df.columns and len(df) >= 2 else lt_slow
        prev_spread = prev_st - prev_lt

        if spread > 0 and prev_spread <= 0:
            cross_state = "fresh bullish cross"
        elif spread < 0 and prev_spread >= 0:
            cross_state = "fresh bearish cross"
        elif spread > 0:
            cross_state = "ST above LT"
        elif spread < 0:
            cross_state = "ST below LT"
        else:
            cross_state = "at crossover"

        if spread > 0 and st_slow_slope > 0 and lt_slow_slope > 0:
            state = "🟢 progression confirmed"
        elif spread > 0 and st_slow_slope > 0:
            state = "🟡 early bullish progression"
        elif spread < 0 and st_slow_slope < 0 and lt_slow_slope < 0:
            state = "🔴 bearish progression"
        elif spread < 0 and st_slow_slope > 0:
            state = "🟡 repair / bottoming progression"
        else:
            state = "🟡 transitional"

        narrative = (
            f"{cross_state} | ST slow slope {st_slow_slope:+.3f}/bar | "
            f"LT slow slope {lt_slow_slope:+.3f}/bar | "
            f"ST hist {st_hist:+.0f} LT hist {lt_hist:+.0f}"
        )

        return {
            "state": state,
            "cross_state": cross_state,
            "spread": spread,
            "st_slow": st_slow,
            "lt_slow": lt_slow,
            "st_slow_slope": st_slow_slope,
            "lt_slow_slope": lt_slow_slope,
            "st_hist": st_hist,
            "lt_hist": lt_hist,
            "vst_hist": vst_hist,
            "vlt_hist": vlt_hist,
            "narrative": narrative,
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_st_progression: {e}")
        return {"state": "⬜ DATA UNAVAILABLE", "cross_state": "unknown", "error": str(e)}


def analyze_force_state(df: pd.DataFrame) -> dict:
    """Force Field + FF ROC layer from MSTR CSV exports."""
    try:
        f_net = last(df["F_net"])

        def get_optional(col, default=float("nan")):
            return last(df[col], default) if col in df.columns else default

        roc1 = get_optional("F_net ROC 1")
        roc3 = get_optional("F_net ROC 3")
        roc5 = get_optional("F_net ROC 5")
        accel = get_optional("F_net Acceleration")

        # Fallbacks for older CSV schemas
        if pd.isna(roc1):
            roc1 = f_net - last(df["F_net"].iloc[:-1]) if len(df) >= 2 else 0.0
        if pd.isna(roc3):
            roc3 = f_net - last(df["F_net"].iloc[:-3]) if len(df) >= 4 else roc1
        if pd.isna(roc5):
            roc5 = f_net - last(df["F_net"].iloc[:-5]) if len(df) >= 6 else roc3
        if pd.isna(accel):
            prev_roc1 = last(df["F_net ROC 1"].iloc[:-1]) if "F_net ROC 1" in df.columns and len(df) >= 2 else 0.0
            accel = roc1 - prev_roc1

        if f_net > -0.19:
            zone = "STRONG BULL"
        elif f_net > -0.60:
            zone = "MOD BULL"
        elif f_net > -1.15:
            zone = "NEUTRAL"
        elif f_net > -1.66:
            zone = "MOD BEAR"
        else:
            zone = "STRONG BEAR"

        if f_net > -0.60 and roc3 > 0 and accel > 0:
            state = "🟢 bullish and strengthening"
        elif f_net > -0.60 and roc3 <= 0:
            state = "🟡 bullish but decelerating"
        elif f_net <= -0.60 and roc3 > 0:
            state = "🟡 bearish but repairing"
        elif f_net <= -0.60 and roc3 <= 0:
            state = "🔴 bearish and worsening"
        else:
            state = "🟡 exhausted / rebuilding"

        if f_net > -0.60 and roc3 > 0:
            tactical = "Force supports continuation / breakout attempts"
        elif f_net > -0.60 and roc3 <= 0:
            tactical = "Force still positive, but reset / consolidation risk elevated"
        elif f_net <= -0.60 and roc3 > 0:
            tactical = "Repairing force — watch for stabilization before directional confidence improves"
        else:
            tactical = "Force deterioration active — defensive posture favored"

        return {
            "zone": zone,
            "state": state,
            "f_net": f_net,
            "roc1": roc1,
            "roc3": roc3,
            "roc5": roc5,
            "accel": accel,
            "tactical": tactical,
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_force_state: {e}")
        return {"zone": "UNKNOWN", "state": "⬜ DATA UNAVAILABLE", "error": str(e)}



def analyze_trend_geometry(df: pd.DataFrame, asset: str = "MSTR") -> dict:
    """Trend-line geometry layer via P10 Trend Line Engine."""
    try:
        eng = TrendLineEngine()
        result = eng.analyze(df.copy(), asset)

        def pick_first(lines):
            return lines[0] if lines else None

        local_res = pick_first(result.near_resistance)
        global_res = result.near_resistance[1] if len(result.near_resistance) > 1 else None
        local_sup = pick_first(result.near_support)
        global_sup = result.near_support[1] if len(result.near_support) > 1 else None

        return {
            "current_price": result.current_price,
            "local_resistance": local_res.proj_now if local_res else float("nan"),
            "global_resistance": global_res.proj_now if global_res else float("nan"),
            "local_support": local_sup.proj_now if local_sup else float("nan"),
            "global_support": global_sup.proj_now if global_sup else float("nan"),
            "distance_to_local_resistance_pct": abs(local_res.distance_pct) if local_res else float("nan"),
            "distance_to_global_resistance_pct": abs(global_res.distance_pct) if global_res else float("nan"),
            "distance_to_local_support_pct": abs(local_sup.distance_pct) if local_sup else float("nan"),
            "distance_to_global_support_pct": abs(global_sup.distance_pct) if global_sup else float("nan"),
            "local_res_label": local_res.label if local_res else "n/a",
            "global_res_label": global_res.label if global_res else "n/a",
            "local_sup_label": local_sup.label if local_sup else "n/a",
            "global_sup_label": global_sup.label if global_sup else "n/a",
            "brief": result.to_brief_str(max_resistance=4, max_support=4),
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] analyze_trend_geometry: {e}")
        return {"brief": "Trend geometry unavailable", "error": str(e)}



def build_scenarios(r1: dict, ff: dict, st_prog: dict, trend: dict) -> list[dict]:
    """Build high-level 2–8 week path scenarios from force + progression + geometry."""
    scenarios = []

    price = r1.get("price", float("nan"))
    local_r = trend.get("local_resistance", float("nan"))
    local_s = trend.get("local_support", float("nan"))
    force_bull = ff.get("f_net", -999) > -0.60
    roc3 = ff.get("roc3", 0.0)
    accel = ff.get("accel", 0.0)
    st_state = st_prog.get("state", "")

    breakout_prob = 15
    shallow_reset_prob = 35
    deeper_reset_prob = 20
    failure_prob = 10

    # force state
    if force_bull and roc3 > 0 and accel > 0:
        breakout_prob += 15
        shallow_reset_prob -= 5
    elif force_bull and roc3 <= 0:
        shallow_reset_prob += 15
        deeper_reset_prob += 5
    elif not force_bull and roc3 > 0:
        deeper_reset_prob += 10
    else:
        failure_prob += 15
        deeper_reset_prob += 10

    # ST progression
    if "progression confirmed" in st_state:
        breakout_prob += 10
    elif "early bullish progression" in st_state:
        breakout_prob += 5
        shallow_reset_prob += 5
    elif "repair / bottoming" in st_state:
        deeper_reset_prob += 10
    elif "bearish progression" in st_state:
        failure_prob += 10
        deeper_reset_prob += 10

    # geometry proximity
    if price == price and local_r == local_r and price >= 0.97 * local_r:
        shallow_reset_prob += 10
        if roc3 > 0:
            breakout_prob += 5
        else:
            breakout_prob -= 5
    if price == price and local_s == local_s and price <= 1.03 * local_s and roc3 > 0:
        breakout_prob += 5

    probs = {
        "Immediate breakout continuation": breakout_prob,
        "Shallow reset then breakout": shallow_reset_prob,
        "Deeper 1B reset": deeper_reset_prob,
        "Bearish structure failure": failure_prob,
    }
    total = sum(max(v, 1) for v in probs.values())
    for name, raw in probs.items():
        prob = round(max(raw, 1) * 100 / total)
        scenarios.append({"name": name, "probability": prob})

    scenarios.sort(key=lambda x: x["probability"], reverse=True)
    return scenarios


def translate_to_buckets(scenarios: list[dict], ff: dict, st_prog: dict) -> dict:
    """Translate scenarios into bucket-level strategic posture only."""
    top = scenarios[0]["name"] if scenarios else "Unknown"
    force_bull = ff.get("f_net", -999) > -0.60
    roc3 = ff.get("roc3", 0.0)

    if top == "Immediate breakout continuation":
        ab3 = "Hold / selective add on confirmation"
        ab2 = "Bullish directional edge"
        ab1 = "Avoid capping upside too early"
        ab4 = "Do not over-raise cash"
    elif top == "Shallow reset then breakout":
        ab3 = "Wait for better structural add zone"
        ab2 = "Directional reversal setup likely after rejection confirms"
        ab1 = "Theta window improving if upside becomes capped"
        ab4 = "Preserve staging capital for reset"
    elif top == "Deeper 1B reset":
        ab3 = "Patience — wait for deeper accumulation zone"
        ab2 = "Bearish directional edge on failed support"
        ab1 = "Near-term call-selling more favorable than chasing longs"
        ab4 = "Raise / preserve cash for redeploy"
    else:
        ab3 = "De-risk / avoid new deployment"
        ab2 = "Bearish directional posture favored"
        ab1 = "Only conservative theta if structure stabilizes"
        ab4 = "Preserve cash defensively"

    return {"AB3": ab3, "AB2": ab2, "AB1": ab1, "AB4": ab4}

# ─────────────────────────────────────────────────────────────────────────────
# ACTION ITEMS
# ─────────────────────────────────────────────────────────────────────────────

def generate_action_items(r1: dict, r2: dict, r3: dict, r4: dict, r5: dict) -> str:
    items = []

    # VLT histogram near zero
    if r1.get("error") is None:
        vlt_bias = r1.get("vlt_bias", float("nan"))
        if -10 < vlt_bias < 10:
            items.append(
                "👁 Watch VLT Histogram flip — if turns positive, VLT headwind removed (major upgrade)"
            )

    # STRC fast slope declining
    if r2.get("error") is None and r2.get("fast_slope", 0) < 0:
        items.append(
            "⚠ Monitor STRC Fast TL direction — declining toward stress zone"
        )

    # Stablecoin dom LT histogram declining from elevated level
    if r3.get("error") is None:
        lt_hist = r3.get("lt_hist", 0)
        lt_hist_slope = r3.get("lt_hist_slope", 0)
        if lt_hist > 20 and lt_hist_slope < 0:
            items.append(
                "📉 Watch stablecoin dom LT histogram — rollover from elevated confirms capital deployment"
            )

    # STRF/LQD ratio near 1.0
    if r4.get("error") is None:
        ratio = r4.get("ratio", 0)
        if abs(ratio - 1.0) < 0.02:
            items.append(
                "🎯 STRF/LQD approaching 1.0 regime threshold — watch for breakout/breakdown"
            )

    # MSTR/IBIT all TFs positive and near LT Slow TL
    if r5.get("error") is None:
        tf_count = r5.get("tf_positive_count", 0)
        ratio5   = r5.get("ratio", 0)
        lt_slow5 = r5.get("lt_slow_tl", 0)
        if tf_count == 4 and lt_slow5 > 0 and abs(ratio5 - lt_slow5) < 0.1:
            items.append(
                "🔺 MSTR/IBIT approaching LT Slow TL resistance — watch for test of {lt_slow5:.4f}"
            )

    # Always include CSV reminder
    items.append(
        "📁 Update and push all 5 suite CSVs by 4:00 PM ET next Friday before the weekly report"
    )

    return "\n".join(f"  • {item}" for item in items)


# ─────────────────────────────────────────────────────────────────────────────
# REPORT BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def build_weekly_cost_section(week_data: dict, prev_week_data: dict) -> str:
    """Build weekly API cost section for Friday suite report (Task 11)."""
    if "error" in week_data or week_data.get("calls", 0) == 0:
        return "💰 **Weekly API Cost:** No automated API calls logged yet (delegation cycle not yet active)"

    w_cost = week_data.get("total_cost_usd", 0)
    w_calls = week_data.get("calls", 0)
    w_avg = w_cost / 7
    p_cost = prev_week_data.get("total_cost_usd", 0)
    trend = ""
    if p_cost > 0:
        pct_change = (w_cost - p_cost) / p_cost * 100
        trend = f" ({'↑' if pct_change > 0 else '↓'}{abs(pct_change):.0f}% vs prior week)"

    alert = ""
    if w_avg > 30:
        alert = f"\n  ⚠️ **COST ALERT: ${w_avg:.2f}/day exceeds $30 threshold**"

    # Top scripts
    top_scripts = week_data.get("by_script", [])[:5]
    script_lines = "\n".join(
        f"    {s['script']:<35} ${s['cost']:.3f}  ({s['calls']} calls)"
        for s in top_scripts
    ) if top_scripts else "    (no data)"

    # By model
    top_models = week_data.get("by_model", [])[:4]
    model_lines = "\n".join(
        f"    {m['model']:<35} ${m['cost']:.3f}  (in={m['input']:,} out={m['output']:,})"
        for m in top_models
    ) if top_models else "    (no data)"

    return (
        f"💰 **Weekly API Cost Report**{alert}\n"
        f"  This week: **${w_cost:.2f}** ({w_calls} calls){trend}\n"
        f"  Daily average: **${w_avg:.2f}/day**\n"
        f"  **Top scripts:**\n{script_lines}\n"
        f"  **By model:**\n{model_lines}"
    )


def build_report(r1: dict, r2: dict, r3: dict, r4: dict, r5: dict,
                 ff: dict, st_prog: dict, trend: dict,
                 scenarios: list[dict], buckets: dict,
                 cost_section: str = "") -> str:
    now = et_now()
    date_s = now.strftime("%A, %B %-d, %Y")

    def sg(d, key, default=float("nan")):
        return d.get(key, default)

    # legacy corroboration score remains as a secondary metric only
    corroboration = r1["score"] + r2["score"] + r3["score"] + r4["score"] + r5["score"]
    bar = fmt_score_bar(corroboration)

    structural_label = "🟢 structurally supportive" if corroboration >= 3.5 else (
        "🟡 mixed / transitional" if corroboration >= 2.0 else "🔴 structurally weak"
    )

    ff_summary = (
        f"**Force Field:** {ff.get('zone', 'UNKNOWN')} | {ff.get('state', 'n/a')} | "
        f"F_net {ff.get('f_net', float('nan')):.3f} | ROC1 {ff.get('roc1', float('nan')):+.3f} | "
        f"ROC3 {ff.get('roc3', float('nan')):+.3f} | ROC5 {ff.get('roc5', float('nan')):+.3f} | "
        f"Accel {ff.get('accel', float('nan')):+.3f}"
        if ff.get("error") is None else "**Force Field:** DATA UNAVAILABLE"
    )
    st_summary = (
        f"**ST Progression:** {st_prog.get('state', 'n/a')} | {st_prog.get('cross_state', 'unknown')} | "
        f"spread {st_prog.get('spread', float('nan')):+.3f} | "
        f"ST slope {st_prog.get('st_slow_slope', float('nan')):+.3f} | LT slope {st_prog.get('lt_slow_slope', float('nan')):+.3f}"
        if st_prog.get("error") is None else "**ST Progression:** DATA UNAVAILABLE"
    )
    trend_summary = (
        f"**Trend Geometry:** local R {trend.get('local_resistance', float('nan')):.2f} ({trend.get('local_res_label','n/a')}) | "
        f"global R {trend.get('global_resistance', float('nan')):.2f} ({trend.get('global_res_label','n/a')}) | "
        f"local S {trend.get('local_support', float('nan')):.2f} ({trend.get('local_sup_label','n/a')}) | "
        f"global S {trend.get('global_support', float('nan')):.2f} ({trend.get('global_sup_label','n/a')})"
        if trend.get("error") is None else "**Trend Geometry:** DATA UNAVAILABLE"
    )

    scenario_lines = "\n".join(
        f"  • {s['name']}: {s['probability']}%"
        for s in scenarios
    ) if scenarios else "  • unavailable"

    bucket_lines = (
        f"  • AB3: {buckets.get('AB3', 'n/a')}\n"
        f"  • AB2: {buckets.get('AB2', 'n/a')}\n"
        f"  • AB1: {buckets.get('AB1', 'n/a')}\n"
        f"  • AB4: {buckets.get('AB4', 'n/a')}"
    )

    # structural chart summaries
    ch1 = "① MSTR LT  ⬜ DATA UNAVAILABLE" if r1.get("error") else (
        f"① MSTR LT  {r1['status']} | Price ${sg(r1,'price'):.2f} | LT Hist {sg(r1,'lt_bias'):+.0f} | "
        f"VLT Hist {sg(r1,'vlt_bias'):+.0f} | LOI {sg(r1,'loi'):+.1f} | {r1['narrative']}"
    )
    ch2 = "② STRC LT  ⬜ DATA UNAVAILABLE" if r2.get("error") else (
        f"② STRC LT  {r2['status']} | Price ${sg(r2,'strc_price'):.2f} | Gap {sg(r2,'gap'):+.2f} | {r2['narrative']}"
    )
    ch3 = "③ Stablecoin Dom LT  ⬜ DATA UNAVAILABLE" if r3.get("error") else (
        f"③ Stablecoin Dom LT  {r3['status']} | Dom {sg(r3,'stab_price'):.2f}% | Hist {sg(r3,'lt_hist'):+.0f} | {r3['narrative']}"
    )
    ch4 = "④ STRF/LQD LT  ⬜ DATA UNAVAILABLE" if r4.get("error") else (
        f"④ STRF/LQD LT  {r4['status']} | Ratio {sg(r4,'ratio'):.4f} | LOI {sg(r4,'loi'):+.1f} | {r4['narrative']}"
    )
    ch5 = "⑤ MSTR/IBIT LT  ⬜ DATA UNAVAILABLE" if r5.get("error") else (
        f"⑤ MSTR/IBIT LT  {r5['status']} | Ratio {sg(r5,'ratio'):.4f} | TFs {sg(r5,'tf_bar','—')} | {r5['narrative']}"
    )

    top_scenario = scenarios[0]['name'] if scenarios else 'Unavailable'
    top_prob = scenarios[0]['probability'] if scenarios else 0
    sep = "══════════════════════════════"

    report = (
        f"📊 **MSTR CHART SUITE — Force-Aware Brief**\n"
        f"{date_s} | Market Close\n"
        f"\n{sep}\n"
        f"**PRIMARY PATH:** {top_scenario} ({top_prob}%)\n"
        f"**STRUCTURAL CORROBORATION:** {corroboration:.1f}/5 — {structural_label}\n"
        f"{bar}\n"
        f"{sep}\n\n"
        f"**1) Structural State**\n"
        f"{ch1}\n{ch2}\n{ch3}\n{ch4}\n{ch5}\n\n"
        f"**2) Force Diagnostics**\n"
        f"{ff_summary}\n"
        f"{st_summary}\n\n"
        f"**3) Trend Geometry**\n"
        f"{trend_summary}\n\n"
        f"**4) Scenario Probabilities**\n"
        f"{scenario_lines}\n\n"
        f"**5) CIO Conclusion**\n"
        f"  • Highest-probability path: {top_scenario}\n"
        f"  • Tactical force read: {ff.get('tactical', 'n/a')}\n"
        f"  • Structural progression read: {st_prog.get('state', 'n/a')}\n"
        f"\n**6) Bucket Strategy Translation**\n"
        f"{bucket_lines}\n"
        f"{sep}"
        + (f"\n\n{cost_section}" if cost_section else "")
    )
    return report


# ─────────────────────────────────────────────────────────────────────────────
# CSV REMINDER
# ─────────────────────────────────────────────────────────────────────────────

def send_csv_reminder():
    """Send the weekly CSV update reminder to all channels."""
    webhooks = load_env()
    if not webhooks:
        print("[ERROR] No Discord webhooks found in .env")
        return

    reminder = (
        "⏰ **MSTR Chart Suite — CSV Update Reminder**\n"
        "Market closes in ~30 minutes. Please export and push the following CSVs to GitHub before 4:30 PM ET:\n\n"
        "① MSTR on SRI LT (4H) → `BATS_MSTR, 240_*.csv`\n"
        "② STRC on SRI LT (4H) → `BATS_STRC, 240_*.csv`\n"
        "③ Stablecoin Dom on SRI LT (4H) → `CRYPTOCAP_STABLE.C.D, 240_*.csv`\n"
        "④ STRF/LQD on SRI LT (4H) → `BATS_STRF_BATS_LQD, 240_*.csv`\n"
        "⑤ MSTR/IBIT on SRI LT (4H) → `BATS_MSTR_BATS_IBIT, 240_*.csv`\n\n"
        "Weekly Suite Report will auto-generate at 4:30 PM ET."
    )

    print("[INFO] Sending CSV reminder...")
    send_discord(webhooks, reminder)
    print("[INFO] CSV reminder sent.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN REPORT RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def generate_suite_report():
    """Load CSVs, analyze, build report, post to Discord."""
    print("[INFO] MSTR Chart Suite — starting report generation")

    webhooks = load_env()
    if not webhooks:
        print("[ERROR] No Discord webhooks configured. Aborting.")
        return

    # Load all CSVs
    dfs = {}
    for key in SUITE_PATTERNS:
        dfs[key] = load_csv(key)

    # Check if all missing
    if all(v is None for v in dfs.values()):
        error_msg = (
            "🚨 **MSTR Chart Suite — REPORT FAILED**\n"
            "All 5 CSV files are missing or unreadable. Cannot generate report.\n"
            "Check /mnt/mstr-data/ and confirm CSVs were pushed to GitHub."
        )
        send_discord(webhooks, error_msg)
        print("[ERROR] All CSVs missing. Error message posted.")
        return

    # Analyze each chart
    unavailable = {"status": "⬜ DATA UNAVAILABLE", "score": 0,
                   "score_display": "0", "error": "CSV not loaded", "narrative": "—"}

    def safe_analyze(fn, df):
        if df is None:
            return dict(unavailable)
        try:
            return fn(df)
        except Exception as e:
            print(f"[ERROR] {fn.__name__}: {e}")
            traceback.print_exc()
            return dict(unavailable)

    r1 = safe_analyze(analyze_mstr_lt,   dfs["MSTR_LT"])
    r2 = safe_analyze(analyze_strc_lt,   dfs["STRC_LT"])
    r3 = safe_analyze(analyze_stab_dom,  dfs["STAB_DOM"])
    r4 = safe_analyze(analyze_strf_lqd,  dfs["STRF_LQD"])
    r5 = safe_analyze(analyze_mstr_ibit, dfs["MSTR_IBIT"])
    ff = safe_analyze(analyze_force_state, dfs["MSTR_LT"])
    st_prog = safe_analyze(analyze_st_progression, dfs["MSTR_LT"])
    trend = safe_analyze(lambda df: analyze_trend_geometry(df, "MSTR"), dfs["MSTR_LT"])
    scenarios = build_scenarios(r1, ff, st_prog, trend)
    buckets = translate_to_buckets(scenarios, ff, st_prog)

    # Print status summary
    total = r1["score"] + r2["score"] + r3["score"] + r4["score"] + r5["score"]
    print(f"[INFO] Scores: MSTR={r1['score']} STRC={r2['score']} "
          f"StabDom={r3['score']} STRF={r4['score']} IBIT={r5['score']} "
          f"TOTAL={total}")

    # Build weekly cost section (Task 11)
    cost_section = ""
    try:
        sys.path.insert(0, "/mnt/mstr-scripts")
        from api_utils import query_api_costs
        week_data = query_api_costs(days=7)
        prev_week_data = query_api_costs(days=14)
        # Subtract this week from 14d to get prior week
        prev_only = {
            "total_cost_usd": prev_week_data.get("total_cost_usd", 0) - week_data.get("total_cost_usd", 0),
            "calls": prev_week_data.get("calls", 0) - week_data.get("calls", 0),
        }
        cost_section = build_weekly_cost_section(week_data, prev_only)
    except Exception as e:
        cost_section = f"💰 **Weekly API Cost:** Error computing — {e}"

    # Build report
    report = build_report(r1, r2, r3, r4, r5, ff, st_prog, trend, scenarios, buckets, cost_section=cost_section)

    # Post — full report to Gavin/CIO, summary to Greg/Gary
    summary_keys = {"DISCORD_WEBHOOK_GREG", "DISCORD_WEBHOOK_GARY"}
    send_discord(webhooks, report, summary_only_keys=summary_keys)
    print("[INFO] Report generation complete.")

    # Print to stdout for cron log
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"

    if mode == "reminder":
        send_csv_reminder()
    else:
        generate_suite_report()
