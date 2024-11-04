from odoo import models, fields

class MemberTeacher(models.Model):
    _name = 'member.teacher'
    _description = 'Teacher'

    name = fields.Char()
    last_name = fields.Char()
    # class_ids = fields.Many2many('academy.class', string='Clases')
    student_ids = fields.Many2many('member.dancer', string='Dancers')
    image = fields.Binary(string='photo')
    biography = fields.Text(string='Biography')
    videos = fields.Binary(string='Videos')
    user_id = fields.Many2one('res.users', string="User", required=True, ondelete="cascade", help="User asociates with teacher")

    def open_payment_window(self):
        # Lógica para abrir ventana de pago (se podría definir en JavaScript)
        pass
