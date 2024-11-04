from odoo import models, fields


class MemberDancer(models.Model):
    _name = 'member.dancer'
    _description = 'Dancer'

    name = fields.Char(required=True)
    last_name = fields.Char()
    # class_ids = fields.Many2many('academy.class', string="Clases")
    teacher_ids = fields.Many2many('member.teacher', string="Teachers")
    comments = fields.Text(string="Comments")
    image = fields.Binary(string="photos")
    user_id = fields.Many2one('res.users', string="user", required=True, ondelete="cascade", help="User associated with Teacher")
