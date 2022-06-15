# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Sale order credit limit',
    'version': '13.0.0.1',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://sinapsys.global',
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': 'Add limit credit to customers',
    'depends': ['base', 'sale'],
    'data': [
        'views/credit_limit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
