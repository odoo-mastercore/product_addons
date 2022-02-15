# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.purchase_id.transit_warehouse_ids:
            Warehouse = self.mapped('purchase_id.transit_warehouse_ids')\
                .filtered(lambda p: p.order_picking_id.id == self.id)
            if Warehouse and not Warehouse.warehouse_receipt_date:
                raise ValidationError(_(
                    'La orden de entrega se encuentra en Transito Warehouse'
                ))
        else:
            raise ValidationError(_(
                'No se encontro transito en la orden de entrega.'
            ))
        if self.purchase_id.transit_land_maritime_ids:
            Transit = self.mapped('purchase_id.transit_land_maritime_ids')\
                .filtered(lambda p: p.order_picking_id.id == self.id)
            if Transit and not Transit.real_date_arrival:
                raise ValidationError(_(
                    'La orden de entrega se encuentra en Transito Maritimo/Terrestre'
                ))
        return res