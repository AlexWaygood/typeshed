"""
Classes and functions for dealing with MAC addresses, EUI-48, EUI-64, OUI, IAB
identifiers.
"""

from _typeshed import ConvertibleToInt
from typing import ClassVar, Literal, overload
from typing_extensions import Self

from netaddr.core import DictDotLookup
from netaddr.ip import IPAddress
from netaddr.strategy.eui48 import mac_eui48
from netaddr.strategy.eui64 import eui64_base

class BaseIdentifier:
    """Base class for all IEEE identifiers."""

    def __init__(self) -> None: ...
    def __int__(self) -> int:
        """:return: integer value of this identifier"""

    def __index__(self) -> int:
        """
        :return: return the integer value of this identifier.
        """

class OUI(BaseIdentifier):
    """
    An individual IEEE OUI (Organisationally Unique Identifier).

    For online details see - http://standards.ieee.org/regauth/oui/

    """

    records: list[dict[str, object]]
    def __init__(self, oui: str | int) -> None:
        """
        Constructor

        :param oui: an OUI string ``XX-XX-XX`` or an unsigned integer.             Also accepts and parses full MAC/EUI-48 address strings (but not             MAC/EUI-48 integers)!
        """

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    @property
    def reg_count(self) -> int:
        """Number of registered organisations with this OUI"""

    def registration(self, index: int = 0) -> DictDotLookup:
        """
        The IEEE registration details for this OUI.

        :param index: the index of record (may contain multiple registrations)
            (Default: 0 - first registration)

        :return: Objectified Python data structure containing registration
            details.
        """

class IAB(BaseIdentifier):
    IAB_EUI_VALUES: ClassVar[tuple[int, int]]
    @classmethod
    def split_iab_mac(cls, eui_int: int, strict: bool = False) -> tuple[int, int]:
        """
        :param eui_int: a MAC IAB as an unsigned integer.

        :param strict: If True, raises a ValueError if the last 12 bits of
            IAB MAC/EUI-48 address are non-zero, ignores them otherwise.
            (Default: False)
        """
    record: dict[str, object]
    def __init__(self, iab: str | int, strict: bool = False) -> None:
        """
        Constructor

        :param iab: an IAB string ``00-50-C2-XX-X0-00`` or an unsigned             integer. This address looks like an EUI-48 but it should not             have any non-zero bits in the last 3 bytes.

        :param strict: If True, raises a ValueError if the last 12 bits             of IAB MAC/EUI-48 address are non-zero, ignores them otherwise.             (Default: False)
        """

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def registration(self) -> DictDotLookup:
        """The IEEE registration details for this IAB"""

class EUI(BaseIdentifier):
    """
    An IEEE EUI (Extended Unique Identifier).

    Both EUI-48 (used for layer 2 MAC addresses) and EUI-64 are supported.

    Input parsing for EUI-48 addresses is flexible, supporting many MAC
    variants.

    """

    def __init__(
        self, addr: EUI | int | str, version: int | None = None, dialect: type[mac_eui48 | eui64_base] | None = None
    ) -> None:
        """
        Constructor.

        :param addr: an EUI-48 (MAC) or EUI-64 address in string format or             an unsigned integer. May also be another EUI object (copy             construction).

        :param version: (optional) the explicit EUI address version, either             48 or 64. Mainly used to distinguish EUI-48 and EUI-64 identifiers             specified as integers which may be numerically equivalent.

        :param dialect: (optional) one of the :ref:`mac_formatting_dialects` to
            be used to configure the formatting of EUI-48 (MAC) addresses.
        """

    @property
    def value(self) -> int:
        """a positive integer representing the value of this EUI identifier."""

    @value.setter
    def value(self, value: ConvertibleToInt) -> None: ...
    @property
    def dialect(self) -> type[mac_eui48 | eui64_base]:
        """a Python class providing support for the interpretation of various MAC
        address formats.
        """

    @dialect.setter
    def dialect(self, value: type[mac_eui48 | eui64_base] | None) -> None: ...
    @property
    def oui(self) -> OUI:
        """The OUI (Organisationally Unique Identifier) for this EUI."""

    @property
    def ei(self) -> str:
        """The EI (Extension Identifier) for this EUI"""

    def is_iab(self) -> bool:
        """:return: True if this EUI is an IAB address, False otherwise"""

    @property
    def iab(self) -> IAB | None:
        """
        If is_iab() is True, the IAB (Individual Address Block) is returned,
        ``None`` otherwise.
        """

    @property
    def version(self) -> Literal[48, 64]:
        """The EUI version represented by this EUI object."""

    @overload
    def __getitem__(self, idx: int) -> int:
        """
        :return: The integer value of the word referenced by index (both             positive and negative). Raises ``IndexError`` if index is out             of bounds. Also supports Python list slices for accessing             word groups.
        """

    @overload
    def __getitem__(self, idx: slice) -> list[int]: ...
    @overload
    def __getitem__(self, idx: int | slice) -> int | list[int]: ...
    def __setitem__(self, idx: int, value: int) -> None:
        """Set the value of the word referenced by index in this address"""

    def __hash__(self) -> int:
        """:return: hash of this EUI object suitable for dict keys, sets etc"""

    def __eq__(self, other: object) -> bool:
        """
        :return: ``True`` if this EUI object is numerically the same as other,             ``False`` otherwise.
        """

    def __ne__(self, other: object) -> bool:
        """
        :return: ``True`` if this EUI object is numerically the same as other,             ``False`` otherwise.
        """

    def __lt__(self, other: EUI | int | str) -> bool:
        """
        :return: ``True`` if this EUI object is numerically lower in value than             other, ``False`` otherwise.
        """

    def __le__(self, other: EUI | int | str) -> bool:
        """
        :return: ``True`` if this EUI object is numerically lower or equal in             value to other, ``False`` otherwise.
        """

    def __gt__(self, other: EUI | int | str) -> bool:
        """
        :return: ``True`` if this EUI object is numerically greater in value             than other, ``False`` otherwise.
        """

    def __ge__(self, other: EUI | int | str) -> bool:
        """
        :return: ``True`` if this EUI object is numerically greater or equal             in value to other, ``False`` otherwise.
        """

    def bits(self, word_sep: str | None = None) -> str:
        """
        :param word_sep: (optional) the separator to insert between words.             Default: None - use default separator for address type.

        :return: human-readable binary digit string of this address.
        """

    @property
    def packed(self) -> bytes:
        """The value of this EUI address as a packed binary string."""

    @property
    def words(self) -> tuple[int, ...]:
        """A list of unsigned integer octets found in this EUI address."""

    @property
    def bin(self) -> str:
        """
        The value of this EUI address in standard Python binary
        representational form (0bxxx). A back port of the format provided by
        the builtin bin() function found in Python 2.6.x and higher.
        """

    def eui64(self) -> Self:
        """
        - If this object represents an EUI-48 it is converted to EUI-64             as per the standard.
        - If this object is already an EUI-64, a new, numerically             equivalent object is returned instead.

        :return: The value of this EUI object as a new 64-bit EUI object.
        """

    def modified_eui64(self) -> Self:
        """
        - create a new EUI object with a modified EUI-64 as described in RFC 4291 section 2.5.1

        :return: a new and modified 64-bit EUI object.
        """

    def ipv6(self, prefix: ConvertibleToInt) -> IPAddress:
        """
        .. note:: This poses security risks in certain scenarios.             Please read RFC 4941 for details. Reference: RFCs 4291 and 4941.

        :param prefix: ipv6 prefix

        :return: new IPv6 `IPAddress` object based on this `EUI`             using the technique described in RFC 4291.
        """

    def ipv6_link_local(self) -> IPAddress:
        """
        .. note:: This poses security risks in certain scenarios.             Please read RFC 4941 for details. Reference: RFCs 4291 and 4941.

        :return: new link local IPv6 `IPAddress` object based on this `EUI`             using the technique described in RFC 4291.
        """

    @property
    def info(self) -> DictDotLookup:
        """
        A record dict containing IEEE registration details for this EUI
        (MAC-48) if available, None otherwise.
        """

    def format(self, dialect: type[mac_eui48 | eui64_base] | None = None) -> str:
        """
        Format the EUI into the representational format according to the given
        dialect

        :param dialect: one of the :ref:`mac_formatting_dialects` defining the
            formatting of EUI-48 (MAC) addresses.

        :return: EUI in representational format according to the given dialect
        """
