"""
oauthlib.oauth1.rfc5849.endpoints.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for signing and checking OAuth 1.0 RFC 5849 requests.
"""

from typing import Any

class BaseEndpoint:
    request_validator: Any
    token_generator: Any
    def __init__(self, request_validator, token_generator=None) -> None: ...
