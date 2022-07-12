# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    def put_in_pack(self):
        for rec in self:
            move_line_ids = rec.move_line_ids.ids
            if len(rec.move_ids_without_package) > 1:
                return {
                    'name':'Asignar paquetes',
                    'view_mode': 'form',
                    'view_id': self.env.ref('package_details.moves_lines_package_wizard_form').id,
                    'view_type': 'form',
                    'res_model': 'stock.picking.package.wizard',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_move_line_ids': rec.move_line_ids.ids}
                }

        rec = super(StockPickingInherit, self).put_in_pack()
        return rec