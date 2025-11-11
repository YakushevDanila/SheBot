from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from pytz import timezone
import asyncio

def setup_scheduler(bot, db_path, anna_id, tz_str, add_daily_prompt):
    scheduler = AsyncIOScheduler(timezone=timezone(tz_str))

    # Ежедневное напоминание в 10 утра
    async def morning_reminder():
        from database import get_shifts_for_date
        today = datetime.now(timezone(tz_str)).strftime("%d.%m.%Y")
        shifts = await get_shifts_for_date(db_path, 1, today)
        if shifts:
            start = shifts[0][3]
            end = shifts[0][4]
            await bot.send_message(anna_id, f"☀️ Анна, сегодня смена с {start} до {end}. Удачного дня ❤️")

    # Вечерний запрос данных (в 23:00)
    async def evening_prompt():
        await add_daily_prompt()

    scheduler.add_job(lambda: asyncio.create_task(morning_reminder()), "cron", hour=10, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(evening_prompt()), "cron", hour=23, minute=0)
    scheduler.start()