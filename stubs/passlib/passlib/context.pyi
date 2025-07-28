"""passlib.context - CryptContext implementation"""

from _typeshed import StrOrBytesPath, SupportsItems
from typing import Any
from typing_extensions import Self

class CryptPolicy:
    """
    .. deprecated:: 1.6
        This class has been deprecated, and will be removed in Passlib 1.8.
        All of its functionality has been rolled into :class:`CryptContext`.

    This class previously stored the configuration options for the
    CryptContext class. In the interest of interface simplification,
    all of this class' functionality has been rolled into the CryptContext
    class itself.
    The documentation for this class is now focused on  documenting how to
    migrate to the new api. Additionally, where possible, the deprecation
    warnings issued by the CryptPolicy methods will list the replacement call
    that should be used.

    Constructors
    ============
    CryptPolicy objects can be constructed directly using any of
    the keywords accepted by :class:`CryptContext`. Direct uses of the
    :class:`!CryptPolicy` constructor should either pass the keywords
    directly into the CryptContext constructor, or to :meth:`CryptContext.update`
    if the policy object was being used to update an existing context object.

    In addition to passing in keywords directly,
    CryptPolicy objects can be constructed by the following methods:

    .. automethod:: from_path
    .. automethod:: from_string
    .. automethod:: from_source
    .. automethod:: from_sources
    .. automethod:: replace

    Introspection
    =============
    All of the informational methods provided by this class have been deprecated
    by identical or similar methods in the :class:`CryptContext` class:

    .. automethod:: has_schemes
    .. automethod:: schemes
    .. automethod:: iter_handlers
    .. automethod:: get_handler
    .. automethod:: get_options
    .. automethod:: handler_is_deprecated
    .. automethod:: get_min_verify_time

    Exporting
    =========
    .. automethod:: iter_config
    .. automethod:: to_dict
    .. automethod:: to_file
    .. automethod:: to_string

    .. note::
        CryptPolicy are immutable.
        Use the :meth:`replace` method to mutate existing instances.

    .. deprecated:: 1.6
    """

    @classmethod
    def from_path(cls, path, section: str = "passlib", encoding: str = "utf-8"):
        """create a CryptPolicy instance from a local file.

        .. deprecated:: 1.6

        Creating a new CryptContext from a file, which was previously done via
        ``CryptContext(policy=CryptPolicy.from_path(path))``, can now be
        done via ``CryptContext.from_path(path)``.
        See :meth:`CryptContext.from_path` for details.

        Updating an existing CryptContext from a file, which was previously done
        ``context.policy = CryptPolicy.from_path(path)``, can now be
        done via ``context.load_path(path)``.
        See :meth:`CryptContext.load_path` for details.
        """

    @classmethod
    def from_string(cls, source, section: str = "passlib", encoding: str = "utf-8"):
        """create a CryptPolicy instance from a string.

        .. deprecated:: 1.6

        Creating a new CryptContext from a string, which was previously done via
        ``CryptContext(policy=CryptPolicy.from_string(data))``, can now be
        done via ``CryptContext.from_string(data)``.
        See :meth:`CryptContext.from_string` for details.

        Updating an existing CryptContext from a string, which was previously done
        ``context.policy = CryptPolicy.from_string(data)``, can now be
        done via ``context.load(data)``.
        See :meth:`CryptContext.load` for details.
        """

    @classmethod
    def from_source(cls, source, _warn: bool = True):
        """create a CryptPolicy instance from some source.

        this method autodetects the source type, and invokes
        the appropriate constructor automatically. it attempts
        to detect whether the source is a configuration string, a filepath,
        a dictionary, or an existing CryptPolicy instance.

        .. deprecated:: 1.6

        Create a new CryptContext, which could previously be done via
        ``CryptContext(policy=CryptPolicy.from_source(source))``, should
        now be done using an explicit method: the :class:`CryptContext`
        constructor itself, :meth:`CryptContext.from_path`,
        or :meth:`CryptContext.from_string`.

        Updating an existing CryptContext, which could previously be done via
        ``context.policy = CryptPolicy.from_source(source)``, should
        now be done using an explicit method: :meth:`CryptContext.update`,
        or :meth:`CryptContext.load`.
        """

    @classmethod
    def from_sources(cls, sources, _warn: bool = True):
        """create a CryptPolicy instance by merging multiple sources.

        each source is interpreted as by :meth:`from_source`,
        and the results are merged together.

        .. deprecated:: 1.6
            Instead of using this method to merge multiple policies together,
            a :class:`CryptContext` instance should be created, and then
            the multiple sources merged together via :meth:`CryptContext.load`.
        """

    def replace(self, *args, **kwds):
        """create a new CryptPolicy, optionally updating parts of the
        existing configuration.

        .. deprecated:: 1.6
            Callers of this method should :meth:`CryptContext.update` or
            :meth:`CryptContext.copy` instead.
        """

    def __init__(self, *args, **kwds) -> None: ...
    def has_schemes(self):
        """return True if policy defines *any* schemes for use.

        .. deprecated:: 1.6
            applications should use ``bool(context.schemes())`` instead.
            see :meth:`CryptContext.schemes`.
        """

    def iter_handlers(self):
        """return iterator over handlers defined in policy.

        .. deprecated:: 1.6
            applications should use ``context.schemes(resolve=True))`` instead.
            see :meth:`CryptContext.schemes`.
        """

    def schemes(self, resolve: bool = False):
        """return list of schemes defined in policy.

        .. deprecated:: 1.6
            applications should use :meth:`CryptContext.schemes` instead.
        """

    def get_handler(self, name=None, category=None, required: bool = False):
        """return handler as specified by name, or default handler.

        .. deprecated:: 1.6
            applications should use :meth:`CryptContext.handler` instead,
            though note that the ``required`` keyword has been removed,
            and the new method will always act as if ``required=True``.
        """

    def get_min_verify_time(self, category=None):
        """get min_verify_time setting for policy.

        .. deprecated:: 1.6
            min_verify_time option will be removed entirely in passlib 1.8

        .. versionchanged:: 1.7
            this method now always returns the value automatically
            calculated by :meth:`CryptContext.min_verify_time`,
            any value specified by policy is ignored.
        """

    def get_options(self, name, category=None):
        """return dictionary of options specific to a given handler.

        .. deprecated:: 1.6
            this method has no direct replacement in the 1.6 api, as there
            is not a clearly defined use-case. however, examining the output of
            :meth:`CryptContext.to_dict` should serve as the closest alternative.
        """

    def handler_is_deprecated(self, name, category=None):
        """check if handler has been deprecated by policy.

        .. deprecated:: 1.6
            this method has no direct replacement in the 1.6 api, as there
            is not a clearly defined use-case. however, examining the output of
            :meth:`CryptContext.to_dict` should serve as the closest alternative.
        """

    def iter_config(self, ini: bool = False, resolve: bool = False):
        """iterate over key/value pairs representing the policy object.

        .. deprecated:: 1.6
            applications should use :meth:`CryptContext.to_dict` instead.
        """

    def to_dict(self, resolve: bool = False):
        """export policy object as dictionary of options.

        .. deprecated:: 1.6
            applications should use :meth:`CryptContext.to_dict` instead.
        """

    def to_file(self, stream, section: str = "passlib") -> None:
        """export policy to file.

        .. deprecated:: 1.6
            applications should use :meth:`CryptContext.to_string` instead,
            and then write the output to a file as desired.
        """

    def to_string(self, section: str = "passlib", encoding=None):
        """export policy to file.

        .. deprecated:: 1.6
            applications should use :meth:`CryptContext.to_string` instead.
        """

class CryptContext:
    """Helper for hashing & verifying passwords using multiple algorithms.

    Instances of this class allow applications to choose a specific
    set of hash algorithms which they wish to support, set limits and defaults
    for the rounds and salt sizes those algorithms should use, flag
    which algorithms should be deprecated, and automatically handle
    migrating users to stronger hashes when they log in.

    Basic usage::

        >>> ctx = CryptContext(schemes=[...])

    See the Passlib online documentation for details and full documentation.
    """

    @classmethod
    def from_string(cls, source: str | bytes, section: str = "passlib", encoding: str = "utf-8") -> Self:
        """create new CryptContext instance from an INI-formatted string.

        :type source: unicode or bytes
        :arg source:
            string containing INI-formatted content.

        :type section: str
        :param section:
            option name of section to read from, defaults to ``"passlib"``.

        :type encoding: str
        :arg encoding:
            optional encoding used when source is bytes, defaults to ``"utf-8"``.

        :returns:
            new :class:`CryptContext` instance, configured based on the
            parameters in the *source* string.

        Usage example::

            >>> from passlib.context import CryptContext
            >>> context = CryptContext.from_string('''
            ... [passlib]
            ... schemes = sha256_crypt, des_crypt
            ... sha256_crypt__default_rounds = 30000
            ... ''')

        .. versionadded:: 1.6

        .. seealso:: :meth:`to_string`, the inverse of this constructor.
        """

    @classmethod
    def from_path(cls, path: StrOrBytesPath, section: str = "passlib", encoding: str = "utf-8") -> Self:
        """create new CryptContext instance from an INI-formatted file.

        this functions exactly the same as :meth:`from_string`,
        except that it loads from a local file.

        :type path: str
        :arg path:
            path to local file containing INI-formatted config.

        :type section: str
        :param section:
            option name of section to read from, defaults to ``"passlib"``.

        :type encoding: str
        :arg encoding:
            encoding used to load file, defaults to ``"utf-8"``.

        :returns:
            new CryptContext instance, configured based on the parameters
            stored in the file *path*.

        .. versionadded:: 1.6

        .. seealso:: :meth:`from_string` for an equivalent usage example.
        """

    def copy(self, **kwds: Any) -> CryptContext:
        """Return copy of existing CryptContext instance.

        This function returns a new CryptContext instance whose configuration
        is exactly the same as the original, with the exception that any keywords
        passed in will take precedence over the original settings.
        As an example::

            >>> from passlib.context import CryptContext

            >>> # given an existing context...
            >>> ctx1 = CryptContext(["sha256_crypt", "md5_crypt"])

            >>> # copy can be used to make a clone, and update
            >>> # some of the settings at the same time...
            >>> ctx2 = custom_app_context.copy(default="md5_crypt")

            >>> # and the original will be unaffected by the change
            >>> ctx1.default_scheme()
            "sha256_crypt"
            >>> ctx2.default_scheme()
            "md5_crypt"

        .. versionadded:: 1.6
            This method was previously named :meth:`!replace`. That alias
            has been deprecated, and will be removed in Passlib 1.8.

        .. seealso:: :meth:`update`
        """

    def using(self, **kwds: Any) -> CryptContext:
        """
        alias for :meth:`copy`, to match PasswordHash.using()
        """

    def replace(self, **kwds):
        """deprecated alias of :meth:`copy`"""

    def __init__(self, schemes=None, policy=..., _autoload: bool = True, **kwds) -> None: ...
    policy: CryptPolicy
    def load_path(self, path: StrOrBytesPath, update: bool = False, section: str = "passlib", encoding: str = "utf-8") -> None:
        """Load new configuration into CryptContext from a local file.

        This function is a wrapper for :meth:`load` which
        loads a configuration string from the local file *path*,
        instead of an in-memory source. Its behavior and options
        are otherwise identical to :meth:`!load` when provided with
        an INI-formatted string.

        .. versionadded:: 1.6
        """

    def load(
        self,
        source: str | bytes | SupportsItems[str, Any] | CryptContext,
        update: bool = False,
        section: str = "passlib",
        encoding: str = "utf-8",
    ) -> None:
        """Load new configuration into CryptContext, replacing existing config.

        :arg source:
            source of new configuration to load.
            this value can be a number of different types:

            * a :class:`!dict` object, or compatible Mapping

                the key/value pairs will be interpreted the same
                keywords for the :class:`CryptContext` class constructor.

            * a :class:`!unicode` or :class:`!bytes` string

                this will be interpreted as an INI-formatted file,
                and appropriate key/value pairs will be loaded from
                the specified *section*.

            * another :class:`!CryptContext` object.

                this will export a snapshot of its configuration
                using :meth:`to_dict`.

        :type update: bool
        :param update:
            By default, :meth:`load` will replace the existing configuration
            entirely. If ``update=True``, it will preserve any existing
            configuration options that are not overridden by the new source,
            much like the :meth:`update` method.

        :type section: str
        :param section:
            When parsing an INI-formatted string, :meth:`load` will look for
            a section named ``"passlib"``. This option allows an alternate
            section name to be used. Ignored when loading from a dictionary.

        :type encoding: str
        :param encoding:
            Encoding to use when **source** is bytes.
            Defaults to ``"utf-8"``. Ignored when loading from a dictionary.

            .. deprecated:: 1.8

                This keyword, and support for bytes input, will be dropped in Passlib 2.0

        :raises TypeError:
            * If the source cannot be identified.
            * If an unknown / malformed keyword is encountered.

        :raises ValueError:
            If an invalid keyword value is encountered.

        .. note::

            If an error occurs during a :meth:`!load` call, the :class:`!CryptContext`
            instance will be restored to the configuration it was in before
            the :meth:`!load` call was made; this is to ensure it is
            *never* left in an inconsistent state due to a load error.

        .. versionadded:: 1.6
        """

    def update(self, *args: Any, **kwds: Any) -> None:
        """Helper for quickly changing configuration.

        This acts much like the :meth:`!dict.update` method:
        it updates the context's configuration,
        replacing the original value(s) for the specified keys,
        and preserving the rest.
        It accepts any :ref:`keyword <context-options>`
        accepted by the :class:`!CryptContext` constructor.

        .. versionadded:: 1.6

        .. seealso:: :meth:`copy`
        """

    def schemes(self, resolve: bool = False, category=None, unconfigured: bool = False):
        """return schemes loaded into this CryptContext instance.

        :type resolve: bool
        :arg resolve:
            if ``True``, will return a tuple of :class:`~passlib.ifc.PasswordHash`
            objects instead of their names.

        :returns:
            returns tuple of the schemes configured for this context
            via the *schemes* option.

        .. versionadded:: 1.6
            This was previously available as ``CryptContext().policy.schemes()``

        .. seealso:: the :ref:`schemes <context-schemes-option>` option for usage example.
        """

    def default_scheme(self, category=None, resolve: bool = False, unconfigured: bool = False):
        """return name of scheme that :meth:`hash` will use by default.

        :type resolve: bool
        :arg resolve:
            if ``True``, will return a :class:`~passlib.ifc.PasswordHash`
            object instead of the name.

        :type category: str or None
        :param category:
            Optional :ref:`user category <user-categories>`.
            If specified, this will return the catgory-specific default scheme instead.

        :returns:
            name of the default scheme.

        .. seealso:: the :ref:`default <context-default-option>` option for usage example.

        .. versionadded:: 1.6

        .. versionchanged:: 1.7

            This now returns a hasher configured with any CryptContext-specific
            options (custom rounds settings, etc).  Previously this returned
            the base hasher from :mod:`passlib.hash`.
        """

    def handler(self, scheme=None, category=None, unconfigured: bool = False):
        """helper to resolve name of scheme -> :class:`~passlib.ifc.PasswordHash` object used by scheme.

        :arg scheme:
            This should identify the scheme to lookup.
            If omitted or set to ``None``, this will return the handler
            for the default scheme.

        :arg category:
            If a user category is specified, and no scheme is provided,
            it will use the default for that category.
            Otherwise this parameter is ignored.

        :param unconfigured:

            By default, this returns a handler object whose .hash()
            and .needs_update() methods will honor the configured
            provided by CryptContext.   See ``unconfigured=True``
            to get the underlying handler from before any context-specific
            configuration was applied.

        :raises KeyError:
            If the scheme does not exist OR is not being used within this context.

        :returns:
            :class:`~passlib.ifc.PasswordHash` object used to implement
            the named scheme within this context (this will usually
            be one of the objects from :mod:`passlib.hash`)

        .. versionadded:: 1.6
            This was previously available as ``CryptContext().policy.get_handler()``

        .. versionchanged:: 1.7

            This now returns a hasher configured with any CryptContext-specific
            options (custom rounds settings, etc).  Previously this returned
            the base hasher from :mod:`passlib.hash`.
        """

    @property
    def context_kwds(self):
        """
        return :class:`!set` containing union of all :ref:`contextual keywords <context-keywords>`
        supported by the handlers in this context.

        .. versionadded:: 1.6.6
        """

    def to_dict(self, resolve: bool = False) -> dict[str, Any]:
        """Return current configuration as a dictionary.

        :type resolve: bool
        :arg resolve:
            if ``True``, the ``schemes`` key will contain a list of
            a :class:`~passlib.ifc.PasswordHash` objects instead of just
            their names.

        This method dumps the current configuration of the CryptContext
        instance. The key/value pairs should be in the format accepted
        by the :class:`!CryptContext` class constructor, in fact
        ``CryptContext(**myctx.to_dict())`` will create an exact copy of ``myctx``.
        As an example::

            >>> # you can dump the configuration of any crypt context...
            >>> from passlib.apps import ldap_nocrypt_context
            >>> ldap_nocrypt_context.to_dict()
            {'schemes': ['ldap_salted_sha1',
            'ldap_salted_md5',
            'ldap_sha1',
            'ldap_md5',
            'ldap_plaintext']}

        .. versionadded:: 1.6
            This was previously available as ``CryptContext().policy.to_dict()``

        .. seealso:: the :ref:`context-serialization-example` example in the tutorial.
        """

    def to_string(self, section: str = "passlib") -> str:
        """serialize to INI format and return as unicode string.

        :param section:
            name of INI section to output, defaults to ``"passlib"``.

        :returns:
            CryptContext configuration, serialized to a INI unicode string.

        This function acts exactly like :meth:`to_dict`, except that it
        serializes all the contents into a single human-readable string,
        which can be hand edited, and/or stored in a file. The
        output of this method is accepted by :meth:`from_string`,
        :meth:`from_path`, and :meth:`load`. As an example::

            >>> # you can dump the configuration of any crypt context...
            >>> from passlib.apps import ldap_nocrypt_context
            >>> print ldap_nocrypt_context.to_string()
            [passlib]
            schemes = ldap_salted_sha1, ldap_salted_md5, ldap_sha1, ldap_md5, ldap_plaintext

        .. versionadded:: 1.6
            This was previously available as ``CryptContext().policy.to_string()``

        .. seealso:: the :ref:`context-serialization-example` example in the tutorial.
        """
    mvt_estimate_max_samples: int
    mvt_estimate_min_samples: int
    mvt_estimate_max_time: int
    mvt_estimate_resolution: float
    harden_verify: Any
    min_verify_time: int
    def reset_min_verify_time(self) -> None: ...
    def needs_update(
        self, hash: str | bytes, scheme: str | None = None, category: str | None = None, secret: str | bytes | None = None
    ) -> bool:
        """Check if hash needs to be replaced for some reason,
        in which case the secret should be re-hashed.

        This function is the core of CryptContext's support for hash migration:
        This function takes in a hash string, and checks the scheme,
        number of rounds, and other properties against the current policy.
        It returns ``True`` if the hash is using a deprecated scheme,
        or is otherwise outside of the bounds specified by the policy
        (e.g. the number of rounds is lower than :ref:`min_rounds <context-min-rounds-option>`
        configuration for that algorithm).
        If so, the password should be re-hashed using :meth:`hash`
        Otherwise, it will return ``False``.

        :type hash: unicode or bytes
        :arg hash:
            The hash string to examine.

        :type scheme: str or None
        :param scheme:

            Optional scheme to use. Scheme must be one of the ones
            configured for this context (see the
            :ref:`schemes <context-schemes-option>` option).
            If no scheme is specified, it will be identified
            based on the value of *hash*.

            .. deprecated:: 1.7

                Support for this keyword is deprecated, and will be removed in Passlib 2.0.

        :type category: str or None
        :param category:
            Optional :ref:`user category <user-categories>`.
            If specified, this will cause any category-specific defaults to
            be used when determining if the hash needs to be updated
            (e.g. is below the minimum rounds).

        :type secret: unicode, bytes, or None
        :param secret:
            Optional secret associated with the provided ``hash``.
            This is not required, or even currently used for anything...
            it's for forward-compatibility with any future
            update checks that might need this information.
            If provided, Passlib assumes the secret has already been
            verified successfully against the hash.

            .. versionadded:: 1.6

        :returns: ``True`` if hash should be replaced, otherwise ``False``.

        :raises ValueError:
            If the hash did not match any of the configured :meth:`schemes`.

        .. versionadded:: 1.6
            This method was previously named :meth:`hash_needs_update`.

        .. seealso:: the :ref:`context-migration-example` example in the tutorial.
        """

    def hash_needs_update(self, hash, scheme=None, category=None):
        """Legacy alias for :meth:`needs_update`.

        .. deprecated:: 1.6
            This method was renamed to :meth:`!needs_update` in version 1.6.
            This alias will be removed in version 2.0, and should only
            be used for compatibility with Passlib 1.3 - 1.5.
        """

    def genconfig(self, scheme=None, category=None, **settings):
        """Generate a config string for specified scheme.

        .. deprecated:: 1.7

            This method will be removed in version 2.0, and should only
            be used for compatibility with Passlib 1.3 - 1.6.
        """

    def genhash(self, secret, config, scheme=None, category=None, **kwds):
        """Generate hash for the specified secret using another hash.

        .. deprecated:: 1.7

            This method will be removed in version 2.0, and should only
            be used for compatibility with Passlib 1.3 - 1.6.
        """

    def identify(self, hash, category=None, resolve: bool = False, required: bool = False, unconfigured: bool = False):
        """Attempt to identify which algorithm the hash belongs to.

        Note that this will only consider the algorithms
        currently configured for this context
        (see the :ref:`schemes <context-schemes-option>` option).
        All registered algorithms will be checked, from first to last,
        and whichever one positively identifies the hash first will be returned.

        :type hash: unicode or bytes
        :arg hash:
            The hash string to test.

        :type category: str or None
        :param category:
            Optional :ref:`user category <user-categories>`.
            Ignored by this function, this parameter
            is provided for symmetry with the other methods.

        :type resolve: bool
        :param resolve:
            If ``True``, returns the hash handler itself,
            instead of the name of the hash.

        :type required: bool
        :param required:
            If ``True``, this will raise a ValueError if the hash
            cannot be identified, instead of returning ``None``.

        :returns:
            The handler which first identifies the hash,
            or ``None`` if none of the algorithms identify the hash.
        """

    def hash(self, secret: str | bytes, scheme: str | None = None, category: str | None = None, **kwds: Any) -> str:
        """run secret through selected algorithm, returning resulting hash.

        :type secret: unicode or bytes
        :arg secret:
            the password to hash.

        :type scheme: str or None
        :param scheme:

            Optional scheme to use. Scheme must be one of the ones
            configured for this context (see the
            :ref:`schemes <context-schemes-option>` option).
            If no scheme is specified, the configured default
            will be used.

            .. deprecated:: 1.7

                Support for this keyword is deprecated, and will be removed in Passlib 2.0.

        :type category: str or None
        :param category:
            Optional :ref:`user category <user-categories>`.
            If specified, this will cause any category-specific defaults to
            be used when hashing the password (e.g. different default scheme,
            different default rounds values, etc).

        :param \\*\\*kwds:
            All other keyword options are passed to the selected algorithm's
            :meth:`PasswordHash.hash() <passlib.ifc.PasswordHash.hash>` method.

        :returns:
            The secret as encoded by the specified algorithm and options.
            The return value will always be a :class:`!str`.

        :raises TypeError, ValueError:
            * If any of the arguments have an invalid type or value.
              This includes any keywords passed to the underlying hash's
              :meth:`PasswordHash.hash() <passlib.ifc.PasswordHash.hash>` method.

        .. seealso:: the :ref:`context-basic-example` example in the tutorial
        """

    def encrypt(self, *args, **kwds):
        """
        Legacy alias for :meth:`hash`.

        .. deprecated:: 1.7
            This method was renamed to :meth:`!hash` in version 1.7.
            This alias will be removed in version 2.0, and should only
            be used for compatibility with Passlib 1.3 - 1.6.
        """

    def verify(
        self, secret: str | bytes, hash: str | bytes | None, scheme: str | None = None, category: str | None = None, **kwds: Any
    ) -> bool:
        """verify secret against an existing hash.

        If no scheme is specified, this will attempt to identify
        the scheme based on the contents of the provided hash
        (limited to the schemes configured for this context).
        It will then check whether the password verifies against the hash.

        :type secret: unicode or bytes
        :arg secret:
            the secret to verify

        :type hash: unicode or bytes
        :arg hash:
            hash string to compare to

            if ``None`` is passed in, this will be treated as "never verifying"

        :type scheme: str
        :param scheme:
            Optionally force context to use specific scheme.
            This is usually not needed, as most hashes can be unambiguously
            identified. Scheme must be one of the ones configured
            for this context
            (see the :ref:`schemes <context-schemes-option>` option).

            .. deprecated:: 1.7

                Support for this keyword is deprecated, and will be removed in Passlib 2.0.

        :type category: str or None
        :param category:
            Optional :ref:`user category <user-categories>` string.
            This is mainly used when generating new hashes, it has little
            effect when verifying; this keyword is mainly provided for symmetry.

        :param \\*\\*kwds:
            All additional keywords are passed to the appropriate handler,
            and should match its :attr:`~passlib.ifc.PasswordHash.context_kwds`.

        :returns:
            ``True`` if the password matched the hash, else ``False``.

        :raises ValueError:
            * if the hash did not match any of the configured :meth:`schemes`.

            * if any of the arguments have an invalid value (this includes
              any keywords passed to the underlying hash's
              :meth:`PasswordHash.verify() <passlib.ifc.PasswordHash.verify>` method).

        :raises TypeError:
            * if any of the arguments have an invalid type (this includes
              any keywords passed to the underlying hash's
              :meth:`PasswordHash.verify() <passlib.ifc.PasswordHash.verify>` method).

        .. seealso:: the :ref:`context-basic-example` example in the tutorial
        """

    def verify_and_update(
        self, secret: str | bytes, hash: str | bytes | None, scheme: str | None = None, category: str | None = None, **kwds: Any
    ) -> tuple[bool, str | None]:
        """verify password and re-hash the password if needed, all in a single call.

        This is a convenience method which takes care of all the following:
        first it verifies the password (:meth:`~CryptContext.verify`), if this is successfull
        it checks if the hash needs updating (:meth:`~CryptContext.needs_update`), and if so,
        re-hashes the password (:meth:`~CryptContext.hash`), returning the replacement hash.
        This series of steps is a very common task for applications
        which wish to update deprecated hashes, and this call takes
        care of all 3 steps efficiently.

        :type secret: unicode or bytes
        :arg secret:
            the secret to verify

        :type secret: unicode or bytes
        :arg hash:
            hash string to compare to.

            if ``None`` is passed in, this will be treated as "never verifying"

        :type scheme: str
        :param scheme:
            Optionally force context to use specific scheme.
            This is usually not needed, as most hashes can be unambiguously
            identified. Scheme must be one of the ones configured
            for this context
            (see the :ref:`schemes <context-schemes-option>` option).

            .. deprecated:: 1.7

                Support for this keyword is deprecated, and will be removed in Passlib 2.0.

        :type category: str or None
        :param category:
            Optional :ref:`user category <user-categories>`.
            If specified, this will cause any category-specific defaults to
            be used if the password has to be re-hashed.

        :param \\*\\*kwds:
            all additional keywords are passed to the appropriate handler,
            and should match that hash's
            :attr:`PasswordHash.context_kwds <passlib.ifc.PasswordHash.context_kwds>`.

        :returns:
            This function returns a tuple containing two elements:
            ``(verified, replacement_hash)``. The first is a boolean
            flag indicating whether the password verified,
            and the second an optional replacement hash.
            The tuple will always match one of the following 3 cases:

            * ``(False, None)`` indicates the secret failed to verify.
            * ``(True, None)`` indicates the secret verified correctly,
              and the hash does not need updating.
            * ``(True, str)`` indicates the secret verified correctly,
              but the current hash needs to be updated. The :class:`!str`
              will be the freshly generated hash, to replace the old one.

        :raises TypeError, ValueError:
            For the same reasons as :meth:`verify`.

        .. seealso:: the :ref:`context-migration-example` example in the tutorial.
        """

    def dummy_verify(self, elapsed: int = 0):
        """
        Helper that applications can call when user wasn't found,
        in order to simulate time it would take to hash a password.

        Runs verify() against a dummy hash, to simulate verification
        of a real account password.

        :param elapsed:

            .. deprecated:: 1.7.1

                this option is ignored, and will be removed in passlib 1.8.

        .. versionadded:: 1.7
        """

    def is_enabled(self, hash: str | bytes) -> bool:
        """
        test if hash represents a usuable password --
        i.e. does not represent an unusuable password such as ``"!"``,
        which is recognized by the :class:`~passlib.hash.unix_disabled` hash.

        :raises ValueError:
            if the hash is not recognized
            (typically solved by adding ``unix_disabled`` to the list of schemes).
        """

    def disable(self, hash: str | bytes | None = None) -> str:
        """
        return a string to disable logins for user,
        usually by returning a non-verifying string such as ``"!"``.

        :param hash:
            Callers can optionally provide the account's existing hash.
            Some disabled handlers (such as :class:`!unix_disabled`)
            will encode this into the returned value,
            so that it can be recovered via :meth:`enable`.

        :raises RuntimeError:
            if this function is called w/o a disabled hasher
            (such as :class:`~passlib.hash.unix_disabled`) included
            in the list of schemes.

        :returns:
            hash string which will be recognized as valid by the context,
            but is guaranteed to not validate against *any* password.
        """

    def enable(self, hash: str | bytes) -> str:
        """
        inverse of :meth:`disable` --
        attempts to recover original hash which was converted
        by a :meth:`!disable` call into a disabled hash --
        thus restoring the user's original password.

        :raises ValueError:
            if original hash not present, or if the disabled handler doesn't
            support encoding the original hash (e.g. ``django_disabled``)

        :returns:
            the original hash.
        """

class LazyCryptContext(CryptContext):
    """CryptContext subclass which doesn't load handlers until needed.

    This is a subclass of CryptContext which takes in a set of arguments
    exactly like CryptContext, but won't import any handlers
    (or even parse its arguments) until
    the first time one of its methods is accessed.

    :arg schemes:
        The first positional argument can be a list of schemes, or omitted,
        just like CryptContext.

    :param onload:

        If a callable is passed in via this keyword,
        it will be invoked at lazy-load time
        with the following signature:
        ``onload(**kwds) -> kwds``;
        where ``kwds`` is all the additional kwds passed to LazyCryptContext.
        It should perform any additional deferred initialization,
        and return the final dict of options to be passed to CryptContext.

        .. versionadded:: 1.6

    :param create_policy:

        .. deprecated:: 1.6
            This option will be removed in Passlib 1.8,
            applications should use ``onload`` instead.

    :param kwds:

        All additional keywords are passed to CryptContext;
        or to the *onload* function (if provided).

    This is mainly used internally by modules such as :mod:`passlib.apps`,
    which define a large number of contexts, but only a few of them will be needed
    at any one time. Use of this class saves the memory needed to import
    the specified handlers until the context instance is actually accessed.
    As well, it allows constructing a context at *module-init* time,
    but using :func:`!onload()` to provide dynamic configuration
    at *application-run* time.

    .. note::
        This class is only useful if you're referencing handler objects by name,
        and don't want them imported until runtime. If you want to have the config
        validated before your application runs, or are passing in already-imported
        handler instances, you should use :class:`CryptContext` instead.

    .. versionadded:: 1.4
    """

    def __init__(self, schemes=None, **kwds) -> None: ...
    def __getattribute__(self, attr: str) -> Any: ...

__all__ = ["CryptContext", "LazyCryptContext", "CryptPolicy"]
