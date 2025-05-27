from discord import Embed, Guild
from config.config import Config
from config.constants import COLOR_ERROR

async def on_guild_join(guild: Guild):
    if guild.id != Config.ORIGINAL_SERVER_ID:
        embed = Embed(
            title="Bot Notice",
            description="This bot is only meant to serve Inbora Studios. It will leave this server shortly.",
            color=COLOR_ERROR
        )
        if guild.system_channel:
            await guild.system_channel.send(embed=embed)
        await guild.leave()