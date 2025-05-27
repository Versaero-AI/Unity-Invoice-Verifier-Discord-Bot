from discord import Interaction, TextInput, Modal
from src.commands.verification import verify_modal

class InvoiceVerificationModal(Modal):
    def __init__(self):
        super().__init__(title="Invoice Verification", timeout=120)
        self.invoice_id_input = TextInput(
            label="Invoice ID/Order ID",
            placeholder="Enter your invoice/Order ID here"
        )
        self.add_item(self.invoice_id_input)

    async def on_submit(self, interaction: Interaction):
        invoice_id = self.invoice_id_input.value
        await verify_modal(interaction, invoice_id)