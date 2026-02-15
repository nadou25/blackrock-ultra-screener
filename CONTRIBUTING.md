# 🤝 Contributing to BlackRock Ultra Screener

Merci de vouloir contribuer ! Voici les guidelines pour participer au projet.

## 🚀 Quick Start

```bash
# 1. Fork et clone
git clone https://github.com/VOTRE_USERNAME/blackrock-ultra-screener.git
cd blackrock-ultra-screener

# 2. Créer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer une branche
git checkout -b feature/ma-feature
```

## 📝 Guidelines

### Code Style
- **PEP 8** avec max 120 caractères par ligne
- **Docstrings** pour les fonctions publiques
- **Type hints** quand possible
- **Commentaires en français** (projet francophone)

### Commits
Format recommandé :
```
🚀 feat: Ajouter support crypto
🐛 fix: Corriger calcul VaR
📝 docs: Mettre à jour README
♻️ refactor: Simplifier RiskManager
🧪 test: Ajouter tests ML
```

### Pull Requests
1. Décrire clairement les changements
2. Référencer les issues liées (`Fixes #123`)
3. S'assurer que le CI passe
4. Demander une review si changement majeur

## 🔒 Sécurité

**JAMAIS** de tokens, clés API ou données sensibles dans le code.
Utiliser des variables d'environnement :

```python
import os
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
```

## 🧪 Tests

```bash
# Vérifier la syntaxe
python -m py_compile stock_screener_ultra_v10.py

# Lancer le screener en mode test
python stock_screener_ultra_v10.py --test
```

## 📋 Idées de Contributions

- [ ] Ajouter des tests unitaires
- [ ] Support pour d'autres brokers (Interactive Brokers API)
- [ ] Dashboard web (Streamlit/Dash)
- [ ] Notifications Discord
- [ ] Docker support
- [ ] Support multi-langue
- [ ] Backtesting intégré

## ❓ Questions ?

Ouvrez une issue avec le tag `question`.

---

Merci pour votre contribution ! 🙏
