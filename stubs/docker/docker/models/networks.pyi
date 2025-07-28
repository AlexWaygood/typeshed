from typing import Any, Literal

from docker.types import IPAMConfig

from .containers import Container
from .resource import Collection, Model

class Network(Model):
    """
    A Docker network.
    """

    @property
    def name(self) -> str | None:
        """
        The name of the network.
        """

    @property
    def containers(self) -> list[Container]:
        """
        The containers that are connected to the network, as a list of
        :py:class:`~docker.models.containers.Container` objects.
        """

    def connect(self, container: str | Container, *args, **kwargs) -> None:
        """
        Connect a container to this network.

        Args:
            container (str): Container to connect to this network, as either
                an ID, name, or :py:class:`~docker.models.containers.Container`
                object.
            aliases (:py:class:`list`): A list of aliases for this endpoint.
                Names in that list can be used within the network to reach the
                container. Defaults to ``None``.
            links (:py:class:`list`): A list of links for this endpoint.
                Containers declared in this list will be linkedto this
                container. Defaults to ``None``.
            ipv4_address (str): The IP address of this container on the
                network, using the IPv4 protocol. Defaults to ``None``.
            ipv6_address (str): The IP address of this container on the
                network, using the IPv6 protocol. Defaults to ``None``.
            link_local_ips (:py:class:`list`): A list of link-local (IPv4/IPv6)
                addresses.
            driver_opt (dict): A dictionary of options to provide to the
                network driver. Defaults to ``None``.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def disconnect(self, container: str | Container, force: bool = False) -> None:
        """
        Disconnect a container from this network.

        Args:
            container (str): Container to disconnect from this network, as
                either an ID, name, or
                :py:class:`~docker.models.containers.Container` object.
            force (bool): Force the container to disconnect from a network.
                Default: ``False``

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def remove(self) -> None:
        """
        Remove this network.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

class NetworkCollection(Collection[Network]):
    """
    Networks on the Docker server.
    """

    model: type[Network]
    def create(  # type:ignore[override]
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
    ) -> Network:
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
            (:py:class:`Network`): The network that was created.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:
            A network using the bridge driver:

                >>> client.networks.create("network1", driver="bridge")

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
                >>> client.networks.create(
                    "network1",
                    driver="bridge",
                    ipam=ipam_config
                )

        """

    def get(
        self, network_id: str, verbose: bool | None = None, scope: Literal["local", "global", "swarm"] | None = None
    ) -> Network:  # type:ignore[override]
        """
        Get a network by its ID.

        Args:
            network_id (str): The ID of the network.
            verbose (bool): Retrieve the service details across the cluster in
                swarm mode.
            scope (str): Filter the network by scope (``swarm``, ``global``
                or ``local``).

        Returns:
            (:py:class:`Network`) The network.

        Raises:
            :py:class:`docker.errors.NotFound`
                If the network does not exist.

            :py:class:`docker.errors.APIError`
                If the server returns an error.

        """

    def list(self, *args, **kwargs) -> list[Network]:
        """
        List networks. Similar to the ``docker network ls`` command.

        Args:
            names (:py:class:`list`): List of names to filter by.
            ids (:py:class:`list`): List of ids to filter by.
            filters (dict): Filters to be processed on the network list.
                Available filters:
                - ``driver=[<driver-name>]`` Matches a network's driver.
                - `label` (str|list): format either ``"key"``, ``"key=value"``
                    or a list of such.
                - ``type=["custom"|"builtin"]`` Filters networks by type.
            greedy (bool): Fetch more details for each network individually.
                You might want this to get the containers attached to them.

        Returns:
            (list of :py:class:`Network`) The networks on the server.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def prune(self, filters: dict[str, Any] | None = None) -> dict[str, Any]:
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
