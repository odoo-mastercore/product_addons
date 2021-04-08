#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Product Tariff Code",
    'version': "13.0",
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': "http://sinapsys.global",
    'sequence': 10,
    'category': "Product",
    'depends': [
        'base',
        'product',
        'purchase'
    ],
    'data': [
        'views/product_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False

}

