from odoo import api, fields, models
import datetime
from odoo.exceptions import ValidationError
import re


class ProductWarranty(models.Model):
    _inherit = 'product.template'

    product_warranty = fields.Text(string="Warranty Code", compute="_conver_time_to_string")  # PWR/031219/030920
    date_from = fields.Date(string="Start", required=True)
    date_to = fields.Date(string="End", required=True)
    day_warranty = fields.Char(string="Number Days Warranty", compute="_count_number_days_warranty")

    @api.constrains('date_to', 'date_from')
    def _constrains_check_date(self):
        for record in self:
            if record.date_from > record.date_to:
                raise models.ValidationError('Date From cannot be less than Date To')

