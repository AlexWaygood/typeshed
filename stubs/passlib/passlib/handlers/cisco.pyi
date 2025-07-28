"""
passlib.handlers.cisco -- Cisco password hashes
"""

from typing import ClassVar
from typing_extensions import Self

import passlib.utils.handlers as uh

class cisco_pix(uh.HasUserContext, uh.StaticHandler):
    """
    This class implements the password hash used by older Cisco PIX firewalls,
    and follows the :ref:`password-hash-api`.
    It does a single round of hashing, and relies on the username
    as the salt.

    This class only allows passwords <= 16 bytes, anything larger
    will result in a :exc:`~passlib.exc.PasswordSizeError` if passed to :meth:`~cisco_pix.hash`,
    and be silently rejected if passed to :meth:`~cisco_pix.verify`.

    The :meth:`~passlib.ifc.PasswordHash.hash`,
    :meth:`~passlib.ifc.PasswordHash.genhash`, and
    :meth:`~passlib.ifc.PasswordHash.verify` methods
    all support the following extra keyword:

    :param str user:
        String containing name of user account this password is associated with.

        This is *required* in order to correctly hash passwords associated
        with a user account on the Cisco device, as it is used to salt
        the hash.

        Conversely, this *must* be omitted or set to ``""`` in order to correctly
        hash passwords which don't have an associated user account
        (such as the "enable" password).

    .. versionadded:: 1.6

    .. versionchanged:: 1.7.1

        Passwords > 16 bytes are now rejected / throw error instead of being silently truncated,
        to match Cisco behavior.  A number of :ref:`bugs <passlib-asa96-bug>` were fixed
        which caused prior releases to generate unverifiable hashes in certain cases.
    """

    name: ClassVar[str]
    truncate_size: ClassVar[int]
    truncate_error: ClassVar[bool]
    truncate_verify_reject: ClassVar[bool]
    checksum_size: ClassVar[int]
    checksum_chars: ClassVar[str]

class cisco_asa(cisco_pix):
    """
    This class implements the password hash used by Cisco ASA/PIX 7.0 and newer (2005).
    Aside from a different internal algorithm, it's use and format is identical
    to the older :class:`cisco_pix` class.

    For passwords less than 13 characters, this should be identical to :class:`!cisco_pix`,
    but will generate a different hash for most larger inputs
    (See the `Format & Algorithm`_ section for the details).

    This class only allows passwords <= 32 bytes, anything larger
    will result in a :exc:`~passlib.exc.PasswordSizeError` if passed to :meth:`~cisco_asa.hash`,
    and be silently rejected if passed to :meth:`~cisco_asa.verify`.

    .. versionadded:: 1.7

    .. versionchanged:: 1.7.1

        Passwords > 32 bytes are now rejected / throw error instead of being silently truncated,
        to match Cisco behavior.  A number of :ref:`bugs <passlib-asa96-bug>` were fixed
        which caused prior releases to generate unverifiable hashes in certain cases.
    """

class cisco_type7(uh.GenericHandler):
    """
    This class implements the "Type 7" password encoding used by Cisco IOS,
    and follows the :ref:`password-hash-api`.
    It has a simple 4-5 bit salt, but is nonetheless a reversible encoding
    instead of a real hash.

    The :meth:`~passlib.ifc.PasswordHash.using` method accepts the following optional keywords:

    :type salt: int
    :param salt:
        This may be an optional salt integer drawn from ``range(0,16)``.
        If omitted, one will be chosen at random.

    :type relaxed: bool
    :param relaxed:
        By default, providing an invalid value for one of the other
        keywords will result in a :exc:`ValueError`. If ``relaxed=True``,
        and the error can be corrected, a :exc:`~passlib.exc.PasslibHashWarning`
        will be issued instead. Correctable errors include
        ``salt`` values that are out of range.

    Note that while this class outputs digests in upper-case hexadecimal,
    it will accept lower-case as well.

    This class also provides the following additional method:

    .. automethod:: decode
    """

    name: ClassVar[str]
    checksum_chars: ClassVar[str]
    min_salt_value: ClassVar[int]
    max_salt_value: ClassVar[int]
    @classmethod
    def using(cls, salt: int | None = None, **kwds): ...  # type: ignore[override]
    @classmethod
    def from_string(cls, hash) -> Self: ...  # type: ignore[override]
    salt: int
    def __init__(self, salt: int | None = None, **kwds) -> None: ...
    @classmethod
    def decode(cls, hash, encoding: str = "utf-8"):
        """decode hash, returning original password.

        :arg hash: encoded password
        :param encoding: optional encoding to use (defaults to ``UTF-8``).
        :returns: password as unicode
        """

__all__ = ["cisco_pix", "cisco_asa", "cisco_type7"]
