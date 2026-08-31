# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestISPServicePlan(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plan = cls.env["product.template"].create(
            {
                "name": "Test Plan Fibra 10 Mbps",
                "type": "service",
                "list_price": 40000,
                "isp_plan": True,
                "isp_periodicity": "monthly",
                "isp_bandwidth_download": 10.0,
                "isp_bandwidth_upload": 2.0,
            }
        )

    def test_default_periodicity_is_monthly(self):
        plan = self.plan
        self.assertEqual(plan.isp_periodicity, "monthly")

    def test_plan_flag(self):
        self.assertTrue(self.plan.isp_plan)
        self.assertEqual(self.plan.isp_bandwidth_download, 10.0)

    def test_plan_extra(self):
        product = self.env["product.product"].create(
            {
                "name": "IP Fija Test",
                "type": "service",
                "list_price": 10000,
            }
        )
        extra = self.env["isp.plan.extra"].create(
            {
                "name": "IP Fija",
                "plan_id": self.plan.id,
                "product_id": product.id,
            }
        )
        self.assertEqual(extra.plan_id, self.plan)
        self.assertIn(extra, self.plan.isp_plan_extra_ids)
