import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TWSCRAPE_USERNAME = os.getenv("TWSCRAPE_USERNAME")
TWSCRAPE_PASSWORD = os.getenv("TWSCRAPE_PASSWORD")
TWSCRAPE_EMAIL = os.getenv("TWSCRAPE_EMAIL")
