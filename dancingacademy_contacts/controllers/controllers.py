# -*- coding: utf-8 -*-
# from odoo import http


# class DancingacademyContacts(http.Controller):
#     @http.route('/dancingacademy_contacts/dancingacademy_contacts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dancingacademy_contacts/dancingacademy_contacts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dancingacademy_contacts.listing', {
#             'root': '/dancingacademy_contacts/dancingacademy_contacts',
#             'objects': http.request.env['dancingacademy_contacts.dancingacademy_contacts'].search([]),
#         })

#     @http.route('/dancingacademy_contacts/dancingacademy_contacts/objects/<model("dancingacademy_contacts.dancingacademy_contacts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dancingacademy_contacts.object', {
#             'object': obj
#         })
