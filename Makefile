# 🏦 BlackRock Ultra Screener - Makefile
# Usage: make [target]

.PHONY: install run bot clean lint help

# Default target
help:
	@echo "🏦 BlackRock Ultra Screener - Commandes disponibles:"
	@echo ""
	@echo "  make install    - Installer les dépendances"
	@echo "  make run        - Lancer le screener (GUI)"
	@echo "  make bot        - Lancer le bot Telegram"
	@echo "  make lint       - Vérifier le code (flake8)"
	@echo "  make clean      - Nettoyer les fichiers temporaires"
	@echo ""

# Installation des dépendances
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ Installation terminée"

# Lancer le screener
run:
	python stock_screener_ultra_v10.py

# Lancer le bot Telegram
bot:
	python telegram_bot.py

# Vérification du code
lint:
	python -m py_compile stock_screener_ultra_v10.py
	python -m py_compile telegram_bot.py
	@echo "✅ Syntaxe OK"

# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf catboost_info/
	@echo "✅ Nettoyage terminé"
