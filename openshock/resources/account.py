from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from ..models import Token, User

if TYPE_CHECKING:
    from ..client import _BaseClient


class AccountResource:
    def __init__(self, client: _BaseClient) -> None:
        self._client = client

    def user_self(self) -> User:
        """GET /1/users/self — Get the authenticated user's info."""
        resp = self._client._request("GET", "/1/users/self")
        return User.from_dict(resp.get("data", resp))

    def token_self(self) -> Token:
        """GET /1/tokens/self — Get info about the API token being used."""
        resp = self._client._request("GET", "/1/tokens/self")
        return Token.from_dict(resp.get("data", resp))

    def list_tokens(self) -> list[Token]:
        """GET /1/tokens — List all API tokens for the authenticated user."""
        resp = self._client._request("GET", "/1/tokens")
        return [Token.from_dict(t) for t in (resp.get("data") or [])]

    def create_token(
        self,
        name: str,
        permissions: list[str],
        valid_until: str | None = None,
    ) -> Token:
        """POST /1/tokens — Create a new API token."""
        body: dict[str, Any] = {"name": name, "permissions": permissions}
        if valid_until is not None:
            body["validUntil"] = valid_until
        resp = self._client._request("POST", "/1/tokens", json=body)
        return Token.from_dict(resp.get("data", resp))

    def get_token(self, token_id: str | UUID) -> Token:
        """GET /1/tokens/{tokenId} — Get a token by ID."""
        resp = self._client._request("GET", f"/1/tokens/{token_id}")
        return Token.from_dict(resp.get("data", resp))

    def edit_token(
        self,
        token_id: str | UUID,
        *,
        name: str | None = None,
        permissions: list[str] | None = None,
    ) -> None:
        """PATCH /1/tokens/{tokenId} — Edit a token's name or permissions."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if permissions is not None:
            body["permissions"] = permissions
        self._client._request("PATCH", f"/1/tokens/{token_id}", json=body)

    def revoke_token(self, token_id: str | UUID) -> None:
        """DELETE /1/tokens/{tokenId} — Permanently revoke a token."""
        self._client._request("DELETE", f"/1/tokens/{token_id}")
