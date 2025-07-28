"""Utilities and constants related to reverse dns lookup"""

from typing import Any

class ReverseDnsSetting:
    OFF: Any
    REQUIRE_RESOLVE_ALL_ADDRESSES: Any
    REQUIRE_RESOLVE_IP_ADDRESSES_ONLY: Any
    OPTIONAL_RESOLVE_ALL_ADDRESSES: Any
    OPTIONAL_RESOLVE_IP_ADDRESSES_ONLY: Any
    SUPPORTED_VALUES: Any

def get_hostname_by_addr(addr, success_required: bool = True):
    """Resolve the hostname for an ip address. If success is required, raise an exception if a hostname cannot
    be resolved for the address.
    Returns the hostname resolved for the address.
    If success is not required, returns None for addresses that do not resolve to hostnames.
    """

def is_ip_addr(addr):
    """Returns True if an address is an ipv4 address or an ipv6 address based on format. False otherwise."""
