"""Tests for model parsing (from_dict / to_dict)."""

from datetime import datetime
from uuid import UUID

from openshock.models import (
    BackendInfo,
    Control,
    Device,
    DeviceWithToken,
    LcgNodeV2,
    PauseReason,
    Session,
    ShareInviteShocker,
    Shocker,
    ShockerLimits,
    ShockerLog,
    ShockerPermissions,
    Stats,
    Token,
    User,
    UserShares,
)


class TestBackendInfo:
    def test_from_any(self):
        data = {
            "version": "3.15.0",
            "commit": "abc123",
            "currentTime": "2024-06-01T12:00:00Z",
            "frontendUrl": "https://openshock.app",
            "shortLinkUrl": "https://os.link",
            "turnstileSiteKey": "key123",
            "isUserAuthenticated": True,
            "oAuthProviders": ["discord"],
        }
        info = BackendInfo.from_any(data)
        assert info.version == "3.15.0"
        assert info.commit == "abc123"
        assert info.is_user_authenticated is True
        assert info.o_auth_providers == ["discord"]
        assert isinstance(info.current_time, datetime)


class TestStats:
    def test_from_any(self):
        stats = Stats.from_any({"devicesOnline": 42})
        assert stats.devices_online == 42


class TestUser:
    def test_from_dict(self):
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "testuser",
            "email": "test@example.com",
            "image": "https://example.com/img.png",
            "roles": ["Admin"],
            "rank": "1",
        }
        user = User.from_dict(data)
        assert user.name == "testuser"
        assert isinstance(user.id, UUID)
        assert user.roles == ["Admin"]


class TestToken:
    def test_from_dict(self):
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "my-token",
            "createdOn": "2024-01-01T00:00:00Z",
            "validUntil": None,
            "lastUsed": "2024-06-01T00:00:00Z",
            "permissions": ["shockers.use"],
        }
        token = Token.from_dict(data)
        assert token.name == "my-token"
        assert token.valid_until is None
        assert isinstance(token.last_used, datetime)


class TestDevice:
    def test_from_dict(self):
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "My Hub",
            "createdOn": "2024-01-01T00:00:00Z",
        }
        device = Device.from_dict(data)
        assert device.name == "My Hub"
        assert isinstance(device.id, UUID)

    def test_with_token(self):
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "New Hub",
            "createdOn": "2024-01-01T00:00:00Z",
            "token": "secret-token-123",
        }
        dt = DeviceWithToken.from_dict(data)
        assert dt.token == "secret-token-123"


class TestShocker:
    def test_from_dict(self):
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Test Shocker",
            "rfId": 12345,
            "model": "CaiXianlin",
            "createdOn": "2024-01-01T00:00:00Z",
            "isPaused": True,
        }
        shocker = Shocker.from_dict(data)
        assert shocker.name == "Test Shocker"
        assert shocker.rf_id == 12345
        assert shocker.is_paused is True


class TestShockerPermissions:
    def test_round_trip(self):
        perms = ShockerPermissions(vibrate=True, sound=True, shock=False, live=False)
        d = perms.to_dict()
        assert d == {"vibrate": True, "sound": True, "shock": False, "live": False}
        restored = ShockerPermissions.from_dict(d)
        assert restored == perms


class TestShockerLimits:
    def test_round_trip(self):
        limits = ShockerLimits(intensity=80, duration=5000)
        d = limits.to_dict()
        restored = ShockerLimits.from_dict(d)
        assert restored == limits


class TestControl:
    def test_to_dict(self):
        ctrl = Control(
            id="550e8400-e29b-41d4-a716-446655440000",
            type="Vibrate",
            intensity=50,
            duration=1000,
        )
        d = ctrl.to_dict()
        assert d["type"] == "Vibrate"
        assert d["intensity"] == 50
        assert d["exclusive"] is False


class TestShockerLog:
    def test_from_dict(self):
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdOn": "2024-06-01T12:00:00Z",
            "type": "Shock",
            "controlledBy": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "name": "user1",
                "image": "https://example.com/img.png",
                "customName": None,
            },
            "intensity": 75,
            "duration": 2000,
        }
        log = ShockerLog.from_dict(data)
        assert log.type == "Shock"
        assert log.intensity == 75
        assert log.controlled_by.name == "user1"


class TestSession:
    def test_from_dict(self):
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "ip": "192.168.1.1",
            "userAgent": "Mozilla/5.0",
            "created": "2024-01-01T00:00:00Z",
            "expires": "2024-02-01T00:00:00Z",
            "lastUsed": "2024-01-15T00:00:00Z",
        }
        session = Session.from_dict(data)
        assert session.ip == "192.168.1.1"
        assert isinstance(session.expires, datetime)


class TestPauseReason:
    def test_bitfield(self):
        reason = PauseReason.SHOCKER | PauseReason.USER_SHARE
        assert reason & PauseReason.SHOCKER
        assert reason & PauseReason.USER_SHARE
        assert not (reason & PauseReason.PUBLIC_SHARE)

    def test_from_int(self):
        reason = PauseReason(6)  # USER_SHARE | PUBLIC_SHARE
        assert reason & PauseReason.USER_SHARE
        assert reason & PauseReason.PUBLIC_SHARE


class TestLcgNodeV2:
    def test_from_dict(self):
        data = {"host": "gw.example.com", "port": 443, "path": "/ws", "country": "DE"}
        node = LcgNodeV2.from_dict(data)
        assert node.host == "gw.example.com"
        assert node.port == 443


class TestUserShares:
    def test_from_dict(self):
        data = {
            "outgoing": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "user2",
                    "image": "https://example.com/img.png",
                    "shares": [
                        {
                            "id": "660e8400-e29b-41d4-a716-446655440000",
                            "name": "Shocker 1",
                            "createdOn": "2024-01-01T00:00:00Z",
                            "permissions": {"vibrate": True, "sound": True, "shock": False},
                            "limits": {"intensity": 80, "duration": 5000},
                            "paused": 0,
                        }
                    ],
                }
            ],
            "incoming": [],
        }
        shares = UserShares.from_dict(data)
        assert len(shares.outgoing) == 1
        assert len(shares.incoming) == 0
        assert shares.outgoing[0].shares[0].name == "Shocker 1"


class TestShareInviteShocker:
    def test_round_trip(self):
        s = ShareInviteShocker(
            permissions=ShockerPermissions(vibrate=True, sound=False, shock=False),
            limits=ShockerLimits(intensity=50, duration=3000),
            id=UUID("550e8400-e29b-41d4-a716-446655440000"),
        )
        d = s.to_dict()
        assert "permissions" in d
        assert d["id"] == "550e8400-e29b-41d4-a716-446655440000"
