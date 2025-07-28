"""Contains _ExtensionDict class to represent extensions."""

from collections.abc import Iterator
from typing import Any, Generic, TypeVar

from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer
from google.protobuf.message import Message

_ContainerMessageT = TypeVar("_ContainerMessageT", bound=Message)
_ExtenderMessageT = TypeVar(
    "_ExtenderMessageT",
    bound=Message | RepeatedScalarFieldContainer[Any] | RepeatedCompositeFieldContainer[Any] | bool | float | str | bytes,
)

class _ExtensionFieldDescriptor(FieldDescriptor, Generic[_ContainerMessageT, _ExtenderMessageT]): ...

class _ExtensionDict(Generic[_ContainerMessageT]):
    """Dict-like container for Extension fields on proto instances.

    Note that in all cases we expect extension handles to be
    FieldDescriptors.
    """

    def __init__(self, extended_message: _ContainerMessageT) -> None:
        """
        Args:
          extended_message: Message instance for which we are the Extensions dict.
        """

    def __getitem__(
        self, extension_handle: _ExtensionFieldDescriptor[_ContainerMessageT, _ExtenderMessageT]
    ) -> _ExtenderMessageT:
        """Returns the current value of the given extension handle."""

    def __setitem__(
        self, extension_handle: _ExtensionFieldDescriptor[_ContainerMessageT, _ExtenderMessageT], value: _ExtenderMessageT
    ) -> None:
        """If extension_handle specifies a non-repeated, scalar extension
        field, sets the value of that field.
        """

    def __delitem__(self, extension_handle: _ExtensionFieldDescriptor[_ContainerMessageT, _ExtenderMessageT]) -> None: ...
    def __contains__(self, extension_handle: _ExtensionFieldDescriptor[_ContainerMessageT, _ExtenderMessageT]) -> bool: ...
    def __iter__(self) -> Iterator[_ExtensionFieldDescriptor[_ContainerMessageT, Any]]: ...
    def __len__(self) -> int: ...
