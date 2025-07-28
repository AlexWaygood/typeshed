from _typeshed import SupportsRead
from collections.abc import Iterator
from io import StringIO
from typing import IO, Any, Literal, TypedDict, overload, type_check_only
from typing_extensions import TypeAlias

from docker._types import JSON

from .resource import Collection, Model

_ImageList: TypeAlias = list[Image]  # To resolve conflicts with a method called "list"

@type_check_only
class _ContainerLimits(TypedDict, total=False):
    memory: int
    memswap: int
    cpushares: int
    cpusetcpus: str

class Image(Model):
    """
    An image on the server.
    """

    @property
    def labels(self) -> dict[str, Any]:
        """
        The labels of an image as dictionary.
        """

    @property
    def short_id(self) -> str:
        """
        The ID of the image truncated to 12 characters, plus the ``sha256:``
        prefix.
        """

    @property
    def tags(self) -> list[str]:
        """
        The image's tags.
        """

    def history(self) -> list[Any]:
        """
        Show the history of an image.

        Returns:
            (list): The history of the image.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def remove(self, force: bool = False, noprune: bool = False) -> dict[str, Any]:
        """
        Remove this image.

        Args:
            force (bool): Force removal of the image
            noprune (bool): Do not delete untagged parents

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def save(self, chunk_size: int = 2097152, named: bool = False) -> Iterator[Any]:
        """
        Get a tarball of an image. Similar to the ``docker save`` command.

        Args:
            chunk_size (int): The generator will return up to that much data
                per iteration, but may return less. If ``None``, data will be
                streamed as it is received. Default: 2 MB
            named (str or bool): If ``False`` (default), the tarball will not
                retain repository and tag information for this image. If set
                to ``True``, the first tag in the :py:attr:`~tags` list will
                be used to identify the image. Alternatively, any element of
                the :py:attr:`~tags` list can be used as an argument to use
                that specific tag as the saved identifier.

        Returns:
            (generator): A stream of raw archive data.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:

            >>> image = cli.images.get("busybox:latest")
            >>> f = open('/tmp/busybox-latest.tar', 'wb')
            >>> for chunk in image.save():
            >>>   f.write(chunk)
            >>> f.close()
        """

    def tag(self, repository: str, tag: str | None = None, **kwargs) -> bool:
        """
        Tag this image into a repository. Similar to the ``docker tag``
        command.

        Args:
            repository (str): The repository to set for the tag
            tag (str): The tag name
            force (bool): Force

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Returns:
            (bool): ``True`` if successful
        """

class RegistryData(Model):
    """
    Image metadata stored on the registry, including available platforms.
    """

    image_name: str
    def __init__(self, image_name: str, *args, **kwargs) -> None: ...
    @property
    def id(self) -> str:
        """
        The ID of the object.
        """

    @property
    def short_id(self) -> str:
        """
        The ID of the image truncated to 12 characters, plus the ``sha256:``
        prefix.
        """

    def pull(self, platform: str | None = None) -> Image:
        """
        Pull the image digest.

        Args:
            platform (str): The platform to pull the image for.
            Default: ``None``

        Returns:
            (:py:class:`Image`): A reference to the pulled image.
        """

    def has_platform(self, platform):
        """
        Check whether the given platform identifier is available for this
        digest.

        Args:
            platform (str or dict): A string using the ``os[/arch[/variant]]``
                format, or a platform dictionary.

        Returns:
            (bool): ``True`` if the platform is recognized as available,
            ``False`` otherwise.

        Raises:
            :py:class:`docker.errors.InvalidArgument`
                If the platform argument is not a valid descriptor.
        """

    def reload(self) -> None:
        """
        Load this object from the server again and update ``attrs`` with the
        new data.
        """

class ImageCollection(Collection[Image]):
    model: type[Image]
    def build(
        self,
        *,
        path: str | None = None,
        fileobj: StringIO | IO[bytes] | None = None,
        tag: str | None = None,
        quiet: bool = False,
        nocache: bool = False,
        rm: bool = False,
        timeout: int | None = None,
        custom_context: bool = False,
        encoding: str | None = None,
        pull: bool = False,
        forcerm: bool = False,
        dockerfile: str | None = None,
        buildargs: dict[str, Any] | None = None,
        container_limits: _ContainerLimits | None = None,
        shmsize: int | None = None,
        labels: dict[str, Any] | None = None,
        # need to use list, because the type must be json serializable
        cache_from: list[str] | None = None,
        target: str | None = None,
        network_mode: str | None = None,
        squash: bool | None = None,
        extra_hosts: list[str] | dict[str, str] | None = None,
        platform: str | None = None,
        isolation: str | None = None,
        use_config_proxy: bool = True,
    ) -> tuple[Image, Iterator[JSON]]:
        """
        Build an image and return it. Similar to the ``docker build``
        command. Either ``path`` or ``fileobj`` must be set.

        If you already have a tar file for the Docker build context (including
        a Dockerfile), pass a readable file-like object to ``fileobj``
        and also pass ``custom_context=True``. If the stream is also
        compressed, set ``encoding`` to the correct value (e.g ``gzip``).

        If you want to get the raw output of the build, use the
        :py:meth:`~docker.api.build.BuildApiMixin.build` method in the
        low-level API.

        Args:
            path (str): Path to the directory containing the Dockerfile
            fileobj: A file object to use as the Dockerfile. (Or a file-like
                object)
            tag (str): A tag to add to the final image
            quiet (bool): Whether to return the status
            nocache (bool): Don't use the cache when set to ``True``
            rm (bool): Remove intermediate containers. The ``docker build``
                command now defaults to ``--rm=true``, but we have kept the old
                default of `False` to preserve backward compatibility
            timeout (int): HTTP timeout
            custom_context (bool): Optional if using ``fileobj``
            encoding (str): The encoding for a stream. Set to ``gzip`` for
                compressing
            pull (bool): Downloads any updates to the FROM image in Dockerfiles
            forcerm (bool): Always remove intermediate containers, even after
                unsuccessful builds
            dockerfile (str): path within the build context to the Dockerfile
            buildargs (dict): A dictionary of build arguments
            container_limits (dict): A dictionary of limits applied to each
                container created by the build process. Valid keys:

                - memory (int): set memory limit for build
                - memswap (int): Total memory (memory + swap), -1 to disable
                    swap
                - cpushares (int): CPU shares (relative weight)
                - cpusetcpus (str): CPUs in which to allow execution, e.g.,
                    ``"0-3"``, ``"0,1"``
            shmsize (int): Size of `/dev/shm` in bytes. The size must be
                greater than 0. If omitted the system uses 64MB
            labels (dict): A dictionary of labels to set on the image
            cache_from (list): A list of images used for build cache
                resolution
            target (str): Name of the build-stage to build in a multi-stage
                Dockerfile
            network_mode (str): networking mode for the run commands during
                build
            squash (bool): Squash the resulting images layers into a
                single layer.
            extra_hosts (dict): Extra hosts to add to /etc/hosts in building
                containers, as a mapping of hostname to IP address.
            platform (str): Platform in the format ``os[/arch[/variant]]``.
            isolation (str): Isolation technology used during build.
                Default: `None`.
            use_config_proxy (bool): If ``True``, and if the docker client
                configuration file (``~/.docker/config.json`` by default)
                contains a proxy configuration, the corresponding environment
                variables will be set in the container being built.

        Returns:
            (tuple): The first item is the :py:class:`Image` object for the
                image that was built. The second item is a generator of the
                build logs as JSON-decoded objects.

        Raises:
            :py:class:`docker.errors.BuildError`
                If there is an error during the build.
            :py:class:`docker.errors.APIError`
                If the server returns any other error.
            ``TypeError``
                If neither ``path`` nor ``fileobj`` is specified.
        """

    def get(self, name: str) -> Image:
        """
        Gets an image.

        Args:
            name (str): The name of the image.

        Returns:
            (:py:class:`Image`): The image.

        Raises:
            :py:class:`docker.errors.ImageNotFound`
                If the image does not exist.
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def get_registry_data(self, name, auth_config: dict[str, Any] | None = None) -> RegistryData:
        """
        Gets the registry data for an image.

        Args:
            name (str): The name of the image.
            auth_config (dict): Override the credentials that are found in the
                config for this request.  ``auth_config`` should contain the
                ``username`` and ``password`` keys to be valid.

        Returns:
            (:py:class:`RegistryData`): The data object.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def list(self, name: str | None = None, all: bool = False, filters: dict[str, Any] | None = None) -> _ImageList:
        """
        List images on the server.

        Args:
            name (str): Only show images belonging to the repository ``name``
            all (bool): Show intermediate image layers. By default, these are
                filtered out.
            filters (dict): Filters to be processed on the image list.
                Available filters:
                - ``dangling`` (bool)
                - `label` (str|list): format either ``"key"``, ``"key=value"``
                    or a list of such.

        Returns:
            (list of :py:class:`Image`): The images.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def load(self, data: bytes | SupportsRead[bytes]) -> _ImageList:
        """
        Load an image that was previously saved using
        :py:meth:`~docker.models.images.Image.save` (or ``docker save``).
        Similar to ``docker load``.

        Args:
            data (binary): Image data to be loaded.

        Returns:
            (list of :py:class:`Image`): The images.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    @overload
    def pull(
        self,
        repository: str,
        tag: str | None = None,
        all_tags: Literal[False] = False,
        *,
        platform: str | None = None,
        auth_config: dict[str, Any] | None = None,
    ) -> Image:
        """
        Pull an image of the given name and return it. Similar to the
        ``docker pull`` command.
        If ``tag`` is ``None`` or empty, it is set to ``latest``.
        If ``all_tags`` is set, the ``tag`` parameter is ignored and all image
        tags will be pulled.

        If you want to get the raw pull output, use the
        :py:meth:`~docker.api.image.ImageApiMixin.pull` method in the
        low-level API.

        Args:
            repository (str): The repository to pull
            tag (str): The tag to pull
            auth_config (dict): Override the credentials that are found in the
                config for this request.  ``auth_config`` should contain the
                ``username`` and ``password`` keys to be valid.
            platform (str): Platform in the format ``os[/arch[/variant]]``
            all_tags (bool): Pull all image tags

        Returns:
            (:py:class:`Image` or list): The image that has been pulled.
                If ``all_tags`` is True, the method will return a list
                of :py:class:`Image` objects belonging to this repository.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:

            >>> # Pull the image tagged `latest` in the busybox repo
            >>> image = client.images.pull('busybox')

            >>> # Pull all tags in the busybox repo
            >>> images = client.images.pull('busybox', all_tags=True)
        """

    @overload
    def pull(
        self,
        repository: str,
        tag: str | None = None,
        *,
        all_tags: Literal[True],
        auth_config: dict[str, Any] | None = None,
        platform: str | None = None,
    ) -> _ImageList: ...
    @overload
    def pull(
        self,
        repository: str,
        tag: str | None,
        all_tags: Literal[True],
        *,
        auth_config: dict[str, Any] | None = None,
        platform: str | None = None,
    ) -> _ImageList: ...
    def push(self, repository: str, tag: str | None = None, **kwargs):
        """
        Push an image or a repository to the registry. Similar to the ``docker
        push`` command.

        Args:
            repository (str): The repository to push to
            tag (str): An optional tag to push
            stream (bool): Stream the output as a blocking generator
            auth_config (dict): Override the credentials that are found in the
                config for this request.  ``auth_config`` should contain the
                ``username`` and ``password`` keys to be valid.
            decode (bool): Decode the JSON data from the server into dicts.
                Only applies with ``stream=True``

        Returns:
            (generator or str): The output from the server.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:
            >>> resp = client.api.push(
            ...     'yourname/app',
            ...     stream=True,
            ...     decode=True,
            ... )
            ... for line in resp:
            ...   print(line)
            {'status': 'Pushing repository yourname/app (1 tags)'}
            {'status': 'Pushing','progressDetail': {}, 'id': '511136ea3c5a'}
            {'status': 'Image already pushed, skipping', 'progressDetail':{},
             'id': '511136ea3c5a'}
            ...

        """

    def remove(self, *args, **kwargs) -> None:
        """
        Remove an image. Similar to the ``docker rmi`` command.

        Args:
            image (str): The image to remove
            force (bool): Force removal of the image
            noprune (bool): Do not delete untagged parents
        """

    def search(self, *args, **kwargs):
        """
        Search for images on Docker Hub. Similar to the ``docker search``
        command.

        Args:
            term (str): A term to search for.
            limit (int): The maximum number of results to return.

        Returns:
            (list of dicts): The response of the search.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def prune(self, filters: dict[str, Any] | None = None):
        """
        Delete unused images

        Args:
            filters (dict): Filters to process on the prune list.
                Available filters:
                - dangling (bool):  When set to true (or 1), prune only
                unused and untagged images.

        Returns:
            (dict): A dict containing a list of deleted image IDs and
                the amount of disk space reclaimed in bytes.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def prune_builds(self, *args, **kwargs):
        """
        Delete the builder cache

        Args:
            filters (dict): Filters to process on the prune list.
                Needs Docker API v1.39+
                Available filters:
                - dangling (bool):  When set to true (or 1), prune only
                unused and untagged images.
                - until (str): Can be Unix timestamps, date formatted
                timestamps, or Go duration strings (e.g. 10m, 1h30m) computed
                relative to the daemon's local time.
            keep_storage (int): Amount of disk space in bytes to keep for cache.
                Needs Docker API v1.39+
            all (bool): Remove all types of build cache.
                Needs Docker API v1.39+

        Returns:
            (dict): A dictionary containing information about the operation's
                    result. The ``SpaceReclaimed`` key indicates the amount of
                    bytes of disk space reclaimed.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

def normalize_platform(platform, engine_info): ...
