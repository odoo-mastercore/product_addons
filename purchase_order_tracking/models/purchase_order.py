# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

import logging
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    def _get_default_volume_uom(self):
        return self.env['product.template']._get_volume_uom_name_from_ir_config_parameter()

    def _get_detaulf_days_init(self):
        return self.env.ref(
            'purchase_dashboard_stage.stage_requisition_order',
            raise_if_not_found=False
        ).estimated_time

    def _get_estimated_stock(self):
        estimated_times = self.env['purchase.order.stage'].search([])
        total_days = 0
        for estimated in estimated_times:
            if estimated.estimated_time:
                total_days += int(estimated.estimated_time.strip())
        return fields.Datetime.now() + relativedelta(days=int(total_days))

    # stage 1
    # date_order es la estimada de requisicion
    warehouse_company = fields.Many2one(
        'res.partner',
        string="Empresa Warehouse",
        compute="_compute_warehouse_company",
        store=True,
        readonly=False
    )
    origin_purchase = fields.Many2one(
        'res.country',
        string='Origin of the purchase', ondelete='restrict'
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
        string="Peso total",
        compute="_compute_weight_total",
        store=True,
    )
    weight_uom_name = fields.Char(
        string="weight uom",
        compute="_compute_weight_uom_name",
        default=_get_default_weight_uom
    )
    volume_total = fields.Float(
        string="Volumen total",
        compute="_compute_weight_total",
        store=True,
    )
    volume_uom_name = fields.Char(
        string="volume uom",
        compute='_compute_volume_uom_name',
        default=_get_default_volume_uom
    )
    estimated_days_init = fields.Integer(
        string="Dias estimados Requisición",
        default=_get_detaulf_days_init
    )
    estimated_stock_date = fields.Datetime(
        string='Fecha de recepción estimada',
        default=_get_estimated_stock,
        compute="_compute_estimated_stock"
    )
    # stage 2
    oc_provider_ids = fields.One2many(
        'order.purchase.provider',
        'purchase_order_id',
        string='Colocación Orden/Compra',
    )
    # stage 3
    supplier_ids = fields.One2many(
        'account.move.estimated',
        'purchase_order_id',
        string='Factura/Pago/Entrega',
    )
    supplier_weight_total = fields.Float(
        string="Peso total",
        compute="_compute_supplier_ids",
    )
    supplier_volume_total = fields.Float(
        string="Volume total",
        compute="_compute_supplier_ids",
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
    # Estimated times
    estimated_time_ids = fields.One2many(
        'estimated.time',
        'purchase_order_id',
        string='Tiempo estimado',
    )

    @api.depends('transit_warehouse_ids')
    def _compute_warehouse_company(self):
        for order in self:
            if not order.warehouse_company:
                warehouse = False
                if order.transit_warehouse_ids:
                    for wh in order.transit_warehouse_ids:
                        warehouse = wh.shipping_company
                order.warehouse_company = warehouse


    @api.depends("order_line.weight", "order_line.volume", "purchase_type")
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

    @api.depends('supplier_ids')
    def _compute_supplier_ids(self):
        for order in self:
            weight = volume = 0
            if order.supplier_ids:
                for supplier in order.supplier_ids:
                    weight += supplier.invoice_id.weight_provider_total
                    volume += supplier.invoice_id.volume_provider_total
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
            if invoices:
                for invoice in invoices:
                    weight += invoice.weight_provider_total
                    volume += invoice.volume_provider_total
            order.warehouse_weight_total = weight
            order.warehouse_volume_total = volume

    def action_view_invoice(self):
        stage_invoice = self.env.ref('purchase_dashboard_stage.stage_invoice_payment', raise_if_not_found=False)
        if len(self.supplier_ids) == 0:
            if self.stage_id.id != stage_invoice.id:
                raise ValidationError(_("Debe estar en la etapa << %s >> para poder crear una factura" % (stage_invoice.name)))
        result = super().action_view_invoice()
        result['context'].update({'default_purchase_type': self.purchase_type})
        return result

    def button_confirm(self):
        rec = super(PurchaseOrder, self).button_confirm()
        for po in self:
            if po.purchase_type == 'international':
                stage_init = self.env.ref('purchase_dashboard_stage.stage_requisition_order', raise_if_not_found=False)
                stage_next = self.env.ref('purchase_dashboard_stage.stage_purchase_order', raise_if_not_found=False)
                estimated_times = self.env['estimated.time'].search([
                    ('purchase_order_id', '=', po.id),
                    ('registry_id', '=', po.id)
                ])
                if stage_init.name == estimated_times.stage_name:
                    try:
                        estimated_times.write({
                            'real_date': fields.Datetime.now()
                        })
                        res_provider = self.env['order.purchase.provider'].create({
                            'estimated_days': stage_next.estimated_time,
                            'stage_entry_date': fields.Datetime.now(),
                            'purchase_order_id': po.id
                        })
                        self.env['estimated.time'].create({
                            'stage_name': stage_next.name,
                            'entry_date': fields.Datetime.now(),
                            'estimated_date': self.estimated(fields.Datetime.now(), stage_next.estimated_time),
                            'purchase_order_id': po.id,
                            'registry_id': res_provider.id
                        })
                        po.stage_id = stage_next.id

                        self.picking_ids[0].write({'scheduled_date': self.estimated_stock_date})
                    except Exception as e:
                        _logger.error("Error - button_confirm %s" % (e))
                        pass
        return rec

    def estimated(self, date, estimated_days):
        return (date + (relativedelta(days=int(estimated_days))))

    def _compute_estimated_stock(self):
        if self.purchase_type == 'international':
            estimated_times = self.env['purchase.order.stage'].search([])
            stage_requisition = self.env.ref('purchase_dashboard_stage.stage_requisition_order', raise_if_not_found=False)
            stage_order = self.env.ref('purchase_dashboard_stage.stage_purchase_order', raise_if_not_found=False)
            stage_invoice = self.env.ref('purchase_dashboard_stage.stage_invoice_payment', raise_if_not_found=False)
            stage_warehouse = self.env.ref('purchase_dashboard_stage.stage_transit_warehouse', raise_if_not_found=False)
            stage_transit = self.env.ref('purchase_dashboard_stage.stage_transit_marine_land', raise_if_not_found=False)
            stage_stock = self.env.ref('purchase_dashboard_stage.stage_stock_reception', raise_if_not_found=False)

            stage_verification = self.env.ref('purchase_dashboard_stage.stage_cost_verification', raise_if_not_found=False)
            stage_partial = self.env.ref('purchase_dashboard_stage.stage_partial_delivery', raise_if_not_found=False)

            default_total_days = 0
            for estimated in estimated_times:
                if estimated.estimated_time:
                    default_total_days += int(estimated.estimated_time.strip())
            stock_from = 0
            if self.stock_receipt_ids:
                for stock in self.stock_receipt_ids:
                    if not stock.stock_receipt_date:
                        stock_from = stock.create_from
                        default_total_days -= int(stage_stock.estimated_time)
                        default_total_days += int(stock.estimated_days)
                        break
            transit_from = 0
            if self.transit_land_maritime_ids:
                if stock_from != 0:
                    transit = self.mapped('transit_land_maritime_ids').filtered(
                        lambda t: t.id == stock_from
                    )
                    transit_from = transit.create_from
                    days = (transit.real_date_arrival - transit.estimated_port_arrival).days
                    if days < 0:
                        new_days_estimated = (transit.estimated_days - abs(days))
                        default_total_days -= transit.estimated_days
                        default_total_days += new_days_estimated
                    elif days > 0:
                        new_days_estimated = (transit.estimated_days + days)
                        default_total_days -= transit.estimated_days
                        default_total_days += new_days_estimated
                    elif days == 0:
                        default_total_days -= int(stage_transit.estimated_time)
                        default_total_days += int(transit.estimated_days)
                else:
                    for transit in self.transit_land_maritime_ids:
                        if not transit.real_date_arrival:
                            transit_from = transit.create_from
                            default_total_days -= int(stage_transit.estimated_time)
                            default_total_days += int(transit.estimated_days)
                            break
            partial = False
            partial_date = False
            if self.transit_warehouse_ids:
                if transit_from != 0:
                    warehouse = self.mapped('transit_warehouse_ids').filtered(
                        lambda w: w.id == transit_from
                    )
                    days = (warehouse.warehouse_receipt_date - warehouse.estimated_date).days
                    if days < 0:
                        new_days_estimated = (warehouse.estimated_days - abs(days))
                        default_total_days -= warehouse.estimated_days
                        default_total_days += new_days_estimated
                    elif days > 0:
                        new_days_estimated = (warehouse.estimated_days + days)
                        default_total_days -= warehouse.estimated_days
                        default_total_days += new_days_estimated
                    elif days == 0:
                        default_total_days -= int(stage_warehouse.estimated_time)
                        default_total_days += int(warehouse.estimated_days)
                    if warehouse.create_view:
                        partial_date = warehouse.create_date
                        partial = True
                else:
                    for warehouse in self.transit_warehouse_ids:
                        if not warehouse.warehouse_receipt_date:
                            default_total_days -= int(stage_warehouse.estimated_time)
                            default_total_days += int(warehouse.estimated_days)
                            if warehouse.create_view:
                                partial_date = warehouse.create_date
                                partial = True
                            break
            if not partial:
                if self.supplier_ids:
                    invoice = self.mapped('supplier_ids').filtered(lambda i: not i.create_view)
                    if invoice.estimated_days != int(stage_invoice.estimated_time):
                        default_total_days -= int(stage_invoice.estimated_time)
                        default_total_days += invoice.estimated_days
                    if invoice.real_date:
                        days = (invoice.real_date - invoice.estimated_date).days
                        if days < 0:
                            new_days_estimated = (invoice.estimated_days - abs(days))
                            default_total_days -= invoice.estimated_days
                            default_total_days += new_days_estimated
                        else:
                            new_days_estimated = (invoice.estimated_days + days)
                            default_total_days -= invoice.estimated_days
                            default_total_days += new_days_estimated
                if self.oc_provider_ids:
                    for provider in self.oc_provider_ids:
                        if provider.estimated_days != int(stage_order.estimated_time):
                            default_total_days -= int(stage_order.estimated_time)
                            default_total_days += provider.estimated_days
                        if provider.provider_recognition_date:
                            days = (provider.provider_recognition_date - provider.provider_estimated_date).days
                            if days < 0:
                                new_days_estimated = (provider.estimated_days - abs(days))
                                default_total_days -= provider.estimated_days
                                default_total_days += new_days_estimated
                            else:
                                new_days_estimated = (provider.estimated_days + days)
                                default_total_days -= provider.estimated_days
                                default_total_days += new_days_estimated
                if self.estimated_days_init != int(stage_requisition.estimated_time):
                    default_total_days -= int(stage_requisition.estimated_time)
                    default_total_days += self.estimated_days_init
                if self.date_approve:
                    estimated_date = self.estimated(self.create_date, self.estimated_days_init)
                    days = (self.date_approve - estimated_date).days
                    if days < 0:
                        new_days_estimated = (self.estimated_days_init - abs(days))
                        default_total_days -= self.estimated_days_init
                        default_total_days += new_days_estimated
                    else:
                        new_days_estimated = (self.estimated_days_init + days)
                        default_total_days -= self.estimated_days_init
                        default_total_days += new_days_estimated
            else:
                total_day_stage = (int(stage_requisition.estimated_time) + int(stage_order.estimated_time) + int(stage_invoice.estimated_time))
                default_total_days -= total_day_stage
            if(self.stage_id.id == stage_verification.id or self.stage_id.id == stage_partial.id):
                self.estimated_stock_date = False
            else:
                if partial:
                    self.estimated_stock_date = partial_date + relativedelta(days=int(default_total_days))
                else:
                    self.estimated_stock_date = self.create_date + relativedelta(days=int(default_total_days))

                if len(self.picking_ids) == 1:
                    if self.state != 'cancel':
                        print("Pasando por aqui")
                        self.picking_ids[0].write({'scheduled_date': self.estimated_stock_date})
                # print("############################################")
                # print(stock_from)
                # print(transit_from)
        else:
            self.estimated_stock_date = False

    @api.model
    def create(self, vals):
        if vals.get('purchase_type') == 'national':
            stage_purchase_national = self.env.ref('purchase_dashboard_stage.stage_national_purchase', raise_if_not_found=False)
            vals.update({
                'stage_id': stage_purchase_national.id
            })
        rec = super(PurchaseOrder, self).create(vals)
        if rec.purchase_type == 'international':
            res_estimated_time = {
                'stage_name': rec.stage_id.name,
                'entry_date': rec.create_date,
                'estimated_date': self.estimated(rec.create_date, rec.estimated_days_init),
                'purchase_order_id': rec.id,
                'registry_id': int(rec.id)
            }
            self.env['estimated.time'].create(res_estimated_time)
        return rec

    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        context = dict(self.env.context)
        context.update({'write_purchase_done': True})
        self = self.with_context(context)
        if self.purchase_type == 'international':
            purchase_completed = True
            purchase_cancel = False
            if self.state == 'cancel':
                purchase_cancel = True
            estimated_time = self.env['estimated.time'].search([
                ('purchase_order_id', '=', self.id),
                ('registry_id', '=', self.id)
            ])
            if 'estimated_days_init' in vals and vals.get('estimated_days_init'):
                estimated_time.write({
                    'estimated_date': self.estimated(self.create_date, int(vals.get('estimated_days_init')))
                })
            if self.state not in ('draft', 'sent'):
                if self.stock_receipt_ids:
                    stock_completed = True
                    for stock in self.stock_receipt_ids:
                        if not stock.stock_receipt_date:
                            stock_completed = False
                            break
                    if not stock_completed:
                        purchase_completed = False
                        stage_stock = self.env.ref('purchase_dashboard_stage.stage_stock_reception', raise_if_not_found=False)
                        vals.update({'stage_id': stage_stock.id})
                        super(PurchaseOrder, self).write(vals)

                if self.transit_land_maritime_ids and purchase_completed:
                    transit_completed = True
                    for transit in self.transit_land_maritime_ids:
                        if not transit.real_date_arrival:
                            transit_completed = False
                            break
                    if not transit_completed:
                        purchase_completed = False
                        stage_transit = self.env.ref('purchase_dashboard_stage.stage_transit_marine_land', raise_if_not_found=False)
                        vals.update({'stage_id': stage_transit.id})
                        super(PurchaseOrder, self).write(vals)

                if self.transit_warehouse_ids and purchase_completed:
                    warehouse_completed = True
                    for warehouse in self.transit_warehouse_ids:
                        if not warehouse.warehouse_receipt_date:
                            warehouse_completed = False
                            break
                    if not warehouse_completed:
                        purchase_completed = False
                        stage_warehouse = self.env.ref('purchase_dashboard_stage.stage_transit_warehouse', raise_if_not_found=False)
                        vals.update({'stage_id': stage_warehouse.id})
                        super(PurchaseOrder, self).write(vals)

                if self.supplier_ids and purchase_completed:
                    supplier_completed = True
                    for supplier in self.supplier_ids:
                        if not supplier.real_date:
                            supplier_completed = False
                            break
                    if not supplier_completed:
                        purchase_completed = False
                        stage_invoice = self.env.ref('purchase_dashboard_stage.stage_invoice_payment', raise_if_not_found=False)
                        vals.update({'stage_id': stage_invoice.id})
                        super(PurchaseOrder, self).write(vals)

                if self.oc_provider_ids and purchase_completed:
                    provider_completed = True
                    for provider in self.oc_provider_ids:
                        if not provider.provider_recognition_date:
                            provider_completed = False
                            break
                    if not provider_completed:
                        purchase_completed = False
                        stage_order = self.env.ref('purchase_dashboard_stage.stage_purchase_order', raise_if_not_found=False)
                        vals.update({'stage_id': stage_order.id})
                        super(PurchaseOrder, self).write(vals)

                if purchase_completed and not purchase_cancel:
                    stage_verification = self.env.ref('purchase_dashboard_stage.stage_cost_verification', raise_if_not_found=False)
                    stage_partial = self.env.ref('purchase_dashboard_stage.stage_partial_delivery', raise_if_not_found=False)
                    pickings = self.env['stock.picking'].search([
                        ('purchase_id', '=', self.id),
                        ('state', '=', 'assigned')
                    ])
                    if len(pickings) > 0:
                        vals.update({'stage_id': stage_partial.id})
                    else:
                        vals.update({'stage_id': stage_verification.id})
                    super(PurchaseOrder, self).write(vals)

                if purchase_cancel:
                    stage_cancel = self.env.ref('purchase_dashboard_stage.stage_purchase_cancel', raise_if_not_found=False)
                    vals.update({'stage_id': stage_cancel.id})
                    super(PurchaseOrder, self).write(vals)

        return res


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