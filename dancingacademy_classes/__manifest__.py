{
    'name': 'Dancing Academy Classes',
    'version': '1.0',
    'depends': ['web','dancingacademy_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/class_views.xml', 
    ],
    'assets': {
        'web.assets_backend': [
            'dancingacademy_classes/static/src/js/youtube_player.js',            
            'dancingacademy_classes/static/src/css/style_classes.css',
        ],
    'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
}
