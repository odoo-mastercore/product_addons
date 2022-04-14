# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Sale Coupoon',
    'summary': """Allows display max quantity in program""",
    'description': """Allows display max quantity in program""",
    'version': '13.0.1.0.0',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'https://www.sinapsys.global',
    'category': 'Product',
    'depends': ['sale_coupon', ],
    'license': 'AGPL-3',
    'data': [
        'views/sale_coupon_program_views.xml',
    ],
    'images': [],
    'installable': True,
    'auto_install': False,
}
