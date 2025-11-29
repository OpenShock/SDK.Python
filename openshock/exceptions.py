class OpenShockError(Exception):
    """Base error for OpenShock client."""


class OpenShockAuthError(OpenShockError):
    """Authentication / authorization failed (401/403)."""


class OpenShockNotFound(OpenShockError):
    """Resource not found (404)."""


class OpenShockApiError(OpenShockError):
    """Unexpected non-2xx response."""
