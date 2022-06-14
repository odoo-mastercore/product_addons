# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2021-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = "res.company"

    warehouse_fiscal = fields.Boolean(string='Almacenes no Fiscales',)
    warehouse_fiscal_id = fields.Many2one('stock.warehouse', string="Depósito")
