"""
Various specifications specify files and file formats. This specification
defines where these files should be looked for by defining one or more base
directories relative to which files should be located.

The XDG Base Directory Specification is based on the following concepts:

- There is a single base directory relative to which user-specific data files
  should be written. This directory is defined by the environment variable
  :code:`$XDG_DATA_HOME`.

- There is a single base directory relative to which user-specific configuration
  files should be written. This directory is defined by the environment variable
  :code:`$XDG_CONFIG_HOME`.

- There is a set of preference ordered base directories relative to which data
  files should be searched. This set of directories is defined by the
  environment variable :code:`$XDG_DATA_DIRS`.

- There is a set of preference ordered base directories relative to which
  configuration files should be searched. This set of directories is defined by
  the environment variable :code:`$XDG_CONFIG_DIRS`.

- There is a single base directory relative to which user-specific non-essential
  (cached) data should be written. This directory is defined by the environment
  variable :code:`$XDG_CACHE_HOME`.

- There is a single base directory relative to which user-specific runtime files
  and other file objects should be placed. This directory is defined by the
  environment variable :code:`$XDG_RUNTIME_DIR`.

All paths set in these environment variables must be absolute. If an
implementation encounters a relative path in any of these variables it should
consider the path invalid and ignore it.
"""

class XDG:
    """
    A top level XDG object that basically just implements the XDG specification.
    """

    def __init__(self) -> None:
        """Initializes the base XDG object."""

    @property
    def XDG_DATA_HOME(self) -> str:
        """
        There is a single base directory relative to which user-specific data
        files should be written. This directory is defined by the environment
        variable :code:`$XDG_DATA_HOME`.

        :code:`$XDG_DATA_HOME` defines the base directory relative to which user
        specific data files should be stored. If :code:`$XDG_DATA_HOME` is
        either not set or empty, a default equal to :code:`$HOME/.local/share`
        should be used.

        :rtype: str
        :return: A string containing the value of :code:`$XDG_DATA_HOME`.
        """

    @property
    def XDG_CONFIG_HOME(self) -> str:
        """
        There is a single base directory relative to which user-specific
        configuration files should be written. This directory is defined by the
        environment variable :code:`$XDG_CONFIG_HOME`.

        :code:`$XDG_CONFIG_HOME` defines the base directory relative to which
        user specific configuration files should be stored. If
        :code:`$XDG_CONFIG_HOME` is either not set or empty, a default equal to
        :code:`$HOME/.config` should be used.

        :rtype: str
        :return: A string containing the value of :code:`$XDG_CONFIG_HOME`.
        """

    @property
    def XDG_CACHE_HOME(self) -> str:
        """
        There is a single base directory relative to which user-specific
        non-essential (cached) data should be written. This directory is defined
        by the environment variable :code:`$XDG_CACHE_HOME`.

        code:`$XDG_CACHE_HOME` defines the base directory relative to which user
        specific non-essential data files should be stored. If
        :code:`$XDG_CACHE_HOME` is either not set or empty, a default equal to
        :code:`$HOME/.cache` should be used.

        :rtype: str
        :return: A string containing the value of :code:`$XDG_CACHE_HOME`.
        """

    @property
    def XDG_RUNTIME_DIR(self) -> str:
        """
        There is a single base directory relative to which user-specific runtime
        files and other file objects should be placed. This directory is defined
        by the environment variable :code:`$XDG_RUNTIME_DIR`.

        :code:`$XDG_RUNTIME_DIR` defines the base directory relative to which
        user-specific non-essential runtime files and other file objects (such
        as sockets, named pipes, ...) should be stored. The directory MUST be
        owned by the user, and he MUST be the only one having read and write
        access to it. Its Unix access mode MUST be 0700.

        The lifetime of the directory MUST be bound to the user being logged in.
        It MUST be created when the user first logs in and if the user fully
        logs out the directory MUST be removed. If the user logs in more than
        once he should get pointed to the same directory, and it is mandatory
        that the directory continues to exist from his first login to his last
        logout on the system, and not removed in between. Files in the directory
        MUST not survive reboot or a full logout/login cycle.

        The directory MUST be on a local file system and not shared with any
        other system. The directory MUST by fully-featured by the standards of
        the operating system. More specifically, on Unix-like operating systems
        AF_UNIX sockets, symbolic links, hard links, proper permissions, file
        locking, sparse files, memory mapping, file change notifications, a
        reliable hard link count must be supported, and no restrictions on the
        file name character set should be imposed. Files in this directory MAY
        be subjected to periodic clean-up. To ensure that your files are not
        removed, they should have their access time timestamp modified at least
        once every 6 hours of monotonic time or the 'sticky' bit should be set
        on the file.

        If :code:`$XDG_RUNTIME_DIR` is not set applications should fall back to
        a replacement directory with similar capabilities and print a warning
        message. Applications should use this directory for communication and
        synchronization purposes and should not place larger files in it, since
        it might reside in runtime memory and cannot necessarily be swapped out
        to disk.

        :rtype: str
        :return: A string containing the value of :code:`$XDG_RUNTIME_DIR`.
        """

    @property
    def XDG_DATA_DIRS(self) -> tuple[str, ...]:
        """
        There is a set of preference ordered base directories relative to which
        data files should be searched. This set of directories is defined by the
        environment variable :code:`$XDG_DATA_DIRS`.

        :code:`$XDG_DATA_DIRS` defines the preference-ordered set of base
        directories to search for data files in addition to the
        :code:`$XDG_DATA_HOME` base directory. The directories in
        :code:`$XDG_DATA_DIRS` should be seperated with a colon ':'.

        If :code:`$XDG_DATA_DIRS` is either not set or empty, a value equal to
        :code:`/usr/local/share/:/usr/share/` should be used.

        The order of base directories denotes their importance; the first
        directory listed is the most important. When the same information is
        defined in multiple places the information defined relative to the more
        important base directory takes precedent. The base directory defined by
        :code:`$XDG_DATA_HOME` is considered more important than any of the base
        directories defined by :code:`$XDG_DATA_DIRS`.

        :rtype: tuple
        :return: A sequence containing the value of :code:`$XDG_DATA_DIRS`.
        """

    @property
    def XDG_CONFIG_DIRS(self) -> tuple[str, ...]:
        """
        There is a set of preference ordered base directories relative to which
        configuration files should be searched. This set of directories is
        defined by the environment variable code:`$XDG_CONFIG_DIRS`.

        :code:`$XDG_CONFIG_DIRS` defines the preference-ordered set of base
        directories to search for configuration files in addition to the
        :code:`$XDG_CONFIG_HOME` base directory. The directories in
        :code:`$XDG_CONFIG_DIRS` should be seperated with a colon ':'.

        If :code:`$XDG_CONFIG_DIRS` is either not set or empty, a value equal to
        :code:`/etc/xdg` should be used.

        The order of base directories denotes their importance; the first
        directory listed is the most important. When the same information is
        defined in multiple places the information defined relative to the more
        important base directory takes precedent. The base directory defined by
        :code:`$XDG_CONFIG_HOME` is considered more important than any of the
        base directories defined by :code:`$XDG_CONFIG_DIRS`.

        :rtype: tuple
        :return: A sequence containing the value of :code:`$XDG_CONFIG_DIRS`.
        """

class XDGPackage(XDG):
    """
    An instance of this class helps build package specific directories according
    to the XDG specification.  In the case of:

        -   :code:`$XDG_DATA_DIR`
        -   :code:`$XDG_CONFIG_DIR`
        -   :code:`$XDG_CACHE_DIR`

    variables, this is accomplished by simply appending the package name to the
    directory locations.  All other variables essentially remain unchanged,
    unless they require the DATA/CONFIG/CACHE package directories.
    """

    def __init__(self, package_name: str) -> None:
        """
        Initializes the object with the specified package name.

        :param str package_name: The name of the package.
        """

    @property
    def XDG_DATA_HOME(self) -> str:
        """:return: A package directory relative to the XDG data directory."""

    @property
    def XDG_CONFIG_HOME(self) -> str:
        """:return: A package directory relative to the XDG config directory."""

    @property
    def XDG_CACHE_HOME(self) -> str:
        """:return: A package directory relative to the XDG cache directory."""

    @property
    def XDG_RUNTIME_DIR(self) -> str:
        """
        :return: A package directory relative to the XDG runtime directory.
        """

class XDGPedanticPackage(XDGPackage):
    """
    An instance of this class goes one step further than the :class:`XDGPackage`
    in that it ensures package-specific directories exist in the file system.
    If one of the

        -   :code:`$XDG_DATA_DIR`
        -   :code:`$XDG_CONFIG_DIR`
        -   :code:`$XDG_CACHE_DIR`

    does not exist, the getter method will ensure the directory (and all parent
    directories) exist.  This same logic is not applied to non-package specific
    directories as they can often contain system level directories.  And thus
    may not be writable by the current user.
    """

    @property
    def XDG_DATA_HOME(self) -> str:
        """
        :return: A package directory relative to the XDG data directory with the
                guarantee that the directory exists.
        """

    @property
    def XDG_CONFIG_HOME(self) -> str:
        """
        :return: A package directory relative to the XDG config directory with
                the guarantee that the directory exists.
        """

    @property
    def XDG_CACHE_HOME(self) -> str:
        """
        :return: A package directory relative to the XDG cache directory with
                the guarantee that the directory exists.
        """

    @property
    def XDG_RUNTIME_DIR(self) -> str:
        """
        :return: A package directory relative to the XDG runtime directory with
                the guarantee that the directory exists.
        """
