import aiosqlite
import os
from datetime import datetime

DB_NAME = os.path.join("/tmp", "users.db")


async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0,
            referrals INTEGER DEFAULT 0,
            invited_by INTEGER DEFAULT 0,
            created_at TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT,
            status TEXT,
            created_at TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS payments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            photo TEXT,
            status TEXT,
            created_at TEXT
        )
        """)

        await db.commit()
        
    
async def add_user(user_id, username, invited_by=0):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (id, username, invited_by, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                invited_by,
                datetime.now().strftime("%d.%m.%Y %H:%M")
            )
        )

        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT * FROM users WHERE id=?",
            (user_id,)
        )

        return await cursor.fetchone()


async def get_balance(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT balance FROM users WHERE id=?",
            (user_id,)
        )

        result = await cursor.fetchone()

        if result:
            return result[0]

        return 0
        
        
async def set_balance(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "UPDATE users SET balance=? WHERE id=?",
            (amount, user_id)
        )

        await db.commit()


async def add_balance(user_id, amount):
    balance = await get_balance(user_id)

    new_balance = balance + amount

    await set_balance(user_id, new_balance)


async def get_referrals(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT referrals FROM users WHERE id=?",
            (user_id,)
        )

        result = await cursor.fetchone()

        if result:
            return result[0]

        return 0


async def add_referral(user_id):
    referrals = await get_referrals(user_id)

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "UPDATE users SET referrals=? WHERE id=?",
            (referrals + 1, user_id)
        )

        await db.commit()
        
        
async def add_order(user_id, service, status="⏳ Buyurtma bajarilmoqda"):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT INTO orders
            (user_id, service, status, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                service,
                status,
                datetime.now().strftime("%d.%m.%Y %H:%M")
            )
        )

        await db.commit()


async def get_orders(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT service, status
            FROM orders
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        return await cursor.fetchall()


async def update_order_status(order_id, status):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "UPDATE orders SET status=? WHERE id=?",
            (status, order_id)
        )

        await db.commit()
        
        
async def add_payment(user_id, amount, photo, status="Kutilmoqda"):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT INTO payments
            (user_id, amount, photo, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                amount,
                photo,
                status,
                datetime.now().strftime("%d.%m.%Y %H:%M")
            )
        )

        await db.commit()


async def get_last_payment(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM payments
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        return await cursor.fetchone()


async def update_payment_status(payment_id, status):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            UPDATE payments
            SET status=?
            WHERE id=?
            """,
            (status, payment_id)
        )

        await db.commit()
        
        
async def payment_exists(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT id
            FROM payments
            WHERE user_id=?
            """,
            (user_id,)
        )

        result = await cursor.fetchone()

        return result is not None


async def get_user_count():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        result = await cursor.fetchone()

        return result[0]


async def delete_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "DELETE FROM users WHERE id=?",
            (user_id,)
        )

        await db.commit()
        
        
async def clear_orders(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "DELETE FROM orders WHERE user_id=?",
            (user_id,)
        )

        await db.commit()


async def clear_payments(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "DELETE FROM payments WHERE user_id=?",
            (user_id,)
        )

        await db.commit()


async def user_exists(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT id FROM users WHERE id=?",
            (user_id,)
        )

        result = await cursor.fetchone()

        return result is not None