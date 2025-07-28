"""passlib.ifc - abstract interfaces used by Passlib"""

from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar, Literal
from typing_extensions import Self

class PasswordHash(metaclass=ABCMeta):
    """This class describes an abstract interface which all password hashes
    in Passlib adhere to. Under Python 2.6 and up, this is an actual
    Abstract Base Class built using the :mod:`!abc` module.

    See the Passlib docs for full documentation.
    """

    is_disabled: ClassVar[bool]
    truncate_size: ClassVar[int | None]
    truncate_error: ClassVar[bool]
    truncate_verify_reject: ClassVar[bool]
    @classmethod
    @abstractmethod
    def hash(cls, secret: str | bytes, **setting_and_context_kwds) -> str:
        """
        Hash secret, returning result.
        Should handle generating salt, etc, and should return string
        containing identifier, salt & other configuration, as well as digest.

        :param \\\\*\\\\*settings_kwds:

            Pass in settings to customize configuration of resulting hash.

            .. deprecated:: 1.7

                Starting with Passlib 1.7, callers should no longer pass settings keywords
                (e.g. ``rounds`` or ``salt`` directly to :meth:`!hash`); should use
                ``.using(**settings).hash(secret)`` construction instead.

                Support will be removed in Passlib 2.0.

        :param \\\\*\\\\*context_kwds:

            Specific algorithms may require context-specific information (such as the user login).
        """

    @classmethod
    def encrypt(cls, secret: str | bytes, **kwds) -> str:
        """
        Legacy alias for :meth:`hash`.

        .. deprecated:: 1.7
            This method was renamed to :meth:`!hash` in version 1.7.
            This alias will be removed in version 2.0, and should only
            be used for compatibility with Passlib 1.3 - 1.6.
        """

    @classmethod
    @abstractmethod
    def verify(cls, secret: str | bytes, hash: str | bytes, **context_kwds):
        """verify secret against hash, returns True/False"""

    @classmethod
    @abstractmethod
    def using(cls, relaxed: bool = False, **kwds: Any) -> type[Self]:
        """
        Return another hasher object (typically a subclass of the current one),
        which integrates the configuration options specified by ``kwds``.
        This should *always* return a new object, even if no configuration options are changed.

        .. todo::

            document which options are accepted.

        :returns:
            typically returns a subclass for most hasher implementations.

        .. todo::

            add this method to main documentation.
        """

    @classmethod
    def needs_update(cls, hash: str, secret: str | bytes | None = None) -> bool:
        """
        check if hash's configuration is outside desired bounds,
        or contains some other internal option which requires
        updating the password hash.

        :param hash:
            hash string to examine

        :param secret:
            optional secret known to have verified against the provided hash.
            (this is used by some hashes to detect legacy algorithm mistakes).

        :return:
            whether secret needs re-hashing.

        .. versionadded:: 1.7
        """

    @classmethod
    @abstractmethod
    def identify(cls, hash: str | bytes) -> bool:
        """check if hash belongs to this scheme, returns True/False"""

    @classmethod
    def genconfig(cls, **setting_kwds: Any) -> str:
        """
        compile settings into a configuration string for genhash()

        .. deprecated:: 1.7

            As of 1.7, this method is deprecated, and slated for complete removal in Passlib 2.0.

            For all known real-world uses, hashing a constant string
            should provide equivalent functionality.

            This deprecation may be reversed if a use-case presents itself in the mean time.
        """

    @classmethod
    def genhash(cls, secret: str | bytes, config: str, **context: Any) -> str:
        """
        generated hash for secret, using settings from config/hash string

        .. deprecated:: 1.7

            As of 1.7, this method is deprecated, and slated for complete removal in Passlib 2.0.

            This deprecation may be reversed if a use-case presents itself in the mean time.
        """
    deprecated: bool

class DisabledHash(PasswordHash, metaclass=ABCMeta):
    """
    extended disabled-hash methods; only need be present if .disabled = True
    """

    is_disabled: ClassVar[Literal[True]]
    @classmethod
    def disable(cls, hash: str | None = None) -> str:
        """
        return string representing a 'disabled' hash;
        optionally including previously enabled hash
        (this is up to the individual scheme).
        """

    @classmethod
    def enable(cls, hash: str) -> str:
        """
        given a disabled-hash string,
        extract previously-enabled hash if one is present,
        otherwise raises ValueError
        """

__all__ = ["PasswordHash"]
