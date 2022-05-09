
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
            picks = self.mapped('picking_ids').filtered(
                lambda p: p.state in 'assigned')
            for pick in picks:
                pick.action_pick_cavv()
        return rec
