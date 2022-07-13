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
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    width_total = fields.Float(string="Ancho total", compute="_compute_totals")
    height_total = fields.Float(string="Alto total", compute="_compute_totals")
    length_total = fields.Float(string="Largo total", compute="_compute_totals")
    weight_total = fields.Float(string="Peso total", compute="_compute_totals")
    volumen_total = fields.Float(string="Volumen total", compute="_compute_totals")
    packages_total = fields.Integer(string="Paquetes totales", compute="_compute_totals")
    dispatcher_id = fields.Many2one('res.partner', string='Despachador')

    def put_in_pack(self):
        for rec in self:
            move_line_ids = []
            if len(rec.move_line_ids) > 1:
                for line in rec.move_line_ids:
                    if not line.result_package_id:
                        move_line_ids.append(line.id)
                return {
                    'name':'Asignar paquetes',
                    'view_mode': 'form',
                    'view_id': self.env.ref('package_details.moves_lines_package_wizard_form').id,
                    'view_type': 'form',
                    'res_model': 'stock.picking.package.wizard',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_move_line_ids': move_line_ids}
                }

        rec = super(StockPickingInherit, self).put_in_pack()
        return rec

    @api.depends('move_line_ids')
    def _compute_totals(self):
        for rec in self:
            width = 0
            height = 0
            length = 0
            weight = 0
            volumen = 0
            qty_package = 0
            if rec.move_line_ids:
                packages = self.move_line_ids.mapped('result_package_id')
                if packages:
                    qty_package = len(packages)
                    for package in packages:
                        width += package.width
                        height += package.height
                        length += package.length
                        weight += package.weight
                        volumen += package.volumen

            rec.width_total = width
            rec.height_total = height
            rec.length_total = length
            rec.weight_total = weight
            rec.volumen_total = volumen
            rec.packages_total = qty_package