# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2021-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ConfirmSaleOrder(models.TransientModel):
    _name = 'confirm.sale.order.wizard'

    invoice_debts = fields.Char()
    sale_order_id = fields.Many2one('sale.order','Order de venta')
    
    def confirm(self):
        return self.sale_order_id.action_quotation_send()
        

