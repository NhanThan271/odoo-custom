from odoo import models, fields

class RestaurantFloor(models.Model):
    _name = 'restaurant.floor'
    _description = 'Restaurant Floor'

    name = fields.Char(required=True)


class RestaurantTable(models.Model):
    _name = 'restaurant.custom.table'
    _description = 'Restaurant Table'

    name = fields.Char(required=True)
    seats = fields.Integer()
    note = fields.Text()
    floor_id = fields.Many2one('restaurant.floor', string="Floor")