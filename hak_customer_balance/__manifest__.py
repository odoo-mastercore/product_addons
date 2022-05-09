# -*- coding: utf-8 -*-
{
    'name': "Partner Balance Customer/Vendor",

    'summary': """
       This module will show partner balance customer balance vendor balance on Sale order and invoice""",

    'description': """
        This module will show partner balance customer balance vendor balance on Sale order and invoice
    """,

    'author': "HAK solutions",
    'category': 'Base',
    'website': 'https://www.HAKsolutions.com/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','purchase'],

	'images': ['static/description/Banner.png'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
