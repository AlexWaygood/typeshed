"""Code for encoding protocol message primitives.

Contains the logic for encoding every logical protocol field type
into one of the 5 physical wire types.

This code is designed to push the Python interpreter's performance to the
limits.

The basic idea is that at startup time, for every field (i.e. every
FieldDescriptor) we construct two functions:  a "sizer" and an "encoder".  The
sizer takes a value of this field's type and computes its byte size.  The
encoder takes a writer function and a value.  It encodes the value into byte
strings and invokes the writer function to write those strings.  Typically the
writer function is the write() method of a BytesIO.

We try to do as much work as possible when constructing the writer and the
sizer rather than when calling them.  In particular:
* We copy any needed global functions to local variables, so that we do not need
  to do costly global table lookups at runtime.
* Similarly, we try to do any attribute lookups at startup time if possible.
* Every field's tag is encoded to bytes at startup, since it can't change at
  runtime.
* Whatever component of the field size we can compute at startup, we do.
* We *avoid* sharing code if doing so would make the code slower and not sharing
  does not burden us too much.  For example, encoders for repeated fields do
  not just call the encoders for singular fields in a loop because this would
  add an extra function call overhead for every loop iteration; instead, we
  manually inline the single-value encoder into the loop.
* If a Python function lacks a return statement, Python actually generates
  instructions to pop the result of the last statement off the stack, push
  None onto the stack, and then return that.  If we really don't care what
  value is returned, then we can save two instructions by returning the
  result of the last statement.  It looks funny but it helps.
* We assume that type and bounds checking has happened at a higher level.
"""

from collections.abc import Callable
from typing_extensions import TypeAlias

from google.protobuf.descriptor import FieldDescriptor

_Sizer: TypeAlias = Callable[[int, bool, bool], int]

Int32Sizer: _Sizer
UInt32Sizer: _Sizer
SInt32Sizer: _Sizer
Fixed32Sizer: _Sizer
Fixed64Sizer: _Sizer
BoolSizer: _Sizer

def StringSizer(field_number: int, is_repeated: bool, is_packed: bool) -> _Sizer:
    """Returns a sizer for a string field."""

def BytesSizer(field_number: int, is_repeated: bool, is_packed: bool) -> _Sizer:
    """Returns a sizer for a bytes field."""

def GroupSizer(field_number: int, is_repeated: bool, is_packed: bool) -> _Sizer:
    """Returns a sizer for a group field."""

def MessageSizer(field_number: int, is_repeated: bool, is_packed: bool) -> _Sizer:
    """Returns a sizer for a message field."""

def MessageSetItemSizer(field_number: int) -> _Sizer:
    """Returns a sizer for extensions of MessageSet.

    The message set message looks like this:
      message MessageSet {
        repeated group Item = 1 {
          required int32 type_id = 2;
          required string message = 3;
        }
      }
    """

def MapSizer(field_descriptor: FieldDescriptor, is_message_map: bool) -> _Sizer:
    """Returns a sizer for a map field."""

def TagBytes(field_number: int, wire_type: int) -> bytes:
    """Encode the given tag and return the bytes.  Only called at startup."""

_Encoder: TypeAlias = Callable[[Callable[[bytes], int], bytes, bool], int]

Int32Encoder: _Encoder
UInt32Encoder: _Encoder
SInt32Encoder: _Encoder
Fixed32Encoder: _Encoder
Fixed64Encoder: _Encoder
SFixed32Encoder: _Encoder
SFixed64Encoder: _Encoder
FloatEncoder: _Encoder
DoubleEncoder: _Encoder

def BoolEncoder(field_number: int, is_repeated: bool, is_packed: bool) -> _Encoder:
    """Returns an encoder for a boolean field."""

def StringEncoder(field_number: int, is_repeated: bool, is_packed: bool) -> _Encoder:
    """Returns an encoder for a string field."""

def BytesEncoder(field_number: int, is_repeated: bool, is_packed: bool) -> _Encoder:
    """Returns an encoder for a bytes field."""

def GroupEncoder(field_number: int, is_repeated: bool, is_packed: bool) -> _Encoder:
    """Returns an encoder for a group field."""

def MessageEncoder(field_number: int, is_repeated: bool, is_packed: bool) -> _Encoder:
    """Returns an encoder for a message field."""

def MessageSetItemEncoder(field_number: int) -> _Encoder:
    """Encoder for extensions of MessageSet.

    The message set message looks like this:
      message MessageSet {
        repeated group Item = 1 {
          required int32 type_id = 2;
          required string message = 3;
        }
      }
    """

def MapEncoder(field_descriptor: FieldDescriptor) -> _Encoder:
    """Encoder for extensions of MessageSet.

    Maps always have a wire format like this:
      message MapEntry {
        key_type key = 1;
        value_type value = 2;
      }
      repeated MapEntry map = N;
    """
