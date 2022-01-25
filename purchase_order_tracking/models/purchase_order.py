# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from cgitb import reset
from odoo import api, fields, models, _, SUPERUSER_ID


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    def _get_default_volume_uom(self):
        return self.env['product.template']._get_volume_uom_name_from_ir_config_parameter()

    # stage 1
    origin_purchase = fields.Many2one(
        'res.country',
        string='Origin of the purchase', ondelete='restrict', required=True
    )
    load_type = fields.Selection(
        string='Type of load', required=True,
        selection=[('marine', 'Maritima'), ('land', 'Terrestre')],
        default='marine')
    purchase_type = fields.Selection(
        string='Type of Purchase', required=True,
        selection=[('international', 'Internacional'), ('national', 'Nacional')],
        default='international')
    weight_total = fields.Float(
        string="Peso total", compute="_compute_weight_total",
        store=True,
    )
    weight_uom_name = fields.Char(
        string="weight uom",
        compute="_compute_weight_uom_name",
        default=_get_default_weight_uom
    )
    volume_total = fields.Float(
        string="Volumen total", compute="_compute_weight_total",
        store=True,
    )
    volume_uom_name = fields.Char(
        string="volume uom",
        compute='_compute_volume_uom_name',
        default=_get_default_volume_uom
    )
    # stage 2
    provider_estimated_date = fields.Datetime(
        string='Provider estimated date',
    )
    provider_recognition_date = fields.Datetime(
        string='Recognition date',
    )
    provider_recognition_number = fields.Char(
        string="Recognition number"
    )
    # stage 3
    supplier_ids = fields.Many2many(
        'account.move',
        string='Facturas/Pagos',
        compute='_compute_supplier_ids',
    )
    supplier_weight_total = fields.Float(
        string="Peso total",
        compute="_compute_supplier_ids",
        store=True
    )
    supplier_volume_total = fields.Float(
        string="Volume total",
        compute="_compute_supplier_ids",
        store=True
    )
    # stage 4
    tracking_number = fields.Char(string="Número de Tracking")
    shipping_company = fields.Char(string="Empresa de Envío")
    warehouse_number = fields.Char(string="Número de Warehouse")
    warehouse_company = fields.Many2one('res.partner', string="Empresa Warehouse")
    warehouse_receipt_date = fields.Datetime(
        string="Fecha de recepción de Warehouse"
    )
    invoice_warehouse_ids = fields.Many2many(
        'account.move',
        string='Facturas/Pagos',
        compute='_compute_invoice_warehouse_ids',
    )
    warehouse_weight_total = fields.Float(
        string="Peso total",
        compute='_compute_invoice_warehouse_ids',
        store=True
    )
    warehouse_volume_total = fields.Float(
        string="Volume total",
        compute='_compute_invoice_warehouse_ids',
        store=True
    )
    # stage 5
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
    # stage 6
    stock_receipt_date = fields.Datetime(
        string="Fecha de recepción de almacén"
    )
    observations = fields.Text(string="Observaciones")

    @api.depends(
        "order_line.weight",
        "order_line.volume",
        "purchase_type"
    )
    def _compute_weight_total(self):
        for order in self:
            weight = volume = 0.0
            if order.purchase_type == 'international':
                for line in order.order_line:
                    weight += line.weight
                    volume += line.volume
            else:
                for line in order.order_line:
                    weight += line.weight_kg
                    volume += line.volume_mc
            order.update({
                'weight_total': float(weight),
                'volume_total': float(volume)
            })
    @api.depends("purchase_type")
    def _compute_weight_uom_name(self):
        for order in self:
            if order.purchase_type == 'international':
                order.weight_uom_name = self.env['product.template'].\
                    _get_weight_uom_name_from_ir_config_parameter()
            else:
                order.weight_uom_name = "kg"

    @api.depends('purchase_type')
    def _compute_volume_uom_name(self):
        for order in self:
            if order.purchase_type == 'international':
                order.volume_uom_name = self.env['product.template'].\
                    _get_volume_uom_name_from_ir_config_parameter()
            else:
                order.volume_uom_name = "m³"

    @api.depends('order_line.invoice_lines.move_id')
    def _compute_supplier_ids(self):
        for order in self:
            invoices = order.mapped('order_line.invoice_lines.move_id').filtered(
                lambda inv: inv.partner_id == order.partner_id
            )
            order.supplier_ids = invoices
            weight = volume = 0
            for invoice in invoices:
                weight += invoice.weight_provider_total
                volume += invoice.volume_provider_total
            order.supplier_weight_total = weight
            order.supplier_volume_total = volume

    @api.depends('order_line.invoice_lines.move_id')
    def _compute_invoice_warehouse_ids(self):
        for order in self:
            invoices = order.mapped('order_line.invoice_lines.move_id').filtered(
                lambda inv: inv.partner_id != order.partner_id
            )
            order.invoice_warehouse_ids = invoices
            weight = volume = 0
            for invoice in invoices:
                weight += invoice.weight_provider_total
                volume += invoice.volume_provider_total
            order.warehouse_weight_total = weight
            order.warehouse_volume_total = volume

    def action_view_invoice(self):
        result = super().action_view_invoice()
        result['context'].update({
            'default_purchase_type': self.purchase_type,
        })
        return result

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    weight = fields.Float(
        related='product_id.product_tmpl_id.weight', string='Peso'
    )
    volume = fields.Float(
        related='product_id.product_tmpl_id.volume', string='Volumen'
    )
    weight_kg = fields.Float(
        related='product_id.product_tmpl_id.weight_kg', string="Peso"
    )
    volume_mc = fields.Float(
        related='product_id.product_tmpl_id.volume_mc', string="Volumen"
    )