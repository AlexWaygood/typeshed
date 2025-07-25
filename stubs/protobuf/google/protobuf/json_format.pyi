"""Contains routines for printing protocol messages in JSON format.

Simple usage example:

  # Create a proto object and serialize it to a json format string.
  message = my_proto_pb2.MyMessage(foo='bar')
  json_string = json_format.MessageToJson(message)

  # Parse a json format string to proto object.
  message = json_format.Parse(json_string, my_proto_pb2.MyMessage())
"""

from typing import Any, TypeVar

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

_MessageT = TypeVar("_MessageT", bound=Message)

class Error(Exception):
    """Top-level module error for json_format."""

class ParseError(Error):
    """Thrown in case of parsing error."""

class SerializeToJsonError(Error):
    """Thrown if serialization to JSON fails."""

def MessageToJson(
    message: Message,
    preserving_proto_field_name: bool = False,
    indent: int | None = 2,
    sort_keys: bool = False,
    use_integers_for_enums: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    float_precision: int | None = None,
    ensure_ascii: bool = True,
    always_print_fields_with_no_presence: bool = False,
) -> str:
    """Converts protobuf message to JSON format.

    Args:
      message: The protocol buffers message instance to serialize.
      always_print_fields_with_no_presence: If True, fields without
        presence (implicit presence scalars, repeated fields, and map fields) will
        always be serialized. Any field that supports presence is not affected by
        this option (including singular message fields and oneof fields).
      preserving_proto_field_name: If True, use the original proto field names as
        defined in the .proto file. If False, convert the field names to
        lowerCamelCase.
      indent: The JSON object will be pretty-printed with this indent level. An
        indent level of 0 or negative will only insert newlines. If the indent
        level is None, no newlines will be inserted.
      sort_keys: If True, then the output will be sorted by field names.
      use_integers_for_enums: If true, print integers instead of enum names.
      descriptor_pool: A Descriptor Pool for resolving types. If None use the
        default.
      float_precision: If set, use this to specify float field valid digits.
      ensure_ascii: If True, strings with non-ASCII characters are escaped. If
        False, Unicode strings are returned unchanged.

    Returns:
      A string containing the JSON formatted protocol buffer message.
    """

def MessageToDict(
    message: Message,
    always_print_fields_with_no_presence: bool = False,
    preserving_proto_field_name: bool = False,
    use_integers_for_enums: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    float_precision: int | None = None,
) -> dict[str, Any]:
    """Converts protobuf message to a dictionary.

    When the dictionary is encoded to JSON, it conforms to proto3 JSON spec.

    Args:
      message: The protocol buffers message instance to serialize.
      always_print_fields_with_no_presence: If True, fields without
        presence (implicit presence scalars, repeated fields, and map fields) will
        always be serialized. Any field that supports presence is not affected by
        this option (including singular message fields and oneof fields).
      preserving_proto_field_name: If True, use the original proto field names as
        defined in the .proto file. If False, convert the field names to
        lowerCamelCase.
      use_integers_for_enums: If true, print integers instead of enum names.
      descriptor_pool: A Descriptor Pool for resolving types. If None use the
        default.
      float_precision: If set, use this to specify float field valid digits.

    Returns:
      A dict representation of the protocol buffer message.
    """

def Parse(
    text: bytes | str,
    message: _MessageT,
    ignore_unknown_fields: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    max_recursion_depth: int = 100,
) -> _MessageT:
    """Parses a JSON representation of a protocol message into a message.

    Args:
      text: Message JSON representation.
      message: A protocol buffer message to merge into.
      ignore_unknown_fields: If True, do not raise errors for unknown fields.
      descriptor_pool: A Descriptor Pool for resolving types. If None use the
        default.
      max_recursion_depth: max recursion depth of JSON message to be deserialized.
        JSON messages over this depth will fail to be deserialized. Default value
        is 100.

    Returns:
      The same message passed as argument.

    Raises::
      ParseError: On JSON parsing problems.
    """

def ParseDict(
    js_dict: Any,
    message: _MessageT,
    ignore_unknown_fields: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    max_recursion_depth: int = 100,
) -> _MessageT:
    """Parses a JSON dictionary representation into a message.

    Args:
      js_dict: Dict representation of a JSON message.
      message: A protocol buffer message to merge into.
      ignore_unknown_fields: If True, do not raise errors for unknown fields.
      descriptor_pool: A Descriptor Pool for resolving types. If None use the
        default.
      max_recursion_depth: max recursion depth of JSON message to be deserialized.
        JSON messages over this depth will fail to be deserialized. Default value
        is 100.

    Returns:
      The same message passed as argument.
    """
