# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    fiscal_warehouse = fields.Boolean('Almacen fiscal')
    journal_fiscal_id = fields.Many2one('account.journal',
        'Diario de facturacion')
