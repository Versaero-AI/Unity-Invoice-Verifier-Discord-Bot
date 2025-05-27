import discord
import random
from config.config import Config
from config.constants import COLOR_INFO, WELCOME_GIF

async def on_message(message: discord.Message, bot: discord.Client):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.author.id in [member.id for member in bot.get_guild(Config.ORIGINAL_SERVER_ID).members]:
            await message.author.send("Please use commands in the server, not via DM.")
            return

    if bot.user.mentioned_in(message):
        responses = [
            f"To verify your invoice, use `+verify` or `/verify`. For more options, use `+menu` or `/menu`.",
            f"Verify your invoice with `+verify` or `/verify`. Type `+menu` or `/menu` for more info.",
            f"Use `+verify` or `/verify` to verify your invoice. Check `+menu` or `/menu` for other commands.",
        ]
        await message.channel.send(random.choice(responses))

    await bot.process_commands(message)

async def manage_message(bot: discord.Client):
    await bot.wait_until_ready()
    channel = bot.get_channel(Config.CHANNEL_ID)
    if not channel:
        print(f"Channel with ID {Config.CHANNEL_ID} not found.")
        return

    bot_message = None
    embed = discord.Embed(
        title=Config.BOT_MESSAGE_TITLE,
        description=Config.BOT_MESSAGE_DESCRIPTION,
        color=Config.BOT_MESSAGE_COLOR
    )
    embed.set_image(url=WELCOME_GIF)

    while True:
        if bot_message is None:
            bot_message = await channel.send(embed=embed)
        
        def check(message):
            return message.channel == channel and message.author != bot.user
        
        try:
            message = await bot.wait_for("message", check=check)
            if bot_message:
                await bot_message.delete()
                bot_message = None
            bot_message = await channel.send(embed=embed)
        except Exception as e:
            print(f"An error occurred in manage_message: {e}")