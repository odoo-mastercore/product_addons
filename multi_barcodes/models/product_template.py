# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.osv import expression

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_ids = fields.One2many(
        'multi.barcode.products', 'product_template_id', string='Barcodes')
    optionals_barcodes = fields.Char(
        string='Barcodes', store=True,
        compute="_compute_barcodes")

    @api.depends('barcode_ids')
    def _compute_barcodes(self):
        for rec in self:
            if rec.barcode_ids:
                list_reference = ""
                for barcode in rec.barcode_ids:
                    if barcode.barcode:
                        list_reference += "<" + barcode.barcode
                rec.optionals_barcodes = list_reference
            else:
                rec.optionals_names = ""

class ProductMultiBarcode(models.Model):
    _name = 'multi.barcode.products'

    barcode = fields.Char(string="Barcode", 
        help="Provide alternate barcodes for this product")
    product_template_id = fields.Many2one('product.template')

    def get_barcode_val(self, product):
        # returns barcode of record in self and product id
        return self.barcode, product
