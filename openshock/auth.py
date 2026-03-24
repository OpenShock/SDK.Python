from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


class Auth:
    """
    Base class for authentication.

    Subclasses should override `headers()` to return the headers
    required for auth on each request.
    """

    def headers(self) -> Mapping[str, str]:
        return {}


@dataclass
class ApiTokenAuth(Auth):
    """
    Auth using an API token.

    Sends: OpenShockToken: <token>
    """

    token: str

    def headers(self) -> Mapping[str, str]:
        return {"OpenShockToken": self.token}


@dataclass
class HubTokenAuth(Auth):
    """
    Auth using a Device / Hub token.

    Sends: DeviceToken: <token>
    """

    token: str

    def headers(self) -> Mapping[str, str]:
        return {"DeviceToken": self.token}
