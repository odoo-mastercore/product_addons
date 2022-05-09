# -*- coding: utf-8 -*-
################################################################################
# Author      : SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyright(c): 2022-Present.
# License URL : AGPL-3
################################################################################

{
    'name': 'Sale Warehouse',
    'version': '13.0.0.1',
    'description': """
        Permite la asignación de un almacen no fiscal
    """,
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'www.sinapsys.global',
    'license': 'AGPL-3',
    'category': 'Stock',
    'depends': [
        'base',
        'stock',
        'sale',
        'sale_stock',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/warehouse.xml',
        'views/sale_order.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}
