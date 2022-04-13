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
    check_warranty = fields.Boolean(string="Check Warranty")


    @api.constrains('date_to', 'date_from')
    def _constrains_check_date(self):
        for record in self:
            if record.date_from > record.date_to:
                raise models.ValidationError('Date From cannot be less than Date To')
                
    @api.onchange('date_to', 'date_from')
    def _conver_time_to_string(self):
        for record in self:
            if record.date_to and record.date_from:
                record.product_warranty = "PWR/" + (
                    record.date_from).strftime("%d%m%Y") + "/" + (
                                              record.date_to).strftime("%d%m%Y")
            else:
                record.product_warranty = ''
                
            
    @api.depends('date_from', 'date_to', 'day_warranty', 'check_warranty')
    def _count_number_days_warranty(self):
        for record in self:
            if record.date_from and record.date_to:
                number_day = (record.date_to - datetime.date.today()).days
                if number_day <= 0:
                    record.day_warranty = "No Warranty"
                    record.check_warranty = False
                elif number_day > 365:
                    record.day_warranty = "Warranty " + str(number_day // 365) + " Year"
                    record.check_warranty = True
                elif number_day > 31:
                    record.day_warranty = "Warranty " + str(number_day // 31) + " Month"
                    record.check_warranty = True
                elif number_day > 0:
                    record.day_warranty = str(number_day) + " Days"
                    record.check_warranty = True
            else:
                record.day_warranty = "No Warranty"
                record.check_warranty = False

