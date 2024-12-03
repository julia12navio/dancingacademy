# -*- coding: utf-8 -*-
{
    'name': ' Members Dancing Academy',
    'version': '1.0',
    'depends': ['dancingacademy_base','payment'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/menus.xml',
        'views/member_dancer_views.xml',
        'views/member_teacher_views.xml',
        'views/members_management_team_views.xml',
        'views/user_views.xml'
    ],
    'application': True,
    'installable': True,
}
