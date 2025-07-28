from _typeshed import Incomplete, SupportsKeysAndGetItem, SupportsNext, SupportsRichComparison
from collections.abc import Generator, Iterable, Iterator, Mapping, MutableMapping
from typing import Literal, TypeVar, overload

_T = TypeVar("_T")

class URIDict(MutableMapping[str, str]):
    """
    Dictionary which uses normalized URIs as keys.
    """

    def normalize(self, uri: str) -> str: ...
    store: dict[str, str]
    def __init__(self, m: SupportsKeysAndGetItem[str, str] | Iterable[tuple[str, str]], /, **kwargs: str) -> None: ...
    def __getitem__(self, uri: str) -> str: ...
    def __setitem__(self, uri: str, value: str) -> None: ...
    def __delitem__(self, uri: str) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...

class Unset:
    """
    An as-of-yet unset attribute or unprovided default parameter.
    """

def format_as_index(container: str, indices: Iterable[Incomplete] | None) -> str:
    """
    Construct a single string containing indexing operations for the indices.

    For example for a container ``bar``, [1, 2, "foo"] -> bar[1][2]["foo"]

    Arguments:

        container (str):

            A word to use for the thing being indexed

        indices (sequence):

            The indices to format.

    """

def find_additional_properties(instance: Iterable[str], schema: Mapping[str, Iterable[str]]) -> Generator[str]:
    """
    Return the set of additional properties for the given ``instance``.

    Weeds out properties that should have been validated by ``properties`` and
    / or ``patternProperties``.

    Assumes ``instance`` is dict-like already.
    """

def extras_msg(extras: Iterable[object]) -> tuple[str, Literal["was", "were"]]:  # elements are passed to the repr() function
    """
    Create an error message for extra items or properties.
    """

@overload
def ensure_list(thing: str) -> list[str]:
    """
    Wrap ``thing`` in a list if it's a single str.

    Otherwise, return it unchanged.
    """

@overload
def ensure_list(thing: _T) -> _T: ...
def equal(one, two) -> bool:
    """
    Check if two things are equal evading some Python type hierarchy semantics.

    Specifically in JSON Schema, evade `bool` inheriting from `int`,
    recursing into sequences to do the same.
    """

def unbool(element, true=..., false=...):
    """
    A hack to make True and 1 and False and 0 unique for ``uniq``.
    """

def uniq(container: Iterable[SupportsRichComparison]) -> bool:
    """
    Check if all of a container's elements are unique.

    Tries to rely on the container being recursively sortable, or otherwise
    falls back on (slow) brute force.
    """

def find_evaluated_item_indexes_by_schema(validator, instance, schema) -> list[Incomplete]:
    """
    Get all indexes of items that get evaluated under the current schema.

    Covers all keywords related to unevaluatedItems: items, prefixItems, if,
    then, else, contains, unevaluatedItems, allOf, oneOf, anyOf
    """

def find_evaluated_property_keys_by_schema(validator, instance, schema) -> list[Incomplete]:
    """
    Get all keys of items that get evaluated under the current schema.

    Covers all keywords related to unevaluatedProperties: properties,
    additionalProperties, unevaluatedProperties, patternProperties,
    dependentSchemas, allOf, oneOf, anyOf, if, then, else
    """

def is_valid(errs_it: SupportsNext[object]) -> bool:
    """Whether there are no errors in the given iterator."""
