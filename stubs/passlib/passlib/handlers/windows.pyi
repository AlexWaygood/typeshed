"""passlib.handlers.nthash - Microsoft Windows -related hashes"""

from typing import Any, ClassVar, Literal, overload

import passlib.utils.handlers as uh

class lmhash(uh.TruncateMixin, uh.HasEncodingContext, uh.StaticHandler):
    """This class implements the Lan Manager Password hash, and follows the :ref:`password-hash-api`.

    It has no salt and a single fixed round.

    The :meth:`~passlib.ifc.PasswordHash.using` method accepts a single
    optional keyword:

    :param bool truncate_error:
        By default, this will silently truncate passwords larger than 14 bytes.
        Setting ``truncate_error=True`` will cause :meth:`~passlib.ifc.PasswordHash.hash`
        to raise a :exc:`~passlib.exc.PasswordTruncateError` instead.

        .. versionadded:: 1.7

    The :meth:`~passlib.ifc.PasswordHash.hash` and :meth:`~passlib.ifc.PasswordHash.verify` methods accept a single
    optional keyword:

    :type encoding: str
    :param encoding:

        This specifies what character encoding LMHASH should use when
        calculating digest. It defaults to ``cp437``, the most
        common encoding encountered.

    Note that while this class outputs digests in lower-case hexadecimal,
    it will accept upper-case as well.
    """

    name: ClassVar[str]
    checksum_chars: ClassVar[str]
    checksum_size: ClassVar[int]
    truncate_size: ClassVar[int]
    @classmethod
    def raw(cls, secret, encoding=None):
        """encode password using LANMAN hash algorithm.

        :type secret: unicode or utf-8 encoded bytes
        :arg secret: secret to hash
        :type encoding: str
        :arg encoding:
            optional encoding to use for unicode inputs.
            this defaults to ``cp437``, which is the
            common case for most situations.

        :returns: returns string of raw bytes
        """

class nthash(uh.StaticHandler):
    """This class implements the NT Password hash, and follows the :ref:`password-hash-api`.

    It has no salt and a single fixed round.

    The :meth:`~passlib.ifc.PasswordHash.hash` and :meth:`~passlib.ifc.PasswordHash.genconfig` methods accept no optional keywords.

    Note that while this class outputs lower-case hexadecimal digests,
    it will accept upper-case digests as well.
    """

    name: ClassVar[str]
    checksum_chars: ClassVar[str]
    checksum_size: ClassVar[int]
    @classmethod
    def raw(cls, secret):
        """encode password using MD4-based NTHASH algorithm

        :arg secret: secret as unicode or utf-8 encoded bytes

        :returns: returns string of raw bytes
        """

    @overload
    @classmethod
    def raw_nthash(cls, secret: str | bytes, hex: Literal[True]) -> str: ...
    @overload
    @classmethod
    def raw_nthash(cls, secret: str | bytes, hex: Literal[False] = False) -> bytes: ...
    @overload
    @classmethod
    def raw_nthash(cls, secret: str | bytes, hex: bool = False) -> str | bytes: ...

bsd_nthash: Any

class msdcc(uh.HasUserContext, uh.StaticHandler):
    """This class implements Microsoft's Domain Cached Credentials password hash,
    and follows the :ref:`password-hash-api`.

    It has a fixed number of rounds, and uses the associated
    username as the salt.

    The :meth:`~passlib.ifc.PasswordHash.hash`, :meth:`~passlib.ifc.PasswordHash.genhash`, and :meth:`~passlib.ifc.PasswordHash.verify` methods
    have the following optional keywords:

    :type user: str
    :param user:
        String containing name of user account this password is associated with.
        This is required to properly calculate the hash.

        This keyword is case-insensitive, and should contain just the username
        (e.g. ``Administrator``, not ``SOMEDOMAIN\\Administrator``).

    Note that while this class outputs lower-case hexadecimal digests,
    it will accept upper-case digests as well.
    """

    name: ClassVar[str]
    checksum_chars: ClassVar[str]
    checksum_size: ClassVar[int]
    @classmethod
    def raw(cls, secret, user):
        """encode password using mscash v1 algorithm

        :arg secret: secret as unicode or utf-8 encoded bytes
        :arg user: username to use as salt

        :returns: returns string of raw bytes
        """

class msdcc2(uh.HasUserContext, uh.StaticHandler):
    """This class implements version 2 of Microsoft's Domain Cached Credentials
    password hash, and follows the :ref:`password-hash-api`.

    It has a fixed number of rounds, and uses the associated
    username as the salt.

    The :meth:`~passlib.ifc.PasswordHash.hash`, :meth:`~passlib.ifc.PasswordHash.genhash`, and :meth:`~passlib.ifc.PasswordHash.verify` methods
    have the following extra keyword:

    :type user: str
    :param user:
        String containing name of user account this password is associated with.
        This is required to properly calculate the hash.

        This keyword is case-insensitive, and should contain just the username
        (e.g. ``Administrator``, not ``SOMEDOMAIN\\Administrator``).
    """

    name: ClassVar[str]
    checksum_chars: ClassVar[str]
    checksum_size: ClassVar[int]
    @classmethod
    def raw(cls, secret, user):
        """encode password using msdcc v2 algorithm

        :type secret: unicode or utf-8 bytes
        :arg secret: secret

        :type user: str
        :arg user: username to use as salt

        :returns: returns string of raw bytes
        """

__all__ = ["lmhash", "nthash", "bsd_nthash", "msdcc", "msdcc2"]
