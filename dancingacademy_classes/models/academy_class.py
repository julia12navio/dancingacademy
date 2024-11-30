from odoo import models, fields

class AcademyClass(models.Model):
    _inherit = 'dancingacademy.class'

    youtube_playlist_url = fields.Char(string="YouTube Playlist URL")

    def write(self, vals):
        res = super(AcademyClass, self).write(vals)
        if 'youtube_playlist_url' in vals:  # Si cambia la URL
            return {
                'type': 'ir.actions.client',
                'tag': 'fetch_videos_action',  # Acción que el JavaScript manejará
            }
        return res
