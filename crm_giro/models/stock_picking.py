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
        for rec in self:
            if rec.origin:
                order = rec.env['sale.order'].search(
                    [('name', '=', rec.origin)]
                )
                if not order or order != False or order != "":
                    lead = rec.env['crm.lead'].search(
                        [('name', '=', order.opportunity_id.name)]
                    )
                    _logger.info("Lead: " + str(lead))
                    if not lead or lead != False or lead != "":
                        if rec.picking_type_code == 'outgoing' and rec.state == 'done':
                            stage = rec.env['crm.stage'].search(
                                [('name', '=', 'Despachado')]
                            )
                            lead.update({
                                'stage_id': stage.id,
                                'state_picking': 'done'
                            })
        return res

