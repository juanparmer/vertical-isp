# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ISPOLT(models.Model):
    _name = "isp.olt"
    _description = "ISP OLT"

    name = fields.Char(required=True)
    node_id = fields.Many2one(
        comodel_name="isp.network.node",
        string="Node",
        ondelete="restrict",
        required=True,
    )
    vendor = fields.Selection(
        [
            ("generic", "Generic"),
            ("huawei", "Huawei"),
            ("zte", "ZTE"),
            ("fiberhome", "FiberHome"),
        ],
        required=True,
        default="generic",
    )
    model = fields.Char()
    host = fields.Char(required=True)
    port = fields.Integer(default=22)
    username = fields.Char()
    password = fields.Char(
        groups="base.group_system",
    )
    snmp_community = fields.Char(
        string="SNMP community",
        groups="base.group_system",
    )
    state = fields.Selection(
        [
            ("untested", "Untested"),
            ("online", "Online"),
            ("offline", "Offline"),
            ("wrong_credentials", "Wrong credentials"),
            ("error", "Error"),
        ],
        default="untested",
    )
    onu_ids = fields.One2many(
        comodel_name="isp.onu",
        inverse_name="olt_id",
        string="ONUs",
    )
    active = fields.Boolean(default=True)

    def action_test_connection(self):
        """Run the vendor adapter authentication to probe the OLT."""
        self.ensure_one()
        adapter_cls = self.env["isp.abstract.olt.adapter"]._get_adapter(self.vendor)
        if not adapter_cls:
            self.state = "error"
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "OLT",
                    "message": (
                        f"No connection adapter registered for vendor {self.vendor}."
                    ),
                    "sticky": False,
                    "type": "warning",
                },
            }
        success, message = adapter_cls.test_connection(self)
        self.state = "online" if success else "wrong_credentials"
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "OLT",
                "message": message,
                "sticky": False,
                "type": "success" if success else "warning",
            },
        }


class ISPOLTProfile(models.Model):
    _name = "isp.olt.profile"
    _description = "ISP OLT Traffic Profile"

    name = fields.Char(required=True)
    vendor = fields.Selection(
        [
            ("generic", "Generic"),
            ("huawei", "Huawei"),
            ("zte", "ZTE"),
            ("fiberhome", "FiberHome"),
        ],
        required=True,
        default="generic",
    )
    onu_template = fields.Char(
        string="ONU template",
        help="Vendor template used to provision ONUs with this profile.",
    )
