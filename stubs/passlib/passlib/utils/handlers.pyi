"""passlib.handler - code for implementing handlers, and global registry for handlers"""

import abc
from _typeshed import Incomplete
from typing import Any, ClassVar
from typing_extensions import Self

from passlib.ifc import PasswordHash
from passlib.utils.binary import BASE64_CHARS, HASH64_CHARS, LOWER_HEX_CHARS, PADDED_BASE64_CHARS, UPPER_HEX_CHARS

H64_CHARS = HASH64_CHARS
B64_CHARS = BASE64_CHARS
PADDED_B64_CHARS = PADDED_BASE64_CHARS
UC_HEX_CHARS = UPPER_HEX_CHARS
LC_HEX_CHARS = LOWER_HEX_CHARS

def parse_mc2(hash, prefix, sep="$", handler=None):
    """parse hash using 2-part modular crypt format.

    this expects a hash of the format :samp:`{prefix}{salt}[${checksum}]`,
    such as md5_crypt, and parses it into salt / checksum portions.

    :arg hash: the hash to parse (bytes or unicode)
    :arg prefix: the identifying prefix (unicode)
    :param sep: field separator (unicode, defaults to ``$``).
    :param handler: handler class to pass to error constructors.

    :returns:
        a ``(salt, chk | None)`` tuple.
    """

def parse_mc3(hash, prefix, sep="$", rounds_base: int = 10, default_rounds=None, handler=None):
    """parse hash using 3-part modular crypt format.

    this expects a hash of the format :samp:`{prefix}[{rounds}]${salt}[${checksum}]`,
    such as sha1_crypt, and parses it into rounds / salt / checksum portions.
    tries to convert the rounds to an integer,
    and throws error if it has zero-padding.

    :arg hash: the hash to parse (bytes or unicode)
    :arg prefix: the identifying prefix (unicode)
    :param sep: field separator (unicode, defaults to ``$``).
    :param rounds_base:
        the numeric base the rounds are encoded in (defaults to base 10).
    :param default_rounds:
        the default rounds value to return if the rounds field was omitted.
        if this is ``None`` (the default), the rounds field is *required*.
    :param handler: handler class to pass to error constructors.

    :returns:
        a ``(rounds : int, salt, chk | None)`` tuple.
    """

def render_mc2(ident, salt, checksum, sep="$"):
    """format hash using 2-part modular crypt format; inverse of parse_mc2()

    returns native string with format :samp:`{ident}{salt}[${checksum}]`,
    such as used by md5_crypt.

    :arg ident: identifier prefix (unicode)
    :arg salt: encoded salt (unicode)
    :arg checksum: encoded checksum (unicode or None)
    :param sep: separator char (unicode, defaults to ``$``)

    :returns:
        config or hash (native str)
    """

def render_mc3(ident, rounds, salt, checksum, sep="$", rounds_base: int = 10):
    """format hash using 3-part modular crypt format; inverse of parse_mc3()

    returns native string with format :samp:`{ident}[{rounds}$]{salt}[${checksum}]`,
    such as used by sha1_crypt.

    :arg ident: identifier prefix (unicode)
    :arg rounds: rounds field (int or None)
    :arg salt: encoded salt (unicode)
    :arg checksum: encoded checksum (unicode or None)
    :param sep: separator char (unicode, defaults to ``$``)
    :param rounds_base: base to encode rounds value (defaults to base 10)

    :returns:
        config or hash (native str)
    """

class MinimalHandler(PasswordHash, metaclass=abc.ABCMeta):
    """
    helper class for implementing hash handlers.
    provides nothing besides a base implementation of the .using() subclass constructor.
    """

    @classmethod
    def using(cls, relaxed: bool = False) -> type[Self]: ...  # type: ignore[override]

class TruncateMixin(MinimalHandler, metaclass=abc.ABCMeta):
    """
    PasswordHash mixin which provides a method
    that will check if secret would be truncated,
    and can be configured to throw an error.

    .. warning::

        Hashers using this mixin will generally need to override
        the default PasswordHash.truncate_error policy of "True",
        and will similarly want to override .truncate_verify_reject as well.

        TODO: This should be done explicitly, but for now this mixin sets
        these flags implicitly.
    """

    truncate_error: ClassVar[bool]
    truncate_verify_reject: ClassVar[bool]
    @classmethod
    def using(cls, truncate_error: object = None, **kwds: Any) -> type[Self]: ...  # type: ignore[override]

class GenericHandler(MinimalHandler):
    """helper class for implementing hash handlers.

    GenericHandler-derived classes will have (at least) the following
    constructor options, though others may be added by mixins
    and by the class itself:

    :param checksum:
        this should contain the digest portion of a
        parsed hash (mainly provided when the constructor is called
        by :meth:`from_string()`).
        defaults to ``None``.

    :param use_defaults:
        If ``False`` (the default), a :exc:`TypeError` should be thrown
        if any settings required by the handler were not explicitly provided.

        If ``True``, the handler should attempt to provide a default for any
        missing values. This means generate missing salts, fill in default
        cost parameters, etc.

        This is typically only set to ``True`` when the constructor
        is called by :meth:`hash`, allowing user-provided values
        to be handled in a more permissive manner.

    :param relaxed:
        If ``False`` (the default), a :exc:`ValueError` should be thrown
        if any settings are out of bounds or otherwise invalid.

        If ``True``, they should be corrected if possible, and a warning
        issue. If not possible, only then should an error be raised.
        (e.g. under ``relaxed=True``, rounds values will be clamped
        to min/max rounds).

        This is mainly used when parsing the config strings of certain
        hashes, whose specifications implementations to be tolerant
        of incorrect values in salt strings.

    Class Attributes
    ================

    .. attribute:: ident

        [optional]
        If this attribute is filled in, the default :meth:`identify` method will use
        it as a identifying prefix that can be used to recognize instances of this handler's
        hash. Filling this out is recommended for speed.

        This should be a unicode str.

    .. attribute:: _hash_regex

        [optional]
        If this attribute is filled in, the default :meth:`identify` method
        will use it to recognize instances of the hash. If :attr:`ident`
        is specified, this will be ignored.

        This should be a unique regex object.

    .. attribute:: checksum_size

        [optional]
        Specifies the number of characters that should be expected in the checksum string.
        If omitted, no check will be performed.

    .. attribute:: checksum_chars

        [optional]
        A string listing all the characters allowed in the checksum string.
        If omitted, no check will be performed.

        This should be a unicode str.

    .. attribute:: _stub_checksum

        Placeholder checksum that will be used by genconfig()
        in lieu of actually generating a hash for the empty string.
        This should be a string of the same datatype as :attr:`checksum`.

    Instance Attributes
    ===================
    .. attribute:: checksum

        The checksum string provided to the constructor (after passing it
        through :meth:`_norm_checksum`).

    Required Subclass Methods
    =========================
    The following methods must be provided by handler subclass:

    .. automethod:: from_string
    .. automethod:: to_string
    .. automethod:: _calc_checksum

    Default Methods
    ===============
    The following methods have default implementations that should work for
    most cases, though they may be overridden if the hash subclass needs to:

    .. automethod:: _norm_checksum

    .. automethod:: genconfig
    .. automethod:: genhash
    .. automethod:: identify
    .. automethod:: hash
    .. automethod:: verify
    """

    setting_kwds: ClassVar[tuple[str, ...]]
    context_kwds: ClassVar[tuple[str, ...]]
    ident: ClassVar[str | None]
    checksum_size: ClassVar[int | None]
    checksum_chars: ClassVar[str | None]
    checksum: str | None
    use_defaults: bool
    def __init__(self, checksum: str | None = None, use_defaults: bool = False) -> None: ...
    @classmethod
    def identify(cls, hash: str | bytes) -> bool: ...
    @classmethod
    def from_string(cls, hash: str | bytes, **context: Any) -> Self:  # context parameters are passed to constructor
        """
        return parsed instance from hash/configuration string

        :param \\\\*\\\\*context:
            context keywords to pass to constructor (if applicable).

        :raises ValueError: if hash is incorrectly formatted

        :returns:
            hash parsed into components,
            for formatting / calculating checksum.
        """

    def to_string(self) -> str:
        """render instance to hash or configuration string

        :returns:
            hash string with salt & digest included.

            should return native string type (ascii-bytes under python 2,
            unicode under python 3)
        """

    @classmethod
    def hash(cls, secret: str | bytes, **kwds: Any) -> str: ...
    @classmethod
    def verify(cls, secret: str | bytes, hash: str | bytes, **context: Any) -> bool: ...
    @classmethod
    def genconfig(cls, **kwds: Any) -> str: ...
    @classmethod
    def genhash(cls, secret: str | bytes, config: str, **context: Any) -> str: ...
    @classmethod
    def needs_update(cls, hash: str | bytes, secret: str | bytes | None = None, **kwds: Any) -> bool: ...
    @classmethod
    def parsehash(cls, hash: str | bytes, checksum: bool = True, sanitize: bool = False) -> dict[str, Any]:
        """[experimental method] parse hash into dictionary of settings.

        this essentially acts as the inverse of :meth:`hash`: for most
        cases, if ``hash = cls.hash(secret, **opts)``, then
        ``cls.parsehash(hash)`` will return a dict matching the original options
        (with the extra keyword *checksum*).

        this method may not work correctly for all hashes,
        and may not be available on some few. its interface may
        change in future releases, if it's kept around at all.

        :arg hash: hash to parse
        :param checksum: include checksum keyword? (defaults to True)
        :param sanitize: mask data for sensitive fields? (defaults to False)
        """

    @classmethod
    def bitsize(cls, **kwds: Any) -> dict[str, Any]:
        """[experimental method] return info about bitsizes of hash"""

class StaticHandler(GenericHandler):
    """GenericHandler mixin for classes which have no settings.

    This mixin assumes the entirety of the hash ise stored in the
    :attr:`checksum` attribute; that the hash has no rounds, salt,
    etc. This class provides the following:

    * a default :meth:`genconfig` that always returns None.
    * a default :meth:`from_string` and :meth:`to_string`
      that store the entire hash within :attr:`checksum`,
      after optionally stripping a constant prefix.

    All that is required by subclasses is an implementation of
    the :meth:`_calc_checksum` method.
    """

    setting_kwds: ClassVar[tuple[str, ...]]

class HasEncodingContext(GenericHandler):
    """helper for classes which require knowledge of the encoding used"""

    default_encoding: ClassVar[str]
    encoding: str
    def __init__(self, encoding: str | None = None, **kwds) -> None: ...

class HasUserContext(GenericHandler):
    """helper for classes which require a user context keyword"""

    user: Incomplete | None
    def __init__(self, user=None, **kwds) -> None: ...
    @classmethod
    def hash(cls, secret, user=None, **context): ...
    @classmethod
    def verify(cls, secret, hash, user=None, **context): ...
    @classmethod
    def genhash(cls, secret, config, user=None, **context): ...

class HasRawChecksum(GenericHandler):
    """mixin for classes which work with decoded checksum bytes

    .. todo::

        document this class's usage
    """

class HasManyIdents(GenericHandler):
    """mixin for hashes which use multiple prefix identifiers

    For the hashes which may use multiple identifier prefixes,
    this mixin adds an ``ident`` keyword to constructor.
    Any value provided is passed through the :meth:`norm_idents` method,
    which takes care of validating the identifier,
    as well as allowing aliases for easier specification
    of the identifiers by the user.

    .. todo::

        document this class's usage

    Class Methods
    =============
    .. todo:: document using() and needs_update() options
    """

    default_ident: ClassVar[str | None]
    ident_values: ClassVar[tuple[str, ...] | None]
    ident_aliases: ClassVar[dict[str, str] | None]
    ident: str  # type: ignore[misc]
    @classmethod
    def using(cls, default_ident=None, ident=None, **kwds):  # type: ignore[override]
        """
        This mixin adds support for the following :meth:`~passlib.ifc.PasswordHash.using` keywords:

        :param default_ident:
            default identifier that will be used by resulting customized hasher.

        :param ident:
            supported as alternate alias for **default_ident**.
        """

    def __init__(self, ident=None, **kwds) -> None: ...

class HasSalt(GenericHandler):
    """mixin for validating salts.

    This :class:`GenericHandler` mixin adds a ``salt`` keyword to the class constuctor;
    any value provided is passed through the :meth:`_norm_salt` method,
    which takes care of validating salt length and content,
    as well as generating new salts if one it not provided.

    :param salt:
        optional salt string

    :param salt_size:
        optional size of salt (only used if no salt provided);
        defaults to :attr:`default_salt_size`.

    Class Attributes
    ================
    In order for :meth:`!_norm_salt` to do its job, the following
    attributes should be provided by the handler subclass:

    .. attribute:: min_salt_size

        The minimum number of characters allowed in a salt string.
        An :exc:`ValueError` will be throw if the provided salt is too small.
        Defaults to ``0``.

    .. attribute:: max_salt_size

        The maximum number of characters allowed in a salt string.
        By default an :exc:`ValueError` will be throw if the provided salt is
        too large; but if ``relaxed=True``, it will be clipped and a warning
        issued instead. Defaults to ``None``, for no maximum.

    .. attribute:: default_salt_size

        [required]
        If no salt is provided, this should specify the size of the salt
        that will be generated by :meth:`_generate_salt`. By default
        this will fall back to :attr:`max_salt_size`.

    .. attribute:: salt_chars

        A string containing all the characters which are allowed in the salt
        string. An :exc:`ValueError` will be throw if any other characters
        are encountered. May be set to ``None`` to skip this check (but see
        in :attr:`default_salt_chars`).

    .. attribute:: default_salt_chars

        [required]
        This attribute controls the set of characters use to generate
        *new* salt strings. By default, it mirrors :attr:`salt_chars`.
        If :attr:`!salt_chars` is ``None``, this attribute must be specified
        in order to generate new salts. Aside from that purpose,
        the main use of this attribute is for hashes which wish to generate
        salts from a restricted subset of :attr:`!salt_chars`; such as
        accepting all characters, but only using a-z.

    Instance Attributes
    ===================
    .. attribute:: salt

        This instance attribute will be filled in with the salt provided
        to the constructor (as adapted by :meth:`_norm_salt`)

    Subclassable Methods
    ====================
    .. automethod:: _norm_salt
    .. automethod:: _generate_salt
    """

    min_salt_size: ClassVar[int]
    max_salt_size: ClassVar[int | None]
    salt_chars: ClassVar[str | None]
    default_salt_size: ClassVar[int | None]
    default_salt_chars: ClassVar[str | None]
    salt: str | bytes | None
    @classmethod
    def using(  # type: ignore[override]
        cls, default_salt_size: int | None = None, salt_size: int | None = None, salt: str | bytes | None = None, **kwds
    ): ...
    def __init__(self, salt: str | bytes | None = None, **kwds) -> None: ...
    @classmethod
    def bitsize(cls, salt_size: int | None = None, **kwds):
        """[experimental method] return info about bitsizes of hash"""

class HasRawSalt(HasSalt):
    """mixin for classes which use decoded salt parameter

    A variant of :class:`!HasSalt` which takes in decoded bytes instead of an encoded string.

    .. todo::

        document this class's usage
    """

    salt_chars: ClassVar[bytes]  # type: ignore[assignment]

class HasRounds(GenericHandler):
    """mixin for validating rounds parameter

    This :class:`GenericHandler` mixin adds a ``rounds`` keyword to the class
    constuctor; any value provided is passed through the :meth:`_norm_rounds`
    method, which takes care of validating the number of rounds.

    :param rounds: optional number of rounds hash should use

    Class Attributes
    ================
    In order for :meth:`!_norm_rounds` to do its job, the following
    attributes must be provided by the handler subclass:

    .. attribute:: min_rounds

        The minimum number of rounds allowed. A :exc:`ValueError` will be
        thrown if the rounds value is too small. Defaults to ``0``.

    .. attribute:: max_rounds

        The maximum number of rounds allowed. A :exc:`ValueError` will be
        thrown if the rounds value is larger than this. Defaults to ``None``
        which indicates no limit to the rounds value.

    .. attribute:: default_rounds

        If no rounds value is provided to constructor, this value will be used.
        If this is not specified, a rounds value *must* be specified by the
        application.

    .. attribute:: rounds_cost

        [required]
        The ``rounds`` parameter typically encodes a cpu-time cost
        for calculating a hash. This should be set to ``"linear"``
        (the default) or ``"log2"``, depending on how the rounds value relates
        to the actual amount of time that will be required.

    Class Methods
    =============
    .. todo:: document using() and needs_update() options

    Instance Attributes
    ===================
    .. attribute:: rounds

        This instance attribute will be filled in with the rounds value provided
        to the constructor (as adapted by :meth:`_norm_rounds`)

    Subclassable Methods
    ====================
    .. automethod:: _norm_rounds
    """

    min_rounds: ClassVar[int]
    max_rounds: ClassVar[int | None]
    rounds_cost: ClassVar[str]
    using_rounds_kwds: ClassVar[tuple[str, ...]]
    min_desired_rounds: ClassVar[int | None]
    max_desired_rounds: ClassVar[int | None]
    default_rounds: ClassVar[int | None]
    vary_rounds: ClassVar[Incomplete | None]
    rounds: int
    @classmethod
    def using(  # type: ignore[override]
        cls,
        min_desired_rounds=None,
        max_desired_rounds=None,
        default_rounds=None,
        vary_rounds=None,
        min_rounds=None,
        max_rounds=None,
        rounds=None,
        **kwds,
    ): ...
    def __init__(self, rounds=None, **kwds) -> None: ...
    @classmethod
    def bitsize(cls, rounds=None, vary_rounds: float = 0.1, **kwds):
        """[experimental method] return info about bitsizes of hash"""

class ParallelismMixin(GenericHandler):
    """
    mixin which provides common behavior for 'parallelism' setting
    """

    parallelism: int
    @classmethod
    def using(cls, parallelism=None, **kwds): ...  # type: ignore[override]
    def __init__(self, parallelism=None, **kwds) -> None: ...

class BackendMixin(PasswordHash, metaclass=abc.ABCMeta):
    """
    PasswordHash mixin which provides generic framework for supporting multiple backends
    within the class.

    Public API
    ----------

    .. attribute:: backends

        This attribute should be a tuple containing the names of the backends
        which are supported. Two common names are ``"os_crypt"`` (if backend
        uses :mod:`crypt`), and ``"builtin"`` (if the backend is a pure-python
        fallback).

    .. automethod:: get_backend
    .. automethod:: set_backend
    .. automethod:: has_backend

    .. warning::

        :meth:`set_backend` is intended to be called during application startup --
        it affects global state, and switching backends is not guaranteed threadsafe.

    Private API (Subclass Hooks)
    ----------------------------
    Subclasses should set the :attr:`!backends` attribute to a tuple of the backends
    they wish to support.  They should also define one method:

    .. classmethod:: _load_backend_{name}(dryrun=False)

        One copy of this method should be defined for each :samp:`name` within :attr:`!backends`.

        It will be called in order to load the backend, and should take care of whatever
        is needed to enable the backend.  This may include importing modules, running tests,
        issuing warnings, etc.

        :param name:
            [Optional] name of backend.

        :param dryrun:
            [Optional] True/False if currently performing a "dry run".

            if True, the method should perform all setup actions *except*
            switching the class over to the new backend.

        :raises passlib.exc.PasslibSecurityError:
            if the backend is available, but cannot be loaded due to a security issue.

        :returns:
            False if backend not available, True if backend loaded.

        .. warning::

            Due to the way passlib's internals are arranged,
            backends should generally store stateful data at the class level
            (not the module level), and be prepared to be called on subclasses
            which may be set to a different backend from their parent.

            (Idempotent module-level data such as lazy imports are fine).

    .. automethod:: _finalize_backend

    .. versionadded:: 1.7
    """

    backends: ClassVar[tuple[str, ...] | None]
    @classmethod
    def get_backend(cls):
        """
        Return name of currently active backend.
        if no backend has been loaded, loads and returns name of default backend.

        :raises passlib.exc.MissingBackendError:
            if no backends are available.

        :returns:
            name of active backend
        """

    @classmethod
    def has_backend(cls, name: str = "any") -> bool:
        """
        Check if support is currently available for specified backend.

        :arg name:
            name of backend to check for.
            can be any string accepted by :meth:`set_backend`.

        :raises ValueError:
            if backend name is unknown

        :returns:
            * ``True`` if backend is available.
            * ``False`` if it's available / can't be loaded.
            * ``None`` if it's present, but won't load due to a security issue.
        """

    @classmethod
    def set_backend(cls, name: str = "any", dryrun: bool = False):
        """
        Load specified backend.

        :arg name:
            name of backend to load, can be any of the following:

            * ``"any"`` -- use current backend if one is loaded,
              otherwise load the first available backend.

            * ``"default"`` -- use the first available backend.

            * any string in :attr:`backends`, loads specified backend.

        :param dryrun:
            If True, this perform all setup actions *except* switching over to the new backend.
            (this flag is used to implement :meth:`has_backend`).

            .. versionadded:: 1.7

        :raises ValueError:
            If backend name is unknown.

        :raises passlib.exc.MissingBackendError:
            If specific backend is missing;
            or in the case of ``"any"`` / ``"default"``, if *no* backends are available.

        :raises passlib.exc.PasslibSecurityError:

            If ``"any"`` or ``"default"`` was specified,
            but the only backend available has a PasslibSecurityError.
        """

class SubclassBackendMixin(BackendMixin, metaclass=abc.ABCMeta):
    """
    variant of BackendMixin which allows backends to be implemented
    as separate mixin classes, and dynamically switches them out.

    backend classes should implement a _load_backend() classmethod,
    which will be invoked with an optional 'dryrun' keyword,
    and should return True or False.

    _load_backend() will be invoked with ``cls`` equal to the mixin,
    *not* the overall class.

    .. versionadded:: 1.7
    """

class HasManyBackends(BackendMixin, GenericHandler):
    """
    GenericHandler mixin which provides selecting from multiple backends.

    .. todo::

        finish documenting this class's usage

    For hashes which need to select from multiple backends,
    depending on the host environment, this class
    offers a way to specify alternate :meth:`_calc_checksum` methods,
    and will dynamically chose the best one at runtime.

    .. versionchanged:: 1.7

        This class now derives from :class:`BackendMixin`, which abstracts
        out a more generic framework for supporting multiple backends.
        The public api (:meth:`!get_backend`, :meth:`!has_backend`, :meth:`!set_backend`)
        is roughly the same.

    Private API (Subclass Hooks)
    ----------------------------
    As of version 1.7, classes should implement :meth:`!_load_backend_{name}`, per
    :class:`BackendMixin`.  This hook should invoke :meth:`!_set_calc_checksum_backcend`
    to install it's backend method.

    .. deprecated:: 1.7

        The following api is deprecated, and will be removed in Passlib 2.0:

    .. attribute:: _has_backend_{name}

        private class attribute checked by :meth:`has_backend` to see if a
        specific backend is available, it should be either ``True``
        or ``False``. One of these should be provided by
        the subclass for each backend listed in :attr:`backends`.

    .. classmethod:: _calc_checksum_{name}

        private class method that should implement :meth:`_calc_checksum`
        for a given backend. it will only be called if the backend has
        been selected by :meth:`set_backend`. One of these should be provided
        by the subclass for each backend listed in :attr:`backends`.
    """

class PrefixWrapper:
    """wraps another handler, adding a constant prefix.

    instances of this class wrap another password hash handler,
    altering the constant prefix that's prepended to the wrapped
    handlers' hashes.

    this is used mainly by the :doc:`ldap crypt <passlib.hash.ldap_crypt>` handlers;
    such as :class:`~passlib.hash.ldap_md5_crypt` which wraps :class:`~passlib.hash.md5_crypt` and adds a ``{CRYPT}`` prefix.

    usage::

        myhandler = PrefixWrapper("myhandler", "md5_crypt", prefix="$mh$", orig_prefix="$1$")

    :param name: name to assign to handler
    :param wrapped: handler object or name of registered handler
    :param prefix: identifying prefix to prepend to all hashes
    :param orig_prefix: prefix to strip (defaults to '').
    :param lazy: if True and wrapped handler is specified by name, don't look it up until needed.
    """

    name: Any
    prefix: Any
    orig_prefix: Any
    __doc__: Any
    def __init__(self, name, wrapped, prefix="", orig_prefix="", lazy: bool = False, doc=None, ident=None) -> None: ...
    @property
    def wrapped(self): ...
    @property
    def ident(self): ...
    @property
    def ident_values(self): ...
    def __dir__(self): ...
    def __getattr__(self, attr: str):
        """proxy most attributes from wrapped class (e.g. rounds, salt size, etc)"""

    def __setattr__(self, attr: str, value) -> None: ...
    def using(self, **kwds): ...
    def needs_update(self, hash, **kwds): ...
    def identify(self, hash): ...
    def genconfig(self, **kwds): ...
    def genhash(self, secret, config, **kwds): ...
    def encrypt(self, secret, **kwds): ...
    def hash(self, secret, **kwds): ...
    def verify(self, secret, hash, **kwds): ...

__all__ = [
    # helpers for implementing MCF handlers
    "parse_mc2",
    "parse_mc3",
    "render_mc2",
    "render_mc3",
    # framework for implementing handlers
    "GenericHandler",
    "StaticHandler",
    "HasUserContext",
    "HasRawChecksum",
    "HasManyIdents",
    "HasSalt",
    "HasRawSalt",
    "HasRounds",
    "HasManyBackends",
    # other helpers
    "PrefixWrapper",
]
