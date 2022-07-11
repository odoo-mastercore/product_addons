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


class ProductTemplate(models.Model):
    _inherit = "stock.quant.package"

    width = fields.Float(string="Ancho")
    height = fields.Float(string="Alto")
    length = fields.Float(string="Largo")
    weight = fields.Float(string="Peso")
    volumen = fields.Float(string="Volumen")
    package_type = fields.Selection([
        ('box', 'Caja'),
        ('envelope', 'Sobre')
        ], string="Tipo de paquete")