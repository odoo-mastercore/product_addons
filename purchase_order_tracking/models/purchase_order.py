# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    def _get_default_volume_uom(self):
        return self.env['product.template']._get_volume_uom_name_from_ir_config_parameter()

    # stage 1
    warehouse_company = fields.Many2one('res.partner', string="Empresa Warehouse")
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
    oc_provider_ids = fields.One2many(
        'order.purchase.provider',
        'purchase_order_id',
        string='Colocación Orden/Compra',
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
    transit_warehouse_ids = fields.One2many(
        'transit.warehouse',
        'purchase_order_id',
        string='Tránsito',
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
    transit_land_maritime_ids = fields.One2many(
        'transit.land.maritime',
        'purchase_order_id',
        string='Tránsito Maritimo/Terrestre',
    )
    # stage 6
    stock_receipt_ids = fields.One2many(
        'stock.receipt',
        'purchase_order_id',
        string='Recepción almacen',
    )
    estimated_time_ids = fields.One2many(
        'estimated.time',
        'purchase_order_id',
        string='Tiempo estimado',
    )

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
                    weight += (line.weight * line.product_qty)
                    volume += (line.volume * line.product_qty)
            else:
                for line in order.order_line:
                    weight += (line.weight_kg * line.product_qty)
                    volume += (line.volume_mc * line.product_qty)
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

    def button_confirm(self):
        rec = super(PurchaseOrder, self).button_confirm()
        for po in self:
            stage_init = self.env.ref('purchase_dashboard_stage.stage_requisition_order', raise_if_not_found=False)
            stage_next = self.env.ref('purchase_dashboard_stage.stage_purchase_order', raise_if_not_found=False)
            estimated_times = self.env['estimated.time'].search([
                ('purchase_order_id', '=', po.id)
            ], order="id DESC", limit=1)
            if stage_init.name == estimated_times.stage_name:
                try:
                    estimated_times.write({
                        'real_date': fields.Datetime.now()
                    })
                    po.stage_id = stage_next.id
                    estimated_res = self.env['estimated.time'].create({
                        'stage_name': stage_next.name,
                        'entry_date': fields.Datetime.now(),
                        'stage_days': stage_next.estimated_time,
                        'purchase_order_id': po.id
                    })
                    self.env['order.purchase.provider'].create({
                        'provider_estimated_date': estimated_res.estimated_date,
                        'purchase_order_id': po.id
                    })
                except Exception as e:
                    _logger.error("Error - button_confirm %s" % (e))
                    pass
        return rec

    @api.model
    def create(self, vals):
        rec = super(PurchaseOrder, self).create(vals)
        res_estimated_time = {
            'stage_name': rec.stage_id.name,
            'entry_date': rec.create_date,
            'stage_days': rec.stage_id.estimated_time,
            'purchase_order_id': rec.id
        }
        self.env['estimated.time'].create(res_estimated_time)
        return rec

    def write(self, vals):
        stage_next = self.env.ref('purchase_dashboard_stage.stage_invoice_payment', raise_if_not_found=False)
        if vals.get('oc_provider_ids'):
            date = vals['oc_provider_ids'][0][2]
            if date.get('provider_recognition_date') and date.get('provider_recognition_date'):
                date_recognition = date.get('provider_recognition_date')
                estimated_times = self.env['estimated.time'].search([
                    ('purchase_order_id', '=', self.id)
                ], order="id DESC", limit=1)
                estimated_times.write({
                    'real_date': date_recognition
                })
                self.stage_id = stage_next.id
                self.env['estimated.time'].create({
                    'stage_name': stage_next.name,
                    'entry_date': date_recognition,
                    'stage_days': stage_next.estimated_time,
                    'purchase_order_id': self.id
                })
        return super(PurchaseOrder, self).write(vals)

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


class OrderPurchaseProvider(models.Model):
    _name = "order.purchase.provider"
    _description = "Colocacion Order/Compra"

    provider_estimated_date = fields.Datetime(
        string='Fecha estamida del proveedor',
    )
    provider_recognition_date = fields.Datetime(
        string='Fechas de reconocimiento',
    )
    provider_recognition_number = fields.Char(
        string="Número de reconocimiento"
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True
    )


class TransitWarehouse(models.Model):
    _name = "transit.warehouse"
    _description = "Transito warehouse"

    tracking_number = fields.Char(string="Número de Tracking")
    shipping_company = fields.Char(string="Empresa de Envío")
    warehouse_number = fields.Char(string="Número de Warehouse")
    warehouse_receipt_date = fields.Datetime(
        string="Fecha de recepción de Warehouse"
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True
    )
    order_picking_id = fields.Many2one(
        'stock.picking',
        string="Orden de entrega",
        domain="[('purchase_id', '=', purchase_order_id)]"
    )

    @api.onchange('purchase_order_id')
    def _onchange_purchase_order_id(self):
        purchase_id = self._context.get('default_purchase_order_id')
        picking = self.env['stock.picking'].search([
            ('purchase_id', '=', purchase_id),
            ('state', '=', 'assigned')
        ],order="id DESC", limit=1)
        if picking:
            self.order_picking_id = picking.id


class TransitLandMaritime(models.Model):
    _name = "transit.land.maritime"
    _description = "Tránsito Maritimo/Terrestre"

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
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True
    )
    order_picking_id = fields.Many2one(
        'stock.picking',
        string="Orden de entrega",
        domain="[('purchase_id', '=', purchase_order_id)]"
    )

    @api.onchange('purchase_order_id')
    def _onchange_purchase_order_id(self):
        purchase_id = self._context.get('default_purchase_order_id')
        picking = self.env['stock.picking'].search([
            ('purchase_id', '=', purchase_id),
            ('state', '=', 'assigned')
        ],order="id DESC", limit=1)
        if picking:
            self.order_picking_id = picking.id


class StockReceipt(models.Model):
    _name = 'stock.receipt'
    _description = 'Recepción Almacen'

    stock_receipt_date = fields.Datetime(
        string="Fecha de recepción de almacén"
    )
    observations = fields.Text(string="Observaciones")
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True
    )
    order_picking_id = fields.Many2one(
        'stock.picking',
        string="Orden de entrega",
        domain="[('purchase_id', '=', purchase_order_id)]"
    )

    @api.onchange('purchase_order_id')
    def _onchange_purchase_order_id(self):
        purchase_id = self._context.get('default_purchase_order_id')
        picking = self.env['stock.picking'].search([
            ('purchase_id', '=', purchase_id),
            ('state', '=', 'done')
        ],order="id DESC", limit=1)
        if picking:
            self.order_picking_id = picking.id
            self.stock_receipt_date = picking.date_done


class EstimatedTime(models.Model):
    _name = 'estimated.time'
    _description = 'Tiempo estimados para OC'

    stage_name = fields.Char(string='Etapa')
    stage_days = fields.Integer(
        string='Dias estimados',
    )
    entry_date = fields.Datetime(string='Fecha de entrada')
    estimated_date = fields.Datetime(
        string='Fecha estimada',
        compute="_compute_estimated_date"
    )
    real_date = fields.Datetime(string='Fecha real')

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True
    )

    @api.depends('stage_days', 'entry_date')
    def _compute_estimated_date(self):
        for record in self:
            estimated_time = record.create_date + (
                relativedelta(days=int(record.stage_days))
            )
            record.estimated_date = estimated_time