from discord import Interaction, Button, View, ButtonStyle
import discord
from src.models.modals import InvoiceVerificationModal

class VerifyView(View):
    def __init__(self, user_id: int):
        super().__init__(timeout=60)
        self.user_id = user_id

    @discord.ui.button(label="Agree and Continue", style=ButtonStyle.green)
    async def agree(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your session.", ephemeral=True)
            return
        modal = InvoiceVerificationModal()
        await interaction.response.send_modal(modal)
        await interaction.message.edit(content="Accepted Agreement. Complete the next steps.", view=None)

    @discord.ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your session.", ephemeral=True)
            return
        await interaction.message.edit(content="Verification canceled.", view=None)