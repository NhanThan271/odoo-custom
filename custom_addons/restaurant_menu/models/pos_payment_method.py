from odoo import fields, models

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    payos_client_id = fields.Char("PayOS Client ID")
    payos_api_key = fields.Char("PayOS API Key")
    payos_checksum_key = fields.Char("PayOS Checksum Key")

    payos_base_url = fields.Char(
        string="PayOS Base URL",
        default="https://api-merchant.payos.vn"
    )

    def _get_payment_terminal_selection(self):
        selection = super()._get_payment_terminal_selection()
        print("BEFORE =", selection)

        selection.append(("payos", "PayOS"))

        print("AFTER =", selection)

        return selection
    
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields += [
            "payos_client_id",
            "payos_api_key",
            "payos_checksum_key",
            "payos_base_url",
        ]
        return fields