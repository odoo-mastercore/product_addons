# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2021-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, fields, api, _

class ToHideProductWizard(models.TransientModel):
    _name = 'to.hide.product.wizard'
    _description = 'to hide Wizard'

    def confirm(self):
        domain = [('id', 'in', self._context.get('active_ids', [])),]

        products = self.env['product.template'].search(domain)
        for rec in products:
            rec.is_published = False

        return {
            'type': 'ir.actions.act_window',
            'name': ' Productos Publicados',
            'res_model': 'to.hide.product.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref(
                    'product_website_publish.consult_to_hide_product_wizard_confirm').id,
            'target': 'new',
        }
