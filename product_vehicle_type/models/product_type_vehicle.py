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
    
    vehicle_type = fields.Selection(string='Tipo de vehículo',
                             selection=[('liviano', 'Vehículo Liviano'),('pesado', 'Vehículo Pesado')])

class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    vehicle_type = fields.Selection(string='Tipo de vehículo',
                             selection=[('liviano', 'Vehículo Liviano'),('pesado', 'Vehículo Pesado')])

class FleetVehicleModelBrand(models.Model):
    _inherit = 'fleet.vehicle.model.brand'

    vehicle_type = fields.Selection(string='Tipo de vehículo',
                             selection=[('liviano', 'Vehículo Liviano'),('pesado', 'Vehículo Pesado')])
