"""
📨 TEST D'ENVOI TELEGRAM — BlackRock Screener
══════════════════════════════════════════════════════════════════════

Ce fichier teste l'envoi **réel** d'un message vers Telegram.

─── COMMENT UTILISER ───────────────────────────────────────────────

  1. Copiez .env.example vers .env et remplissez :
       TELEGRAM_BOT_TOKEN=<votre token @BotFather>
       TELEGRAM_CHAT_ID=<votre chat id>

  2. Lancez le test :
       pytest tests/test_envoi.py -v -s          # via pytest
       python  tests/test_envoi.py                # en direct

  3. Vérifiez que votre bot vous a envoyé le message sur Telegram.

─── OBTENIR SON CHAT_ID ────────────────────────────────────────────

  • Envoyez /start à votre bot
  • Ouvrez : https://api.telegram.org/bot<TOKEN>/getUpdates
  • Repérez "chat":{"id": XXXXXXX} — c'est votre TELEGRAM_CHAT_ID

══════════════════════════════════════════════════════════════════════
"""

import os
import sys
import asyncio
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─── Helper : chargement des credentials ──────────────────────────────────────

def _charger_credentials():
    """
    Charge TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID depuis :
      1. variables d'environnement
      2. fichier .env à la racine du projet
    Retourne (token, chat_id) ou ("", "") si absents.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if token and chat_id:
        return token, chat_id

    # Essayer de lire le fichier .env
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                val = val.strip().strip('"').strip("'")
                if key.strip() == "TELEGRAM_BOT_TOKEN" and not token:
                    token = val
                elif key.strip() == "TELEGRAM_CHAT_ID" and not chat_id:
                    chat_id = val

    return token, chat_id


_TOKEN, _CHAT_ID = _charger_credentials()
# Telegram bot tokens are at least 30 chars: "<bot_id>:<random_string>"
_MIN_TOKEN_LEN = 30
_CREDENTIALS_OK = bool(_TOKEN and _CHAT_ID and len(_TOKEN) >= _MIN_TOKEN_LEN and _CHAT_ID.lstrip("-").isdigit())

_SKIP_REASON = (
    "Credentials Telegram manquants. "
    "Remplissez TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID dans .env ou en variable d'environnement."
)


# ─── Tests d'envoi ────────────────────────────────────────────────────────────

class TestEnvoiTelegram:
    """Tests qui envoient de **vrais** messages Telegram."""

    @pytest.mark.skipif(not _CREDENTIALS_OK, reason=_SKIP_REASON)
    @pytest.mark.asyncio
    async def test_envoi_message_simple(self):
        """Envoie un message de test simple et vérifie la réponse."""
        from telegram import Bot
        from datetime import datetime

        bot = Bot(token=_TOKEN)
        chat_id = int(_CHAT_ID)

        texte = (
            "✅ <b>TEST D'ENVOI — BlackRock Screener</b>\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            "🤖 Envoi depuis <code>pytest tests/test_envoi.py</code>"
        )

        result = await bot.send_message(chat_id=chat_id, text=texte, parse_mode="HTML")

        assert result.message_id is not None, "Aucun message_id reçu"
        assert result.chat.id == chat_id, f"chat_id inattendu: {result.chat.id}"
        print(f"\n✅ Message envoyé — message_id={result.message_id}, chat_id={result.chat.id}")

    @pytest.mark.skipif(not _CREDENTIALS_OK, reason=_SKIP_REASON)
    @pytest.mark.asyncio
    async def test_envoi_rapport_formate(self):
        """
        Génère un mini-rapport formaté (sans screener réel) et l'envoie.
        Vérifie que le message arrive avec le bon format HTML.
        """
        from telegram import Bot
        from unittest.mock import MagicMock, patch
        from datetime import datetime

        # Importer telegram_bot sans le screener lourd
        screener_mock = MagicMock()
        with patch.dict("sys.modules", {"stock_screener_ultra_v10": screener_mock}):
            if "telegram_bot" in sys.modules:
                del sys.modules["telegram_bot"]
            import telegram_bot as tb

        # Construire un résultat fictif représentatif
        sample = {
            "symbole": "AAPL",  "score_final": 88, "prix": 182.50,
            "decision": "ACHAT FORT", "action": "ACHAT FORT",
            "ratio_rr": 2.8, "ev_pct": 4.1,
            "stop_loss": 172.0, "take_profit": 200.0,
            "stop_loss_pct": -5.8, "take_profit_pct": 9.6,
            "kelly_used_pct": 12.0, "risk_score": 25,
            "secteur": "Technology", "marche": "NASDAQ",
            "ml_probabilite": 82, "ppo_action": "BUY", "ppo_fiabilite": 85,
            "potentiel": 14.0, "var_1j": 1.8, "var_1s": -1.5, "var_1m": 6.2,
            "rsi": 61, "beta": 1.15, "hurst": 0.57, "sharpe": 2.1,
            "blackrock_score": 91, "news_signal": "positive",
            "horizon_jours": 252, "raison": "ML bullish, insider buying, breakout technique",
            "score_technique": 85, "score_fondamental": 92, "score_momentum": 87,
            "pe": 29.5, "roe": 150.0, "div_yield": 0.5,
            "var_hist_1d_pct": 1.3, "var_montecarlo_pct": 7.5,
        }

        # Générer le message de section
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        msgs = tb.generate_section_message(
            "INVESTISSEUR_1AN",
            "📈 INVESTISSEUR (1 AN) — TEST",
            "Test d'envoi depuis pytest",
            [sample],
            date_str,
        )

        bot = Bot(token=_TOKEN)
        chat_id = int(_CHAT_ID)

        # Envoyer chaque partie
        sent_ids = []
        for msg in msgs:
            result = await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
            assert result.message_id is not None
            sent_ids.append(result.message_id)

        assert len(sent_ids) > 0, "Aucun message envoyé"
        print(f"\n✅ {len(sent_ids)} message(s) envoyé(s) — ids={sent_ids}")

    @pytest.mark.skipif(not _CREDENTIALS_OK, reason=_SKIP_REASON)
    @pytest.mark.asyncio
    async def test_envoi_message_long(self):
        """
        Envoie un message proche de la limite 4096 chars
        et vérifie qu'il est accepté par Telegram.
        """
        from telegram import Bot
        from datetime import datetime

        bot = Bot(token=_TOKEN)
        chat_id = int(_CHAT_ID)

        # Construire un corps d'environ 3 900 chars pour rester sous la limite Telegram de 4 096
        _LINE_LENGTH = 80   # largeur d'une ligne de remplissage
        _LINE_COUNT = 48    # 48 × (80 + 1) ≈ 3 888 caractères
        bloc = "A" * _LINE_LENGTH + "\n"
        corps = bloc * _LINE_COUNT
        texte = (
            "🧪 <b>TEST MESSAGE LONG</b>\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            "─────────────────────────────────\n"
            + corps[:3900]
        )

        result = await bot.send_message(chat_id=chat_id, text=texte, parse_mode="HTML")

        assert result.message_id is not None
        print(f"\n✅ Message long envoyé ({len(texte)} chars) — id={result.message_id}")


# ─── Exécution directe ────────────────────────────────────────────────────────

async def _main():
    """Point d'entrée pour `python tests/test_envoi.py`."""
    print("=" * 60)
    print("  📨 TEST D'ENVOI TELEGRAM — BlackRock Screener")
    print("=" * 60)

    if not _CREDENTIALS_OK:
        print("\n❌ Credentials manquants.")
        print("   Remplissez TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID")
        print("   dans le fichier .env à la racine du projet.")
        print("\n   Exemple :")
        print("     TELEGRAM_BOT_TOKEN=123456789:ABCDefghIJKlmnoPQRstuvwXYZ")
        print("     TELEGRAM_CHAT_ID=123456789")
        return

    from telegram import Bot
    from datetime import datetime

    print(f"\n🔑 Token  : {_TOKEN[:10]}...")
    print(f"💬 Chat ID: {_CHAT_ID}")
    print("\n⏳ Envoi en cours...")

    bot = Bot(token=_TOKEN)
    chat_id = int(_CHAT_ID)

    msg = (
        "✅ <b>TEST D'ENVOI — BlackRock Screener</b>\n"
        f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        "🤖 Ce message confirme que votre bot Telegram\n"
        "   est bien configuré et peut envoyer des rapports.\n\n"
        "📌 <b>Prochaines étapes :</b>\n"
        "  1. Lancez le bot : <code>python telegram_bot.py</code>\n"
        "  2. Envoyez <code>/start</code> à votre bot\n"
        "  3. Recevez le rapport quotidien à l'heure configurée\n\n"
        "✨ <i>BlackRock Ultra Screener — Tests OK</i>"
    )

    result = await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
    print(f"\n✅ Message envoyé avec succès !")
    print(f"   message_id = {result.message_id}")
    print(f"   chat_id    = {result.chat.id}")
    print("\nVérifiez votre Telegram — vous devriez voir le message.")


if __name__ == "__main__":
    asyncio.run(_main())
