# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ISP Network Node",
    "summary": "Manage ISP network nodes and coverage areas",
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
    "depends": ["base"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "views/isp_network_node_views.xml",
    ],
    "demo": ["demo/isp_network_node_demo.xml"],
}
