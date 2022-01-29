# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    
    def _compute_state_invoice(self):
        _logger.info("######################################################")
        if self.sale_id:
            if self.sale_id.invoice_count >= 1:
                for rec in self:
                    if rec.sale_id.invoice_ids[0].invoice_payment_state == 'paid':
                        rec.state_invoice = "PAGADA"
                    elif rec.sale_id.invoice_ids[0].invoice_payment_state == 'in_payment':
                        rec.state_invoice = "PROCESO"
                    else:
                        rec.state_invoice = "NO_PAGO"
            else:
                self.state_invoice = "SIN_FACTURA"
        else:
            self.state_invoice = "N/A"

    invoice_id = fields.Many2one('account.move', string="Factura")
    state_invoice = fields.Char(
        string="Status Factura",
        compute="_compute_state_invoice",
    )

