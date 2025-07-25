"""discovery

Module to aid with Nanoleaf discovery on a network.
"""

def discover_devices(timeout: int = 30, debug: bool = False) -> dict[str | None, str]:
    """
    Discovers Nanoleaf devices on the network using SSDP

    :param timeout: The timeout on the search in seconds (default 30)
    :param debug: Prints each device string for the SSDP discovery
    :returns: Dictionary of found devices in format {name: ip}
    """
