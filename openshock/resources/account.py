# openshock/resources/account.py
from __future__ import annotations

from typing import Any, Dict


class AccountResource:
    def __init__(self, client: "OpenShockClient") -> None:
        self._client = client

    def user_self(self) -> Dict[str, Any]:
        """
        GET /1/users/self
        Get the current user's information.
        """
        return self._client._request("GET", "/1/users/self")

    def token_self(self) -> Dict[str, Any]:
        """
        GET /1/tokens/self
        Get info about the API token used.
        """
        return self._client._request("GET", "/1/tokens/self")
