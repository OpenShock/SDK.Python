from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from ..models import (
    OwnPublicShare,
    PublicShare,
    ShockerLimits,
    ShockerPermissions,
)

if TYPE_CHECKING:
    from ..client import _BaseClient


class SharesResource:
    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    # --- public share links ---

    def list_public(self) -> list[OwnPublicShare]:
        """GET /1/shares/links — List all public shares owned by the user."""
        resp = self._client._request("GET", "/1/shares/links")
        return [OwnPublicShare.from_dict(s) for s in (resp.get("data") or [])]

    def create_public(
        self,
        name: str,
        *,
        expires_on: str | None = None,
    ) -> str:
        """POST /1/shares/links — Create a new public share. Returns share ID."""
        body: dict[str, Any] = {"name": name}
        if expires_on is not None:
            body["expiresOn"] = expires_on
        resp: Any = self._client._request("POST", "/1/shares/links", json=body)
        if isinstance(resp, dict):
            return str(resp.get("data", ""))
        return str(resp)

    def delete_public(self, public_share_id: str | UUID) -> None:
        """DELETE /1/shares/links/{publicShareId} — Delete a public share."""
        self._client._request("DELETE", f"/1/shares/links/{public_share_id}")

    def public_get(self, public_share_id: str | UUID) -> PublicShare:
        """GET /1/public/shares/links/{publicShareId} — Get public share info (unauthenticated)."""
        resp = self._client._request("GET", f"/1/public/shares/links/{public_share_id}")
        return PublicShare.from_dict(resp.get("data", resp))

    # --- shockers within public shares ---

    def add_shocker(
        self,
        public_share_id: str | UUID,
        shocker_id: str | UUID,
    ) -> None:
        """POST /1/shares/links/{publicShareId}/{shockerId}"""
        self._client._request("POST", f"/1/shares/links/{public_share_id}/{shocker_id}")

    def edit_shocker(
        self,
        public_share_id: str | UUID,
        shocker_id: str | UUID,
        *,
        permissions: ShockerPermissions,
        limits: ShockerLimits,
        cooldown: int | None = None,
    ) -> None:
        """PATCH /1/shares/links/{publicShareId}/{shockerId}"""
        body: dict[str, Any] = {
            "permissions": permissions.to_dict(),
            "limits": limits.to_dict(),
        }
        if cooldown is not None:
            body["cooldown"] = cooldown
        self._client._request(
            "PATCH",
            f"/1/shares/links/{public_share_id}/{shocker_id}",
            json=body,
        )

    def remove_shocker(
        self,
        public_share_id: str | UUID,
        shocker_id: str | UUID,
    ) -> None:
        """DELETE /1/shares/links/{publicShareId}/{shockerId}"""
        self._client._request("DELETE", f"/1/shares/links/{public_share_id}/{shocker_id}")

    def pause_shocker(
        self,
        public_share_id: str | UUID,
        shocker_id: str | UUID,
        pause: bool,
    ) -> Any:
        """POST /1/shares/links/{publicShareId}/{shockerId}/pause"""
        return self._client._request(
            "POST",
            f"/1/shares/links/{public_share_id}/{shocker_id}/pause",
            json={"pause": pause},
        )

    # --- share codes ---

    def link_code(self, share_code_id: str | UUID) -> None:
        """POST /1/shares/code/{shareCodeId} — Redeem a share code."""
        self._client._request("POST", f"/1/shares/code/{share_code_id}")

    def delete_code(self, share_code_id: str | UUID) -> None:
        """DELETE /1/shares/code/{shareCodeId} — Delete a share code."""
        self._client._request("DELETE", f"/1/shares/code/{share_code_id}")
