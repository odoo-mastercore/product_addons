# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Website custom giro',
    'version': '13.0.0.1',
    'summary': 'custom website giro',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://sinapsys.global',
    'license': 'AGPL-3',
    "category": "Product",
    "depends": ["website_sale", "droggol_theme_common", 'theme_prime'],
    'data': [
        'views/products.xml'
    ],
    'installable': True,
    "auto_install": False,
}
