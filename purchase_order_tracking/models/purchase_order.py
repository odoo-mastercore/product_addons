# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin_purchase = fields.Many2one(
        'res.country',
        string='Origin of the purchase', ondelete='restrict', required=True
    )
    load_type = fields.Selection(
        string='Type of load', required=True,
        selection=[('marine', 'Maritima'), ('land', 'Terrestre')],
        default='marine')
    weight_total = fields.Float(
        string="Peso total", compute="_all_weight_volume",
        store=True,
        readonly=True
    )
    volume_total = fields.Float(
        string="Volumen total", compute="_all_weight_volume",
        store=True,
        readonly=True
    )

    provider_estimated_date = fields.Datetime(
        string='Provider estimated date',
    )
    provider_recognition_date = fields.Datetime(
        string='Recognition date',
    )
    provider_recognition_number = fields.Char(
        string="Recognition number"
    )

    tracking_number = fields.Char(string="Número de Tracking")
    shipping_company = fields.Char(string="Empresa de Envío")
    warehouse_number = fields.Char(string="Número de Warehouse")
    warehouse_company = fields.Many2one('res.partner', string="Empresa Warehouse")
    warehouse_receipt_date = fields.Datetime(
        string="Fecha de recepción de Warehouse"
    )

    trip_name = fields.Char(string="Nombre del viaje")
    shipowner = fields.Many2one('res.partner', string="Naviera")
    booking_number = fields.Char(string="Número de Booking")
    ship_name = fields.Char(string="Nombre del barco")
    container_number = fields.Char(string="Número del contenedor")
    bl = fields.Char(string="BL")
    port_arrival = fields.Selection(
        string='Puerto de llegada',
        selection=[
            ('0', 'Guanta'),
            ('1', 'La Guaira'),
            ('2', 'Maracaibo'),
            ('3', 'Puerto Cabello'),
            ('4', 'Porlamar'),
        ],
        default='0'
    )
    estimated_departure_date = fields.Datetime(
        string="Fecha estimada de salida"
    )
    estimated_port_arrival = fields.Datetime(
        string="Fecha estimada de llegada al puerto"
    )
    real_date_arrival = fields.Datetime(
        string="Fecha real llegada al puerto"
    )

    stock_receipt_date = fields.Datetime(
        string="Fecha de recepción de almacén"
    )
    observations = fields.Text(string="Observaciones")

    @api.depends("order_line.weight", "order_line.volume")
    def _all_weight_volume(self):
        for order in self:
            weight = volume = 0.0
            for line in order.order_line:
                weight += line.weight
                volume += line.volume
            order.update({
                'weight_total': float(weight),
                'volume_total': float(volume)
            })

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    weight = fields.Float(
        related='product_id.product_tmpl_id.weight', string='Peso'
    )
    volume = fields.Float(
        related='product_id.product_tmpl_id.volume', string='Volumen'
    )