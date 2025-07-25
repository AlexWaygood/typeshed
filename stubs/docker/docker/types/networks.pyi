from _typeshed import Incomplete
from collections.abc import Iterable

class EndpointConfig(dict[str, Incomplete]):
    def __init__(
        self,
        version: str,
        aliases: list[Incomplete] | None = None,
        links: dict[str, str] | dict[str, None] | dict[str, str | None] | Iterable[tuple[str, str | None]] | None = None,
        ipv4_address: str | None = None,
        ipv6_address: str | None = None,
        link_local_ips: list[str] | None = None,
        driver_opt=None,
        mac_address: str | None = None,
    ) -> None: ...

class NetworkingConfig(dict[str, Incomplete]):
    def __init__(self, endpoints_config: EndpointConfig | None = None) -> None: ...

class IPAMConfig(dict[str, Incomplete]):
    """
    Create an IPAM (IP Address Management) config dictionary to be used with
    :py:meth:`~docker.api.network.NetworkApiMixin.create_network`.

    Args:

        driver (str): The IPAM driver to use. Defaults to ``default``.
        pool_configs (:py:class:`list`): A list of pool configurations
          (:py:class:`~docker.types.IPAMPool`). Defaults to empty list.
        options (dict): Driver options as a key-value dictionary.
          Defaults to `None`.

    Example:

        >>> ipam_config = docker.types.IPAMConfig(driver='default')
        >>> network = client.create_network('network1', ipam=ipam_config)

    """

    def __init__(
        self,
        driver: str = "default",
        pool_configs: list[IPAMPool] | None = None,
        options: dict[Incomplete, Incomplete] | None = None,
    ) -> None: ...

class IPAMPool(dict[str, Incomplete]):
    """
    Create an IPAM pool config dictionary to be added to the
    ``pool_configs`` parameter of
    :py:class:`~docker.types.IPAMConfig`.

    Args:

        subnet (str): Custom subnet for this IPAM pool using the CIDR
            notation. Defaults to ``None``.
        iprange (str): Custom IP range for endpoints in this IPAM pool using
            the CIDR notation. Defaults to ``None``.
        gateway (str): Custom IP address for the pool's gateway.
        aux_addresses (dict): A dictionary of ``key -> ip_address``
            relationships specifying auxiliary addresses that need to be
            allocated by the IPAM driver.

    Example:

        >>> ipam_pool = docker.types.IPAMPool(
            subnet='124.42.0.0/16',
            iprange='124.42.0.0/24',
            gateway='124.42.0.254',
            aux_addresses={
                'reserved1': '124.42.1.1'
            }
        )
        >>> ipam_config = docker.types.IPAMConfig(
                pool_configs=[ipam_pool])
    """

    def __init__(
        self,
        subnet: str | None = None,
        iprange: str | None = None,
        gateway: str | None = None,
        aux_addresses: dict[str, str] | None = None,
    ) -> None: ...
