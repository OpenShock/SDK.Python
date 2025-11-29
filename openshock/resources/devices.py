from __future__ import annotations

from typing import Any, Dict, List


class DevicesResource:
    def __init__(self, client: "OpenShockClient") -> None:
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        GET /1/devices
        Get all devices for the current user.
        Returns the 'data' array.
        """
        resp = self._client._request("GET", "/1/devices")
        return resp.get("data") or []

    def get(self, device_id: str) -> Dict[str, Any]:
        """
        GET /1/devices/{deviceId}
        Get a device by its id.
        Returns the 'data' object.
        """
        resp = self._client._request("GET", f"/1/devices/{device_id}")
        return resp.get("data") or {}

    def delete(self, device_id: str) -> None:
        """
        DELETE /1/devices/{deviceId}
        Remove a device from the current user's account.
        """
        self._client._request("DELETE", f"/1/devices/{device_id}")

    def regenerate_token(self, device_id: str) -> str:
        """
        PUT /1/devices/{deviceId}
        Regenerate a device token. Returns the plain string token.
        """
        resp = self._client._request("PUT", f"/1/devices/{device_id}")
        if isinstance(resp, str):
            return resp
        raise RuntimeError("Unexpected response while regenerating device token")

    def shockers(self, device_id: str) -> List[Dict[str, Any]]:
        """
        GET /1/devices/{deviceId}/shockers
        Get all shockers for a device.
        Returns the 'data' array.
        """
        resp = self._client._request("GET", f"/1/devices/{device_id}/shockers")
        return resp.get("data") or []
