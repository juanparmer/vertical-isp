# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ISP IP Pool",
    "summary": "Manage ISP IPv4/IPv6 pools and individual addresses",
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
    "depends": ["isp_network_node"],
    "external_dependencies": {"python": ["netaddr"], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "data/isp_ip_pool_data.xml",
        "views/isp_ip_pool_views.xml",
    ],
    "demo": ["demo/isp_ip_pool_demo.xml"],
}
