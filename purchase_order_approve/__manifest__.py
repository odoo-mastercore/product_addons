###############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2021-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
{
    'name': "Purchase Order Approve",
    'description': """
        Este módulo extiende algunos modelos base de Odoo relacionados
        para aprobar ordenes de compra.
    """,

    'author': "SINAPSYS GLOBAL SA || MASTERCORE SAS",
    'website': "http://sinapsys.global",
    'version': '13.0.1',
    'category': 'Localization',
    'license': 'AGPL-3',
    'depends': [
        'web_digital_sign','purchase'],
    'data': [
        'reports/report_purchase.xml',
    ],
}
