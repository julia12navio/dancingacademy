from odoo import models, fields, api

class Members(models.Model):
        _inherit = 'res.partner'  

        company_type = fields.Selection(
                selection_add=[
                        ("management_team","Management Team"),
                        ("teachers", "Teachers"),
                        ("dancers","Dancers")
                ]
        )

        classes = fields.Text()

        teachers = fields.Many2many("teachers")
