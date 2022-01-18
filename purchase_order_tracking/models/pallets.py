# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountMovePallets(models.Model):
    _name = 'account.move.pallets'

    width = fields.Float(string="Ancho")
    height = fields.Float(string="Alto")
    long = fields.Float(string="Largo")
    volume = fields.Float(string="Volumen")
    move_id = fields.Many2one('account.move', string="Account Move", readonly=True)