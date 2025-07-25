"""passlib.apache - apache password support"""

from typing_extensions import Self

from .context import CryptContext
from .hash import htdigest

class _CommonFile:
    """common framework for HtpasswdFile & HtdigestFile"""

    encoding: str
    return_unicode: bool
    autosave: bool
    @classmethod
    def from_string(
        cls,
        data: str | bytes,
        *,
        new: bool = False,
        autoload: bool = True,
        autosave: bool = False,
        encoding: str = "utf-8",
        return_unicode: bool = True,
    ) -> Self:
        """create new object from raw string.

        :type data: unicode or bytes
        :arg data:
            database to load, as single string.

        :param \\*\\*kwds:
            all other keywords are the same as in the class constructor
        """

    @classmethod
    def from_path(
        cls,
        path: str,
        *,
        new: bool = False,
        autoload: bool = True,
        autosave: bool = False,
        encoding: str = "utf-8",
        return_unicode: bool = True,
    ) -> Self:
        """create new object from file, without binding object to file.

        :type path: str
        :arg path:
            local filepath to load from

        :param \\*\\*kwds:
            all other keywords are the same as in the class constructor
        """

    def __init__(
        self,
        path: str | None = None,
        new: bool = False,
        autoload: bool = True,
        autosave: bool = False,
        encoding: str = "utf-8",
        return_unicode: bool = True,
    ) -> None: ...
    @property
    def path(self) -> str: ...
    @path.setter
    def path(self, value: str) -> None: ...
    @property
    def mtime(self) -> float:
        """modify time when last loaded (if bound to a local file)"""

    def load_if_changed(self) -> bool:
        """Reload from ``self.path`` only if file has changed since last load"""

    def load(self, path: str | None = None, force: bool = True) -> bool:
        """Load state from local file.
        If no path is specified, attempts to load from ``self.path``.

        :type path: str
        :arg path: local file to load from

        :type force: bool
        :param force:
            if ``force=False``, only load from ``self.path`` if file
            has changed since last load.

            .. deprecated:: 1.6
                This keyword will be removed in Passlib 1.8;
                Applications should use :meth:`load_if_changed` instead.
        """

    def load_string(self, data: str | bytes) -> None:
        """Load state from unicode or bytes string, replacing current state"""

    def save(self, path: str | None = None) -> None:
        """Save current state to file.
        If no path is specified, attempts to save to ``self.path``.
        """

    def to_string(self) -> bytes:
        """Export current state as a string of bytes"""

class HtpasswdFile(_CommonFile):
    """class for reading & writing Htpasswd files.

    The class constructor accepts the following arguments:

    :type path: filepath
    :param path:

        Specifies path to htpasswd file, use to implicitly load from and save to.

        This class has two modes of operation:

        1. It can be "bound" to a local file by passing a ``path`` to the class
           constructor. In this case it will load the contents of the file when
           created, and the :meth:`load` and :meth:`save` methods will automatically
           load from and save to that file if they are called without arguments.

        2. Alternately, it can exist as an independant object, in which case
           :meth:`load` and :meth:`save` will require an explicit path to be
           provided whenever they are called. As well, ``autosave`` behavior
           will not be available.

           This feature is new in Passlib 1.6, and is the default if no
           ``path`` value is provided to the constructor.

        This is also exposed as a readonly instance attribute.

    :type new: bool
    :param new:

        Normally, if *path* is specified, :class:`HtpasswdFile` will
        immediately load the contents of the file. However, when creating
        a new htpasswd file, applications can set ``new=True`` so that
        the existing file (if any) will not be loaded.

        .. versionadded:: 1.6
            This feature was previously enabled by setting ``autoload=False``.
            That alias has been deprecated, and will be removed in Passlib 1.8

    :type autosave: bool
    :param autosave:

        Normally, any changes made to an :class:`HtpasswdFile` instance
        will not be saved until :meth:`save` is explicitly called. However,
        if ``autosave=True`` is specified, any changes made will be
        saved to disk immediately (assuming *path* has been set).

        This is also exposed as a writeable instance attribute.

    :type encoding: str
    :param encoding:

        Optionally specify character encoding used to read/write file
        and hash passwords. Defaults to ``utf-8``, though ``latin-1``
        is the only other commonly encountered encoding.

        This is also exposed as a readonly instance attribute.

    :type default_scheme: str
    :param default_scheme:
        Optionally specify default scheme to use when encoding new passwords.

        This can be any of the schemes with builtin Apache support,
        OR natively supported by the host OS's :func:`crypt.crypt` function.

        * Builtin schemes include ``"bcrypt"`` (apache 2.4+), ``"apr_md5_crypt"`,
          and ``"des_crypt"``.

        * Schemes commonly supported by Unix hosts
          include ``"bcrypt"``, ``"sha256_crypt"``, and ``"des_crypt"``.

        In order to not have to sort out what you should use,
        passlib offers a number of aliases, that will resolve
        to the most appropriate scheme based on your needs:

        * ``"portable"``, ``"portable_apache_24"`` -- pick scheme that's portable across hosts
          running apache >= 2.4. **This will be the default as of Passlib 2.0**.

        * ``"portable_apache_22"`` -- pick scheme that's portable across hosts
          running apache >= 2.4. **This is the default up to Passlib 1.9**.

        * ``"host"``, ``"host_apache_24"`` -- pick strongest scheme supported by
           apache >= 2.4 and/or host OS.

        * ``"host_apache_22"`` -- pick strongest scheme supported by
           apache >= 2.2 and/or host OS.

        .. versionadded:: 1.6
            This keyword was previously named ``default``. That alias
            has been deprecated, and will be removed in Passlib 1.8.

        .. versionchanged:: 1.6.3

            Added support for ``"bcrypt"``, ``"sha256_crypt"``, and ``"portable"`` alias.

        .. versionchanged:: 1.7

            Added apache 2.4 semantics, and additional aliases.

    :type context: :class:`~passlib.context.CryptContext`
    :param context:
        :class:`!CryptContext` instance used to create
        and verify the hashes found in the htpasswd file.
        The default value is a pre-built context which supports all
        of the hashes officially allowed in an htpasswd file.

        This is also exposed as a readonly instance attribute.

        .. warning::

            This option may be used to add support for non-standard hash
            formats to an htpasswd file. However, the resulting file
            will probably not be usable by another application,
            and particularly not by Apache.

    :param autoload:
        Set to ``False`` to prevent the constructor from automatically
        loaded the file from disk.

        .. deprecated:: 1.6
            This has been replaced by the *new* keyword.
            Instead of setting ``autoload=False``, you should use
            ``new=True``. Support for this keyword will be removed
            in Passlib 1.8.

    :param default:
        Change the default algorithm used to hash new passwords.

        .. deprecated:: 1.6
            This has been renamed to *default_scheme* for clarity.
            Support for this alias will be removed in Passlib 1.8.

    Loading & Saving
    ================
    .. automethod:: load
    .. automethod:: load_if_changed
    .. automethod:: load_string
    .. automethod:: save
    .. automethod:: to_string

    Inspection
    ================
    .. automethod:: users
    .. automethod:: check_password
    .. automethod:: get_hash

    Modification
    ================
    .. automethod:: set_password
    .. automethod:: delete

    Alternate Constructors
    ======================
    .. automethod:: from_string

    Attributes
    ==========
    .. attribute:: path

        Path to local file that will be used as the default
        for all :meth:`load` and :meth:`save` operations.
        May be written to, initialized by the *path* constructor keyword.

    .. attribute:: autosave

        Writeable flag indicating whether changes will be automatically
        written to *path*.

    Errors
    ======
    :raises ValueError:
        All of the methods in this class will raise a :exc:`ValueError` if
        any user name contains a forbidden character (one of ``:\\r\\n\\t\\x00``),
        or is longer than 255 characters.
    """

    context: CryptContext
    def __init__(
        self,
        path: str | None = None,
        default_scheme: str | None = None,
        context: CryptContext = ...,
        *,
        new: bool = False,
        autoload: bool = True,
        autosave: bool = False,
        encoding: str = "utf-8",
        return_unicode: bool = True,
    ) -> None: ...
    def users(self) -> list[str | bytes]:
        """
        Return list of all users in database
        """

    def set_password(self, user: str, password: str | bytes) -> bool:
        """Set password for user; adds user if needed.

        :returns:
            * ``True`` if existing user was updated.
            * ``False`` if user account was added.

        .. versionchanged:: 1.6
            This method was previously called ``update``, it was renamed
            to prevent ambiguity with the dictionary method.
            The old alias is deprecated, and will be removed in Passlib 1.8.
        """

    def update(self, user: str, password: str | bytes) -> bool:
        """set password for user"""

    def get_hash(self, user: str) -> bytes | None:
        """Return hash stored for user, or ``None`` if user not found.

        .. versionchanged:: 1.6
            This method was previously named ``find``, it was renamed
            for clarity. The old name is deprecated, and will be removed
            in Passlib 1.8.
        """

    def set_hash(self, user: str, hash: str | bytes) -> bool:
        """
        semi-private helper which allows writing a hash directly;
        adds user if needed.

        .. warning::
            does not (currently) do any validation of the hash string

        .. versionadded:: 1.7
        """

    def find(self, user: str) -> bytes | None:
        """return hash for user"""

    def delete(self, user: str) -> bool:
        """Delete user's entry.

        :returns:
            * ``True`` if user deleted.
            * ``False`` if user not found.
        """

    def check_password(self, user: str, password: str | bytes) -> bool | None:
        """
        Verify password for specified user.
        If algorithm marked as deprecated by CryptContext, will automatically be re-hashed.

        :returns:
            * ``None`` if user not found.
            * ``False`` if user found, but password does not match.
            * ``True`` if user found and password matches.

        .. versionchanged:: 1.6
            This method was previously called ``verify``, it was renamed
            to prevent ambiguity with the :class:`!CryptContext` method.
            The old alias is deprecated, and will be removed in Passlib 1.8.
        """

    def verify(self, user: str, password: str | bytes) -> bool | None:
        """verify password for user"""

class HtdigestFile(_CommonFile):
    """class for reading & writing Htdigest files.

    The class constructor accepts the following arguments:

    :type path: filepath
    :param path:

        Specifies path to htdigest file, use to implicitly load from and save to.

        This class has two modes of operation:

        1. It can be "bound" to a local file by passing a ``path`` to the class
           constructor. In this case it will load the contents of the file when
           created, and the :meth:`load` and :meth:`save` methods will automatically
           load from and save to that file if they are called without arguments.

        2. Alternately, it can exist as an independant object, in which case
           :meth:`load` and :meth:`save` will require an explicit path to be
           provided whenever they are called. As well, ``autosave`` behavior
           will not be available.

           This feature is new in Passlib 1.6, and is the default if no
           ``path`` value is provided to the constructor.

        This is also exposed as a readonly instance attribute.

    :type default_realm: str
    :param default_realm:

        If ``default_realm`` is set, all the :class:`HtdigestFile`
        methods that require a realm will use this value if one is not
        provided explicitly. If unset, they will raise an error stating
        that an explicit realm is required.

        This is also exposed as a writeable instance attribute.

        .. versionadded:: 1.6

    :type new: bool
    :param new:

        Normally, if *path* is specified, :class:`HtdigestFile` will
        immediately load the contents of the file. However, when creating
        a new htpasswd file, applications can set ``new=True`` so that
        the existing file (if any) will not be loaded.

        .. versionadded:: 1.6
            This feature was previously enabled by setting ``autoload=False``.
            That alias has been deprecated, and will be removed in Passlib 1.8

    :type autosave: bool
    :param autosave:

        Normally, any changes made to an :class:`HtdigestFile` instance
        will not be saved until :meth:`save` is explicitly called. However,
        if ``autosave=True`` is specified, any changes made will be
        saved to disk immediately (assuming *path* has been set).

        This is also exposed as a writeable instance attribute.

    :type encoding: str
    :param encoding:

        Optionally specify character encoding used to read/write file
        and hash passwords. Defaults to ``utf-8``, though ``latin-1``
        is the only other commonly encountered encoding.

        This is also exposed as a readonly instance attribute.

    :param autoload:
        Set to ``False`` to prevent the constructor from automatically
        loaded the file from disk.

        .. deprecated:: 1.6
            This has been replaced by the *new* keyword.
            Instead of setting ``autoload=False``, you should use
            ``new=True``. Support for this keyword will be removed
            in Passlib 1.8.

    Loading & Saving
    ================
    .. automethod:: load
    .. automethod:: load_if_changed
    .. automethod:: load_string
    .. automethod:: save
    .. automethod:: to_string

    Inspection
    ==========
    .. automethod:: realms
    .. automethod:: users
    .. automethod:: check_password(user[, realm], password)
    .. automethod:: get_hash

    Modification
    ============
    .. automethod:: set_password(user[, realm], password)
    .. automethod:: delete
    .. automethod:: delete_realm

    Alternate Constructors
    ======================
    .. automethod:: from_string

    Attributes
    ==========
    .. attribute:: default_realm

        The default realm that will be used if one is not provided
        to methods that require it. By default this is ``None``,
        in which case an explicit realm must be provided for every
        method call. Can be written to.

    .. attribute:: path

        Path to local file that will be used as the default
        for all :meth:`load` and :meth:`save` operations.
        May be written to, initialized by the *path* constructor keyword.

    .. attribute:: autosave

        Writeable flag indicating whether changes will be automatically
        written to *path*.

    Errors
    ======
    :raises ValueError:
        All of the methods in this class will raise a :exc:`ValueError` if
        any user name or realm contains a forbidden character (one of ``:\\r\\n\\t\\x00``),
        or is longer than 255 characters.
    """

    default_realm: str | None
    def __init__(
        self,
        path: str | None = None,
        default_realm: str | None = None,
        *,
        new: bool = False,
        autoload: bool = True,
        autosave: bool = False,
        encoding: str = "utf-8",
        return_unicode: bool = True,
    ) -> None: ...
    def realms(self) -> list[str | bytes]:
        """Return list of all realms in database"""

    def users(self, realm: str | None = None) -> list[str | bytes]:
        """Return list of all users in specified realm.

        * uses ``self.default_realm`` if no realm explicitly provided.
        * returns empty list if realm not found.
        """

    def set_password(self, user: str, realm: str | None = None, password: str | bytes = ...) -> bool:
        """Set password for user; adds user & realm if needed.

        If ``self.default_realm`` has been set, this may be called
        with the syntax ``set_password(user, password)``,
        otherwise it must be called with all three arguments:
        ``set_password(user, realm, password)``.

        :returns:
            * ``True`` if existing user was updated
            * ``False`` if user account added.
        """

    def update(self, user: str, realm: str | None, password: str | bytes) -> bool:
        """set password for user"""

    def get_hash(self, user: str, realm: str | None = None) -> htdigest | None:
        """Return :class:`~passlib.hash.htdigest` hash stored for user.

        * uses ``self.default_realm`` if no realm explicitly provided.
        * returns ``None`` if user or realm not found.

        .. versionchanged:: 1.6
            This method was previously named ``find``, it was renamed
            for clarity. The old name is deprecated, and will be removed
            in Passlib 1.8.
        """

    def set_hash(self, user: str, realm: str | None = None, hash: str | bytes = ...) -> bool:
        """
        semi-private helper which allows writing a hash directly;
        adds user & realm if needed.

        If ``self.default_realm`` has been set, this may be called
        with the syntax ``set_hash(user, hash)``,
        otherwise it must be called with all three arguments:
        ``set_hash(user, realm, hash)``.

        .. warning::
            does not (currently) do any validation of the hash string

        .. versionadded:: 1.7
        """

    def find(self, user: str, realm: str | None) -> htdigest | None:
        """return hash for user"""

    def delete(self, user: str, realm: str | None = None) -> bool:
        """Delete user's entry for specified realm.

        if realm is not specified, uses ``self.default_realm``.

        :returns:
            * ``True`` if user deleted,
            * ``False`` if user not found in realm.
        """

    def delete_realm(self, realm: str | None) -> int:
        """Delete all users for specified realm.

        if realm is not specified, uses ``self.default_realm``.

        :returns: number of users deleted (0 if realm not found)
        """

    def check_password(self, user: str, realm: str | None = None, password: str | bytes = ...) -> bool | None:
        """Verify password for specified user + realm.

        If ``self.default_realm`` has been set, this may be called
        with the syntax ``check_password(user, password)``,
        otherwise it must be called with all three arguments:
        ``check_password(user, realm, password)``.

        :returns:
            * ``None`` if user or realm not found.
            * ``False`` if user found, but password does not match.
            * ``True`` if user found and password matches.

        .. versionchanged:: 1.6
            This method was previously called ``verify``, it was renamed
            to prevent ambiguity with the :class:`!CryptContext` method.
            The old alias is deprecated, and will be removed in Passlib 1.8.
        """

    def verify(self, user: str, realm: str | None, password: str | bytes) -> bool | None:
        """verify password for user"""

__all__ = ["HtpasswdFile", "HtdigestFile"]
