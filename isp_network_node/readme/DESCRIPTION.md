# ISP Network Node

This module adds the `isp.network.node` model to manage the physical and
logical nodes of an ISP network (GPON fiber PoPs, wireless towers, ...)
together with their hierarchical relationships and coverage city.

Each node keeps its type, parent node, city/state, GPS coordinates and
maximum client capacity. Nodes are the anchor for IP pools and OLT/ONU
equipment managed by the other modules of the `vertical-isp` set.