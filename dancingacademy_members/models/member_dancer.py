from odoo import models, fields, api

class MemberDancer(models.Model):
    _inherit = 'member.dancer'

    total_due = fields.Float(string="Total a Pagar", compute="_compute_total_due", store=True)
    payment_method = fields.Selection([
        ('cash', 'Efectivo'),
        ('direct_debit', 'Domiciliado')
    ], string="Método de Pago", default='cash', required=True)
    bank_account = fields.Char(string="Cuenta Bancaria")
    attached_document = fields.Binary(string="Documento Adjunto")
    attached_document_name = fields.Char(string="Nombre del Documento")

    is_teacher = fields.Boolean(
            string="Es Profesor",
            compute="_compute_is_user_teacher",
            store=False
        )

    @api.depends()
    def _compute_is_user_teacher(self):
        """Calcula si el usuario actual pertenece al grupo de profesores."""
        for record in self:
            record.is_teacher = self.env.user.has_group('dancingacademy_base.group_academy_teacher')


    @api.depends('class_ids.price', 'class_ids')
    def _compute_total_due(self):
        """Calcula el total a pagar por las clases del mes actual."""
        for dancer in self:
            total = sum(dancer.class_ids.mapped('price'))
            dancer.total_due = total
