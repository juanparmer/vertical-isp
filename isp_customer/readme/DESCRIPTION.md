# ISP Customer

This module extends `res.partner` with the fields and workflow an ISP
needs to manage subscribers:

- ISP plan, status (new / active / suspended / offline / cancelled)
- Network node, IP pool and assigned IP address
- ONU serial (validated, 14 hexadecimal digits), service address,
  installation and cutoff dates, installing technician
- Sequential client code and a full status/plan change history

The partner form gets an *ISP* page and the *Customers* menu mirrors the
classic ISP dashboard filters (new, pending, suspended, offline,
cancelled).