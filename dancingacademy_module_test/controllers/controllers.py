# -*- coding: utf-8 -*-
# from odoo import http


# class DancingacademyModuleTest(http.Controller):
#     @http.route('/dancingacademy_module_test/dancingacademy_module_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dancingacademy_module_test/dancingacademy_module_test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dancingacademy_module_test.listing', {
#             'root': '/dancingacademy_module_test/dancingacademy_module_test',
#             'objects': http.request.env['dancingacademy_module_test.dancingacademy_module_test'].search([]),
#         })

#     @http.route('/dancingacademy_module_test/dancingacademy_module_test/objects/<model("dancingacademy_module_test.dancingacademy_module_test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dancingacademy_module_test.object', {
#             'object': obj
#         })
