"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.
"""

import sys
from _typeshed import Incomplete, StrOrBytesPath
from collections.abc import Generator, Iterable, Mapping
from contextlib import _GeneratorContextManager
from io import BufferedWriter
from typing import AnyStr
from typing_extensions import TypeAlias

from . import compat, cookies, exceptions, structures
from .models import PreparedRequest, Request

_Uri: TypeAlias = str | bytes
OrderedDict = compat.OrderedDict
cookiejar_from_dict = cookies.cookiejar_from_dict
CaseInsensitiveDict = structures.CaseInsensitiveDict
InvalidURL = exceptions.InvalidURL

NETRC_FILES: tuple[str, str]
DEFAULT_CA_BUNDLE_PATH: Incomplete
DEFAULT_PORTS: dict[str, int]
DEFAULT_ACCEPT_ENCODING: str

def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""

def super_len(o): ...
def get_netrc_auth(url: _Uri, raise_errors: bool = False) -> tuple[str, str] | None:
    """Returns the Requests tuple auth for a given url from netrc."""

def guess_filename(obj):
    """Tries to guess the filename of the given object."""

def extract_zipped_paths(path):
    """Replace nonexistent paths that look like they refer to a member of a zip
    archive with the location of an extracted copy of the target, or else
    just return the provided path unchanged.
    """

def atomic_open(filename: StrOrBytesPath) -> _GeneratorContextManager[BufferedWriter]:
    """Write a file to the disk in an atomic fashion"""

def from_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. Unless it can not be represented as such, return an
    OrderedDict, e.g.,

    ::

        >>> from_key_val_list([('key', 'val')])
        OrderedDict([('key', 'val')])
        >>> from_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples
        >>> from_key_val_list({'key': 'val'})
        OrderedDict([('key', 'val')])

    :rtype: OrderedDict
    """

def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    ::

        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples

    :rtype: list
    """

def parse_list_header(value):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    :rtype: list
    """

def parse_dict_header(value):
    """Parse lists of key, value pairs as described by RFC 2068 Section 2 and
    convert them into a python dict:

    >>> d = parse_dict_header('foo="is a fish", bar="as well"')
    >>> type(d) is dict
    True
    >>> sorted(d.items())
    [('bar', 'as well'), ('foo', 'is a fish')]

    If there is no value for a key it will be `None`:

    >>> parse_dict_header('key_without_value')
    {'key_without_value': None}

    To create a header from the :class:`dict` again, use the
    :func:`dump_header` function.

    :param value: a string with a dict header.
    :return: :class:`dict`
    :rtype: dict
    """

def unquote_header_value(value, is_filename: bool = False):
    """Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    :param value: the header value to unquote.
    :rtype: str
    """

def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    :rtype: dict
    """

def add_dict_to_cookiejar(cj, cookie_dict):
    """Returns a CookieJar from a key/value dictionary.

    :param cj: CookieJar to insert cookies into.
    :param cookie_dict: Dict of key/values to insert into CookieJar.
    :rtype: CookieJar
    """

def get_encodings_from_content(content):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """

def get_encoding_from_headers(headers: Mapping[str, str]) -> str | None:
    """Returns encodings from given HTTP Header Dict.

    :param headers: dictionary to extract encoding from.
    :rtype: str
    """

def stream_decode_response_unicode(iterator, r):
    """Stream decodes an iterator."""

def iter_slices(string: str, slice_length: int | None) -> Generator[str, None, None]:
    """Iterate over slices of a string."""

def get_unicode_from_response(r):
    """Returns the requested content back in unicode.

    :param r: Response object to get unicode content from.

    Tried:

    1. charset from content-type
    2. fall back and replace all unicode characters

    :rtype: str
    """

UNRESERVED_SET: frozenset[str]

def unquote_unreserved(uri: str) -> str:
    """Un-escape any percent-escape sequences in a URI that are unreserved
    characters. This leaves all reserved, illegal and non-ASCII bytes encoded.

    :rtype: str
    """

def requote_uri(uri: str) -> str:
    """Re-quote the given URI.

    This function passes the given URI through an unquote/quote cycle to
    ensure that it is fully and consistently quoted.

    :rtype: str
    """

def address_in_network(ip: str, net: str) -> bool:
    """This function allows you to check if an IP belongs to a network subnet

    Example: returns True if ip = 192.168.1.1 and net = 192.168.1.0/24
             returns False if ip = 192.168.1.1 and net = 192.168.100.0/24

    :rtype: bool
    """

def dotted_netmask(mask: int) -> str:
    """Converts mask from /xx format to xxx.xxx.xxx.xxx

    Example: if mask is 24 function returns 255.255.255.0

    :rtype: str
    """

def is_ipv4_address(string_ip: str) -> bool:
    """
    :rtype: bool
    """

def is_valid_cidr(string_network: str) -> bool:
    """
    Very simple check of the cidr format in no_proxy variable.

    :rtype: bool
    """

def set_environ(env_name: str, value: None) -> _GeneratorContextManager[None]:
    """Set the environment variable 'env_name' to 'value'

    Save previous value, yield, and then restore the previous value stored in
    the environment variable 'env_name'.

    If 'value' is None, do nothing
    """

def should_bypass_proxies(url: _Uri, no_proxy: Iterable[str] | None) -> bool:
    """
    Returns whether we should bypass proxies or not.

    :rtype: bool
    """

def get_environ_proxies(url: _Uri, no_proxy: Iterable[str] | None = None) -> dict[Incomplete, Incomplete]:
    """
    Return a dict of environment proxies.

    :rtype: dict
    """

def select_proxy(url: _Uri, proxies: Mapping[str, str] | None) -> str:
    """Select a proxy for the url, if applicable.

    :param url: The url being for the request
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    """

def resolve_proxies(request: Request | PreparedRequest, proxies: dict[str, str] | None, trust_env: bool = True) -> dict[str, str]:
    """This method takes proxy information from a request and configuration
    input to resolve a mapping of target proxies. This will consider settings
    such as NO_PROXY to strip proxy configurations.

    :param request: Request or PreparedRequest
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    :param trust_env: Boolean declaring whether to trust environment configs

    :rtype: dict
    """

def default_user_agent(name: str = "python-requests") -> str:
    """
    Return a string representing the default user agent.

    :rtype: str
    """

def default_headers() -> CaseInsensitiveDict[str]:
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """

def parse_header_links(value: str) -> list[dict[str, str]]:
    """Return a list of parsed link headers proxies.

    i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"

    :rtype: list
    """

def guess_json_utf(data):
    """
    :rtype: str
    """

def prepend_scheme_if_needed(url, new_scheme):
    """Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument.

    :rtype: str
    """

def get_auth_from_url(url: _Uri) -> tuple[str, str]:
    """Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """

def to_native_string(string, encoding="ascii"):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """

def urldefragauth(url: _Uri):
    """
    Given a url remove the fragment and the authentication part.

    :rtype: str
    """

def rewind_body(prepared_request: PreparedRequest) -> None:
    """Move file pointer back to its recorded starting position
    so it can be read again on redirect.
    """

def check_header_validity(header: tuple[AnyStr, AnyStr]) -> None:
    """Verifies that header parts don't contain leading whitespace
    reserved characters, or return characters.

    :param header: tuple, in the format (name, value).
    """

if sys.platform == "win32":
    def proxy_bypass_registry(host: str) -> bool: ...
    def proxy_bypass(host: str) -> bool: ...
