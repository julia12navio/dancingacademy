# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class dancingacademy_classes(models.Model):
#     _name = 'dancingacademy_classes.dancingacademy_classes'
#     _description = 'dancingacademy_classes.dancingacademy_classes'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
