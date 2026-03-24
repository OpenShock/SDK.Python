from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from .common import parse_dt, require_dt, require_uuid


@dataclass
class Session:
    id: UUID
    ip: str
    user_agent: str
    created: datetime
    expires: datetime
    last_used: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Session:
        return cls(
            id=require_uuid(data["id"]),
            ip=data["ip"],
            user_agent=data["userAgent"],
            created=require_dt(data["created"]),
            expires=require_dt(data["expires"]),
            last_used=parse_dt(data.get("lastUsed")),
        )
