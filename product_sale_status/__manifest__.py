# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Product Sale Status',
    'summary': """Allows display & categorize product sale status""",
    'description': """Allows display & categorize product sale status""",
    'version': '13.0.1.0.0',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://www.sinapsys.global',
    'category': 'Product',
    'depends': ['product',],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'data/sale_category_cron.xml',
        'views/product_views.xml',
        'views/product_sale_category_views.xml',
        'views/product_category_history_views.xml',
    ],
    'images': [],
    'installable': True,
    'auto_install': False,
}
