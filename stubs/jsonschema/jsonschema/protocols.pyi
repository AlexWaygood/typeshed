"""
typing.Protocol classes for jsonschema interfaces.
"""

from _typeshed import Incomplete
from collections.abc import Iterator, Mapping, Sequence
from typing import ClassVar, Protocol
from typing_extensions import TypeAlias

import referencing.jsonschema
from jsonschema._format import FormatChecker
from jsonschema._types import TypeChecker
from jsonschema.exceptions import ValidationError

_JsonParameter: TypeAlias = str | int | float | bool | None | Mapping[str, _JsonParameter] | Sequence[_JsonParameter]

class Validator(Protocol):
    """
    The protocol to which all validator classes adhere.

    Arguments:

        schema:

            The schema that the validator object will validate with.
            It is assumed to be valid, and providing
            an invalid schema can lead to undefined behavior. See
            `Validator.check_schema` to validate a schema first.

        registry:

            a schema registry that will be used for looking up JSON references

        resolver:

            a resolver that will be used to resolve :kw:`$ref`
            properties (JSON references). If unprovided, one will be created.

            .. deprecated:: v4.18.0

                `RefResolver <_RefResolver>` has been deprecated in favor of
                `referencing`, and with it, this argument.

        format_checker:

            if provided, a checker which will be used to assert about
            :kw:`format` properties present in the schema. If unprovided,
            *no* format validation is done, and the presence of format
            within schemas is strictly informational. Certain formats
            require additional packages to be installed in order to assert
            against instances. Ensure you've installed `jsonschema` with
            its `extra (optional) dependencies <index:extras>` when
            invoking ``pip``.

    .. deprecated:: v4.12.0

        Subclassing validator classes now explicitly warns this is not part of
        their public API.

    """

    META_SCHEMA: ClassVar[dict[Incomplete, Incomplete]]
    VALIDATORS: ClassVar[dict[Incomplete, Incomplete]]
    TYPE_CHECKER: ClassVar[TypeChecker]
    FORMAT_CHECKER: ClassVar[FormatChecker]
    schema: dict[Incomplete, Incomplete] | bool
    def __init__(
        self,
        schema: dict[Incomplete, Incomplete] | bool,
        registry: referencing.jsonschema.SchemaRegistry,
        format_checker: FormatChecker | None = None,
    ) -> None: ...
    @classmethod
    def check_schema(cls, schema: dict[Incomplete, Incomplete]) -> None:
        """
        Validate the given schema against the validator's `META_SCHEMA`.

        Raises:

            `jsonschema.exceptions.SchemaError`:

                if the schema is invalid

        """

    def is_type(self, instance: _JsonParameter, type: str) -> bool:
        """
        Check if the instance is of the given (JSON Schema) type.

        Arguments:

            instance:

                the value to check

            type:

                the name of a known (JSON Schema) type

        Returns:

            whether the instance is of the given type

        Raises:

            `jsonschema.exceptions.UnknownType`:

                if ``type`` is not a known type

        """

    def is_valid(self, instance: _JsonParameter) -> bool:
        """
        Check if the instance is valid under the current `schema`.

        Returns:

            whether the instance is valid or not

        >>> schema = {"maxItems" : 2}
        >>> Draft202012Validator(schema).is_valid([2, 3, 4])
        False

        """

    def iter_errors(self, instance: _JsonParameter) -> Iterator[ValidationError]:
        """
        Lazily yield each of the validation errors in the given instance.

        >>> schema = {
        ...     "type" : "array",
        ...     "items" : {"enum" : [1, 2, 3]},
        ...     "maxItems" : 2,
        ... }
        >>> v = Draft202012Validator(schema)
        >>> for error in sorted(v.iter_errors([2, 3, 4]), key=str):
        ...     print(error.message)
        4 is not one of [1, 2, 3]
        [2, 3, 4] is too long

        .. deprecated:: v4.0.0

            Calling this function with a second schema argument is deprecated.
            Use `Validator.evolve` instead.
        """

    def validate(self, instance: _JsonParameter) -> None:
        """
        Check if the instance is valid under the current `schema`.

        Raises:

            `jsonschema.exceptions.ValidationError`:

                if the instance is invalid

        >>> schema = {"maxItems" : 2}
        >>> Draft202012Validator(schema).validate([2, 3, 4])
        Traceback (most recent call last):
            ...
        ValidationError: [2, 3, 4] is too long

        """

    def evolve(self, **kwargs) -> Validator:
        """
        Create a new validator like this one, but with given changes.

        Preserves all other attributes, so can be used to e.g. create a
        validator with a different schema but with the same :kw:`$ref`
        resolution behavior.

        >>> validator = Draft202012Validator({})
        >>> validator.evolve(schema={"type": "number"})
        Draft202012Validator(schema={'type': 'number'}, format_checker=None)

        The returned object satisfies the validator protocol, but may not
        be of the same concrete class! In particular this occurs
        when a :kw:`$ref` occurs to a schema with a different
        :kw:`$schema` than this one (i.e. for a different draft).

        >>> validator.evolve(
        ...     schema={"$schema": Draft7Validator.META_SCHEMA["$id"]}
        ... )
        Draft7Validator(schema=..., format_checker=None)
        """
