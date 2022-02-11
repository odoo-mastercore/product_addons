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
    def _compute_stage_id(self):
        for rec in self:
            if rec.quotation_count == 0:
                if len(rec.order_ids) == 0:
                    stage = self.env['crm.stage'].search(
                        [('name', '=', 'Contacto Inicial')]
                    )
                    self.stage_id = stage.id
                elif len(rec.order_ids) == 1:
                    order = rec.order_ids[0].state
                    if order == 'sale':
                        stage = self.env['crm.stage'].search(
                            [('name', '=', 'Apartado de Inventario')]
                        )
                        self.stage_id = stage.id
                else:
                    order = self.env['sale.order'].search(
                        [('opportunity_id.id', '=', rec.id)]
                    )
                    pass
            elif rec.quotation_count == 1:
                order_stage = rec.order_ids[0].state
                if order_stage == 'draft':
                    stage = self.env['crm.stage'].search(
                        [('name', '=', 'Presupuesto')]
                    )
                    self.stage_id = stage.id
                elif order_stage == 'sent':
                    stage = self.env['crm.stage'].search(
                        [('name', '=', 'Negociación de Presupuesto')]
                    )
                    self.stage_id = stage.id
                elif order_stage == 'done' or order_stage == 'cancel':
                    stage = self.env['crm.stage'].search(
                        [('name', '=', 'Perdida')]
                    )
                    self.stage_id = stage.id
            else:
                if rec.quotation_count > 1:
                    for order in rec.order_ids:
                        pass
                


    stage_id = fields.Many2one(
        compute=_compute_stage_id,
        store=True
    )

