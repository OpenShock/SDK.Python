from __future__ import annotations

from typing import Any, Dict


class HubResource:
    """
    Endpoints that are used with a Hub / DeviceToken.
    """

    def __init__(self, client: "OpenShockClient") -> None:
        self._client = client

    def self(self) -> Dict[str, Any]:
        """
        GET /1/device/self
        Gets information about the authenticated device (HubToken).
        """
        resp = self._client._request("GET", "/1/device/self")
        return resp.get("data") or {}

    def assign_lcg(self) -> Dict[str, Any]:
        """
        GET /1/device/assignLCG
        Gets the best suited Live Control Gateway node for this device.

        Returns the full node response.
        """
        return self._client._request("GET", "/1/device/assignLCG")

    def pair(self, pair_code: str) -> str:
        """
        GET /1/device/pair/{pairCode}
        Pair a device with a pair code.

        Returns the 'data' string from the response.
        """
        resp = self._client._request("GET", f"/1/device/pair/{pair_code}")
        if isinstance(resp, dict):
            return resp.get("data") or ""
        return str(resp)
