from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from .common import ControlType, ShockerModelType, require_dt, require_uuid


@dataclass
class ShockerPermissions:
    vibrate: bool
    sound: bool
    shock: bool
    live: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShockerPermissions:
        return cls(
            vibrate=data["vibrate"],
            sound=data["sound"],
            shock=data["shock"],
            live=data.get("live", False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "vibrate": self.vibrate,
            "sound": self.sound,
            "shock": self.shock,
            "live": self.live,
        }


@dataclass
class ShockerLimits:
    intensity: int | None = None
    duration: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShockerLimits:
        return cls(
            intensity=data.get("intensity"),
            duration=data.get("duration"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "intensity": self.intensity,
            "duration": self.duration,
        }


@dataclass
class Shocker:
    id: UUID
    name: str
    rf_id: int
    model: ShockerModelType
    created_on: datetime
    is_paused: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Shocker:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            rf_id=data["rfId"],
            model=data["model"],
            created_on=require_dt(data["createdOn"]),
            is_paused=data.get("isPaused", False),
        )


@dataclass
class MinimalShocker:
    id: UUID
    rf_id: int
    model: ShockerModelType

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MinimalShocker:
        return cls(
            id=require_uuid(data["id"]),
            rf_id=data["rfId"],
            model=data["model"],
        )


@dataclass
class ControlLogSender:
    id: UUID
    name: str
    image: str
    custom_name: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ControlLogSender:
        return cls(
            id=require_uuid(data["id"]),
            name=data["name"],
            image=data["image"],
            custom_name=data.get("customName"),
        )


@dataclass
class ShockerLog:
    id: UUID
    created_on: datetime
    type: ControlType
    controlled_by: ControlLogSender
    intensity: int
    duration: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShockerLog:
        return cls(
            id=require_uuid(data["id"]),
            created_on=require_dt(data["createdOn"]),
            type=data["type"],
            controlled_by=ControlLogSender.from_dict(data["controlledBy"]),
            intensity=data["intensity"],
            duration=data["duration"],
        )


@dataclass
class Control:
    """A single control command for POST /2/shockers/control."""

    id: str | UUID
    type: ControlType
    intensity: int
    duration: int
    exclusive: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "type": self.type,
            "intensity": self.intensity,
            "duration": self.duration,
            "exclusive": self.exclusive,
        }


@dataclass
class ShareInfo:
    shared_with: dict[str, Any]  # BasicUserInfo
    created_on: datetime
    permissions: ShockerPermissions
    limits: ShockerLimits
    paused: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShareInfo:
        return cls(
            shared_with=data["sharedWith"],
            created_on=require_dt(data["createdOn"]),
            permissions=ShockerPermissions.from_dict(data["permissions"]),
            limits=ShockerLimits.from_dict(data["limits"]),
            paused=data.get("paused", False),
        )


@dataclass
class ShareCode:
    id: UUID
    created_on: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShareCode:
        return cls(
            id=require_uuid(data["id"]),
            created_on=require_dt(data["createdOn"]),
        )
