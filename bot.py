from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from twitter_search import get_latest_tweets
from gemini_summary import summarize

async def send_report(summaries: list[tuple[str, str]], chat_id: str):
    lines = []
    for summary, url in summaries:
        lines.append(f"{summary}\n   🔗 {url}")
    message = "🤖 *AI-Scout Report*\n\n" + "\n\n".join(lines)

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    print("Report sent to Telegram.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweets = get_latest_tweets(limit=20)
    if not tweets:
        await update.message.reply_text("Belum ada data. Tunggu jadwal scraping berikutnya.")
        return

    summaries = summarize(tweets)
    lines = [f"{summary}\n   🔗 {url}" for summary, url in summaries]
    message = "🤖 *AI-Scout Latest Data*\n\n" + "\n\n".join(lines)
    await update.message.reply_text(message, parse_mode="Markdown")

def run_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot polling for messages...")
    app.run_polling()
