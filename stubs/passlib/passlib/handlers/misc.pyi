"""passlib.handlers.misc - misc generic handlers"""

from typing import Any, ClassVar
from typing_extensions import deprecated

import passlib.utils.handlers as uh
from passlib.ifc import DisabledHash

class unix_fallback(DisabledHash, uh.StaticHandler):
    """This class provides the fallback behavior for unix shadow files, and follows the :ref:`password-hash-api`.

    This class does not implement a hash, but instead provides fallback
    behavior as found in /etc/shadow on most unix variants.
    If used, should be the last scheme in the context.

    * this class will positively identify all hash strings.
    * for security, passwords will always hash to ``!``.
    * it rejects all passwords if the hash is NOT an empty string (``!`` or ``*`` are frequently used).
    * by default it rejects all passwords if the hash is an empty string,
      but if ``enable_wildcard=True`` is passed to verify(),
      all passwords will be allowed through if the hash is an empty string.

    .. deprecated:: 1.6
        This has been deprecated due to its "wildcard" feature,
        and will be removed in Passlib 1.8. Use :class:`unix_disabled` instead.
    """

    name: ClassVar[str]
    @classmethod
    def identify(cls, hash: str | bytes) -> bool: ...
    enable_wildcard: Any
    def __init__(self, enable_wildcard: bool = False, **kwds) -> None: ...
    @classmethod
    def verify(cls, secret: str | bytes, hash: str | bytes, enable_wildcard: bool = False): ...  # type: ignore[override]

class unix_disabled(DisabledHash, uh.MinimalHandler):
    """This class provides disabled password behavior for unix shadow files,
    and follows the :ref:`password-hash-api`.

    This class does not implement a hash, but instead matches the "disabled account"
    strings found in ``/etc/shadow`` on most Unix variants. "encrypting" a password
    will simply return the disabled account marker. It will reject all passwords,
    no matter the hash string. The :meth:`~passlib.ifc.PasswordHash.hash`
    method supports one optional keyword:

    :type marker: str
    :param marker:
        Optional marker string which overrides the platform default
        used to indicate a disabled account.

        If not specified, this will default to ``"*"`` on BSD systems,
        and use the Linux default ``"!"`` for all other platforms.
        (:attr:`!unix_disabled.default_marker` will contain the default value)

    .. versionadded:: 1.6
        This class was added as a replacement for the now-deprecated
        :class:`unix_fallback` class, which had some undesirable features.
    """

    name: ClassVar[str]
    default_marker: ClassVar[str]
    setting_kwds: ClassVar[tuple[str, ...]]
    context_kwds: ClassVar[tuple[str, ...]]
    @classmethod
    def using(cls, marker=None, **kwds): ...  # type: ignore[override]
    @classmethod
    def identify(cls, hash: str | bytes) -> bool: ...
    @classmethod
    def verify(cls, secret: str | bytes, hash: str | bytes) -> bool: ...  # type: ignore[override]
    @classmethod
    def hash(cls, secret: str | bytes, **kwds) -> str: ...
    @classmethod
    def genhash(cls, secret: str | bytes, config, marker=None): ...  # type: ignore[override]
    @classmethod
    def disable(cls, hash: str | bytes | None = None) -> str: ...
    @classmethod
    def enable(cls, hash: str | bytes) -> str: ...

class plaintext(uh.MinimalHandler):
    """This class stores passwords in plaintext, and follows the :ref:`password-hash-api`.

    The :meth:`~passlib.ifc.PasswordHash.hash`, :meth:`~passlib.ifc.PasswordHash.genhash`, and :meth:`~passlib.ifc.PasswordHash.verify` methods all require the
    following additional contextual keyword:

    :type encoding: str
    :param encoding:
        This controls the character encoding to use (defaults to ``utf-8``).

        This encoding will be used to encode :class:`!unicode` passwords
        under Python 2, and decode :class:`!bytes` hashes under Python 3.

    .. versionchanged:: 1.6
        The ``encoding`` keyword was added.
    """

    name: ClassVar[str]
    default_encoding: ClassVar[str]
    setting_kwds: ClassVar[tuple[str, ...]]
    context_kwds: ClassVar[tuple[str, ...]]
    @classmethod
    def identify(cls, hash: str | bytes): ...
    @classmethod
    def hash(cls, secret: str | bytes, encoding=None): ...  # type: ignore[override]
    @classmethod
    def verify(cls, secret: str | bytes, hash: str | bytes, encoding: str | None = None): ...  # type: ignore[override]
    @deprecated("Deprecated since Passlib 1.7, will be removed in 2.0")
    @classmethod
    def genconfig(cls): ...  # type: ignore[override]
    @deprecated("Deprecated since Passlib 1.7, will be removed in 2.0")
    @classmethod
    def genhash(cls, secret, config, encoding: str | None = None): ...  # type: ignore[override]

__all__ = ["unix_disabled", "unix_fallback", "plaintext"]
