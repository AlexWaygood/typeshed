"""
Validation errors, and some surrounding helpers.
"""

from _typeshed import Incomplete, SupportsRichComparison, sentinel
from collections import deque
from collections.abc import Callable, Container, Iterable, Iterator, Mapping, MutableMapping, Sequence
from typing import Any
from typing_extensions import Self, TypeAlias, deprecated

from ._types import TypeChecker
from ._utils import Unset
from .protocols import Validator

_RelevanceFuncType: TypeAlias = Callable[[ValidationError], SupportsRichComparison]

WEAK_MATCHES: frozenset[str]
STRONG_MATCHES: frozenset[str]

class _Error(Exception):
    message: str
    path: deque[str | int]
    relative_path: deque[str | int]
    schema_path: deque[str | int]
    relative_schema_path: deque[str | int]
    context: list[ValidationError] | None
    cause: Exception | None
    validator: Validator | Unset
    validator_value: Any | Unset
    instance: Any | Unset
    schema: Mapping[str, Any] | bool | Unset
    parent: _Error | None
    def __init__(
        self,
        message: str,
        validator: str | Unset = sentinel,
        path: Iterable[str | int] = (),
        cause: Exception | None = None,
        context: Sequence[ValidationError] = (),
        validator_value: Any | Unset = sentinel,
        instance: Any | Unset = sentinel,
        schema: Mapping[str, Any] | bool | Unset = sentinel,
        schema_path: Iterable[str | int] = (),
        parent: _Error | None = None,
        type_checker: TypeChecker | Unset = sentinel,
    ) -> None: ...
    @classmethod
    def create_from(cls, other: _Error) -> Self: ...
    @property
    def absolute_path(self) -> Sequence[str | int]: ...
    @property
    def absolute_schema_path(self) -> Sequence[str | int]: ...
    @property
    def json_path(self) -> str: ...
    # TODO: this type could be made more precise using TypedDict to
    # enumerate the types of the members
    def _contents(self) -> dict[str, Incomplete]: ...

class ValidationError(_Error):
    """
    An instance was invalid under a provided schema.
    """

class SchemaError(_Error):
    """
    A schema was invalid under its corresponding metaschema.
    """

class RefResolutionError(Exception):
    def __init__(self, cause: str) -> None: ...

class UndefinedTypeCheck(Exception):
    """
    A type checker was asked to check a type it did not have registered.
    """

    type: Incomplete
    def __init__(self, type) -> None: ...

class UnknownType(Exception):
    """
    A validator was asked to validate an instance against an unknown type.
    """

    type: Incomplete
    instance: Incomplete
    schema: Incomplete
    def __init__(self, type, instance, schema) -> None: ...

class FormatError(Exception):
    """
    Validating a format failed.
    """

    message: Incomplete
    cause: Incomplete
    def __init__(self, message, cause=None) -> None: ...

class ErrorTree:
    """
    ErrorTrees make it easier to check which validations failed.
    """

    errors: MutableMapping[str, ValidationError]
    def __init__(self, errors: Iterable[ValidationError] = ()) -> None: ...
    def __contains__(self, index: object) -> bool:
        """
        Check whether ``instance[index]`` has any errors.
        """

    def __getitem__(self, index):
        """
        Retrieve the child tree one level down at the given ``index``.

        If the index is not in the instance that this tree corresponds
        to and is not known by this tree, whatever error would be raised
        by ``instance.__getitem__`` will be propagated (usually this is
        some subclass of `LookupError`.
        """

    @deprecated("ErrorTree.__setitem__ is deprecated without replacement.")
    def __setitem__(self, index: str | int, value: ErrorTree) -> None:
        """
        Add an error to the tree at the given ``index``.

        .. deprecated:: v4.20.0

            Setting items on an `ErrorTree` is deprecated without replacement.
            To populate a tree, provide all of its sub-errors when you
            construct the tree.
        """

    def __iter__(self) -> Iterator[str]:
        """
        Iterate (non-recursively) over the indices in the instance with errors.
        """

    def __len__(self) -> int:
        """
        Return the `total_errors`.
        """

    @property
    def total_errors(self):
        """
        The total number of errors in the entire tree, including children.
        """

def by_relevance(weak: Container[str] = ..., strong: Container[str] = ...) -> _RelevanceFuncType:
    """
    Create a key function that can be used to sort errors by relevance.

    Arguments:
        weak (set):
            a collection of validation keywords to consider to be
            "weak".  If there are two errors at the same level of the
            instance and one is in the set of weak validation keywords,
            the other error will take priority. By default, :kw:`anyOf`
            and :kw:`oneOf` are considered weak keywords and will be
            superseded by other same-level validation errors.

        strong (set):
            a collection of validation keywords to consider to be
            "strong"

    """

relevance: _RelevanceFuncType

def best_match(errors: Iterable[ValidationError], key: _RelevanceFuncType = ...):
    """
    Try to find an error that appears to be the best match among given errors.

    In general, errors that are higher up in the instance (i.e. for which
    `ValidationError.path` is shorter) are considered better matches,
    since they indicate "more" is wrong with the instance.

    If the resulting match is either :kw:`oneOf` or :kw:`anyOf`, the
    *opposite* assumption is made -- i.e. the deepest error is picked,
    since these keywords only need to match once, and any other errors
    may not be relevant.

    Arguments:
        errors (collections.abc.Iterable):

            the errors to select from. Do not provide a mixture of
            errors from different validation attempts (i.e. from
            different instances or schemas), since it won't produce
            sensical output.

        key (collections.abc.Callable):

            the key to use when sorting errors. See `relevance` and
            transitively `by_relevance` for more details (the default is
            to sort with the defaults of that function). Changing the
            default is only useful if you want to change the function
            that rates errors but still want the error context descent
            done by this function.

    Returns:
        the best matching error, or ``None`` if the iterable was empty

    .. note::

        This function is a heuristic. Its return value may change for a given
        set of inputs from version to version if better heuristics are added.

    """
