# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class partner(models.Model):
    _inherit = 'res.partner'

    warehouse_id = fields.Many2one('stock.warehouse', string="Depósito")

    @api.model
    def create(self, vals):
        rec = super(partner, self).create(vals)
        domain = []
        if rec.municipality_id:
            domain.append(('municipality_ids', 'in', [rec.municipality_id.id]))

        warehouse = self.env['stock.warehouse'].search(domain, limit=1)
        if warehouse:
            rec.warehouse_id = warehouse.id
        else:
            domain = []
            if rec.state_id:
                domain.append(('state_ids', 'in', [rec.state_id.id]))
            warehouse_state = self.env['stock.warehouse'].search(domain, limit=1)
            if warehouse_state:
                rec.warehouse_id = warehouse_state.id
            else:
                rec.warehouse_id = False

        return rec
