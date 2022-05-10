# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):

    _inherit = 'sale.order'
    fiscal_sale = fields.Boolean('fiscal_sale')
    warehouse_fiscal_id = fields.Many2one('stock.warehouse', string="Depósito")

    @api.onchange('fiscal_sale')
    def _onchange_fiscal_sale(self):
        if self.fiscal_sale:
            if self.company_id.warehouse_fiscal:
                self.warehouse_fiscal_id = self.company_id.warehouse_fiscal_id.id
            else:
                self.warehouse_fiscal_id = False
        else:
            self.warehouse_fiscal_id = False

    def action_confirm(self):
        rec = super(SaleOrder, self).action_confirm()
        if self.fiscal_sale and self.order_line:
            pick_init = self.mapped('picking_ids').filtered(lambda p: p.state in 'assigned')
            picking_type_id = self.env['stock.picking.type'].search([
                ('warehouse_id.fiscal_warehouse', '=', True),
                ('code', '=', 'outgoing')
            ], limit=1)
            fiscal_pick = pick_init.copy({
                'picking_type_id': picking_type_id.id,
                'location_id': picking_type_id.default_location_src_id.id
            })
            fiscal_pick.action_confirm()
            fiscal_pick.action_assign()

            Purchase = self.env['purchase.order'].sudo().search([
                ('state', '=', 'draft'),
                ('monthly_fiscal_purchase', '=', True)
            ], limit=1)
            if not Purchase:
                Purchase = self.env['purchase.order'].sudo().create({
                    'date_order': fields.Datetime.now(),
                    'partner_id': self.company_id.partner_id.id,
                    'purchase_type': 'national',
                    'monthly_fiscal_purchase': True
                })
            order_line = []
            if self.order_line:
                for line in self.order_line:
                    fpos = Purchase.fiscal_position_id
                    taxes = fpos.map_tax(line.product_id.supplier_taxes_id) if fpos else line.product_id.supplier_taxes_id
                    if taxes:
                        taxes = taxes.filtered(lambda t: t.company_id.id == self.company_id.id)
                    order_line.append([0, 0, {
                        'name': line.name,
                        'product_qty': line.product_uom_qty,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_id.uom_po_id.id,
                        'date_planned': fields.Datetime.now(),
                        'price_unit': 1.0,
                        'taxes_id': [(6, 0, taxes.ids)],
                        'sale_origin_create': self.id,
                    }])
            Purchase.order_line = order_line
        return rec

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        if res:
            PurchaseLine = self.env['purchase.order.line'].sudo().search([
                ('sale_origin_create', '=', self.id),
                ('state', '=', 'draft')
            ])
            PurchaseLine.unlink()
        return res

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.fiscal_sale:
            res.update({
                'journal_id': self.warehouse_fiscal_id.journal_fiscal_id.id
            })
        return res