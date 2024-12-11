{
    'name': 'Website Dancing Academy',
    'version': '1.0',
    'summary': 'Módulo para integrar las clases en el sitio web.',
    'author': 'Julia Navío',
    'depends': ['base', 'website', 'dancingacademy_classes'], 
    'data': [
        'security/ir.model.access.csv',
        'views/dancingacademy_website_templates.xml',
        'views/dancingacademy_website_menus.xml',
    ],
    'installable': True,
    'application': True,
}

