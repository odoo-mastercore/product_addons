# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2021-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_confirm(self):
        for rec in self:
            for line in rec.order_line:
                if line.product_uom_qty > line.free_qty_today and line.product_uom_qty > line.product_id.free_qty:
                    raise ValidationError(
                        _('No hay disponibilidad para el producto %s' % line.\
                            product_id.name)
                    )
        super(SaleOrder, self).action_confirm()
