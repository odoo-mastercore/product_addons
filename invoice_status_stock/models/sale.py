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

class SeleOrder(models.Model):
    _inherit = 'sale.order'

    
    def _compute_state_invoice(self):
        if self.invoice_count >= 1:
            for rec in self:
                if rec.invoice_ids[0].invoice_payment_state == 'paid':
                    rec.state_invoice = "PAGADA"
                elif rec.invoice_ids[0].invoice_payment_state == 'in_payment':
                    rec.state_invoice = "PROCESO"
                else:
                    rec.state_invoice = "NO_PAGO"
        else:
            self.state_invoice = "SIN_FACTURA"

    state_invoice = fields.Char(
        string="Status Factura",
        compute="_compute_state_invoice",
    )


