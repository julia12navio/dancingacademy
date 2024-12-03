# -*- coding: utf-8 -*-
# from odoo import http


# class DancingacademyAttendance(http.Controller):
#     @http.route('/dancingacademy_attendance/dancingacademy_attendance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dancingacademy_attendance/dancingacademy_attendance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dancingacademy_attendance.listing', {
#             'root': '/dancingacademy_attendance/dancingacademy_attendance',
#             'objects': http.request.env['dancingacademy_attendance.dancingacademy_attendance'].search([]),
#         })

#     @http.route('/dancingacademy_attendance/dancingacademy_attendance/objects/<model("dancingacademy_attendance.dancingacademy_attendance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dancingacademy_attendance.object', {
#             'object': obj
#         })
