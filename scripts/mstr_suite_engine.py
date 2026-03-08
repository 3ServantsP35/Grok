"""
mstr_suite_engine.py — P-MSTR-SUITE Magnetic Force Signal Engine
=================================================================
Computes a net directional force (F_net) from six instrument inputs
and classifies the current MSTR options trade environment.

Architecture (Rule 8 compliant — does NOT modify sri_engine.py):
  Layer 0.75: Force field above Layer 0 (GLI), below Layer 1 (Regime)
  Inputs: MSTR/IBIT, STRF/LQD, STRC, STABLE.D, MSTR (self), BTC (optional)
  Output: Signal zone, confidence tier, trade structure recommendation

Confidence Tiers:
  HIGH       — validated ≥70% WR at +10d (bearish zones, N≥29)
  PROVISIONAL — architecture confirmed, bull cycle validation pending
               (bullish zones; remove provisional tag when 6-month
               checkpoint confirms WR ≥70% on STRONG BULL)

6-Month Calibration Checkpoint:
  Target date: ~2026-09-08
  Action:      Re-run calibrate(forward_days=10) on STRONG BULL zone.
               If WR ≥ 70%, remove PROVISIONAL tag and go full sizing.
  Owner:       Project co-owner (see AGENTS.md)
"""

import os
import sys
import csv
import math
import json
import bisect
import sqlite3
import logging
import requests
from io import StringIO
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path("/mnt/mstr-scripts")
DATA_DIR    = Path("/mnt/mstr-data")
CONFIG_FILE = Path("/mnt/mstr-config/.env")
DB_PATH     = DATA_DIR / "mstr.db"
CSV_CACHE   = DATA_DIR / "suite_csv"

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [suite_engine] %(levelname)s %(message)s")
log = logging.getLogger("suite_engine")

# ── Load env ──────────────────────────────────────────────────────────────────
def load_env():
    env = {}
    for path in [CONFIG_FILE, DATA_DIR / ".env_tokens"]:
        if path.exists():
            for line in path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip().strip('"').strip("'")
    env.update(os.environ)
    return env

# ── GitHub CSV download ───────────────────────────────────────────────────────
GITHUB_REPO  = "3ServantsP35/Grok"
GITHUB_BRANCH = "main"

# Map: local name → GitHub filename (exact match in repo)
CSV_MAP = {
    "MSTR":      "BATS_MSTR, 240_8ee08.csv",
    "BTC":       "INDEX_BTCUSD, 240_29008.csv",
    "STABLE_D":  "CRYPTOCAP_STABLE.C.D, 240_cbdd5.csv",
    "STRC":      "BATS_STRC, 240_92d2f.csv",
    "STRF_LQD":  "BATS_STRF_BATS_LQD, 240_22e21.csv",
    "MSTR_IBIT": "BATS_MSTR_BATS_IBIT, 240_56652.csv",
}

def get_github_token(env: dict) -> Optional[str]:
    return env.get("GITHUB_TOKEN") or env.get("GH_TOKEN")

def list_repo_files(token: str) -> dict:
    """Returns {filename: download_url} for all CSV files in repo root."""
    headers = {"Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/{GITHUB_BRANCH}?recursive=1"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    tree = resp.json().get("tree", [])
    result = {}
    for item in tree:
        if item["path"].endswith(".csv"):
            fname = item["path"].split("/")[-1]
            result[fname] = item["url"]
    return result

def download_csv(token: str, filename: str, file_tree: dict) -> Optional[str]:
    """Download a CSV file by filename from repo. Returns content as string."""
    # Try exact match first
    if filename in file_tree:
        blob_url = file_tree[filename]
    else:
        # Fuzzy match on basename
        match = next((v for k, v in file_tree.items() if filename in k), None)
        if not match:
            log.warning(f"CSV not found in repo: {filename}")
            return None
        blob_url = match

    headers = {"Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3.raw"}
    # Blob API returns base64; use raw URL instead
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{filename}"
    resp = requests.get(raw_url, headers={"Authorization": f"token {token}"}, timeout=30)
    if resp.status_code == 200:
        return resp.text
    # Fallback: try with URL encoding
    from urllib.parse import quote
    raw_url2 = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{quote(filename)}"
    resp2 = requests.get(raw_url2, headers={"Authorization": f"token {token}"}, timeout=30)
    if resp2.status_code == 200:
        return resp2.text
    log.warning(f"Failed to download {filename}: HTTP {resp.status_code}")
    return None

def load_csvs(use_cache: bool = True, force_refresh: bool = False) -> dict:
    """
    Load all 6 suite CSVs. Returns {key: list_of_rows}.
    Tries cache first, falls back to GitHub download.
    """
    CSV_CACHE.mkdir(parents=True, exist_ok=True)
    env = load_env()
    token = get_github_token(env)
    result = {}
    file_tree = None

    for key, filename in CSV_MAP.items():
        cache_path = CSV_CACHE / f"{key}.csv"
        content = None

        # Try cache
        if use_cache and not force_refresh and cache_path.exists():
            age_hours = (datetime.now().timestamp() - cache_path.stat().st_mtime) / 3600
            if age_hours < 6:
                log.info(f"Using cached CSV: {key} ({age_hours:.1f}h old)")
                content = cache_path.read_text()

        # Try /tmp (from previous session)
        if content is None:
            tmp_path = Path(f"/tmp/force_{key.replace('_D','').replace('_','-')}.csv")
            # Try multiple /tmp conventions
            for tp in [Path(f"/tmp/force_{key}.csv"),
                       Path(f"/tmp/force_{key.replace('_','.')}.csv"),
                       Path(f"/tmp/force_{key.replace('_D','').replace('_','_')}.csv")]:
                if tp.exists():
                    content = tp.read_text()
                    log.info(f"Using /tmp CSV: {tp}")
                    break

        # Download from GitHub
        if content is None and token:
            if file_tree is None:
                try:
                    file_tree = list_repo_files(token)
                except Exception as e:
                    log.warning(f"Could not list repo files: {e}")
                    file_tree = {}
            content = download_csv(token, filename, file_tree)
            if content:
                cache_path.write_text(content)
                log.info(f"Downloaded and cached: {key}")

        if content is None:
            log.warning(f"Could not load CSV for {key}")
            result[key] = []
            continue

        rows = list(csv.DictReader(StringIO(content)))
        parsed = []
        for r in rows:
            try:
                ts = int(float(r["time"]))
                close = float(r.get("close", "nan") or "nan")
                if not math.isnan(close):
                    parsed.append({"ts": ts, "close": close, "raw": r})
            except Exception:
                pass
        parsed.sort(key=lambda x: x["ts"])
        result[key] = parsed
        log.info(f"Loaded {key}: {len(parsed)} bars, "
                 f"{datetime.fromtimestamp(parsed[0]['ts'],tz=timezone.utc).date() if parsed else '?'}"
                 f" → {datetime.fromtimestamp(parsed[-1]['ts'],tz=timezone.utc).date() if parsed else '?'}")

    return result

# ── Force computation ─────────────────────────────────────────────────────────
def _fval(row: dict, *keys) -> Optional[float]:
    for k in keys:
        v = row.get(k, "")
        if v not in ("", "NaN", "nan", None):
            try: return float(v)
            except: pass
    return None

def build_force_series(rows: list, fast_col: str, slow_col: str,
                       invert: bool = False) -> dict:
    """
    Returns {ts: ForceBar} where ForceBar = {gap, gv, state, force_raw}.
    gap       = (fast - slow) / |slow|  [optionally inverted]
    gv        = gap velocity (first diff)
    state     = one of 8 states: MOMENTUM_BULL/BEAR, DECEL_BULL/BEAR,
                CROSS_BULL/BEAR, TRANSITION, REPULSION
    force_raw = gap × gv  (raw product, not used in F_net directly)
    """
    result = {}
    prev_gap = None
    THRESH = 0.001

    for r in rows:
        fast = _fval(r["raw"], fast_col)
        slow = _fval(r["raw"], slow_col)
        if fast is None or slow is None or slow == 0:
            prev_gap = None
            continue

        gap = (fast - slow) / abs(slow)
        if invert:
            gap = -gap

        gv = (gap - prev_gap) if prev_gap is not None else 0.0

        if prev_gap is not None and prev_gap < 0 and gap > 0:
            state = "CROSS_BULL"
        elif prev_gap is not None and prev_gap > 0 and gap < 0:
            state = "CROSS_BEAR"
        elif gv > 0 and gap > THRESH:
            state = "MOMENTUM_BULL"
        elif gv < 0 and gap > THRESH:
            state = "DECEL_BULL"
        elif gv > 0 and gap < -THRESH:
            state = "DECEL_BEAR"
        elif gv < 0 and gap < -THRESH:
            state = "MOMENTUM_BEAR"
        else:
            state = "TRANSITION"

        result[r["ts"]] = {
            "gap": gap,
            "gv": gv,
            "state": state,
            "force_raw": gap * gv,
        }
        prev_gap = gap

    return result

def normalized_force(entry: Optional[dict]) -> float:
    """
    Convert a ForceBar to a normalized scalar in [-1, +1].
    Magnitude = min(|gap| × 40, 1.0)  — gap of 0.025 → 1.0
    Direction = sign(gap)
    Decel factor: 0.6 when gap and gv have opposite signs (force retreating)
    """
    if entry is None:
        return 0.0
    gap = entry["gap"]
    gv  = entry["gv"]
    mag = min(abs(gap) * 40, 1.0)
    direction = math.copysign(1.0, gap) if abs(gap) > 0.001 else 0.0
    decel = 0.6 if direction * gv < 0 else 1.0
    return direction * mag * decel

def nearest_prior(sorted_keys: list, ts_dict: dict, target_ts: int,
                  window_sec: int = 172800) -> Optional[dict]:
    """Find the most recent entry at or before target_ts within window."""
    idx = bisect.bisect_right(sorted_keys, target_ts) - 1
    if idx < 0:
        return None
    k = sorted_keys[idx]
    if target_ts - k > window_sec:
        return None
    return ts_dict[k]

# ── Signal zone classification ────────────────────────────────────────────────
SIGNAL_ZONES = [
    "STRONG_BULL",
    "MOD_BULL",
    "NEUTRAL",
    "MOD_BEAR",
    "STRONG_BEAR",
]

# Confidence tiers (will auto-upgrade STRONG_BULL when checkpoint passes)
CONFIDENCE = {
    "STRONG_BULL":  "PROVISIONAL",  # checkpoint: 2026-09-08 — upgrade if WR ≥70%
    "MOD_BULL":     "PROVISIONAL",
    "NEUTRAL":      "CONFIRMED",
    "MOD_BEAR":     "HIGH",
    "STRONG_BEAR":  "HIGH",
}

# Trade structure recommendations per zone
TRADE_STRUCTURES = {
    "STRONG_BULL": {
        "direction": "BULLISH",
        "structures": ["long_call", "bull_call_spread", "long_leap_call"],
        "dte_range": "10–21",
        "sizing": "HALF (provisional — confirm MSTR/IBIT LT = MOMENTUM_BULL)",
        "gate": "Require MSTR/IBIT LT = MOMENTUM_BULL before entry",
    },
    "MOD_BULL": {
        "direction": "BULLISH",
        "structures": ["long_call", "bull_call_spread"],
        "dte_range": "10–21",
        "sizing": "HALF (provisional)",
        "gate": "Require F_net trend positive (rising 2+ bars)",
    },
    "NEUTRAL": {
        "direction": "NONE",
        "structures": ["ab2_pmcc_income_only"],
        "dte_range": "30–45",
        "sizing": "AB2 income overlay only — no new directional risk",
        "gate": "No directional entries until zone resolves",
    },
    "MOD_BEAR": {
        "direction": "BEARISH",
        "structures": ["long_put", "bear_put_spread", "short_call_spread"],
        "dte_range": "20–45",
        "sizing": "FULL",
        "gate": "None — validated signal",
    },
    "STRONG_BEAR": {
        "direction": "BEARISH",
        "structures": ["long_put", "bear_put_spread", "reduce_calls"],
        "dte_range": "20–45",
        "sizing": "FULL",
        "gate": "None — validated signal",
    },
}

# ── Core engine ───────────────────────────────────────────────────────────────
class MSTRSuiteEngine:
    """
    Magnetic Force Signal Engine for MSTR options entry points.

    Usage:
        engine = MSTRSuiteEngine()
        signal = engine.compute_current_signal()
        print(signal)

        # For integration with morning_brief / daily_analysis_cycle:
        engine.store_signal(signal)
    """

    def __init__(self, force_refresh: bool = False):
        self.env = load_env()
        self._raw = load_csvs(use_cache=True, force_refresh=force_refresh)
        self._build_all_series()
        self._build_mstr_daily()

    def _build_all_series(self):
        """Build all force component timeseries."""
        raw = self._raw

        self._series = {
            "strf_lt":  build_force_series(raw.get("STRF_LQD",[]),
                            "LT Fast Trackline", "LT Slow Trackline"),
            "strf_st":  build_force_series(raw.get("STRF_LQD",[]),
                            "ST Fast Trackline", "ST Slow Trackline"),
            "mibit_lt": build_force_series(raw.get("MSTR_IBIT",[]),
                            "LT Fast Trackline", "LT Slow Trackline"),
            "mibit_st": build_force_series(raw.get("MSTR_IBIT",[]),
                            "ST Fast Trackline", "ST Slow Trackline"),
            "strc_st":  build_force_series(raw.get("STRC",[]),
                            "ST Fast Trackline", "ST Slow Trackline"),
            "strc_lt":  build_force_series(raw.get("STRC",[]),
                            "LT Fast Trackline", "LT Slow Trackline"),
            "stable_lt":build_force_series(raw.get("STABLE_D",[]),
                            "LT Fast Trackline", "LT Slow Trackline", invert=True),
            "stable_st":build_force_series(raw.get("STABLE_D",[]),
                            "ST Fast Trackline", "ST Slow Trackline", invert=True),
            "mstr_st":  build_force_series(raw.get("MSTR",[]),
                            "ST Fast Trackline", "ST Slow Trackline"),
            "mstr_lt":  build_force_series(raw.get("MSTR",[]),
                            "LT Fast Trackline", "LT Slow Trackline"),
            "btc_lt":   build_force_series(raw.get("BTC",[]),
                            "LT Fast Trackline", "LT Slow Trackline"),
        }
        self._sorted_keys = {k: sorted(v.keys()) for k, v in self._series.items()}

    def _build_mstr_daily(self):
        """Build day-level MSTR close lookup."""
        self._mstr_by_day = {}
        for r in self._raw.get("MSTR", []):
            day = datetime.fromtimestamp(r["ts"], tz=timezone.utc).date()
            self._mstr_by_day[day] = r["close"]

    def _get(self, series_name: str, ts: int) -> Optional[dict]:
        """Nearest-prior lookup for a series at timestamp ts."""
        return nearest_prior(
            self._sorted_keys[series_name],
            self._series[series_name],
            ts
        )

    def compute_force_at(self, ts: int) -> dict:
        """
        Compute the full force field at a given timestamp.
        Returns a dict with all components and F_net.

        F_net formula:
          f_primary  = STRF/LQD LT direction × ST magnitude
          multiplier = f(MSTR/IBIT LT state)
          f_credit   = STRC ST normalized force × 0.5
          f_stable   = STABLE.D LT normalized force × 0.4
          f_self     = MSTR ST normalized force × 0.3
          F_net      = multiplier × f_primary + f_credit + f_stable + f_self
        """
        strf_lt  = self._get("strf_lt",  ts)
        strf_st  = self._get("strf_st",  ts)
        mibit_lt = self._get("mibit_lt", ts)
        strc_st  = self._get("strc_st",  ts)
        stable_lt= self._get("stable_lt",ts)
        mstr_st_ = self._get("mstr_st",  ts)
        mstr_lt_ = self._get("mstr_lt",  ts)
        btc_lt_  = self._get("btc_lt",   ts)

        f_strf_lt  = normalized_force(strf_lt)
        f_strf_st  = normalized_force(strf_st)
        f_mibit_lt = normalized_force(mibit_lt)
        f_strc     = normalized_force(strc_st)  * 0.5
        f_stable   = normalized_force(stable_lt) * 0.4
        f_mstr_st  = normalized_force(mstr_st_)  * 0.3

        # Primary direction = STRF/LQD LT; magnitude = STRF/LQD ST
        if f_strf_lt != 0:
            f_primary = math.copysign(abs(f_strf_st), f_strf_lt)
        else:
            f_primary = f_strf_st

        # Multiplier: MSTR/IBIT LT amplifies aligned forces, dampens opposed
        if f_mibit_lt * f_primary > 0:
            multiplier = 1.0 + 0.5 * abs(f_mibit_lt)
        elif f_mibit_lt == 0:
            multiplier = 1.0
        else:
            multiplier = max(0.4, 1.0 - 0.4 * abs(f_mibit_lt))

        f_net = multiplier * f_primary + f_strc + f_stable + f_mstr_st

        return {
            "ts":              ts,
            "f_net":           round(f_net, 4),
            "multiplier":      round(multiplier, 4),
            "f_primary":       round(f_primary, 4),
            "f_credit":        round(f_strc, 4),
            "f_friction":      round(f_stable, 4),
            "f_self":          round(f_mstr_st, 4),
            "mibit_lt_state":  mibit_lt["state"] if mibit_lt else "N/A",
            "strf_lt_state":   strf_lt["state"]  if strf_lt  else "N/A",
            "strc_st_state":   strc_st["state"]  if strc_st  else "N/A",
            "stable_lt_state": stable_lt["state"] if stable_lt else "N/A",
            "mstr_lt_state":   mstr_lt_["state"] if mstr_lt_ else "N/A",
            "btc_lt_state":    btc_lt_["state"]  if btc_lt_  else "N/A",
        }

    def classify_zone(self, f_net: float, context: dict) -> tuple[str, str]:
        """
        Classify F_net into a signal zone using rolling percentiles.
        Returns (zone, confidence).

        Uses dynamic thresholds: F_net vs its own rolling 90-day distribution.
        Falls back to static thresholds if history is thin.
        """
        # Pull historical F_net from DB for dynamic thresholds
        history = self._load_f_net_history(days=90)

        if len(history) >= 30:
            history_sorted = sorted(history)
            n = len(history_sorted)
            t_sb = history_sorted[int(n * 0.80)]
            t_b  = history_sorted[int(n * 0.65)]
            t_br = history_sorted[int(n * 0.35)]
            t_sb2= history_sorted[int(n * 0.20)]
        else:
            # Static fallback (from backtesting results)
            t_sb  = -0.19
            t_b   = -0.60
            t_br  = -1.15
            t_sb2 = -1.66

        if f_net > t_sb:
            zone = "STRONG_BULL"
        elif f_net > t_b:
            zone = "MOD_BULL"
        elif f_net > t_br:
            zone = "NEUTRAL"
        elif f_net > t_sb2:
            zone = "MOD_BEAR"
        else:
            zone = "STRONG_BEAR"

        confidence = CONFIDENCE[zone]

        # Auto-upgrade STRONG_BULL if 6-month checkpoint passed
        # (to be updated manually after September 2026 review)
        checkpoint_date = datetime(2026, 9, 8, tzinfo=timezone.utc)
        if zone == "STRONG_BULL" and datetime.now(tz=timezone.utc) > checkpoint_date:
            # Placeholder: CIO reviews and updates this flag in DB
            confidence = self._check_bull_graduation()

        return zone, confidence

    def _check_bull_graduation(self) -> str:
        """Read graduation flag from DB. Returns 'HIGH' or 'PROVISIONAL'."""
        try:
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute(
                "SELECT value FROM engine_config WHERE key='suite_bull_graduated'"
            ).fetchone()
            conn.close()
            return "HIGH" if row and row[0] == "1" else "PROVISIONAL"
        except Exception:
            return "PROVISIONAL"

    def compute_current_signal(self) -> dict:
        """
        Compute the force field signal for the most recent available bar.
        Returns a full signal dict ready for storage and reporting.
        """
        mstr_rows = self._raw.get("MSTR", [])
        if not mstr_rows:
            raise ValueError("No MSTR data loaded")

        latest = mstr_rows[-1]
        ts = latest["ts"]
        close = latest["close"]
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)

        force = self.compute_force_at(ts)
        zone, confidence = self.classify_zone(force["f_net"], force)
        structure = TRADE_STRUCTURES[zone]

        # Trend: direction of F_net over last 3 bars
        recent = self._compute_recent_trend(n=3)

        signal = {
            "timestamp":        dt.isoformat(),
            "mstr_close":       close,
            "f_net":            force["f_net"],
            "zone":             zone,
            "confidence":       confidence,
            "direction":        structure["direction"],
            "trade_structures": structure["structures"],
            "dte_range":        structure["dte_range"],
            "sizing":           structure["sizing"],
            "gate":             structure["gate"],
            "f_trend":          recent["trend"],
            "f_net_3bar":       recent["values"],
            # Component detail
            "multiplier":       force["multiplier"],
            "f_primary":        force["f_primary"],
            "f_credit":         force["f_credit"],
            "f_friction":       force["f_friction"],
            "f_self":           force["f_self"],
            # Instrument states
            "mibit_lt_state":   force["mibit_lt_state"],
            "strf_lt_state":    force["strf_lt_state"],
            "strc_st_state":    force["strc_st_state"],
            "stable_lt_state":  force["stable_lt_state"],
            "mstr_lt_state":    force["mstr_lt_state"],
        }

        return signal

    def _compute_recent_trend(self, n: int = 3) -> dict:
        """Compute F_net values for last n MSTR bars and determine trend direction."""
        mstr_rows = self._raw.get("MSTR", [])[-n:]
        values = []
        for r in mstr_rows:
            f = self.compute_force_at(r["ts"])
            values.append(round(f["f_net"], 4))
        if len(values) < 2:
            return {"trend": "FLAT", "values": values}
        if values[-1] > values[0]:
            trend = "RISING"
        elif values[-1] < values[0]:
            trend = "FALLING"
        else:
            trend = "FLAT"
        return {"trend": trend, "values": values}

    def _load_f_net_history(self, days: int = 90) -> list:
        """Load historical F_net values from DB for dynamic threshold computation."""
        try:
            cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)
            conn = sqlite3.connect(DB_PATH)
            rows = conn.execute(
                "SELECT f_net FROM mstr_suite_signals WHERE timestamp >= ? ORDER BY timestamp",
                (cutoff.isoformat(),)
            ).fetchall()
            conn.close()
            return [r[0] for r in rows]
        except Exception:
            return []

    def store_signal(self, signal: dict) -> None:
        """Write signal to mstr_suite_signals table. Creates table if needed."""
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mstr_suite_signals (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT NOT NULL,
                mstr_close      REAL,
                f_net           REAL,
                zone            TEXT,
                confidence      TEXT,
                direction       TEXT,
                f_trend         TEXT,
                multiplier      REAL,
                f_primary       REAL,
                f_credit        REAL,
                f_friction      REAL,
                f_self          REAL,
                mibit_lt_state  TEXT,
                strf_lt_state   TEXT,
                strc_st_state   TEXT,
                stable_lt_state TEXT,
                mstr_lt_state   TEXT,
                full_json       TEXT
            )
        """)
        conn.execute("""
            INSERT INTO mstr_suite_signals
                (timestamp, mstr_close, f_net, zone, confidence, direction,
                 f_trend, multiplier, f_primary, f_credit, f_friction, f_self,
                 mibit_lt_state, strf_lt_state, strc_st_state, stable_lt_state,
                 mstr_lt_state, full_json)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            signal["timestamp"], signal["mstr_close"], signal["f_net"],
            signal["zone"], signal["confidence"], signal["direction"],
            signal["f_trend"], signal["multiplier"], signal["f_primary"],
            signal["f_credit"], signal["f_friction"], signal["f_self"],
            signal["mibit_lt_state"], signal["strf_lt_state"],
            signal["strc_st_state"], signal["stable_lt_state"],
            signal["mstr_lt_state"], json.dumps(signal)
        ))
        conn.commit()
        conn.close()
        log.info(f"Signal stored: {signal['zone']} ({signal['confidence']}) "
                 f"F_net={signal['f_net']:+.4f}")

    def format_brief_block(self, signal: dict) -> str:
        """
        Format a signal for inclusion in morning_brief.py output.
        Returns a markdown-formatted string block.
        """
        zone = signal["zone"].replace("_", " ")
        conf_icon = "✅" if signal["confidence"] == "HIGH" else "⚠️ PROVISIONAL"
        dir_icon = {"BULLISH": "📈", "BEARISH": "📉", "NONE": "➡️"}.get(
            signal["direction"], "")

        trend_icon = {"RISING": "↗", "FALLING": "↘", "FLAT": "→"}.get(
            signal["f_trend"], "")

        structures = " / ".join(signal["trade_structures"])

        lines = [
            f"## 🧲 MSTR Suite Force Signal",
            f"**Zone:** {dir_icon} {zone}  |  **Confidence:** {conf_icon}",
            f"**F_net:** {signal['f_net']:+.4f}  |  **Trend:** {trend_icon} {signal['f_trend']}  "
            f"  ({' → '.join(str(v) for v in signal['f_net_3bar'])})",
            f"",
            f"**Component Breakdown:**",
            f"  • Primary (STRF/LQD): {signal['f_primary']:+.4f}  ← {signal['strf_lt_state']}",
            f"  • Multiplier (MIBIT LT): {signal['multiplier']:.3f}  ← {signal['mibit_lt_state']}",
            f"  • Credit (STRC): {signal['f_credit']:+.4f}  ← {signal['strc_st_state']}",
            f"  • Liquidity (STABLE.D): {signal['f_friction']:+.4f}  ← {signal['stable_lt_state']}",
            f"  • Self (MSTR LT): {signal['mstr_lt_state']}",
            f"",
            f"**Trade Action:** {signal['direction']}  |  "
            f"Structures: {structures}  |  DTE: {signal['dte_range']}",
            f"**Sizing:** {signal['sizing']}",
        ]
        if signal["gate"] != "None — validated signal":
            lines.append(f"**Gate:** {signal['gate']}")

        return "\n".join(lines)

    def calibrate(self, forward_days: int = 10, zone_filter: str = None) -> dict:
        """
        Re-run forward return analysis against stored signals.
        Use for the 6-month checkpoint (2026-09-08).

        Args:
            forward_days: look-ahead window for MSTR return
            zone_filter:  if set, only evaluate this zone

        Returns:
            dict of {zone: {"wr": float, "median": float, "n": int}}
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            query = "SELECT timestamp, f_net, zone FROM mstr_suite_signals"
            params = []
            if zone_filter:
                query += " WHERE zone = ?"
                params.append(zone_filter)
            rows = conn.execute(query, params).fetchall()
            conn.close()
        except Exception as e:
            log.error(f"Calibration DB read failed: {e}")
            return {}

        results = {}
        for ts_str, f_net, zone in rows:
            try:
                ts = int(datetime.fromisoformat(ts_str).timestamp())
            except Exception:
                continue
            ret = self._mstr_forward_return(ts, forward_days)
            if ret is None:
                continue
            if zone not in results:
                results[zone] = []
            results[zone].append(ret)

        output = {}
        for zone, rets in results.items():
            if not rets:
                continue
            bull = zone in ("STRONG_BULL", "MOD_BULL")
            wins = sum(1 for r in rets if (r > 0) == bull)
            sorted_rets = sorted(rets)
            output[zone] = {
                "wr":     round(wins / len(rets), 3),
                "median": round(sorted_rets[len(sorted_rets) // 2], 4),
                "n":      len(rets),
            }

        log.info(f"Calibration (+{forward_days}d): {output}")
        return output

    def _mstr_forward_return(self, ts: int, days: int) -> Optional[float]:
        sig_day = datetime.fromtimestamp(ts, tz=timezone.utc).date()
        entry = None
        for d in range(0, 5):
            entry = self._mstr_by_day.get(sig_day + timedelta(days=d))
            if entry:
                break
        if not entry:
            return None
        for d in range(0, 8):
            v = self._mstr_by_day.get(sig_day + timedelta(days=days + d))
            if v:
                return (v - entry) / entry
        return None


# ── CLI entry point ───────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="MSTR Suite Force Engine")
    parser.add_argument("--refresh", action="store_true",
                        help="Force re-download CSVs from GitHub")
    parser.add_argument("--store",   action="store_true",
                        help="Store signal to DB after computing")
    parser.add_argument("--calibrate", type=int, default=0,
                        help="Run calibration for N forward days (e.g. --calibrate 10)")
    parser.add_argument("--zone",   default=None,
                        help="Filter calibration to specific zone")
    parser.add_argument("--json",   action="store_true",
                        help="Output raw JSON instead of formatted brief")
    args = parser.parse_args()

    engine = MSTRSuiteEngine(force_refresh=args.refresh)

    if args.calibrate > 0:
        results = engine.calibrate(forward_days=args.calibrate, zone_filter=args.zone)
        print(json.dumps(results, indent=2))
        return

    signal = engine.compute_current_signal()

    if args.store:
        engine.store_signal(signal)

    if args.json:
        print(json.dumps(signal, indent=2))
    else:
        print(engine.format_brief_block(signal))
        print()
        print(f"Raw F_net: {signal['f_net']:+.4f}  |  Zone: {signal['zone']}  |  "
              f"Confidence: {signal['confidence']}")

if __name__ == "__main__":
    main()
