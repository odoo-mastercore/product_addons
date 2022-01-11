# -*- coding: utf-8 -*-
##############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2020-Present.
# License LGPL-3.0 or later (http: //www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID

class PurchaseOrderStage(models.Model):
    _name = 'purchase.order.stage'
    _order = 'sequence asc'
    _description = 'Purchase Stages'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(help="Used to order the note stages")

    identifier = fields.Char(
        required=True,
        string="Identifier",
        help="It is used to identify or validate the purchase order"
    )

    _sql_constraints = [
        ('purchase_stage_name_unique', 'unique(name)', 'Stage name already exists'),
        ('purchase_stage_identifier_unique', 'unique(identifier)', 'Stage identifier already exists')
    ]


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_default_stage(self):
        state = self.env.ref('purchase_dashboard_stage.p_order_coc', raise_if_not_found=False)
        return state if state and state.id else False

    stage_id = fields.Many2one('purchase.order.stage', 'Stage',
        default=_get_default_stage, group_expand='_read_group_stage_ids',
        tracking=True,
        help='Current stage of the Purchase', ondelete="set null")

    # -------------------------------------------------------------
    # This field is used at the development level to identify
    # the different stages of a purchase order.
    # -------------------------------------------------------------
    stage_identifier = fields.Char(related="stage_id.identifier", readonly=True)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        all_stages = self.env['purchase.order.stage'].sudo().search([])
        search_domain = [('id', 'in', all_stages.ids)]
        stage_ids = stages._search(search_domain,
                                   order=order,
                                   access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)
