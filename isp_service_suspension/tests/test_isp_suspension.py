# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.tests.common import TransactionCase

from odoo.addons.isp_olt.models.olt_adapter import ISPAbstractOLTAdapter


class TestISPSuspension(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.node = cls.env["isp.network.node"].create(
            {"name": "Node Test", "code": "TEST-01"}
        )
        cls.olt = cls.env["isp.olt"].create(
            {
                "name": "OLT Test",
                "node_id": cls.node.id,
                "vendor": "generic",
                "host": "192.0.2.1",
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Cliente Corte",
                "isp_customer": True,
                "isp_status": "active",
            }
        )
        cls.onu = cls.env["isp.onu"].create(
            {
                "name": "43445443AF955212",
                "olt_id": cls.olt.id,
                "partner_id": cls.partner.id,
                "state": "active",
            }
        )

    def test_cutoff_without_adapter_logs_error(self):
        self.partner.action_isp_cutoff()
        event = self.partner.suspension_event_ids[0]
        self.assertEqual(event.event_type, "cutoff")
        self.assertEqual(event.state, "error")
        self.assertIn("OLT adapter", event.error_message)

    def test_error_event_stays_retryable(self):
        self.partner.action_isp_cutoff()
        first = self.partner.suspension_event_ids[0]
        self.partner.action_isp_cutoff()
        self.assertEqual(len(self.partner.suspension_event_ids), 2)
        self.assertEqual(first.state, "error")

    def test_successful_cutoff_updates_status(self):
        fake_adapter = type(
            "FakeAdapter",
            (),
            {
                "deactivate_onu": lambda self, olt, onu: (True, "ok"),
                "activate_onu": lambda self, olt, onu: (True, "ok"),
            },
        )()
        with patch.object(
            ISPAbstractOLTAdapter, "_get_adapter", return_value=fake_adapter
        ):
            self.partner.action_isp_cutoff()
        event = self.partner.suspension_event_ids[0]
        self.assertEqual(event.state, "success")
        self.assertEqual(self.partner.isp_status, "suspended_cutoff")
        self.assertEqual(self.onu.state, "inactive")
