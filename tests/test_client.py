"""Tests for client construction and error handling."""

import pytest

from openshock import OpenShockClient, OpenShockHubClient
from openshock.exceptions import OpenShockApiError, OpenShockAuthError, OpenShockError, OpenShockNotFound


class TestClientConstruction:
    def test_api_token(self):
        client = OpenShockClient(api_token="test-token")
        assert client._auth is not None
        client.close()

    def test_hub_token(self):
        client = OpenShockHubClient(hub_token="test-token")
        assert client._auth is not None
        client.close()

    def test_no_auth_raises(self):
        with pytest.raises(ValueError, match="must provide"):
            OpenShockClient()

    def test_both_auth_raises(self):
        from openshock.auth import ApiTokenAuth

        with pytest.raises(ValueError, match="not both"):
            OpenShockClient(auth=ApiTokenAuth("x"), api_token="y")

    def test_context_manager(self):
        with OpenShockClient(api_token="test") as client:
            assert hasattr(client, "meta")
            assert hasattr(client, "account")
            assert hasattr(client, "devices")
            assert hasattr(client, "shockers")
            assert hasattr(client, "shares")
            assert hasattr(client, "sessions")
            assert hasattr(client, "user_shares")

    def test_hub_context_manager(self):
        with OpenShockHubClient(hub_token="test") as client:
            assert hasattr(client, "hub")
            assert hasattr(client, "meta")

    def test_custom_base_url(self):
        client = OpenShockClient(api_token="test", base_url="https://custom.api.example.com")
        assert "custom.api.example.com" in str(client._client.base_url)
        client.close()


class TestExceptionHierarchy:
    def test_auth_error_is_openshock_error(self):
        assert issubclass(OpenShockAuthError, OpenShockError)

    def test_not_found_is_openshock_error(self):
        assert issubclass(OpenShockNotFound, OpenShockError)

    def test_api_error_is_openshock_error(self):
        assert issubclass(OpenShockApiError, OpenShockError)
