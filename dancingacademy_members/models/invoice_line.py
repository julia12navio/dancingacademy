from odoo import models, fields

class InvoiceLine(models.Model):
    _name = 'invoice.line'
    _description = 'Línea de Factura'

    date = fields.Date(string="Fecha factura", required=True, default=fields.Date.today)
    date_to_pay = fields.Date(string="Fecha de Pago")
    name = fields.Char(string="Número de Factura", required=True)
    price = fields.Float(string="Importe a pagar (€)", required=True)
    pdf_invoice = fields.Binary(string="PDF de la Factura")
    is_paid = fields.Boolean(string="Pagada", default=False)

    teacher_id = fields.Many2one('member.teacher', string="Profesor", ondelete='cascade')
