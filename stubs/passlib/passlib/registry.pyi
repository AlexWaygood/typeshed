"""passlib.registry - registry for password hash handlers"""

from typing import Any

class _PasslibRegistryProxy:
    """proxy module passlib.hash

    this module is in fact an object which lazy-loads
    the requested password hash algorithm from wherever it has been stored.
    it acts as a thin wrapper around :func:`passlib.registry.get_crypt_handler`.
    """

    __name__: str
    __package__: str | None
    def __getattr__(self, attr: str) -> Any: ...  # returns handler that is a value from object.__dict__
    def __setattr__(self, attr: str, value) -> None: ...
    def __dir__(self) -> list[str]: ...

def register_crypt_handler_path(name: str, path: str) -> None:
    """register location to lazy-load handler when requested.

    custom hashes may be registered via :func:`register_crypt_handler`,
    or they may be registered by this function,
    which will delay actually importing and loading the handler
    until a call to :func:`get_crypt_handler` is made for the specified name.

    :arg name: name of handler
    :arg path: module import path

    the specified module path should contain a password hash handler
    called :samp:`{name}`, or the path may contain a colon,
    specifying the module and module attribute to use.
    for example, the following would cause ``get_handler("myhash")`` to look
    for a class named ``myhash`` within the ``myapp.helpers`` module::

        >>> from passlib.registry import registry_crypt_handler_path
        >>> registry_crypt_handler_path("myhash", "myapp.helpers")

    ...while this form would cause ``get_handler("myhash")`` to look
    for a class name ``MyHash`` within the ``myapp.helpers`` module::

        >>> from passlib.registry import registry_crypt_handler_path
        >>> registry_crypt_handler_path("myhash", "myapp.helpers:MyHash")
    """

def register_crypt_handler(
    handler: Any, force: bool = False, _attr: str | None = None
) -> None:  # expected handler is object with attr handler.name
    """register password hash handler.

    this method immediately registers a handler with the internal passlib registry,
    so that it will be returned by :func:`get_crypt_handler` when requested.

    :arg handler: the password hash handler to register
    :param force: force override of existing handler (defaults to False)
    :param _attr:
        [internal kwd] if specified, ensures ``handler.name``
        matches this value, or raises :exc:`ValueError`.

    :raises TypeError:
        if the specified object does not appear to be a valid handler.

    :raises ValueError:
        if the specified object's name (or other required attributes)
        contain invalid values.

    :raises KeyError:
        if a (different) handler was already registered with
        the same name, and ``force=True`` was not specified.
    """

def get_crypt_handler(name: str, default: Any = ...) -> Any:  # returns handler or default
    """return handler for specified password hash scheme.

    this method looks up a handler for the specified scheme.
    if the handler is not already loaded,
    it checks if the location is known, and loads it first.

    :arg name: name of handler to return
    :param default: optional default value to return if no handler with specified name is found.

    :raises KeyError: if no handler matching that name is found, and no default specified, a KeyError will be raised.

    :returns: handler attached to name, or default value (if specified).
    """

def list_crypt_handlers(loaded_only: bool = False) -> list[str]:
    """return sorted list of all known crypt handler names.

    :param loaded_only: if ``True``, only returns names of handlers which have actually been loaded.

    :returns: list of names of all known handlers
    """

__all__ = ["register_crypt_handler_path", "register_crypt_handler", "get_crypt_handler", "list_crypt_handlers"]
