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

    # Campos calculados
    total_classes = fields.Integer(string="Clases Totales", compute="_compute_totals", store=True)
    total_students = fields.Integer(string="Alumnos Totales", compute="_compute_totals", store=True)

    @api.depends('class_ids', 'student_ids')
    def _compute_totals(self):
        """Calcula la cantidad total de clases y alumnos asociados a cada profesor."""
        for teacher in self:
            teacher.total_classes = len(teacher.class_ids)
            teacher.total_students = len(teacher.student_ids)