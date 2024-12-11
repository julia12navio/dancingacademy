from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    dancer_id = fields.Many2one('member.dancer', string="Alumno", help="Alumno relacionado con esta factura.")
