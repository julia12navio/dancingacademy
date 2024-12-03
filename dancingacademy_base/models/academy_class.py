from odoo import models, fields, api
from datetime import datetime, timedelta

class DancingAcademyClass(models.Model):
    _name = 'dancingacademy.class'
    _description = 'Class'

    name = fields.Char(required=True)
    teacher_id = fields.Many2one('member.teacher', string="Teacher", required=True)
    dancer_ids = fields.Many2many('member.dancer', string="Dancers")
    total_dancers = fields.Integer(string="Total Dancers", compute='_compute_total_dancers')
    price = fields.Float(string="Price")

    # Boolean fields for each day of the week
    monday = fields.Boolean(string="Monday")
    tuesday = fields.Boolean(string="Tuesday")
    wednesday = fields.Boolean(string="Wednesday")
    thursday = fields.Boolean(string="Thursday")
    friday = fields.Boolean(string="Friday")
    saturday = fields.Boolean(string="Saturday")
    sunday = fields.Boolean(string="Sunday")

    # Time fields for each day of the week
    monday_start_time = fields.Char(string="Monday Start Time")
    monday_end_time = fields.Char(string="Monday End Time")
    tuesday_start_time = fields.Char(string="Tuesday Start Time")
    tuesday_end_time = fields.Char(string="Tuesday End Time")
    wednesday_start_time = fields.Char(string="Wednesday Start Time")
    wednesday_end_time = fields.Char(string="Wednesday End Time")
    thursday_start_time = fields.Char(string="Thursday Start Time")
    thursday_end_time = fields.Char(string="Thursday End Time")
    friday_start_time = fields.Char(string="Friday Start Time")
    friday_end_time = fields.Char(string="Friday End Time")
    saturday_start_time = fields.Char(string="Saturday Start Time")
    saturday_end_time = fields.Char(string="Saturday End Time")
    sunday_start_time = fields.Char(string="Sunday Start Time")
    sunday_end_time = fields.Char(string="Sunday End Time")

    schedule_ids = fields.One2many('calendar.event', 'class_id', string='Schedules')

    is_user_dancer = fields.Boolean(string="Is User Dancer", compute="_compute_is_user_dancer")
    is_user_teacher = fields.Boolean(string="Is Current User Teacher", compute="_compute_user_is_teacher", store=False)

    @api.depends('dancer_ids')
    def _compute_is_user_dancer(self):
        for record in self:
            record.is_user_dancer = self.env.user.has_group('dancingacademy_base.group_academy_dancer')

    @api.depends('teacher_id')
    def _compute_user_is_teacher(self):
        """Determina si el usuario actual es el profesor de esta clase."""
        for record in self:
            user = self.env.user
            # Verifica si el usuario actual está relacionado con el profesor asignado
            is_teacher = self.env['member.teacher'].search([('user_id', '=', user.id)], limit=1)
            record.is_user_teacher = bool(is_teacher and is_teacher.id == record.teacher_id.id)
            
    def _update_teacher_and_students(self):
        """Actualiza relaciones entre la clase, el profesor y los alumnos."""
        for record in self:
            # Si hay un profesor asignado
            if record.teacher_id:
                # Asignar la clase al profesor
                if record.id not in record.teacher_id.class_ids.ids:
                    record.teacher_id.class_ids = [(4, record.id)]

                # Asignar los alumnos de la clase al profesor
                for dancer in record.dancer_ids:
                    if dancer.id not in record.teacher_id.student_ids.ids:
                        record.teacher_id.student_ids = [(4, dancer.id)]

            # Asignar la clase y el profesor a los alumnos
            for dancer in record.dancer_ids:
                if record.id not in dancer.class_ids.ids:
                    dancer.class_ids = [(4, record.id)]
                if record.teacher_id and record.teacher_id.id not in dancer.teacher_ids.ids:
                    dancer.teacher_ids = [(4, record.teacher_id.id)]

    @api.model
    def create(self, vals):
        """Sobrescribe create para incluir relaciones al crear una nueva clase."""
        record = super(DancingAcademyClass, self).create(vals)
        record.create_calendar_events()
        # Actualizar relaciones una vez que el registro tenga ID
        record._update_teacher_and_students()
        return record

    def write(self, vals):
        """Override write to update the schedules when timings or days change."""
        result = super(DancingAcademyClass, self).write(vals)
        affected_fields = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] + \
                        [f"{day}_start_time" for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']] + \
                        [f"{day}_end_time" for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']]
        if any(field in vals for field in affected_fields):
            self.update_calendar_events()
                # Actualizar relaciones después de guardar cambios


        for record in self:
            # Obtener todos los profesores relacionados con esta clase
            all_teachers = self.env['member.teacher'].search([('class_ids', 'in', record.id)])
            for teacher in all_teachers:
                # Si el profesor no es el asignado actual, eliminar la relación con la clase
                if teacher.id != record.teacher_id.id:
                    teacher.class_ids = [(3, record.id)]

                    # Eliminar estudiantes de este profesor si no comparten clases válidas
                    students_to_remove = teacher.student_ids.filtered(
                        lambda student: not any(class_id in teacher.class_ids.ids for class_id in student.class_ids.ids)
                    )
                    teacher.student_ids = [(3, student.id) for student in students_to_remove]

                # Validar los estudiantes asociados al profesor
                students_to_remove = teacher.student_ids.filtered(
                    lambda student: not any(class_id in teacher.class_ids.ids for class_id in student.class_ids.ids)
                )
                teacher.student_ids = [(3, student.id) for student in students_to_remove]

        self._update_teacher_and_students()
        return result


    def create_calendar_events(self):
        """Generate weekly events in the calendar for all future weeks."""
        calendar_event_obj = self.env['calendar.event']
        weekday_mapping = {
            'monday': ('monday_start_time', 'monday_end_time'),
            'tuesday': ('tuesday_start_time', 'tuesday_end_time'),
            'wednesday': ('wednesday_start_time', 'wednesday_end_time'),
            'thursday': ('thursday_start_time', 'thursday_end_time'),
            'friday': ('friday_start_time', 'friday_end_time'),
            'saturday': ('saturday_start_time', 'saturday_end_time'),
            'sunday': ('sunday_start_time', 'sunday_end_time'),
        }

        for rec in self:
            for day, times in weekday_mapping.items():
                start_time_field, end_time_field = times
                if getattr(rec, day) and getattr(rec, start_time_field) and getattr(rec, end_time_field):
                    try:
                        start_time = datetime.strptime(getattr(rec, start_time_field), '%H:%M').time()
                        end_time = datetime.strptime(getattr(rec, end_time_field), '%H:%M').time()
                    except ValueError:
                        raise ValueError(f"Invalid time format for {day}. Please use HH:MM format.")

                    today = datetime.now().date()
                    weekday_number = list(weekday_mapping.keys()).index(day)

                    # Generate events indefinitely (e.g., up to 1 years)
                    max_date = today + timedelta(days=365)
                    current_date = today

                    while current_date <= max_date:
                        start_date = current_date + timedelta(days=(weekday_number - current_date.weekday()) % 7)
                        start_datetime = datetime.combine(start_date, start_time)
                        end_datetime = datetime.combine(start_date, end_time)

                        # Create calendar event
                        calendar_event_obj.create({
                            'name': rec.name,
                            'start': start_datetime,
                            'stop': end_datetime,
                            'class_id': rec.id,
                        })

                        current_date += timedelta(weeks=1)  # Increment by one week

    def update_calendar_events(self):
        """Update calendar events based on class schedule changes."""
        for rec in self:
            rec.schedule_ids.unlink()  # Eliminar eventos existentes
            rec.create_calendar_events()

    def unlink(self):
        """Override unlink to ensure all related calendar events are removed."""
        for rec in self:
            rec.schedule_ids.unlink()  # Borra manualmente los eventos antes de eliminar la clase (si no usas `cascade`)
        return super(DancingAcademyClass, self).unlink()

    @api.depends('dancer_ids')
    def _compute_total_dancers(self):
        for rec in self:
            rec.total_dancers = len(rec.dancer_ids)
