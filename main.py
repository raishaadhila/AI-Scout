import asyncio
from bot import send_report
from config import TELEGRAM_CHAT_ID
from news_collector import init_db, collect, get_latest_articles

async def run_pipeline():
    init_db()

    with open("keywords.txt") as f:
        keywords = [line.strip() for line in f if line.strip()]
    collect(keywords)

    articles = get_latest_articles(limit=20)
    formatted = [(f"<b>{title}</b>\n{description}", url) for _, title, description, url in articles]

    await send_report(formatted, TELEGRAM_CHAT_ID)

if __name__ == "__main__":
    asyncio.run(run_pipeline())
