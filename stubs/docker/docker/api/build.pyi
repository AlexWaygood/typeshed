from collections.abc import Generator
from io import StringIO
from logging import Logger
from typing import IO, Any, TypedDict, type_check_only

log: Logger

@type_check_only
class _ContainerLimits(TypedDict, total=False):
    memory: int
    memswap: int
    cpushares: int
    cpusetcpus: str

@type_check_only
class _Filers(TypedDict, total=False):
    dangling: bool
    until: str

class BuildApiMixin:
    def build(
        self,
        path: str | None = None,
        tag: str | None = None,
        quiet: bool = False,
        fileobj: StringIO | IO[bytes] | None = None,
        nocache: bool = False,
        rm: bool = False,
        timeout: int | None = None,
        custom_context: bool = False,
        encoding: str | None = None,
        pull: bool = False,
        forcerm: bool = False,
        dockerfile: str | None = None,
        container_limits: _ContainerLimits | None = None,
        decode: bool = False,
        buildargs: dict[str, Any] | None = None,
        gzip: bool = False,
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
    ) -> Generator[Any, None, None]:
        """
        Similar to the ``docker build`` command. Either ``path`` or ``fileobj``
        needs to be set. ``path`` can be a local path (to a directory
        containing a Dockerfile) or a remote URL. ``fileobj`` must be a
        readable file-like object to a Dockerfile.

        If you have a tar file for the Docker build context (including a
        Dockerfile) already, pass a readable file-like object to ``fileobj``
        and also pass ``custom_context=True``. If the stream is compressed
        also, set ``encoding`` to the correct value (e.g ``gzip``).

        Example:
            >>> from io import BytesIO
            >>> from docker import APIClient
            >>> dockerfile = '''
            ... # Shared Volume
            ... FROM busybox:buildroot-2014.02
            ... VOLUME /data
            ... CMD ["/bin/sh"]
            ... '''
            >>> f = BytesIO(dockerfile.encode('utf-8'))
            >>> cli = APIClient(base_url='tcp://127.0.0.1:2375')
            >>> response = [line for line in cli.build(
            ...     fileobj=f, rm=True, tag='yourname/volume'
            ... )]
            >>> response
            ['{"stream":" ---\\u003e a9eb17255234\\n"}',
             '{"stream":"Step 1 : VOLUME /data\\n"}',
             '{"stream":" ---\\u003e Running in abdc1e6896c6\\n"}',
             '{"stream":" ---\\u003e 713bca62012e\\n"}',
             '{"stream":"Removing intermediate container abdc1e6896c6\\n"}',
             '{"stream":"Step 2 : CMD [\\"/bin/sh\\"]\\n"}',
             '{"stream":" ---\\u003e Running in dba30f2a1a7e\\n"}',
             '{"stream":" ---\\u003e 032b8b2855fc\\n"}',
             '{"stream":"Removing intermediate container dba30f2a1a7e\\n"}',
             '{"stream":"Successfully built 032b8b2855fc\\n"}']

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
            gzip (bool): If set to ``True``, gzip compression/encoding is used
            buildargs (dict): A dictionary of build arguments
            container_limits (dict): A dictionary of limits applied to each
                container created by the build process. Valid keys:

                - memory (int): set memory limit for build
                - memswap (int): Total memory (memory + swap), -1 to disable
                    swap
                - cpushares (int): CPU shares (relative weight)
                - cpusetcpus (str): CPUs in which to allow execution, e.g.,
                    ``"0-3"``, ``"0,1"``
            decode (bool): If set to ``True``, the returned stream will be
                decoded into dicts on the fly. Default ``False``
            shmsize (int): Size of `/dev/shm` in bytes. The size must be
                greater than 0. If omitted the system uses 64MB
            labels (dict): A dictionary of labels to set on the image
            cache_from (:py:class:`list`): A list of images used for build
                cache resolution
            target (str): Name of the build-stage to build in a multi-stage
                Dockerfile
            network_mode (str): networking mode for the run commands during
                build
            squash (bool): Squash the resulting images layers into a
                single layer.
            extra_hosts (dict): Extra hosts to add to /etc/hosts in building
                containers, as a mapping of hostname to IP address.
            platform (str): Platform in the format ``os[/arch[/variant]]``
            isolation (str): Isolation technology used during build.
                Default: `None`.
            use_config_proxy (bool): If ``True``, and if the docker client
                configuration file (``~/.docker/config.json`` by default)
                contains a proxy configuration, the corresponding environment
                variables will be set in the container being built.

        Returns:
            A generator for the build output.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
            ``TypeError``
                If neither ``path`` nor ``fileobj`` is specified.
        """

    def prune_builds(
        self, filters: _Filers | None = None, keep_storage: int | None = None, all: bool | None = None
    ) -> dict[str, Any]:
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

def process_dockerfile(dockerfile: str | None, path: str) -> tuple[str | None, str | None]: ...
