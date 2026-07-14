from odoo import fields, models


class PosPayosTransaction(models.Model):
    _name = "pos.payos.transaction"
    _description = "PayOS Transaction Tracking"
    _order = "id desc"

    order_code = fields.Char(required=True, index=True)
    payment_method_id = fields.Many2one("pos.payment.method", required=True)
    payment_link_id = fields.Char()
    amount = fields.Float()
    status = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("cancelled", "Cancelled"),
            ("expired", "Expired"),
        ],
        default="pending",
        required=True,
    )
    raw_webhook_data = fields.Text()

    _sql_constraints = [
        ("order_code_unique", "unique(order_code)", "Order code phải là duy nhất."),
    ]