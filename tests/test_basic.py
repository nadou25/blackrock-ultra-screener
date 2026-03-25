"""
🧪 Tests basiques pour BlackRock Ultra Screener
Run: pytest tests/ -v
"""

import sys
import os
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestImports:
    """Test que les imports fonctionnent."""

    def test_import_pandas(self):
        pd = pytest.importorskip("pandas", minversion="1.5.0")
        assert pd.__version__ >= "1.5.0"

    def test_import_numpy(self):
        np = pytest.importorskip("numpy", minversion="1.23.0")
        assert np.__version__ >= "1.23.0"

    def test_import_yfinance(self):
        yf = pytest.importorskip("yfinance")
        assert yf is not None

    def test_import_sklearn(self):
        sklearn = pytest.importorskip("sklearn")
        from sklearn.ensemble import RandomForestClassifier
        assert RandomForestClassifier is not None


class TestScreenerModule:
    """Test le module screener."""

    def test_import_screener(self):
        """Test que le screener s'importe sans erreur."""
        pytest.importorskip("pandas")
        pytest.importorskip("numpy")
        pytest.importorskip("sklearn")
        import stock_screener_ultra_v10 as screener
        assert hasattr(screener, 'Config')
        assert hasattr(screener, 'MoteurAnalyse')

    def test_config_load(self):
        """Test le chargement de la config."""
        pytest.importorskip("pandas")
        pytest.importorskip("numpy")
        pytest.importorskip("sklearn")
        import stock_screener_ultra_v10 as screener
        config = screener.Config.charger()
        assert config is not None
        assert hasattr(config, 'SCORE_MINIMUM')

    def test_config_profiles(self):
        """Test les profils prédéfinis."""
        pytest.importorskip("pandas")
        pytest.importorskip("numpy")
        pytest.importorskip("sklearn")
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
        pytest.importorskip("pandas")
        pytest.importorskip("numpy")
        pytest.importorskip("sklearn")
        import stock_screener_ultra_v10 as screener

        config = screener.Config.charger()
        rm = screener.RiskManager(config)

        # Juste vérifier que la classe existe et est instanciable
        assert rm is not None


class TestIndicators:
    """Test les indicateurs techniques."""

    def test_rsi_bounds(self):
        """RSI doit être entre 0 et 100."""
        np = pytest.importorskip("numpy")
        pd = pytest.importorskip("pandas")
        pytest.importorskip("sklearn")
        import stock_screener_ultra_v10 as screener

        # Créer des données de test
        np.random.seed(42)
        prices = pd.Series(100 + np.cumsum(np.random.randn(100)))

        indic = screener.Indicateurs()
        rsi = indic.rsi(prices, 14)

        # RSI doit être dans [0, 100]
        assert rsi.dropna().min() >= 0
        assert rsi.dropna().max() <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
