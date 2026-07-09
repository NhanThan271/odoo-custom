from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_restaurant_food = fields.Boolean(
        string='Restaurant Food',
        default=True
    )

    food_category = fields.Selection([
        ('food', 'Food'),
        ('drink', 'Drink'),
        ('dessert', 'Dessert')
    ],
    string='Food Category'
    )

    spicy_level = fields.Selection([
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('hot', 'Hot')
    ],
    string='Spicy Level'
    )

    cooking_time = fields.Integer(
        string='Cooking Time (minutes)'
    )

    description_food = fields.Text(
        string='Food Description'
    )