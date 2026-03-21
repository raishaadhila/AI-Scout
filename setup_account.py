import asyncio
import json
from twscrape import API
from config import TWSCRAPE_USERNAME, TWSCRAPE_PASSWORD, TWSCRAPE_EMAIL

async def setup():
    with open("x_cookies.json") as f:
        cookies = json.load(f)
    cookies_dict = {c["name"]: c["value"] for c in cookies}

    api = API()
    # Remove existing account first
    await api.pool.delete_accounts(TWSCRAPE_USERNAME)
    await api.pool.add_account(
        TWSCRAPE_USERNAME, TWSCRAPE_PASSWORD, TWSCRAPE_EMAIL, TWSCRAPE_PASSWORD,
        cookies=cookies_dict
    )
    await api.pool.login_all()
    print("Done. Account added with cookies.")

asyncio.run(setup())
