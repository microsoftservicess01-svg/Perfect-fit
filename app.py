import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
user_data = {}

SHOP_LINKS = {
    "low": {
        "Amazon": "https://www.amazon.in/s?k=cotton+bra+women",
        "Clovia": "https://www.clovia.com/bras/"
    },
    "mid": {
        "Zivame": "https://www.zivame.com/bras.html",
        "Amazon": "https://www.amazon.in/s?k=t+shirt+bra+women"
    },
    "high": {
        "Marks & Spencer": "https://www.marksandspencer.in/lingerie",
        "Amazon": "https://www.amazon.in/s?k=premium+seamless+bra"
    }
}

KEYWORDS = {
    "size": "SIZE", "fit": "SIZE", "measure": "SIZE",
    "sports": "SPORTS", "gym": "SPORTS",
    "daily": "DAILY", "office": "DAILY",
    "comfortable": "COMFORT", "wireless": "COMFORT",
    "under 500": "LOW", "under 1000": "MID", "under 1500": "MID",
    "premium": "HIGH", "plus": "PLUS"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👙 *Perfect Fit*\n\nType things like:\n"
        "• bra size calculator\n• sports bra under 1000\n• comfortable bra",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Find My Perfect Bra 👙", callback_data="start")]
        ])
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_data[q.from_user.id] = {}
    await q.edit_message_text(
        "Choose usage:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Daily", callback_data="use_daily")],
            [InlineKeyboardButton("Sports", callback_data="use_sports")],
            [InlineKeyboardButton("Party", callback_data="use_party")]
        ])
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    for k, v in KEYWORDS.items():
        if k in text:
            await respond(update, v)
            return
    await update.message.reply_text("Try typing: *bra size* or *sports bra under 1000*", parse_mode="Markdown")

async def respond(update, flow):
    if flow == "SIZE":
        await update.message.reply_text("📏 Tap below to find your size 👇",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Start Quiz", callback_data="start")]]))

    elif flow == "SPORTS":
        await update.message.reply_text(build("Sports Bra", "mid"), parse_mode="Markdown")

    elif flow == "DAILY":
        await update.message.reply_text(build("Daily Comfort Bra", "low"), parse_mode="Markdown")

    elif flow == "COMFORT":
        await update.message.reply_text("💖 Wireless, cotton, full coverage bras recommended.", parse_mode="Markdown")

    elif flow == "LOW":
        await update.message.reply_text(build("Daily Comfort Bra", "low"), parse_mode="Markdown")

    elif flow == "MID":
        await update.message.reply_text(build("Daily Comfort Bra", "mid"), parse_mode="Markdown")

    elif flow == "HIGH":
        await update.message.reply_text(build("Premium Seamless Bra", "high"), parse_mode="Markdown")

    elif flow == "PLUS":
        await update.message.reply_text("🧍‍♀️ Plus-size tip: full coverage, wide straps.", parse_mode="Markdown")

def build(style, price):
    links = SHOP_LINKS[price]
    link_text = "\n".join([f"🔗 [{k}]({v})" for k,v in links.items()])
    return f"👙 *{style}*\n\n🛍 Shop Now:\n{link_text}"

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

if __name__ == "__main__":
    main()