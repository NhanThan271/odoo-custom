# -*- coding: utf-8 -*-
# from odoo import http


# class RestaurantTable(http.Controller):
#     @http.route('/restaurant_table/restaurant_table', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restaurant_table/restaurant_table/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restaurant_table.listing', {
#             'root': '/restaurant_table/restaurant_table',
#             'objects': http.request.env['restaurant_table.restaurant_table'].search([]),
#         })

#     @http.route('/restaurant_table/restaurant_table/objects/<model("restaurant_table.restaurant_table"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restaurant_table.object', {
#             'object': obj
#         })

