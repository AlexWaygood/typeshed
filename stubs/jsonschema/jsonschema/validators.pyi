"""
Creation and extension of validators, with implementations for existing drafts.
"""

from _typeshed import Incomplete, SupportsKeysAndGetItem
from collections.abc import Callable, Generator, Iterable, Iterator, Mapping
from contextlib import contextmanager
from typing import Any, ClassVar, overload
from typing_extensions import TypeAlias, deprecated

from referencing.jsonschema import Schema, SchemaRegistry
from referencing.typing import URI

from ._format import FormatChecker
from ._types import TypeChecker
from ._utils import Unset, URIDict
from .exceptions import ValidationError
from .protocols import Validator

# these type aliases do not exist at runtime, they're only defined here in the stub
_JsonObject: TypeAlias = Mapping[str, Any]
_JsonValue: TypeAlias = _JsonObject | list[Any] | str | int | float | bool | None
_ValidatorCallback: TypeAlias = Callable[[Any, Any, _JsonValue, _JsonObject], Iterator[ValidationError]]

# This class does not exist at runtime. Compatible classes are created at
# runtime by create().
class _Validator:
    VALIDATORS: ClassVar[dict[Incomplete, Incomplete]]
    META_SCHEMA: ClassVar[dict[Incomplete, Incomplete]]
    TYPE_CHECKER: ClassVar[Incomplete]
    FORMAT_CHECKER: ClassVar[Incomplete]
    @staticmethod
    def ID_OF(contents: Schema) -> URI | None: ...
    schema: Schema
    format_checker: FormatChecker | None
    def __init__(
        self,
        schema: Schema,
        resolver=None,
        format_checker: FormatChecker | None = None,
        *,
        registry: SchemaRegistry = ...,
        _resolver=None,
    ) -> None: ...
    @classmethod
    def check_schema(cls, schema: Schema, format_checker: FormatChecker | Unset = ...) -> None: ...
    @property
    @deprecated(
        "Accessing resolver() is deprecated as of v4.18.0, "
        "in favor of the https://github.com/python-jsonschema/referencing library."
    )
    def resolver(self): ...
    def evolve(self, **changes) -> _Validator: ...
    @overload
    def iter_errors(self, instance) -> Generator[Incomplete]: ...
    @overload
    @deprecated("Passing a schema to Validator.iter_errors is deprecated and will be removed in a future release.")
    def iter_errors(self, instance, _schema: Schema | None) -> Generator[Incomplete]: ...
    def descend(
        self, instance, schema: Schema, path: Incomplete | None = ..., schema_path: Incomplete | None = ..., resolver=None
    ) -> Generator[Incomplete]: ...
    def validate(self, *args, **kwargs) -> None: ...
    def is_type(self, instance, type) -> bool: ...
    @overload
    def is_valid(self, instance) -> bool: ...
    @overload
    @deprecated("Passing a schema to Validator.is_valid is deprecated and will be removed in a future release.")
    def is_valid(self, instance, _schema: Schema | None) -> bool: ...

def validates(version: str) -> Callable[[_Validator], _Validator]:
    """
    Register the decorated validator for a ``version`` of the specification.

    Registered validators and their meta schemas will be considered when
    parsing :kw:`$schema` keywords' URIs.

    Arguments:

        version (str):

            An identifier to use as the version's name

    Returns:

        collections.abc.Callable:

            a class decorator to decorate the validator with the version

    """

def create(
    meta_schema: Schema,
    validators: Mapping[str, _ValidatorCallback] | tuple[()] = (),
    version=None,
    type_checker: TypeChecker = ...,
    format_checker: FormatChecker = ...,
    id_of: Callable[[Schema], str] = ...,
    applicable_validators: Callable[[Schema], Iterable[tuple[str, _ValidatorCallback]]] = ...,
) -> type[_Validator]:
    """
    Create a new validator class.

    Arguments:

        meta_schema:

            the meta schema for the new validator class

        validators:

            a mapping from names to callables, where each callable will
            validate the schema property with the given name.

            Each callable should take 4 arguments:

                1. a validator instance,
                2. the value of the property being validated within the
                   instance
                3. the instance
                4. the schema

        version:

            an identifier for the version that this validator class will
            validate. If provided, the returned validator class will
            have its ``__name__`` set to include the version, and also
            will have `jsonschema.validators.validates` automatically
            called for the given version.

        type_checker:

            a type checker, used when applying the :kw:`type` keyword.

            If unprovided, a `jsonschema.TypeChecker` will be created
            with a set of default types typical of JSON Schema drafts.

        format_checker:

            a format checker, used when applying the :kw:`format` keyword.

            If unprovided, a `jsonschema.FormatChecker` will be created
            with a set of default formats typical of JSON Schema drafts.

        id_of:

            A function that given a schema, returns its ID.

        applicable_validators:

            A function that, given a schema, returns the list of
            applicable schema keywords and associated values
            which will be used to validate the instance.
            This is mostly used to support pre-draft 7 versions of JSON Schema
            which specified behavior around ignoring keywords if they were
            siblings of a ``$ref`` keyword. If you're not attempting to
            implement similar behavior, you can typically ignore this argument
            and leave it at its default.

    Returns:

        a new `jsonschema.protocols.Validator` class

    """

def extend(validator, validators=(), version=None, type_checker=None, format_checker=None):
    """
    Create a new validator class by extending an existing one.

    Arguments:

        validator (jsonschema.protocols.Validator):

            an existing validator class

        validators (collections.abc.Mapping):

            a mapping of new validator callables to extend with, whose
            structure is as in `create`.

            .. note::

                Any validator callables with the same name as an
                existing one will (silently) replace the old validator
                callable entirely, effectively overriding any validation
                done in the "parent" validator class.

                If you wish to instead extend the behavior of a parent's
                validator callable, delegate and call it directly in
                the new validator function by retrieving it using
                ``OldValidator.VALIDATORS["validation_keyword_name"]``.

        version (str):

            a version for the new validator class

        type_checker (jsonschema.TypeChecker):

            a type checker, used when applying the :kw:`type` keyword.

            If unprovided, the type checker of the extended
            `jsonschema.protocols.Validator` will be carried along.

        format_checker (jsonschema.FormatChecker):

            a format checker, used when applying the :kw:`format` keyword.

            If unprovided, the format checker of the extended
            `jsonschema.protocols.Validator` will be carried along.

    Returns:

        a new `jsonschema.protocols.Validator` class extending the one
        provided

    .. note:: Meta Schemas

        The new validator class will have its parent's meta schema.

        If you wish to change or extend the meta schema in the new
        validator class, modify ``META_SCHEMA`` directly on the returned
        class. Note that no implicit copying is done, so a copy should
        likely be made before modifying it, in order to not affect the
        old validator.

    """

# At runtime these are fields that are assigned the return values of create() calls.
class Draft3Validator(_Validator): ...
class Draft4Validator(_Validator): ...
class Draft6Validator(_Validator): ...
class Draft7Validator(_Validator): ...
class Draft201909Validator(_Validator): ...
class Draft202012Validator(_Validator): ...

_Handler: TypeAlias = Callable[[str], Incomplete]

class RefResolver:
    referrer: dict[str, Incomplete]
    cache_remote: Incomplete
    handlers: dict[str, _Handler]
    store: URIDict
    def __init__(
        self,
        base_uri: str,
        referrer: dict[str, Incomplete],
        store: SupportsKeysAndGetItem[str, str] | Iterable[tuple[str, str]] = ...,
        cache_remote: bool = True,
        handlers: SupportsKeysAndGetItem[str, _Handler] | Iterable[tuple[str, _Handler]] = (),
        urljoin_cache=None,
        remote_cache=None,
    ) -> None: ...
    @classmethod
    def from_schema(cls, schema: Schema, id_of=..., *args, **kwargs): ...
    def push_scope(self, scope) -> None: ...
    def pop_scope(self) -> None: ...
    @property
    def resolution_scope(self): ...
    @property
    def base_uri(self) -> str: ...
    @contextmanager
    @deprecated("jsonschema.RefResolver.in_scope is deprecated and will be removed in a future release.")
    def in_scope(self, scope) -> Generator[None]: ...
    @contextmanager
    def resolving(self, ref: str) -> Generator[Incomplete]: ...
    def resolve(self, ref: str) -> tuple[str, Incomplete]: ...
    def resolve_from_url(self, url: str): ...
    def resolve_fragment(self, document, fragment: str): ...
    def resolve_remote(self, uri: str): ...

def validate(instance: object, schema: Schema, cls: type[_Validator] | None = None, *args: Any, **kwargs: Any) -> None:
    """
    Validate an instance under the given schema.

        >>> validate([2, 3, 4], {"maxItems": 2})
        Traceback (most recent call last):
            ...
        ValidationError: [2, 3, 4] is too long

    :func:`~jsonschema.validators.validate` will first verify that the
    provided schema is itself valid, since not doing so can lead to less
    obvious error messages and fail in less obvious or consistent ways.

    If you know you have a valid schema already, especially
    if you intend to validate multiple instances with
    the same schema, you likely would prefer using the
    `jsonschema.protocols.Validator.validate` method directly on a
    specific validator (e.g. ``Draft202012Validator.validate``).


    Arguments:

        instance:

            The instance to validate

        schema:

            The schema to validate with

        cls (jsonschema.protocols.Validator):

            The class that will be used to validate the instance.

    If the ``cls`` argument is not provided, two things will happen
    in accordance with the specification. First, if the schema has a
    :kw:`$schema` keyword containing a known meta-schema [#]_ then the
    proper validator will be used. The specification recommends that
    all schemas contain :kw:`$schema` properties for this reason. If no
    :kw:`$schema` property is found, the default validator class is the
    latest released draft.

    Any other provided positional and keyword arguments will be passed
    on when instantiating the ``cls``.

    Raises:

        `jsonschema.exceptions.ValidationError`:

            if the instance is invalid

        `jsonschema.exceptions.SchemaError`:

            if the schema itself is invalid

    .. rubric:: Footnotes
    .. [#] known by a validator registered with
        `jsonschema.validators.validates`

    """

def validator_for(schema: Schema | bool, default: type[Validator] | Unset = ...) -> type[Validator]:
    """
    Retrieve the validator class appropriate for validating the given schema.

    Uses the :kw:`$schema` keyword that should be present in the given
    schema to look up the appropriate validator class.

    Arguments:

        schema (collections.abc.Mapping or bool):

            the schema to look at

        default:

            the default to return if the appropriate validator class
            cannot be determined.

            If unprovided, the default is to return the latest supported
            draft.

    Examples:

        The :kw:`$schema` JSON Schema keyword will control which validator
        class is returned:

        >>> schema = {
        ...     "$schema": "https://json-schema.org/draft/2020-12/schema",
        ...     "type": "integer",
        ... }
        >>> jsonschema.validators.validator_for(schema)
        <class 'jsonschema.validators.Draft202012Validator'>


        Here, a draft 7 schema instead will return the draft 7 validator:

        >>> schema = {
        ...     "$schema": "http://json-schema.org/draft-07/schema#",
        ...     "type": "integer",
        ... }
        >>> jsonschema.validators.validator_for(schema)
        <class 'jsonschema.validators.Draft7Validator'>


        Schemas with no ``$schema`` keyword will fallback to the default
        argument:

        >>> schema = {"type": "integer"}
        >>> jsonschema.validators.validator_for(
        ...     schema, default=Draft7Validator,
        ... )
        <class 'jsonschema.validators.Draft7Validator'>

        or if none is provided, to the latest version supported.
        Always including the keyword when authoring schemas is highly
        recommended.

    """
