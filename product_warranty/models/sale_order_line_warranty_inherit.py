from odoo import api, models, fields


class SaleOrderWarranty(models.Model):
    _inherit = 'sale.order.line'

    show_discount_estimated = fields.Monetary(string="Discount Estimated", default=0,
                                              compute="_compute_discount_estimated")
    total_discount_estimated = fields.Monetary(string="Total Discount Estimated", default=0,
                                               compute="_compute_total_discount_estimated", readonly="1")
    day_warranty = fields.Char(string="Number days warranty", related="product_template_id.day_warranty")

    @api.onchange('product_uom_qty', 'price_tax', 'price_unit')
    def _compute_discount_estimated(self):
        for record in self:
            record.show_discount_estimated = (record.price_unit * record.product_uom_qty) * (
                        record.order_id.partner_id.sale_order_discount_estimated / 100.0)

    @api.onchange('show_discount_estimated', 'total_discount_estimated')
    def _compute_total_discount_estimated(self):
        for record in self:
            record.total_discount_estimated += record.show_discount_estimated

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     res = super(SaleOrderWarranty, self)._compute_amount()
    #     for line in self:
    #         line.price_subtotal -= line.show_discount_estimated
    #
    #     return res
