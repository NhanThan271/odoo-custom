# -*- coding: utf-8 -*-
{
    'name': 'Restaurant Table Management',

    'summary': 'Manage restaurant tables',

    'description': """
Restaurant table management module
    """,

    'author': 'Nhom 2',
    'website': 'http://localhost',

    'category': 'Sales',
    'version': '1.0',

    'depends': ['base',],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1
}