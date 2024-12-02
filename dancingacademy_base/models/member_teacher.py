from odoo import models, fields, api

class MemberTeacher(models.Model):
    _name = 'member.teacher'
    _description = 'Teacher'

    name = fields.Char()
    last_name = fields.Char()
    phone = fields.Char()
    class_ids = fields.Many2many('dancingacademy.class', string='Clases', readonly=True)
    student_ids = fields.Many2many('member.dancer', string='Dancers', readonly=True)
    image = fields.Binary(string='photo', attachment=True)
    biography = fields.Html(string='Biography')
    user_id = fields.Many2one('res.users', string="User", required=True, ondelete="cascade", help="User asociates with teacher")

    youtube_playlist_url = fields.Char(string="YouTube Playlist URL")

