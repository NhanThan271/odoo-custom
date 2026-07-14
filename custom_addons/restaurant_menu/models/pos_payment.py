from odoo import fields, models

class PosPayment(models.Model):
    _inherit = 'pos.payment'

    payos_order_code = fields.Char()
    payos_payment_link_id = fields.Char()