"""
This module is based on a rox module (LGPL):

http://cvs.sourceforge.net/viewcvs.py/rox/ROX-Lib2/python/rox/basedir.py?rev=1.9&view=log

The freedesktop.org Base Directory specification provides a way for
applications to locate shared data and configuration:

    http://standards.freedesktop.org/basedir-spec/

(based on version 0.6)

This module can be used to load and save from and to these directories.

Typical usage:

    from rox import basedir

    for dir in basedir.load_config_paths('mydomain.org', 'MyProg', 'Options'):
        print "Load settings from", dir

    dir = basedir.save_config_path('mydomain.org', 'MyProg')
    print >>file(os.path.join(dir, 'Options'), 'w'), "foo=2"

Note: see the rox.Options module for a higher-level API for managing options.
"""

from _typeshed import StrPath
from collections.abc import Iterator

xdg_data_home: str
xdg_data_dirs: list[str]
xdg_config_home: str
xdg_config_dirs: list[str]
xdg_cache_home: str
xdg_state_home: str

def save_config_path(*resource: StrPath) -> str:
    """Ensure ``$XDG_CONFIG_HOME/<resource>/`` exists, and return its path.
    'resource' should normally be the name of your application. Use this
    when saving configuration settings.
    """

def save_data_path(*resource: StrPath) -> str:
    """Ensure ``$XDG_DATA_HOME/<resource>/`` exists, and return its path.
    'resource' should normally be the name of your application or a shared
    resource. Use this when saving or updating application data.
    """

def save_cache_path(*resource: StrPath) -> str:
    """Ensure ``$XDG_CACHE_HOME/<resource>/`` exists, and return its path.
    'resource' should normally be the name of your application or a shared
    resource.
    """

def save_state_path(*resource: StrPath) -> str:
    """Ensure ``$XDG_STATE_HOME/<resource>/`` exists, and return its path.
    'resource' should normally be the name of your application or a shared
    resource.
    """

def load_config_paths(*resource: StrPath) -> Iterator[str]:
    """Returns an iterator which gives each directory named 'resource' in the
    configuration search path. Information provided by earlier directories should
    take precedence over later ones, and the user-specific config dir comes
    first.
    """

def load_first_config(*resource: StrPath) -> str:
    """Returns the first result from load_config_paths, or None if there is nothing
    to load.
    """

def load_data_paths(*resource: StrPath) -> Iterator[str]:
    """Returns an iterator which gives each directory named 'resource' in the
    application data search path. Information provided by earlier directories
    should take precedence over later ones.
    """

def get_runtime_dir(strict: bool = True) -> str:
    """Returns the value of $XDG_RUNTIME_DIR, a directory path.

    This directory is intended for 'user-specific non-essential runtime files
    and other file objects (such as sockets, named pipes, ...)', and
    'communication and synchronization purposes'.

    As of late 2012, only quite new systems set $XDG_RUNTIME_DIR. If it is not
    set, with ``strict=True`` (the default), a KeyError is raised. With
    ``strict=False``, PyXDG will create a fallback under /tmp for the current
    user. This fallback does *not* provide the same guarantees as the
    specification requires for the runtime directory.

    The strict default is deliberately conservative, so that application
    developers can make a conscious decision to allow the fallback.
    """
