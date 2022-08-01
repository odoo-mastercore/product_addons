# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    order = fields.Boolean(
        string="Orden",
        compute="_compute_quotation",
        default=False
    )
    stage_id = fields.Many2one(
        compute="_compute_stage",
        index=True,
        store=True,
        readonly=True
    )
    state_picking = fields.Selection(
        selection=[
            ('assigned', 'PREPARADO'),
            ('partial', 'PARCIALMENTE'),
            ('done', 'REALIZADO'),
            ('returns', 'DEVOLUCIONES'),
            ('mediation', 'RECLAMOS')
        ],
        string="Estado del Picking"
    )
    amount_total_sale = fields.Char(
        compute='_compute_amount_total_sale', 
        string="Sum of Orders", 
        help="Untaxed Total of Confirmed Orders", 
    )

    @api.depends('order_ids.currency_id')
    def _compute_amount_total_sale(self):
        for lead in self:
            total = 0.0
            if lead.order_ids:
                for order in lead.order_ids:
                    total += order.amount_total
                lead.amount_total_sale = str(total) +" "+ str(lead.order_ids[0].currency_id.name) 
            else:
                lead.amount_total_sale = None


    @api.depends('order_ids')
    def _compute_quotation(self):
        for lead in self:
            orders = self.mapped('order_ids').filtered(
                lambda o: o.state in ('draft', 'sent', 'sale')
            )
            if orders:
                lead.update({'order': True})
            else:
                lead.update({'order': False})

    @api.depends('quotation_count')
    def _compute_stage(self):
        for rec in self:
            if len(rec.order_ids) == 0:
                stage = self.env['crm.stage'].search(
                    [('name', '=', 'Contacto Inicial')]
                )
                self.stage_id = stage.id
            elif len(rec.order_ids) == 1:
                state_order = rec.order_ids[0].state
                # invoices = rec.order_ids[0].invoice_ids
                if state_order == 'draft':
                    stage = self.env['crm.stage'].search(
                        [('name', '=', 'Presupuesto')]
                    )
                    self.stage_id = stage.id
                elif state_order == 'sent':
                    stage = self.env['crm.stage'].search(
                        [('name', '=', 'Negociación de Presupuesto')]
                    )
                    self.stage_id = stage.id
                elif state_order == 'sale':
                    stage = self.env['crm.stage'].search(
                        [('name', '=', 'Apartado de Inventario')]
                    )
                    self.stage_id = stage.id
                else:
                    pass
            elif len(rec.order_ids) >= 2:
                pass

    def action_sale_quotations_new(self):
        res = super(CrmLead, self).action_sale_quotations_new()
        orders = self.mapped('order_ids').filtered(
            lambda o: o.state in ('draft', 'sent', 'sale')
        )
        if orders:
            raise UserError(_("No puede crear mas de un pedido de venta a una aportunidad"))

        return res
