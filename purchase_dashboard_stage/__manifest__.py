# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': "Purchase dashboard stage",
    'description': """
        This module adds stages to purchase orders
    """,
    'author': "SINAPSYS GLOBAL SA || MASTERCORE SAS",
    'website': "http://sinapsys.global",
    'version': '13.0.2',
    'category': '',
    'license': 'AGPL-3',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_stage.xml',
        'views/purchase_order.xml',
        'data/purchase_stage.xml',
    ],
}