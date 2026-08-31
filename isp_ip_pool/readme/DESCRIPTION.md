# ISP IP Pool

This module adds IPv4/IPv6 pool management to the Odoo backend:

- `isp.ip.pool`: subnet in CIDR notation attached to a network node, with
  gateway, DNS servers and a computed state (free / partial / full).
- `isp.ip.address`: one record per usable host, expanded from the pool
  CIDR through the `netaddr` library (broadcast addresses excluded).

A cron job expands new pools automatically, and individual addresses can
be assigned to partners, reserved or blacklisted.