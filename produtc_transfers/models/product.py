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


    purchase_stock_move_ids = fields.Many2many(
        'stock.move',
        string="Ordenes de Recepción",
        compute_sudo=True,
        help="Historial de movimientos de entrada para este producto"
    )
    sale_stock_move_ids = fields.Many2many(
        'stock.move',
        string='Ordenes de Entrega', 
        compute='_compute_product_move', 
        compute_sudo=True,
        help="Historial de movimientos de Salida para este producto"
    )


    @api.depends('order_line.invoice_lines.move_id')
    def _compute_invoice_warehouse_ids(self):
        for order in self:
            invoices = order.mapped('order_line.invoice_lines.move_id').filtered(
                lambda inv: inv.partner_id != order.partner_id
            )
            order.invoice_warehouse_ids = invoices
            weight = volume = 0
            if invoices:
                for invoice in invoices:
                    weight += invoice.weight_provider_total
                    volume += invoice.volume_provider_total
            order.warehouse_weight_total = weight
            order.warehouse_volume_total = volume

    @api.depends('purchase_stock_move_ids', 'sale_stock_move_ids')
    def _compute_product_stock_picking(self):
        for moves in self:
            move = moves.mapped('product_stock_move_ids').filtered(
                lambda inv: inv.picking_code == 'incoming'
            )
            moves.product_move_ids = move


    
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
    type_picking = fields.Selection(
        strinf="Tipo de Operacion",
        related='picking_id.picking_type_id.code',
        readonly=False,
        store=True
    )
