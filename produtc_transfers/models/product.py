# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    product_stock_move_ids = fields.One2many(
        'stock.move',
        'product_tmpl_id',
        # domain="[('picking_code', '=', 'incoming')]",
        string="Ordenes de Entrega",
        help="Historial de movimientos de entrada para este producto"
    )
    # product_move_ids = fields.One2many(
        # 'stock.move',
        # 'product_tmpl_id',
        # string='Ordenes de Entrega', 
        # compute='_compute_product_move', 
        # compute_sudo=True
    # )


    # @api.depends('product_stock_move_ids')
    # def _compute_product_move(self):
        # for moves in self:
            # move = moves.mapped('product_stock_move_ids').filtered(
                # lambda inv: inv.picking_code == 'incoming'
            # )
            # moves.product_move_ids = move


    
class StockMoveLine(models.Model):
    _inherit = 'stock.move'


    stage = fields.Selection(
        string="Estado",
        related='picking_id.state'
    )
    scheduled_date = fields.Datetime(
        string="Fecha Programada",
        related='picking_id.scheduled_date'
    )
    
