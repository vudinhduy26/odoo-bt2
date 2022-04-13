from odoo import api, fields, models, tools
import logging
from odoo.exceptions import ValidationError
import re

_logger = logging.getLogger(__name__)


class OrderDiscountWizard(models.TransientModel):
    _name = "order.discount.wizard"
    customer_discount_code = fields.Char('Discount Code')
    code_valid = fields.Boolean('Sale code Valid', default=False)

    def multi_update_discount(self):
        ids = self.env.context['active_ids']
        customers = self.env["res.partner"].browse(ids)
        check = self._check_discount_valid(code=self.customer_discount_code)
        if self.customer_discount_code and check:
            new_data = {
                "customer_discount_code": self.customer_discount_code,
                "code_valid": check
            }
            customers.write(new_data)
        else:
            raise ValidationError("Vip format is not allowed, please re-enter ex: 'VIP_8' ")

    @api.model
    def _check_discount_valid(self, code):
        if len(code) < 5:
            return False
        else:
            first = code[0:4]
            last = code[4:]
            if first == "VIP_" and last.isdigit() and len(last) < 3:
                return True
            else:
                return False
