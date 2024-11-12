# -*- coding: utf-8 -*-
# from odoo import http


# class DancingacademyBase(http.Controller):
#     @http.route('/dancingacademy_base/dancingacademy_base', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dancingacademy_base/dancingacademy_base/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dancingacademy_base.listing', {
#             'root': '/dancingacademy_base/dancingacademy_base',
#             'objects': http.request.env['dancingacademy_base.dancingacademy_base'].search([]),
#         })

#     @http.route('/dancingacademy_base/dancingacademy_base/objects/<model("dancingacademy_base.dancingacademy_base"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dancingacademy_base.object', {
#             'object': obj
#         })
