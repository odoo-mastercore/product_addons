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


class SaleRequisitions(models.Model):

    _inherit = 'material.purchase.requisition'

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Orden de venta",
        domain="[('state', '=', 'draft')]"
    )
    type_requisitions = fields.Selection(
        selection=[
            ('internal', 'Interna'),
            ('lost_sale', 'Venta Perdida'),
            ('sale_validity', 'Por Venta Validada')
        ],
        default='internal',
        string="Type Requisitions",
    )

    @api.onchange('sale_order_id')
    def _load_sale_order_line(self):
        for rec in self:
            if rec.sale_order_id.order_line:
                order_lines = rec.sale_order_id.order_line
                requisition_lines = []
                for line in order_lines:
                    requisition_lines.append([0, 0, {
                        "product_id": line.product_id.id,
                        "description": line.product_id.name,
                        "qty": line.product_uom_qty,
                        "uom": line.product_id.uom_id.id,
                        "requisition_type": 'purchase'
                    }])
                rec.requisition_line_ids = requisition_lines
