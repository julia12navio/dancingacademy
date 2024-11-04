from odoo import models, fields

class MemberManagementTeam(models.Model):
    _name = 'member.management.team'
    _description = 'Management Team'

    name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary(string='photo')
    phone = fields.Char()
    location = fields.Char()
    user_id = fields.Many2one('res.users', string="user", required=True, ondelete="cascade", help="User asociated with management team")
