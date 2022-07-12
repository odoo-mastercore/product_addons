# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class StockPickingPackageWizard(models.TransientModel):

    _name = "stock.picking.package.wizard"
    
    move_line_ids = fields.Many2many('stock.move.line', string='Operations')


    def execute(self):
        for rec in self:
            for move in rec.move_line_ids:
                move.write({
                    'result_package_id' : move.result_package_id
                })
            