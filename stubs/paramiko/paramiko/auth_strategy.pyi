"""
Modern, adaptable authentication machinery.

Replaces certain parts of `.SSHClient`. For a concrete implementation, see the
``OpenSSHAuthStrategy`` class in `Fabric <https://fabfile.org>`_.
"""

import abc
from collections.abc import Callable, Iterator
from logging import Logger
from pathlib import Path
from typing import NamedTuple

from paramiko.config import SSHConfig
from paramiko.pkey import PKey
from paramiko.ssh_exception import AuthenticationException
from paramiko.transport import Transport

class AuthSource:
    """
    Some SSH authentication source, such as a password, private key, or agent.

    See subclasses in this module for concrete implementations.

    All implementations must accept at least a ``username`` (``str``) kwarg.
    """

    username: str
    def __init__(self, username: str) -> None: ...
    @abc.abstractmethod
    def authenticate(self, transport: Transport) -> list[str]:
        """
        Perform authentication.
        """

class NoneAuth(AuthSource):
    """
    Auth type "none", ie https://www.rfc-editor.org/rfc/rfc4252#section-5.2 .
    """

    def authenticate(self, transport: Transport) -> list[str]: ...

class Password(AuthSource):
    """
    Password authentication.

    :param callable password_getter:
        A lazy callable that should return a `str` password value at
        authentication time, such as a `functools.partial` wrapping
        `getpass.getpass`, an API call to a secrets store, or similar.

        If you already know the password at instantiation time, you should
        simply use something like ``lambda: "my literal"`` (for a literal, but
        also, shame on you!) or ``lambda: variable_name`` (for something stored
        in a variable).
    """

    password_getter: Callable[[], str]
    def __init__(self, username: str, password_getter: Callable[[], str]) -> None: ...
    def authenticate(self, transport: Transport) -> list[str]: ...

class PrivateKey(AuthSource):
    """
    Essentially a mixin for private keys.

    Knows how to auth, but leaves key material discovery/loading/decryption to
    subclasses.

    Subclasses **must** ensure that they've set ``self.pkey`` to a decrypted
    `.PKey` instance before calling ``super().authenticate``; typically
    either in their ``__init__``, or in an overridden ``authenticate`` prior to
    its `super` call.
    """

    def authenticate(self, transport: Transport) -> list[str]: ...

class InMemoryPrivateKey(PrivateKey):
    """
    An in-memory, decrypted `.PKey` object.
    """

    pkey: PKey
    def __init__(self, username: str, pkey: PKey) -> None: ...

class OnDiskPrivateKey(PrivateKey):
    """
    Some on-disk private key that needs opening and possibly decrypting.

    :param str source:
        String tracking where this key's path was specified; should be one of
        ``"ssh-config"``, ``"python-config"``, or ``"implicit-home"``.
    :param Path path:
        The filesystem path this key was loaded from.
    :param PKey pkey:
        The `PKey` object this auth source uses/represents.
    """

    source: str
    path: Path
    pkey: PKey
    def __init__(self, username: str, source: str, path: Path, pkey: PKey) -> None: ...

class SourceResult(NamedTuple):
    """SourceResult(source, result)"""

    source: AuthSource
    result: list[str] | Exception

class AuthResult(list[SourceResult]):
    """
    Represents a partial or complete SSH authentication attempt.

    This class conceptually extends `AuthStrategy` by pairing the former's
    authentication **sources** with the **results** of trying to authenticate
    with them.

    `AuthResult` is a (subclass of) `list` of `namedtuple`, which are of the
    form ``namedtuple('SourceResult', 'source', 'result')`` (where the
    ``source`` member is an `AuthSource` and the ``result`` member is either a
    return value from the relevant `.Transport` method, or an exception
    object).

    .. note::
        Transport auth method results are always themselves a ``list`` of "next
        allowable authentication methods".

        In the simple case of "you just authenticated successfully", it's an
        empty list; if your auth was rejected but you're allowed to try again,
        it will be a list of string method names like ``pubkey`` or
        ``password``.

        The ``__str__`` of this class represents the empty-list scenario as the
        word ``success``, which should make reading the result of an
        authentication session more obvious to humans.

    Instances also have a `strategy` attribute referencing the `AuthStrategy`
    which was attempted.
    """

    strategy: AuthStrategy
    def __init__(self, strategy: AuthStrategy, *args: SourceResult, **kwargs: object) -> None: ...

class AuthFailure(AuthenticationException):
    """
    Basic exception wrapping an `AuthResult` indicating overall auth failure.

    Note that `AuthFailure` descends from `AuthenticationException` but is
    generally "higher level"; the latter is now only raised by individual
    `AuthSource` attempts and should typically only be seen by users when
    encapsulated in this class. It subclasses `AuthenticationException`
    primarily for backwards compatibility reasons.
    """

    result: AuthResult
    def __init__(self, result: AuthResult) -> None: ...

class AuthStrategy:
    """
    This class represents one or more attempts to auth with an SSH server.

    By default, subclasses must at least accept an ``ssh_config``
    (`.SSHConfig`) keyword argument, but may opt to accept more as needed for
    their particular strategy.
    """

    ssh_config: SSHConfig
    log: Logger
    def __init__(self, ssh_config: SSHConfig) -> None: ...
    @abc.abstractmethod
    def get_sources(self) -> Iterator[AuthSource]:
        """
        Generator yielding `AuthSource` instances, in the order to try.

        This is the primary override point for subclasses: you figure out what
        sources you need, and ``yield`` them.

        Subclasses _of_ subclasses may find themselves wanting to do things
        like filtering or discarding around a call to `super`.
        """

    def authenticate(self, transport: Transport) -> list[SourceResult]:
        """
        Handles attempting `AuthSource` instances yielded from `get_sources`.

        You *normally* won't need to override this, but it's an option for
        advanced users.
        """
