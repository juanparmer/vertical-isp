# ISP Service Plan

This module extends the `product.template` model to identify and manage
Internet Service Provider (ISP) service plans (fiber, radio, TV, VoIP...)
together with their additional products.

It adds the typical fields needed by an ISP billing system: download/upload
bandwidth in Mbps and the recurring billing periodicity (monthly, biweekly,
annual). Additional products sold alongside a plan (fixed IP, WiFi extender,
decoder, ...) are managed through the new `isp.plan.extra` model.

This is the first building block of the `vertical-isp` set of modules,
designed for GPON fiber ISPs in Colombia but usable by any ISP.