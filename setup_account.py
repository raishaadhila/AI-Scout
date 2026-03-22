import asyncio
import json
from twscrape import API
from config import TWSCRAPE_USERNAME, TWSCRAPE_PASSWORD, TWSCRAPE_EMAIL, TWSCRAPE_EMAIL_PASSWORD

async def setup():
    with open("x_cookies.json") as f:
        cookies = json.load(f)
    cookies_dict = {
        c['name']: c['value'].strip('"') 
        for c in cookies
    }
    
    print("Cookies keys:", list(cookies_dict.keys()))
    print("auth_token:", cookies_dict.get('auth_token', 'NOT FOUND'))
    print("ct0:", cookies_dict.get('ct0', 'NOT FOUND')[:20], "...")


    api = API()
    await api.pool.delete_accounts(TWSCRAPE_USERNAME)
    await api.pool.add_account(
        username=TWSCRAPE_USERNAME,
        password=TWSCRAPE_PASSWORD,
        email=TWSCRAPE_EMAIL,
        email_password=TWSCRAPE_EMAIL_PASSWORD,
        cookies=json.dumps(cookies_dict)
    )

    # Mark account as logged in without hitting X login endpoint
    await api.pool.set_active(TWSCRAPE_USERNAME, True)
    print("Done.")

    # Verify
    accounts = await api.pool.get_all()
    for a in accounts:
        print(f"username={a.username} active={a.active}")

asyncio.run(setup())
