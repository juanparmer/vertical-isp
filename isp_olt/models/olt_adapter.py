# Copyright 2026 Juan Parmer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ISPAbstractOLTAdapter(models.AbstractModel):
    """Contract every OLT vendor adapter must implement.

    Vendor implementations live in dedicated glue modules (for example
    ``isp_olt_huawei``) and register themselves by overriding
    :meth:`_get_adapters` with their vendor key. Commands execute against
    a live OLT and should return ``(True, message)`` / ``(False, message)``
    so the caller can log a suspension event with its error (mirroring
    NovaISP behaviour).
    """

    _name = "isp.abstract.olt.adapter"
    _description = "ISP OLT adapter contract"

    @classmethod
    def _get_adapters(cls):
        """Map of ``{vendor: adapter_model_name}``.

        Registered by each vendor module, e.g.::

            '@classmethod'
            'def _get_adapters(cls):'
            '    adapters = super()._get_adapters()'
            '    adapters["huawei"] = "isp.olt.huawei.adapter"'
            '    return adapters'
        """
        return {}

    def _get_adapter(self, vendor):
        adapters = self._get_adapters()
        adapter_name = adapters.get(vendor)
        return adapter_name and self.env[adapter_name]

    def test_connection(self, olt):
        raise NotImplementedError

    def get_onu_status(self, olt, onu):
        raise NotImplementedError

    def activate_onu(self, olt, onu):
        raise NotImplementedError

    def deactivate_onu(self, olt, onu):
        raise NotImplementedError

    def set_plan_bandwidth(self, olt, onu, download, upload):
        raise NotImplementedError

    def sync_onus(self, olt):
        raise NotImplementedError
