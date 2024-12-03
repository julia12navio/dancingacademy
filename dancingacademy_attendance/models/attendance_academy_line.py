from odoo import models, fields

class AttendanceAcademyLine(models.Model):
    _name = 'attendance.academy.line'
    _description = 'Detalle de Asistencia'

    attendance_id = fields.Many2one('attendance.academy', string="Attendance record", ondelete='cascade')
    student_name = fields.Char(string="Nombre del Alumno")
    attended = fields.Boolean(string="Asistió", default=False)