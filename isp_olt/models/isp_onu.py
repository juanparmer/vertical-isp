# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ISPONU(models.Model):
    _name = "isp.onu"
    _description = "ISP ONU / ONT"
    _order = "olt_id, olt_port, olt_pon"

    name = fields.Char(
        string="Serial",
        required=True,
        help="14- or 16-character hexadecimal ONU serial as seen by the OLT.",
    )
    olt_id = fields.Many2one(
        comodel_name="isp.olt",
        string="OLT",
        required=True,
        ondelete="cascade",
        index=True,
    )
    olt_port = fields.Char(string="OLT port")
    olt_pon = fields.Char(string="PON port")
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        ondelete="restrict",
    )
    state = fields.Selection(
        [
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("error", "Error"),
            ("signal_loss", "Signal loss"),
        ],
        required=True,
        default="inactive",
    )
    rx_power = fields.Float(string="RX power (dBm)", digits=(16, 2))
    last_seen = fields.Datetime(string="Last seen")
