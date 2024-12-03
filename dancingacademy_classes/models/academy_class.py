from odoo import models, fields

class AcademyClass(models.Model):
    _inherit = 'dancingacademy.class'

    youtube_playlist_url = fields.Char(string="YouTube Playlist URL")

    is_user_management = fields.Boolean(string="Es Management", compute="_compute_is_user_management")

    def _compute_is_user_management(self):
        for record in self:
            record.is_user_management = self.env.user.has_group('dancingacademy_base.group_academy_management_team')
