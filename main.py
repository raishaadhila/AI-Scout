import asyncio
from twitter_search import init_db, collect, get_latest_tweets
from gemini_summary import summarize
from bot import send_report
from config import TELEGRAM_CHAT_ID

async def run_pipeline():
    # 1. Init DB
    init_db()

    # 2. Collect tweets
    with open("keywords.txt") as f:
        keywords = [line.strip() for line in f if line.strip()]
    await collect(keywords)

    # 3. Summarize with Gemini
    tweets = get_latest_tweets(limit=20)
    summaries = summarize(tweets)

    # 4. Send to Telegram
    await send_report(summaries, TELEGRAM_CHAT_ID)

if __name__ == "__main__":
    asyncio.run(run_pipeline())
