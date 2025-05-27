from discord import app_commands, Interaction, Embed
from discord.ext import commands
from config.config import Config
from config.constants import COLOR_SUCCESS, COLOR_ERROR, COLOR_INFO, ACCESS_DENIED_GIF, LOADING_GIF
from src.database.db_handler import get_verified_users, delete_invoice, update_invoice_user, count_verified_invoices
import os
import sys

def setup(bot: commands.Bot):
    @bot.command()
    async def adminmenu(ctx):
        if not ctx.author.guild_permissions.administrator:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to use this command.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title="Admin Commands",
            description="Explore the bot's administrative commands to manage verified invoices and users.",
            color=COLOR_INFO
        )
        embed.add_field(
            name="`/list_verified` or `+list_verified`",
            value="**Description**\nRetrieve a list of all verified users on the server.",
            inline=False
        )
        embed.add_field(
            name="`/delete_invoice` or `+delete_invoice`",
            value="**Description**\nDelete a verified invoice by specifying its ID.",
            inline=False
        )
        embed.add_field(
            name="`/update_invoice_user` or `+update_invoice_user`",
            value="**Description**\nReassign a verified invoice to a new user by providing the invoice ID and the new user’s ID.",
            inline=False
        )
        embed.add_field(
            name="`/count_verified` or `+count_verified`",
            value="**Description**\nGet a count of all verified invoices in the system.",
            inline=False
        )
        await ctx.send(embed=embed)

    @bot.command()
    async def list_verified(ctx):
        if not ctx.author.guild_permissions.administrator:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to use this command.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await ctx.send(embed=embed)
            return

        users = await get_verified_users()
        if users:
            embed = Embed(
                title="List of Verified Users",
                description="Verified users and their respective invoice IDs:",
                color=COLOR_SUCCESS
            )
            for user_id, invoice_id in users:
                user = await bot.fetch_user(user_id)
                embed.add_field(name=f"User: {user.name}", value=f"Invoice ID: {invoice_id}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No verified users found.")

    @bot.command()
    async def delete_invoice(ctx, invoice_id: str):
        if not ctx.author.guild_permissions.administrator:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to use this command.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await ctx.send(embed=embed)
            return

        await delete_invoice(invoice_id)
        await ctx.send(f"Verified invoice with ID {invoice_id} has been deleted.")

    @bot.command()
    async def update_invoice_user(ctx, invoice_id: str, new_user_id: int):
        if not ctx.author.guild_permissions.administrator:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to use this command.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await ctx.send(embed=embed)
            return

        await update_invoice_user(invoice_id, new_user_id)
        await ctx.send(f"Verified invoice with ID {invoice_id} has been updated to user {new_user_id}.")

    @bot.command()
    async def count_verified(ctx):
        if not ctx.author.guild_permissions.administrator:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to use this command.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await ctx.send(embed=embed)
            return

        total = await count_verified_invoices()
        await ctx.send(f"Total number of verified invoices: {total}")

    @bot.command()
    async def stop(ctx):
        if ctx.author.id != Config.BOT_OWNER_ID:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to stop the bot.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title="Bot Shutdown",
            description="Shutting down the bot...",
            color=COLOR_ERROR
        )
        embed.set_image(url=LOADING_GIF)
        await ctx.send(embed=embed)
        await bot.close()

    @bot.command()
    async def restart(ctx):
        if ctx.author.id != Config.BOT_OWNER_ID:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to restart the bot.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title="Bot Restart",
            description="Restarting the bot...",
            color=COLOR_SUCCESS
        )
        embed.set_image(url=LOADING_GIF)
        await ctx.send(embed=embed)
        await bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    @bot.tree.command(name="adminmenu", description="List all admin-only commands.")
    async def slash_adminmenu(interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            embed = Embed(
                title="Permission Denied",
                description="You do not have permission to use this command.",
                color=COLOR_ERROR
            )
            embed.set_image(url=ACCESS_DENIED_GIF)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = Embed(
            title="Admin Commands",
            description="Explore the bot's administrative commands to manage verified invoices and users.",
            color=COLOR_INFO
        )
        embed.add_field(
            name="`/list_verified` or `+list_verified`",
            value="**Description**\nRetrieve a list of all verified users on the server.",
            inline=False
        )
        embed.add_field(
            name="`/delete_invoice` or `+delete_invoice`",
            value="**Description**\nDelete a verified invoice by specifying its ID.",
            inline=False
        )
        embed.add_field(
            name="`/update_invoice_user` or `+update_invoice_user`",
            value="**Description**\nReassign a verified invoice to a new user by providing the invoice ID and the new user’s ID.",
            inline=False
        )
        embed.add_field(
            name="`/count_verified` or `+count_verified`",
            value="**Description**\nGet a count of all verified invoices in the system.",
            inline=False
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="list_verified", description="List all verified users (Admin only).")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_list_verified(interaction: Interaction):
        users = await get_verified_users()
        if users:
            embed = Embed(
                title="List of Verified Users",
                description="Verified users and their respective invoice IDs:",
                color=COLOR_SUCCESS
            )
            for user_id, invoice_id in users:
                user = await bot.fetch_user(user_id)
                embed.add_field(name=f"User: {user.name}", value=f"Invoice ID: {invoice_id}", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No verified users found.")

    @bot.tree.command(name="delete_invoice", description="Delete a verified invoice (Admin only).")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_delete_invoice(interaction: Interaction, invoice_id: str):
        await delete_invoice(invoice_id)
        await interaction.response.send_message(f"Verified invoice with ID {invoice_id} has been deleted.")

    @bot.tree.command(name="update_invoice_user", description="Update a verified invoice to a new user (Admin only).")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_update_invoice_user(interaction: Interaction, invoice_id: str, new_user_id: int):
        await update_invoice_user(invoice_id, new_user_id)
        await interaction.response.send_message(f"Verified invoice with ID {invoice_id} has been updated to user {new_user_id}.")

    @bot.tree.command(name="count_verified", description="Count the total number of verified invoices (Admin only).")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_count_verified(interaction: Interaction):
        total = await count_verified_invoices()
        await interaction.response.send_message(f"Total number of verified invoices: {total}")