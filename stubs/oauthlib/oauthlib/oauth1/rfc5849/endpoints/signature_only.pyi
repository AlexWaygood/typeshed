"""
oauthlib.oauth1.rfc5849.endpoints.signature_only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of the signing logic of OAuth 1.0 RFC 5849.
"""

from logging import Logger

from .base import BaseEndpoint as BaseEndpoint

log: Logger

class SignatureOnlyEndpoint(BaseEndpoint):
    """An endpoint only responsible for verifying an oauth signature."""

    def validate_request(self, uri, http_method: str = "GET", body=None, headers=None):
        """Validate a signed OAuth request.

        :param uri: The full URI of the token request.
        :param http_method: A valid HTTP verb, i.e. GET, POST, PUT, HEAD, etc.
        :param body: The request body as a string.
        :param headers: The request headers as a dict.
        :returns: A tuple of 2 elements.
                  1. True if valid, False otherwise.
                  2. An oauthlib.common.Request object.
        """
