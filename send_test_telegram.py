"""
📨 BLACKROCK SCREENER — TEST D'ENVOI TELEGRAM
══════════════════════════════════════════════
Script autonome pour vérifier votre token et envoyer un message de test
directement sur Telegram, sans lancer le bot complet.

Usage:
  python send_test_telegram.py
  python send_test_telegram.py VOTRE_TOKEN
  python send_test_telegram.py VOTRE_TOKEN VOTRE_CHAT_ID

Si TOKEN non fourni, il est lu depuis :
  1. Variable d'environnement TELEGRAM_BOT_TOKEN
  2. Fichier .env (TELEGRAM_BOT_TOKEN=...)

Si CHAT_ID non fourni, il est détecté automatiquement via getUpdates
(il faut avoir envoyé au moins un message à votre bot au préalable).
"""

import sys
import os
import json
import urllib.request
import urllib.error
from datetime import datetime


# ─── Lecture du token ────────────────────────────────────────────────────────

def _lire_env_file(path):
    """Lit le token depuis un fichier .env."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("TELEGRAM_BOT_TOKEN=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


def _charger_token():
    """Charge le token depuis variable d'env ou fichier .env."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if token:
        return token, "variable d'environnement"
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    token = _lire_env_file(env_file)
    if token:
        return token, "fichier .env"
    return "", "introuvable"


# ─── Appels HTTP Telegram ─────────────────────────────────────────────────────

def _appel_api(token, methode, params=None):
    """
    Appelle l'API Telegram Bot via HTTPS.
    Retourne (ok: bool, data: dict, erreur: str).
    """
    url = f"https://api.telegram.org/bot{token}/{methode}"
    if params:
        data = json.dumps(params).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
        )
    else:
        req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if body.get("ok"):
                return True, body.get("result"), ""
            return False, None, body.get("description", "Erreur inconnue")
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
            return False, None, body.get("description", str(e))
        except Exception:
            return False, None, str(e)
    except Exception as e:
        return False, None, str(e)


def verifier_token(token):
    """Appelle getMe pour vérifier le token. Retourne (ok, bot_info, erreur)."""
    return _appel_api(token, "getMe")


def obtenir_chat_ids(token):
    """
    Appelle getUpdates pour récupérer les chat_ids des utilisateurs
    qui ont envoyé un message au bot.
    Retourne une liste de chat_ids uniques.
    """
    ok, updates, err = _appel_api(token, "getUpdates", {"limit": 100, "timeout": 0})
    if not ok:
        return [], err
    ids = []
    for upd in (updates or []):
        msg = upd.get("message") or upd.get("edited_message") or upd.get("channel_post")
        if msg and msg.get("chat", {}).get("id"):
            cid = msg["chat"]["id"]
            if cid not in ids:
                ids.append(cid)
    return ids, ""


def envoyer_message(token, chat_id, texte):
    """Envoie un message HTML à un chat_id. Retourne (ok, erreur)."""
    ok, _, err = _appel_api(token, "sendMessage", {
        "chat_id": chat_id,
        "text": texte,
        "parse_mode": "HTML",
    })
    return ok, err


# ─── Script principal ─────────────────────────────────────────────────────────

def _masquer_token(token):
    """Retourne une version masquée du token pour affichage sécurisé."""
    if not token:
        return "****"
    parts = token.split(":", 1)
    if len(parts) == 2 and len(parts[1]) >= 3:
        return f"{parts[0]}:{'*' * (len(parts[1]) - 3)}{parts[1][-3:]}"
    if len(token) >= 4:
        return f"{'*' * (len(token) - 4)}{token[-4:]}"
    return "****"


def main():
    print()
    print("╔══════════════════════════════════════════════╗")
    print("║  📨 BLACKROCK SCREENER — TEST TELEGRAM       ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    # 1. Obtenir le token
    if len(sys.argv) >= 2:
        token = sys.argv[1]
        token_source = "argument ligne de commande"
    else:
        token, token_source = _charger_token()

    if not token:
        print("❌ ERREUR : Token Telegram non trouvé !")
        print()
        print("   Solutions :")
        print("   1. Créez un fichier .env contenant :")
        print("      TELEGRAM_BOT_TOKEN=votre_token_ici")
        print()
        print("   2. Ou lancez avec votre token en argument :")
        print("      python send_test_telegram.py VOTRE_TOKEN")
        print()
        print("   3. Ou définissez la variable d'environnement :")
        print("      set TELEGRAM_BOT_TOKEN=votre_token_ici  (Windows)")
        print("      export TELEGRAM_BOT_TOKEN=votre_token_ici  (Linux/Mac)")
        sys.exit(1)

    token_masque = _masquer_token(token)
    print(f"🔑 Token source : {token_source}")
    print(f"🔒 Token (masqué) : {token_masque}")
    print()

    # 2. Vérifier le token avec getMe
    print("🔍 Vérification du token avec Telegram...")
    ok, bot_info, err = verifier_token(token)
    if not ok:
        print(f"❌ Token invalide ou réseau inaccessible : {err}")
        print()
        print("   Vérifiez que :")
        print("   • Votre token est correct (récupérez-le via @BotFather)")
        print("   • Votre connexion internet fonctionne")
        sys.exit(1)

    bot_name = bot_info.get("first_name", "?")
    bot_username = bot_info.get("username", "?")
    print(f"✅ Token valide ! Bot : {bot_name} (@{bot_username})")
    print()

    # 3. Obtenir le(s) chat_id(s)
    if len(sys.argv) >= 3:
        try:
            chat_ids = [int(sys.argv[2])]
            print(f"🆔 Chat ID fourni en argument : {chat_ids[0]}")
        except ValueError:
            print(f"❌ Chat ID invalide : {sys.argv[2]} (doit être un nombre entier)")
            sys.exit(1)
    else:
        print("🔍 Recherche de vos chat_ids via getUpdates...")
        chat_ids, err = obtenir_chat_ids(token)
        if err:
            print(f"⚠️  Erreur getUpdates : {err}")
        if not chat_ids:
            print()
            print("⚠️  Aucun chat_id trouvé.")
            print()
            print("   → Ouvrez Telegram, cherchez @" + bot_username)
            print("   → Envoyez /start à votre bot")
            print("   → Relancez ce script")
            print()
            print("   Ou fournissez votre chat_id directement :")
            print("   python send_test_telegram.py TOKEN CHAT_ID")
            sys.exit(1)
        print(f"✅ {len(chat_ids)} chat_id(s) trouvé(s) : {chat_ids}")

    print()

    # 4. Envoyer le message de test
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message_test = (
        f"🧪 <b>MESSAGE DE TEST — BLACKROCK SCREENER</b>\n"
        f"{'─' * 32}\n"
        f"✅ Connexion Telegram : <b>OK</b>\n"
        f"🤖 Bot : {bot_name} (@{bot_username})\n"
        f"📅 Heure : {now_str}\n"
        f"{'─' * 32}\n"
        f"✅ <b>Votre bot fonctionne correctement !</b>\n"
        f"Lancez <code>python telegram_bot.py</code> pour démarrer\n"
        f"le rapport quotidien automatique."
    )

    nb_ok = 0
    nb_err = 0
    for cid in chat_ids:
        print(f"📤 Envoi vers chat_id {cid}...")
        ok, err = envoyer_message(token, cid, message_test)
        if ok:
            print(f"   ✅ Message envoyé avec succès !")
            nb_ok += 1
        else:
            print(f"   ❌ Échec : {err}")
            nb_err += 1

    print()
    print(f"{'═' * 46}")
    if nb_ok > 0:
        print(f"✅ Test réussi ! {nb_ok} message(s) envoyé(s) sur Telegram.")
    if nb_err > 0:
        print(f"⚠️  {nb_err} envoi(s) échoué(s).")
    print(f"{'═' * 46}")
    print()


if __name__ == "__main__":
    main()
