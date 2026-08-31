# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ISP Customer",
    "summary": "Extend partners with ISP customer management",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Sales",
    "website": "https://github.com/OCA/vertical-isp",
    "author": "Juan Parmer, Arcme Colombia (arcme.co), "
    "Odoo Community Association (OCA)",
    "maintainers": ["juanparmer"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale", "isp_service_plan", "isp_network_node", "isp_ip_pool"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "data/isp_customer_data.xml",
        "views/res_partner_views.xml",
    ],
    "demo": ["demo/isp_customer_demo.xml"],
}
