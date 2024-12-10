import base64
import io
import xlsxwriter
from odoo import models, fields, api
from odoo.exceptions import UserError

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
            
    def export_attendance_to_excel(self):
        if not self:
            raise UserError("No se han seleccionado registros para exportar.")

        # Crear un buffer para el archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Informe de Asistencias')

        # Encabezados
        headers = ['Alumno', 'Clase', 'Fecha', 'Hora', 'Asistió']
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header)

        # Rellenar filas con los datos seleccionados
        row = 1
        for record in self:
            for line in record.student_ids:
                sheet.write(row, 0, line.student_name)
                sheet.write(row, 1, record.class_id.name)
                sheet.write(row, 2, record.date.strftime('%d/%m/%Y'))
                sheet.write(row, 3, record.time)
                sheet.write(row, 4, 'Sí' if line.attended else 'No')
                row += 1

        # Cerrar el archivo Excel
        workbook.close()
        output.seek(0)

        # Crear un adjunto en Odoo
        attachment = self.env['ir.attachment'].create({
            'name': 'Informe_Asistencias.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()).decode('utf-8'),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        output.close()

        # Descargar el archivo Excel
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }