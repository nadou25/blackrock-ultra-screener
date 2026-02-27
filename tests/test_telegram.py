"""
🧪 Tests pour BlackRock Screener — Bot Telegram
Run: pytest tests/test_telegram.py -v

Tests couverts:
  - Chargement/sauvegarde de la config
  - Formatage des messages (format_stock_line, generate_section_message)
  - Envoi Telegram avec mocking (envoyer_rapport_planifie)
  - Test d'intégration réel si TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID sont définis
"""

import sys
import os
import json
import asyncio
import pytest
import tempfile
import unittest.mock as mock
from unittest.mock import AsyncMock, MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _import_telegram_bot():
    """
    Importe telegram_bot en mockant le module screener lourd
    (pandas / numpy / sklearn / etc. non-requis pour ces tests).
    """
    screener_mock = MagicMock()
    with patch.dict("sys.modules", {"stock_screener_ultra_v10": screener_mock}):
        # Forcer le rechargement si déjà chargé
        if "telegram_bot" in sys.modules:
            del sys.modules["telegram_bot"]
        import telegram_bot as tb
    return tb


def _sample_result():
    """Retourne un résultat fictif représentant un titre."""
    return {
        "symbole": "AAPL",
        "score_final": 85.5,
        "prix": 180.25,
        "decision": "ACHAT FORT",
        "action": "ACHAT FORT",
        "ratio_rr": 2.5,
        "ev_pct": 3.2,
        "stop_loss": 170.0,
        "take_profit": 195.0,
        "stop_loss_pct": -5.7,
        "take_profit_pct": 8.2,
        "kelly_used_pct": 10.0,
        "risk_score": 30,
        "secteur": "Technology",
        "marche": "NASDAQ",
        "ml_probabilite": 78,
        "ppo_action": "BUY",
        "ppo_fiabilite": 82,
        "potentiel": 12.5,
        "var_1j": 1.5,
        "var_1s": -2.1,
        "var_1m": 5.3,
        "rsi": 58,
        "beta": 1.2,
        "hurst": 0.55,
        "sharpe": 1.8,
        "blackrock_score": 88,
        "news_signal": "positive",
        "horizon_jours": 252,
        "raison": "Momentum fort, ML bullish, insider buying",
        "score_technique": 80,
        "score_fondamental": 90,
        "score_momentum": 85,
        "pe": 28.5,
        "roe": 145.0,
        "div_yield": 0.6,
        "var_hist_1d_pct": 1.2,
        "var_montecarlo_pct": 8.0,
    }


# ─── Config tests ─────────────────────────────────────────────────────────────

class TestConfig:
    """Tests pour charger_config / sauver_config."""

    def test_charger_config_default(self, tmp_path, monkeypatch):
        """Sans fichier, la config par défaut est retournée."""
        monkeypatch.setattr(
            "telegram_bot.CONFIG_FILE",
            str(tmp_path / "telegram_config_nonexistent.json"),
        )
        tb = _import_telegram_bot()
        monkeypatch.setattr(
            tb, "CONFIG_FILE",
            str(tmp_path / "telegram_config_nonexistent.json"),
        )
        cfg = tb.charger_config()
        assert isinstance(cfg, dict)
        assert cfg["chat_ids"] == []
        assert cfg["heure_rapport"] == "08:00"
        assert cfg["actif"] is True
        assert cfg["retrain_interval_days"] == 7

    def test_sauver_et_charger_config(self, tmp_path, monkeypatch):
        """Sauvegarder puis recharger la config doit retourner les mêmes données."""
        cfg_file = str(tmp_path / "telegram_config.json")
        tb = _import_telegram_bot()
        monkeypatch.setattr(tb, "CONFIG_FILE", cfg_file)

        cfg = tb.charger_config()
        cfg["chat_ids"] = [123456789, 987654321]
        cfg["heure_rapport"] = "09:30"
        tb.sauver_config(cfg)

        cfg2 = tb.charger_config()
        assert cfg2["chat_ids"] == [123456789, 987654321]
        assert cfg2["heure_rapport"] == "09:30"

    def test_enregistrer_chat(self, tmp_path, monkeypatch):
        """_enregistrer_chat doit ajouter le chat_id une seule fois."""
        cfg_file = str(tmp_path / "telegram_config.json")
        tb = _import_telegram_bot()
        monkeypatch.setattr(tb, "CONFIG_FILE", cfg_file)

        tb._enregistrer_chat(111222333)
        tb._enregistrer_chat(111222333)  # doublon → ignoré
        tb._enregistrer_chat(444555666)

        cfg = tb.charger_config()
        assert cfg["chat_ids"].count(111222333) == 1
        assert 444555666 in cfg["chat_ids"]
        assert len(cfg["chat_ids"]) == 2


# ─── Formatage messages ───────────────────────────────────────────────────────

class TestFormatStockLine:
    """Tests pour format_stock_line."""

    def test_contient_symbole(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        line = tb.format_stock_line(1, result)
        assert "AAPL" in line

    def test_contient_prix(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        line = tb.format_stock_line(1, result)
        assert "180.25" in line

    def test_contient_score(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        line = tb.format_stock_line(1, result)
        assert "85" in line  # score arrondi

    def test_emoji_achat_fort(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        result["decision"] = "ACHAT FORT"
        line = tb.format_stock_line(1, result)
        assert "🟢🟢" in line

    def test_emoji_achat(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        result["decision"] = "ACHETER"
        line = tb.format_stock_line(1, result)
        assert "🟢" in line

    def test_emoji_surveiller(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        result["decision"] = "SURVEILLER"
        line = tb.format_stock_line(1, result)
        assert "🟡" in line

    def test_emoji_vendre(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        result["decision"] = "VENDRE"
        line = tb.format_stock_line(1, result)
        assert "🔴" in line

    def test_emoji_vente_forte(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        result["decision"] = "VENTE FORTE"
        line = tb.format_stock_line(1, result)
        assert "🔴🔴" in line

    def test_html_bold(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        line = tb.format_stock_line(1, result)
        assert "<b>" in line and "</b>" in line

    def test_pe_na_quand_nul(self):
        tb = _import_telegram_bot()
        result = _sample_result()
        result["pe"] = None
        line = tb.format_stock_line(1, result)
        assert "N/A" in line


class TestGenerateSectionMessage:
    """Tests pour generate_section_message."""

    def test_aucun_signal(self):
        tb = _import_telegram_bot()
        msgs = tb.generate_section_message(
            "SCALP_MAX", "⚡ SCALP", "Court terme", [], "27/02/2026 08:00"
        )
        assert len(msgs) >= 1
        assert "Aucun signal" in msgs[0]

    def test_avec_resultats(self):
        tb = _import_telegram_bot()
        results = [_sample_result()]
        msgs = tb.generate_section_message(
            "INVESTISSEUR_1AN", "📈 INVESTISSEUR", "Long terme",
            results, "27/02/2026 08:00"
        )
        assert len(msgs) >= 1
        combined = "".join(msgs)
        assert "AAPL" in combined
        assert "RÉSUMÉ" in combined

    def test_messages_sous_4096_chars(self):
        tb = _import_telegram_bot()
        results = [_sample_result() for _ in range(10)]
        msgs = tb.generate_section_message(
            "SWING_MAX", "🔄 SWING", "Moyen terme",
            results, "27/02/2026 08:00"
        )
        for msg in msgs:
            assert len(msg) <= 4096, f"Message trop long: {len(msg)} chars"


# ─── Envoi Telegram (mocking) ─────────────────────────────────────────────────

class TestEnvoyerRapportPlanifie:
    """Tests d'envoi du rapport via Telegram avec mock."""

    @pytest.mark.asyncio
    async def test_envoi_si_chat_ids_presents(self, tmp_path, monkeypatch):
        """Le rapport doit être envoyé à chaque chat_id enregistré."""
        tb = _import_telegram_bot()
        cfg_file = str(tmp_path / "telegram_config.json")
        monkeypatch.setattr(tb, "CONFIG_FILE", cfg_file)

        # Enregistrer deux abonnés
        tb._enregistrer_chat(100)
        tb._enregistrer_chat(200)

        # Mock generate_full_report
        monkeypatch.setattr(tb, "generate_full_report", lambda: ["msg1", "msg2"])

        # Mock Application avec bot.send_message
        mock_bot = MagicMock()
        mock_bot.send_message = AsyncMock()
        mock_app = MagicMock()
        mock_app.bot = mock_bot

        await tb.envoyer_rapport_planifie(mock_app)

        # 2 abonnés × 2 messages = 4 appels
        assert mock_bot.send_message.call_count == 4

    @pytest.mark.asyncio
    async def test_pas_envoi_si_aucun_abonne(self, tmp_path, monkeypatch):
        """Sans abonné, aucun message ne doit être envoyé."""
        tb = _import_telegram_bot()
        cfg_file = str(tmp_path / "telegram_config.json")
        monkeypatch.setattr(tb, "CONFIG_FILE", cfg_file)

        mock_bot = MagicMock()
        mock_bot.send_message = AsyncMock()
        mock_app = MagicMock()
        mock_app.bot = mock_bot

        await tb.envoyer_rapport_planifie(mock_app)

        mock_bot.send_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_erreur_generation_rapport(self, tmp_path, monkeypatch):
        """Si generate_full_report plante, le bot envoie un message d'erreur."""
        tb = _import_telegram_bot()
        cfg_file = str(tmp_path / "telegram_config.json")
        monkeypatch.setattr(tb, "CONFIG_FILE", cfg_file)

        tb._enregistrer_chat(100)

        def _raise():
            raise RuntimeError("Screener down")

        monkeypatch.setattr(tb, "generate_full_report", _raise)

        mock_bot = MagicMock()
        mock_bot.send_message = AsyncMock()
        mock_app = MagicMock()
        mock_app.bot = mock_bot

        # Ne doit pas lever d'exception
        await tb.envoyer_rapport_planifie(mock_app)

        # Un message d'erreur doit être envoyé
        assert mock_bot.send_message.call_count >= 1
        call_kwargs = mock_bot.send_message.call_args_list[0]
        text_sent = call_kwargs.kwargs.get("text", "")
        if not text_sent and call_kwargs.args:
            text_sent = call_kwargs.args[1] if len(call_kwargs.args) > 1 else str(call_kwargs.args[0])
        assert "Erreur" in text_sent or "erreur" in text_sent.lower()

    @pytest.mark.asyncio
    async def test_parse_mode_html(self, tmp_path, monkeypatch):
        """Les messages doivent être envoyés avec parse_mode='HTML'."""
        tb = _import_telegram_bot()
        cfg_file = str(tmp_path / "telegram_config.json")
        monkeypatch.setattr(tb, "CONFIG_FILE", cfg_file)

        tb._enregistrer_chat(100)
        monkeypatch.setattr(tb, "generate_full_report", lambda: ["<b>Test</b>"])

        mock_bot = MagicMock()
        mock_bot.send_message = AsyncMock()
        mock_app = MagicMock()
        mock_app.bot = mock_bot

        await tb.envoyer_rapport_planifie(mock_app)

        call_kwargs = mock_bot.send_message.call_args
        assert call_kwargs.kwargs.get("parse_mode") == "HTML"

    @pytest.mark.asyncio
    async def test_date_dernier_rapport_mise_a_jour(self, tmp_path, monkeypatch):
        """Après envoi, 'dernier_rapport' doit être mis à jour dans la config."""
        tb = _import_telegram_bot()
        cfg_file = str(tmp_path / "telegram_config.json")
        monkeypatch.setattr(tb, "CONFIG_FILE", cfg_file)

        tb._enregistrer_chat(100)
        monkeypatch.setattr(tb, "generate_full_report", lambda: ["rapport"])

        mock_bot = MagicMock()
        mock_bot.send_message = AsyncMock()
        mock_app = MagicMock()
        mock_app.bot = mock_bot

        await tb.envoyer_rapport_planifie(mock_app)

        cfg = tb.charger_config()
        assert cfg["dernier_rapport"] is not None


# ─── Test de token loading ─────────────────────────────────────────────────────

class TestTokenLoading:
    """Tests pour _load_token."""

    def test_charge_depuis_env_var(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456789:ABCDefgh")
        if "telegram_bot" in sys.modules:
            del sys.modules["telegram_bot"]
        screener_mock = MagicMock()
        with patch.dict("sys.modules", {"stock_screener_ultra_v10": screener_mock}):
            import telegram_bot as tb
        # _load_token doit trouver la var d'env
        token = tb._load_token()
        assert token == "123456789:ABCDefgh"

    def test_retourne_vide_si_absent(self, monkeypatch, tmp_path):
        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        if "telegram_bot" in sys.modules:
            del sys.modules["telegram_bot"]
        screener_mock = MagicMock()
        with patch.dict("sys.modules", {"stock_screener_ultra_v10": screener_mock}):
            import telegram_bot as tb
        # Pointer vers un .env inexistant
        with patch("os.path.exists", return_value=False):
            token = tb._load_token()
        assert token == ""

    def test_charge_depuis_fichier_env(self, tmp_path, monkeypatch):
        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text('TELEGRAM_BOT_TOKEN="999:TESTTOKEN"\n')
        if "telegram_bot" in sys.modules:
            del sys.modules["telegram_bot"]
        screener_mock = MagicMock()
        with patch.dict("sys.modules", {"stock_screener_ultra_v10": screener_mock}):
            import telegram_bot as tb
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock.mock_open(read_data='TELEGRAM_BOT_TOKEN="999:TESTTOKEN"\n')):
            token = tb._load_token()
        assert token == "999:TESTTOKEN"


# ─── Test d'intégration réel (skippé si pas de credentials) ───────────────────

class TestIntegrationTelegram:
    """
    Test d'intégration réel — envoie un vrai message Telegram.
    Requis: variables d'environnement TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID.
    """

    @pytest.mark.skipif(
        not (os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID")),
        reason="TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID requis pour le test d'intégration",
    )
    @pytest.mark.asyncio
    async def test_envoi_message_reel(self):
        """Envoie un message de test réel au chat Telegram configuré."""
        from telegram import Bot
        from datetime import datetime

        token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = int(os.environ["TELEGRAM_CHAT_ID"])

        bot = Bot(token=token)
        msg = (
            f"✅ <b>TEST BlackRock Screener Bot</b>\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"🤖 Test d'intégration pytest réussi !"
        )
        result = await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
        assert result.message_id is not None
        assert result.chat.id == chat_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
