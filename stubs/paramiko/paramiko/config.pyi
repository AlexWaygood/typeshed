"""
Configuration file (aka ``ssh_config``) support.
"""

from _typeshed import FileDescriptorOrPath
from collections.abc import Iterable
from re import Pattern
from typing import IO
from typing_extensions import Self

from paramiko.ssh_exception import ConfigParseError as ConfigParseError, CouldNotCanonicalize as CouldNotCanonicalize

invoke_import_error: ImportError | None
SSH_PORT: int

class SSHConfig:
    """
    Representation of config information as stored in the format used by
    OpenSSH. Queries can be made via `lookup`. The format is described in
    OpenSSH's ``ssh_config`` man page. This class is provided primarily as a
    convenience to posix users (since the OpenSSH format is a de-facto
    standard on posix) but should work fine on Windows too.

    .. versionadded:: 1.6
    """

    SETTINGS_REGEX: Pattern[str]
    TOKENS_BY_CONFIG_KEY: dict[str, list[str]]
    def __init__(self) -> None:
        """
        Create a new OpenSSH config object.

        Note: the newer alternate constructors `from_path`, `from_file` and
        `from_text` are simpler to use, as they parse on instantiation. For
        example, instead of::

            config = SSHConfig()
            config.parse(open("some-path.config")

        you could::

            config = SSHConfig.from_file(open("some-path.config"))
            # Or more directly:
            config = SSHConfig.from_path("some-path.config")
            # Or if you have arbitrary ssh_config text from some other source:
            config = SSHConfig.from_text("Host foo\\n\\tUser bar")
        """

    @classmethod
    def from_text(cls, text: str) -> Self:
        """
        Create a new, parsed `SSHConfig` from ``text`` string.

        .. versionadded:: 2.7
        """

    @classmethod
    def from_path(cls, path: FileDescriptorOrPath) -> Self:
        """
        Create a new, parsed `SSHConfig` from the file found at ``path``.

        .. versionadded:: 2.7
        """

    @classmethod
    def from_file(cls, flo: IO[str]) -> Self:
        """
        Create a new, parsed `SSHConfig` from file-like object ``flo``.

        .. versionadded:: 2.7
        """

    def parse(self, file_obj: IO[str]) -> None:
        """
        Read an OpenSSH config from the given file object.

        :param file_obj: a file-like object to read the config file from
        """

    def lookup(self, hostname: str) -> SSHConfigDict:
        """
        Return a dict (`SSHConfigDict`) of config options for a given hostname.

        The host-matching rules of OpenSSH's ``ssh_config`` man page are used:
        For each parameter, the first obtained value will be used.  The
        configuration files contain sections separated by ``Host`` and/or
        ``Match`` specifications, and that section is only applied for hosts
        which match the given patterns or keywords

        Since the first obtained value for each parameter is used, more host-
        specific declarations should be given near the beginning of the file,
        and general defaults at the end.

        The keys in the returned dict are all normalized to lowercase (look for
        ``"port"``, not ``"Port"``. The values are processed according to the
        rules for substitution variable expansion in ``ssh_config``.

        Finally, please see the docs for `SSHConfigDict` for deeper info on
        features such as optional type conversion methods, e.g.::

            conf = my_config.lookup('myhost')
            assert conf['passwordauthentication'] == 'yes'
            assert conf.as_bool('passwordauthentication') is True

        .. note::
            If there is no explicitly configured ``HostName`` value, it will be
            set to the being-looked-up hostname, which is as close as we can
            get to OpenSSH's behavior around that particular option.

        :param str hostname: the hostname to lookup

        .. versionchanged:: 2.5
            Returns `SSHConfigDict` objects instead of dict literals.
        .. versionchanged:: 2.7
            Added canonicalization support.
        .. versionchanged:: 2.7
            Added ``Match`` support.
        .. versionchanged:: 3.3
            Added ``Match final`` support.
        """

    def canonicalize(self, hostname: str, options: SSHConfigDict, domains: Iterable[str]) -> str:
        """
        Return canonicalized version of ``hostname``.

        :param str hostname: Target hostname.
        :param options: An `SSHConfigDict` from a previous lookup pass.
        :param domains: List of domains (e.g. ``["paramiko.org"]``).

        :returns: A canonicalized hostname if one was found, else ``None``.

        .. versionadded:: 2.7
        """

    def get_hostnames(self) -> set[str]:
        """
        Return the set of literal hostnames defined in the SSH config (both
        explicit hostnames and wildcard entries).
        """

class LazyFqdn:
    """
    Returns the host's fqdn on request as string.
    """

    fqdn: str | None
    config: SSHConfig
    host: str | None
    def __init__(self, config: SSHConfigDict, host: str | None = None) -> None: ...

class SSHConfigDict(dict[str, str]):
    """
    A dictionary wrapper/subclass for per-host configuration structures.

    This class introduces some usage niceties for consumers of `SSHConfig`,
    specifically around the issue of variable type conversions: normal value
    access yields strings, but there are now methods such as `as_bool` and
    `as_int` that yield casted values instead.

    For example, given the following ``ssh_config`` file snippet::

        Host foo.example.com
            PasswordAuthentication no
            Compression yes
            ServerAliveInterval 60

    the following code highlights how you can access the raw strings as well as
    usefully Python type-casted versions (recalling that keys are all
    normalized to lowercase first)::

        my_config = SSHConfig()
        my_config.parse(open('~/.ssh/config'))
        conf = my_config.lookup('foo.example.com')

        assert conf['passwordauthentication'] == 'no'
        assert conf.as_bool('passwordauthentication') is False
        assert conf['compression'] == 'yes'
        assert conf.as_bool('compression') is True
        assert conf['serveraliveinterval'] == '60'
        assert conf.as_int('serveraliveinterval') == 60

    .. versionadded:: 2.5
    """

    def as_bool(self, key: str) -> bool:
        """
        Express given key's value as a boolean type.

        Typically, this is used for ``ssh_config``'s pseudo-boolean values
        which are either ``"yes"`` or ``"no"``. In such cases, ``"yes"`` yields
        ``True`` and any other value becomes ``False``.

        .. note::
            If (for whatever reason) the stored value is already boolean in
            nature, it's simply returned.

        .. versionadded:: 2.5
        """

    def as_int(self, key: str) -> int:
        """
        Express given key's value as an integer, if possible.

        This method will raise ``ValueError`` or similar if the value is not
        int-appropriate, same as the builtin `int` type.

        .. versionadded:: 2.5
        """
