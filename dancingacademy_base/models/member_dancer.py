from odoo import models, fields, api


class MemberDancer(models.Model):
    _name = 'member.dancer'
    _description = 'Dancer'

    name = fields.Char(required=True)
    last_name = fields.Char()
    class_ids = fields.Many2many('dancingacademy.class', string="Clases")
    teacher_ids = fields.Many2many('member.teacher', string="Teachers")
    comments = fields.Text(string="Comments")
    image = fields.Binary(string="photos")
    user_id = fields.Many2one('res.users', string="user", required=True, ondelete="cascade", help="User associated with Teacher")

    mandate_reference = fields.Char(string="Referencia de Mandato")
    mandate_date = fields.Date(string="Fecha de Firma del Mandato")

    @api.onchange('class_ids')
    def _onchange_class_ids(self):
        """Update related models when class_ids changes."""
        for dancer in self:
            current_classes = dancer.class_ids
            all_teacher_ids = set()

            # Actualizar clases
            for dance_class in current_classes:
                if dancer.id not in dance_class.dancer_ids.ids:
                    dance_class.dancer_ids = [(4, dancer.id)]
                if dance_class.teacher_id:
                    all_teacher_ids.add(dance_class.teacher_id.id)
            
            # Actualizar profesores relacionados
            for teacher_id in dancer.teacher_ids.ids:
                if teacher_id not in all_teacher_ids:
                    self.env['member.teacher'].browse(teacher_id).student_ids = [(3, dancer.id)]
            dancer.teacher_ids = [(6, 0, list(all_teacher_ids))]