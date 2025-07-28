"""authlib.spec.rfc5849.parameters.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains methods related to `section 3.5`_ of the OAuth 1.0a spec.

.. _`section 3.5`: https://tools.ietf.org/html/rfc5849#section-3.5
"""

def prepare_headers(oauth_params, headers=None, realm=None):
    """**Prepare the Authorization header.**
    Per `section 3.5.1`_ of the spec.

    Protocol parameters can be transmitted using the HTTP "Authorization"
    header field as defined by `RFC2617`_ with the auth-scheme name set to
    "OAuth" (case insensitive).

    For example::

        Authorization: OAuth realm="Photos",
            oauth_consumer_key="dpf43f3p2l4k3l03",
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp="137131200",
            oauth_nonce="wIjqoS",
            oauth_callback="http%3A%2F%2Fprinter.example.com%2Fready",
            oauth_signature="74KNZJeDHnMBp0EMJ9ZHt%2FXKycU%3D",
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
