from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from uuid import UUID

from ..models import (
    ShareInvite,
    ShareInviteShocker,
    ShockerLimits,
    ShockerPermissions,
    UserShare,
    UserShares,
)

if TYPE_CHECKING:
    from ..client import _BaseClient


class UserSharesResource:
    """V2 user-to-user share management."""

    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    def get(self) -> UserShares:
        """GET /2/shares/user — Get all user shares (incoming and outgoing)."""
        resp = self._client._request("GET", "/2/shares/user")
        return UserShares.from_dict(resp)

    def create_invite(
        self,
        shockers: Sequence[ShareInviteShocker | dict[str, Any]],
        *,
        user: str | UUID | None = None,
    ) -> str:
        """POST /2/shares/user/invites — Create a share invite. Returns invite ID."""
        shocker_list = []
        for s in shockers:
            if isinstance(s, ShareInviteShocker):
                shocker_list.append(s.to_dict())
            else:
                shocker_list.append(s)

        body: dict[str, Any] = {"shockers": shocker_list}
        if user is not None:
            body["user"] = str(user)

        resp = self._client._request("POST", "/2/shares/user/invites", json=body)
        if isinstance(resp, str):
            return resp
        return str(resp)

    def list_outgoing_invites(self) -> list[ShareInvite]:
        """GET /2/shares/user/invites/outgoing — List pending outgoing invites."""
        resp = self._client._request("GET", "/2/shares/user/invites/outgoing")
        return [ShareInvite.from_dict(i) for i in (resp if isinstance(resp, list) else [])]

    def list_incoming_invites(self) -> list[ShareInvite]:
        """GET /2/shares/user/invites/incoming — List pending incoming invites."""
        resp = self._client._request("GET", "/2/shares/user/invites/incoming")
        return [ShareInvite.from_dict(i) for i in (resp if isinstance(resp, list) else [])]

    def accept_invite(self, invite_id: str | UUID) -> UserShare:
        """POST /2/shares/user/invites/incoming/{inviteId} — Accept a share invite."""
        resp = self._client._request("POST", f"/2/shares/user/invites/incoming/{invite_id}")
        return UserShare.from_dict(resp)

    def delete_outgoing_invite(self, invite_id: str | UUID) -> None:
        """DELETE /2/shares/user/invites/outgoing/{inviteId} — Cancel an outgoing invite."""
        self._client._request("DELETE", f"/2/shares/user/invites/outgoing/{invite_id}")

    def deny_incoming_invite(self, invite_id: str | UUID) -> None:
        """DELETE /2/shares/user/invites/incoming/{inviteId} — Deny an incoming invite."""
        self._client._request("DELETE", f"/2/shares/user/invites/incoming/{invite_id}")

    def bulk_pause_shockers(
        self,
        user_id: str | UUID,
        shockers: Sequence[str | UUID],
        pause: bool,
    ) -> dict[str, Any]:
        """POST /2/shares/user/{userId}/shockers/pause — Bulk pause/unpause shared shockers."""
        body = {
            "shockers": [str(s) for s in shockers],
            "pause": pause,
        }
        return self._client._request("POST", f"/2/shares/user/{user_id}/shockers/pause", json=body)

    def bulk_remove_shockers(
        self,
        user_id: str | UUID,
        shockers: Sequence[str | UUID],
    ) -> dict[str, Any]:
        """DELETE /2/shares/user/{userId}/shockers — Bulk remove shared shockers."""
        return self._client._request(
            "DELETE",
            f"/2/shares/user/{user_id}/shockers",
            json=[str(s) for s in shockers],
        )

    def bulk_update_shockers(
        self,
        user_id: str | UUID,
        shockers: Sequence[str | UUID],
        *,
        permissions: ShockerPermissions,
        limits: ShockerLimits,
    ) -> None:
        """PATCH /2/shares/user/{userId}/shockers — Bulk update shared shocker permissions."""
        body = {
            "permissions": permissions.to_dict(),
            "limits": limits.to_dict(),
            "shockers": [str(s) for s in shockers],
        }
        self._client._request("PATCH", f"/2/shares/user/{user_id}/shockers", json=body)
