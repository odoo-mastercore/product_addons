# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountMovePallets(models.Model):
    _name = 'account.move.pallets'
    _description = "Pallets and boxs"

    type = fields.Selection(
        string='Tipo', required=True,
        selection=[('pallet', 'Pallet'), ('box', 'Caja')],
        default='pallet'
    )
    long = fields.Float(string='Largo')
    width = fields.Float(string="Ancho")
    height = fields.Float(string="Alto")
    weight = fields.Float(string="Peso")
    weight_uom_name = fields.Char(related="move_id.weight_uom_name")
    volume = fields.Float(string="Volumen")
    volume_uom_name = fields.Char(related='move_id.volume_uom_name')
    move_id = fields.Many2one('account.move', string="Account Move", readonly=True)
    inches = fields.Selection(
        string='label pulgadas',
        selection=[('p', 'Pulgadas')],
        default='p',
        readonly=True
    )