from odoo import models, fields

class Members(models.Model):
        _inherit = 'res.partner'  

        # type_member = fields.Selection(
        #          selection=[
        #                  ('management_team','Management Team'),
        #                  ('teachers', 'Teachers'),
        #                  ('dancers','Dancers')]
        #          )

        # # Campo para identificar si es un profesor o bailarín
        # contact_type = fields.Selection(
        #         [('profesor', 'Profesor'), ('bailarin', 'Bailarín')],
        #         string="Tipo de Contacto"
        # )

        # # Relación profesor-alumno (muchos a muchos)
        # student_ids = fields.Many2many(
        # 'res.partner', 
        # 'profesor_alumno_rel',  # Tabla relacional para profesor-alumno
        # 'profesor_id',          # Nombre de la columna para profesor
        # 'alumno_id',            # Nombre de la columna para alumno
        # string="Alumnos", 
        # domain=[('contact_type', '=', 'bailarin')]
        # )

        # # Relación alumno-profesor (muchos a muchos inversa)
        # teacher_ids = fields.Many2many(
        # 'res.partner', 
        # 'alumno_profesor_rel',  # Una tabla relacional diferente para alumno-profesor
        # 'alumno_id',            # Nombre de la columna para alumno
        # 'profesor_id',          # Nombre de la columna para profesor
        # string="Profesores", 
        # domain=[('contact_type', '=', 'profesor')]
        # )

