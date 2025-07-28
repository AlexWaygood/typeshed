"""Provides type checking routines.

This module defines type checking utilities in the forms of dictionaries:

VALUE_CHECKERS: A dictionary of field types and a value validation object.
TYPE_TO_BYTE_SIZE_FN: A dictionary with field types and a size computing
  function.
TYPE_TO_SERIALIZE_METHOD: A dictionary with field types and serialization
  function.
FIELD_TYPE_TO_WIRE_TYPE: A dictionary with field typed and their
  corresponding wire types.
TYPE_TO_DESERIALIZE_METHOD: A dictionary with field types and deserialization
  function.
"""

from typing import Generic, TypeVar

_T = TypeVar("_T")

class TypeChecker(Generic[_T]):
    """Type checker used to catch type errors as early as possible
    when the client is setting scalar fields in protocol messages.
    """

    def __init__(self, *acceptable_types: _T): ...
    def CheckValue(self, proposed_value: _T) -> _T:
        """Type check the provided value and return it.

        The returned value might have been normalized to another type.
        """

class TypeCheckerWithDefault(TypeChecker[_T]):
    def __init__(self, default_value: _T, *acceptable_types: _T): ...
    def DefaultValue(self) -> _T: ...
