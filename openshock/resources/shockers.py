from __future__ import annotations

from typing import Any, Dict, List, Sequence


class ShockersResource:
    def __init__(self, client: "OpenShockClient") -> None:
        self._client = client

    # --- lists & info ------------------------------------------------------

    def list_own(self) -> List[Dict[str, Any]]:
        """
        GET /1/shockers/own
        List all shockers belonging to the authenticated user.

        Returns array of devices-with-shockers.
        """
        resp = self._client._request("GET", "/1/shockers/own")
        return resp.get("data") or []

    def list_shared(self) -> List[Dict[str, Any]]:
        """
        GET /1/shockers/shared
        List all shockers shared with the authenticated user.
        """
        resp = self._client._request("GET", "/1/shockers/shared")
        return resp.get("data") or []

    def get(self, shocker_id: str) -> Dict[str, Any]:
        """
        GET /1/shockers/{shockerId}
        Get information about a specific shocker (with its device).
        """
        resp = self._client._request("GET", f"/1/shockers/{shocker_id}")
        return resp.get("data") or {}

    # --- logs --------------------------------------------------------------

    def logs(
        self,
        shocker_id: str,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        GET /1/shockers/{shockerId}/logs
        Get logs for a shocker (offset + limit, limit max 500).
        """
        params = {"offset": offset, "limit": limit}
        resp = self._client._request("GET", f"/1/shockers/{shocker_id}/logs", params=params)
        return resp.get("data") or []

    # --- pause / control ---------------------------------------------------

    def pause(self, shocker_id: str, pause: bool) -> bool:
        """
        POST /1/shockers/{shockerId}/pause
        Pause or unpause a shocker. Body is { "pause": bool }.

        Returns the underlying boolean data field.
        """
        body = {"pause": pause}
        resp = self._client._request("POST", f"/1/shockers/{shocker_id}/pause", json=body)
        if isinstance(resp, dict):
            return bool(resp.get("data"))
        return bool(resp)

    def control(self, controls: Sequence[Dict[str, Any]]) -> Any:
        """
        POST /1/shockers/control  (deprecated in favor of /2/shockers/control, but still usable)

        'controls' should be a sequence of Control objects as dictionaries
        following the 'Control' schema from the spec:
        {
          "shockerId": "...",
          "type": "...",   # e.g. "shock", "vibrate", etc.
          "intensity": 50,
          "duration": 1000
        }

        This just POSTs the JSON array and returns the raw response.
        """
        if not controls:
            raise ValueError("controls must be a non-empty sequence")

        return self._client._request("POST", "/1/shockers/control", json=list(controls))
