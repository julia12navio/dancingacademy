from odoo import models, fields

class Class(models.Model):
    _name = 'dancingacademy.class'
    _description = 'Class'

    nombre = fields.Char(string="Nombre", required=True)
    profesor = fields.Many2one(
        'member.teacher', 
        string="Profesor", 
        required=True,
        help="Profesor asignado a la clase"
    )
    alumnos = fields.Many2many(
        'member.dancer',
        string="Alumnos",
        help="Alumnos que asisten a la clase"
    )
    videos = fields.Binary(string="Videos", help="Material en video de la clase")
    precio = fields.Float(string="Precio", help="Costo de la clase")