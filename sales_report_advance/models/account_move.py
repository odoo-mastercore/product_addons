# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    product_line_cost_totals = fields.Float(string="Costo total", compute="_compute_product_line_cost_total", store=True)
    product_line_price_totals = fields.Float(string="Precio total", compute="_compute_product_line_cost_total", store=True)
    product_line_margin_totals = fields.Float(string="Margen", compute="_compute_product_line_cost_total", store=True)
    product_line_percentage_totals = fields.Float(string="% de utilidad", compute="_compute_product_line_cost_total", store=True)
    
    # @api.depends('invoice_line_ids')
    def _compute_product_line_cost_total(self):
        for rec in self:
            _logger.info('***********************' + str(rec.invoice_line_ids))
            cost = 0
            price = 0
            for line in rec.invoice_line_ids:
                cost += line.product_id.standard_price
                price += line.price_total
                _logger.info('***********COSTO&***********' + str(cost))
            rec.product_line_cost_totals = cost
            rec.product_line_price_totals = price
            rec.product_line_margin_totals = price - cost if cost > 0 else 1
            rec.product_line_percentage_totals = price * 100 / (cost if cost > 0 else 1)
