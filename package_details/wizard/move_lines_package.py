# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class StockPickingPackageWizard(models.TransientModel):

    _name = "stock.picking.package.wizard"
    
    move_line_ids = fields.Many2many('stock.move.line', string='Operations')
    width = fields.Float(string="Ancho", default=0)
    height = fields.Float(string="Alto", default=0)
    length = fields.Float(string="Largo", default=0)
    weight = fields.Float(string="Peso", default=0)
    volumen = fields.Float(string="Volumen", default=0)
    package_type = fields.Selection([
        ('box', 'Caja'),
        ('envelope', 'Sobre')
        ], string="Tipo de paquete")


    def execute(self):
        for rec in self:
            package_id = self.env['stock.quant.package'].create({
                'width': rec.width,
                'height': rec.height,
                'length': rec.length,
                'weight': rec.weight,
                'volumen': rec.volumen,
                'package_type': rec.package_type
            })
            
            for move in rec.move_line_ids:
                move.write({
                    'result_package_id' : package_id.id
                })
            