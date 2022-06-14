# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': "Purchase order tracking",
    'description': """
        This module works to track a purchase order depending on the stages
    """,
    'author': "SINAPSYS GLOBAL SA || MASTERCORE SAS",
    'website': "http://sinapsys.global",
    'version': '13.0.4',
    'category': '',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'purchase_dashboard_stage',
        'account',
        'stock_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order.xml',
        'views/account_move.xml',
        'views/pallets.xml',
        'views/product_template.xml',
        'views/stock_picking.xml'
    ],
}