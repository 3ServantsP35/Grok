#!/usr/bin/env python3
"""
SRI Decision Engine v1.0
========================
Core signal engine for the MSTR Options Recommendation System.

Architecture:
  TradingView (sensor) → CSV → Engine (brain) → Alerts (Discord/Telegram)

Layers:
  1. Data Ingest: Parse CSV exports with 4-TF SRI data
  2. Context Classification: Headwind / Mixed / Tailwind from LT/VLT
  3. Signal Generation: ST-primary framework (ST=decision, VST=timing, LT/VLT=context)
  4. PC Val: Perpetual Call valuation model (MSTR-specific)
  5. LOI: LEAP Opportunity Index computation
  6. Trade Management: Entry/exit tracking, P&L, hypothesis scoring

Author: CIO Engine
Date: 2026-03-01
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Any
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import json
import math
import glob as _glob

# Layer 0: GLI Engine (optional import — engine runs without it if unavailable)
try:
    from gli_engine import GLIEngine, GLIState
    _GLI_AVAILABLE = True
except ImportError:
    _GLI_AVAILABLE = False
    GLIState = None  # type: ignore

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

class AssetMode(Enum):
    MOMENTUM = "Momentum"               # Generic Momentum (legacy)
    MOMENTUM_BTC = "Momentum-BTC"       # BTC-proxy: MSTR, IBIT, PURR — CT1 sweet spot
    MOMENTUM_FUNDAMENTAL = "Momentum-Fundamental"  # Business-driven: TSLA — CT3 required
    MEAN_REVERTING = "MR"               # Broad market: SPY, QQQ, IWM — CT2 sweet spot
    MR_SMALL = "MR-Small"               # Small-cap: IWM — CT1 entry, CT3 = trim signal
    TRENDING = "Trending"               # GLD — all tiers viable, CT1/CT2 best

    def is_momentum(self):
        """True for any Momentum sub-type."""
        return self in (AssetMode.MOMENTUM, AssetMode.MOMENTUM_BTC, AssetMode.MOMENTUM_FUNDAMENTAL)

    def is_mr(self):
        """True for any MR sub-type."""
        return self in (AssetMode.MEAN_REVERTING, AssetMode.MR_SMALL)

    def ab1_requires_ct3(self):
        """True if AB1 entry requires full LT alignment (CT3) rather than CT1."""
        return self == AssetMode.MOMENTUM_FUNDAMENTAL

    def ab1_min_ct_tier(self):
        """Minimum concordance tier required for AB1 entry."""
        if self.ab1_requires_ct3():   return 3
        if self == AssetMode.MR_SMALL: return 1
        return 1  # CT1 default for BTC-proxy, Trending, MR-Large

class Context(Enum):
    HEADWIND = "HEADWIND"       # LT- and VLT-
    MIXED = "MIXED"             # LT and VLT disagree
    TAILWIND = "TAILWIND"       # LT+ and VLT+

class SignalType(Enum):
    AB1_ENTRY = "AB1_ENTRY"
    AB1_EXIT_LT = "AB1_EXIT_LT"
    AB1_EXIT_TRAIL = "AB1_EXIT_TRAIL"
    AB2_BULL_PUT = "AB2_BULL_PUT"
    AB2_BEAR_CALL = "AB2_BEAR_CALL"
    AB2_IRON_CONDOR = "AB2_IC"
    AB2_EXIT = "AB2_EXIT"
    AB3_ACCUMULATE = "AB3_ACC"
    AB3_DEEP_ACCUMULATE = "AB3_DEEP"
    AB3_TRIM = "AB3_TRIM"

ASSET_MODES = {
    # BTC-proxy Momentum: CT1 sweet spot, structural floor via BTC cycle
    "MSTR":    AssetMode.MOMENTUM_BTC,
    "IBIT":    AssetMode.MOMENTUM_BTC,
    "PURR":    AssetMode.MOMENTUM_BTC,
    "BTC":     AssetMode.MOMENTUM_BTC,
    "BTCUSD":  AssetMode.MOMENTUM_BTC,
    "BLOK":    AssetMode.MOMENTUM_BTC,
    # Business-fundamental Momentum: CT3 required, LT must confirm
    "TSLA":    AssetMode.MOMENTUM_FUNDAMENTAL,
    # Mean-Reverting
    "SPY":     AssetMode.MEAN_REVERTING,
    "QQQ":     AssetMode.MEAN_REVERTING,
    "IWM":     AssetMode.MR_SMALL,      # CT1 entry, CT3 = trim signal
    # Trending
    "GLD":     AssetMode.TRENDING,
}

# PC Val constants (update from 8-K filings)
MSTR_BTC_HOLDINGS = 717_130         # Last 8-K
MSTR_SHARES = 333_750_000           # Diluted
MSTR_DEBT = 8_190_000_000           # Total debt
MSTR_PREFERRED = 6_920_000_000      # Preferred equity
MSTR_CASH = 2_300_000_000           # Cash
MSTR_DILUTION_RATE = 0.05           # Annual dilution
MSTR_T_YEARS = 5.0                  # Option tenor
PC_VAL_HOLDINGS_DATE = "2026-02-01" # Staleness check

# ═══════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════

@dataclass
class SRIBIState:
    """SRIBI values across all 4 timeframes at a point in time"""
    vst: float = 0.0
    st: float = 0.0
    lt: float = 0.0
    vlt: float = 0.0
    
    @property
    def avg(self) -> float:
        return (self.vst + self.st + self.lt + self.vlt) / 4.0
    
    @property
    def bull_count(self) -> int:
        return sum(1 for v in [self.vst, self.st, self.lt, self.vlt] if v > 0)
    
    @property
    def context(self) -> Context:
        if self.lt < 0 and self.vlt < 0:
            return Context.HEADWIND
        elif self.lt > 0 and self.vlt > 0:
            return Context.TAILWIND
        return Context.MIXED

@dataclass
class TracklineState:
    """Trackline levels across all 4 timeframes"""
    vst_ftl: float = 0.0
    vst_stl: float = 0.0
    st_ftl: float = 0.0
    st_stl: float = 0.0
    lt_ftl: float = 0.0
    lt_stl: float = 0.0
    vlt_ftl: float = 0.0
    vlt_stl: float = 0.0

@dataclass
class ReversalBandState:
    """Reversal band levels across all 4 timeframes"""
    vst_support: float = 0.0
    vst_resistance: float = 0.0
    vst_robust: float = 0.0
    st_support: float = 0.0
    st_resistance: float = 0.0
    st_robust: float = 0.0
    lt_support: float = 0.0
    lt_resistance: float = 0.0
    lt_robust: float = 0.0
    vlt_support: float = 0.0
    vlt_resistance: float = 0.0
    vlt_robust: float = 0.0

@dataclass
class BarData:
    """Complete data for one 4H bar"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    sribi: SRIBIState = field(default_factory=SRIBIState)
    tracklines: TracklineState = field(default_factory=TracklineState)
    reversal: ReversalBandState = field(default_factory=ReversalBandState)
    # Stage transitions (bool flags)
    stages: Dict[str, bool] = field(default_factory=dict)

@dataclass
class Signal:
    """A generated trading signal"""
    timestamp: datetime
    asset: str
    signal_type: SignalType
    context: Context
    price: float
    sribi: SRIBIState
    confidence: float = 0.0     # 0-1
    metadata: Dict = field(default_factory=dict)

@dataclass 
class Trade:
    """An active or closed trade"""
    entry_signal: Signal
    entry_price: float
    entry_time: datetime
    context_at_entry: Context
    asset: str
    # Exit
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    exit_reason: Optional[str] = None
    # Tracking
    peak_price: float = 0.0
    bars_held: int = 0
    
    @property
    def pnl_pct(self) -> float:
        exit_p = self.exit_price or self.peak_price
        return (exit_p - self.entry_price) / self.entry_price * 100
    
    @property
    def is_open(self) -> bool:
        return self.exit_price is None

@dataclass
class PCValuation:
    """Perpetual Call valuation for MSTR"""
    timestamp: datetime
    btc_price: float
    mstr_price: float
    fair_value: float
    band_position: float    # 0 = bottom, 1 = top
    bottom_band: float
    top_band: float
    discount_pct: float     # negative = trading below FV
    regime: str             # "DISCOUNT", "FAIR", "PREMIUM"

# ═══════════════════════════════════════════════════════════════
# CSV INGEST
# ═══════════════════════════════════════════════════════════════

class SRIDataIngest:
    """Parse TradingView CSV exports into structured bar data"""
    
    SRIBI_COLS = {
        'VST': 'VST SRI Bias Histogram',
        'ST': 'ST SRI Bias Histogram',
        'LT': 'LT SRI Bias Histogram',
        'VLT': 'VLT SRI Bias Histogram',
    }
    
    FTL_COLS = {
        'VST': 'VST Fast Trackline',
        'ST': 'ST Fast Trackline',
        'LT': 'LT Fast Trackline',
        'VLT': 'VLT Fast Trackline',
    }
    
    STL_COLS = {
        'VST': 'VST Slow Trackline',
        'ST': 'ST Slow Trackline',
        'LT': 'LT Slow Trackline',
        'VLT': 'VLT Slow Trackline',
    }
    
    REV_COLS = {
        'VST': ('VST Reversal Support', 'VST Reversal Resistance', 'VST Reversal Robust Fit'),
        'ST': ('ST Reversal Support', 'ST Reversal Resistance', 'ST Reversal Robust Fit'),
        'LT': ('LT Reversal Support', 'LT Reversal Resistance', 'LT Reversal Robust Fit'),
        'VLT': ('VLT Reversal Support', 'VLT Reversal Resistance', 'VLT Reversal Robust Fit'),
    }
    
    STAGE_COLS = {
        f'{tf} Stage {a} to {b}': (tf, f'{a}to{b}')
        for tf in ['VST', 'ST', 'LT', 'VLT']
        for a, b in [(4,1), (1,2), (2,3), (3,4)]
    }
    
    @classmethod
    def load_csv(cls, path: str) -> List[BarData]:
        """Load a TradingView CSV export into BarData list"""
        df = pd.read_csv(path)
        bars = []
        
        for _, row in df.iterrows():
            ts = datetime.utcfromtimestamp(row['time']) if 'time' in row else None
            if ts is None:
                continue
            
            # SRIBI
            sribi = SRIBIState(
                vst=cls._safe_float(row, cls.SRIBI_COLS['VST']),
                st=cls._safe_float(row, cls.SRIBI_COLS['ST']),
                lt=cls._safe_float(row, cls.SRIBI_COLS['LT']),
                vlt=cls._safe_float(row, cls.SRIBI_COLS['VLT']),
            )
            
            # Tracklines
            tracklines = TracklineState(
                vst_ftl=cls._safe_float(row, cls.FTL_COLS['VST']),
                vst_stl=cls._safe_float(row, cls.STL_COLS['VST']),
                st_ftl=cls._safe_float(row, cls.FTL_COLS['ST']),
                st_stl=cls._safe_float(row, cls.STL_COLS['ST']),
                lt_ftl=cls._safe_float(row, cls.FTL_COLS['LT']),
                lt_stl=cls._safe_float(row, cls.STL_COLS['LT']),
                vlt_ftl=cls._safe_float(row, cls.FTL_COLS['VLT']),
                vlt_stl=cls._safe_float(row, cls.STL_COLS['VLT']),
            )
            
            # Reversal bands
            reversal = ReversalBandState()
            for tf, (sup, res, rob) in cls.REV_COLS.items():
                setattr(reversal, f'{tf.lower()}_support', cls._safe_float(row, sup))
                setattr(reversal, f'{tf.lower()}_resistance', cls._safe_float(row, res))
                setattr(reversal, f'{tf.lower()}_robust', cls._safe_float(row, rob))
            
            # Stage transitions
            stages = {}
            for col, (tf, trans) in cls.STAGE_COLS.items():
                if col in row.index:
                    val = row[col]
                    stages[f'{tf}_{trans}'] = bool(val == 1) if not pd.isna(val) else False
            
            bar = BarData(
                timestamp=ts,
                open=float(row['open']),
                high=float(row['high']),
                low=float(row['low']),
                close=float(row['close']),
                sribi=sribi,
                tracklines=tracklines,
                reversal=reversal,
                stages=stages,
            )
            bars.append(bar)
        
        return bars
    
    @staticmethod
    def _safe_float(row, col) -> float:
        if col not in row.index:
            return 0.0
        val = row[col]
        if pd.isna(val):
            return 0.0
        return float(val)

# ═══════════════════════════════════════════════════════════════
# PC VALUATION ENGINE
# ═══════════════════════════════════════════════════════════════

class PCValEngine:
    """
    Perpetual Call Valuation for MSTR
    
    Models MSTR as a Black-Scholes call option on its BTC holdings.
    BTC/share is the underlying, strike is debt/share + preferred/share,
    T=5yr, vol from 30d realized, rf from US02Y.
    
    Band position indicates whether MSTR is cheap/fair/expensive
    relative to its theoretical option value.
    """
    
    def __init__(self,
                 btc_holdings: int = MSTR_BTC_HOLDINGS,
                 shares: int = MSTR_SHARES,
                 debt: float = MSTR_DEBT,
                 preferred: float = MSTR_PREFERRED,
                 cash: float = MSTR_CASH,
                 dilution_rate: float = MSTR_DILUTION_RATE,
                 t_years: float = MSTR_T_YEARS):
        self.btc_holdings = btc_holdings
        self.shares = shares
        self.debt = debt
        self.preferred = preferred
        self.cash = cash
        self.dilution_rate = dilution_rate
        self.t_years = t_years
    
    @property
    def btc_per_share(self) -> float:
        return self.btc_holdings / self.shares
    
    @property
    def strike_per_share(self) -> float:
        return (self.debt + self.preferred - self.cash) / self.shares
    
    def compute(self, btc_price: float, mstr_price: float,
                realized_vol: float = 0.80, risk_free: float = 0.04) -> PCValuation:
        """
        Compute PC Val for current prices.
        
        Args:
            btc_price: Current BTC/USD
            mstr_price: Current MSTR price
            realized_vol: 30-day realized vol (annualized, decimal)
            risk_free: Risk-free rate (decimal)
        """
        S = self.btc_per_share * btc_price  # underlying = BTC value per share
        K = self.strike_per_share            # strike = net debt per share
        T = self.t_years
        sigma = realized_vol
        r = risk_free
        q = self.dilution_rate              # continuous dilution as "dividend"
        
        # Black-Scholes call
        d1 = (math.log(S / K) + (r - q + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        from scipy.stats import norm
        fair_value = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        
        # Bands: ±1σ of fair value (simplified)
        top_band = fair_value * (1 + sigma * math.sqrt(T) * 0.5)
        bottom_band = fair_value * (1 - sigma * math.sqrt(T) * 0.3)
        bottom_band = max(bottom_band, S - K)  # floor at intrinsic
        
        # Band position: 0 = bottom, 1 = top
        band_range = top_band - bottom_band
        band_position = (mstr_price - bottom_band) / band_range if band_range > 0 else 0.5
        band_position = max(0, min(1, band_position))
        
        # Discount/premium
        discount_pct = (mstr_price - fair_value) / fair_value * 100
        
        # Regime
        if discount_pct < -20:
            regime = "DEEP_DISCOUNT"
        elif discount_pct < -5:
            regime = "DISCOUNT"
        elif discount_pct < 15:
            regime = "FAIR"
        elif discount_pct < 40:
            regime = "PREMIUM"
        else:
            regime = "EXTREME_PREMIUM"
        
        return PCValuation(
            timestamp=datetime.utcnow(),
            btc_price=btc_price,
            mstr_price=mstr_price,
            fair_value=fair_value,
            band_position=band_position,
            bottom_band=bottom_band,
            top_band=top_band,
            discount_pct=discount_pct,
            regime=regime,
        )

# ═══════════════════════════════════════════════════════════════
# LOI COMPUTATION
# ═══════════════════════════════════════════════════════════════

def compute_loi(sribi: SRIBIState, prev_vlt: float = 0.0) -> float:
    """
    LEAP Opportunity Index
    Weights: VLT SRIBI (40%) + VLT Acceleration (30%) + LT SRIBI (15%) + Concordance (15%)
    """
    vlt_norm = max(-100, min(100, sribi.vlt / 80 * 100))
    lt_norm = max(-100, min(100, sribi.lt / 80 * 100))
    conc_norm = (sribi.bull_count - 2.0) / 2.0 * 100
    vlt_accel = sribi.vlt - prev_vlt
    roc_norm = max(-100, min(100, vlt_accel / 40 * 100))
    
    return (vlt_norm * 40 + roc_norm * 30 + lt_norm * 15 + conc_norm * 15) / 100

# ═══════════════════════════════════════════════════════════════
# SRIBI ROC (Rate-of-Change) DERIVATIVE — ENGINE SYNC
# ═══════════════════════════════════════════════════════════════
#
# Mirrors the SRIBI_VST/ST/LT/VLT Pine indicators' ROC wave line.
# Lookbacks calibrated per timeframe's natural periodicity (4H bars):
#   VST lb=5 (20h), ST lb=6 (24h), LT lb=7 (28h), VLT lb=8 (32h)
# EMA smoothing = 3 bars (same as Pine).
#
# ROC states (used in dashboard Panel 2 and PMCC gate output):
#   Accel Bull    : ROC > 0 AND SRIBI > 0  — momentum building
#   Decel Bull    : ROC < 0 AND SRIBI > 0  — early warning, still positive
#   Drag Diffusing: ROC > 0 AND SRIBI < 0  — ★ bottom signal, momentum turning
#   Accel Bear    : ROC < 0 AND SRIBI < 0  — full momentum to downside

_SRIBI_ROC_PARAMS = {
    'vst': ('VST SRI Bias Histogram', 5),
    'st':  ('ST SRI Bias Histogram',  6),
    'lt':  ('LT SRI Bias Histogram',  7),
    'vlt': ('VLT SRI Bias Histogram', 8),
}

def add_sribi_roc_columns(df: 'pd.DataFrame', smooth: int = 3) -> 'pd.DataFrame':
    """
    Add vst_roc / st_roc / lt_roc / vlt_roc columns to a DataFrame in-place.

    Formula (matches Pine exactly):
      roc_raw  = bias_score - bias_score[lb]   (difference, not %)
      roc_line = EMA(roc_raw, smooth)

    Call this once on any CSV DataFrame before passing to PMCC engine or
    dashboard to ensure ROC columns are available.
    """
    import pandas as pd
    for tf, (col, lb) in _SRIBI_ROC_PARAMS.items():
        roc_col = f'{tf}_roc'
        if col not in df.columns:
            df[roc_col] = 0.0
            continue
        vals    = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        roc_raw = vals - vals.shift(lb).fillna(0.0)
        df[roc_col] = roc_raw.ewm(span=smooth, adjust=False).mean()
    return df


def roc_state_label(roc: float, sribi: float) -> str:
    """
    Classify a single bar's ROC + SRIBI into a human-readable state.

    Mirrors the four Pine SRIBI indicator label states.
    The 'Drag Diffusing' state is the primary bottom-detection signal —
    momentum turns positive before the zero-line cross (100% lead rate
    at 27 MSTR cycle bottoms, lb=7, 2022-2026 backtest).
    """
    if roc >= 0 and sribi >= 0:  return "Accel Bull"
    if roc <  0 and sribi >= 0:  return "Decel Bull"
    if roc >= 0 and sribi <  0:  return "Drag Diffusing"   # ★ bottom signal
    return "Accel Bear"


# ═══════════════════════════════════════════════════════════════
# ST-PRIMARY SIGNAL ENGINE
# ═══════════════════════════════════════════════════════════════

class STSignalEngine:
    """
    ST-Primary Signal Framework
    
    Hierarchy:
      ST = Decision (whether to trade)
      VST = Timing (when to execute)
      LT/VLT = Context (headwind/mixed/tailwind → sizing + exit rules)
    
    Entry: ST SRIBI crosses positive + VST SRIBI positive
    Exit (Mixed/Headwind): LT SRIBI turns positive OR trailing stop
    Exit (Tailwind): Trailing stop only (wider)
    """
    
    def __init__(self, asset: str, mode: AssetMode,
                 cooldown_bars: int = 18,
                 trail_hw: float = 8.0,
                 trail_tw: float = 10.0):
        self.asset = asset
        self.mode = mode
        self.cooldown_bars = cooldown_bars
        self.trail_hw = trail_hw
        self.trail_tw = trail_tw
        
        # State
        self.prev_sribi: Optional[SRIBIState] = None
        self.last_entry_bar: int = -999
        self.bar_index: int = 0
        self.active_trade: Optional[Trade] = None
        self.closed_trades: List[Trade] = []
        self.signals: List[Signal] = []
    
    def process_bar(self, bar: BarData) -> List[Signal]:
        """Process one 4H bar and return any signals generated"""
        new_signals = []
        
        if self.prev_sribi is not None:
            # ── Check for entry ──
            st_cross_bull = bar.sribi.st > 0 and self.prev_sribi.st <= 0
            vst_confirms = bar.sribi.vst > 0
            cooldown_ok = (self.bar_index - self.last_entry_bar) > self.cooldown_bars
            
            if st_cross_bull and vst_confirms and cooldown_ok and not self.active_trade:
                sig = Signal(
                    timestamp=bar.timestamp,
                    asset=self.asset,
                    signal_type=SignalType.AB1_ENTRY,
                    context=bar.sribi.context,
                    price=bar.close,
                    sribi=bar.sribi,
                    confidence=self._compute_confidence(bar),
                    metadata={
                        'st_cross': True,
                        'vst_value': bar.sribi.vst,
                        'lt_value': bar.sribi.lt,
                        'vlt_value': bar.sribi.vlt,
                    }
                )
                new_signals.append(sig)
                self.signals.append(sig)
                self.last_entry_bar = self.bar_index
                
                # Open trade
                trail_pct = self.trail_tw if bar.sribi.context == Context.TAILWIND else self.trail_hw
                self.active_trade = Trade(
                    entry_signal=sig,
                    entry_price=bar.close,
                    entry_time=bar.timestamp,
                    context_at_entry=bar.sribi.context,
                    asset=self.asset,
                    peak_price=bar.close,
                )
            
            # ── Check for ST alert (VST pending) ──
            if st_cross_bull and not vst_confirms and not self.active_trade:
                sig = Signal(
                    timestamp=bar.timestamp,
                    asset=self.asset,
                    signal_type=SignalType.AB1_ENTRY,
                    context=bar.sribi.context,
                    price=bar.close,
                    sribi=bar.sribi,
                    confidence=0.3,  # Low — waiting for VST
                    metadata={'st_alert_only': True, 'vst_value': bar.sribi.vst}
                )
                # Don't add to main signals — this is a watch alert
                new_signals.append(sig)
            
            # ── Manage active trade ──
            if self.active_trade:
                self.active_trade.peak_price = max(self.active_trade.peak_price, bar.close)
                self.active_trade.bars_held += 1
                
                trail_pct = self.trail_tw if self.active_trade.context_at_entry == Context.TAILWIND else self.trail_hw
                trail_level = self.active_trade.peak_price * (1 - trail_pct / 100)
                
                exit_reason = None
                
                # Exit: LT turns positive (for Mixed/Headwind context)
                if self.active_trade.context_at_entry != Context.TAILWIND:
                    lt_cross_bull = bar.sribi.lt > 0 and self.prev_sribi.lt <= 0
                    if lt_cross_bull:
                        exit_reason = "LT_CONFIRM"
                
                # Exit: Trailing stop
                if bar.close < trail_level:
                    exit_reason = "TRAIL_STOP"
                
                if exit_reason:
                    self.active_trade.exit_price = bar.close
                    self.active_trade.exit_time = bar.timestamp
                    self.active_trade.exit_reason = exit_reason
                    
                    exit_type = SignalType.AB1_EXIT_LT if exit_reason == "LT_CONFIRM" else SignalType.AB1_EXIT_TRAIL
                    sig = Signal(
                        timestamp=bar.timestamp,
                        asset=self.asset,
                        signal_type=exit_type,
                        context=bar.sribi.context,
                        price=bar.close,
                        sribi=bar.sribi,
                        metadata={
                            'exit_reason': exit_reason,
                            'pnl_pct': self.active_trade.pnl_pct,
                            'bars_held': self.active_trade.bars_held,
                            'entry_context': self.active_trade.context_at_entry.value,
                        }
                    )
                    new_signals.append(sig)
                    self.signals.append(sig)
                    self.closed_trades.append(self.active_trade)
                    self.active_trade = None
        
        self.prev_sribi = bar.sribi
        self.bar_index += 1
        return new_signals
    
    def _compute_confidence(self, bar: BarData) -> float:
        """Compute entry confidence 0-1 based on context and SRIBI strength"""
        conf = 0.5  # Baseline
        
        # Context boost
        if bar.sribi.context == Context.MIXED:
            conf += 0.2  # Best context per backtest
        elif bar.sribi.context == Context.HEADWIND:
            conf -= 0.1
        
        # ST strength
        if bar.sribi.st > 10:
            conf += 0.1
        
        # VST strength
        if bar.sribi.vst > 10:
            conf += 0.1
        
        # Near reversal support = better entry
        # (would need reversal band data comparison)
        
        return max(0, min(1, conf))
    
    def summary(self) -> Dict:
        """Return performance summary"""
        if not self.closed_trades:
            return {'asset': self.asset, 'trades': 0}
        
        pnls = [t.pnl_pct for t in self.closed_trades]
        wins = [p for p in pnls if p > 0]
        
        by_context = {}
        for ctx in Context:
            ctx_trades = [t for t in self.closed_trades if t.context_at_entry == ctx]
            if ctx_trades:
                ctx_pnls = [t.pnl_pct for t in ctx_trades]
                by_context[ctx.value] = {
                    'n': len(ctx_trades),
                    'win_pct': len([p for p in ctx_pnls if p > 0]) / len(ctx_pnls) * 100,
                    'median_pnl': float(np.median(ctx_pnls)),
                    'mean_pnl': float(np.mean(ctx_pnls)),
                }
        
        return {
            'asset': self.asset,
            'mode': self.mode.value,
            'trades': len(self.closed_trades),
            'win_pct': len(wins) / len(pnls) * 100 if pnls else 0,
            'median_pnl': float(np.median(pnls)),
            'mean_pnl': float(np.mean(pnls)),
            'open_trade': self.active_trade is not None,
            'by_context': by_context,
        }

# ═══════════════════════════════════════════════════════════════
# AB2 SPREAD ENGINE
# ═══════════════════════════════════════════════════════════════

class AB2SpreadEngine:
    """
    Credit Spread Signal Engine
    
    Sell premium INTO the structural divergence (ST+, LT-).
    Close when LT catches up (confirms positive).
    
    Bull Put: ST crosses + with VST confirming
    Bear Call: MR only, ST crosses - with VST confirming, price extended
    Iron Condor: MR only, neutral zone
    """
    
    def __init__(self, asset: str, mode: AssetMode,
                 cooldown_bars: int = 12):
        self.asset = asset
        self.mode = mode
        self.cooldown_bars = cooldown_bars
        self.prev_sribi: Optional[SRIBIState] = None
        self.bar_index: int = 0
        self.last_entry_bar: int = -999
        self.active_spread: Optional[Dict] = None
        self.closed_spreads: List[Dict] = []
        self.signals: List[Signal] = []
    
    def process_bar(self, bar: BarData) -> List[Signal]:
        new_signals = []
        
        if self.prev_sribi is not None:
            cooldown_ok = (self.bar_index - self.last_entry_bar) > self.cooldown_bars
            
            st_cross_bull = bar.sribi.st > 0 and self.prev_sribi.st <= 0
            st_cross_bear = bar.sribi.st < 0 and self.prev_sribi.st >= 0
            vst_pos = bar.sribi.vst > 0
            vst_neg = bar.sribi.vst < 0
            
            # Bull Put: ST crosses + with VST confirming
            if st_cross_bull and vst_pos and cooldown_ok and not self.active_spread:
                sig = Signal(
                    timestamp=bar.timestamp,
                    asset=self.asset,
                    signal_type=SignalType.AB2_BULL_PUT,
                    context=bar.sribi.context,
                    price=bar.close,
                    sribi=bar.sribi,
                    metadata={'spread_type': 'BULL_PUT'}
                )
                new_signals.append(sig)
                self.signals.append(sig)
                self.last_entry_bar = self.bar_index
                self.active_spread = {
                    'type': 'BULL_PUT',
                    'entry_price': bar.close,
                    'entry_time': bar.timestamp,
                    'context': bar.sribi.context,
                    'entry_bar': self.bar_index,
                }
            
            # Bear Call: MR only
            if self.mode.is_mr() and st_cross_bear and vst_neg and cooldown_ok and not self.active_spread:
                pct_from_ftl = (bar.close - bar.tracklines.lt_ftl) / bar.tracklines.lt_ftl * 100 if bar.tracklines.lt_ftl > 0 else 0
                if pct_from_ftl > 3.0 and bar.sribi.avg > 15:
                    sig = Signal(
                        timestamp=bar.timestamp,
                        asset=self.asset,
                        signal_type=SignalType.AB2_BEAR_CALL,
                        context=bar.sribi.context,
                        price=bar.close,
                        sribi=bar.sribi,
                        metadata={'spread_type': 'BEAR_CALL', 'pct_from_ftl': pct_from_ftl}
                    )
                    new_signals.append(sig)
                    self.signals.append(sig)
                    self.last_entry_bar = self.bar_index
                    self.active_spread = {
                        'type': 'BEAR_CALL',
                        'entry_price': bar.close,
                        'entry_time': bar.timestamp,
                        'context': bar.sribi.context,
                        'entry_bar': self.bar_index,
                    }
            
            # Manage active spread
            if self.active_spread:
                bars_held = self.bar_index - self.active_spread['entry_bar']
                exit_reason = None
                
                # LT confirms positive (for bull puts in mixed/headwind)
                if self.active_spread['type'] == 'BULL_PUT':
                    if self.active_spread['context'] != Context.TAILWIND:
                        if bar.sribi.lt > 0 and self.prev_sribi.lt <= 0:
                            exit_reason = "LT_CONFIRM"
                
                # LT turns negative (for bear calls)
                if self.active_spread['type'] == 'BEAR_CALL':
                    if bar.sribi.lt < 0 and self.prev_sribi.lt >= 0:
                        exit_reason = "LT_REVERT"
                
                # Time stop: 60 bars = 10 days
                if bars_held > 60:
                    exit_reason = "TIME_STOP"
                
                if exit_reason:
                    entry_p = self.active_spread['entry_price']
                    if self.active_spread['type'] == 'BEAR_CALL':
                        pnl = (entry_p - bar.close) / entry_p * 100
                    else:
                        pnl = (bar.close - entry_p) / entry_p * 100
                    
                    sig = Signal(
                        timestamp=bar.timestamp,
                        asset=self.asset,
                        signal_type=SignalType.AB2_EXIT,
                        context=bar.sribi.context,
                        price=bar.close,
                        sribi=bar.sribi,
                        metadata={
                            'exit_reason': exit_reason,
                            'spread_type': self.active_spread['type'],
                            'pnl_pct': pnl,
                            'bars_held': bars_held,
                        }
                    )
                    new_signals.append(sig)
                    self.signals.append(sig)
                    self.active_spread['exit_price'] = bar.close
                    self.active_spread['exit_reason'] = exit_reason
                    self.active_spread['pnl'] = pnl
                    self.active_spread['bars_held'] = bars_held
                    self.closed_spreads.append(self.active_spread)
                    self.active_spread = None
        
        self.prev_sribi = bar.sribi
        self.bar_index += 1
        return new_signals

# ═══════════════════════════════════════════════════════════════
# AB3 LOI ENGINE
# ═══════════════════════════════════════════════════════════════

class AB3LOIEngine:
    """
    LEAP Opportunity Index engine
    
    Accumulate when LOI drops below threshold.
    Trim in phases as LOI rises.
    Mode-dependent thresholds (Momentum vs MR).
    """
    
    def __init__(self, asset: str, mode: AssetMode):
        self.asset = asset
        self.mode = mode
        self.prev_vlt: float = 0.0
        self.signals: List[Signal] = []
        
        # Mode-dependent thresholds
        if mode.is_momentum() or mode == AssetMode.TRENDING:
            self.acc_threshold = -60
            self.deep_acc_threshold = -80
            self.trim_levels = [40, 60, 80]
        else:  # MR / MR_SMALL
            self.acc_threshold = -40
            self.deep_acc_threshold = -60
            self.trim_levels = [10, 30, 50]
    
    def process_bar(self, bar: BarData) -> Tuple[float, List[Signal]]:
        loi = compute_loi(bar.sribi, self.prev_vlt)
        new_signals = []
        
        # Accumulation signals
        if loi < self.deep_acc_threshold:
            sig = Signal(
                timestamp=bar.timestamp, asset=self.asset,
                signal_type=SignalType.AB3_DEEP_ACCUMULATE,
                context=bar.sribi.context, price=bar.close,
                sribi=bar.sribi, metadata={'loi': loi}
            )
            new_signals.append(sig)
        elif loi < self.acc_threshold:
            sig = Signal(
                timestamp=bar.timestamp, asset=self.asset,
                signal_type=SignalType.AB3_ACCUMULATE,
                context=bar.sribi.context, price=bar.close,
                sribi=bar.sribi, metadata={'loi': loi}
            )
            new_signals.append(sig)
        
        # Trim signals
        for level in self.trim_levels:
            if loi > level:
                # Only fire on cross
                prev_loi = compute_loi(
                    SRIBIState(bar.sribi.vst, bar.sribi.st, bar.sribi.lt, self.prev_vlt),
                    self.prev_vlt
                )
                if prev_loi <= level:
                    sig = Signal(
                        timestamp=bar.timestamp, asset=self.asset,
                        signal_type=SignalType.AB3_TRIM,
                        context=bar.sribi.context, price=bar.close,
                        sribi=bar.sribi,
                        metadata={'loi': loi, 'trim_level': level}
                    )
                    new_signals.append(sig)
        
        self.prev_vlt = bar.sribi.vlt
        self.signals.extend(new_signals)
        return loi, new_signals

# ═══════════════════════════════════════════════════════════════
# MAIN ENGINE ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════

class SRIEngine:
    """
    Main orchestrator — processes all assets, generates signals,
    manages state, outputs alerts.
    """
    
    def __init__(self):
        self.assets: Dict[str, Dict] = {}  # asset -> {bars, ab1, ab2, ab3}
        self.pc_val = PCValEngine()
        self.all_signals: List[Signal] = []
    
    def load_asset(self, path: str, asset: str):
        """Load CSV and initialize engines for an asset"""
        mode = ASSET_MODES.get(asset, AssetMode.MEAN_REVERTING)
        bars = SRIDataIngest.load_csv(path)
        
        self.assets[asset] = {
            'bars': bars,
            'mode': mode,
            'ab1': STSignalEngine(asset, mode),
            'ab2': AB2SpreadEngine(asset, mode),
            'ab3': AB3LOIEngine(asset, mode),
        }
        print(f"  Loaded {asset} ({mode.value}): {len(bars)} bars, {bars[0].timestamp.date()} to {bars[-1].timestamp.date()}")
    
    def run_backtest(self, asset: str) -> Dict:
        """Run full backtest on loaded asset data"""
        if asset not in self.assets:
            return {'error': f'{asset} not loaded'}
        
        data = self.assets[asset]
        bars = data['bars']
        ab1 = data['ab1']
        ab2 = data['ab2']
        ab3 = data['ab3']
        
        all_sigs = []
        loi_values = []
        
        for bar in bars:
            sigs1 = ab1.process_bar(bar)
            sigs2 = ab2.process_bar(bar)
            loi, sigs3 = ab3.process_bar(bar)
            
            all_sigs.extend(sigs1 + sigs2 + sigs3)
            loi_values.append(loi)
        
        self.all_signals.extend(all_sigs)
        
        return {
            'asset': asset,
            'mode': data['mode'].value,
            'bars': len(bars),
            'ab1': ab1.summary(),
            'ab2_closed': len(ab2.closed_spreads),
            'ab2_spreads': ab2.closed_spreads[-5:] if ab2.closed_spreads else [],
            'ab3_signals': len(ab3.signals),
            'loi_current': loi_values[-1] if loi_values else None,
            'total_signals': len(all_sigs),
        }
    
    def run_all(self):
        """Run backtest on all loaded assets and print results"""
        print("\n" + "=" * 90)
        print("  SRI DECISION ENGINE v1.0 — BACKTEST RESULTS")
        print("=" * 90)
        
        for asset in self.assets:
            result = self.run_backtest(asset)
            ab1 = result['ab1']
            
            print(f"\n  {'=' * 85}")
            print(f"  {asset} ({result['mode']}) — {result['bars']} bars")
            print(f"  {'=' * 85}")
            
            # AB1
            if ab1['trades'] > 0:
                print(f"  AB1: {ab1['trades']} trades | {ab1['win_pct']:.0f}% win | med {ab1['median_pnl']:+.1f}% | mean {ab1['mean_pnl']:+.1f}%")
                for ctx, stats in ab1.get('by_context', {}).items():
                    marker = " ***" if stats['win_pct'] >= 65 and stats['n'] >= 5 else ""
                    print(f"    {ctx:<12} n={stats['n']:>3} | {stats['win_pct']:>5.0f}% win | med {stats['median_pnl']:>+6.1f}% | mean {stats['mean_pnl']:>+6.1f}%{marker}")
            else:
                print(f"  AB1: No trades")
            
            # AB2
            if result['ab2_closed'] > 0:
                print(f"  AB2: {result['ab2_closed']} closed spreads")
                for sp in result['ab2_spreads']:
                    tag = "W" if sp.get('pnl', 0) > 0 else "L"
                    print(f"    [{tag}] {sp.get('type','?')} {sp.get('entry_time','?')} {sp.get('pnl',0):+.1f}% ({sp.get('bars_held',0)/6:.0f}d) [{sp.get('exit_reason','?')}]")
            
            # AB3
            if result['ab3_signals'] > 0:
                print(f"  AB3: {result['ab3_signals']} signals | LOI current: {result['loi_current']:.1f}")
            
            # Open trade
            if ab1.get('open_trade'):
                engine = self.assets[asset]['ab1']
                t = engine.active_trade
                print(f"  >>> OPEN TRADE: ${t.entry_price:.2f} entry, {t.bars_held} bars, {t.pnl_pct:+.1f}%, ctx={t.context_at_entry.value}")


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    import glob
    
    engine = SRIEngine()
    
    # Auto-discover CSV files
    data_dir = "/mnt/mstr-data"
    csv_map = {
        "MSTR": f"{data_dir}/BATS_MSTR, 240_7b1cc.csv",
        "BTC":  f"{data_dir}/INDEX_BTCUSD, 240_6739b.csv",
        "SPY":  f"{data_dir}/BATS_SPY, 240_8f6d8.csv",
        "QQQ":  f"{data_dir}/BATS_QQQ, 240_5de53.csv",
        "GLD":  f"{data_dir}/BATS_GLD, 240_41f2b.csv",
        "IWM":  f"{data_dir}/BATS_IWM, 240_9624e.csv",
    }
    
    print("Loading assets...")
    for asset, path in csv_map.items():
        try:
            engine.load_asset(path, asset)
        except Exception as e:
            print(f"  FAILED {asset}: {e}")
    
    engine.run_all()


# ═══════════════════════════════════════════════════════════════
# ENGINE v2.0 — ADDITIONS (2026-03-01)
# Regime Layer, AB1 Pre-Breakout, AB3 State Machine, Allocation
# ═══════════════════════════════════════════════════════════════

import glob
import os

@dataclass
class RegimeInput:
    """State of a single regime input at last bar"""
    name: str
    price: float
    sribi: SRIBIState
    context: Context
    score: int          # -1 bearish, 0 neutral, +1 bullish
    interpretation: str
    last_date: datetime

@dataclass
class RegimeState:
    """Composite regime state from all 8 inputs + Layer 0 GLI adjustment"""
    timestamp: datetime
    inputs: Dict[str, RegimeInput] = field(default_factory=dict)
    composite_score: int = 0        # -7 to +7 (raw Layer 1)
    regime_label: str = "NEUTRAL"
    vehicle: str = "IBIT"           # MSTR or IBIT (from ratio SRIBI)
    btc_avg_sribi: float = 0.0
    vix_level: float = 0.0
    # Layer 0 fields (populated when GLIEngine is available)
    gli_state: Optional[object] = None   # GLIState instance
    adjusted_score: int = 0              # composite_score + gli.score_adjustment
    adjusted_regime_label: str = ""      # Label based on adjusted_score

    @property
    def effective_score(self) -> int:
        """Use adjusted score if GLI is available, otherwise raw composite."""
        return self.adjusted_score if self.gli_state is not None else self.composite_score

    @property
    def is_risk_on(self) -> bool:
        return self.effective_score >= 2

    @property
    def is_risk_off(self) -> bool:
        return self.effective_score <= -2

    @property
    def allow_new_entries(self) -> bool:
        return self.effective_score >= -1  # Block entries at -2 or worse

    @property
    def size_multiplier(self) -> float:
        """Recommended position size multiplier (0.5 to 1.0)"""
        score = self.effective_score
        if score >= 3:
            return 1.0
        elif score >= 1:
            return 0.75
        elif score >= -1:
            return 0.5
        else:
            return 0.0  # No new entries

@dataclass
class BucketAllocation:
    """Allocation state for a single bucket"""
    bucket: str             # AB1, AB2, AB3, AB4
    target_pct: float       # Target %
    current_pct: float      # Current mark-to-market %
    deployed_pct: float     # Actually deployed (excl. appreciation)
    floor_pct: float = 0.0  # Minimum allowed
    ceiling_pct: float = 100.0  # Maximum allowed
    
    @property
    def is_over_ceiling(self) -> bool:
        return self.current_pct > self.ceiling_pct
    
    @property
    def is_under_floor(self) -> bool:
        return self.current_pct < self.floor_pct

@dataclass
class AllocationState:
    """Full portfolio allocation state"""
    portfolio_id: str           # "greg", "gavin", "gary"
    total_capital: float
    timestamp: datetime
    buckets: Dict[str, BucketAllocation] = field(default_factory=dict)
    pending_transitions: List[Dict] = field(default_factory=list)  # AB1→AB3 queue
    
    def __post_init__(self):
        if not self.buckets:
            # Default 25/25/25/25 baseline
            defaults = [
                ("AB1", 25.0, 0.0, 100.0),  # no floor, no ceiling
                ("AB2", 25.0, 0.0, 100.0),
                ("AB3", 25.0, 0.0, 35.0),   # 35% ceiling
                ("AB4", 25.0, 10.0, 100.0), # 10% floor (cash/STRC)
            ]
            for bucket, target, floor, ceiling in defaults:
                self.buckets[bucket] = BucketAllocation(
                    bucket=bucket,
                    target_pct=target,
                    current_pct=target,
                    deployed_pct=target,
                    floor_pct=floor,
                    ceiling_pct=ceiling,
                )
    
    @property
    def ab3_at_ceiling(self) -> bool:
        return self.buckets["AB3"].current_pct >= 35.0
    
    @property
    def ab4_at_floor(self) -> bool:
        return self.buckets["AB4"].current_pct <= 10.0

@dataclass
class AB1Trade:
    """AB1 pre-breakout LEAP trade tracking"""
    asset: str
    entry_date: datetime
    entry_price: float
    loi_at_entry: float
    context_at_entry: Context
    bucket: str = "AB1"         # starts AB1, may transition to AB3
    status: str = "OPEN"        # OPEN, BREAKOUT, FAILED, TRANSITIONED, CLOSED
    # Hypothesis tracking
    breakout_target_pct: float = 10.0
    days_max: int = 90
    # Exit tracking
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None
    # Transition tracking
    transitioned_to_ab3: bool = False
    transition_date: Optional[datetime] = None
    
    @property
    def bars_held(self) -> int:
        if self.exit_date:
            return int((self.exit_date - self.entry_date).total_seconds() / (4 * 3600))
        return 0
    
    @property
    def pnl_pct(self) -> float:
        p = self.exit_price or self.entry_price
        return (p - self.entry_price) / self.entry_price * 100


# ═══════════════════════════════════════════════════════════════
# HOWELL PHASE ENGINE  (Layer 0.5)
# ═══════════════════════════════════════════════════════════════

@dataclass
class HowellPhaseState:
    """
    Current Howell macro phase + per-sector signals.
    Four phases: Rebound → Calm → Speculation → Turbulence → repeat
    """
    timestamp: datetime
    phase: str                          # Rebound | Calm | Speculation | Turbulence
    confidence: float                   # Score gap to next-best (0–100 normalised)
    phase_scores: Dict[str, float]      # raw score per phase
    sector_signals: Dict[str, str]      # ticker → BULL | BEAR | NEUTRAL
    sector_sribi: Dict[str, float]      # ticker → LT SRIBI value
    prev_phase: Optional[str] = None
    is_transition: bool = False

    PHASE_ORDER  = ['Rebound', 'Calm', 'Speculation', 'Turbulence']
    PHASE_EMOJIS = {'Rebound': '🌱', 'Calm': '☀️', 'Speculation': '🍂', 'Turbulence': '🌧️'}

    @property
    def emoji(self) -> str:
        return self.PHASE_EMOJIS.get(self.phase, '❓')

    @property
    def ab3_beta_eligible(self) -> bool:
        """MSTR / IBIT AB3 full sizing allowed."""
        return self.phase in ('Rebound', 'Calm')

    @property
    def ab3_beta_caution(self) -> bool:
        """MSTR / IBIT AB3 at 50 % max sizing."""
        return self.phase == 'Speculation'

    @property
    def ab3_equity_eligible(self) -> bool:
        """SPY / QQQ AB3 — Turbulence flush entry only."""
        return self.phase == 'Turbulence'

    @property
    def ab3_cyclicals_eligible(self) -> bool:
        """TSLA / IWM AB3 entry window."""
        return self.phase in ('Rebound', 'Calm')

    @property
    def ab2_paused(self) -> bool:
        """Pause AB2 call-selling across all assets."""
        return self.phase == 'Turbulence'

    @property
    def ab2_delta_cap_adjustment(self) -> float:
        """
        Adjustment to apply to max_delta in AB2 gate.
        Speculation → reduce by 0.05 on equity / cyclical assets.
        """
        return -0.05 if self.phase == 'Speculation' else 0.0

    def ab3_size_multiplier(self, asset_class: str) -> float:
        """
        Phase-conditioned size multiplier for AB3 entries.
        asset_class: 'beta' (MSTR/IBIT), 'equity' (SPY/QQQ),
                     'cyclical' (TSLA/IWM), 'commodity' (GLD),
                     'bond' (TLT)
        """
        table = {
            # phase      beta  equity  cyclical  commodity  bond
            'Rebound':   (1.0,  1.0,    1.0,      0.0,       0.0),
            'Calm':      (1.0,  1.0,    1.0,      1.0,       0.0),
            'Speculation':(0.5, 0.0,    0.0,      0.75,      0.0),
            'Turbulence': (0.0, 1.0,    0.0,      0.0,       1.0),
        }
        idx = {'beta': 0, 'equity': 1, 'cyclical': 2, 'commodity': 3, 'bond': 4}
        row = table.get(self.phase, (0.5,)*5)
        return row[idx.get(asset_class, 0)]


class HowellPhaseEngine:
    """
    Detects the current Howell macro phase by reading LT SRIBI from
    sector ETF CSV exports (downloaded alongside the 16 trading CSVs).

    Phase signature matrix (sign = expected LT SRIBI direction):
      +1 → expect BULL   −1 → expect BEAR   0 → neutral (no contribution)

    Sectors:
        XLK = Technology     XLY = Cyclicals      XLF = Financials
        XLE = Energy         XLP = Defensives      TLT = Bond Duration
        GLD = Commodities    IWM = Cyclicals broad
    """

    # Glob prefix per sector (scans DATA_DIR for latest matching file)
    SECTOR_PREFIXES: Dict[str, str] = {
        'XLK': 'BATS_XLK, 240_',
        'XLY': 'BATS_XLY, 240_',
        'XLF': 'BATS_XLF, 240_',
        'XLE': 'BATS_XLE, 240_',
        'XLP': 'BATS_XLP, 240_',
        'TLT': 'BATS_TLT, 240_',
        'GLD': 'BATS_GLD, 240_',
        'IWM': 'BATS_IWM, 240_',
        'VT':  'BATS_VT, 240_',     # Global equity breadth (world ETF)
    }

    # Phase signature matrix
    # VT = World ETF — global equity breadth signal
    #   Rebound:     +1  global equities recovering alongside domestic
    #   Calm:        +1  global equities healthy
    #   Speculation:  0  US leads; global breadth may lag — neutral contribution
    #   Turbulence:  -1  global risk-off; broad equity selling
    PHASE_SIGNATURES: Dict[str, Dict[str, int]] = {
        'Rebound': {
            'XLK': +1, 'XLY': +1, 'XLF': +1,
            'XLE': -1, 'XLP': -1, 'TLT': -1, 'GLD': -1, 'IWM': +1,
            'VT':  +1,
        },
        'Calm': {
            'XLK': +1, 'XLY': +1, 'XLF': +1,
            'XLE': +1, 'XLP': +1, 'TLT':  0, 'GLD':  0, 'IWM': +1,
            'VT':  +1,
        },
        'Speculation': {
            'XLK': +1, 'XLY': -1, 'XLF':  0,
            'XLE': +1, 'XLP': +1, 'TLT': -1, 'GLD': +1, 'IWM': -1,
            'VT':   0,
        },
        'Turbulence': {
            'XLK': -1, 'XLY': -1, 'XLF': -1,
            'XLE': -1, 'XLP': +1, 'TLT': +1, 'GLD': -1, 'IWM': -1,
            'VT':  -1,
        },
    }

    # SRIBI neutral band — signals within ±THRESHOLD treated as NEUTRAL
    BULL_THRESHOLD = +5.0
    BEAR_THRESHOLD = -5.0

    # Asset-class classification for AB3 size multiplier lookup
    ASSET_CLASS_MAP: Dict[str, str] = {
        'MSTR':  'beta',    'IBIT':  'beta',
        'SPY':   'equity',  'QQQ':   'equity',
        'TSLA':  'cyclical','IWM':   'cyclical',
        'GLD':   'commodity',
        'TLT':   'bond',
        'PURR':  'beta',
    }

    def __init__(self, data_dir: str = "/mnt/mstr-data"):
        self.data_dir = Path(data_dir)

    # ── Internal helpers ─────────────────────────────────────────

    def _find_csv(self, ticker: str) -> Optional[Path]:
        """Return the latest (alphabetically last) CSV matching the prefix."""
        prefix = self.SECTOR_PREFIXES[ticker]
        matches = sorted(self.data_dir.glob(f'{prefix}*.csv'))
        if not matches:
            return None
        # Prefer files with LOI data (larger = more columns); pick the newest
        # by choosing the last sorted match (TradingView names have hash suffix)
        return matches[-1]

    def _load_df(self, ticker: str) -> Optional[pd.DataFrame]:
        """Load sector CSV; return None if unavailable."""
        try:
            path = self._find_csv(ticker)
            if path is None:
                return None
            df = pd.read_csv(path)
            if df.empty:
                return None
            return df
        except Exception:
            return None

    def _classify_signal(self, df: Optional[pd.DataFrame]) -> tuple:
        """
        Extract LT SRIBI from the last bar and classify as BULL/BEAR/NEUTRAL.
        Falls back to VLT if LT is not present.
        Returns (lt_value: float, signal: str)
        """
        if df is None or len(df) == 0:
            return 0.0, 'NEUTRAL'
        last = df.iloc[-1]
        lt  = float(last.get('LT SRI Bias Histogram',  last.get('LT_SRIBI',  0)) or 0)
        vlt = float(last.get('VLT SRI Bias Histogram', last.get('VLT_SRIBI', 0)) or 0)
        # Primary signal: LT. If zero (column missing), use VLT with higher bar.
        if lt > self.BULL_THRESHOLD or (lt == 0.0 and vlt > 20.0):
            return lt, 'BULL'
        if lt < self.BEAR_THRESHOLD or (lt == 0.0 and vlt < -20.0):
            return lt, 'BEAR'
        return lt, 'NEUTRAL'

    # ── Public API ───────────────────────────────────────────────

    def compute(self, prev_phase: Optional[str] = None) -> HowellPhaseState:
        """
        Load all sector CSVs, score each Howell phase, return HowellPhaseState.
        prev_phase: pass the last known phase to detect transitions.
        """
        sector_sribi:   Dict[str, float] = {}
        sector_signals: Dict[str, str]   = {}
        latest_ts = datetime.utcnow()

        for ticker in self.SECTOR_PREFIXES:
            df = self._load_df(ticker)
            if df is not None and len(df) > 0:
                try:
                    bar_ts = datetime.utcfromtimestamp(int(df.iloc[-1]['time']))
                    if bar_ts > latest_ts:
                        latest_ts = bar_ts
                except Exception:
                    pass
            lt_val, sig = self._classify_signal(df)
            sector_sribi[ticker]   = lt_val
            sector_signals[ticker] = sig

        # Score each phase
        phase_scores: Dict[str, float] = {}
        for phase, sigs in self.PHASE_SIGNATURES.items():
            score = 0.0
            for ticker, expected in sigs.items():
                if expected == 0:
                    continue
                actual = sector_signals.get(ticker, 'NEUTRAL')
                actual_val = +1 if actual == 'BULL' else (-1 if actual == 'BEAR' else 0)
                score += expected * actual_val
            phase_scores[phase] = score

        # Rank
        ranked = sorted(phase_scores, key=phase_scores.get, reverse=True)
        best_phase  = ranked[0]
        best_score  = phase_scores[best_phase]
        second_score = phase_scores[ranked[1]] if len(ranked) > 1 else 0.0

        # Confidence: score gap normalised to max possible (non-zero expected entries)
        n_active = sum(1 for v in self.PHASE_SIGNATURES[best_phase].values() if v != 0)
        gap = best_score - second_score
        confidence = round(min(100.0, (gap / max(n_active, 1)) * 100), 1)

        is_transition = (prev_phase is not None and best_phase != prev_phase)

        return HowellPhaseState(
            timestamp      = latest_ts,
            phase          = best_phase,
            confidence     = confidence,
            phase_scores   = phase_scores,
            sector_signals = sector_signals,
            sector_sribi   = sector_sribi,
            prev_phase     = prev_phase,
            is_transition  = is_transition,
        )

    def asset_class(self, asset: str) -> str:
        """Return the Howell asset class string for a given trading asset."""
        return self.ASSET_CLASS_MAP.get(asset.upper(), 'equity')

    def ab3_size_multiplier(self, asset: str, phase_state: HowellPhaseState) -> float:
        """Convenience wrapper: return size multiplier for asset given current phase."""
        ac = self.asset_class(asset)
        return phase_state.ab3_size_multiplier(ac)


# ═══════════════════════════════════════════════════════════════
# REGIME ENGINE
# ═══════════════════════════════════════════════════════════════

class RegimeEngine:
    """
    Processes 8 regime input CSVs into a composite regime state.
    
    Scoring:
      BTC avg SRIBI: <-20 bearish(-1), >10 bullish(+1)
      Stablecoin Dom ST: >0 risk-off(-1), <0 risk-on(+1)
      DXY ST: >0 strong dollar(-1), <0 weak dollar(+1)
      HYG ST: <0 credit stress(-1), >0 credit healthy(+1)
      TLT ST: >0 rates falling(+1), <0 rates rising(-1)
      STRC ST: >0 Saylor engine healthy(+1), <0 weak(-1)
      VIX: >25 high vol(+0 neutral), <18 low vol(-1), 18-25 normal(+0)
      MSTR/IBIT ratio context: used for vehicle selection only
    """
    
    DATA_DIR = "/mnt/mstr-data"
    
    REGIME_FILES = {
        "BTC":        "INDEX_BTCUSD",          # switched from BITSTAMP to INDEX source
        "MSTR_IBIT":  "BATS_MSTR_BATS_IBIT",
        "STABLE":     "CRYPTOCAP_STABLE.C.D",
        "STRC":       "BATS_STRC",
        "TLT":        "BATS_TLT",
        "DXY":        "TVC_DXY",
        "HYG":        "BATS_HYG",
        "VIX":        "TVC_VIX",
    }
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or self.DATA_DIR
        self._cache: Dict[str, pd.DataFrame] = {}
    
    def _find_file(self, prefix: str) -> Optional[str]:
        """Find most recent CSV file matching prefix"""
        pattern = os.path.join(self.data_dir, f"{prefix}*240*.csv")
        matches = sorted(glob.glob(pattern))
        if not matches:
            # Try without 240 constraint
            pattern = os.path.join(self.data_dir, f"{prefix}*.csv")
            matches = sorted(glob.glob(pattern))
        return matches[-1] if matches else None
    
    def _load(self, key: str) -> Optional[pd.DataFrame]:
        if key in self._cache:
            return self._cache[key]
        prefix = self.REGIME_FILES.get(key)
        if not prefix:
            return None
        path = self._find_file(prefix)
        if not path:
            return None
        try:
            df = pd.read_csv(path)
            df['date'] = pd.to_datetime(df['time'], unit='s')
            self._cache[key] = df
            return df
        except Exception:
            return None
    
    def _get_sribi(self, df: pd.DataFrame, row_idx: int = -1) -> SRIBIState:
        row = df.iloc[row_idx]
        return SRIBIState(
            vst=float(row.get('VST SRI Bias Histogram', 0) or 0),
            st=float(row.get('ST SRI Bias Histogram', 0) or 0),
            lt=float(row.get('LT SRI Bias Histogram', 0) or 0),
            vlt=float(row.get('VLT SRI Bias Histogram', 0) or 0),
        )
    
    def _compute_raw(self) -> RegimeState:
        """Compute raw Layer 1 regime state from all 8 market inputs."""
        state = RegimeState(timestamp=datetime.utcnow())
        score = 0
        
        # 1. BTC
        btc_df = self._load("BTC")
        if btc_df is not None:
            sribi = self._get_sribi(btc_df)
            avg = sribi.avg
            state.btc_avg_sribi = avg
            if avg < -20:
                s = -1; interp = "BEARISH — pause MSTR/IBIT entries"
            elif avg > 10:
                s = +1; interp = "BULLISH — full size"
            else:
                s = 0; interp = "NEUTRAL"
            score += s
            state.inputs["BTC"] = RegimeInput(
                "BTC", float(btc_df.iloc[-1]['close']), sribi,
                sribi.context, s, interp, btc_df.iloc[-1]['date']
            )
        
        # 2. Stablecoin Dominance (rising = risk-off)
        stable_df = self._load("STABLE")
        if stable_df is not None:
            sribi = self._get_sribi(stable_df)
            if sribi.st > 0:
                s = -1; interp = "RISK-OFF — capital fleeing crypto"
            else:
                s = +1; interp = "RISK-ON — capital deploying"
            score += s
            state.inputs["STABLE"] = RegimeInput(
                "STABLE", float(stable_df.iloc[-1]['close']), sribi,
                sribi.context, s, interp, stable_df.iloc[-1]['date']
            )
        
        # 3. DXY (strong dollar = headwind)
        dxy_df = self._load("DXY")
        if dxy_df is not None:
            sribi = self._get_sribi(dxy_df)
            if sribi.st > 0:
                s = -1; interp = "STRONG $ — headwind for risk assets"
            else:
                s = +1; interp = "WEAK $ — tailwind for risk assets"
            score += s
            state.inputs["DXY"] = RegimeInput(
                "DXY", float(dxy_df.iloc[-1]['close']), sribi,
                sribi.context, s, interp, dxy_df.iloc[-1]['date']
            )
        
        # 4. HYG (credit stress)
        hyg_df = self._load("HYG")
        if hyg_df is not None:
            sribi = self._get_sribi(hyg_df)
            if sribi.st < 0:
                s = -1; interp = "CREDIT STRESS — risk-off warning"
            else:
                s = +1; interp = "CREDIT HEALTHY — supportive"
            score += s
            state.inputs["HYG"] = RegimeInput(
                "HYG", float(hyg_df.iloc[-1]['close']), sribi,
                sribi.context, s, interp, hyg_df.iloc[-1]['date']
            )
        
        # 5. TLT (rates)
        tlt_df = self._load("TLT")
        if tlt_df is not None:
            sribi = self._get_sribi(tlt_df)
            if sribi.st > 0:
                s = +1; interp = "RATES FALLING — risk tailwind"
            else:
                s = -1; interp = "RATES RISING — risk headwind"
            score += s
            state.inputs["TLT"] = RegimeInput(
                "TLT", float(tlt_df.iloc[-1]['close']), sribi,
                sribi.context, s, interp, tlt_df.iloc[-1]['date']
            )
        
        # 6. STRC (Saylor engine health)
        strc_df = self._load("STRC")
        if strc_df is not None:
            sribi = self._get_sribi(strc_df)
            price = float(strc_df.iloc[-1]['close'])
            if sribi.st > 0 and price >= 97:
                s = +1; interp = f"HEALTHY (${price:.0f}) — engine running"
            elif price < 97:
                s = -1; interp = f"STRESS (${price:.0f}) — preferred under pressure"
            else:
                s = 0; interp = f"NEUTRAL (${price:.0f})"
            score += s
            state.inputs["STRC"] = RegimeInput(
                "STRC", price, sribi, sribi.context, s, interp, strc_df.iloc[-1]['date']
            )
        
        # 7. VIX (vol regime — informs strategy, not direction)
        vix_df = self._load("VIX")
        if vix_df is not None:
            sribi = self._get_sribi(vix_df)
            vix_level = float(vix_df.iloc[-1]['close'])
            state.vix_level = vix_level
            if vix_level > 25:
                s = 0; interp = f"HIGH VOL ({vix_level:.0f}) — sell premium aggressively"
            elif vix_level > 18:
                s = 0; interp = f"NORMAL ({vix_level:.0f}) — standard AB2 sizing"
            else:
                s = -1; interp = f"LOW VOL ({vix_level:.0f}) — reduce premium selling"
            score += s
            state.inputs["VIX"] = RegimeInput(
                "VIX", vix_level, sribi, sribi.context, s, interp, vix_df.iloc[-1]['date']
            )
        
        # 8. MSTR/IBIT Ratio — vehicle selection only (no score)
        ratio_df = self._load("MSTR_IBIT")
        if ratio_df is not None:
            sribi = self._get_sribi(ratio_df)
            ctx = sribi.context
            if ctx == Context.TAILWIND:
                state.vehicle = "IBIT"  # Premium peaked — favor IBIT
            elif ctx == Context.MIXED:
                state.vehicle = "MSTR"  # Premium expanding — favor MSTR
            else:
                state.vehicle = "IBIT"  # Premium compressing
            state.inputs["MSTR_IBIT"] = RegimeInput(
                "MSTR_IBIT", float(ratio_df.iloc[-1]['close']), sribi,
                ctx, 0, f"Vehicle: {state.vehicle}", ratio_df.iloc[-1]['date']
            )
        
        state.composite_score = score
        state.adjusted_score = score  # default until GLI applied

        # Regime label
        if score >= 4:
            state.regime_label = "RISK-ON — full allocation, favor momentum"
        elif score >= 2:
            state.regime_label = "CAUTIOUS BULLISH — standard allocation"
        elif score >= 0:
            state.regime_label = "NEUTRAL — 50% size, favor MR/GLD"
        elif score >= -2:
            state.regime_label = "CAUTIOUS BEARISH — defensive, spreads + cash"
        else:
            state.regime_label = "RISK-OFF — cash/STRC, no new entries"

        state.adjusted_regime_label = state.regime_label
        return state

    def compute(self, gli_state=None) -> "RegimeState":
        """
        Compute Layer 1 regime state.
        Optionally accepts a GLIState from Layer 0 to apply probability adjustments.
        Call signature: regime_engine.compute(gli_state=gli_engine.compute())
        """
        state = self._compute_raw()
        if gli_state is not None:
            state.gli_state = gli_state
            adj = gli_state.score_adjustment
            adjusted = max(-7, min(7, state.composite_score + adj))
            state.adjusted_score = adjusted
            def _regime_label(s: int) -> str:
                if s >= 4:   return "RISK-ON — full allocation, favor momentum"
                elif s >= 2: return "CAUTIOUS BULLISH — standard allocation"
                elif s >= 0: return "NEUTRAL — 50% size, favor MR/GLD"
                elif s >= -2: return "CAUTIOUS BEARISH — defensive, spreads + cash"
                else:         return "RISK-OFF — cash/STRC, no new entries"
            state.adjusted_regime_label = _regime_label(adjusted)
        return state
    
    def ab2_strategy(self, regime: RegimeState) -> str:
        """Recommended AB2 strategy given VIX regime"""
        v = regime.vix_level
        if v > 30:
            return "IRON_CONDOR_WIDE"
        elif v > 25:
            return "IRON_CONDOR"
        elif v > 18:
            return "BULL_PUT_OR_BEAR_CALL"
        else:
            return "AVOID_SELLING"


# ═══════════════════════════════════════════════════════════════
# AB1 PRE-BREAKOUT ENGINE
# ═══════════════════════════════════════════════════════════════

class AB1PreBreakoutEngine:
    """
    AB1 Tactical LEAP Engine
    
    Signal: AB3 anchor (deep LOI) + FTL crosses above STL (Stage 4→1) 
            + MIXED context + VST+ + ST+
    
    Hold: 1 week to 90 days, exit when LT turns positive
    Target: 10%+ underlying move (3-5× on OTM LEAP)
    
    Failure: ST cross- fires within 40 bars of entry AND price <5% gain
             → transition to AB3 (accounting reclassification, no forced close)
    """
    
    def __init__(self, mode: AssetMode = AssetMode.MOMENTUM_BTC):
        self.mode = mode
        self.acc_thresh = -60 if (mode.is_momentum() or mode == AssetMode.TRENDING) else -40
        self.anchor_window = 120    # bars to look back for LOI anchor
        self.cooldown_bars = 40     # min bars between signals
        self.failure_window = 40    # bars to watch for failure
        self.failure_min_gain = 5.0 # % gain required to NOT trigger failure
        # MSTR filter (validated Mar 2026): LOI must have recovered to ≥+10
        # at signal time to confirm genuine momentum vs false bottom bounce.
        # Backtest: LOI<10 → 0% win rate (N=2 both failures);
        #           LOI≥10 → 100% win rate (N=5, med20d=+59.9%)
        self.min_loi_at_signal = 8.0  # slight buffer below 10 to avoid over-fit
    
    def _compute_loi_series(self, df: pd.DataFrame) -> List[float]:
        loi = []
        prev_vlt = 0.0
        for _, row in df.iterrows():
            s = SRIBIState(
                vst=float(row.get('VST SRI Bias Histogram', 0) or 0),
                st=float(row.get('ST SRI Bias Histogram', 0) or 0),
                lt=float(row.get('LT SRI Bias Histogram', 0) or 0),
                vlt=float(row.get('VLT SRI Bias Histogram', 0) or 0),
            )
            loi.append(compute_loi(s, prev_vlt))
            prev_vlt = s.vlt
        return loi
    
    def _detect_ftl_cross(self, df: pd.DataFrame, tf: str = 'ST') -> pd.Series:
        """FTL crosses above STL (Stage 4→1 proxy)"""
        ftl = df.get(f'{tf} Fast Trackline', pd.Series(dtype=float))
        stl = df.get(f'{tf} Slow Trackline', pd.Series(dtype=float))
        sribi = df.get(f'{tf} SRI Bias Histogram', pd.Series(dtype=float))
        if ftl is None or stl is None or len(ftl) == 0:
            return pd.Series(False, index=df.index)
        # Cross up: FTL > STL now, FTL <= STL last bar
        cross = (ftl > stl) & (ftl.shift(1) <= stl.shift(1)) & (sribi.shift(1) < 0)
        return cross.fillna(False)
    
    def scan(self, df: pd.DataFrame) -> List[Signal]:
        """Scan dataframe for AB1 pre-breakout signals"""
        df = df.copy().reset_index(drop=True)
        df['date'] = pd.to_datetime(df['time'], unit='s')
        
        loi_series = self._compute_loi_series(df)
        df['loi'] = loi_series
        
        st_cross = self._detect_ftl_cross(df, 'ST')
        lt_cross = self._detect_ftl_cross(df, 'LT')
        
        signals = []
        last_signal_bar = -self.cooldown_bars
        
        n = len(df)
        for i in range(self.anchor_window, n):
            if i - last_signal_bar < self.cooldown_bars:
                continue
            
            row = df.iloc[i]
            sribi = SRIBIState(
                vst=float(row.get('VST SRI Bias Histogram', 0) or 0),
                st=float(row.get('ST SRI Bias Histogram', 0) or 0),
                lt=float(row.get('LT SRI Bias Histogram', 0) or 0),
                vlt=float(row.get('VLT SRI Bias Histogram', 0) or 0),
            )
            
            # C1: AB3 anchor — LOI was deeply negative in last anchor_window bars
            recent_min_loi = min(loi_series[max(0, i-self.anchor_window):i])
            if recent_min_loi >= self.acc_thresh:
                continue
            
            # C2: Stage 4→1 proxy — FTL crossed above STL (ST or LT) recently
            st_cross_recent = st_cross.iloc[max(0,i-30):i+1].any()
            lt_cross_recent = lt_cross.iloc[max(0,i-30):i+1].any()
            if not (st_cross_recent or lt_cross_recent):
                continue
            
            # C3: Context gate — mode-dependent
            # BTC-proxy + Trending + MR: MIXED context (LT<0, VLT>0) = room to run
            # MOMENTUM_FUNDAMENTAL (TSLA): require TAILWIND (LT>0, VLT>0) = CT3 entry
            if self.mode.ab1_requires_ct3():
                if sribi.context != Context.TAILWIND:
                    continue
            else:
                if sribi.context != Context.MIXED:
                    continue
            
            # C4: VST positive (entry timing)
            if sribi.vst <= 0:
                continue
            
            # C5: ST positive (direction confirmed)
            if sribi.st <= 0:
                continue

            # C6: LOI recovery filter — LOI at signal time must show genuine
            # momentum recovery. Shallow LOI (<8) = false bottom signal.
            # Validated: LOI≥8 removes both MSTR historical false signals (Dec 2021,
            # Oct 2025) with 0 false negatives among confirmed winners.
            current_loi = loi_series[i]
            if current_loi < self.min_loi_at_signal:
                continue

            # Confidence scoring (1-5 conditions met beyond the 5 required)
            confidence = 0.6  # base
            if lt_cross_recent:  # LT cross is stronger than ST cross
                confidence += 0.1
            if recent_min_loi < (self.acc_thresh - 20):  # deeper anchor = higher confidence
                confidence += 0.1
            if df['loi'].iloc[i] > 0:  # LOI recovering above 0 = momentum
                confidence += 0.1
            confidence = min(1.0, confidence)
            
            signals.append(Signal(
                timestamp=row['date'],
                asset="",
                signal_type=SignalType.AB1_ENTRY,
                context=Context.MIXED,
                price=float(row['close']),
                sribi=sribi,
                confidence=confidence,
                metadata={
                    'loi': df['loi'].iloc[i],
                    'min_loi_anchor': recent_min_loi,
                    'st_cross': bool(st_cross_recent),
                    'lt_cross': bool(lt_cross_recent),
                    'target_pct': 10.0,
                    'max_hold_bars': 540,  # 90 days × 6 bars/day
                }
            ))
            last_signal_bar = i
        
        return signals
    
    def check_failure(self, trade: AB1Trade, current_bar: BarData,
                      current_sribi: SRIBIState, bars_since_entry: int) -> Optional[str]:
        """
        Check if AB1 trade should be flagged for AB3 transition.
        Failure: ST cross- fires AND price <5% gain within failure_window bars
        """
        if trade.status != "OPEN":
            return None
        if bars_since_entry > self.failure_window:
            return None  # Past failure window — hold until LT exit
        
        # ST turning negative = loss of confidence
        if current_sribi.st < 0:
            gain_pct = (current_bar.close - trade.entry_price) / trade.entry_price * 100
            if gain_pct < self.failure_min_gain:
                return "AB3_TRANSITION"
        
        return None
    
    def check_exit(self, trade: AB1Trade, current_bar: BarData,
                   current_sribi: SRIBIState, prev_lt: float,
                   bars_since_entry: int) -> Optional[str]:
        """
        AB1 exit rules:
        1. LT turns positive (primary — structural catch-up)
        2. 90-day max (time stop)
        3. First check failure → transition to AB3 if warranted
        """
        if trade.status != "OPEN":
            return None
        
        # Primary exit: LT turns positive
        if current_sribi.lt > 0 and prev_lt <= 0:
            return "LT_POSITIVE"
        
        # Time stop
        if bars_since_entry >= 540:  # 90 days
            return "MAX_HOLD"
        
        return None


# ═══════════════════════════════════════════════════════════════
# AB3 STATE MACHINE v2
# ═══════════════════════════════════════════════════════════════

class AB3StateMachine:
    """
    AB3 LEAP Accumulation — Cycle State Machine
    
    States: NEUTRAL → ACCUMULATING → HOLDING → TRIMMING
    
    Transition logic:
    - NEUTRAL→ACCUMULATING: LOI crosses below acc_thresh
    - ACCUMULATING→HOLDING: LOI rises above acc_thresh + 20 (hysteresis)
    - HOLDING→TRIMMING: LOI crosses above trim levels (25%/50%/75% exits)
    - TRIMMING→NEUTRAL: Final trim executed, LOI reset
    
    Signal frequency: ~4-12/year (not every bar below threshold)
    """
    
    class State(Enum):
        NEUTRAL = "NEUTRAL"
        ACCUMULATING = "ACCUMULATING"
        HOLDING = "HOLDING"
        TRIMMING = "TRIMMING"
    
    def __init__(self, mode: AssetMode = AssetMode.MOMENTUM_BTC):
        self.mode = mode
        if mode.is_momentum() or mode == AssetMode.TRENDING:
            self.acc_thresh = -60
            self.deep_thresh = -80
            self.trim_levels = [40, 60, 80]
            self.hysteresis = 20
        else:  # MR / MR_SMALL
            self.acc_thresh = -40
            self.deep_thresh = -60
            self.trim_levels = [10, 30, 50]
            self.hysteresis = 15

        self.state = self.State.NEUTRAL
        self.trim_idx = 0
        self.last_signal_bar = -30
        self.cooldown = 30
    
    def _get_loi(self, sribi: SRIBIState, prev_vlt: float) -> float:
        return compute_loi(sribi, prev_vlt)
    
    def process_bar(self, bar_idx: int, sribi: SRIBIState, 
                    prev_vlt: float) -> Optional[Tuple[str, float]]:
        """
        Process one bar. Returns (signal_type, loi) or None.
        """
        loi = self._get_loi(sribi, prev_vlt)
        cooldown_ok = (bar_idx - self.last_signal_bar) >= self.cooldown
        sig = None
        
        if self.state == self.State.NEUTRAL:
            if loi < self.deep_thresh and cooldown_ok:
                sig = ("DEEP_ACC", loi)
                self.state = self.State.ACCUMULATING
                self.last_signal_bar = bar_idx
            elif loi < self.acc_thresh and cooldown_ok:
                sig = ("ACC", loi)
                self.state = self.State.ACCUMULATING
                self.last_signal_bar = bar_idx
        
        elif self.state == self.State.ACCUMULATING:
            # Additional deep acc if LOI drops further
            if loi < self.deep_thresh and cooldown_ok:
                sig = ("DEEP_ACC", loi)
                self.last_signal_bar = bar_idx
            # Transition to holding when LOI recovers
            if loi > self.acc_thresh + self.hysteresis:
                self.state = self.State.HOLDING
                self.trim_idx = 0
            # Back to neutral on extreme drop recovery
            elif loi > self.acc_thresh and self.state == self.State.ACCUMULATING:
                pass  # Stay accumulating until hysteresis clears
        
        elif self.state == self.State.HOLDING:
            # Fire trim signals in sequence
            if self.trim_idx < len(self.trim_levels):
                if loi > self.trim_levels[self.trim_idx] and cooldown_ok:
                    pct = (self.trim_idx + 1) * 25
                    sig = (f"TRIM_{pct}%", loi)
                    self.last_signal_bar = bar_idx
                    self.trim_idx += 1
                    if self.trim_idx >= len(self.trim_levels):
                        self.state = self.State.TRIMMING
            # Relapse: drop back to accumulating
            if loi < self.acc_thresh:
                self.state = self.State.ACCUMULATING
                self.trim_idx = 0
        
        elif self.state == self.State.TRIMMING:
            # Final exit
            if cooldown_ok:
                sig = ("EXIT_100%", loi)
                self.state = self.State.NEUTRAL
                self.trim_idx = 0
                self.last_signal_bar = bar_idx
            if loi < self.acc_thresh:
                # New cycle starts immediately
                self.state = self.State.ACCUMULATING
                self.trim_idx = 0
        
        return sig
    
    def scan(self, df: pd.DataFrame) -> List[Tuple[datetime, str, float, float]]:
        """
        Full backtest scan. Returns list of (date, signal_type, loi, price).
        """
        df = df.copy().reset_index(drop=True)
        df['date'] = pd.to_datetime(df['time'], unit='s')
        
        # Reset state
        self.state = self.State.NEUTRAL
        self.trim_idx = 0
        self.last_signal_bar = -self.cooldown
        
        results = []
        prev_vlt = 0.0
        
        for i, row in df.iterrows():
            sribi = SRIBIState(
                vst=float(row.get('VST SRI Bias Histogram', 0) or 0),
                st=float(row.get('ST SRI Bias Histogram', 0) or 0),
                lt=float(row.get('LT SRI Bias Histogram', 0) or 0),
                vlt=float(row.get('VLT SRI Bias Histogram', 0) or 0),
            )
            
            sig = self.process_bar(i, sribi, prev_vlt)
            if sig:
                sig_type, loi = sig
                results.append((row['date'], sig_type, loi, float(row['close'])))
            
            prev_vlt = sribi.vlt
        
        return results


# ═══════════════════════════════════════════════════════════════
# ALLOCATION ENGINE
# ═══════════════════════════════════════════════════════════════

class AllocationEngine:
    """
    Portfolio allocation tracker and transition manager.
    
    Tracks each portfolio independently.
    Handles AB1→AB3 transitions (accounting/tagging, not forced sells).
    Enforces: AB3 ≤35%, AB4 ≥10%.
    """
    
    DEFAULT_TARGETS = {"AB1": 25.0, "AB2": 25.0, "AB3": 25.0, "AB4": 25.0}
    AB3_CEILING = 35.0
    AB4_FLOOR = 10.0
    
    def __init__(self):
        self._portfolios: Dict[str, AllocationState] = {}
    
    def init_portfolio(self, portfolio_id: str, total_capital: float,
                       custom_targets: Dict[str, float] = None):
        """Initialize a portfolio with default 25/25/25/25 allocation"""
        targets = custom_targets or self.DEFAULT_TARGETS
        state = AllocationState(
            portfolio_id=portfolio_id,
            total_capital=total_capital,
            timestamp=datetime.utcnow(),
        )
        for bucket, target in targets.items():
            floor = self.AB4_FLOOR if bucket == "AB4" else 0.0
            ceiling = self.AB3_CEILING if bucket == "AB3" else 100.0
            state.buckets[bucket] = BucketAllocation(
                bucket=bucket,
                target_pct=target,
                current_pct=target,
                deployed_pct=target,
                floor_pct=floor,
                ceiling_pct=ceiling,
            )
        self._portfolios[portfolio_id] = state
        return state
    
    def get(self, portfolio_id: str) -> Optional[AllocationState]:
        return self._portfolios.get(portfolio_id)
    
    def transition_ab1_to_ab3(self, portfolio_id: str, 
                               position_pct: float,
                               trade: AB1Trade,
                               reason: str = "breakout_failed") -> Dict:
        """
        Tag an AB1 LEAP as AB3 (accounting change — no forced close).
        Returns instructions dict with alerts if ceilings/floors triggered.
        """
        state = self._portfolios.get(portfolio_id)
        if not state:
            return {"error": "Portfolio not found"}
        
        ab1 = state.buckets["AB1"]
        ab3 = state.buckets["AB3"]
        
        # Check AB3 ceiling
        new_ab3_pct = ab3.current_pct + position_pct
        alerts = []
        
        if new_ab3_pct > self.AB3_CEILING:
            alerts.append(
                f"⚠️ AB3 would reach {new_ab3_pct:.1f}% (ceiling: {self.AB3_CEILING}%). "
                f"Owner guidance required on new allocation targets."
            )
        
        # Execute transition
        ab1.current_pct -= position_pct
        ab1.deployed_pct -= position_pct
        ab3.current_pct += position_pct
        ab3.deployed_pct += position_pct
        
        # Tag the trade
        trade.transitioned_to_ab3 = True
        trade.transition_date = datetime.utcnow()
        trade.bucket = "AB3"
        
        # Log transition
        state.pending_transitions.append({
            "timestamp": datetime.utcnow().isoformat(),
            "trade_asset": trade.asset,
            "trade_entry_date": trade.entry_date.isoformat(),
            "position_pct": position_pct,
            "reason": reason,
            "new_ab1_pct": ab1.current_pct,
            "new_ab3_pct": ab3.current_pct,
            "alerts": alerts,
        })
        
        return {
            "transitioned": True,
            "new_ab1_pct": ab1.current_pct,
            "new_ab3_pct": ab3.current_pct,
            "alerts": alerts,
        }
    
    def mark_to_market(self, portfolio_id: str, bucket_values: Dict[str, float]):
        """
        Update current_pct based on mark-to-market values.
        Alerts if AB3 > ceiling or AB4 < floor.
        """
        state = self._portfolios.get(portfolio_id)
        if not state:
            return
        
        total = sum(bucket_values.values())
        if total == 0:
            return
        
        alerts = []
        for bucket, value in bucket_values.items():
            if bucket in state.buckets:
                state.buckets[bucket].current_pct = (value / total) * 100
        
        # Check constraints
        ab3 = state.buckets.get("AB3")
        ab4 = state.buckets.get("AB4")
        
        if ab3 and ab3.current_pct > self.AB3_CEILING:
            alerts.append(
                f"⚠️ AB3 at {ab3.current_pct:.1f}% (ceiling {self.AB3_CEILING}%) "
                f"— appreciation triggered. Owner guidance needed."
            )
        
        if ab4 and ab4.current_pct < self.AB4_FLOOR:
            alerts.append(
                f"⚠️ AB4 at {ab4.current_pct:.1f}% (floor {self.AB4_FLOOR}%) "
                f"— cash reserve depleted. Rebalance required."
            )
        
        return alerts
    
    def summary(self, portfolio_id: str) -> str:
        """Human-readable allocation summary"""
        state = self._portfolios.get(portfolio_id)
        if not state:
            return "Portfolio not found"
        
        lines = [
            f"Portfolio: {portfolio_id.upper()} | Capital: ${state.total_capital:,.0f}",
            f"{'Bucket':<6} {'Target':>8} {'Current':>8} {'Deployed':>8} {'Status'}"
        ]
        for bucket, b in sorted(state.buckets.items()):
            status = ""
            if b.is_over_ceiling: status = "⚠️ OVER CEILING"
            elif b.is_under_floor: status = "⚠️ UNDER FLOOR"
            elif abs(b.current_pct - b.target_pct) > 5: status = "⚡ DRIFT"
            lines.append(
                f"{bucket:<6} {b.target_pct:>7.1f}% {b.current_pct:>7.1f}% "
                f"{b.deployed_pct:>7.1f}%  {status}"
            )
        
        if state.pending_transitions:
            lines.append(f"\nPending transitions: {len(state.pending_transitions)}")
            for t in state.pending_transitions[-3:]:  # last 3
                lines.append(
                    f"  {t['trade_asset']} {t['position_pct']:.1f}% AB1→AB3 "
                    f"({t['reason']}) {t['timestamp'][:10]}"
                )
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# UPDATED ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════

class SRIEngineV2:
    """
    SRI Decision Engine v2.0
    
    Full pipeline:
      1. Regime layer (8 inputs → composite score + vehicle)
      2. AB1 pre-breakout signals (tactical LEAPs)
      3. AB2 spread signals (credit spreads, regime-gated)
      4. AB3 state machine (strategic LEAPs, phased trims)
      5. Allocation tracking (bucket percentages + transitions)
      6. PC Val (MSTR fair value from BTC)
    
    CSV assets:
      Trading (8): MSTR, IBIT, SPY, QQQ, GLD, IWM, TSLA, PURR
      Regime (8):  BTC, MSTR/IBIT, StableDom, STRC, TLT, DXY, HYG, VIX
    """
    
    DATA_DIR = "/mnt/mstr-data"
    
    TRADING_ASSETS = {
        # Prefix includes ", " separator to avoid partial matches (e.g. MSTR vs MSTR_BATS_IBIT)
        "MSTR":  ("BATS_MSTR, ",  AssetMode.MOMENTUM_BTC),
        "IBIT":  ("BATS_IBIT, ",  AssetMode.MOMENTUM_BTC),
        "TSLA":  ("BATS_TSLA, ",  AssetMode.MOMENTUM_FUNDAMENTAL),  # CT3 required — P6 finding
        "PURR":  ("BATS_PURR, ",  AssetMode.MOMENTUM_BTC),          # obs mode; BTC-adjacent
        "SPY":   ("BATS_SPY, ",   AssetMode.MEAN_REVERTING),
        "QQQ":   ("BATS_QQQ, ",   AssetMode.MEAN_REVERTING),
        "IWM":   ("BATS_IWM, ",   AssetMode.MR_SMALL),              # CT3 = trim signal, not entry
        "GLD":   ("BATS_GLD, ",   AssetMode.TRENDING),
    }
    
    OBS_ASSETS = {"PURR"}  # Observation mode — track but don't signal
    OBS_MIN_BARS = 500
    
    def __init__(self):
        self.regime_engine  = RegimeEngine(self.DATA_DIR)
        self.howell_engine  = HowellPhaseEngine(self.DATA_DIR)
        self.pc_val_engine  = PCValEngine()
        self.allocation_engine = AllocationEngine()
        self._dfs: Dict[str, pd.DataFrame] = {}
        self._ab3_machines: Dict[str, AB3StateMachine] = {}
        self._ab1_engines: Dict[str, AB1PreBreakoutEngine] = {}
        self._pbear_engines: Dict[str, 'PBearEngine'] = {}
    
    def _load_asset(self, asset: str, prefix: str) -> Optional[pd.DataFrame]:
        if asset in self._dfs:
            return self._dfs[asset]
        pattern = os.path.join(self.DATA_DIR, f"{prefix}*240*.csv")
        matches = sorted(glob.glob(pattern))
        if not matches:
            return None
        try:
            df = pd.read_csv(matches[-1])
            df['date'] = pd.to_datetime(df['time'], unit='s')
            self._dfs[asset] = df
            return df
        except Exception as e:
            print(f"  Load error {asset}: {e}")
            return None
    
    def load_all(self) -> Dict[str, bool]:
        """Load all trading asset CSVs"""
        status = {}
        for asset, (prefix, mode) in self.TRADING_ASSETS.items():
            df = self._load_asset(asset, prefix)
            status[asset] = df is not None
            if df is not None:
                self._ab3_machines[asset] = AB3StateMachine(mode)
                self._ab1_engines[asset] = AB1PreBreakoutEngine(mode)
        return status
    
    def regime(self, with_gli: bool = True) -> RegimeState:
        """Get current regime state (Layer 0 + Layer 1)"""
        gli_state = None
        if with_gli and _GLI_AVAILABLE:
            try:
                gli_state = GLIEngine().compute()
            except Exception:
                pass
        return self.regime_engine.compute(gli_state=gli_state)

    def run_howell(self, prev_phase: Optional[str] = None) -> HowellPhaseState:
        """Run Layer 0.5 — Howell Phase Engine from sector ETF SRI states."""
        return self.howell_engine.compute(prev_phase=prev_phase)

    def run_ab1(self, regime: RegimeState = None) -> Dict[str, List[Signal]]:
        """Run AB1 pre-breakout scan on all assets"""
        results = {}
        reg = regime or self.regime_engine.compute()
        
        for asset, (prefix, mode) in self.TRADING_ASSETS.items():
            df = self._dfs.get(asset)
            if df is None:
                continue
            
            # Observation mode check
            if asset in self.OBS_ASSETS and len(df) < self.OBS_MIN_BARS:
                continue
            
            # Regime gate: block new AB1 entries in risk-off regime
            if not reg.allow_new_entries:
                continue
            
            engine = self._ab1_engines.get(asset)
            if not engine:
                continue
            
            sigs = engine.scan(df)
            for s in sigs:
                s.asset = asset
            results[asset] = sigs
        
        return results
    
    def run_ab3(self) -> Dict[str, List[Tuple]]:
        """Run AB3 state machine scan on all assets"""
        results = {}
        for asset, (prefix, mode) in self.TRADING_ASSETS.items():
            df = self._dfs.get(asset)
            if df is None or asset in self.OBS_ASSETS:
                continue
            machine = self._ab3_machines.get(asset)
            if not machine:
                continue
            results[asset] = machine.scan(df)
        return results

    def run_pbear(self) -> Dict[str, 'PBearSignal']:
        """Layer 2 — P-BEAR bearish top detection for all trading assets."""
        results: Dict[str, 'PBearSignal'] = {}
        for asset, (prefix, mode) in self.TRADING_ASSETS.items():
            if asset in self.OBS_ASSETS:
                continue
            df = self._dfs.get(asset)
            if df is None or len(df) == 0:
                continue
            if asset not in self._pbear_engines:
                self._pbear_engines[asset] = PBearEngine(asset)
            results[asset] = self._pbear_engines[asset].compute(df)
        return results

    def run_ab2(self, regime: RegimeState = None,
                gli_state=None) -> Dict[str, Any]:
        """
        Run AB2 PMCC gate scan on all assets (Framework v3.0).
        GLI state (Layer 0) adjusts the DELTA_MGMT LOI threshold per asset.
        Returns per-asset gate state + income window summary.
        """
        results = {}
        reg     = regime or self.regime_engine.compute()
        pmcc    = AB2PMCCEngine()

        # Extract GLI inputs for threshold adjustment
        # gli_state.gegi is a GEGIState object — extract scalar composite value
        gli_z  = float(getattr(gli_state, 'z_score',  0.0) or 0.0)
        _gegi  = getattr(gli_state, 'gegi', None)
        gegi   = float(_gegi.composite if hasattr(_gegi, 'composite') else (_gegi or 0.0))

        for asset in self.TRADING_ASSETS:
            df = self._dfs.get(asset)
            if df is None or len(df) == 0:
                continue
            signals = pmcc.scan(df, asset,
                                regime_score=reg.composite_score,
                                gli_z=gli_z, gegi=gegi)
            windows = pmcc.income_windows(signals)
            current = pmcc.current_signal(df, asset, gli_z=gli_z, gegi=gegi)
            results[asset] = {
                'current': current,
                'windows': windows,
                'signals': signals,
            }
        return results
    
    def run_all(self, verbose: bool = True, skip_gli: bool = False) -> Dict:
        """Full pipeline run — Layer 0 (GLI) → Layer 1 (Regime) → Layer 2 (Signals) → Layer 3 (Allocation)"""
        load_status = self.load_all()

        # Layer 0: GLI Engine
        gli_state = None
        if _GLI_AVAILABLE and not skip_gli:
            try:
                gli_engine = GLIEngine()
                gli_state = gli_engine.compute()
                if verbose and gli_state.error is None:
                    gli_engine.print_report(gli_state)
                elif verbose and gli_state.error:
                    print(f"  [Layer 0] GLI unavailable: {gli_state.error}")
            except Exception as e:
                print(f"  [Layer 0] GLI engine error: {e}")

        # Layer 0.5: Howell Phase Engine
        howell_state = None
        try:
            howell_state = self.howell_engine.compute()
            if verbose:
                emoji = howell_state.emoji
                conf  = howell_state.confidence
                scores = " | ".join(f"{p}:{v:+.0f}" for p, v in howell_state.phase_scores.items())
                print(f"  [Layer 0.5] Howell Phase: {emoji} {howell_state.phase}  conf={conf:.0f}%  [{scores}]")
        except Exception as e:
            print(f"  [Layer 0.5] Howell engine error: {e}")

        # Layer 1: Regime Engine (with GLI adjustment)
        reg = self.regime_engine.compute(gli_state=gli_state)
        ab1_sigs = self.run_ab1(reg)
        ab2_sigs = self.run_ab2(reg, gli_state=gli_state)
        ab3_sigs = self.run_ab3()
        pbear_sigs = self.run_pbear()
        
        # Current state summary
        current_state = {}
        for asset, df in self._dfs.items():
            if len(df) == 0:
                continue
            last = df.iloc[-1]
            sribi = SRIBIState(
                vst=float(last.get('VST SRI Bias Histogram', 0) or 0),
                st=float(last.get('ST SRI Bias Histogram', 0) or 0),
                lt=float(last.get('LT SRI Bias Histogram', 0) or 0),
                vlt=float(last.get('VLT SRI Bias Histogram', 0) or 0),
            )
            loi_arr = self._ab1_engines[asset]._compute_loi_series(df) if asset in self._ab1_engines else []
            loi_now = loi_arr[-1] if loi_arr else 0
            
            current_state[asset] = {
                "price": float(last['close']),
                "date": last['date'].strftime('%Y-%m-%d') if hasattr(last['date'], 'strftime') else str(last['date']),
                "sribi": {"vst": sribi.vst, "st": sribi.st, "lt": sribi.lt, "vlt": sribi.vlt},
                "context": sribi.context.value,
                "loi": loi_now,
                "mode": self.TRADING_ASSETS[asset][1].value,
                "pbear_state":   pbear_sigs.get(asset).state.name if pbear_sigs.get(asset) else "INACTIVE",
                "pbear_emoji":   pbear_sigs.get(asset).emoji if pbear_sigs.get(asset) else '⚪',
                "pbear_signals": pbear_sigs.get(asset).signals_fired() if pbear_sigs.get(asset) else [],
                "ab2_fast_gate": pbear_sigs.get(asset).ab2_fast_gate if pbear_sigs.get(asset) else False,
            }
        
        # Open AB3 positions (last signal type)
        ab3_last = {}
        for asset, sigs in ab3_sigs.items():
            if sigs:
                ab3_last[asset] = sigs[-1]
        
        if verbose:
            self._print_report(reg, current_state, ab1_sigs, ab2_sigs, ab3_sigs, ab3_last)
        
        return {
            "regime": reg,
            "howell": howell_state,
            "current_state": current_state,
            "ab1_signals": ab1_sigs,
            "ab2_signals": ab2_sigs,
            "ab3_signals": ab3_sigs,
            "pbear_signals": pbear_sigs,
        }
    
    def _print_report(self, reg, current_state, ab1_sigs, ab2_sigs, ab3_sigs, ab3_last):
        import datetime as dt
        print("=" * 90)
        print(f"  SRI ENGINE v2.0 — {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
        print("=" * 90)
        
        # Layer 0 summary (if GLI ran)
        if reg.gli_state is not None:
            g = reg.gli_state
            gli_tag = f"[{g.label}]" if g.error is None else "[UNAVAILABLE]"
            adj_str = f"{g.score_adjustment:+d}" if g.score_adjustment != 0 else "±0"
            print(f"\n  LAYER 0 — GLI: Z={g.gli_zscore:+.2f} {gli_tag}  "
                  f"GEGI={g.gegi.composite:+.2f} [{g.gegi.label}]  "
                  f"SOFR-IORB={g.sofr_iorb_spread_bps:+.0f}bps  "
                  f"Score adj: {adj_str}")

        # Regime
        if reg.gli_state is not None and reg.adjusted_score != reg.composite_score:
            print(f"\n  LAYER 1 REGIME: {reg.adjusted_regime_label}  (GLI-adjusted)")
            print(f"  Raw Score: {reg.composite_score:+d}/7  →  Adjusted: {reg.adjusted_score:+d}/7 | Vehicle: {reg.vehicle} | VIX: {reg.vix_level:.1f}")
        else:
            print(f"\n  LAYER 1 REGIME: {reg.regime_label}")
            print(f"  Score: {reg.composite_score:+d}/7 | Vehicle: {reg.vehicle} | VIX: {reg.vix_level:.1f}")
        print(f"  {'Input':<12} {'Score':>6} {'Interpretation'}")
        for name, inp in reg.inputs.items():
            print(f"  {name:<12} {inp.score:>+5d}  {inp.interpretation}")
        
        # Current asset state
        print(f"\n  {'─'*88}")
        print(f"  {'Asset':<6} {'Price':>9} {'Date':>12} {'VST':>6} {'ST':>6} {'LT':>6} {'VLT':>6} {'LOI':>7} {'Context'}")
        for asset, s in current_state.items():
            sr = s['sribi']
            loi_str = f"{s['loi']:+.1f}"
            print(f"  {asset:<6} ${s['price']:>8.2f} {s['date']:>12} "
                  f"{sr['vst']:>+5.0f} {sr['st']:>+5.0f} {sr['lt']:>+5.0f} {sr['vlt']:>+5.0f} "
                  f"{loi_str:>7} {s['context']}")
        
        # AB1 signals (last 2 per asset)
        print(f"\n  AB1 PRE-BREAKOUT SIGNALS")
        any_ab1 = False
        for asset, sigs in ab1_sigs.items():
            if sigs:
                any_ab1 = True
                for s in sigs[-2:]:
                    ts = s.timestamp.strftime('%Y-%m-%d') if hasattr(s.timestamp, 'strftime') else str(s.timestamp)
                    print(f"  {asset:<6} {ts} ${s.price:.2f} conf={s.confidence:.0%} "
                          f"loi={s.metadata.get('loi',0):+.1f}")
        if not any_ab1:
            print("  No recent AB1 pre-breakout signals")
        
        # AB2 signals (open positions + last entry per asset)
        print(f"\n  AB2 CREDIT SPREADS — MIXED context only (v2)")
        any_ab2 = False
        for asset, sigs in ab2_sigs.items():
            if not sigs:
                continue
            # Show open position or last closed
            open_pos = [s for s in sigs if s.get('status') == 'OPEN']
            last_closed = [s for s in sigs if s.get('status') != 'OPEN']
            if open_pos:
                any_ab2 = True
                p = open_pos[-1]
                ed = p['entry_date'].strftime('%Y-%m-%d') if hasattr(p['entry_date'], 'strftime') else str(p['entry_date'])[:10]
                print(f"  {asset:<6} 🟢 OPEN  entered {ed} @ ${p['entry']:.2f}  "
                      f"ctx={p['context']}  {p['bars_held']}b held")
            elif last_closed:
                any_ab2 = True
                p = last_closed[-1]
                ed = p['entry_date'].strftime('%Y-%m-%d') if hasattr(p['entry_date'], 'strftime') else str(p['entry_date'])[:10]
                pnl = p.get('underlying_pnl', 0)
                mark = "✓" if pnl > 0 else "✗"
                print(f"  {asset:<6} ⚫ last  {ed} @ ${p['entry']:.2f}  "
                      f"exit={p.get('exit_reason','?')}  underlying {pnl:+.1f}% {mark}")
        
        # Current AB2 opportunity scan
        ab2_engine = AB2EngineV2()
        for asset, df in self._dfs.items():
            if asset in AB2EngineV2.AB2_DISABLED or len(df) < 2:
                continue
            sig = ab2_engine.current_signal(df, asset)
            if sig == "BULL_PUT_ENTRY":
                any_ab2 = True
                price = float(df.iloc[-1]['close'])
                print(f"  {asset:<6} 🚨 LIVE SIGNAL: BULL_PUT_ENTRY @ ${price:.2f}")
            elif sig == "LT_EXIT":
                any_ab2 = True
                print(f"  {asset:<6} 🔔 LT_EXIT signal — close open spread")
        
        if not any_ab2:
            print("  No active AB2 positions or signals")
        
        # AB3 recent signals per asset
        print(f"\n  AB3 STRATEGIC LEAP — RECENT SIGNALS")
        for asset, sigs in ab3_sigs.items():
            if sigs:
                recent = sigs[-3:]
                sig_strs = " | ".join(
                    f"{s[1]} {s[0].strftime('%Y-%m-%d')} ${s[3]:.0f}" for s in recent
                )
                print(f"  {asset:<6}: {sig_strs}")



# ═══════════════════════════════════════════════════════════════
# AB2 ENGINE v2 (2026-03-01)
# MIXED context only, LT_POSITIVE exit — validated across 7 assets
# ═══════════════════════════════════════════════════════════════

class AB2EngineV2:
    """
    Credit Spread Engine v2
    
    Validated spec (2026-03-01 backtest):
      Entry: ST cross+ AND VST+ AND MIXED context (LT<0, VLT>0)
      Exit:  LT turns positive (primary) | 90-bar time stop (secondary)
      Gate:  Regime score ≥ -1; VIX size scaling
      
    Win rates: MSTR 72% | QQQ 84% | IWM 75% | GLD 75% | SPY 67% | TSLA 61%
    Disabled:  IBIT (MIXED context doesn't predict LT catch-up reliably)
    
    Hold: ~4-6 trading days (22-30 bars @ 4H)
    Note: P/L shown in underlying % — actual spread P/L will differ based on
          strike selection and premium received. Use as entry/exit timing signal.
    """
    
    AB2_DISABLED = {"IBIT", "BTC", "PURR"}  # No spreads on these assets
    
    def __init__(self, cooldown_bars: int = 12):
        self.cooldown_bars = cooldown_bars
    
    def scan(self, df: pd.DataFrame, asset: str,
             regime_score: int = 0,
             vix_level: float = 20.0) -> List[Dict]:
        """
        Full backtest/live scan. Returns list of closed + open spread dicts.
        """
        if asset in self.AB2_DISABLED:
            return []
        
        # Regime gate: no new entries in risk-off
        if regime_score <= -2:
            return []
        
        # VIX size scaling factor (informational — affects sizing, not signals)
        if vix_level < 18:
            size_scale = 0.5
        elif vix_level > 25:
            size_scale = 1.25
        else:
            size_scale = 1.0
        
        df = df.copy().reset_index(drop=True)
        if 'date' not in df.columns:
            df['date'] = pd.to_datetime(df['time'], unit='s')
        
        closed = []
        active = None
        prev_sribi = None
        last_entry_bar = -self.cooldown_bars
        
        for i, row in df.iterrows():
            sribi = SRIBIState(
                vst=float(row.get('VST SRI Bias Histogram', 0) or 0),
                st=float(row.get('ST SRI Bias Histogram', 0) or 0),
                lt=float(row.get('LT SRI Bias Histogram', 0) or 0),
                vlt=float(row.get('VLT SRI Bias Histogram', 0) or 0),
            )
            price = float(row['close'])
            date = row['date']
            ctx = sribi.context
            
            if prev_sribi is not None:
                cooldown_ok = (i - last_entry_bar) > self.cooldown_bars
                st_cross_bull = sribi.st > 0 and prev_sribi.st <= 0
                
                # Entry: MIXED context only
                if active is None and cooldown_ok:
                    if st_cross_bull and sribi.vst > 0 and ctx == Context.MIXED:
                        active = {
                            'asset': asset,
                            'type': 'BULL_PUT',
                            'entry': price,
                            'entry_bar': i,
                            'entry_date': date,
                            'context': ctx.value,
                            'lt_at_entry': sribi.lt,
                            'size_scale': size_scale,
                            'vix_at_entry': vix_level,
                        }
                        last_entry_bar = i
                
                # Exit management
                if active is not None:
                    bars_held = i - active['entry_bar']
                    exit_reason = None
                    
                    if sribi.lt > 0 and prev_sribi.lt <= 0:
                        exit_reason = "LT_POSITIVE"
                    elif bars_held > 90:
                        exit_reason = "TIME_STOP"
                    
                    if exit_reason:
                        underlying_pnl = (price - active['entry']) / active['entry'] * 100
                        active.update({
                            'exit': price,
                            'exit_date': date,
                            'exit_bar': i,
                            'exit_reason': exit_reason,
                            'underlying_pnl': underlying_pnl,
                            'bars_held': bars_held,
                            'days_held': bars_held / 6,
                        })
                        closed.append(dict(active))
                        active = None
            
            prev_sribi = sribi
        
        # Include open position if any
        if active is not None:
            active['status'] = 'OPEN'
            active['bars_held'] = len(df) - 1 - active['entry_bar']
            closed.append(dict(active))
        
        return closed
    
    def current_signal(self, df: pd.DataFrame, asset: str) -> Optional[str]:
        """
        Check if current bar meets AB2 entry conditions.
        Returns signal type string or None.
        """
        if asset in self.AB2_DISABLED or len(df) < 2:
            return None
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        sribi_now = SRIBIState(
            vst=float(last.get('VST SRI Bias Histogram', 0) or 0),
            st=float(last.get('ST SRI Bias Histogram', 0) or 0),
            lt=float(last.get('LT SRI Bias Histogram', 0) or 0),
            vlt=float(last.get('VLT SRI Bias Histogram', 0) or 0),
        )
        sribi_prev = SRIBIState(
            vst=float(prev.get('VST SRI Bias Histogram', 0) or 0),
            st=float(prev.get('ST SRI Bias Histogram', 0) or 0),
            lt=float(prev.get('LT SRI Bias Histogram', 0) or 0),
            vlt=float(prev.get('VLT SRI Bias Histogram', 0) or 0),
        )
        
        st_cross_bull = sribi_now.st > 0 and sribi_prev.st <= 0
        ctx = sribi_now.context
        
        if st_cross_bull and sribi_now.vst > 0 and ctx == Context.MIXED:
            return "BULL_PUT_ENTRY"
        
        # Exit check for active positions
        if sribi_now.lt > 0 and sribi_prev.lt <= 0:
            return "LT_EXIT"
        
        return None



# ════════════════════════════════════════════════════════════════════
# AB2 PMCC ENGINE v1  (Framework v3.0 — 2026-03-02)
# Replaces: AB2EngineV2 (Bull Put Spreads)
# Reference: briefs/four-bucket-framework-v3.0.md
# ════════════════════════════════════════════════════════════════════

class PMCCGateState(Enum):
    NO_POSITION = "NO_POSITION"  # No AB3 LEAP to write against
    NO_CALLS    = "NO_CALLS"     # LOI < -20: accumulation — preserve upside
    OTM_INCOME  = "OTM_INCOME"   # LOI -20 to thresh: standard income mode, δ ≤ 0.25
    DELTA_MGMT  = "DELTA_MGMT"   # LOI ≥ thresh + CT ≥ 3: trim via calls, δ ≤ 0.40
    PAUSED_AB1  = "PAUSED_AB1"   # AB1 breakout active: don't cap the move


class AB2PMCCEngine:
    """
    PMCC Income Engine — Framework v3.0

    Architecture
    ────────────
    AB3  →  2-year LEAPs (synthetic long stock)
    AB2  →  short calls <90 DTE sold against AB3 LEAPs (income overlay)

    Gate states (LOI + CT tier → max short call delta):
      NO_CALLS   : LOI < -20                       → δ = 0.00  (accumulation — preserve upside)
      OTM_INCOME : LOI -20 to thresh               → δ ≤ 0.25  (income mode)
      DELTA_MGMT : LOI ≥ thresh  AND  CT ≥ 3      → δ ≤ 0.40  (trim exposure via calls)
      PAUSED_AB1 : AB1 signal active               → δ = 0.00  (don't cap the breakout)

    DELTA_MGMT threshold (approved 2026-03-02, Gavin):
      Momentum assets (MSTR, TSLA, IBIT) : base = +40  (avoid capping momentum runs)
      MR assets (SPY, QQQ, GLD, IWM)     : base = +20  (mean-reversion — earlier reduction fine)
      GLI Z > +0.5 or GEGI > 1.0         : min(base + 20, 40)  — liquidity-driven, cap at 40
      GLI Z < -0.5                        : max(base - 10, 10)  — contraction, reduce earlier

    Upside protection (OTM_INCOME): never sell calls within 20% of spot.
    Income target: 2–5%/month of LEAP cost basis (cycle average, not monthly floor).
    IBIT re-enabled — prior restriction was specific to Bull Put Spreads.
    """

    MOMENTUM_ASSETS    = frozenset({'MSTR', 'TSLA', 'IBIT'})  # High-momentum: delay DELTA_MGMT
    LOI_NO_CALL_FLOOR  = -20.0  # Below: no calls (accumulation — preserve upside)
    LOI_TRIM_BASE_MR   = +20.0  # MR assets: standard DELTA_MGMT threshold
    LOI_TRIM_BASE_TR   = +40.0  # Momentum assets: raised base — avoid capping big runs
    CT_DELTA_MGMT_MIN  =  3     # CT tier required to enter DELTA_MGMT

    DELTA_LIMITS: Dict[PMCCGateState, float] = {
        PMCCGateState.NO_POSITION: 0.00,
        PMCCGateState.NO_CALLS:    0.00,
        PMCCGateState.OTM_INCOME:  0.25,
        PMCCGateState.DELTA_MGMT:  0.40,
        PMCCGateState.PAUSED_AB1:  0.00,
    }

    # ── helpers ────────────────────────────────────────────────────

    def _get_loi(self, row: pd.Series) -> float:
        v = row.get('LOI')
        try:
            return float(v) if v is not None and str(v).strip() else 0.0
        except:
            return 0.0

    def _get_ct_tier(self, row: pd.Series) -> int:
        return sum(
            1 for col in ('VST SRI Bias Histogram', 'ST SRI Bias Histogram',
                          'LT SRI Bias Histogram',  'VLT SRI Bias Histogram')
            if (lambda v: bool(v and float(v) > 0))(row.get(col, 0))
        )

    def _check_ab1_active(self, row: pd.Series) -> bool:
        for col in ('CT1 Cross', 'CT2 Cross', 'BP Entry', 'AB1 Active'):
            try:
                if row.get(col) and float(row[col]) > 0:
                    return True
            except:
                pass
        return False

    def _context(self, row: pd.Series) -> str:
        lt  = float(row.get('LT SRI Bias Histogram',  0) or 0)
        vlt = float(row.get('VLT SRI Bias Histogram', 0) or 0)
        if lt > 0 and vlt > 0:  return "TAILWIND"
        if lt <= 0 and vlt <= 0: return "HEADWIND"
        return "MIXED"

    # ── gate logic ─────────────────────────────────────────────────

    def _trim_threshold(self, asset: str = '', gli_z: float = 0.0, gegi: float = 0.0) -> float:
        """
        Asset-class + GLI-adjusted DELTA_MGMT threshold.

        Approved 2026-03-02 (Gavin): Momentum assets (MSTR, TSLA, IBIT) use a
        higher base threshold (+40) to avoid capping monster momentum runs — e.g.
        MSTR rallied 152% during the Sep'24–Jan'25 cycle while LOI was in the
        +20 to +60 range. MR assets use the original +20 base (shallower moves,
        earlier delta reduction is appropriate).

        GLI layer then adjusts on top of the asset-class base:
          GLI Z > +0.5 or GEGI > 1.0  →  min(base + 20, 40)  liquidity-driven, cap at 40
          -0.5 ≤ GLI Z ≤ +0.5         →  base                 neutral — no adjustment
          GLI Z < -0.5                 →  max(base - 10, 10)  contraction — reduce earlier

        Asset class base:
          Momentum (MSTR/TSLA/IBIT)  →  +40
          MR (SPY/QQQ/GLD/IWM)       →  +20
        """
        is_momentum = asset.upper() in self.MOMENTUM_ASSETS
        base = self.LOI_TRIM_BASE_TR if is_momentum else self.LOI_TRIM_BASE_MR
        if gli_z > 0.5 or gegi > 1.0:
            return min(base + 20.0, 40.0)   # cap at 40 — Momentum already there; MR hits 40
        if gli_z < -0.5:
            return max(base - 10.0, 10.0)   # floor at 10 — Momentum=30, MR=10
        return base                          # neutral: Momentum=40, MR=20

    def gate_state(self, loi: float, ct_tier: int,
                   ab1_active: bool = False,
                   has_position: bool = True,
                   asset: str = '',
                   gli_z: float = 0.0,
                   gegi: float = 0.0,
                   pbear_forming: bool = False) -> PMCCGateState:
        if not has_position:
            return PMCCGateState.NO_POSITION
        if ab1_active:
            return PMCCGateState.PAUSED_AB1
        if pbear_forming:
            return PMCCGateState.NO_CALLS  # P-BEAR fast-gate: distribution top forming
        if loi < self.LOI_NO_CALL_FLOOR:
            return PMCCGateState.NO_CALLS
        trim_thresh = self._trim_threshold(asset, gli_z, gegi)
        if loi >= trim_thresh and ct_tier >= self.CT_DELTA_MGMT_MIN:
            return PMCCGateState.DELTA_MGMT
        return PMCCGateState.OTM_INCOME

    def _rationale(self, state: PMCCGateState, loi: float, ct_tier: int,
                   asset: str = '', gli_z: float = 0.0, gegi: float = 0.0,
                   pbear_forming: bool = False) -> str:
        d      = self.DELTA_LIMITS[state]
        thresh = self._trim_threshold(asset, gli_z, gegi)
        is_momentum = asset.upper() in self.MOMENTUM_ASSETS
        asset_tag = f" [{asset.upper()} Momentum base=40]" if is_momentum else ""
        gli_tag = (f" [GLI Z={gli_z:+.2f}, GEGI={gegi:.2f} → thresh={thresh:.0f}]"
                   if gli_z != 0.0 or gegi != 0.0 else "")
        return {
            PMCCGateState.NO_POSITION: "No AB3 LEAP — nothing to write against",
            PMCCGateState.NO_CALLS: (
                f"P-BEAR fast-gate: distribution forming ({asset})"
                if pbear_forming
                else f"LOI {loi:.1f} < {self.LOI_NO_CALL_FLOOR:.0f} — accumulation, preserve upside"
            ),
            PMCCGateState.OTM_INCOME:  f"LOI {loi:.1f} in neutral zone, CT{ct_tier} — OTM calls δ≤{d}{asset_tag}{gli_tag}",
            PMCCGateState.DELTA_MGMT:  f"LOI {loi:.1f} ≥ {thresh:.0f} (asset+GLI adj), CT{ct_tier} — delta reduction δ≤{d}{asset_tag}{gli_tag}",
            PMCCGateState.PAUSED_AB1:  "AB1 breakout active — call selling paused",
        }.get(state, "")

    # ── main scan ──────────────────────────────────────────────────

    def scan(self, df: pd.DataFrame, asset: str,
             regime_score: int = 0,
             gli_z: float = 0.0,
             gegi: float = 0.0) -> List[Dict]:
        """
        Per-bar PMCC gate state across the full history.
        gli_z / gegi adjust the DELTA_MGMT LOI threshold (Layer 0 integration).
        Returns list of signal dicts (one per bar).
        """
        df = df.copy().reset_index(drop=True)
        if 'date' not in df.columns:
            df['date'] = pd.to_datetime(df['time'], unit='s')

        # Add SRIBI ROC derivative columns (mirrors Pine SRIBI_VST/ST/LT/VLT wave lines)
        df = add_sribi_roc_columns(df)

        signals    = []
        prev_state: Optional[PMCCGateState] = None
        trim_thresh = self._trim_threshold(asset, gli_z, gegi)

        for i, row in df.iterrows():
            loi_val    = self._get_loi(row)
            ct_tier    = self._get_ct_tier(row)
            ab1_active = self._check_ab1_active(row)
            price      = float(row['close'])
            state      = self.gate_state(loi_val, ct_tier, ab1_active,
                                         asset=asset, gli_z=gli_z, gegi=gegi)

            # ROC values + state labels
            lt_roc  = float(row.get('lt_roc',  0) or 0)
            st_roc  = float(row.get('st_roc',  0) or 0)
            vst_roc = float(row.get('vst_roc', 0) or 0)
            vlt_roc = float(row.get('vlt_roc', 0) or 0)
            lt_sribi  = float(row.get('LT SRI Bias Histogram',  0) or 0)
            st_sribi  = float(row.get('ST SRI Bias Histogram',  0) or 0)
            vst_sribi = float(row.get('VST SRI Bias Histogram', 0) or 0)
            vlt_sribi = float(row.get('VLT SRI Bias Histogram', 0) or 0)

            signals.append({
                'bar':            i,
                'date':           row['date'],
                'price':          price,
                'loi':            loi_val,
                'ct_tier':        ct_tier,
                'context':        self._context(row),
                'gate_state':     state.value,
                'max_delta':      self.DELTA_LIMITS[state],
                'trim_threshold': trim_thresh,
                'asset_class':    'Momentum' if asset.upper() in self.MOMENTUM_ASSETS else 'MR',
                'gli_z':          gli_z,
                'gegi':           gegi,
                'rationale':      self._rationale(state, loi_val, ct_tier, asset, gli_z, gegi),
                'state_changed':  state != prev_state,
                'ab1_active':     ab1_active,
                # ROC derivative (mirrors Pine SRIBI indicator wave lines)
                'lt_roc':         lt_roc,
                'st_roc':         st_roc,
                'vst_roc':        vst_roc,
                'vlt_roc':        vlt_roc,
                'lt_roc_state':   roc_state_label(lt_roc,  lt_sribi),
                'st_roc_state':   roc_state_label(st_roc,  st_sribi),
                'vst_roc_state':  roc_state_label(vst_roc, vst_sribi),
                'vlt_roc_state':  roc_state_label(vlt_roc, vlt_sribi),
            })
            prev_state = state

        return signals

    def current_signal(self, df: pd.DataFrame, asset: str,
                       gli_z: float = 0.0, gegi: float = 0.0) -> Dict:
        """Gate state for the most recent bar (asset-class + GLI-adjusted, with ROC)."""
        if len(df) < 1:
            return {'gate_state': PMCCGateState.NO_POSITION.value, 'max_delta': 0.0}
        # Enrich with ROC columns before reading last bar
        df = add_sribi_roc_columns(df.copy())
        row     = df.iloc[-1]
        loi_val = self._get_loi(row)
        ct_tier = self._get_ct_tier(row)
        ab1_act = self._check_ab1_active(row)
        state   = self.gate_state(loi_val, ct_tier, ab1_act, asset=asset, gli_z=gli_z, gegi=gegi)

        lt_roc   = float(row.get('lt_roc',  0) or 0)
        st_roc   = float(row.get('st_roc',  0) or 0)
        vst_roc  = float(row.get('vst_roc', 0) or 0)
        vlt_roc  = float(row.get('vlt_roc', 0) or 0)
        lt_sribi = float(row.get('LT SRI Bias Histogram',  0) or 0)
        st_sribi = float(row.get('ST SRI Bias Histogram',  0) or 0)
        vst_sribi= float(row.get('VST SRI Bias Histogram', 0) or 0)
        vlt_sribi= float(row.get('VLT SRI Bias Histogram', 0) or 0)

        return {
            'asset':          asset,
            'gate_state':     state.value,
            'max_delta':      self.DELTA_LIMITS[state],
            'loi':            loi_val,
            'ct_tier':        ct_tier,
            'context':        self._context(row),
            'price':          float(row['close']),
            'ab1_active':     ab1_act,
            'asset_class':    'Momentum' if asset.upper() in self.MOMENTUM_ASSETS else 'MR',
            'trim_threshold': self._trim_threshold(asset, gli_z, gegi),
            'gli_z':          gli_z,
            'gegi':           gegi,
            'rationale':      self._rationale(state, loi_val, ct_tier, asset, gli_z, gegi),
            # ROC derivative (mirrors Pine SRIBI indicator wave lines)
            'lt_roc':         lt_roc,
            'st_roc':         st_roc,
            'vst_roc':        vst_roc,
            'vlt_roc':        vlt_roc,
            'lt_roc_state':   roc_state_label(lt_roc,  lt_sribi),
            'st_roc_state':   roc_state_label(st_roc,  st_sribi),
            'vst_roc_state':  roc_state_label(vst_roc, vst_sribi),
            'vlt_roc_state':  roc_state_label(vlt_roc, vlt_sribi),
        }

    # ── window summary ─────────────────────────────────────────────

    def income_windows(self, signals: List[Dict]) -> List[Dict]:
        """
        Collapse per-bar signals into contiguous income windows
        (gate = OTM_INCOME or DELTA_MGMT). Returns window summaries.
        """
        ACTIVE = {PMCCGateState.OTM_INCOME.value, PMCCGateState.DELTA_MGMT.value}
        windows: List[Dict] = []
        cur: Optional[Dict] = None

        for s in signals:
            active = s['gate_state'] in ACTIVE
            if active and cur is None:
                cur = {
                    'start_bar':   s['bar'],
                    'start_date':  s['date'],
                    'start_price': s['price'],
                    'start_loi':   s['loi'],
                    'peak_delta':  s['max_delta'],
                    '_bars':       [s],
                }
            elif active and cur is not None:
                cur['_bars'].append(s)
                cur['peak_delta'] = max(cur['peak_delta'], s['max_delta'])
            elif not active and cur is not None:
                windows.append(self._close_window(cur, s))
                cur = None

        if cur and cur['_bars']:
            windows.append(self._close_window(cur, signals[-1], open_ended=True))

        return windows

    def _close_window(self, w: Dict, last: Dict, open_ended: bool = False) -> Dict:
        bars = w.pop('_bars')
        n    = len(bars)
        w.update({
            'end_bar':       last['bar'],
            'end_date':      last['date'],
            'end_price':     last['price'],
            'end_loi':       last['loi'],
            'duration_bars': n,
            'duration_days': round(n / 6, 1),
            'avg_loi':       round(sum(b['loi'] for b in bars) / n, 1),
            'avg_ct':        round(sum(b['ct_tier'] for b in bars) / n, 1),
            'price_chg_pct': round((last['price'] - w['start_price']) / w['start_price'] * 100, 1),
            'status':        'OPEN' if open_ended else 'CLOSED',
        })
        return w


# ═════════════════════════════════════════════════════════════════════════════
# P-BEAR SIGNAL LAYER — Phase 1
# Bearish top detection for distribution → markdown transitions.
# Asset-class-specific confirmation ladders derived from Track B empirical analysis.
# ═════════════════════════════════════════════════════════════════════════════

class PBearState(Enum):
    """
    Bearish signal ladder states.
    INACTIVE     : LOI below watch threshold; no bearish monitoring
    WATCH        : LOI entered elevated zone; divergence monitoring active
    FORMING      : Primary bearish signal fires (per asset class)
    FORMING_PLUS : Secondary signal also confirms
    CONFIRMED    : Dual-timeframe confirmation + LOI rolling; AB2 pause recommended
    CONFIRMED_PLUS: Tertiary confirmation (strongest; use for hedge entry)
    INVALIDATED  : Bearish thesis invalidated; monitoring resets
    """
    INACTIVE       = 0
    WATCH          = 1
    FORMING        = 2
    FORMING_PLUS   = 3
    CONFIRMED      = 4
    CONFIRMED_PLUS = 5
    INVALIDATED    = 6


@dataclass
class PBearSignal:
    """P-BEAR state snapshot for a single asset at a single point in time."""
    asset:           str
    state:           PBearState
    asset_class:     str          # MOMENTUM / BTC_CORRELATED / MR / TRENDING
    loi:             float
    watch_threshold: float

    # Individual signal flags
    macd_neg:        bool = False   # MACD histogram < 0
    rsi4h_div:       bool = False   # RSI 4H bearish divergence
    rsid_div:        bool = False   # RSI Daily bearish divergence
    obv_div:         bool = False   # OBV bearish divergence
    loi_rolling:     bool = False   # LOI rolled over from recent peak
    st_bear:         bool = False   # Supertrend flipped BEAR

    # Context values
    price:           float = 0.0
    rsi_4h:          float = 0.0
    rsi_daily:       float = 0.0
    macd_hist:       float = 0.0

    @property
    def ab2_fast_gate(self) -> bool:
        """True if call-selling should be paused immediately (FORMING or above)."""
        return self.state.value >= PBearState.FORMING.value

    @property
    def emoji(self) -> str:
        return {
            PBearState.INACTIVE:       '⚪',
            PBearState.WATCH:          '👁',
            PBearState.FORMING:        '🟡',
            PBearState.FORMING_PLUS:   '🟠',
            PBearState.CONFIRMED:      '🔴',
            PBearState.CONFIRMED_PLUS: '🚨',
            PBearState.INVALIDATED:    '✅',
        }.get(self.state, '⚪')

    @property
    def label(self) -> str:
        return self.state.name.replace('_', ' ')

    def signals_fired(self) -> List[str]:
        fired = []
        if self.macd_neg:     fired.append('MACD<0')
        if self.rsi4h_div:    fired.append('RSI4H_DIV')
        if self.rsid_div:     fired.append('RSI_D_DIV')
        if self.obv_div:      fired.append('OBV_DIV')
        if self.loi_rolling:  fired.append('LOI_ROLL')
        if self.st_bear:      fired.append('ST_BEAR')
        return fired


class PBearEngine:
    """
    P-BEAR Signal Layer — Phase 1.

    Computes the bearish top detection state for a trading asset using
    per-asset-class confirmation ladders derived from Track B empirical analysis.

    Asset classes and primary signals (Track B findings):
      MOMENTUM (MSTR, TSLA):
        WATCH       -> LOI > +40
        FORMING     -> MACD_hist < 0 AND LOI > +20
        FORMING+    -> RSI4H divergence confirmed
        CONFIRMED   -> RSI_Daily divergence + LOI rolling over
        CONF+       -> OBV divergence (tertiary)
        INVALIDATION -> MACD_hist > 0 AND price at/near 20-bar high

      BTC_CORRELATED (IBIT):
        WATCH       -> LOI > +20
        FORMING     -> OBV divergence (OBV < OBV_SMA20 or OBV < peak OBV)
        FORMING+    -> RSI4H divergence also fires
        CONFIRMED   -> RSI_Daily also diverging
        INVALIDATION -> OBV recovers above SMA20

      MR (SPY, QQQ, IWM):
        WATCH       -> LOI > +20
        FORMING     -> RSI4H divergence
        FORMING+    -> OBV < OBV_SMA20 (volume confirmation)
        CONFIRMED   -> RSI_Daily divergence also fires
        INVALIDATION -> RSI4H recovers + price at/near new high

      TRENDING (GLD):
        WATCH       -> LOI > +20
        FORMING     -> OBV divergence AND RSI4H divergence simultaneously
        CONFIRMED   -> Supertrend flips BEAR
        INVALIDATION -> Supertrend flips back BULL

    Column name mapping (TradingView CSV format):
      MTF RSI     = RSI 4H (updates every 4H bar)
      MTF RSI.1   = RSI Daily (forward-filled; updates on daily close)
      Histogram   = MACD histogram
      OnBalanceVolume = OBV
      Up Trend    = Supertrend BULL (notna = BULL active)
      Down Trend  = Supertrend BEAR (notna = BEAR active)
      LOI         = LEAP Opportunity Index
      %K / %D     = Weekly StochRSI (secondary only; long warmup)
    """

    MOMENTUM_ASSETS    = frozenset({'MSTR', 'TSLA'})
    BTC_CORRELATED     = frozenset({'IBIT'})
    MR_ASSETS          = frozenset({'SPY', 'QQQ', 'IWM'})
    TRENDING_ASSETS    = frozenset({'GLD'})

    WATCH_MOMENTUM     = +40.0   # Momentum: DELTA_MGMT threshold = watch start
    WATCH_DEFAULT      = +20.0   # All other classes

    DIV_LOOKBACK       = 20      # bars (4H x 20 = ~3.5 trading days)
    PRICE_NEAR_PEAK    = 0.05    # within 5% of local high = "at the top"
    RSI_DIV_MIN_GAP    = 2.0     # RSI must be at least 2 pts below peak RSI
    LOI_ROLL_LOOKBACK  = 5       # bars to check LOI rollover

    def __init__(self, asset: str):
        self.asset       = asset.upper()
        self.asset_class = self._classify(self.asset)
        self.watch_threshold = (
            self.WATCH_MOMENTUM if self.asset_class == 'MOMENTUM'
            else self.WATCH_DEFAULT
        )

    def _classify(self, asset: str) -> str:
        if asset in self.MOMENTUM_ASSETS:   return 'MOMENTUM'
        if asset in self.BTC_CORRELATED:    return 'BTC_CORRELATED'
        if asset in self.MR_ASSETS:         return 'MR'
        if asset in self.TRENDING_ASSETS:   return 'TRENDING'
        return 'MR'

    # -- helpers ----------------------------------------------------------------

    @staticmethod
    def _safe(val, default: float = 0.0) -> float:
        try:
            v = float(val)
            return default if (v != v) else v   # NaN check
        except Exception:
            return default

    @staticmethod
    def _col(df: pd.DataFrame, *names) -> Optional[pd.Series]:
        for n in names:
            if n in df.columns:
                return df[n]
        return None

    # -- signal detectors -------------------------------------------------------

    def _rsi4h_div(self, df: pd.DataFrame) -> bool:
        """Bearish RSI4H divergence: price at/near prior local high, RSI below prior peak RSI."""
        try:
            rsi_s = self._col(df, 'MTF RSI')
            if rsi_s is None or len(df) < self.DIV_LOOKBACK + 2:
                return False
            w       = df.tail(self.DIV_LOOKBACK + 1)
            prices  = w['close'].values.astype(float)
            rsis    = pd.Series(rsi_s.tail(self.DIV_LOOKBACK + 1).values).ffill().values.astype(float)
            cur_p, cur_r = prices[-1], rsis[-1]
            if cur_p <= 0 or cur_r <= 0:
                return False
            prior_p, prior_r = prices[:-1], rsis[:-1]
            pk = int(np.argmax(prior_p))
            pk_p, pk_r = prior_p[pk], prior_r[pk]
            return bool(
                cur_p >= pk_p * (1 - self.PRICE_NEAR_PEAK) and
                cur_r < pk_r - self.RSI_DIV_MIN_GAP and
                pk_r > 0
            )
        except Exception:
            return False

    def _rsid_div(self, df: pd.DataFrame) -> bool:
        """Bearish RSI Daily divergence (MTF RSI.1 column, forward-filled)."""
        try:
            rsi_s = self._col(df, 'MTF RSI.1')
            if rsi_s is None or len(df) < self.DIV_LOOKBACK + 2:
                return False
            w       = df.tail(self.DIV_LOOKBACK + 1)
            prices  = w['close'].values.astype(float)
            rsisd   = pd.Series(rsi_s.tail(self.DIV_LOOKBACK + 1).values).ffill().values.astype(float)
            cur_p, cur_rd = prices[-1], rsisd[-1]
            if cur_p <= 0 or cur_rd <= 0:
                return False
            prior_p, prior_rd = prices[:-1], rsisd[:-1]
            pk  = int(np.argmax(prior_p))
            pk_p, pk_rd = prior_p[pk], prior_rd[pk]
            return bool(
                cur_p >= pk_p * (1 - self.PRICE_NEAR_PEAK) and
                cur_rd < pk_rd - self.RSI_DIV_MIN_GAP and
                pk_rd > 0
            )
        except Exception:
            return False

    def _obv_div(self, df: pd.DataFrame) -> bool:
        """Bearish OBV divergence: price near local high but OBV below that high's OBV."""
        try:
            obv_s = self._col(df, 'OnBalanceVolume')
            if obv_s is None or len(df) < self.DIV_LOOKBACK + 2:
                return False
            w      = df.tail(self.DIV_LOOKBACK + 1)
            prices = w['close'].values.astype(float)
            obvs   = obv_s.tail(self.DIV_LOOKBACK + 1).values.astype(float)
            cur_p, cur_obv = prices[-1], obvs[-1]
            prior_p, prior_obv = prices[:-1], obvs[:-1]
            pk = int(np.argmax(prior_p))
            pk_p, pk_obv = prior_p[pk], prior_obv[pk]
            near_peak = cur_p >= pk_p * (1 - self.PRICE_NEAR_PEAK)
            obv_lower = cur_obv < pk_obv * 0.999   # even small divergence counts
            # also check OBV vs SMA20
            below_sma20 = False
            if len(df) >= 20:
                sma20 = obv_s.tail(20).mean()
                below_sma20 = bool(cur_obv < sma20)
            return bool(near_peak and (obv_lower or below_sma20))
        except Exception:
            return False

    def _macd_neg(self, df: pd.DataFrame) -> bool:
        try:
            col = self._col(df, 'Histogram')
            return bool(col is not None and self._safe(col.iloc[-1]) < 0)
        except Exception:
            return False

    def _loi_rolling(self, df: pd.DataFrame) -> bool:
        """LOI has rolled over: current LOI below recent peak by at least 2 points."""
        try:
            col = self._col(df, 'LOI')
            if col is None or len(df) < self.LOI_ROLL_LOOKBACK + 1:
                return False
            recent = col.tail(self.LOI_ROLL_LOOKBACK + 1).values.astype(float)
            return bool(recent[-1] < np.nanmax(recent[:-1]) - 2.0)
        except Exception:
            return False

    def _st_bear(self, df: pd.DataFrame) -> bool:
        try:
            col = self._col(df, 'Down Trend')
            if col is None:
                return False
            v = col.iloc[-1]
            return bool(v is not None and str(v).strip() not in ('', 'nan', 'NaN'))
        except Exception:
            return False

    def _st_bull(self, df: pd.DataFrame) -> bool:
        try:
            col = self._col(df, 'Up Trend')
            if col is None:
                return False
            v = col.iloc[-1]
            return bool(v is not None and str(v).strip() not in ('', 'nan', 'NaN'))
        except Exception:
            return False

    def _loi_now(self, df: pd.DataFrame) -> float:
        try:
            col = self._col(df, 'LOI')
            return self._safe(col.iloc[-1]) if col is not None and len(df) > 0 else 0.0
        except Exception:
            return 0.0

    # -- main compute -----------------------------------------------------------

    def compute(self, df: pd.DataFrame) -> PBearSignal:
        """
        Compute P-BEAR state for this asset using the last DIV_LOOKBACK bars.
        Returns a PBearSignal with full state + individual signal flags.
        """
        if df is None or len(df) < self.DIV_LOOKBACK:
            return PBearSignal(
                asset=self.asset, state=PBearState.INACTIVE,
                asset_class=self.asset_class, loi=0.0,
                watch_threshold=self.watch_threshold,
            )

        last      = df.iloc[-1]
        loi       = self._loi_now(df)
        price     = self._safe(last.get('close', 0))
        _rsi4h_col = self._col(df, 'MTF RSI')
        rsi_4h    = self._safe(_rsi4h_col.iloc[-1] if _rsi4h_col is not None else 0.0)
        _rsid_col  = self._col(df, 'MTF RSI.1')
        rsi_daily = self._safe(_rsid_col.iloc[-1] if _rsid_col is not None else 0.0)
        _macd_col  = self._col(df, 'Histogram')
        macd_hist = self._safe(_macd_col.iloc[-1] if _macd_col is not None else 0.0)

        # Compute individual signals
        macd_neg   = self._macd_neg(df)
        rsi4h_div  = self._rsi4h_div(df)
        rsid_div   = self._rsid_div(df)
        obv_div    = self._obv_div(df)
        loi_roll   = self._loi_rolling(df)
        st_bear    = self._st_bear(df)
        st_bull    = self._st_bull(df)

        sig = PBearSignal(
            asset=self.asset, asset_class=self.asset_class,
            loi=loi, watch_threshold=self.watch_threshold,
            macd_neg=macd_neg, rsi4h_div=rsi4h_div, rsid_div=rsid_div,
            obv_div=obv_div, loi_rolling=loi_roll, st_bear=st_bear,
            price=price, rsi_4h=rsi_4h, rsi_daily=rsi_daily, macd_hist=macd_hist,
            state=PBearState.INACTIVE,
        )

        # -- MOMENTUM (MSTR, TSLA) -----------------------------------------------
        if self.asset_class == 'MOMENTUM':
            if loi < self.watch_threshold:
                sig.state = PBearState.INACTIVE
            else:
                sig.state = PBearState.WATCH
                if loi > self.WATCH_DEFAULT and macd_neg:
                    sig.state = PBearState.FORMING
                    if rsi4h_div:
                        sig.state = PBearState.FORMING_PLUS
                        if rsid_div and loi_roll:
                            sig.state = PBearState.CONFIRMED
                            if obv_div:
                                sig.state = PBearState.CONFIRMED_PLUS
            # Invalidation: MACD back positive + price at/near 20-bar high
            if (sig.state.value >= PBearState.FORMING.value
                    and not macd_neg and not rsi4h_div):
                price_20h = float(df['close'].tail(20).max()) if 'close' in df.columns else price
                if price >= price_20h * 0.998:
                    sig.state = PBearState.INVALIDATED

        # -- BTC_CORRELATED (IBIT) -----------------------------------------------
        elif self.asset_class == 'BTC_CORRELATED':
            if loi < self.watch_threshold:
                sig.state = PBearState.INACTIVE
            else:
                sig.state = PBearState.WATCH
                if obv_div:
                    sig.state = PBearState.FORMING
                    if rsi4h_div:
                        sig.state = PBearState.FORMING_PLUS
                        if rsid_div:
                            sig.state = PBearState.CONFIRMED
            # Invalidation: OBV recovers
            if sig.state.value >= PBearState.FORMING.value and not obv_div:
                sig.state = PBearState.INVALIDATED

        # -- MR (SPY, QQQ, IWM) -------------------------------------------------
        elif self.asset_class == 'MR':
            if loi < self.watch_threshold:
                sig.state = PBearState.INACTIVE
            else:
                sig.state = PBearState.WATCH
                if rsi4h_div:
                    sig.state = PBearState.FORMING
                    if obv_div:
                        sig.state = PBearState.FORMING_PLUS
                        if rsid_div:
                            sig.state = PBearState.CONFIRMED
            # Invalidation: RSI4H recovers + price at/near new high
            if sig.state.value >= PBearState.FORMING.value and not rsi4h_div:
                price_20h = float(df['close'].tail(20).max()) if 'close' in df.columns else price
                if price >= price_20h * 0.998:
                    sig.state = PBearState.INVALIDATED

        # -- TRENDING (GLD) ------------------------------------------------------
        elif self.asset_class == 'TRENDING':
            if loi < self.watch_threshold:
                sig.state = PBearState.INACTIVE
            else:
                sig.state = PBearState.WATCH
                if obv_div and rsi4h_div:
                    sig.state = PBearState.FORMING
                    if st_bear:
                        sig.state = PBearState.CONFIRMED
            # Invalidation: Supertrend flips back BULL after CONFIRMED
            if sig.state.value >= PBearState.CONFIRMED.value and st_bull:
                sig.state = PBearState.INVALIDATED

        return sig
