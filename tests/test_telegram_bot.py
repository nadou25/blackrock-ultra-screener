"""
🧪 Tests pour le bot Telegram
Run: pytest tests/test_telegram_bot.py -v
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestTelegramBotImport:
    """Test que le bot Telegram s'importe correctement."""
    
    def test_import_telegram_bot(self):
        """Test que le module telegram_bot s'importe sans erreur."""
        import telegram_bot
        assert telegram_bot is not None
    
    def test_bot_functions_exist(self):
        """Test que les fonctions principales existent."""
        import telegram_bot
        
        # Fonctions de configuration
        assert hasattr(telegram_bot, 'charger_config')
        assert hasattr(telegram_bot, 'sauver_config')
        
        # Fonctions de rapport
        assert hasattr(telegram_bot, 'generate_full_report')
        assert hasattr(telegram_bot, 'format_stock_line')
        
        # Fonctions async (commandes)
        assert hasattr(telegram_bot, 'cmd_start')
        assert hasattr(telegram_bot, 'cmd_rapport')
        assert hasattr(telegram_bot, 'cmd_status')
        
        # Fonction principale
        assert hasattr(telegram_bot, 'main')


class TestTelegramBotConfig:
    """Test la configuration du bot Telegram."""
    
    def test_charger_config_default(self):
        """Test le chargement de la config par défaut."""
        import telegram_bot
        
        config = telegram_bot.charger_config()
        assert config is not None
        assert isinstance(config, dict)
        
        # Vérifier les clés essentielles
        assert "chat_ids" in config
        assert "heure_rapport" in config
        assert "actif" in config
        assert "retrain_interval_days" in config
        
        # Vérifier les valeurs par défaut
        assert isinstance(config["chat_ids"], list)
        assert config["heure_rapport"] == "08:00"
        assert config["actif"] == True
        assert config["retrain_interval_days"] == 7


class TestTelegramRateLimits:
    """Test que les rate limits sont respectés."""
    
    def test_asyncio_sleep_in_code(self):
        """Vérifier que le code contient des asyncio.sleep pour respecter les rate limits."""
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'telegram_bot.py'), 'r') as f:
            content = f.read()
        
        # Vérifier que asyncio.sleep est utilisé
        assert 'await asyncio.sleep' in content, "Le code doit contenir des delays (asyncio.sleep)"
        
        # Vérifier qu'il y a plusieurs occurrences (dans différentes fonctions)
        sleep_count = content.count('await asyncio.sleep')
        assert sleep_count >= 4, f"Expected at least 4 asyncio.sleep calls, found {sleep_count}"
    
    def test_error_logging_exists(self):
        """Vérifier que le logging d'erreurs est présent."""
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'telegram_bot.py'), 'r') as f:
            content = f.read()
        
        # Vérifier la présence de logging d'erreurs
        assert 'log.error' in content, "Le code doit contenir du logging d'erreurs"
        assert 'exc_info=True' in content, "Le code doit utiliser exc_info=True pour logger les stack traces"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
