"""
Lucky Jet – Telegram bot d'analyse statistique (prototype)
IMPORTANT:
- Ce bot ne prédit pas les prochains résultats et ne se connecte pas à 1win.
- Il calcule uniquement des fréquences observées dans l'historique fourni par l'utilisateur.
- Les fréquences passées ne garantissent pas les résultats futurs.
"""
import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def parse_values(raw: str):
    # Accepte : 1.23 2,50 200x 1.5x ; séparateurs espace, virgule, point-virgule ou retour ligne
    parts = re.split(r"[\s;]+", raw.strip())
    values = []
    for part in parts:
        part = part.lower().replace("x", "").replace(",", ".")
        part = re.sub(r"[^0-9.]", "", part)
        if not part or part == ".":
            continue
        try:
            value = float(part)
            if value >= 1:
                values.append(value)
        except ValueError:
            pass
    return values

def rate_report(values, threshold):
    hits = sum(v >= threshold for v in values)
    n = len(values)
    rate = hits / n if n else 0
    return hits, n, rate

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 ANALYSER L'HISTORIQUE", callback_data="analyse")],
        [InlineKeyboardButton("🎯 CIBLES 200×–1 200×", callback_data="targets")],
        [InlineKeyboardButton("ℹ️ À PROPOS", callback_data="about")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🚀 *LUCKY JET — ANALYSEUR STATISTIQUE*\n\n"
        "Je peux analyser les multiplicateurs que tu me transmets. "
        "Je ne suis pas connecté à 1win et je ne peux pas connaître le prochain résultat.\n\n"
        "Choisis une action ci-dessous.",
        parse_mode="Markdown", reply_markup=menu()
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "analyse":
        context.user_data["waiting_history"] = True
        await q.message.reply_text(
            "Envoie les multiplicateurs visibles dans ton historique, séparés par des espaces.\n"
            "Exemple : 1.25 2.10 1.04 3.50 12.4 1.80\n\n"
            "Plus l'échantillon est grand, plus la fréquence historique est descriptive. "
            "Cela ne rend pas le prochain tour prévisible."
        )
    elif q.data == "targets":
        await q.message.reply_text(
            "🎯 *Cibles demandées*\n"
            "200× • 300× • 500× • 800× • 1 000× • 1 200×\n\n"
            "Ces seuils sont très rares. Je peux mesurer leur fréquence dans un historique "
            "fourni, mais je ne peux pas annoncer honnêtement qu'un de ces multiplicateurs "
            "va sortir à une heure précise.", parse_mode="Markdown"
        )
    elif q.data == "about":
        await q.message.reply_text(
            "Ce prototype est un outil d'analyse descriptive. Il n'effectue aucun pari, "
            "ne lit pas automatiquement l'écran 1win et ne garantit aucun gain."
        )

async def receive_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_history"):
        await update.message.reply_text("Utilise /start pour afficher le menu.")
        return
    values = parse_values(update.message.text or "")
    context.user_data["waiting_history"] = False
    if len(values) < 10:
        await update.message.reply_text(
            f"Je n'ai trouvé que {len(values)} valeur(s). Envoie au moins 10 multiplicateurs "
            "pour obtenir un résumé descriptif."
        )
        context.user_data["waiting_history"] = True
        return

    lines = [f"📊 *Analyse de {len(values)} tours fournis*"]
    for threshold in [2, 10, 50, 100, 200, 300, 500, 800, 1000, 1200]:
        hits, n, rate = rate_report(values, threshold)
        lines.append(f"• ≥ {threshold}× : {hits}/{n} ({rate*100:.2f} % observés)")
    lines.append("")
    lines.append("⚠️ Ces pourcentages décrivent uniquement l'échantillon transmis. "
                 "Ils ne sont pas une probabilité fiable du prochain tour et ne constituent "
                 "pas un signal de pari.")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown", reply_markup=menu())

def main():
    if not TOKEN:
        raise RuntimeError("Définis la variable TELEGRAM_BOT_TOKEN avec le token BotFather.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_history))
    app.run_polling()

if __name__ == "__main__":
    main()
