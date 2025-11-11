import aiosqlite
from datetime import datetime

async def init_db(db_path: str):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            name TEXT
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            start_time TEXT,
            end_time TEXT,
            revenue REAL DEFAULT 0,
            tips REAL DEFAULT 0,
            hours REAL DEFAULT 0,
            filled INTEGER DEFAULT 0
        )""")
        await db.commit()

async def add_user(db_path, telegram_id, name):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
        await db.commit()

async def add_shift(db_path, user_id, date, start, end):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT INTO shifts (user_id, date, start_time, end_time) VALUES (?, ?, ?, ?)",
                         (user_id, date, start, end))
        await db.commit()

async def get_shifts_for_date(db_path, user_id, date):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM shifts WHERE user_id=? AND date=?", (user_id, date))
        return await cursor.fetchall()

async def update_shift_data(db_path, user_id, date, revenue, tips, hours):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            UPDATE shifts
            SET revenue=?, tips=?, hours=?, filled=1
            WHERE user_id=? AND date=?""", (revenue, tips, hours, user_id, date))
        await db.commit()