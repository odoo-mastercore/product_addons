# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    
    def _compute_state_invoice(self):
        if self.sale_id:
            if self.sale_id.invoice_count >= 1:
                for rec in self:
                    if rec.sale_id.invoice_ids[0].invoice_payment_state == 'paid':
                        rec.state_invoice = "PAGADA"
                    elif rec.sale_id.invoice_ids[0].invoice_payment_state == 'in_payment':
                        rec.state_invoice = "PROCESO"
                    else:
                        rec.state_invoice = "NO_PAGO"
                        if rec.sale_id.invoice_ids[0].payment_type == 'credit_payment':
                            rec.state_invoice = 'CREDITO'
            else:
                self.state_invoice = "SIN_FACTURA"
        else:
            self.state_invoice = "N/A"


    def _compute_withdrawal_payment(self):
        if self.sale_id:
            for rec in self:
                rec.withdrawal_type = rec.sale_id.withdrawal_type
                rec.by_payment = rec.sale_id.by_payment
        else:
            self.withdrawal_type = ""
            self.by_payment = ""


    invoice_id = fields.Many2one('account.move', string="Factura")
    state_invoice = fields.Char(
        string="Status Factura",
        compute="_compute_state_invoice",
        # store=True
    )
    withdrawal_type = fields.Selection(
        [
            ('office_retreat', 'Retiro en Oficina'),
            ('shipping_to_freight', 'Envíar a Fletera')
        ],string="Tipo de Retiro",
        compute="_compute_withdrawal_payment",
        help="Indica si el pedido sera retirado en Oficina o enviado a Fletera."
    )
    by_payment = fields.Selection(
        [
            ('charge_at_destination', 'Cobro en Destino'),
            ('pay_per_giro', 'Pago por Giro')
        ],string="Pagado por",
        compute="_compute_withdrawal_payment",
    )
    fleet_contact_id = fields.Many2one(
        'fleet.contact',
        related='sale_id.fleet_contact_id',
        string="Fleet Contact"
    )


    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.sale_id:
            if self.sale_id.invoice_count >= 1:
                if self.state_invoice == "PAGADA" or self.state_invoice == "CREDITO":
                    return res
                else:
                    raise UserError(_(' No puede validar una transferencia si no tiene factura pagada o factura a credito.'))
            else:
                raise UserError(_(' No puede validar una transferencia si no tiene factura pagada o factura a credito.'))
        else:
            return res

