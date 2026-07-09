# -*- coding: utf-8 -*-
# from odoo import http


# class RestaurantMenu(http.Controller):
#     @http.route('/restaurant_menu/restaurant_menu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restaurant_menu/restaurant_menu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restaurant_menu.listing', {
#             'root': '/restaurant_menu/restaurant_menu',
#             'objects': http.request.env['restaurant_menu.restaurant_menu'].search([]),
#         })

#     @http.route('/restaurant_menu/restaurant_menu/objects/<model("restaurant_menu.restaurant_menu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restaurant_menu.object', {
#             'object': obj
#         })

