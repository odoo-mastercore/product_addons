# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _


class SaleCouponRule(models.Model):
    _inherit = 'sale.coupon.rule'

    rule_max_quantity = fields.Integer(string="Maximun Quantity",
        help="Maximun required product quantity to get the reward")
