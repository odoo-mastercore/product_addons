# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

{
    'name': "Sales Report Advance",
    'version': "13.0",
    "description": 'Reporte de ventas para la empresa Giro',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': "http://sinapsys.global",
    'license': 'AGPL-3',
    'category': "Product",
    'depends': [
        'base',
        'invoice_status_stock',
        'account'
    ],
    'data': [
        'views/account_move_tree.xml',
        'security/security.xml'
    ],
    'installable': True,

}

