from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .exceptions import (
    OpenShockError,
    OpenShockAuthError,
    OpenShockNotFound,
    OpenShockApiError,
)
from .auth import Auth, ApiTokenAuth, HubTokenAuth
from .resources.meta import MetaResource
from .resources.account import AccountResource
from .resources.devices import DevicesResource
from .resources.shockers import ShockersResource
from .resources.shares import SharesResource
from .resources.hub import HubResource


class _BaseClient:
    """
    Internal base client that handles HTTP, auth and error mapping.
    Concrete clients subclass this and attach resources.
    """

    def __init__(
        self,
        *,
        auth: Auth,
        base_url: str = "https://api.openshock.app",
        timeout: float = 10.0,
    ) -> None:
        self._auth = auth
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
        )

    # --- lifecycle ---------------------------------------------------------

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # --- internal helpers --------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Any:
        """
        Perform an HTTP request and return parsed JSON for 2xx responses.

        On non-2xx, raises one of:
        - OpenShockAuthError (401/403)
        - OpenShockNotFound (404)
        - OpenShockApiError (anything else)
        """
        headers = dict(self._auth.headers() or {})

        resp = self._client.request(
            method,
            path,
            params=params,
            json=json,
            headers=headers,
        )

        if 200 <= resp.status_code < 300:
            if "application/json" in resp.headers.get("Content-Type", ""):
                return resp.json()
            try:
                return resp.json()
            except ValueError:
                return resp.text

        # Try to parse problem details if present.
        message = None
        detail = None
        title = None
        try:
            body = resp.json()
            message = body.get("message") or body.get("detail") or body.get("title")
            detail = body.get("detail")
            title = body.get("title")
        except Exception:
            body = None  # noqa: F841

        text = message or detail or title or resp.text or f"HTTP {resp.status_code}"

        if resp.status_code in (401, 403):
            raise OpenShockAuthError(text)
        if resp.status_code == 404:
            raise OpenShockNotFound(text)

        raise OpenShockApiError(
            f"{resp.status_code} error calling {resp.request.method} {resp.request.url}: {text}"
        )


class OpenShockClient(_BaseClient):
    """
    High-level client for the *user* OpenShock REST API (ApiToken-based).

    Usage:

        from openshock import OpenShockClient

        client = OpenShockClient(api_token="os_xxx")
        devices = client.devices.list()

    Or with an explicit ApiTokenAuth:

        from openshock import OpenShockClient, ApiTokenAuth

        auth = ApiTokenAuth("os_xxx")
        client = OpenShockClient(auth=auth)
    """

    def __init__(
        self,
        *,
        auth: Optional[ApiTokenAuth] = None,
        api_token: Optional[str] = None,
        base_url: str = "https://api.openshock.app",
        timeout: float = 10.0,
    ) -> None:
        # Resolve auth: explicit `auth` wins, then api_token
        if auth is not None and api_token is not None:
            raise ValueError("Provide either `auth` or `api_token`, not both.")

        if auth is None and api_token is None:
            raise ValueError("You must provide either `auth` or `api_token`.")

        if auth is None:
            auth = ApiTokenAuth(api_token)  # type: ignore[arg-type]

        super().__init__(auth=auth, base_url=base_url, timeout=timeout)

        # Resources available for normal API tokens
        self.meta = MetaResource(self)
        self.account = AccountResource(self)
        self.devices = DevicesResource(self)
        self.shockers = ShockersResource(self)
        self.shares = SharesResource(self)


class OpenShockHubClient(_BaseClient):
    """
    High-level client for the *hub/device* OpenShock REST API (HubToken-based).

    Usage:

        from openshock import OpenShockHubClient

        client = OpenShockHubClient(hub_token="hub_xxx")
        info = client.hub.self()

    Or with an explicit HubTokenAuth:

        from openshock import OpenShockHubClient, HubTokenAuth

        auth = HubTokenAuth("hub_xxx")
        client = OpenShockHubClient(auth=auth)
    """

    def __init__(
        self,
        *,
        auth: Optional[HubTokenAuth] = None,
        hub_token: Optional[str] = None,
        base_url: str = "https://api.openshock.app",
        timeout: float = 10.0,
    ) -> None:
        if auth is not None and hub_token is not None:
            raise ValueError("Provide either `auth` or `hub_token`, not both.")

        if auth is None and hub_token is None:
            raise ValueError("You must provide either `auth` or `hub_token`.")

        if auth is None:
            auth = HubTokenAuth(hub_token)  # type: ignore[arg-type]

        super().__init__(auth=auth, base_url=base_url, timeout=timeout)

        # Hub-specific endpoints
        self.hub = HubResource(self)
        # You *can* also expose meta here if you want backend info/stats from a hub:
        self.meta = MetaResource(self)
