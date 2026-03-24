from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..models import DeviceSelf, LcgNodeV2

if TYPE_CHECKING:
    from ..client import _BaseClient


class HubResource:
    """Endpoints called by ESP32 hubs using DeviceToken auth."""

    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    def self_info(self) -> DeviceSelf:
        """GET /1/device/self — Get info about the authenticated hub."""
        resp = self._client._request("GET", "/1/device/self")
        return DeviceSelf.from_dict(resp.get("data", resp))

    def assign_lcg(self, *, version: int | None = None) -> LcgNodeV2:
        """GET /2/device/assignLCG — Get the best LCG node for this hub (V2)."""
        params: dict[str, Any] = {}
        if version is not None:
            params["version"] = version
        resp = self._client._request("GET", "/2/device/assignLCG", params=params or None)
        return LcgNodeV2.from_dict(resp)

    def pair(self, pair_code: str) -> str:
        """GET /1/device/pair/{pairCode} — Pair hub with account."""
        resp: Any = self._client._request("GET", f"/1/device/pair/{pair_code}")
        if isinstance(resp, dict):
            return str(resp.get("data", ""))
        return str(resp)
