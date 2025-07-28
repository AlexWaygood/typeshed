"""
requests.auth
~~~~~~~~~~~~~

This module contains the authentication handlers for Requests.
"""

from typing import Any

from . import cookies, models, utils

extract_cookies_to_jar = cookies.extract_cookies_to_jar
parse_dict_header = utils.parse_dict_header
to_native_string = utils.to_native_string

CONTENT_TYPE_FORM_URLENCODED: Any
CONTENT_TYPE_MULTI_PART: Any

def _basic_auth_str(username: bytes | str, password: bytes | str) -> str:
    """Returns a Basic Auth string."""

class AuthBase:
    """Base class that all auth implementations derive from"""

    def __call__(self, r: models.PreparedRequest) -> models.PreparedRequest: ...

class HTTPBasicAuth(AuthBase):
    """Attaches HTTP Basic Authentication to the given Request object."""

    username: bytes | str
    password: bytes | str
    def __init__(self, username: bytes | str, password: bytes | str) -> None: ...
    def __call__(self, r): ...

class HTTPProxyAuth(HTTPBasicAuth):
    """Attaches HTTP Proxy Authentication to a given Request object."""

    def __call__(self, r): ...

class HTTPDigestAuth(AuthBase):
    """Attaches HTTP Digest Authentication to the given Request object."""

    username: bytes | str
    password: bytes | str
    last_nonce: Any
    nonce_count: Any
    chal: Any
    pos: Any
    num_401_calls: Any
    def __init__(self, username: bytes | str, password: bytes | str) -> None: ...
    def build_digest_header(self, method, url):
        """
        :rtype: str
        """

    def handle_redirect(self, r, **kwargs):
        """Reset num_401_calls counter on redirects."""

    def handle_401(self, r, **kwargs):
        """
        Takes the given response and tries digest-auth, if needed.

        :rtype: requests.Response
        """

    def __call__(self, r): ...
    def init_per_thread_state(self) -> None: ...
