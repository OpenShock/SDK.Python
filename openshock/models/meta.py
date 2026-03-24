from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .common import require_dt


@dataclass
class BackendInfo:
    """
    Represents the backend info returned from GET /1 (after unwrapping legacy).

    Example payload (inner `data` object):

        {
          "version": "1.2.3",
          "commit": "abcdef",
          "currentTime": "2024-06-01T12:34:56Z",
          "frontendUrl": "https://openshock.app",
          "shortLinkUrl": "https://os.link",
          "turnstileSiteKey": "xxx",
          "isUserAuthenticated": true,
          "oAuthProviders": ["discord", "github"],
          "docsUrl": "https://docs.openshock.app"
        }
    """

    version: str
    commit: str
    current_time: datetime
    frontend_url: str
    short_link_url: str
    turnstile_site_key: str
    is_user_authenticated: bool
    o_auth_providers: list[str]
    docs_url: str | None = None

    @classmethod
    def from_any(cls, data: Any) -> BackendInfo:
        if not isinstance(data, dict):
            raise TypeError(f"BackendInfo.from_any expected dict, got {type(data)!r}")

        return cls(
            version=data["version"],
            commit=data["commit"],
            current_time=require_dt(data["currentTime"]),
            frontend_url=data["frontendUrl"],
            short_link_url=data["shortLinkUrl"],
            turnstile_site_key=data["turnstileSiteKey"],
            is_user_authenticated=bool(data["isUserAuthenticated"]),
            o_auth_providers=list(data.get("oAuthProviders", [])),
            docs_url=data.get("docsUrl"),
        )


@dataclass
class Stats:
    """
    Represents the stats returned from GET /1/public/stats (after unwrapping).

    Example payload (inner `data` object):

        {
          "devicesOnline": 42
        }
    """

    devices_online: int

    @classmethod
    def from_any(cls, data: Any) -> Stats:
        if not isinstance(data, dict):
            raise TypeError(f"Stats.from_any expected dict, got {type(data)!r}")

        return cls(
            devices_online=int(data["devicesOnline"]),
        )
