"""AMQP Table Encoding/Decoding"""

from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing_extensions import TypeAlias

_Value: TypeAlias = str | bytes | bool | int | Decimal | datetime | _ArgumentMapping | list[_Value] | None
_ArgumentMapping: TypeAlias = Mapping[str, _Value]

def encode_short_string(pieces: list[bytes], value: str | bytes) -> int:
    """Encode a string value as short string and append it to pieces list
    returning the size of the encoded value.

    :param list pieces: Already encoded values
    :param str value: String value to encode
    :rtype: int

    """

def decode_short_string(encoded: bytes, offset: int) -> tuple[str, int]:
    """Decode a short string value from ``encoded`` data at ``offset``."""

def encode_table(pieces: list[bytes], table: _ArgumentMapping) -> int:
    """Encode a dict as an AMQP table appending the encded table to the
    pieces list passed in.

    :param list pieces: Already encoded frame pieces
    :param dict table: The dict to encode
    :rtype: int

    """

def encode_value(pieces: list[bytes], value: _Value) -> int:
    """Encode the value passed in and append it to the pieces list returning
    the the size of the encoded value.

    :param list pieces: Already encoded values
    :param any value: The value to encode
    :rtype: int

    """

def decode_table(encoded: bytes, offset: int) -> tuple[dict[str, _Value], int]:
    """Decode the AMQP table passed in from the encoded value returning the
    decoded result and the number of bytes read plus the offset.

    :param str encoded: The binary encoded data to decode
    :param int offset: The starting byte offset
    :rtype: tuple

    """

def decode_value(encoded: bytes, offset: int) -> tuple[_Value, int]:
    """Decode the value passed in returning the decoded value and the number
    of bytes read in addition to the starting offset.

    :param str encoded: The binary encoded data to decode
    :param int offset: The starting byte offset
    :rtype: tuple
    :raises: pika.exceptions.InvalidFieldTypeException

    """
