# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Sale requisitions',
    'version': '13.0.0.1',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://sinapsys.global',
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': 'Add to sale order on requisitions',
    'depends': [
        'sale',
        'sale_stock',
        'material_purchase_requisitions',
        'purchase_order_tracking',
    ],
    'data': [
        'views/sale_requisitions.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
}
