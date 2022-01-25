# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    def _get_default_volume_uom(self):
        return self.env['product.template']._get_volume_uom_name_from_ir_config_parameter()

    weight_provider_total = fields.Float('Peso total')
    weight_uom_name = fields.Char(
        string="weight uom",
        compute="_compute_weight_uom_name",
        default=_get_default_weight_uom
    )
    volume_provider_total = fields.Float('Volumen total')
    volume_uom_name = fields.Char(
        string="volume uom",
        compute='_compute_volume_uom_name',
        default=_get_default_volume_uom
    )
    purchase_type = fields.Selection(
        string='Type of Purchase', required=True,
        selection=[('international', 'Internacional'), ('national', 'Nacional')],
        default='international')
    pallets_ids = fields.One2many(
        'account.move.pallets',
        'move_id'
    )

    @api.depends('purchase_type')
    def _compute_weight_uom_name(self):
        for account in self:
            if account.purchase_type == 'international':
                account.weight_uom_name = self.env['product.template'].\
                    _get_weight_uom_name_from_ir_config_parameter()
            else:
                account.weight_uom_name = 'kg'

    @api.depends('purchase_type')
    def _compute_volume_uom_name(self):
        for account in self:
            if account.purchase_type == 'international':
                account.volume_uom_name = self.env['product.template'].\
                    _get_volume_uom_name_from_ir_config_parameter()
            else:
                account.volume_uom_name = "m³"