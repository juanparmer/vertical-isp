# ISP OLT

This module adds GPON equipment management to the backend:

- `isp.olt`: OLT devices attached to a network node, with vendor, model,
  host/port, credentials (restricted to administrators) and a connection
  probe button that runs the vendor adapter.
- `isp.olt.profile`: traffic profiles used to provision ONUs.
- `isp.onu`: ONU/ONT registers with the 14-digit serial, OLT/port/PON
  location, customer, state, RX power and last seen time.

Commanding the OLT (activate/deactivate ONU, change plan bandwidth, sync
the ONU list) goes through :code:`isp.abstract.olt.adapter`, a contract
that vendor modules (Huawei, ZTE, FiberHome, ...) implement in dedicated
addons, keeping the core vendor-agnostic.