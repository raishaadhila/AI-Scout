from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def send_report(summaries: list[tuple[str, str]]):
    """summaries: list of (summary_text, url)"""
    lines = []
    for summary, url in summaries:
        lines.append(f"{summary}\n   🔗 {url}")
    message = "🤖 *AI-Scout Report*\n\n" + "\n\n".join(lines)

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=message,
        parse_mode="Markdown"
    )
    print("Report sent to Telegram.")
