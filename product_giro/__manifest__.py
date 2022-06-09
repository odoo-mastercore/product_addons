# -*- coding: utf-8 -*-
###############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    "name": "Product Giro",
    "version": "13.0.0.0.1",
    "summary": "Add stock free in product template",
    "author": "SINAPSYS GLOBAL SA || MASTERCORE SAS",
    "license": "AGPL-3",
    "category": "Product",
    "depends": [
        'base',
        'product',
        'sale',
        'stock',
    ],
    "data": [
        "views/product_template.xml",
        # 'views/sale_order.xml'
    ],
    "auto_install": False,
    "installable": True,
}
