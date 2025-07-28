from collections.abc import Iterable
from datetime import timedelta
from logging import Logger
from re import Match, Pattern
from typing import Any, Final, Literal, TypedDict, TypeVar, overload
from typing_extensions import TypeAlias

import flask

_IterableT = TypeVar("_IterableT", bound=Iterable[Any])
_T = TypeVar("_T")
_MultiDict: TypeAlias = Any  # werkzeug is not part of typeshed

class _Options(TypedDict, total=False):
    resources: dict[str, dict[str, Any]] | list[str] | str | None
    origins: str | list[str] | None
    methods: str | list[str] | None
    expose_headers: str | list[str] | None
    allow_headers: str | list[str] | None
    supports_credentials: bool | None
    max_age: timedelta | int | str | None
    send_wildcard: bool | None
    vary_header: bool | None
    automatic_options: bool | None
    intercept_exceptions: bool | None
    always_send: bool | None

LOG: Logger

ACL_ORIGIN: Final = "Access-Control-Allow-Origin"
ACL_METHODS: Final = "Access-Control-Allow-Methods"
ACL_ALLOW_HEADERS: Final = "Access-Control-Allow-Headers"
ACL_EXPOSE_HEADERS: Final = "Access-Control-Expose-Headers"
ACL_CREDENTIALS: Final = "Access-Control-Allow-Credentials"
ACL_MAX_AGE: Final = "Access-Control-Max-Age"
ACL_RESPONSE_PRIVATE_NETWORK: Final = "Access-Control-Allow-Private-Network"
ACL_REQUEST_METHOD: Final = "Access-Control-Request-Method"
ACL_REQUEST_HEADERS: Final = "Access-Control-Request-Headers"
ACL_REQUEST_HEADER_PRIVATE_NETWORK: Final = "Access-Control-Request-Private-Network"
ALL_METHODS: Final[list[str]]
CONFIG_OPTIONS: Final[list[str]]
FLASK_CORS_EVALUATED: Final = "_FLASK_CORS_EVALUATED"
RegexObject: Final[type[Pattern[str]]]
DEFAULT_OPTIONS: Final[_Options]

def parse_resources(resources: dict[str, _Options] | Iterable[str] | str | Pattern[str]) -> list[tuple[str, _Options]]: ...
def get_regexp_pattern(regexp: str | Pattern[str]) -> str:
    """
    Helper that returns regexp pattern from given value.

    :param regexp: regular expression to stringify
    :type regexp: _sre.SRE_Pattern or str
    :returns: string representation of given regexp pattern
    :rtype: str
    """

def get_cors_origins(options: _Options, request_origin: str | None) -> list[str] | None: ...
def get_allow_headers(options: _Options, acl_request_headers: str | None) -> str | None: ...
def get_cors_headers(options: _Options, request_headers: dict[str, Any], request_method: str) -> _MultiDict: ...
def set_cors_headers(resp: flask.Response, options: _Options) -> flask.Response:
    """
    Performs the actual evaluation of Flask-CORS options and actually
    modifies the response object.

    This function is used both in the decorator and the after_request
    callback
    """

@overload
def probably_regex(maybe_regex: Pattern[str]) -> Literal[True]: ...
@overload
def probably_regex(maybe_regex: str) -> bool: ...
def re_fix(reg: str) -> str:
    """
    Replace the invalid regex r'*' with the valid, wildcard regex r'/.*' to
    enable the CORS app extension to have a more user friendly api.
    """

def try_match_any_pattern(inst: str, patterns: Iterable[str | Pattern[str]], caseSensitive: bool = True) -> bool: ...
def try_match_pattern(value: str, pattern: str | Pattern[str], caseSensitive: bool = True) -> bool | Match[str]:
    """
    Safely attempts to match a pattern or string to a value. This
    function can be used to match request origins, headers, or paths.
    The value of caseSensitive should be set in accordance to the
    data being compared e.g. origins and headers are case insensitive
    whereas paths are case-sensitive
    """

def get_cors_options(appInstance: flask.Flask | None, *dicts: _Options) -> _Options:
    """
    Compute CORS options for an application by combining the DEFAULT_OPTIONS,
    the app's configuration-specified options and any dictionaries passed. The
    last specified option wins.
    """

def get_app_kwarg_dict(appInstance: flask.Flask | None = None) -> _Options:
    """Returns the dictionary of CORS specific app configurations."""

def flexible_str(obj: object) -> str | None:
    """
    A more flexible str function which intelligently handles stringifying
    strings, lists and other iterables. The results are lexographically sorted
    to ensure generated responses are consistent when iterables such as Set
    are used.
    """

def serialize_option(options_dict: _Options, key: str, upper: bool = False) -> None: ...
@overload
def ensure_iterable(inst: str) -> list[str]:  # type: ignore[overload-overlap]
    """
    Wraps scalars or string types as a list, or returns the iterable instance.
    """

@overload
def ensure_iterable(inst: _IterableT) -> _IterableT: ...  # type: ignore[overload-overlap]
@overload
def ensure_iterable(inst: _T) -> list[_T]: ...
def sanitize_regex_param(param: str | list[str]) -> list[str]: ...
def serialize_options(opts: _Options) -> _Options:
    """
    A helper method to serialize and processes the options dictionary.
    """
