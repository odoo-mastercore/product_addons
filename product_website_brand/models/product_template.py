# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    web_categories = fields.Char(string='Categorias web', compute='_compute_website_categories', store=True)

    @api.depends('public_categ_ids')
    def _compute_website_categories(self):
       for record in self:
            if record.public_categ_ids:
                web_categories = ', '.join([p.name for p in record.public_categ_ids])
            else:
                web_categories = ''
            
            record.web_categories = web_categories