# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class SaleCouponProgram(models.Model):
    _inherit = 'sale.coupon.program'

    rule_max_quantity = fields.Integer(string="Maximun Quantity",
        help="Maximun required product quantity to get the reward")

    def _filter_programs_on_products(self, order):
        """
        To get valid programs according to product list.
        i.e Buy 1 imac + get 1 ipad mini free then check 1 imac is on cart or not
        or  Buy 1 coke + get 1 coke free then check 2 cokes are on cart or not
        """
        order_lines = order.order_line.filtered(
            lambda line: line.product_id) - order._get_reward_lines()
        products = order_lines.mapped('product_id')
        products_qties = dict.fromkeys(products, 0)
        for line in order_lines:
            products_qties[line.product_id] += line.product_uom_qty
        valid_program_ids = list()
        for program in self:
            if not program.rule_products_domain:
                valid_program_ids.append(program.id)
                continue
            valid_products = program._get_valid_products(products)
            if not valid_products:
                # The program can be directly discarded
                continue
            ordered_rule_products_qty = sum(
                products_qties[product] for product in valid_products)
            # Avoid program if 1 ordered foo on a program '1 foo, 1 free foo'
            if program.promo_applicability == 'on_current_order' and \
               program.reward_type == 'product' and program._get_valid_products(program.reward_product_id):
                ordered_rule_products_qty -= program.reward_product_quantity
            if program.rule_max_quantity > 0:
                _logger.warning('-----------------------------------IF MAX')
                if ordered_rule_products_qty < program.rule_max_quantity:
                    valid_program_ids.append(program.id)
            else:
                _logger.warning('-----------------------------------ELSE MAX')
                if ordered_rule_products_qty >= program.rule_min_quantity:
                    valid_program_ids.append(program.id)
        return self.browse(valid_program_ids)
