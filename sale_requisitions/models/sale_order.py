# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from email.policy import default
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    weight_total = fields.Float(
        string='Peso total',
        compute="_compute_weight_total"
    )
    weight_uom_kg = fields.Char(
        'weight in kg',
        default="kg",
        readonly=True
    )
    volume_total = fields.Float(
        string='Volumen total',
        compute="_compute_weight_total"
    )
    volume_uom_mc = fields.Char(
        'volume in m³',
        default="m³",
        readonly=True
    )
    show_meter_report = fields.Boolean(
        string='Show meter in report',
        default=False
    )
    withdrawal_type = fields.Selection(
        [
            ('office_retreat', 'Retiro en Oficina'),
            ('shipping_to_freight', 'Envíar a Fletera')
        ],string="Tipo de Retiro",
        help="Indica si el pedido sera retirado en Oficina o enviado a Fletera."
    )
    by_payment = fields.Selection(
        [
            ('charge_at_destination', 'Cobro en Destino'),
            ('pay_per_giro', 'Pago por Giro')
        ],string="Pagado por"
    )
    fleet_contact_id = fields.Many2one(
        'fleet.contact',
        string="Fleet Contact"
    )


    @api.onchange('withdrawal_type')
    def _onchange_withdrawal_type(self):
        if self.withdrawal_type == 'office_retreat':
            self.by_payment = False

    @api.depends("order_line.weight_kg", "order_line.volume_mc")
    def _compute_weight_total(self):
        for order in self:
            weight = volume = 0.0
            for line in order.order_line:
                weight += (line.weight_kg * line.product_uom_qty)
                volume += (line.volume_mc * line.product_uom_qty)
            order.update({
                'weight_total': float(weight),
                'volume_total': float(volume)
            })

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    weight_kg = fields.Float(
        string="Peso",
        related='product_id.product_tmpl_id.weight_kg'
    )
    volume_mc = fields.Float(
        string="Volumen",
        related='product_id.product_tmpl_id.volume_mc'
    )
    product_uom_qty = fields.Float(
        digits=(12, 0)
    )
