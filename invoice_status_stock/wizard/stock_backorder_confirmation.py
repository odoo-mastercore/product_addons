# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
import logging
_logger = logging.getLogger(__name__)


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'
    _description = 'Backorder Confirmation'


    # # @api.depends('pick_ids')
    # def picking_transfers(self, cancel_backorder=True):
        # _logger.info("#####################################")
        # picking = None
        # for confirmation in self:
            # _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # if cancel_backorder:
                # for pick_id in confirmation.pick_ids:
                    # _logger.info("IDS: " + str(picking))
                    # picking = pick_id
        # _logger.info("Picking: " + str(picking))
        # return {
            # 'name': _('Transfers'),
            # 'res_model': 'stock.picking',
            # 'type': 'ir.actions.act_window',
            # 'view_mode': 'form',
            # 'target': 'new',
            # 'context': {
                # 'default_partner_id': picking.partner_id.id,
                # 'default_location_id': picking.location_id.id,
                # # 'default_location_id': 11,
                # 'default_location_dest_id': 8,
                # 'default_picking_type_id': 5
            # }
            # # 'res_id': mrp_bom_id.id

        # }

    # def process_cancel_backorder(self):
        # res = super(StockBackorderConfirmation, self).process_cancel_backorder()
        # self.picking_transfers(cancel_backorder=True)
        # return res


