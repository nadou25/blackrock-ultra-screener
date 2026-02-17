# 📬 Guide d'Utilisation des Rapports Quotidiens

## ✅ Réponse Rapide

**OUI, le bot envoie automatiquement des rapports chaque jour !**

Le bot Telegram envoie automatiquement un rapport complet tous les jours à l'heure configurée (par défaut 08:00).

---

## 🚀 Démarrage Rapide

### Étape 1: Configurer le Token Telegram

Créez un fichier `.env` à la racine du projet :

```bash
TELEGRAM_BOT_TOKEN=votre_token_ici
```

Pour obtenir un token :
1. Ouvrez Telegram et cherchez **@BotFather**
2. Envoyez `/newbot` et suivez les instructions
3. Copiez le token fourni

### Étape 2: Lancer le Bot

```bash
python telegram_bot.py
```

Vous devriez voir :

```
+==================================================+
|  🤖 BLACKROCK SCREENER — BOT TELEGRAM PRO     |
|  Bot: @nadououbot                              |
|  Rapport quotidien: TOP 10 x 3 horizons       |
|  Re-entraînement ML+PPO: auto tous les 7j     |
+==================================================+

⏰ Heure du rapport: 08:00
🔄 Retrain tous les: 7j
📅 Dernier retrain: Jamais
👥 Abonnés: 0
📌 Envoyez /start à @nadououbot pour vous abonner

🚀 Bot démarré — polling...
```

### Étape 3: S'Abonner aux Rapports

1. Ouvrez Telegram
2. Cherchez votre bot (ex: @nadououbot)
3. Envoyez `/start`

Vous recevrez un message de confirmation et serez automatiquement ajouté à la liste des abonnés.

**C'est tout !** 🎉 Vous recevrez maintenant un rapport tous les jours à 08:00.

---

## 📊 Que Contient le Rapport Quotidien ?

Chaque jour, vous recevez **30 signaux** répartis en 3 horizons :

### 📈 Top 10 INVESTISSEUR (1 an)
- Horizon long terme
- Focus : qualité, valeur, croissance
- Pour : investissements à moyen/long terme

### ⚡ Top 10 SCALP/INTRADAY
- Horizon très court terme (2-15 jours)
- Focus : momentum, reversals, volume
- Pour : trading actif

### 🔄 Top 10 SWING (5-20 jours)
- Horizon moyen terme
- Focus : tendances, breakouts, smart money
- Pour : swing trading

### Informations par Signal

Chaque signal inclut :
- **Score global** (0-100) avec décomposition (technique, fondamental, momentum)
- **Prix actuel** et variation (1j, 1s, 1m)
- **Décision** : ACHAT FORT 🟢🟢, ACHAT 🟢, SURVEILLANCE 🟡
- **Stop-Loss et Take-Profit** avec pourcentages
- **Ratio Risque/Rendement (R:R)** et **Espérance de gain (EV%)**
- **Kelly %** — taille de position recommandée
- **Risk Score** — score de risque global (0-100)
- **ML & PPO** — probabilité ML, action PPO, fiabilité
- **Indicateurs** — RSI, Beta, Hurst, Sharpe, BlackRock score
- **Fondamentaux** — PE, ROE, Dividende
- **Secteur et marché**
- **Raison** — explication du signal

---

## ⚙️ Configuration

### Changer l'Heure du Rapport

Par défaut, le rapport est envoyé à **08:00**. Pour changer :

```
/heure 09:30
```

Le bot confirmera : ✅ *Heure du rapport changée à 09:30*

### Vérifier l'État du Bot

```
/status
```

Affiche :
- État du bot (actif/inactif)
- Heure du rapport configurée
- Nombre d'abonnés
- Date du dernier rapport
- État des modèles ML/PPO
- Date du dernier re-entraînement

### Obtenir un Rapport Immédiatement

Pas besoin d'attendre demain ! Utilisez :

```
/rapport
```

Le bot génère et envoie un rapport complet immédiatement (2-5 minutes).

### Rapports par Horizon

Vous voulez juste un horizon spécifique ?

```
/investisseur   # Top 10 investisseur uniquement
/scalp          # Top 10 scalp/intraday
/swing          # Top 10 swing
```

---

## 🔄 Re-entraînement Automatique

Le bot se réentraîne automatiquement tous les 7 jours :
- **Quand** : Tous les 7 jours à 03:00 du matin
- **Quoi** : ML (13 modèles) + PPO (3 agents) pour chaque profil
- **Durée** : ~15-45 minutes
- **Notification** : Vous recevez un message au début et à la fin

Pour forcer un re-entraînement immédiat :

```
/retrain
```

---

## 🐳 Déploiement 24/7

Pour que le bot envoie les rapports quotidiens, il doit rester en exécution en permanence.

### Option 1: Docker (Recommandé)

```bash
# Build
docker build -t screener-bot .

# Run en arrière-plan
docker run -d --name screener-bot \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN=votre_token \
  screener-bot
```

Ou avec Docker Compose :

```bash
docker-compose up -d bot
```

### Option 2: systemd (Linux)

Créez `/etc/systemd/system/screener-bot.service` :

```ini
[Unit]
Description=BlackRock Screener Telegram Bot
After=network.target

[Service]
Type=simple
User=votre_utilisateur
WorkingDirectory=/chemin/vers/blackrock-ultra-screener
Environment="TELEGRAM_BOT_TOKEN=votre_token"
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Puis :

```bash
sudo systemctl daemon-reload
sudo systemctl enable screener-bot
sudo systemctl start screener-bot
sudo systemctl status screener-bot
```

### Option 3: screen/tmux (Quick & Dirty)

```bash
# Avec screen
screen -S screener-bot
python telegram_bot.py
# Ctrl+A puis D pour détacher

# Pour revenir
screen -r screener-bot

# Avec tmux
tmux new -s screener-bot
python telegram_bot.py
# Ctrl+B puis D pour détacher

# Pour revenir
tmux attach -t screener-bot
```

---

## 🧪 Vérification

Pour vérifier que la logique de planification fonctionne :

```bash
python verify_daily_reports.py
```

Ce script teste :
- ✅ Détection correcte de l'heure du rapport
- ✅ Rapport envoyé une seule fois par jour
- ✅ Fréquence de vérification (toutes les 30s)
- ✅ Re-entraînement hebdomadaire automatique

---

## 🐛 Dépannage

### Le bot ne démarre pas

**Erreur : Token invalide**
```
❌ Token Telegram invalide!
```

**Solution** : Vérifiez que `TELEGRAM_BOT_TOKEN` est bien défini dans `.env` ou comme variable d'environnement.

**Erreur : Module non trouvé**
```
ModuleNotFoundError: No module named 'telegram'
```

**Solution** : Installez les dépendances :
```bash
pip install python-telegram-bot==20.7
```

### Le bot ne répond pas

1. Vérifiez que le bot est en cours d'exécution :
   ```bash
   ps aux | grep telegram_bot.py
   ```

2. Vérifiez les logs :
   ```bash
   tail -f telegram_bot.log
   ```

3. Redémarrez le bot :
   ```bash
   # Si lancé manuellement
   Ctrl+C pour arrêter, puis relancer
   
   # Si en systemd
   sudo systemctl restart screener-bot
   
   # Si en Docker
   docker restart screener-bot
   ```

### Je ne reçois pas de rapport quotidien

1. Vérifiez que vous êtes abonné :
   ```
   /status
   ```
   Doit afficher "Abonnés: 1" (ou plus)

2. Vérifiez l'heure configurée :
   ```
   /status
   ```
   Regardez "Heure rapport: XX:XX"

3. Vérifiez que le bot est actif 24/7 :
   ```bash
   # Doit être en cours d'exécution
   ps aux | grep telegram_bot.py
   ```

4. Testez immédiatement :
   ```
   /rapport
   ```
   Si ça fonctionne, le bot est OK, attendez le lendemain à l'heure configurée.

### Le rapport prend trop de temps

C'est normal ! La génération d'un rapport complet (30 signaux × 3 horizons) prend **2-5 minutes** car :
- Analyse de 200+ titres
- Calculs ML (13 modèles) et PPO (3 agents)
- Indicateurs techniques avancés
- Risk management complet

Pour accélérer :
- Réduire `ML_MAX_SYMBOLES` dans `screener_config_v10.json`
- Utiliser `FAST_MODE: true` (utilise le cache ML)

---

## 📝 Exemples de Messages Reçus

### Message de Bienvenue (/start)

```
👋 Bienvenue John !

🏦 BLACKROCK SCREENER BOT PRO

📬 Rapport quotidien à 08:00 :
  📈 Top 10 INVESTISSEUR (1 an)
  ⚡ Top 10 SCALP / INTRADAY
  🔄 Top 10 SWING

🧠 ML: Ensemble 13 modèles
🎮 RL: PPO × 3 agents
🔄 Re-entraînement auto: tous les 7j
📅 Dernier training: 2026-02-15

🆔 Chat ID: 123456789

📌 Commandes :
/rapport — Rapport complet immédiat
/investisseur — Top 10 Investisseur
/scalp — Top 10 Scalp/Intraday
/swing — Top 10 Swing
/retrain — Forcer re-entraînement ML+PPO
/status — État du bot
/heure HH:MM — Changer l'heure
```

### Rapport Quotidien (Extrait)

```
🏦 BLACKROCK SCREENER — RAPPORT PRO
📅 Lundi 17/02/2026 08:00
🔄 Dernier entraînement ML/PPO: 2026-02-15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 3 horizons × Top 10 = 30 signaux
⚠️ Ceci n'est pas un conseil en investissement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

════════════════════════════════
📈 INVESTISSEUR (1 AN)
Long terme — Qualité, Valeur & Croissance
📅 17/02/2026 08:00
────────────────────────────────

1. 🟢🟢 AAPL  •  $182.45
   ACHAT FORT
   📊 Score: 85/100  (Tech 88 | Fonda 82 | Mom 85)
   🏦 BlackRock: 87  |  ML: 78%  |  PPO: ACHAT (85%)
   🎯 SL: $175.20 (-3.9%)  →  TP: $196.80 (+7.8%)
   ⚖️ R:R: 2.00  |  EV: +12.5%  |  Potentiel: +7.8%
   💰 Kelly: 8.5%  |  Risk: 35/100  |  Sharpe: 1.85
   📈 1j: +1.2%  |  1s: +3.5%  |  1m: +8.2%
   📐 RSI: 62  |  β: 1.15  |  Hurst: 0.58
   🏷 PE: 28.5  |  ROE: 147.3%  |  Div: 0.5%
   🏢 NASDAQ — Technology
   💡 Momentum solide, qualité exceptionnelle, position de marché dominante

[... 9 autres signaux ...]

────────────────────────────────
📊 RÉSUMÉ INVESTISSEUR (1 AN)
  🏆 Top: AAPL (85/100)
  📈 Score moyen: 74/100
  ⚖️ R:R moyen: 2.3  |  EV moy: +15.2%
  🟢 8 ACHAT  |  🟡 2 SURVEILLER  |  10 titres
```

---

## 📞 Support

Si vous avez des questions ou problèmes :

1. Consultez d'abord la [FAQ dans le README](README.md#-faq--rapports-quotidiens)
2. Exécutez `python verify_daily_reports.py` pour diagnostiquer
3. Vérifiez les logs : `tail -f telegram_bot.log`
4. Ouvrez une [issue sur GitHub](https://github.com/nadou25/blackrock-ultra-screener/issues)

---

## ✅ Checklist de Vérification

Avant de signaler un problème, vérifiez :

- [ ] Le token Telegram est configuré (`.env` ou variable d'environnement)
- [ ] Le bot est en cours d'exécution (`ps aux | grep telegram_bot.py`)
- [ ] Vous avez envoyé `/start` au bot (vérifiez avec `/status`)
- [ ] Le bot est actif 24/7 (pas juste lancé manuellement temporairement)
- [ ] L'heure du rapport est correcte (`/status` pour vérifier)
- [ ] Les dépendances sont installées (`pip install -r requirements.txt`)
- [ ] Python 3.10+ est utilisé (`python --version`)

---

**Dernière mise à jour** : 17/02/2026

**⭐ N'oubliez pas** : Le bot DOIT rester en exécution 24/7 pour envoyer les rapports quotidiens. Utilisez Docker, systemd, ou une autre solution pour le garder actif en permanence !
