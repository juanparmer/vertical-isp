# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo import _, api, fields, models

_ONU_SERIAL_PATTERN = re.compile(r"^[0-9A-Fa-f]{14}(?:[0-9A-Fa-f]{2})?$")


class ResPartner(models.Model):
    _inherit = "res.partner"

    isp_customer = fields.Boolean(string="ISP Customer")
    isp_client_no = fields.Char(
        string="Client No.",
        readonly=True,
        copy=False,
        help="Internal sequential customer code.",
    )
    isp_plan_id = fields.Many2one(
        comodel_name="product.template",
        string="ISP Plan",
        domain="[('isp_plan', '=', True)]",
    )
    isp_status = fields.Selection(
        [
            ("new_pending", "New / Pending"),
            ("active", "Active"),
            ("suspended_cutoff", "Suspended (non-payment)"),
            ("offline", "Offline"),
            ("cancelled", "Cancelled"),
        ],
        string="ISP Status",
        default="new_pending",
        track_visibility="onchange",
    )
    node_id = fields.Many2one(
        comodel_name="isp.network.node",
        string="Node",
    )
    ip_pool_id = fields.Many2one(
        comodel_name="isp.ip.pool",
        string="IP Pool",
        domain="[('ip_version', '=', 'v4')]",
    )
    ip_address_id = fields.Many2one(
        comodel_name="isp.ip.address",
        string="Assigned IP",
    )
    onu_serial = fields.Char(
        string="ONU Serial",
        help="14- or 16-character hexadecimal serial of the customer ONU.",
    )
    service_address = fields.Char(string="Service address")
    installation_date = fields.Date(string="Installation date")
    cutoff_date = fields.Date(string="Cutoff date")
    install_tech_id = fields.Many2one(
        comodel_name="res.users",
        string="Installing technician",
    )
    isp_history_ids = fields.One2many(
        comodel_name="res.partner.isp.history",
        inverse_name="partner_id",
        string="ISP history",
    )

    @api.constrains("onu_serial")
    def _check_onu_serial(self):
        for partner in self:
            if partner.onu_serial and not _ONU_SERIAL_PATTERN.match(partner.onu_serial):
                raise models.ValidationError(
                    _(
                        "ONU Serial must be a 14- or 16-character hexadecimal "
                        "value (e.g. 43445443AF955212)."
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        for partner, values in zip(partners, vals_list, strict=False):
            if partner.isp_customer:
                if not partner.isp_client_no:
                    partner.isp_client_no = partner._get_next_client_no()
                partner._log_isp_history(values=values)
        return partners

    def write(self, values):
        old_values = {partner.id: self._read_isp_state(partner) for partner in self}
        result = super().write(values)
        for partner in self:
            if not partner.isp_customer:
                continue
            new_values = self._read_isp_state(partner)
            if old_values[partner.id] != new_values:
                partner._log_isp_history(
                    old_state=old_values[partner.id], new_state=new_values
                )
        return result

    def _read_isp_state(self, partner):
        return {
            "isp_status": partner.isp_status,
            "isp_plan_id": partner.isp_plan_id.id,
        }

    def _get_next_client_no(self):
        sequence = self.env["ir.sequence"].next_by_code("isp.client")
        return sequence

    def _log_isp_history(self, old_state=None, new_state=None, values=None):
        if values and not old_state:
            old_state = {"isp_status": "new_pending", "isp_plan_id": False}
            new_state = {
                "isp_status": values.get("isp_status", "new_pending"),
                "isp_plan_id": values.get("isp_plan_id"),
            }
        if not new_state:
            new_state = self._read_isp_state(self)
        self.env["res.partner.isp.history"].create(
            {
                "partner_id": self.id,
                "old_status": old_state and old_state.get("isp_status"),
                "new_status": new_state.get("isp_status"),
                "old_plan_id": old_state and old_state.get("isp_plan_id"),
                "new_plan_id": new_state.get("isp_plan_id"),
            }
        )


class ResPartnerIspHistory(models.Model):
    _name = "res.partner.isp.history"
    _description = "Partner ISP History"
    _order = "date desc"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        ondelete="cascade",
        index=True,
    )
    date = fields.Datetime(default=fields.Datetime.now)
    old_status = fields.Selection(
        [
            ("new_pending", "New / Pending"),
            ("active", "Active"),
            ("suspended_cutoff", "Suspended (non-payment)"),
            ("offline", "Offline"),
            ("cancelled", "Cancelled"),
        ],
        string="Old status",
    )
    new_status = fields.Selection(
        [
            ("new_pending", "New / Pending"),
            ("active", "Active"),
            ("suspended_cutoff", "Suspended (non-payment)"),
            ("offline", "Offline"),
            ("cancelled", "Cancelled"),
        ],
        string="New status",
    )
    old_plan_id = fields.Many2one(
        comodel_name="product.template",
        string="Old plan",
    )
    new_plan_id = fields.Many2one(
        comodel_name="product.template",
        string="New plan",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user,
    )
