import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
from src.models.modals import InvoiceVerificationModal
from src.models.views import VerifyView
from src.database.db_handler import is_invoice_verified, store_verified_invoice
from src.utils.api_client import verify_invoice
from config.config import Config
from config.constants import COLOR_SUCCESS, COLOR_ERROR, COLOR_WARNING, ACCESS_DENIED_GIF

def setup(bot: commands.Bot):
    @bot.command()
    async def verify(ctx):
        embed = Embed(
            title="Verification Terms",
            description="Click Agree to proceed or Cancel to exit.",
            color=COLOR_WARNING
        )
        view = VerifyView(user_id=ctx.author.id)
        await ctx.send(embed=embed, view=view)

    @bot.tree.command(name="verify", description="Verify your Unity Asset Store invoice.")
    async def slash_verify(interaction: Interaction):
        embed = Embed(
            title="Verification Terms",
            description="Click Agree to proceed or Cancel to exit.",
            color=COLOR_WARNING
        )
        view = VerifyView(user_id=interaction.user.id)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="verify_modal", description="Internal modal handler (not user-facing).")
    async def verify_modal(interaction: Interaction, invoice_id: str):
        await interaction.response.defer(ephemeral=True)

        if not invoice_id.isdigit():
            await interaction.followup.send(embed=Embed(
                title="Invalid Invoice ID",
                description="Invoice ID must contain only numbers.",
                color=COLOR_ERROR
            ), ephemeral=True)
            return

        existing_entry = await is_invoice_verified(invoice_id)
        if existing_entry:
            embed = Embed(
                title="Invoice Already Verified",
                description=f"Invoice ID {invoice_id} is already verified.",
                color=COLOR_ERROR
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        invoice = await verify_invoice(invoice_id)
        if invoice:
            embed = Embed(
                title="Invoice Verified",
                description="Your invoice has been verified successfully.",
                color=COLOR_SUCCESS
            )
            await store_verified_invoice(invoice_id, interaction.user.id)

            guild = interaction.guild
            role = discord.utils.get(guild.roles, id=Config.ROLE_ID)
            if role and role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                embed.add_field(name="Role Assigned", value=f"You have been assigned the **{role.name}** role.")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(embed=Embed(
                title="Verification Failed",
                description="Invoice could not be verified.",
                color=COLOR_ERROR
            ), ephemeral=True)