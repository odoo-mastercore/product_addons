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

    weight_provider_total = fields.Float('Peso Total')
    volume_provider_total = fields.Float('Volumen Total')
    pallets_ids = fields.One2many(
        'account.move.pallets',
        'move_id',
        string='Pallets'
    )