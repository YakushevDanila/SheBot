import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime
from config import *
from database import *
from sheets import add_row
from scheduler import setup_scheduler
from pytz import timezone

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id != ANNA_ID:
        await message.answer("⛔ Доступ только для Анны.")
        return
    await add_user(DB_PATH, message.from_user.id, message.from_user.first_name)
    await message.answer("Привет, Анна! 🌸\nБот готов к работе. Введи /смена чтобы добавить рабочий день.")

@dp.message(Command("смена"))
async def new_shift(message: types.Message):
    await message.answer("📅 Введи дату и время смены в формате:\n`12.11.2025 12:00 23:00`", parse_mode="Markdown")

@dp.message()
async def text_handler(message: types.Message):
    if message.from_user.id != ANNA_ID:
        return
    parts = message.text.split()
    # Добавление смены
    if len(parts) == 3 and ":" in parts[1]:
        date, start, end = parts
        await add_shift(DB_PATH, 1, date, start, end)
        await message.answer(f"✅ Добавлена смена {date}: {start}-{end}")
    # Добавление данных после смены
    elif len(parts) == 3 and all(p.replace('.', '', 1).isdigit() for p in parts):
        revenue, tips, hours = map(float, parts)
        today = datetime.now(timezone(TIMEZONE)).strftime("%d.%m.%Y")
        await update_shift_data(DB_PATH, 1, today, revenue, tips, hours)
        add_row(SHEET_ID, [today, revenue, tips, hours, revenue + tips])
        await message.answer("💾 Данные сохранены! Отличная работа 💪")
    else:
        await message.answer("⚠️ Непонятная команда. Попробуй /смена или введи данные: `выручка чай часы`")

async def add_daily_prompt():
    await bot.send_message(ANNA_ID, "🌙 Анна, как прошёл день? Введи `выручка чай часы`")

async def main():
    await init_db(DB_PATH)
    setup_scheduler(bot, DB_PATH, ANNA_ID, TIMEZONE, add_daily_prompt)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())