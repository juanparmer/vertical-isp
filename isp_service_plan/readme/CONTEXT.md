# Context

**BUSINESS NEED**

An ISP needs to catalog the services it sells before it can automate
billing, customer accounting and network provisioning. Each plan has a
speed (download/upload), a price and a recurring billing cycle
(almost always monthly). Plans can also bundle additional billable
products (fixed public IP, WiFi extender, IPTV decoder).

**APPROACH**

Instead of creating a new isolated model, ISP plans reuse the standard
Odoo `product.template`: every plan is a *service* product flagged with
`isp_plan`. This keeps integration free with Sale Orders, Invoicing and
the OCA `contract` module (which generates the recurring invoices from
sale/contract lines). Additional products are linked to a plan through
the `isp.plan.extra` model.

**USEFUL INFORMATION**

This module is meant to work together with:

- `contract` (OCA): recurring invoicing generated from plan lines.
- `isp_network_node` / `isp_ip_pool`: network provisioning for plans.
- `isp_customer`: assigns a plan to each customer and tracks its state.