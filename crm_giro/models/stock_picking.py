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


    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if self.origin:
            order = self.env['sale.order'].search(
                [('name', '=', self.origin)]
            )
            if not order or order != False or order != "":
                lead = self.env['crm.lead'].search(
                    [('name', '=', order.opportunity_id.name)]
                )
                _logger.info("Lead: " + str(lead))
                if not lead or lead != False or lead != "":
                    if self.picking_type_code == 'outgoing' and self.state == 'done':
                        stage = self.env['crm.stage'].search(
                            [('name', '=', 'Despachado')]
                        )
                        lead.update({
                            'stage_id': stage.id,
                            'state_picking': 'done'
                        })
        return res

