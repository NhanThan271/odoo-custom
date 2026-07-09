from odoo import models, api

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = vals.get('full_product_name') or 'Order Line'
        return super().create(vals_list)