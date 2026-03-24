# openshock/models/account.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from .common import PermissionType, RoleType, parse_dt, require_dt, require_uuid


@dataclass
class User:
    id: UUID
    name: str
    email: str
    image: str
    roles: list[RoleType]
    rank: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            email=data["email"],
            image=data["image"],
            roles=list(data.get("roles", [])),
            rank=data["rank"],
        )


@dataclass
class Token:
    id: UUID
    name: str
    created_on: datetime
    valid_until: datetime | None
    last_used: datetime | None
    permissions: list[PermissionType]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Token:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            created_on=require_dt(data["createdOn"]),
            valid_until=parse_dt(data.get("validUntil")),
            last_used=parse_dt(data.get("lastUsed")),
            permissions=list(data.get("permissions", [])),
        )
