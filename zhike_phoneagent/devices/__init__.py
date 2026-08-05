"""Device implementations for the DeviceProtocol interface.

This package provides concrete implementations of DeviceProtocol:
- ADBDevice: Local ADB subprocess calls
- MockDevice: State machine driven mock for testing
- RemoteDevice: HTTP client for remote device agents

Example:
    >>> from zhike_phoneagent.devices import ADBDevice, RemoteDevice
    >>>
    >>> # Local ADB device
    >>> device = ADBDevice("emulator-5554")
    >>> device.tap(100, 200)
    >>>
    >>> # Remote device via HTTP
    >>> remote = RemoteDevice("phone_001", "http://device-agent:8001")
    >>> remote.tap(100, 200)
"""

from zhike_phoneagent.devices.adb_device import (
    ADBDevice,
    ADBDeviceManager,
    AsyncADBDevice,
    AsyncADBDeviceManager,
)
from zhike_phoneagent.devices.async_adapter import AsyncDeviceAdapter
from zhike_phoneagent.devices.mock_device import MockDevice
from zhike_phoneagent.devices.remote_device import RemoteDevice, RemoteDeviceManager

__all__ = [
    "ADBDevice",
    "ADBDeviceManager",
    "AsyncADBDevice",
    "AsyncADBDeviceManager",
    "AsyncDeviceAdapter",
    "MockDevice",
    "RemoteDevice",
    "RemoteDeviceManager",
]
