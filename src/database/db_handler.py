import aiosqlite
import logging
from config.config import Config

async def setup_database():
    try:
        async with aiosqlite.connect(Config.DB_NAME) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS verified_invoices (
                                invoice_id TEXT PRIMARY KEY,
                                user_id INTEGER)''')
            await db.commit()
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Error setting up database: {e}")
        raise

async def is_invoice_verified(invoice_id: str) -> bool:
    try:
        async with aiosqlite.connect(Config.DB_NAME) as db:
            async with db.execute("SELECT user_id FROM verified_invoices WHERE invoice_id = ?", (invoice_id,)) as cursor:
                return await cursor.fetchone()
    except Exception as e:
        logging.error(f"Error checking invoice {invoice_id}: {e}")
        return None

async def store_verified_invoice(invoice_id: str, user_id: int):
    try:
        async with aiosqlite.connect(Config.DB_NAME) as db:
            await db.execute("INSERT INTO verified_invoices (invoice_id, user_id) VALUES (?, ?)", (invoice_id, user_id))
            await db.commit()
        logging.info(f"Stored verified invoice {invoice_id} for user {user_id}")
    except Exception as e:
        logging.error(f"Error storing invoice {invoice_id}: {e}")
        raise

async def get_verified_users() -> list:
    try:
        async with aiosqlite.connect(Config.DB_NAME) as db:
            async with db.execute("SELECT user_id, invoice_id FROM verified_invoices") as cursor:
                return await cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching verified users: {e}")
        return []

async def delete_invoice(invoice_id: str):
    try:
        async with aiosqlite.connect(Config.DB_NAME) as db:
            await db.execute("DELETE FROM verified_invoices WHERE invoice_id = ?", (invoice_id,))
            await db.commit()
        logging.info(f"Deleted invoice {invoice_id}")
    except Exception as e:
        logging.error(f"Error deleting invoice {invoice_id}: {e}")
        raise

async def update_invoice_user(invoice_id: str, new_user_id: int):
    try:
        async with aiosqlite.connect(Config.DB_NAME) as db:
            await db.execute("UPDATE verified_invoices SET user_id = ? WHERE invoice_id = ?", (new_user_id, invoice_id))
            await db.commit()
        logging.info(f"Updated invoice {invoice_id} to user {new_user_id}")
    except Exception as e:
        logging.error(f"Error updating invoice {invoice_id}: {e}")
        raise

async def count_verified_invoices() -> int:
    try:
        async with aiosqlite.connect(Config.DB_NAME) as db:
            async with db.execute("SELECT COUNT(*) FROM verified_invoices") as cursor:
                return (await cursor.fetchone())[0]
    except Exception as e:
        logging.error(f"Error counting verified invoices: {e}")
        return 0