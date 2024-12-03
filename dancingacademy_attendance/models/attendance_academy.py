from odoo import models, fields, api
from datetime import datetime

class AttendanceAcademy(models.Model):
    _name = 'attendance.academy'
    _description = 'Attendance record'

    name = fields.Char(string="Nombre", compute="_compute_name", store=True)
    date = fields.Date(string="Fecha", required=True, default=fields.Date.context_today)
    time = fields.Char(string="Hora", required=True)
    class_id = fields.Many2one('dancingacademy.class', string="Clase", required=True)
    teacher_id = fields.Many2one('member.teacher', string="Teacher", required=True)
    student_ids = fields.One2many('attendance.academy.line', 'attendance_id', string="Lista de Asistencia")

    @api.depends('class_id', 'date', 'time')
    def _compute_name(self):
        """Genera automáticamente el nombre del registro de asistencia."""
        for record in self:
            if record.class_id and record.date and record.time:
                record.name = f"{record.class_id.name} {record.date} {record.time}"

    @api.onchange('class_id')
    def _onchange_class_id(self):
        """Sobrescribe el método create para generar automáticamente las líneas de asistencia."""
            # Obtener los estudiantes asociados a la clase
        students = self.class_id.dancer_ids
            # Crear las líneas de asistencia
        for student in students:
            self.env['attendance.academy.line'].create({
                    'attendance_id': self.id,
                    'student_name': student.name,
                })