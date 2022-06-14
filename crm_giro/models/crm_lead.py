# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    @api.depends('quotation_count')
    def _compute_stage(self):
        _logger.info("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZz")
        for rec in self:
            if len(rec.order_ids) == 0:
                stage = self.env['crm.stage'].search(
                    [('name', '=', 'Contacto Inicial')]
                )
                self.stage_id = stage.id
            elif len(rec.order_ids) == 1:
                _logger.info("####################################")
                state_order = rec.order_ids[0].state
                invoices = rec.order_ids[0].invoice_ids
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

                # invoice = len(rec.order_ids[0].invoice_ids)
                # _logger.info("Facturas " + str(invoice))
                elif len(invoices) == 1 or len(rec.order_ids[0].invoice_count) == 1:
                    _logger.info("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                    if invoices[0].payment_type == 'credit_payment':
                        _logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                        stage = self.env['crm.stage'].search(
                            [('name', '=', 'Facturación')]
                        )
                        self.stage_id = stage.id
                    # if invoices[0].payment_type == 'cash_payment':
                    else:
                    # elif len(rec.order_ids) == 1 and len(rec.order_ids[0].invoice_ids) == 1:
                        _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        stage = self.env['crm.stage'].search(
                            [('name', '=', 'Pago por Confirmar')]
                        )
                        self.stage_id = stage.id
                else:
                    pass
            elif len(rec.order_ids) >= 2:
                pass
                # for order in rec.order_ids:
                    # if order.state == 'sale':
                        # stage = self.env['crm.stage'].search(
                            # [('name', '=', 'Apartado de Inventario')]
                        # )
                        # self.stage_id = stage.id
                        # break
                    # elif order.state == 'sent':
                        # stage = self.env['crm.stage'].search(
                            # [('name', '=', 'Negociación de Presupuesto')]
                        # )
                        # self.stage_id = stage.id
                        # break
                    # else:
                        # stage = self.env['crm.stage'].search(
                            # [('name', '=', 'Presupuesto')]
                        # )
                        # self.stage_id = stage.id




            # if rec.quotation_count == 0:
                # if len(rec.order_ids) == 0:
                    # stage = self.env['crm.stage'].search(
                        # [('name', '=', 'Contacto Inicial')]
                    # )
                    # self.stage_id = stage.id
                # elif len(rec.order_ids) >= 1:
                    # order = rec.order_ids[0].state
                    # if order == 'sale':
                        # stage = self.env['crm.stage'].search(
                            # [('name', '=', 'Apartado de Inventario')]
                        # )
                        # self.stage_id = stage.id
                # else:
                    # order = self.env['sale.order'].search(
                        # [('opportunity_id.id', '=', rec.id)]
                    # )
                    # pass
            # elif rec.quotation_count == 1:
                # order_stage = rec.order_ids[0].state
                # if order_stage == 'draft':
                    # stage = self.env['crm.stage'].search(
                        # [('name', '=', 'Presupuesto')]
                    # )
                    # self.stage_id = stage.id
                # elif order_stage == 'sent':
                    # stage = self.env['crm.stage'].search(
                        # [('name', '=', 'Negociación de Presupuesto')]
                    # )
                    # self.stage_id = stage.id
                # elif order_stage == 'done' or order_stage == 'cancel':
                    # stage = self.env['crm.stage'].search(
                        # [('name', '=', 'Perdida')]
                    # )
                    # self.stage_id = stage.id
            # else:
                # for order in rec.order_ids:
                    # if order.state == 'sale':
                        # stage = self.env['crm.stage'].search(
                            # [('name', '=', 'Apartado de Inventario')]
                        # )
                        # self.stage_id = stage.id
                        # break
                    # elif order.state == 'sent':
                        # stage = self.env['crm.stage'].search(
                            # [('name', '=', 'Negociación de Presupuesto')]
                        # )
                        # self.stage_id = stage.id
                        # break
                    # else:
                        # stage = self.env['crm.stage'].search(
                            # [('name', '=', 'Presupuesto')]
                        # )
                        # self.stage_id = stage.id
                        



    stage_id = fields.Many2one(
        compute="_compute_stage",
        index=True,
        store=True,
        readonly=True
    )


