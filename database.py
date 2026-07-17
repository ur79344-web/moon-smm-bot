import aiosqlite
import os

DB_NAME = os.path.join("/tmp", "users.db")


async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0
        )
        """)
        await db.commit()


async def add_user(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users(id, username) VALUES(?, ?)",
            (user_id, username)
        )
        await db.commit()


async def get_balance(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT balance FROM users WHERE id=?",
            (user_id,)
        )

        row = await cursor.fetchone()

        if row:
            return row[0]

        return 0


async def update_balance(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET balance=? WHERE id=?",
            (amount, user_id)
        )
        await db.commit()