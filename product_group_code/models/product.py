# -*- coding: utf-8 -*-
###############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models


class ProductGroup(models.Model):
    _name = "product.group"
    _rec_name = 'name'
    name = fields.Char(string="Codigo de Agrupamiento",)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    code_group_id = fields.Many2one('product.group', 
        string='Codigo De Agrupamiento')
