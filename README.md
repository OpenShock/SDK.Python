# OpenShock Python SDK

[![CI](https://github.com/OpenShock/SDK.Python/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenShock/SDK.Python/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/openshock)](https://pypi.org/project/openshock/)
[![Python](https://img.shields.io/pypi/pyversions/openshock)](https://pypi.org/project/openshock/)
[![License](https://img.shields.io/github/license/OpenShock/SDK.Python)](LICENSE)

Python SDK for the [OpenShock](https://openshock.org) platform. Provides a typed REST API client with planned support for live WebSocket connections.

## Install

```bash
pip install openshock
```

## Quick start

```python
from openshock import OpenShockClient

client = OpenShockClient(api_token="your-api-token")

# Get backend info
info = client.meta.backend_info()
print(f"OpenShock {info.version}")

# List your shockers
shockers = client.shockers.list_own()

# Send a vibrate command
from openshock import Control

client.shockers.control([
    Control(id="shocker-uuid", type="Vibrate", intensity=50, duration=1000)
])

client.close()
```

Or use as a context manager:

```python
with OpenShockClient(api_token="your-api-token") as client:
    stats = client.meta.online_stats()
    print(f"Devices online: {stats.devices_online}")
```

## Resources

| Resource | Description | Example |
|----------|-------------|---------|
| `client.meta` | Backend info and stats | `client.meta.backend_info()` |
| `client.account` | User info and API tokens | `client.account.user_self()` |
| `client.devices` | Hub (device) management | `client.devices.list()` |
| `client.shockers` | Shocker CRUD, control, logs | `client.shockers.control(...)` |
| `client.shares` | Public share links and codes | `client.shares.list_public()` |
| `client.user_shares` | User-to-user shares (V2) | `client.user_shares.get()` |
| `client.sessions` | Login session management | `client.sessions.list()` |

For hub/device endpoints, use `OpenShockHubClient`:

```python
from openshock import OpenShockHubClient

hub = OpenShockHubClient(hub_token="device-token")
lcg = hub.hub.assign_lcg()
print(f"Connect to {lcg.host}:{lcg.port}")
```

## Authentication

Two client types for two auth schemes:

- **`OpenShockClient(api_token=...)`** — User API token (`OpenShockToken` header)
- **`OpenShockHubClient(hub_token=...)`** — Device token (`DeviceToken` header)

Create API tokens at [openshock.app](https://openshock.app) under Settings > API Tokens.

## Typed models

All responses are parsed into typed dataclasses:

```python
from openshock import (
    BackendInfo, Stats, User, Token, Device, Shocker,
    ShockerPermissions, ShockerLimits, ShockerLog, Control,
    Session, PublicShare, UserShares, ShareInvite, PauseReason,
)
```

## Self-hosting

To connect to a self-hosted instance:

```python
client = OpenShockClient(
    api_token="your-token",
    base_url="https://api.your-instance.com",
)
```

## Development

```bash
git clone https://github.com/OpenShock/SDK.Python.git
cd SDK.Python
pip install -e ".[dev]"

# Format
ruff format .

# Lint
ruff check .

# Type check
mypy openshock/

# Test
pytest
```

## License

[MIT](LICENSE)
