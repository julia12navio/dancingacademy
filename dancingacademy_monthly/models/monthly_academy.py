from odoo import models, fields, api

class MensualidadAcademy(models.Model):
    _name = 'monthly.academy'
    _description = 'Página de Mensualidad'

    name = fields.Char(required=True)
    student_count = fields.Integer(string="Cantidad de Alumnos")
    total_students_payment = fields.Float(string="Total Pago Alumnos")
    teacher_count = fields.Integer(string="Cantidad de Profesores")
    total_teachers_salary = fields.Float(string="Total Sueldos Profesores")
    total_monthly_costs = fields.Float(string="Costes Mensuales")
    benefit = fields.Float(string="Beneficio")

    @api.model
    def create(self, vals):
        """Sobrescribe el método de creación para calcular los valores al crear un registro."""
        vals['student_count'] = self.env['member.dancer'].search_count([])
        vals['total_students_payment'] = sum(self.env['member.dancer'].search([]).mapped('total_due'))
        vals['teacher_count'] = self.env['member.teacher'].search_count([])
        vals['total_teachers_salary'] = sum(self.env['member.teacher'].search([]).mapped('sueldo'))
        vals['total_monthly_costs'] = sum(self.env['monthly_costs.academy'].search([]).mapped('price'))
        vals['benefit'] = vals['total_students_payment'] - (
            vals['total_teachers_salary'] + vals['total_monthly_costs']
        )
        return super(MensualidadAcademy, self).create(vals)

    def write(self, vals):
        """Sobrescribe el método de escritura para recalcular los valores solo si se edita el registro."""
        if any(field in vals for field in ['name']):
            vals['student_count'] = self.env['member.dancer'].search_count([])
            vals['total_students_payment'] = sum(self.env['member.dancer'].search([]).mapped('total_due'))
            vals['teacher_count'] = self.env['member.teacher'].search_count([])
            vals['total_teachers_salary'] = sum(self.env['member.teacher'].search([]).mapped('sueldo'))
            vals['total_monthly_costs'] = sum(self.env['monthly_costs.academy'].search([]).mapped('price'))
            vals['benefit'] = vals['total_students_payment'] - (
                vals['total_teachers_salary'] + vals['total_monthly_costs']
            )
        return super(MensualidadAcademy, self).write(vals)
