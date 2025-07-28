from collections.abc import Callable, Collection, Iterable, Mapping
from typing import Any, TypeVar, overload
from typing_extensions import TypeAlias

from ._utils import NO_DEFAULT, ExtractorError

_Traversable: TypeAlias = Mapping[str, Any] | Iterable[Any]
_PathArg: TypeAlias = str | int

def traverse_obj(
    obj: _Traversable,
    *paths: _PathArg,
    default: Any = ...,  # Anything or type[NO_DEFAULT]
    expected_type: type[Any] | None = None,
    get_all: bool = True,
    casesense: bool = True,
    is_user_input: bool | type[NO_DEFAULT] = ...,
    traverse_string: bool = False,
) -> Any:  # Unknown return type
    """
    Safely traverse nested `dict`s and `Iterable`s

    >>> obj = [{}, {"key": "value"}]
    >>> traverse_obj(obj, (1, "key"))
    'value'

    Each of the provided `paths` is tested and the first producing a valid result will be returned.
    The next path will also be tested if the path branched but no results could be found.
    Supported values for traversal are `Mapping`, `Iterable`, `re.Match`,
    `xml.etree.ElementTree` (xpath) and `http.cookies.Morsel`.
    Unhelpful values (`{}`, `None`) are treated as the absence of a value and discarded.

    The paths will be wrapped in `variadic`, so that `'key'` is conveniently the same as `('key', )`.

    The keys in the path can be one of:
        - `None`:           Return the current object.
        - `set`:            Requires the only item in the set to be a type or function,
                            like `{type}`/`{type, type, ...}`/`{func}`. If a `type`, return only
                            values of this type. If a function, returns `func(obj)`.
        - `str`/`int`:      Return `obj[key]`. For `re.Match`, return `obj.group(key)`.
        - `slice`:          Branch out and return all values in `obj[key]`.
        - `Ellipsis`:       Branch out and return a list of all values.
        - `tuple`/`list`:   Branch out and return a list of all matching values.
                            Read as: `[traverse_obj(obj, branch) for branch in branches]`.
        - `function`:       Branch out and return values filtered by the function.
                            Read as: `[value for key, value in obj if function(key, value)]`.
                            For `Iterable`s, `key` is the index of the value.
                            For `re.Match`es, `key` is the group number (0 = full match)
                            as well as additionally any group names, if given.
        - `dict`:           Transform the current object and return a matching dict.
                            Read as: `{key: traverse_obj(obj, path) for key, path in dct.items()}`.
        - `any`-builtin:    Take the first matching object and return it, resetting branching.
        - `all`-builtin:    Take all matching objects and return them as a list, resetting branching.
        - `filter`-builtin: Return the value if it is truthy, `None` otherwise.

        `tuple`, `list`, and `dict` all support nested paths and branches.

    @params paths           Paths by which to traverse.
    @param default          Value to return if the paths do not match.
                            If the last key in the path is a `dict`, it will apply to each value inside
                            the dict instead, depth first. Try to avoid if using nested `dict` keys.
    @param expected_type    If a `type`, only accept final values of this type.
                            If any other callable, try to call the function on each result.
                            If the last key in the path is a `dict`, it will apply to each value inside
                            the dict instead, recursively. This does respect branching paths.
    @param get_all          If `False`, return the first matching result, otherwise all matching ones.
    @param casesense        If `False`, consider string dictionary keys as case insensitive.

    `traverse_string` is only meant to be used by YoutubeDL.prepare_outtmpl and is not part of the API

    @param traverse_string  Whether to traverse into objects as strings.
                            If `True`, any non-compatible object will first be
                            converted into a string and then traversed into.
                            The return value of that path will be a string instead,
                            not respecting any further branching.


    @returns                The result of the object traversal.
                            If successful, `get_all=True`, and the path branches at least once,
                            then a list of results is returned instead.
                            If no `default` is given and the last path branches, a `list` of results
                            is always returned. If a path ends on a `dict` that result will always be a `dict`.
    """

_T = TypeVar("_T")

def value(value: _T, /) -> _T: ...
def require(name: str, /, *, expected: bool = False) -> Callable[[_T], _T]: ...

class _RequiredError(ExtractorError): ...

@overload
def subs_list_to_dict(
    *, lang: str | None = "und", ext: str | None = None
) -> Callable[[list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    """
    Convert subtitles from a traversal into a subtitle dict.
    The path should have an `all` immediately before this function.

    Arguments:
    `ext`      The default value for `ext` in the subtitle dict

    In the dict you can set the following additional items:
    `id`       The subtitle id to sort the dict into
    `quality`  The sort order for each subtitle
    """

@overload
def subs_list_to_dict(
    subs: list[dict[str, Any]] | None, /, *, lang: str | None = "und", ext: str | None = None
) -> dict[str, list[dict[str, Any]]]: ...
@overload
def find_element(*, attr: str, value: str, tag: str | None = None, html: bool = False, regex: bool = False) -> str: ...
@overload
def find_element(*, cls: str, html: bool = False) -> str: ...
@overload
def find_element(*, id: str, tag: str | None = None, html: bool = False, regex: bool = False) -> str: ...
@overload
def find_element(*, tag: str, html: bool = False, regex: bool = False) -> str: ...
@overload
def find_element(
    *,
    tag: str | None = None,
    id: str | None = None,
    cls: str | None = None,
    attr: str | None = None,
    value: str | None = None,
    html: bool = False,
    regex: bool = False,
) -> str: ...
@overload
def find_elements(*, cls: str, html: bool = False) -> list[str]: ...
@overload
def find_elements(*, attr: str, value: str, tag: str | None = None, html: bool = False, regex: bool = False) -> list[str]: ...
@overload
def find_elements(
    *,
    tag: str | None = None,
    cls: str | None = None,
    attr: str | None = None,
    value: str | None = None,
    html: bool = False,
    regex: bool = False,
) -> list[str]: ...
def trim_str(*, start: str | None = None, end: str | None = None) -> Callable[[str], str]: ...

# Returns a callable f(items) which calls func(*items, **kwargs).
def unpack(func: Callable[..., Any], **kwargs: Any) -> Callable[..., Any]: ...
def get_first(
    obj: _Traversable,
    *paths: _PathArg,
    default: Any = ...,  # Anything or type[NO_DEFAULT]
    expected_type: type[Any] | None = None,
    get_all: bool = True,
    casesense: bool = True,
    is_user_input: bool | type[NO_DEFAULT] = ...,
    traverse_string: bool = False,
) -> Any: ...
@overload
def dict_get(d: str, key_or_keys: str | Collection[str]) -> Any | None: ...
@overload
def dict_get(
    d: str, key_or_keys: str | Collection[str], default: Any | None = None, skip_false_values: bool = True
) -> Any | None: ...
