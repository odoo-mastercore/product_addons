# -*- coding: utf-8 -*-
###############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    "name": "Product Group Code",
    "version": "13.0.2.0.0",
    "summary": "Adds group code models on the product view.",
    "author": "SINAPSYS GLOBAL SA || MASTERCORE SAS",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["product",],
    "data": [
        "security/ir.model.access.csv",
        "views/product_view.xml"
    ],
    "auto_install": False,
    "installable": True,
}
