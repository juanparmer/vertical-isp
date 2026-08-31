# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ISPNetworkNode(models.Model):
    _name = "isp.network.node"
    _description = "ISP Network Node"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    node_type = fields.Selection(
        [
            ("fiber", "Fiber (GPON)"),
            ("radio", "Wireless"),
            ("tower", "Tower"),
            ("pop", "PoP"),
        ],
        string="Node type",
        required=True,
        default="fiber",
    )
    parent_id = fields.Many2one(
        comodel_name="isp.network.node",
        string="Parent node",
        ondelete="restrict",
    )
    child_ids = fields.One2many(
        comodel_name="isp.network.node",
        inverse_name="parent_id",
        string="Child nodes",
    )
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State",
    )
    city_id = fields.Many2one(
        comodel_name="res.city",
        string="City",
    )
    latitude = fields.Float(digits=(16, 6))
    longitude = fields.Float(digits=(16, 6))
    capacity = fields.Integer(
        string="Maximum clients",
        help="Maximum number of clients this node can serve.",
    )
    active = fields.Boolean(default=True)
