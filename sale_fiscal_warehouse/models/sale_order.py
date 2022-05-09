
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
        if self.fiscal_sale:
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
        return rec

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.fiscal_sale:
            res.update({
                'journal_id': self.warehouse_fiscal_id.journal_fiscal_id.id
            })
        return res