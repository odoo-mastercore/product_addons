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
        compute='_compute_purchase_stock_move', 
        compute_sudo=True,
        help="Historial de movimientos de entrada para este producto"
    )
    sale_stock_move_ids = fields.Many2many(
        'stock.move',
        string='Ordenes de Entrega', 
        compute='_compute_sale_stock_move', 
        compute_sudo=True,
        help="Historial de movimientos de Salida para este producto"
    )



    def _compute_purchase_stock_move(self):
        for rec in self:
            picking = self.env['stock.move'].search([
                ('product_tmpl_id.id', '=', rec.id),
                ('picking_type_id.code', '=', 'incoming')
            ])
            if len(picking) >= 1:
                self.purchase_stock_move_ids = picking
        else:
            self.purchase_stock_move_ids = []


    def _compute_sale_stock_move(self):
        for rec in self:
            picking = self.env['stock.move'].search([
                ('product_tmpl_id.id', '=', rec.id),
                ('picking_type_id.code', '=', 'outgoing')
            ])
            if len(picking) >= 1:
                self.sale_stock_move_ids = picking
        else:
            self.sale_stock_move_ids = []


    
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


