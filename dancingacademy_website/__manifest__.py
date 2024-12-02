{
    'name': 'Dancing Academy Website',
    'version': '1.0',
    'summary': 'Website integration for Dancing Academy classes',
    'author': 'Tu Nombre',
    'depends': ['base', 'website', 'dancingacademy_classes'],  # Agrega la dependencia de clases
    'data': [
        'views/dancingacademy_website_templates.xml',
        'views/dancingacademy_website_menus.xml',
    ],
    'installable': True,
    'application': True,
}

