from odoo import models, fields

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    class_id = fields.Many2one(
        'dancingacademy.class', 
        string="Class", 
        ondelete="cascade"  # Borra los eventos si se elimina la clase asociada
    )
