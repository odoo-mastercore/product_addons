# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    qty_not_available = fields.Boolean(string='Quantity not available',
        compute='_compute_product_qty_', store=True, default=False)
    
    @api.depends('product_uom_qty', 'qty_available_today',)
    def _compute_product_qty_(self):
        for rec in self:
            if rec.product_uom_qty <= rec.qty_available_today:
                rec.qty_not_available = False
            else:
                rec.qty_not_available = True

    @api.model
    def create(self, vals):
        result = super(SaleOrderLine, self).create(vals)
        if result.qty_not_available:
            raise ValidationError(
                _('No hay disponibilidad para el producto %s' % result.product_id.name)
            )
        return result
    

    def write(self, vals):
        result = super(SaleOrderLine, self).write(vals)
        if self.qty_not_available:
            raise ValidationError(
                _('No hay disponibilidad para el producto %s' % self.product_id.name)
            )
        return result