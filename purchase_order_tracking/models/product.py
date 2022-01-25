# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _

KG = 2.205
MC = 35.315


class ProductTemplate(models.Model):
    _inherit = "product.template"

    weight_kg = fields.Float( string='Peso', compute="_compute_weight")
    weight_uom_kg = fields.Char(
        'weight in kg',
        default="kg",
        readonly=True
    )
    volume_mc = fields.Float(string='Volumen', compute="_compute_volume" )
    volume_uom_mc = fields.Char(
        'volume in m³',
        default="m³",
        readonly=True
    )

    @api.depends('weight')
    def _compute_weight(self):
        for rec in self:
            rec.weight_kg = round((float(rec.weight) / KG), 2)

    @api.depends('volume')
    def _compute_volume(self):
        for rec in self:
            rec.volume_mc = round((float(rec.volume) / MC), 2)