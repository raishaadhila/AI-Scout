import sqlite3
from datetime import datetime, timezone
from newsapi import NewsApiClient
from config import NEWSAPI_KEY

DB_PATH = "scout.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            keyword TEXT,
            source TEXT,
            title TEXT,
            description TEXT,
            url TEXT,
            published_at TEXT,
            collected_at TEXT
        )
    """)
    con.commit()
    con.close()

def save_article(article_id, keyword, source, title, description, url, published_at):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (article_id, keyword, source, title, description, url, published_at,
         datetime.now(timezone.utc).isoformat())
    )
    con.commit()
    con.close()

def get_latest_articles(limit=20):
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT keyword, title, description, url FROM articles ORDER BY collected_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    con.close()
    return rows

def collect(keywords: list[str], articles_per_keyword=5):
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    for kw in keywords:
        response = newsapi.get_everything(
            q=kw,
            language="en",
            sort_by="publishedAt",
            page_size=articles_per_keyword
        )

        if response["status"] != "ok":
            print(f"[{kw}] Error: {response}")
            continue

        for article in response["articles"]:
            url = article["url"]
            article_id = url  # URL as unique ID
            source = article["source"]["name"]
            title = article["title"] or ""
            description = article["description"] or ""
            published_at = article["publishedAt"] or ""

            save_article(article_id, kw, source, title, description, url, published_at)
            print(f"[{kw}] {source}: {title[:60]}...")

if __name__ == "__main__":
    init_db()
    with open("keywords.txt") as f:
        keywords = [line.strip() for line in f if line.strip()]
    collect(keywords)
    print("Collection done.")