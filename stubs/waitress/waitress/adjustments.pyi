"""Adjustments are tunable parameters."""

from _typeshed import Incomplete
from collections.abc import Iterable, Sequence
from socket import socket
from typing import Final
from typing_extensions import TypeAlias

# Really complex, consider unpacking a TypedDict
_AdjustmentsParams: TypeAlias = Incomplete

truthy: frozenset[str]
KNOWN_PROXY_HEADERS: Final[frozenset[str]]

def asbool(s: bool | str | int | None) -> bool:
    """Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is any of ``t``, ``true``, ``y``, ``on``, or ``1``, otherwise
    return the boolean value ``False``.  If ``s`` is the value ``None``,
    return ``False``.  If ``s`` is already one of the boolean values ``True``
    or ``False``, return it.
    """

def asoctal(s: str) -> int:
    """Convert the given octal string to an actual number."""

def aslist_cronly(value: str) -> list[str]: ...
def aslist(value: str) -> list[str]:
    """Return a list of strings, separating the input based on newlines
    and, if flatten=True (the default), also split on spaces within
    each line.
    """

def asset(value: str | None) -> set[str]: ...
def slash_fixed_str(s: str | None) -> str: ...
def str_iftruthy(s: str | None) -> str | None: ...
def as_socket_list(sockets: Sequence[object]) -> list[socket]:
    """Checks if the elements in the list are of type socket and
    removes them if not.
    """

class _str_marker(str): ...
class _int_marker(int): ...

class Adjustments:
    """This class contains tunable parameters."""

    host: _str_marker
    port: _int_marker
    listen: list[str]
    threads: int
    trusted_proxy: str | None
    trusted_proxy_count: int | None
    trusted_proxy_headers: set[str]
    log_untrusted_proxy_headers: bool
    clear_untrusted_proxy_headers: bool
    url_scheme: str
    url_prefix: str
    ident: str
    backlog: int
    recv_bytes: int
    send_bytes: int
    outbuf_overflow: int
    outbuf_high_watermark: int
    inbuf_overflow: int
    connection_limit: int
    cleanup_interval: int
    channel_timeout: int
    log_socket_errors: bool
    max_request_header_size: int
    max_request_body_size: int
    expose_tracebacks: bool
    unix_socket: str | None
    unix_socket_perms: int
    socket_options: list[tuple[int, int, int]]
    asyncore_loop_timeout: int
    asyncore_use_poll: bool
    ipv4: bool
    ipv6: bool
    sockets: list[socket]
    channel_request_lookahead: int
    server_name: str
    def __init__(self, **kw: _AdjustmentsParams) -> None: ...
    @classmethod
    def parse_args(cls, argv: str) -> tuple[dict[str, bool], list[str]]:
        """Pre-parse command line arguments for input into __init__.  Note that
        this does not cast values into adjustment types, it just creates a
        dictionary suitable for passing into __init__, where __init__ does the
        casting.
        """

    @classmethod
    def check_sockets(cls, sockets: Iterable[socket]) -> None: ...
