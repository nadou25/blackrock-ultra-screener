"""
🧪 Tests basiques pour BlackRock Ultra Screener
Run: pytest tests/ -v
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestImports:
    """Test que les imports fonctionnent."""
    
    def test_import_pandas(self):
        import pandas as pd
        assert pd.__version__ >= "1.5.0"
    
    def test_import_numpy(self):
        import numpy as np
        assert np.__version__ >= "1.23.0"
    
    def test_import_yfinance(self):
        import yfinance as yf
        assert yf is not None
    
    def test_import_sklearn(self):
        from sklearn.ensemble import RandomForestClassifier
        assert RandomForestClassifier is not None


class TestScreenerModule:
    """Test le module screener."""
    
    def test_import_screener(self):
        """Test que le screener s'importe sans erreur."""
        import stock_screener_ultra_v10 as screener
        assert hasattr(screener, 'Config')
        assert hasattr(screener, 'MoteurAnalyse')
    
    def test_config_load(self):
        """Test le chargement de la config."""
        import stock_screener_ultra_v10 as screener
        config = screener.Config.charger()
        assert config is not None
        assert hasattr(config, 'SCORE_MINIMUM')
    
    def test_config_profiles(self):
        """Test les profils prédéfinis."""
        import stock_screener_ultra_v10 as screener
        config = screener.Config.charger()
        
        profiles = [
            "BALANCED", "SCALP_MAX", "SWING_MAX", 
            "INVESTISSEUR_1AN", "NASDAQ_SNIPER"
        ]
        for profile in profiles:
            config.appliquer_profil(profile)
            assert config.HORIZON_MODE is not None


class TestRiskManager:
    """Test le gestionnaire de risques."""
    
    def test_kelly_criterion(self):
        """Test le calcul du Kelly Criterion."""
        import stock_screener_ultra_v10 as screener
        
        # Kelly = W - (1-W)/R où W=win_rate, R=win/loss ratio
        # Si W=60%, R=2 → Kelly = 0.6 - 0.4/2 = 0.4
        config = screener.Config.charger()
        rm = screener.RiskManager(config)
        
        # Juste vérifier que la classe existe et est instanciable
        assert rm is not None


class TestIndicators:
    """Test les indicateurs techniques."""
    
    def test_rsi_bounds(self):
        """RSI doit être entre 0 et 100."""
        import numpy as np
        import pandas as pd
        import stock_screener_ultra_v10 as screener
        
        # Créer des données de test
        np.random.seed(42)
        prices = pd.Series(100 + np.cumsum(np.random.randn(100)))
        
        indic = screener.Indicateurs()
        rsi_series = indic.rsi_series(prices, 14)
        
        # RSI doit être dans [0, 100]
        assert rsi_series.dropna().min() >= 0
        assert rsi_series.dropna().max() <= 100


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
