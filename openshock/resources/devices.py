from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any
from uuid import UUID

from ..models import Device, DeviceWithToken, LcgInfo, OtaUpdate, PairCode, Shocker

if TYPE_CHECKING:
    from ..client import _BaseClient


class DevicesResource:
    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    def list(self) -> builtins.list[Device]:
        """GET /1/devices — List all devices for the authenticated user."""
        resp = self._client._request("GET", "/1/devices")
        return [Device.from_dict(d) for d in (resp.get("data") or [])]

    def create(self, name: str) -> DeviceWithToken:
        """POST /2/devices — Create a new device. Returns device with token."""
        resp = self._client._request("POST", "/2/devices", json={"name": name})
        return DeviceWithToken.from_dict(resp.get("data", resp))

    def get(self, device_id: str | UUID) -> Device:
        """GET /1/devices/{deviceId} — Get a device by ID."""
        resp = self._client._request("GET", f"/1/devices/{device_id}")
        return Device.from_dict(resp.get("data", resp))

    def edit(self, device_id: str | UUID, *, name: str) -> None:
        """PATCH /1/devices/{deviceId} — Update a device's name."""
        self._client._request("PATCH", f"/1/devices/{device_id}", json={"name": name})

    def delete(self, device_id: str | UUID) -> None:
        """DELETE /1/devices/{deviceId} — Remove a device."""
        self._client._request("DELETE", f"/1/devices/{device_id}")

    def regenerate_token(self, device_id: str | UUID) -> str:
        """PUT /1/devices/{deviceId} — Regenerate device token. Returns new token string."""
        resp: Any = self._client._request("PUT", f"/1/devices/{device_id}")
        if isinstance(resp, dict):
            return str(resp.get("data", ""))
        return str(resp)

    def shockers(self, device_id: str | UUID) -> builtins.list[Shocker]:
        """GET /1/devices/{deviceId}/shockers — Get all shockers for a device."""
        resp = self._client._request("GET", f"/1/devices/{device_id}/shockers")
        return [Shocker.from_dict(s) for s in (resp.get("data") or [])]

    def pair_code(self, device_id: str | UUID) -> PairCode:
        """GET /1/devices/{deviceId}/pair — Get the current pair code."""
        resp = self._client._request("GET", f"/1/devices/{device_id}/pair")
        return PairCode.from_dict(resp.get("data", resp))

    def lcg_info(self, device_id: str | UUID) -> LcgInfo:
        """GET /1/devices/{deviceId}/lcg — Get LCG connection info."""
        resp = self._client._request("GET", f"/1/devices/{device_id}/lcg")
        return LcgInfo.from_dict(resp.get("data", resp))

    def ota_history(self, device_id: str | UUID) -> builtins.list[OtaUpdate]:
        """GET /1/devices/{deviceId}/ota — Get OTA update history."""
        resp = self._client._request("GET", f"/1/devices/{device_id}/ota")
        return [OtaUpdate.from_dict(o) for o in (resp.get("data") or [])]
