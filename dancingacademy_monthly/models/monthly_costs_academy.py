from odoo import models, fields

class MonthlyCosts(models.Model):
    _name = 'monthly_costs.academy'
    _description = 'Costes Mensuales'

    name = fields.Char(string="Nombre del Coste", required=True)
    price = fields.Float(string="Precio", required=True)
