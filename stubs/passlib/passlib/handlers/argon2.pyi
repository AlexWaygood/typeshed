"""passlib.handlers.argon2 -- argon2 password hash wrapper

References
==========
* argon2
    - home: https://github.com/P-H-C/phc-winner-argon2
    - whitepaper: https://github.com/P-H-C/phc-winner-argon2/blob/master/argon2-specs.pdf
* argon2 cffi wrapper
    - pypi: https://pypi.python.org/pypi/argon2_cffi
    - home: https://github.com/hynek/argon2_cffi
* argon2 pure python
    - pypi: https://pypi.python.org/pypi/argon2pure
    - home: https://github.com/bwesterb/argon2pure
"""

from typing import Any, ClassVar
from typing_extensions import Self

import passlib.utils.handlers as uh

class _DummyCffiHasher:
    """
    dummy object to use as source of defaults when argon2_cffi isn't present.
    this tries to mimic the attributes of ``argon2.PasswordHasher()`` which the rest of
    this module reads.

    .. note:: values last synced w/ argon2 19.2 as of 2019-11-09
    """

    time_cost: int
    memory_cost: int
    parallelism: int
    salt_len: int
    hash_len: int

class _Argon2Common(  # type: ignore[misc]
    uh.SubclassBackendMixin, uh.ParallelismMixin, uh.HasRounds, uh.HasRawSalt, uh.HasRawChecksum, uh.GenericHandler
):
    """
    Base class which implements brunt of Argon2 code.
    This is then subclassed by the various backends,
    to override w/ backend-specific methods.

    When a backend is loaded, the bases of the 'argon2' class proper
    are modified to prepend the correct backend-specific subclass.
    """

    name: ClassVar[str]
    checksum_size: ClassVar[int]
    default_salt_size: ClassVar[int]
    min_salt_size: ClassVar[int]
    max_salt_size: ClassVar[int]
    default_rounds: ClassVar[int]
    min_rounds: ClassVar[int]
    max_rounds: ClassVar[int]
    rounds_cost: ClassVar[str]
    max_parallelism: ClassVar[int]
    max_version: ClassVar[int]
    min_desired_version: ClassVar[int | None]
    min_memory_cost: ClassVar[int]
    max_threads: ClassVar[int]
    pure_use_threads: ClassVar[bool]
    def type_values(cls):
        """Function decorator which acts like a combination of classmethod+property (limited to read-only properties)"""
    type: str
    parallelism: int
    version: int
    memory_cost: int
    @property
    def type_d(self):
        """
        flag indicating a Type D hash

        .. deprecated:: 1.7.2; will be removed in passlib 2.0
        """
    data: Any
    @classmethod
    def using(  # type: ignore[override]
        cls,
        type=None,
        memory_cost=None,
        salt_len=None,
        time_cost=None,
        digest_size=None,
        checksum_size=None,
        hash_len=None,
        max_threads=None,
        **kwds,
    ): ...
    @classmethod
    def identify(cls, hash): ...
    @classmethod
    def from_string(cls, hash) -> Self: ...  # type: ignore[override]
    def __init__(self, type=None, type_d: bool = False, version=None, memory_cost=None, data=None, **kwds) -> None: ...

class _NoBackend(_Argon2Common):
    """
    mixin used before any backend has been loaded.
    contains stubs that force loading of one of the available backends.
    """

    @classmethod
    def hash(cls, secret): ...  # type: ignore[override]
    @classmethod
    def verify(cls, secret, hash): ...  # type: ignore[override]
    @classmethod
    def genhash(cls, secret, config): ...  # type: ignore[override]

class _CffiBackend(_Argon2Common):
    """
    argon2_cffi backend
    """

    @classmethod
    def hash(cls, secret): ...  # type: ignore[override]
    @classmethod
    def verify(cls, secret, hash): ...  # type: ignore[override]
    @classmethod
    def genhash(cls, secret, config): ...  # type: ignore[override]

class _PureBackend(_Argon2Common):
    """
    argon2pure backend
    """

class argon2(_NoBackend, _Argon2Common):  # type: ignore[misc]
    """
    This class implements the Argon2 password hash [#argon2-home]_, and follows the :ref:`password-hash-api`.

    Argon2 supports a variable-length salt, and variable time & memory cost,
    and a number of other configurable parameters.

    The :meth:`~passlib.ifc.PasswordHash.replace` method accepts the following optional keywords:

    :type type: str
    :param type:
        Specify the type of argon2 hash to generate.
        Can be one of "ID", "I", "D".

        This defaults to "ID" if supported by the backend, otherwise "I".

    :type salt: str
    :param salt:
        Optional salt string.
        If specified, the length must be between 0-1024 bytes.
        If not specified, one will be auto-generated (this is recommended).

    :type salt_size: int
    :param salt_size:
        Optional number of bytes to use when autogenerating new salts.

    :type rounds: int
    :param rounds:
        Optional number of rounds to use.
        This corresponds linearly to the amount of time hashing will take.

    :type time_cost: int
    :param time_cost:
        An alias for **rounds**, for compatibility with underlying argon2 library.

    :param int memory_cost:
        Defines the memory usage in kibibytes.
        This corresponds linearly to the amount of memory hashing will take.

    :param int parallelism:
        Defines the parallelization factor.
        *NOTE: this will affect the resulting hash value.*

    :param int digest_size:
        Length of the digest in bytes.

    :param int max_threads:
        Maximum number of threads that will be used.
        -1 means unlimited; otherwise hashing will use ``min(parallelism, max_threads)`` threads.

        .. note::

            This option is currently only honored by the argon2pure backend.

    :type relaxed: bool
    :param relaxed:
        By default, providing an invalid value for one of the other
        keywords will result in a :exc:`ValueError`. If ``relaxed=True``,
        and the error can be corrected, a :exc:`~passlib.exc.PasslibHashWarning`
        will be issued instead. Correctable errors include ``rounds``
        that are too small or too large, and ``salt`` strings that are too long.

    .. versionchanged:: 1.7.2

        Added the "type" keyword, and support for type "D" and "ID" hashes.
        (Prior versions could verify type "D" hashes, but not generate them).

    .. todo::

        * Support configurable threading limits.
    """

    backends: ClassVar[tuple[str, ...]]

__all__ = ["argon2"]
