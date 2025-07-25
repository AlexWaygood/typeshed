"""Routines for IPv4 and IPv6 addresses, subnets and ranges."""

from _typeshed import ConvertibleToInt, Unused
from abc import abstractmethod
from collections.abc import Iterable, Iterator
from typing import Literal, SupportsIndex, SupportsInt, overload
from typing_extensions import Self, TypeAlias

from netaddr.core import DictDotLookup
from netaddr.strategy.ipv6 import ipv6_verbose

class BaseIP:
    """
    An abstract base class for common operations shared between various IP
    related subclasses.

    """

    def __init__(self) -> None:
        """Constructor."""

    @property
    def value(self) -> int | None:
        """a positive integer representing the value of IP address/subnet."""

    @value.setter
    def value(self, value: int) -> None: ...
    @abstractmethod
    def key(self) -> tuple[int, ...]:
        """
        :return: a key tuple that uniquely identifies this IP address.
        """

    @abstractmethod
    def sort_key(self) -> tuple[int, ...]:
        """
        :return: A key tuple used to compare and sort this `IPAddress`
            correctly.
        """

    def __hash__(self) -> int:
        """
        :return: A hash value uniquely identifying this IP object.
        """

    def __eq__(self, other: object) -> bool:
        """
        :param other: an `IPAddress` or `IPNetwork` object.

        :return: ``True`` if this `IPAddress` or `IPNetwork` object is
            equivalent to ``other``, ``False`` otherwise.
        """

    def __ne__(self, other: object) -> bool:
        """
        :param other: an `IPAddress` or `IPNetwork` object.

        :return: ``True`` if this `IPAddress` or `IPNetwork` object is
            not equivalent to ``other``, ``False`` otherwise.
        """

    def __lt__(self, other: BaseIP) -> bool:
        """
        :param other: an `IPAddress` or `IPNetwork` object.

        :return: ``True`` if this `IPAddress` or `IPNetwork` object is
            less than ``other``, ``False`` otherwise.
        """

    def __le__(self, other: BaseIP) -> bool:
        """
        :param other: an `IPAddress` or `IPNetwork` object.

        :return: ``True`` if this `IPAddress` or `IPNetwork` object is
            less than or equal to ``other``, ``False`` otherwise.
        """

    def __gt__(self, other: BaseIP) -> bool:
        """
        :param other: an `IPAddress` or `IPNetwork` object.

        :return: ``True`` if this `IPAddress` or `IPNetwork` object is
            greater than ``other``, ``False`` otherwise.
        """

    def __ge__(self, other: BaseIP) -> bool:
        """
        :param other: an `IPAddress` or `IPNetwork` object.

        :return: ``True`` if this `IPAddress` or `IPNetwork` object is
            greater than or equal to ``other``, ``False`` otherwise.
        """

    def is_unicast(self) -> bool:
        """:return: ``True`` if this IP is unicast, ``False`` otherwise"""

    def is_multicast(self) -> bool:
        """:return: ``True`` if this IP is multicast, ``False`` otherwise"""

    def is_loopback(self) -> bool:
        """
        :return: ``True`` if this IP is loopback address (not for network
            transmission), ``False`` otherwise.
            References: RFC 3330 and 4291.

        .. note:: |ipv4_in_ipv6_handling|
        """

    def is_link_local(self) -> bool:
        """
        :return: ``True`` if this IP is link-local address ``False`` otherwise.
            Reference: RFCs 3927 and 4291.

        .. note:: |ipv4_in_ipv6_handling|
        """

    def is_reserved(self) -> bool:
        """
        :return: ``True`` if this IP is in IANA reserved range, ``False``
            otherwise. Reference: RFCs 3330 and 3171.

        .. note:: |ipv4_in_ipv6_handling|
        """

    def is_ipv4_mapped(self) -> bool:
        """
        :return: ``True`` if this IP is IPv4-mapped IPv6 address, ``False``
            otherwise.
        """

    def is_ipv4_compat(self) -> bool:
        """
        :return: ``True`` if this IP is IPv4-compatible IPv6 address, ``False``
            otherwise.
        """

    @property
    def info(self) -> DictDotLookup:
        """
        A record dict containing IANA registration details for this IP address
        if available, None otherwise.
        """

    @property
    def version(self) -> Literal[4, 6]:
        """the IP protocol version represented by this IP object."""

_IPAddressAddr: TypeAlias = BaseIP | int | str
_IPNetworkAddr: TypeAlias = IPNetwork | IPAddress | tuple[int, int] | str

class IPAddress(BaseIP):
    """
    An individual IPv4 or IPv6 address without a net mask or subnet prefix.

    To support these and other network based operations, see `IPNetwork`.

    """

    def __init__(self, addr: _IPAddressAddr, version: Literal[4, 6] | None = None, flags: int = 0) -> None:
        """
        Constructor.

        :param addr: an IPv4 or IPv6 address which may be represented in an
            accepted string format, as an unsigned integer or as another
            IPAddress object (copy construction).

        :param version: (optional) optimizes version detection if specified
            and distinguishes between IPv4 and IPv6 for addresses with an
            equivalent integer value.

        :param flags: (optional) decides which rules are applied to the
            interpretation of the addr value if passed as a string.

            Matters only in IPv4 context.

            Allowed flag values:

            * :data:`INET_ATON`. Follows `inet_aton semantics
              <https://www.netmeister.org/blog/inet_aton.html>`_ and allows all kinds of
              weird-looking addresses to be parsed. For example:

              >>> IPAddress('1', flags=INET_ATON)
              IPAddress('0.0.0.1')
              >>> IPAddress('1.0xf', flags=INET_ATON)
              IPAddress('1.0.0.15')
              >>> IPAddress('010.020.030.040', flags=INET_ATON)
              IPAddress('8.16.24.32')

            * ``INET_ATON | ZEROFILL`` or :data:`ZEROFILL` – like ``INET_ATON``, except leading zeros are discarded:

              >>> IPAddress('010', flags=INET_ATON | ZEROFILL)
              IPAddress('0.0.0.10')

            * The default (``0``) or :data:`INET_PTON` – requires four decimal octets:

              >>> IPAddress('10.0.0.1', flags=INET_PTON)
              IPAddress('10.0.0.1')

              Leading zeros may be ignored or rejected, depending on the platform.

            * ``INET_PTON | ZEROFILL`` – like the default :data:`INET_PTON`, except leading
              zeros are discarded:

              >>> IPAddress('010.020.030.040', flags=INET_PTON | ZEROFILL)
              IPAddress('10.20.30.40')

        .. versionchanged:: 1.0.0
            Changed the default IPv4 parsing mode from :data:`INET_ATON` to :data:`INET_PTON`.
        """

    def netmask_bits(self) -> int:
        """
        @return: If this IP is a valid netmask, the number of non-zero
            bits are returned, otherwise it returns the width in bits for
            the IP address version.
        """

    def is_hostmask(self) -> bool:
        """
        :return: ``True`` if this IP address host mask, ``False`` otherwise.
        """

    def is_netmask(self) -> bool:
        """
        :return: ``True`` if this IP address network mask, ``False`` otherwise.
        """

    def __iadd__(self, num: int) -> Self:
        """
        Increases the numerical value of this IPAddress by num.

        An IndexError is raised if result exceeds maximum IP address value or
        is less than zero.

        :param num: size of IP address increment.
        """

    def __isub__(self, num: int) -> Self:
        """
        Decreases the numerical value of this IPAddress by num.

        An IndexError is raised if result is less than zero or exceeds maximum
        IP address value.

        :param num: size of IP address decrement.
        """

    def __add__(self, num: int) -> Self:
        """
        Add the numerical value of this IP address to num and provide the
        result as a new IPAddress object.

        :param num: size of IP address increase.

        :return: a new IPAddress object with its numerical value increased by num.
        """
    __radd__ = __add__
    def __sub__(self, num: int) -> Self:
        """
        Subtract the numerical value of this IP address from num providing
        the result as a new IPAddress object.

        :param num: size of IP address decrease.

        :return: a new IPAddress object with its numerical value decreased by num.
        """

    def __rsub__(self, num: int) -> Self:
        """
        Subtract num (lvalue) from the numerical value of this IP address
        (rvalue) providing the result as a new IPAddress object.

        :param num: size of IP address decrease.

        :return: a new IPAddress object with its numerical value decreased by num.
        """

    def key(self) -> tuple[int, ...]:
        """
        :return: a key tuple that uniquely identifies this IP address.
        """

    def sort_key(self) -> tuple[int, ...]:
        """:return: A key tuple used to compare and sort this `IPAddress` correctly."""

    def __int__(self) -> int:
        """:return: the value of this IP address as an unsigned integer"""

    def __index__(self) -> int:
        """
        :return: return the integer value of this IP address.
        """

    def __bytes__(self) -> bytes:
        """
        :return: a bytes object equivalent to this IP address. In network
            byte order, big-endian.
        """

    def bits(self, word_sep: str | None = None) -> str:
        """
        :param word_sep: (optional) the separator to insert between words.
            Default: None - use default separator for address type.

        :return: the value of this IP address as a binary digit string.
        """

    @property
    def packed(self) -> bytes:
        """The value of this IP address as a packed binary string."""

    @property
    def words(self) -> tuple[int, ...]:
        """
        A list of unsigned integer words (octets for IPv4, hextets for IPv6)
        found in this IP address.
        """

    @property
    def bin(self) -> str:
        """
        The value of this IP address in standard Python binary
        representational form (0bxxx). A back port of the format provided by
        the builtin bin() function found in Python 2.6.x and higher.
        """

    @property
    def reverse_dns(self) -> str:
        """The reverse DNS lookup record for this IP address"""

    def ipv4(self) -> Self:
        """
        Raises an `AddrConversionError` if IPv6 address cannot be converted
        to IPv4.

        :return: A numerically equivalent version 4 `IPAddress` object.
        """

    def ipv6(self, ipv4_compatible: bool = False) -> Self:
        """
        .. note:: The IPv4-compatible IPv6 address format is now considered             deprecated. See RFC 4291 or later for details.

        :param ipv4_compatible: If ``True`` returns an IPv4-compatible address
            (::x.x.x.x), an IPv4-mapped (::ffff:x.x.x.x) address
            otherwise. Default: False (IPv4-mapped).

        :return: A numerically equivalent version 6 `IPAddress` object.
        """

    def format(self, dialect: type[ipv6_verbose] | None = None) -> str:
        """
        Only relevant for IPv6 addresses. Has no effect for IPv4.

        :param dialect: One of the :ref:`ipv6_formatting_dialects`.

        :return: an alternate string representation for this IP address.
        """

    def __or__(self, other: SupportsInt | SupportsIndex) -> Self:
        """
        :param other: An `IPAddress` object (or other int-like object).

        :return: bitwise OR (x | y) between the integer value of this IP
            address and ``other``.
        """

    def __and__(self, other: SupportsInt | SupportsIndex) -> Self:
        """
        :param other: An `IPAddress` object (or other int-like object).

        :return: bitwise AND (x & y) between the integer value of this IP
            address and ``other``.
        """

    def __xor__(self, other: SupportsInt | SupportsIndex) -> Self:
        """
        :param other: An `IPAddress` object (or other int-like object).

        :return: bitwise exclusive OR (x ^ y) between the integer value of
            this IP address and ``other``.
        """

    def __lshift__(self, numbits: int) -> Self:
        """
        :param numbits: size of bitwise shift.

        :return: an `IPAddress` object based on this one with its integer
            value left shifted by ``numbits``.
        """

    def __rshift__(self, numbits: int) -> Self:
        """
        :param numbits: size of bitwise shift.

        :return: an `IPAddress` object based on this one with its integer
            value right shifted by ``numbits``.
        """

    def __bool__(self) -> bool:
        """:return: ``True`` if the numerical value of this IP address is not             zero, ``False`` otherwise."""

    def to_canonical(self) -> Self:
        """
        Converts the address to IPv4 if it is an IPv4-mapped IPv6 address (`RFC 4291
        Section 2.5.5.2 <https://datatracker.ietf.org/doc/html/rfc4291.html#section-2.5.5.2>`_),
        otherwise returns the address as-is.

        >>> # IPv4-mapped IPv6
        >>> IPAddress('::ffff:10.0.0.1').to_canonical()
        IPAddress('10.0.0.1')
        >>>
        >>> # Everything else
        >>> IPAddress('::1').to_canonical()
        IPAddress('::1')
        >>> IPAddress('10.0.0.1').to_canonical()
        IPAddress('10.0.0.1')

        .. versionadded:: 0.10.0
        """

    def is_global(self) -> bool:
        """
        Returns ``True`` if this address is considered globally reachable, ``False`` otherwise.

        An address is considered globally reachable if it's not a special-purpose address
        or it's a special-purpose address listed as globally reachable in the relevant
        registries:

        * |iana_special_ipv4|
        * |iana_special_ipv6|

        Addresses for which the ``Globally Reachable`` value is ``N/A`` are not considered
        globally reachable.

        Address blocks with set termination date are not taken into consideration.

        Whether or not an address can actually be reached in any local or global context will
        depend on the network configuration and may differ from what this method returns.

        Examples:

        >>> IPAddress('1.1.1.1').is_global()
        True
        >>> IPAddress('::1').is_global()
        False

        .. note:: |ipv4_in_ipv6_handling|
        """

    def is_ipv4_private_use(self) -> bool:
        """
        Returns ``True`` if this address is an IPv4 private-use address as defined in
        :rfc:`1918`.

        The private-use address blocks:

        * ``10.0.0.0/8``
        * ``172.16.0.0/12``
        * ``192.168.0.0/16``

        .. note:: |ipv4_in_ipv6_handling|

        .. versionadded:: 0.10.0
        """

    def is_ipv6_unique_local(self) -> bool:
        """
        Returns ``True`` if this address is an IPv6 unique local address as defined in
        :rfc:`4193` and listed in |iana_special_ipv6|.

        The IPv6 unique local address block: ``fc00::/7``.

        .. versionadded:: 0.10.0
        """

class IPListMixin:
    """
    A mixin class providing shared list-like functionality to classes
    representing groups of IP addresses.

    """

    def __iter__(self) -> Iterator[IPAddress]:
        """
        :return: An iterator providing access to all `IPAddress` objects
            within range represented by this ranged IP object.
        """

    @property
    def size(self) -> int:
        """
        The total number of IP addresses within this ranged IP object.
        """

    def __len__(self) -> int:
        """
        :return: the number of IP addresses in this ranged IP object. Raises
            an `IndexError` if size > system max int (a Python 2.x
            limitation). Use the .size property for subnets of any size.
        """

    @overload
    def __getitem__(self, index: SupportsIndex) -> IPAddress:
        """
        :return: The IP address(es) in this `IPNetwork` object referenced by
            index or slice. As slicing can produce large sequences of objects
            an iterator is returned instead of the more usual `list`.
        """

    @overload
    def __getitem__(self, index: slice) -> Iterator[IPAddress]: ...
    @overload
    def __getitem__(self, index: SupportsIndex | slice) -> IPAddress | Iterator[IPAddress]: ...
    def __contains__(self, other: BaseIP | _IPAddressAddr) -> bool:
        """
        :param other: an `IPAddress` or ranged IP object.

        :return: ``True`` if other falls within the boundary of this one,
            ``False`` otherwise.
        """

    def __bool__(self) -> Literal[True]:
        """
        Ranged IP objects always represent a sequence of at least one IP
        address and are therefore always True in the boolean context.
        """

def parse_ip_network(module, addr: tuple[int, int] | str, flags: int = 0, *, expand_partial: bool = False) -> tuple[int, int]: ...

class IPNetwork(BaseIP, IPListMixin):
    """
    An IPv4 or IPv6 network or subnet.

    A combination of an IP address and a network mask.

    Accepts CIDR and several related variants :

    a) Standard CIDR::

        x.x.x.x/y -> 192.0.2.0/24
        x::/y -> fe80::/10

    b) Hybrid CIDR format (netmask address instead of prefix), where 'y'        address represent a valid netmask::

        x.x.x.x/y.y.y.y -> 192.0.2.0/255.255.255.0
        x::/y:: -> fe80::/ffc0::

    c) ACL hybrid CIDR format (hostmask address instead of prefix like        Cisco's ACL bitmasks), where 'y' address represent a valid netmask::

        x.x.x.x/y.y.y.y -> 192.0.2.0/0.0.0.255
        x::/y:: -> fe80::/3f:ffff:ffff:ffff:ffff:ffff:ffff:ffff

    .. versionchanged:: 1.0.0
        Removed the ``implicit_prefix`` switch that used to enable the abbreviated CIDR
        format support, use :func:`cidr_abbrev_to_verbose` if you need this behavior.

    .. versionchanged:: 1.1.0
        Removed partial IPv4 address support accidentally left when making 1.0.0 release.
        Use :func:`expand_partial_ipv4_address` if you need this behavior.

    .. versionchanged:: 1.3.0
        Added the expand_partial flag, which restores the previous behavior to expand
        partial IPv4 address
    """

    def __init__(
        self, addr: _IPNetworkAddr, version: Literal[4, 6] | None = None, flags: int = 0, *, expand_partial: bool = False
    ) -> None:
        """
        Constructor.

        :param addr: an IPv4 or IPv6 address with optional CIDR prefix,
            netmask or hostmask. May be an IP address in presentation
            (string) format, an tuple containing and integer address and a
            network prefix, or another IPAddress/IPNetwork object (copy
            construction).

        :param version: (optional) optimizes version detection if specified
            and distinguishes between IPv4 and IPv6 for addresses with an
            equivalent integer value.

        :param flags: (optional) decides which rules are applied to the
            interpretation of the addr value. Currently only supports the
            :data:`NOHOST` option.

        :param expand_partial: (optional) decides whether partial address is
            expanded. Currently this is only effective for IPv4 address.

            >>> IPNetwork('1.2.3.4/24')
            IPNetwork('1.2.3.4/24')
            >>> IPNetwork('1.2.3.4/24', flags=NOHOST)
            IPNetwork('1.2.3.0/24')
            >>> IPNetwork('10/24', expand_partial=True)
            IPNetwork('10.0.0.0/24')
        """

    @property
    def prefixlen(self) -> int:
        """size of the bitmask used to separate the network from the host bits"""

    @prefixlen.setter
    def prefixlen(self, value: int) -> None: ...
    @property
    def ip(self) -> IPAddress:
        """
        The IP address of this `IPNetwork` object. This is may or may not be
        the same as the network IP address which varies according to the value
        of the CIDR subnet prefix.
        """

    @property
    def network(self) -> IPAddress:
        """The network address of this `IPNetwork` object."""

    @property
    def broadcast(self) -> IPAddress | None:
        """The broadcast address of this `IPNetwork` object."""

    @property
    def first(self) -> int:
        """
        The integer value of first IP address found within this `IPNetwork`
        object.
        """

    @property
    def last(self) -> int:
        """
        The integer value of last IP address found within this `IPNetwork`
        object.
        """

    @property
    def netmask(self) -> IPAddress:
        """The subnet mask of this `IPNetwork` object."""

    @netmask.setter
    def netmask(self, value: _IPAddressAddr) -> None: ...
    @property
    def hostmask(self) -> IPAddress:
        """The host mask of this `IPNetwork` object."""

    @property
    def cidr(self) -> IPNetwork:
        """
        The true CIDR address for this `IPNetwork` object which omits any
        host bits to the right of the CIDR subnet prefix.
        """

    def __iadd__(self, num: int) -> Self:
        """
        Increases the value of this `IPNetwork` object by the current size
        multiplied by ``num``.

        An `IndexError` is raised if result exceeds maximum IP address value
        or is less than zero.

        :param num: (optional) number of `IPNetwork` blocks to increment             this IPNetwork's value by.
        """

    def __isub__(self, num: int) -> Self:
        """
        Decreases the value of this `IPNetwork` object by the current size
        multiplied by ``num``.

        An `IndexError` is raised if result is less than zero or exceeds
        maximum IP address value.

        :param num: (optional) number of `IPNetwork` blocks to decrement             this IPNetwork's value by.
        """
    # runtime overrides __contains__ with incompatible type for "other"
    def __contains__(self, other: BaseIP | _IPNetworkAddr) -> bool:  # type: ignore[override]
        """
        :param other: an `IPAddress` or ranged IP object.

        :return: ``True`` if other falls within the boundary of this one,
            ``False`` otherwise.
        """

    def key(self) -> tuple[int, ...]:
        """
        :return: A key tuple used to uniquely identify this `IPNetwork`.
        """

    def sort_key(self) -> tuple[int, ...]:
        """
        :return: A key tuple used to compare and sort this `IPNetwork` correctly.
        """

    def ipv4(self) -> Self:
        """
        :return: A numerically equivalent version 4 `IPNetwork` object.             Raises an `AddrConversionError` if IPv6 address cannot be             converted to IPv4.
        """

    def ipv6(self, ipv4_compatible: bool = False) -> Self:
        """
        .. note:: the IPv4-mapped IPv6 address format is now considered         deprecated. See RFC 4291 or later for details.

        :param ipv4_compatible: If ``True`` returns an IPv4-compatible address
            (::x.x.x.x), an IPv4-mapped (::ffff:x.x.x.x) address
            otherwise. Default: False (IPv4-mapped).

        :return: A numerically equivalent version 6 `IPNetwork` object.
        """

    def previous(self, step: int = 1) -> Self:
        """
        :param step: the number of IP subnets between this `IPNetwork` object
            and the expected subnet. Default: 1 (the previous IP subnet).

        :return: The adjacent subnet preceding this `IPNetwork` object.
        """

    def next(self, step: int = 1) -> Self:
        """
        :param step: the number of IP subnets between this `IPNetwork` object
            and the expected subnet. Default: 1 (the next IP subnet).

        :return: The adjacent subnet succeeding this `IPNetwork` object.
        """

    def supernet(self, prefixlen: int = 0) -> list[IPNetwork]:
        """
        Provides a list of supernets for this `IPNetwork` object between the
        size of the current prefix and (if specified) an endpoint prefix.

        :param prefixlen: (optional) a CIDR prefix for the maximum supernet.
            Default: 0 - returns all possible supernets.

        :return: a tuple of supernet `IPNetwork` objects.
        """

    def subnet(self, prefixlen: int, count: int | None = None, fmt: Unused = None) -> Iterator[Self]:
        """
        A generator that divides up this IPNetwork's subnet into smaller
        subnets based on a specified CIDR prefix.

        :param prefixlen: a CIDR prefix indicating size of subnets to be
            returned.

        :param count: (optional) number of consecutive IP subnets to be
            returned.

        :return: an iterator containing IPNetwork subnet objects.
        """

    def iter_hosts(self) -> Iterator[IPAddress]:
        """
        A generator that provides all the IP addresses that can be assigned
        to hosts within the range of this IP object's subnet.

        - for IPv4, the network and broadcast addresses are excluded, excepted           when using /31 or /32 subnets as per RFC 3021.

        - for IPv6, only Subnet-Router anycast address (first address in the           network) is excluded as per RFC 4291 section 2.6.1, excepted when using           /127 or /128 subnets as per RFC 6164.

        :return: an IPAddress iterator
        """

class IPRange(BaseIP, IPListMixin):
    """
    An arbitrary IPv4 or IPv6 address range.

    Formed from a lower and upper bound IP address. The upper bound IP cannot
    be numerically smaller than the lower bound and the IP version of both
    must match.

    """

    def __init__(self, start: _IPAddressAddr, end: _IPAddressAddr, flags: int = 0) -> None:
        """
        Constructor.

        :param start: an IPv4 or IPv6 address that forms the lower
            boundary of this IP range.

        :param end: an IPv4 or IPv6 address that forms the upper
            boundary of this IP range.

        :param flags: (optional) decides which rules are applied to the
            interpretation of the start and end values. Refer to the :meth:`IPAddress.__init__`
            documentation for details.

        """

    def __contains__(self, other: BaseIP | _IPAddressAddr) -> bool: ...
    @property
    def first(self) -> int:
        """The integer value of first IP address in this `IPRange` object."""

    @property
    def last(self) -> int:
        """The integer value of last IP address in this `IPRange` object."""

    def key(self) -> tuple[int, ...]:
        """
        :return: A key tuple used to uniquely identify this `IPRange`.
        """

    def sort_key(self) -> tuple[int, ...]:
        """
        :return: A key tuple used to compare and sort this `IPRange` correctly.
        """

    def cidrs(self) -> list[IPNetwork]:
        """
        The list of CIDR addresses found within the lower and upper bound
        addresses of this `IPRange`.
        """

def iter_unique_ips(*args: IPRange | _IPNetworkAddr) -> Iterator[IPAddress]:
    """
    :param args: A list of IP addresses and subnets passed in as arguments.

    :return: A generator that flattens out IP subnets, yielding unique
        individual IP addresses (no duplicates).
    """

def cidr_abbrev_to_verbose(abbrev_cidr: ConvertibleToInt) -> str:
    """
    A function that converts abbreviated IPv4 CIDRs to their more verbose
    equivalent.

    :param abbrev_cidr: an abbreviated CIDR.

    Uses the old-style classful IP address rules to decide on a default
    subnet prefix if one is not explicitly provided.

    Only supports IPv4 addresses.

    Examples ::

        10                  - 10.0.0.0/8
        10/16               - 10.0.0.0/16
        128                 - 128.0.0.0/16
        128/8               - 128.0.0.0/8
        192.168             - 192.168.0.0/16

    :return: A verbose CIDR from an abbreviated CIDR or old-style classful         network address. The original value if it was not recognised as a         supported abbreviation.
    """

def cidr_merge(ip_addrs: Iterable[IPRange | _IPNetworkAddr]) -> list[IPNetwork]:
    """
    A function that accepts an iterable sequence of IP addresses and subnets
    merging them into the smallest possible list of CIDRs. It merges adjacent
    subnets where possible, those contained within others and also removes
    any duplicates.

    :param ip_addrs: an iterable sequence of IP addresses, subnets or ranges.

    :return: a summarized list of `IPNetwork` objects.
    """

def cidr_exclude(target: _IPNetworkAddr, exclude: _IPNetworkAddr) -> list[IPNetwork]:
    """
    Removes an exclude IP address or subnet from target IP subnet.

    :param target: the target IP address or subnet to be divided up.

    :param exclude: the IP address or subnet to be removed from target.

    :return: list of `IPNetwork` objects remaining after exclusion.
    """

def cidr_partition(target: _IPNetworkAddr, exclude: _IPNetworkAddr) -> tuple[list[IPNetwork], list[IPNetwork], list[IPNetwork]]:
    """
    Partitions a target IP subnet on an exclude IP address.

    :param target: the target IP address or subnet to be divided up.

    :param exclude: the IP address or subnet to partition on

    :return: list of `IPNetwork` objects before, the partition and after, sorted.

    Adding the three lists returns the equivalent of the original subnet.
    """

def spanning_cidr(ip_addrs: Iterable[_IPNetworkAddr]) -> IPNetwork:
    """
    Function that accepts a sequence of IP addresses and subnets returning
    a single `IPNetwork` subnet that is large enough to span the lower and
    upper bound IP addresses with a possible overlap on either end.

    :param ip_addrs: sequence of IP addresses and subnets.

    :return: a single spanning `IPNetwork` subnet.
    """

def iter_iprange(start: _IPAddressAddr, end: _IPAddressAddr, step: SupportsInt | SupportsIndex = 1) -> Iterator[IPAddress]:
    """
    A generator that produces IPAddress objects between an arbitrary start
    and stop IP address with intervals of step between them. Sequences
    produce are inclusive of boundary IPs.

    :param start: start IP address.

    :param end: end IP address.

    :param step: (optional) size of step between IP addresses. Default: 1

    :return: an iterator of one or more `IPAddress` objects.
    """

def iprange_to_cidrs(start: _IPNetworkAddr, end: _IPNetworkAddr) -> list[IPNetwork]:
    """
    A function that accepts an arbitrary start and end IP address or subnet
    and returns a list of CIDR subnets that fit exactly between the boundaries
    of the two with no overlap.

    :param start: the start IP address or subnet.

    :param end: the end IP address or subnet.

    :return: a list of one or more IP addresses and subnets.
    """

def smallest_matching_cidr(ip: _IPAddressAddr, cidrs: Iterable[_IPNetworkAddr]) -> IPNetwork | None:
    """
    Matches an IP address or subnet against a given sequence of IP addresses
    and subnets.

    :param ip: a single IP address or subnet.

    :param cidrs: a sequence of IP addresses and/or subnets.

    :return: the smallest (most specific) matching IPAddress or IPNetwork
        object from the provided sequence, None if there was no match.
    """

def largest_matching_cidr(ip: _IPAddressAddr, cidrs: Iterable[_IPNetworkAddr]) -> IPNetwork | None:
    """
    Matches an IP address or subnet against a given sequence of IP addresses
    and subnets.

    :param ip: a single IP address or subnet.

    :param cidrs: a sequence of IP addresses and/or subnets.

    :return: the largest (least specific) matching IPAddress or IPNetwork
        object from the provided sequence, None if there was no match.
    """

def all_matching_cidrs(ip: _IPAddressAddr, cidrs: Iterable[_IPNetworkAddr]) -> list[IPNetwork]:
    """
    Matches an IP address or subnet against a given sequence of IP addresses
    and subnets.

    :param ip: a single IP address.

    :param cidrs: a sequence of IP addresses and/or subnets.

    :return: all matching IPAddress and/or IPNetwork objects from the provided
        sequence, an empty list if there was no match.
    """

IPV4_LOOPBACK: IPNetwork
IPV4_PRIVATE_USE: list[IPNetwork]
IPV4_LINK_LOCAL: IPNetwork
IPV4_MULTICAST: IPNetwork
IPV4_6TO4: IPNetwork
IPV4_RESERVED: tuple[IPNetwork | IPRange, ...]
IPV4_NOT_GLOBALLY_REACHABLE: list[IPNetwork]
IPV4_NOT_GLOBALLY_REACHABLE_EXCEPTIONS: list[IPNetwork]
IPV6_LOOPBACK: IPNetwork
IPV6_UNIQUE_LOCAL: IPNetwork
IPV6_LINK_LOCAL: IPNetwork
IPV6_MULTICAST: IPNetwork
IPV6_RESERVED: tuple[IPNetwork, ...]
IPV6_NOT_GLOBALLY_REACHABLE: list[IPNetwork]
IPV6_NOT_GLOBALLY_REACHABLE_EXCEPTIONS: list[IPNetwork]
