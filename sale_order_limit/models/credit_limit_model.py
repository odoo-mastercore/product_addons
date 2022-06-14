# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2022-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _
from odoo.tools.translate import _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    warning_stage = fields.Float(string='Monto de advertencia',
                                 help="Aparecerá un mensaje de advertencia una vez que el cliente seleccionado haya cruzado la cantidad de advertencia"
                                 )
    blocking_stage = fields.Float(string='Monto de bloqueo',
                                  help="No se pueden realizar ventas una vez que se cruza el monto de bloqueo del cliente seleccionado"
                                  )
    due_amount = fields.Float(string="Total de deuda", compute="compute_due_amount")
    is_debtor = fields.Boolean(string="Es deudor", compute="_compute_debts_active")
    active_limit = fields.Boolean("Activar limite de credito", default=False)
    invoices_debts_name = fields.Char("Facturas adeudadas")

    def compute_due_amount(self):
        for rec in self:
            if not rec.id:
                continue
            debts_amount = rec.env['account.move'].search([
                ('partner_id', '=', rec.id),
                ('type', '=', 'out_invoice'),
                ('invoice_payment_state', 'in', ['not_paid','in_payment']),
                ('state', '=', 'posted')])
            
            debit_amount = 0
            invoice_debts = ''
            if debts_amount:
                for debt in debts_amount:
                    debit_amount += debt.amount_residual
                    invoice_debts += ' ' + debt.name
            rec.invoices_debts_name = invoice_debts
            rec.due_amount = debit_amount
    
    @api.depends('due_amount')
    def _compute_debts_active(self):
        for rec in self:
            if rec.active_limit:
                if rec.due_amount >= rec.blocking_stage:
                    rec.is_debtor = True
                else:
                    rec.is_debtor = False


    @api.constrains('warning_stage', 'blocking_stage')
    def constrains_warning_stage(self):
        if self.active_limit:
            if self.warning_stage >= self.blocking_stage:
                if self.blocking_stage > 0:
                    raise UserError(_("Monto de advertencia debe ser menor al monto de bloqueo"))

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_due = fields.Boolean()
    is_warning = fields.Boolean()
    due_amount = fields.Float(related='partner_id.due_amount')
    invoices_debts_name = fields.Char(related='partner_id.invoices_debts_name')

    @api.onchange('partner_id')
    def check_due(self):

        if self.partner_id and self.partner_id.active_limit:
            if self.partner_id.is_debtor:
                raise UserError('Se ha superado el limite de crédito de este cliente y no se podra generar una orden de venta. Las facturas con deudas son:' + str(self.invoices_debts_name))
            elif self.partner_id and not self.partner_id.is_debtor and self.partner_id.due_amount > self.partner_id.warning_stage:
                self.is_warning = True
            else:
                self.is_warning = False
