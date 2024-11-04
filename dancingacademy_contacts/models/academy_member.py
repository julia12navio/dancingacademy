from odoo import models, fields, api

class AcademyMember(models.Model):
    _name = 'academy.member'
    _description = 'Academy Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Nombre', required=True)
    member_type = fields.Selection([
        ('directivo', 'Equipo Directivo'),
        ('profesor', 'Profesor'),
        ('bailarin', 'Bailarín')
    ], string='Tipo de Miembro', required=True)
    user_id = fields.Many2one('res.users', string="Usuario del sistema", required=True)

    # Relaciones
    student_ids = fields.Many2many(
        'academy.member', 
        'academy_member_profesor_rel', 
        'profesor_id', 
        'student_id', 
        string='Alumnos'
    )
    professor_ids = fields.Many2many(
        'academy.member', 
        'academy_member_student_rel', 
        'student_id', 
        'profesor_id', 
        string='Profesores'
    )

    # Computed fields para roles basados en tipos de miembro
    is_directivo = fields.Boolean(string="Es del equipo directivo", compute='_compute_roles')
    is_profesor = fields.Boolean(string="Es profesor", compute='_compute_roles')
    is_bailarin = fields.Boolean(string="Es bailarín", compute='_compute_roles')

    @api.depends('member_type')
    def _compute_roles(self):
        for record in self:
            record.is_directivo = record.member_type == 'directivo'
            record.is_profesor = record.member_type == 'profesor'
            record.is_bailarin = record.member_type == 'bailarin'