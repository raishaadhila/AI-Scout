import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from main import run_pipeline
from bot import run_bot

def job():
    asyncio.run(run_pipeline())

scheduler = BackgroundScheduler(timezone="Asia/Jakarta")
scheduler.add_job(job, "cron", hour=8, minute=0)
scheduler.add_job(job, "cron", hour=16, minute=0)
scheduler.start()


print("Scheduler started. Running at 08:00 & 16:00 WIB.")
print("Bot getting ready...")
run_bot()
