import aiohttp
import logging
from config.config import Config

async def verify_invoice(invoice_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                Config.VERIFY_URL,
                params={"key": Config.UNITY_API_KEY, "invoice": invoice_id},
                ssl=True
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if "invoices" in data and data["invoices"]:
                        return data["invoices"][0]
        except Exception as e:
            logging.error(f"Error verifying invoice {invoice_id}: {e}")
        return None