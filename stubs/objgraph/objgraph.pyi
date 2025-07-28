"""
Tools for drawing Python object reference graphs with graphviz.

You can find documentation online at https://mg.pov.lt/objgraph/

Copyright (c) 2008-2023 Marius Gedminas <marius@pov.lt> and contributors

Released under the MIT licence.
"""

from _typeshed import Incomplete, SupportsWrite
from collections import defaultdict
from collections.abc import Callable, Container, Iterable
from types import ModuleType
from typing import Final, Literal
from typing_extensions import TypeAlias, TypeGuard

IS_INTERACTIVE: bool

__author__: Final[str]
__copyright__: Final[str]
__license__: Final[str]
__version__: Final[str]
__date__: Final[str]

# GraphViz has types, but does not include the py.typed file.
# See https://github.com/xflr6/graphviz/pull/180
_GraphvizSource: TypeAlias = Incomplete
_Filter: TypeAlias = Callable[[object], bool]

def count(typename: str, objects: Iterable[object] | None = None) -> int:
    """Count objects tracked by the garbage collector with a given class name.

    The class name can optionally be fully qualified.

    Example:

        >>> count('dict')
        42
        >>> count('mymodule.MyClass')
        2

    .. note::

        The Python garbage collector does not track simple
        objects like int or str.  See
        https://docs.python.org/3/library/gc.html#gc.is_tracked
        for more information.

    Instead of looking through all objects tracked by the GC, you may
    specify your own collection, e.g.

        >>> count('MyClass', get_leaking_objects())
        3

    See also: :func:`get_leaking_objects`.

    .. versionchanged:: 1.7
       New parameter: ``objects``.

    .. versionchanged:: 1.8
       Accepts fully-qualified type names (i.e. 'package.module.ClassName')
       as well as short type names (i.e. 'ClassName').

    """

def typestats(objects: Iterable[object] | None = None, shortnames: bool = True, filter: _Filter | None = None) -> dict[str, int]:
    """Count the number of instances for each type tracked by the GC.

    Note that the GC does not track simple objects like int or str.

    Note that classes with the same name but defined in different modules
    will be lumped together if ``shortnames`` is True.

    If ``filter`` is specified, it should be a function taking one argument and
    returning a boolean. Objects for which ``filter(obj)`` returns ``False``
    will be ignored.

    Example:

        >>> typestats()
        {'list': 12041, 'tuple': 10245, ...}
        >>> typestats(get_leaking_objects())
        {'MemoryError': 1, 'tuple': 2795, 'RuntimeError': 1, 'list': 47, ...}

    .. versionadded:: 1.1

    .. versionchanged:: 1.7
       New parameter: ``objects``.

    .. versionchanged:: 1.8
       New parameter: ``shortnames``.

    .. versionchanged:: 3.1.3
       New parameter: ``filter``.

    """

def most_common_types(
    limit: int = 10, objects: Iterable[object] | None = None, shortnames: bool = True, filter: _Filter | None = None
) -> list[tuple[str, int]]:
    """Count the names of types with the most instances.

    Returns a list of (type_name, count), sorted most-frequent-first.

    Limits the return value to at most ``limit`` items.  You may set ``limit``
    to None to avoid that.

    If ``filter`` is specified, it should be a function taking one argument and
    returning a boolean. Objects for which ``filter(obj)`` returns ``False``
    will be ignored.

    The caveats documented in :func:`typestats` apply.

    Example:

        >>> most_common_types(limit=2)
        [('list', 12041), ('tuple', 10245)]

    .. versionadded:: 1.4

    .. versionchanged:: 1.7
       New parameter: ``objects``.

    .. versionchanged:: 1.8
       New parameter: ``shortnames``.

    .. versionchanged:: 3.1.3
       New parameter: ``filter``.

    """

def show_most_common_types(
    limit: int = 10,
    objects: Iterable[object] | None = None,
    shortnames: bool = True,
    file: SupportsWrite[str] | None = None,
    filter: _Filter | None = None,
) -> None:
    """Print the table of types of most common instances.

    If ``filter`` is specified, it should be a function taking one argument and
    returning a boolean. Objects for which ``filter(obj)`` returns ``False``
    will be ignored.

    The caveats documented in :func:`typestats` apply.

    Example:

        >>> show_most_common_types(limit=5)
        tuple                      8959
        function                   2442
        wrapper_descriptor         1048
        dict                       953
        builtin_function_or_method 800

    .. versionadded:: 1.1

    .. versionchanged:: 1.7
       New parameter: ``objects``.

    .. versionchanged:: 1.8
       New parameter: ``shortnames``.

    .. versionchanged:: 3.0
       New parameter: ``file``.

    .. versionchanged:: 3.1.3
       New parameter: ``filter``.

    """

def growth(
    limit: int = 10, peak_stats: dict[str, int] = {}, shortnames: bool = True, filter: _Filter | None = None
) -> list[tuple[str, int, int]]:
    """Count the increase in peak object since last call.

    Returns a list of (type_name, total_count, increase_delta),
    descending order by increase_delta.

    Limits the output to ``limit`` largest deltas.  You may set ``limit`` to
    None to see all of them.

    Uses and updates ``peak_stats``, a dictionary from type names to previously
    seen peak object counts.  Usually you don't need to pay attention to this
    argument.

    If ``filter`` is specified, it should be a function taking one argument and
    returning a boolean. Objects for which ``filter(obj)`` returns ``False``
    will be ignored.

    The caveats documented in :func:`typestats` apply.

    Example:

        >>> growth(2)
        [(tuple, 12282, 10), (dict, 1922, 7)]

    .. versionadded:: 3.3.0

    """

def show_growth(
    limit: int = 10,
    peak_stats: dict[str, int] | None = None,
    shortnames: bool = True,
    file: SupportsWrite[str] | None = None,
    filter: _Filter | None = None,
) -> None:
    """Show the increase in peak object counts since last call.

    if ``peak_stats`` is None, peak object counts will recorded in
    func `growth`, and your can record the counts by yourself with set
    ``peak_stats`` to a dictionary.

    The caveats documented in :func:`growth` apply.

    Example:

        >>> show_growth()
        wrapper_descriptor       970       +14
        tuple                  12282       +10
        dict                    1922        +7
        ...

    .. versionadded:: 1.5

    .. versionchanged:: 1.8
       New parameter: ``shortnames``.

    .. versionchanged:: 2.1
       New parameter: ``file``.

    .. versionchanged:: 3.1.3
       New parameter: ``filter``.

    """

def get_new_ids(
    skip_update: bool = False,
    limit: int = 10,
    sortby: Literal["old", "current", "new", "deltas"] = "deltas",
    shortnames: bool | None = None,
    file: SupportsWrite[str] | None = None,
) -> defaultdict[str, set[int]]:
    """Find and display new objects allocated since last call.

    Shows the increase in object counts since last call to this
    function and returns the memory address ids for new objects.

    Returns a dictionary mapping object type names to sets of object IDs
    that have been created since the last time this function was called.

    ``skip_update`` (bool): If True, returns the same dictionary that
    was returned during the previous call without updating the internal
    state or examining the objects currently in memory.

    ``limit`` (int): The maximum number of rows that you want to print
    data for.  Use 0 to suppress the printing.  Use None to print everything.

    ``sortby`` (str): This is the column that you want to sort by in
    descending order.  Possible values are: 'old', 'current', 'new',
    'deltas'

    ``shortnames`` (bool): If True, classes with the same name but
    defined in different modules will be lumped together.  If False,
    all type names will be qualified with the module name.  If None (default),
    ``get_new_ids`` will remember the value from previous calls, so it's
    enough to prime this once.  By default the primed value is True.

    ``_state`` (dict): Stores old, current, and new_ids in memory.
    It is used by the function to store the internal state between calls.
    Never pass in this argument unless you know what you're doing.

    The caveats documented in :func:`growth` apply.

    When one gets new_ids from :func:`get_new_ids`, one can use
    :func:`at_addrs` to get a list of those objects. Then one can iterate over
    the new objects, print out what they are, and call :func:`show_backrefs` or
    :func:`show_chain` to see where they are referenced.

    Example:

        >>> _ = get_new_ids() # store current objects in _state
        >>> _ = get_new_ids() # current_ids become old_ids in _state
        >>> a = [0, 1, 2] # list we don't know about
        >>> b = [3, 4, 5] # list we don't know about
        >>> new_ids = get_new_ids(limit=3) # we see new lists
        ======================================================================
        Type                    Old_ids  Current_ids      New_ids Count_Deltas
        ======================================================================
        list                        324          326           +3           +2
        dict                       1125         1125           +0           +0
        wrapper_descriptor         1001         1001           +0           +0
        ======================================================================
        >>> new_lists = at_addrs(new_ids['list'])
        >>> a in new_lists
        True
        >>> b in new_lists
        True

    .. versionadded:: 3.4
    """

def get_leaking_objects(objects: Iterable[object] | None = None) -> list[object]:
    """Return objects that do not have any referents.

    These could indicate reference-counting bugs in C code.  Or they could
    be legitimate.

    Note that the GC does not track simple objects like int or str.

    .. versionadded:: 1.7
    """

def by_type(typename: str, objects: Iterable[object] | None = None) -> list[object]:
    """Return objects tracked by the garbage collector with a given class name.

    Example:

        >>> by_type('MyClass')
        [<mymodule.MyClass object at 0x...>]

    Note that the GC does not track simple objects like int or str.

    .. versionchanged:: 1.7
       New parameter: ``objects``.

    .. versionchanged:: 1.8
       Accepts fully-qualified type names (i.e. 'package.module.ClassName')
       as well as short type names (i.e. 'ClassName').

    """

def at(addr: int) -> object:
    """Return an object at a given memory address.

    The reverse of id(obj):

        >>> at(id(obj)) is obj
        True

    Note that this function does not work on objects that are not tracked by
    the GC (e.g. ints or strings).
    """

def at_addrs(address_set: Container[int]) -> list[object]:
    """Return a list of objects for a given set of memory addresses.

    The reverse of [id(obj1), id(obj2), ...].  Note that objects are returned
    in an arbitrary order.

    When one gets ``new_ids`` from :func:`get_new_ids`, one can use this
    function to get a list of those objects.  Then one can iterate over the new
    objects, print out what they are, and call :func:`show_backrefs` or
    :func:`show_chain` to see where they are referenced.

        >>> a = [0, 1, 2]
        >>> new_ids = get_new_ids()
        >>> new_lists = at_addrs(new_ids['list'])
        >>> a in new_lists
        True

    Note that this function does not work on objects that are not tracked
    by the GC (e.g. ints or strings).

    .. versionadded:: 3.4
    """

def find_ref_chain(obj: object, predicate: _Filter, max_depth: int = 20, extra_ignore: Iterable[int] = ()) -> list[object]:
    """Find a shortest chain of references leading from obj.

    The end of the chain will be some object that matches your predicate.

    ``predicate`` is a function taking one argument and returning a boolean.

    ``max_depth`` limits the search depth.

    ``extra_ignore`` can be a list of object IDs to exclude those objects from
    your search.

    Example:

        >>> find_ref_chain(obj, lambda x: isinstance(x, MyClass))
        [obj, ..., <MyClass object at ...>]

    Returns ``[obj]`` if such a chain could not be found.

    .. versionadded:: 1.7
    """

def find_backref_chain(obj: object, predicate: _Filter, max_depth: int = 20, extra_ignore: Iterable[int] = ()) -> list[object]:
    """Find a shortest chain of references leading to obj.

    The start of the chain will be some object that matches your predicate.

    ``predicate`` is a function taking one argument and returning a boolean.

    ``max_depth`` limits the search depth.

    ``extra_ignore`` can be a list of object IDs to exclude those objects from
    your search.

    Example:

        >>> find_backref_chain(obj, is_proper_module)
        [<module ...>, ..., obj]

    Returns ``[obj]`` if such a chain could not be found.

    .. versionchanged:: 1.5
       Returns ``obj`` instead of ``None`` when a chain could not be found.

    """

def show_backrefs(
    objs: object,
    max_depth: int = 3,
    extra_ignore: Iterable[int] = (),
    filter: _Filter | None = None,
    too_many: int = 10,
    highlight: object = None,
    filename: str | None = None,
    extra_info: Callable[[object], str] | None = None,
    refcounts: bool = False,
    shortnames: bool = True,
    output: SupportsWrite[str] | None = None,
    extra_node_attrs: Callable[[object], dict[str, str]] | None = None,
) -> None | _GraphvizSource:
    """Generate an object reference graph ending at ``objs``.

    The graph will show you what objects refer to ``objs``, directly and
    indirectly.

    ``objs`` can be a single object, or it can be a list of objects.  If
    unsure, wrap the single object in a new list.

    ``filename`` if specified, can be the name of a .dot or a image
    file, whose extension indicates the desired output format; note
    that output to a specific format is entirely handled by GraphViz:
    if the desired format is not supported, you just get the .dot
    file.  If ``filename`` and ``output`` are not specified, ``show_backrefs``
    will try to display the graph inline (if you're using IPython), otherwise
    it'll try to produce a .dot file and spawn a viewer (xdot).  If xdot is
    not available, ``show_backrefs`` will convert the .dot file to a
    .png and print its name.

    ``output`` if specified, the GraphViz output will be written to this
    file object. ``output`` and ``filename`` should not both be specified.

    Use ``max_depth`` and ``too_many`` to limit the depth and breadth of the
    graph.

    Use ``filter`` (a predicate) and ``extra_ignore`` (a list of object IDs) to
    remove undesired objects from the graph.

    Use ``highlight`` (a predicate) to highlight certain graph nodes in blue.

    Use ``extra_info`` (a function taking one argument and returning a
    string) to report extra information for objects.

    Use ``extra_node_attrs`` (a function taking the current object as argument,
    returning a dict of strings) to add extra attributes to the nodes. See
    https://www.graphviz.org/doc/info/attrs.html for a list of possible node
    attributes.

    Specify ``refcounts=True`` if you want to see reference counts.
    These will mostly match the number of arrows pointing to an object,
    but can be different for various reasons.

    Specify ``shortnames=False`` if you want to see fully-qualified type
    names ('package.module.ClassName').  By default you get to see only the
    class name part.

    Examples:

        >>> show_backrefs(obj)
        >>> show_backrefs([obj1, obj2])
        >>> show_backrefs(obj, max_depth=5)
        >>> show_backrefs(obj, filter=lambda x: not inspect.isclass(x))
        >>> show_backrefs(obj, highlight=inspect.isclass)
        >>> show_backrefs(obj, extra_ignore=[id(locals())])
        >>> show_backrefs(obj, extra_node_attrs=lambda x: dict(URL=str(id(x))))

    .. versionchanged:: 1.3
       New parameters: ``filename``, ``extra_info``.

    .. versionchanged:: 1.5
       New parameter: ``refcounts``.

    .. versionchanged:: 1.8
       New parameter: ``shortnames``.

    .. versionchanged:: 2.0
       New parameter: ``output``.

    .. versionchanged:: 3.5
       New parameter: ``extra_node_attrs``.
    """

def show_refs(
    objs: object,
    max_depth: int = 3,
    extra_ignore: Iterable[int] = (),
    filter: _Filter | None = None,
    too_many: int = 10,
    highlight: object = None,
    filename: str | None = None,
    extra_info: Callable[[object], str] | None = None,
    refcounts: bool = False,
    shortnames: bool = True,
    output: SupportsWrite[str] | None = None,
    extra_node_attrs: Callable[[object], dict[str, str]] | None = None,
) -> None | _GraphvizSource:
    """Generate an object reference graph starting at ``objs``.

    The graph will show you what objects are reachable from ``objs``, directly
    and indirectly.

    ``objs`` can be a single object, or it can be a list of objects.  If
    unsure, wrap the single object in a new list.

    ``filename`` if specified, can be the name of a .dot or a image
    file, whose extension indicates the desired output format; note
    that output to a specific format is entirely handled by GraphViz:
    if the desired format is not supported, you just get the .dot
    file.  If ``filename`` and ``output`` is not specified, ``show_refs`` will
    try to display the graph inline (if you're using IPython), otherwise it'll
    try to produce a .dot file and spawn a viewer (xdot).  If xdot is
    not available, ``show_refs`` will convert the .dot file to a
    .png and print its name.

    ``output`` if specified, the GraphViz output will be written to this
    file object. ``output`` and ``filename`` should not both be specified.

    Use ``max_depth`` and ``too_many`` to limit the depth and breadth of the
    graph.

    Use ``filter`` (a predicate) and ``extra_ignore`` (a list of object IDs) to
    remove undesired objects from the graph.

    Use ``highlight`` (a predicate) to highlight certain graph nodes in blue.

    Use ``extra_info`` (a function returning a string) to report extra
    information for objects.

    Use ``extra_node_attrs`` (a function taking the current object as argument,
    returning a dict of strings) to add extra attributes to the nodes. See
    https://www.graphviz.org/doc/info/attrs.html for a list of possible node
    attributes.

    Specify ``refcounts=True`` if you want to see reference counts.

    Examples:

        >>> show_refs(obj)
        >>> show_refs([obj1, obj2])
        >>> show_refs(obj, max_depth=5)
        >>> show_refs(obj, filter=lambda x: not inspect.isclass(x))
        >>> show_refs(obj, highlight=inspect.isclass)
        >>> show_refs(obj, extra_ignore=[id(locals())])
        >>> show_refs(obj, extra_node_attrs=lambda x: dict(URL=str(id(x))))

    .. versionadded:: 1.1

    .. versionchanged:: 1.3
       New parameters: ``filename``, ``extra_info``.

    .. versionchanged:: 1.5
       Follows references from module objects instead of stopping.
       New parameter: ``refcounts``.

    .. versionchanged:: 1.8
       New parameter: ``shortnames``.

    .. versionchanged:: 2.0
       New parameter: ``output``.

    .. versionchanged:: 3.5
       New parameter: ``extra_node_attrs``.
    """

def show_chain(
    *chains: list[object], obj: object, predicate: _Filter, max_depth: int = 20, extra_ignore: Iterable[int] = ()
) -> None:
    """Show a chain (or several chains) of object references.

    Useful in combination with :func:`find_ref_chain` or
    :func:`find_backref_chain`, e.g.

        >>> show_chain(find_backref_chain(obj, is_proper_module))

    You can specify if you want that chain traced backwards or forwards
    by passing a ``backrefs`` keyword argument, e.g.

        >>> show_chain(find_ref_chain(obj, is_proper_module),
        ...            backrefs=False)

    Ideally this shouldn't matter, but for some objects
    :func:`gc.get_referrers` and :func:`gc.get_referents` are not perfectly
    symmetrical.

    You can specify ``highlight``, ``extra_info``, ``refcounts``,
    ``shortnames``, ``filename`` or ``output`` arguments like for
    :func:`show_backrefs` or :func:`show_refs`.

    .. versionadded:: 1.5

    .. versionchanged:: 1.7
       New parameter: ``backrefs``.

    .. versionchanged:: 2.0
       New parameter: ``output``.

    """

def is_proper_module(obj: object) -> TypeGuard[ModuleType]:
    """
    Returns ``True`` if ``obj`` can be treated like a garbage collector root.

    That is, if ``obj`` is a module that is in ``sys.modules``.

    >>> import types
    >>> is_proper_module([])
    False
    >>> is_proper_module(types)
    True
    >>> is_proper_module(types.ModuleType('foo'))
    False

    .. versionadded:: 1.8
    """
