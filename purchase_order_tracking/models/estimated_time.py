# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class EstimatedTime(models.Model):
    _name = 'estimated.time'
    _description = 'Tiempo estimados para OC'

    stage_name = fields.Char(string='Etapa')
    entry_date = fields.Datetime(string='Fecha de entrada')
    estimated_date = fields.Datetime(string='Fecha estimada')
    real_date = fields.Datetime(string='Fecha real')

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True
    )
    registry_id = fields.Integer(string="id de registro")