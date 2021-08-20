# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': "Remove options to product_id fields",
    'description': """
        Extends views and remove option create in product_id field
    """,
    'version': "13.0.1.0.0",
    'category': "sale",
    'depends': ['sale',],
    'author': "SINAPSYS GLOBAL SA || MASTERCORE SAS",
    'website': "http://sinapsys.global",
    'license': "GPL-3",
    'data': [
        'views/sale_view.xml',
        'views/account_move_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
