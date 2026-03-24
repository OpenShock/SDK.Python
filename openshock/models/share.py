from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from .common import PauseReason, parse_dt, parse_uuid, require_dt, require_uuid
from .shocker import ShockerLimits, ShockerPermissions


@dataclass
class BasicUserInfo:
    id: UUID
    name: str
    image: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BasicUserInfo:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            image=data["image"],
        )


@dataclass
class PublicShareShocker:
    id: UUID
    name: str
    permissions: ShockerPermissions
    limits: ShockerLimits
    paused: PauseReason

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PublicShareShocker:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            permissions=ShockerPermissions.from_dict(data["permissions"]),
            limits=ShockerLimits.from_dict(data["limits"]),
            paused=PauseReason(data.get("paused", 0)),
        )


@dataclass
class PublicShareDevice:
    id: UUID
    name: str
    shockers: list[PublicShareShocker]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PublicShareDevice:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            shockers=[PublicShareShocker.from_dict(s) for s in data.get("shockers", [])],
        )


@dataclass
class PublicShare:
    id: UUID
    name: str
    created_on: datetime
    expires_on: datetime | None
    author: BasicUserInfo
    devices: list[PublicShareDevice]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PublicShare:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            created_on=require_dt(data["createdOn"]),
            expires_on=parse_dt(data.get("expiresOn")),
            author=BasicUserInfo.from_dict(data["author"]),
            devices=[PublicShareDevice.from_dict(d) for d in data.get("devices", [])],
        )


@dataclass
class OwnPublicShare:
    """Response from GET /1/shares/links (listing own shares)."""

    id: UUID
    name: str
    created_on: datetime
    expires_on: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OwnPublicShare:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            created_on=require_dt(data["createdOn"]),
            expires_on=parse_dt(data.get("expiresOn")),
        )


@dataclass
class UserShareInfo:
    id: UUID
    name: str
    created_on: datetime
    permissions: ShockerPermissions
    limits: ShockerLimits
    paused: PauseReason

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserShareInfo:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            created_on=require_dt(data["createdOn"]),
            permissions=ShockerPermissions.from_dict(data["permissions"]),
            limits=ShockerLimits.from_dict(data["limits"]),
            paused=PauseReason(data.get("paused", 0)),
        )


@dataclass
class UserShare:
    """A user and their shared shockers."""

    id: UUID
    name: str
    image: str
    shares: list[UserShareInfo]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserShare:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            image=data["image"],
            shares=[UserShareInfo.from_dict(s) for s in data.get("shares", [])],
        )


@dataclass
class UserShares:
    """Response from GET /2/shares/user."""

    outgoing: list[UserShare]
    incoming: list[UserShare]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserShares:
        return cls(
            outgoing=[UserShare.from_dict(s) for s in data.get("outgoing", [])],
            incoming=[UserShare.from_dict(s) for s in data.get("incoming", [])],
        )


@dataclass
class ShareInviteShocker:
    permissions: ShockerPermissions
    limits: ShockerLimits
    id: UUID | None = None
    name: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShareInviteShocker:
        return cls(
            permissions=ShockerPermissions.from_dict(data["permissions"]),
            limits=ShockerLimits.from_dict(data["limits"]),
            id=parse_uuid(data.get("id")),
            name=data.get("name"),
        )

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "permissions": self.permissions.to_dict(),
            "limits": self.limits.to_dict(),
        }
        if self.id is not None:
            d["id"] = str(self.id)
        return d


@dataclass
class ShareInvite:
    id: UUID
    created_at: datetime
    owner: BasicUserInfo
    shared_with: BasicUserInfo
    shockers: list[ShareInviteShocker]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShareInvite:
        return cls(
            id=require_uuid(data["id"]),
            created_at=require_dt(data["createdAt"]),
            owner=BasicUserInfo.from_dict(data["owner"]),
            shared_with=BasicUserInfo.from_dict(data["sharedWith"]),
            shockers=[ShareInviteShocker.from_dict(s) for s in data.get("shockers", [])],
        )
