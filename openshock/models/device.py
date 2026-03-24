from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from .common import require_dt, require_uuid


@dataclass
class Device:
    id: UUID
    name: str
    created_on: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Device:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            created_on=require_dt(data["createdOn"]),
        )


@dataclass
class DeviceWithToken:
    """Response from creating a new device."""

    id: UUID
    name: str
    created_on: datetime
    token: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeviceWithToken:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            created_on=require_dt(data["createdOn"]),
            token=data["token"],
        )


@dataclass
class PairCode:
    id: str
    created_on: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PairCode:
        return cls(
            id=data["id"],
            created_on=require_dt(data["createdOn"]),
        )


@dataclass
class LcgNode:
    """V1 LCG assignment response."""

    fqdn: str
    country: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LcgNode:
        return cls(
            fqdn=data["fqdn"],
            country=data["country"],
        )


@dataclass
class LcgNodeV2:
    """V2 LCG assignment response."""

    host: str
    port: int
    path: str
    country: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LcgNodeV2:
        return cls(
            host=data["host"],
            port=data["port"],
            path=data["path"],
            country=data["country"],
        )


@dataclass
class LcgInfo:
    """LCG connection info for a specific device."""

    gateway: str
    country: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LcgInfo:
        return cls(
            gateway=data["gateway"],
            country=data["country"],
        )


@dataclass
class OtaUpdate:
    id: int
    started_at: datetime
    status: str
    version: str
    message: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OtaUpdate:
        return cls(
            id=data["id"],
            started_at=require_dt(data["startedAt"]),
            status=data["status"],
            version=data["version"],
            message=data.get("message"),
        )


@dataclass
class DeviceSelf:
    """Response from GET /1/device/self (hub endpoint)."""

    id: UUID
    name: str
    shockers: list[Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeviceSelf:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            shockers=data.get("shockers", []),
        )
