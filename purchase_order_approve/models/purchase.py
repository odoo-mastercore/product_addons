###############################################################################
# Author: SINAPSYS GLOBAL SA || MASTERCORE SAS
# Copyleft: 2021-Present.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
#
###############################################################################
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import datetime
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    validator_user_id = fields.Many2one('res.users', "Validator User")

    def button_approve(self, force=False):
        self.write({
            'state': 'purchase',
            'validator_user_id':self._context.get('uid'),
            'date_approve': fields.Datetime.now()})
        self.filtered(lambda p: p.company_id.po_lock == 'lock').write(
            {'state': 'done'})
        return {}