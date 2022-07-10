# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'




    @api.model
    def create(self, vals):
        if vals.get('opportunity_id'):
            lead = self.env['crm.lead'].search(
                [('id', '=', vals.get('opportunity_id'))]
            )
            orders = lead.mapped('order_ids').filtered(
                lambda o: o.state in ('draft', 'sent', 'sale')
            )
            _logger.info("Order: " + str(orders))
            if orders:
                raise UserError(_("No puede crear mas de un pedido de venta a una aportunidad"))
        return super(SaleOrder, self).create(vals)


