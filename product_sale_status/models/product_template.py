# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    history_category_ids = fields.One2many(
        'product.category.history', 'product_template_id',
        string='Sale History')
    category_sale_id = fields.Many2one('product.category.history', 
        string='Sale status', store=True, compute="_compute_sale_status")
    
    @api.depends('history_category_ids')
    def _compute_sale_status(self):
        for rec in self:
            if rec.history_category_ids:
                rec.category_sale_id = self.env[
                    'product.category.history'].search([
                        ('product_template_id', '=', rec.id)], limit=1)
            else:
                rec.category_sale_id = []

    def action_view_classification_sale(self):
        self.ensure_one()
        action = self.env.ref(
            'product_sale_status.product_category_history_action_form').read()[0]
        action['domain'] = [('product_template_id', 'in', self.ids)]
        return action


class productProduct(models.Model):
    _inherit = 'product.product'

    def action_view_classification_sale(self):
        self.ensure_one()
        action = self.env.ref(
            'product_sale_status.product_category_history_action_form').read()[0]
        action['domain'] = [('product_template_id', 'in', self.product_tmpl_id.ids)]
        return action