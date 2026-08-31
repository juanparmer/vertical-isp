# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    suspension_event_ids = fields.One2many(
        comodel_name="isp.suspension.event",
        inverse_name="partner_id",
        string="Suspension events",
    )

    def action_isp_cutoff(self):
        """Suspend the customer service (deactivate the ONU on the OLT)."""
        for partner in self:
            self.env["isp.suspension.event"]._create_and_run(partner, "cutoff")
        return self.action_isp_reload_partner()

    def action_isp_reconnect(self):
        """Reconnect the customer service (reactivate the ONU on the OLT)."""
        for partner in self:
            self.env["isp.suspension.event"]._create_and_run(partner, "reconnect")
        return self.action_isp_reload_partner()

    def action_isp_reload_partner(self):
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }


class ISPSuspensionEvent(models.Model):
    _inherit = "isp.suspension.event"

    @api.model
    def _create_and_run(self, partner, event_type):
        """Create an event record and dispatch it to the OLT adapter.

        OLT failures (credentials, reachability, missing adapter...) are
        logged on the event instead of killing the write, mirroring the
        NovaISP behaviour: cutoffs must surface errors and stay retryable.
        """
        onu = self.env["isp.onu"].search(
            [
                ("partner_id", "=", partner.id),
                ("state", "in", ("active", "inactive")),
            ],
            limit=1,
        )
        event = self.create(
            {
                "partner_id": partner.id,
                "onu": onu.id,
                "onu_serial": onu.name if onu else partner.onu_serial,
                "olt_id": onu.olt_id.id if onu else False,
                "event_type": event_type,
            }
        )
        if not onu:
            event._mark_error(f"No active ONU found for customer {partner.name}")
            return event
        adapter = self.env["isp.abstract.olt.adapter"]._get_adapter(onu.olt_id.vendor)
        if not adapter:
            event._mark_error(
                f"No OLT adapter registered for vendor {onu.olt_id.vendor}"
            )
            return event
        method = (
            "deactivate_onu"
            if event_type in ("cutoff", "manual_suspend")
            else "activate_onu"
        )
        success = False
        message = "No response from OLT"
        try:
            success, message = getattr(adapter, method)(onu.olt_id, onu)
        except Exception as err:  # noqa: BLE001
            _logger.exception("OLT %s failed for ONU %s", onu.olt_id.name, onu.name)
            event._mark_error(str(err))
            return event
        if success:
            partner.isp_status = (
                "suspended_cutoff" if method == "deactivate_onu" else "active"
            )
            onu.state = "inactive" if method == "deactivate_onu" else "active"
            event.state = "success"
        else:
            event._mark_error(message)
        return event

    def _mark_error(self, message):
        self.state = "error"
        self.error_message = message
