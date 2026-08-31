# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestISPCustomer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plan = cls.env["product.template"].create(
            {
                "name": "Fibra 20 Mbps Test",
                "type": "service",
                "isp_plan": True,
                "isp_periodicity": "monthly",
                "isp_bandwidth_download": 20.0,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Cliente Test",
                "isp_customer": True,
                "isp_status": "new_pending",
                "isp_plan_id": cls.plan.id,
                "onu_serial": "43445443AF955212",
            }
        )

    def test_client_no_assigned(self):
        self.assertTrue(self.partner.isp_client_no)
        self.assertTrue(self.partner.isp_client_no.startswith("ISP-"))

    def test_status_history_created(self):
        self.assertTrue(self.partner.isp_history_ids)
        self.assertEqual(self.partner.isp_history_ids[0].new_status, "new_pending")

    def test_status_change_logs_history(self):
        before = len(self.partner.isp_history_ids)
        self.partner.isp_status = "active"
        self.assertEqual(len(self.partner.isp_history_ids), before + 1)
        self.assertEqual(self.partner.isp_history_ids[-1].old_status, "new_pending")
        self.assertEqual(self.partner.isp_history_ids[-1].new_status, "active")

    def test_invalid_onu_serial(self):
        with self.assertRaises(ValidationError):
            self.partner.onu_serial = "ABC-defg-hij-kl"
