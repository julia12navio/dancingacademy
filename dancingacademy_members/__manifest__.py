# -*- coding: utf-8 -*-
{
    'name': ' Members Dancing Academy',
    'version': '1.0',
    'summary': 'Módulo para gestionar los miembros de una academia',
    'depends': ['dancingacademy_base','payment', 'base','account','product'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/menus.xml',
        'views/member_dancer_views.xml',
        'views/member_teacher_views.xml',
        'views/members_management_team_views.xml',
        'views/user_views.xml',
        'data/cron.xml'
    ],
    'application': True,
    'installable': True,
}
