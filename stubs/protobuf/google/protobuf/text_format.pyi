"""Contains routines for printing protocol messages in text format.

Simple usage example::

  # Create a proto object and serialize it to a text proto string.
  message = my_proto_pb2.MyMessage(foo='bar')
  text_proto = text_format.MessageToString(message)

  # Parse a text proto string.
  message = text_format.Parse(text_proto, my_proto_pb2.MyMessage())
"""

from _typeshed import SupportsWrite
from collections.abc import Callable, Iterable
from typing import Any, TypeVar
from typing_extensions import TypeAlias

from .descriptor import FieldDescriptor
from .descriptor_pool import DescriptorPool
from .message import Message

_M = TypeVar("_M", bound=Message)  # message type (of self)

class Error(Exception):
    """Top-level module error for text_format."""

class ParseError(Error):
    """Thrown in case of text parsing or tokenizing error."""

    def __init__(self, message: str | None = None, line: int | None = None, column: int | None = None) -> None: ...
    def GetLine(self) -> int | None: ...
    def GetColumn(self) -> int | None: ...

class TextWriter:
    def __init__(self, as_utf8: bool) -> None: ...
    def write(self, val: str) -> int: ...
    def getvalue(self) -> str: ...
    def close(self) -> None: ...

_MessageFormatter: TypeAlias = Callable[[Message, int, bool], str | None]

def MessageToString(
    message: Message,
    as_utf8: bool = True,
    as_one_line: bool = False,
    use_short_repeated_primitives: bool = False,
    pointy_brackets: bool = False,
    use_index_order: bool = False,
    float_format: str | None = None,
    double_format: str | None = None,
    use_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    indent: int = 0,
    message_formatter: _MessageFormatter | None = None,
    print_unknown_fields: bool = False,
    force_colon: bool = False,
) -> str:
    """Convert protobuf message to text format.

    Double values can be formatted compactly with 15 digits of
    precision (which is the most that IEEE 754 "double" can guarantee)
    using double_format='.15g'. To ensure that converting to text and back to a
    proto will result in an identical value, double_format='.17g' should be used.

    Args:
      message: The protocol buffers message.
      as_utf8: Return unescaped Unicode for non-ASCII characters.
      as_one_line: Don't introduce newlines between fields.
      use_short_repeated_primitives: Use short repeated format for primitives.
      pointy_brackets: If True, use angle brackets instead of curly braces for
        nesting.
      use_index_order: If True, fields of a proto message will be printed using
        the order defined in source code instead of the field number, extensions
        will be printed at the end of the message and their relative order is
        determined by the extension number. By default, use the field number
        order.
      float_format (str): If set, use this to specify float field formatting
        (per the "Format Specification Mini-Language"); otherwise, shortest float
        that has same value in wire will be printed. Also affect double field
        if double_format is not set but float_format is set.
      double_format (str): If set, use this to specify double field formatting
        (per the "Format Specification Mini-Language"); if it is not set but
        float_format is set, use float_format. Otherwise, use ``str()``
      use_field_number: If True, print field numbers instead of names.
      descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
      indent (int): The initial indent level, in terms of spaces, for pretty
        print.
      message_formatter (function(message, indent, as_one_line) -> unicode|None):
        Custom formatter for selected sub-messages (usually based on message
        type). Use to pretty print parts of the protobuf for easier diffing.
      print_unknown_fields: If True, unknown fields will be printed.
      force_colon: If set, a colon will be added after the field name even if the
        field is a proto message.

    Returns:
      str: A string of the text formatted protocol buffer message.
    """

def MessageToBytes(
    message: Message,
    *,
    # Same kwargs as MessageToString
    as_utf8: bool = True,
    as_one_line: bool = False,
    use_short_repeated_primitives: bool = False,
    pointy_brackets: bool = False,
    use_index_order: bool = False,
    float_format: str | None = None,
    double_format: str | None = None,
    use_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    indent: int = 0,
    message_formatter: _MessageFormatter | None = None,
    print_unknown_fields: bool = False,
    force_colon: bool = False,
) -> bytes:
    """Convert protobuf message to encoded text format.  See MessageToString."""

def PrintMessage(
    message: Message,
    out: SupportsWrite[str],
    indent: int = 0,
    as_utf8: bool = True,
    as_one_line: bool = False,
    use_short_repeated_primitives: bool = False,
    pointy_brackets: bool = False,
    use_index_order: bool = False,
    float_format: str | None = None,
    double_format: str | None = None,
    use_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    message_formatter: _MessageFormatter | None = None,
    print_unknown_fields: bool = False,
    force_colon: bool = False,
) -> None:
    """Convert the message to text format and write it to the out stream.

    Args:
      message: The Message object to convert to text format.
      out: A file handle to write the message to.
      indent: The initial indent level for pretty print.
      as_utf8: Return unescaped Unicode for non-ASCII characters.
      as_one_line: Don't introduce newlines between fields.
      use_short_repeated_primitives: Use short repeated format for primitives.
      pointy_brackets: If True, use angle brackets instead of curly braces for
        nesting.
      use_index_order: If True, print fields of a proto message using the order
        defined in source code instead of the field number. By default, use the
        field number order.
      float_format: If set, use this to specify float field formatting
        (per the "Format Specification Mini-Language"); otherwise, shortest
        float that has same value in wire will be printed. Also affect double
        field if double_format is not set but float_format is set.
      double_format: If set, use this to specify double field formatting
        (per the "Format Specification Mini-Language"); if it is not set but
        float_format is set, use float_format. Otherwise, str() is used.
      use_field_number: If True, print field numbers instead of names.
      descriptor_pool: A DescriptorPool used to resolve Any types.
      message_formatter: A function(message, indent, as_one_line): unicode|None
        to custom format selected sub-messages (usually based on message type).
        Use to pretty print parts of the protobuf for easier diffing.
      print_unknown_fields: If True, unknown fields will be printed.
      force_colon: If set, a colon will be added after the field name even if
        the field is a proto message.
    """

def PrintField(
    field: FieldDescriptor,
    value: Any,
    out: SupportsWrite[str],
    indent: int = 0,
    as_utf8: bool = True,
    as_one_line: bool = False,
    use_short_repeated_primitives: bool = False,
    pointy_brackets: bool = False,
    use_index_order: bool = False,
    float_format: str | None = None,
    double_format: str | None = None,
    message_formatter: _MessageFormatter | None = None,
    print_unknown_fields: bool = False,
    force_colon: bool = False,
) -> None:
    """Print a single field name/value pair."""

def PrintFieldValue(
    field: FieldDescriptor,
    value: Any,
    out: SupportsWrite[str],
    indent: int = 0,
    as_utf8: bool = True,
    as_one_line: bool = False,
    use_short_repeated_primitives: bool = False,
    pointy_brackets: bool = False,
    use_index_order: bool = False,
    float_format: str | None = None,
    double_format: str | None = None,
    message_formatter: _MessageFormatter | None = None,
    print_unknown_fields: bool = False,
    force_colon: bool = False,
) -> None:
    """Print a single field value (not including name)."""

class _Printer:
    """Text format printer for protocol message."""

    out: SupportsWrite[str]
    indent: int
    as_utf8: bool
    as_one_line: bool
    use_short_repeated_primitives: bool
    pointy_brackets: bool
    use_index_order: bool
    float_format: str | None
    double_format: str | None
    use_field_number: bool
    descriptor_pool: DescriptorPool | None
    message_formatter: _MessageFormatter | None
    print_unknown_fields: bool
    force_colon: bool
    def __init__(
        self,
        out: SupportsWrite[str],
        indent: int = 0,
        as_utf8: bool = True,
        as_one_line: bool = False,
        use_short_repeated_primitives: bool = False,
        pointy_brackets: bool = False,
        use_index_order: bool = False,
        float_format: str | None = None,
        double_format: str | None = None,
        use_field_number: bool = False,
        descriptor_pool: DescriptorPool | None = None,
        message_formatter: _MessageFormatter | None = None,
        print_unknown_fields: bool = False,
        force_colon: bool = False,
    ) -> None:
        """Initialize the Printer.

        Double values can be formatted compactly with 15 digits of precision
        (which is the most that IEEE 754 "double" can guarantee) using
        double_format='.15g'. To ensure that converting to text and back to a proto
        will result in an identical value, double_format='.17g' should be used.

        Args:
          out: To record the text format result.
          indent: The initial indent level for pretty print.
          as_utf8: Return unescaped Unicode for non-ASCII characters.
          as_one_line: Don't introduce newlines between fields.
          use_short_repeated_primitives: Use short repeated format for primitives.
          pointy_brackets: If True, use angle brackets instead of curly braces for
            nesting.
          use_index_order: If True, print fields of a proto message using the order
            defined in source code instead of the field number. By default, use the
            field number order.
          float_format: If set, use this to specify float field formatting
            (per the "Format Specification Mini-Language"); otherwise, shortest
            float that has same value in wire will be printed. Also affect double
            field if double_format is not set but float_format is set.
          double_format: If set, use this to specify double field formatting
            (per the "Format Specification Mini-Language"); if it is not set but
            float_format is set, use float_format. Otherwise, str() is used.
          use_field_number: If True, print field numbers instead of names.
          descriptor_pool: A DescriptorPool used to resolve Any types.
          message_formatter: A function(message, indent, as_one_line): unicode|None
            to custom format selected sub-messages (usually based on message type).
            Use to pretty print parts of the protobuf for easier diffing.
          print_unknown_fields: If True, unknown fields will be printed.
          force_colon: If set, a colon will be added after the field name even if
            the field is a proto message.
        """

    def PrintMessage(self, message: Message) -> None:
        """Convert protobuf message to text format.

        Args:
          message: The protocol buffers message.
        """

    def PrintField(self, field: FieldDescriptor, value: Any) -> None:
        """Print a single field name/value pair."""

    def PrintFieldValue(self, field: FieldDescriptor, value: Any) -> None:
        """Print a single field value (not including name).

        For repeated fields, the value should be a single element.

        Args:
          field: The descriptor of the field to be printed.
          value: The value of the field.
        """

def Parse(
    text: str | bytes,
    message: _M,
    allow_unknown_extension: bool = False,
    allow_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    allow_unknown_field: bool = False,
) -> _M:
    """Parses a text representation of a protocol message into a message.

    NOTE: for historical reasons this function does not clear the input
    message. This is different from what the binary msg.ParseFrom(...) does.
    If text contains a field already set in message, the value is appended if the
    field is repeated. Otherwise, an error is raised.

    Example::

      a = MyProto()
      a.repeated_field.append('test')
      b = MyProto()

      # Repeated fields are combined
      text_format.Parse(repr(a), b)
      text_format.Parse(repr(a), b) # repeated_field contains ["test", "test"]

      # Non-repeated fields cannot be overwritten
      a.singular_field = 1
      b.singular_field = 2
      text_format.Parse(repr(a), b) # ParseError

      # Binary version:
      b.ParseFromString(a.SerializeToString()) # repeated_field is now "test"

    Caller is responsible for clearing the message as needed.

    Args:
      text (str): Message text representation.
      message (Message): A protocol buffer message to merge into.
      allow_unknown_extension: if True, skip over missing extensions and keep
        parsing
      allow_field_number: if True, both field number and field name are allowed.
      descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
      allow_unknown_field: if True, skip over unknown field and keep
        parsing. Avoid to use this option if possible. It may hide some
        errors (e.g. spelling error on field name)

    Returns:
      Message: The same message passed as argument.

    Raises:
      ParseError: On text parsing problems.
    """

def Merge(
    text: str | bytes,
    message: _M,
    allow_unknown_extension: bool = False,
    allow_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    allow_unknown_field: bool = False,
) -> _M:
    """Parses a text representation of a protocol message into a message.

    Like Parse(), but allows repeated values for a non-repeated field, and uses
    the last one. This means any non-repeated, top-level fields specified in text
    replace those in the message.

    Args:
      text (str): Message text representation.
      message (Message): A protocol buffer message to merge into.
      allow_unknown_extension: if True, skip over missing extensions and keep
        parsing
      allow_field_number: if True, both field number and field name are allowed.
      descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
      allow_unknown_field: if True, skip over unknown field and keep
        parsing. Avoid to use this option if possible. It may hide some
        errors (e.g. spelling error on field name)

    Returns:
      Message: The same message passed as argument.

    Raises:
      ParseError: On text parsing problems.
    """

def MergeLines(
    lines: Iterable[str | bytes],
    message: _M,
    allow_unknown_extension: bool = False,
    allow_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    allow_unknown_field: bool = False,
) -> _M:
    """Parses a text representation of a protocol message into a message.

    See Merge() for more details.

    Args:
      lines: An iterable of lines of a message's text representation.
      message: A protocol buffer message to merge into.
      allow_unknown_extension: if True, skip over missing extensions and keep
        parsing
      allow_field_number: if True, both field number and field name are allowed.
      descriptor_pool: A DescriptorPool used to resolve Any types.
      allow_unknown_field: if True, skip over unknown field and keep
        parsing. Avoid to use this option if possible. It may hide some
        errors (e.g. spelling error on field name)

    Returns:
      The same message passed as argument.

    Raises:
      ParseError: On text parsing problems.
    """

class _Parser:
    """Text format parser for protocol message."""

    allow_unknown_extension: bool
    allow_field_number: bool
    descriptor_pool: DescriptorPool | None
    allow_unknown_field: bool
    def __init__(
        self,
        allow_unknown_extension: bool = False,
        allow_field_number: bool = False,
        descriptor_pool: DescriptorPool | None = None,
        allow_unknown_field: bool = False,
    ) -> None: ...
    def ParseLines(self, lines: Iterable[str | bytes], message: _M) -> _M:
        """Parses a text representation of a protocol message into a message."""

    def MergeLines(self, lines: Iterable[str | bytes], message: _M) -> _M:
        """Merges a text representation of a protocol message into a message."""

_ParseError: TypeAlias = ParseError

class Tokenizer:
    """Protocol buffer text representation tokenizer.

    This class handles the lower level string parsing by splitting it into
    meaningful tokens.

    It was directly ported from the Java protocol buffer API.
    """

    token: str
    def __init__(self, lines: Iterable[str], skip_comments: bool = True) -> None: ...
    def LookingAt(self, token: str) -> bool: ...
    def AtEnd(self) -> bool:
        """Checks the end of the text was reached.

        Returns:
          True iff the end was reached.
        """

    def TryConsume(self, token: str) -> bool:
        """Tries to consume a given piece of text.

        Args:
          token: Text to consume.

        Returns:
          True iff the text was consumed.
        """

    def Consume(self, token: str) -> None:
        """Consumes a piece of text.

        Args:
          token: Text to consume.

        Raises:
          ParseError: If the text couldn't be consumed.
        """

    def ConsumeComment(self) -> str: ...
    def ConsumeCommentOrTrailingComment(self) -> tuple[bool, str]:
        """Consumes a comment, returns a 2-tuple (trailing bool, comment str)."""

    def TryConsumeIdentifier(self) -> bool: ...
    def ConsumeIdentifier(self) -> str:
        """Consumes protocol message field identifier.

        Returns:
          Identifier string.

        Raises:
          ParseError: If an identifier couldn't be consumed.
        """

    def TryConsumeIdentifierOrNumber(self) -> bool: ...
    def ConsumeIdentifierOrNumber(self) -> str:
        """Consumes protocol message field identifier.

        Returns:
          Identifier string.

        Raises:
          ParseError: If an identifier couldn't be consumed.
        """

    def TryConsumeInteger(self) -> bool: ...
    def ConsumeInteger(self) -> int:
        """Consumes an integer number.

        Returns:
          The integer parsed.

        Raises:
          ParseError: If an integer couldn't be consumed.
        """

    def TryConsumeFloat(self) -> bool: ...
    def ConsumeFloat(self) -> float:
        """Consumes an floating point number.

        Returns:
          The number parsed.

        Raises:
          ParseError: If a floating point number couldn't be consumed.
        """

    def ConsumeBool(self) -> bool:
        """Consumes a boolean value.

        Returns:
          The bool parsed.

        Raises:
          ParseError: If a boolean value couldn't be consumed.
        """

    def TryConsumeByteString(self) -> bool: ...
    def ConsumeString(self) -> str:
        """Consumes a string value.

        Returns:
          The string parsed.

        Raises:
          ParseError: If a string value couldn't be consumed.
        """

    def ConsumeByteString(self) -> bytes:
        """Consumes a byte array value.

        Returns:
          The array parsed (as a string).

        Raises:
          ParseError: If a byte array value couldn't be consumed.
        """

    def ConsumeEnum(self, field: FieldDescriptor) -> int: ...
    def ParseErrorPreviousToken(self, message: Message) -> _ParseError:
        """Creates and *returns* a ParseError for the previously read token.

        Args:
          message: A message to set for the exception.

        Returns:
          A ParseError instance.
        """

    def ParseError(self, message: Message) -> _ParseError:
        """Creates and *returns* a ParseError for the current token."""

    def NextToken(self) -> None:
        """Reads the next meaningful token."""

def ParseInteger(text: str, is_signed: bool = False, is_long: bool = False) -> int:
    """Parses an integer.

    Args:
      text: The text to parse.
      is_signed: True if a signed integer must be parsed.
      is_long: True if a long integer must be parsed.

    Returns:
      The integer value.

    Raises:
      ValueError: Thrown Iff the text is not a valid integer.
    """

def ParseFloat(text: str) -> float:
    """Parse a floating point number.

    Args:
      text: Text to parse.

    Returns:
      The number parsed.

    Raises:
      ValueError: If a floating point number couldn't be parsed.
    """

def ParseBool(text: str) -> bool:
    """Parse a boolean value.

    Args:
      text: Text to parse.

    Returns:
      Boolean values parsed

    Raises:
      ValueError: If text is not a valid boolean.
    """

def ParseEnum(field: FieldDescriptor, value: str) -> int:
    """Parse an enum value.

    The value can be specified by a number (the enum value), or by
    a string literal (the enum name).

    Args:
      field: Enum field descriptor.
      value: String value.

    Returns:
      Enum value number.

    Raises:
      ValueError: If the enum value could not be parsed.
    """
