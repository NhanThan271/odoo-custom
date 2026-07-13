{
    'name': 'Restaurant Menu',

    'summary': 'Restaurant Menu Management',

    'description': 'Manage restaurant foods and drinks',

    'author': 'Nhom 2',

    'category': 'Sales',

    'version': '1.0',

    'depends': ['base', 'product', 'restaurant_table', 'point_of_sale'],

    'data': [
        'views/views.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'restaurant_menu/static/src/js/notification.js',
            'restaurant_menu/static/src/css/notification.css',
            'restaurant_menu/static/src/js/payment_notification.js',
            'restaurant_menu/static/src/js/table_notification.js',
            'restaurant_menu/static/src/js/release_table_notification.js',
        ],
    },

    'installable': True,
    'application': True,
}