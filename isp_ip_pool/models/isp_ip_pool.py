# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from netaddr import IPNetwork
from netaddr.core import AddrFormatError

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ISPIPPool(models.Model):
    _name = "isp.ip.pool"
    _description = "ISP IP Pool"
    _order = "ip_version, name"

    name = fields.Char(required=True)
    node_id = fields.Many2one(
        comodel_name="isp.network.node",
        string="Node",
        ondelete="restrict",
    )
    ip_version = fields.Selection(
        [("v4", "IPv4"), ("v6", "IPv6")],
        string="IP version",
        required=True,
        default="v4",
    )
    network_address = fields.Char(
        string="Network (CIDR)",
        required=True,
        placeholder="e.g. 10.10.0.0/24",
    )
    gateway = fields.Char()
    dns1 = fields.Char(string="Primary DNS")
    dns2 = fields.Char(string="Secondary DNS")
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Reserved for",
        ondelete="restrict",
        help="Customer this pool is dedicated to, if any.",
    )
    state = fields.Selection(
        [
            ("free", "Free"),
            ("partial", "Partially used"),
            ("full", "Full"),
        ],
        compute="_compute_state",
        store=True,
    )
    address_ids = fields.One2many(
        comodel_name="isp.ip.address",
        inverse_name="pool_id",
        string="Addresses",
    )
    address_count = fields.Integer(
        string="Address count",
        compute="_compute_address_count",
    )
    address_free_count = fields.Integer(
        string="Free address count",
        compute="_compute_address_count",
    )
    active = fields.Boolean(default=True)

    @api.depends("address_ids", "address_ids.state")
    def _compute_state(self):
        for pool in self:
            if not pool.address_ids:
                pool.state = "free"
            elif all(address.state == "free" for address in pool.address_ids):
                pool.state = "free"
            elif all(address.state != "free" for address in pool.address_ids):
                pool.state = "full"
            else:
                pool.state = "partial"

    @api.depends("address_ids")
    def _compute_address_count(self):
        for pool in self:
            pool.address_count = len(pool.address_ids)
            pool.address_free_count = len(
                pool.address_ids.filtered(lambda a: a.state == "free")
            )

    @api.constrains("network_address")
    def _check_network_address(self):
        for pool in self:
            try:
                IPNetwork(pool.network_address)
            except (OSError, ValueError, TypeError, AddrFormatError) as err:
                raise models.ValidationError(
                    _(f"Invalid CIDR notation {pool.network_address}")
                ) from err

    def action_generate_addresses(self):
        """Expand the pool CIDR and (re)create its individual addresses."""
        for pool in self:
            network = IPNetwork(pool.network_address)
            existing = {address.ip_address for address in pool.address_ids}
            for ip in network.iter_hosts():
                ip_address = str(ip)
                if ip_address not in existing:
                    self.env["isp.ip.address"].create(
                        {
                            "pool_id": pool.id,
                            "ip_address": ip_address,
                        }
                    )

    @api.model
    def _cron_generate_addresses(self):
        pools = self.search([("address_ids", "=", False)])
        _logger.info("Generating IP addresses for %s pools", len(pools))
        pools.action_generate_addresses()


class ISPIPAddress(models.Model):
    _name = "isp.ip.address"
    _description = "ISP IP Address"
    _order = "pool_id, ip_address"

    ip_address = fields.Char(string="IP address", required=True)
    pool_id = fields.Many2one(
        comodel_name="isp.ip.pool",
        string="Pool",
        required=True,
        ondelete="cascade",
        index=True,
    )
    state = fields.Selection(
        [
            ("free", "Free"),
            ("used", "Used"),
            ("reserved", "Reserved"),
            ("blacklisted", "Blacklisted"),
        ],
        required=True,
        default="free",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Assigned to",
        ondelete="restrict",
    )

    _sql_constraints = [
        (
            "ip_address_pool_uniq",
            "unique(pool_id, ip_address)",
            "IP address must be unique within its pool.",
        )
    ]
