# openshock/models/account.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from .common import parse_dt, parse_uuid, PermissionType, RoleType


@dataclass
class User:
    id: UUID
    name: str
    email: str
    image: str
    roles: List[RoleType]
    rank: str

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=parse_uuid(data["id"]),
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
    permissions: List[PermissionType]

    @classmethod
    def from_dict(cls, data: dict) -> "Token":
        return cls(
            id=parse_uuid(data["id"]),
            name=data["name"],
            created_on=parse_dt(data["createdOn"]),
            valid_until=parse_dt(data.get("validUntil")),
            last_used=parse_dt(data.get("lastUsed")),
            permissions=list(data.get("permissions", [])),
        )
