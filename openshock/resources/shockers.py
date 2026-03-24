from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from uuid import UUID

from ..models import (
    Control,
    ShareCode,
    ShareInfo,
    ShockerLimits,
    ShockerLog,
    ShockerPermissions,
)

if TYPE_CHECKING:
    from ..client import _BaseClient


class ShockersResource:
    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    # --- lists & info ---

    def list_own(self) -> list[dict[str, Any]]:
        """GET /1/shockers/own — List all shockers belonging to the authenticated user."""
        resp = self._client._request("GET", "/1/shockers/own")
        return resp.get("data") or []

    def list_shared(self) -> list[dict[str, Any]]:
        """GET /1/shockers/shared — List all shockers shared with the authenticated user."""
        resp = self._client._request("GET", "/1/shockers/shared")
        return resp.get("data") or []

    def get(self, shocker_id: str | UUID) -> dict[str, Any]:
        """GET /1/shockers/{shockerId} — Get shocker info with device details."""
        resp = self._client._request("GET", f"/1/shockers/{shocker_id}")
        return resp.get("data") or {}

    # --- CRUD ---

    def register(
        self,
        *,
        name: str,
        rf_id: int,
        device: str | UUID,
        model: str,
    ) -> str:
        """POST /1/shockers — Register a new shocker. Returns the new shocker ID."""
        body = {
            "name": name,
            "rfId": rf_id,
            "device": str(device),
            "model": model,
        }
        resp: Any = self._client._request("POST", "/1/shockers", json=body)
        if isinstance(resp, dict):
            return str(resp.get("data", ""))
        return str(resp)

    def edit(
        self,
        shocker_id: str | UUID,
        *,
        name: str | None = None,
        rf_id: int | None = None,
        device: str | UUID | None = None,
        model: str | None = None,
    ) -> None:
        """PATCH /1/shockers/{shockerId} — Update a shocker."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if rf_id is not None:
            body["rfId"] = rf_id
        if device is not None:
            body["device"] = str(device)
        if model is not None:
            body["model"] = model
        self._client._request("PATCH", f"/1/shockers/{shocker_id}", json=body)

    def delete(self, shocker_id: str | UUID) -> None:
        """DELETE /1/shockers/{shockerId} — Remove a shocker."""
        self._client._request("DELETE", f"/1/shockers/{shocker_id}")

    # --- control & pause ---

    def control(
        self,
        controls: Sequence[Control | dict[str, Any]],
        *,
        custom_name: str | None = None,
    ) -> Any:
        """POST /2/shockers/control — Send control commands to shockers (V2)."""
        if not controls:
            raise ValueError("controls must be a non-empty sequence")

        shocks = []
        for c in controls:
            if isinstance(c, Control):
                shocks.append(c.to_dict())
            else:
                shocks.append(c)

        body: dict[str, Any] = {"shocks": shocks}
        if custom_name is not None:
            body["customName"] = custom_name

        return self._client._request("POST", "/2/shockers/control", json=body)

    def pause(self, shocker_id: str | UUID, pause: bool) -> Any:
        """POST /1/shockers/{shockerId}/pause — Pause or unpause a shocker."""
        return self._client._request("POST", f"/1/shockers/{shocker_id}/pause", json={"pause": pause})

    # --- logs ---

    def logs(
        self,
        shocker_id: str | UUID,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ShockerLog]:
        """GET /1/shockers/{shockerId}/logs — Get control log history."""
        params = {"offset": offset, "limit": limit}
        resp = self._client._request("GET", f"/1/shockers/{shocker_id}/logs", params=params)
        return [ShockerLog.from_dict(e) for e in (resp.get("data") or [])]

    def all_logs(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """GET /1/shockers/logs — Get logs across all owned shockers."""
        params = {"offset": offset, "limit": limit}
        resp = self._client._request("GET", "/1/shockers/logs", params=params)
        return resp.get("data") or []

    # --- shares ---

    def get_shares(self, shocker_id: str | UUID) -> list[ShareInfo]:
        """GET /1/shockers/{shockerId}/shares — Get all user shares for a shocker."""
        resp = self._client._request("GET", f"/1/shockers/{shocker_id}/shares")
        return [ShareInfo.from_dict(s) for s in (resp.get("data") or [])]

    def create_share_code(
        self,
        shocker_id: str | UUID,
        *,
        permissions: ShockerPermissions,
        limits: ShockerLimits,
    ) -> str:
        """POST /1/shockers/{shockerId}/shares — Create a share code. Returns code ID."""
        body = {
            "permissions": permissions.to_dict(),
            "limits": limits.to_dict(),
        }
        resp: Any = self._client._request("POST", f"/1/shockers/{shocker_id}/shares", json=body)
        if isinstance(resp, dict):
            return str(resp.get("data", ""))
        return str(resp)

    def list_share_codes(self, shocker_id: str | UUID) -> list[ShareCode]:
        """GET /1/shockers/{shockerId}/shareCodes — List all share codes."""
        resp = self._client._request("GET", f"/1/shockers/{shocker_id}/shareCodes")
        return [ShareCode.from_dict(c) for c in (resp.get("data") or [])]

    def update_share(
        self,
        shocker_id: str | UUID,
        shared_with_user_id: str | UUID,
        *,
        permissions: ShockerPermissions,
        limits: ShockerLimits,
    ) -> None:
        """PATCH /1/shockers/{shockerId}/shares/{sharedWithUserId}"""
        body = {
            "permissions": permissions.to_dict(),
            "limits": limits.to_dict(),
        }
        self._client._request(
            "PATCH",
            f"/1/shockers/{shocker_id}/shares/{shared_with_user_id}",
            json=body,
        )

    def remove_share(
        self,
        shocker_id: str | UUID,
        shared_with_user_id: str | UUID,
    ) -> None:
        """DELETE /1/shockers/{shockerId}/shares/{sharedWithUserId}"""
        self._client._request(
            "DELETE",
            f"/1/shockers/{shocker_id}/shares/{shared_with_user_id}",
        )

    def pause_share(
        self,
        shocker_id: str | UUID,
        shared_with_user_id: str | UUID,
        pause: bool,
    ) -> Any:
        """POST /1/shockers/{shockerId}/shares/{sharedWithUserId}/pause"""
        return self._client._request(
            "POST",
            f"/1/shockers/{shocker_id}/shares/{shared_with_user_id}/pause",
            json={"pause": pause},
        )
