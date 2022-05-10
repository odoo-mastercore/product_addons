# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    monthly_fiscal_purchase = fields.Boolean('Monthly fiscal purchase')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sale_origin_create = fields.Char('Origen de creación')