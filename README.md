<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/ML-Ensemble%2013%20Models-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/RL-PPO%20Ensemble-00C853?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Telegram-Bot%20Daily%20Reports-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<h1 align="center">🏦 BlackRock Ultra Screener v10</h1>
<h3 align="center">Système de Screening Quantitatif Multi-Factoriel — Style Aladdin</h3>

<p align="center">
  <i>Screener d'actions professionnel combinant analyse quantitative avancée, Machine Learning (13 modèles ensemble), Reinforcement Learning (PPO), gestion des risques institutionnelle, et reporting automatisé via Telegram.</i>
</p>

---

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Dashboard Web](#-dashboard-web)
- [Backtesting](#-backtesting)
- [Profils de Trading](#-profils-de-trading)
- [Bot Telegram](#-bot-telegram)
- [Gestion des Risques](#-gestion-des-risques)
- [Docker](#-docker)
- [Avertissement](#-avertissement)

---

> ## 📬 OUI, LE BOT ENVOIE DES RAPPORTS CHAQUE JOUR !
> 
> Le bot Telegram envoie **automatiquement** un rapport complet tous les jours à 8h00 (configurable).  
> ✅ **30 signaux** (Top 10 × 3 horizons : Investisseur, Scalp, Swing)  
> ✅ **Entièrement automatique** — lancez une fois, recevez tous les jours  
> ✅ **Abonnement simple** — envoyez `/start` au bot
> 
> 👉 [Voir la section Bot Telegram](#-bot-telegram) pour plus de détails

---

## 🆕 Nouveautés v10.1

- 🌐 **Dashboard Web Streamlit** — Interface interactive complète
- 📉 **Backtesting Engine** — Testez vos stratégies historiquement
- 🐳 **Docker Support** — Déploiement simplifié
- 🧪 **Tests Unitaires** — CI/CD avec GitHub Actions
- 📦 **Packaging Moderne** — pyproject.toml, setup.py

---

## 🔭 Vue d'ensemble

**BlackRock Ultra Screener** est un système de screening d'actions tout-en-un, conçu pour l'analyse quantitative de niveau institutionnel. Il combine :

- **Analyse multi-factorielle** inspirée du modèle BlackRock/Aladdin (6 facteurs)
- **Machine Learning avancé** avec ensemble de 13 modèles (XGBoost, LightGBM, CatBoost, MLP, Random Forest, etc.)
- **Reinforcement Learning** via PPO (Proximal Policy Optimization) — ensemble de 3 agents
- **Risk Management professionnel** (Kelly Criterion, VaR, Monte Carlo, Stress Testing)
- **Horizons adaptatifs** : Scalp → Intraday → Swing → Position → Investisseur (1 an)
- **Bot Telegram** pour rapports quotidiens automatisés
- **Interface GUI** complète (Tkinter) avec tableau de bord risques

**Couverture marchés** : NASDAQ 100, S&P 500, PEA Europe (200+), PME, Commodities, Crypto, Gaming

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFACE GUI (Tkinter)                    │
│  Tableau • Détails • Paramètres • Risques • PPO • Export     │
├─────────────────────────────────────────────────────────────┤
│                     MOTEUR D'ANALYSE                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ BlackRock│ │  News &  │ │Corrélat. │ │    Risk      │   │
│  │  Factor  │ │ Earnings │ │Cross-Asset│ │  Manager     │   │
│  │  Model   │ │  Engine  │ │  Engine  │ │ (14 methods) │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
├─────────────────────────────────────────────────────────────┤
│               PRÉDICTION & INTELLIGENCE                      │
│  ┌────────────────────┐  ┌────────────────────────────┐     │
│  │   ML Ensemble (13) │  │   PPO Reinforcement (x3)   │     │
│  │  Triple Barrier     │  │  Gymnasium Environment     │     │
│  │  Purged K-Fold     │  │  Adaptive Horizons         │     │
│  │  Meta-Labeling     │  │  150+ Features             │     │
│  └────────────────────┘  └────────────────────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                    DONNÉES & CACHE                            │
│  Yahoo Finance • Google News • RSS • LRU Cache • SQLite      │
└─────────────────────────────────────────────────────────────┘
```

### Classes principales (~7 600 lignes)

| Classe | Lignes | Rôle |
|--------|--------|------|
| `Config` | ~360 | Configuration dynamique, 10 profils prédéfinis, persistance JSON |
| `UniversActions` | ~350 | Univers d'actions (NASDAQ, S&P, PEA, EU, Crypto, etc.) |
| `MathQuant` | ~170 | Hurst, Fractal Dimension, Entropy, Omega Ratio |
| `BlackRockFactorModel` | ~150 | Modèle 6 facteurs (Market, Size, Value, Momentum, Quality, Vol) |
| `NewsSentimentEngine` | ~120 | Scraping multi-source, 200+ mots-clés pondérés |
| `EarningsEngine` | ~80 | Suivi EPS/Revenue surprises, calendrier earnings |
| `CorrelationEngine` | ~80 | Corrélation dynamique cross-asset (VIX, SPY, TNX, DXY, Or) |
| `RiskManager` | ~430 | Kelly, VaR, Monte Carlo, Stress Test, R-Multiples, Risk Score |
| `Indicateurs` | ~170 | 40+ indicateurs techniques (RSI, MACD, Bollinger, Ichimoku...) |
| `PredicteurML` | ~530 | Ensemble 13 modèles, Triple Barrier, Purged K-Fold |
| `MoteurAnalyse` | ~800 | Orchestrateur principal, scoring, ranking |
| `RapportExcel` | ~870 | Export Excel multi-onglets professionnel |
| `SystemePPO` | ~1 040 | Env Gymnasium, PPO x3, entraînement, prédiction |
| `SystemeDecisionIA` | ~420 | Fusion ML + PPO + quant en décision finale |
| `InterfaceScreener` | ~1 800 | GUI complète Tkinter (5 onglets) |

---

## ✨ Fonctionnalités

### 🧠 Analyse Quantitative
- **Modèle multi-factoriel BlackRock** : Market β, Size, Value, Momentum, Quality, Volatility
- **Hurst Exponent** — détection tendance/mean-reversion
- **Fractal Dimension** — complexité de la série temporelle
- **Shannon Entropy** — mesure d'incertitude du marché
- **CUSUM Regime Detection** — changements de régime
- **Omega, Sortino, Calmar, Information Ratios**

### 🤖 Machine Learning
- **13 modèles en ensemble** : XGBoost, LightGBM, CatBoost, MLP, Random Forest, Extra Trees, Gradient Boosting, AdaBoost, Bagging, Logistic Regression, Ridge, KNN, SVC
- **Triple Barrier Labeling** (méthode López de Prado)
- **Purged K-Fold Cross-Validation** — pas de data leakage
- **Meta-Labeling & Stacking**
- **150+ features quantitatives**
- **Cache intelligent** avec invalidation par horizon

### 🎮 Reinforcement Learning (PPO)
- **3 agents PPO en ensemble** (vote majoritaire)
- **Environnement Gymnasium custom** avec 35+ observations
- **Horizons adaptatifs** : le PPO s'ajuste au profil (Scalp → Investisseur)
- **Récompenses calibrées** : Sharpe-based, risk-adjusted

### 📰 News & Earnings
- Scraping multi-source (Google News, Yahoo Finance, RSS)
- Analyse de sentiment (200+ mots-clés pondérés)
- Suivi des earnings (EPS surprise, revenue surprise)
- Impact scoring intégré au score final

### 📊 Corrélations Cross-Asset
- Matrice de corrélation dynamique (rolling 60 jours)
- Corrélation avec : VIX, SPY, TNX (taux), DXY (dollar), Or
- Beta-adjusted returns & Alpha generation

### 🛡️ Gestion des Risques (14 méthodes)
- **Kelly Criterion** — sizing optimal des positions
- **Value at Risk** (historique + Monte Carlo 10 000 simulations)
- **Stress Testing** (crash -30%, correction -15%, taux +200bp, etc.)
- **R-Multiples** tracking
- **Expectancy** & Edge ratio
- **Portfolio Correlation** & concentration risk
- **Risk Score Composite** (0-100)

### 🤖 Bot Telegram
- Rapport quotidien automatique (configurable)
- Top 10 par horizon : Investisseur, Scalp, Swing
- Commandes `/rapport`, `/investisseur`, `/scalp`, `/swing`
- Chat ID auto-détecté via `/start`

---

## 📦 Prérequis

- **Python 3.10+**
- **Windows 10/11** (GUI Tkinter native)
- Connexion internet (données Yahoo Finance)

### Dépendances principales

```
pandas · numpy · yfinance · scikit-learn
xgboost · lightgbm · catboost
stable-baselines3 · gymnasium · torch
openpyxl · python-telegram-bot · schedule
```

---

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/VOTRE_USERNAME/blackrock-ultra-screener.git
cd blackrock-ultra-screener
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
```

### 3. Installer les dépendances

```bash
pip install pandas numpy yfinance scikit-learn
pip install xgboost lightgbm catboost
pip install stable-baselines3 gymnasium torch
pip install openpyxl python-telegram-bot==20.7 schedule
```

### 4. Lancer l'application

```bash
python stock_screener_ultra_v10.py
```

---

## ⚙️ Configuration

### Fichier `screener_config_v10.json`

Le screener utilise un fichier JSON pour persister tous les paramètres. Il est créé automatiquement au premier lancement avec des valeurs par défaut optimisées.

**Paramètres clés :**

| Paramètre | Défaut | Description |
|-----------|--------|-------------|
| `SCORE_MINIMUM` | 55 | Score minimum pour afficher un titre |
| `ML_MAX_SYMBOLES` | 300 | Nombre max de titres à analyser |
| `FAST_MODE` | true | Mode rapide (cache ML) |
| `MODE_PEA` | false | Filtrer uniquement les titres éligibles PEA |
| `HORIZON_MODE` | INVESTISSEUR | Horizon temporel actif |
| `KELLY_FRACTION` | 0.20 | Fraction de Kelly pour le sizing |
| `VAR_CONFIDENCE` | 0.95 | Niveau de confiance VaR |
| `MAX_POSITION_PCT` | 5.0 | Taille max d'une position (% du portefeuille) |

### Variables d'environnement

Pour le bot Telegram, créez un fichier `.env` ou définissez :

```
TELEGRAM_BOT_TOKEN=votre_token_ici
```

> ⚠️ **Ne jamais committer votre token Telegram.** Utilisez des variables d'environnement ou un fichier `.env` ajouté au `.gitignore`.

---

## 🎯 Utilisation

### Interface Graphique (GUI)

```bash
python stock_screener_ultra_v10.py
```

L'interface propose **5 onglets** :
1. **📊 Résultats** — Tableau des titres analysés avec scores, décisions, SL/TP
2. **⚙️ Paramètres** — Configuration complète (univers, scoring, ML, horizons)
3. **🤖 PPO** — Entraînement et évaluation du Reinforcement Learning
4. **🛡️ Risques** — Dashboard risk management (Kelly, VaR, stress test)
5. **📋 Logs** — Journal d'exécution en temps réel

### Mode Headless (sans GUI)

```python
from stock_screener_ultra_v10 import Config, MoteurAnalyse

config = Config.charger()
config.appliquer_profil("INVESTISSEUR_1AN")
moteur = MoteurAnalyse(config)
results = moteur.executer()

for r in results[:10]:
    print(f"{r['symbole']} — Score: {r['score_final']:.0f} — {r['decision']}")
```

---

## 🌐 Dashboard Web

Interface web interactive avec Streamlit pour visualiser et analyser les résultats.

### Lancer le Dashboard

```bash
streamlit run dashboard.py
```

Ouvrez http://localhost:8501 dans votre navigateur.

### Fonctionnalités du Dashboard

| Onglet | Description |
|--------|-------------|
| 📊 Résultats | Tableau des titres avec scores et signaux |
| 📈 Analyse Détaillée | Graphiques candlestick, indicateurs techniques |
| 🛡️ Risk Management | Calculateur Kelly, VaR, position sizing |
| 📉 Backtesting | Testez les stratégies sur données historiques |

---

## 📉 Backtesting

Module de backtesting pour tester les stratégies sur données historiques.

### Usage CLI

```bash
# Backtest SMA Crossover sur AAPL (2 ans)
python backtester.py AAPL -s sma_crossover -p 2y

# Backtest RSI sur SPY (5 ans) avec $50k
python backtester.py SPY -s rsi_oversold -p 5y -c 50000
```

### Usage Python

```python
from backtester import Backtester

bt = Backtester(initial_capital=10000)
results = bt.run("NVDA", strategy="momentum", period="2y")
print(bt.report())

# Accès aux métriques
print(f"Sharpe: {results.sharpe_ratio:.2f}")
print(f"Max DD: {results.max_drawdown_pct:.1f}%")
```

### Stratégies Disponibles

| Stratégie | Description |
|-----------|-------------|
| `buy_hold` | Buy & Hold simple |
| `sma_crossover` | Croisement SMA 20/50 |
| `rsi_oversold` | Achat RSI < 30, vente RSI > 70 |
| `macd_signal` | Signal MACD |
| `momentum` | ROC 20 jours positif |
| `mean_reversion` | Bollinger Bands |

---

## 📈 Profils de Trading

10 profils prédéfinis optimisés pour différents styles :

| Profil | Horizon | Style | Description |
|--------|---------|-------|-------------|
| `BALANCED` | Swing | Équilibré | Paramètres par défaut, bon compromis |
| `PROFIT_MAX` | Swing | Agressif | Maximise l'espérance de gain |
| `PRECISION_MAX` | Swing | Conservateur | Maximise la précision des signaux |
| `SCALP_MAX` | Scalp | Ultra-court | 2-10 jours, momentum rapide |
| `INTRADAY_MAX` | Intraday | Court terme | 3-15 jours, mean-reversion |
| `SWING_MAX` | Swing | Moyen terme | 5-20 jours, tendance |
| `NASDAQ_SNIPER` | Swing | Sectoriel | Focus NASDAQ 100 |
| `SP500_VALUE` | Position | Value | Focus S&P 500, critères value |
| `INVESTISSEUR_1AN` | Investisseur | Long terme | Horizon 252 jours, qualité & valeur |
| `COMMODITIES` | Swing | Matières premières | Or, pétrole, matières premières |

### Horizons adaptatifs

Le système ajuste **automatiquement** tous les calculs (ML, PPO, indicateurs, SL/TP) selon l'horizon :

| Mode | Court | Moyen | Long | Usage |
|------|-------|-------|------|-------|
| SCALP | 2j | 5j | 10j | Trading ultra-court |
| INTRADAY | 3j | 7j | 15j | Day trading |
| SWING | 5j | 10j | 20j | Swing trading |
| POSITION | 10j | 30j | 60j | Position trading |
| INVESTISSEUR | 20j | 60j | 252j | Investissement long terme |

---

## 🤖 Bot Telegram

> **📬 RAPPORTS AUTOMATIQUES QUOTIDIENS** : Le bot envoie automatiquement un rapport complet chaque jour à 8h00 (configurable). Il suffit de lancer le bot une fois et de s'abonner avec `/start` !

### Configuration

1. Créez un bot via [@BotFather](https://t.me/BotFather)
2. Configurez le token dans `telegram_bot.py` via variable d'environnement
3. Lancez le bot :

```bash
python telegram_bot.py
```

4. Envoyez `/start` au bot pour vous abonner

### Commandes disponibles

| Commande | Description |
|----------|-------------|
| `/start` | S'abonner aux rapports (enregistrement auto du chat ID) |
| `/rapport` | Rapport complet immédiat (3 horizons) |
| `/investisseur` | Top 10 Investisseur (1 an) |
| `/scalp` | Top 10 Scalp/Intraday |
| `/swing` | Top 10 Swing |
| `/status` | État du bot et statistiques |
| `/heure HH:MM` | Modifier l'heure du rapport quotidien |

### Rapport quotidien

Chaque jour à l'heure configurée (défaut 08:00), le bot envoie automatiquement :
- 📈 **Top 10 Investisseur** — Horizon 1 an, qualité & valeur
- ⚡ **Top 10 Scalp/Intraday** — Court terme, momentum
- 🔄 **Top 10 Swing** — Moyen terme, tendance

Chaque signal inclut : Score, Ratio R:R, EV%, Stop-Loss, Take-Profit, Kelly%, Risk Score.

### ❓ FAQ — Rapports Quotidiens

**Q: Est-ce que le bot envoie des rapports chaque jour ?**  
**R: OUI** ✅ — Le bot envoie automatiquement un rapport complet tous les jours à l'heure configurée (par défaut 08:00).

**Q: Comment fonctionne l'envoi automatique ?**  
**R:** Une fois que vous lancez le bot avec `python telegram_bot.py`, il reste actif en arrière-plan et vérifie l'heure toutes les 30 secondes. Lorsque l'heure du rapport est atteinte, il génère et envoie automatiquement le rapport à tous les abonnés.

**Q: Comment s'abonner aux rapports quotidiens ?**  
**R:** Envoyez simplement `/start` au bot. Votre chat ID sera automatiquement enregistré et vous recevrez tous les rapports quotidiens.

**Q: Puis-je changer l'heure du rapport ?**  
**R:** Oui, utilisez la commande `/heure HH:MM`. Par exemple : `/heure 09:30` pour recevoir le rapport à 9h30.

**Q: Que contient le rapport quotidien ?**  
**R:** Le rapport inclut 3 sections avec 10 titres chacune (30 signaux au total) :
- 📈 Top 10 **INVESTISSEUR** (horizon 1 an)
- ⚡ Top 10 **SCALP/INTRADAY** (horizon court terme)
- 🔄 Top 10 **SWING** (horizon moyen terme)

**Q: Le bot doit-il rester actif en permanence ?**  
**R:** Oui, pour envoyer les rapports quotidiens, le processus `telegram_bot.py` doit rester en exécution 24/7. Utilisez Docker ou un service comme systemd/supervisor pour le maintenir actif.

**Q: Que se passe-t-il si le bot est arrêté ?**  
**R:** Si le bot est arrêté, il ne pourra pas envoyer de rapport. Redémarrez-le et il reprendra le cycle normal. Le prochain rapport sera envoyé à l'heure configurée le jour suivant.

---

## 🛡️ Gestion des Risques

Le module `RiskManager` intègre 14 méthodes de gestion des risques :

### Position Level
- **Kelly Criterion** — Sizing optimal basé sur le win rate et le ratio gains/pertes
- **VaR Historique** — Value at Risk au seuil de confiance configurable
- **VaR Monte Carlo** — 10 000 simulations pour estimation de la distribution des pertes
- **R-Multiples** — Tracking du risque en unités de R

### Portfolio Level
- **Portfolio Correlation** — Matrice de corrélation des positions
- **Concentration Risk** — HHI (Herfindahl–Hirschman Index)
- **Stress Testing** — 5 scénarios (crash, correction, taux, récession, flash crash)
- **Risk Score Composite** — Score 0-100 agrégé multi-critères

### Métriques affichées
- Expectancy & Edge Ratio
- Max Drawdown estimé
- VaR 1-jour & 5-jours
- Stress impact par scénario
- Score de risque global

---

## 🔒 Sécurité

> **Ne jamais committer de données sensibles** (tokens, clés API, identifiants).

Le fichier `.gitignore` exclut automatiquement :
- Tokens et fichiers de configuration sensibles
- Modèles ML/PPO pré-entraînés (volumineux)
- Caches et logs
- Fichiers d'environnement

Pour le bot Telegram, utilisez une **variable d'environnement** :

```python
import os
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
```

---

## 📁 Structure du Projet

```
blackrock-ultra-screener/
├── stock_screener_ultra_v10.py    # Application principale (~7 600 lignes)
├── telegram_bot.py                # Bot Telegram quotidien
├── screener_config_v10.json       # Configuration persistante
├── requirements.txt               # Dépendances Python
├── .env.example                   # Template variables d'environnement
├── .gitignore                     # Exclusions Git
└── README.md                      # Ce fichier
```

---

## 🐳 Docker

Déployez facilement avec Docker.

### Build et Run

```bash
# Build l'image
docker build -t screener .

# Lancer le bot Telegram
docker run -d --name screener-bot \
  -e TELEGRAM_BOT_TOKEN=votre_token \
  screener

# Lancer une analyse one-shot
docker run --rm screener python -c "
from stock_screener_ultra_v10 import Config, MoteurAnalyse
config = Config.charger()
config.appliquer_profil('INVESTISSEUR_1AN')
moteur = MoteurAnalyse(config)
for r in moteur.executer()[:10]:
    print(f\"{r['symbole']} - Score: {r['score_final']:.0f}\")
"
```

### Docker Compose

```bash
# Bot 24/7
docker-compose up -d bot

# Analyse manuelle
docker-compose run --rm screener
```

---

## ⚠️ Avertissement

> **Ce logiciel est fourni à titre éducatif et de recherche uniquement.**
>
> Il ne constitue en aucun cas un conseil en investissement. Les marchés financiers comportent des risques de perte en capital. Les performances passées ne préjugent pas des performances futures. L'utilisateur est seul responsable de ses décisions d'investissement.
>
> Les auteurs déclinent toute responsabilité quant aux pertes financières résultant de l'utilisation de ce logiciel.

---

## 📄 License

Ce projet est sous licence [MIT](LICENSE).

---

<p align="center">
  <b>Built with ❤️ — Quantitative Analysis meets Modern AI</b>
</p>
