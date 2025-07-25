import socket
from collections.abc import Mapping

from paramiko.pkey import PKey

class SSHException(Exception):
    """
    Exception raised by failures in SSH2 protocol negotiation or logic errors.
    """

class AuthenticationException(SSHException):
    """
    Exception raised when authentication failed for some reason.  It may be
    possible to retry with different credentials.  (Other classes specify more
    specific reasons.)

    .. versionadded:: 1.6
    """

class PasswordRequiredException(AuthenticationException):
    """
    Exception raised when a password is needed to unlock a private key file.
    """

class BadAuthenticationType(AuthenticationException):
    """
    Exception raised when an authentication type (like password) is used, but
    the server isn't allowing that type.  (It may only allow public-key, for
    example.)

    .. versionadded:: 1.1
    """

    allowed_types: list[str]
    explanation: str
    def __init__(self, explanation: str, types: list[str]) -> None: ...

class PartialAuthentication(AuthenticationException):
    """
    An internal exception thrown in the case of partial authentication.
    """

    allowed_types: list[str]
    def __init__(self, types: list[str]) -> None: ...

class UnableToAuthenticate(AuthenticationException): ...

class ChannelException(SSHException):
    """
    Exception raised when an attempt to open a new `.Channel` fails.

    :param int code: the error code returned by the server

    .. versionadded:: 1.6
    """

    code: int
    text: str
    def __init__(self, code: int, text: str) -> None: ...

class BadHostKeyException(SSHException):
    """
    The host key given by the SSH server did not match what we were expecting.

    :param str hostname: the hostname of the SSH server
    :param PKey got_key: the host key presented by the server
    :param PKey expected_key: the host key expected

    .. versionadded:: 1.6
    """

    hostname: str
    key: PKey
    expected_key: PKey
    def __init__(self, hostname: str, got_key: PKey, expected_key: PKey) -> None: ...

class IncompatiblePeer(SSHException):
    """
    A disagreement arose regarding an algorithm required for key exchange.

    .. versionadded:: 2.9
    """

class ProxyCommandFailure(SSHException):
    """
    The "ProxyCommand" found in the .ssh/config file returned an error.

    :param str command: The command line that is generating this exception.
    :param str error: The error captured from the proxy command output.
    """

    command: str
    error: str
    def __init__(self, command: str, error: str) -> None: ...

class MessageOrderError(SSHException):
    """
    Out-of-order protocol messages were received, violating "strict kex" mode.

    .. versionadded:: 3.4
    """

class NoValidConnectionsError(socket.error):
    """
    Multiple connection attempts were made and no families succeeded.

    This exception class wraps multiple "real" underlying connection errors,
    all of which represent failed connection attempts. Because these errors are
    not guaranteed to all be of the same error type (i.e. different errno,
    `socket.error` subclass, message, etc) we expose a single unified error
    message and a ``None`` errno so that instances of this class match most
    normal handling of `socket.error` objects.

    To see the wrapped exception objects, access the ``errors`` attribute.
    ``errors`` is a dict whose keys are address tuples (e.g. ``('127.0.0.1',
    22)``) and whose values are the exception encountered trying to connect to
    that address.

    It is implied/assumed that all the errors given to a single instance of
    this class are from connecting to the same hostname + port (and thus that
    the differences are in the resolution of the hostname - e.g. IPv4 vs v6).

    .. versionadded:: 1.16
    """

    errors: Mapping[tuple[str, int] | tuple[str, int, int, int], Exception]
    def __init__(self, errors: Mapping[tuple[str, int] | tuple[str, int, int, int], Exception]) -> None:
        """
        :param dict errors:
            The errors dict to store, as described by class docstring.
        """

    def __reduce__(self) -> tuple[type, tuple[Mapping[tuple[str, int] | tuple[str, int, int, int], Exception]]]: ...

class CouldNotCanonicalize(SSHException):
    """
    Raised when hostname canonicalization fails & fallback is disabled.

    .. versionadded:: 2.7
    """

class ConfigParseError(SSHException):
    """
    A fatal error was encountered trying to parse SSH config data.

    Typically this means a config file violated the ``ssh_config``
    specification in a manner that requires exiting immediately, such as not
    matching ``key = value`` syntax or misusing certain ``Match`` keywords.

    .. versionadded:: 2.7
    """
