from __future__ import annotations

import builtins
from typing import TYPE_CHECKING
from uuid import UUID

from ..models import Session

if TYPE_CHECKING:
    from ..client import _BaseClient


class SessionsResource:
    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    def list(self) -> builtins.list[Session]:
        """GET /1/sessions — List all active login sessions."""
        resp = self._client._request("GET", "/1/sessions")
        return [Session.from_dict(s) for s in (resp.get("data") or [])]

    def get_current(self) -> Session:
        """GET /1/sessions/self — Get info about the current session."""
        resp = self._client._request("GET", "/1/sessions/self")
        return Session.from_dict(resp.get("data", resp))

    def delete(self, session_id: str | UUID) -> None:
        """DELETE /1/sessions/{sessionId} — Revoke a session."""
        self._client._request("DELETE", f"/1/sessions/{session_id}")
