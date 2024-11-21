{
    'name': 'Dancing Academy Classes',
    'version': '1.0',
    'depends': ['dancingacademy_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/class_views.xml', 
    ],
    'assets': {
    'web.assets_frontend': [
        'dancingacademy_classes/static/src/html/video_list.html',
        'dancingacademy_classes/static/src/css/video_list.css',
        'dancingacademy_classes/static/src/js/video_list.js',
    ],
},
    'installable': True,
    'application': True,
}
