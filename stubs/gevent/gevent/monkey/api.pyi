"""
Higher level functions that comprise parts of
the public monkey patching API.


"""

from types import ModuleType
from typing import Any

def get_original(mod_name: str, item_name: str) -> Any:
    """
    Retrieve the original object from a module.

    If the object has not been patched, then that object will still be
    retrieved.

    :param str|sequence mod_name: The name of the standard library module,
        e.g., ``'socket'``. Can also be a sequence of standard library
        modules giving alternate names to try, e.g., ``('thread', '_thread')``;
        the first importable module will supply all *item_name* items.
    :param str|sequence item_name: A string or sequence of strings naming the
        attribute(s) on the module ``mod_name`` to return.

    :return: The original value if a string was given for
             ``item_name`` or a sequence of original values if a
             sequence was passed.
    """

def patch_item(module: ModuleType, attr: str, newitem: object) -> None: ...
def remove_item(module: ModuleType, attr: str) -> None: ...
def patch_module(target_module: ModuleType, source_module: ModuleType, items: list[str] | None = None) -> bool:
    """
    patch_module(target_module, source_module, items=None)

    Replace attributes in *target_module* with the attributes of the
    same name in *source_module*.

    The *source_module* can provide some attributes to customize the process:

    * ``__implements__`` is a list of attribute names to copy; if not present,
      the *items* keyword argument is mandatory. ``__implements__`` must only have
      names from the standard library module in it.
    * ``_gevent_will_monkey_patch(target_module, items, warn, **kwargs)``
    * ``_gevent_did_monkey_patch(target_module, items, warn, **kwargs)``
      These two functions in the *source_module* are called *if* they exist,
      before and after copying attributes, respectively. The "will" function
      may modify *items*. The value of *warn* is a function that should be called
      with a single string argument to issue a warning to the user. If the "will"
      function raises :exc:`gevent.events.DoNotPatch`, no patching will be done. These functions
      are called before any event subscribers or plugins.

    :keyword list items: A list of attribute names to replace. If
       not given, this will be taken from the *source_module* ``__implements__``
       attribute.
    :return: A true value if patching was done, a false value if patching was canceled.

    .. versionadded:: 1.3b1
    """
