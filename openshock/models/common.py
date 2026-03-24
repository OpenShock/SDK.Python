from __future__ import annotations

from datetime import datetime
from enum import IntFlag
from uuid import UUID


def parse_dt(value: str | None) -> datetime | None:
    if value is None:
        return None
    # Handle "2023-01-01T00:00:00Z" style
    value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


def parse_uuid(value: str | None) -> UUID | None:
    if value is None:
        return None
    return UUID(value)


def require_dt(value: str) -> datetime:
    """Parse a required datetime string (never None)."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def require_uuid(value: str) -> UUID:
    """Parse a required UUID string (never None)."""
    return UUID(value)


# A couple of simple enum-ish types as strings
ControlType = str  # "Stop" | "Shock" | "Vibrate" | "Sound"
ShockerModelType = str  # "CaiXianlin" | "PetTrainer" | "Petrainer998DR"
PermissionType = str  # "shockers.use" | "shockers.edit" | ...
RoleType = str  # "Support" | "Staff" | "Admin" | "System"


class PauseReason(IntFlag):
    """Bitfield for pause reasons. Values can be OR'd together."""

    NONE = 0
    SHOCKER = 1
    USER_SHARE = 2
    PUBLIC_SHARE = 4
