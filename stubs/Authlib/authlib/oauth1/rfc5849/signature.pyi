"""authlib.oauth1.rfc5849.signature.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module represents a direct implementation of `section 3.4`_ of the spec.

.. _`section 3.4`: https://tools.ietf.org/html/rfc5849#section-3.4
"""

SIGNATURE_HMAC_SHA1: str
SIGNATURE_RSA_SHA1: str
SIGNATURE_PLAINTEXT: str
SIGNATURE_TYPE_HEADER: str
SIGNATURE_TYPE_QUERY: str
SIGNATURE_TYPE_BODY: str

def construct_base_string(method, uri, params, host=None):
    """Generate signature base string from request, per `Section 3.4.1`_.

    For example, the HTTP request::

        POST /request?b5=%3D%253D&a3=a&c%40=&a2=r%20b HTTP/1.1
        Host: example.com
        Content-Type: application/x-www-form-urlencoded
        Authorization: OAuth realm="Example",
            oauth_consumer_key="9djdj82h48djs9d2",
            oauth_token="kkk9d7dh3k39sjv7",
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp="137131201",
            oauth_nonce="7d8f3e4a",
            oauth_signature="bYT5CMsGcbgUdFHObYMEfcx6bsw%3D"

        c2&a3=2+q

    is represented by the following signature base string (line breaks
    are for display purposes only)::

        POST&http%3A%2F%2Fexample.com%2Frequest&a2%3Dr%2520b%26a3%3D2%2520q
        %26a3%3Da%26b5%3D%253D%25253D%26c%2540%3D%26c2%3D%26oauth_consumer_
        key%3D9djdj82h48djs9d2%26oauth_nonce%3D7d8f3e4a%26oauth_signature_m
        ethod%3DHMAC-SHA1%26oauth_timestamp%3D137131201%26oauth_token%3Dkkk
        9d7dh3k39sjv7

    .. _`Section 3.4.1`: https://tools.ietf.org/html/rfc5849#section-3.4.1
    """

def normalize_base_string_uri(uri, host=None):
    """Normalize Base String URI per `Section 3.4.1.2`_.

    For example, the HTTP request::

        GET /r%20v/X?id=123 HTTP/1.1
        Host: EXAMPLE.COM:80

    is represented by the base string URI: "http://example.com/r%20v/X".

    In another example, the HTTPS request::

        GET /?q=1 HTTP/1.1
        Host: www.example.net:8080

    is represented by the base string URI: "https://www.example.net:8080/".

    .. _`Section 3.4.1.2`: https://tools.ietf.org/html/rfc5849#section-3.4.1.2

    The host argument overrides the netloc part of the uri argument.
    """

def normalize_parameters(params):
    """Normalize parameters per `Section 3.4.1.3.2`_.

    For example, the list of parameters from the previous section would
    be normalized as follows:

    Encoded::

    +------------------------+------------------+
    |          Name          |       Value      |
    +------------------------+------------------+
    |           b5           |     %3D%253D     |
    |           a3           |         a        |
    |          c%40          |                  |
    |           a2           |       r%20b      |
    |   oauth_consumer_key   | 9djdj82h48djs9d2 |
    |       oauth_token      | kkk9d7dh3k39sjv7 |
    | oauth_signature_method |     HMAC-SHA1    |
    |     oauth_timestamp    |     137131201    |
    |       oauth_nonce      |     7d8f3e4a     |
    |           c2           |                  |
    |           a3           |       2%20q      |
    +------------------------+------------------+

    Sorted::

    +------------------------+------------------+
    |          Name          |       Value      |
    +------------------------+------------------+
    |           a2           |       r%20b      |
    |           a3           |       2%20q      |
    |           a3           |         a        |
    |           b5           |     %3D%253D     |
    |          c%40          |                  |
    |           c2           |                  |
    |   oauth_consumer_key   | 9djdj82h48djs9d2 |
    |       oauth_nonce      |     7d8f3e4a     |
    | oauth_signature_method |     HMAC-SHA1    |
    |     oauth_timestamp    |     137131201    |
    |       oauth_token      | kkk9d7dh3k39sjv7 |
    +------------------------+------------------+

    Concatenated Pairs::

    +-------------------------------------+
    |              Name=Value             |
    +-------------------------------------+
    |               a2=r%20b              |
    |               a3=2%20q              |
    |                 a3=a                |
    |             b5=%3D%253D             |
    |                c%40=                |
    |                 c2=                 |
    | oauth_consumer_key=9djdj82h48djs9d2 |
    |         oauth_nonce=7d8f3e4a        |
    |   oauth_signature_method=HMAC-SHA1  |
    |      oauth_timestamp=137131201      |
    |     oauth_token=kkk9d7dh3k39sjv7    |
    +-------------------------------------+

    and concatenated together into a single string (line breaks are for
    display purposes only)::

        a2=r%20b&a3=2%20q&a3=a&b5=%3D%253D&c%40=&c2=&oauth_consumer_key=9dj
        dj82h48djs9d2&oauth_nonce=7d8f3e4a&oauth_signature_method=HMAC-SHA1
        &oauth_timestamp=137131201&oauth_token=kkk9d7dh3k39sjv7

    .. _`Section 3.4.1.3.2`: https://tools.ietf.org/html/rfc5849#section-3.4.1.3.2
    """

def generate_signature_base_string(request):
    """Generate signature base string from request."""

def hmac_sha1_signature(base_string, client_secret, token_secret):
    """Generate signature via HMAC-SHA1 method, per `Section 3.4.2`_.

    The "HMAC-SHA1" signature method uses the HMAC-SHA1 signature
    algorithm as defined in `RFC2104`_::

        digest = HMAC - SHA1(key, text)

    .. _`RFC2104`: https://tools.ietf.org/html/rfc2104
    .. _`Section 3.4.2`: https://tools.ietf.org/html/rfc5849#section-3.4.2
    """

def rsa_sha1_signature(base_string, rsa_private_key):
    """Generate signature via RSA-SHA1 method, per `Section 3.4.3`_.

    The "RSA-SHA1" signature method uses the RSASSA-PKCS1-v1_5 signature
    algorithm as defined in `RFC3447, Section 8.2`_ (also known as
    PKCS#1), using SHA-1 as the hash function for EMSA-PKCS1-v1_5.  To
    use this method, the client MUST have established client credentials
    with the server that included its RSA public key (in a manner that is
    beyond the scope of this specification).

    .. _`Section 3.4.3`: https://tools.ietf.org/html/rfc5849#section-3.4.3
    .. _`RFC3447, Section 8.2`: https://tools.ietf.org/html/rfc3447#section-8.2
    """

def plaintext_signature(client_secret, token_secret):
    """Generate signature via PLAINTEXT method, per `Section 3.4.4`_.

    The "PLAINTEXT" method does not employ a signature algorithm.  It
    MUST be used with a transport-layer mechanism such as TLS or SSL (or
    sent over a secure channel with equivalent protections).  It does not
    utilize the signature base string or the "oauth_timestamp" and
    "oauth_nonce" parameters.

    .. _`Section 3.4.4`: https://tools.ietf.org/html/rfc5849#section-3.4.4
    """

def sign_hmac_sha1(client, request):
    """Sign a HMAC-SHA1 signature."""

def sign_rsa_sha1(client, request):
    """Sign a RSASSA-PKCS #1 v1.5 base64 encoded signature."""

def sign_plaintext(client, request):
    """Sign a PLAINTEXT signature."""

def verify_hmac_sha1(request):
    """Verify a HMAC-SHA1 signature."""

def verify_rsa_sha1(request):
    """Verify a RSASSA-PKCS #1 v1.5 base64 encoded signature."""

def verify_plaintext(request):
    """Verify a PLAINTEXT signature."""
