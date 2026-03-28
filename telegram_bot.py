"""
🤖 BLACKROCK SCREENER — TELEGRAM BOT PRO
═══════════════════════════════════════════
Envoie chaque jour à 8h00 un rapport TOP 10 pour:
  • 📈 INVESTISSEUR (1 an)
  • ⚡ SCALP / INTRADAY
  • 🔄 SWING

🔄 Re-entraîne ML + PPO automatiquement tous les 7 jours.

Bot: @nadououbot
Récupère le chat_id automatiquement.
"""

import os, sys, json, time, logging, asyncio, threading, signal, traceback
from datetime import datetime, timedelta, date

# ═══ BOT CONFIG ═══
# Token chargé depuis : 1) variable d'env  2) fichier .env  3) valeur locale
def _load_token():
    """Charge le token Telegram de façon sécurisée."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if token:
        return token
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("TELEGRAM_BOT_TOKEN=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""

BOT_TOKEN = _load_token()
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telegram_config.json")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ═══ TELEGRAM RATE LIMITS ═══
# Telegram API limits: 30 messages/second across all users, 1 message/second per user
RATE_LIMIT_DELAY_SAME_USER = 1.2  # Seconds between messages to the same user (slightly above 1s for safety)
RATE_LIMIT_DELAY_DIFFERENT_USERS = 0.1  # Seconds between messages to different users

# ═══ LOGGING ═══
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(SCRIPT_DIR, "telegram_bot.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("TelegramBot")

# ═══ CHARGER / SAUVER CONFIG LOCALE ═══
def charger_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "chat_ids": [],
        "heure_rapport": "08:00",
        "actif": True,
        "retrain_interval_days": 7,
        "last_retrain_date": None,
        "retrain_profiles": ["SCALP_MAX", "SWING_MAX", "INVESTISSEUR_1AN"],
        "dernier_rapport": None
    }

def sauver_config(cfg):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════════════
#  MOTEUR D'ANALYSE — Import du screener existant
# ═══════════════════════════════════════════════════════════════════
sys.path.insert(0, SCRIPT_DIR)

_screener_mod = None

def _get_screener():
    """Import le module screener une seule fois (lazy load)."""
    global _screener_mod
    if _screener_mod is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "screener_mod", os.path.join(SCRIPT_DIR, "stock_screener_ultra_v10.py"))
        _screener_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_screener_mod)
    return _screener_mod


def run_screener_for_profile(profile_name, top_n=10):
    """
    Lance le screener avec un profil donné, retourne le top N résultats.
    Chaque profil change l'horizon (INVESTISSEUR, SCALP, INTRADAY, SWING).
    """
    try:
        mod = _get_screener()

        # Créer config + appliquer profil
        config = mod.Config.charger()
        config.appliquer_profil(profile_name)
        config.FAST_MODE = True
        config.INCLURE_US = True
        config.INCLURE_NASDAQ100 = True
        config.INCLURE_SP500 = True
        config.MODE_PEA = False
        config.ML_MAX_SYMBOLES = 200

        # Lancer l'analyse
        moteur = mod.MoteurAnalyse(config)
        results = moteur.executer(callback=lambda s, c, t: None)

        # Trier et retourner le top N
        results.sort(key=lambda x: x.get('score_final', 0), reverse=True)
        return results[:top_n]

    except Exception as e:
        log.error(f"Erreur screener profil {profile_name}: {e}")
        traceback.print_exc()
        return []


# ═══════════════════════════════════════════════════════════════════
#  RE-ENTRAINEMENT AUTO ML + PPO (tous les 7 jours)
# ═══════════════════════════════════════════════════════════════════
def retrain_needed():
    """Vérifie si un re-entraînement est nécessaire."""
    cfg = charger_config()
    interval = cfg.get("retrain_interval_days", 7)
    last = cfg.get("last_retrain_date")
    if not last:
        return True  # jamais entraîné
    try:
        last_date = datetime.strptime(last, "%Y-%m-%d").date()
        return (date.today() - last_date).days >= interval
    except:
        return True


def run_retrain(notify_fn=None):
    """
    Re-entraîne ML et PPO pour chaque profil configuré.
    notify_fn(text) = callback async pour envoyer un message Telegram.
    """
    cfg = charger_config()
    profiles = cfg.get("retrain_profiles", ["SCALP_MAX", "SWING_MAX", "INVESTISSEUR_1AN"])
    mod = _get_screener()
    results_log = []
    t0_global = time.time()

    for profile_name in profiles:
        log.info(f"🔄 Re-entraînement pour profil {profile_name}...")
        t0 = time.time()
        try:
            config = mod.Config.charger()
            config.appliquer_profil(profile_name)
            config.FAST_MODE = False  # Force re-training complet
            config.ML_MAX_SYMBOLES = 300

            # 1. ML Re-training
            log.info(f"   🧠 ML Training ({profile_name})...")
            actions = mod.UniversActions.obtenir_actions(
                us=True, europe=True, france=True,
                gaming=True, matieres=True, crypto=False,
                mode_pea=False, inclure_pme=True,
                inclure_sante=True, inclure_nasdaq100=True, inclure_sp500=True
            )
            symboles = list(actions.keys())[:config.ML_MAX_SYMBOLES]
            ml = mod.PredicteurML(config)
            ml_ok = ml.entrainer(symboles, callback=lambda s, c, t: None)
            ml_status = "✅" if ml_ok else "⚠️"

            # 2. PPO Re-training
            ppo_status = "⏭️ Skip"
            if hasattr(mod, 'PPO_OK') and mod.PPO_OK:
                log.info(f"   🎮 PPO Training ({profile_name})...")
                ppo = mod.SystemePPO(config)
                ppo_ok, ppo_msg = ppo.entrainer(
                    symboles=symboles[:150],
                    nb_timesteps=200000,
                    callback=lambda s, c, t: None
                )
                ppo_status = "✅" if ppo_ok else f"⚠️ {ppo_msg[:50]}"
            else:
                ppo_status = "❌ PPO non dispo"

            elapsed = time.time() - t0
            results_log.append(f"  {profile_name}: ML {ml_status} | PPO {ppo_status} ({elapsed:.0f}s)")
            log.info(f"   ✅ {profile_name} terminé en {elapsed:.0f}s")

        except Exception as e:
            elapsed = time.time() - t0
            results_log.append(f"  {profile_name}: ❌ {str(e)[:80]} ({elapsed:.0f}s)")
            log.error(f"   ❌ Erreur retrain {profile_name}: {e}")

    total_time = time.time() - t0_global

    # Sauver la date du dernier re-entraînement
    cfg["last_retrain_date"] = date.today().strftime("%Y-%m-%d")
    sauver_config(cfg)

    summary = (
        f"🔄 <b>RE-ENTRAÎNEMENT ML + PPO TERMINÉ</b>\n"
        f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        f"⏱ Durée totale: {total_time/60:.0f} min\n"
        f"{'─' * 30}\n"
        + "\n".join(results_log) + "\n"
        f"{'─' * 30}\n"
        f"✅ Prochain entraînement dans {cfg.get('retrain_interval_days', 7)} jours"
    )
    log.info(f"🔄 Re-entraînement global terminé en {total_time/60:.1f} min")
    return summary


def format_stock_line(rank, r):
    """Formate une ligne PRO pour un stock dans le rapport Telegram."""
    sym = r.get('symbole', '?')
    score = r.get('score_final', 0)
    prix = r.get('prix', 0)
    decision = r.get('decision', '')
    action = r.get('action', '')
    rr = r.get('ratio_rr', 0)
    ev = r.get('ev_pct', 0)
    sl = r.get('stop_loss', 0)
    tp = r.get('take_profit', 0)
    sl_pct = abs(r.get('stop_loss_pct', 0) or 0)
    tp_pct = r.get('take_profit_pct', 0) or 0
    kelly = r.get('kelly_used_pct', 0)
    risk_s = r.get('risk_score', 0)
    secteur = r.get('secteur', '')
    marche = r.get('marche', '')
    ml_prob = r.get('ml_probabilite', 0) or 0
    ppo_act = r.get('ppo_action', 'N/A')
    ppo_fiab = r.get('ppo_fiabilite', 0) or 0
    potentiel = r.get('potentiel', 0) or 0
    var_1j = r.get('var_1j', 0) or 0
    var_1s = r.get('var_1s', 0) or 0
    var_1m = r.get('var_1m', 0) or 0
    rsi = r.get('rsi', 50) or 50
    beta = r.get('beta', 1) or 1
    hurst = r.get('hurst', 0.5) or 0.5
    sharpe = r.get('sharpe', 0) or 0
    bk_score = r.get('blackrock_score', 0) or 0
    news_signal = r.get('news_signal', '')
    horizon_j = r.get('horizon_jours', 0) or 0
    raison = r.get('raison', '')
    score_tech = r.get('score_technique', 0) or 0
    score_fonda = r.get('score_fondamental', 0) or 0
    score_mom = r.get('score_momentum', 0) or 0
    pe = r.get('pe')
    roe = r.get('roe', 0)
    div_y = r.get('div_yield', 0)
    var_1j_pct = r.get('var_hist_1d_pct', 0) or 0
    var_mc = r.get('var_montecarlo_pct', 0) or 0

    # Emoji décision
    if 'FORT' in str(decision).upper() and 'ACHET' in str(decision).upper():
        emoji = '🟢🟢'
    elif 'ACHET' in str(decision).upper():
        emoji = '🟢'
    elif 'SURVEILL' in str(decision).upper():
        emoji = '🟡'
    elif 'FORT' in str(decision).upper() and 'VEND' in str(decision).upper():
        emoji = '🔴🔴'
    elif 'VEND' in str(decision).upper():
        emoji = '🔴'
    else:
        emoji = '⚪'

    # Variation emoji
    def var_emoji(v):
        return '📈' if v > 2 else ('📉' if v < -2 else '➡️')

    # PE formaté
    pe_str = f"{pe:.1f}" if pe and pe > 0 else "N/A"

    line = (
        f"{rank}. {emoji} <b>{sym}</b>  •  <b>${prix:.2f}</b>\n"
        f"   {decision}\n"
        f"   📊 Score: <b>{score:.0f}</b>/100  (Tech {score_tech:.0f} | Fonda {score_fonda:.0f} | Mom {score_mom:.0f})\n"
        f"   🏦 BlackRock: {bk_score:.0f}  |  ML: {ml_prob:.0f}%  |  PPO: {ppo_act} ({ppo_fiab:.0f}%)\n"
        f"   🎯 SL: ${sl:.2f} (-{sl_pct:.1f}%)  →  TP: ${tp:.2f} (+{tp_pct:.1f}%)\n"
        f"   ⚖️ R:R: <b>{rr:.2f}</b>  |  EV: {ev:+.2f}%  |  Potentiel: {potentiel:+.1f}%\n"
        f"   💰 Kelly: {kelly:.1f}%  |  Risk: {risk_s:.0f}/100  |  Sharpe: {sharpe:.2f}\n"
        f"   {var_emoji(var_1j)} 1j: {var_1j:+.1f}%  |  1s: {var_1s:+.1f}%  |  1m: {var_1m:+.1f}%\n"
        f"   📐 RSI: {rsi:.0f}  |  β: {beta:.2f}  |  Hurst: {hurst:.2f}\n"
        f"   🏷 PE: {pe_str}  |  ROE: {roe:.1f}%  |  Div: {div_y:.1f}%\n"
        f"   🏢 {marche} — {secteur}\n"
        f"   💡 <i>{raison[:80]}</i>\n"
    )
    return line


def generate_section_message(profile_name, title, subtitle, results, date_str):
    """Génère un message Telegram pour une seule section/horizon."""
    msg = (
        f"{'═' * 32}\n"
        f"<b>{title}</b>\n"
        f"<i>{subtitle}</i>\n"
        f"📅 {date_str}\n"
        f"{'─' * 32}\n\n"
    )

    if not results:
        msg += "❌ Aucun signal trouvé pour cet horizon\n"
        return [msg]

    # Chaque stock est un message séparé si trop long
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(format_stock_line(i, r))

    # Stats résumé
    avg_score = sum(r.get('score_final', 0) for r in results) / len(results)
    avg_rr = sum(r.get('ratio_rr', 0) for r in results) / len(results)
    avg_ev = sum(r.get('ev_pct', 0) for r in results) / len(results)
    n_acheter = sum(1 for r in results if 'ACHAT' in r.get('action', ''))
    n_surveiller = sum(1 for r in results if r.get('action') == 'SURVEILLER')
    best = results[0]
    best_sym = best.get('symbole', '?')
    best_score = best.get('score_final', 0)

    recap = (
        f"\n{'─' * 32}\n"
        f"📊 <b>RÉSUMÉ {title}</b>\n"
        f"  🏆 Top: <b>{best_sym}</b> ({best_score:.0f}/100)\n"
        f"  📈 Score moyen: {avg_score:.0f}/100\n"
        f"  ⚖️ R:R moyen: {avg_rr:.1f}  |  EV moy: {avg_ev:+.1f}%\n"
        f"  🟢 {n_acheter} ACHAT  |  🟡 {n_surveiller} SURVEILLER  |  {len(results)} titres\n"
    )

    # Assembler en respectant limite 4096
    result_msgs = []
    current = msg
    for line in lines:
        if len(current) + len(line) + 100 > 4000:
            result_msgs.append(current)
            current = f"<b>{title}</b> (suite)\n{'─' * 32}\n\n"
        current += line + "\n"
    current += recap
    result_msgs.append(current)
    return result_msgs


def generate_full_report():
    """Génère le rapport PRO complet (3 horizons) en messages Telegram."""
    now = datetime.now()
    date_str = now.strftime('%d/%m/%Y %H:%M')
    weekday = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'][now.weekday()]

    profiles = {
        "INVESTISSEUR_1AN": ("📈 INVESTISSEUR (1 AN)", "🏦 Long terme — Qualité, Valeur & Croissance"),
        "SCALP_MAX": ("⚡ SCALP / INTRADAY", "🎯 Court terme — Momentum, Reversals & Volume"),
        "SWING_MAX": ("🔄 SWING (5-20 jours)", "📊 Moyen terme — Tendance, Smart Money & Breakouts"),
    }

    # ═══ HEADER GLOBAL ═══
    cfg = charger_config()
    last_retrain = cfg.get('last_retrain_date', 'Jamais')
    header = (
        f"🏦 <b>BLACKROCK SCREENER — RAPPORT PRO</b>\n"
        f"📅 {weekday} {date_str}\n"
        f"🔄 Dernier entraînement ML/PPO: {last_retrain}\n"
        f"{'━' * 32}\n"
        f"📌 3 horizons × Top 10 = 30 signaux\n"
        f"⚠️ Ceci n'est pas un conseil en investissement\n"
        f"{'━' * 32}\n"
    )

    all_messages = [header]
    total_buy = 0
    total_strong = 0

    for profile_name, (title, subtitle) in profiles.items():
        log.info(f"🔬 Analyse {profile_name}...")
        t0 = time.time()
        results = run_screener_for_profile(profile_name, top_n=10)
        elapsed = time.time() - t0
        log.info(f"   → {len(results)} résultats en {elapsed:.0f}s")

        total_buy += sum(1 for r in results if 'ACHAT' in r.get('action', ''))
        total_strong += sum(1 for r in results if r.get('action') == 'ACHAT FORT')

        section_msgs = generate_section_message(profile_name, title, subtitle, results, date_str)
        all_messages.extend(section_msgs)

    # ═══ FOOTER GLOBAL ═══
    footer = (
        f"\n{'━' * 32}\n"
        f"📊 <b>BILAN GLOBAL</b>\n"
        f"  🟢🟢 {total_strong} signaux ACHAT FORT\n"
        f"  🟢 {total_buy} signaux ACHAT total\n"
        f"  🔄 Prochain rapport: demain {cfg.get('heure_rapport', '08:00')}\n"
        f"{'─' * 32}\n"
        f"🤖 @nadououbot — {date_str}\n"
        f"<i>Données: Yahoo Finance | ML: Ensemble 13 modèles | RL: PPO x3</i>\n"
    )
    all_messages.append(footer)

    return all_messages


# ═══════════════════════════════════════════════════════════════════
#  TELEGRAM BOT — Async avec python-telegram-bot v20
# ═══════════════════════════════════════════════════════════════════
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /start — enregistre le chat_id automatiquement."""
    chat_id = update.effective_chat.id
    user = update.effective_user
    name = user.first_name if user else "Utilisateur"

    # Sauver le chat_id
    cfg = charger_config()
    if chat_id not in cfg["chat_ids"]:
        cfg["chat_ids"].append(chat_id)
        sauver_config(cfg)
        log.info(f"✅ Nouveau chat_id enregistré: {chat_id} ({name})")

    last_retrain = cfg.get('last_retrain_date', 'Jamais')
    interval = cfg.get('retrain_interval_days', 7)

    await update.message.reply_text(
        f"👋 Bienvenue <b>{name}</b> !\n\n"
        f"🏦 <b>BLACKROCK SCREENER BOT PRO</b>\n\n"
        f"📬 Rapport quotidien à <b>{cfg['heure_rapport']}</b> :\n"
        f"  📈 Top 10 INVESTISSEUR (1 an)\n"
        f"  ⚡ Top 10 SCALP / INTRADAY\n"
        f"  🔄 Top 10 SWING\n\n"
        f"🧠 ML: Ensemble 13 modèles\n"
        f"🎮 RL: PPO × 3 agents\n"
        f"🔄 Re-entraînement auto: tous les <b>{interval}j</b>\n"
        f"📅 Dernier training: {last_retrain}\n\n"
        f"🆔 Chat ID: <code>{chat_id}</code>\n\n"
        f"📌 <b>Commandes</b> :\n"
        f"/rapport — Rapport complet immédiat\n"
        f"/investisseur — Top 10 Investisseur\n"
        f"/scalp — Top 10 Scalp/Intraday\n"
        f"/swing — Top 10 Swing\n"
        f"/retrain — Forcer re-entraînement ML+PPO\n"
        f"/status — État du bot\n"
        f"/heure HH:MM — Changer l'heure\n",
        parse_mode='HTML'
    )


async def cmd_rapport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /rapport — envoie le rapport complet maintenant."""
    chat_id = update.effective_chat.id
    _enregistrer_chat(chat_id)

    await update.message.reply_text("⏳ Analyse en cours... (2-5 min)")
    try:
        messages = generate_full_report()
        for i, msg in enumerate(messages):
            await update.message.reply_text(msg, parse_mode='HTML')
            # Respect Telegram rate limits: 1 message/second per user
            if i < len(messages) - 1:
                await asyncio.sleep(RATE_LIMIT_DELAY_SAME_USER)
    except Exception as e:
        log.error(f"❌ Erreur cmd_rapport: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Erreur: {e}")


async def cmd_single_horizon(update: Update, context: ContextTypes.DEFAULT_TYPE, profile, title):
    """Commande pour un seul horizon."""
    chat_id = update.effective_chat.id
    _enregistrer_chat(chat_id)

    await update.message.reply_text(f"⏳ Analyse {title}...")
    try:
        results = run_screener_for_profile(profile, top_n=10)
        if not results:
            await update.message.reply_text(f"❌ Aucun signal {title}")
            return
        date_str = datetime.now().strftime('%d/%m/%Y %H:%M')
        msg = f"🏦 <b>{title}</b>\n📅 {date_str}\n{'─' * 30}\n\n"
        for i, r in enumerate(results, 1):
            msg += format_stock_line(i, r) + "\n"
        msg += f"\n🤖 @nadououbot"

        # Split si trop long
        if len(msg) <= 4096:
            await update.message.reply_text(msg, parse_mode='HTML')
        else:
            parts = [msg[i:i+4000] for i in range(0, len(msg), 4000)]
            for i, p in enumerate(parts):
                await update.message.reply_text(p, parse_mode='HTML')
                # Respect Telegram rate limits: 1 message/second per user
                if i < len(parts) - 1:
                    await asyncio.sleep(RATE_LIMIT_DELAY_SAME_USER)
    except Exception as e:
        log.error(f"❌ Erreur cmd_single_horizon: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Erreur: {e}")


async def cmd_investisseur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_single_horizon(update, context, "INVESTISSEUR_1AN", "📈 INVESTISSEUR (1 AN)")

async def cmd_scalp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_single_horizon(update, context, "SCALP_MAX", "⚡ SCALP / INTRADAY")

async def cmd_swing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_single_horizon(update, context, "SWING_MAX", "🔄 SWING")


async def cmd_retrain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /retrain — force le re-entraînement ML+PPO."""
    chat_id = update.effective_chat.id
    _enregistrer_chat(chat_id)

    await update.message.reply_text(
        "🔄 <b>Re-entraînement ML + PPO lancé...</b>\n"
        "⏳ Cela peut prendre 15-45 min.\n"
        "Vous recevrez un message quand c'est terminé.",
        parse_mode='HTML'
    )

    try:
        summary = await asyncio.get_event_loop().run_in_executor(None, run_retrain)
        await update.message.reply_text(summary, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur re-entraînement: {e}")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /status — état du bot."""
    chat_id = update.effective_chat.id
    _enregistrer_chat(chat_id)
    cfg = charger_config()

    last_retrain = cfg.get('last_retrain_date', 'Jamais')
    interval = cfg.get('retrain_interval_days', 7)
    needs_retrain = retrain_needed()

    # Vérifier modèles ML/PPO
    ml_exists = os.path.exists(os.path.join(SCRIPT_DIR, 'ml_models_cache.pkl'))
    ppo_exists = os.path.exists(os.path.join(SCRIPT_DIR, 'ppo_v5_model_0.zip'))

    await update.message.reply_text(
        f"🤖 <b>STATUS BOT PRO</b>\n\n"
        f"✅ Bot actif: {'OUI' if cfg.get('actif', True) else 'NON'}\n\n"
        f"⏰ Heure rapport: <b>{cfg.get('heure_rapport', '08:00')}</b>\n"
        f"👥 Abonnés: {len(cfg.get('chat_ids', []))}\n"
        f"📅 Dernier rapport: {cfg.get('dernier_rapport', 'Jamais')}\n\n"
        f"🧠 <b>MODÈLES</b>\n"
        f"  ML cache: {'✅' if ml_exists else '❌'}\n"
        f"  PPO modèles: {'✅' if ppo_exists else '❌'}\n"
        f"  Dernier retrain: {last_retrain}\n"
        f"  Intervalle: tous les {interval}j\n"
        f"  Retrain nécessaire: {'🔴 OUI' if needs_retrain else '🟢 NON'}\n\n"
        f"🆔 Votre ID: <code>{chat_id}</code>",
        parse_mode='HTML'
    )


async def cmd_heure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /heure HH:MM — change l'heure du rapport quotidien."""
    chat_id = update.effective_chat.id
    _enregistrer_chat(chat_id)

    if not context.args:
        await update.message.reply_text("Usage: /heure 08:00")
        return

    heure = context.args[0]
    try:
        # Valider le format
        h, m = heure.split(':')
        int(h); int(m)
        cfg = charger_config()
        cfg["heure_rapport"] = heure
        sauver_config(cfg)
        await update.message.reply_text(f"✅ Heure du rapport changée à <b>{heure}</b>", parse_mode='HTML')
    except:
        await update.message.reply_text("❌ Format invalide. Usage: /heure 08:00")


async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enregistre le chat_id lors de n'importe quel message."""
    if update.effective_chat:
        _enregistrer_chat(update.effective_chat.id)


def _enregistrer_chat(chat_id):
    """Enregistre un chat_id si pas encore connu."""
    cfg = charger_config()
    if chat_id not in cfg["chat_ids"]:
        cfg["chat_ids"].append(chat_id)
        sauver_config(cfg)
        log.info(f"✅ Chat ID enregistré: {chat_id}")


# ═══════════════════════════════════════════════════════════════════
#  ENVOI PLANIFIÉ — Rapport quotidien à l'heure configurée
# ═══════════════════════════════════════════════════════════════════
async def envoyer_rapport_planifie(app: Application):
    """Envoie le rapport à tous les abonnés."""
    cfg = charger_config()
    chat_ids = cfg.get("chat_ids", [])
    if not chat_ids:
        log.warning("⚠️ Aucun abonné — envoyez /start au bot d'abord")
        return

    log.info(f"📬 Envoi rapport planifié à {len(chat_ids)} abonné(s)...")

    try:
        messages = generate_full_report()

        for cid in chat_ids:
            try:
                for i, msg in enumerate(messages):
                    await app.bot.send_message(
                        chat_id=cid, text=msg, parse_mode='HTML')
                    # Respect Telegram rate limits: 1 message/second per user
                    if i < len(messages) - 1:
                        await asyncio.sleep(RATE_LIMIT_DELAY_SAME_USER)
                log.info(f"   ✅ Envoyé à {cid}")
            except Exception as e:
                log.error(f"   ❌ Erreur envoi à {cid}: {e}", exc_info=True)

        # Sauver la date du dernier rapport
        cfg["dernier_rapport"] = datetime.now().strftime('%d/%m/%Y %H:%M')
        sauver_config(cfg)

    except Exception as e:
        log.error(f"❌ Erreur génération rapport: {e}", exc_info=True)
        for cid in chat_ids:
            try:
                await app.bot.send_message(
                    chat_id=cid, text=f"❌ Erreur rapport: {e}")
            except:
                pass


async def scheduler_loop(app: Application):
    """Boucle principale: rapport quotidien + re-entraînement hebdo."""
    last_report_date = None
    last_retrain_check = None
    while True:
        try:
            cfg = charger_config()
            if not cfg.get("actif", True):
                await asyncio.sleep(60)
                continue

            now = datetime.now()
            today = now.date()

            # ═══ CHECK 1: RE-ENTRAÎNEMENT HEBDOMADAIRE ═══
            # Vérifie une fois par jour, à 03:00 du matin (avant le rapport)
            if (now.hour == 3 and last_retrain_check != today):
                last_retrain_check = today
                if retrain_needed():
                    log.info("🔄 Re-entraînement hebdomadaire ML+PPO lancé...")
                    chat_ids = cfg.get("chat_ids", [])

                    # Notifier le début
                    for i, cid in enumerate(chat_ids):
                        try:
                            await app.bot.send_message(
                                chat_id=cid,
                                text="🔄 <b>Re-entraînement ML + PPO en cours...</b>\n⏳ ~15-45 min",
                                parse_mode='HTML')
                            # Respect Telegram rate limits between users
                            if i < len(chat_ids) - 1:
                                await asyncio.sleep(RATE_LIMIT_DELAY_DIFFERENT_USERS)
                        except Exception as e:
                            log.error(f"❌ Erreur notification début retrain à {cid}: {e}")

                    # Lancer dans un executor (lourd, bloquant)
                    summary = await asyncio.get_event_loop().run_in_executor(None, run_retrain)

                    # Notifier la fin
                    for i, cid in enumerate(chat_ids):
                        try:
                            await app.bot.send_message(
                                chat_id=cid, text=summary, parse_mode='HTML')
                            # Respect Telegram rate limits between users
                            if i < len(chat_ids) - 1:
                                await asyncio.sleep(RATE_LIMIT_DELAY_DIFFERENT_USERS)
                        except Exception as e:
                            log.error(f"❌ Erreur notification fin retrain à {cid}: {e}")

                    log.info("🔄 Re-entraînement terminé")

            # ═══ CHECK 2: RAPPORT QUOTIDIEN ═══
            heure_target = cfg.get("heure_rapport", "08:00")
            h, m = heure_target.split(":")
            target_time = now.replace(hour=int(h), minute=int(m), second=0, microsecond=0)

            if (now >= target_time and
                last_report_date != today and
                now < target_time + timedelta(minutes=5)):

                log.info(f"⏰ C'est l'heure du rapport ({heure_target})!")
                last_report_date = today
                await envoyer_rapport_planifie(app)

        except Exception as e:
            log.error(f"Scheduler error: {e}")
            traceback.print_exc()

        await asyncio.sleep(30)  # Check toutes les 30 secondes


# ═══════════════════════════════════════════════════════════════════
#  MAIN — Lancement du bot
# ═══════════════════════════════════════════════════════════════════
def main():
    print("+" + "=" * 50 + "+")
    print("|  🤖 BLACKROCK SCREENER — BOT TELEGRAM PRO     |")
    print("|  Bot: @nadououbot                              |")
    print("|  Rapport quotidien: TOP 10 x 3 horizons       |")
    print("|  Re-entraînement ML+PPO: auto tous les 7j     |")
    print("+" + "=" * 50 + "+")
    print()

    # Vérifier le token
    if not BOT_TOKEN or len(BOT_TOKEN) < 30:
        print("❌ Token Telegram invalide!")
        return

    cfg = charger_config()
    print(f"⏰ Heure du rapport: {cfg.get('heure_rapport', '08:00')}")
    print(f"� Retrain tous les: {cfg.get('retrain_interval_days', 7)}j")
    print(f"📅 Dernier retrain: {cfg.get('last_retrain_date', 'Jamais')}")
    print(f"�👥 Abonnés: {len(cfg.get('chat_ids', []))}")
    print(f"📌 Envoyez /start à @nadououbot pour vous abonner")
    print()

    # Construire l'application
    app = Application.builder().token(BOT_TOKEN).build()

    # Commandes
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("rapport", cmd_rapport))
    app.add_handler(CommandHandler("investisseur", cmd_investisseur))
    app.add_handler(CommandHandler("scalp", cmd_scalp))
    app.add_handler(CommandHandler("swing", cmd_swing))
    app.add_handler(CommandHandler("retrain", cmd_retrain))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("heure", cmd_heure))

    # Capturer tout message pour auto-enregistrer le chat_id
    app.add_handler(MessageHandler(filters.ALL, handle_any_message))

    # Lancer le scheduler en tâche de fond
    async def post_init(application: Application):
        asyncio.create_task(scheduler_loop(application))

    app.post_init = post_init

    log.info("🚀 Bot démarré — polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
