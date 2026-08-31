# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    isp_plan = fields.Boolean(
        string="ISP Plan",
        help="Check this box to identify this product as an ISP service "
        "plan (Internet, TV, VoIP,...).",
    )
    isp_periodicity = fields.Selection(
        [
            ("monthly", "Monthly"),
            ("biweekly", "Biweekly"),
            ("annual", "Annual"),
        ],
        string="Billing periodicity",
        default="monthly",
        help="Recurring billing cycle applied to this plan. Most ISP "
        "customers are billed monthly.",
    )
    isp_bandwidth_download = fields.Float(
        string="Download speed (Mbps)",
        digits=(16, 2),
    )
    isp_bandwidth_upload = fields.Float(
        string="Upload speed (Mbps)",
        digits=(16, 2),
    )
    isp_plan_extra_ids = fields.One2many(
        comodel_name="isp.plan.extra",
        inverse_name="plan_id",
        string="Additional products",
    )


class ISPServicePlanExtra(models.Model):
    _name = "isp.plan.extra"
    _description = "ISP Plan Additional Product"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="Description", required=True)
    plan_id = fields.Many2one(
        comodel_name="product.template",
        string="ISP Plan",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        ondelete="restrict",
    )
    active = fields.Boolean(default=True)
