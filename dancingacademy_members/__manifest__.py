# -*- coding: utf-8 -*-
{
    'name': 'Academy Members',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/member_dancer_views.xml',
        'views/member_teacher_views.xml',
        'views/members_management_team_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dancingacademy_members/static/src/css/style.css',
        ],
    },
    'installable': True,
}
