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
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class OrderPurchaseProvider(models.Model):
    _name = "order.purchase.provider"
    _description = "Colocacion Order/Compra"

    estimated_days = fields.Integer(string='Dias estimados')
    stage_entry_date = fields.Datetime(
        string="create entry stage",
        default=fields.Datetime.now,
    )
    provider_estimated_date = fields.Datetime(
        string='Fecha estamida del proveedor',
        compute="_compute_estimated_date",
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
    stage_identifier = fields.Char(related='purchase_order_id.stage_id.identifier')

    @api.depends('estimated_days', 'stage_entry_date')
    def _compute_estimated_date(self):
        for rec in self:
            if rec.estimated_days and rec.stage_entry_date:
                new_estimated = rec.stage_entry_date + relativedelta(days=int(rec.estimated_days))
                try:
                    rec.provider_estimated_date = new_estimated
                except Exception as e:
                    _logger.error("Error compute estimated_date provider %s" % (e))
                    pass
            else:
                rec.provider_estimated_date = False

    @api.model
    def write(self, vals):
        if not 'write_purchase_done' in self.env.context:
            stage_next = self.env.ref('purchase_dashboard_stage.stage_invoice_payment', raise_if_not_found=False)
            estimated_times = self.env['estimated.time'].search([
                ('purchase_order_id', '=', self.purchase_order_id.id),
                ('registry_id', '=', self.id)
            ])
            if 'estimated_days' in vals and vals.get('estimated_days'):
                new_estimated = self.stage_entry_date + relativedelta(days=int(vals.get('estimated_days')))
                estimated_times.write({
                    'estimated_date': new_estimated
                })
            if 'provider_recognition_date' in vals and vals.get('provider_recognition_date'):
                date_recognition = vals.get('provider_recognition_date')
                estimated_times.write({
                    'real_date': date_recognition
                })
                res_invoice = self.env['account.move.estimated'].create({
                    'purchase_order_id': self.purchase_order_id.id,
                    'estimated_days': stage_next.estimated_time,
                    'create_view': False,
                    'stage_entry_date': date_recognition
                })
                self.env['estimated.time'].create({
                    'stage_name': stage_next.name,
                    'entry_date': date_recognition,
                    'estimated_date': fields.Datetime.from_string(date_recognition) + relativedelta(days=int(stage_next.estimated_time)),
                    'purchase_order_id': self.purchase_order_id.id,
                    'registry_id': res_invoice.id
                })
        return super(OrderPurchaseProvider, self).write(vals)


class AccountMoveEstimated(models.Model):
    _name = 'account.move.estimated'
    _description = 'Tiempos estimados para facturas/pagos/entrega'

    def _get_detaulf_days_invoice(self):
        return self.env.ref(
            'purchase_dashboard_stage.stage_invoice_payment',
            raise_if_not_found=False
        ).estimated_time

    estimated_days = fields.Integer(
        string="Dias estimados",
        default=_get_detaulf_days_invoice
    )
    stage_entry_date = fields.Datetime(
        string="create entry stage",
        default=fields.Datetime.now,
    )
    create_view = fields.Boolean(
        string='Registro creado desde la vista',
        default=False
    )
    estimated_date = fields.Datetime(
        string='Fecha estimada',
        compute="_compute_estimated_date_invoice",
    )
    real_date = fields.Datetime(string='Fecha de despacho del proveedor')
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True
    )
    purchase_order_name = fields.Char(related='purchase_order_id.name')
    purchase_order_partner = fields.Integer(related='purchase_order_id.partner_id.id')
    stage_name = fields.Char(related='purchase_order_id.stage_id.identifier')
    invoice_id = fields.Many2one(
        'account.move',
        string='Facturas',
        domain="""[
            ('invoice_origin', '=', purchase_order_name),
            ('partner_id', '=', purchase_order_partner)
        ]""",
    )

    @api.depends('estimated_days', 'stage_entry_date')
    def _compute_estimated_date_invoice(self):
        for rec in self:
            if rec.estimated_days and rec.stage_entry_date:
                new_estimated = rec.stage_entry_date + relativedelta(days=int(rec.estimated_days))
                try:
                    rec.estimated_date = new_estimated
                except Exception as e:
                    _logger.error("Error compute estimated_date invoice %s" % (e))
                    pass
            else:
                rec.estimated_date = False

    @api.model
    def create(self, vals):
        if not 'write_purchase_done' in self.env.context:
            invoice_exist = self.search([
                ('purchase_order_id', '=', vals.get('purchase_order_id')),
                ('invoice_id', '=', vals.get('invoice_id'))
            ])
            if invoice_exist:
                raise ValidationError(_(
                    'La factura << %s >> en Facturación/Pago/Entrega ya se encuentra seleccionada' % (
                        invoice_exist.invoice_id.name
                    )
                ))
            res = super(AccountMoveEstimated, self).create(vals)
            if 'create_view' in vals and vals.get('create_view'):
                stage_invoice = self.env.ref('purchase_dashboard_stage.stage_invoice_payment', raise_if_not_found=False)
                real_date_invoice = vals.get('warehouse_receipt_date') \
                    if 'warehouse_receipt_date' in vals and vals.get('warehouse_receipt_date') \
                    else False
                self.env['estimated.time'].create({
                    'stage_name': stage_invoice.name,
                    'entry_date': res.stage_entry_date,
                    'estimated_date': fields.Datetime.from_string(res.stage_entry_date) + relativedelta(days=int(stage_invoice.estimated_time)),
                    'purchase_order_id': res.purchase_order_id.id,
                    'real_date': real_date_invoice,
                    'registry_id': res.id
                })
            return res
        return self

    @api.model
    def write(self, vals):
        if not 'write_purchase_done' in self.env.context:
            stage_next = self.env.ref('purchase_dashboard_stage.stage_transit_warehouse', raise_if_not_found=False)
            estimated_times = self.env['estimated.time'].search([
                ('purchase_order_id', '=', self.purchase_order_id.id),
                ('registry_id', '=', self.id)
            ])
            if 'estimated_days' in vals and vals.get('estimated_days'):
                new_estimated = self.stage_entry_date + relativedelta(days=int(vals.get('estimated_days')))
                estimated_times.write({
                    'estimated_date': new_estimated
                })
            if not self.create_view:
                if 'real_date' in vals and vals.get('real_date'):
                    real_date = vals.get('real_date')
                    estimated_times.write({'real_date': real_date})
                    res_warehouse = self.env['transit.warehouse'].create({
                        'purchase_order_id': self.purchase_order_id.id,
                        'create_view': False,
                        'estimated_days': stage_next.estimated_time,
                        'stage_entry_date': real_date,
                        'shipping_company': self.purchase_order_id.warehouse_company.id or False
                    })
                    self.env['estimated.time'].create({
                        'stage_name': stage_next.name,
                        'entry_date': real_date,
                        'estimated_date': fields.Datetime.from_string(real_date) + relativedelta(days=int(stage_next.estimated_time)),
                        'purchase_order_id': self.purchase_order_id.id,
                        'registry_id': res_warehouse.id
                    })
            else:
                if 'real_date' in vals and vals.get('real_date'):
                    real_date = vals.get('real_date')
                    estimated_times.write({'real_date': real_date})

        return super(AccountMoveEstimated, self).write(vals)


class TransitWarehouse(models.Model):
    _name = "transit.warehouse"
    _description = "Transito warehouse"

    def _get_detaulf_days_warehouse(self):
        return self.env.ref(
            'purchase_dashboard_stage.stage_transit_warehouse',
            raise_if_not_found=False
        ).estimated_time

    estimated_days = fields.Integer(
        string="Dias estimados",
        default=_get_detaulf_days_warehouse
    )
    stage_entry_date = fields.Datetime(
        string="create entry stage",
        default=fields.Datetime.now,
    )
    create_view = fields.Boolean(
        string='Registro creado desde la vista',
        default=False
    )
    estimated_date = fields.Datetime(
        string='Fecha estimada',
        compute="_compute_estimated_date_warehouse",
    )
    tracking_number = fields.Char(string="Número de Tracking")
    shipping_company = fields.Many2one('res.partner', string="Empresa de Envío")
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
        domain="[('purchase_id', '=', purchase_order_id),('state', '=', 'assigned')]"
    )

    @api.onchange('order_picking_id')
    def _onchange_purchase_order_id(self):
        if self.order_picking_id:
            if self.create_view:
                self.stage_entry_date = self.order_picking_id.create_date

    @api.depends('estimated_days', 'stage_entry_date')
    def _compute_estimated_date_warehouse(self):
        for rec in self:
            if rec.estimated_days and rec.stage_entry_date:
                new_estimated = rec.stage_entry_date + relativedelta(days=int(rec.estimated_days))
                try:
                    rec.estimated_date = new_estimated
                except Exception as e:
                    _logger.error("Error compute estimated_date warehouse %s" % (e))
                    pass
            else:
                rec.estimated_date = False

    @api.model
    def create(self, vals):
        if not 'write_purchase_done' in self.env.context:
            warehouse_exist = self.search([
                ('purchase_order_id', '=', vals.get('purchase_order_id')),
                ('order_picking_id', '=', vals.get('order_picking_id'))
            ])
            if warehouse_exist:
                raise ValidationError(_(
                    'La orden de entrega << %s >> en Transito Warehouse ya se encuentra seleccionada' % (
                        warehouse_exist.order_picking_id.name
                    )
                ))
            res = super(TransitWarehouse, self).create(vals)
            if 'create_view' in vals and vals.get('create_view'):
                stage_warehouse = self.env.ref('purchase_dashboard_stage.stage_transit_warehouse', raise_if_not_found=False)
                real_date_warehouse = vals.get('warehouse_receipt_date') \
                    if 'warehouse_receipt_date' in vals and vals.get('warehouse_receipt_date') \
                    else False
                self.env['estimated.time'].create({
                    'stage_name': stage_warehouse.name,
                    'entry_date': res.stage_entry_date,
                    'estimated_date': fields.Datetime.from_string(res.stage_entry_date) + relativedelta(days=int(stage_warehouse.estimated_time)),
                    'purchase_order_id': res.purchase_order_id.id,
                    'real_date': real_date_warehouse,
                    'registry_id': res.id,
                    'pick_id': res.order_picking_id.id if res.order_picking_id else False
                })
                if 'warehouse_receipt_date' in vals and vals.get('warehouse_receipt_date'):
                    stage_next = self.env.ref('purchase_dashboard_stage.stage_transit_marine_land', raise_if_not_found=False)
                    warehouse_date = vals.get('warehouse_receipt_date')
                    res_warehouse = self.env['transit.land.maritime'].create({
                        'purchase_order_id': res.purchase_order_id.id,
                        'estimated_days': stage_next.estimated_time,
                        'stage_entry_date': warehouse_date,
                        'create_from': res.id,
                        'order_picking_id': res.order_picking_id.id
                    })
                    self.env['estimated.time'].create({
                        'stage_name': stage_next.name,
                        'entry_date': warehouse_date,
                        'estimated_date': fields.Datetime.from_string(warehouse_date) + relativedelta(days=int(stage_next.estimated_time)),
                        'purchase_order_id': res.purchase_order_id.id,
                        'registry_id': res_warehouse.id,
                        'pick_id': res.order_picking_id.id if res.order_picking_id else False
                    })
            return res
        return self

    @api.model
    def write(self, vals):
        if not 'write_purchase_done' in self.env.context:
            if 'order_picking_id' in vals and vals.get('order_picking_id'):
                warehouse_exist = self.search([
                    ('purchase_order_id', '=', self.purchase_order_id.id),
                    ('order_picking_id', '=', vals.get('order_picking_id'))
                ])
                if warehouse_exist:
                    raise ValidationError(_(
                        'La orden de entrega %s en Transito Warehouse ya se encuentra seleccionada' % (
                            warehouse_exist.order_picking_id.name
                        )
                    ))
            stage_next = self.env.ref('purchase_dashboard_stage.stage_transit_marine_land', raise_if_not_found=False)
            estimated_times = self.env['estimated.time'].search([
                ('purchase_order_id', '=', self.purchase_order_id.id),
                ('registry_id', '=', self.id)
            ])

            if 'estimated_days' in vals and vals.get('estimated_days'):
                new_estimated = self.stage_entry_date + relativedelta(days=int(vals.get('estimated_days')))
                estimated_times.write({'estimated_date': new_estimated})

            pick_id = 0
            if 'order_picking_id' in vals and vals.get('order_picking_id'):
                pick_id = self.env['stock.picking'].sudo().search([('id', '=', int(vals.get('order_picking_id')))]).id
                if pick_id:
                    estimated_times.write({'pick_id': pick_id})

            if 'warehouse_receipt_date' in vals and vals.get('warehouse_receipt_date'):
                warehouse_date = vals.get('warehouse_receipt_date')
                estimated_times.write({
                    'real_date': warehouse_date,
                    'pick_id': pick_id if pick_id else False
                })
                res_warehouse = self.env['transit.land.maritime'].create({
                    'purchase_order_id': self.purchase_order_id.id,
                    'estimated_days': stage_next.estimated_time,
                    'stage_entry_date': warehouse_date,
                    'create_from': self.id,
                    'order_picking_id': int(vals.get('order_picking_id'))\
                        if ('order_picking_id' in vals and vals.get('order_picking_id'))\
                             else self.order_picking_id.id
                })
                self.env['estimated.time'].create({
                    'stage_name': stage_next.name,
                    'entry_date': warehouse_date,
                    'estimated_date': fields.Datetime.from_string(warehouse_date) + relativedelta(days=int(stage_next.estimated_time)),
                    'purchase_order_id': self.purchase_order_id.id,
                    'registry_id': res_warehouse.id,
                    'pick_id': res_warehouse.order_picking_id.id
                })
        return super(TransitWarehouse, self).write(vals)

class TransitLandMaritime(models.Model):
    _name = "transit.land.maritime"
    _description = "Tránsito Maritimo/Terrestre"

    def _get_detaulf_days_land_maritime(self):
        return self.env.ref(
            'purchase_dashboard_stage.stage_transit_marine_land',
            raise_if_not_found=False
        ).estimated_time

    estimated_days = fields.Integer(
        string="Dias estimados",
        default=_get_detaulf_days_land_maritime
    )
    stage_entry_date = fields.Datetime(
        string="create entry stage",
        default=fields.Datetime.now,
    )
    create_from = fields.Integer(string="creado desde")
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
        string="Fecha estimada de llegada al puerto",
        compute="_compute_estimated_date_land_maritime"
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
        domain="[('purchase_id', '=', purchase_order_id), ('state', '=', 'assigned')]"
    )

    @api.depends('estimated_days', 'stage_entry_date')
    def _compute_estimated_date_land_maritime(self):
        for rec in self:
            if rec.estimated_days and rec.stage_entry_date:
                new_estimated = rec.stage_entry_date + relativedelta(days=int(rec.estimated_days))
                try:
                    rec.estimated_port_arrival = new_estimated
                except Exception as e:
                    _logger.error("Error compute estimated_port_arrival land maritime %s" % (e))
                    pass
            else:
                rec.estimated_port_arrival = False

    @api.model
    def write(self, vals):
        if not 'write_purchase_done' in self.env.context:
            stage_next = self.env.ref('purchase_dashboard_stage.stage_stock_reception', raise_if_not_found=False)
            estimated_times = self.env['estimated.time'].search([
                ('purchase_order_id', '=', self.purchase_order_id.id),
                ('registry_id', '=', self.id)
            ])
            if 'estimated_days' in vals and vals.get('estimated_days'):
                new_estimated = self.stage_entry_date + relativedelta(days=int(vals.get('estimated_days')))
                estimated_times.write({
                    'estimated_date': new_estimated
                })
            if 'order_picking_id' in vals and vals.get('order_picking_id'):
                pick = self.env['stock.picking'].sudo().search([('id', '=', int(vals.get('order_picking_id')))])
                if pick:
                    estimated_times.write({'pick_id': pick.id})

            if 'real_date_arrival' in vals and vals.get('real_date_arrival'):
                real_date_arrival = vals.get('real_date_arrival')
                estimated_times.write({'real_date': real_date_arrival})
                res_stock = self.env['stock.receipt'].create({
                    'purchase_order_id': self.purchase_order_id.id,
                    'estimated_days': stage_next.estimated_time,
                    'stage_entry_date': real_date_arrival,
                    'create_from': self.id
                })
                self.env['estimated.time'].create({
                    'stage_name': stage_next.name,
                    'entry_date': real_date_arrival,
                    'estimated_date': fields.Datetime.from_string(real_date_arrival) + relativedelta(days=int(stage_next.estimated_time)),
                    'purchase_order_id': self.purchase_order_id.id,
                    'registry_id': res_stock.id
                })
        return super(TransitLandMaritime, self).write(vals)

class StockReceipt(models.Model):
    _name = 'stock.receipt'
    _description = 'Recepción Almacen'

    def _get_detaulf_days_stock(self):
        return self.env.ref(
            'purchase_dashboard_stage.stage_stock_reception',
            raise_if_not_found=False
        ).estimated_time

    estimated_days = fields.Integer(
        string="Dias estimados",
        default=_get_detaulf_days_stock
    )
    stage_entry_date = fields.Datetime(
        string="create entry stage",
        default=fields.Datetime.now,
    )
    create_from = fields.Integer(string="creado desde")
    estimated_date = fields.Datetime(
        string='Fecha estimada',
        compute="_compute_estimated_date_stock",
    )
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
        domain="[('purchase_id', '=', purchase_order_id),('state', '=', 'done')]"
    )

    @api.onchange('order_picking_id')
    def _onchange_purchase_order_id(self):
        if self.order_picking_id:
            self.stock_receipt_date = self.order_picking_id.date_done

    @api.depends('estimated_days', 'stage_entry_date')
    def _compute_estimated_date_stock(self):
        for rec in self:
            if rec.estimated_days and rec.stage_entry_date:
                new_estimated = rec.stage_entry_date + relativedelta(days=int(rec.estimated_days))
                try:
                    rec.estimated_date = new_estimated
                except Exception as e:
                    _logger.error("Error compute estimated_port_arrival land maritime %s" % (e))
                    pass
            else:
                rec.estimated_date = False

    @api.model
    def write(self, vals):
        if not 'write_purchase_done' in self.env.context:
            estimated_times = self.env['estimated.time'].search([
                ('purchase_order_id', '=', self.purchase_order_id.id),
                ('registry_id', '=', self.id)
            ])
            if 'estimated_days' in vals and vals.get('estimated_days'):
                new_estimated = self.stage_entry_date + relativedelta(days=int(vals.get('estimated_days')))
                estimated_times.write({
                    'estimated_date': new_estimated
                })
            if 'stock_receipt_date' in vals and vals.get('stock_receipt_date'):
                date_stock = vals.get('stock_receipt_date')
                estimated_times.write({'real_date': date_stock})
            return super(StockReceipt, self).write(vals)