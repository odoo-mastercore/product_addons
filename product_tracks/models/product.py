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
    


    name = fields.Char(tracking=True)
    sale_ok = fields.Boolean(tracking=True)
    purchase_ok = fields.Boolean(tracking=True)
    is_combo = fields.Boolean(tracking=True)
    categ_id = fields.Many2one(tracking=True)
    default_code = fields.Char(tracking=True)
    barcode = fields.Char(tracking=True)
    code_group_id = fields.Many2one(tracking=True)
    vehicle_type = fields.Selection(tracking=True)
    #tag_ids = fields.Many2one(track_visibility='onchange')
    list_price = fields.Float(tracking=True)
    #taxes_id = fields.Many2many(track_visibility='onchange')
    standard_price = fields.Float(tracking=True)
    company_id = fields.Many2one(tracking=True)
    uom_id = fields.Many2one(track_visibility='onchange')
    uom_po_id = fields.Many2one(track_visibility='onchange')
    description = fields.Char(tracking=True)
    
    model_fleet_part = fields.Char(tracking=True)
    cross_reference = fields.Char(tracking=True)
    optionals_names = fields.Char(tracking=True)
    #cross_reference_ids = fields.One2many(tracking=True)
    #name_ids = fields.One2many(tracking=True)
    manufacturer = fields.Many2one(track_visibility='onchange')
    manufacturer_pname = fields.Char(tracking=True)
    manufacturer_pref = fields.Char(tracking=True)
    manufacturer_purl = fields.Char(tracking=True)
    optionals_barcodes = fields.Char(tracking=True)
    #attribute_line_ids = fields.One2many(track_visibility='onchange')
    invoice_policy = fields.Selection(tracking=True)
    expense_policy = fields.Selection(tracking=True)
    optional_product_ids = fields.Many2many(track_visibility='onchage')
    description_sale = fields.Char(tracking=True)
    website_sequence = fields.Integer(tracking=True)
    # public_categ_ids = fields.Many2many(track_visibility='always')
    # alternative_product_ids = fields.Many2many(track_visibility='always')
    # accessory_product_ids = fields.Many2many(track_visibility='onchange')
    # website_style_ids = fields.Many2many(tracking=True)
    dr_brand_id = fields.Many2one(track_visibility='onchange')
    dr_label_id = fields.Many2one(track_visibility='onchange')
    inventory_availability = fields.Selection(tracking=True)
    # seller_ids = fields.One2many(tracking=True)
    tariff_code = fields.Char(tracking=True)
    # supplier_taxed_id = fields.Many2many(tracking=True)
    purchase_method = fields.Selection(tracking=True)
    description_purchase = fields.Char(tracking=True)
    # route_ids = fields.Many2many(tracking=True)
    sale_delay = fields.Float(tracking=True)
    property_stock_production = fields.Many2one(track_visibility='onchange')
    property_stock_inventory = fields.Many2one(track_visibility='onchange')
    weight = fields.Float(tracking=True)
    volume = fields.Float(tracking=True)
    responsible_id = fields.Many2one(track_visibility='onchange')
    weight_kg = fields.Float(tracking=True)
    volume = fields.Float(tracking=True)
    dimensional_oum_id = fields.Many2one(track_visibility='onchange')
    product_length = fields.Float(tracking=True)
    product_height = fields.Float(tracking=True)
    product_width = fields.Float(tracking=True)
    description_pickingout = fields.Char(tracking=True)
    description_pickingin = fields.Char(tracking=True)
    description_picking = fields.Char(tracking=True)
    property_account_income_id = fields.Many2one(track_visibility='onchange')
    property_account_expense_id = fields.Many2one(track_visibility='onchange')
    property_account_creditor_price_difference = fields.Many2one(track_visibility='onchange')