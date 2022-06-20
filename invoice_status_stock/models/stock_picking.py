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



    @api.depends('backorder_id')
    def _compuete_delivery_is_partial(self):
        for rec in self:
            if rec.backorder_id:
                self.is_partial = True
            else:
                picking = self.env['stock.picking'].search([
                    ('backorder_id.name', '=', rec.name)
                ])
                if len(picking) >= 1:
                    rec.is_partial = True
                else:
                    rec.is_partial = False



    invoice_id = fields.Many2one('account.move', string="Factura")
    state_invoice = fields.Char(
        string="Status Factura",
        compute="_compute_state_invoice",
        # store=True
    )
    withdrawal_type = fields.Selection(
        strin="Tipo de Retiro",
        related="sale_id.withdrawal_type",
        help="Indica si el pedido sera retirado en Oficina o enviado a Fletera."
    )
    by_payment = fields.Selection(
        strin="Pagado por",
        related="sale_id.by_payment",
    )
    fleet_contact_id = fields.Many2one(
        'res.partner',
        related='sale_id.fleet_contact_id',
        string="Fleet Contact"
    )
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Documentos Adjuntos', 
        compute='_compute_attachment_ids', 
        compute_sudo=True
    )
    is_partial = fields.Boolean(
        string="Entrega parcial?",
        default=False,
        compute=_compuete_delivery_is_partial
    )


    @api.depends('sale_id')
    def _compute_attachment_ids(self):
        if self.sale_id:
            attachments = []
            sales = self.env['ir.attachment'].search([
                ('res_model', '=', 'sale.order'),
                ('res_id', '=', self.sale_id.id)
            ])
            if sales != None or sales != False or sales != ():
                self.attachment_ids = sales
            else:
                self.attachment_ids = []
        else:
            self.attachment_ids = []

    
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
                        if rec.sale_id.invoice_ids[0].payment_type2 == 'credit_payment':
                            rec.state_invoice = 'CREDITO'
            else:
                self.state_invoice = "SIN_FACTURA"
        else:
            self.state_invoice = "N/A"


    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.sale_id:
            if self.sale_id.invoice_count >= 1:
                if self.state_invoice == "PAGADA":
                    return res
                elif self.state_invoice == "CREDITO":
                    if self.sale_id.invoice_ids[0].authorized_clearence:
                        return res
                    else:
                        raise UserError(_(' No puede validar una transferencia sin autorización de despacho.'))
                else:
                    raise UserError(_(' No puede validar una transferencia si no tiene factura pagada o factura a credito.'))
            else:
                raise UserError(_(' No puede validar una transferencia si no tiene factura pagada o factura a credito.'))
        else:
            return res

    
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if self.sale_id:
            if 'move_line_ids_without_package' in vals.keys():
                for rec in vals['move_line_ids_without_package']:
                    if rec[0] == 1 and 'qty_done' in rec[2].keys():
                        qty_done = rec[2]['qty_done']
                        p_uom_qty = self.env['stock.move.line'].search([
                            ('id', '=', rec[1])
                        ])
                        if qty_done > p_uom_qty.product_uom_qty:
                            raise UserError(_("¡No Puede entregar mas cantidad de la reservada!"))
        return res 
        
    



