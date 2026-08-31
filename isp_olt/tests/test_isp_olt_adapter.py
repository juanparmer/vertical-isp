# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestISPOLTAdapter(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.adapter = cls.env["isp.abstract.olt.adapter"]
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

    def test_no_adapter_registered_by_default(self):
        adapter = self.adapter._get_adapter("generic")
        self.assertFalse(adapter)

    def test_unknown_vendor_returns_none(self):
        self.assertFalse(self.adapter._get_adapter("nonexistent"))

    def test_ont_creation(self):
        onu = self.env["isp.onu"].create(
            {
                "name": "43445443AF955212",
                "olt_id": self.olt.id,
                "state": "active",
            }
        )
        self.assertEqual(onu.olt_id, self.olt)
        self.assertEqual(onu.state, "active")
