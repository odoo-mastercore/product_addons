# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.osv import expression
import logging

_logger = logging.getLogger(__name__)


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    width = fields.Float(string="Ancho", default=0)
    height = fields.Float(string="Alto", default=0)
    length = fields.Float(string="Largo", default=0)
    weight = fields.Float(string="Peso", default=0)
    volumen = fields.Float(string="Volumen", default=0)
    package_type = fields.Selection([
        ('box', 'Caja'),
        ('envelope', 'Sobre')
        ], string="Tipo de paquete")