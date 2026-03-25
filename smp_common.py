"""Shared utilities for SMP02 test scripts."""

from Devices import Device
from Lab import Lab

import time

READS_PER_POINT = 3
READ_DELAY = 0.05
POINT_DELAY = 0.15


def connect_smp(verbose=True):
    """Connect to the SMP02 and return the device handle."""
    dev = Lab.connectByType(
        Device.Type.RF_GEN, hint="SMP02", verbose=verbose
    )
    if dev is None:
        raise ConnectionError("Failed to connect to SMP02")
    return dev


def read_tp(dev, tp):
    """Read a diagnostic test point, return averaged value."""
    time.sleep(POINT_DELAY)
    values = []
    for i in range(READS_PER_POINT):
        if i > 0:
            time.sleep(READ_DELAY)
        reply = dev.query(f":DIAG:MEAS:POINT{tp}?")
        values.append(float(reply))
    return sum(values) / len(values)


def query_options(dev):
    """Query *OPT? and return set of installed option names."""
    reply = dev.query("*OPT?").strip()
    return {o for o in reply.split(",") if o != "0"}


def query_hw_modules(dev):
    """Query :DIAG:INFO:MOD? and return dict of module info."""
    reply = dev.query(":DIAG:INFO:MOD?").strip()
    modules = {}
    for entry in reply.split(","):
        parts = entry.strip().split()
        if len(parts) >= 3:
            name = parts[0]
            var = parts[1]
            rev = parts[2]
            modules[name] = (var, rev)
    return modules


def list_hw_modules(dev):
    """Print hardware modules from :DIAG:INFO:MOD?."""
    hw = query_hw_modules(dev)
    for name, (var, rev) in hw.items():
        print(f"  {name:8s}  {var}  {rev}")
