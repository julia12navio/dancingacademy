from odoo import models, fields

class MemberTeacher(models.Model):
    _inherit = 'member.teacher'

    sueldo = fields.Float()    
    bank_account = fields.Char(string="Cuenta Bancaria")
                            