import asyncio
import discord
from discord.ext import commands
import logging
from config.config import Config
from config.constants import *
from src.database.db_handler import setup_database
from src.commands.verification import setup as setup_verification
from src.commands.public import setup as setup_public
from src.commands.admin import setup as setup_admin
from src.events.guild_events import on_guild_join
from src.events.message_events import on_message, manage_message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"Bot is ready. Logged in as {bot.user}")
    try:
        await setup_database()
        setup_verification(bot)
        setup_public(bot)
        setup_admin(bot)
        bot.add_listener(on_guild_join, 'on_guild_join')
        bot.add_listener(on_message, 'on_message')
        asyncio.create_task(manage_message(bot))
    except Exception as e:
        logging.error(f"Error during bot setup: {e}")

async def main():
    try:
        async with bot:
            await bot.start(Config.DISCORD_TOKEN)
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())