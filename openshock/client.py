from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Any, TypeVar

import httpx

from .auth import ApiTokenAuth, Auth, HubTokenAuth
from .exceptions import (
    OpenShockApiError,
    OpenShockAuthError,
    OpenShockNotFound,
)
from .resources.account import AccountResource
from .resources.devices import DevicesResource
from .resources.hub import HubResource
from .resources.meta import MetaResource
from .resources.sessions import SessionsResource
from .resources.shares import SharesResource
from .resources.shockers import ShockersResource
from .resources.user_shares import UserSharesResource

T = TypeVar("T")
_SelfT = TypeVar("_SelfT", bound="_BaseClient")


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

    def __enter__(self: _SelfT) -> _SelfT:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    # --- internal helpers --------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        transform: Callable[[Any], T] | None = None,
    ) -> T | Any:
        """
        Perform an HTTP request and return parsed JSON/text for 2xx responses.

        - NO special handling of any "wrapper" formats.
        - If `transform` is provided, it's called with the parsed payload
          (JSON-decoded object or text), and its return value is returned.
        - Otherwise the parsed payload is returned as-is.

        On non-2xx, raises:
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

        # Success
        if 200 <= resp.status_code < 300:
            # Parse body -> payload
            if "application/json" in resp.headers.get("Content-Type", ""):
                payload: Any = resp.json()
            else:
                try:
                    payload = resp.json()
                except ValueError:
                    payload = resp.text

            if transform is not None:
                return transform(payload)
            return payload

        # Error path: try to parse problem details if present.
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

        raise OpenShockApiError(f"{resp.status_code} error calling {resp.request.method} {resp.request.url}: {text}")


class OpenShockClient(_BaseClient):
    """
    High-level client for the *user* OpenShock REST API (ApiToken-based).
    """

    def __init__(
        self,
        *,
        auth: ApiTokenAuth | None = None,
        api_token: str | None = None,
        base_url: str = "https://api.openshock.app",
        timeout: float = 10.0,
    ) -> None:
        if auth is not None and api_token is not None:
            raise ValueError("Provide either `auth` or `api_token`, not both.")

        if auth is None and api_token is None:
            raise ValueError("You must provide either `auth` or `api_token`.")

        if auth is None:
            auth = ApiTokenAuth(api_token)  # type: ignore[arg-type]

        super().__init__(auth=auth, base_url=base_url, timeout=timeout)

        self.meta = MetaResource(self)
        self.account = AccountResource(self)
        self.devices = DevicesResource(self)
        self.shockers = ShockersResource(self)
        self.shares = SharesResource(self)
        self.sessions = SessionsResource(self)
        self.user_shares = UserSharesResource(self)


class OpenShockHubClient(_BaseClient):
    """
    High-level client for the *hub/device* OpenShock REST API (HubToken-based).
    """

    def __init__(
        self,
        *,
        auth: HubTokenAuth | None = None,
        hub_token: str | None = None,
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

        self.hub = HubResource(self)
        self.meta = MetaResource(self)
