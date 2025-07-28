from collections.abc import Iterable
from typing import Any, Literal, TypedDict, type_check_only
from typing_extensions import TypeAlias

from docker.types import IPAMConfig

@type_check_only
class _HasId(TypedDict):
    Id: str

@type_check_only
class _HasID(TypedDict):
    ID: str

_Network: TypeAlias = _HasId | _HasID | str
_Container: TypeAlias = _HasId | _HasID | str

class NetworkApiMixin:
    def networks(self, names=None, ids=None, filters=None):
        """
        List networks. Similar to the ``docker network ls`` command.

        Args:
            names (:py:class:`list`): List of names to filter by
            ids (:py:class:`list`): List of ids to filter by
            filters (dict): Filters to be processed on the network list.
                Available filters:
                - ``driver=[<driver-name>]`` Matches a network's driver.
                - ``label=[<key>]``, ``label=[<key>=<value>]`` or a list of
                    such.
                - ``type=["custom"|"builtin"]`` Filters networks by type.

        Returns:
            (dict): List of network objects.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def create_network(
        self,
        name: str,
        driver: str | None = None,
        options: dict[str, Any] | None = None,
        ipam: IPAMConfig | None = None,
        check_duplicate: bool | None = None,
        internal: bool = False,
        labels: dict[str, Any] | None = None,
        enable_ipv6: bool = False,
        attachable: bool | None = None,
        scope: Literal["local", "global", "swarm"] | None = None,
        ingress: bool | None = None,
    ) -> dict[str, str]:
        """
        Create a network. Similar to the ``docker network create``.

        Args:
            name (str): Name of the network
            driver (str): Name of the driver used to create the network
            options (dict): Driver options as a key-value dictionary
            ipam (IPAMConfig): Optional custom IP scheme for the network.
            check_duplicate (bool): Request daemon to check for networks with
                same name. Default: ``None``.
            internal (bool): Restrict external access to the network. Default
                ``False``.
            labels (dict): Map of labels to set on the network. Default
                ``None``.
            enable_ipv6 (bool): Enable IPv6 on the network. Default ``False``.
            attachable (bool): If enabled, and the network is in the global
                scope,  non-service containers on worker nodes will be able to
                connect to the network.
            scope (str): Specify the network's scope (``local``, ``global`` or
                ``swarm``)
            ingress (bool): If set, create an ingress network which provides
                the routing-mesh in swarm mode.

        Returns:
            (dict): The created network reference object

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:
            A network using the bridge driver:

                >>> client.api.create_network("network1", driver="bridge")

            You can also create more advanced networks with custom IPAM
            configurations. For example, setting the subnet to
            ``192.168.52.0/24`` and gateway address to ``192.168.52.254``.

            .. code-block:: python

                >>> ipam_pool = docker.types.IPAMPool(
                    subnet='192.168.52.0/24',
                    gateway='192.168.52.254'
                )
                >>> ipam_config = docker.types.IPAMConfig(
                    pool_configs=[ipam_pool]
                )
                >>> client.api.create_network("network1", driver="bridge",
                                                 ipam=ipam_config)
        """

    def prune_networks(self, filters=None):
        """
        Delete unused networks

        Args:
            filters (dict): Filters to process on the prune list.

        Returns:
            (dict): A dict containing a list of deleted network names and
                the amount of disk space reclaimed in bytes.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def remove_network(self, net_id: _Network) -> None:
        """
        Remove a network. Similar to the ``docker network rm`` command.

        Args:
            net_id (str): The network's id
        """

    def inspect_network(
        self, net_id: _Network, verbose: bool | None = None, scope: Literal["local", "global", "swarm"] | None = None
    ):
        """
        Get detailed information about a network.

        Args:
            net_id (str): ID of network
            verbose (bool): Show the service details across the cluster in
                swarm mode.
            scope (str): Filter the network by scope (``swarm``, ``global``
                or ``local``).
        """

    def connect_container_to_network(
        self,
        container: _Container,
        net_id: str,
        ipv4_address=None,
        ipv6_address=None,
        aliases=None,
        links: dict[str, str] | dict[str, None] | dict[str, str | None] | Iterable[tuple[str, str | None]] | None = None,
        link_local_ips=None,
        driver_opt=None,
        mac_address=None,
    ) -> None:
        """
        Connect a container to a network.

        Args:
            container (str): container-id/name to be connected to the network
            net_id (str): network id
            aliases (:py:class:`list`): A list of aliases for this endpoint.
                Names in that list can be used within the network to reach the
                container. Defaults to ``None``.
            links (:py:class:`list`): A list of links for this endpoint.
                Containers declared in this list will be linked to this
                container. Defaults to ``None``.
            ipv4_address (str): The IP address of this container on the
                network, using the IPv4 protocol. Defaults to ``None``.
            ipv6_address (str): The IP address of this container on the
                network, using the IPv6 protocol. Defaults to ``None``.
            link_local_ips (:py:class:`list`): A list of link-local
                (IPv4/IPv6) addresses.
            mac_address (str): The MAC address of this container on the
                network. Defaults to ``None``.
        """

    def disconnect_container_from_network(self, container: _Container, net_id: str, force: bool = False) -> None:
        """
        Disconnect a container from a network.

        Args:
            container (str): container ID or name to be disconnected from the
                network
            net_id (str): network ID
            force (bool): Force the container to disconnect from a network.
                Default: ``False``
        """
