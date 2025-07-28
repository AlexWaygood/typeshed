"""
SSH client & key policies
"""

from _typeshed import FileDescriptorOrPath
from collections.abc import Iterable, Mapping
from typing import NoReturn, Protocol

from paramiko.auth_strategy import AuthStrategy
from paramiko.channel import Channel, ChannelFile, ChannelStderrFile, ChannelStdinFile
from paramiko.hostkeys import HostKeys
from paramiko.pkey import PKey
from paramiko.sftp_client import SFTPClient
from paramiko.transport import Transport, _SocketLike
from paramiko.util import ClosingContextManager

class _TransportFactory(Protocol):
    def __call__(
        self,
        sock: _SocketLike,
        /,
        *,
        gss_kex: bool,
        gss_deleg_creds: bool,
        disabled_algorithms: Mapping[str, Iterable[str]] | None,
    ) -> Transport: ...

class SSHClient(ClosingContextManager):
    """
    A high-level representation of a session with an SSH server.  This class
    wraps `.Transport`, `.Channel`, and `.SFTPClient` to take care of most
    aspects of authenticating and opening channels.  A typical use case is::

        client = SSHClient()
        client.load_system_host_keys()
        client.connect('ssh.example.com')
        stdin, stdout, stderr = client.exec_command('ls -l')

    You may pass in explicit overrides for authentication and server host key
    checking.  The default mechanism is to try to use local key files or an
    SSH agent (if one is running).

    Instances of this class may be used as context managers.

    .. versionadded:: 1.6
    """

    def __init__(self) -> None:
        """
        Create a new SSHClient.
        """

    def load_system_host_keys(self, filename: FileDescriptorOrPath | None = None) -> None:
        """
        Load host keys from a system (read-only) file.  Host keys read with
        this method will not be saved back by `save_host_keys`.

        This method can be called multiple times.  Each new set of host keys
        will be merged with the existing set (new replacing old if there are
        conflicts).

        If ``filename`` is left as ``None``, an attempt will be made to read
        keys from the user's local "known hosts" file, as used by OpenSSH,
        and no exception will be raised if the file can't be read.  This is
        probably only useful on posix.

        :param str filename: the filename to read, or ``None``

        :raises: ``IOError`` --
            if a filename was provided and the file could not be read
        """

    def load_host_keys(self, filename: FileDescriptorOrPath) -> None:
        """
        Load host keys from a local host-key file.  Host keys read with this
        method will be checked after keys loaded via `load_system_host_keys`,
        but will be saved back by `save_host_keys` (so they can be modified).
        The missing host key policy `.AutoAddPolicy` adds keys to this set and
        saves them, when connecting to a previously-unknown server.

        This method can be called multiple times.  Each new set of host keys
        will be merged with the existing set (new replacing old if there are
        conflicts).  When automatically saving, the last hostname is used.

        :param str filename: the filename to read

        :raises: ``IOError`` -- if the filename could not be read
        """

    def save_host_keys(self, filename: FileDescriptorOrPath) -> None:
        """
        Save the host keys back to a file.  Only the host keys loaded with
        `load_host_keys` (plus any added directly) will be saved -- not any
        host keys loaded with `load_system_host_keys`.

        :param str filename: the filename to save to

        :raises: ``IOError`` -- if the file could not be written
        """

    def get_host_keys(self) -> HostKeys:
        """
        Get the local `.HostKeys` object.  This can be used to examine the
        local host keys or change them.

        :return: the local host keys as a `.HostKeys` object.
        """

    def set_log_channel(self, name: str) -> None:
        """
        Set the channel for logging.  The default is ``"paramiko.transport"``
        but it can be set to anything you want.

        :param str name: new channel name for logging
        """

    def set_missing_host_key_policy(self, policy: type[MissingHostKeyPolicy] | MissingHostKeyPolicy) -> None:
        """
        Set policy to use when connecting to servers without a known host key.

        Specifically:

        * A **policy** is a "policy class" (or instance thereof), namely some
          subclass of `.MissingHostKeyPolicy` such as `.RejectPolicy` (the
          default), `.AutoAddPolicy`, `.WarningPolicy`, or a user-created
          subclass.
        * A host key is **known** when it appears in the client object's cached
          host keys structures (those manipulated by `load_system_host_keys`
          and/or `load_host_keys`).

        :param .MissingHostKeyPolicy policy:
            the policy to use when receiving a host key from a
            previously-unknown server
        """

    def connect(
        self,
        hostname: str,
        port: int = 22,
        username: str | None = None,
        password: str | None = None,
        pkey: PKey | None = None,
        key_filename: str | None = None,
        timeout: float | None = None,
        allow_agent: bool = True,
        look_for_keys: bool = True,
        compress: bool = False,
        sock: _SocketLike | None = None,
        gss_auth: bool = False,
        gss_kex: bool = False,
        gss_deleg_creds: bool = True,
        gss_host: str | None = None,
        banner_timeout: float | None = None,
        auth_timeout: float | None = None,
        channel_timeout: float | None = None,
        gss_trust_dns: bool = True,
        passphrase: str | None = None,
        disabled_algorithms: Mapping[str, Iterable[str]] | None = None,
        transport_factory: _TransportFactory | None = None,
        auth_strategy: AuthStrategy | None = None,
    ) -> None:
        """
        Connect to an SSH server and authenticate to it.  The server's host key
        is checked against the system host keys (see `load_system_host_keys`)
        and any local host keys (`load_host_keys`).  If the server's hostname
        is not found in either set of host keys, the missing host key policy
        is used (see `set_missing_host_key_policy`).  The default policy is
        to reject the key and raise an `.SSHException`.

        Authentication is attempted in the following order of priority:

            - The ``pkey`` or ``key_filename`` passed in (if any)

              - ``key_filename`` may contain OpenSSH public certificate paths
                as well as regular private-key paths; when files ending in
                ``-cert.pub`` are found, they are assumed to match a private
                key, and both components will be loaded. (The private key
                itself does *not* need to be listed in ``key_filename`` for
                this to occur - *just* the certificate.)

            - Any key we can find through an SSH agent
            - Any "id_rsa", "id_dsa" or "id_ecdsa" key discoverable in
              ``~/.ssh/``

              - When OpenSSH-style public certificates exist that match an
                existing such private key (so e.g. one has ``id_rsa`` and
                ``id_rsa-cert.pub``) the certificate will be loaded alongside
                the private key and used for authentication.

            - Plain username/password auth, if a password was given

        If a private key requires a password to unlock it, and a password is
        passed in, that password will be used to attempt to unlock the key.

        :param str hostname: the server to connect to
        :param int port: the server port to connect to
        :param str username:
            the username to authenticate as (defaults to the current local
            username)
        :param str password:
            Used for password authentication; is also used for private key
            decryption if ``passphrase`` is not given.
        :param str passphrase:
            Used for decrypting private keys.
        :param .PKey pkey: an optional private key to use for authentication
        :param str key_filename:
            the filename, or list of filenames, of optional private key(s)
            and/or certs to try for authentication
        :param float timeout:
            an optional timeout (in seconds) for the TCP connect
        :param bool allow_agent:
            set to False to disable connecting to the SSH agent
        :param bool look_for_keys:
            set to False to disable searching for discoverable private key
            files in ``~/.ssh/``
        :param bool compress: set to True to turn on compression
        :param socket sock:
            an open socket or socket-like object (such as a `.Channel`) to use
            for communication to the target host
        :param bool gss_auth:
            ``True`` if you want to use GSS-API authentication
        :param bool gss_kex:
            Perform GSS-API Key Exchange and user authentication
        :param bool gss_deleg_creds: Delegate GSS-API client credentials or not
        :param str gss_host:
            The targets name in the kerberos database. default: hostname
        :param bool gss_trust_dns:
            Indicates whether or not the DNS is trusted to securely
            canonicalize the name of the host being connected to (default
            ``True``).
        :param float banner_timeout: an optional timeout (in seconds) to wait
            for the SSH banner to be presented.
        :param float auth_timeout: an optional timeout (in seconds) to wait for
            an authentication response.
        :param float channel_timeout: an optional timeout (in seconds) to wait
             for a channel open response.
        :param dict disabled_algorithms:
            an optional dict passed directly to `.Transport` and its keyword
            argument of the same name.
        :param transport_factory:
            an optional callable which is handed a subset of the constructor
            arguments (primarily those related to the socket, GSS
            functionality, and algorithm selection) and generates a
            `.Transport` instance to be used by this client. Defaults to
            `.Transport.__init__`.
        :param auth_strategy:
            an optional instance of `.AuthStrategy`, triggering use of this
            newer authentication mechanism instead of SSHClient's legacy auth
            method.

            .. warning::
                This parameter is **incompatible** with all other
                authentication-related parameters (such as, but not limited to,
                ``password``, ``key_filename`` and ``allow_agent``) and will
                trigger an exception if given alongside them.

        :returns:
            `.AuthResult` if ``auth_strategy`` is non-``None``; otherwise,
            returns ``None``.

        :raises BadHostKeyException:
            if the server's host key could not be verified.
        :raises AuthenticationException:
            if authentication failed.
        :raises UnableToAuthenticate:
            if authentication failed (when ``auth_strategy`` is non-``None``;
            and note that this is a subclass of ``AuthenticationException``).
        :raises socket.error:
            if a socket error (other than connection-refused or
            host-unreachable) occurred while connecting.
        :raises NoValidConnectionsError:
            if all valid connection targets for the requested hostname (eg IPv4
            and IPv6) yielded connection-refused or host-unreachable socket
            errors.
        :raises SSHException:
            if there was any other error connecting or establishing an SSH
            session.

        .. versionchanged:: 1.15
            Added the ``banner_timeout``, ``gss_auth``, ``gss_kex``,
            ``gss_deleg_creds`` and ``gss_host`` arguments.
        .. versionchanged:: 2.3
            Added the ``gss_trust_dns`` argument.
        .. versionchanged:: 2.4
            Added the ``passphrase`` argument.
        .. versionchanged:: 2.6
            Added the ``disabled_algorithms`` argument.
        .. versionchanged:: 2.12
            Added the ``transport_factory`` argument.
        .. versionchanged:: 3.2
            Added the ``auth_strategy`` argument.
        """

    def close(self) -> None:
        """
        Close this SSHClient and its underlying `.Transport`.

        This should be called anytime you are done using the client object.

        .. warning::
            Paramiko registers garbage collection hooks that will try to
            automatically close connections for you, but this is not presently
            reliable. Failure to explicitly close your client after use may
            lead to end-of-process hangs!
        """

    def exec_command(
        self,
        command: str,
        bufsize: int = -1,
        timeout: float | None = None,
        get_pty: bool = False,
        environment: Mapping[str, str] | None = None,
    ) -> tuple[ChannelStdinFile, ChannelFile, ChannelStderrFile]:
        """
        Execute a command on the SSH server.  A new `.Channel` is opened and
        the requested command is executed.  The command's input and output
        streams are returned as Python ``file``-like objects representing
        stdin, stdout, and stderr.

        :param str command: the command to execute
        :param int bufsize:
            interpreted the same way as by the built-in ``file()`` function in
            Python
        :param int timeout:
            set command's channel timeout. See `.Channel.settimeout`
        :param bool get_pty:
            Request a pseudo-terminal from the server (default ``False``).
            See `.Channel.get_pty`
        :param dict environment:
            a dict of shell environment variables, to be merged into the
            default environment that the remote command executes within.

            .. warning::
                Servers may silently reject some environment variables; see the
                warning in `.Channel.set_environment_variable` for details.

        :return:
            the stdin, stdout, and stderr of the executing command, as a
            3-tuple

        :raises: `.SSHException` -- if the server fails to execute the command

        .. versionchanged:: 1.10
            Added the ``get_pty`` kwarg.
        """

    def invoke_shell(
        self,
        term: str = "vt100",
        width: int = 80,
        height: int = 24,
        width_pixels: int = 0,
        height_pixels: int = 0,
        environment: Mapping[str, str] | None = None,
    ) -> Channel:
        """
        Start an interactive shell session on the SSH server.  A new `.Channel`
        is opened and connected to a pseudo-terminal using the requested
        terminal type and size.

        :param str term:
            the terminal type to emulate (for example, ``"vt100"``)
        :param int width: the width (in characters) of the terminal window
        :param int height: the height (in characters) of the terminal window
        :param int width_pixels: the width (in pixels) of the terminal window
        :param int height_pixels: the height (in pixels) of the terminal window
        :param dict environment: the command's environment
        :return: a new `.Channel` connected to the remote shell

        :raises: `.SSHException` -- if the server fails to invoke a shell
        """

    def open_sftp(self) -> SFTPClient:
        """
        Open an SFTP session on the SSH server.

        :return: a new `.SFTPClient` session object
        """

    def get_transport(self) -> Transport | None:
        """
        Return the underlying `.Transport` object for this SSH connection.
        This can be used to perform lower-level tasks, like opening specific
        kinds of channels.

        :return: the `.Transport` for this connection
        """

class MissingHostKeyPolicy:
    """
    Interface for defining the policy that `.SSHClient` should use when the
    SSH server's hostname is not in either the system host keys or the
    application's keys.  Pre-made classes implement policies for automatically
    adding the key to the application's `.HostKeys` object (`.AutoAddPolicy`),
    and for automatically rejecting the key (`.RejectPolicy`).

    This function may be used to ask the user to verify the key, for example.
    """

    def missing_host_key(self, client: SSHClient, hostname: str, key: PKey) -> None:
        """
        Called when an `.SSHClient` receives a server key for a server that
        isn't in either the system or local `.HostKeys` object.  To accept
        the key, simply return.  To reject, raised an exception (which will
        be passed to the calling application).
        """

class AutoAddPolicy(MissingHostKeyPolicy):
    """
    Policy for automatically adding the hostname and new host key to the
    local `.HostKeys` object, and saving it.  This is used by `.SSHClient`.
    """

    def missing_host_key(self, client: SSHClient, hostname: str, key: PKey) -> None: ...

class RejectPolicy(MissingHostKeyPolicy):
    """
    Policy for automatically rejecting the unknown hostname & key.  This is
    used by `.SSHClient`.
    """

    def missing_host_key(self, client: SSHClient, hostname: str, key: PKey) -> NoReturn: ...

class WarningPolicy(MissingHostKeyPolicy):
    """
    Policy for logging a Python-style warning for an unknown host key, but
    accepting it. This is used by `.SSHClient`.
    """

    def missing_host_key(self, client: SSHClient, hostname: str, key: PKey) -> None: ...
