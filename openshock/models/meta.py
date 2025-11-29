from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .common import parse_dt


@dataclass
class BackendInfo:
    version: str
    commit: str
    current_time: datetime
    frontend_url: str
    short_link_url: str
    turnstile_site_key: str
    is_user_authenticated: bool
    o_auth_providers: List[str]
    # nullable in spec
    docs_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "BackendInfo":
        return cls(
            version=data["version"],
            commit=data["commit"],
            current_time=parse_dt(data["currentTime"]),
            frontend_url=data["frontendUrl"],
            short_link_url=data["shortLinkUrl"],
            turnstile_site_key=data["turnstileSiteKey"],
            is_user_authenticated=bool(data["isUserAuthenticated"]),
            o_auth_providers=list(data.get("oAuthProviders", [])),
            docs_url=data.get("docsUrl"),
        )


@dataclass
class Stats:
    devices_online: int

    @classmethod
    def from_dict(cls, data: dict) -> "Stats":
        return cls(devices_online=int(data["devicesOnline"]))
