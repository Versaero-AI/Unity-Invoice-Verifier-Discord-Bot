import os
from dotenv import load_dotenv

load_dotenv()

# Configuration loaded from environment variables
class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    UNITY_API_KEY = os.getenv("UNITY_API_KEY")
    ROLE_ID = int(os.getenv("ROLE_ID"))
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
    ORIGINAL_SERVER_ID = int(os.getenv("ORIGINAL_SERVER_ID"))
    BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "1166748594896900126"))
    DB_NAME = "verified_invoices.db"
    VERIFY_URL = "https://api.assetstore.unity3d.com/publisher/v1/invoice/verify.json"