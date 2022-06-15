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
        for rec in self:
            if len(rec.order_ids) == 0:
                stage = self.env['crm.stage'].search(
                    [('name', '=', 'Contacto Inicial')]
                )
                self.stage_id = stage.id
            elif len(rec.order_ids) == 1:
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
                else:
                    pass
            elif len(rec.order_ids) >= 2:
                pass


    stage_id = fields.Many2one(
        compute="_compute_stage",
        index=True,
        store=True,
        readonly=True
    )


