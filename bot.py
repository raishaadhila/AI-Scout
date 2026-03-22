from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from news_collector import get_latest_articles

async def send_report(summaries: list[tuple[str, str]], chat_id: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    chunk = []
    current_len = 0

    for summary, url in summaries:
        line = f"{summary}\n   🔗 {url}\n"
        if current_len + len(line) > 3800:
            message = "🤖 <b>AI-Scout Report</b>\n\n" + "\n".join(chunk)
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
            chunk = []
            current_len = 0
        chunk.append(line)
        current_len += len(line)

    if chunk:
        message = "🤖 <b>AI-Scout Report</b>\n\n" + "\n".join(chunk)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")

    print("Report sent to Telegram.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = get_latest_articles(limit=20)
    if not articles:
        await update.message.reply_text("Belum ada data. Tunggu jadwal scraping berikutnya.")
        return

    chunk = []
    current_len = 0
    for _, title, description, url in articles:
        line = f"<b>{title}</b>\n{description}\n   🔗 {url}\n"
        if current_len + len(line) > 3800:
            await update.message.reply_text("🤖 <b>AI-Scout Latest Data</b>\n\n" + "\n".join(chunk), parse_mode="HTML")
            chunk = []
            current_len = 0
        chunk.append(line)
        current_len += len(line)

    if chunk:
        await update.message.reply_text("🤖 <b>AI-Scout Latest Data</b>\n\n" + "\n".join(chunk), parse_mode="HTML")

def run_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot polling for messages...")
    app.run_polling()
