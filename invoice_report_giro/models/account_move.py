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



    @api.depends('invoice_line_ids')
    def base_exenta(self):
        base_exenta = 0.00
        for account in self:
            taxes = self.mapped('invoice_line_ids').filtered(
                lambda o: o.tax_ids.amount == 0 
            )
            if taxes:
                for line in taxes:
                    base_exenta += line.price_subtotal
        return base_exenta


    @api.depends('invoice_line_ids')
    def base_gravable(self):
        base_gravable = 0.00
        for account in self:
            lines = self.mapped('invoice_line_ids').filtered(
                lambda o: o.tax_ids.amount != 0 
            )
            if lines:
                for line in lines:
                    base_gravable += line.price_subtotal
        return base_gravable
