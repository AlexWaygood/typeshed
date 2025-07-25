"""
oauthlib.utils
~~~~~~~~~~~~~~

This module contains utility methods used by various parts of the OAuth 2 spec.
"""

import datetime
from typing import overload

@overload
def list_to_scope(scope: None) -> None:
    """Convert a list of scopes to a space separated string."""

@overload
def list_to_scope(scope: str | set[object] | tuple[object] | list[object]) -> str: ...
@overload
def scope_to_list(scope: None) -> None:
    """Convert a space separated string to a list of scopes."""

@overload
def scope_to_list(scope: str | set[object] | tuple[object] | list[object]) -> list[str]: ...
def params_from_uri(uri: str) -> dict[str, str | list[str]]: ...
def host_from_uri(uri: str) -> tuple[str, str | None]:
    """Extract hostname and port from URI.

    Will use default port for HTTP and HTTPS if none is present in the URI.
    """

def escape(u: str) -> str:
    """Escape a string in an OAuth-compatible fashion.

    TODO: verify whether this can in fact be used for OAuth 2

    """

def generate_age(issue_time: datetime.datetime | datetime.timedelta) -> str:
    """Generate a age parameter for MAC authentication draft 00."""

def is_secure_transport(uri: str) -> bool:
    """Check if the uri is over ssl."""
