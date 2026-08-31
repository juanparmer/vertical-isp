# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ISP Service Plan",
    "summary": "Manage ISP service plans and their additional products",
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
    "depends": ["product", "sale", "isp_network_node"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "views/isp_service_plan_views.xml",
        "views/product_template_views.xml",
    ],
    "demo": ["demo/isp_service_plan_demo.xml"],
}
