# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestISPNetworkNode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.node = cls.env["isp.network.node"].create(
            {
                "name": "Nodo Test",
                "code": "TST-01",
                "node_type": "fiber",
                "capacity": 100,
            }
        )

    def test_node_creation(self):
        self.assertEqual(self.node.name, "Nodo Test")
        self.assertEqual(self.node.node_type, "fiber")

    def test_hierarchy(self):
        child = self.env["isp.network.node"].create(
            {
                "name": "Nodo Hijo",
                "code": "TST-02",
                "node_type": "fiber",
                "parent_id": self.node.id,
            }
        )
        self.assertEqual(child.parent_id, self.node)
        self.assertIn(child, self.node.child_ids)
