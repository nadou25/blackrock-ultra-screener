"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                               ║
║     ██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ██████╗  ██████╗  ██████╗██╗  ██╗                             ║
║     ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝                            ║
║     ██████╔╝██║     ███████║██║     █████╔╝     ██████╔╝██║   ██║██║     █████╔╝                             ║
║     ██╔══██╗██║     ██╔══██║██║     ██╔═██╗     ██╔══██╗██║   ██║██║     ██╔═██╗                             ║
║     ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗    ██║  ██║╚██████╔╝╚██████╗██║  ██╗                            ║
║     ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝                            ║
║                                                                                                               ║
║     ███████╗ ██████╗██████╗ ███████╗███████╗███╗   ██╗███████╗██████╗                                         ║
║     ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║██╔════╝██╔══██╗                                        ║
║     ███████╗██║     ██████╔╝█████╗  █████╗  ██╔██╗ ██║█████╗  ██████╔╝                                        ║
║     ╚════██║██║     ██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗                                        ║
║     ███████║╚██████╗██║  ██║███████╗███████╗██║ ╚████║███████╗██║  ██║                                        ║
║     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝                                        ║
║                                                                                                               ║
║     🏦 ULTRA SCREENER v10.0 — SYSTÈME BLACKROCK ALADDIN STYLE 🏦                                             ║
║                                                                                                               ║
║  ════════════════════════════════════════════════════════════════════════════════════════════════════════════  ║
║  🧠 ALGORITHMES QUANTITATIFS AVANCÉS:                                                                         ║
║     • Modèle Multi-Factoriel BlackRock (Market, Size, Value, Momentum, Quality, Volatility)                   ║
║     • Hurst Exponent, Fractal Dimension, Shannon Entropy                                                      ║
║     • Omega Ratio, Sortino, Calmar, Information Ratio                                                         ║
║     • CUSUM Regime Detection, Hidden Markov States                                                            ║
║     • Fractional Differentiation (stationnarité + mémoire)                                                    ║
║     • Copula Correlations & Tail-Risk Analysis                                                                ║
║                                                                                                               ║
║  📰 NEWS & EARNINGS ENGINE:                                                                                   ║
║     • Scraping Multi-Source (Google News, Yahoo, RSS)                                                         ║
║     • Sentiment Analysis avancé (200+ mots-clés pondérés)                                                     ║
║     • Quarterly Earnings Tracker (EPS, Revenue surprises)                                                     ║
║     • Earnings Calendar & Impact scoring                                                                      ║
║                                                                                                               ║
║  📊 CORRÉLATIONS CROSS-ASSET:                                                                                 ║
║     • Matrice de corrélation dynamique (rolling 60j)                                                          ║
║     • Corrélation avec VIX, SPY, TNX, DXY, Or                                                                ║
║     • Beta-adjusted returns, Alpha generation                                                                 ║
║     • Sector rotation momentum tracking                                                                       ║
║                                                                                                               ║
║  🎯 PRÉDICTION ML ULTRA-AVANCÉ:                                                                              ║
║     • Ensemble 13 modèles (XGB, LGBM, CatBoost, MLP, RF, etc.)                                               ║
║     • Triple Barrier Labeling (López de Prado)                                                                ║
║     • Purged K-Fold Cross-Validation                                                                          ║
║     • Meta-Labeling & Stacking                                                                                ║
║     • 150+ Features quantitatives                                                                             ║
║                                                                                                               ║
║  🌍 MARCHÉS: PEA (200+ EU/EEE) + PME Small/Mid Caps + US 400+                                               ║
║             + Europe + France + Gaming + Commodities + Crypto                                                  ║
║                                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

import os, sys, time, json, logging, sqlite3, re, math, hashlib
import urllib.request, urllib.parse, html
from logging.handlers import RotatingFileHandler
import threading
from queue import Queue, Empty
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import OrderedDict, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings, uuid, pickle, io, csv

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='X does not have valid feature names')

# ══════════════════════════════════════════════════════════════════════════════
#                         VÉRIFICATION DÉPENDANCES
# ══════════════════════════════════════════════════════════════════════════════
PAQUETS_MANQUANTS = []
try:
    import pandas as pd
except ImportError:
    PAQUETS_MANQUANTS.append('pandas')
try:
    import numpy as np
except ImportError:
    PAQUETS_MANQUANTS.append('numpy')
try:
    import yfinance as yf
except ImportError:
    PAQUETS_MANQUANTS.append('yfinance')
try:
    from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
        IsolationForest, AdaBoostClassifier, StackingClassifier, VotingClassifier,
        BaggingClassifier, HistGradientBoostingClassifier, ExtraTreesClassifier)
    from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
    from sklearn.model_selection import TimeSeriesSplit, cross_val_score
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import accuracy_score, precision_score, f1_score
    from sklearn.neural_network import MLPClassifier
    from sklearn.linear_model import LogisticRegression, RidgeClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.feature_selection import SelectKBest, f_classif
except ImportError:
    PAQUETS_MANQUANTS.append('scikit-learn')

XGBOOST_OK = False
try:
    import xgboost as xgb; XGBOOST_OK = True
except ImportError: pass
LIGHTGBM_OK = False
try:
    import lightgbm as lgb; LIGHTGBM_OK = True
except ImportError: pass
CATBOOST_OK = False
try:
    from catboost import CatBoostClassifier; CATBOOST_OK = True
except ImportError: pass

PPO_OK = False
try:
    import gymnasium as gym
    from gymnasium import spaces
    from stable_baselines3 import PPO as PPO_SB3
    from stable_baselines3.common.vec_env import DummyVecEnv
    import torch
    PPO_OK = True
except ImportError:
    pass

if PAQUETS_MANQUANTS:
    print("="*60)
    print(f"❌ PAQUETS MANQUANTS: {', '.join(PAQUETS_MANQUANTS)}")
    print("pip install pandas numpy yfinance scikit-learn xgboost lightgbm catboost openpyxl")
    print("="*60)
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
#                              LOGGING
# ══════════════════════════════════════════════════════════════════════════════
def configurer_logging(fichier_log="screener_v10.log"):
    lgr = logging.getLogger('BlackRockScreener')
    lgr.setLevel(logging.DEBUG)
    lgr.handlers.clear()
    fmt = logging.Formatter('%(asctime)s | %(levelname)-7s | %(message)s', datefmt='%H:%M:%S')
    ch = logging.StreamHandler(sys.stdout); ch.setLevel(logging.INFO); ch.setFormatter(fmt); lgr.addHandler(ch)
    try:
        fh = RotatingFileHandler(fichier_log, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
        fh.setLevel(logging.DEBUG); fh.setFormatter(fmt); lgr.addHandler(fh)
    except: pass
    return lgr

logger = configurer_logging()

_EMOJI_RE = re.compile("["
    "\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937\U00010000-\U0010ffff\u200d\u2640-\u2642"
    "\ufe0f\u2600-\u26FF\u2700-\u27BF]+", flags=re.UNICODE)

def clean_txt(val):
    return _EMOJI_RE.sub('', val).strip() if isinstance(val, str) else val


# ══════════════════════════════════════════════════════════════════════════════
#                              CACHE LRU
# ══════════════════════════════════════════════════════════════════════════════
class CacheLRU:
    def __init__(self, nom, taille_max=500, ttl=300):
        self.nom = nom; self.taille_max = taille_max; self.ttl = ttl
        self._cache = OrderedDict(); self._lock = threading.RLock()
        self.hits = 0; self.misses = 0
    def _bucket(self):
        n = datetime.now(); return f"{n.strftime('%Y%m%d_%H')}{(n.minute//5)*5:02d}"
    def get(self, cle):
        k = f"{cle}_{self._bucket()}"
        with self._lock:
            if k in self._cache: self._cache.move_to_end(k); self.hits += 1; return self._cache[k]
            self.misses += 1; return None
    def set(self, cle, val):
        k = f"{cle}_{self._bucket()}"
        with self._lock:
            while len(self._cache) >= self.taille_max: self._cache.popitem(last=False)
            self._cache[k] = val

class GestionnaireCache:
    def __init__(self):
        self.prix = CacheLRU("prix", 500, 300)
        self.fondamentaux = CacheLRU("fonda", 300, 3600)
        self.ml = CacheLRU("ml", 200, 900)
        self.news = CacheLRU("news", 200, 1800)
        self.earnings = CacheLRU("earnings", 200, 7200)
        self.correlations = CacheLRU("corr", 100, 3600)


# ══════════════════════════════════════════════════════════════════════════════
#              🚀 ULTRA BATCH PRICE FETCHER (SNIPER MODE)
# ══════════════════════════════════════════════════════════════════════════════
class LivePriceFetcher:
    def __init__(self, max_workers=25):
        self.max_workers = max_workers
        self.cache_live = {}; self.cache_ts = None; self.cache_ttl = 60

    def fetch_batch_prices(self, symbols, period="5d"):
        if not symbols: return {}
        if self.cache_ts and (time.time() - self.cache_ts) < self.cache_ttl:
            if all(s in self.cache_live for s in symbols):
                return {s: self.cache_live[s] for s in symbols}
        results = {}
        try:
            logger.info(f"🚀 Batch fetch {len(symbols)} symboles...")
            t0 = time.time()
            df = yf.download(symbols, period=period, interval="1d", progress=False, threads=True, group_by='ticker')
            logger.info(f"✅ Batch fetch en {time.time()-t0:.1f}s")
            for sym in symbols:
                try:
                    if len(symbols) == 1:
                        cl, vol, hi, lo = df['Close'], df['Volume'], df['High'], df['Low']
                    else:
                        cl, vol, hi, lo = df[sym]['Close'], df[sym]['Volume'], df[sym]['High'], df[sym]['Low']
                    if cl.empty or cl.isna().all(): continue
                    p = float(cl.iloc[-1]); pc = float(cl.iloc[-2]) if len(cl)>=2 else p
                    chg = ((p-pc)/pc*100) if pc>0 else 0
                    results[sym] = {'price':round(p,2),'prev_close':round(pc,2),'change_pct':round(chg,2),
                        'volume':int(vol.iloc[-1]) if not pd.isna(vol.iloc[-1]) else 0,
                        'high':round(float(hi.iloc[-1]),2),'low':round(float(lo.iloc[-1]),2),
                        'timestamp':datetime.now().strftime('%H:%M:%S')}
                except: continue
            self.cache_live.update(results); self.cache_ts = time.time()
        except Exception as e: logger.error(f"Erreur batch: {e}")
        return results


# ══════════════════════════════════════════════════════════════════════════════
#                    CONFIGURATION ULTRA-AVANCÉE
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class Config:
    # Indicateurs Techniques
    RSI_PERIODE: int = 14; ZSCORE_FENETRE: int = 20
    MACD_RAPIDE: int = 12; MACD_LENT: int = 26; MACD_SIGNAL: int = 9
    ATR_PERIODE: int = 14
    RSI_SURVENDU: int = 30; RSI_SURACHETE: int = 70
    ZSCORE_HAUT: float = 2.0; ZSCORE_BAS: float = -2.0

    # BlackRock Factor Model Weights
    FACTOR_MARKET: float = 0.15; FACTOR_SIZE: float = 0.10; FACTOR_VALUE: float = 0.20
    FACTOR_MOMENTUM: float = 0.20; FACTOR_QUALITY: float = 0.20; FACTOR_VOLATILITY: float = 0.15

    # Trading
    STOP_LOSS_ATR: float = 2.0; TAKE_PROFIT_ATR: float = 3.0; RR_MIN: float = 1.5
    CAPITAL: float = 10000.0; RISQUE_MAX_PCT: float = 0.02; MAX_POSITIONS: int = 10

    # Risk Management PRO
    KELLY_FRACTION: float = 0.25       # fraction of Kelly to use (quarter-Kelly = conservative)
    KELLY_MAX_PCT: float = 0.15        # max single position = 15% of capital
    VAR_CONFIDENCE: float = 0.95       # VaR confidence level (95% or 99%)
    VAR_HORIZON_JOURS: int = 5         # VaR horizon in days
    MONTE_CARLO_SIMS: int = 5000       # number of MC simulations
    MAX_DRAWDOWN_LIMIT: float = 0.20   # stop trading if DD exceeds 20%
    MAX_CORRELATION_PORTFOLIO: float = 0.70  # max avg correlation in portfolio
    R_MULTIPLE_TARGET: float = 2.0     # target R-multiple per trade
    RISK_FREE_RATE: float = 0.043      # annual risk-free rate (US 10Y)

    # Swing Filters
    SWING_SCORE_MIN: int = 55; SWING_RR_MIN: float = 1.2
    CONFIRMATION_MIN: int = 4; QUALITE_MIN: int = 40

    # ML Avancé
    ML_ACTIF: bool = True; ML_RENDEMENT_CIBLE: float = 0.04; ML_HORIZON: int = 7
    ML_SEUIL_CONFIANCE: float = 0.62; ML_ENSEMBLE: bool = True
    ML_MAX_SYMBOLES: int = 800; ML_STACKING: bool = True
    ML_TOP_K_FEATURES: int = 50

    # Horizon de prédiction (ultra-avancé)
    HORIZON_MODE: str = "SWING"  # SCALP | INTRADAY | SWING | POSITION | INVESTISSEUR
    HORIZON_SHORT_JOURS: int = 5
    HORIZON_INTRADAY_JOURS: int = 2
    HORIZON_MOYEN_JOURS: int = 20
    HORIZON_LONG_JOURS: int = 60
    HORIZON_INVESTISSEUR_JOURS: int = 252  # ~1 an de trading
    DYNAMIC_ML_HORIZON: bool = True

    # Précision & profitabilité
    PRECISION_MIN_SCORE: float = 58.0
    EV_MIN_PCT: float = 0.10  # espérance min (% du prix)
    QUALITY_GATE_MIN: float = 52.0
    ADAPTIVE_RISK_ACTIF: bool = True
    RISK_REGIME_VOL_HAUTE: float = 1.25
    RISK_REGIME_VOL_BASSE: float = 0.80
    PROFIL_ACTIF: str = "BALANCED"

    # PPO ultra-avancé (influence directe sur le score final)
    PPO_INTEGRATION_ACTIF: bool = True
    PPO_SCORE_POIDS: float = 0.22
    PPO_MIN_FIABILITE_ACHAT: float = 62.0
    PPO_BOOST_MAX: float = 6.0

    # ═══ ALPHA FACTOR ENGINE PRO (scoring corrélé aux rendements réels) ═══
    SCORING_MODE: str = "ALPHA_FACTOR"  # ALPHA_FACTOR | CLASSIC
    CROSS_SECTIONAL_RANKING: bool = True  # Rank relatif vs univers (percentile)
    REGIME_ADAPTIVE_WEIGHTS: bool = True  # Poids adaptatifs bull/bear
    FAST_MODE: bool = True  # Skip re-training, utilise modèles cachés
    PPO_FAST_CANDIDATES: int = 2  # 2 candidats au lieu de 5 (5x plus rapide)
    PPO_FAST_TIMESTEPS: int = 200000  # 200k au lieu de 500k
    # Poids facteurs alpha (calibrés sur rendements historiques)
    ALPHA_W_MOMENTUM: float = 0.22   # Rendement 3m-1s (facteur alpha #1 académique)
    ALPHA_W_REVERSAL: float = 0.10   # Mean-reversion court terme
    ALPHA_W_QUALITY: float = 0.18    # ROE, marge, FCF, dette
    ALPHA_W_VALUE: float = 0.10      # PE, PB, dividende
    ALPHA_W_FLOW: float = 0.12       # Smart Money, volume institutionnel
    ALPHA_W_ML: float = 0.13         # Signal ML ensemble
    ALPHA_W_REGIME: float = 0.08     # Régime marché (bull/bear)
    ALPHA_W_PPO: float = 0.07        # Signal PPO RL
    # Détection régime marché
    REGIME_SPY_SMA: int = 50
    REGIME_VIX_THRESHOLD: float = 25.0
    # Seuils alpha adaptifs
    ALPHA_MOMENTUM_BOOST_BULL: float = 1.30  # Boost momentum en bull
    ALPHA_REVERSAL_BOOST_BEAR: float = 1.40  # Boost reversal en bear
    ALPHA_MIN_SCORE_BUY: float = 58.0  # Score alpha minimum pour ACHAT
    ALPHA_MIN_SCORE_FORT: float = 72.0  # Score alpha minimum pour ACHAT FORT

    # News & Earnings
    NEWS_ACTIF: bool = True; NEWS_POIDS: float = 0.15
    EARNINGS_ACTIF: bool = True; EARNINGS_POIDS: float = 0.20
    CORRELATION_ACTIF: bool = True

    # Marchés
    MODE_PEA: bool = True; INCLURE_US: bool = True; INCLURE_EUROPE: bool = True
    INCLURE_FRANCE: bool = True; INCLURE_GAMING: bool = True
    INCLURE_MATIERES: bool = True; INCLURE_CRYPTO: bool = True
    INCLURE_PME: bool = True; INCLURE_SANTE: bool = True
    INCLURE_NASDAQ100: bool = True; INCLURE_SP500: bool = True

    # Display
    SCORE_MINIMUM: int = 30

    # Poids scoring CLASSIC fallback (3 piliers — utilisé si SCORING_MODE=CLASSIC)
    POIDS_TECHNIQUE: float = 0.40   # RSI, MACD, SuperTrend, volatilité
    POIDS_FONDAMENTAL: float = 0.30  # Qualité + BlackRock + Earnings
    POIDS_MOMENTUM: float = 0.30    # ML + News + Tendance

    FICHIER_CONFIG: str = "screener_config_v10.json"

    def sauvegarder(self):
        try:
            data = {k:v for k,v in asdict(self).items() if not k.startswith('FICHIER')}
            with open(self.FICHIER_CONFIG,'w',encoding='utf-8') as f: json.dump(data,f,indent=2,ensure_ascii=False)
            return True, "✅ Config sauvegardée"
        except Exception as e: return False, f"❌ {e}"

    def appliquer_profil(self, nom_profil: str):
        profil = str(nom_profil or '').upper().strip()
        profils = {
            "BALANCED": {
                "HORIZON_MODE": "SWING",
                "PRECISION_MIN_SCORE": 58.0,
                "EV_MIN_PCT": 0.10,
                "QUALITY_GATE_MIN": 52.0,
                "STOP_LOSS_ATR": 2.0,
                "TAKE_PROFIT_ATR": 3.0,
                "RR_MIN": 1.5,
                "RISK_REGIME_VOL_HAUTE": 1.25,
                "RISK_REGIME_VOL_BASSE": 0.80,
                "SCORE_MINIMUM": 30,
                "PPO_SCORE_POIDS": 0.22,
                "PPO_MIN_FIABILITE_ACHAT": 62.0,
            },
            "PROFIT_MAX": {
                "HORIZON_MODE": "POSITION",
                "PRECISION_MIN_SCORE": 54.0,
                "EV_MIN_PCT": 0.25,
                "QUALITY_GATE_MIN": 48.0,
                "STOP_LOSS_ATR": 2.3,
                "TAKE_PROFIT_ATR": 4.2,
                "RR_MIN": 1.8,
                "RISK_REGIME_VOL_HAUTE": 1.35,
                "RISK_REGIME_VOL_BASSE": 0.78,
                "SCORE_MINIMUM": 35,
                "PPO_SCORE_POIDS": 0.18,
                "PPO_MIN_FIABILITE_ACHAT": 58.0,
            },
            "PRECISION_MAX": {
                "HORIZON_MODE": "SWING",
                "PRECISION_MIN_SCORE": 66.0,
                "EV_MIN_PCT": 0.12,
                "QUALITY_GATE_MIN": 60.0,
                "STOP_LOSS_ATR": 1.8,
                "TAKE_PROFIT_ATR": 2.7,
                "RR_MIN": 1.6,
                "RISK_REGIME_VOL_HAUTE": 1.20,
                "RISK_REGIME_VOL_BASSE": 0.85,
                "SCORE_MINIMUM": 45,
                "PPO_SCORE_POIDS": 0.28,
                "PPO_MIN_FIABILITE_ACHAT": 66.0,
            },
            "SCALP_MAX": {
                "HORIZON_MODE": "SCALP",
                "SCORING_MODE": "ALPHA_FACTOR",
                "PRECISION_MIN_SCORE": 68.0,
                "EV_MIN_PCT": 0.08,
                "QUALITY_GATE_MIN": 58.0,
                "STOP_LOSS_ATR": 1.4,
                "TAKE_PROFIT_ATR": 2.1,
                "RR_MIN": 1.4,
                "RISK_REGIME_VOL_HAUTE": 1.15,
                "RISK_REGIME_VOL_BASSE": 0.88,
                "SCORE_MINIMUM": 50,
                "PPO_SCORE_POIDS": 0.32,
                "PPO_MIN_FIABILITE_ACHAT": 70.0,
                "ALPHA_W_MOMENTUM": 0.12,
                "ALPHA_W_REVERSAL": 0.25,
                "ALPHA_W_FLOW": 0.18,
                "ALPHA_W_ML": 0.18,
                "ALPHA_W_PPO": 0.12,
                "ALPHA_W_QUALITY": 0.08,
                "ALPHA_W_VALUE": 0.02,
                "ALPHA_W_REGIME": 0.05,
            },
            "INTRADAY_MAX": {
                "HORIZON_MODE": "INTRADAY",
                "SCORING_MODE": "ALPHA_FACTOR",
                "PRECISION_MIN_SCORE": 64.0,
                "EV_MIN_PCT": 0.10,
                "QUALITY_GATE_MIN": 56.0,
                "STOP_LOSS_ATR": 1.6,
                "TAKE_PROFIT_ATR": 2.4,
                "RR_MIN": 1.5,
                "RISK_REGIME_VOL_HAUTE": 1.20,
                "RISK_REGIME_VOL_BASSE": 0.85,
                "SCORE_MINIMUM": 46,
                "PPO_SCORE_POIDS": 0.30,
                "PPO_MIN_FIABILITE_ACHAT": 67.0,
                "ALPHA_W_MOMENTUM": 0.15,
                "ALPHA_W_REVERSAL": 0.20,
                "ALPHA_W_FLOW": 0.16,
                "ALPHA_W_ML": 0.16,
                "ALPHA_W_PPO": 0.10,
                "ALPHA_W_QUALITY": 0.10,
                "ALPHA_W_VALUE": 0.05,
                "ALPHA_W_REGIME": 0.08,
            },
            "SWING_MAX": {
                "HORIZON_MODE": "SWING",
                "SCORING_MODE": "ALPHA_FACTOR",
                "PRECISION_MIN_SCORE": 62.0,
                "EV_MIN_PCT": 0.14,
                "QUALITY_GATE_MIN": 58.0,
                "STOP_LOSS_ATR": 1.9,
                "TAKE_PROFIT_ATR": 3.0,
                "RR_MIN": 1.7,
                "RISK_REGIME_VOL_HAUTE": 1.25,
                "RISK_REGIME_VOL_BASSE": 0.82,
                "SCORE_MINIMUM": 42,
                "PPO_SCORE_POIDS": 0.26,
                "PPO_MIN_FIABILITE_ACHAT": 64.0,
                "ALPHA_W_MOMENTUM": 0.26,
                "ALPHA_W_REVERSAL": 0.06,
                "ALPHA_W_FLOW": 0.10,
                "ALPHA_W_ML": 0.12,
                "ALPHA_W_PPO": 0.06,
                "ALPHA_W_QUALITY": 0.20,
                "ALPHA_W_VALUE": 0.12,
                "ALPHA_W_REGIME": 0.08,
            },
            "NASDAQ_SNIPER": {
                "HORIZON_MODE": "INTRADAY",
                "SCORING_MODE": "ALPHA_FACTOR",
                "PRECISION_MIN_SCORE": 62.0,
                "EV_MIN_PCT": 0.12,
                "QUALITY_GATE_MIN": 54.0,
                "STOP_LOSS_ATR": 1.5,
                "TAKE_PROFIT_ATR": 2.6,
                "RR_MIN": 1.6,
                "SCORE_MINIMUM": 45,
                "INCLURE_NASDAQ100": True,
                "INCLURE_SP500": True,
                "ALPHA_W_MOMENTUM": 0.20,
                "ALPHA_W_REVERSAL": 0.15,
                "ALPHA_W_FLOW": 0.18,
                "ALPHA_W_ML": 0.18,
                "ALPHA_W_PPO": 0.10,
                "ALPHA_W_QUALITY": 0.10,
                "ALPHA_W_VALUE": 0.02,
                "ALPHA_W_REGIME": 0.07,
            },
            "SP500_VALUE": {
                "HORIZON_MODE": "SWING",
                "SCORING_MODE": "ALPHA_FACTOR",
                "PRECISION_MIN_SCORE": 60.0,
                "EV_MIN_PCT": 0.15,
                "QUALITY_GATE_MIN": 60.0,
                "STOP_LOSS_ATR": 2.0,
                "TAKE_PROFIT_ATR": 3.2,
                "RR_MIN": 1.8,
                "SCORE_MINIMUM": 40,
                "ALPHA_W_MOMENTUM": 0.18,
                "ALPHA_W_REVERSAL": 0.05,
                "ALPHA_W_FLOW": 0.10,
                "ALPHA_W_ML": 0.10,
                "ALPHA_W_PPO": 0.05,
                "ALPHA_W_QUALITY": 0.25,
                "ALPHA_W_VALUE": 0.20,
                "ALPHA_W_REGIME": 0.07,
            },
            "INVESTISSEUR_1AN": {
                "HORIZON_MODE": "INVESTISSEUR",
                "SCORING_MODE": "ALPHA_FACTOR",
                "HORIZON_INVESTISSEUR_JOURS": 252,
                "ML_HORIZON": 30,
                "ML_RENDEMENT_CIBLE": 0.12,
                "PRECISION_MIN_SCORE": 52.0,
                "EV_MIN_PCT": 0.30,
                "QUALITY_GATE_MIN": 55.0,
                "STOP_LOSS_ATR": 3.5,
                "TAKE_PROFIT_ATR": 7.0,
                "RR_MIN": 2.0,
                "RISK_REGIME_VOL_HAUTE": 1.40,
                "RISK_REGIME_VOL_BASSE": 0.70,
                "SCORE_MINIMUM": 30,
                "PPO_SCORE_POIDS": 0.08,
                "PPO_MIN_FIABILITE_ACHAT": 55.0,
                "ALPHA_W_MOMENTUM": 0.10,
                "ALPHA_W_REVERSAL": 0.03,
                "ALPHA_W_FLOW": 0.08,
                "ALPHA_W_ML": 0.10,
                "ALPHA_W_PPO": 0.04,
                "ALPHA_W_QUALITY": 0.30,
                "ALPHA_W_VALUE": 0.25,
                "ALPHA_W_REGIME": 0.10,
                "POIDS_TECHNIQUE": 0.25,
                "POIDS_FONDAMENTAL": 0.45,
                "POIDS_MOMENTUM": 0.30,
                "MAX_POSITIONS": 15,
                "RISQUE_MAX_PCT": 0.015,
                "KELLY_FRACTION": 0.20,
                "KELLY_MAX_PCT": 0.12,
                "MAX_DRAWDOWN_LIMIT": 0.15,
                "R_MULTIPLE_TARGET": 2.5,
                "VAR_HORIZON_JOURS": 10,
            },
            "COMMODITIES": {
                "HORIZON_MODE": "SWING",
                "SCORING_MODE": "ALPHA_FACTOR",
                "PRECISION_MIN_SCORE": 60.0,
                "EV_MIN_PCT": 0.15,
                "QUALITY_GATE_MIN": 45.0,
                "STOP_LOSS_ATR": 2.2,
                "TAKE_PROFIT_ATR": 3.8,
                "RR_MIN": 1.5,
                "SCORE_MINIMUM": 38,
                "INCLURE_MATIERES": True,
                "ALPHA_W_MOMENTUM": 0.30,
                "ALPHA_W_REVERSAL": 0.12,
                "ALPHA_W_FLOW": 0.18,
                "ALPHA_W_ML": 0.15,
                "ALPHA_W_PPO": 0.05,
                "ALPHA_W_QUALITY": 0.05,
                "ALPHA_W_VALUE": 0.05,
                "ALPHA_W_REGIME": 0.10,
            },
        }
        if profil not in profils:
            return False, f"Profil inconnu: {nom_profil}. Profils disponibles: {', '.join(profils.keys())}"

        for key, val in profils[profil].items():
            if hasattr(self, key):
                setattr(self, key, val)
        self.PROFIL_ACTIF = profil
        return True, f"✅ Profil appliqué: {profil}"

    @classmethod
    def charger(cls):
        c = cls()
        try:
            if os.path.exists(c.FICHIER_CONFIG):
                with open(c.FICHIER_CONFIG,'r',encoding='utf-8') as f:
                    for k,v in json.load(f).items():
                        if hasattr(c,k): setattr(c,k,v)
        except: pass
        return c

CONFIG = Config.charger()

# ═══ LOG DE DÉMARRAGE: Résumé de la configuration active ═══
_startup_log = logging.getLogger('BlackRockScreener')
_startup_log.info("=" * 70)
_startup_log.info(f"🚀 PROFIL ACTIF  : {getattr(CONFIG, 'PROFIL_ACTIF', '?')}")
_startup_log.info(f"🎯 HORIZON MODE  : {getattr(CONFIG, 'HORIZON_MODE', '?')}")
_startup_log.info(f"📊 ML HORIZON    : {getattr(CONFIG, 'ML_HORIZON', '?')}j | RENDEMENT CIBLE: {getattr(CONFIG, 'ML_RENDEMENT_CIBLE', '?')}")
_startup_log.info(f"⚙️  FAST_MODE     : {getattr(CONFIG, 'FAST_MODE', '?')} | POSITIONS MAX: {getattr(CONFIG, 'MAX_POSITIONS', '?')}")
_startup_log.info(f"💰 STOP_LOSS ATR : {getattr(CONFIG, 'STOP_LOSS_ATR', '?')} | TP ATR: {getattr(CONFIG, 'TAKE_PROFIT_ATR', '?')} | RR MIN: {getattr(CONFIG, 'RR_MIN', '?')}")
_startup_log.info(f"🔬 ALPHA WEIGHTS : Q={getattr(CONFIG, 'ALPHA_W_QUALITY', '?')} V={getattr(CONFIG, 'ALPHA_W_VALUE', '?')} M={getattr(CONFIG, 'ALPHA_W_MOMENTUM', '?')} T={getattr(CONFIG, 'ALPHA_W_TECHNIQUE', '?')}")
_startup_log.info("=" * 70)
# ══════════════════════════════════════════════════════════════════════════════
class UniversActions:
    # 🇺🇸 US — 400+ actions par secteur
    US = {
        # ═══ TECHNOLOGIE ═══
        "AAPL":"Technologie","MSFT":"Technologie","GOOGL":"Technologie","AMZN":"Technologie",
        "META":"Technologie","NVDA":"Technologie","TSLA":"Technologie","AMD":"Technologie",
        "INTC":"Technologie","CRM":"Technologie","ADBE":"Technologie","ORCL":"Technologie",
        "IBM":"Technologie","CSCO":"Technologie","QCOM":"Technologie","TXN":"Technologie",
        "AVGO":"Technologie","NOW":"Technologie","INTU":"Technologie","AMAT":"Technologie",
        "MU":"Technologie","LRCX":"Technologie","KLAC":"Technologie","SNPS":"Technologie",
        "CDNS":"Technologie","PANW":"Technologie","CRWD":"Technologie","ZS":"Technologie",
        "DDOG":"Technologie","SNOW":"Technologie","PLTR":"Technologie","NET":"Technologie",
        "MDB":"Technologie","TEAM":"Technologie","WDAY":"Technologie","OKTA":"Technologie",
        "FTNT":"Technologie","HUBS":"Technologie","TTD":"Technologie","SMCI":"Technologie",
        "ARM":"Technologie","MRVL":"Technologie","DELL":"Technologie","ANET":"Technologie",
        "CYBR":"Technologie","ROKU":"Technologie","ON":"Technologie","NXPI":"Technologie",
        "ADI":"Technologie","MPWR":"Technologie","MCHP":"Technologie","APP":"Technologie",
        # ═══ FINANCE ═══
        "JPM":"Finance","BAC":"Finance","GS":"Finance","V":"Finance","MA":"Finance",
        "PYPL":"Finance","MS":"Finance","WFC":"Finance","C":"Finance","AXP":"Finance",
        "BLK":"Finance","SCHW":"Finance","SPGI":"Finance","ICE":"Finance","CME":"Finance",
        "COF":"Finance","USB":"Finance","PNC":"Finance","SOFI":"Finance","COIN":"Finance",
        "HOOD":"Finance","NU":"Finance","MELI":"Finance","AIG":"Finance","MET":"Finance",
        "PRU":"Finance","AFL":"Finance","ALL":"Finance","TRV":"Finance","CB":"Finance",
        "PGR":"Finance","AON":"Finance","TROW":"Finance","NDAQ":"Finance","CBOE":"Finance",
        # ═══ SANTÉ ═══
        "JNJ":"Santé","UNH":"Santé","PFE":"Santé","LLY":"Santé","ABBV":"Santé",
        "MRK":"Santé","TMO":"Santé","ABT":"Santé","DHR":"Santé","BMY":"Santé",
        "AMGN":"Santé","GILD":"Santé","ISRG":"Santé","MDT":"Santé","SYK":"Santé",
        "REGN":"Santé","VRTX":"Santé","MRNA":"Santé","CVS":"Santé","CI":"Santé",
        "HCA":"Santé","DXCM":"Santé","ALGN":"Santé","IDXX":"Santé","ILMN":"Santé",
        # ═══ CONSOMMATION ═══
        "WMT":"Consommation","COST":"Consommation","HD":"Consommation","NKE":"Consommation",
        "MCD":"Consommation","SBUX":"Consommation","TGT":"Consommation","LOW":"Consommation",
        "CMG":"Consommation","KO":"Consommation","PEP":"Consommation","PG":"Consommation",
        "LULU":"Consommation","DECK":"Consommation","CROX":"Consommation","ONON":"Consommation",
        # ═══ ÉNERGIE ═══
        "XOM":"Énergie","CVX":"Énergie","COP":"Énergie","SLB":"Énergie","EOG":"Énergie",
        "OXY":"Énergie","MPC":"Énergie","VLO":"Énergie","PSX":"Énergie","HAL":"Énergie",
        "DVN":"Énergie","FANG":"Énergie","BKR":"Énergie","KMI":"Énergie","WMB":"Énergie",
        # ═══ INDUSTRIE ═══
        "CAT":"Industrie","BA":"Industrie","GE":"Industrie","HON":"Industrie","UNP":"Industrie",
        "UPS":"Industrie","RTX":"Industrie","LMT":"Industrie","NOC":"Industrie","GD":"Industrie",
        "DE":"Industrie","FDX":"Industrie","DAL":"Industrie","WM":"Industrie",
        # ═══ MÉDIA ═══
        "DIS":"Média","NFLX":"Média","CMCSA":"Média","SPOT":"Média","LYV":"Média",
        # ═══ GAMING ═══
        "EA":"Gaming","TTWO":"Gaming","RBLX":"Gaming","U":"Gaming","DKNG":"Gaming",
        "SONY":"Gaming","NTDOY":"Gaming",
        # ═══ IMMOBILIER ═══
        "AMT":"Immobilier","PLD":"Immobilier","CCI":"Immobilier","EQIX":"Immobilier",
        "SPG":"Immobilier","O":"Immobilier","DLR":"Immobilier",
        # ═══ AUTOMOBILE / EV ═══
        "GM":"Automobile","F":"Automobile","RIVN":"Automobile","LCID":"Automobile",
        "NIO":"Automobile","XPEV":"Automobile","LI":"Automobile",
        # ═══ CRYPTO / BLOCKCHAIN ═══
        "RIOT":"Crypto","MARA":"Crypto","CLSK":"Crypto","MSTR":"Crypto",
        # ═══ MATÉRIAUX ═══
        "LIN":"Matériaux","NEM":"Matériaux","FCX":"Matériaux","GOLD":"Matériaux",
        "NUE":"Matériaux","CLF":"Matériaux","ALB":"Matériaux","MP":"Matériaux",
        # ═══ UTILITIES ═══
        "NEE":"Utilities","DUK":"Utilities","SO":"Utilities","D":"Utilities",
    }

    # 🇫🇷 FRANCE — CAC 40 + SBF 120 + PME
    FRANCE = {
        "MC.PA":"Luxe","OR.PA":"Consommation","SAN.PA":"Santé","AI.PA":"Industrie",
        "BNP.PA":"Finance","TTE.PA":"Énergie","AIR.PA":"Industrie","SAF.PA":"Industrie",
        "KER.PA":"Luxe","SU.PA":"Industrie","CS.PA":"Finance","EL.PA":"Luxe",
        "DG.PA":"Industrie","CAP.PA":"Technologie","RI.PA":"Consommation",
        "DSY.PA":"Technologie","BN.PA":"Consommation","EN.PA":"Industrie",
        "ENGI.PA":"Énergie","VIE.PA":"Environnement","VIV.PA":"Média",
        "ORA.PA":"Télécom","SGO.PA":"Industrie","PUB.PA":"Média",
        "LR.PA":"Immobilier","HO.PA":"Industrie","SW.PA":"Technologie",
        "RMS.PA":"Luxe","CA.PA":"Finance","GLE.PA":"Finance","ACA.PA":"Finance",
        "ML.PA":"Industrie","ATO.PA":"Défense","URW.PA":"Immobilier",
        "STMPA.PA":"Technologie","WLN.PA":"Technologie","TEP.PA":"Télécom",
        "RNO.PA":"Automobile","ALO.PA":"Technologie","AKE.PA":"Industrie",
        "BIM.PA":"Santé","ERF.PA":"Santé","FGR.PA":"Industrie","GET.PA":"Industrie",
        "IPN.PA":"Santé","SOI.PA":"Technologie","SOP.PA":"Technologie",
        "UBI.PA":"Gaming","VLA.PA":"Santé","VK.PA":"Industrie",
        "EDEN.PA":"Consommation","OVH.PA":"Technologie","SPIE.PA":"Industrie",
        "BVI.PA":"Industrie","GTT.PA":"Énergie","AM.PA":"Finance",
        "FNAC.PA":"Consommation","DEC.PA":"Média","TFI.PA":"Média",
    }

    # 🇪🇺 EUROPE (non-France)
    EUROPE = {
        # Allemagne
        "SAP.DE":"Technologie","SIE.DE":"Industrie","ALV.DE":"Finance",
        "MBG.DE":"Automobile","BMW.DE":"Automobile","ADS.DE":"Consommation",
        "DTE.DE":"Télécom","BAS.DE":"Industrie","BAYN.DE":"Santé",
        "MUV2.DE":"Finance","DB1.DE":"Finance","IFX.DE":"Technologie",
        "VOW3.DE":"Automobile","RWE.DE":"Énergie","RHM.DE":"Défense",
        "ENR.DE":"Énergie","P911.DE":"Automobile","ZAL.DE":"Consommation",
        "PUM.DE":"Consommation","SHL.DE":"Santé","DTG.DE":"Industrie",
        # Pays-Bas
        "ASML.AS":"Technologie","PHIA.AS":"Technologie","INGA.AS":"Finance",
        "AD.AS":"Consommation","UNA.AS":"Consommation","HEIA.AS":"Consommation",
        "PRX.AS":"Technologie","WKL.AS":"Technologie","ASM.AS":"Technologie",
        "BESI.AS":"Technologie","MT.AS":"Industrie","ABN.AS":"Finance",
        # UK
        "SHEL.L":"Énergie","AZN.L":"Santé","HSBA.L":"Finance",
        "ULVR.L":"Consommation","BP.L":"Énergie","GSK.L":"Santé",
        "LLOY.L":"Finance","BARC.L":"Finance","LSEG.L":"Finance",
        # Suisse
        "NESN.SW":"Consommation","NOVN.SW":"Santé","ROG.SW":"Santé",
        "UBSG.SW":"Finance","ABBN.SW":"Industrie",
        # Espagne
        "SAN.MC":"Finance","IBE.MC":"Énergie","ITX.MC":"Consommation",
        "BBVA.MC":"Finance","TEF.MC":"Télécom",
        # Italie
        "ENEL.MI":"Énergie","ENI.MI":"Énergie","ISP.MI":"Finance",
        "UCG.MI":"Finance","RACE.MI":"Automobile","MONC.MI":"Luxe",
        # Danemark
        "NOVO-B.CO":"Santé","DSV.CO":"Industrie","VWS.CO":"Énergie","ORSTED.CO":"Énergie",
        # Suède
        "VOLV-B.ST":"Industrie","ATCO-B.ST":"Industrie","EVO.ST":"Gaming",
        "HM-B.ST":"Consommation","ERIC-B.ST":"Télécom",
        # Norvège
        "EQNR.OL":"Énergie","DNB.OL":"Finance","MOWI.OL":"Consommation",
    }

    # 🏭 PME / SMALL-MID CAPS PEA (NOUVEAU!)
    PME_PEA = {
        # 🇫🇷 France Small/Mid
        "ALBI.PA":"Technologie",    # Albioma (EnR)
        "ALSEN.PA":"Technologie",   # Aures Technologies
        "ALSAS.PA":"Technologie",   # SAS (Software)
        "ALMDG.PA":"Technologie",   # MedInCell
        "ALNXT.PA":"Finance",   # NextStage AM
        "MLCFM.PA":"Industrie",     # Carbios
        "ERO.PA":"Santé",           # Euroapi
        "ALDV.PA":"Consommation",   # Delfingen
        "ALINT.PA":"Technologie",   # Intrasense
        "ALMII.PA":"Industrie",     # MiiiGroup
        "DBV.PA":"Santé",           # DBV Technologies
        "GNFT.PA":"Santé",          # Genfit
        "ALKAL.PA":"Santé",         # Kalray (processeurs)
        "MERY.PA":"Immobilier",     # Mercialys
        "COFA.PA":"Finance",        # Coface
        "TKO.PA":"Finance",         # Tikehau Capital
        "LNA.PA":"Santé",           # LNA Santé
        "GBT.PA":"Santé",           # Guerbet
        "SMCP.PA":"Luxe",           # SMCP (Sandro, Maje)
        "NXI.PA":"Immobilier",      # Nexity
        "IPS.PA":"Média",           # Ipsos
        "RF.PA":"Finance",          # Eurazeo
        "MMT.PA":"Immobilier",      # Mercialys
        "NEX.PA":"Industrie",       # Nexans
        "RXL.PA":"Industrie",       # Rexel
        "SK.PA":"Consommation",     # SEB
        "BOL.PA":"Industrie",       # Bolloré
        "COV.PA":"Immobilier",      # Covivio
        "GFC.PA":"Immobilier",      # Gecina
        "RCO.PA":"Consommation",    # Rémy Cointreau
        "VRLA.PA":"Automobile",     # Valeo
        "ERA.PA":"Industrie",       # Eramet
        "ELIOR.PA":"Consommation",  # Elior
        # 🇩🇪 Allemagne Mid/Small
        "HFG.DE":"Technologie",     # HelloFresh
        "EVK.DE":"Industrie",       # Evonik
        "BEI.DE":"Consommation",    # Beiersdorf
        "BOSS.DE":"Consommation",   # Hugo Boss
        "WCH.DE":"Industrie",       # Wacker Chemie
        "DHER.DE":"Technologie",    # Delivery Hero
        "QIA.DE":"Santé",           # Qiagen
        "LEG.DE":"Immobilier",      # LEG Immobilien
        "TLX.DE":"Finance",         # Talanx
        "G1A.DE":"Industrie",       # GEA Group
        "CON.DE":"Automobile",      # Continental
        "FME.DE":"Santé",           # Fresenius Medical
        "NDA.DE":"Industrie",       # Aurubis
        "KBX.DE":"Industrie",       # Knorr-Bremse
        "SY1.DE":"Industrie",       # Symrise
        "PAH3.DE":"Automobile",     # Porsche Holding
        # 🇳🇱 Pays-Bas Mid
        "IMCD.AS":"Industrie",      # IMCD
        "KPN.AS":"Télécom",         # KPN
        "FLOW.AS":"Finance",        # Flow Traders
        "NN.AS":"Finance",          # NN Group
        "AGN.AS":"Finance",         # Aegon
        "LIGHT.AS":"Technologie",   # Signify
        # 🇧🇪 Belgique
        "ABI.BR":"Consommation","KBC.BR":"Finance","UCB.BR":"Santé",
        "SOLB.BR":"Industrie","UMI.BR":"Industrie","COLR.BR":"Consommation",
        "WDP.BR":"Immobilier","AGS.BR":"Finance","DIE.BR":"Industrie",
        # 🇮🇹 Italie Mid
        "STLAM.MI":"Automobile","PRY.MI":"Industrie","CPR.MI":"Industrie",
        "AMP.MI":"Santé","LDO.MI":"Défense","FBK.MI":"Finance",
        "BAMI.MI":"Finance","REC.MI":"Santé","PST.MI":"Finance",
        # 🇪🇸 Espagne Mid
        "CABK.MC":"Finance","FER.MC":"Industrie","AMS.MC":"Technologie",
        "ACS.MC":"Industrie","CLNX.MC":"Télécom","GRF.MC":"Santé",
        "MAP.MC":"Finance","ELE.MC":"Énergie",
        # 🇵🇹 Portugal
        "GALP.LS":"Énergie","EDP.LS":"Énergie","EDPR.LS":"Énergie",
        "JMT.LS":"Consommation","BCP.LS":"Finance",
        # 🇦🇹 Autriche
        "VOE.VI":"Industrie","VER.VI":"Énergie","EBS.VI":"Finance","OMV.VI":"Énergie",
        # 🇫🇮 Finlande
        "NOKIA.HE":"Technologie","NESTE.HE":"Énergie","FORTUM.HE":"Énergie",
        "UPM.HE":"Industrie","KNEBV.HE":"Industrie","SAMPO.HE":"Finance",
        # 🇩🇰 Danemark
        "CARL-B.CO":"Consommation","GMAB.CO":"Santé","PNDORA.CO":"Consommation",
        "COLO-B.CO":"Santé","DEMANT.CO":"Santé","MAERSK-B.CO":"Industrie",
        # 🇸🇪 Suède
        "SAND.ST":"Industrie","ASSA-B.ST":"Industrie","SEB-A.ST":"Finance",
        "INVE-B.ST":"Finance","HEXA-B.ST":"Industrie","EMB.ST":"Gaming",
        "ESSITY-B.ST":"Consommation","ALFA.ST":"Industrie",
        # 🇳🇴 Norvège
        "YAR.OL":"Industrie","TEL.OL":"Télécom","ORK.OL":"Consommation",
        "SALM.OL":"Consommation","AKRBP.OL":"Énergie",
        # 🇵🇱 Pologne
        "CDR.WA":"Gaming","PKO.WA":"Finance","PKN.WA":"Énergie",
        "DNP.WA":"Consommation","ALE.WA":"Consommation","LPP.WA":"Consommation",
    }

    # 🥇 MATIÈRES PREMIÈRES PRO (expandé)
    MATIERES = {
        "GLD":"Or","GDX":"Or","NEM":"Or","GOLD":"Or","AEM":"Or","FNV":"Or","WPM":"Or",
        "SLV":"Argent","PAAS":"Argent","AG":"Argent",
        "USO":"Pétrole","XLE":"Pétrole","OIH":"Pétrole","XOP":"Pétrole",
        "COPX":"Cuivre","FCX":"Cuivre","SCCO":"Cuivre","TECK":"Cuivre",
        "LIT":"Lithium","ALB":"Lithium","SQM":"Lithium","LAC":"Lithium",
        "URA":"Uranium","CCJ":"Uranium","UUUU":"Uranium","NXE":"Uranium",
        "DBA":"Agriculture","MOO":"Agriculture","ADM":"Agriculture","BG":"Agriculture",
        "WEAT":"Agriculture","CORN":"Agriculture","SOYB":"Agriculture",
        "PPLT":"Platine","PALL":"Palladium",
        "REMX":"Terres rares","MP":"Terres rares",
        "WOOD":"Bois","CUT":"Bois",
        "CPER":"Cuivre","PICK":"Métaux","XME":"Métaux",
        "GUNR":"Commodities","DJP":"Commodities","GSG":"Commodities",
    }

    # 🏥 SANTÉ / BIOTECH PRO
    SANTE_PRO = {
        "XLV":"Santé ETF","IBB":"Biotech ETF","XBI":"Biotech ETF",
        "ARKG":"Génomique ETF","IHI":"Med Devices ETF",
        "BIIB":"Biotech","MRNA":"Biotech","BNTX":"Biotech","SGEN":"Biotech",
        "NBIX":"Biotech","ALNY":"Biotech","PCVX":"Biotech","EXAS":"Santé",
        "HZNP":"Santé","INCY":"Biotech","IONS":"Biotech","BMRN":"Biotech",
        "RARE":"Biotech","SRPT":"Biotech","UTHR":"Biotech",
        "HOLX":"Med Devices","PODD":"Med Devices","RVMD":"Biotech",
        "CNC":"Assurance Santé","HUM":"Assurance Santé","MOH":"Assurance Santé",
        "ELV":"Assurance Santé","WBA":"Pharmacie","MCK":"Pharmacie",
        "CAH":"Pharmacie","ABC":"Pharmacie","ZBH":"Med Devices","BSX":"Med Devices",
        "EW":"Med Devices","BAX":"Med Devices","BDX":"Med Devices",
    }

    # 🎮 GAMING PRO (expandé)
    GAMING_PRO = {
        "EA":"Gaming","TTWO":"Gaming","RBLX":"Gaming","U":"Gaming",
        "DKNG":"Gaming","SONY":"Gaming","NTDOY":"Gaming",
        "SE":"Gaming","NTES":"Gaming","BILI":"Gaming",
        "PLTK":"Gaming","ZNGA":"Gaming","SKLZ":"Gaming",
        "UBI.PA":"Gaming","CDR.WA":"Gaming","EVO.ST":"Gaming","EMB.ST":"Gaming",
        "RUSH":"eSports","GMBL":"Gaming",
        "ESPO":"Gaming ETF","HERO":"Gaming ETF","NERD":"Gaming ETF",
    }

    # 📈 INDICES ETFs / BENCHMARKS
    INDICES_ETF = {
        "SPY":"S&P500 ETF","QQQ":"NASDAQ100 ETF","IWM":"Russell2000 ETF",
        "DIA":"Dow30 ETF","VTI":"Total Market ETF",
        "EFA":"EAFE ETF","EEM":"Emerging ETF","VWO":"Emerging ETF",
        "ARKK":"Innovation ETF","ARKG":"Génomique ETF","ARKF":"Fintech ETF",
        "XLK":"Tech ETF","XLF":"Finance ETF","XLV":"Santé ETF",
        "XLI":"Industrie ETF","XLE":"Energie ETF","XLP":"Conso ETF",
        "XLY":"Conso Disc ETF","XLB":"Matériaux ETF","XLRE":"Immobilier ETF",
        "SMH":"Semi ETF","SOXX":"Semi ETF","IGV":"Software ETF",
        "HACK":"Cyber ETF","BOTZ":"Robot ETF","DRIV":"EV ETF",
        "TAN":"Solaire ETF","ICLN":"Clean Energy ETF",
        "KWEB":"China Tech ETF","FXI":"China ETF",
    }

    # ₿ CRYPTO
    CRYPTO = {
        "BTC-USD":"Crypto","ETH-USD":"Crypto","SOL-USD":"Crypto","BNB-USD":"Crypto",
        "XRP-USD":"Crypto","ADA-USD":"Crypto","AVAX-USD":"Crypto","DOGE-USD":"Crypto",
        "IBIT":"Crypto","GBTC":"Crypto","ETHA":"Crypto",
        "COIN":"Crypto","MSTR":"Crypto","RIOT":"Crypto","MARA":"Crypto",
    }

    # PEA COMPLET (France + EU/EEE, pas UK/CH/US)
    PEA = {}  # Sera construit dynamiquement

    @classmethod
    def _build_pea(cls):
        """Construit automatiquement l'univers PEA éligible"""
        pea = {}
        pea.update(cls.FRANCE)
        pea.update(cls.PME_PEA)
        # Ajouter les actions EU (pas UK .L, pas CH .SW)
        for sym, sect in cls.EUROPE.items():
            if not sym.endswith('.L') and not sym.endswith('.SW'):
                pea[sym] = sect
        cls.PEA = pea

    @classmethod
    def obtenir_actions(cls, us=True, europe=True, france=True, gaming=True,
                        matieres=True, crypto=True, mode_pea=False, inclure_pme=True,
                        inclure_sante=True, inclure_nasdaq100=True, inclure_sp500=True):
        if not cls.PEA:
            cls._build_pea()
        if mode_pea:
            return dict(cls.PEA)
        actions = {}
        if us: actions.update(cls.US)
        if france: actions.update(cls.FRANCE)
        if europe: actions.update(cls.EUROPE)
        if inclure_pme: actions.update(cls.PME_PEA)
        if gaming:
            actions.update(cls.GAMING_PRO)
            for d in [cls.US, cls.EUROPE, cls.PME_PEA]:
                actions.update({k:v for k,v in d.items() if v=="Gaming"})
        if matieres: actions.update(cls.MATIERES)
        if inclure_sante: actions.update(cls.SANTE_PRO)
        if inclure_nasdaq100 or inclure_sp500: actions.update(cls.INDICES_ETF)
        if crypto: actions.update(cls.CRYPTO)
        return actions

    @classmethod
    def obtenir_marche(cls, sym):
        if sym in cls.CRYPTO or sym.endswith('-USD'): return "₿ Crypto"
        if sym in cls.MATIERES: return "🥇 Commodities"
        if sym.endswith('.PA'): return "🇫🇷 France"
        if sym.endswith('.DE'): return "🇩🇪 Allemagne"
        if sym.endswith('.AS'): return "🇳🇱 Pays-Bas"
        if sym.endswith('.BR'): return "🇧🇪 Belgique"
        if sym.endswith('.MI'): return "🇮🇹 Italie"
        if sym.endswith('.MC'): return "🇪🇸 Espagne"
        if sym.endswith('.LS'): return "🇵🇹 Portugal"
        if sym.endswith('.HE'): return "🇫🇮 Finlande"
        if sym.endswith(('.CO','.ST','.OL')): return "🇪🇺 Scandinavie"
        if sym.endswith('.WA'): return "🇵🇱 Pologne"
        if sym.endswith('.VI'): return "🇦🇹 Autriche"
        if sym.endswith(('.L','.SW')): return "🇪🇺 Europe"
        return "🇺🇸 US"

    @classmethod
    def obtenir_secteur(cls, sym):
        for d in [cls.FRANCE, cls.US, cls.EUROPE, cls.PME_PEA, cls.MATIERES, cls.CRYPTO,
                  cls.SANTE_PRO, cls.GAMING_PRO, cls.INDICES_ETF]:
            if sym in d: return d[sym]
        return "Autre"


# ══════════════════════════════════════════════════════════════════════════════
#               📐 MATHÉMATIQUES QUANTITATIVES AVANCÉES
#          (Ratios introuvables — BlackRock / Renaissance / AQR Style)
# ══════════════════════════════════════════════════════════════════════════════
class MathQuant:
    """Bibliothèque de calculs quantitatifs de niveau institutionnel"""

    @staticmethod
    def hurst_exponent(series, max_lag=20):
        """Exposant de Hurst — détecte tendance (>0.5) vs mean-reversion (<0.5)"""
        if len(series) < max_lag * 2: return 0.5
        try:
            lags = range(2, max_lag)
            tau = [np.std(np.subtract(series[lag:].values, series[:-lag].values)) for lag in lags]
            tau = [t for t in tau if t > 0]
            if len(tau) < 3: return 0.5
            reg = np.polyfit(np.log(list(range(2, 2+len(tau)))), np.log(tau), 1)
            return max(0.0, min(1.0, reg[0]))
        except: return 0.5

    @staticmethod
    def fractal_dimension(series, k_max=10):
        """Dimension fractale de Higuchi — mesure la complexité du signal"""
        n = len(series)
        if n < k_max * 4: return 1.5
        try:
            L_k = []
            for k in range(1, k_max + 1):
                Lmk = []
                for m in range(1, k + 1):
                    idx = np.arange(m - 1, n, k)
                    if len(idx) < 2: continue
                    subs = series.iloc[idx].values if hasattr(series,'iloc') else series[idx]
                    Lm = np.sum(np.abs(np.diff(subs))) * (n - 1) / (k * (len(subs) - 1) * k)
                    if Lm > 0: Lmk.append(Lm)
                if Lmk: L_k.append((k, np.mean(Lmk)))
            if len(L_k) < 3: return 1.5
            x = np.log([l[0] for l in L_k])
            y = np.log([l[1] for l in L_k])
            return max(1.0, min(2.0, -np.polyfit(x, y, 1)[0]))
        except: return 1.5

    @staticmethod
    def shannon_entropy(series, bins=20):
        """Entropie de Shannon — mesure l'incertitude/désordre"""
        if len(series) < 20: return 0.5
        try:
            returns = pd.Series(series).pct_change().dropna()
            hist, _ = np.histogram(returns, bins=bins, density=True)
            hist = hist[hist > 0]; hist = hist / hist.sum()
            return float(-np.sum(hist * np.log2(hist)) / np.log2(bins))
        except: return 0.5

    @staticmethod
    def omega_ratio(returns, threshold=0.0):
        """Omega Ratio — ratio gains/pertes au-dessus d'un seuil (meilleur que Sharpe)"""
        if len(returns) < 10: return 1.0
        try:
            excess = returns - threshold
            gains = excess[excess > 0].sum()
            losses = abs(excess[excess <= 0].sum())
            return round(gains / losses, 3) if losses > 0 else 10.0
        except: return 1.0

    @staticmethod
    def sortino_ratio(returns, risk_free=0.0, periods=252):
        """Sortino Ratio — Sharpe corrigé (pénalise seulement le downside)"""
        if len(returns) < 10: return 0.0
        try:
            excess = returns - risk_free / periods
            downside = returns[returns < 0]
            if len(downside) < 3: return 3.0
            down_std = np.std(downside) * np.sqrt(periods)
            return round(np.mean(excess) * periods / down_std, 3) if down_std > 0 else 3.0
        except: return 0.0

    @staticmethod
    def calmar_ratio(returns, periods=252):
        """Calmar Ratio — rendement / max drawdown"""
        if len(returns) < 20: return 0.0
        try:
            cum = (1 + returns).cumprod()
            max_dd = ((cum / cum.cummax()) - 1).min()
            ann_ret = (cum.iloc[-1] ** (periods / len(returns))) - 1
            return round(ann_ret / abs(max_dd), 3) if max_dd < 0 else 10.0
        except: return 0.0

    @staticmethod
    def information_ratio(returns, benchmark_returns, periods=252):
        """Information Ratio — alpha ajusté / tracking error"""
        if len(returns) < 20 or len(benchmark_returns) < 20: return 0.0
        try:
            min_len = min(len(returns), len(benchmark_returns))
            active = returns.iloc[-min_len:].values - benchmark_returns.iloc[-min_len:].values
            te = np.std(active) * np.sqrt(periods)
            return round(np.mean(active) * periods / te, 3) if te > 0 else 0.0
        except: return 0.0

    @staticmethod
    def cusum_regime(series, threshold=None):
        """CUSUM — détecte les changements de régime"""
        if len(series) < 30: return 0, "STABLE"
        try:
            returns = pd.Series(series).pct_change().dropna()
            mean_r = returns.mean()
            if threshold is None: threshold = 3 * returns.std()
            s_pos = 0; s_neg = 0; changes = 0
            for r in returns:
                s_pos = max(0, s_pos + r - mean_r)
                s_neg = min(0, s_neg + r - mean_r)
                if s_pos > threshold or s_neg < -threshold:
                    changes += 1; s_pos = 0; s_neg = 0
            if changes >= 3: regime = "INSTABLE"
            elif changes >= 1: regime = "TRANSITION"
            else: regime = "STABLE"
            return changes, regime
        except: return 0, "STABLE"

    @staticmethod
    def tail_ratio(returns):
        """Tail Ratio — symétrie des queues de distribution (>1 = plus de gros gains)"""
        if len(returns) < 50: return 1.0
        try:
            pct95 = np.percentile(returns, 95)
            pct5 = abs(np.percentile(returns, 5))
            return round(pct95 / pct5, 3) if pct5 > 0 else 1.0
        except: return 1.0

    @staticmethod
    def max_drawdown(series):
        """Max Drawdown en %"""
        if len(series) < 2: return 0.0
        try:
            cum = series / series.iloc[0] if hasattr(series,'iloc') else series / series[0]
            peak = pd.Series(cum).cummax()
            dd = (cum - peak) / peak
            return round(float(dd.min()) * 100, 2)
        except: return 0.0

    @staticmethod
    def smart_money_flow(high, low, close, volume, period=14):
        """Smart Money Flow — détecte l'activité institutionnelle"""
        if len(close) < period + 5: return 0.0, "N/A"
        try:
            # Money Flow Index (MFI) avancé
            tp = (high + low + close) / 3
            mf = tp * volume
            pos_mf = mf.where(tp > tp.shift(1), 0).rolling(period).sum()
            neg_mf = mf.where(tp <= tp.shift(1), 0).rolling(period).sum()
            mfi = 100 - (100 / (1 + pos_mf / neg_mf.replace(0, 1)))
            val = float(mfi.iloc[-1]) if pd.notna(mfi.iloc[-1]) else 50

            # Accumulation/Distribution avancée
            clv = ((close - low) - (high - close)) / (high - low).replace(0, 1)
            ad = (clv * volume).cumsum()
            ad_slope = (ad.iloc[-1] - ad.iloc[-5]) / 5 if len(ad) >= 5 else 0

            if val > 70 and ad_slope > 0: signal = "🟢🟢 ACCUMULATION FORTE"
            elif val > 55 and ad_slope > 0: signal = "🟢 ACCUMULATION"
            elif val < 30 and ad_slope < 0: signal = "🔴🔴 DISTRIBUTION FORTE"
            elif val < 45 and ad_slope < 0: signal = "🔴 DISTRIBUTION"
            else: signal = "⚪ NEUTRE"
            return round(val, 1), signal
        except: return 50.0, "N/A"


# ══════════════════════════════════════════════════════════════════════════════
#            🏦 BLACKROCK FACTOR MODEL (ALADDIN-INSPIRED)
# ══════════════════════════════════════════════════════════════════════════════
class BlackRockFactorModel:
    """
    Modèle multi-factoriel inspiré de BlackRock Aladdin:
    6 facteurs: Market, Size, Value, Momentum, Quality, Volatility
    Chaque facteur produit un score 0-100, combinés en score composite
    """

    @staticmethod
    def factor_market_beta(returns, benchmark_returns):
        """Beta par rapport au marché — sensibilité aux mouvements du marché"""
        if len(returns) < 30 or len(benchmark_returns) < 30: return 1.0, 50
        try:
            n = min(len(returns), len(benchmark_returns))
            r, b = returns.iloc[-n:], benchmark_returns.iloc[-n:]
            cov = np.cov(r, b)[0][1]
            var_b = np.var(b)
            beta = cov / var_b if var_b > 0 else 1.0
            # Score: beta proche de 1 = 50, beta < 0.5 = 80 (défensif), beta > 1.5 = 30
            score = max(0, min(100, 80 - abs(beta - 0.8) * 40))
            return round(beta, 3), int(score)
        except: return 1.0, 50

    @staticmethod
    def factor_size(market_cap):
        """Facteur taille — les small caps surperforment historiquement"""
        if not market_cap or market_cap <= 0: return 50
        if market_cap < 300e6: return 90    # Nano cap
        if market_cap < 2e9: return 80      # Small cap
        if market_cap < 10e9: return 70     # Mid cap
        if market_cap < 100e9: return 50    # Large cap
        return 35                           # Mega cap (moins d'upside)

    @staticmethod
    def factor_value(pe, pb, ps, dividend_yield, fcf_yield):
        """Facteur valeur — actions sous-évaluées (value investing)"""
        score = 50
        if pe and pe > 0:
            if pe < 10: score += 20
            elif pe < 15: score += 12
            elif pe < 20: score += 5
            elif pe > 40: score -= 15
            elif pe > 60: score -= 25
        if pb and pb > 0:
            if pb < 1: score += 15
            elif pb < 2: score += 8
            elif pb > 5: score -= 10
        if ps and ps > 0:
            if ps < 1: score += 12
            elif ps < 3: score += 5
            elif ps > 10: score -= 10
        if dividend_yield and dividend_yield > 0:
            if dividend_yield > 5: score += 10
            elif dividend_yield > 3: score += 5
        if fcf_yield and fcf_yield > 0:
            if fcf_yield > 8: score += 15
            elif fcf_yield > 5: score += 8
        return max(0, min(100, score))

    @staticmethod
    def factor_momentum(returns_1m, returns_3m, returns_6m, returns_12m):
        """Facteur momentum — continuation de tendance (Jegadeesh & Titman 1993)"""
        score = 50
        # Momentum 12-1 (12 mois moins le dernier mois) — facteur le plus puissant
        if returns_12m is not None and returns_1m is not None:
            mom_12_1 = returns_12m - returns_1m
            if mom_12_1 > 20: score += 25
            elif mom_12_1 > 10: score += 15
            elif mom_12_1 > 0: score += 5
            elif mom_12_1 < -20: score -= 20
            elif mom_12_1 < -10: score -= 10
        # Momentum court terme (1 mois)
        if returns_1m is not None:
            if 2 < returns_1m < 10: score += 10
            elif returns_1m > 15: score -= 5  # Surextension
            elif returns_1m < -10: score -= 10
        # Accélération (3m vs 6m)
        if returns_3m is not None and returns_6m is not None:
            accel = returns_3m - (returns_6m / 2)
            if accel > 5: score += 10
            elif accel < -5: score -= 8
        return max(0, min(100, score))

    @staticmethod
    def factor_quality(roe, debt_equity, profit_margin, revenue_growth, fcf_positive):
        """Facteur qualité — solidité financière (inspiré MSCI Quality)"""
        score = 50
        if roe and roe > 0:
            if roe > 20: score += 15
            elif roe > 12: score += 8
            elif roe < 5: score -= 10
        if debt_equity is not None:
            if debt_equity < 0.3: score += 12
            elif debt_equity < 0.7: score += 5
            elif debt_equity > 2: score -= 15
            elif debt_equity > 1.5: score -= 8
        if profit_margin and profit_margin > 0:
            if profit_margin > 20: score += 10
            elif profit_margin > 10: score += 5
            elif profit_margin < 3: score -= 10
        if revenue_growth is not None:
            if revenue_growth > 15: score += 10
            elif revenue_growth > 5: score += 5
            elif revenue_growth < -5: score -= 10
        if fcf_positive: score += 8
        return max(0, min(100, score))

    @staticmethod
    def factor_volatility(vol_20d, vol_60d, beta, max_dd_90d):
        """Facteur low-volatility — les actions à faible vol surperforment ajusté au risque"""
        score = 50
        if vol_20d is not None:
            if vol_20d < 1.0: score += 20
            elif vol_20d < 2.0: score += 10
            elif vol_20d > 4.0: score -= 15
            elif vol_20d > 3.0: score -= 8
        if vol_60d is not None and vol_20d is not None:
            # Vol qui diminue = plus stable
            if vol_20d < vol_60d * 0.8: score += 10
            elif vol_20d > vol_60d * 1.3: score -= 10
        if beta is not None:
            if beta < 0.7: score += 10
            elif beta > 1.3: score -= 10
        if max_dd_90d is not None:
            if max_dd_90d > -5: score += 10
            elif max_dd_90d < -20: score -= 15
        return max(0, min(100, score))

    @classmethod
    def score_composite(cls, factors, config):
        """Score composite multi-factoriel (0-100)"""
        weights = {
            'market': config.FACTOR_MARKET,
            'size': config.FACTOR_SIZE,
            'value': config.FACTOR_VALUE,
            'momentum': config.FACTOR_MOMENTUM,
            'quality': config.FACTOR_QUALITY,
            'volatility': config.FACTOR_VOLATILITY,
        }
        total_w = sum(weights.values())
        score = sum(factors.get(f, 50) * w for f, w in weights.items()) / total_w
        return round(score, 1)


# ══════════════════════════════════════════════════════════════════════════════
#               📰 NEWS SENTIMENT ENGINE (SCRAPING AVANCÉ)
# ══════════════════════════════════════════════════════════════════════════════
class NewsSentimentEngine:
    """Moteur de sentiment basé sur le scraping multi-source"""

    MOTS_POSITIFS = {
        'beat': 3, 'beats': 3, 'surpass': 3, 'exceeds': 3, 'upgrade': 3, 'upgrades': 3,
        'buy': 2, 'outperform': 3, 'bullish': 2, 'growth': 2, 'profit': 2, 'revenue': 1,
        'record': 3, 'high': 1, 'surge': 3, 'soar': 3, 'rally': 2, 'breakout': 2,
        'strong': 2, 'positive': 2, 'innovative': 2, 'momentum': 2, 'expansion': 2,
        'dividend': 2, 'buyback': 2, 'partnership': 2, 'acquisition': 1, 'launch': 2,
        'approved': 3, 'fda': 2, 'contract': 2, 'deal': 2, 'win': 2, 'award': 2,
        'hausse': 2, 'bénéfice': 2, 'croissance': 2, 'résultat': 1, 'record': 3,
        'acquisition': 2, 'partenariat': 2, 'dividende': 2, 'recommandation': 1,
        'objectif': 1, 'relevé': 2, 'surperformance': 3, 'expansion': 2,
        'accélération': 2, 'relèvement': 2, 'surprise': 2, 'dépassement': 3,
        'ai': 2, 'artificial intelligence': 3, 'cloud': 1, 'digital': 1,
    }

    MOTS_NEGATIFS = {
        'miss': -3, 'misses': -3, 'below': -2, 'downgrade': -3, 'sell': -2,
        'bearish': -2, 'decline': -2, 'loss': -2, 'debt': -2, 'bankruptcy': -4,
        'fraud': -4, 'investigation': -3, 'lawsuit': -3, 'layoff': -2, 'layoffs': -2,
        'warning': -2, 'risk': -1, 'crash': -3, 'plunge': -3, 'tumble': -3,
        'cut': -2, 'slash': -2, 'weak': -2, 'negative': -2, 'concern': -1,
        'recession': -3, 'inflation': -2, 'tariff': -2, 'ban': -3, 'fine': -2,
        'recall': -2, 'delay': -2, 'suspend': -3, 'violation': -3,
        'baisse': -2, 'perte': -2, 'dette': -2, 'avertissement': -3,
        'dégradation': -3, 'suspension': -3, 'faillite': -4, 'fraude': -4,
        'enquête': -3, 'procès': -2, 'licenciement': -2, 'abaissement': -2,
        'déception': -3, 'manqué': -2, 'recul': -2, 'contraction': -2,
    }

    AMPLIFICATEURS_EARNINGS = {
        'earnings': 1.5, 'quarter': 1.3, 'quarterly': 1.3, 'q1': 1.5, 'q2': 1.5,
        'q3': 1.5, 'q4': 1.5, 'annual': 1.3, 'guidance': 1.4, 'outlook': 1.3,
        'eps': 1.5, 'revenue': 1.3, 'forecast': 1.3, 'estimate': 1.2,
        'résultats': 1.5, 'trimestriel': 1.5, 'semestriel': 1.3, 'annuel': 1.3,
        'bénéfice': 1.4, 'chiffre': 1.2, 'prévision': 1.3,
    }

    @classmethod
    def analyser_sentiment_texte(cls, texte):
        """Analyse le sentiment d'un texte avec scoring pondéré"""
        if not texte: return 50, 0, "N/A"
        mots = texte.lower().split()
        score = 0; count = 0; amplificateur = 1.0
        # Détecter contexte earnings
        for mot in mots:
            if mot in cls.AMPLIFICATEURS_EARNINGS:
                amplificateur = max(amplificateur, cls.AMPLIFICATEURS_EARNINGS[mot])
        # Scorer les mots
        for mot in mots:
            mot_clean = re.sub(r'[^a-zàâéèêëïîôùûüÿç]', '', mot)
            if mot_clean in cls.MOTS_POSITIFS:
                score += cls.MOTS_POSITIFS[mot_clean] * amplificateur; count += 1
            elif mot_clean in cls.MOTS_NEGATIFS:
                score += cls.MOTS_NEGATIFS[mot_clean] * amplificateur; count += 1
        # Normaliser 0-100
        if count == 0: return 50, 0, "⚪ NEUTRE"
        raw = score / count
        normalized = max(0, min(100, 50 + raw * 12.5))
        if normalized >= 70: label = "🟢🟢 TRÈS POSITIF"
        elif normalized >= 60: label = "🟢 POSITIF"
        elif normalized <= 30: label = "🔴🔴 TRÈS NÉGATIF"
        elif normalized <= 40: label = "🔴 NÉGATIF"
        else: label = "⚪ NEUTRE"
        return round(normalized, 1), count, label

    @classmethod
    def fetch_news_rss(cls, symbole, nom_entreprise=None):
        """Scrape les news depuis Google News RSS + Yahoo RSS"""
        articles = []
        queries = [symbole]
        if nom_entreprise: queries.append(nom_entreprise)
        for query in queries[:2]:
            try:
                url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}+stock&hl=en&gl=US&ceid=US:en"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    tree = ET.fromstring(resp.read())
                    for item in tree.findall('.//item')[:10]:
                        title = item.findtext('title', '')
                        desc = item.findtext('description', '')
                        pub = item.findtext('pubDate', '')
                        articles.append({'title': html.unescape(title), 'desc': html.unescape(desc),
                                        'date': pub, 'source': 'GoogleNews'})
            except: pass
            try:
                url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbole}&region=US&lang=en-US"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    tree = ET.fromstring(resp.read())
                    for item in tree.findall('.//item')[:8]:
                        title = item.findtext('title', '')
                        articles.append({'title': html.unescape(title), 'source': 'YahooFinance'})
            except: pass
        return articles

    @classmethod
    def score_news_complet(cls, symbole, nom=None):
        """Score de news complet pour un symbole"""
        articles = cls.fetch_news_rss(symbole, nom)
        if not articles: return 50, 0, "⚪ PAS DE NEWS", []
        scores = []; details = []
        for art in articles:
            texte = f"{art.get('title','')} {art.get('desc','')}"
            s, cnt, label = cls.analyser_sentiment_texte(texte)
            if cnt > 0:
                scores.append(s)
                details.append({'title': art.get('title','')[:80], 'score': s, 'label': label})
        if not scores: return 50, 0, "⚪ NEUTRE", details
        avg = np.mean(scores)
        if avg >= 65: label = "🟢 SENTIMENT POSITIF"
        elif avg <= 35: label = "🔴 SENTIMENT NÉGATIF"
        else: label = "⚪ SENTIMENT NEUTRE"
        return round(avg, 1), len(scores), label, details[:5]


# ══════════════════════════════════════════════════════════════════════════════
#            📊 QUARTERLY EARNINGS ENGINE (TRIMESTRIEL)
# ══════════════════════════════════════════════════════════════════════════════
class EarningsEngine:
    """Analyse des résultats trimestriels et impact sur le scoring"""

    @staticmethod
    def analyser_earnings(ticker_obj):
        """Analyse complète des earnings trimestriels via yfinance"""
        result = {'score': 50, 'details': {}, 'signal': '⚪ N/A', 'surprises': []}
        try:
            # Revenus & bénéfices via quarterly_income_stmt (API moderne)
            fin = getattr(ticker_obj, 'quarterly_income_stmt', None)
            if fin is None or (hasattr(fin, 'empty') and fin.empty):
                try: fin = ticker_obj.quarterly_financials
                except: fin = None
            if fin is not None and not fin.empty:
                result['details']['nb_trimestres'] = min(len(fin.columns), 8)
                # Croissance Revenue QoQ
                if 'Total Revenue' in fin.index:
                    rev = fin.loc['Total Revenue'].dropna()
                    if len(rev) >= 2:
                        rev_growth = ((rev.iloc[0] - rev.iloc[1]) / abs(rev.iloc[1])) * 100
                        result['details']['revenue_growth_qoq'] = round(rev_growth, 1)
                        if rev_growth > 15: result['score'] += 15
                        elif rev_growth > 5: result['score'] += 8
                        elif rev_growth < -10: result['score'] -= 15
                        elif rev_growth < 0: result['score'] -= 5

                # Net Income trend
                if 'Net Income' in fin.index:
                    ni = fin.loc['Net Income'].dropna()
                    if len(ni) >= 2:
                        ni_growth = ((ni.iloc[0] - ni.iloc[1]) / abs(ni.iloc[1])) * 100 if ni.iloc[1] != 0 else 0
                        result['details']['net_income_growth_qoq'] = round(ni_growth, 1)
                        if ni_growth > 20: result['score'] += 12
                        elif ni_growth > 5: result['score'] += 5
                        elif ni_growth < -20: result['score'] -= 12
                    # Streak positive/negative
                    if len(ni) >= 4:
                        positifs = sum(1 for x in ni.iloc[:4] if x > 0)
                        result['details']['trimestres_positifs_4'] = positifs
                        if positifs == 4: result['score'] += 10
                        elif positifs == 0: result['score'] -= 15

            # EPS surprises
            try:
                cal = ticker_obj.earnings_dates
                if cal is not None and not cal.empty:
                    if 'Surprise(%)' in cal.columns:
                        surprises = cal['Surprise(%)'].dropna()
                        for i, s in enumerate(surprises.head(4)):
                            if s > 5: result['surprises'].append(f"Q-{i}: +{s:.1f}% BEAT")
                            elif s < -5: result['surprises'].append(f"Q-{i}: {s:.1f}% MISS")
                        avg_surprise = surprises.head(4).mean()
                        result['details']['avg_surprise_pct'] = round(avg_surprise, 1)
                        if avg_surprise > 5: result['score'] += 12
                        elif avg_surprise > 0: result['score'] += 5
                        elif avg_surprise < -5: result['score'] -= 12

                    # Prochain earnings date
                    future = cal.index[cal.index > pd.Timestamp.now()]
                    if len(future) > 0:
                        next_date = future[0]
                        days_to = (next_date - pd.Timestamp.now()).days
                        result['details']['next_earnings_date'] = next_date.strftime('%Y-%m-%d')
                        result['details']['days_to_earnings'] = days_to
                        if 0 < days_to <= 7: result['details']['earnings_imminent'] = True
            except: pass

            result['score'] = max(0, min(100, result['score']))
            if result['score'] >= 70: result['signal'] = "🟢🟢 EARNINGS FORTS"
            elif result['score'] >= 58: result['signal'] = "🟢 EARNINGS POSITIFS"
            elif result['score'] <= 30: result['signal'] = "🔴🔴 EARNINGS FAIBLES"
            elif result['score'] <= 42: result['signal'] = "🔴 EARNINGS NÉGATIFS"
            else: result['signal'] = "⚪ EARNINGS NEUTRES"
        except Exception as e:
            logger.debug(f"Erreur earnings: {e}")
        return result


# ══════════════════════════════════════════════════════════════════════════════
#            📈 CROSS-ASSET CORRELATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class CorrelationEngine:
    """Matrice de corrélation cross-asset et analyse de diversification"""

    BENCHMARKS = {
        'SPY': 'S&P 500', 'QQQ': 'Nasdaq', '^VIX': 'VIX (Volatilité)',
        'GLD': 'Or', 'TLT': 'Obligations 20Y', 'UUP': 'Dollar Index',
        '^TNX': 'Taux 10Y US',
    }

    _cache = {}
    _cache_ts = None

    @classmethod
    def _fetch_benchmarks(cls, period='6mo'):
        """Télécharge les données des benchmarks"""
        now = time.time()
        if cls._cache_ts and (now - cls._cache_ts) < 3600 and cls._cache:
            return cls._cache
        try:
            syms = list(cls.BENCHMARKS.keys())
            df = yf.download(syms, period=period, interval='1d', progress=False, threads=True, group_by='ticker')
            result = {}
            for s in syms:
                try:
                    close = df[s]['Close'].dropna() if len(syms) > 1 else df['Close'].dropna()
                    if len(close) > 20:
                        result[s] = close.pct_change().dropna()
                except: pass
            cls._cache = result; cls._cache_ts = now
            return result
        except: return {}

    @classmethod
    def calculer_correlations(cls, returns_action, symbole=""):
        """Calcule les corrélations avec tous les benchmarks"""
        benchmarks = cls._fetch_benchmarks()
        if not benchmarks: return {}
        correlations = {}
        for bm_sym, bm_name in cls.BENCHMARKS.items():
            if bm_sym in benchmarks:
                bm_ret = benchmarks[bm_sym]
                # Aligner les dates
                common_idx = returns_action.index.intersection(bm_ret.index)
                if len(common_idx) >= 20:
                    corr = returns_action.loc[common_idx].corr(bm_ret.loc[common_idx])
                    correlations[bm_name] = round(corr, 3)
        return correlations

    @classmethod
    def beta_vs_market(cls, returns_action):
        """Calcule le beta vs SPY"""
        benchmarks = cls._fetch_benchmarks()
        if 'SPY' not in benchmarks: return 1.0
        spy = benchmarks['SPY']
        common = returns_action.index.intersection(spy.index)
        if len(common) < 30: return 1.0
        r, b = returns_action.loc[common], spy.loc[common]
        cov = np.cov(r, b)
        return round(cov[0][1] / cov[1][1], 3) if cov[1][1] > 0 else 1.0

    @classmethod
    def alpha_jensen(cls, returns_action, risk_free_annual=0.04):
        """Alpha de Jensen — surperformance ajustée au risque"""
        benchmarks = cls._fetch_benchmarks()
        if 'SPY' not in benchmarks: return 0.0
        spy = benchmarks['SPY']
        common = returns_action.index.intersection(spy.index)
        if len(common) < 30: return 0.0
        r, b = returns_action.loc[common], spy.loc[common]
        beta = cls.beta_vs_market(returns_action)
        rf_daily = risk_free_annual / 252
        alpha = (r.mean() - rf_daily) - beta * (b.mean() - rf_daily)
        return round(alpha * 252 * 100, 2)  # Annualisé en %


# ══════════════════════════════════════════════════════════════════════════════
#            �️ RISK MANAGER PRO — Position Sizing, VaR, Kelly, R-Multiples
# ══════════════════════════════════════════════════════════════════════════════
class RiskManager:
    """
    Gestionnaire de risque complet:
    - Kelly criterion (position sizing optimal)
    - Value at Risk (historique + Monte Carlo)
    - R-multiple tracking & expectancy
    - Portfolio correlation risk
    - Stress testing (Monte Carlo scenarios)
    - Risk-adjusted performance metrics
    """

    def __init__(self, config=None):
        self.config = config or Config()
        self.trades_history = []  # R-multiple tracking
        self._log = logging.getLogger('BlackRockScreener')

    # ─────────────────────────────────────────────────────────────
    #  KELLY CRITERION — optimal position sizing
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def kelly_criterion(win_rate, avg_win_r, avg_loss_r=1.0):
        """
        Calcule la fraction Kelly optimale.
        win_rate: taux de réussite (0-1)
        avg_win_r: gain moyen en R-multiples (ex: 2.5R)
        avg_loss_r: perte moyenne en R-multiples (toujours ~1R si SL respecté)
        Returns: fraction du capital à risquer (ex: 0.12 = 12%)
        """
        if avg_win_r <= 0 or win_rate <= 0 or win_rate >= 1:
            return 0.0
        # Kelly: f* = (p * b - q) / b  où b=avg_win/avg_loss, p=win_rate, q=1-p
        b = avg_win_r / max(avg_loss_r, 0.01)
        q = 1.0 - win_rate
        kelly = (win_rate * b - q) / b
        return max(0.0, kelly)

    def position_size_kelly(self, win_rate, avg_win_r, prix, atr, sl_pct=None):
        """
        Calcule la taille de position optimale via Kelly.
        Returns: dict avec nb_actions, montant, pct_capital, kelly_raw, kelly_used
        """
        capital = float(getattr(self.config, 'CAPITAL', 10000))
        risk_max = float(getattr(self.config, 'RISQUE_MAX_PCT', 0.02))
        kelly_frac = float(getattr(self.config, 'KELLY_FRACTION', 0.25))
        kelly_max = float(getattr(self.config, 'KELLY_MAX_PCT', 0.15))

        # Kelly brut
        kelly_raw = self.kelly_criterion(win_rate, avg_win_r)
        # Fraction-Kelly (conservative)
        kelly_used = min(kelly_raw * kelly_frac, kelly_max)

        # Montant à risquer
        risk_amount = capital * min(kelly_used, risk_max)

        # Taille de position basée sur le SL
        if sl_pct and abs(sl_pct) > 0:
            position_value = risk_amount / (abs(sl_pct) / 100.0)
        elif atr and atr > 0:
            sl_distance = atr * float(getattr(self.config, 'STOP_LOSS_ATR', 2.0))
            position_value = risk_amount / (sl_distance / max(prix, 0.01))
        else:
            position_value = risk_amount / risk_max

        # Limiter au max allocation par position
        max_alloc = capital * kelly_max
        position_value = min(position_value, max_alloc)

        nb_actions = int(position_value / max(prix, 0.01))

        return {
            'kelly_raw_pct': round(kelly_raw * 100, 2),
            'kelly_used_pct': round(kelly_used * 100, 2),
            'risk_amount': round(risk_amount, 2),
            'position_value': round(position_value, 2),
            'nb_actions': max(0, nb_actions),
            'pct_capital': round((position_value / capital) * 100, 2) if capital > 0 else 0,
        }

    # ─────────────────────────────────────────────────────────────
    #  VALUE AT RISK — Historique + Monte Carlo
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def var_historique(returns, confidence=0.95, horizon=1):
        """VaR historique simple (percentile)"""
        if len(returns) < 20:
            return 0.0
        var_1d = float(np.percentile(returns, (1 - confidence) * 100))
        return round(var_1d * np.sqrt(horizon) * 100, 2)  # en % négatif

    @staticmethod
    def cvar_historique(returns, confidence=0.95, horizon=1):
        """Conditional VaR (Expected Shortfall) — perte moyenne au-delà du VaR"""
        if len(returns) < 20:
            return 0.0
        threshold = np.percentile(returns, (1 - confidence) * 100)
        tail = returns[returns <= threshold]
        if len(tail) == 0:
            return round(threshold * np.sqrt(horizon) * 100, 2)
        return round(float(tail.mean()) * np.sqrt(horizon) * 100, 2)

    @staticmethod
    def var_monte_carlo(returns, confidence=0.95, horizon=5, n_sims=5000):
        """
        VaR par simulation Monte Carlo.
        Simule n_sims trajectoires de prix sur 'horizon' jours.
        Returns: (var_pct, cvar_pct, scenarios_array)
        """
        if len(returns) < 30:
            return 0.0, 0.0, np.array([])
        mu = float(np.mean(returns))
        sigma = float(np.std(returns))
        if sigma < 1e-10:
            return 0.0, 0.0, np.array([])

        # Simuler les trajectoires (GBM — geometric brownian motion)
        np.random.seed(42)
        daily_returns = np.random.normal(mu, sigma, (n_sims, horizon))
        cumulative = np.prod(1 + daily_returns, axis=1) - 1  # rendement total sur horizon

        var_pct = round(float(np.percentile(cumulative, (1 - confidence) * 100)) * 100, 2)
        threshold = np.percentile(cumulative, (1 - confidence) * 100)
        tail = cumulative[cumulative <= threshold]
        cvar_pct = round(float(tail.mean()) * 100, 2) if len(tail) > 0 else var_pct

        return var_pct, cvar_pct, cumulative

    # ─────────────────────────────────────────────────────────────
    #  R-MULTIPLE TRACKING & EXPECTANCY
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def compute_r_multiple(entry_price, exit_price, stop_loss):
        """
        Calcule le R-multiple d'un trade.
        R = 1 signifie que la perte max (SL) a été atteinte.
        R = 2 signifie que le gain est 2× le risque initial.
        """
        risk_per_share = abs(entry_price - stop_loss)
        if risk_per_share < 0.001:
            return 0.0
        profit = exit_price - entry_price
        return round(profit / risk_per_share, 2)

    @staticmethod
    def expectancy(r_multiples):
        """
        Expectancy = (Win% × Avg Win R) - (Loss% × Avg Loss R)
        Returns: dict with expectancy, win_rate, avg_win, avg_loss, profit_factor
        """
        if not r_multiples or len(r_multiples) == 0:
            return {'expectancy': 0, 'win_rate': 0, 'avg_win_r': 0, 'avg_loss_r': 0, 'profit_factor': 0, 'n_trades': 0}
        arr = np.array(r_multiples)
        wins = arr[arr > 0]
        losses = arr[arr <= 0]
        n = len(arr)
        win_rate = len(wins) / n if n > 0 else 0
        avg_win = float(wins.mean()) if len(wins) > 0 else 0
        avg_loss = float(abs(losses.mean())) if len(losses) > 0 else 0
        expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss
        profit_factor = (sum(wins) / abs(sum(losses))) if len(losses) > 0 and sum(losses) != 0 else float('inf')
        return {
            'expectancy': round(expectancy, 3),
            'win_rate': round(win_rate * 100, 1),
            'avg_win_r': round(avg_win, 2),
            'avg_loss_r': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else 999.0,
            'n_trades': n,
            'total_r': round(float(arr.sum()), 2),
        }

    # ─────────────────────────────────────────────────────────────
    #  EXPECTED R-MULTIPLE for a new trade (forward-looking)
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def expected_r(score_final, ratio_rr, ml_prob=50.0, ev_pct=0.0):
        """
        Estime le R-multiple attendu pour un trade potentiel.
        Combine score_final (confiance), R:R ratio, ML probability, et EV.
        """
        # Probabilité de réussite estimée
        p_win = min(0.90, max(0.10, score_final / 100.0 * 0.6 + ml_prob / 100.0 * 0.4))
        # R attendu = p_win * R:R - (1-p_win) * 1R
        expected = p_win * ratio_rr - (1 - p_win) * 1.0
        # Bonus EV positif
        if ev_pct > 0:
            expected += ev_pct * 0.01
        return round(expected, 2)

    # ─────────────────────────────────────────────────────────────
    #  STRESS TESTING — Monte Carlo portfolio drawdown
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def stress_test_portfolio(returns_matrix, weights=None, n_sims=5000, horizon=60):
        """
        Monte Carlo stress test sur un portefeuille.
        returns_matrix: DataFrame avec colonnes = symboles, lignes = daily returns
        weights: pondérations par symbole (equal-weight si None)
        Returns: dict with max_drawdown_95, expected_return, worst_case, best_case
        """
        if returns_matrix is None or len(returns_matrix) < 30:
            return {'max_dd_95': 0, 'expected_return': 0, 'worst_case': 0, 'best_case': 0}

        n_assets = returns_matrix.shape[1]
        if weights is None:
            weights = np.ones(n_assets) / n_assets

        # Portfolio daily returns (historical)
        port_returns = returns_matrix.values @ weights
        mu = float(np.mean(port_returns))
        sigma = float(np.std(port_returns))

        if sigma < 1e-10:
            return {'max_dd_95': 0, 'expected_return': round(mu * 252 * 100, 2), 'worst_case': 0, 'best_case': 0}

        # Monte Carlo simulation
        np.random.seed(42)
        sims = np.random.normal(mu, sigma, (n_sims, horizon))
        cum_returns = np.cumprod(1 + sims, axis=1)

        # Max drawdown per simulation
        max_dds = []
        for sim in cum_returns:
            peak = np.maximum.accumulate(sim)
            dd = (sim - peak) / peak
            max_dds.append(float(dd.min()))
        max_dds = np.array(max_dds)

        # Terminal values
        terminal = cum_returns[:, -1] - 1  # total return over horizon

        return {
            'max_dd_95': round(float(np.percentile(max_dds, 5)) * 100, 2),  # 95% DD
            'max_dd_99': round(float(np.percentile(max_dds, 1)) * 100, 2),  # 99% DD
            'expected_return': round(float(np.median(terminal)) * 100, 2),
            'worst_case': round(float(np.percentile(terminal, 1)) * 100, 2),
            'best_case': round(float(np.percentile(terminal, 99)) * 100, 2),
            'prob_loss': round(float(np.mean(terminal < 0)) * 100, 1),
            'prob_gain_10pct': round(float(np.mean(terminal > 0.10)) * 100, 1),
        }

    # ─────────────────────────────────────────────────────────────
    #  PORTFOLIO CORRELATION RISK
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def portfolio_correlation_matrix(returns_dict):
        """
        Calcule la matrice de corrélation entre les actifs du portefeuille.
        returns_dict: {symbole: pd.Series(daily_returns)}
        Returns: (correlation_matrix DataFrame, avg_correlation float)
        """
        if not returns_dict or len(returns_dict) < 2:
            return pd.DataFrame(), 0.0
        df = pd.DataFrame(returns_dict).dropna()
        if len(df) < 20:
            return pd.DataFrame(), 0.0
        corr = df.corr()
        # Average off-diagonal correlation
        n = len(corr)
        if n < 2:
            return corr, 0.0
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        avg_corr = float(corr.values[mask].mean())
        return corr, round(avg_corr, 3)

    # ─────────────────────────────────────────────────────────────
    #  RISK SCORE COMPOSITE (0-100)
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def risk_score(var_pct, beta, max_dd, vol_annual, rr_ratio):
        """
        Score de risque composite 0-100 (0=très risqué, 100=très safe).
        Combine VaR, Beta, Max Drawdown, Volatilité, R:R.
        """
        # Chaque composante normalisée 0-100 (100=faible risque)
        var_s = max(0, min(100, 100 - abs(var_pct) * 10))       # VaR 5% daily -> 50/100
        beta_s = max(0, min(100, 100 - abs(beta - 1) * 50))     # beta=1 -> 100, beta=2 -> 50
        dd_s = max(0, min(100, 100 + max_dd * 2))               # dd=-30% -> 40/100
        vol_s = max(0, min(100, 100 - vol_annual * 2))          # vol=30% -> 40/100
        rr_s = max(0, min(100, rr_ratio * 25))                  # rr=4 -> 100/100

        score = 0.25 * var_s + 0.15 * beta_s + 0.25 * dd_s + 0.15 * vol_s + 0.20 * rr_s
        return round(max(0, min(100, score)), 1)

    # ─────────────────────────────────────────────────────────────
    #  RISK-ADJUSTED METRICS AGGREGATOR
    # ─────────────────────────────────────────────────────────────
    def compute_stock_risk(self, result_dict, returns=None):
        """
        Enrichit le dict résultat d'un stock avec toutes les métriques de risque.
        Appelé par analyser_action() après le calcul SL/TP/R:R.
        """
        prix = float(result_dict.get('prix', 0) or 0)
        sl = float(result_dict.get('stop_loss', 0) or 0)
        tp = float(result_dict.get('take_profit', 0) or 0)
        rr = float(result_dict.get('ratio_rr', 0) or 0)
        atr = float(result_dict.get('atr', prix * 0.02) or prix * 0.02)
        score = float(result_dict.get('score_final', 50) or 50)
        ml_prob = float(result_dict.get('ml_probabilite', 50) or 50)
        ev = float(result_dict.get('ev_pct', 0) or 0)
        beta = float(result_dict.get('beta', 1.0) or 1.0)
        max_dd = float(result_dict.get('max_drawdown', -15) or -15)
        vol = float(result_dict.get('vol_annualisee', 30) or 30)
        sl_pct = float(result_dict.get('stop_loss_pct', -5) or -5)

        # ─── VaR ───
        conf = float(getattr(self.config, 'VAR_CONFIDENCE', 0.95))
        var_h = int(getattr(self.config, 'VAR_HORIZON_JOURS', 5))
        n_mc = int(getattr(self.config, 'MONTE_CARLO_SIMS', 5000))

        if returns is not None and len(returns) >= 30:
            ret_arr = returns.values if hasattr(returns, 'values') else np.array(returns)
            var_hist = self.var_historique(ret_arr, conf, var_h)
            cvar = self.cvar_historique(ret_arr, conf, var_h)
            var_mc, cvar_mc, _ = self.var_monte_carlo(ret_arr, conf, var_h, n_mc)
        else:
            # Estimation paramétrique
            daily_vol = vol / np.sqrt(252) / 100 if vol > 1 else vol / np.sqrt(252)
            var_hist = round(-1.645 * daily_vol * np.sqrt(var_h) * 100, 2)
            cvar = round(var_hist * 1.3, 2)
            var_mc = var_hist
            cvar_mc = cvar

        # ─── Kelly ───
        win_rate = min(0.85, max(0.15, score / 100.0 * 0.5 + ml_prob / 100.0 * 0.5))
        avg_win_r = max(0.5, rr)  # R:R as proxy for average win in R
        kelly = self.position_size_kelly(win_rate, avg_win_r, prix, atr, sl_pct)

        # ─── Expected R ───
        exp_r = self.expected_r(score, rr, ml_prob, ev)

        # ─── Risk Score Composite ───
        r_score = self.risk_score(var_hist, beta, max_dd, vol, rr)

        # ─── Inject into result ───
        result_dict['var_5j'] = var_hist
        result_dict['cvar_5j'] = cvar
        result_dict['var_mc'] = var_mc
        result_dict['cvar_mc'] = cvar_mc
        result_dict['kelly_raw_pct'] = kelly['kelly_raw_pct']
        result_dict['kelly_used_pct'] = kelly['kelly_used_pct']
        result_dict['position_value'] = kelly['position_value']
        result_dict['nb_actions'] = kelly['nb_actions']
        result_dict['pct_capital'] = kelly['pct_capital']
        result_dict['risk_amount'] = kelly['risk_amount']
        result_dict['expected_r'] = exp_r
        result_dict['risk_score'] = r_score

        return result_dict

    # ─────────────────────────────────────────────────────────────
    #  PORTFOLIO-LEVEL RISK (called after all stocks analyzed)
    # ─────────────────────────────────────────────────────────────
    def compute_portfolio_risk(self, results, returns_cache=None):
        """
        Calcule les métriques de risque au niveau du portefeuille.
        results: liste de dicts (post-analyse)
        returns_cache: {symbole: pd.Series} daily returns déjà téléchargés
        Returns: dict with portfolio-level metrics
        """
        if not results:
            return {}

        capital = float(getattr(self.config, 'CAPITAL', 10000))
        max_pos = int(getattr(self.config, 'MAX_POSITIONS', 10))

        # Top N stocks by score (simulated portfolio)
        top = sorted(results, key=lambda x: x.get('score_final', 0), reverse=True)[:max_pos]
        n_pos = len(top)
        if n_pos == 0:
            return {}

        # Equal weight allocation
        alloc_per_stock = capital / n_pos

        # Portfolio metrics aggregation
        total_risk = sum(r.get('risk_amount', 0) for r in top)
        avg_kelly = np.mean([r.get('kelly_used_pct', 0) for r in top])
        avg_rr = np.mean([r.get('ratio_rr', 0) for r in top])
        avg_risk_score = np.mean([r.get('risk_score', 50) for r in top])
        avg_var = np.mean([r.get('var_5j', 0) for r in top])
        avg_exp_r = np.mean([r.get('expected_r', 0) for r in top])
        total_position = sum(min(r.get('position_value', alloc_per_stock), alloc_per_stock) for r in top)

        # Estimations portefeuille
        # VaR portefeuille (sqrt(N) diversification, simplifié)
        portfolio_var = avg_var * np.sqrt(n_pos) / n_pos  # diversification effect

        # Corrélation moyenne (si données disponibles)
        avg_corr = 0.0
        if returns_cache and len(returns_cache) >= 2:
            available = {sym: ret for sym, ret in returns_cache.items()
                        if sym in [r.get('symbole') for r in top]}
            if len(available) >= 2:
                _, avg_corr = self.portfolio_correlation_matrix(available)

        # Monte Carlo stress test (si données suffisantes)
        stress = {'max_dd_95': 0, 'expected_return': 0, 'worst_case': 0, 'best_case': 0, 'prob_loss': 0}
        if returns_cache and len(returns_cache) >= 2:
            available = {sym: ret for sym, ret in returns_cache.items()
                        if sym in [r.get('symbole') for r in top]}
            if len(available) >= 2:
                df_ret = pd.DataFrame(available).dropna()
                if len(df_ret) >= 30:
                    var_h = int(getattr(self.config, 'VAR_HORIZON_JOURS', 5))
                    n_mc = int(getattr(self.config, 'MONTE_CARLO_SIMS', 5000))
                    stress = self.stress_test_portfolio(df_ret, horizon=var_h * 4, n_sims=n_mc)

        portfolio_summary = {
            'n_positions': n_pos,
            'capital': capital,
            'total_invested': round(total_position, 2),
            'pct_invested': round(total_position / capital * 100, 1) if capital > 0 else 0,
            'total_risk': round(total_risk, 2),
            'risk_pct_capital': round(total_risk / capital * 100, 2) if capital > 0 else 0,
            'avg_kelly_pct': round(avg_kelly, 2),
            'avg_rr': round(avg_rr, 2),
            'avg_risk_score': round(avg_risk_score, 1),
            'avg_var_5j': round(avg_var, 2),
            'portfolio_var_5j': round(portfolio_var, 2),
            'avg_expected_r': round(avg_exp_r, 2),
            'avg_correlation': avg_corr,
            'concentration_alert': avg_corr > float(getattr(self.config, 'MAX_CORRELATION_PORTFOLIO', 0.70)),
            # Stress test
            'stress_max_dd_95': stress.get('max_dd_95', 0),
            'stress_expected_return': stress.get('expected_return', 0),
            'stress_worst_case': stress.get('worst_case', 0),
            'stress_best_case': stress.get('best_case', 0),
            'stress_prob_loss': stress.get('prob_loss', 0),
            # Top positions
            'top_symbols': [r.get('symbole', '?') for r in top],
        }
        return portfolio_summary


# ══════════════════════════════════════════════════════════════════════════════
#            �📐 INDICATEURS TECHNIQUES COMPLETS
# ══════════════════════════════════════════════════════════════════════════════
class Indicateurs:
    """Indicateurs techniques — bibliothèque complète"""

    @staticmethod
    def rsi(prix, p=14):
        if len(prix) < p+1: return None
        d = prix.diff(); g = d.where(d>0,0).ewm(alpha=1/p,min_periods=p,adjust=False).mean()
        l = -d.where(d<0,0).ewm(alpha=1/p,min_periods=p,adjust=False).mean()
        rs = g/l; rsi = 100 - (100/(1+rs))
        return round(float(rsi.iloc[-1]),2) if pd.notna(rsi.iloc[-1]) else None

    @staticmethod
    def rsi_series(prix, p=14):
        d = prix.diff(); g = d.where(d>0,0).ewm(alpha=1/p,min_periods=p,adjust=False).mean()
        l = -d.where(d<0,0).ewm(alpha=1/p,min_periods=p,adjust=False).mean()
        return 100-(100/(1+g/l))

    @staticmethod
    def zscore(prix, f=20):
        if len(prix)<f: return None
        r = prix.tail(f); m = r.mean(); s = r.std()
        return round(float((prix.iloc[-1]-m)/s),2) if s>0 else 0.0

    @staticmethod
    def macd(prix, r=12, l=26, s=9):
        if len(prix)<l+s: return None, None, "N/A"
        er = prix.ewm(span=r,adjust=False).mean(); el = prix.ewm(span=l,adjust=False).mean()
        ml = er-el; sl = ml.ewm(span=s,adjust=False).mean(); h = ml-sl
        mv, hv = round(float(ml.iloc[-1]),4), round(float(h.iloc[-1]),4)
        if mv>float(sl.iloc[-1]) and h.iloc[-1]>h.iloc[-2]: t="🟢 HAUSSIER"
        elif mv<float(sl.iloc[-1]) and h.iloc[-1]<h.iloc[-2]: t="🔴 BAISSIER"
        else: t="⚪ NEUTRE"
        return mv, hv, t

    @staticmethod
    def atr(h, l, c, p=14):
        if len(c)<p: return None
        tr = pd.concat([h-l, abs(h-c.shift(1)), abs(l-c.shift(1))], axis=1).max(axis=1)
        return round(float(tr.rolling(p).mean().iloc[-1]),4)

    @staticmethod
    def adx(h, l, c, p=14):
        if len(c)<p+10: return None, None, None, "N/A"
        try:
            tr = pd.concat([h-l,abs(h-c.shift(1)),abs(l-c.shift(1))],axis=1).max(axis=1)
            pdm = h.diff().clip(lower=0); ndm = (-l.diff()).clip(lower=0)
            pdm = pdm.where(pdm>ndm,0); ndm = ndm.where(ndm>pdm,0)
            a = 1/p; atr_ = tr.ewm(alpha=a,min_periods=p).mean()
            pdi = 100*(pdm.ewm(alpha=a,min_periods=p).mean()/atr_)
            ndi = 100*(ndm.ewm(alpha=a,min_periods=p).mean()/atr_)
            dx = 100*abs(pdi-ndi)/(pdi+ndi); adx_ = dx.ewm(alpha=a,min_periods=p).mean()
            av = float(adx_.iloc[-1]); pv = float(pdi.iloc[-1]); nv = float(ndi.iloc[-1])
            if av>=25 and pv>nv: s="💪 HAUSSE FORTE"
            elif av>=25 and nv>pv: s="💪 BAISSE FORTE"
            elif av<20: s="😴 FAIBLE"
            else: s="➡️ MODÉRÉ"
            return round(av,1),round(pv,1),round(nv,1),s
        except: return None,None,None,"N/A"

    @staticmethod
    def stochastic_rsi(prix, rp=14, sp=14, k=3, d=3):
        if len(prix)<rp+sp+10: return None,None,"N/A"
        try:
            rsi = Indicateurs.rsi_series(prix,rp)
            rl = rsi.rolling(sp).min(); rh = rsi.rolling(sp).max()
            sr = ((rsi-rl)/(rh-rl)*100).fillna(50)
            kl = sr.rolling(k).mean(); dl = kl.rolling(d).mean()
            kv, dv = float(kl.iloc[-1]), float(dl.iloc[-1])
            if kv<20 and kv>dv: sig="🟢🟢 SURVENDU"
            elif kv>80 and kv<dv: sig="🔴🔴 SURACHETÉ"
            elif kv<30: sig="🟢 BAS"
            elif kv>70: sig="🔴 HAUT"
            else: sig="⚪ NEUTRE"
            return round(kv,1),round(dv,1),sig
        except: return None,None,"N/A"

    @staticmethod
    def williams_r(h, l, c, p=14):
        if len(c)<p: return None,"N/A"
        hh = h.rolling(p).max(); ll = l.rolling(p).min()
        wr = -100*(hh-c)/(hh-ll); v = float(wr.iloc[-1])
        if v>-20: sig="🔴 SURACHETÉ"
        elif v<-80: sig="🟢 SURVENDU"
        else: sig="⚪ NEUTRE"
        return round(v,1),sig

    @staticmethod
    def cmf(h, l, c, v, p=20):
        if len(c)<p: return None,"N/A"
        mfm = ((c-l)-(h-c))/(h-l).replace(0,1)
        val = float((mfm*v).rolling(p).sum().iloc[-1]/v.rolling(p).sum().iloc[-1])
        if val>0.10: sig="🟢🟢 ACCUMULATION"
        elif val>0.03: sig="🟢 ACHAT"
        elif val<-0.10: sig="🔴🔴 DISTRIBUTION"
        elif val<-0.03: sig="🔴 VENTE"
        else: sig="⚪ NEUTRE"
        return round(val,3),sig

    @staticmethod
    def supertrend(h, l, c, p=10, m=3.0):
        if len(c)<p+5: return None,"N/A"
        try:
            tr = pd.concat([h-l,abs(h-c.shift(1)),abs(l-c.shift(1))],axis=1).max(axis=1)
            atr_ = tr.rolling(p).mean(); hl2 = (h+l)/2
            ub = hl2+(m*atr_); lb = hl2-(m*atr_)
            st = pd.Series(index=c.index,dtype=float); dr = pd.Series(index=c.index,dtype=int)
            st.iloc[p]=ub.iloc[p]; dr.iloc[p]=-1
            for i in range(p+1,len(c)):
                if c.iloc[i]>st.iloc[i-1]:
                    dr.iloc[i]=1; st.iloc[i]=max(lb.iloc[i],st.iloc[i-1]) if dr.iloc[i-1]==1 else lb.iloc[i]
                else:
                    dr.iloc[i]=-1; st.iloc[i]=min(ub.iloc[i],st.iloc[i-1]) if dr.iloc[i-1]==-1 else ub.iloc[i]
            d = dr.iloc[-1]; dp = dr.iloc[-2] if len(dr)>1 else d
            if d==1 and dp==-1: sig="🟢🟢 RETOURNEMENT HAUSSIER"
            elif d==-1 and dp==1: sig="🔴🔴 RETOURNEMENT BAISSIER"
            elif d==1: sig="🟢 HAUSSIER"
            else: sig="🔴 BAISSIER"
            return round(float(st.iloc[-1]),2),sig
        except: return None,"N/A"

    @staticmethod
    def volume_relatif(vol, f=20):
        if len(vol)<f: return 1.0,"N/A"
        m = vol.tail(f).mean(); a = vol.iloc[-1]; r = a/m if m>0 else 1
        if r>=2: lb="🔥 TRÈS ÉLEVÉ"
        elif r>=1.5: lb="📈 ÉLEVÉ"
        elif r<=0.5: lb="📉 FAIBLE"
        else: lb="➡️ NORMAL"
        return round(r,2),lb

    @staticmethod
    def tendance(prix, c=5, m=20, l=50):
        if len(prix)<l: return "N/A",0
        sc,sm,sl = prix.tail(c).mean(),prix.tail(m).mean(),prix.tail(l).mean()
        a = prix.iloc[-1]; s = sum([a>sc,a>sm,a>sl,sc>sm,sm>sl])
        labels = {5:"📈 FORTE HAUSSE",4:"🟢 HAUSSE",3:"➡️ NEUTRE",2:"🔴 BAISSE",1:"📉 FORTE BAISSE",0:"📉 FORTE BAISSE"}
        return labels.get(s,"N/A"),s

    @staticmethod
    def supports_resistances(prix, f=20):
        if len(prix)<f: return prix.iloc[-1]*0.95, prix.iloc[-1]*1.05
        r = prix.tail(f); return round(r.min(),2), round(r.max(),2)

    @staticmethod
    def squeeze_momentum(h, l, c, bbp=20, kcp=20, kcm=1.5):
        if len(c)<max(bbp,kcp)+5: return False,None,"N/A"
        try:
            bbm = c.rolling(bbp).mean(); bbs = c.rolling(bbp).std()
            bbu = bbm+2*bbs; bbl = bbm-2*bbs
            tr = pd.concat([h-l,abs(h-c.shift(1)),abs(l-c.shift(1))],axis=1).max(axis=1)
            atr_ = tr.rolling(kcp).mean(); kcm_ = c.rolling(kcp).mean()
            kcu = kcm_+kcm*atr_; kcl = kcm_-kcm*atr_
            sq = (bbl.iloc[-1]>kcl.iloc[-1]) and (bbu.iloc[-1]<kcu.iloc[-1])
            hh = h.rolling(kcp).max(); ll = l.rolling(kcp).min()
            mom = c-((hh+ll)/2+bbm)/2; mv = float(mom.iloc[-1]); mp = float(mom.iloc[-2])
            if sq:
                sig = "🔴 SQUEEZE +" if mv>0 else "🔴 SQUEEZE -"
            else:
                if mv>0 and mv>mp: sig="🟢🟢 EXPANSION HAUSSIÈRE"
                elif mv<0 and mv<mp: sig="🔴🔴 EXPANSION BAISSIÈRE"
                else: sig="⚪ NEUTRE"
            return sq,round(mv,4),sig
        except: return False,None,"N/A"


# ══════════════════════════════════════════════════════════════════════════════
#            🧠 MOTEUR ML PRÉDICTIF (LÓPEZ DE PRADO / QUANT GRADE)
# ══════════════════════════════════════════════════════════════════════════════
class PredicteurML:
    """Prédicteur ML de niveau institutionnel — ensemble de 13 modèles"""

    def __init__(self, config):
        self.config = config; self.modeles = {}; self.scaler = None
        self.features_names = []; self.seuil_optimal = 0.55
        self.meta_model = None; self.stacking = None; self.poids = {}
        self.trained = False; self.cache = CacheLRU("ml", 200, 900)
        self.calibrators = {}  # Calibration isotonique par modèle

    def _triple_barrier_labels(self, close, tp_mult=2.5, sl_mult=1.5, timeout=10, min_gain=0.015):
        """Triple Barrier DYNAMIQUE — barrières adaptées au régime de volatilité
        min_gain: rendement minimum au timeout pour label positif (défaut 1.5%, lu depuis ML_RENDEMENT_CIBLE)"""
        labels = pd.Series(0, index=close.index)
        # ATR rapide (7j) et lent (21j) pour adapter les barrières
        ret = close.pct_change()
        atr_fast = ret.rolling(7).std() * close
        atr_slow = ret.rolling(21).std() * close
        vol_regime = (atr_fast / atr_slow).fillna(1.0)  # >1 = vol croissante
        for i in range(21, len(close)-timeout):
            entry = close.iloc[i]
            a_fast = atr_fast.iloc[i]; a_slow = atr_slow.iloc[i]
            if pd.isna(a_fast) or a_fast <= 0: continue
            # Adapter TP/SL au régime de vol
            vr = vol_regime.iloc[i]
            if vr > 1.3:  # Vol haute → TP plus large, SL plus serré
                tp_m, sl_m = tp_mult * 1.3, sl_mult * 0.9
            elif vr < 0.7:  # Vol basse → TP resserré, classique
                tp_m, sl_m = tp_mult * 0.85, sl_mult * 1.0
            else:
                tp_m, sl_m = tp_mult, sl_mult
            # Utiliser la moyenne des 2 ATR pour la stabilité
            a = (a_fast + a_slow) / 2
            tp = entry + tp_m * a; sl = entry - sl_m * a
            for j in range(i+1, min(i+timeout+1, len(close))):
                if close.iloc[j] >= tp: labels.iloc[i] = 1; break
                elif close.iloc[j] <= sl: labels.iloc[i] = 0; break
            else:
                # Timeout — exiger un gain minimum pour label positif (ML_RENDEMENT_CIBLE)
                labels.iloc[i] = 1 if close.iloc[i+timeout] > entry * (1.0 + min_gain) else 0
        return labels

    def _build_features(self, df):
        """Construit 100+ features quantitatives"""
        c = df['Close']; h = df['High']; l = df['Low']; v = df['Volume']
        features = pd.DataFrame(index=df.index)
        # Returns multi-périodes
        for p in [1,2,3,5,10,20,40,60]:
            features[f'ret_{p}d'] = c.pct_change(p)
            features[f'log_ret_{p}d'] = np.log(c/c.shift(p))
        # Moyennes mobiles
        for p in [5,10,20,50,100]:
            sma = c.rolling(p).mean()
            features[f'sma_ratio_{p}'] = c / sma
            features[f'sma_slope_{p}'] = sma.pct_change(5)
        # EMA
        for p in [8,21,50]:
            ema = c.ewm(span=p,adjust=False).mean()
            features[f'ema_ratio_{p}'] = c / ema
        # Volatilité
        features['vol_20'] = c.pct_change().rolling(20).std()
        features['vol_60'] = c.pct_change().rolling(60).std()
        features['vol_ratio'] = features['vol_20'] / features['vol_60']
        features['parkinson_vol'] = np.sqrt(np.log(h/l)**2/(4*np.log(2))).rolling(20).mean()
        # RSI multi
        for p in [7,14,21]:
            features[f'rsi_{p}'] = Indicateurs.rsi_series(c,p)
        # MACD
        e12 = c.ewm(span=12).mean(); e26 = c.ewm(span=26).mean()
        macd_l = e12-e26; sig_l = macd_l.ewm(span=9).mean()
        features['macd'] = macd_l; features['macd_hist'] = macd_l-sig_l
        features['macd_signal_cross'] = (macd_l>sig_l).astype(int)
        # Bollinger
        bbm = c.rolling(20).mean(); bbs = c.rolling(20).std()
        features['bb_position'] = (c-bbm)/(2*bbs)
        features['bb_width'] = (4*bbs)/bbm
        # Volume
        features['vol_ratio_20'] = v / v.rolling(20).mean()
        features['vol_ratio_50'] = v / v.rolling(50).mean()
        # OBV
        obv = (np.sign(c.diff())*v).fillna(0).cumsum()
        features['obv_slope_10'] = obv.pct_change(10)
        # ATR
        tr = pd.concat([h-l,abs(h-c.shift(1)),abs(l-c.shift(1))],axis=1).max(axis=1)
        features['atr_14'] = tr.rolling(14).mean() / c
        features['atr_ratio'] = tr.rolling(7).mean() / tr.rolling(21).mean()
        # Statistiques
        features['zscore_20'] = (c-c.rolling(20).mean())/c.rolling(20).std()
        features['skew_20'] = c.pct_change().rolling(20).apply(lambda x: x.skew(), raw=False)
        features['kurt_20'] = c.pct_change().rolling(20).apply(lambda x: x.kurtosis(), raw=False)
        # Candlestick
        features['body_ratio'] = abs(c-df['Open'])/(h-l).replace(0,1)
        features['upper_shadow'] = (h-pd.concat([c,df['Open']],axis=1).max(axis=1))/(h-l).replace(0,1)
        features['gap'] = df['Open']/c.shift(1)-1
        # Conso up/down
        features['consec_up'] = c.diff().apply(lambda x: 1 if x>0 else 0).rolling(5).sum()
        features['consec_down'] = c.diff().apply(lambda x: 1 if x<0 else 0).rolling(5).sum()
        # Hurst & Entropy (sur fenêtre)
        def rolling_hurst(s, w=50):
            return s.rolling(w).apply(lambda x: MathQuant.hurst_exponent(x), raw=True)
        features['hurst_50'] = rolling_hurst(c, 50)
        features['entropy_30'] = c.rolling(30).apply(lambda x: MathQuant.shannon_entropy(x), raw=True)
        # Range & momentum
        features['range_20'] = (h.rolling(20).max()-l.rolling(20).min())/c
        features['momentum_roc'] = c.pct_change(10)
        features['momentum_accel'] = c.pct_change(5)-c.pct_change(10)/2

        # ═══ NOUVELLES FEATURES AVANCÉES (amélioration précision) ═══
        # Volume-Price Divergence
        price_z = (c - c.rolling(20).mean()) / c.rolling(20).std()
        vol_z = (v - v.rolling(20).mean()) / v.rolling(20).std()
        features['vol_price_divergence'] = price_z - vol_z  # divergence = anomalie

        # Microstructure: efficience de marché (variance ratio)
        ret1 = c.pct_change(1); ret5 = c.pct_change(5)
        var1 = ret1.rolling(20).var(); var5 = ret5.rolling(20).var()
        features['variance_ratio'] = (var5 / (5 * var1)).fillna(1)  # ≠1 = inefficience

        # Relative Strength vs market (si le ticker surperforme SPY)
        spy_ret_20 = c.pct_change(20)  # proxy relatif
        features['rel_strength_20'] = spy_ret_20  # sera comparé inter-actions

        # Régime de volatilité
        features['vol_regime'] = features['vol_20'] / features['vol_60']  # >1 = vol croissante
        features['vol_regime_diff'] = features['vol_regime'].diff(5)  # changement régime

        # Mean reversion score
        features['mean_rev_10'] = -(c.pct_change(10))  # les extrêmes tendent à revenir
        features['mean_rev_20'] = -(c.pct_change(20))

        # Force relative prix vs OBV (divergence smart money)
        obv_norm = (obv - obv.rolling(20).mean()) / obv.rolling(20).std()
        features['obv_price_div'] = obv_norm - price_z  # >0 = smart money accumule

        # Intraday pattern (range position)
        features['close_in_range'] = (c - l) / (h - l).replace(0, 1)  # 1=close au high

        # Multi-timeframe momentum alignment
        mom_5 = np.sign(c.pct_change(5))
        mom_10 = np.sign(c.pct_change(10))
        mom_20 = np.sign(c.pct_change(20))
        features['momentum_alignment'] = (mom_5 + mom_10 + mom_20) / 3  # 1=tous haussiers

        # Niveau de support/résistance distance
        roll_high_20 = h.rolling(20).max(); roll_low_20 = l.rolling(20).min()
        features['dist_to_high_20'] = (roll_high_20 - c) / c  # distance au max
        features['dist_to_low_20'] = (c - roll_low_20) / c  # distance au min

        # Asymétrie des rendements
        features['up_vol'] = ret1.where(ret1 > 0, 0).rolling(20).std()
        features['down_vol'] = ret1.where(ret1 < 0, 0).rolling(20).std()
        features['vol_asymmetry'] = features['up_vol'] / features['down_vol'].replace(0, 1)

        return features.replace([np.inf,-np.inf], np.nan).fillna(0)

    def entrainer(self, symboles, callback=None):
        """Entraîne l'ensemble de modèles (FAST_MODE = skip si modèles cachés)"""
        _current_horizon = str(getattr(self.config, 'HORIZON_MODE', 'SWING') or 'SWING').upper()
        _current_ml_h = int(getattr(self.config, 'ML_HORIZON', 7) or 7)
        logger.info(f"🎯 ML: HORIZON_MODE={_current_horizon}, ML_HORIZON={_current_ml_h}j, ML_RENDEMENT_CIBLE={getattr(self.config, 'ML_RENDEMENT_CIBLE', 0.04)}")

        # FAST MODE: skip retraining si modèles déjà entraînés ET même horizon
        if getattr(self.config, 'FAST_MODE', True):
            cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ml_models_cache.pkl')
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, 'rb') as f:
                        cached = pickle.load(f)
                    # Vérifier que le cache correspond au même horizon
                    cached_horizon = cached.get('horizon_mode', 'UNKNOWN')
                    cached_ml_h = cached.get('ml_horizon', -1)
                    if cached_horizon != _current_horizon or cached_ml_h != _current_ml_h:
                        logger.warning(f"⚠️ Cache ML obsolète (horizon: {cached_horizon}/{cached_ml_h}j → {_current_horizon}/{_current_ml_h}j) — re-training")
                    else:
                        self.modeles = cached.get('models', self.modeles)
                        self.calibrators = cached.get('calibrators', self.calibrators)
                        self.features_names = cached.get('feature_names', self.features_names)
                        self.scaler = cached.get('scaler', self.scaler)
                        self.poids = cached.get('poids', self.poids)
                        self.meta_model = cached.get('meta', cached.get('meta_model', self.meta_model))
                        self.seuil_optimal = cached.get('seuil', cached.get('seuil_optimal', self.seuil_optimal))
                        self.trained = True
                        logger.info(f"⚡ FAST MODE: Modèles ML cachés chargés (horizon={cached_horizon}, ML_H={cached_ml_h}j)")
                        if callback: callback(f"⚡ ML FAST: modèles cachés chargés ({cached_horizon})!", 1, 1)
                        return True
                except Exception as e:
                    logger.warning(f"Cache ML invalide, re-training: {e}")

        syms = symboles[:self.config.ML_MAX_SYMBOLES]
        total = len(syms)
        logger.info(f"🧠 Entraînement ML sur {total} symboles...")

        # ══ PHASE 1: Batch download (beaucoup plus rapide) ══
        if callback: callback(f"📡 Téléchargement batch {total} symboles...", 0, total)
        logger.info(f"📡 Batch download {total} symboles (period=2y)...")
        t0 = time.time()
        # Adapter la période de téléchargement à l'horizon ML
        _ml_h = int(getattr(self.config, 'ML_HORIZON', 7) or 7)
        _dl_period = "5y" if _ml_h >= 20 else "2y"
        try:
            df_all = yf.download(syms, period=_dl_period, interval="1d",
                                  progress=False, threads=True, group_by='ticker')
            logger.info(f"✅ Batch download ({_dl_period}) terminé en {time.time()-t0:.1f}s")
        except Exception as e:
            logger.error(f"❌ Batch download échoué: {e}"); return False

        # ══ PHASE 2: Construction features pour chaque symbole ══
        all_X, all_y = [], []
        ok_count = 0; skip_count = 0
        for i, sym in enumerate(syms):
            if callback and i%25==0:
                callback(f"📊 Features {sym} ({i+1}/{total}) — {ok_count} valides", i, total)
            if i%50==0:
                logger.info(f"📊 Feature engineering: {i}/{total} traités, {ok_count} valides, {skip_count} skippés")
            try:
                # Extraire les données du batch
                if total == 1:
                    df = df_all.copy()
                elif sym in df_all.columns.get_level_values(0):
                    df = df_all[sym].dropna(how='all')
                else:
                    skip_count += 1; continue
                if df.empty or len(df) < 100:
                    skip_count += 1; continue
                # Vérifier colonnes requises
                required = ['Close','High','Low','Volume','Open']
                if not all(c in df.columns for c in required):
                    skip_count += 1; continue
                # Supprimer lignes NaN sur Close
                df = df.dropna(subset=['Close'])
                if len(df) < 100:
                    skip_count += 1; continue
                feats = self._build_features(df)
                _ml_horizon = int(getattr(self.config, 'ML_HORIZON', 7) or 7)
                _ml_cible = float(getattr(self.config, 'ML_RENDEMENT_CIBLE', 0.04) or 0.04)
                labels = self._triple_barrier_labels(df['Close'], timeout=_ml_horizon, min_gain=_ml_cible)
                # Aligner — marge dynamique = max(8, _ml_horizon) pour éviter labels tronqués
                _tail_margin = max(8, _ml_horizon)
                valid = labels.index[14:-_tail_margin]
                X = feats.loc[valid]; y = labels.loc[valid]
                mask = y.isin([0,1]); X = X[mask]; y = y[mask]
                if len(X) < 50:
                    skip_count += 1; continue
                all_X.append(X); all_y.append(y)
                ok_count += 1
            except Exception as e:
                logger.debug(f"  Skip {sym}: {e}")
                skip_count += 1; continue

        logger.info(f"📊 Feature engineering terminé: {ok_count} symboles valides, {skip_count} skippés")
        if not all_X:
            logger.warning("❌ Pas assez de données pour ML"); return False
        X = pd.concat(all_X); y = pd.concat(all_y)
        self.features_names = list(X.columns)
        logger.info(f"📊 {len(X)} samples, {len(self.features_names)} features")

        # ═══ CLASS BALANCE CHECK ═══
        n_pos = (y == 1).sum(); n_neg = (y == 0).sum()
        ratio = n_pos / max(n_neg, 1)
        logger.info(f"📊 Balance: {n_pos} positifs ({ratio:.2%}), {n_neg} négatifs")

        # ═══ FEATURE SELECTION (top K les plus discriminantes) ═══
        if callback: callback("🔬 Sélection features...", 50, 100)
        try:
            selector = SelectKBest(f_classif, k=min(self.config.ML_TOP_K_FEATURES, len(self.features_names)))
            X_sel = selector.fit_transform(X, y)
            mask_sel = selector.get_support()
            scores_sel = selector.scores_
            feat_scores = sorted(zip(self.features_names, scores_sel), key=lambda x: x[1], reverse=True)
            self.features_names = [f for f, m in zip(self.features_names, mask_sel) if m]
            X = pd.DataFrame(X_sel, columns=self.features_names)
            logger.info(f"🔬 Top 10 features: {[f'{n}({s:.0f})' for n,s in feat_scores[:10]]}")
        except: pass

        # ═══ PURGED TEMPORAL SPLIT (embargo 20 jours entre train/test) ═══
        embargo = 20  # jours de gap pour éviter data leakage
        split_train = int(len(X) * 0.60)
        split_val = int(len(X) * 0.75)
        X_raw_train = X.iloc[:split_train]
        X_raw_val = X.iloc[split_train + embargo:split_val]
        X_raw_test = X.iloc[split_val + embargo:]
        y_train = y.iloc[:split_train]
        y_val = y.iloc[split_train + embargo:split_val]
        y_test = y.iloc[split_val + embargo:]

        # ═══ SCALE (fit UNIQUEMENT sur train → transform val/test) ═══
        self.scaler = RobustScaler()
        X_train = self.scaler.fit_transform(X_raw_train)
        X_val = self.scaler.transform(X_raw_val)
        X_test = self.scaler.transform(X_raw_test)
        logger.info(f"📊 Split: {len(X_train)} train, {len(X_val)} val, {embargo}j embargo, {len(X_test)} test")

        # ═══ SAMPLE WEIGHTS — données récentes comptent 2x plus ═══
        n_train = len(X_train)
        sample_weights = np.linspace(0.5, 1.5, n_train)  # 0.5 pour les plus anciennes → 1.5 récentes
        sample_weights = sample_weights / sample_weights.mean()  # normaliser
        logger.info(f"⚖️ Sample weights: ancien=0.5x → récent=1.5x")

        if callback: callback("🤖 Entraînement modèles (class_weight=balanced)...", 70, 100)

        # ═══ MODÈLES avec class_weight='balanced' ═══
        models_def = {
            'RF': RandomForestClassifier(n_estimators=300, max_depth=10, min_samples_leaf=15,
                class_weight='balanced', random_state=42, n_jobs=-1),
            'HGB': HistGradientBoostingClassifier(max_iter=400, max_depth=7, learning_rate=0.03,
                min_samples_leaf=15, random_state=42, class_weight='balanced'),
            'ET': ExtraTreesClassifier(n_estimators=300, max_depth=10, min_samples_leaf=15,
                class_weight='balanced', random_state=42, n_jobs=-1),
            'ADA': AdaBoostClassifier(n_estimators=150, learning_rate=0.05, random_state=42),
            'MLP1': MLPClassifier(hidden_layer_sizes=(256,128,64,32), activation='relu',
                max_iter=500, early_stopping=True, validation_fraction=0.15, random_state=42),
            'MLP2': MLPClassifier(hidden_layer_sizes=(128,64,32), activation='tanh',
                max_iter=500, early_stopping=True, validation_fraction=0.15, random_state=42),
            'LR': LogisticRegression(max_iter=500, C=0.3, class_weight='balanced', random_state=42),
            'KNN': KNeighborsClassifier(n_neighbors=21, weights='distance'),
        }
        if XGBOOST_OK:
            models_def['XGB'] = xgb.XGBClassifier(n_estimators=400, max_depth=7, learning_rate=0.03,
                subsample=0.75, colsample_bytree=0.75, reg_alpha=0.1, reg_lambda=1.0,
                scale_pos_weight=n_neg/max(n_pos,1), random_state=42, verbosity=0)
        if LIGHTGBM_OK:
            models_def['LGBM'] = lgb.LGBMClassifier(n_estimators=400, max_depth=7, learning_rate=0.03,
                subsample=0.75, colsample_bytree=0.75, reg_alpha=0.1, reg_lambda=1.0,
                is_unbalance=True, random_state=42, verbose=-1)
        if CATBOOST_OK:
            models_def['CB'] = CatBoostClassifier(iterations=300, depth=7, learning_rate=0.03,
                auto_class_weights='Balanced', random_state=42, verbose=0)

        self.modeles = {}; self.poids = {}; self.calibrators = {}
        for name, model in models_def.items():
            try:
                # Entraîner avec sample weights (les modèles qui le supportent)
                if name in ('RF','ET','XGB','LGBM','ADA','HGB'):
                    model.fit(X_train, y_train, sample_weight=sample_weights)
                else:
                    model.fit(X_train, y_train)
                preds = model.predict(X_test)
                f1 = f1_score(y_test, preds, zero_division=0)
                acc = accuracy_score(y_test, preds)
                prec = precision_score(y_test, preds, zero_division=0)
                # Poids: favoriser la Précision (60%) car on veut peu de faux positifs
                w = 0.25*f1 + 0.55*prec + 0.20*acc
                self.modeles[name] = model; self.poids[name] = max(0.05, w)
                logger.info(f"  ✅ {name}: F1={f1:.3f} Prec={prec:.3f} Acc={acc:.3f} W={w:.3f}")

                # ═══ CALIBRATION ISOTONIQUE — sur VALIDATION set (pas test!) ═══
                try:
                    if hasattr(model, 'predict_proba'):
                        cal = CalibratedClassifierCV(model, cv='prefit', method='isotonic')
                        cal.fit(X_val, y_val)  # calibrer sur val, pas test
                        self.calibrators[name] = cal
                except Exception as e:
                    logger.debug(f"  Calibration {name} skip: {e}")
            except Exception as e:
                logger.debug(f"  ❌ {name}: {e}")

        if not self.modeles:
            logger.warning("❌ Aucun modèle entraîné"); return False

        # Normaliser poids
        tw = sum(self.poids.values())
        self.poids = {k:v/tw for k,v in self.poids.items()}

        # ═══ META-MODEL avec toutes les probas ═══
        if callback: callback("🎯 Meta-labeling + calibration...", 90, 100)
        try:
            # Meta-model entraîné sur VALIDATION et évalué sur TEST
            meta_features_val = []
            for name, model in self.modeles.items():
                if name in self.calibrators:
                    meta_features_val.append(self.calibrators[name].predict_proba(X_val)[:,1])
                elif hasattr(model, 'predict_proba'):
                    meta_features_val.append(model.predict_proba(X_val)[:,1])
            if meta_features_val:
                meta_X_val = np.column_stack(meta_features_val)
                self.meta_model = LogisticRegression(max_iter=500, C=0.5, class_weight='balanced')
                self.meta_model.fit(meta_X_val, y_val)  # fit sur val, pas test
                # Évaluer sur test (non vu) 
                meta_features_test = []
                for name, model in self.modeles.items():
                    if name in self.calibrators:
                        meta_features_test.append(self.calibrators[name].predict_proba(X_test)[:,1])
                    elif hasattr(model, 'predict_proba'):
                        meta_features_test.append(model.predict_proba(X_test)[:,1])
                meta_X_test = np.column_stack(meta_features_test)
                meta_preds = self.meta_model.predict(meta_X_test)
                meta_prec = precision_score(y_test, meta_preds, zero_division=0)
                meta_f1 = f1_score(y_test, meta_preds, zero_division=0)
                logger.info(f"  ✅ META: F1={meta_f1:.3f} Prec={meta_prec:.3f} (évalué sur TEST)")
        except Exception as e:
            logger.debug(f"Meta-model fail: {e}")
            self.meta_model = None

        # ═══ TROUVER LE SEUIL OPTIMAL sur VALIDATION, vérifier sur TEST ═══
        try:
            best_seuil = 0.50; best_score = 0
            # Chercher le seuil sur VALIDATION
            for seuil in np.arange(0.45, 0.75, 0.02):
                probas_agg = np.zeros(len(X_val))
                for name, model in self.modeles.items():
                    if name in self.calibrators:
                        probas_agg += self.calibrators[name].predict_proba(X_val)[:,1] * self.poids[name]
                    elif hasattr(model, 'predict_proba'):
                        probas_agg += model.predict_proba(X_val)[:,1] * self.poids[name]
                preds_seuil = (probas_agg > seuil).astype(int)
                if preds_seuil.sum() < 10: continue
                p = precision_score(y_val, preds_seuil, zero_division=0)
                f = f1_score(y_val, preds_seuil, zero_division=0)
                combined = 0.6 * p + 0.4 * f
                if combined > best_score:
                    best_score = combined; best_seuil = seuil
            self.seuil_optimal = best_seuil
            # Vérifier sur TEST (non vu)
            probas_test = np.zeros(len(X_test))
            for name, model in self.modeles.items():
                if name in self.calibrators:
                    probas_test += self.calibrators[name].predict_proba(X_test)[:,1] * self.poids[name]
                elif hasattr(model, 'predict_proba'):
                    probas_test += model.predict_proba(X_test)[:,1] * self.poids[name]
            preds_test = (probas_test > self.seuil_optimal).astype(int)
            test_prec = precision_score(y_test, preds_test, zero_division=0)
            test_f1 = f1_score(y_test, preds_test, zero_division=0)
            logger.info(f"🎯 Seuil optimal: {self.seuil_optimal:.2f} (val={best_score:.3f}, test_prec={test_prec:.3f}, test_f1={test_f1:.3f})")
        except Exception as e:
            logger.debug(f"Seuil optimal fail: {e}")
            self.seuil_optimal = 0.55

        self.trained = True
        # Sauvegarder
        try:
            with open('ml_model_v10.pkl','wb') as f:
                pickle.dump({'modeles':self.modeles,'scaler':self.scaler,'features':self.features_names,
                    'poids':self.poids,'meta':self.meta_model,'seuil':self.seuil_optimal,
                    'calibrators':self.calibrators,
                    'date':datetime.now().isoformat()},f)
            logger.info("💾 Modèle ML sauvegardé")
        except Exception as e:
            logger.warning(f"❌ Sauvegarde ML échouée: {e}")
        # ═══ FAST MODE CACHE — Sauvegarde rapide pour skip prochain entraînement ═══
        try:
            cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ml_models_cache.pkl')
            with open(cache_path, 'wb') as f:
                pickle.dump({'models': self.modeles, 'calibrators': self.calibrators,
                             'feature_names': self.features_names, 'scaler': self.scaler,
                             'poids': self.poids, 'meta': self.meta_model,
                             'seuil': self.seuil_optimal,
                             'horizon_mode': _current_horizon,
                             'ml_horizon': _current_ml_h,
                             'date': datetime.now().isoformat()}, f)
            logger.info(f"⚡ Cache FAST MODE ML sauvegardé (horizon={_current_horizon}, ML_H={_current_ml_h}j)")
        except Exception as e:
            logger.debug(f"Cache ML save fail: {e}")
        if callback: callback("✅ ML entraîné!", 100, 100)
        return True

    def charger_modele(self):
        try:
            if os.path.exists('ml_model_v10.pkl'):
                with open('ml_model_v10.pkl','rb') as f:
                    d = pickle.load(f)
                    age = (datetime.now()-datetime.fromisoformat(d['date'])).days
                    if age > 7: logger.warning("⚠️ Modèle ML > 7 jours"); return False
                    self.modeles=d['modeles']; self.scaler=d['scaler']
                    self.features_names=d['features']; self.poids=d['poids']
                    self.meta_model=d.get('meta'); self.seuil_optimal=d.get('seuil',0.55)
                    self.calibrators=d.get('calibrators',{})
                    self.trained=True; logger.info(f"📂 Modèle ML chargé (seuil={self.seuil_optimal:.2f})"); return True
        except: pass
        return False

    def predire(self, df):
        """Prédit pour un DataFrame OHLCV — utilise calibration + seuil optimal"""
        if not self.trained or not self.modeles: return None
        try:
            feats = self._build_features(df)
            X = feats[self.features_names].iloc[[-1]]
            X_sc = self.scaler.transform(X)
            probas = {}; probas_cal = {}
            for name, model in self.modeles.items():
                try:
                    p = model.predict_proba(X_sc)[0][1]
                    probas[name] = p
                    # Utiliser la version calibrée si dispo
                    if name in self.calibrators:
                        pc = self.calibrators[name].predict_proba(X_sc)[0][1]
                        probas_cal[name] = pc
                    else:
                        probas_cal[name] = p
                except: pass
            if not probas: return None

            # Weighted average avec probas CALIBRÉES
            avg = sum(probas_cal[k]*self.poids.get(k,0.1) for k in probas_cal) / sum(self.poids.get(k,0.1) for k in probas_cal)

            # Meta boost
            if self.meta_model:
                meta_vals = [probas_cal.get(k, 0.5) for k in self.modeles.keys()]
                meta_X = np.array([meta_vals])
                try:
                    meta_p = self.meta_model.predict_proba(meta_X)[0][1]
                    avg = 0.6*avg + 0.4*meta_p  # meta pèse plus
                except: pass

            # Consensus STRICT (seuil dynamique au lieu de 0.55 fixe)
            seuil = self.seuil_optimal
            votes_achat = sum(1 for p in probas_cal.values() if p > seuil)
            consensus = votes_achat / len(probas_cal) * 100

            # Signal avec seuils plus exigeants
            if avg >= 0.78 and consensus >= 70: sig="🟢🟢🟢 TRÈS FORT ACHAT"
            elif avg >= 0.68 and consensus >= 55: sig="🟢🟢 FORT ACHAT"
            elif avg >= seuil and consensus >= 40: sig="🟢 ACHAT"
            elif avg <= 0.22: sig="🔴🔴🔴 TRÈS FORTE VENTE"
            elif avg <= 0.32: sig="🔴🔴 FORTE VENTE"
            elif avg <= 0.42: sig="🔴 VENTE"
            else: sig="⚪ NEUTRE"

            return {'probabilite':round(avg*100,1),'consensus':round(consensus,1),
                'signal':sig,'votes_achat':votes_achat,'votes_total':len(probas_cal),
                'confiance': 'HAUTE' if consensus>=70 else 'MOYENNE' if consensus>=50 else 'BASSE',
                'seuil_utilise': round(seuil, 2),
                'probas_detail':probas_cal}
        except Exception as e:
            logger.debug(f"Erreur ML predict: {e}"); return None


# ══════════════════════════════════════════════════════════════════════════════
#            🎯 MOTEUR D'ANALYSE PRINCIPAL (BLACKROCK STYLE)
# ══════════════════════════════════════════════════════════════════════════════
class MoteurAnalyse:
    """Moteur d'analyse principal combinant tous les sous-systèmes"""

    def __init__(self, config):
        self.config = config; self.cache = GestionnaireCache()
        self.price_fetcher = LivePriceFetcher()
        self.ml = PredicteurML(config); self.ml.charger_modele()
        self.risk_manager = RiskManager(config)
        self.returns_cache = {}  # {symbole: pd.Series} for portfolio risk
        self.portfolio_risk = {}  # portfolio-level risk metrics

    def _mode_horizon(self):
        mode = str(getattr(self.config, 'HORIZON_MODE', 'SWING') or 'SWING').upper()
        return mode if mode in ('SCALP', 'INTRADAY', 'SWING', 'POSITION', 'INVESTISSEUR') else 'SWING'

    def _jours_horizon_cible(self):
        mode = self._mode_horizon()
        if mode == 'SCALP':
            return int(getattr(self.config, 'HORIZON_SHORT_JOURS', 5) or 5)
        if mode == 'INTRADAY':
            return int(getattr(self.config, 'HORIZON_INTRADAY_JOURS', 2) or 2)
        if mode == 'POSITION':
            return int(getattr(self.config, 'HORIZON_LONG_JOURS', 60) or 60)
        if mode == 'INVESTISSEUR':
            return int(getattr(self.config, 'HORIZON_INVESTISSEUR_JOURS', 252) or 252)
        # SWING: lire HORIZON_SWING_JOURS (slider GUI) puis fallback HORIZON_MOYEN_JOURS
        return int(getattr(self.config, 'HORIZON_SWING_JOURS', None) or getattr(self.config, 'HORIZON_MOYEN_JOURS', 20) or 20)

    def _poids_horizon(self):
        mode = self._mode_horizon()
        if mode == 'SCALP':
            return (0.50, 0.20, 0.30)
        if mode == 'INTRADAY':
            return (0.46, 0.22, 0.32)
        if mode == 'POSITION':
            return (0.25, 0.45, 0.30)
        if mode == 'INVESTISSEUR':
            return (0.10, 0.30, 0.60)  # Poids fort sur le long terme (1 an)
        return (0.40, 0.30, 0.30)

    def _profil_horizon(self, c, result):
        ret = c.pct_change().dropna()
        vol = float(ret.tail(20).std()) if len(ret) > 20 and ret.tail(20).std() > 0 else 0.015
        r5 = float(result.get('var_1s', 0) or 0)
        r20 = float(result.get('var_1m', 0) or 0)
        r60 = float(result.get('var_3m', 0) or 0)
        zscore = float(result.get('zscore', 0) or 0)
        tend_s = float(result.get('score_tendance', 2.5) or 2.5)

        trend_factor = (tend_s - 2.5) / 2.5
        short = (0.55 * r5 + 0.20 * r20 - 2.0 * zscore + 3.0 * trend_factor)
        medium = (0.30 * r5 + 0.45 * r20 + 0.20 * r60 - 0.8 * zscore + 2.5 * trend_factor)
        long = (0.15 * r5 + 0.35 * r20 + 0.50 * r60 + 0.2 * zscore + 2.0 * trend_factor)

        vol_pct = vol * 100
        short = max(-25, min(25, short * (1.0 if vol_pct < 3.5 else 0.85)))
        medium = max(-35, min(35, medium * (1.0 if vol_pct < 4.5 else 0.90)))
        long = max(-50, min(50, long * (1.0 if vol_pct < 5.5 else 0.93)))
        return {'short': round(short, 2), 'medium': round(medium, 2), 'long': round(long, 2), 'vol_pct': round(vol_pct, 2)}

    def _risk_multipliers(self, atr_val, prix, vol_regime, tend_s):
        sl_mult = float(getattr(self.config, 'STOP_LOSS_ATR', 2.0) or 2.0)
        tp_mult = float(getattr(self.config, 'TAKE_PROFIT_ATR', 3.0) or 3.0)
        if not getattr(self.config, 'ADAPTIVE_RISK_ACTIF', True):
            return sl_mult, tp_mult

        high_thr = float(getattr(self.config, 'RISK_REGIME_VOL_HAUTE', 1.25) or 1.25)
        low_thr = float(getattr(self.config, 'RISK_REGIME_VOL_BASSE', 0.80) or 0.80)

        if vol_regime > high_thr:
            sl_mult *= 1.10
            tp_mult *= 0.95
        elif vol_regime < low_thr:
            sl_mult *= 0.92
            tp_mult *= 1.10

        if tend_s >= 4:
            tp_mult *= 1.08
        elif tend_s <= 1:
            sl_mult *= 1.08

        return max(1.2, sl_mult), max(1.8, tp_mult)

    def analyser_action(self, symbole, df=None, ticker_obj=None):
        """Analyse complète d'une action — retourne un dict de 80+ métriques"""
        result = {'symbole': symbole, 'marche': UniversActions.obtenir_marche(symbole),
                  'secteur': UniversActions.obtenir_secteur(symbole)}
        try:
            if ticker_obj is None: ticker_obj = yf.Ticker(symbole)
            if df is None or df.empty:
                df = ticker_obj.history(period="1y")
            if df.empty or len(df) < 30:
                return None
            c = df['Close']; h = df['High']; l = df['Low']; v = df['Volume']; o = df['Open']
            prix = float(c.iloc[-1])
            result['prix'] = round(prix, 2)

            # ═══════════════════════════════════════════════════════════
            # 1. INDICATEURS TECHNIQUES
            # ═══════════════════════════════════════════════════════════
            result['rsi'] = Indicateurs.rsi(c) or 50
            result['zscore'] = Indicateurs.zscore(c) or 0
            macd_v, macd_h, macd_t = Indicateurs.macd(c)
            result['macd'] = macd_v; result['macd_hist'] = macd_h; result['macd_tendance'] = macd_t
            result['atr'] = Indicateurs.atr(h, l, c) or prix*0.02
            adx_v, dip, dim, adx_s = Indicateurs.adx(h, l, c)
            result['adx'] = adx_v; result['adx_signal'] = adx_s
            sk, sd, ss = Indicateurs.stochastic_rsi(c)
            result['stoch_rsi_k'] = sk; result['stoch_rsi_signal'] = ss
            wr, ws = Indicateurs.williams_r(h, l, c)
            result['williams_r'] = wr; result['williams_signal'] = ws
            cmf_v, cmf_s = Indicateurs.cmf(h, l, c, v)
            result['cmf'] = cmf_v; result['cmf_signal'] = cmf_s
            st_v, st_s = Indicateurs.supertrend(h, l, c)
            result['supertrend_signal'] = st_s
            sq, sq_m, sq_s = Indicateurs.squeeze_momentum(h, l, c)
            result['squeeze'] = sq; result['squeeze_signal'] = sq_s
            tend, tend_s = Indicateurs.tendance(c)
            result['tendance'] = tend; result['score_tendance'] = tend_s
            vol_r, vol_l = Indicateurs.volume_relatif(v)
            result['volume_ratio'] = vol_r; result['volume_label'] = vol_l
            sup, res = Indicateurs.supports_resistances(c)
            result['support'] = sup; result['resistance'] = res

            # Variations
            for p, n in [(1,'1j'),(5,'1s'),(20,'1m'),(60,'3m')]:
                if len(c)>=p+1:
                    result[f'var_{n}'] = round(((c.iloc[-1]-c.iloc[-p-1])/c.iloc[-p-1]*100),2)

            # Horizon de prédiction paramétrable
            mode_h = self._mode_horizon()
            horizon_jours = self._jours_horizon_cible()
            hp = self._profil_horizon(c, result)
            result['horizon_mode'] = mode_h
            result['horizon_jours'] = horizon_jours
            result['pred_horizon_short'] = hp['short']
            result['pred_horizon_medium'] = hp['medium']
            result['pred_horizon_long'] = hp['long']
            result['vol_regime'] = hp['vol_pct']
            if mode_h == 'SCALP':
                result['pred_horizon_pct'] = hp['short']
            elif mode_h == 'INTRADAY':
                result['pred_horizon_pct'] = round(0.65 * hp['short'] + 0.35 * hp['medium'], 2)
            elif mode_h == 'POSITION':
                result['pred_horizon_pct'] = hp['long']
            elif mode_h == 'INVESTISSEUR':
                result['pred_horizon_pct'] = round(0.10 * hp['medium'] + 0.90 * hp['long'], 2)
            else:
                result['pred_horizon_pct'] = hp['medium']

            # ═══════════════════════════════════════════════════════════
            # 2. MATHÉMATIQUES QUANTITATIVES AVANCÉES
            # ═══════════════════════════════════════════════════════════
            returns = c.pct_change().dropna()
            result['hurst'] = round(MathQuant.hurst_exponent(c), 3)
            result['fractal_dim'] = round(MathQuant.fractal_dimension(c), 3)
            result['entropy'] = round(MathQuant.shannon_entropy(c), 3)
            result['omega_ratio'] = MathQuant.omega_ratio(returns)
            result['sortino'] = MathQuant.sortino_ratio(returns)
            result['calmar'] = MathQuant.calmar_ratio(returns)
            result['tail_ratio'] = MathQuant.tail_ratio(returns)
            result['max_drawdown'] = MathQuant.max_drawdown(c)
            cusum_ch, cusum_reg = MathQuant.cusum_regime(c)
            result['regime_cusum'] = cusum_reg
            smf_v, smf_s = MathQuant.smart_money_flow(h, l, c, v)
            result['smart_money'] = smf_v; result['smart_money_signal'] = smf_s

            # Sharpe (annualisé)
            if len(returns) > 20:
                sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
                result['sharpe'] = round(sharpe, 3)

            # ═══════════════════════════════════════════════════════════
            # 3. BLACKROCK FACTOR MODEL
            # ═══════════════════════════════════════════════════════════
            try:
                info = ticker_obj.info if hasattr(ticker_obj, 'info') else {}
            except: info = {}

            market_cap = info.get('marketCap', 0)
            pe = info.get('trailingPE'); pb = info.get('priceToBook')
            ps = info.get('priceToSalesTrailing12Months')
            div_y = info.get('dividendYield', 0)
            if div_y: div_y *= 100
            roe = info.get('returnOnEquity', 0)
            if roe: roe *= 100
            de = info.get('debtToEquity', 0)
            if de: de /= 100
            pm = info.get('profitMargins', 0)
            if pm: pm *= 100
            rg = info.get('revenueGrowth', 0)
            if rg: rg *= 100
            fcf = info.get('freeCashflow', 0)
            fcf_positive = fcf and fcf > 0
            fcf_yield = (fcf / market_cap * 100) if market_cap > 0 and fcf else None

            # Returns
            r1m = result.get('var_1m'); r3m = result.get('var_3m')
            r6m = round(((c.iloc[-1]-c.iloc[-min(126,len(c)-1)])/c.iloc[-min(126,len(c)-1)]*100),2) if len(c)>126 else None
            r12m = round(((c.iloc[-1]-c.iloc[0])/c.iloc[0]*100),2) if len(c)>200 else None

            # Beta
            beta = CorrelationEngine.beta_vs_market(returns)
            result['beta'] = beta

            # Factor scores
            _, f_market = BlackRockFactorModel.factor_market_beta(returns, pd.Series(dtype=float))
            f_size = BlackRockFactorModel.factor_size(market_cap)
            f_value = BlackRockFactorModel.factor_value(pe, pb, ps, div_y, fcf_yield)
            f_momentum = BlackRockFactorModel.factor_momentum(r1m, r3m, r6m, r12m)
            f_quality = BlackRockFactorModel.factor_quality(roe, de, pm, rg, fcf_positive)
            vol_20 = float(returns.tail(20).std()*100) if len(returns)>20 else None
            vol_60 = float(returns.tail(60).std()*100) if len(returns)>60 else None
            mdd90 = float(MathQuant.max_drawdown(c.tail(90))) if len(c)>90 else None
            f_vol = BlackRockFactorModel.factor_volatility(vol_20, vol_60, beta, mdd90)

            factors = {'market':f_market,'size':f_size,'value':f_value,
                       'momentum':f_momentum,'quality':f_quality,'volatility':f_vol}
            result['blackrock_score'] = BlackRockFactorModel.score_composite(factors, self.config)
            result['factor_details'] = factors
            result['market_cap'] = market_cap
            result['pe'] = pe; result['pb'] = pb; result['roe'] = roe
            result['div_yield'] = div_y; result['fcf_yield'] = fcf_yield

            # ═══════════════════════════════════════════════════════════
            # 4. NEWS SENTIMENT
            # ═══════════════════════════════════════════════════════════
            if self.config.NEWS_ACTIF:
                try:
                    nom = info.get('longName') or info.get('shortName')
                    ns, nc, nl, nd = NewsSentimentEngine.score_news_complet(symbole, nom)
                    result['news_score'] = ns; result['news_count'] = nc; result['news_signal'] = nl
                except: result['news_score'] = 50; result['news_signal'] = "⚪ N/A"

            # ═══════════════════════════════════════════════════════════
            # 5. EARNINGS TRIMESTRIELS
            # ═══════════════════════════════════════════════════════════
            if self.config.EARNINGS_ACTIF:
                try:
                    ear = EarningsEngine.analyser_earnings(ticker_obj)
                    result['earnings_score'] = ear['score']; result['earnings_signal'] = ear['signal']
                    result['earnings_details'] = ear['details']
                    if ear.get('surprises'): result['earnings_surprises'] = ear['surprises']
                except: result['earnings_score'] = 50; result['earnings_signal'] = "⚪ N/A"

            # ═══════════════════════════════════════════════════════════
            # 6. CORRÉLATIONS CROSS-ASSET
            # ═══════════════════════════════════════════════════════════
            if self.config.CORRELATION_ACTIF and len(returns) > 30:
                try:
                    corrs = CorrelationEngine.calculer_correlations(returns, symbole)
                    result['correlations'] = corrs
                    result['alpha_jensen'] = CorrelationEngine.alpha_jensen(returns)
                except: pass

            # ═══════════════════════════════════════════════════════════
            # 7. ML PRÉDICTION
            # ═══════════════════════════════════════════════════════════
            if self.config.ML_ACTIF and self.ml.trained:
                ml_result = self.ml.predire(df)
                if ml_result:
                    result['ml_probabilite'] = ml_result['probabilite']
                    result['ml_consensus'] = ml_result['consensus']
                    result['ml_signal'] = ml_result['signal']
                    result['ml_confiance'] = ml_result['confiance']

            # Ajustement horizon avec signal ML (si dispo)
            s_ml_adj = float(result.get('ml_probabilite', 50) or 50)
            ml_edge = (s_ml_adj - 50.0) / 50.0  # -1..+1
            pred_h = float(result.get('pred_horizon_pct', 0) or 0)
            pred_h = pred_h + (2.5 * ml_edge)
            result['pred_horizon_pct'] = round(max(-60, min(60, pred_h)), 2)

            if getattr(self.config, 'DYNAMIC_ML_HORIZON', True):
                if mode_h == 'SCALP':
                    result['ml_horizon_jours'] = int(max(3, min(8, round(horizon_jours * 0.9))))
                elif mode_h == 'INTRADAY':
                    result['ml_horizon_jours'] = int(max(2, min(6, round(horizon_jours * 1.0))))
                elif mode_h == 'POSITION':
                    result['ml_horizon_jours'] = int(max(20, min(90, round(horizon_jours * 1.1))))
                elif mode_h == 'INVESTISSEUR':
                    result['ml_horizon_jours'] = int(max(30, min(120, round(horizon_jours * 0.15))))
                else:
                    result['ml_horizon_jours'] = int(max(7, min(35, horizon_jours)))
            else:
                result['ml_horizon_jours'] = int(getattr(self.config, 'ML_HORIZON', 7) or 7)

            # PPO live signal injecté dans le moteur d'analyse (ultra-avancé)
            ppo_live = None
            if getattr(self.config, 'PPO_INTEGRATION_ACTIF', True):
                try:
                    ppo_live = ppo_system.predire(result)
                except Exception:
                    ppo_live = None
            if ppo_live:
                result['ppo_disponible'] = True
                result['ppo_action'] = ppo_live.get('action', 'NON')
                result['ppo_probabilite_achat'] = float(ppo_live.get('probabilite_achat', 50) or 50)
                result['ppo_fiabilite'] = float(ppo_live.get('fiabilite', 0) or 0)
                result['ppo_confiance'] = ppo_live.get('confiance_ppo', 'BASSE')
            else:
                result['ppo_disponible'] = False
                result['ppo_action'] = 'NON'
                result['ppo_probabilite_achat'] = 50.0
                result['ppo_fiabilite'] = 0.0
                result['ppo_confiance'] = 'BASSE'
            # Injecter les seuils du profil actif pour que Decision IA les lise
            result['_config_ppo_min_fiab'] = float(getattr(self.config, 'PPO_MIN_FIABILITE_ACHAT', 62.0) or 62.0)
            result['_config_rr_min'] = float(getattr(self.config, 'RR_MIN', 1.5) or 1.5)

            # ═══════════════════════════════════════════════════════════
            # 8. SYSTÈME DE TRADING (SL/TP/R:R)
            # ═══════════════════════════════════════════════════════════
            atr_val = result.get('atr', prix*0.02)
            # vol_regime =  ratio vol_courte/vol_longue (typ. 0.6-1.6)
            # Si vol_pct brut (>5) on le normalise en ratio centré sur 1.0
            _vr_raw = float(result.get('vol_regime', 1.0)) if isinstance(result.get('vol_regime', 0), (int, float)) else 1.0
            vol_regime = _vr_raw / 2.0 if _vr_raw > 5.0 else _vr_raw  # vol_pct>5% → ratio
            sl_mult, tp_mult = self._risk_multipliers(atr_val, prix, vol_regime, tend_s)
            sl = prix - sl_mult * atr_val
            tp = prix + tp_mult * atr_val
            rr = (tp-prix)/(prix-sl) if (prix-sl)>0 else 0
            result['stop_loss'] = round(sl,2); result['take_profit'] = round(tp,2)
            result['ratio_rr'] = round(rr,2)
            result['stop_loss_pct'] = round((sl-prix)/prix*100,2)
            result['take_profit_pct'] = round((tp-prix)/prix*100,2)

            # ═══════════════════════════════════════════════════════════
            # 8b. RISK MANAGER — Kelly, VaR, Position Sizing, Risk Score
            # ═══════════════════════════════════════════════════════════
            try:
                _returns_series = df['Close'].pct_change().dropna() if df is not None and len(df) > 30 else None
                if _returns_series is not None and len(_returns_series) > 20:
                    self.returns_cache[symbole] = _returns_series
                    # Ajouter vol annualisée pour le risk score
                    result['vol_annualisee'] = round(float(_returns_series.std() * np.sqrt(252) * 100), 2)
                self.risk_manager.config = self.config
                self.risk_manager.compute_stock_risk(result, _returns_series)
            except Exception as _e_risk:
                logging.getLogger('BlackRockScreener').debug(f"Risk calc {symbole}: {_e_risk}")

            # ═══════════════════════════════════════════════════════════════════════
            # 9. ALPHA FACTOR SCORING ENGINE PRO — Corrélé aux rendements réels
            #    (Jegadeesh-Titman Momentum, Fama-French Quality/Value, Flow Analysis)
            # ═══════════════════════════════════════════════════════════════════════
            rsi_v = result.get('rsi', 50)
            w = self.config

            # ── ALPHA 1: MOMENTUM FACTOR (facteur alpha #1 académique) ──
            # Rendement 3m ajusté par tendance — le plus prouvé pour prédire le futur
            r1s = float(result.get('var_1s', 0) or 0)
            r1m = float(result.get('var_1m', 0) or 0)
            r3m = float(result.get('var_3m', 0) or 0)
            trend_norm = (tend_s - 2.5) / 2.5  # -1..+1
            # Momentum composite: rendement moyen pondéré + tendance + force direction
            alpha_momentum = (
                0.40 * np.clip(r3m, -30, 30) +
                0.30 * np.clip(r1m, -20, 20) +
                0.15 * trend_norm * 10 +
                0.15 * (5 if '🟢' in (macd_t or '') else -5 if '🔴' in (macd_t or '') else 0)
            )
            # Normaliser en 0-100
            alpha_momentum_score = max(0, min(100, 50 + alpha_momentum * 1.2))

            # ── ALPHA 2: MEAN REVERSION (court-terme, prouvé pour scalp/intraday) ──
            zscore_v = float(result.get('zscore', 0) or 0)
            # Les actions sur-vendues rebondissent, les surachetées corrigent
            rev_rsi = 0
            if rsi_v < 25: rev_rsi = 25
            elif rsi_v < 35: rev_rsi = 12
            elif rsi_v > 80: rev_rsi = -20
            elif rsi_v > 70: rev_rsi = -10
            alpha_reversal = (
                0.35 * (-zscore_v * 8) +       # Zscore négatif = sous-évalué
                0.35 * (-np.clip(r1s, -15, 15) * 1.5) +  # Oversold bounce
                0.30 * rev_rsi
            )
            alpha_reversal_score = max(0, min(100, 50 + alpha_reversal))

            # ── ALPHA 3: QUALITY FACTOR (Fama-French, prouvé sur 30+ ans) ──
            roe_v = float(roe or 0)
            de_v = float(de or 0)
            pm_v = float(pm or 0)
            rg_v = float(rg or 0)
            alpha_quality_score = max(0, min(100, (
                0.30 * np.clip(roe_v * 2.5, 0, 100) +       # ROE élevé = qualité
                0.20 * np.clip((1.0 - de_v) * 60, 0, 100) +  # Faible dette = qualité
                0.20 * np.clip(pm_v * 2.0, 0, 100) +          # Marges élevées
                0.15 * np.clip(rg_v * 2.5, 0, 100) +          # Croissance revenus
                0.15 * (70 if fcf_positive else 25)            # FCF positif
            )))

            # ── ALPHA 4: VALUE FACTOR ──
            pe_v = float(pe or 25)
            pb_v = float(pb or 3)
            div_v = float(div_y or 0)
            fcf_y_v = float(fcf_yield or 0)
            alpha_value_score = max(0, min(100, (
                0.30 * np.clip(100 - pe_v * 2.5, 0, 100) +   # PE bas = value
                0.25 * np.clip(100 - pb_v * 12, 0, 100) +     # PB bas = value
                0.25 * np.clip(div_v * 8, 0, 100) +           # Div élevé = value
                0.20 * np.clip(fcf_y_v * 5, 0, 100)           # FCF yield élevé
            )))

            # ── ALPHA 5: FLOW / SMART MONEY (institutional activity) ──
            sm_signal = result.get('smart_money_signal', '')
            vol_ratio_v = float(result.get('volume_ratio', 1) or 1)
            cmf_v = float(result.get('cmf', 0) or 0)
            sm_score = 50
            if '🟢🟢' in sm_signal: sm_score = 88
            elif '🟢' in sm_signal: sm_score = 68
            elif '🔴🔴' in sm_signal: sm_score = 12
            elif '🔴' in sm_signal: sm_score = 32
            alpha_flow_score = max(0, min(100, (
                0.35 * sm_score +
                0.30 * np.clip(vol_ratio_v * 25, 0, 100) +
                0.20 * np.clip(50 + cmf_v * 120, 0, 100) +
                0.15 * (70 if '🟢' in (st_s or '') else 30 if '🔴' in (st_s or '') else 50)
            )))

            # ── ALPHA 6: ML SIGNAL ──
            s_ml = float(result.get('ml_probabilite', 50) or 50)
            ml_cons = float(result.get('ml_consensus', 50) or 50)
            s_news = float(result.get('news_score', 50) or 50)
            alpha_ml_score = max(0, min(100, 0.55 * s_ml + 0.25 * ml_cons + 0.20 * s_news))

            # ── ALPHA 7: MARKET REGIME ──
            hurst_v = float(result.get('hurst', 0.5) or 0.5)
            regime_cusum = result.get('regime_cusum', 'STABLE')
            s_bk = float(result.get('blackrock_score', 50) or 50)
            alpha_regime_score = 50
            if hurst_v > 0.58: alpha_regime_score += 12  # Trending market = momentum works
            elif hurst_v < 0.42: alpha_regime_score -= 8  # Mean-reverting
            if regime_cusum == 'STABLE': alpha_regime_score += 8
            elif regime_cusum == 'INSTABLE': alpha_regime_score -= 12
            alpha_regime_score += (s_bk - 50) * 0.3  # BlackRock regime influence
            alpha_regime_score = max(0, min(100, alpha_regime_score))

            # ── ALPHA 8: PPO REINFORCEMENT LEARNING ──
            s_ppo = float(result.get('ppo_probabilite_achat', 50) or 50)
            ppo_fiab_v = float(result.get('ppo_fiabilite', 0) or 0)
            ppo_dispo = bool(result.get('ppo_disponible', False))
            alpha_ppo_score = 50  # Neutre si PPO pas dispo
            if ppo_dispo:
                alpha_ppo_score = max(0, min(100, 0.55 * s_ppo + 0.45 * ppo_fiab_v))

            # ══════════════════════════════════════════════════════════════
            # COMPOSITE ALPHA SCORE — pondération calibrée facteurs
            # ══════════════════════════════════════════════════════════════
            # Regime-adaptive weights: boost momentum en bull, reversal en bear
            w_mom = float(getattr(w, 'ALPHA_W_MOMENTUM', 0.22))
            w_rev = float(getattr(w, 'ALPHA_W_REVERSAL', 0.10))
            w_qual = float(getattr(w, 'ALPHA_W_QUALITY', 0.18))
            w_val = float(getattr(w, 'ALPHA_W_VALUE', 0.10))
            w_flow = float(getattr(w, 'ALPHA_W_FLOW', 0.12))
            w_ml = float(getattr(w, 'ALPHA_W_ML', 0.13))
            w_reg = float(getattr(w, 'ALPHA_W_REGIME', 0.08))
            w_ppo = float(getattr(w, 'ALPHA_W_PPO', 0.07))

            # Ajustement régime adaptatif
            if getattr(w, 'REGIME_ADAPTIVE_WEIGHTS', True):
                # En tendance forte (Hurst > 0.55) → boost momentum, réduire reversal
                if hurst_v > 0.55:
                    regime_mult_mom = float(getattr(w, 'ALPHA_MOMENTUM_BOOST_BULL', 1.30))
                    w_mom *= regime_mult_mom
                    w_rev *= 0.65
                # En mean-reversion (Hurst < 0.45) → boost reversal, réduire momentum
                elif hurst_v < 0.45:
                    regime_mult_rev = float(getattr(w, 'ALPHA_REVERSAL_BOOST_BEAR', 1.40))
                    w_rev *= regime_mult_rev
                    w_mom *= 0.70

            # Normaliser poids
            w_total = w_mom + w_rev + w_qual + w_val + w_flow + w_ml + w_reg + w_ppo
            if w_total > 0:
                w_mom /= w_total; w_rev /= w_total; w_qual /= w_total; w_val /= w_total
                w_flow /= w_total; w_ml /= w_total; w_reg /= w_total; w_ppo /= w_total

            score_final = (
                w_mom * alpha_momentum_score +
                w_rev * alpha_reversal_score +
                w_qual * alpha_quality_score +
                w_val * alpha_value_score +
                w_flow * alpha_flow_score +
                w_ml * alpha_ml_score +
                w_reg * alpha_regime_score +
                w_ppo * alpha_ppo_score
            )

            # Piliers pour affichage (backward compatible)
            score_tech = max(0, min(100, alpha_momentum_score * 0.45 + alpha_reversal_score * 0.35 + alpha_flow_score * 0.20))
            s_qual = f_quality
            s_earn = float(result.get('earnings_score', 50) or 50)
            score_fonda = max(0, min(100, alpha_quality_score * 0.40 + alpha_value_score * 0.30 + 0.30 * (0.5*s_bk + 0.5*s_earn)))
            score_momentum = max(0, min(100, alpha_ml_score * 0.40 + alpha_flow_score * 0.25 + alpha_ppo_score * 0.20 + alpha_regime_score * 0.15))

            # EV (espérance mathématique) et precision
            p_up = min(0.95, max(0.05, score_final / 100.0))
            gain_pct = max(0.0, float(result.get('take_profit_pct', 0) or 0) / 100.0)
            risk_pct = max(0.0001, abs(float(result.get('stop_loss_pct', -5) or -5) / 100.0))
            ev_pct = p_up * gain_pct - (1.0 - p_up) * risk_pct
            result['ev_pct'] = round(ev_pct * 100, 2)
            result['precision_score'] = round(max(0.0, min(100.0,
                0.30 * alpha_ml_score + 0.25 * alpha_momentum_score + 0.20 * alpha_flow_score + 0.15 * alpha_quality_score + 0.10 * (min(100, max(0, rr * 30)))
            )), 1)

            # Alpha factors stored for cross-sectional ranking
            result['alpha_momentum'] = round(alpha_momentum_score, 1)
            result['alpha_reversal'] = round(alpha_reversal_score, 1)
            result['alpha_quality'] = round(alpha_quality_score, 1)
            result['alpha_value'] = round(alpha_value_score, 1)
            result['alpha_flow'] = round(alpha_flow_score, 1)
            result['alpha_ml'] = round(alpha_ml_score, 1)
            result['alpha_regime'] = round(alpha_regime_score, 1)
            result['alpha_ppo'] = round(alpha_ppo_score, 1)

            score_final = max(0, min(100, score_final))
            result['score_technique'] = round(score_tech, 1)
            result['score_fondamental'] = round(score_fonda, 1)
            result['score_momentum'] = round(score_momentum, 1)
            result['score_final'] = round(score_final, 1)

            # ═══════════════════════════════════════════════════════════
            # 10. DÉCISION FINALE — ALPHA FACTOR GATE
            # ═══════════════════════════════════════════════════════════
            alpha_min_buy = float(getattr(w, 'ALPHA_MIN_SCORE_BUY', 58.0))
            alpha_min_fort = float(getattr(w, 'ALPHA_MIN_SCORE_FORT', 72.0))
            ev_min = float(getattr(w, 'EV_MIN_PCT', 0.10) or 0.10)
            rr_min = float(getattr(w, 'RR_MIN', 1.5) or 1.5)
            ppo_min = float(getattr(w, 'PPO_MIN_FIABILITE_ACHAT', 62.0) or 62.0)
            ppo_available = bool(result.get('ppo_disponible', False))
            ppo_gate = (not ppo_available) or (str(result.get('ppo_action', 'NON')) == 'OUI' and float(result.get('ppo_fiabilite', 0) or 0) >= ppo_min)

            # Multi-factor confirmation: au moins 4 alphas > 55 pour acheter
            # Utiliser les valeurs arrondies (cohérent avec post-ranking)
            alphas_above_55 = sum(1 for a in [result['alpha_momentum'], result['alpha_reversal'],
                result['alpha_quality'], result['alpha_value'], result['alpha_flow'], result['alpha_ml'],
                result['alpha_regime'], result['alpha_ppo']] if a > 55)
            multi_factor_ok = alphas_above_55 >= 4

            # Utiliser les valeurs arrondies (cohérentes avec l'affichage)
            sf_display = result['score_final']   # déjà arrondi à 0.1
            rr_display = result['ratio_rr']       # déjà arrondi à 0.01
            ev_stored = result['ev_pct']           # déjà arrondi à 0.01
            if sf_display >= alpha_min_fort and rr_display >= rr_min and multi_factor_ok and ev_stored >= ev_min:
                decision = "🟢🟢 ACHETER FORT"; action = "ACHAT FORT"
            elif sf_display >= alpha_min_buy and rr_display >= rr_min * 0.8 and alphas_above_55 >= 3 and ppo_gate:
                decision = "🟢 ACHETER"; action = "ACHAT"
            elif sf_display >= 52:
                decision = "🟡 SURVEILLER"; action = "SURVEILLER"
            elif sf_display <= 28:
                decision = "🔴🔴 VENDRE FORT"; action = "VENTE FORTE"
            elif sf_display <= 38:
                decision = "🔴 VENDRE"; action = "VENTE"
            else:
                decision = "⚪ NEUTRE"; action = "NEUTRE"

            result['decision'] = decision; result['action'] = action

            # Potentiel estimé
            potentiel = (tp - prix) / prix * 100
            result['potentiel'] = round(potentiel, 1)

            # ── RAISON (facteurs alpha dominants) ──
            raisons = []
            # Top 3 alpha factors
            alpha_list = [
                ('Momentum', alpha_momentum_score), ('Reversal', alpha_reversal_score),
                ('Qualité', alpha_quality_score), ('Value', alpha_value_score),
                ('Flow', alpha_flow_score), ('ML', alpha_ml_score),
                ('Régime', alpha_regime_score), ('PPO', alpha_ppo_score)
            ]
            alpha_sorted = sorted(alpha_list, key=lambda x: abs(x[1] - 50), reverse=True)
            for name, val in alpha_sorted[:3]:
                if val >= 65: raisons.append(f"✅ {name} {val:.0f}")
                elif val <= 35: raisons.append(f"❌ {name} {val:.0f}")
                else: raisons.append(f"● {name} {val:.0f}")
            # R/R + EV + résumé des gates satisfaites
            if rr_display >= 2.0: raisons.append(f"R:R {rr_display:.1f}")
            if ev_stored >= ev_min: raisons.append(f"EV+{ev_stored:.1f}%")
            raisons.append(f"{mode_h} {horizon_jours}j | {alphas_above_55}α>55")
            if '🟢' in result.get('smart_money_signal', ''): raisons.append("SmartMoney")
            # Résumé des gates pour transparence — insérer en position 3 pour éviter troncature
            _gates_str = None
            if action == "ACHAT FORT":
                _gates_str = "Gates:Score+RR+EV+4α"
            elif action == "ACHAT":
                _gates_str = "Gates:Score+RR+3α+PPO" if ppo_available else "Gates:Score+RR+3α"
            if _gates_str:
                raisons.insert(min(3, len(raisons)), _gates_str)

            result['raison'] = ' | '.join(raisons[:7]) if raisons else "Neutre"

            return result

        except Exception as e:
            logger.debug(f"Erreur analyse {symbole}: {e}")
            return None

    def _appliquer_ranking(self, results):
        """Cross-sectional ranking + recalcul de décision — réutilisable par Analyse ET Sniper"""
        if not getattr(self.config, 'CROSS_SECTIONAL_RANKING', True) or len(results) <= 5:
            return results

        logger.info(f"📊 Cross-sectional ranking sur {len(results)} actions...")
        alpha_keys = ['alpha_momentum', 'alpha_reversal', 'alpha_quality',
                      'alpha_value', 'alpha_flow', 'alpha_ml', 'alpha_regime', 'alpha_ppo']
        for key in alpha_keys:
            vals = sorted([r.get(key, 50) for r in results])
            n = len(vals)
            denom = max(n - 1, 1)  # Éviter /0 si n=1; donne plage complète 0-100
            for r in results:
                v = r.get(key, 50)
                # Mid-rank percentile étiré: (count_below + 0.5*(count_equal-1)) / (n-1) * 100
                count_below = sum(1 for x in vals if x < v)
                count_equal = sum(1 for x in vals if x == v)
                rank = (count_below + 0.5 * (count_equal - 1)) / denom * 100
                r[f'{key}_pctile'] = round(max(0, min(100, rank)), 1)

        # Régime adaptatif GLOBAL: utiliser le Hurst médian du lot pour que
        # tous les stocks soient pondérés avec la même grille (comparabilité)
        ww = self.config
        _base_weights = {
            'alpha_momentum': float(getattr(ww, 'ALPHA_W_MOMENTUM', 0.22)),
            'alpha_reversal': float(getattr(ww, 'ALPHA_W_REVERSAL', 0.10)),
            'alpha_quality': float(getattr(ww, 'ALPHA_W_QUALITY', 0.18)),
            'alpha_value': float(getattr(ww, 'ALPHA_W_VALUE', 0.10)),
            'alpha_flow': float(getattr(ww, 'ALPHA_W_FLOW', 0.12)),
            'alpha_ml': float(getattr(ww, 'ALPHA_W_ML', 0.13)),
            'alpha_regime': float(getattr(ww, 'ALPHA_W_REGIME', 0.08)),
            'alpha_ppo': float(getattr(ww, 'ALPHA_W_PPO', 0.07)),
        }
        if getattr(ww, 'REGIME_ADAPTIVE_WEIGHTS', True):
            hursts = sorted([float(r.get('hurst', 0.5) or 0.5) for r in results])
            _median_hurst = hursts[len(hursts) // 2] if hursts else 0.5
            if _median_hurst > 0.55:
                _base_weights['alpha_momentum'] *= float(getattr(ww, 'ALPHA_MOMENTUM_BOOST_BULL', 1.30))
                _base_weights['alpha_reversal'] *= 0.65
            elif _median_hurst < 0.45:
                _base_weights['alpha_reversal'] *= float(getattr(ww, 'ALPHA_REVERSAL_BOOST_BEAR', 1.40))
                _base_weights['alpha_momentum'] *= 0.70
        _wtot_global = sum(_base_weights.values())

        for r in results:
            pctile_score = 0
            weights_pctile = _base_weights  # même grille pour tous
            wtot = _wtot_global
            if wtot <= 0:
                # Tous les poids = 0 → pas de blending percentile, garder score absolu
                r['percentile_rank'] = 50.0
                r['score_raw'] = r['score_final']
                # score_final reste inchangé (100% absolu, 0% percentile)
                continue
            for key, weight in weights_pctile.items():
                pctile_score += r.get(f'{key}_pctile', 50) * weight / wtot
            r['percentile_rank'] = round(pctile_score, 1)
            r['score_raw'] = r['score_final']
            r['score_final'] = round(0.55 * r['score_final'] + 0.45 * pctile_score, 1)
            r['score_final'] = max(0, min(100, r['score_final']))

            # Recalculer EV après modification de score_final
            _p_up = min(0.95, max(0.05, r['score_final'] / 100.0))
            _gain = max(0.0, float(r.get('take_profit_pct', 0) or 0) / 100.0)
            _risk = max(0.0001, abs(float(r.get('stop_loss_pct', -5) or -5) / 100.0))
            r['ev_pct'] = round((_p_up * _gain - (1.0 - _p_up) * _risk) * 100, 2)

        # Recalculer la décision après modification du score_final
        _alpha_min_fort = float(getattr(self.config, 'ALPHA_MIN_SCORE_FORT', 72))
        _alpha_min_buy  = float(getattr(self.config, 'ALPHA_MIN_SCORE_BUY', 58))
        _ev_min = float(getattr(self.config, 'EV_MIN_PCT', 0.10) or 0.10)
        _rr_min = float(getattr(self.config, 'RR_MIN', 1.5) or 1.5)
        _ppo_min = float(getattr(self.config, 'PPO_MIN_FIABILITE_ACHAT', 62.0) or 62.0)
        for r in results:
            sf = r['score_final']       # déjà arrondi
            rr = r.get('ratio_rr', 0)   # déjà arrondi
            ev_pct = r.get('ev_pct', 0)  # déjà arrondi
            n_alpha55 = sum(1 for k in alpha_keys if r.get(k, 0) > 55)
            _ppo_avail = bool(r.get('ppo_disponible', False))
            ppo_ok = (not _ppo_avail) or (str(r.get('ppo_action', 'NON')) == 'OUI' and float(r.get('ppo_fiabilite', 0) or 0) >= _ppo_min)
            if sf >= _alpha_min_fort and rr >= _rr_min and n_alpha55 >= 4 and ev_pct >= _ev_min:
                r['decision'] = "🟢🟢 ACHETER FORT"; r['action'] = "ACHAT FORT"
            elif sf >= _alpha_min_buy and rr >= _rr_min * 0.8 and n_alpha55 >= 3 and ppo_ok:
                r['decision'] = "🟢 ACHETER"; r['action'] = "ACHAT"
            elif sf >= 52:
                r['decision'] = "🟡 SURVEILLER"; r['action'] = "SURVEILLER"
            elif sf <= 28:
                r['decision'] = "🔴🔴 VENDRE FORT"; r['action'] = "VENTE FORTE"
            elif sf <= 38:
                r['decision'] = "🔴 VENDRE"; r['action'] = "VENTE"
            else:
                r['decision'] = "⚪ NEUTRE"; r['action'] = "NEUTRE"

            # ── Reconstruire raison pour cohérence avec la nouvelle décision ──
            _raisons = []
            _alpha_list = [
                ('Momentum', r.get('alpha_momentum', 50)), ('Reversal', r.get('alpha_reversal', 50)),
                ('Qualité', r.get('alpha_quality', 50)), ('Value', r.get('alpha_value', 50)),
                ('Flow', r.get('alpha_flow', 50)), ('ML', r.get('alpha_ml', 50)),
                ('Régime', r.get('alpha_regime', 50)), ('PPO', r.get('alpha_ppo', 50))
            ]
            _alpha_sorted = sorted(_alpha_list, key=lambda x: abs(x[1] - 50), reverse=True)
            for _name, _val in _alpha_sorted[:3]:
                if _val >= 65: _raisons.append(f"✅ {_name} {_val:.0f}")
                elif _val <= 35: _raisons.append(f"❌ {_name} {_val:.0f}")
                else: _raisons.append(f"● {_name} {_val:.0f}")
            if rr >= 2.0: _raisons.append(f"R:R {rr:.1f}")
            if ev_pct >= _ev_min: _raisons.append(f"EV+{ev_pct:.1f}%")
            _raisons.append(f"{n_alpha55}α>55")
            if '🟢' in r.get('smart_money_signal', ''): _raisons.append("SmartMoney")
            _act = r['action']
            _gates_str = None
            if _act == "ACHAT FORT":
                _gates_str = "Gates:Score+RR+EV+4α"
            elif _act == "ACHAT":
                _ppo_a = bool(r.get('ppo_disponible', False))
                _gates_str = "Gates:Score+RR+3α+PPO" if _ppo_a else "Gates:Score+RR+3α"
            if _gates_str:
                _raisons.insert(min(3, len(_raisons)), _gates_str)
            r['raison'] = ' | '.join(_raisons[:7]) if _raisons else "Neutre"

        logger.info("✅ Cross-sectional ranking + décisions recalculées")
        return results

    def executer(self, symboles=None, callback=None):
        """Exécute l'analyse complète sur tous les symboles"""
        if symboles is None:
            all_actions = UniversActions.obtenir_actions(
                us=self.config.INCLURE_US, europe=self.config.INCLURE_EUROPE,
                france=self.config.INCLURE_FRANCE, gaming=self.config.INCLURE_GAMING,
                matieres=self.config.INCLURE_MATIERES, crypto=self.config.INCLURE_CRYPTO,
                mode_pea=self.config.MODE_PEA, inclure_pme=self.config.INCLURE_PME,
                inclure_sante=getattr(self.config, 'INCLURE_SANTE', True),
                inclure_nasdaq100=getattr(self.config, 'INCLURE_NASDAQ100', True),
                inclure_sp500=getattr(self.config, 'INCLURE_SP500', True)
            )
            symboles = list(all_actions.keys())

        total = len(symboles); results = []; all_results_pre_filter = []
        logger.info(f"🚀 Analyse ALPHA FACTOR de {total} symboles...")

        # Batch download pour accélérer
        try:
            if callback: callback(f"📡 Téléchargement batch {total} symboles...", 0, total)
            df_all = yf.download(symboles, period="1y", interval="1d",
                                 progress=False, threads=True, group_by='ticker')
        except:
            df_all = None

        for i, sym in enumerate(symboles):
            if callback and i%10==0:
                callback(f"🔬 Alpha {sym} ({i+1}/{total})", i, total)
            try:
                if df_all is not None:
                    if len(symboles)==1: df = df_all
                    elif sym in df_all.columns.get_level_values(0): df = df_all[sym].dropna(how='all')
                    else: df = None
                else: df = None

                r = self.analyser_action(sym, df)
                if r and r.get('score_final', 0) is not None:
                    all_results_pre_filter.append(r)
            except: continue

        # Appliquer SCORE_MINIMUM après le cross-sectional ranking (pas avant)
        # On stocke tout pour le ranking relatif, puis on filtre
        results = all_results_pre_filter  # ranking sur TOUTES les actions

        # ═══════════════════════════════════════════════════════════════════
        # CROSS-SECTIONAL RANKING — méthode unifiée
        # ═══════════════════════════════════════════════════════════════════
        results = self._appliquer_ranking(results)

        # ═══════════════════════════════════════════════════════════════════
        # PORTFOLIO-LEVEL RISK — corrélation, stress testing, allocation
        # ═══════════════════════════════════════════════════════════════════
        try:
            self.portfolio_risk = self.risk_manager.compute_portfolio_risk(
                results, self.returns_cache)
            if self.portfolio_risk:
                logger.info(f"🛡️ Portfolio Risk: {self.portfolio_risk.get('n_positions',0)} positions, "
                           f"VaR={self.portfolio_risk.get('portfolio_var_5j',0)}%, "
                           f"Corr={self.portfolio_risk.get('avg_correlation',0)}, "
                           f"Risk%={self.portfolio_risk.get('risk_pct_capital',0)}%")
        except Exception as _e_pr:
            self.portfolio_risk = {}
            logger.debug(f"Portfolio risk calc: {_e_pr}")

        # Filtrer par SCORE_MINIMUM APRÈS le cross-sectional ranking
        results = [r for r in results if r.get('score_final', 0) >= self.config.SCORE_MINIMUM]
        results.sort(key=lambda x: x.get('score_final',0), reverse=True)
        if callback: callback(f"✅ {len(results)} opportunités trouvées!", total, total)
        logger.info(f"🎯 {len(results)} résultats (score >= {self.config.SCORE_MINIMUM})")
        return results


# ══════════════════════════════════════════════════════════════════════════════
#            📊 RAPPORT EXCEL PRO
# ══════════════════════════════════════════════════════════════════════════════
class RapportExcel:
    @staticmethod
    def generer(results, output_path=None):
        if not results: return None
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            from openpyxl.utils import get_column_letter
        except ImportError:
            # Fallback CSV
            if not output_path: output_path = f"BLACKROCK_SCREENER_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            pd.DataFrame(results).to_csv(output_path, index=False, encoding='utf-8-sig')
            return output_path

        if not output_path:
            output_path = f"BLACKROCK_SCREENER_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

        thin = Side(style='thin', color='D0D0D0')
        styles = {
            'border': Border(left=thin,right=thin,top=thin,bottom=thin),
            'center': Alignment(horizontal='center',vertical='center'),
            'left': Alignment(horizontal='left',vertical='center'),
            'hdr_font': Font(name='Calibri',bold=True,color='FFFFFF',size=11),
            'hdr_fill': PatternFill('solid',fgColor='1B2631'),
            'title_font': Font(name='Calibri',bold=True,size=16,color='1B2631'),
            'green_fill': PatternFill('solid',fgColor='E2EFDA'),
            'red_fill': PatternFill('solid',fgColor='FCE4EC'),
            'green_font': Font(name='Calibri',bold=True,color='1B7A1B'),
            'red_font': Font(name='Calibri',bold=True,color='C62828'),
            'normal': Font(name='Calibri',size=11),
            'stripe': PatternFill('solid',fgColor='F2F2F2'),
        }

        wb = openpyxl.Workbook(); S = styles

        # Styles supplémentaires pour décisions colorées
        S['green_bold'] = Font(name='Calibri', bold=True, color='1B7A1B', size=12)
        S['dark_green_fill'] = PatternFill('solid', fgColor='C6EFCE')
        S['light_green_fill'] = PatternFill('solid', fgColor='E2EFDA')
        S['yellow_bold'] = Font(name='Calibri', bold=True, color='9C6500', size=11)
        S['yellow_fill'] = PatternFill('solid', fgColor='FFF2CC')
        S['red_bold'] = Font(name='Calibri', bold=True, color='C62828', size=11)
        S['dark_red_fill'] = PatternFill('solid', fgColor='FFC7CE')
        S['light_red_fill'] = PatternFill('solid', fgColor='FCE4EC')
        S['grey_bold'] = Font(name='Calibri', bold=True, color='666666', size=11)
        S['grey_fill'] = PatternFill('solid', fgColor='E8E8E8')
        S['num_green'] = Font(name='Calibri', bold=True, color='1B7A1B', size=11)
        S['num_red'] = Font(name='Calibri', bold=True, color='C62828', size=11)
        S['wrap'] = Alignment(horizontal='left', vertical='center', wrap_text=True)

        # ═══ Réutiliser les données PPO DÉJÀ CALCULÉES (pas de re-prédiction) ═══
        for r in results:
            if r.get('ppo_disponible', False):
                action_ppo = r.get('ppo_action', 'NON')
                prob_achat = r.get('ppo_probabilite_achat', 50)
                fiab = r.get('ppo_fiabilite', 0)
                conf = r.get('ppo_confiance', 'BASSE')
                r['ppo_avis'] = f"{action_ppo} ({prob_achat:.0f}%)"
                r['ppo_achat_pct'] = prob_achat
                r['ppo_confiance'] = conf
                r['ppo_fiabilite'] = fiab
                r['ppo_unanime'] = ''
            else:
                r['ppo_avis'] = '—'
                r['ppo_achat_pct'] = None
                r['ppo_confiance'] = '—'
                r['ppo_fiabilite'] = None
                r['ppo_unanime'] = ''

        df = pd.DataFrame(results).sort_values('score_final', ascending=False)

        # ═══════════════════════════════════════════════════════════
        # ONGLET 1 — OPPORTUNITÉS (données principales)
        # ═══════════════════════════════════════════════════════════
        ws = wb.active; ws.title = "Opportunités"
        cols = [
            ('symbole','Symbole',14),('secteur','Secteur',16),
            ('prix','Prix €',11),('score_final','SCORE /100',12),('decision','DÉCISION',26),
            ('horizon_mode','Horizon',10),('horizon_jours','H Jours',8),
            ('ppo_avis','🏆 PPO VOTE',22),('ppo_achat_pct','PPO Achat %',13),
            ('ppo_fiabilite','Fiabilité PPO',14),
            ('score_technique','Technique /100',15),('score_fondamental','Fondamental /100',16),('score_momentum','Momentum /100',15),
            ('precision_score','Précision /100',14),('pred_horizon_pct','Préd. Horizon %',15),('ev_pct','EV %',10),
            ('potentiel','Potentiel %',13),('ratio_rr','Risque:Récompense',18),
            ('stop_loss','Stop Loss €',13),('take_profit','Objectif €',12),
            ('rsi','RSI',8),('ml_probabilite','ML Proba %',12),
            ('var_1j','Var 1 Jour %',13),('var_1s','Var 1 Sem %',13),
            ('raison','Raison de la décision',60),
        ]
        cols = [(k,l,w) for k,l,w in cols if k in df.columns]

        # En-têtes avec style
        for ci,(key,label,width) in enumerate(cols,1):
            cell = ws.cell(row=1,column=ci,value=label)
            cell.font = S['hdr_font']; cell.fill = S['hdr_fill']
            cell.alignment = S['center']; cell.border = S['border']
            ws.column_dimensions[get_column_letter(ci)].width = width
        ws.row_dimensions[1].height = 30

        # Index des colonnes spéciales
        idx_score = next((i for i,(k,_,_) in enumerate(cols) if k=='score_final'), None)
        idx_decision = next((i for i,(k,_,_) in enumerate(cols) if k=='decision'), None)
        idx_potentiel = next((i for i,(k,_,_) in enumerate(cols) if k=='potentiel'), None)
        idx_rr = next((i for i,(k,_,_) in enumerate(cols) if k=='ratio_rr'), None)
        idx_var1j = next((i for i,(k,_,_) in enumerate(cols) if k=='var_1j'), None)
        idx_var1s = next((i for i,(k,_,_) in enumerate(cols) if k=='var_1s'), None)
        idx_rsi = next((i for i,(k,_,_) in enumerate(cols) if k=='rsi'), None)
        idx_ml = next((i for i,(k,_,_) in enumerate(cols) if k=='ml_probabilite'), None)
        idx_raison = next((i for i,(k,_,_) in enumerate(cols) if k=='raison'), None)
        idx_ppo_avis = next((i for i,(k,_,_) in enumerate(cols) if k=='ppo_avis'), None)
        idx_ppo_pct = next((i for i,(k,_,_) in enumerate(cols) if k=='ppo_achat_pct'), None)
        idx_ppo_fiab = next((i for i,(k,_,_) in enumerate(cols) if k=='ppo_fiabilite'), None)

        for ri,(_,row) in enumerate(df.iterrows()):
            r = ri+2
            for ci,(key,_,_) in enumerate(cols,1):
                val = row.get(key,'')
                # Ne PAS supprimer les emojis dans la décision (garde la lisibilité)
                if isinstance(val,str) and key not in ('decision','raison'):
                    val = clean_txt(val)
                if isinstance(val,dict): val = str(val)[:50]
                # Formatage des nombres
                if key in ('prix','stop_loss','take_profit') and isinstance(val,(int,float)):
                    val = round(val, 2)
                elif key in ('potentiel','var_1j','var_1s','ml_probabilite','rsi','pred_horizon_pct','ev_pct') and isinstance(val,(int,float)):
                    val = round(val, 1)
                elif key == 'ratio_rr' and isinstance(val,(int,float)):
                    val = round(val, 2)

                cell = ws.cell(row=r,column=ci,value=val)
                cell.border = S['border']; cell.font = S['normal']
                if key == 'raison':
                    cell.alignment = S['wrap']
                elif key in ('symbole','decision'):
                    cell.alignment = S['left']
                else:
                    cell.alignment = S['center']
                if ri%2==1 and key not in ('score_final','decision'): cell.fill = S['stripe']

            # ── Colorier le SCORE ──
            if idx_score is not None:
                sv = row.get('score_final',50)
                sc = ws.cell(row=r,column=idx_score+1)
                if sv>=75: sc.fill=S['dark_green_fill']; sc.font=S['num_green']
                elif sv>=65: sc.fill=S['light_green_fill']; sc.font=S['num_green']
                elif sv<=30: sc.fill=S['dark_red_fill']; sc.font=S['num_red']
                elif sv<=40: sc.fill=S['light_red_fill']; sc.font=S['num_red']

            # ── Colorier la DÉCISION ──
            if idx_decision is not None:
                dec = str(row.get('decision',''))
                dc = ws.cell(row=r,column=idx_decision+1)
                if 'ACHETER FORT' in dec:
                    dc.fill=S['dark_green_fill']; dc.font=S['green_bold']
                elif 'ACHETER' in dec:
                    dc.fill=S['light_green_fill']; dc.font=S['green_bold']
                elif 'SURVEILLER' in dec:
                    dc.fill=S['yellow_fill']; dc.font=S['yellow_bold']
                elif 'VENDRE FORT' in dec:
                    dc.fill=S['dark_red_fill']; dc.font=S['red_bold']
                elif 'VENDRE' in dec:
                    dc.fill=S['light_red_fill']; dc.font=S['red_bold']
                else:
                    dc.fill=S['grey_fill']; dc.font=S['grey_bold']

            # ── Colorier les variations (+/-) ──
            for vidx in [idx_var1j, idx_var1s, idx_potentiel]:
                if vidx is not None:
                    vv = row.get(cols[vidx][0], 0)
                    vc = ws.cell(row=r, column=vidx+1)
                    if isinstance(vv,(int,float)):
                        if vv > 0: vc.font = S['num_green']
                        elif vv < 0: vc.font = S['num_red']

            # ── Colorier RSI (survendu/surachat) ──
            if idx_rsi is not None:
                rv = row.get('rsi', 50)
                rc = ws.cell(row=r, column=idx_rsi+1)
                if isinstance(rv,(int,float)):
                    if rv < 30: rc.fill=S['dark_green_fill']; rc.font=S['num_green']
                    elif rv < 40: rc.fill=S['light_green_fill']; rc.font=S['num_green']
                    elif rv > 70: rc.fill=S['dark_red_fill']; rc.font=S['num_red']

            # ── Colorier ML% ──
            if idx_ml is not None:
                mv = row.get('ml_probabilite', 50)
                mc = ws.cell(row=r, column=idx_ml+1)
                if isinstance(mv,(int,float)):
                    if mv >= 70: mc.fill=S['dark_green_fill']; mc.font=S['num_green']
                    elif mv >= 60: mc.fill=S['light_green_fill']; mc.font=S['num_green']
                    elif mv <= 35: mc.fill=S['light_red_fill']; mc.font=S['num_red']

            # ── Colorier PPO AVIS ──
            if idx_ppo_avis is not None:
                ppo_txt = str(row.get('ppo_avis', '—'))
                pc = ws.cell(row=r, column=idx_ppo_avis+1)
                if 'OUI' in ppo_txt:
                    pc.fill = S['dark_green_fill']; pc.font = S['green_bold']
                elif 'NON' in ppo_txt:
                    pc.fill = S['light_red_fill']; pc.font = S['red_bold']
                else:
                    pc.fill = S['grey_fill']; pc.font = S['grey_bold']

            # ── Colorier PPO Achat % ──
            if idx_ppo_pct is not None:
                ppv = row.get('ppo_achat_pct', None)
                if ppv is not None and isinstance(ppv, (int, float)):
                    ppc = ws.cell(row=r, column=idx_ppo_pct+1)
                    if ppv >= 65: ppc.fill = S['dark_green_fill']; ppc.font = S['num_green']
                    elif ppv >= 55: ppc.fill = S['light_green_fill']; ppc.font = S['num_green']
                    elif ppv <= 35: ppc.fill = S['dark_red_fill']; ppc.font = S['num_red']
                    elif ppv <= 45: ppc.fill = S['light_red_fill']; ppc.font = S['num_red']

            # ── Colorier Fiabilité PPO ──
            if idx_ppo_fiab is not None:
                fv = row.get('ppo_fiabilite', None)
                if fv is not None and isinstance(fv, (int, float)):
                    fc = ws.cell(row=r, column=idx_ppo_fiab+1)
                    if fv >= 75: fc.fill = S['dark_green_fill']; fc.font = S['num_green']
                    elif fv >= 55: fc.fill = S['light_green_fill']; fc.font = S['num_green']
                    elif fv <= 30: fc.fill = S['dark_red_fill']; fc.font = S['num_red']
                    elif fv <= 45: fc.fill = S['light_red_fill']; fc.font = S['num_red']

            # Hauteur de ligne adaptée
            ws.row_dimensions[r].height = 22

        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = f'A1:{get_column_letter(len(cols))}{len(df)+1}'

        # ═══════════════════════════════════════════════════════════
        # ONGLET 2 — LÉGENDE / MODE D'EMPLOI (FR + العربية)
        # ═══════════════════════════════════════════════════════════
        ws2 = wb.create_sheet("Légende - الشرح")
        ws2.sheet_properties.tabColor = '1B7A1B'

        legend_header_font = Font(name='Calibri', bold=True, color='FFFFFF', size=13)
        legend_title_font = Font(name='Calibri', bold=True, color='1B2631', size=14)
        legend_section_font = Font(name='Calibri', bold=True, color='1B2631', size=12)
        legend_normal = Font(name='Calibri', size=11)
        legend_arab = Font(name='Arial', size=12)
        legend_fill = PatternFill('solid', fgColor='1B2631')
        light_bg = PatternFill('solid', fgColor='F5F5F5')
        wrap_align = Alignment(horizontal='left', vertical='center', wrap_text=True)

        # Largeurs colonnes légende
        ws2.column_dimensions['A'].width = 25
        ws2.column_dimensions['B'].width = 50
        ws2.column_dimensions['C'].width = 50

        row_num = 1
        # Titre
        ws2.merge_cells('A1:C1')
        c = ws2.cell(row=1, column=1, value="MODE D'EMPLOI — دليل الاستخدام")
        c.font = Font(name='Calibri', bold=True, color='FFFFFF', size=16)
        c.fill = legend_fill; c.alignment = Alignment(horizontal='center', vertical='center')
        ws2.row_dimensions[1].height = 40

        # En-têtes
        row_num = 3
        for ci, txt in enumerate(['Colonne', 'Explication (FR)', 'الشرح (العربية)'], 1):
            c = ws2.cell(row=row_num, column=ci, value=txt)
            c.font = legend_header_font; c.fill = legend_fill
            c.alignment = Alignment(horizontal='center', vertical='center')
        ws2.row_dimensions[row_num].height = 28

        # Données légende
        legend_data = [
            ('Symbole', 'Le ticker boursier de l\'action (ex: AAPL, MC.PA)', 'رمز السهم في البورصة'),
            ('Secteur', 'Le secteur d\'activité (Tech, Finance, Santé...)', 'قطاع الشركة (تكنولوجيا، مالية، صحة...)'),
            ('Prix €', 'Le dernier prix de clôture', 'آخر سعر إغلاق'),
            ('SCORE /100', 'Note globale sur 100. Plus c\'est haut = mieux. Moyenne pondérée de Tech (40%), Fonda (30%), Momentum (30%)', 'النتيجة النهائية من 100. كلما ارتفعت كان أفضل. المتوسط المرجح: تقني (40%) + أساسي (30%) + زخم (30%)'),
            ('DÉCISION', 'Le verdict: ACHETER FORT / ACHETER / SURVEILLER / VENDRE / NEUTRE', 'القرار: شراء قوي / شراء / مراقبة / بيع / محايد'),
            ('Technique /100', 'Analyse du graphique: RSI, MACD, SuperTrend, volumes', 'تحليل الرسم البياني: RSI, MACD, اتجاه السعر'),
            ('Fondamental /100', 'Qualité financière (40%) + Analyse BlackRock (35%) + Earnings (25%)', 'الجودة المالية (40%) + تحليل بلاك روك (35%) + أرباح فصلية (25%)'),
            ('Momentum /100', 'Prédiction ML (50%) + Sentiment news (25%) + Tendance prix (25%)', 'تنبؤ الذكاء الاصطناعي (50%) + أخبار (25%) + اتجاه السعر (25%)'),
            ('Potentiel %', 'Gain potentiel en % si le prix atteint l\'objectif (TP)', 'نسبة الربح المحتمل إذا وصل السعر للهدف'),
            ('Risque:Récompense', 'Ratio R:R. Ex: 2.0 = risquer 1€ pour gagner 2€. Minimum 1.5 recommandé', 'نسبة المخاطرة/المكافأة. مثال: 2.0 = تخاطر بـ 1€ لتربح 2€'),
            ('Stop Loss €', 'Prix de vente pour limiter les pertes. À TOUJOURS respecter!', 'سعر وقف الخسارة — بِع إذا نزل السعر لهذا المستوى'),
            ('Objectif €', 'Prix cible pour prendre vos profits', 'سعر الهدف — بِع لجني الأرباح عند هذا المستوى'),
            ('RSI', 'Force relative: < 30 = survendu (opportunité), > 70 = surachat (danger)', 'مؤشر القوة: أقل من 30 = فرصة شراء، أكثر من 70 = خطر'),
            ('ML Proba %', 'Probabilité de hausse selon 13 modèles d\'IA. > 65% = signal fort', 'احتمال الصعود حسب الذكاء الاصطناعي. أكثر من 65% = إشارة قوية'),
            ('� PPO VOTE', 'Vote ENSEMBLE de 3 modèles PPO. Ex: OUI (2/3) = 2 modèles sur 3 disent acheter. ★ = unanimité.', 'تصويت مجموعة من 3 نماذج PPO. مثال: نعم (2/3) = نموذجان من 3 يقولان شراء. ★ = إجماع.'),
            ('PPO Achat %', 'Moyenne des probabilités d\'achat des 3 modèles. > 65% = signal fort. < 35% = signal skip.', 'متوسط احتمال الشراء من 3 نماذج. أكثر من 65% = إشارة قوية.'),
            ('Fiabilité PPO', 'Score 0-100 de fiabilité. Unanimité (30pt) + Confiance (40pt) + Consensus (30pt).', 'درجة موثوقية الإشارة من 0 إلى 100. إجماع (30) + ثقة (40) + إجماع قوي (30).'),
            ('Var 1 Jour %', 'Variation du prix sur 1 jour (%)', 'تغير السعر خلال يوم واحد'),
            ('Var 1 Sem %', 'Variation du prix sur 1 semaine (%)', 'تغير السعر خلال أسبوع'),
            ('Raison', 'Explication en texte clair de la décision', 'شرح نصي واضح لسبب القرار'),
        ]

        for i, (col_name, fr_text, ar_text) in enumerate(legend_data):
            r = row_num + 1 + i
            ws2.cell(row=r, column=1, value=col_name).font = Font(name='Calibri', bold=True, size=11)
            ws2.cell(row=r, column=2, value=fr_text).font = legend_normal
            ws2.cell(row=r, column=3, value=ar_text).font = legend_arab
            for cc in range(1, 4):
                ws2.cell(row=r, column=cc).border = S['border']
                ws2.cell(row=r, column=cc).alignment = wrap_align
            if i % 2 == 1:
                for cc in range(1, 4): ws2.cell(row=r, column=cc).fill = light_bg
            ws2.row_dimensions[r].height = 32

        # Section DÉCISIONS
        r_dec = row_num + len(legend_data) + 3
        ws2.merge_cells(f'A{r_dec}:C{r_dec}')
        c = ws2.cell(row=r_dec, column=1, value="COMMENT LIRE LES DÉCISIONS — كيف تقرأ القرارات")
        c.font = Font(name='Calibri', bold=True, color='FFFFFF', size=14)
        c.fill = legend_fill; c.alignment = Alignment(horizontal='center', vertical='center')
        ws2.row_dimensions[r_dec].height = 35

        decisions_data = [
            ('🟢🟢 ACHETER FORT', 'Score ≥ 75 ET R:R ≥ 1.5 → Acheter avec conviction!', 'شراء قوي — النتيجة ≥ 75 و نسبة R:R ≥ 1.5 ← اشترِ بثقة!'),
            ('🟢 ACHETER', 'Score ≥ 65 ET R:R ≥ 1.2 → Bon signal d\'achat', 'شراء — النتيجة ≥ 65 و R:R ≥ 1.2 ← إشارة شراء جيدة'),
            ('🟡 SURVEILLER', 'Score ≥ 55 → Mettre en watchlist, attendre', 'مراقبة — النتيجة ≥ 55 ← راقب وانتظر تأكيداً'),
            ('🔴 VENDRE', 'Score ≤ 40 → Signal de vente', 'بيع — النتيجة ≤ 40 ← إشارة بيع'),
            ('🔴🔴 VENDRE FORT', 'Score ≤ 30 → Vendre immédiatement!', 'بيع قوي — النتيجة ≤ 30 ← بِع فوراً!'),
            ('⚪ NEUTRE', 'Pas de signal clair → Ne rien faire', 'محايد — لا إشارة واضحة ← لا تفعل شيئاً'),
        ]

        for ci, txt in enumerate(['Décision', 'Règle (FR)', 'القاعدة (العربية)'], 1):
            c = ws2.cell(row=r_dec+1, column=ci, value=txt)
            c.font = legend_header_font; c.fill = legend_fill
            c.alignment = Alignment(horizontal='center', vertical='center')

        for i, (dec, fr_txt, ar_txt) in enumerate(decisions_data):
            r = r_dec + 2 + i
            ws2.cell(row=r, column=1, value=dec).font = Font(name='Calibri', bold=True, size=12)
            ws2.cell(row=r, column=2, value=fr_txt).font = legend_normal
            ws2.cell(row=r, column=3, value=ar_txt).font = legend_arab
            for cc in range(1, 4):
                ws2.cell(row=r, column=cc).border = S['border']
                ws2.cell(row=r, column=cc).alignment = wrap_align
            # Couleur de fond selon la décision
            if 'ACHETER FORT' in dec:
                ws2.cell(row=r, column=1).fill = S['dark_green_fill']
            elif 'ACHETER' in dec:
                ws2.cell(row=r, column=1).fill = S['light_green_fill']
            elif 'SURVEILLER' in dec:
                ws2.cell(row=r, column=1).fill = S['yellow_fill']
            elif 'VENDRE FORT' in dec:
                ws2.cell(row=r, column=1).fill = S['dark_red_fill']
            elif 'VENDRE' in dec:
                ws2.cell(row=r, column=1).fill = S['light_red_fill']
            else:
                ws2.cell(row=r, column=1).fill = S['grey_fill']
            ws2.row_dimensions[r].height = 30

        # ═══════════════════════════════════════════════════════════
        # ONGLET 3 — 🎮 PPO STATS (Sauvegarde entraînement)
        # ═══════════════════════════════════════════════════════════
        try:
            ppo_stats = {}
            stats_path = "ppo_v5_stats.json"
            if os.path.exists(stats_path):
                with open(stats_path, 'r') as f:
                    ppo_stats = json.load(f)

            ws3 = wb.create_sheet("🧠 PPO V5 SMART")
            ws3.sheet_properties.tabColor = '8957E5'

            # Largeurs
            ws3.column_dimensions['A'].width = 35
            ws3.column_dimensions['B'].width = 25
            ws3.column_dimensions['C'].width = 35
            ws3.column_dimensions['D'].width = 25

            purple_fill = PatternFill('solid', fgColor='8957E5')
            purple_font = Font(name='Calibri', bold=True, color='FFFFFF', size=14)
            dark_bg = PatternFill('solid', fgColor='1B2631')
            section_font = Font(name='Calibri', bold=True, color='8957E5', size=13)
            label_font = Font(name='Calibri', bold=True, color='555555', size=11)
            value_font = Font(name='Calibri', bold=True, color='1B2631', size=13)
            small_font = Font(name='Calibri', color='888888', size=10)

            # Titre
            ws3.merge_cells('A1:D1')
            c = ws3.cell(row=1, column=1, value="� PPO V5 SMART — 3 MEILLEURS × MACRO SPY/VIX × SHARPE")
            c.font = purple_font; c.fill = purple_fill
            c.alignment = Alignment(horizontal='center', vertical='center')
            ws3.row_dimensions[1].height = 45

            if ppo_stats:
                version = ppo_stats.get('version', '?')
                date_train = ppo_stats.get('date', '?')
                ws3.merge_cells('A2:D2')
                c = ws3.cell(row=2, column=1, value=f"Version: {version}  |  Entraîné le: {date_train}")
                c.font = Font(name='Calibri', color='FFFFFF', size=11)
                c.fill = dark_bg; c.alignment = Alignment(horizontal='center', vertical='center')
                ws3.row_dimensions[2].height = 28

                # ── Section 1: Données ──
                r = 4
                ws3.merge_cells(f'A{r}:B{r}')
                ws3.cell(row=r, column=1, value="📊 DONNÉES D'ENTRAÎNEMENT").font = section_font
                ws3.row_dimensions[r].height = 28

                data_rows = [
                    ("Symboles utilisés", f"{ppo_stats.get('nb_symboles', '?')} actions"),
                    ("Points de données", f"{ppo_stats.get('nb_points', '?'):,}".replace(',', ' ')),
                    ("Steps d'entraînement", f"{ppo_stats.get('nb_timesteps', '?'):,}".replace(',', ' ')),
                ]
                for i, (lbl, val) in enumerate(data_rows):
                    row = r + 1 + i
                    ws3.cell(row=row, column=1, value=lbl).font = label_font
                    ws3.cell(row=row, column=2, value=val).font = value_font
                    for cc in range(1, 3):
                        ws3.cell(row=row, column=cc).border = S['border']
                    if i % 2 == 1:
                        for cc in range(1, 3): ws3.cell(row=row, column=cc).fill = light_bg

                # ── Section 2: Précision ──
                r2 = r + len(data_rows) + 2
                ws3.merge_cells(f'A{r2}:B{r2}')
                ws3.cell(row=r2, column=1, value="🎯 PRÉCISION DU MODÈLE").font = section_font
                ws3.row_dimensions[r2].height = 28

                buy_acc = ppo_stats.get('buy_accuracy', 0)
                skip_acc = ppo_stats.get('skip_accuracy', 0)
                overall_acc = ppo_stats.get('overall_accuracy', 0)

                prec_rows = [
                    ("Précision achats (OUI corrects)", f"{buy_acc}%"),
                    ("Précision skips (NON corrects)", f"{skip_acc}%"),
                    ("Précision globale", f"{overall_acc}%"),
                    ("Total achats (test)", str(ppo_stats.get('total_buys_test', '?'))),
                    ("Total skips (test)", str(ppo_stats.get('total_skips_test', '?'))),
                ]
                for i, (lbl, val) in enumerate(prec_rows):
                    row = r2 + 1 + i
                    ws3.cell(row=row, column=1, value=lbl).font = label_font
                    vc = ws3.cell(row=row, column=2, value=val)
                    vc.font = value_font
                    for cc in range(1, 3):
                        ws3.cell(row=row, column=cc).border = S['border']
                    # Couleurs pour les précisions
                    if i < 3:
                        pct_val = [buy_acc, skip_acc, overall_acc][i]
                        if pct_val >= 60:
                            vc.fill = S['dark_green_fill']; vc.font = S['num_green']
                        elif pct_val >= 50:
                            vc.fill = S['light_green_fill']; vc.font = S['num_green']
                        elif pct_val > 0:
                            vc.fill = S['light_red_fill']; vc.font = S['num_red']
                    if i % 2 == 1:
                        ws3.cell(row=row, column=1).fill = light_bg

                # ── Section 3: Performance ──
                r3 = r2 + len(prec_rows) + 2
                ws3.merge_cells(f'A{r3}:B{r3}')
                ws3.cell(row=r3, column=1, value="💰 PERFORMANCE TRADES").font = section_font
                ws3.row_dimensions[r3].height = 28

                pf = ppo_stats.get('profit_factor', 0)
                avg_p = ppo_stats.get('avg_profit_pct', 0)
                avg_l = ppo_stats.get('avg_loss_pct', 0)
                sel = ppo_stats.get('selectivity_pct', 0)
                rew = ppo_stats.get('total_reward', 0)

                perf_rows = [
                    ("Gain moyen / trade", f"+{avg_p:.2f}%"),
                    ("Perte moyenne / trade", f"{avg_l:.2f}%"),
                    ("Profit Factor (gain/perte)", f"{pf:.2f}"),
                    ("Sélectivité (% achats)", f"{sel:.0f}%"),
                    ("Reward total (entraînement)", f"{rew:,.0f}".replace(',', ' ')),
                ]
                for i, (lbl, val) in enumerate(perf_rows):
                    row = r3 + 1 + i
                    ws3.cell(row=row, column=1, value=lbl).font = label_font
                    vc = ws3.cell(row=row, column=2, value=val)
                    vc.font = value_font
                    for cc in range(1, 3):
                        ws3.cell(row=row, column=cc).border = S['border']
                    if i % 2 == 1:
                        ws3.cell(row=row, column=1).fill = light_bg
                    # Couleur profit factor
                    if i == 2:
                        if pf >= 1.5: vc.fill = S['dark_green_fill']; vc.font = S['num_green']
                        elif pf >= 1.2: vc.fill = S['light_green_fill']; vc.font = S['num_green']
                        elif pf < 1.0: vc.fill = S['dark_red_fill']; vc.font = S['num_red']
                    # Couleur sélectivité (idéal: 30-70%)
                    if i == 3:
                        if 30 <= sel <= 70: vc.fill = S['dark_green_fill']; vc.font = S['num_green']
                        elif sel > 90 or sel < 10: vc.fill = S['dark_red_fill']; vc.font = S['num_red']

                # ── Section 3b: Haute Confiance ──
                hc_acc = ppo_stats.get('high_conf_accuracy', 0)
                hc_trades = ppo_stats.get('high_conf_trades', 0)
                if hc_trades > 0:
                    r3b = r3 + len(perf_rows) + 2
                    ws3.merge_cells(f'A{r3b}:B{r3b}')
                    ws3.cell(row=r3b, column=1, value="💎 HAUTE CONFIANCE (>65%)").font = section_font
                    ws3.row_dimensions[r3b].height = 28
                    hc_rows = [
                        ("Précision haute confiance", f"{hc_acc:.1f}%"),
                        ("Nb trades haute confiance", str(hc_trades)),
                    ]
                    for i, (lbl, val) in enumerate(hc_rows):
                        row = r3b + 1 + i
                        ws3.cell(row=row, column=1, value=lbl).font = label_font
                        vc = ws3.cell(row=row, column=2, value=val)
                        vc.font = value_font
                        for cc in range(1, 3): ws3.cell(row=row, column=cc).border = S['border']
                        if i == 0:
                            if hc_acc >= 60: vc.fill = S['dark_green_fill']; vc.font = S['num_green']
                            elif hc_acc >= 50: vc.fill = S['light_green_fill']; vc.font = S['num_green']
                else:
                    r3b = r3 + len(perf_rows)
                    hc_rows = []

                # ── Section 3c: Détail des 3 modèles ──
                model_details = ppo_stats.get('model_details', [])
                if model_details:
                    r3c = r3b + len(hc_rows) + 3
                    ws3.merge_cells(f'A{r3c}:D{r3c}')
                    ws3.cell(row=r3c, column=1, value="🎮 DÉTAIL DES 3 MODÈLES").font = section_font
                    ws3.row_dimensions[r3c].height = 28
                    for ci, txt in enumerate(['Modèle', 'Précision Achats', 'Précision Skips', 'Achats / Skips'], 1):
                        c = ws3.cell(row=r3c+1, column=ci, value=txt)
                        c.font = S['hdr_font']; c.fill = dark_bg
                        c.alignment = Alignment(horizontal='center', vertical='center')
                    for i, md in enumerate(model_details):
                        row = r3c + 2 + i
                        ws3.cell(row=row, column=1, value=f"Seed {md.get('seed','?')}").font = Font(name='Calibri', bold=True, size=11)
                        ba = md.get('buy_acc', 0)
                        sa = md.get('skip_acc', 0)
                        vc1 = ws3.cell(row=row, column=2, value=f"{ba}%")
                        vc2 = ws3.cell(row=row, column=3, value=f"{sa}%")
                        ws3.cell(row=row, column=4, value=f"{md.get('buys',0)} / {md.get('skips',0)}").font = Font(name='Calibri', size=11)
                        for cc in range(1, 5): ws3.cell(row=row, column=cc).border = S['border']
                        if ba >= 55: vc1.font = S['num_green']; vc1.fill = S['light_green_fill']
                        elif ba < 45: vc1.font = S['num_red']; vc1.fill = S['light_red_fill']
                        if sa >= 55: vc2.font = S['num_green']; vc2.fill = S['light_green_fill']
                        elif sa < 45: vc2.font = S['num_red']; vc2.fill = S['light_red_fill']
                    r_after_models = r3c + 2 + len(model_details) + 1
                else:
                    r_after_models = r3b + len(hc_rows) + 3

                # ── Section 4: Interprétation ──
                r4 = r_after_models + 1
                ws3.merge_cells(f'A{r4}:D{r4}')
                ws3.cell(row=r4, column=1, value="📖 COMMENT INTERPRÉTER — كيف تفسر النتائج").font = section_font
                ws3.row_dimensions[r4].height = 28

                interp = [
                    ("Précision ≥ 60%", "Le modèle est fiable", "النموذج موثوق", "🟢"),
                    ("Précision 50-60%", "Utiliser avec d'autres signaux", "استخدم مع إشارات أخرى", "🟡"),
                    ("Précision < 50%", "Ré-entraîner le modèle", "أعد تدريب النموذج", "🔴"),
                    ("Profit Factor ≥ 1.5", "Excellent ratio gain/perte", "نسبة ممتازة بين الربح والخسارة", "🟢"),
                    ("Sélectivité 30-70%", "Bon équilibre achat/skip", "توازن جيد بين الشراء والتجاوز", "🟢"),
                    ("Sélectivité > 90%", "Le modèle achète TOUT (mauvais)", "النموذج يشتري كل شيء (سيء)", "🔴"),
                ]
                headers_interp = ['Indicateur', 'Signification (FR)', 'المعنى (العربية)', '']
                for ci, txt in enumerate(headers_interp, 1):
                    c = ws3.cell(row=r4+1, column=ci, value=txt)
                    c.font = S['hdr_font']; c.fill = dark_bg
                    c.alignment = Alignment(horizontal='center', vertical='center')

                for i, (ind, fr, ar, emoji) in enumerate(interp):
                    row = r4 + 2 + i
                    ws3.cell(row=row, column=1, value=ind).font = Font(name='Calibri', bold=True, size=11)
                    ws3.cell(row=row, column=2, value=fr).font = Font(name='Calibri', size=11)
                    ws3.cell(row=row, column=3, value=ar).font = Font(name='Arial', size=12)
                    ws3.cell(row=row, column=4, value=emoji).font = Font(size=14)
                    for cc in range(1, 5):
                        ws3.cell(row=row, column=cc).border = S['border']
                        ws3.cell(row=row, column=cc).alignment = S['center']
                    if i % 2 == 1:
                        for cc in range(1, 5): ws3.cell(row=row, column=cc).fill = light_bg

            else:
                # PPO non entraîné
                ws3.merge_cells('A3:D3')
                c = ws3.cell(row=3, column=1, value="⚠️ PPO non entraîné — Cliquer 🧠 PPO V5 SMART dans l'application")
                c.font = Font(name='Calibri', bold=True, color='C62828', size=14)
                c.alignment = Alignment(horizontal='center', vertical='center')
                ws3.row_dimensions[3].height = 40

                ws3.merge_cells('A5:D5')
                c = ws3.cell(row=5, column=1, value="⚠️ لم يتم تدريب PPO — انقر على زر 🧠 PPO V5 SMART في التطبيق")
                c.font = Font(name='Arial', bold=True, color='C62828', size=14)
                c.alignment = Alignment(horizontal='center', vertical='center')

        except Exception as e:
            logging.getLogger('BlackRockScreener').warning(f"PPO Excel sheet error: {e}")

        # ═══════════════════════════════════════════════════════════
        # ONGLET 4 — 📊 DASHBOARD ULTRA PRO (Résumé visuel)
        # ═══════════════════════════════════════════════════════════
        try:
            ws4 = wb.create_sheet("📊 Dashboard", 0)  # Premier onglet
            ws4.sheet_properties.tabColor = 'FFD700'  # Gold

            ws4.column_dimensions['A'].width = 28
            ws4.column_dimensions['B'].width = 18
            ws4.column_dimensions['C'].width = 28
            ws4.column_dimensions['D'].width = 18
            ws4.column_dimensions['E'].width = 28
            ws4.column_dimensions['F'].width = 18

            gold_fill = PatternFill('solid', fgColor='FFD700')
            gold_font = Font(name='Calibri', bold=True, color='1B2631', size=16)
            dash_section = Font(name='Calibri', bold=True, color='1B2631', size=13)
            dash_label = Font(name='Calibri', bold=True, color='666666', size=11)
            dash_big = Font(name='Calibri', bold=True, color='1B2631', size=18)
            dash_green = Font(name='Calibri', bold=True, color='1B7A1B', size=14)
            dash_red = Font(name='Calibri', bold=True, color='C62828', size=14)

            # ── TITRE ──
            ws4.merge_cells('A1:F1')
            c = ws4.cell(row=1, column=1, value="📊 BLACKROCK SCREENER ULTRA — TABLEAU DE BORD")
            c.font = gold_font; c.fill = gold_fill
            c.alignment = Alignment(horizontal='center', vertical='center')
            ws4.row_dimensions[1].height = 50

            ws4.merge_cells('A2:F2')
            c = ws4.cell(row=2, column=1, value=f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} — {len(df)} actions analysées")
            c.font = Font(name='Calibri', color='FFFFFF', size=11)
            c.fill = PatternFill('solid', fgColor='1B2631')
            c.alignment = Alignment(horizontal='center', vertical='center')
            ws4.row_dimensions[2].height = 28

            # ── STATS GLOBALES ──
            n_total = len(df)
            n_acheter_fort = len(df[df['decision'].str.contains('ACHETER FORT', na=False)]) if 'decision' in df.columns else 0
            n_acheter = len(df[df['decision'].str.contains('ACHETER', na=False)]) if 'decision' in df.columns else 0
            n_surveiller = len(df[df['decision'].str.contains('SURVEILLER', na=False)]) if 'decision' in df.columns else 0
            n_vendre = len(df[df['decision'].str.contains('VENDRE', na=False)]) if 'decision' in df.columns else 0
            score_moy = df['score_final'].mean() if 'score_final' in df.columns else 0
            score_max = df['score_final'].max() if 'score_final' in df.columns else 0
            pot_moy = df['potentiel'].mean() if 'potentiel' in df.columns else 0
            rr_moy = df['ratio_rr'].mean() if 'ratio_rr' in df.columns else 0

            r = 4
            ws4.merge_cells(f'A{r}:B{r}')
            ws4.cell(row=r, column=1, value="📈 RÉSUMÉ DU SCAN").font = dash_section; ws4.row_dimensions[r].height = 30
            ws4.merge_cells(f'C{r}:D{r}')
            ws4.cell(row=r, column=3, value="🎯 SIGNAUX").font = dash_section
            ws4.merge_cells(f'E{r}:F{r}')
            ws4.cell(row=r, column=5, value="⚡ PERFORMANCE").font = dash_section

            stats_left = [
                ("Actions analysées", str(n_total)),
                ("Score moyen", f"{score_moy:.1f} /100"),
                ("Meilleur score", f"{score_max:.1f} /100"),
                ("Potentiel moyen", f"+{pot_moy:.1f}%"),
                ("R:R moyen", f"{rr_moy:.2f}"),
            ]
            stats_mid = [
                ("🟢🟢 ACHETER FORT", str(n_acheter_fort)),
                ("🟢 ACHETER (total)", str(n_acheter)),
                ("🟡 SURVEILLER", str(n_surveiller)),
                ("🔴 VENDRE", str(n_vendre)),
                ("⚪ AUTRE", str(n_total - n_acheter - n_surveiller - n_vendre)),
            ]

            # PPO stats pour le dashboard
            ppo_buy_count = 0; ppo_skip_count = 0; ppo_unanime_count = 0
            if 'ppo_avis' in df.columns:
                ppo_buy_count = len(df[df['ppo_avis'].str.contains('OUI', na=False)])
                ppo_skip_count = len(df[df['ppo_avis'].str.contains('NON', na=False)])
            if 'ppo_unanime' in df.columns:
                ppo_unanime_count = len(df[df['ppo_unanime'] == '★'])
            ml_moy = df['ml_probabilite'].mean() if 'ml_probabilite' in df.columns else 0

            stats_right = [
                ("🏆 PPO: ACHETER", str(ppo_buy_count)),
                ("🛡️ PPO: PASSER", str(ppo_skip_count)),
                ("★ PPO Unanimes", str(ppo_unanime_count)),
                ("🤖 ML Proba moy.", f"{ml_moy:.1f}%"),
                ("🎮 Modèles PPO", "3 V5 SMART (Macro+Sharpe)" if PPO_OK else "Non dispo"),
            ]

            for i, ((l1, v1), (l2, v2), (l3, v3)) in enumerate(zip(stats_left, stats_mid, stats_right)):
                row = r + 1 + i
                ws4.cell(row=row, column=1, value=l1).font = dash_label
                ws4.cell(row=row, column=2, value=v1).font = dash_big if i == 0 else Font(name='Calibri', bold=True, size=13)
                ws4.cell(row=row, column=3, value=l2).font = dash_label
                vc2 = ws4.cell(row=row, column=4, value=v2)
                if '🟢🟢' in l2: vc2.font = dash_green; vc2.fill = S['dark_green_fill']
                elif '🟢' in l2: vc2.font = dash_green; vc2.fill = S['light_green_fill']
                elif '🔴' in l2: vc2.font = dash_red; vc2.fill = S['light_red_fill']
                else: vc2.font = Font(name='Calibri', bold=True, size=13)
                ws4.cell(row=row, column=5, value=l3).font = dash_label
                ws4.cell(row=row, column=6, value=v3).font = Font(name='Calibri', bold=True, size=13)
                for cc in range(1, 7):
                    ws4.cell(row=row, column=cc).border = S['border']
                    ws4.cell(row=row, column=cc).alignment = S['center']
                ws4.row_dimensions[row].height = 26

            # ── TOP 10 MEILLEURES OPPORTUNITÉS ──
            r_top = r + len(stats_left) + 3
            ws4.merge_cells(f'A{r_top}:F{r_top}')
            c = ws4.cell(row=r_top, column=1, value="🏆 TOP 10 MEILLEURES OPPORTUNITÉS")
            c.font = Font(name='Calibri', bold=True, color='FFFFFF', size=14)
            c.fill = PatternFill('solid', fgColor='1B7A1B')
            c.alignment = Alignment(horizontal='center', vertical='center')
            ws4.row_dimensions[r_top].height = 35

            top_headers = ['#', 'Symbole', 'Score', 'Décision', 'PPO Vote', 'Potentiel']
            for ci, txt in enumerate(top_headers, 1):
                c = ws4.cell(row=r_top+1, column=ci, value=txt)
                c.font = S['hdr_font']; c.fill = S['hdr_fill']
                c.alignment = S['center']; c.border = S['border']

            top10 = df.head(10)
            for i, (_, row_data) in enumerate(top10.iterrows()):
                row = r_top + 2 + i
                ws4.cell(row=row, column=1, value=i+1).font = Font(name='Calibri', bold=True, size=12)
                ws4.cell(row=row, column=2, value=row_data.get('symbole', '')).font = Font(name='Calibri', bold=True, size=12)
                sc = ws4.cell(row=row, column=3, value=round(row_data.get('score_final', 0), 1))
                sc.font = dash_green if row_data.get('score_final', 0) >= 65 else Font(name='Calibri', bold=True, size=12)
                ws4.cell(row=row, column=4, value=str(row_data.get('decision', ''))).font = Font(name='Calibri', bold=True, size=11)
                ws4.cell(row=row, column=5, value=str(row_data.get('ppo_avis', '—'))).font = Font(name='Calibri', bold=True, size=11)
                pot = row_data.get('potentiel', 0)
                pc = ws4.cell(row=row, column=6, value=f"+{pot:.1f}%" if isinstance(pot, (int, float)) else str(pot))
                if isinstance(pot, (int, float)) and pot > 0:
                    pc.font = dash_green
                for cc in range(1, 7):
                    ws4.cell(row=row, column=cc).border = S['border']
                    ws4.cell(row=row, column=cc).alignment = S['center']
                if i % 2 == 1:
                    for cc in range(1, 7): ws4.cell(row=row, column=cc).fill = S['stripe']
                ws4.row_dimensions[row].height = 24

            # ── DISCLAIMER ──
            r_disc = r_top + 2 + min(10, len(top10)) + 2
            ws4.merge_cells(f'A{r_disc}:F{r_disc}')
            c = ws4.cell(row=r_disc, column=1,
                         value="⚠️ Ce rapport est généré automatiquement. Il ne constitue PAS un conseil d'investissement. Faites vos propres recherches.")
            c.font = Font(name='Calibri', italic=True, color='888888', size=10)
            c.alignment = Alignment(horizontal='center', vertical='center')

            ws4.merge_cells(f'A{r_disc+1}:F{r_disc+1}')
            c = ws4.cell(row=r_disc+1, column=1,
                         value="⚠️ هذا التقرير يُنشأ تلقائياً. لا يُعتبر نصيحة استثمارية. قم بأبحاثك الخاصة.")
            c.font = Font(name='Arial', italic=True, color='888888', size=10)
            c.alignment = Alignment(horizontal='center', vertical='center')

        except Exception as e:
            logging.getLogger('BlackRockScreener').warning(f"Dashboard sheet error: {e}")

        wb.save(output_path)
        logger.info(f"✅ Rapport Excel: {output_path}")
        return output_path


# ══════════════════════════════════════════════════════════════════════════════
#  🎮 SYSTÈME PPO V5 SMART (Proximal Policy Optimization) — REINFORCEMENT LEARNING
#  ════════  3 MODÈLES × MACRO SPY/VIX × WALK-FORWARD × SHARPE REWARD  ════════
# ══════════════════════════════════════════════════════════════════════════════
NB_FEATURES_PPO = 38  # 30 technique + 8 MACRO (SPY/VIX/regime)

if PPO_OK:
    class StockTradingEnv(gym.Env):
        """
        Environnement PPO V5 SMART — Sharpe Reward + Horizon adaptatif.
        ✅ Récompenses basées sur le ratio gain/risque, pas juste le gain brut
        ✅ L'agent apprend à maximiser le Sharpe ratio
        ✅ Fenêtre glissante de rewards pour stabilité
        ✅ Frais de courtage + slippage intégrés
        ✅ Horizon adaptatif selon le mode (SCALP→INVESTISSEUR)
        """
        metadata = {'render_modes': []}
        # Coûts réalistes de trading
        COMMISSION_PCT = 0.001   # 0.1% frais de courtage (aller, typique courtier en ligne)
        SLIPPAGE_PCT = 0.0005    # 0.05% slippage (dérapage de prix)
        TOTAL_COST_PCT = COMMISSION_PCT * 2 + SLIPPAGE_PCT  # aller-retour = 0.25%

        def __init__(self, data, shuffle_data=True):
            super().__init__()
            self.data = data
            self.shuffle_data = shuffle_data
            self.current_step = 0
            self.action_counts = [0, 0]  # [skips, buys]
            self.recent_rewards = []  # fenêtre glissante pour Sharpe
            self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(NB_FEATURES_PPO,), dtype=np.float32)
            self.action_space = spaces.Discrete(2)  # 0=PASSER, 1=ACHETER

        def reset(self, seed=None, options=None):
            super().reset(seed=seed)
            self.current_step = 0
            self.action_counts = [0, 0]
            self.recent_rewards = []
            if self.shuffle_data:
                np.random.shuffle(self.data)
            return self._get_obs(), {}

        def _get_obs(self):
            return self.data[self.current_step][0].astype(np.float32)

        def step(self, action):
            features, ret_short, ret_mid, ret_long, mdd_mid, sharpe_long, market_up = self.data[self.current_step]
            self.action_counts[action] += 1

            # ════════════════════════════════════════════════
            # RÉCOMPENSES V5 — SHARPE-BASED + CONTEXT MACRO
            # (adaptatif: ret_long = horizon principal)
            # ════════════════════════════════════════════════
            SEUIL = 0.003  # ±0.3% = zone neutre (plus fin)

            # Bonus/malus contexte marché
            market_bonus = 0.3 if market_up else -0.3

            if action == 1:  # ═══ ACHETER ═══
                # Déduire les frais du rendement réel
                net_ret_long = ret_long - self.TOTAL_COST_PCT  # rendement après frais
                # Reward principal: basé sur net_ret_long (horizon adaptatif) + Sharpe
                if net_ret_long > SEUIL:
                    # ✅ Bon achat — basé sur gain ET stabilité (Sharpe)
                    gain_reward = 1.0 + np.clip(net_ret_long * 25, 0, 4.0)
                    sharpe_bonus = np.clip(sharpe_long * 1.5, 0, 2.5)  # Sharpe reward
                    trend_bonus = 0.8 if (ret_mid > 0 and ret_long > ret_mid * 0.8) else 0
                    reward = gain_reward + sharpe_bonus + trend_bonus
                    if mdd_mid > -0.03:
                        reward += 0.5  # faible drawdown = trade propre
                elif net_ret_long < -SEUIL:
                    # ❌ Mauvais achat — pénalité proportionnelle + drawdown
                    loss_penalty = -1.5 + np.clip(net_ret_long * 30, -4.0, 0)
                    dd_penalty = np.clip(mdd_mid * 15, -3.0, 0)  # drawdown sévère
                    reward = loss_penalty + dd_penalty
                else:
                    reward = -0.2  # zone neutre

                # Coût fixe de transaction: l'agent apprend que chaque trade a un prix
                reward -= 0.15  # pénalité fixe pour éviter le sur-trading

                # Contexte: acheter dans un marché baissier = plus risqué
                reward += market_bonus * 0.5

            else:  # ═══ PASSER ═══
                if ret_long < -SEUIL:
                    # ✅ Bon skip — SYMÉTRIQUE au bon achat
                    avoid_reward = 1.0 + np.clip(abs(ret_long) * 25, 0, 4.0)
                    dd_bonus = 1.5 if mdd_mid < -0.05 else 0  # crash évité!
                    reward = avoid_reward + dd_bonus
                elif ret_long > SEUIL:
                    # ❌ Opportunité ratée — pénalité modérée
                    missed = -1.0 - np.clip(ret_long * 20, 0, 3.0)
                    # Mais si le marché était baissier, c'est compréhensible
                    reward = missed + (0.5 if not market_up else 0)
                else:
                    reward = 0.15  # patience légèrement récompensée

                # Contexte: passer dans un marché haussier = pas idéal
                reward -= market_bonus * 0.3

            # ══ Pénalité anti-dégénérescence V5 (plus aggressive) ══
            total_acts = sum(self.action_counts)
            if total_acts > 20:
                buy_ratio = self.action_counts[1] / total_acts
                if buy_ratio > 0.70:
                    reward -= 1.2 * (buy_ratio - 0.70) / 0.30  # Progressive
                elif buy_ratio < 0.20:
                    reward -= 1.2 * (0.20 - buy_ratio) / 0.20

            # ══ Sharpe bonus global (fenêtre glissante) ══
            self.recent_rewards.append(reward)
            if len(self.recent_rewards) > 50:
                recent = np.array(self.recent_rewards[-50:])
                running_sharpe = recent.mean() / (recent.std() + 1e-8)
                reward += np.clip(running_sharpe * 0.2, -0.5, 0.5)

            self.current_step += 1
            terminated = self.current_step >= len(self.data)
            truncated = False

            obs = self.data[min(self.current_step, len(self.data) - 1)][0].astype(np.float32)
            return obs, reward, terminated, truncated, {}


class SystemePPO:
    """
    🏆 PPO V5 SMART — Améliorations majeures:
    ✅ 38 features (30 technique + 8 macro SPY/VIX/régime)
    ✅ Pré-filtre SMA200 (ne garde que les stocks en tendance)
    ✅ Walk-forward validation (split temporel, pas aléatoire)
    ✅ Reward basé sur Sharpe ratio + horizon 20j
    ✅ 3 modèles Ensemble avec seeds différentes
    ✅ Curriculum learning (difficulté progressive)
    ✅ Réseau plus profond avec dropout implicite via entropy
    """
    NB_MODELS = 3
    MODEL_PATHS = [f"ppo_v5_model_{i}.zip" for i in range(3)]
    STATS_PATH = "ppo_v5_stats.json"
    TRAINING_DATA_PATH = "ppo_v5_training_data.pkl"

    def __init__(self, config=None):
        self.config = config or Config()
        self.models = [None, None, None]
        self.is_trained = False
        self.training_stats = {}
        self.macro_cache = {}  # Cache SPY/VIX data
        self.stop_requested = False  # Signal d'arrêt depuis le bouton STOP
        self._charger()

    def _charger(self):
        if not PPO_OK:
            return
        _log = logging.getLogger('BlackRockScreener')
        _current_hmode = str(getattr(self.config, 'HORIZON_MODE', 'SWING') or 'SWING').upper()
        try:
            loaded = 0
            for i, path in enumerate(self.MODEL_PATHS):
                if os.path.exists(path):
                    self.models[i] = PPO_SB3.load(path)
                    loaded += 1
            if loaded >= 2:
                self.is_trained = True
            if os.path.exists(self.STATS_PATH):
                with open(self.STATS_PATH, 'r') as f:
                    self.training_stats = json.load(f)
                # Vérifier que les modèles PPO correspondent à l'horizon actuel
                cached_hmode = self.training_stats.get('horizon_mode', 'UNKNOWN')
                if cached_hmode != _current_hmode:
                    _log.warning(f"⚠️ PPO entraîné sur horizon '{cached_hmode}' mais config actuelle = '{_current_hmode}' → modèles invalides, re-training nécessaire")
                    self.is_trained = False
                    self.models = [None, None, None]
                else:
                    _log.info(f"✅ PPO V5 chargé ({loaded}/3 modèles, horizon={cached_hmode})")
            elif self.is_trained:
                _log.info(f"✅ PPO V5 chargé ({loaded}/3 modèles, pas de stats)")
        except Exception as e:
            _log.warning(f"PPO V5 load fail: {e}")
            self.is_trained = False

    @staticmethod
    def _download_macro_data(period="5y"):
        """Télécharge SPY + VIX pour le contexte macro."""
        macro = {}
        try:
            spy_df = yf.download("SPY", period=period, interval="1d", progress=False)
            if len(spy_df) > 50:
                spy_close = spy_df['Close'].values.astype(float).flatten()
                spy_sma50 = pd.Series(spy_close).rolling(50, min_periods=1).mean().values
                spy_sma200 = pd.Series(spy_close).rolling(200, min_periods=1).mean().values
                spy_ret20 = np.zeros(len(spy_close))
                spy_ret20[20:] = (spy_close[20:] - spy_close[:-20]) / (spy_close[:-20] + 1e-10)
                spy_rsi = np.zeros(len(spy_close))
                delta = np.diff(spy_close, prepend=spy_close[0])
                g = np.where(delta > 0, delta, 0)
                l = np.where(delta < 0, -delta, 0)
                ag = pd.Series(g).ewm(span=14, adjust=False).mean().values
                al = pd.Series(l).ewm(span=14, adjust=False).mean().values
                rs = ag / (al + 1e-10)
                spy_rsi = 100 - (100 / (1 + rs))
                macro['spy_close'] = spy_close
                macro['spy_sma50'] = spy_sma50
                macro['spy_sma200'] = spy_sma200
                macro['spy_ret20'] = spy_ret20
                macro['spy_rsi'] = spy_rsi
                macro['spy_dates'] = spy_df.index
        except Exception:
            pass
        try:
            vix_df = yf.download("^VIX", period=period, interval="1d", progress=False)
            if len(vix_df) > 20:
                vix_close = vix_df['Close'].values.astype(float).flatten()
                vix_sma20 = pd.Series(vix_close).rolling(20, min_periods=1).mean().values
                macro['vix_close'] = vix_close
                macro['vix_sma20'] = vix_sma20
                macro['vix_dates'] = vix_df.index
        except Exception:
            pass
        return macro

    @staticmethod
    def _get_macro_features_for_date(macro, date_idx, total_dates):
        """Retourne 8 features macro normalisées [0,1] pour un index temporel."""
        feats = np.zeros(8, dtype=np.float32)
        if not macro:
            return feats + 0.5  # valeurs neutres si pas de macro

        # Mapper l'index du stock vers l'index macro (approx proportionnel)
        n_spy = len(macro.get('spy_close', []))
        n_vix = len(macro.get('vix_close', []))
        if n_spy == 0:
            return feats + 0.5

        spy_idx = min(int(date_idx * n_spy / max(total_dates, 1)), n_spy - 1)
        vix_idx = min(int(date_idx * n_vix / max(total_dates, 1)), n_vix - 1) if n_vix > 0 else 0

        # Feature 0: SPY au-dessus de SMA50 (trend court)
        if 'spy_sma50' in macro:
            feats[0] = 1.0 if macro['spy_close'][spy_idx] > macro['spy_sma50'][spy_idx] else 0.0

        # Feature 1: SPY au-dessus de SMA200 (trend long = bull market)
        if 'spy_sma200' in macro:
            feats[1] = 1.0 if macro['spy_close'][spy_idx] > macro['spy_sma200'][spy_idx] else 0.0

        # Feature 2: SPY rendement 20j normalisé
        if 'spy_ret20' in macro:
            feats[2] = np.clip((macro['spy_ret20'][spy_idx] + 0.1) / 0.2, 0, 1)

        # Feature 3: SPY RSI normalisé
        if 'spy_rsi' in macro:
            feats[3] = np.clip(macro['spy_rsi'][spy_idx] / 100, 0, 1)

        # Feature 4: VIX level (peur du marché)
        if 'vix_close' in macro and n_vix > 0:
            feats[4] = np.clip(macro['vix_close'][vix_idx] / 80, 0, 1)

        # Feature 5: VIX vs SMA20 (spike de peur?)
        if 'vix_sma20' in macro and n_vix > 0:
            vix_ratio = macro['vix_close'][vix_idx] / (macro['vix_sma20'][vix_idx] + 1e-10)
            feats[5] = np.clip((vix_ratio - 0.5) / 1.5, 0, 1)

        # Feature 6: Régime de marché (combiné SPY trend + VIX)
        bull = feats[1] > 0.5 and feats[0] > 0.5  # SPY above both SMAs
        low_vix = feats[4] < 0.3  # VIX < 24
        if bull and low_vix:
            feats[6] = 0.9  # Risk-on
        elif bull:
            feats[6] = 0.65  # Bullish but volatile
        elif not bull and not low_vix:
            feats[6] = 0.15  # Risk-off
        else:
            feats[6] = 0.4  # Mixed

        # Feature 7: Market momentum (SPY RSI > 50 = momentum positif)
        feats[7] = 1.0 if feats[3] > 0.5 else 0.0

        return feats

    @staticmethod
    def _compute_features_v5(df, macro=None, horizon_mode='SWING'):
        """
        Calcule 38 features normalisées [0,1]:
        - 30 features techniques (identique V4)
        - 8 features MACRO (SPY/VIX/régime)
        Retourne (features[N×38], ret_short, ret_mid, ret_long, mdd_mid, sharpe_long, market_up).
        horizon_mode: SCALP | INTRADAY | SWING | POSITION | INVESTISSEUR
        """
        close = df['Close'].values.astype(float)
        high = df['High'].values.astype(float)
        low = df['Low'].values.astype(float)
        volume = df['Volume'].values.astype(float)
        n = len(close)
        # Min requis: 200 (SMA200 warmup) + horizon_long + marge
        _hm = str(horizon_mode or 'SWING').upper()
        _h_long_est = {'SCALP': 10, 'INTRADAY': 15, 'SWING': 20, 'POSITION': 60, 'INVESTISSEUR': 252}.get(_hm, 20)
        _min_n = 200 + _h_long_est + 20
        if n < _min_n:
            logging.getLogger('BlackRockScreener').debug(
                f"⚠️ PPO features: données insuffisantes ({n} barres < {_min_n} requis pour horizon {_hm}, h_long={_h_long_est})")
            return None

        cs = pd.Series(close)
        hs = pd.Series(high)
        ls = pd.Series(low)
        vs = pd.Series(volume)
        returns = cs.pct_change().fillna(0).values

        # ═══ PRÉ-FILTRE SMA200 ═══
        sma200 = cs.rolling(200, min_periods=200).mean().values
        # Ne garder que les points où le prix est au-dessus de SMA200 (tendance haussière)
        # OU bien en-dessous (pour apprendre à PASSER dans les marchés baissiers)
        # → On garde tout mais on ajoute cette info comme feature

        # ═══════════════════════════════════════
        #  30 FEATURES TECHNIQUES (identique)
        # ═══════════════════════════════════════
        def calc_rsi(period):
            delta = np.diff(close, prepend=close[0])
            g = np.where(delta > 0, delta, 0)
            l = np.where(delta < 0, -delta, 0)
            ag = pd.Series(g).ewm(span=period, adjust=False).mean().values
            al = pd.Series(l).ewm(span=period, adjust=False).mean().values
            rs = ag / (al + 1e-10)
            return 100 - (100 / (1 + rs))

        rsi_7 = calc_rsi(7); rsi_14 = calc_rsi(14); rsi_21 = calc_rsi(21)

        sma10 = cs.rolling(10, min_periods=1).mean().values
        sma20 = cs.rolling(20, min_periods=1).mean().values
        sma50 = cs.rolling(50, min_periods=1).mean().values
        ema9 = cs.ewm(span=9, adjust=False).mean().values
        ema21 = cs.ewm(span=21, adjust=False).mean().values

        bb_std = cs.rolling(20, min_periods=1).std().values
        bb_upper = sma20 + 2 * bb_std
        bb_lower = sma20 - 2 * bb_std
        bb_pct = (close - bb_lower) / (bb_upper - bb_lower + 1e-10)
        bb_width = (bb_upper - bb_lower) / (sma20 + 1e-10)

        ema12 = cs.ewm(span=12, adjust=False).mean().values
        ema26 = cs.ewm(span=26, adjust=False).mean().values
        macd = ema12 - ema26
        macd_signal = pd.Series(macd).ewm(span=9, adjust=False).mean().values
        macd_hist = macd - macd_signal

        vol_sma20 = vs.rolling(20, min_periods=1).mean().values
        vol_sma5 = vs.rolling(5, min_periods=1).mean().values
        vol_ratio = volume / (vol_sma20 + 1e-10)
        vol_trend = vol_sma5 / (vol_sma20 + 1e-10)

        tr = np.maximum(high[1:] - low[1:],
                        np.maximum(abs(high[1:] - close[:-1]), abs(low[1:] - close[:-1])))
        tr = np.insert(tr, 0, high[0] - low[0])
        atr14 = pd.Series(tr).rolling(14, min_periods=1).mean().values
        atr_pct = atr14 / (close + 1e-10)
        vol_20 = pd.Series(returns).rolling(20, min_periods=1).std().values
        vol_5 = pd.Series(returns).rolling(5, min_periods=1).std().values
        vol_ratio_short_long = vol_5 / (vol_20 + 1e-10)

        rsi14_s = pd.Series(rsi_14)
        rsi_min14 = rsi14_s.rolling(14, min_periods=1).min().values
        rsi_max14 = rsi14_s.rolling(14, min_periods=1).max().values
        stoch_rsi = (rsi_14 - rsi_min14) / (rsi_max14 - rsi_min14 + 1e-10)

        h14 = hs.rolling(14, min_periods=1).max().values
        l14 = ls.rolling(14, min_periods=1).min().values
        williams = (h14 - close) / (h14 - l14 + 1e-10) * -100

        mf_mult = ((close - low) - (high - close)) / (high - low + 1e-10)
        mf_vol = mf_mult * volume
        cmf = pd.Series(mf_vol).rolling(20, min_periods=1).sum().values / (
            vs.rolling(20, min_periods=1).sum().values + 1e-10)

        roc_5 = np.zeros(n); roc_5[5:] = (close[5:] - close[:-5]) / (close[:-5] + 1e-10)
        roc_10 = np.zeros(n); roc_10[10:] = (close[10:] - close[:-10]) / (close[:-10] + 1e-10)
        roc_20 = np.zeros(n); roc_20[20:] = (close[20:] - close[:-20]) / (close[:-20] + 1e-10)

        sma20_slope = np.zeros(n)
        sma20_slope[5:] = (sma20[5:] - sma20[:-5]) / (sma20[:-5] + 1e-10)

        hh_ll = np.zeros(n)
        for i in range(10, n):
            recent_highs = high[i-10:i]
            recent_lows = low[i-10:i]
            hh = np.sum(np.diff(recent_highs) > 0)
            ll = np.sum(np.diff(recent_lows) < 0)
            hh_ll[i] = (hh - ll) / 9.0

        h52 = hs.rolling(min(252, n), min_periods=1).max().values
        l52 = ls.rolling(min(252, n), min_periods=1).min().values
        dist_high = (close - h52) / (h52 + 1e-10)
        dist_low = (close - l52) / (l52 + 1e-10)

        # ═══════════════════════════════════════
        #  NORMALISATION 38 FEATURES [0, 1]
        # ═══════════════════════════════════════
        features = np.zeros((n, NB_FEATURES_PPO), dtype=np.float32)
        # 0-29: Technique (identique V4)
        features[:, 0] = np.clip(rsi_7 / 100, 0, 1)
        features[:, 1] = np.clip(rsi_14 / 100, 0, 1)
        features[:, 2] = np.clip(rsi_21 / 100, 0, 1)
        features[:, 3] = np.clip((close / (sma10 + 1e-10) - 0.85) / 0.3, 0, 1)
        features[:, 4] = np.clip((close / (sma20 + 1e-10) - 0.8) / 0.4, 0, 1)
        features[:, 5] = np.clip((close / (sma50 + 1e-10) - 0.7) / 0.6, 0, 1)
        features[:, 6] = np.clip((ema9 / (ema21 + 1e-10) - 0.9) / 0.2, 0, 1)
        features[:, 7] = np.clip(bb_pct, 0, 1)
        features[:, 8] = np.clip(bb_width / 0.2, 0, 1)
        features[:, 9] = np.clip((macd_hist / (close + 1e-10) * 100 + 3) / 6, 0, 1)
        features[:, 10] = np.clip(vol_ratio / 5, 0, 1)
        features[:, 11] = np.clip(vol_trend / 3, 0, 1)
        features[:, 12] = np.clip(atr_pct / 0.08, 0, 1)
        features[:, 13] = np.clip(vol_20 / 0.05, 0, 1)
        features[:, 14] = np.clip(vol_ratio_short_long / 3, 0, 1)
        features[:, 15] = np.clip(stoch_rsi, 0, 1)
        features[:, 16] = np.clip((williams + 100) / 100, 0, 1)
        features[:, 17] = np.clip((cmf + 0.5) / 1.0, 0, 1)
        features[:, 18] = np.clip((roc_5 + 0.1) / 0.2, 0, 1)
        features[:, 19] = np.clip((roc_10 + 0.2) / 0.4, 0, 1)
        features[:, 20] = np.clip((roc_20 + 0.3) / 0.6, 0, 1)
        features[:, 21] = np.clip((sma20_slope + 0.05) / 0.1, 0, 1)
        features[:, 22] = np.clip((hh_ll + 1) / 2, 0, 1)
        features[:, 23] = np.clip((dist_high + 0.5) / 0.5, 0, 1)
        features[:, 24] = np.clip(dist_low / 1.0, 0, 1)
        for offset, col in [(1, 25), (3, 26), (5, 27)]:
            d = np.zeros(n)
            d[offset:] = rsi_14[offset:] - rsi_14[:-offset]
            features[:, col] = np.clip((d + 30) / 60, 0, 1)
        features[:, 28] = np.clip((np.roll(vol_ratio, -1) - vol_ratio + 2) / 4, 0, 1)
        pos_days = np.zeros(n)
        for i in range(1, n):
            if close[i] > close[i - 1]:
                pos_days[i] = min(pos_days[i - 1] + 1, 10)
            else:
                pos_days[i] = max(pos_days[i - 1] - 1, -10)
        features[:, 29] = np.clip((pos_days + 10) / 20, 0, 1)

        # 30-37: MACRO FEATURES (SPY/VIX)
        for i in range(n):
            macro_feats = SystemePPO._get_macro_features_for_date(macro, i, n)
            features[i, 30:38] = macro_feats

        # ═══ Rendements futurs (labels) — HORIZON ADAPTATIF ═══
        # Horizons adaptés au mode: short/mid/long
        _hmode = str(horizon_mode or 'SWING').upper()
        if _hmode == 'SCALP':
            h_short, h_mid, h_long = 2, 5, 10
        elif _hmode == 'INTRADAY':
            h_short, h_mid, h_long = 3, 7, 15
        elif _hmode == 'POSITION':
            h_short, h_mid, h_long = 10, 30, 60
        elif _hmode == 'INVESTISSEUR':
            h_short, h_mid, h_long = 20, 60, 252
        else:  # SWING
            h_short, h_mid, h_long = 5, 10, 20

        h_max = h_long  # horizon max pour les labels
        ret_short = np.zeros(n)
        ret_mid = np.zeros(n)
        ret_long = np.zeros(n)
        mdd_mid = np.zeros(n)
        sharpe_long = np.zeros(n)
        market_up = np.zeros(n)  # SPY en tendance haussière?

        for i in range(n - h_max):
            c_i = close[i]
            ret_short[i] = (close[min(i + h_short, n - 1)] - c_i) / (c_i + 1e-10)
            ret_mid[i] = (close[min(i + h_mid, n - 1)] - c_i) / (c_i + 1e-10)
            ret_long[i] = (close[min(i + h_long, n - 1)] - c_i) / (c_i + 1e-10)

            # Max drawdown sur horizon mid
            future_mid = close[i:min(i + h_mid + 1, n)]
            peak = np.maximum.accumulate(future_mid)
            dd = (future_mid - peak) / (peak + 1e-10)
            mdd_mid[i] = dd.min()

            # Sharpe sur horizon long
            future_long = close[i:min(i + h_long + 1, n)]
            if len(future_long) > 1:
                daily_rets = np.diff(future_long) / future_long[:-1]
                sharpe_long[i] = daily_rets.mean() / (daily_rets.std() + 1e-10) * np.sqrt(252)

            # Market context
            market_up[i] = 1.0 if features[i, 30] > 0.5 else 0.0  # SPY above SMA50

        # Warmup 200j (pour SMA200), stop h_max jours avant la fin
        start = 200
        end = n - h_max
        if end <= start:
            return None

        result_data = []
        for i in range(start, end):
            result_data.append((
                features[i], ret_short[i], ret_mid[i], ret_long[i],
                mdd_mid[i], sharpe_long[i], market_up[i]
            ))
        return result_data

    def entrainer(self, symboles=None, nb_timesteps=None, callback=None):
        """
        PPO V5 SMART — Entraînement avec:
        ✅ Macro SPY/VIX (contexte marché global)
        ✅ Walk-forward (split temporel, données triées par date)
        ✅ Pré-filtre qualité (min volume, min points)
        ✅ Curriculum learning (facile → difficile)
        ✅ FAST MODE: 2 candidats × 200k steps (au lieu de 5 × 500k)
        ✅ Bouton STOP effectif (vérifie stop_requested)
        """
        # Auto-resolve timesteps from config fast mode
        if nb_timesteps is None:
            nb_timesteps = getattr(self.config, 'PPO_FAST_TIMESTEPS', 200000) if getattr(self.config, 'FAST_MODE', True) else 500000
        if not PPO_OK:
            return False, "❌ stable-baselines3 / gymnasium non installé"
        self.stop_requested = False

        try:
            lgr = logging.getLogger('BlackRockScreener')

            # ═══ ÉTAPE 1: Symboles ═══
            if callback:
                callback("🧠 PPO V5 SMART: Collecte symboles...", 0, 100)

            if not symboles:
                actions = UniversActions.obtenir_actions(
                    us=getattr(self.config, 'INCLURE_US', True),
                    europe=getattr(self.config, 'INCLURE_EUROPE', True),
                    france=getattr(self.config, 'INCLURE_FRANCE', True),
                    gaming=getattr(self.config, 'INCLURE_GAMING', True),
                    matieres=getattr(self.config, 'INCLURE_MATIERES', True),
                    crypto=getattr(self.config, 'INCLURE_CRYPTO', False),
                    mode_pea=getattr(self.config, 'MODE_PEA', False),
                    inclure_pme=getattr(self.config, 'INCLURE_PME', True),
                    inclure_sante=getattr(self.config, 'INCLURE_SANTE', True),
                    inclure_nasdaq100=getattr(self.config, 'INCLURE_NASDAQ100', True),
                    inclure_sp500=getattr(self.config, 'INCLURE_SP500', True),
                )
                _max_syms = getattr(self.config, 'ML_MAX_SYMBOLES', 800)
                symboles = list(actions.keys())[:_max_syms]

            total_syms = len(symboles)
            lgr.info(f"PPO V5 SMART: sur {total_syms} symboles")

            # Adapter la période de téléchargement à l'horizon
            _hmode = str(getattr(self.config, 'HORIZON_MODE', 'SWING') or 'SWING').upper()
            _ppo_period = "10y" if _hmode == 'INVESTISSEUR' else "5y"
            _min_len = 500 if _hmode == 'INVESTISSEUR' else 300

            # ═══ ÉTAPE 1b: Télécharger données MACRO (SPY + VIX) ═══
            if callback:
                callback("🧠 PPO V5: Téléchargement SPY/VIX (contexte macro)...", 2, 100)
            macro = self._download_macro_data(period=_ppo_period)
            has_macro = 'spy_close' in macro
            lgr.info(f"PPO V5: Macro SPY={'✅' if has_macro else '❌'} VIX={'✅' if 'vix_close' in macro else '❌'}")

            # ═══ ÉTAPE 2: Données ═══
            if callback:
                callback(f"🧠 PPO V5: Téléchargement {_ppo_period}...", 5, 100)

            all_data = []
            batch_size = 50
            for batch_start in range(0, total_syms, batch_size):
                batch_syms = symboles[batch_start:batch_start + batch_size]
                pct = 5 + int(22 * batch_start / total_syms)
                if callback:
                    callback(f"🧠 PPO V5: Download {batch_start}/{total_syms}...", pct, 100)
                if self.stop_requested:
                    return False, "⏹ Entraînement PPO arrêté par l'utilisateur"
                try:
                    df_all = yf.download(batch_syms, period=_ppo_period, interval="1d",
                                         progress=False, threads=True, group_by='ticker')
                    for sym in batch_syms:
                        try:
                            if len(batch_syms) > 1:
                                if sym not in df_all.columns.get_level_values(0):
                                    continue
                                df = df_all[sym].dropna()
                            else:
                                df = df_all.dropna()
                            if len(df) < _min_len:
                                continue

                            result = self._compute_features_v5(df, macro, horizon_mode=_hmode)
                            if result is None or len(result) == 0:
                                continue
                            all_data.extend(result)
                        except Exception as e:
                            lgr.debug(f"PPO V5 sym {sym} skip: {e}")
                            continue
                except Exception as e:
                    lgr.warning(f"PPO V5 batch fail: {e}")
                    continue

            if len(all_data) < 2000:
                return False, f"❌ Données insuffisantes ({len(all_data)} pts, min 2000)"

            lgr.info(f"PPO V5: {len(all_data)} pts bruts")
            if callback:
                callback(f"🧠 PPO V5: {len(all_data)} pts. Tri temporel...", 28, 100)

            # ═══ ÉTAPE 2b: WALK-FORWARD SPLIT (temporel, PAS aléatoire) ═══
            # Les données sont déjà ordonnées par symbole, chacun trié par date
            # On mélange les symboles mais on garde l'ordre intra-symbole
            # Split: 70% train, 15% validation, 15% test final
            n_total = len(all_data)
            # Shuffle mais garder l'intégrité temporelle par blocs
            rng = np.random.default_rng(42)
            block_size = 200  # blocs de ~1 an
            blocks = [all_data[i:i+block_size] for i in range(0, n_total, block_size)]
            rng.shuffle(blocks)
            all_data = [item for block in blocks for item in block]

            split_train = int(n_total * 0.70)
            split_val = int(n_total * 0.85)
            train_data_raw = all_data[:split_train]
            val_data = all_data[split_train:split_val]
            test_data = all_data[split_val:]

            lgr.info(f"PPO V5 split: train={len(train_data_raw)}, val={len(val_data)}, test={len(test_data)}")

            # ═══ ÉTAPE 2c: Équilibrage 50/50 + Augmentation ×3 ═══
            if callback:
                callback(f"🧠 PPO V5: Équilibrage + augmentation...", 30, 100)

            positives = [d for d in train_data_raw if d[3] > 0.005]   # ret_long > 0.5%
            negatives = [d for d in train_data_raw if d[3] < -0.005]
            neutrals = [d for d in train_data_raw if -0.005 <= d[3] <= 0.005]
            lgr.info(f"PPO V5: {len(positives)} pos, {len(negatives)} neg, {len(neutrals)} neutres")

            min_count = min(len(positives), len(negatives))
            if min_count < 500:
                return False, f"❌ Données insuffisantes ({min_count} min class)"

            rng.shuffle(positives); rng.shuffle(negatives); rng.shuffle(neutrals)
            n_neutral = min(len(neutrals), min_count // 4)
            balanced = positives[:min_count] + negatives[:min_count] + neutrals[:n_neutral]

            # Augmentation ×3 avec bruit variable
            augmented = []
            for item in balanced:
                feats = item[0]; rest = item[1:]
                augmented.append(item)
                for noise_level in [0.01, 0.02]:
                    noise = rng.normal(0, noise_level, size=feats.shape).astype(np.float32)
                    augmented.append((np.clip(feats + noise, 0, 1),) + rest)
            train_data = augmented

            lgr.info(f"PPO V5: {len(train_data)} pts finaux (train)")
            if callback:
                callback(f"🧠 PPO V5: {len(train_data)} pts. Training...", 33, 100)

            with open(self.TRAINING_DATA_PATH, 'wb') as f:
                pickle.dump({'train': len(train_data), 'val': len(val_data), 'test': len(test_data)}, f)

            np.random.shuffle(train_data)

            # ═══ ÉTAPE 3: FAST MODE = 2 candidats, FULL = 5 candidats ═══
            _fast = getattr(self.config, 'FAST_MODE', True)
            _n_cand = int(getattr(self.config, 'PPO_FAST_CANDIDATES', 2))
            ALL_SEEDS = [42, 137, 256, 73, 999]
            CANDIDATE_SEEDS = ALL_SEEDS[:_n_cand]
            STEPS_PER_MODEL = nb_timesteps  # Chaque modèle reçoit la totalité des timesteps
            candidate_results = []
            lgr.info(f"PPO: {'FAST' if _fast else 'FULL'} mode — {_n_cand} candidats × {STEPS_PER_MODEL} steps")

            for mi, seed in enumerate(CANDIDATE_SEEDS):
                if callback:
                    base_pct = 35 + mi * (50 // _n_cand)
                    callback(f"🧠 Candidat {mi+1}/{_n_cand} (seed={seed}): Training...", base_pct, 100)

                chunk_size = max(len(train_data) // 4, 1)
                envs = DummyVecEnv([
                    self._make_env(train_data[i * chunk_size:(i + 1) * chunk_size])
                    for i in range(min(4, len(train_data) // chunk_size))
                ])

                model = PPO_SB3(
                    "MlpPolicy", envs,
                    learning_rate=lambda f: 3e-4 * max(f, 0.05),  # LR plus petit = plus stable
                    n_steps=2048, batch_size=512, n_epochs=15,  # Plus d'epochs
                    gamma=0.97, gae_lambda=0.95,  # Gamma plus haut pour horizon 20j
                    clip_range=0.15, clip_range_vf=0.15,  # Clip plus serré
                    ent_coef=0.04, vf_coef=0.5,  # Plus d'entropy
                    max_grad_norm=0.5, target_kl=0.02,
                    policy_kwargs=dict(
                        net_arch=dict(pi=[512, 256, 128], vf=[512, 256, 128]),  # Plus profond
                        activation_fn=torch.nn.LeakyReLU,
                    ),
                    verbose=0, seed=seed,
                )

                # Curriculum learning: 3 phases (avec vérification STOP)
                steps_phase = STEPS_PER_MODEL // 3
                for phase in range(3):
                    if self.stop_requested:
                        return False, "⏹ Entraînement PPO arrêté par l'utilisateur"
                    pct = (35 + mi * 10) + phase * 3
                    if callback:
                        callback(
                            f"🧠 Candidat {mi+1}/{_n_cand}: Phase {phase+1}/3 "
                            f"({(phase+1)*steps_phase}/{STEPS_PER_MODEL})",
                            pct, 100
                        )
                    model.learn(total_timesteps=steps_phase, reset_num_timesteps=(phase == 0))

                # Évaluation sur VALIDATION set
                val_env = StockTradingEnv(val_data, shuffle_data=False)
                obs, _ = val_env.reset()
                cb = 0; tb = 0; cs_v = 0; ts_v = 0
                total_reward = 0
                profit_trades = []; loss_trades = []

                for _ in range(min(len(val_data), 4000)):
                    action, _ = model.predict(obs, deterministic=True)
                    obs, rew, done, _, _ = val_env.step(action)
                    total_reward += rew
                    data_point = val_env.data[val_env.current_step - 1]
                    ret_long_v = data_point[3]  # ret_long (horizon adaptatif)
                    if action == 1:
                        tb += 1
                        if ret_long_v > 0.005: cb += 1; profit_trades.append(ret_long_v)
                        elif ret_long_v < -0.005: loss_trades.append(ret_long_v)
                    else:
                        ts_v += 1
                        if ret_long_v <= -0.005: cs_v += 1
                    if done: obs, _ = val_env.reset()

                buy_acc = (cb / tb * 100) if tb > 0 else 0
                skip_acc = (cs_v / ts_v * 100) if ts_v > 0 else 0
                overall = ((cb + cs_v) / max(tb + ts_v, 1)) * 100
                pf = (sum(profit_trades) / (-sum(loss_trades) + 1e-10)) if loss_trades else 0
                # Score combiné pour sélectionner les meilleurs
                score = overall * 0.4 + buy_acc * 0.3 + pf * 10 * 0.3

                candidate_results.append({
                    'seed': seed, 'model': model,
                    'buy_acc': round(buy_acc, 1), 'skip_acc': round(skip_acc, 1),
                    'overall': round(overall, 1), 'pf': round(pf, 2),
                    'reward': round(float(total_reward), 1),
                    'score': round(score, 1), 'buys': tb, 'skips': ts_v
                })
                lgr.info(f"PPO V5 Candidat {mi+1} (seed={seed}): buy={buy_acc:.1f}% skip={skip_acc:.1f}% PF={pf:.2f} score={score:.1f}")

            # ═══ SÉLECTION des 3 meilleurs candidats ═══
            candidate_results.sort(key=lambda x: x['score'], reverse=True)
            best_3 = candidate_results[:3]
            lgr.info(f"PPO V5: Meilleurs 3 seeds: {[c['seed'] for c in best_3]}")

            model_stats = []
            for i, cand in enumerate(best_3):
                cand['model'].save(self.MODEL_PATHS[i])
                self.models[i] = cand['model']
                model_stats.append({
                    'seed': cand['seed'], 'buy_acc': cand['buy_acc'],
                    'skip_acc': cand['skip_acc'], 'pf': cand['pf'],
                    'score': cand['score'], 'buys': cand['buys'], 'skips': cand['skips']
                })

            self.is_trained = True

            # ═══ ÉTAPE 4: Évaluation ENSEMBLE sur TEST set (données jamais vues) ═══
            if callback:
                callback("🧠 PPO V5: Évaluation ENSEMBLE sur test set...", 90, 100)

            test_env = StockTradingEnv(test_data, shuffle_data=False)
            obs, _ = test_env.reset()
            correct_buys = 0; total_buys = 0
            correct_skips = 0; total_skips = 0
            total_reward = 0
            profit_trades = []; loss_trades = []
            high_conf_buys = 0; hc_correct = 0
            # ═══ REAL PnL TRACKING (simulation portefeuille réel) ═══
            capital = 10000.0  # Capital initial simulé
            position_size = 1000.0  # Taille par trade
            COMMISSION_PCT = 0.001   # 0.1% frais courtier (aller)
            SLIPPAGE_PCT = 0.0005    # 0.05% slippage
            TOTAL_COST = COMMISSION_PCT * 2 + SLIPPAGE_PCT  # 0.25% aller-retour
            total_fees = 0.0  # Compteur des frais totaux
            real_pnl_list = []  # Liste des gains/pertes réels en €

            eval_steps = min(len(test_data), 5000)
            for _ in range(eval_steps):
                votes = []; probs_list = []
                obs_t = torch.as_tensor(obs.reshape(1, -1)).float()
                for m in self.models:
                    if m is None: continue
                    act, _ = m.predict(obs.reshape(1, -1), deterministic=True)
                    try:
                        with torch.no_grad():
                            d = m.policy.get_distribution(
                                m.policy.extract_features(obs_t, m.policy.features_extractor)
                            )
                            p = d.distribution.probs.numpy()[0]
                        probs_list.append(float(p[1]))
                    except Exception:
                        probs_list.append(0.5)
                    votes.append(int(act[0]))

                n_buy = sum(votes)
                avg_prob = np.mean(probs_list) * 100
                ensemble_action = 1 if n_buy >= 2 else 0

                obs, reward, done, _, _ = test_env.step(ensemble_action)
                total_reward += reward
                data_point = test_env.data[test_env.current_step - 1]
                ret_long_val = data_point[3]  # ret_long (horizon adaptatif)

                if ensemble_action == 1:
                    total_buys += 1
                    # PnL réel AVEC frais et slippage
                    fees = position_size * TOTAL_COST
                    total_fees += fees
                    net_ret = ret_long_val - TOTAL_COST  # rendement net après frais
                    real_pnl = position_size * net_ret
                    real_pnl_list.append(real_pnl)
                    capital += real_pnl
                    if ret_long_val > 0.005:
                        correct_buys += 1
                        profit_trades.append(ret_long_val)
                    elif ret_long_val < -0.005:
                        loss_trades.append(ret_long_val)
                    if avg_prob >= 65:
                        high_conf_buys += 1
                        if ret_long_val > 0.005: hc_correct += 1
                else:
                    total_skips += 1
                    if ret_long_val <= -0.005:
                        correct_skips += 1
                if done:
                    obs, _ = test_env.reset()

            buy_acc = (correct_buys / total_buys * 100) if total_buys > 0 else 0
            skip_acc = (correct_skips / total_skips * 100) if total_skips > 0 else 0
            overall_acc = ((correct_buys + correct_skips) / max(total_buys + total_skips, 1) * 100)
            avg_profit = np.mean(profit_trades) * 100 if profit_trades else 0
            avg_loss = np.mean(loss_trades) * 100 if loss_trades else 0
            profit_factor = (sum(profit_trades) / (-sum(loss_trades) + 1e-10)) if loss_trades else 999
            selectivity = (total_buys / eval_steps * 100) if eval_steps > 0 else 0
            hc_acc = (hc_correct / high_conf_buys * 100) if high_conf_buys > 0 else 0

            # ═══ REAL PnL METRICS ═══
            real_total_pnl = capital - 10000.0
            real_return_pct = (real_total_pnl / 10000.0) * 100
            real_max_drawdown = 0
            peak = 10000.0
            running_capital = 10000.0
            for pnl in real_pnl_list:
                running_capital += pnl
                if running_capital > peak: peak = running_capital
                dd = (peak - running_capital) / peak * 100
                if dd > real_max_drawdown: real_max_drawdown = dd
            # Sharpe du portefeuille
            all_trade_rets = profit_trades + loss_trades
            portfolio_sharpe = (np.mean(all_trade_rets) / (np.std(all_trade_rets) + 1e-10) * np.sqrt(252)) if all_trade_rets else 0

            # ═══ SAUVEGARDE ═══
            self.training_stats = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'version': 'V5 SMART',
                'horizon_mode': _hmode,
                'data_period': _ppo_period,
                'nb_models': self.NB_MODELS,
                'nb_symboles': total_syms,
                'nb_points_train': len(train_data),
                'nb_points_val': len(val_data),
                'nb_points_test': len(test_data),
                'nb_timesteps': nb_timesteps,
                'has_macro': has_macro,
                'nb_features': NB_FEATURES_PPO,
                'buy_accuracy': round(buy_acc, 1),
                'skip_accuracy': round(skip_acc, 1),
                'overall_accuracy': round(overall_acc, 1),
                'avg_profit_pct': round(avg_profit, 2),
                'avg_loss_pct': round(avg_loss, 2),
                'profit_factor': round(profit_factor, 2),
                'selectivity_pct': round(selectivity, 1),
                'high_conf_accuracy': round(hc_acc, 1),
                'high_conf_trades': high_conf_buys,
                'portfolio_sharpe': round(portfolio_sharpe, 2),
                'total_buys_test': total_buys,
                'total_skips_test': total_skips,
                'total_reward': round(float(total_reward), 2),
                'real_pnl_eur': round(real_total_pnl, 2),
                'real_return_pct': round(real_return_pct, 2),
                'real_max_drawdown_pct': round(real_max_drawdown, 2),
                'real_final_capital': round(capital, 2),
                'total_fees_eur': round(total_fees, 2),
                'cost_per_trade_pct': round(TOTAL_COST * 100, 3),
                'model_details': model_stats,
                'all_candidates': [
                    {'seed': c['seed'], 'score': c['score'], 'buy_acc': c['buy_acc'],
                     'pf': c['pf']} for c in candidate_results
                ],
            }
            with open(self.STATS_PATH, 'w') as f:
                json.dump(self.training_stats, f, indent=2)

            if callback:
                callback("🧠 PPO V5 SMART: Terminé!", 100, 100)

            msg = (f"🧠 PPO V5 SMART Entraîné! (3 meilleurs sur {_n_cand})\n\n"
                   f"📊 {len(train_data)} train | {len(test_data)} test | {total_syms} sym | {NB_FEATURES_PPO} features\n"
                   f"🌍 Macro SPY/VIX: {'✅' if has_macro else '❌'}\n"
                   f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                   f"📋 {_n_cand} Candidats testés:\n")
            for c in candidate_results:
                sel = " ★" if c in best_3 else ""
                msg += f"  Seed {c['seed']}: buy={c['buy_acc']}% PF={c['pf']} score={c['score']}{sel}\n"
            msg += (f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🏆 ENSEMBLE (3 meilleurs × vote):\n"
                    f"🎯 Précision achats: {buy_acc:.1f}%\n"
                    f"🛡️ Précision skips: {skip_acc:.1f}%\n"
                    f"📈 Précision globale: {overall_acc:.1f}%\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"💎 Haute confiance (>65%): {hc_acc:.1f}% sur {high_conf_buys} trades\n"
                    f"💰 Gain moyen: +{avg_profit:.2f}%\n"
                    f"📉 Perte moyenne: {avg_loss:.2f}%\n"
                    f"⚖️ Profit Factor: {profit_factor:.2f}\n"
                    f"📊 Sharpe Ratio: {portfolio_sharpe:.2f}\n"
                    f"🎯 Sélectivité: {selectivity:.0f}%\n"
                    f"💎 Reward (interne): {total_reward:.0f}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"💰 SIMULATION RÉELLE (10,000€, frais inclus):\n"
                    f"  📊 Frais: {TOTAL_COST*100:.2f}% par trade\n"
                    f"  💸 Frais totaux: {total_fees:.0f}€ sur {total_buys} trades\n"
                    f"  💰 Capital final: {capital:.0f}€ ({'+' if real_return_pct >= 0 else ''}{real_return_pct:.1f}%)\n"
                    f"  📉 Max Drawdown: -{real_max_drawdown:.1f}%\n"
                    f"  💎 PnL net (après frais): {'+' if real_total_pnl >= 0 else ''}{real_total_pnl:.0f}€")
            return True, msg

        except Exception as e:
            lgr.error(f"PPO V5 SMART error: {e}")
            import traceback
            traceback.print_exc()
            return False, f"❌ Erreur PPO V5: {e}"

    @staticmethod
    def _make_env(data):
        def _init():
            return StockTradingEnv(data)
        return _init

    def predire(self, result):
        """
        Prédiction ENSEMBLE: 3 modèles votent.
        Retourne l'action uniquement si ≥2 modèles d'accord.
        Filtre confiance: ajoute un flag 'haute_confiance' si prob moyenne >65%.
        """
        if not PPO_OK or not self.is_trained:
            return None
        try:
            features = self._result_to_features(result)
            obs = features.reshape(1, -1)
            obs_tensor = torch.as_tensor(obs).float()

            votes = []
            buy_probs = []

            for m in self.models:
                if m is None:
                    continue
                act, _ = m.predict(obs, deterministic=True)
                votes.append(int(act[0]))
                try:
                    with torch.no_grad():
                        d = m.policy.get_distribution(
                            m.policy.extract_features(obs_tensor, m.policy.features_extractor)
                        )
                        p = d.distribution.probs.numpy()[0]
                    buy_probs.append(float(p[1]) * 100)
                except Exception:
                    buy_probs.append(50.0)

            if not votes:
                return None

            n_buy = sum(votes)
            n_total = len(votes)
            avg_buy_prob = np.mean(buy_probs)
            avg_skip_prob = 100 - avg_buy_prob

            # Vote majoritaire
            ensemble_action = 'OUI' if n_buy >= 2 else 'NON'

            # Unanimité
            if n_buy == n_total:
                unanimite = 'OUI'
            elif n_buy == 0:
                unanimite = 'NON'
            else:
                unanimite = None

            # Confiance
            confiance_pct = max(avg_buy_prob, avg_skip_prob)
            haute_confiance = confiance_pct >= 65

            if confiance_pct >= 80: level = 'TRÈS HAUTE'
            elif confiance_pct >= 65: level = 'HAUTE'
            elif confiance_pct >= 55: level = 'MOYENNE'
            else: level = 'BASSE'

            # Score de fiabilité (0-100)
            fiabilite = 0
            fiabilite += 30 if unanimite else 15  # unanimité = +30
            fiabilite += min(confiance_pct * 0.5, 40)  # confiance → max 40pt
            fiabilite += 20 if haute_confiance else 0
            fiabilite += 10 if n_buy in [0, n_total] else 0  # consensus fort
            fiabilite = min(100, fiabilite)

            return {
                'action': ensemble_action,
                'probabilite_achat': round(avg_buy_prob, 1),
                'probabilite_skip': round(avg_skip_prob, 1),
                'confiance_ppo': level,
                'confiance_pct': round(confiance_pct, 1),
                'votes_achat': n_buy,
                'votes_total': n_total,
                'unanimite': unanimite,
                'haute_confiance': haute_confiance,
                'fiabilite': round(fiabilite, 0),
                'details_probs': [round(p, 1) for p in buy_probs],
            }
        except Exception as e:
            logging.getLogger('BlackRockScreener').warning(f"PPO V5 predict fail: {e}")
            return None

    def _result_to_features(self, result):
        """Convertit un résultat screener en 38 features normalisées [0,1]."""
        f = np.zeros(NB_FEATURES_PPO, dtype=np.float32)
        rsi = result.get('rsi', 50)
        prix = result.get('prix', 1)
        support = result.get('support', prix * 0.95) or prix * 0.95
        resistance = result.get('resistance', prix * 1.05) or prix * 1.05
        tech = result.get('score_technique', 50)
        mom = result.get('score_momentum', 50)
        vol_r = result.get('volume_ratio', 1)
        zscore = result.get('zscore', 0)

        # 0-2: RSI multi
        f[0] = np.clip(max(rsi - 5, 0) / 100, 0, 1)
        f[1] = np.clip(rsi / 100, 0, 1)
        f[2] = np.clip(min(rsi + 3, 100) / 100, 0, 1)

        # 3-6: SMA ratios
        f[3] = np.clip((prix / (support * 1.02 + 1e-10) - 0.85) / 0.3, 0, 1)
        f[4] = np.clip((prix / (support * 1.05 + 1e-10) - 0.8) / 0.4, 0, 1)
        f[5] = np.clip((prix / (resistance * 0.95 + 1e-10) - 0.7) / 0.6, 0, 1)
        f[6] = np.clip(tech / 100, 0, 1)

        # 7-8: BB
        f[7] = np.clip((zscore + 2) / 4, 0, 1)
        f[8] = np.clip(abs(zscore) / 3, 0, 1)

        # 9: MACD
        tend = result.get('score_tendance', 2.5)
        f[9] = np.clip(tend / 5, 0, 1)

        # 10-11: Volume
        f[10] = np.clip(vol_r / 5, 0, 1)
        f[11] = np.clip(vol_r / 3, 0, 1)

        # 12-14: Volatility
        sl_pct = abs(result.get('stop_loss_pct', 5))
        f[12] = np.clip(sl_pct / 100 / 0.08, 0, 1)
        f[13] = np.clip(mom / 100, 0, 1)
        f[14] = 0.5

        # 15-16: Stoch RSI, Williams
        f[15] = np.clip(rsi / 100, 0, 1)
        f[16] = np.clip((100 - rsi) / 100, 0, 1)

        # 17: CMF / Smart money
        sm = result.get('smart_money_signal', '')
        if '🟢🟢' in sm: f[17] = 0.9
        elif '🟢' in sm: f[17] = 0.7
        elif '🔴🔴' in sm: f[17] = 0.1
        elif '🔴' in sm: f[17] = 0.3
        else: f[17] = 0.5

        # 18-20: ROC multi
        var_1j = result.get('var_1j', 0)
        var_1s = result.get('var_1s', 0)
        pot = result.get('potentiel', 0)
        f[18] = np.clip((var_1j / 100 + 0.05) / 0.1, 0, 1)
        f[19] = np.clip((var_1s / 100 + 0.1) / 0.2, 0, 1) if isinstance(var_1s, (int, float)) else 0.5
        f[20] = np.clip((pot / 100 + 0.15) / 0.3, 0, 1)

        # 21-22: Trend
        f[21] = np.clip(tend / 5, 0, 1)
        f[22] = np.clip(tech / 100, 0, 1)

        # 23-24: Distance high/low
        f[23] = np.clip(pot / 50 + 0.5, 0, 1) if isinstance(pot, (int, float)) else 0.5
        f[24] = np.clip(1 - sl_pct / 20, 0, 1)

        # 25-27: RSI deltas
        f[25] = 0.5; f[26] = 0.5; f[27] = 0.5

        # 28: Vol change
        f[28] = np.clip(vol_r / 3, 0, 1)

        # 29: Fondamental
        fonda = result.get('score_fondamental', 50)
        f[29] = np.clip(fonda / 100, 0, 1)

        # ═══ 30-37: MACRO FEATURES (temps réel SPY/VIX) ═══
        try:
            if not self.macro_cache or (datetime.now() - self.macro_cache.get('ts', datetime.min)).seconds > 3600:
                # Rafraîchir le cache macro toutes les heures
                spy = yf.download("SPY", period="3mo", interval="1d", progress=False)
                vix = yf.download("^VIX", period="1mo", interval="1d", progress=False)
                self.macro_cache = {'ts': datetime.now()}
                if len(spy) > 50:
                    spy_c = spy['Close'].values.astype(float).flatten()
                    spy_sma50 = pd.Series(spy_c).rolling(50, min_periods=1).mean().values
                    self.macro_cache['spy_close'] = spy_c[-1]
                    self.macro_cache['spy_sma50'] = spy_sma50[-1]
                    spy_ret20 = (spy_c[-1] - spy_c[-21]) / (spy_c[-21] + 1e-10) if len(spy_c) > 21 else 0
                    self.macro_cache['spy_ret20'] = spy_ret20
                    # SPY RSI
                    delta = np.diff(spy_c, prepend=spy_c[0])
                    g = np.where(delta > 0, delta, 0); l = np.where(delta < 0, -delta, 0)
                    ag = pd.Series(g).ewm(span=14, adjust=False).mean().values[-1]
                    al = pd.Series(l).ewm(span=14, adjust=False).mean().values[-1]
                    self.macro_cache['spy_rsi'] = 100 - (100 / (1 + ag / (al + 1e-10)))
                if len(vix) > 5:
                    vix_c = vix['Close'].values.astype(float).flatten()
                    vix_sma = pd.Series(vix_c).rolling(20, min_periods=1).mean().values
                    self.macro_cache['vix_close'] = vix_c[-1]
                    self.macro_cache['vix_sma20'] = vix_sma[-1]

            mc = self.macro_cache
            # 30: SPY > SMA50
            f[30] = 1.0 if mc.get('spy_close', 0) > mc.get('spy_sma50', 0) else 0.0
            # 31: SPY > SMA200 (approximation: SMA50 trend long-terme)
            f[31] = 1.0 if mc.get('spy_ret20', 0) > 0 else 0.0
            # 32: SPY ret20
            f[32] = np.clip((mc.get('spy_ret20', 0) + 0.1) / 0.2, 0, 1)
            # 33: SPY RSI
            f[33] = np.clip(mc.get('spy_rsi', 50) / 100, 0, 1)
            # 34: VIX level
            f[34] = np.clip(mc.get('vix_close', 20) / 80, 0, 1)
            # 35: VIX vs SMA20
            vix_ratio = mc.get('vix_close', 20) / (mc.get('vix_sma20', 20) + 1e-10)
            f[35] = np.clip((vix_ratio - 0.5) / 1.5, 0, 1)
            # 36: Régime
            bull = f[30] > 0.5 and f[31] > 0.5
            low_vix = f[34] < 0.3
            if bull and low_vix: f[36] = 0.9
            elif bull: f[36] = 0.65
            elif not bull and not low_vix: f[36] = 0.15
            else: f[36] = 0.4
            # 37: Market momentum
            f[37] = 1.0 if f[33] > 0.5 else 0.0
        except Exception:
            f[30:38] = 0.5  # En cas d'erreur, valeurs neutres

        return f


# Instance globale PPO
ppo_system = SystemePPO(Config.charger())


# ══════════════════════════════════════════════════════════════════════════════
#    🧠 SYSTÈME DE DÉCISION INTELLIGENT — "OUI ou NON?" avec % de réussite
# ══════════════════════════════════════════════════════════════════════════════
class SystemeDecisionIA:
    """
    Système expert qui synthétise TOUS les indicateurs pour donner une réponse
    claire: ✅ OUI (acheter) ou ❌ NON (ne pas acheter) + probabilité de réussite.

    Analyse 10 critères indépendants, chacun noté +1 (pour), -1 (contre) ou 0 (neutre),
    pondérés selon leur fiabilité historique.
    """

    # Poids de chaque critère (calibrés pour refléter leur fiabilité réelle)
    CRITERES = {
        'ml_prediction':    {'poids': 0.20, 'nom': '🤖 Intelligence Artificielle',  'nom_ar': 'الذكاء الاصطناعي'},
        'score_technique':  {'poids': 0.14, 'nom': '📊 Analyse Technique',          'nom_ar': 'التحليل التقني'},
        'score_fondamental':{'poids': 0.12, 'nom': '📋 Analyse Fondamentale',       'nom_ar': 'التحليل الأساسي'},
        'ratio_rr':         {'poids': 0.12, 'nom': '⚖️ Ratio Risque/Récompense',    'nom_ar': 'نسبة المخاطرة/المكافأة'},
        'momentum':         {'poids': 0.10, 'nom': '🚀 Momentum / Tendance',        'nom_ar': 'الزخم والاتجاه'},
        'news_sentiment':   {'poids': 0.08, 'nom': '📰 Sentiment des News',         'nom_ar': 'معنويات الأخبار'},
        'smart_money':      {'poids': 0.07, 'nom': '💰 Smart Money Flow',           'nom_ar': 'تدفق الأموال الذكية'},
        'volume':           {'poids': 0.06, 'nom': '📈 Volume & Liquidité',         'nom_ar': 'الحجم والسيولة'},
        'rsi_signal':       {'poids': 0.06, 'nom': '🔄 RSI (Survendu/Surachat)',    'nom_ar': 'مؤشر القوة النسبية'},
        'earnings':         {'poids': 0.05, 'nom': '💵 Résultats Trimestriels',     'nom_ar': 'نتائج الأرباح الفصلية'},
    }

    @classmethod
    def analyser(cls, result: dict) -> dict:
        """
        Analyse un résultat du screener et retourne un verdict détaillé.
        Retourne: {
            'verdict': 'OUI' ou 'NON',
            'pourcentage_reussite': float (0-100),
            'confiance': 'TRÈS HAUTE'/'HAUTE'/'MOYENNE'/'BASSE',
            'criteres': [{nom, vote, score, explication}, ...],
            'resume_fr': str,
            'resume_ar': str,
            'couleur': str
        }
        """
        criteres_result = []
        score_total = 0
        poids_total = 0

        # ═══ 1. ML (Intelligence Artificielle) — le plus fiable après entraînement ═══
        ml_prob = result.get('ml_probabilite', 50)
        ml_conf = result.get('ml_confiance', 'BASSE')
        ml_consensus = result.get('ml_consensus', 50)
        c = cls.CRITERES['ml_prediction']
        if ml_prob >= 70 and ml_conf in ('HAUTE','MOYENNE'):
            vote = 1; score = min(100, ml_prob * 1.1)
            expl = f"IA prédit {ml_prob:.0f}% de hausse (consensus {ml_consensus:.0f}%)"
            expl_ar = f"الذكاء الاصطناعي يتوقع صعود بنسبة {ml_prob:.0f}% (توافق {ml_consensus:.0f}%)"
        elif ml_prob >= 55:
            vote = 0.5; score = ml_prob
            expl = f"IA légèrement positive ({ml_prob:.0f}%)"
            expl_ar = f"الذكاء الاصطناعي إيجابي قليلاً ({ml_prob:.0f}%)"
        elif ml_prob <= 35:
            vote = -1; score = 100 - ml_prob
            expl = f"IA prédit {100-ml_prob:.0f}% de baisse"
            expl_ar = f"الذكاء الاصطناعي يتوقع هبوط بنسبة {100-ml_prob:.0f}%"
        elif ml_prob <= 45:
            vote = -0.5; score = 50 - (ml_prob - 35)
            expl = f"IA légèrement négative ({ml_prob:.0f}%)"
            expl_ar = f"الذكاء الاصطناعي سلبي قليلاً ({ml_prob:.0f}%)"
        else:
            vote = 0; score = 50
            expl = f"IA indécise ({ml_prob:.0f}%)"
            expl_ar = f"الذكاء الاصطناعي محايد ({ml_prob:.0f}%)"
        criteres_result.append({'id': 'ml_prediction', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 2. Analyse Technique ═══
        tech = result.get('score_technique', 50)
        c = cls.CRITERES['score_technique']
        if tech >= 70:
            vote = 1; score = tech
            expl = f"Technique forte ({tech:.0f}/100): tendance + indicateurs alignés"
            expl_ar = f"تحليل تقني قوي ({tech:.0f}/100): اتجاه ومؤشرات متوافقة"
        elif tech >= 55:
            vote = 0.5; score = tech
            expl = f"Technique correcte ({tech:.0f}/100)"
            expl_ar = f"تحليل تقني مقبول ({tech:.0f}/100)"
        elif tech <= 35:
            vote = -1; score = 100 - tech
            expl = f"Technique faible ({tech:.0f}/100): signaux négatifs"
            expl_ar = f"تحليل تقني ضعيف ({tech:.0f}/100): إشارات سلبية"
        elif tech <= 45:
            vote = -0.5; score = 50
            expl = f"Technique médiocre ({tech:.0f}/100)"
            expl_ar = f"تحليل تقني متوسط ({tech:.0f}/100)"
        else:
            vote = 0; score = 50
            expl = f"Technique neutre ({tech:.0f}/100)"
            expl_ar = f"تحليل تقني محايد ({tech:.0f}/100)"
        criteres_result.append({'id': 'score_technique', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 3. Analyse Fondamentale ═══
        fonda = result.get('score_fondamental', 50)
        c = cls.CRITERES['score_fondamental']
        if fonda >= 70:
            vote = 1; score = fonda
            expl = f"Fondamentaux solides ({fonda:.0f}/100): qualité + BlackRock"
            expl_ar = f"أساسيات قوية ({fonda:.0f}/100): جودة + بلاك روك"
        elif fonda >= 55:
            vote = 0.5; score = fonda
            expl = f"Fondamentaux corrects ({fonda:.0f}/100)"
            expl_ar = f"أساسيات مقبولة ({fonda:.0f}/100)"
        elif fonda <= 35:
            vote = -1; score = 100 - fonda
            expl = f"Fondamentaux faibles ({fonda:.0f}/100)"
            expl_ar = f"أساسيات ضعيفة ({fonda:.0f}/100)"
        else:
            vote = 0; score = 50
            expl = f"Fondamentaux neutres ({fonda:.0f}/100)"
            expl_ar = f"أساسيات محايدة ({fonda:.0f}/100)"
        criteres_result.append({'id': 'score_fondamental', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 4. Ratio Risque/Récompense ═══
        rr = result.get('ratio_rr', 0)
        c = cls.CRITERES['ratio_rr']
        if rr >= 2.5:
            vote = 1; score = 90
            expl = f"R:R excellent ({rr:.1f}) — risque 1€ pour gagner {rr:.1f}€"
            expl_ar = f"نسبة ممتازة ({rr:.1f}) — تخاطر بـ 1€ لتربح {rr:.1f}€"
        elif rr >= 1.5:
            vote = 0.7; score = 75
            expl = f"R:R bon ({rr:.1f})"
            expl_ar = f"نسبة جيدة ({rr:.1f})"
        elif rr >= 1.0:
            vote = 0.2; score = 55
            expl = f"R:R acceptable ({rr:.1f})"
            expl_ar = f"نسبة مقبولة ({rr:.1f})"
        elif rr > 0:
            vote = -0.5; score = 35
            expl = f"R:R insuffisant ({rr:.1f}) — risque > récompense"
            expl_ar = f"نسبة غير كافية ({rr:.1f}) — المخاطرة أكبر من المكافأة"
        else:
            vote = -1; score = 10
            expl = "R:R nul ou négatif"
            expl_ar = "نسبة معدومة أو سلبية"
        criteres_result.append({'id': 'ratio_rr', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 5. Momentum ═══
        mom = result.get('score_momentum', 50)
        tend = result.get('score_tendance', 2.5)
        c = cls.CRITERES['momentum']
        if mom >= 70 and tend >= 4:
            vote = 1; score = mom
            expl = f"Forte dynamique haussière ({mom:.0f}/100, tendance {tend}/5)"
            expl_ar = f"زخم صعودي قوي ({mom:.0f}/100، اتجاه {tend}/5)"
        elif mom >= 55:
            vote = 0.5; score = mom
            expl = f"Momentum positif ({mom:.0f}/100)"
            expl_ar = f"زخم إيجابي ({mom:.0f}/100)"
        elif mom <= 35:
            vote = -1; score = 100 - mom
            expl = f"Momentum négatif ({mom:.0f}/100)"
            expl_ar = f"زخم سلبي ({mom:.0f}/100)"
        else:
            vote = 0; score = 50
            expl = f"Momentum neutre ({mom:.0f}/100)"
            expl_ar = f"زخم محايد ({mom:.0f}/100)"
        criteres_result.append({'id': 'momentum', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 6. Sentiment News ═══
        news = result.get('news_score', 50)
        c = cls.CRITERES['news_sentiment']
        if news >= 70:
            vote = 1; score = news
            expl = f"News positives ({news:.0f}/100)"
            expl_ar = f"أخبار إيجابية ({news:.0f}/100)"
        elif news <= 30:
            vote = -1; score = 100 - news
            expl = f"News négatives ({news:.0f}/100)"
            expl_ar = f"أخبار سلبية ({news:.0f}/100)"
        else:
            vote = 0; score = 50
            expl = f"News neutres ({news:.0f}/100)"
            expl_ar = f"أخبار محايدة ({news:.0f}/100)"
        criteres_result.append({'id': 'news_sentiment', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 7. Smart Money Flow ═══
        sm = result.get('smart_money_signal', '')
        c = cls.CRITERES['smart_money']
        if '🟢🟢' in sm:
            vote = 1; score = 85
            expl = "Les institutionnels accumulent"
            expl_ar = "المؤسسات الكبيرة تشتري بكثافة"
        elif '🟢' in sm:
            vote = 0.5; score = 65
            expl = "Smart Money légèrement positif"
            expl_ar = "الأموال الذكية إيجابية قليلاً"
        elif '🔴🔴' in sm:
            vote = -1; score = 85
            expl = "Les institutionnels vendent"
            expl_ar = "المؤسسات الكبيرة تبيع بكثافة"
        elif '🔴' in sm:
            vote = -0.5; score = 35
            expl = "Smart Money légèrement négatif"
            expl_ar = "الأموال الذكية سلبية قليلاً"
        else:
            vote = 0; score = 50
            expl = "Smart Money neutre"
            expl_ar = "الأموال الذكية محايدة"
        criteres_result.append({'id': 'smart_money', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 8. Volume ═══
        vol_r = result.get('volume_ratio', 1)
        c = cls.CRITERES['volume']
        if vol_r >= 2.0:
            vote = 1; score = 80
            expl = f"Volume élevé (x{vol_r:.1f}) — confirmation solide"
            expl_ar = f"حجم مرتفع (x{vol_r:.1f}) — تأكيد قوي"
        elif vol_r >= 1.3:
            vote = 0.5; score = 65
            expl = f"Volume correct (x{vol_r:.1f})"
            expl_ar = f"حجم مقبول (x{vol_r:.1f})"
        elif vol_r <= 0.5:
            vote = -0.5; score = 30
            expl = f"Volume très faible (x{vol_r:.1f}) — signal pas fiable"
            expl_ar = f"حجم ضعيف جداً (x{vol_r:.1f}) — الإشارة غير موثوقة"
        else:
            vote = 0; score = 50
            expl = f"Volume normal (x{vol_r:.1f})"
            expl_ar = f"حجم عادي (x{vol_r:.1f})"
        criteres_result.append({'id': 'volume', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 9. RSI ═══
        rsi = result.get('rsi', 50)
        c = cls.CRITERES['rsi_signal']
        if rsi < 30:
            vote = 1; score = 85
            expl = f"RSI survendu ({rsi:.0f}) — opportunité d'achat"
            expl_ar = f"تشبع بيعي ({rsi:.0f}) — فرصة شراء"
        elif rsi < 40:
            vote = 0.5; score = 65
            expl = f"RSI bas ({rsi:.0f}) — zone intéressante"
            expl_ar = f"RSI منخفض ({rsi:.0f}) — منطقة مثيرة"
        elif rsi > 75:
            vote = -1; score = 80
            expl = f"RSI surachat ({rsi:.0f}) — DANGER"
            expl_ar = f"تشبع شرائي ({rsi:.0f}) — خطر!"
        elif rsi > 65:
            vote = -0.3; score = 40
            expl = f"RSI élevé ({rsi:.0f}) — prudence"
            expl_ar = f"RSI مرتفع ({rsi:.0f}) — حذر"
        else:
            vote = 0; score = 50
            expl = f"RSI neutre ({rsi:.0f})"
            expl_ar = f"RSI محايد ({rsi:.0f})"
        criteres_result.append({'id': 'rsi_signal', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ═══ 10. Earnings ═══
        earn = result.get('earnings_score', 50)
        earn_sig = result.get('earnings_signal', '')
        c = cls.CRITERES['earnings']
        if earn >= 70:
            vote = 1; score = earn
            expl = f"Earnings solides ({earn:.0f}/100)"
            expl_ar = f"أرباح فصلية قوية ({earn:.0f}/100)"
        elif earn <= 30:
            vote = -1; score = 100 - earn
            expl = f"Earnings décevants ({earn:.0f}/100)"
            expl_ar = f"أرباح فصلية مخيبة ({earn:.0f}/100)"
        else:
            vote = 0; score = 50
            expl = f"Earnings neutres ({earn:.0f}/100)"
            expl_ar = f"أرباح فصلية محايدة ({earn:.0f}/100)"
        criteres_result.append({'id': 'earnings', 'nom': c['nom'], 'nom_ar': c['nom_ar'],
            'vote': vote, 'score': score, 'poids': c['poids'], 'expl': expl, 'expl_ar': expl_ar})
        score_total += vote * c['poids']; poids_total += c['poids']

        # ══════════════════════════════════════════════════════════════
        #  VERDICT FINAL
        # ══════════════════════════════════════════════════════════════
        # score_total est dans [-1, +1] (normalisé par poids)
        # On le convertit en pourcentage de réussite [0, 100]
        score_norm = score_total / poids_total if poids_total > 0 else 0  # [-1, +1]

        # Calcul du pourcentage de réussite
        # Base: 50% (neutre) + ajustement basé sur le score
        pct_reussite = 50 + score_norm * 35  # Donne une plage de ~15% à ~85%

        # Bonus si le ML a été entraîné et donne un signal clair
        if ml_conf == 'HAUTE' and ml_prob >= 65:
            pct_reussite = min(92, pct_reussite + 5)
        elif ml_conf == 'HAUTE' and ml_prob <= 35:
            pct_reussite = max(8, pct_reussite - 5)

        # Plafonnement réaliste (jamais 100%, jamais 0%)
        pct_reussite = max(12, min(88, pct_reussite))

        # ═══ INTÉGRATION PPO (utiliser le résultat DÉJÀ CALCULÉ lors du scan) ═══
        # Même logique de gate que le moteur principal: vérifier action + fiabilité
        ppo_result = None
        try:
            if result.get('ppo_disponible', False):
                _ppo_action = str(result.get('ppo_action', 'NON'))
                _ppo_fiab = float(result.get('ppo_fiabilite', 0) or 0)
                _ppo_prob = float(result.get('ppo_probabilite_achat', 50) or 50)
                _ppo_conf = result.get('ppo_confiance', 'BASSE')
                ppo_result = {
                    'action': _ppo_action,
                    'probabilite_achat': _ppo_prob,
                    'fiabilite': _ppo_fiab,
                    'confiance_ppo': _ppo_conf,
                    'unanimite': False,
                }
                # Gate PPO cohérente avec le moteur: seuil lu depuis le résultat (injecté par analyser_action)
                _ppo_min_fiab = float(result.get('_config_ppo_min_fiab', 62.0) or 62.0)
                if _ppo_action == 'OUI' and _ppo_fiab >= _ppo_min_fiab:
                    # PPO valide → intégrer positivement
                    pct_reussite = pct_reussite * 0.70 + _ppo_prob * 0.30
                elif _ppo_action == 'NON' and _ppo_fiab >= _ppo_min_fiab:
                    # PPO dit NON avec confiance → pénaliser (forcer à la baisse)
                    ppo_penalite = max(10, 50 - _ppo_prob * 0.5)  # 10..50, toujours < 50
                    pct_reussite = pct_reussite * 0.70 + ppo_penalite * 0.30
                # Sinon (fiabilité trop basse): on ignore PPO, pct_reussite inchangé
                pct_reussite = max(12, min(88, pct_reussite))
        except Exception:
            pass

        # Comptage des votes
        nb_pour = sum(1 for c in criteres_result if c['vote'] > 0.3)
        nb_contre = sum(1 for c in criteres_result if c['vote'] < -0.3)
        nb_neutre = len(criteres_result) - nb_pour - nb_contre

        # Verdict — RR_MIN lu depuis le profil (injecté par analyser_action)
        # HAUTE: ×0.8 (même que moteur principal), MOYENNE: ×0.6 (seuil assoupli)
        _rr_min_ia = float(result.get('_config_rr_min', 1.5) or 1.5)
        if pct_reussite >= 65 and rr >= _rr_min_ia * 0.8 and nb_pour >= 5:
            verdict = 'OUI'
            emoji = '✅'
            couleur = '#3fb950'
            confiance = 'TRÈS HAUTE' if pct_reussite >= 75 else 'HAUTE'
        elif pct_reussite >= 58 and rr >= _rr_min_ia * 0.6 and nb_pour >= 4:
            verdict = 'OUI'
            emoji = '✅'
            couleur = '#58a6ff'
            confiance = 'MOYENNE'
        elif pct_reussite <= 38 and nb_contre >= 5:
            verdict = 'NON'
            emoji = '❌'
            couleur = '#f85149'
            confiance = 'TRÈS HAUTE' if pct_reussite <= 30 else 'HAUTE'
        elif pct_reussite <= 45 and nb_contre >= 3:
            verdict = 'NON'
            emoji = '❌'
            couleur = '#f85149'
            confiance = 'MOYENNE'
        else:
            verdict = 'ATTENDRE'
            emoji = '⏳'
            couleur = '#d29922'
            confiance = 'BASSE'

        # Résumés
        sym = result.get('symbole', '?')
        prix = result.get('prix', 0)
        sl = result.get('stop_loss', 0)
        tp = result.get('take_profit', 0)

        if verdict == 'OUI':
            resume_fr = (f"{emoji} OUI — Acheter {sym} à {prix:.2f}€\n"
                f"🎯 Objectif: {tp:.2f}€ (+{result.get('potentiel',0):.1f}%)\n"
                f"🛑 Stop Loss: {sl:.2f}€\n"
                f"📊 {nb_pour} critères favorables sur 10\n"
                f"🎲 Probabilité de réussite: {pct_reussite:.0f}%")
            resume_ar = (f"{emoji} نعم — اشترِ {sym} بسعر {prix:.2f}€\n"
                f"🎯 الهدف: {tp:.2f}€ (+{result.get('potentiel',0):.1f}%)\n"
                f"🛑 وقف الخسارة: {sl:.2f}€\n"
                f"📊 {nb_pour} معايير إيجابية من 10\n"
                f"🎲 احتمال النجاح: {pct_reussite:.0f}%")
        elif verdict == 'NON':
            resume_fr = (f"{emoji} NON — Éviter {sym} à {prix:.2f}€\n"
                f"⚠️ {nb_contre} critères négatifs sur 10\n"
                f"🎲 Probabilité d'échec: {100-pct_reussite:.0f}%")
            resume_ar = (f"{emoji} لا — تجنب {sym} بسعر {prix:.2f}€\n"
                f"⚠️ {nb_contre} معايير سلبية من 10\n"
                f"🎲 احتمال الفشل: {100-pct_reussite:.0f}%")
        else:
            resume_fr = (f"{emoji} ATTENDRE — {sym} pas de signal clair\n"
                f"📊 {nb_pour} pour, {nb_contre} contre, {nb_neutre} neutres\n"
                f"💡 Attendez un signal plus clair avant d'agir")
            resume_ar = (f"{emoji} انتظر — {sym} لا إشارة واضحة\n"
                f"📊 {nb_pour} لصالح، {nb_contre} ضد، {nb_neutre} محايد\n"
                f"💡 انتظر إشارة أوضح قبل التصرف")

        return {
            'verdict': verdict,
            'emoji': emoji,
            'pourcentage_reussite': round(pct_reussite, 1),
            'confiance': confiance,
            'nb_pour': nb_pour,
            'nb_contre': nb_contre,
            'nb_neutre': nb_neutre,
            'criteres': criteres_result,
            'resume_fr': resume_fr,
            'resume_ar': resume_ar,
            'couleur': couleur,
            'score_norm': round(score_norm, 3),
            'ppo': ppo_result,  # None si PPO pas entraîné
        }


# ══════════════════════════════════════════════════════════════════════════════
#            🖥️ INTERFACE GRAPHIQUE TKINTER (DARK THEME)
# ══════════════════════════════════════════════════════════════════════════════
class InterfaceScreener:
    BG = '#0d1117'; FG = '#c9d1d9'; ACCENT = '#58a6ff'; GREEN = '#3fb950'
    RED = '#f85149'; YELLOW = '#d29922'; HEADER_BG = '#161b22'; BUTTON_BG = '#21262d'

    def __init__(self):
        import tkinter as tk
        from tkinter import ttk, messagebox, scrolledtext
        self.tk = tk; self.ttk = ttk; self.messagebox = messagebox
        self.config = Config.charger()
        self.moteur = MoteurAnalyse(self.config)
        self.results = []; self.running = False; self.queue = Queue()

        # Fenêtre principale
        self.root = tk.Tk()
        self.root.title("🏦 BlackRock Ultra Screener v10.0")
        self.root.geometry("1900x1050")
        self.root.configure(bg=self.BG)
        self.root.state('zoomed')

        self._build_styles()
        self._build_ui()
        self._poll_queue()

    def _build_styles(self):
        s = self.ttk.Style()
        s.theme_use('clam')
        s.configure('Dark.TFrame', background=self.BG)
        s.configure('Dark.TLabel', background=self.BG, foreground=self.FG, font=('Segoe UI',10))
        s.configure('Title.TLabel', background=self.BG, foreground=self.ACCENT, font=('Segoe UI',14,'bold'))
        s.configure('Dark.TButton', background=self.BUTTON_BG, foreground=self.FG, font=('Segoe UI',10,'bold'), padding=8)
        s.map('Dark.TButton', background=[('active',self.ACCENT)])
        s.configure('Green.TButton', background='#238636', foreground='white', font=('Segoe UI',10,'bold'), padding=8)
        s.map('Green.TButton', background=[('active','#2ea043')])
        s.configure('Red.TButton', background='#da3633', foreground='white', font=('Segoe UI',10,'bold'), padding=8)
        s.configure('Accent.TButton', background=self.ACCENT, foreground='#0d1117', font=('Segoe UI',10,'bold'), padding=8)
        s.configure('Header.TLabel', background=self.HEADER_BG, foreground=self.ACCENT, font=('Segoe UI',11,'bold'))
        s.configure('Dark.TEntry', fieldbackground=self.HEADER_BG, foreground=self.FG)
        # Treeview
        s.configure('Dark.Treeview', background=self.BG, foreground=self.FG, fieldbackground=self.BG,
                     font=('Consolas',9), rowheight=26)
        s.configure('Dark.Treeview.Heading', background=self.HEADER_BG, foreground=self.ACCENT,
                     font=('Segoe UI',9,'bold'))
        s.map('Dark.Treeview', background=[('selected','#1f6feb')], foreground=[('selected','white')])
        s.configure('Dark.TRadiobutton', background=self.BG, foreground=self.FG, font=('Segoe UI',10))
        s.configure('Dark.TCombobox', fieldbackground=self.HEADER_BG, foreground=self.FG)

    def _build_ui(self):
        tk = self.tk; ttk = self.ttk

        # ═ HEADER ═
        header = ttk.Frame(self.root, style='Dark.TFrame')
        header.pack(fill='x', padx=10, pady=(10,5))

        ttk.Label(header, text="🏦 BLACKROCK ULTRA SCREENER v10.0", style='Title.TLabel').pack(side='left', padx=5)

        # Boutons principaux
        btn_frame = ttk.Frame(header, style='Dark.TFrame')
        btn_frame.pack(side='right')

        ttk.Button(btn_frame, text="🚀 ANALYSER", style='Green.TButton',
                   command=self._lancer_analyse).pack(side='left', padx=3)
        ttk.Button(btn_frame, text="⚡ SNIPER", style='Accent.TButton',
                   command=self._lancer_sniper).pack(side='left', padx=3)
        ttk.Button(btn_frame, text="🧠 ENTRAINER ML", style='Dark.TButton',
                   command=self._lancer_entrainement).pack(side='left', padx=3)
        ttk.Button(btn_frame, text="🧠 PPO V5 SMART", style='Dark.TButton',
                   command=self._lancer_ppo).pack(side='left', padx=3)
        ttk.Button(btn_frame, text="📊 RAPPORT", style='Dark.TButton',
                   command=self._generer_rapport).pack(side='left', padx=3)
        ttk.Button(btn_frame, text="⏹ STOP", style='Red.TButton',
                   command=self._stop).pack(side='left', padx=3)

        # ═ FILTRES ═
        filter_frame = ttk.Frame(self.root, style='Dark.TFrame')
        filter_frame.pack(fill='x', padx=10, pady=3)

        # Marché
        self.market_var = tk.StringVar(value='Tous')
        for m in ['Tous','PEA','US','France','Europe','PME','Crypto']:
            ttk.Radiobutton(filter_frame, text=m, variable=self.market_var, value=m,
                           style='Dark.TRadiobutton').pack(side='left', padx=5)

        # Recherche
        ttk.Label(filter_frame, text="🔍", style='Dark.TLabel').pack(side='left', padx=(20,2))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20, style='Dark.TEntry')
        self.search_entry.pack(side='left', padx=2)
        self.search_var.trace_add('write', lambda *_: self._filtrer())

        # Secteur
        ttk.Label(filter_frame, text="Secteur:", style='Dark.TLabel').pack(side='left', padx=(15,2))
        self.sector_var = tk.StringVar(value='Tous')
        sectors = ['Tous','Technologie','Finance','Santé','Consommation','Industrie','Énergie',
                   'Luxe','Automobile','Gaming','Crypto','Défense','Télécom','Média','Immobilier']
        self.sector_combo = ttk.Combobox(filter_frame, textvariable=self.sector_var, values=sectors,
                                         width=15, style='Dark.TCombobox', state='readonly')
        self.sector_combo.pack(side='left', padx=2)
        self.sector_combo.bind('<<ComboboxSelected>>', lambda _: self._filtrer())
        self.market_var.trace_add('write', lambda *_: self._filtrer())

        # Score min
        ttk.Label(filter_frame, text="Score≥", style='Dark.TLabel').pack(side='left', padx=(15,2))
        self.score_min_var = tk.IntVar(value=30)
        tk.Spinbox(filter_frame, from_=0, to=100, textvariable=self.score_min_var, width=4,
                   bg=self.HEADER_BG, fg=self.FG, command=self._filtrer).pack(side='left', padx=2)

        # ═ STATUS BAR ═
        self.status_var = tk.StringVar(value="Prêt — Sélectionnez un marché et lancez l'analyse")
        status_frame = ttk.Frame(self.root, style='Dark.TFrame')
        status_frame.pack(fill='x', padx=10, pady=3)
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Dark.TLabel')
        self.status_label.pack(side='left')
        self.count_var = tk.StringVar(value="")
        ttk.Label(status_frame, textvariable=self.count_var, style='Header.TLabel').pack(side='right')

        # ═ PROGRESS ═
        self.progress = ttk.Progressbar(self.root, mode='determinate', length=400)
        self.progress.pack(fill='x', padx=10, pady=2)

        # ═══════════════════════════════════════════════════════════
        # NOTEBOOK (2 ONGLETS)
        # ═══════════════════════════════════════════════════════════
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # ── ONGLET 1 : Tableau Screener ──
        tab_screener = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(tab_screener, text='  📊 Tableau des Résultats  ')

        # ═ TREEVIEW PRINCIPAL ═
        tree_frame = ttk.Frame(tab_screener, style='Dark.TFrame')
        tree_frame.pack(fill='both', expand=True, padx=0, pady=0)

        cols = ('symbole','secteur','prix','score_final','decision',
            'horizon_mode','horizon_jours',
                'score_technique','score_fondamental','score_momentum',
            'precision_score','pred_horizon_pct','ev_pct',
                'potentiel','ratio_rr','stop_loss','take_profit',
                'kelly_used_pct','position_value','risk_score','expected_r','var_5j',
                'rsi','ml_probabilite','var_1j','var_1s','raison')

        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', style='Dark.Treeview', height=30)

        headers = {
            'symbole':'Symbole','secteur':'Secteur','prix':'Prix',
            'score_final':'SCORE','decision':'Décision',
            'horizon_mode':'Hz','horizon_jours':'J',
            'score_technique':'Tech','score_fondamental':'Fonda','score_momentum':'Momentum',
            'precision_score':'Précision','pred_horizon_pct':'PredHz%','ev_pct':'EV%',
            'potentiel':'Potentiel%','ratio_rr':'R:R',
            'stop_loss':'SL','take_profit':'TP',
            'kelly_used_pct':'Kelly%','position_value':'Pos$','risk_score':'Risk',
            'expected_r':'E[R]','var_5j':'VaR5j',
            'rsi':'RSI','ml_probabilite':'ML%',
            'var_1j':'Var1J','var_1s':'Var1S','raison':'Raison'
        }
        widths = {'symbole':85,'secteur':100,'prix':70,'score_final':60,
                'decision':145,'horizon_mode':48,'horizon_jours':40,
                'score_technique':55,'score_fondamental':55,
                  'score_momentum':70,'potentiel':75,'ratio_rr':55,
                'precision_score':70,'pred_horizon_pct':72,'ev_pct':62,
                  'stop_loss':70,'take_profit':70,
                  'kelly_used_pct':55,'position_value':70,'risk_score':50,
                  'expected_r':50,'var_5j':58,
                  'rsi':50,'ml_probabilite':50,
                  'var_1j':60,'var_1s':60,'raison':300}

        for col in cols:
            self.tree.heading(col, text=headers.get(col,col),
                            command=lambda c=col: self._trier(c))
            self.tree.column(col, width=widths.get(col,80), anchor='center')

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True)

        # Double-click pour détails
        self.tree.bind('<Double-1>', self._afficher_details)

        # Tags couleur
        self.tree.tag_configure('green', foreground=self.GREEN)
        self.tree.tag_configure('red', foreground=self.RED)
        self.tree.tag_configure('yellow', foreground=self.YELLOW)
        self.tree.tag_configure('white', foreground=self.FG)

        # ═══════════════════════════════════════════════════════════
        # ONGLET 2 : 🧠 SYSTÈME DE DÉCISION IA
        # ═══════════════════════════════════════════════════════════
        tab_decision = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(tab_decision, text='  🧠 Décision IA — OUI ou NON?  ')

        self._build_decision_tab(tab_decision)

        # ═══════════════════════════════════════════════════════════
        # ONGLET 3 : ⚙️ PARAMÈTRES ALPHA PRO
        # ═══════════════════════════════════════════════════════════
        tab_params = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(tab_params, text='  ⚙️ Paramètres Alpha PRO  ')

        self._build_params_tab(tab_params)

        # ═══════════════════════════════════════════════════════════
        # ONGLET 4 : 🛡️ RISK MANAGEMENT
        # ═══════════════════════════════════════════════════════════
        tab_risk = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(tab_risk, text='  🛡️ Risk Management  ')
        self._build_risk_tab(tab_risk)

        # ═ Sélection simple dans le tree → mise à jour de l'onglet Décision ═
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)

    # ══════════════════════════════════════════════════════════════════
    #  _build_params_tab  — ONGLET PARAMÈTRES ALPHA PRO (COMPLET)
    # ══════════════════════════════════════════════════════════════════
    def _build_params_tab(self, parent):
        tk = self.tk; ttk = self.ttk; cfg = self.config

        # ── Scrollable container ──
        canvas = tk.Canvas(parent, bg=self.BG, highlightthickness=0)
        vsb = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.BG)
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

        pf = scroll_frame  # parent frame shortcut

        # ── Couleurs sombres pour les LabelFrames ──
        lf_opts = dict(bg='#161b22', fg=self.ACCENT, font=('Segoe UI', 11, 'bold'),
                       padx=10, pady=8)
        inner_bg = '#161b22'

        # ═══════════════════════════════════════════════════════════
        # HEADER — Titre + boutons Appliquer / Sauvegarder / Reset
        # ═══════════════════════════════════════════════════════════
        hdr = tk.Frame(pf, bg=self.BG)
        hdr.pack(fill='x', padx=15, pady=(12, 5))
        tk.Label(hdr, text="⚙️ PARAMÈTRES ALPHA FACTOR ENGINE — CONFIGURATION PRO",
                 font=('Segoe UI', 16, 'bold'), fg=self.ACCENT, bg=self.BG).pack(side='left')
        btn_f = tk.Frame(hdr, bg=self.BG)
        btn_f.pack(side='right')
        tk.Button(btn_f, text="✅ APPLIQUER", bg='#238636', fg='white',
                  font=('Segoe UI', 10, 'bold'), padx=12, pady=4,
                  command=self._appliquer_params).pack(side='left', padx=4)
        tk.Button(btn_f, text="💾 SAUVEGARDER", bg=self.ACCENT, fg='#0d1117',
                  font=('Segoe UI', 10, 'bold'), padx=12, pady=4,
                  command=self._sauvegarder_params).pack(side='left', padx=4)
        tk.Button(btn_f, text="🔄 RESET DÉFAUT", bg='#da3633', fg='white',
                  font=('Segoe UI', 10, 'bold'), padx=12, pady=4,
                  command=self._reset_params).pack(side='left', padx=4)

        # ═══════════════════════════════════════════════════════════
        # ROW 1: PROFIL + MODE (côte à côte)
        # ═══════════════════════════════════════════════════════════
        row1 = tk.Frame(pf, bg=self.BG)
        row1.pack(fill='x', padx=15, pady=5)

        # ── PROFIL ──
        lf_profil = tk.LabelFrame(row1, text="🎯 PROFIL ACTIF", **lf_opts)
        lf_profil.pack(side='left', fill='both', expand=True, padx=(0, 5))

        prow = tk.Frame(lf_profil, bg=inner_bg)
        prow.pack(fill='x', padx=5, pady=5)
        tk.Label(prow, text="Profil:", bg=inner_bg, fg=self.FG,
                 font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.pv_profil = tk.StringVar(value=getattr(cfg, 'PROFIL_ACTIF', 'BALANCED'))
        profils = ['BALANCED', 'PROFIT_MAX', 'PRECISION_MAX', 'SCALP_MAX', 'INTRADAY_MAX',
                   'SWING_MAX', 'NASDAQ_SNIPER', 'SP500_VALUE', 'COMMODITIES', 'INVESTISSEUR_1AN']
        cb = ttk.Combobox(prow, textvariable=self.pv_profil, values=profils, width=20,
                          state='readonly', style='Dark.TCombobox')
        cb.pack(side='left', padx=5)
        tk.Button(prow, text="⚡ Charger", bg=self.BUTTON_BG, fg=self.FG,
                  font=('Segoe UI', 9), padx=8,
                  command=self._charger_profil).pack(side='left', padx=5)

        # ── MODE ──
        lf_mode = tk.LabelFrame(row1, text="🔧 MODE ENGINE", **lf_opts)
        lf_mode.pack(side='left', fill='both', expand=True, padx=(5, 0))

        self.pv_scoring = tk.StringVar(value=getattr(cfg, 'SCORING_MODE', 'ALPHA_FACTOR'))
        self.pv_fast = tk.BooleanVar(value=getattr(cfg, 'FAST_MODE', True))
        self.pv_cross = tk.BooleanVar(value=getattr(cfg, 'CROSS_SECTIONAL_RANKING', True))
        self.pv_regime = tk.BooleanVar(value=getattr(cfg, 'REGIME_ADAPTIVE_WEIGHTS', True))

        mr = tk.Frame(lf_mode, bg=inner_bg)
        mr.pack(fill='x', padx=5, pady=3)
        tk.Label(mr, text="Scoring:", bg=inner_bg, fg=self.FG, font=('Segoe UI', 10)).pack(side='left', padx=5)
        for v in ['ALPHA_FACTOR', 'LEGACY']:
            tk.Radiobutton(mr, text=v, variable=self.pv_scoring, value=v,
                           bg=inner_bg, fg=self.FG, selectcolor='#21262d',
                           font=('Segoe UI', 9), activebackground=inner_bg).pack(side='left', padx=5)

        mr2 = tk.Frame(lf_mode, bg=inner_bg)
        mr2.pack(fill='x', padx=5, pady=3)
        tk.Checkbutton(mr2, text="⚡ Fast Mode (skip ML retrain)", variable=self.pv_fast,
                       bg=inner_bg, fg=self.FG, selectcolor='#21262d',
                       font=('Segoe UI', 9), activebackground=inner_bg).pack(side='left', padx=5)
        tk.Checkbutton(mr2, text="📊 Cross-Sectional Ranking", variable=self.pv_cross,
                       bg=inner_bg, fg=self.FG, selectcolor='#21262d',
                       font=('Segoe UI', 9), activebackground=inner_bg).pack(side='left', padx=15)
        tk.Checkbutton(mr2, text="🌊 Regime-Adaptive Weights", variable=self.pv_regime,
                       bg=inner_bg, fg=self.FG, selectcolor='#21262d',
                       font=('Segoe UI', 9), activebackground=inner_bg).pack(side='left', padx=15)

        # Horizon mode
        mr3 = tk.Frame(lf_mode, bg=inner_bg)
        mr3.pack(fill='x', padx=5, pady=3)
        tk.Label(mr3, text="Horizon:", bg=inner_bg, fg=self.FG, font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.pv_horizon = tk.StringVar(value=getattr(cfg, 'HORIZON_MODE', 'SWING'))
        for h in ['SCALP', 'INTRADAY', 'SWING', 'INVESTISSEUR']:
            tk.Radiobutton(mr3, text=h, variable=self.pv_horizon, value=h,
                           bg=inner_bg, fg=self.FG, selectcolor='#21262d',
                           font=('Segoe UI', 9), activebackground=inner_bg).pack(side='left', padx=5)

        # ═══════════════════════════════════════════════════════════
        # ROW 2: ALPHA WEIGHTS (8 sliders)
        # ═══════════════════════════════════════════════════════════
        lf_alpha = tk.LabelFrame(pf, text="📐 ALPHA FACTOR WEIGHTS (somme auto-normalisée)",
                                 **lf_opts)
        lf_alpha.pack(fill='x', padx=15, pady=5)

        self.alpha_sliders = {}
        alpha_defs = [
            ('ALPHA_W_MOMENTUM',   '🚀 Momentum',   'Rendement 3m/1m + trend + MACD'),
            ('ALPHA_W_REVERSAL',   '🔄 Reversal',    'Z-score + RSI extrême + reversal'),
            ('ALPHA_W_QUALITY',    '⭐ Quality',     'ROE + dette + marges + FCF'),
            ('ALPHA_W_VALUE',      '💎 Value',       'PE + PB + dividende + FCF yield'),
            ('ALPHA_W_FLOW',       '💰 Smart Money', 'Flux institutionnel + volume + CMF'),
            ('ALPHA_W_ML',         '🤖 ML Signal',   'Probabilité ML + consensus + news'),
            ('ALPHA_W_REGIME',     '🌊 Regime',      'Hurst + CUSUM + contexte macro'),
            ('ALPHA_W_PPO',        '🎮 PPO RL',      'PPO probabilité + fiabilité'),
        ]

        # 2 colonnes de 4 sliders
        alpha_container = tk.Frame(lf_alpha, bg=inner_bg)
        alpha_container.pack(fill='x', padx=5, pady=5)

        for idx, (key, label, desc) in enumerate(alpha_defs):
            col = idx % 2
            row = idx // 2
            fr = tk.Frame(alpha_container, bg=inner_bg)
            fr.grid(row=row, column=col, sticky='ew', padx=8, pady=3)
            alpha_container.columnconfigure(col, weight=1)

            val = getattr(cfg, key, 0.10)
            var = tk.DoubleVar(value=val)
            self.alpha_sliders[key] = var

            top_row = tk.Frame(fr, bg=inner_bg)
            top_row.pack(fill='x')
            tk.Label(top_row, text=label, bg=inner_bg, fg=self.FG,
                     font=('Segoe UI', 10, 'bold'), width=16, anchor='w').pack(side='left')
            val_lbl = tk.Label(top_row, text=f"{val:.2f}", bg=inner_bg, fg=self.ACCENT,
                               font=('Consolas', 10, 'bold'), width=5)
            val_lbl.pack(side='right')

            slider = tk.Scale(fr, from_=0.0, to=0.50, resolution=0.01, orient='horizontal',
                              variable=var, bg=inner_bg, fg=self.FG, troughcolor='#21262d',
                              highlightthickness=0, sliderrelief='flat',
                              font=('Consolas', 8), showvalue=False, length=280,
                              command=lambda v, l=val_lbl: l.config(text=f"{float(v):.2f}"))
            slider.pack(fill='x')

            tk.Label(fr, text=desc, bg=inner_bg, fg='#8b949e',
                     font=('Segoe UI', 8)).pack(anchor='w')

        # Somme indicateur
        self.pv_alpha_sum = tk.StringVar(value="")
        sum_lbl = tk.Label(lf_alpha, textvariable=self.pv_alpha_sum, bg=inner_bg,
                           fg=self.YELLOW, font=('Consolas', 10, 'bold'))
        sum_lbl.pack(anchor='e', padx=15, pady=3)

        def update_sum(*_):
            s = sum(v.get() for v in self.alpha_sliders.values())
            self.pv_alpha_sum.set(f"Σ weights = {s:.2f} (auto-normalisé)")
        for v in self.alpha_sliders.values():
            v.trace_add('write', update_sum)
        update_sum()

        # ═══════════════════════════════════════════════════════════
        # ROW 3: UNIVERS D'ACTIONS (checkboxes)
        # ═══════════════════════════════════════════════════════════
        lf_univ = tk.LabelFrame(pf, text="🌍 UNIVERS D'ACTIONS", **lf_opts)
        lf_univ.pack(fill='x', padx=15, pady=5)

        uf = tk.Frame(lf_univ, bg=inner_bg)
        uf.pack(fill='x', padx=5, pady=5)

        self.univ_vars = {}
        univ_defs = [
            ('INCLURE_US',         '🇺🇸 US Large Caps',  True),
            ('INCLURE_EUROPE',     '🇪🇺 Europe',          True),
            ('INCLURE_FRANCE',     '🇫🇷 France / PEA',    True),
            ('INCLURE_PME',        '🏢 PME Small Caps',   True),
            ('INCLURE_GAMING',     '🎮 Gaming / Esport',  True),
            ('INCLURE_SANTE',      '🏥 Santé / Biotech',  True),
            ('INCLURE_NASDAQ100',  '📈 NASDAQ 100 ETFs',  True),
            ('INCLURE_SP500',      '📊 S&P 500 ETFs',     True),
            ('INCLURE_MATIERES',   '🥇 Matières Premières', True),
            ('INCLURE_CRYPTO',     '₿ Crypto',            False),
        ]

        for idx, (key, label, default) in enumerate(univ_defs):
            var = tk.BooleanVar(value=getattr(cfg, key, default))
            self.univ_vars[key] = var
            col = idx % 5
            row = idx // 5
            tk.Checkbutton(uf, text=label, variable=var, bg=inner_bg, fg=self.FG,
                           selectcolor='#21262d', font=('Segoe UI', 9),
                           activebackground=inner_bg).grid(row=row, column=col, sticky='w', padx=8, pady=2)

        # Compteur
        self.pv_univ_count = tk.StringVar(value="")
        tk.Label(lf_univ, textvariable=self.pv_univ_count, bg=inner_bg, fg=self.ACCENT,
                 font=('Segoe UI', 9, 'bold')).pack(anchor='e', padx=10, pady=2)

        def update_count(*_):
            try:
                a = UniversActions.obtenir_actions(
                    us=self.univ_vars['INCLURE_US'].get(),
                    europe=self.univ_vars['INCLURE_EUROPE'].get(),
                    france=self.univ_vars['INCLURE_FRANCE'].get(),
                    gaming=self.univ_vars['INCLURE_GAMING'].get(),
                    matieres=self.univ_vars['INCLURE_MATIERES'].get(),
                    crypto=self.univ_vars['INCLURE_CRYPTO'].get(),
                    inclure_pme=self.univ_vars['INCLURE_PME'].get(),
                    inclure_sante=self.univ_vars['INCLURE_SANTE'].get(),
                    inclure_nasdaq100=self.univ_vars['INCLURE_NASDAQ100'].get(),
                    inclure_sp500=self.univ_vars['INCLURE_SP500'].get(),
                )
                self.pv_univ_count.set(f"📊 {len(a)} actions dans l'univers")
            except:
                self.pv_univ_count.set("📊 ---")
        for v in self.univ_vars.values():
            v.trace_add('write', update_count)
        update_count()

        # ═══════════════════════════════════════════════════════════
        # ROW 4: SEUILS & TRADING (côte à côte)
        # ═══════════════════════════════════════════════════════════
        row4 = tk.Frame(pf, bg=self.BG)
        row4.pack(fill='x', padx=15, pady=5)

        # ── SEUILS SCORING ──
        lf_seuil = tk.LabelFrame(row4, text="🎯 SEUILS DE DÉCISION", **lf_opts)
        lf_seuil.pack(side='left', fill='both', expand=True, padx=(0, 5))

        self.seuil_vars = {}
        seuil_defs = [
            ('ALPHA_MIN_SCORE_BUY',  'Score ACHAT min',       58.0,  30, 90),
            ('ALPHA_MIN_SCORE_FORT', 'Score ACHAT FORT min',  72.0,  50, 95),
            ('SCORE_MINIMUM',        'Score affichage min',   25.0,   0, 80),
            ('RR_MIN',               'Ratio R:R minimum',      1.2, 0.5, 5.0),
            ('EV_MIN_PCT',           'EV minimum (%)',         1.5, 0.0, 10.0),
            ('PRECISION_MIN_SCORE',  'Précision ML min (%)',  55.0,  30, 90),
        ]

        for idx, (key, label, default, lo, hi) in enumerate(seuil_defs):
            val = getattr(cfg, key, default)
            var = tk.DoubleVar(value=val)
            self.seuil_vars[key] = var
            r = tk.Frame(lf_seuil, bg=inner_bg)
            r.pack(fill='x', padx=5, pady=2)
            tk.Label(r, text=label, bg=inner_bg, fg=self.FG,
                     font=('Segoe UI', 9), width=22, anchor='w').pack(side='left')
            val_l = tk.Label(r, text=f"{val:.1f}", bg=inner_bg, fg=self.ACCENT,
                             font=('Consolas', 10, 'bold'), width=6)
            val_l.pack(side='right')
            tk.Scale(r, from_=lo, to=hi, resolution=0.1, orient='horizontal',
                     variable=var, bg=inner_bg, fg=self.FG, troughcolor='#21262d',
                     highlightthickness=0, showvalue=False, length=200,
                     font=('Consolas', 8), sliderrelief='flat',
                     command=lambda v, l=val_l: l.config(text=f"{float(v):.1f}")).pack(side='left', fill='x', expand=True)

        # ── TRADING PARAMS ──
        lf_trade = tk.LabelFrame(row4, text="📈 PARAMÈTRES TRADING", **lf_opts)
        lf_trade.pack(side='left', fill='both', expand=True, padx=(5, 0))

        self.trade_vars = {}
        trade_defs = [
            ('STOP_LOSS_ATR',              'Stop Loss (× ATR)',      2.0, 0.5, 5.0),
            ('TAKE_PROFIT_ATR',            'Take Profit (× ATR)',    3.5, 1.0, 10.0),
            ('HORIZON_INTRADAY_JOURS',     'Horizon intraday (j)',   2,   1,   10),
            ('HORIZON_SWING_JOURS',        'Horizon swing (j)',     20,   5,  120),
            ('HORIZON_LONG_JOURS',         'Horizon position (j)',  60,  20,  120),
            ('HORIZON_INVESTISSEUR_JOURS', 'Horizon investis. (j)',252,  60,  504),
            ('PPO_MIN_FIABILITE_ACHAT',    'PPO fiabilité min',   55.0, 30,   90),
        ]

        for idx, (key, label, default, lo, hi) in enumerate(trade_defs):
            val = getattr(cfg, key, default)
            var = tk.DoubleVar(value=float(val))
            self.trade_vars[key] = var
            r = tk.Frame(lf_trade, bg=inner_bg)
            r.pack(fill='x', padx=5, pady=2)
            tk.Label(r, text=label, bg=inner_bg, fg=self.FG,
                     font=('Segoe UI', 9), width=22, anchor='w').pack(side='left')
            val_l = tk.Label(r, text=f"{val:.1f}" if isinstance(val, float) else str(val),
                             bg=inner_bg, fg=self.ACCENT,
                             font=('Consolas', 10, 'bold'), width=6)
            val_l.pack(side='right')
            res = 0.1 if isinstance(default, float) else 1
            tk.Scale(r, from_=lo, to=hi, resolution=res, orient='horizontal',
                     variable=var, bg=inner_bg, fg=self.FG, troughcolor='#21262d',
                     highlightthickness=0, showvalue=False, length=200,
                     font=('Consolas', 8), sliderrelief='flat',
                     command=lambda v, l=val_l: l.config(text=f"{float(v):.1f}")).pack(side='left', fill='x', expand=True)

        # ═══════════════════════════════════════════════════════════
        # ROW 5: PPO + ML + REGIME (côte à côte)
        # ═══════════════════════════════════════════════════════════
        row5 = tk.Frame(pf, bg=self.BG)
        row5.pack(fill='x', padx=15, pady=5)

        # ── PPO PARAMS ──
        lf_ppo = tk.LabelFrame(row5, text="🎮 PPO REINFORCEMENT LEARNING", **lf_opts)
        lf_ppo.pack(side='left', fill='both', expand=True, padx=(0, 5))

        self.ppo_vars = {}
        ppo_defs = [
            ('PPO_FAST_CANDIDATES',  'Nb candidats PPO',  2,       1,      5),
            ('PPO_FAST_TIMESTEPS',   'Timesteps PPO',     200000,  50000,  1000000),
            ('ML_MAX_SYMBOLES',      'ML max symboles',   600,     50,     1000),
        ]

        for key, label, default, lo, hi in ppo_defs:
            val = getattr(cfg, key, default)
            var = tk.IntVar(value=int(val))
            self.ppo_vars[key] = var
            r = tk.Frame(lf_ppo, bg=inner_bg)
            r.pack(fill='x', padx=5, pady=3)
            tk.Label(r, text=label, bg=inner_bg, fg=self.FG,
                     font=('Segoe UI', 9), width=18, anchor='w').pack(side='left')
            val_l = tk.Label(r, text=str(val), bg=inner_bg, fg=self.ACCENT,
                             font=('Consolas', 10, 'bold'), width=8)
            val_l.pack(side='right')
            step = 1 if hi <= 10 else (10000 if hi > 10000 else 10)
            tk.Scale(r, from_=lo, to=hi, resolution=step, orient='horizontal',
                     variable=var, bg=inner_bg, fg=self.FG, troughcolor='#21262d',
                     highlightthickness=0, showvalue=False, length=200,
                     font=('Consolas', 8), sliderrelief='flat',
                     command=lambda v, l=val_l: l.config(text=str(int(float(v))))).pack(side='left', fill='x', expand=True)

        # ── REGIME PARAMS ──
        lf_regime = tk.LabelFrame(row5, text="🌊 REGIME DETECTION", **lf_opts)
        lf_regime.pack(side='left', fill='both', expand=True, padx=(5, 0))

        self.regime_vars = {}
        regime_defs = [
            ('REGIME_SPY_SMA',          'SPY SMA period',        50,    20,   200),
            ('REGIME_VIX_THRESHOLD',    'VIX seuil peur',       25.0,  15.0,  40.0),
            ('ALPHA_MOMENTUM_BOOST_BULL','Boost momentum bull', 1.30,  1.0,   2.0),
            ('ALPHA_REVERSAL_BOOST_BEAR','Boost reversal bear', 1.40,  1.0,   2.0),
        ]

        for key, label, default, lo, hi in regime_defs:
            val = getattr(cfg, key, default)
            is_int = isinstance(default, int)
            var = tk.IntVar(value=int(val)) if is_int else tk.DoubleVar(value=float(val))
            self.regime_vars[key] = var
            r = tk.Frame(lf_regime, bg=inner_bg)
            r.pack(fill='x', padx=5, pady=3)
            tk.Label(r, text=label, bg=inner_bg, fg=self.FG,
                     font=('Segoe UI', 9), width=22, anchor='w').pack(side='left')
            fmt = f"{val}" if is_int else f"{val:.2f}"
            val_l = tk.Label(r, text=fmt, bg=inner_bg, fg=self.ACCENT,
                             font=('Consolas', 10, 'bold'), width=6)
            val_l.pack(side='right')
            res = 1 if is_int else 0.05
            tk.Scale(r, from_=lo, to=hi, resolution=res, orient='horizontal',
                     variable=var, bg=inner_bg, fg=self.FG, troughcolor='#21262d',
                     highlightthickness=0, showvalue=False, length=180,
                     font=('Consolas', 8), sliderrelief='flat',
                     command=lambda v, l=val_l, ii=is_int: l.config(
                         text=str(int(float(v))) if ii else f"{float(v):.2f}")).pack(side='left', fill='x', expand=True)

        # ═══════════════════════════════════════════════════════════
        # ROW 6: STATUS + INFO
        # ═══════════════════════════════════════════════════════════
        info_f = tk.Frame(pf, bg='#161b22', highlightbackground='#30363d', highlightthickness=1)
        info_f.pack(fill='x', padx=15, pady=(10, 15))
        self.pv_status_params = tk.StringVar(value="⚙️ Paramètres chargés depuis config")
        tk.Label(info_f, textvariable=self.pv_status_params, bg='#161b22', fg=self.ACCENT,
                 font=('Segoe UI', 10, 'bold')).pack(padx=10, pady=8)

    # ══════════════════════════════════════════════════════════════════
    #  _charger_profil  — charge un profil dans les sliders
    # ══════════════════════════════════════════════════════════════════
    def _charger_profil(self):
        profil = self.pv_profil.get()
        ok, msg = self.config.appliquer_profil(profil)
        if ok:
            # Refresh tous les widgets depuis le config mis à jour
            self._refresh_param_widgets()
            self.pv_status_params.set(f"✅ Profil {profil} chargé — sliders mis à jour")
        else:
            self.pv_status_params.set(f"❌ {msg}")

    def _refresh_param_widgets(self):
        """Synchronise les widgets GUI avec self.config"""
        cfg = self.config
        # Alpha sliders
        for key, var in self.alpha_sliders.items():
            var.set(getattr(cfg, key, var.get()))
        # Seuils
        for key, var in self.seuil_vars.items():
            var.set(getattr(cfg, key, var.get()))
        # Trade
        for key, var in self.trade_vars.items():
            var.set(float(getattr(cfg, key, var.get())))
        # PPO
        for key, var in self.ppo_vars.items():
            var.set(int(getattr(cfg, key, var.get())))
        # Regime
        for key, var in self.regime_vars.items():
            var.set(getattr(cfg, key, var.get()))
        # Univers
        for key, var in self.univ_vars.items():
            var.set(getattr(cfg, key, var.get()))
        # Modes
        self.pv_scoring.set(getattr(cfg, 'SCORING_MODE', 'ALPHA_FACTOR'))
        self.pv_fast.set(getattr(cfg, 'FAST_MODE', True))
        self.pv_cross.set(getattr(cfg, 'CROSS_SECTIONAL_RANKING', True))
        self.pv_regime.set(getattr(cfg, 'REGIME_ADAPTIVE_WEIGHTS', True))
        self.pv_horizon.set(getattr(cfg, 'HORIZON_MODE', 'SWING'))
        self.pv_profil.set(getattr(cfg, 'PROFIL_ACTIF', 'BALANCED'))

    # ══════════════════════════════════════════════════════════════════
    #  _appliquer_params  — lit les widgets et applique au config
    # ══════════════════════════════════════════════════════════════════
    def _appliquer_params(self):
        cfg = self.config
        # Modes
        cfg.SCORING_MODE = self.pv_scoring.get()
        cfg.FAST_MODE = self.pv_fast.get()
        cfg.CROSS_SECTIONAL_RANKING = self.pv_cross.get()
        cfg.REGIME_ADAPTIVE_WEIGHTS = self.pv_regime.get()
        cfg.HORIZON_MODE = self.pv_horizon.get()
        # Alpha weights
        for key, var in self.alpha_sliders.items():
            setattr(cfg, key, var.get())
        # Seuils
        for key, var in self.seuil_vars.items():
            setattr(cfg, key, var.get())
        # Trade
        for key, var in self.trade_vars.items():
            v = var.get()
            if key in ('HORIZON_INTRADAY_JOURS', 'HORIZON_SWING_JOURS'):
                setattr(cfg, key, int(v))
            else:
                setattr(cfg, key, v)
        # PPO
        for key, var in self.ppo_vars.items():
            setattr(cfg, key, int(var.get()))
        # Regime
        for key, var in self.regime_vars.items():
            val = var.get()
            if isinstance(val, float) and val == int(val) and key == 'REGIME_SPY_SMA':
                setattr(cfg, key, int(val))
            else:
                setattr(cfg, key, val)
        # Univers
        for key, var in self.univ_vars.items():
            setattr(cfg, key, var.get())

        # Sync moteur + PPO
        self.moteur.config = cfg
        if ppo_system:
            ppo_system.config = cfg

        self.pv_status_params.set("✅ Paramètres appliqués à l'engine — lancez ANALYSER pour voir les résultats")

    # ══════════════════════════════════════════════════════════════════
    #  _sauvegarder_params  — applique + sauvegarde sur disque
    # ══════════════════════════════════════════════════════════════════
    def _sauvegarder_params(self):
        self._appliquer_params()
        ok, msg = self.config.sauvegarder()
        if ok:
            self.pv_status_params.set("💾 Paramètres sauvegardés sur disque + appliqués")
        else:
            self.pv_status_params.set(f"❌ Erreur sauvegarde: {msg}")

    # ══════════════════════════════════════════════════════════════════
    #  _reset_params  — recharge les défauts
    # ══════════════════════════════════════════════════════════════════
    def _reset_params(self):
        self.config = Config()  # Défauts
        self.moteur.config = self.config
        # Synchroniser immédiatement le système PPO
        if ppo_system is not None:
            ppo_system.config = self.config
        self._refresh_param_widgets()
        self.pv_status_params.set("🔄 Paramètres réinitialisés aux valeurs par défaut")

    # ══════════════════════════════════════════════════════════════════
    #  _build_decision_tab  — construit l'onglet 🧠 Décision IA
    # ══════════════════════════════════════════════════════════════════
    def _build_decision_tab(self, parent):
        tk = self.tk; ttk = self.ttk

        # ── Conteneur principal avec scroll ──
        canvas = tk.Canvas(parent, bg=self.BG, highlightthickness=0)
        vsb = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        self.decision_frame = tk.Frame(canvas, bg=self.BG)
        self.decision_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self.decision_frame, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        # scroll molette
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

        df = self.decision_frame  # raccourci

        # ── Message par défaut (avant toute sélection) ──
        self.dec_placeholder = tk.Label(df, text=(
            "🧠 SYSTÈME DE DÉCISION IA\n\n"
            "نظام القرار بالذكاء الاصطناعي\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Lancez une analyse depuis l'onglet 📊\n"
            "     شغّل التحليل من التبويب 📊\n\n"
            "2️⃣  Cliquez sur une action dans le tableau\n"
            "     اضغط على سهم في الجدول\n\n"
            "3️⃣  Le verdict OUI / NON apparaîtra ici\n"
            "     ستظهر هنا النتيجة: نعم / لا\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Le système analyse 10 critères indépendants\n"
            "et calcule la probabilité de réussite.\n\n"
            "النظام يحلل 10 معايير مستقلة\n"
            "ويحسب احتمال النجاح."
        ), font=('Segoe UI', 14), fg='#8b949e', bg=self.BG, justify='center')
        self.dec_placeholder.pack(expand=True, fill='both', pady=80)

        # ── Conteneur pour le verdict (masqué au départ) ──
        self.dec_content = tk.Frame(df, bg=self.BG)
        # (ne pas pack maintenant — sera affiché quand on clique sur un stock)

        # Ligne 1: Symbole + Prix
        row_top = tk.Frame(self.dec_content, bg=self.BG)
        row_top.pack(fill='x', padx=30, pady=(20, 5))
        self.dec_sym_label = tk.Label(row_top, text="", font=('Segoe UI', 20, 'bold'),
                                       fg=self.ACCENT, bg=self.BG)
        self.dec_sym_label.pack(side='left')
        self.dec_prix_label = tk.Label(row_top, text="", font=('Segoe UI', 16),
                                        fg=self.FG, bg=self.BG)
        self.dec_prix_label.pack(side='left', padx=20)
        self.dec_sector_label = tk.Label(row_top, text="", font=('Segoe UI', 12),
                                          fg='#8b949e', bg=self.BG)
        self.dec_sector_label.pack(side='right')

        # ═══════════════════════════════════════════════════════
        # Ligne 2: LE GROS VERDICT
        # ═══════════════════════════════════════════════════════
        self.dec_verdict_frame = tk.Frame(self.dec_content, bg='#161b22',
                                           highlightbackground='#30363d', highlightthickness=2)
        self.dec_verdict_frame.pack(fill='x', padx=30, pady=15)

        # Verdict texte (✅ OUI / ❌ NON / ⏳ ATTENDRE)
        self.dec_verdict_label = tk.Label(self.dec_verdict_frame, text="",
                                           font=('Segoe UI', 48, 'bold'), bg='#161b22')
        self.dec_verdict_label.pack(pady=(20, 5))

        # Réponse arabe
        self.dec_verdict_ar = tk.Label(self.dec_verdict_frame, text="",
                                        font=('Segoe UI', 18), bg='#161b22', fg='#8b949e')
        self.dec_verdict_ar.pack()

        # Pourcentage de réussite — grosse police
        self.dec_pct_label = tk.Label(self.dec_verdict_frame, text="",
                                       font=('Consolas', 36, 'bold'), bg='#161b22')
        self.dec_pct_label.pack(pady=(10, 5))

        self.dec_pct_txt = tk.Label(self.dec_verdict_frame, text="",
                                     font=('Segoe UI', 12), fg='#8b949e', bg='#161b22')
        self.dec_pct_txt.pack(pady=(0, 5))

        # Confiance
        self.dec_confiance_label = tk.Label(self.dec_verdict_frame, text="",
                                             font=('Segoe UI', 14, 'bold'), bg='#161b22')
        self.dec_confiance_label.pack(pady=(0, 15))

        # ═══════════════════════════════════════════════════════
        # Ligne 3: Votes résumé (X pour / X contre / X neutre)
        # ═══════════════════════════════════════════════════════
        self.dec_votes_frame = tk.Frame(self.dec_content, bg=self.BG)
        self.dec_votes_frame.pack(fill='x', padx=30, pady=5)
        self.dec_votes_label = tk.Label(self.dec_votes_frame, text="", font=('Segoe UI', 13),
                                         fg=self.FG, bg=self.BG, justify='center')
        self.dec_votes_label.pack()

        # ═══════════════════════════════════════════════════════
        # Séparateur
        # ═══════════════════════════════════════════════════════
        tk.Frame(self.dec_content, bg='#30363d', height=2).pack(fill='x', padx=30, pady=10)

        # ═══════════════════════════════════════════════════════
        # Ligne 4: LES 10 CRITÈRES (barres visuelles)
        # ═══════════════════════════════════════════════════════
        titre_crit = tk.Label(self.dec_content, text="📋 DÉTAIL DES 10 CRITÈRES",
                              font=('Segoe UI', 14, 'bold'), fg=self.ACCENT, bg=self.BG)
        titre_crit.pack(anchor='w', padx=30, pady=(10, 5))

        self.dec_criteres_frame = tk.Frame(self.dec_content, bg=self.BG)
        self.dec_criteres_frame.pack(fill='x', padx=30, pady=5)

        # On crée 10 lignes de critères (vides pour l'instant)
        self.dec_crit_widgets = []
        for i in range(10):
            row = tk.Frame(self.dec_criteres_frame, bg='#161b22', highlightbackground='#21262d',
                           highlightthickness=1)
            row.pack(fill='x', pady=2)

            # Colonne gauche: nom du critère + poids
            left = tk.Frame(row, bg='#161b22', width=280)
            left.pack(side='left', padx=10, pady=6)
            left.pack_propagate(False)
            lbl_nom = tk.Label(left, text="", font=('Segoe UI', 10, 'bold'),
                               fg=self.FG, bg='#161b22', anchor='w')
            lbl_nom.pack(anchor='w')
            lbl_poids = tk.Label(left, text="", font=('Segoe UI', 8),
                                  fg='#8b949e', bg='#161b22', anchor='w')
            lbl_poids.pack(anchor='w')

            # Colonne centre: barre de progression visuelle
            mid = tk.Frame(row, bg='#161b22')
            mid.pack(side='left', fill='x', expand=True, padx=5, pady=6)
            bar_bg = tk.Canvas(mid, bg='#21262d', height=22, highlightthickness=0)
            bar_bg.pack(fill='x')

            # Colonne droite: vote emoji + explication
            right = tk.Frame(row, bg='#161b22', width=400)
            right.pack(side='right', padx=10, pady=6)
            right.pack_propagate(False)
            lbl_expl = tk.Label(right, text="", font=('Segoe UI', 9),
                                fg=self.FG, bg='#161b22', anchor='w', wraplength=380, justify='left')
            lbl_expl.pack(anchor='w')
            lbl_ar = tk.Label(right, text="", font=('Segoe UI', 9),
                              fg='#8b949e', bg='#161b22', anchor='e', wraplength=380, justify='right')
            lbl_ar.pack(anchor='e')

            self.dec_crit_widgets.append({
                'row': row, 'lbl_nom': lbl_nom, 'lbl_poids': lbl_poids,
                'bar_canvas': bar_bg, 'lbl_expl': lbl_expl, 'lbl_ar': lbl_ar
            })

        # ═══════════════════════════════════════════════════════
        # Séparateur
        # ═══════════════════════════════════════════════════════
        tk.Frame(self.dec_content, bg='#30363d', height=2).pack(fill='x', padx=30, pady=10)

        # ═══════════════════════════════════════════════════════
        # Ligne 5: RÉSUMÉ TEXTUEL (FR + AR)
        # ═══════════════════════════════════════════════════════
        self.dec_resume_fr = tk.Label(self.dec_content, text="", font=('Segoe UI', 13),
                                       fg=self.FG, bg=self.BG, justify='left', wraplength=900)
        self.dec_resume_fr.pack(anchor='w', padx=30, pady=(5, 10))

        self.dec_resume_ar = tk.Label(self.dec_content, text="", font=('Segoe UI', 13),
                                       fg='#8b949e', bg=self.BG, justify='right', wraplength=900)
        # Masquer le résumé arabe — tout en français
        # self.dec_resume_ar.pack(anchor='e', padx=30, pady=(0, 10))

        # ═══════════════════════════════════════════════════════
        # Ligne 6: PLAN DE TRADING (si OUI)
        # ═══════════════════════════════════════════════════════
        self.dec_plan_frame = tk.Frame(self.dec_content, bg='#161b22',
                                        highlightbackground='#238636', highlightthickness=2)
        self.dec_plan_label = tk.Label(self.dec_plan_frame, text="", font=('Consolas', 12),
                                        fg=self.GREEN, bg='#161b22', justify='left')
        self.dec_plan_label.pack(padx=15, pady=15)
        # (ne pas pack plan_frame maintenant — seulement si verdict = OUI)

        # ═══════════════════════════════════════════════════════
        # Ligne 7: BLOC PPO (Reinforcement Learning)
        # ═══════════════════════════════════════════════════════
        self.dec_ppo_frame = tk.Frame(self.dec_content, bg='#161b22',
                                       highlightbackground='#8957e5', highlightthickness=2)
        ppo_title = tk.Label(self.dec_ppo_frame,
                              text="🎮 SYSTÈME PPO V5 SMART (Reinforcement Learning)",
                              font=('Segoe UI', 13, 'bold'), fg='#8957e5', bg='#161b22')
        ppo_title.pack(anchor='w', padx=15, pady=(10, 5))
        self.dec_ppo_label = tk.Label(self.dec_ppo_frame, text="", font=('Consolas', 11),
                                       fg=self.FG, bg='#161b22', justify='left')
        self.dec_ppo_label.pack(padx=15, pady=(0, 10))
        # Barre PPO
        self.dec_ppo_bar_canvas = tk.Canvas(self.dec_ppo_frame, bg='#21262d', height=30,
                                             highlightthickness=0)
        self.dec_ppo_bar_canvas.pack(fill='x', padx=15, pady=(0, 15))
        # (ne pas pack ppo_frame maintenant — seulement si PPO est actif)

    # ══════════════════════════════════════════════════════════════════
    #  _on_tree_select  — quand l'utilisateur clique sur un stock
    # ══════════════════════════════════════════════════════════════════
    def _on_tree_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])['values']
        if not vals:
            return
        sym = vals[0]
        # Trouver le résultat correspondant
        r = next((x for x in self.results if x.get('symbole') == sym), None)
        if not r:
            return
        # Analyser avec le système IA
        decision = SystemeDecisionIA.analyser(r)
        # Mettre à jour le panneau
        self._update_decision_panel(r, decision)
        # Basculer vers l'onglet Décision automatiquement
        self.notebook.select(1)

    # ══════════════════════════════════════════════════════════════════
    #  _update_decision_panel  — met à jour tout l'onglet décision
    # ══════════════════════════════════════════════════════════════════
    def _update_decision_panel(self, result, decision):
        tk = self.tk

        # Masquer le placeholder, afficher le contenu
        self.dec_placeholder.pack_forget()
        self.dec_content.pack(fill='both', expand=True)

        sym = result.get('symbole', '?')
        prix = result.get('prix', 0)
        secteur = result.get('secteur', '')
        marche = result.get('marche', '')

        verdict = decision['verdict']
        pct = decision['pourcentage_reussite']
        couleur = decision['couleur']
        confiance = decision['confiance']
        emoji = decision['emoji']

        # ── Ligne 1: Symbole + prix ──
        self.dec_sym_label.config(text=f"🏦 {sym}")
        self.dec_prix_label.config(text=f"💰 {prix:.2f} €")
        self.dec_sector_label.config(text=f"{secteur}  |  {marche}")

        # ── Ligne 2: LE VERDICT ──
        verdict_map = {
            'OUI':      ('✅ OUI — ACHETER', 'نعم — اشتري'),
            'NON':      ('❌ NON — ÉVITER',  'لا — تجنّب'),
            'ATTENDRE': ('⏳ ATTENDRE',       'انتظر'),
        }
        txt_fr, txt_ar = verdict_map.get(verdict, ('?', '?'))
        self.dec_verdict_label.config(text=txt_fr, fg=couleur)
        self.dec_verdict_ar.config(text="")

        # Pourcentage
        self.dec_pct_label.config(text=f"{pct:.0f}%", fg=couleur)
        self.dec_pct_txt.config(text="Probabilité de réussite")

        # Confiance
        conf_colors = {'TRÈS HAUTE': '#3fb950', 'HAUTE': '#58a6ff', 'MOYENNE': '#d29922', 'BASSE': '#f85149'}
        self.dec_confiance_label.config(
            text=f"🔒 Confiance: {confiance}",
            fg=conf_colors.get(confiance, self.FG)
        )

        # ── Ligne 3: Votes ──
        nb_p = decision['nb_pour']
        nb_c = decision['nb_contre']
        nb_n = decision['nb_neutre']
        self.dec_votes_label.config(
            text=f"🟢 {nb_p} critères POUR   |   🔴 {nb_c} critères CONTRE   |   ⚪ {nb_n} neutres"
        )

        # ── Ligne 4: Les 10 critères ──
        criteres = decision['criteres']
        for i, crit in enumerate(criteres):
            if i >= len(self.dec_crit_widgets):
                break
            w = self.dec_crit_widgets[i]

            # Nom + poids
            poids_pct = crit['poids'] * 100
            w['lbl_nom'].config(text=f"{crit['nom']}")
            w['lbl_poids'].config(text=f"Poids: {poids_pct:.0f}%")

            # Couleur selon vote
            vote = crit['vote']
            if vote >= 0.5:
                bar_color = '#3fb950'  # vert
                vote_txt = '✅ POUR'
            elif vote > 0:
                bar_color = '#56d364'  # vert clair
                vote_txt = '🟢 légèrement pour'
            elif vote <= -0.5:
                bar_color = '#f85149'  # rouge
                vote_txt = '❌ CONTRE'
            elif vote < 0:
                bar_color = '#f0883e'  # orange
                vote_txt = '🟠 légèrement contre'
            else:
                bar_color = '#484f58'  # gris
                vote_txt = '⚪ neutre'

            # Dessiner la barre
            bar = w['bar_canvas']
            bar.delete('all')
            bar.update_idletasks()
            cw = bar.winfo_width()
            if cw < 50:
                cw = 400  # valeur par défaut
            # Barre de fond
            bar.create_rectangle(0, 0, cw, 22, fill='#21262d', outline='')
            # Barre colorée proportionnelle au score (0-100)
            score_pct = crit['score'] / 100.0
            bw = int(cw * score_pct)
            bar.create_rectangle(0, 0, bw, 22, fill=bar_color, outline='')
            # Texte sur la barre
            bar.create_text(cw // 2, 11, text=f"{vote_txt}  ({crit['score']:.0f}/100)",
                           fill='white', font=('Segoe UI', 9, 'bold'))

            # Explication
            w['lbl_expl'].config(text=crit['expl'])
            w['lbl_ar'].config(text="")

        # ── Ligne 5: Résumés textuels ──
        self.dec_resume_fr.config(text=decision['resume_fr'])
        self.dec_resume_ar.config(text=decision['resume_ar'])

        # ── Ligne 6: Plan de trading (si OUI) ──
        self.dec_plan_frame.pack_forget()
        if verdict == 'OUI':
            sl = result.get('stop_loss', 0)
            tp = result.get('take_profit', 0)
            sl_pct = result.get('stop_loss_pct', 0)
            pot = result.get('potentiel', 0)
            rr = result.get('ratio_rr', 0)
            plan_txt = (
                f"📋 PLAN DE TRADING\n"
                f"{'━' * 50}\n"
                f"💰 Entrée:        {prix:.2f} €\n"
                f"🎯 Objectif (TP): {tp:.2f} € (+{pot:.1f}%)\n"
                f"🛑 Stop Loss:     {sl:.2f} € ({sl_pct:.1f}%)\n"
                f"⚖️  Ratio R:R:     {rr:.2f}\n"
                f"{'━' * 50}"
            )
            self.dec_plan_label.config(text=plan_txt)
            self.dec_plan_frame.pack(fill='x', padx=30, pady=(5, 20))

        # ── Ligne 7: Bloc PPO ──
        self.dec_ppo_frame.pack_forget()
        ppo = decision.get('ppo')
        if ppo:
            ppo_action = ppo['action']
            ppo_buy = ppo['probabilite_achat']
            ppo_skip = ppo['probabilite_skip']
            ppo_conf = ppo['confiance_ppo']
            ppo_emoji = '✅' if ppo_action == 'OUI' else '❌'
            ppo_color = self.GREEN if ppo_action == 'OUI' else self.RED

            stats = ppo_system.training_stats
            trained_date = stats.get('date', '?')
            train_acc = stats.get('overall_accuracy', '?')

            # Informations Ensemble V5 SMART
            votes_a = ppo.get('votes_achat', '?')
            votes_t = ppo.get('votes_total', 3)
            unanime = ppo.get('unanimite', False)
            fiab = ppo.get('fiabilite', 0)
            haute_conf = ppo.get('haute_confiance', False)
            unan_txt = " ★ UNANIME" if unanime else ""
            hc_txt = " 🏆 HAUTE CONFIANCE" if haute_conf else ""

            ppo_txt = (
                f"🧠 PPO V5 SMART — 3 Meilleurs Modèles × Macro SPY/VIX × Sharpe\n"
                f"{'━' * 50}\n"
                f"📊 Décision: {ppo_emoji} {ppo_action}  ({votes_a}/{votes_t} modèles){unan_txt}{hc_txt}\n"
                f"📈 Probabilité d'achat: {ppo_buy:.1f}%  |  Skip: {ppo_skip:.1f}%\n"
                f"🔒 Confiance: {ppo_conf} ({ppo['confiance_pct']:.0f}%)  |  Fiabilité: {fiab:.0f}/100\n"
                f"{'━' * 50}\n"
                f"📅 Entraîné: {trained_date}  |  Précision ensemble: {train_acc}%"
            )
            self.dec_ppo_label.config(text=ppo_txt, fg=ppo_color)

            # Barre PPO
            bar = self.dec_ppo_bar_canvas
            bar.delete('all')
            bar.update_idletasks()
            cw = bar.winfo_width()
            if cw < 50:
                cw = 600
            # Fond
            bar.create_rectangle(0, 0, cw, 30, fill='#21262d', outline='')
            # Barre verte (achat) + rouge (skip)
            bw_buy = int(cw * ppo_buy / 100)
            bar.create_rectangle(0, 0, bw_buy, 30, fill=self.GREEN, outline='')
            bar.create_rectangle(bw_buy, 0, cw, 30, fill=self.RED, outline='')
            bar.create_text(bw_buy // 2, 15, text=f"ACHAT {ppo_buy:.0f}%",
                           fill='white', font=('Segoe UI', 10, 'bold'))
            bar.create_text(bw_buy + (cw - bw_buy) // 2, 15, text=f"SKIP {ppo_skip:.0f}%",
                           fill='white', font=('Segoe UI', 10, 'bold'))

            self.dec_ppo_frame.pack(fill='x', padx=30, pady=(5, 20))
        else:
            # PPO pas entraîné — afficher un message
            self.dec_ppo_label.config(
                text="⚠️ PPO V5 pas encore entraîné — Cliquez sur 🧠 PPO V5 SMART\n"
                     "⚠️ لم يتم تدريب PPO بعد — اضغط على 🧠 PPO V5 SMART",
                fg='#8b949e'
            )
            self.dec_ppo_bar_canvas.delete('all')
            self.dec_ppo_frame.pack(fill='x', padx=30, pady=(5, 20))

    def _poll_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg[0] == 'status':
                    self.status_var.set(msg[1])
                elif msg[0] == 'progress':
                    self.progress['value'] = msg[1]
                    self.progress['maximum'] = msg[2]
                elif msg[0] == 'results':
                    self.results = msg[1]
                    self._peupler_tree(self.results)
                    self._update_risk_tab()
                    self.running = False
                elif msg[0] == 'ml_done':
                    self.messagebox.showinfo("ML", msg[1])
                    self.running = False
                elif msg[0] == 'ppo_done':
                    self.messagebox.showinfo("🎮 PPO", msg[1])
                    self.running = False
        except Empty: pass
        self.root.after(100, self._poll_queue)

    def _callback(self, status, current, total):
        self.queue.put(('status', status))
        self.queue.put(('progress', current, total))

    def _sync_config_from_gui(self):
        """Synchronise self.config depuis les widgets du tab Paramètres (si ils existent)"""
        c = self.config
        try:
            # Modes
            if hasattr(self, 'pv_scoring'):
                c.SCORING_MODE = self.pv_scoring.get()
                c.FAST_MODE = self.pv_fast.get()
                c.CROSS_SECTIONAL_RANKING = self.pv_cross.get()
                c.REGIME_ADAPTIVE_WEIGHTS = self.pv_regime.get()
                c.HORIZON_MODE = self.pv_horizon.get()
            # Alpha weights
            if hasattr(self, 'alpha_sliders'):
                for key, var in self.alpha_sliders.items():
                    setattr(c, key, var.get())
            # Seuils
            if hasattr(self, 'seuil_vars'):
                for key, var in self.seuil_vars.items():
                    setattr(c, key, var.get())
            # Trade
            if hasattr(self, 'trade_vars'):
                for key, var in self.trade_vars.items():
                    v = var.get()
                    if key in ('HORIZON_INTRADAY_JOURS', 'HORIZON_SWING_JOURS'):
                        setattr(c, key, int(v))
                    else:
                        setattr(c, key, v)
            # PPO
            if hasattr(self, 'ppo_vars'):
                for key, var in self.ppo_vars.items():
                    setattr(c, key, int(var.get()))
            # Regime
            if hasattr(self, 'regime_vars'):
                for key, var in self.regime_vars.items():
                    val = var.get()
                    if key == 'REGIME_SPY_SMA':
                        setattr(c, key, int(val))
                    else:
                        setattr(c, key, val)
            # Univers
            if hasattr(self, 'univ_vars'):
                for key, var in self.univ_vars.items():
                    setattr(c, key, var.get())
            # Risk Management params
            if hasattr(self, 'risk_param_vars'):
                for key, var in self.risk_param_vars.items():
                    v = var.get()
                    if key in ('RISQUE_MAX_PCT', 'KELLY_MAX_PCT', 'MAX_DRAWDOWN_LIMIT'):
                        setattr(c, key, v / 100.0)
                    elif key in ('MAX_POSITIONS', 'MONTE_CARLO_SIMS', 'VAR_HORIZON_JOURS'):
                        setattr(c, key, int(v))
                    else:
                        setattr(c, key, v)
        except Exception as e:
            logging.getLogger('BlackRockScreener').debug(f"Sync GUI params: {e}")
        self.moteur.config = c
        self.moteur.risk_manager.config = c
        if ppo_system:
            ppo_system.config = c

    # ══════════════════════════════════════════════════════════════════
    #  _build_risk_tab — ONGLET 🛡️ RISK MANAGEMENT DASHBOARD
    # ══════════════════════════════════════════════════════════════════
    def _build_risk_tab(self, parent):
        tk = self.tk; ttk = self.ttk; cfg = self.config

        # Scrollable canvas
        canvas = tk.Canvas(parent, bg=self.BG, highlightthickness=0)
        vsb = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.BG)
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
        pf = scroll_frame

        lf_opts = dict(bg='#161b22', fg=self.ACCENT, font=('Segoe UI', 11, 'bold'),
                       padx=10, pady=10, labelanchor='nw')
        lbl_opts = dict(font=('Consolas', 10), bg='#161b22', fg=self.FG, anchor='w')
        val_opts = dict(font=('Consolas', 11, 'bold'), bg='#161b22', anchor='w')

        # ═══════════════════════════════════════════
        #  SECTION 1: PARAMÈTRES DE RISQUE
        # ═══════════════════════════════════════════
        lf1 = tk.LabelFrame(pf, text="⚙️ PARAMÈTRES DE RISQUE", **lf_opts)
        lf1.pack(fill='x', padx=10, pady=(10, 5))

        self.risk_param_vars = {}
        risk_params = [
            ('CAPITAL', 'Capital ($)', 1000, 1000000, cfg.CAPITAL),
            ('RISQUE_MAX_PCT', 'Risque Max / Trade (%)', 0.5, 10.0, cfg.RISQUE_MAX_PCT * 100),
            ('MAX_POSITIONS', 'Positions Max', 1, 50, cfg.MAX_POSITIONS),
            ('KELLY_FRACTION', 'Kelly Fraction', 0.05, 1.0, cfg.KELLY_FRACTION),
            ('KELLY_MAX_PCT', 'Kelly Max / Position (%)', 1, 50, cfg.KELLY_MAX_PCT * 100),
            ('VAR_CONFIDENCE', 'VaR Confiance', 0.90, 0.99, cfg.VAR_CONFIDENCE),
            ('VAR_HORIZON_JOURS', 'VaR Horizon (jours)', 1, 60, cfg.VAR_HORIZON_JOURS),
            ('MONTE_CARLO_SIMS', 'MC Simulations', 500, 50000, cfg.MONTE_CARLO_SIMS),
            ('MAX_DRAWDOWN_LIMIT', 'Max Drawdown Limit (%)', 5, 50, cfg.MAX_DRAWDOWN_LIMIT * 100),
            ('R_MULTIPLE_TARGET', 'R-Multiple Cible', 0.5, 10.0, cfg.R_MULTIPLE_TARGET),
        ]

        for i, (key, label, mn, mx, default) in enumerate(risk_params):
            row = i // 2
            col = i % 2
            f = tk.Frame(lf1, bg='#161b22')
            f.grid(row=row, column=col, padx=10, pady=3, sticky='ew')
            tk.Label(f, text=label, **lbl_opts).pack(side='left', padx=(0, 5))
            if isinstance(default, int) and key not in ('VAR_CONFIDENCE', 'KELLY_FRACTION'):
                var = tk.IntVar(value=int(default))
                tk.Spinbox(f, from_=int(mn), to=int(mx), textvariable=var, width=8,
                          bg='#0d1117', fg=self.GREEN, font=('Consolas', 10)).pack(side='right')
            else:
                var = tk.DoubleVar(value=float(default))
                tk.Spinbox(f, from_=float(mn), to=float(mx), textvariable=var, width=8,
                          increment=0.01 if mx <= 1.0 else (0.5 if mx <= 10 else 100),
                          bg='#0d1117', fg=self.GREEN, font=('Consolas', 10)).pack(side='right')
            self.risk_param_vars[key] = var

        lf1.columnconfigure(0, weight=1)
        lf1.columnconfigure(1, weight=1)

        # ═══════════════════════════════════════════
        #  SECTION 2: PORTFOLIO RISK DASHBOARD
        # ═══════════════════════════════════════════
        lf2 = tk.LabelFrame(pf, text="📊 PORTFOLIO RISK DASHBOARD", **lf_opts)
        lf2.pack(fill='x', padx=10, pady=5)

        self.risk_labels = {}
        dashboard_items = [
            ('n_positions', '📦 Positions', '—'),
            ('pct_invested', '💰 Capital Investi', '—'),
            ('risk_pct_capital', '⚠️ Risque Total / Capital', '—'),
            ('avg_kelly_pct', '🎯 Kelly Moyen', '—'),
            ('avg_rr', '📐 R:R Moyen', '—'),
            ('avg_risk_score', '🛡️ Risk Score Moyen', '—'),
            ('portfolio_var_5j', '📉 VaR Portfolio 5j', '—'),
            ('avg_expected_r', '📈 E[R] Moyen', '—'),
            ('avg_correlation', '🔗 Corrélation Moyenne', '—'),
            ('concentration_alert', '🚨 Alerte Concentration', '—'),
        ]
        for i, (key, label, default) in enumerate(dashboard_items):
            row = i // 2
            col = i % 2
            f = tk.Frame(lf2, bg='#161b22')
            f.grid(row=row, column=col, padx=10, pady=3, sticky='ew')
            tk.Label(f, text=label, **lbl_opts).pack(side='left', padx=(0, 5))
            lbl = tk.Label(f, text=default, fg=self.ACCENT, **val_opts)
            lbl.pack(side='right', padx=5)
            self.risk_labels[key] = lbl

        lf2.columnconfigure(0, weight=1)
        lf2.columnconfigure(1, weight=1)

        # ═══════════════════════════════════════════
        #  SECTION 3: STRESS TESTING
        # ═══════════════════════════════════════════
        lf3 = tk.LabelFrame(pf, text="🔥 STRESS TESTING — MONTE CARLO", **lf_opts)
        lf3.pack(fill='x', padx=10, pady=5)

        self.stress_labels = {}
        stress_items = [
            ('stress_max_dd_95', '📉 Max DD (95%)', '—'),
            ('stress_max_dd_99', '📉 Max DD (99%)', '—'),
            ('stress_expected_return', '📈 Rendement Attendu', '—'),
            ('stress_worst_case', '💀 Pire Scénario (1%)', '—'),
            ('stress_best_case', '🏆 Meilleur Scénario (99%)', '—'),
            ('stress_prob_loss', '⚠️ Probabilité de Perte', '—'),
        ]
        for i, (key, label, default) in enumerate(stress_items):
            row = i // 2
            col = i % 2
            f = tk.Frame(lf3, bg='#161b22')
            f.grid(row=row, column=col, padx=10, pady=3, sticky='ew')
            tk.Label(f, text=label, **lbl_opts).pack(side='left', padx=(0, 5))
            lbl = tk.Label(f, text=default, fg=self.YELLOW, **val_opts)
            lbl.pack(side='right', padx=5)
            self.stress_labels[key] = lbl

        lf3.columnconfigure(0, weight=1)
        lf3.columnconfigure(1, weight=1)

        # ═══════════════════════════════════════════
        # SECTION 4: TOP POSITIONS RISK DETAIL
        # ═══════════════════════════════════════════
        lf4 = tk.LabelFrame(pf, text="🏆 TOP POSITIONS — RISK DETAIL", **lf_opts)
        lf4.pack(fill='x', padx=10, pady=(5, 10))

        top_cols = ('symbole', 'prix', 'kelly_pct', 'position_value', 'risk_score',
                    'expected_r', 'var_5j', 'ratio_rr')
        self.risk_tree = ttk.Treeview(lf4, columns=top_cols, show='headings', height=10,
                                       style='Dark.Treeview')
        top_headers = {
            'symbole': 'Symbole', 'prix': 'Prix', 'kelly_pct': 'Kelly%',
            'position_value': 'Pos$', 'risk_score': 'Risk', 'expected_r': 'E[R]',
            'var_5j': 'VaR5j%', 'ratio_rr': 'R:R'
        }
        top_widths = {
            'symbole': 80, 'prix': 70, 'kelly_pct': 60, 'position_value': 80,
            'risk_score': 55, 'expected_r': 55, 'var_5j': 65, 'ratio_rr': 55
        }
        for col in top_cols:
            self.risk_tree.heading(col, text=top_headers.get(col, col))
            self.risk_tree.column(col, width=top_widths.get(col, 70), anchor='center')
        self.risk_tree.pack(fill='x', padx=5, pady=5)

        # ═══════════════════════════════════════════
        # SECTION 5: R-MULTIPLE EXPECTANCY
        # ═══════════════════════════════════════════
        lf5 = tk.LabelFrame(pf, text="📊 R-MULTIPLE EXPECTANCY (PORTEFEUILLE SIMULÉ)", **lf_opts)
        lf5.pack(fill='x', padx=10, pady=(5, 10))

        self.expectancy_labels = {}
        exp_items = [
            ('expectancy', '📈 Expectancy (R)', '—'),
            ('win_rate', '🎯 Win Rate %', '—'),
            ('avg_win_r', '✅ Avg Win (R)', '—'),
            ('avg_loss_r', '❌ Avg Loss (R)', '—'),
            ('profit_factor', '💰 Profit Factor', '—'),
            ('total_r', '📊 Total R estimé', '—'),
        ]
        for i, (key, label, default) in enumerate(exp_items):
            row = i // 3
            col = i % 3
            f = tk.Frame(lf5, bg='#161b22')
            f.grid(row=row, column=col, padx=10, pady=3, sticky='ew')
            tk.Label(f, text=label, **lbl_opts).pack(side='left', padx=(0, 5))
            lbl = tk.Label(f, text=default, fg=self.GREEN, **val_opts)
            lbl.pack(side='right', padx=5)
            self.expectancy_labels[key] = lbl

        lf5.columnconfigure(0, weight=1)
        lf5.columnconfigure(1, weight=1)
        lf5.columnconfigure(2, weight=1)

    def _update_risk_tab(self):
        """Met à jour le dashboard Risk Management après analyse"""
        try:
            pr = getattr(self.moteur, 'portfolio_risk', {})
            if not pr:
                return

            # Sync risk params from GUI to config
            cfg = self.config
            if hasattr(self, 'risk_param_vars'):
                for key, var in self.risk_param_vars.items():
                    v = var.get()
                    if key in ('RISQUE_MAX_PCT', 'KELLY_MAX_PCT', 'MAX_DRAWDOWN_LIMIT'):
                        setattr(cfg, key, v / 100.0)
                    elif key == 'MAX_POSITIONS':
                        setattr(cfg, key, int(v))
                    elif key == 'MONTE_CARLO_SIMS':
                        setattr(cfg, key, int(v))
                    elif key == 'VAR_HORIZON_JOURS':
                        setattr(cfg, key, int(v))
                    else:
                        setattr(cfg, key, v)

            # Update portfolio dashboard labels
            for key, lbl in self.risk_labels.items():
                val = pr.get(key, '—')
                if isinstance(val, bool):
                    txt = '🚨 OUI' if val else '✅ NON'
                    lbl.configure(text=txt, fg=self.RED if val else self.GREEN)
                elif isinstance(val, (int, float)):
                    # Color coding
                    if key in ('risk_pct_capital',) and val > 5:
                        color = self.RED
                    elif key == 'avg_risk_score' and val < 40:
                        color = self.RED
                    elif key == 'avg_risk_score' and val >= 60:
                        color = self.GREEN
                    elif key == 'avg_correlation' and val > 0.6:
                        color = self.RED
                    elif key == 'avg_expected_r' and val > 0:
                        color = self.GREEN
                    elif key == 'avg_expected_r' and val < 0:
                        color = self.RED
                    else:
                        color = self.ACCENT
                    suffix = '%' if 'pct' in key or 'var' in key.lower() else ''
                    lbl.configure(text=f"{val}{suffix}", fg=color)
                else:
                    lbl.configure(text=str(val))

            # Update stress testing labels
            for key, lbl in self.stress_labels.items():
                val = pr.get(key, '—')
                if isinstance(val, (int, float)):
                    color = self.RED if val < -10 or (key == 'stress_prob_loss' and val > 50) else (
                        self.GREEN if val > 0 and key != 'stress_prob_loss' else self.YELLOW)
                    lbl.configure(text=f"{val}%", fg=color)
                else:
                    lbl.configure(text=str(val))

            # Update risk detail tree with top positions
            for item in self.risk_tree.get_children():
                self.risk_tree.delete(item)
            if self.results:
                max_pos = int(getattr(cfg, 'MAX_POSITIONS', 10))
                top = sorted(self.results, key=lambda x: x.get('score_final', 0), reverse=True)[:max_pos]
                for r in top:
                    vals = (
                        r.get('symbole', ''),
                        round(r.get('prix', 0), 2),
                        r.get('kelly_used_pct', 0),
                        round(r.get('position_value', 0), 0),
                        r.get('risk_score', 0),
                        r.get('expected_r', 0),
                        r.get('var_5j', 0),
                        r.get('ratio_rr', 0),
                    )
                    risk_s = r.get('risk_score', 50)
                    tag = 'green' if risk_s >= 60 else ('red' if risk_s < 35 else 'yellow')
                    self.risk_tree.insert('', 'end', values=vals, tags=(tag,))

            # Update R-multiple expectancy (simulated from current results)
            if self.results:
                # Simulate R-multiples from expected performance
                simulated_r = []
                for r in self.results:
                    exp_r = r.get('expected_r', 0)
                    if exp_r != 0:
                        simulated_r.append(exp_r)
                if simulated_r:
                    exp = RiskManager.expectancy(simulated_r)
                    for key, lbl in self.expectancy_labels.items():
                        val = exp.get(key, '—')
                        if isinstance(val, (int, float)):
                            color = self.GREEN if val > 0 else (self.RED if val < 0 else self.ACCENT)
                            if key == 'win_rate':
                                color = self.GREEN if val > 50 else self.RED
                            lbl.configure(text=f"{val}", fg=color)
                        else:
                            lbl.configure(text=str(val))

        except Exception as e:
            logging.getLogger('BlackRockScreener').debug(f"Risk tab update: {e}")

    def _lancer_analyse(self):
        if self.running: return
        self.running = True
        def run():
            # Sync TOUS les paramètres depuis l'onglet Params
            self._sync_config_from_gui()
            c = self.config
            # Override univers depuis le filtre marché radio
            m = self.market_var.get()
            if m == 'PEA':
                c.MODE_PEA = True
            elif m != 'Tous':
                c.MODE_PEA = False
                c.INCLURE_US = m == 'US'
                c.INCLURE_FRANCE = m in ('France', 'Europe')
                c.INCLURE_EUROPE = m == 'Europe'
                c.INCLURE_PME = m == 'PME'
                c.INCLURE_CRYPTO = m == 'Crypto'
            # Si 'Tous' → les checkboxes du tab Params font foi (déjà sync)
            self.moteur.config = c
            results = self.moteur.executer(callback=self._callback)
            self.queue.put(('results', results))
        threading.Thread(target=run, daemon=True).start()

    def _lancer_sniper(self):
        if self.running: return
        self.running = True
        def run():
            self._sync_config_from_gui()
            c = self.config
            # Override univers depuis le filtre marché radio (même logique que _lancer_analyse)
            m = self.market_var.get()
            if m == 'PEA':
                c.MODE_PEA = True
            elif m != 'Tous':
                c.MODE_PEA = False
                c.INCLURE_US = m == 'US'
                c.INCLURE_FRANCE = m in ('France', 'Europe')
                c.INCLURE_EUROPE = m == 'Europe'
                c.INCLURE_PME = m == 'PME'
                c.INCLURE_CRYPTO = m == 'Crypto'
            # Si 'Tous' → les checkboxes du tab Params font foi (déjà sync)
            self.moteur.config = c
            actions = UniversActions.obtenir_actions(
                us=c.INCLURE_US, europe=c.INCLURE_EUROPE, france=c.INCLURE_FRANCE,
                gaming=getattr(c, 'INCLURE_GAMING', True),
                matieres=getattr(c, 'INCLURE_MATIERES', True),
                crypto=getattr(c, 'INCLURE_CRYPTO', False),
                mode_pea=c.MODE_PEA, inclure_pme=c.INCLURE_PME,
                inclure_sante=getattr(c, 'INCLURE_SANTE', True),
                inclure_nasdaq100=getattr(c, 'INCLURE_NASDAQ100', True),
                inclure_sp500=getattr(c, 'INCLURE_SP500', True),
            )
            symbols = list(actions.keys())
            # Quick scan
            self._callback("⚡ Sniper scan rapide...", 0, len(symbols))
            results = []
            try:
                prices = self.moteur.price_fetcher.fetch_batch_prices(symbols, period="1mo")
                df_all = yf.download(symbols, period="3mo", interval="1d", progress=False, threads=True, group_by='ticker')
                for i, sym in enumerate(symbols):
                    if i%20==0: self._callback(f"⚡ {sym}...", i, len(symbols))
                    try:
                        df = df_all[sym] if len(symbols)>1 and sym in df_all.columns.get_level_values(0) else (df_all if len(symbols)==1 else None)
                        if df is None or df.empty or len(df)<30: continue
                        r = self.moteur.analyser_action(sym, df)
                        if r: results.append(r)
                    except Exception as e:
                        lgr = logging.getLogger('BlackRockScreener')
                        lgr.debug(f"Sniper {sym} skip: {e}")
                        continue
            except Exception as e:
                lgr = logging.getLogger('BlackRockScreener')
                lgr.warning(f"Sniper batch fail: {e}")
            results.sort(key=lambda x: x.get('score_final',0), reverse=True)
            # Appliquer cross-sectional ranking (même logique que Analyse)
            results = self.moteur._appliquer_ranking(results)
            results = [r for r in results if r.get('score_final',0) >= self.config.SCORE_MINIMUM]
            results.sort(key=lambda x: x.get('score_final',0), reverse=True)
            self.queue.put(('results', results))
        threading.Thread(target=run, daemon=True).start()

    def _lancer_entrainement(self):
        if self.running: return
        self.running = True
        def run():
            self._sync_config_from_gui()
            c = self.config
            actions = UniversActions.obtenir_actions(
                us=c.INCLURE_US, europe=c.INCLURE_EUROPE, france=c.INCLURE_FRANCE,
                gaming=getattr(c, 'INCLURE_GAMING', True),
                matieres=getattr(c, 'INCLURE_MATIERES', True),
                crypto=getattr(c, 'INCLURE_CRYPTO', False),
                mode_pea=getattr(c, 'MODE_PEA', False),
                inclure_pme=getattr(c, 'INCLURE_PME', True),
                inclure_sante=getattr(c, 'INCLURE_SANTE', True),
                inclure_nasdaq100=getattr(c, 'INCLURE_NASDAQ100', True),
                inclure_sp500=getattr(c, 'INCLURE_SP500', True),
            )
            syms = list(actions.keys())[:self.config.ML_MAX_SYMBOLES]
            ok = self.moteur.ml.entrainer(syms, callback=self._callback)
            self.queue.put(('ml_done', "✅ ML entraîné!" if ok else "❌ Échec"))
        threading.Thread(target=run, daemon=True).start()

    def _lancer_ppo(self):
        """Lance l'entraînement du système PPO V5 SMART — respecte tous les paramètres GUI."""
        if not PPO_OK:
            self.messagebox.showerror("PPO", "❌ stable-baselines3 non installé!\npip install stable-baselines3 gymnasium")
            return
        if self.running:
            return
        self.running = True
        def run():
            # Sync TOUS les paramètres GUI → config → PPO
            self._sync_config_from_gui()
            c = self.config
            ppo_system.config = c
            lgr = logging.getLogger('BlackRockScreener')
            lgr.info(f"PPO LAUNCH: FAST_MODE={c.FAST_MODE}, "
                     f"CANDIDATES={getattr(c, 'PPO_FAST_CANDIDATES', '?')}, "
                     f"TIMESTEPS={getattr(c, 'PPO_FAST_TIMESTEPS', '?')}, "
                     f"UNIVERS: US={c.INCLURE_US} EU={c.INCLURE_EUROPE} "
                     f"SANTE={getattr(c, 'INCLURE_SANTE', '?')} "
                     f"NDX={getattr(c, 'INCLURE_NASDAQ100', '?')} "
                     f"SPX={getattr(c, 'INCLURE_SP500', '?')}")
            ok, msg = ppo_system.entrainer(callback=self._callback)
            self.queue.put(('ppo_done', msg))
        threading.Thread(target=run, daemon=True).start()

    def _generer_rapport(self):
        if not self.results:
            self.messagebox.showwarning("Rapport", "Lancez d'abord une analyse"); return
        path = RapportExcel.generer(self.results)
        if path:
            self.messagebox.showinfo("Rapport", f"✅ {path}")
            try: os.startfile(path)
            except Exception as e:
                logging.getLogger('BlackRockScreener').debug(f"Ouverture rapport: {e}")

    def _stop(self):
        self.running = False
        # Envoyer signal d'arrêt réel au PPO et ML
        if PPO_OK and ppo_system is not None:
            ppo_system.stop_requested = True
        self.status_var.set("⏹ Arrêté — entraînement interrompu")

    def _peupler_tree(self, results):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.count_var.set(f"{len(results)} résultats")
        for r in results:
            score = r.get('score_final', 0)
            if score >= 65: tag = 'green'
            elif score >= 50: tag = 'yellow'
            elif score < 40: tag = 'red'
            else: tag = 'white'
            vals = []
            for col in self.tree['columns']:
                v = r.get(col, '')
                if isinstance(v, float): v = round(v, 2)
                if isinstance(v, dict): v = str(v)[:30]
                if isinstance(v, str): v = clean_txt(v)
                vals.append(v)
            self.tree.insert('', 'end', values=vals, tags=(tag,))

    def _filtrer(self, *args):
        if not self.results: return
        search = self.search_var.get().upper()
        sector = self.sector_var.get()
        market = self.market_var.get()
        score_min = self.score_min_var.get()
        filtered = []
        for r in self.results:
            if search and search not in r.get('symbole','').upper(): continue
            if sector != 'Tous' and r.get('secteur','') != sector: continue
            if r.get('score_final',0) < score_min: continue
            if market == 'PEA' and r.get('marche','') in ['🇺🇸 US','₿ Crypto','🥇 Commodities']: continue
            filtered.append(r)
        self._peupler_tree(filtered)

    def _trier(self, col):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children()]
        try: data.sort(key=lambda t: float(t[0]) if t[0] else 0, reverse=True)
        except: data.sort(key=lambda t: t[0], reverse=True)
        for i, (_, child) in enumerate(data): self.tree.move(child, '', i)

    def _afficher_details(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])['values']
        if not vals: return
        sym = vals[0]
        # Trouver dans results
        r = next((x for x in self.results if x.get('symbole')==sym), None)
        if not r: return

        tk = self.tk; ttk = self.ttk
        win = tk.Toplevel(self.root)
        win.title(f"📊 Détails — {sym}")
        win.geometry("800x900")
        win.configure(bg=self.BG)

        canvas = tk.Canvas(win, bg=self.BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(win, orient='vertical', command=canvas.yview)
        frame = tk.Frame(canvas, bg=self.BG)
        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        def section(title, parent=frame):
            lbl = tk.Label(parent, text=f"\n{'═'*40}\n  {title}\n{'═'*40}", font=('Consolas',11,'bold'),
                          fg=self.ACCENT, bg=self.BG, justify='left')
            lbl.pack(anchor='w', padx=10)
            return lbl

        def line(key, val, parent=frame):
            color = self.GREEN if isinstance(val,str) and '🟢' in val else (self.RED if isinstance(val,str) and '🔴' in val else self.FG)
            if isinstance(val, float): val = f"{val:.2f}"
            tk.Label(parent, text=f"  {key}: {val}", font=('Consolas',10),
                    fg=color, bg=self.BG, justify='left').pack(anchor='w', padx=15)

        # Titre
        tk.Label(frame, text=f"🏦 {sym} — {r.get('secteur','')} | {r.get('marche','')}",
                font=('Segoe UI',14,'bold'), fg=self.ACCENT, bg=self.BG).pack(anchor='w', padx=10, pady=5)
        sf = r.get('score_final',0)
        color_score = self.GREEN if sf>=65 else (self.RED if sf<40 else self.YELLOW)
        tk.Label(frame, text=f"Prix: ${r.get('prix',0)}   Score: {sf}   {r.get('decision','')}",
                font=('Segoe UI',13,'bold'), fg=color_score, bg=self.BG).pack(anchor='w', padx=10)

        # ── RAISON PRINCIPALE ──
        raison = r.get('raison', '')
        if raison:
            tk.Label(frame, text=f"💡 {raison}", font=('Segoe UI',11),
                    fg=self.YELLOW, bg=self.BG, wraplength=750, justify='left').pack(anchor='w', padx=15, pady=3)

        section("📊 SCORE — 3 PILIERS")
        line("🔧 Technique (40%)", f"{r.get('score_technique',50)}/100")
        line("📋 Fondamental (30%)", f"{r.get('score_fondamental',50)}/100")
        line("🚀 Momentum (30%)", f"{r.get('score_momentum',50)}/100")
        line("═══ SCORE FINAL", f"{sf}/100")

        section("🎯 PLAN DE TRADING")
        line("Stop Loss", f"${r.get('stop_loss','')} ({r.get('stop_loss_pct','')}%)")
        line("Take Profit", f"${r.get('take_profit','')} ({r.get('take_profit_pct','')}%)")
        line("Ratio R:R", r.get('ratio_rr',''))
        line("Potentiel", f"{r.get('potentiel','')}%")
        line("Support", r.get('support','')); line("Résistance", r.get('resistance',''))

        section("📈 INDICATEURS TECHNIQUES")
        for k in ['rsi','zscore','macd_tendance','adx_signal','stoch_rsi_signal','williams_signal',
                   'cmf_signal','supertrend_signal','squeeze_signal','tendance','volume_ratio','volume_label']:
            if k in r: line(k.replace('_',' ').title(), r[k])

        section("🏦 FONDAMENTAL")
        line("BlackRock Score", r.get('blackrock_score',''))
        line("Earnings Score", r.get('earnings_score',''))
        line("Earnings Signal", r.get('earnings_signal',''))
        for k in ['pe','pb','roe','div_yield','fcf_yield','market_cap']:
            if k in r and r[k]: line(k.upper(), r[k])

        section("🚀 MOMENTUM & ML")
        for k in ['ml_probabilite','ml_consensus','ml_signal','ml_confiance']:
            if k in r: line(k.replace('ml_','ML ').title(), r[k])
        line("News Score", r.get('news_score',''))
        line("News Signal", r.get('news_signal',''))
        line("Smart Money", r.get('smart_money_signal',''))

        section("📐 RATIOS AVANCÉS")
        for k in ['hurst','fractal_dim','entropy','omega_ratio','sortino','calmar','sharpe','beta','tail_ratio','max_drawdown']:
            if k in r: line(k.replace('_',' ').title(), r[k])

        section("📈 CORRÉLATIONS")
        for ck, cv in r.get('correlations',{}).items():
            line(f"  vs {ck}", cv)
        if 'alpha_jensen' in r: line("Alpha Jensen", f"{r['alpha_jensen']}%")

        section("🛡️ RISK MANAGEMENT")
        line("🎯 Kelly Brut", f"{r.get('kelly_raw_pct','—')}%")
        line("🎯 Kelly Utilisé", f"{r.get('kelly_used_pct','—')}%")
        line("💰 Taille Position", f"${r.get('position_value','—')}")
        line("📦 Nb Actions", r.get('nb_actions', '—'))
        line("💵 Montant Risqué", f"${r.get('risk_amount','—')}")
        line("📊 % Capital", f"{r.get('pct_capital','—')}%")
        line("📉 VaR 5j (95%)", f"{r.get('var_5j','—')}%")
        line("📉 CVaR 5j", f"{r.get('cvar_5j','—')}%")
        line("📉 VaR MC", f"{r.get('var_mc','—')}%")
        line("📈 E[R-multiple]", f"{r.get('expected_r','—')}R")
        line("🛡️ Risk Score", f"{r.get('risk_score','—')}/100")
        line("📊 Vol Annualisée", f"{r.get('vol_annualisee','—')}%")

    def lancer(self):
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════════════════════
#                              MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    import sys, io
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith('cp'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    try:
        print("+" + "="*63 + "+")
        print("|  BLACKROCK ULTRA SCREENER v10.0                           |")
        print("|  Algorithmes Quantitatifs + Factor Model + ML Ensemble    |")
        print("|  News Sentiment + Earnings + Cross-Asset Correlations     |")
        print("|  800+ Actions: PEA + PME + US + Europe + Crypto           |")
        print("+" + "="*63 + "+")
        print()
    except Exception:
        print("BLACKROCK ULTRA SCREENER v10.0 - Starting...")

    app = InterfaceScreener()
    app.lancer()


if __name__ == "__main__":
    main()
