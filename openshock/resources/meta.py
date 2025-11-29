from __future__ import annotations

from typing import Any, Dict


class MetaResource:
    def __init__(self, client: "OpenShockClient") -> None:
        self._client = client

    def backend_info(self) -> Dict[str, Any]:
        """
        GET /1
        Gets the version and info about the OpenShock backend.

        Returns the full legacy data response dict.
        """
        return self._client._request("GET", "/1")

    def online_stats(self) -> Dict[str, Any]:
        """
        GET /1/public/stats
        Gets public online devices statistics.
        """
        return self._client._request("GET", "/1/public/stats")
