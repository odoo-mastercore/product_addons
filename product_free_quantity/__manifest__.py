# -*- coding: utf-8 -*-
################################################################################
# Author      : SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyright(c): 2021-Present.
# License URL : AGPL-3
################################################################################

{
    'name': 'Product Free Quantity',
    'version': '13.0.0.1',
    'description': """
    Stock Libre en product.
    """,
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'www.sinapsys.global',
    'license': 'AGPL-3',
    'category': 'Stock',
    'depends': [
        'base',
        'product',
        'stock',
    ],
    'data': [
        'views/product_view.xml'
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}
