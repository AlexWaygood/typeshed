from _typeshed import sentinel
from _typeshed.wsgi import WSGIEnvironment
from collections.abc import Collection, ItemsView, Iterator, KeysView, MutableMapping, ValuesView
from datetime import date, datetime, timedelta
from time import _TimeTuple, struct_time
from typing import Any, Literal, Protocol, TypeVar, overload
from typing_extensions import TypeAlias

from webob._types import AsymmetricProperty
from webob.request import BaseRequest
from webob.response import Response

__all__ = [
    "Cookie",
    "CookieProfile",
    "SignedCookieProfile",
    "SignedSerializer",
    "JSONSerializer",
    "Base64Serializer",
    "make_cookie",
]

_T = TypeVar("_T")
# we accept both the official spelling and the one used in the WebOb docs
# the implementation compares after lower() so technically there are more
# valid spellings, but it seems more natural to support these two spellings
_SameSitePolicy: TypeAlias = Literal["Strict", "Lax", "None", "strict", "lax", "none"]

class _Serializer(Protocol):
    def dumps(self, appstruct: Any, /) -> bytes: ...
    def loads(self, bstruct: bytes, /) -> Any: ...

class RequestCookies(MutableMapping[str, str]):
    def __init__(self, environ: WSGIEnvironment) -> None: ...
    def __setitem__(self, name: str, value: str) -> None: ...
    def __getitem__(self, name: str) -> str: ...
    @overload
    def get(self, name: str, default: None = None) -> str | None: ...
    @overload
    def get(self, name: str, default: str) -> str: ...
    @overload
    def get(self, name: str, default: _T) -> str | _T: ...
    def __delitem__(self, name: str) -> None: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> ValuesView[str]: ...
    def items(self) -> ItemsView[str, str]: ...
    def __contains__(self, name: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def clear(self) -> None: ...

class Cookie(dict[bytes, Morsel]):
    def __init__(self, input: str | None = None) -> None: ...
    def load(self, data: str) -> None: ...
    def add(self, key: str | bytes, val: str | bytes) -> Morsel | dict[bytes, bytes]: ...
    def __setitem__(self, key: str | bytes, val: str | bytes) -> Morsel | dict[bytes, bytes]: ...  # type: ignore[override]
    def serialize(self, full: bool = True) -> str: ...
    def values(self) -> list[Morsel]: ...  # type: ignore[override]
    def __str__(self, full: bool = True) -> str: ...

class Morsel(dict[bytes, bytes | bool | None]):
    name: bytes
    value: bytes
    def __init__(self, name: str | bytes, value: str | bytes) -> None: ...
    @property
    def path(self) -> bytes | None: ...
    @path.setter
    def path(self, v: bytes | None) -> None: ...
    @property
    def domain(self) -> bytes | None: ...
    @domain.setter
    def domain(self, v: bytes | None) -> None: ...
    @property
    def comment(self) -> bytes | None: ...
    @comment.setter
    def comment(self, v: bytes | None) -> None: ...
    expires: AsymmetricProperty[bytes | None, datetime | date | timedelta | _TimeTuple | struct_time | int | str | bytes | None]
    max_age: AsymmetricProperty[bytes | None, timedelta | int | str | bytes | None]
    httponly: AsymmetricProperty[bool, bool | None]
    secure: AsymmetricProperty[bool, bool | None]
    samesite: AsymmetricProperty[bytes, _SameSitePolicy | bytes]
    def __setitem__(self, k: str | bytes, v: bytes | bool | None) -> None: ...
    def serialize(self, full: bool = True) -> str: ...
    def __str__(self, full: bool = True) -> str: ...

def make_cookie(
    name: str | bytes,
    value: str | bytes | None,
    max_age: int | timedelta | None = None,
    path: str = "/",
    domain: str | None = None,
    secure: bool | None = False,
    httponly: bool | None = False,
    comment: str | None = None,
    samesite: _SameSitePolicy | None = None,
) -> str:
    """
    Generate a cookie value.

    ``name``
      The name of the cookie.

    ``value``
      The ``value`` of the cookie. If it is ``None``, it will generate a cookie
      value with an expiration date in the past.

    ``max_age``
      The maximum age of the cookie used for sessioning (in seconds).
      Default: ``None`` (browser scope).

    ``path``
      The path used for the session cookie. Default: ``/``.

    ``domain``
      The domain used for the session cookie. Default: ``None`` (no domain).

    ``secure``
      The 'secure' flag of the session cookie. Default: ``False``.

    ``httponly``
      Hide the cookie from JavaScript by setting the 'HttpOnly' flag of the
      session cookie. Default: ``False``.

    ``comment``
      Set a comment on the cookie. Default: ``None``

    ``samesite``
      The 'SameSite' attribute of the cookie, can be either ``"strict"``,
      ``"lax"``, ``"none"``, or ``None``. By default, WebOb will validate the
      value to ensure it conforms to the allowable options in the various draft
      RFC's that exist.

      To disable this check and send headers that are experimental or introduced
      in a future RFC, set the module flag ``SAMESITE_VALIDATION`` to a
      false value like:

      .. code::

          import webob.cookies
          webob.cookies.SAMESITE_VALIDATION = False

          ck = webob.cookies.make_cookie(cookie_name, value, samesite='future')

      .. danger::

          This feature has known compatibility issues with various user agents,
          and is not yet an accepted RFC. It is therefore considered
          experimental and subject to change.

          For more information please see :ref:`Experimental: SameSite Cookies
          <samesiteexp>`
    """

class JSONSerializer:
    """A serializer which uses `json.dumps`` and ``json.loads``"""

    def dumps(self, appstruct: Any) -> bytes: ...
    def loads(self, bstruct: bytes | str) -> Any: ...

class Base64Serializer:
    """A serializer which uses base64 to encode/decode data"""

    serializer: _Serializer
    def __init__(self, serializer: _Serializer | None = None) -> None: ...
    def dumps(self, appstruct: Any) -> bytes:
        """
        Given an ``appstruct``, serialize and sign the data.

        Returns a bytestring.
        """

    def loads(self, bstruct: bytes) -> Any:
        """
        Given a ``bstruct`` (a bytestring), verify the signature and then
        deserialize and return the deserialized value.

        A ``ValueError`` will be raised if the signature fails to validate.
        """

class SignedSerializer:
    """
    A helper to cryptographically sign arbitrary content using HMAC.

    The serializer accepts arbitrary functions for performing the actual
    serialization and deserialization.

    ``secret``
      A string which is used to sign the cookie. The secret should be at
      least as long as the block size of the selected hash algorithm. For
      ``sha512`` this would mean a 512 bit (64 character) secret.

    ``salt``
      A namespace to avoid collisions between different uses of a shared
      secret.

    ``hashalg``
      The HMAC digest algorithm to use for signing. The algorithm must be
      supported by the :mod:`hashlib` library. Default: ``'sha512'``.

    ``serializer``
      An object with two methods: `loads`` and ``dumps``.  The ``loads`` method
      should accept bytes and return a Python object.  The ``dumps`` method
      should accept a Python object and return bytes.  A ``ValueError`` should
      be raised for malformed inputs.  Default: ``None`, which will use a
      derivation of :func:`json.dumps` and ``json.loads``.

    """

    salt: str | bytes
    secret: str | bytes
    hashalg: str
    salted_secret: bytes
    digest_size: int
    serializer: _Serializer
    def __init__(
        self, secret: str | bytes, salt: str | bytes, hashalg: str = "sha512", serializer: _Serializer | None = None
    ) -> None: ...
    def dumps(self, appstruct: Any) -> bytes:
        """
        Given an ``appstruct``, serialize and sign the data.

        Returns a bytestring.
        """

    def loads(self, bstruct: bytes) -> Any:
        """
        Given a ``bstruct`` (a bytestring), verify the signature and then
        deserialize and return the deserialized value.

        A ``ValueError`` will be raised if the signature fails to validate.
        """

class CookieProfile:
    """
    A helper class that helps bring some sanity to the insanity that is cookie
    handling.

    The helper is capable of generating multiple cookies if necessary to
    support subdomains and parent domains.

    ``cookie_name``
      The name of the cookie used for sessioning. Default: ``'session'``.

    ``max_age``
      The maximum age of the cookie used for sessioning (in seconds).
      Default: ``None`` (browser scope).

    ``secure``
      The 'secure' flag of the session cookie. Default: ``False``.

    ``httponly``
      Hide the cookie from Javascript by setting the 'HttpOnly' flag of the
      session cookie. Default: ``False``.

    ``samesite``
      The 'SameSite' attribute of the cookie, can be either ``b"strict"``,
      ``b"lax"``, ``b"none"``, or ``None``.

      For more information please see the ``samesite`` documentation in
      :meth:`webob.cookies.make_cookie`

    ``path``
      The path used for the session cookie. Default: ``'/'``.

    ``domains``
      The domain(s) used for the session cookie. Default: ``None`` (no domain).
      Can be passed an iterable containing multiple domains, this will set
      multiple cookies one for each domain.

    ``serializer``
      An object with two methods: ``loads`` and ``dumps``.  The ``loads`` method
      should accept a bytestring and return a Python object.  The ``dumps``
      method should accept a Python object and return bytes.  A ``ValueError``
      should be raised for malformed inputs.  Default: ``None``, which will use
      a derivation of :func:`json.dumps` and :func:`json.loads`.

    """

    cookie_name: str
    secure: bool
    max_age: int | timedelta | None
    httponly: bool | None
    samesite: _SameSitePolicy | None
    path: str
    domains: Collection[str] | None
    serializer: _Serializer
    request: BaseRequest | None
    def __init__(
        self,
        cookie_name: str,
        secure: bool = False,
        max_age: int | timedelta | None = None,
        httponly: bool | None = None,
        samesite: _SameSitePolicy | None = None,
        path: str = "/",
        # even though the docs claim any iterable is fine, that is
        # clearly not the case judging by the implementation
        domains: Collection[str] | None = None,
        serializer: _Serializer | None = None,
    ) -> None: ...
    def __call__(self, request: BaseRequest) -> CookieProfile:
        """Bind a request to a copy of this instance and return it"""

    def bind(self, request: BaseRequest) -> CookieProfile:
        """Bind a request to a copy of this instance and return it"""

    def get_value(self) -> Any | None:
        """Looks for a cookie by name in the currently bound request, and
        returns its value.  If the cookie profile is not bound to a request,
        this method will raise a :exc:`ValueError`.

        Looks for the cookie in the cookies jar, and if it can find it it will
        attempt to deserialize it.  Returns ``None`` if there is no cookie or
        if the value in the cookie cannot be successfully deserialized.
        """

    def set_cookies(
        self,
        response: Response,
        value: Any,
        domains: Collection[str] = sentinel,
        max_age: int | timedelta | None = sentinel,
        path: str = sentinel,
        secure: bool = sentinel,
        httponly: bool = sentinel,
        samesite: _SameSitePolicy | None = sentinel,
    ) -> Response:
        """Set the cookies on a response."""

    def get_headers(
        self,
        value: Any,
        domains: Collection[str] = sentinel,
        max_age: int | timedelta | None = sentinel,
        path: str = sentinel,
        secure: bool = sentinel,
        httponly: bool = sentinel,
        samesite: _SameSitePolicy | None = sentinel,
    ) -> list[tuple[str, str]]:
        """Retrieve raw headers for setting cookies.

        Returns a list of headers that should be set for the cookies to
        be correctly tracked.
        """

class SignedCookieProfile(CookieProfile):
    """
    A helper for generating cookies that are signed to prevent tampering.

    By default this will create a single cookie, given a value it will
    serialize it, then use HMAC to cryptographically sign the data. Finally
    the result is base64-encoded for transport. This way a remote user can
    not tamper with the value without uncovering the secret/salt used.

    ``secret``
      A string which is used to sign the cookie. The secret should be at
      least as long as the block size of the selected hash algorithm. For
      ``sha512`` this would mean a 512 bit (64 character) secret.

    ``salt``
      A namespace to avoid collisions between different uses of a shared
      secret.

    ``hashalg``
      The HMAC digest algorithm to use for signing. The algorithm must be
      supported by the :mod:`hashlib` library. Default: ``'sha512'``.

    ``cookie_name``
      The name of the cookie used for sessioning. Default: ``'session'``.

    ``max_age``
      The maximum age of the cookie used for sessioning (in seconds).
      Default: ``None`` (browser scope).

    ``secure``
      The 'secure' flag of the session cookie. Default: ``False``.

    ``httponly``
      Hide the cookie from Javascript by setting the 'HttpOnly' flag of the
      session cookie. Default: ``False``.

    ``samesite``
      The 'SameSite' attribute of the cookie, can be either ``b"strict"``,
      ``b"lax"``, ``b"none"``, or ``None``.

    ``path``
      The path used for the session cookie. Default: ``'/'``.

    ``domains``
      The domain(s) used for the session cookie. Default: ``None`` (no domain).
      Can be passed an iterable containing multiple domains, this will set
      multiple cookies one for each domain.

    ``serializer``
      An object with two methods: `loads`` and ``dumps``.  The ``loads`` method
      should accept bytes and return a Python object.  The ``dumps`` method
      should accept a Python object and return bytes.  A ``ValueError`` should
      be raised for malformed inputs.  Default: ``None`, which will use a
      derivation of :func:`json.dumps` and ``json.loads``.
    """

    secret: str | bytes
    salt: str | bytes
    hashalg: str
    original_serializer: _Serializer
    def __init__(
        self,
        secret: str,
        salt: str,
        cookie_name: str,
        secure: bool = False,
        max_age: int | timedelta | None = None,
        httponly: bool | None = False,
        samesite: _SameSitePolicy | None = None,
        path: str = "/",
        domains: Collection[str] | None = None,
        hashalg: str = "sha512",
        serializer: _Serializer | None = None,
    ) -> None: ...
    def __call__(self, request: BaseRequest) -> SignedCookieProfile:
        """Bind a request to a copy of this instance and return it"""

    def bind(self, request: BaseRequest) -> SignedCookieProfile:
        """Bind a request to a copy of this instance and return it"""
