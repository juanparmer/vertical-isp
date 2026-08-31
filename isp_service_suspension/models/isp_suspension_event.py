# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ISPSuspensionEvent(models.Model):
    _name = "isp.suspension.event"
    _description = "ISP Suspension Event"
    _order = "execute_date desc, id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: self._get_default_name(),
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        ondelete="cascade",
        index=True,
    )
    onu = fields.Many2one(
        comodel_name="isp.onu",
        string="ONU",
        ondelete="set null",
    )
    onu_serial = fields.Char(
        string="ONU serial",
        readonly=True,
    )
    olt_id = fields.Many2one(
        comodel_name="isp.olt",
        string="OLT",
        ondelete="set null",
    )
    event_type = fields.Selection(
        [
            ("cutoff", "Cutoff"),
            ("reconnect", "Reconnect"),
            ("manual_suspend", "Manual suspend"),
            ("manual_resume", "Manual resume"),
        ],
        string="Event type",
        required=True,
    )
    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("success", "Success"),
            ("error", "Error"),
        ],
        required=True,
        default="pending",
    )
    error_message = fields.Text(string="Error message")
    execute_date = fields.Datetime(
        string="Execution date",
        default=fields.Datetime.now,
    )
    executed_by = fields.Many2one(
        comodel_name="res.users",
        string="Executed by",
        default=lambda self: self.env.user,
    )

    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("isp.suspension.event") or "/"
