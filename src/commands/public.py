from discord import app_commands, Interaction, Embed
from discord.ext import commands
from config.constants import COLOR_INFO, ACCESS_DENIED_GIF

def setup(bot: commands.Bot):
    @bot.command()
    async def menu(ctx):
        embed = Embed(
            title="All Commands",
            description="Explore the bot's functionality with these detailed commands. Use them wisely to interact with the bot and manage tasks effectively:",
            color=COLOR_INFO
        )
        embed.add_field(
            name="`/verify` or `+verify`",
            value="**Description**\nSubmit your Unity Asset Store invoice for verification to gain necessary permissions or access.",
            inline=False
        )
        embed.add_field(
            name="`/menu` or `+menu`",
            value="**Description**\nView this list of commands with detailed descriptions.",
            inline=False
        )
        await ctx.send(embed=embed)

    @bot.tree.command(name="menu", description="List all available commands.")
    async def slash_menu(interaction: Interaction):
        embed = Embed(
            title="All Commands",
            description="Explore the bot's functionality with these detailed commands. Use them wisely to interact with the bot and manage tasks effectively:",
            color=COLOR_INFO
        )
        embed.add_field(
            name="`/verify` or `+verify`",
            value="**Description**\nSubmit your Unity Asset Store invoice for verification to gain necessary permissions or access.",
            inline=False
        )
        embed.add_field(
            name="`/menu` or `+menu`",
            value="**Description**\nView this list of commands with detailed descriptions.",
            inline=False
        )
        await interaction.response.send_message(embed=embed)