"""
oauthlib.oauth1.rfc5849.errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error used both by OAuth 1 clients and provicers to represent the spec
defined error responses for all four core grant types.
"""

from typing import Any

class OAuth1Error(Exception):
    error: Any
    description: str
    uri: Any
    status_code: Any
    def __init__(self, description=None, uri=None, status_code: int = 400, request=None) -> None:
        """
        description:    A human-readable ASCII [USASCII] text providing
                        additional information, used to assist the client
                        developer in understanding the error that occurred.
                        Values for the "error_description" parameter MUST NOT
                        include characters outside the set
                        x20-21 / x23-5B / x5D-7E.

        uri:    A URI identifying a human-readable web page with information
                about the error, used to provide the client developer with
                additional information about the error.  Values for the
                "error_uri" parameter MUST conform to the URI- Reference
                syntax, and thus MUST NOT include characters outside the set
                x21 / x23-5B / x5D-7E.

        state:  A CSRF protection value received from the client.

        request:  Oauthlib Request object
        """

    def in_uri(self, uri): ...
    @property
    def twotuples(self): ...
    @property
    def urlencoded(self): ...

class InsecureTransportError(OAuth1Error):
    error: str
    description: str

class InvalidSignatureMethodError(OAuth1Error):
    error: str

class InvalidRequestError(OAuth1Error):
    error: str

class InvalidClientError(OAuth1Error):
    error: str
