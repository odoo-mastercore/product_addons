# -*- coding: utf-8 -*-
###############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    "name": "Package Details",
    "version": "13.0.0.0.1",
    "summary": "Add package dimensions fields",
    "author": "SINAPSYS GLOBAL SA || MASTERCORE SAS",
    "license": "AGPL-3",
    "category": "stock",
    "depends": [
        'base',
        'stock',
    ],
    "data": [
        "views/view_quant_package_form.xml",
        "wizard/move_lines_package.xml",
        "views/picking.xml",
        "reports/package_report.xml"
    ],
    "auto_install": False,
    "installable": True,
}
