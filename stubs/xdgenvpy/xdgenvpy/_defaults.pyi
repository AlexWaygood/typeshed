"""
Helper module that defines the default XDG Base Directory values.

This is designed to minimize system specific logic, effectively allowing for
Linux CI systems, like the Gitlab runners, to test as much code coverage as
possible.  This should help maximize the possibility that the Gitlab CI will
identify bugs rather than the AppVeyor environments.  The AppVeyor CI
environment is configured to test MacOS and Windows systems.
"""

def system_path_separator() -> str:
    """:returns: The platform specific path separator."""

def XDG_DATA_HOME() -> str:
    """
    :rtype: str
    :returns: The spec defined value for the :code:`XDG_DATA_HOME` variable.
    """

def XDG_CONFIG_HOME() -> str:
    """
    :rtype: str
    :returns: The spec defined value for the :code:`XDG_CONFIG_HOME` variable.
    """

def XDG_CACHE_HOME() -> str:
    """
    :rtype: str
    :returns: The spec defined value for the :code:`XDG_CACHE_HOME` variable.
    """

def XDG_RUNTIME_DIR() -> str:
    """
    :rtype: str
    :returns: The spec defined value for the :code:`XDG_RUNTIME_DIR` variable.
    """

def XDG_DATA_DIRS() -> str:
    """
    :rtype: str
    :returns: The spec defined value for the :code:`XDG_DATA_DIRS` variable.
    """

def XDG_CONFIG_DIRS() -> str:
    """
    :rtype: str
    :returns: The spec defined value for the :code:`XDG_CONFIG_DIRS` variable.
    """
