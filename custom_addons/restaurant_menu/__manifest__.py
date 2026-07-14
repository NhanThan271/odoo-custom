{
    'name': 'Restaurant Menu',

    'summary': 'Restaurant Menu Management',

    'description': 'Manage restaurant foods and drinks',

    'author': 'Nhom 2',

    'category': 'Sales',

    'version': '1.0',

    'depends': ['base', 'product', 'restaurant_table', 'point_of_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'restaurant_menu/static/src/js/notification.js',
            'restaurant_menu/static/src/css/notification.css',
            'restaurant_menu/static/src/js/payment_notification.js',
            'restaurant_menu/static/src/js/table_notification.js',
            'restaurant_menu/static/src/js/release_table_notification.js',
            'restaurant_menu/static/src/xml/floor_screen.xml',
            'restaurant_menu/static/src/scss/floor_screen.scss',
            "restaurant_menu/static/src/js/payment_payos.js",
            'restaurant_menu/static/src/js/payos_popup.js',
            'restaurant_menu/static/src/xml/payment_payos.xml',
            'restaurant_menu/static/src/scss/payment_payos.scss',
        ],
    },

    'installable': True,
    'application': True,
}