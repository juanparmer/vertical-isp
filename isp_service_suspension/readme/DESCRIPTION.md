# ISP Service Suspension

This module handles service cutoffs and reconnections (GPON):

- `isp.suspension.event`: audit record with type (cutoff, reconnect,
  manual suspend/resume), trigger, state (pending / success / error),
  error message, executor and execution date.
- Partner buttons *Cut off service* / *Reconnect service* deactivate or
  reactivate the customer ONU through the OLT adapter linked to its
  network.

OLT failures (wrong credentials, unreachable host, missing vendor
adapter, command errors) never block the operation: they are logged on
the event as *Error* and stay visible and retryable, mirroring the
behaviour observed on NovaISP (`No se pudo eliminar el equipo de la
OLT ...`).