from _typeshed import Incomplete
from typing import Final

DEBUG: Final[bool]
NULL_COLUMN: Final[int]
UNSIGNED_CHAR_COLUMN: Final[int]
UNSIGNED_SHORT_COLUMN: Final[int]
UNSIGNED_INT24_COLUMN: Final[int]
UNSIGNED_INT64_COLUMN: Final[int]

def dump_packet(data) -> None: ...

class MysqlPacket:
    """Representation of a MySQL response packet.

    Provides an interface for reading/parsing the packet results.
    """

    def __init__(self, data, encoding) -> None: ...
    def get_all_data(self): ...
    def read(self, size):
        """Read the first 'size' bytes in packet and advance cursor past them."""

    def read_all(self):
        """Read all remaining data in the packet.

        (Subsequent read() will return errors.)
        """

    def advance(self, length: int) -> None:
        """Advance the cursor in data buffer 'length' bytes."""

    def rewind(self, position: int = 0) -> None:
        """Set the position of the data buffer cursor to 'position'."""

    def get_bytes(self, position: int, length: int = 1):
        """Get 'length' bytes starting at 'position'.

        Position is start of payload (first four packet header bytes are not
        included) starting at index '0'.

        No error checking is done.  If requesting outside end of buffer
        an empty string (or string shorter than 'length') may be returned!
        """

    def read_uint8(self): ...
    def read_uint16(self): ...
    def read_uint24(self): ...
    def read_uint32(self): ...
    def read_uint64(self): ...
    def read_string(self): ...
    def read_length_encoded_integer(self) -> Incomplete | None:
        """Read a 'Length Coded Binary' number from the data buffer.

        Length coded numbers can be anywhere from 1 to 9 bytes depending
        on the value of the first byte.
        """

    def read_length_coded_string(self):
        """Read a 'Length Coded String' from the data buffer.

        A 'Length Coded String' consists first of a length coded
        (unsigned, positive) integer represented in 1-9 bytes followed by
        that many bytes of binary data.  (For example "cat" would be "3cat".)
        """

    def read_struct(self, fmt: str): ...
    def is_ok_packet(self) -> bool: ...
    def is_eof_packet(self) -> bool: ...
    def is_auth_switch_request(self) -> bool: ...
    def is_extra_auth_data(self) -> bool: ...
    def is_resultset_packet(self) -> bool: ...
    def is_load_local_packet(self) -> bool: ...
    def is_error_packet(self) -> bool: ...
    def check_error(self) -> None: ...
    def raise_for_error(self) -> None: ...
    def dump(self) -> None: ...

class FieldDescriptorPacket(MysqlPacket):
    """A MysqlPacket that represents a specific column's metadata in the result.

    Parsing is automatically done and the results are exported via public
    attributes on the class such as: db, table_name, name, length, type_code.
    """

    def __init__(self, data, encoding) -> None: ...
    def description(self):
        """Provides a 7-item tuple compatible with the Python PEP249 DB Spec."""

    def get_column_length(self): ...

class OKPacketWrapper:
    """
    OK Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet) -> None: ...
    # TODO: add attrs from `from_packet`
    def __getattr__(self, key: str): ...

class EOFPacketWrapper:
    """
    EOF Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet) -> None: ...
    # TODO: add attrs from `from_packet`
    def __getattr__(self, key: str): ...

class LoadLocalPacketWrapper:
    """
    Load Local Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet) -> None: ...
    # TODO: add attrs from `from_packet`
    def __getattr__(self, key: str): ...
