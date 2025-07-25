"""Contains well known classes.

This files defines well known classes which need extra maintenance including:
  - Any
  - Duration
  - FieldMask
  - Struct
  - Timestamp
"""

from _typeshed import Incomplete, SupportsItems
from collections.abc import Iterable, Iterator, KeysView, Mapping, Sequence
from datetime import datetime, timedelta, tzinfo
from typing import Any as tAny
from typing_extensions import TypeAlias

from google.protobuf import struct_pb2

class Any:
    """Class for Any Message type."""

    type_url: str
    value: Incomplete
    def Pack(self, msg, type_url_prefix: str = "type.googleapis.com/", deterministic=None) -> None:
        """Packs the specified message into current Any message."""

    def Unpack(self, msg) -> bool:
        """Unpacks the current Any message into specified message."""

    def TypeName(self) -> str:
        """Returns the protobuf type name of the inner message."""

    def Is(self, descriptor) -> bool:
        """Checks if this Any represents the given protobuf type."""

class Timestamp:
    """Class for Timestamp message type."""

    def ToJsonString(self) -> str:
        """Converts Timestamp to RFC 3339 date string format.

        Returns:
          A string converted from timestamp. The string is always Z-normalized
          and uses 3, 6 or 9 fractional digits as required to represent the
          exact time. Example of the return format: '1972-01-01T10:00:20.021Z'
        """
    seconds: int
    nanos: int
    def FromJsonString(self, value: str) -> None:
        """Parse a RFC 3339 date string format to Timestamp.

        Args:
          value: A date string. Any fractional digits (or none) and any offset are
              accepted as long as they fit into nano-seconds precision.
              Example of accepted format: '1972-01-01T10:00:20.021-05:00'

        Raises:
          ValueError: On parsing problems.
        """

    def GetCurrentTime(self) -> None:
        """Get the current UTC into Timestamp."""

    def ToNanoseconds(self) -> int:
        """Converts Timestamp to nanoseconds since epoch."""

    def ToMicroseconds(self) -> int:
        """Converts Timestamp to microseconds since epoch."""

    def ToMilliseconds(self) -> int:
        """Converts Timestamp to milliseconds since epoch."""

    def ToSeconds(self) -> int:
        """Converts Timestamp to seconds since epoch."""

    def FromNanoseconds(self, nanos: int) -> None:
        """Converts nanoseconds since epoch to Timestamp."""

    def FromMicroseconds(self, micros: int) -> None:
        """Converts microseconds since epoch to Timestamp."""

    def FromMilliseconds(self, millis: int) -> None:
        """Converts milliseconds since epoch to Timestamp."""

    def FromSeconds(self, seconds: int) -> None:
        """Converts seconds since epoch to Timestamp."""

    def ToDatetime(self, tzinfo: tzinfo | None = None) -> datetime:
        """Converts Timestamp to a datetime.

        Args:
          tzinfo: A datetime.tzinfo subclass; defaults to None.

        Returns:
          If tzinfo is None, returns a timezone-naive UTC datetime (with no timezone
          information, i.e. not aware that it's UTC).

          Otherwise, returns a timezone-aware datetime in the input timezone.
        """

    def FromDatetime(self, dt: datetime) -> None:
        """Converts datetime to Timestamp.

        Args:
          dt: A datetime. If it's timezone-naive, it's assumed to be in UTC.
        """

class Duration:
    """Class for Duration message type."""

    def ToJsonString(self) -> str:
        """Converts Duration to string format.

        Returns:
          A string converted from self. The string format will contains
          3, 6, or 9 fractional digits depending on the precision required to
          represent the exact Duration value. For example: "1s", "1.010s",
          "1.000000100s", "-3.100s"
        """
    seconds: int
    nanos: int
    def FromJsonString(self, value: tAny) -> None:
        """Converts a string to Duration.

        Args:
          value: A string to be converted. The string must end with 's'. Any
              fractional digits (or none) are accepted as long as they fit into
              precision. For example: "1s", "1.01s", "1.0000001s", "-3.100s

        Raises:
          ValueError: On parsing problems.
        """

    def ToNanoseconds(self) -> int:
        """Converts a Duration to nanoseconds."""

    def ToMicroseconds(self) -> int:
        """Converts a Duration to microseconds."""

    def ToMilliseconds(self) -> int:
        """Converts a Duration to milliseconds."""

    def ToSeconds(self) -> int:
        """Converts a Duration to seconds."""

    def FromNanoseconds(self, nanos: int) -> None:
        """Converts nanoseconds to Duration."""

    def FromMicroseconds(self, micros: int) -> None:
        """Converts microseconds to Duration."""

    def FromMilliseconds(self, millis: int) -> None:
        """Converts milliseconds to Duration."""

    def FromSeconds(self, seconds: int) -> None:
        """Converts seconds to Duration."""

    def ToTimedelta(self) -> timedelta:
        """Converts Duration to timedelta."""

    def FromTimedelta(self, td: timedelta) -> None:
        """Converts timedelta to Duration."""

class FieldMask:
    """Class for FieldMask message type."""

    def ToJsonString(self) -> str:
        """Converts FieldMask to string according to proto3 JSON spec."""

    def FromJsonString(self, value: tAny) -> None:
        """Converts string to FieldMask according to proto3 JSON spec."""

    def IsValidForDescriptor(self, message_descriptor: tAny):
        """Checks whether the FieldMask is valid for Message Descriptor."""

    def AllFieldsFromDescriptor(self, message_descriptor: tAny) -> None:
        """Gets all direct fields of Message Descriptor to FieldMask."""

    def CanonicalFormFromMask(self, mask: tAny) -> None:
        """Converts a FieldMask to the canonical form.

        Removes paths that are covered by another path. For example,
        "foo.bar" is covered by "foo" and will be removed if "foo"
        is also in the FieldMask. Then sorts all paths in alphabetical order.

        Args:
          mask: The original FieldMask to be converted.
        """

    def Union(self, mask1: tAny, mask2: tAny) -> None:
        """Merges mask1 and mask2 into this FieldMask."""

    def Intersect(self, mask1: tAny, mask2: tAny) -> None:
        """Intersects mask1 and mask2 into this FieldMask."""

    def MergeMessage(
        self, source: tAny, destination: tAny, replace_message_field: bool = False, replace_repeated_field: bool = False
    ) -> None:
        """Merges fields specified in FieldMask from source to destination.

        Args:
          source: Source message.
          destination: The destination message to be merged into.
          replace_message_field: Replace message field if True. Merge message
              field if False.
          replace_repeated_field: Replace repeated field if True. Append
              elements of repeated field if False.
        """

class _FieldMaskTree:
    def __init__(self, field_mask: Incomplete | None = ...) -> None: ...
    def MergeFromFieldMask(self, field_mask: tAny) -> None: ...
    def AddPath(self, path: tAny): ...
    def ToFieldMask(self, field_mask: tAny) -> None: ...
    def IntersectPath(self, path: tAny, intersection: tAny): ...
    def AddLeafNodes(self, prefix: tAny, node: tAny) -> None: ...
    def MergeMessage(self, source: tAny, destination: tAny, replace_message: tAny, replace_repeated: tAny) -> None: ...

_StructValue: TypeAlias = struct_pb2.Struct | struct_pb2.ListValue | str | float | bool | None
_StructValueArg: TypeAlias = _StructValue | Mapping[str, _StructValueArg] | Sequence[_StructValueArg]

class Struct:
    """Class for Struct message type."""

    def __getitem__(self, key: str) -> _StructValue: ...
    def __setitem__(self, key: str, value: _StructValueArg) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[str]: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> list[_StructValue]: ...
    def items(self) -> list[tuple[str, _StructValue]]: ...
    def get_or_create_list(self, key: str) -> struct_pb2.ListValue:
        """Returns a list for this key, creating if it didn't exist already."""

    def get_or_create_struct(self, key: str) -> struct_pb2.Struct:
        """Returns a struct for this key, creating if it didn't exist already."""

    def update(self, dictionary: SupportsItems[str, _StructValueArg]) -> None: ...

class ListValue:
    """Class for ListValue message type."""

    def __len__(self) -> int: ...
    def append(self, value: _StructValue) -> None: ...
    def extend(self, elem_seq: Iterable[_StructValue]) -> None: ...
    def __getitem__(self, index: int) -> _StructValue:
        """Retrieves item by the specified index."""

    def __setitem__(self, index: int, value: _StructValueArg) -> None: ...
    def __delitem__(self, key: int) -> None: ...
    # Doesn't actually exist at runtime; needed so type checkers understand the class is iterable
    def __iter__(self) -> Iterator[_StructValue]: ...
    def items(self) -> Iterator[_StructValue]: ...
    def add_struct(self) -> struct_pb2.Struct:
        """Appends and returns a struct value as the next value in the list."""

    def add_list(self) -> struct_pb2.ListValue:
        """Appends and returns a list value as the next value in the list."""

WKTBASES: dict[str, type[tAny]]
