# -*- coding: utf-8 -*-
{
    'name': 'Base Dancing Academy',
    'version': '1.0',
    'depends': ['base', 'calendar'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'dancingacademy_base/static/src/css/style.css',
        ],
    },
    'installable': True,
}
