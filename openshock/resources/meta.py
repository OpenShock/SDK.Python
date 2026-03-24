from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import BackendInfo, Stats

if TYPE_CHECKING:
    from ..client import _BaseClient


class MetaResource:
    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    def backend_info(self) -> BackendInfo:
        """GET /1 — Returns backend version and metadata."""
        resp = self._client._request("GET", "/1")
        return BackendInfo.from_any(resp.get("data", resp))

    def online_stats(self) -> Stats:
        """GET /1/public/stats — Returns online device/shocker counts."""
        resp = self._client._request("GET", "/1/public/stats")
        return Stats.from_any(resp.get("data", resp))
