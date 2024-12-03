{
    'name': 'Asistencia Dancing Academy',
    'version': '1.0',
    'summary': 'Módulo para gestionar la asistencia de clases',
    'description': """
        Este módulo permite a los profesores registrar la asistencia de los alumnos para cada clase. 
        Incluye funcionalidades para seleccionar fecha, hora, clase, y alumnos asociados, 
        así como registrar quién asistió.""",
    'author': 'Julia Navío',
    'category': 'Education',
    'depends': ['base', 'dancingacademy_members'],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
