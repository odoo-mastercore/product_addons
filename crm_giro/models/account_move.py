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

class AccountMove(models.Model):
    _inherit = 'account.move'


    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        if self.invoice_origin:
            order = self.env['sale.order'].search(
                [('name', '=', self.invoice_origin)]
            )
            if not order or order != False or order != "":
                lead = self.env['crm.lead'].search(
                    [('name', '=', order.opportunity_id.name)]
                )
                _logger.info("Lead: " + str(lead))
                if not lead or lead != False or lead != "":
                    if vals.get('payment_type2') == 'cash_payment':
                        stage = self.env['crm.stage'].search(
                            [('name', '=', 'Pago por Confirmar')]
                        )
                        lead.update({'stage_id': stage.id})
                    elif vals.get('payment_type2') == 'credit_payment':
                        stage = self.env['crm.stage'].search(
                            [('name', '=', 'Facturación')]
                        )
                        lead.update({'stage_id': stage.id})
        return res


