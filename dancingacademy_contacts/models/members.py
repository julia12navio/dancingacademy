# -*- coding: utf-8 -*-

#from odoo import models, fields, api


#class Members(models.Model):
#        _inherit = 'res.partner'  # Esto indica que estás heredando del modelo de contactos

        # Ejemplo: añadir un nuevo campo llamado 'membership_id'
#        membership_id = fields.Char(string="Membership ID")
#        is_member = fields.Boolean(string="Is a Member?", default=False)



#     _name = 'dancingacademy_contacts.dancingacademy_contacts'
#     _description = 'dancingacademy_contacts.dancingacademy_contacts'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
