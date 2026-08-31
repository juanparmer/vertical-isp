# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestISPIPPool(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pool = cls.env["isp.ip.pool"].create(
            {
                "name": "Pool Test",
                "network_address": "192.168.1.0/30",
                "ip_version": "v4",
                "gateway": "192.168.1.1",
            }
        )

    def test_network_address_generation(self):
        self.pool.action_generate_addresses()
        addresses = [a.ip_address for a in self.pool.address_ids]
        # 192.168.1.0/30 has 2 usable hosts
        self.assertEqual(len(addresses), 2)
        self.assertIn("192.168.1.1", addresses)
        self.assertIn("192.168.1.2", addresses)

    def test_generation_is_idempotent(self):
        self.pool.action_generate_addresses()
        self.pool.action_generate_addresses()
        self.assertEqual(len(self.pool.address_ids), 2)

    def test_invalid_cidr(self):
        with self.assertRaises(ValidationError):
            self.pool.network_address = "not-a-cidr"
