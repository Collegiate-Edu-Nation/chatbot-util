# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Authentication helpers for deployments behind a trusted reverse proxy."""

import os
import re
from dataclasses import dataclass

import fastapi
import fastapi.responses
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

PROXY_AUTH_ENV = "CHATBOT_UTIL_PROXY_AUTH"
AUTH_HEADER_ENV = "CHATBOT_UTIL_AUTH_HEADER"
DEFAULT_AUTH_HEADER = "X-Authenticated-User"

# A custom header makes browser form submissions insufficient to invoke mutating
# endpoints. Production does not enable cross-origin requests, so a foreign origin
# cannot add this header without a successful CORS preflight.
APPLICATION_REQUEST_HEADER = "X-Chatbot-Util-Request"
APPLICATION_REQUEST_VALUE = "1"

_HEADER_NAME = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
_IDENTITY = re.compile(r"^[^\x00-\x20\x7f,]{1,320}$")


def _boolean_environment(name: str, default: bool = False) -> bool:
    """Read a strict boolean environment variable."""
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().casefold()
    if normalized in {"1", "true"}:
        return True
    if normalized in {"0", "false"}:
        return False
    raise RuntimeError(f"{name} must be one of: true, false, 1, 0")


@dataclass(frozen=True)
class ProxyAuthConfig:
    """Trusted reverse-proxy authentication settings."""

    enabled: bool = False
    user_header: str = DEFAULT_AUTH_HEADER

    def __post_init__(self) -> None:
        if _HEADER_NAME.fullmatch(self.user_header) is None:
            raise ValueError(
                f"Invalid HTTP authentication header: {self.user_header!r}"
            )

    @classmethod
    def from_environment(cls) -> "ProxyAuthConfig":
        """Resolve proxy authentication settings from the environment."""
        return cls(
            enabled=_boolean_environment(PROXY_AUTH_ENV),
            user_header=os.getenv(AUTH_HEADER_ENV, DEFAULT_AUTH_HEADER),
        )


class ProxyAuthenticationMiddleware(BaseHTTPMiddleware):
    """Reject requests that lack an identity asserted by the trusted proxy."""

    def __init__(self, app: ASGIApp, config: ProxyAuthConfig) -> None:
        super().__init__(app)
        self.config = config

    async def dispatch(
        self,
        request: fastapi.Request,
        call_next: RequestResponseEndpoint,
    ) -> fastapi.Response:
        identity: str | None = None

        if self.config.enabled:
            candidates = request.headers.getlist(self.config.user_header)
            candidate = candidates[0] if len(candidates) == 1 else None
            if candidate is None or _IDENTITY.fullmatch(candidate) is None:
                return fastapi.responses.JSONResponse(
                    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authentication required"},
                    headers={"Cache-Control": "no-store"},
                )
            identity = candidate

        # Headers are ignored when proxy auth is disabled, so local callers cannot
        # accidentally become authenticated merely by supplying one.
        request.state.authenticated_user = identity
        return await call_next(request)


def authenticated_user(request: fastapi.Request) -> str | None:
    """Return the proxy-authenticated identity attached to a request."""
    identity = getattr(request.state, "authenticated_user", None)
    return identity if isinstance(identity, str) else None


def request_actor(request: fastapi.Request) -> str:
    """Return an audit-friendly actor for authenticated and local operation."""
    return authenticated_user(request) or "local-user"


def require_application_request(request: fastapi.Request) -> None:
    """Require the frontend's non-simple marker on state-changing requests."""
    if request.headers.get(APPLICATION_REQUEST_HEADER) != APPLICATION_REQUEST_VALUE:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Missing application request marker",
        )
