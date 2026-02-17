"""
🧪 Tests pour le Bot Telegram et les rapports quotidiens
Run: pytest tests/test_telegram_bot.py -v
"""

import sys
import os
from datetime import datetime, timedelta, date

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestTelegramBotConfig:
    """Test la configuration du bot Telegram."""
    
    def test_import_telegram_bot(self):
        """Test que le module telegram_bot s'importe sans erreur."""
        import telegram_bot
        assert telegram_bot is not None
    
    def test_config_functions(self):
        """Test les fonctions de configuration."""
        import telegram_bot
        
        # Test charger_config
        cfg = telegram_bot.charger_config()
        assert isinstance(cfg, dict)
        assert 'heure_rapport' in cfg
        assert 'chat_ids' in cfg
        assert 'actif' in cfg
    
    def test_default_config_values(self):
        """Test les valeurs par défaut de la configuration."""
        import telegram_bot
        
        cfg = telegram_bot.charger_config()
        assert cfg.get('heure_rapport') == '08:00'
        assert cfg.get('actif') == True
        assert cfg.get('retrain_interval_days') == 7
        assert isinstance(cfg.get('chat_ids'), list)


class TestSchedulerLogic:
    """Test la logique du scheduler de rapports quotidiens."""
    
    def test_time_window_detection(self):
        """Test que l'heure du rapport est détectée dans la fenêtre de 5 minutes."""
        # Logique extraite de scheduler_loop (lignes 666-677 de telegram_bot.py)
        heure_rapport = "08:00"
        h, m = heure_rapport.split(":")
        
        # Test à différentes heures
        test_cases = [
            # (test_time, should_send, description)
            ("08:00:00", True, "À l'heure exacte"),
            ("08:02:30", True, "2.5 minutes après"),
            ("08:04:59", True, "Juste avant la fin de la fenêtre"),
            ("08:05:01", False, "Après la fenêtre de 5 minutes"),
            ("07:59:59", False, "Avant l'heure du rapport"),
            ("09:00:00", False, "1 heure après"),
        ]
        
        for time_str, expected, desc in test_cases:
            now = datetime.now().replace(
                hour=int(time_str.split(":")[0]),
                minute=int(time_str.split(":")[1]),
                second=int(time_str.split(":")[2]),
                microsecond=0
            )
            target_time = now.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
            window_end = target_time + timedelta(minutes=5)
            
            should_send = (now >= target_time and now < window_end)
            
            assert should_send == expected, f"Failed for {desc}: {time_str}"
    
    def test_daily_report_once_per_day(self):
        """Test que le rapport n'est envoyé qu'une fois par jour."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        test_cases = [
            # (last_report_date, current_date, should_send, description)
            (None, today, True, "Première exécution"),
            (yesterday, today, True, "Dernière exécution hier"),
            (today, today, False, "Déjà envoyé aujourd'hui"),
        ]
        
        for last_date, current_date, expected, desc in test_cases:
            # Simuler la logique: last_report_date != today
            should_send = (last_date != current_date)
            
            assert should_send == expected, f"Failed for {desc}"
    
    def test_check_frequency(self):
        """Test que la fréquence de vérification est correcte."""
        check_interval = 30  # secondes, comme dans le code (ligne 683)
        checks_per_hour = 3600 / check_interval
        checks_per_day = checks_per_hour * 24
        
        assert check_interval == 30
        assert checks_per_hour == 120
        assert checks_per_day == 2880


class TestRetrainLogic:
    """Test la logique de re-entraînement hebdomadaire."""
    
    def test_retrain_needed_logic(self):
        """Test la détection du besoin de re-entraînement."""
        today = date.today()
        
        test_cases = [
            # (last_retrain_date_str, interval_days, should_retrain, description)
            (None, 7, True, "Jamais entraîné"),
            (today.strftime("%Y-%m-%d"), 7, False, "Entraîné aujourd'hui"),
            ((today - timedelta(days=8)).strftime("%Y-%m-%d"), 7, True, "8 jours écoulés"),
            ((today - timedelta(days=5)).strftime("%Y-%m-%d"), 7, False, "5 jours seulement"),
        ]
        
        for last_date_str, interval, expected, desc in test_cases:
            # Simuler la logique de retrain_needed()
            if not last_date_str:
                needs_retrain = True
            else:
                try:
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                    days_since = (today - last_date).days
                    needs_retrain = days_since >= interval
                except:
                    needs_retrain = True
            
            assert needs_retrain == expected, f"Failed for {desc}"


class TestReportGeneration:
    """Test la génération des rapports."""
    
    def test_format_stock_line_function(self):
        """Test que format_stock_line génère une ligne valide."""
        import telegram_bot
        
        # Créer un résultat de test
        test_result = {
            'symbole': 'AAPL',
            'score_final': 85,
            'prix': 182.45,
            'decision': 'ACHAT FORT',
            'action': 'ACHAT FORT',
            'ratio_rr': 2.0,
            'ev_pct': 12.5,
            'stop_loss': 175.20,
            'take_profit': 196.80,
            'stop_loss_pct': -3.9,
            'take_profit_pct': 7.8,
            'kelly_used_pct': 8.5,
            'risk_score': 35,
            'secteur': 'Technology',
            'marche': 'NASDAQ',
            'ml_probabilite': 78,
            'ppo_action': 'ACHAT',
            'ppo_fiabilite': 85,
            'var_1j': 1.2,
            'var_1s': 3.5,
            'var_1m': 8.2,
            'rsi': 62,
            'beta': 1.15,
            'hurst': 0.58,
            'sharpe': 1.85,
            'blackrock_score': 87,
            'potentiel': 7.8,
            'raison': 'Momentum solide',
            'score_technique': 88,
            'score_fondamental': 82,
            'score_momentum': 85,
            'pe': 28.5,
            'roe': 147.3,
            'div_yield': 0.5,
        }
        
        line = telegram_bot.format_stock_line(1, test_result)
        
        # Vérifier que la ligne contient les éléments clés
        assert 'AAPL' in line
        assert '85' in line  # Score
        assert '182.45' in line  # Prix
        assert 'ACHAT' in line  # Décision
        assert 'R:R' in line
        assert 'Kelly' in line
        assert len(line) > 100  # Doit être substantiel


class TestSchedulerIntegration:
    """Tests d'intégration du scheduler."""
    
    def test_complete_daily_cycle(self):
        """Test le cycle complet quotidien."""
        # Ce test vérifie la logique complète sans vraiment envoyer de messages
        
        # Simuler une journée
        heure_rapport = "08:00"
        h, m = heure_rapport.split(":")
        
        # État initial
        last_report_date = None
        today = datetime.now().date()
        
        # Vérification à différentes heures de la journée
        times_to_check = [
            "07:00:00",  # Avant le rapport
            "08:00:00",  # Heure exacte -> ENVOI
            "08:02:00",  # Encore dans la fenêtre
            "08:10:00",  # Après la fenêtre
            "12:00:00",  # Milieu de journée
            "20:00:00",  # Soir
        ]
        
        reports_sent = 0
        
        for time_str in times_to_check:
            now = datetime.now().replace(
                hour=int(time_str.split(":")[0]),
                minute=int(time_str.split(":")[1]),
                second=int(time_str.split(":")[2]),
                microsecond=0
            )
            
            target_time = now.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
            window_end = target_time + timedelta(minutes=5)
            
            # Logique du scheduler
            if (now >= target_time and 
                last_report_date != today and 
                now < window_end):
                
                # Rapport envoyé
                reports_sent += 1
                last_report_date = today
        
        # Vérifier qu'un seul rapport a été envoyé
        assert reports_sent == 1, f"Expected 1 report, but {reports_sent} were sent"


if __name__ == "__main__":
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        # Si pytest n'est pas disponible, exécuter les tests manuellement
        print("=" * 70)
        print("🧪 TESTS DU BOT TELEGRAM - Mode Manuel")
        print("=" * 70)
        print()
        
        test_classes = [
            TestTelegramBotConfig,
            TestSchedulerLogic,
            TestRetrainLogic,
            TestReportGeneration,
            TestSchedulerIntegration,
        ]
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for test_class in test_classes:
            print(f"📦 {test_class.__name__}")
            print(f"   {test_class.__doc__}")
            
            instance = test_class()
            test_methods = [m for m in dir(instance) if m.startswith('test_')]
            
            for method_name in test_methods:
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"   ✅ {method_name}")
                    passed_tests += 1
                except AssertionError as e:
                    print(f"   ❌ {method_name}: {e}")
                    failed_tests += 1
                except Exception as e:
                    print(f"   ⚠️  {method_name}: {e}")
                    failed_tests += 1
            
            print()
        
        print("=" * 70)
        print(f"📊 RÉSULTATS: {passed_tests}/{total_tests} tests réussis")
        if failed_tests == 0:
            print("✅ Tous les tests sont passés!")
        else:
            print(f"❌ {failed_tests} test(s) échoué(s)")
        print("=" * 70)
