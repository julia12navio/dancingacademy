{
    'name': 'Mensualidades Dancing Academy',
    'version': '1.0',
    'summary': 'Gestión de mensualidades y costes mensuales en la escuela',
    'author': 'Julia Navío',
    'category': 'Custom',
    'depends': ['base', 'dancingacademy_members'],
    'data': [
        'security/ir.model.access.csv',
        'views/mensualidad_views.xml',
        'views/costes_mensuales_views.xml',
    ],
    'installable': True,
    'application': True,
}
