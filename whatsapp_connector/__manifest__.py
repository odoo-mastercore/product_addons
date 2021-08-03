# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': 'WhatsApp Odoo Connector Services',
    'version': '13.0.0.1',
    'summary': 'WhatsApp Odoo Connector To Services Company',
    'author': 'SINAPSYS GLOBAL SA || MASTERCORE SAS',
    'website': 'http://sinapsys.global',
    'images': [],
    'sequence': 4,
    'license': 'LGPL-3',
    'description': """WhatsApp Odoo Connector To Services Company""",
    'category': 'Connector',
    'depends': [
        'base', 'contacts', 'sale', 'crm', 'sale_management',
        'account', 'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/whatsapp_template.xml',
        'views/whatsapp_button_views.xml',
        'wizard/whatsapp_wizard.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
