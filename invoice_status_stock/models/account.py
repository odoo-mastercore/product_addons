# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_type = fields.Selection(
        selection=[
            ('cash_payment','Pago de Contado'), 
            ('credit_payment','Pago a Credito')
        ],string="Tipo de Pago",
        help="Seleccione el tipo de pago."
    )
    authorized_clearence = fields.Boolean(
        string="Despacho Autorizado",
        default=False
    )

    def authorized_dispatch(self):
        for record in self:
            if (record.payment_type == 'credit_payment' and
                    not record.authorized_clearence):
                record.authorized_clearence = True


