"""Code for decoding protocol buffer primitives.

This code is very similar to encoder.py -- read the docs for that module first.

A "decoder" is a function with the signature:
  Decode(buffer, pos, end, message, field_dict)
The arguments are:
  buffer:     The string containing the encoded message.
  pos:        The current position in the string.
  end:        The position in the string where the current message ends.  May be
              less than len(buffer) if we're reading a sub-message.
  message:    The message object into which we're parsing.
  field_dict: message._fields (avoids a hashtable lookup).
The decoder reads the field and stores it into field_dict, returning the new
buffer position.  A decoder for a repeated field may proactively decode all of
the elements of that field, if they appear consecutively.

Note that decoders may throw any of the following:
  IndexError:  Indicates a truncated message.
  struct.error:  Unpacking of a fixed-width field failed.
  message.DecodeError:  Other errors.

Decoders are expected to raise an exception if they are called with pos > end.
This allows callers to be lax about bounds checking:  it's fineto read past
"end" as long as you are sure that someone else will notice and throw an
exception later on.

Something up the call stack is expected to catch IndexError and struct.error
and convert them to message.DecodeError.

Decoders are constructed using decoder constructors with the signature:
  MakeDecoder(field_number, is_repeated, is_packed, key, new_default)
The arguments are:
  field_number:  The field number of the field we want to decode.
  is_repeated:   Is the field a repeated field? (bool)
  is_packed:     Is the field a packed field? (bool)
  key:           The key to use when looking up the field within field_dict.
                 (This is actually the FieldDescriptor but nothing in this
                 file should depend on that.)
  new_default:   A function which takes a message object as a parameter and
                 returns a new instance of the default value for this field.
                 (This is called for repeated fields and sub-messages, when an
                 instance does not already exist.)

As with encoders, we define a decoder constructor for every type of field.
Then, for every field of every message class we construct an actual decoder.
That decoder goes into a dict indexed by tag, so when we decode a message
we repeatedly read a tag, look up the corresponding decoder, and invoke it.
"""

from collections.abc import Callable
from typing import Any
from typing_extensions import TypeAlias

from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.message import Message

_Decoder: TypeAlias = Callable[[str, int, int, Message, dict[FieldDescriptor, Any]], int]
_NewDefault: TypeAlias = Callable[[Message], Message]

def ReadTag(buffer, pos):
    """Read a tag from the memoryview, and return a (tag_bytes, new_pos) tuple.

    We return the raw bytes of the tag rather than decoding them.  The raw
    bytes can then be used to look up the proper decoder.  This effectively allows
    us to trade some work that would be done in pure-python (decoding a varint)
    for work that is done in C (searching for a byte string in a hash table).
    In a low-level language it would be much cheaper to decode the varint and
    use that, but not in Python.

    Args:
      buffer: memoryview object of the encoded bytes
      pos: int of the current position to start from

    Returns:
      Tuple[bytes, int] of the tag data and new position.
    """

Int32Decoder: _Decoder
Int64Decoder: _Decoder
UInt32Decoder: _Decoder
UInt64Decoder: _Decoder
SInt32Decoder: _Decoder
SInt64Decoder: _Decoder
Fixed32Decoder: _Decoder
Fixed64Decoder: _Decoder
SFixed32Decoder: _Decoder
SFixed64Decoder: _Decoder
FloatDecoder: _Decoder
DoubleDecoder: _Decoder
BoolDecoder: _Decoder

def EnumDecoder(
    field_number: int,
    is_repeated: bool,
    is_packed: bool,
    key: FieldDescriptor,
    new_default: _NewDefault,
    clear_if_default: bool = False,
) -> _Decoder:
    """Returns a decoder for enum field."""

def StringDecoder(
    field_number: int,
    is_repeated: bool,
    is_packed: bool,
    key: FieldDescriptor,
    new_default: _NewDefault,
    clear_if_default: bool = False,
) -> _Decoder:
    """Returns a decoder for a string field."""

def BytesDecoder(
    field_number: int,
    is_repeated: bool,
    is_packed: bool,
    key: FieldDescriptor,
    new_default: _NewDefault,
    clear_if_default: bool = False,
) -> _Decoder:
    """Returns a decoder for a bytes field."""

def GroupDecoder(
    field_number: int, is_repeated: bool, is_packed: bool, key: FieldDescriptor, new_default: _NewDefault
) -> _Decoder:
    """Returns a decoder for a group field."""

def MessageDecoder(
    field_number: int, is_repeated: bool, is_packed: bool, key: FieldDescriptor, new_default: _NewDefault
) -> _Decoder:
    """Returns a decoder for a message field."""

MESSAGE_SET_ITEM_TAG: bytes

def MessageSetItemDecoder(descriptor: Descriptor) -> _Decoder:
    """Returns a decoder for a MessageSet item.

    The parameter is the message Descriptor.

    The message set message looks like this:
      message MessageSet {
        repeated group Item = 1 {
          required int32 type_id = 2;
          required string message = 3;
        }
      }
    """

def MapDecoder(field_descriptor, new_default, is_message_map) -> _Decoder:
    """Returns a decoder for a map field."""
