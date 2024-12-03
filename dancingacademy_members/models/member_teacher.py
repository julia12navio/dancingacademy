from odoo import models, fields, api

class MemberTeacher(models.Model):
    _inherit = 'member.teacher'

    sueldo = fields.Float()    
    bank_account = fields.Char(string="Cuenta Bancaria")
    
    is_user_teacher = fields.Boolean(string="Es Profesor", compute="_compute_is_user_teacher")
    is_user_management = fields.Boolean(string="Es Management", compute="_compute_is_user_management")

    @api.depends('user_id')
    def _compute_is_user_teacher(self):
        for record in self:
            record.is_user_teacher = self.env.user.id == record.user_id.id and \
                                    self.env.user.has_group('dancingacademy_base.group_academy_teacher')

    @api.depends('user_id')
    def _compute_is_user_management(self):
        for record in self:
            record.is_user_management = self.env.user.has_group('dancingacademy_base.group_academy_management_team')
