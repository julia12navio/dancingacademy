{
    'name': 'Dancing Academy Classes',
    'version': '1.0',
    'depends': ['base', 'dancingacademy_members'],
    'data': [
        'security/ir.model.access.csv',
        'views/class_views.xml',  # Verifica que esta línea esté presente
    ],
    'installable': True,
    'application': True,
}
