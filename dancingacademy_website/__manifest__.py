{
    'name': 'Dancing Academy Website',
    'version': '1.0',
    'summary': 'Website integration for Dancing Academy classes',
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

