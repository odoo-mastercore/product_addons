# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class ProductSaleCategory(models.Model):
    _name = 'product.sale.category'
    _rec_name = "category"

    category = fields.Char(string='Category')
    start_interval = fields.Integer(string='Start interval')
    end_interval = fields.Integer(string='End interval')
    active = fields.Boolean(string='Active')





class ProductCategoryHistory(models.Model):
    _name = 'product.category.history'
    _rec_name = 'category_id'

    category_id = fields.Many2one('product.sale.category', string='Category')
    product_template_id = fields.Many2one('product.template')
    date = fields.Date(string='Date')


    @api.model
    def _cron_generate_classification(self):
        """
            Generates classification based on month sales
        """
        categories = self.env['product.sale.category'].search([
            ('active', '=', True)])
        for product in self.env['product.template'].search([
            ('active', '=', True)]):
            last_sale = self.env['sale.report'].search([
                ('product_tmpl_id', '=', product.id)], limit=1)
            rate_sale = 0
            if last_sale.date:
                date_obj = (last_sale.date).strftime("%Y-%m-%d")
                today = (fields.Date.context_today(self)).strftime("%Y-%m-%d")
                rate_sale = (
                    datetime.strptime(today, '%Y-%m-%d') - datetime.strptime(
                        date_obj, '%Y-%m-%d')).days
                if rate_sale == 0:
                    rate_sale +=1
            for categ in categories:
                if rate_sale >= categ.start_interval and rate_sale <= categ.end_interval:
                    self.env['product.category.history'].create({
                        'category_id': categ.id,
                        'product_template_id': product.id,
                        'date': fields.Date.context_today(self),
                    })