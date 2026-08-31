# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ISP Service Suspension",
    "summary": "Cut off and reconnect ISP services with event tracking",
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
    "depends": ["isp_customer", "isp_olt"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "data/isp_suspension_event_data.xml",
        "views/isp_suspension_event_views.xml",
        "views/res_partner_views.xml",
    ],
    "demo": ["demo/isp_suspension_event_demo.xml"],
}
