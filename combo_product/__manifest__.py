# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'Combo Product',
    'summary': "Combo Product",
    'description': """
        Combo Product.
        ========================
        Create Combo Product . extension by SINAPSYS GLOBAL SA || MASTERCORE SAS
    """,

    'author': 'iPredict IT Solutions Pvt, SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': "http://sinapsys.global",
    'category': 'Product',
    'version': '13.0.0.1.0',
    'depends': ['product', 'sale', 'sale_stock',],

    'data': [
        'security/ir.model.access.csv',
        'views/combo_product_view.xml',
    ],

    'license': "OPL-1",

    'auto_install': False,
    'installable': True,

    'images': ['static/description/banner.png'],
}
