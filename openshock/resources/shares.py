from __future__ import annotations

from typing import Any, Dict


class SharesResource:
    def __init__(self, client: "OpenShockClient") -> None:
        self._client = client

    def public_get(self, public_share_id: str) -> Dict[str, Any]:
        """
        GET /1/public/shares/links/{publicShareId}
        Get information about a public share, including devices + shockers.
        """
        resp = self._client._request("GET", f"/1/public/shares/links/{public_share_id}")
        return resp.get("data") or {}

    def pause_shocker(
        self,
        public_share_id: str,
        shocker_id: str,
        pause: bool,
    ) -> Dict[str, Any]:
        """
        POST /1/shares/links/{publicShareId}/{shockerId}/pause
        Pause/unpause a shocker within a specific public share (owner side).

        Returns the full response (includes pause reason etc.).
        """
        body = {"pause": pause}
        return self._client._request(
            "POST",
            f"/1/shares/links/{public_share_id}/{shocker_id}/pause",
            json=body,
        )
