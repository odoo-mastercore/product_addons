# -*- coding: utf-8 -*-
###############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = "Product Template"


    tariff_code = fields.Char(
        string='Tariff Code', 
        size=10
    )

    @api.model
    def create(self, values):
        res = super(ProductTemplate, self).create(values)
        if res.tariff_code:
            if len(res.tariff_code) < 6 or len(res.tariff_code) > 10:
                raise ValidationError(_('Tariff code must be between 6 to 10 digits'))
        return res


    def write(self, values):
        res = super(ProductTemplate, self).write(values)
        if values.get('tariff_code'):
            if len(values.get('tariff_code')) < 6 or len(values.get('tariff_code')) > 10:
                raise ValidationError(_('Tariff code must be between 6 to 10 digits'))
        return res


