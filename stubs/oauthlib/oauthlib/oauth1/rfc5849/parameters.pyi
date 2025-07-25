"""
oauthlib.parameters
~~~~~~~~~~~~~~~~~~~

This module contains methods related to `section 3.5`_ of the OAuth 1.0a spec.

.. _`section 3.5`: https://tools.ietf.org/html/rfc5849#section-3.5
"""

from _typeshed import Incomplete

def prepare_headers(params, headers: Incomplete | None = ..., realm: Incomplete | None = ...):
    """**Prepare the Authorization header.**
    Per `section 3.5.1`_ of the spec.

    Protocol parameters can be transmitted using the HTTP "Authorization"
    header field as defined by `RFC2617`_ with the auth-scheme name set to
    "OAuth" (case insensitive).

    For example::

        Authorization: OAuth realm="Example",
            oauth_consumer_key="0685bd9184jfhq22",
            oauth_token="ad180jjd733klru7",
            oauth_signature_method="HMAC-SHA1",
            oauth_signature="wOJIO9A2W5mFwDgiDvZbTSMK%2FPY%3D",
            oauth_timestamp="137131200",
            oauth_nonce="4572616e48616d6d65724c61686176",
            oauth_version="1.0"


    .. _`section 3.5.1`: https://tools.ietf.org/html/rfc5849#section-3.5.1
    .. _`RFC2617`: https://tools.ietf.org/html/rfc2617
    """

def prepare_form_encoded_body(oauth_params, body):
    """Prepare the Form-Encoded Body.

    Per `section 3.5.2`_ of the spec.

    .. _`section 3.5.2`: https://tools.ietf.org/html/rfc5849#section-3.5.2

    """

def prepare_request_uri_query(oauth_params, uri):
    """Prepare the Request URI Query.

    Per `section 3.5.3`_ of the spec.

    .. _`section 3.5.3`: https://tools.ietf.org/html/rfc5849#section-3.5.3

    """
