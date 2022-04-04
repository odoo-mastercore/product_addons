# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_published = fields.Boolean('Is Published', copy=False, default=lambda self: self._default_is_published())

    def _default_is_published(self):
        return False
        
    def publish_product(self):
        self.is_published = True

    def hide_product(self):
        self.is_published = False