from odoo import models, fields, api

class AcademyClass(models.Model):
    _name = 'dancingacademy.class'
    _description = 'Class'

    name = fields.Char(required=True)
    teacher_id = fields.Many2one(
        'member.teacher', 
        string="Teacher", 
        required=True,
    )
    dancer_ids = fields.Many2many(
        'member.dancer',
        string="Dancers",
    )
    total_dancers = fields.Integer(string="Total Dancers" ,compute='_compute_total_dancers')
    price = fields.Float(string="Price")

    @api.depends('dancer_ids')
    def _compute_total_dancers(self):
        self.total_dancers = len(self.dancer_ids)
