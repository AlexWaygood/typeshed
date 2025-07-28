"""
This module is an implementation of `section 3.4`_ of RFC 5849.

**Usage**

Steps for signing a request:

1. Collect parameters from the request using ``collect_parameters``.
2. Normalize those parameters using ``normalize_parameters``.
3. Create the *base string URI* using ``base_string_uri``.
4. Create the *signature base string* from the above three components
   using ``signature_base_string``.
5. Pass the *signature base string* and the client credentials to one of the
   sign-with-client functions. The HMAC-based signing functions needs
   client credentials with secrets. The RSA-based signing functions needs
   client credentials with an RSA private key.

To verify a request, pass the request and credentials to one of the verify
functions. The HMAC-based signing functions needs the shared secrets. The
RSA-based verify functions needs the RSA public key.

**Scope**

All of the functions in this module should be considered internal to OAuthLib,
since they are not imported into the "oauthlib.oauth1" module. Programs using
OAuthLib should not use directly invoke any of the functions in this module.

**Deprecated functions**

The "sign_" methods that are not "_with_client" have been deprecated. They may
be removed in a future release. Since they are all internal functions, this
should have no impact on properly behaving programs.

.. _`section 3.4`: https://tools.ietf.org/html/rfc5849#section-3.4
"""

from _typeshed import Unused
from collections.abc import Iterable
from logging import Logger

from oauthlib.common import Request, _HTTPMethod

log: Logger

def signature_base_string(http_method: _HTTPMethod, base_str_uri: str, normalized_encoded_request_parameters: str) -> str:
    """
    Construct the signature base string.

    The *signature base string* is the value that is calculated and signed by
    the client. It is also independently calculated by the server to verify
    the signature, and therefore must produce the exact same value at both
    ends or the signature won't verify.

    The rules for calculating the *signature base string* are defined in
    section 3.4.1.1`_ of RFC 5849.

    .. _`section 3.4.1.1`: https://tools.ietf.org/html/rfc5849#section-3.4.1.1
    """

def base_string_uri(uri: str, host: str | None = None) -> str:
    """
    Calculates the _base string URI_.

    The *base string URI* is one of the components that make up the
     *signature base string*.

    The ``host`` is optional. If provided, it is used to override any host and
    port values in the ``uri``. The value for ``host`` is usually extracted from
    the "Host" request header from the HTTP request. Its value may be just the
    hostname, or the hostname followed by a colon and a TCP/IP port number
    (hostname:port). If a value for the``host`` is provided but it does not
    contain a port number, the default port number is used (i.e. if the ``uri``
    contained a port number, it will be discarded).

    The rules for calculating the *base string URI* are defined in
    section 3.4.1.2`_ of RFC 5849.

    .. _`section 3.4.1.2`: https://tools.ietf.org/html/rfc5849#section-3.4.1.2

    :param uri: URI
    :param host: hostname with optional port number, separated by a colon
    :return: base string URI
    """

def collect_parameters(
    uri_query: str = "",
    body: str | bytes | dict[str, str] | Iterable[tuple[str, str]] | None = None,
    headers: dict[str, str] | None = None,
    exclude_oauth_signature: bool = True,
    with_realm: bool = False,
) -> list[tuple[str, str]]:
    """
    Gather the request parameters from all the parameter sources.

    This function is used to extract all the parameters, which are then passed
    to ``normalize_parameters`` to produce one of the components that make up
    the *signature base string*.

    Parameters starting with `oauth_` will be unescaped.

    Body parameters must be supplied as a dict, a list of 2-tuples, or a
    form encoded query string.

    Headers must be supplied as a dict.

    The rules where the parameters must be sourced from are defined in
    `section 3.4.1.3.1`_ of RFC 5849.

    .. _`Sec 3.4.1.3.1`: https://tools.ietf.org/html/rfc5849#section-3.4.1.3.1
    """

def normalize_parameters(params: dict[str, str]) -> str:
    """
    Calculate the normalized request parameters.

    The *normalized request parameters* is one of the components that make up
    the *signature base string*.

    The rules for parameter normalization are defined in `section 3.4.1.3.2`_ of
    RFC 5849.

    .. _`Sec 3.4.1.3.2`: https://tools.ietf.org/html/rfc5849#section-3.4.1.3.2
    """

def sign_hmac_sha1_with_client(sig_base_str: str, client): ...
def verify_hmac_sha1(request: Request, client_secret=None, resource_owner_secret=None) -> bool: ...
def sign_hmac_sha1(base_string: str | bytes, client_secret, resource_owner_secret):
    """
    Deprecated function for calculating a HMAC-SHA1 signature.

    This function has been replaced by invoking ``sign_hmac`` with "SHA-1"
    as the hash algorithm name.

    This function was invoked by sign_hmac_sha1_with_client and
    test_signatures.py, but does any application invoke it directly? If not,
    it can be removed.
    """

def sign_hmac_sha256_with_client(sig_base_str, client): ...
def verify_hmac_sha256(request, client_secret=None, resource_owner_secret=None) -> bool: ...
def sign_hmac_sha256(base_string: str | bytes, client_secret, resource_owner_secret):
    """
    Deprecated function for calculating a HMAC-SHA256 signature.

    This function has been replaced by invoking ``sign_hmac`` with "SHA-256"
    as the hash algorithm name.

    This function was invoked by sign_hmac_sha256_with_client and
    test_signatures.py, but does any application invoke it directly? If not,
    it can be removed.
    """

def sign_hmac_sha512_with_client(sig_base_str: str, client): ...
def verify_hmac_sha512(request, client_secret: str | None = None, resource_owner_secret: str | None = None) -> bool: ...
def sign_rsa_sha1_with_client(sig_base_str: str | bytes, client): ...
def verify_rsa_sha1(request, rsa_public_key: str) -> bool: ...
def sign_rsa_sha1(base_string, rsa_private_key):
    """
    Deprecated function for calculating a RSA-SHA1 signature.

    This function has been replaced by invoking ``sign_rsa`` with "SHA-1"
    as the hash algorithm name.

    This function was invoked by sign_rsa_sha1_with_client and
    test_signatures.py, but does any application invoke it directly? If not,
    it can be removed.
    """

def sign_rsa_sha256_with_client(sig_base_str: str, client): ...
def verify_rsa_sha256(request, rsa_public_key: str) -> bool: ...
def sign_rsa_sha512_with_client(sig_base_str: str, client): ...
def verify_rsa_sha512(request, rsa_public_key: str) -> bool: ...
def sign_plaintext_with_client(_signature_base_string: Unused, client) -> str: ...
def sign_plaintext(client_secret: str | None, resource_owner_secret: str | None) -> str:
    """Sign a request using plaintext.

    Per `section 3.4.4`_ of the spec.

    The "PLAINTEXT" method does not employ a signature algorithm.  It
    MUST be used with a transport-layer mechanism such as TLS or SSL (or
    sent over a secure channel with equivalent protections).  It does not
    utilize the signature base string or the "oauth_timestamp" and
    "oauth_nonce" parameters.

    .. _`section 3.4.4`: https://tools.ietf.org/html/rfc5849#section-3.4.4

    """

def verify_plaintext(request, client_secret: str | None = None, resource_owner_secret: str | None = None) -> bool:
    """Verify a PLAINTEXT signature.

    Per `section 3.4`_ of the spec.

    .. _`section 3.4`: https://tools.ietf.org/html/rfc5849#section-3.4
    """
