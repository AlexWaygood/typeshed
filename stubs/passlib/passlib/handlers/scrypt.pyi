"""passlib.handlers.scrypt -- scrypt password hash"""

from typing import ClassVar
from typing_extensions import Self

import passlib.utils.handlers as uh

class scrypt(uh.ParallelismMixin, uh.HasRounds, uh.HasRawSalt, uh.HasRawChecksum, uh.HasManyIdents, uh.GenericHandler):  # type: ignore[misc]
    """This class implements an SCrypt-based password [#scrypt-home]_ hash, and follows the :ref:`password-hash-api`.

    It supports a variable-length salt, a variable number of rounds,
    as well as some custom tuning parameters unique to scrypt (see below).

    The :meth:`~passlib.ifc.PasswordHash.using` method accepts the following optional keywords:

    :type salt: str
    :param salt:
        Optional salt string.
        If specified, the length must be between 0-1024 bytes.
        If not specified, one will be auto-generated (this is recommended).

    :type salt_size: int
    :param salt_size:
        Optional number of bytes to use when autogenerating new salts.
        Defaults to 16 bytes, but can be any value between 0 and 1024.

    :type rounds: int
    :param rounds:
        Optional number of rounds to use.
        Defaults to 16, but must be within ``range(1,32)``.

        .. warning::

            Unlike many hash algorithms, increasing the rounds value
            will increase both the time *and memory* required to hash a password.

    :type block_size: int
    :param block_size:
        Optional block size to pass to scrypt hash function (the ``r`` parameter).
        Useful for tuning scrypt to optimal performance for your CPU architecture.
        Defaults to 8.

    :type parallelism: int
    :param parallelism:
        Optional parallelism to pass to scrypt hash function (the ``p`` parameter).
        Defaults to 1.

    :type relaxed: bool
    :param relaxed:
        By default, providing an invalid value for one of the other
        keywords will result in a :exc:`ValueError`. If ``relaxed=True``,
        and the error can be corrected, a :exc:`~passlib.exc.PasslibHashWarning`
        will be issued instead. Correctable errors include ``rounds``
        that are too small or too large, and ``salt`` strings that are too long.

    .. note::

        The underlying scrypt hash function has a number of limitations
        on it's parameter values, which forbids certain combinations of settings.
        The requirements are:

        * ``linear_rounds = 2**<some positive integer>``
        * ``linear_rounds < 2**(16 * block_size)``
        * ``block_size * parallelism <= 2**30-1``

    .. todo::

        This class currently does not support configuring default values
        for ``block_size`` or ``parallelism`` via a :class:`~passlib.context.CryptContext`
        configuration.
    """

    backends: ClassVar[tuple[str, ...]]
    name: ClassVar[str]
    checksum_size: ClassVar[int]
    default_ident: ClassVar[str]
    ident_values: ClassVar[tuple[str, ...]]
    default_salt_size: ClassVar[int]
    max_salt_size: ClassVar[int]
    default_rounds: ClassVar[int]
    min_rounds: ClassVar[int]
    max_rounds: ClassVar[int]
    rounds_cost: ClassVar[str]
    parallelism: int
    block_size: int
    @classmethod
    def using(cls, block_size=None, **kwds): ...  # type: ignore[override]
    @classmethod
    def from_string(cls, hash) -> Self: ...  # type: ignore[override]
    @classmethod
    def parse(cls, hash): ...
    def to_string(self): ...
    def __init__(self, block_size=None, **kwds) -> None: ...
    @classmethod
    def get_backend(cls): ...
    @classmethod
    def has_backend(cls, name: str = "any"): ...
    @classmethod
    def set_backend(cls, name: str = "any", dryrun: bool = False) -> None: ...

__all__ = ["scrypt"]
