# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Product vehicle type',
    'version': '13.0.0.1',
    'summary': 'Add vehicle type field in model product',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://sinapsys.global',
    'license': 'AGPL-3',
    "category": "Product",
    "depends": ["product", "website_sale", "fleet"],
    'data': [
        'views/product_form_inherit.xml'
    ],
    'installable': True,
    "auto_install": False,
}
