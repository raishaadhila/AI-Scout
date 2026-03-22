import asyncio
import os
import sqlite3
from datetime import datetime, timezone
from twscrape import API
from config import TWSCRAPE_USERNAME, TWSCRAPE_PASSWORD, TWSCRAPE_EMAIL

DB_PATH = "scout.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id TEXT PRIMARY KEY,
            keyword TEXT,
            username TEXT,
            content TEXT,
            url TEXT,
            collected_at TEXT
        )
    """)
    con.commit()
    con.close()

def save_tweet(tweet_id, keyword, username, content, url):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT OR IGNORE INTO tweets VALUES (?, ?, ?, ?, ?, ?)",
        (tweet_id, keyword, username, content, url, datetime.now(timezone.utc).isoformat())
    )
    con.commit()
    con.close()

def get_latest_tweets(limit=20):
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT keyword, content, url FROM tweets ORDER BY collected_at DESC LIMIT ?", (limit,)
    ).fetchall()
    con.close()
    return rows

async def get_api() -> API:
    api = API()
    accounts = await api.pool.get_all()
    if not accounts:
        import json
        with open("x_cookies.json") as f:
            cookies = json.load(f)

        cookies=json.dumps({c["name"]: c["value"] for c in cookies})

        await api.pool.add_account(
            username=TWSCRAPE_USERNAME,
            password=TWSCRAPE_PASSWORD,
            email=TWSCRAPE_EMAIL,
            cookies=cookies
        )
        
        await api.pool.login_all()
        print("twscrape: account logged in.")
    return api

async def collect(keywords: list[str], tweets_per_keyword=3):
    api = await get_api()
    for kw in keywords:
        async for tweet in api.search(f"{kw} lang:en", limit=tweets_per_keyword):
            url = f"https://x.com/{tweet.user.username}/status/{tweet.id}"
            save_tweet(str(tweet.id), kw, tweet.user.username, tweet.rawContent, url)
            print(f"[{kw}] @{tweet.user.username}: {tweet.rawContent[:60]}...")

if __name__ == "__main__":
    init_db()
    with open("keywords.txt") as f:
        keywords = [line.strip() for line in f if line.strip()]
    asyncio.run(collect(keywords))
    print("Collection done.")
