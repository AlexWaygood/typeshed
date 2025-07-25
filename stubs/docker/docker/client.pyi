from collections.abc import Iterable
from typing import NoReturn, Protocol, type_check_only

from docker import APIClient
from docker.models.configs import ConfigCollection
from docker.models.containers import ContainerCollection
from docker.models.images import ImageCollection
from docker.models.networks import NetworkCollection
from docker.models.nodes import NodeCollection
from docker.models.plugins import PluginCollection
from docker.models.secrets import SecretCollection
from docker.models.services import ServiceCollection
from docker.models.swarm import Swarm
from docker.models.volumes import VolumeCollection

@type_check_only
class _Environ(Protocol):
    def __getitem__(self, k: str, /) -> str: ...
    def keys(self) -> Iterable[str]: ...

class DockerClient:
    """
    A client for communicating with a Docker server.

    Example:

        >>> import docker
        >>> client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    Args:
        base_url (str): URL to the Docker server. For example,
            ``unix:///var/run/docker.sock`` or ``tcp://127.0.0.1:1234``.
        version (str): The version of the API to use. Set to ``auto`` to
            automatically detect the server's version. Default: ``1.35``
        timeout (int): Default timeout for API calls, in seconds.
        tls (bool or :py:class:`~docker.tls.TLSConfig`): Enable TLS. Pass
            ``True`` to enable it with default options, or pass a
            :py:class:`~docker.tls.TLSConfig` object to use custom
            configuration.
        user_agent (str): Set a custom user agent for requests to the server.
        credstore_env (dict): Override environment variables when calling the
            credential store process.
        use_ssh_client (bool): If set to `True`, an ssh connection is made
            via shelling out to the ssh client. Ensure the ssh client is
            installed and configured on the host.
        max_pool_size (int): The maximum number of connections
            to save in the pool.
    """

    api: APIClient
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def from_env(
        cls,
        *,
        version: str | None = None,
        timeout: int = ...,
        max_pool_size: int = ...,
        environment: _Environ | None = None,
        use_ssh_client: bool = False,
    ) -> DockerClient:
        """
        Return a client configured from environment variables.

        The environment variables used are the same as those used by the
        Docker command-line client. They are:

        .. envvar:: DOCKER_HOST

            The URL to the Docker host.

        .. envvar:: DOCKER_TLS_VERIFY

            Verify the host against a CA certificate.

        .. envvar:: DOCKER_CERT_PATH

            A path to a directory containing TLS certificates to use when
            connecting to the Docker host.

        Args:
            version (str): The version of the API to use. Set to ``auto`` to
                automatically detect the server's version. Default: ``auto``
            timeout (int): Default timeout for API calls, in seconds.
            max_pool_size (int): The maximum number of connections
                to save in the pool.
            environment (dict): The environment to read environment variables
                from. Default: the value of ``os.environ``
            credstore_env (dict): Override environment variables when calling
                the credential store process.
            use_ssh_client (bool): If set to `True`, an ssh connection is
                made via shelling out to the ssh client. Ensure the ssh
                client is installed and configured on the host.

        Example:

            >>> import docker
            >>> client = docker.from_env()

        .. _`SSL version`:
            https://docs.python.org/3.5/library/ssl.html#ssl.PROTOCOL_TLSv1
        """

    @property
    def configs(self) -> ConfigCollection:
        """
        An object for managing configs on the server. See the
        :doc:`configs documentation <configs>` for full details.
        """

    @property
    def containers(self) -> ContainerCollection:
        """
        An object for managing containers on the server. See the
        :doc:`containers documentation <containers>` for full details.
        """

    @property
    def images(self) -> ImageCollection:
        """
        An object for managing images on the server. See the
        :doc:`images documentation <images>` for full details.
        """

    @property
    def networks(self) -> NetworkCollection:
        """
        An object for managing networks on the server. See the
        :doc:`networks documentation <networks>` for full details.
        """

    @property
    def nodes(self) -> NodeCollection:
        """
        An object for managing nodes on the server. See the
        :doc:`nodes documentation <nodes>` for full details.
        """

    @property
    def plugins(self) -> PluginCollection:
        """
        An object for managing plugins on the server. See the
        :doc:`plugins documentation <plugins>` for full details.
        """

    @property
    def secrets(self) -> SecretCollection:
        """
        An object for managing secrets on the server. See the
        :doc:`secrets documentation <secrets>` for full details.
        """

    @property
    def services(self) -> ServiceCollection:
        """
        An object for managing services on the server. See the
        :doc:`services documentation <services>` for full details.
        """

    @property
    def swarm(self) -> Swarm:
        """
        An object for managing a swarm on the server. See the
        :doc:`swarm documentation <swarm>` for full details.
        """

    @property
    def volumes(self) -> VolumeCollection:
        """
        An object for managing volumes on the server. See the
        :doc:`volumes documentation <volumes>` for full details.
        """

    def events(self, *args, **kwargs):
        """
        Get real-time events from the server. Similar to the ``docker events``
        command.

        Args:
            since (UTC datetime or int): Get events from this point
            until (UTC datetime or int): Get events until this point
            filters (dict): Filter the events by event time, container or image
            decode (bool): If set to true, stream will be decoded into dicts on
                the fly. False by default.

        Returns:
            A :py:class:`docker.types.daemon.CancellableStream` generator

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:

            >>> for event in client.events(decode=True)
            ...   print(event)
            {u'from': u'image/with:tag',
             u'id': u'container-id',
             u'status': u'start',
             u'time': 1423339459}
            ...

            or

            >>> events = client.events()
            >>> for event in events:
            ...   print(event)
            >>> # and cancel from another thread
            >>> events.close()
        """

    def df(self):
        """
        Get data usage information.

        Returns:
            (dict): A dictionary representing different resource categories
            and their respective data usage.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def info(self, *args, **kwargs):
        """
        Display system-wide information. Identical to the ``docker info``
        command.

        Returns:
            (dict): The info as a dict

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def login(self, *args, **kwargs):
        """
        Authenticate with a registry. Similar to the ``docker login`` command.

        Args:
            username (str): The registry username
            password (str): The plaintext password
            email (str): The email for the registry account
            registry (str): URL to the registry.  E.g.
                ``https://index.docker.io/v1/``
            reauth (bool): Whether or not to refresh existing authentication on
                the Docker server.
            dockercfg_path (str): Use a custom path for the Docker config file
                (default ``$HOME/.docker/config.json`` if present,
                otherwise ``$HOME/.dockercfg``)

        Returns:
            (dict): The response from the login request

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def ping(self, *args, **kwargs):
        """
        Checks the server is responsive. An exception will be raised if it
        isn't responding.

        Returns:
            (bool) The response from the server.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def version(self, *args, **kwargs):
        """
        Returns version information from the server. Similar to the ``docker
        version`` command.

        Returns:
            (dict): The server version information

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def close(self):
        """Closes all adapters and as such the session"""

    def __getattr__(self, name: str) -> NoReturn: ...

from_env = DockerClient.from_env
