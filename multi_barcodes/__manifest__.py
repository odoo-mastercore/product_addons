# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Product Multi Barcode',
    'summary': """Allows to create multiple barcode for a single product""",
    'description': """Allows to create multiple barcode for a single product""",
    'version': '13.0.1.0.0',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://www.sinapsys.global',
    'category': 'Product',
    'depends': ['product',],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
    ],
    'images': [],
    'installable': True,
    'auto_install': False,
}
