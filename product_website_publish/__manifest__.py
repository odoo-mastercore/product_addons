# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Product Website Published',
    'version': '13.0.0.1',
    'summary': 'Add button to published product in product form and massive published',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://sinapsys.global',
    'license': 'AGPL-3',
    "category": "Product",
    "depends": ["product"],
    'data': [
        'views/product_template.xml',
        'wizard/to_publish_product.xml',
        'wizard/to_hide_product.xml'
    ],
    'installable': True,
    "auto_install": False,
}
