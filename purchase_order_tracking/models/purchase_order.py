# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin_purchase = fields.Char(
        related='partner_id.country_id.name',
        readonly=True,
        string="Origin of purchase"
    )
    load_type = fields.Selection(
        string='Type of load', required=True,
        selection=[('marine', 'Maritima'), ('land', 'Terrestre')],
        default='marine')
    provider_estimated_date = fields.Datetime(
        string='Provider estimated date',
    )
    provider_recognition_date = fields.Datetime(
        string='Recognition date',
    )
    provider_recognition_number = fields.Char(
        string="Recognition number"
    )
    provider_number_tracking = fields.Char(
        string="Number of Tracking"
    )