# -*- coding: utf-8 -*-
{
    'name': "dancingacademy_contacts",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/academy_security.xml',
        # 'security/ir.model.access.csv',
        # 'views/academy_menus.xml',
        # 'views/academy_member_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dancingacademy_contacts/static/src/css/style.css',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
}
