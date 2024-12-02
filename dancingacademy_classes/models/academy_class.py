from odoo import models, fields

class AcademyClass(models.Model):
    _inherit = 'dancingacademy.class'

    youtube_playlist_url = fields.Char(string="YouTube Playlist URL")

