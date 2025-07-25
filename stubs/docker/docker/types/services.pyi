from _typeshed import Incomplete
from collections.abc import Iterable, Mapping
from typing import Final, Literal, TypeVar, overload

from .healthcheck import Healthcheck

_T = TypeVar("_T")

class TaskTemplate(dict[str, Incomplete]):
    """
    Describe the task specification to be used when creating or updating a
    service.

    Args:

        container_spec (ContainerSpec): Container settings for containers
          started as part of this task.
        log_driver (DriverConfig): Log configuration for containers created as
          part of the service.
        resources (Resources): Resource requirements which apply to each
          individual container created as part of the service.
        restart_policy (RestartPolicy): Specification for the restart policy
          which applies to containers created as part of this service.
        placement (Placement): Placement instructions for the scheduler.
            If a list is passed instead, it is assumed to be a list of
            constraints as part of a :py:class:`Placement` object.
        networks (:py:class:`list`): List of network names or IDs or
            :py:class:`NetworkAttachmentConfig` to attach the service to.
        force_update (int): A counter that triggers an update even if no
            relevant parameters have been changed.
    """

    def __init__(
        self,
        container_spec: ContainerSpec,
        resources: Resources | None = None,
        restart_policy: RestartPolicy | None = None,
        placement: Placement | list[str] | None = None,
        log_driver: DriverConfig | None = None,
        networks: Iterable[str | NetworkAttachmentConfig] | None = None,
        force_update: int | None = None,
    ) -> None: ...
    @property
    def container_spec(self) -> ContainerSpec: ...
    @property
    def resources(self) -> Resources: ...
    @property
    def restart_policy(self) -> RestartPolicy: ...
    @property
    def placement(self) -> Placement: ...

class ContainerSpec(dict[str, Incomplete]):
    """
    Describes the behavior of containers that are part of a task, and is used
    when declaring a :py:class:`~docker.types.TaskTemplate`.

    Args:

        image (string): The image name to use for the container.
        command (string or list):  The command to be run in the image.
        args (:py:class:`list`): Arguments to the command.
        hostname (string): The hostname to set on the container.
        env (dict): Environment variables.
        workdir (string): The working directory for commands to run in.
        user (string): The user inside the container.
        labels (dict): A map of labels to associate with the service.
        mounts (:py:class:`list`): A list of specifications for mounts to be
            added to containers created as part of the service. See the
            :py:class:`~docker.types.Mount` class for details.
        stop_grace_period (int): Amount of time to wait for the container to
            terminate before forcefully killing it.
        secrets (:py:class:`list`): List of :py:class:`SecretReference` to be
            made available inside the containers.
        tty (boolean): Whether a pseudo-TTY should be allocated.
        groups (:py:class:`list`): A list of additional groups that the
            container process will run as.
        open_stdin (boolean): Open ``stdin``
        read_only (boolean): Mount the container's root filesystem as read
            only.
        stop_signal (string): Set signal to stop the service's containers
        healthcheck (Healthcheck): Healthcheck
            configuration for this service.
        hosts (:py:class:`dict`): A set of host to IP mappings to add to
            the container's ``hosts`` file.
        dns_config (DNSConfig): Specification for DNS
            related configurations in resolver configuration file.
        configs (:py:class:`list`): List of :py:class:`ConfigReference` that
            will be exposed to the service.
        privileges (Privileges): Security options for the service's containers.
        isolation (string): Isolation technology used by the service's
            containers. Only used for Windows containers.
        init (boolean): Run an init inside the container that forwards signals
            and reaps processes.
        cap_add (:py:class:`list`): A list of kernel capabilities to add to the
            default set for the container.
        cap_drop (:py:class:`list`): A list of kernel capabilities to drop from
            the default set for the container.
        sysctls (:py:class:`dict`): A dict of sysctl values to add to
            the container
    """

    def __init__(
        self,
        image: str,
        command: str | list[str] | None = None,
        args: list[str] | None = None,
        hostname: str | None = None,
        env: dict[str, Incomplete] | list[str] | None = None,
        workdir: str | None = None,
        user: str | None = None,
        labels: dict[Incomplete, Incomplete] | None = None,
        mounts: Iterable[str | Mount] | None = None,
        stop_grace_period: int | None = None,
        secrets: list[SecretReference] | None = None,
        tty: bool | None = None,
        groups: list[Incomplete] | None = None,
        open_stdin: bool | None = None,
        read_only: bool | None = None,
        stop_signal: str | None = None,
        healthcheck: Healthcheck | None = None,
        hosts: Mapping[str, str] | None = None,
        dns_config: DNSConfig | None = None,
        configs: list[ConfigReference] | None = None,
        privileges: Privileges | None = None,
        isolation: str | None = None,
        init: bool | None = None,
        cap_add: list[Incomplete] | None = None,
        cap_drop: list[Incomplete] | None = None,
        sysctls: dict[str, Incomplete] | None = None,
    ) -> None: ...

class Mount(dict[str, Incomplete]):
    """
    Describes a mounted folder's configuration inside a container. A list of
    :py:class:`Mount` would be used as part of a
    :py:class:`~docker.types.ContainerSpec`.

    Args:

        target (string): Container path.
        source (string): Mount source (e.g. a volume name or a host path).
        type (string): The mount type (``bind`` / ``volume`` / ``tmpfs`` /
            ``npipe``). Default: ``volume``.
        read_only (bool): Whether the mount should be read-only.
        consistency (string): The consistency requirement for the mount. One of
        ``default```, ``consistent``, ``cached``, ``delegated``.
        propagation (string): A propagation mode with the value ``[r]private``,
          ``[r]shared``, or ``[r]slave``. Only valid for the ``bind`` type.
        no_copy (bool): False if the volume should be populated with the data
          from the target. Default: ``False``. Only valid for the ``volume``
          type.
        labels (dict): User-defined name and labels for the volume. Only valid
          for the ``volume`` type.
        driver_config (DriverConfig): Volume driver configuration. Only valid
          for the ``volume`` type.
        tmpfs_size (int or string): The size for the tmpfs mount in bytes.
        tmpfs_mode (int): The permission mode for the tmpfs mount.
    """

    def __init__(
        self,
        target: str,
        source: str,
        type: Literal["bind", "volume", "tmpfs", "npipe"] = "volume",
        read_only: bool = False,
        consistency: Literal["default", "consistent", "cached", "delegated"] | None = None,
        propagation: str | None = None,
        no_copy: bool = False,
        labels: dict[Incomplete, Incomplete] | None = None,
        driver_config: DriverConfig | None = None,
        tmpfs_size: int | str | None = None,
        tmpfs_mode: int | None = None,
    ) -> None: ...
    @classmethod
    def parse_mount_string(cls, string: str) -> Mount: ...

class Resources(dict[str, Incomplete]):
    """
    Configures resource allocation for containers when made part of a
    :py:class:`~docker.types.ContainerSpec`.

    Args:

        cpu_limit (int): CPU limit in units of 10^9 CPU shares.
        mem_limit (int): Memory limit in Bytes.
        cpu_reservation (int): CPU reservation in units of 10^9 CPU shares.
        mem_reservation (int): Memory reservation in Bytes.
        generic_resources (dict or :py:class:`list`): Node level generic
          resources, for example a GPU, using the following format:
          ``{ resource_name: resource_value }``. Alternatively, a list of
          of resource specifications as defined by the Engine API.
    """

    def __init__(
        self,
        cpu_limit: int | None = None,
        mem_limit: int | None = None,
        cpu_reservation: int | None = None,
        mem_reservation: int | None = None,
        generic_resources: dict[str, Incomplete] | list[str] | None = None,
    ) -> None: ...

class UpdateConfig(dict[str, Incomplete]):
    """

    Used to specify the way container updates should be performed by a service.

    Args:

        parallelism (int): Maximum number of tasks to be updated in one
          iteration (0 means unlimited parallelism). Default: 0.
        delay (int): Amount of time between updates, in nanoseconds.
        failure_action (string): Action to take if an updated task fails to
          run, or stops running during the update. Acceptable values are
          ``continue``, ``pause``, as well as ``rollback`` since API v1.28.
          Default: ``continue``
        monitor (int): Amount of time to monitor each updated task for
          failures, in nanoseconds.
        max_failure_ratio (float): The fraction of tasks that may fail during
          an update before the failure action is invoked, specified as a
          floating point number between 0 and 1. Default: 0
        order (string): Specifies the order of operations when rolling out an
          updated task. Either ``start-first`` or ``stop-first`` are accepted.
    """

    def __init__(
        self,
        parallelism: int = 0,
        delay: int | None = None,
        failure_action: Literal["pause", "continue", "rollback"] = "continue",
        monitor: int | None = None,
        max_failure_ratio: float | None = None,
        order: Literal["start-first", "stop-first"] | None = None,
    ) -> None: ...

class RollbackConfig(UpdateConfig):
    """
    Used to specify the way container rollbacks should be performed by a
    service

    Args:
        parallelism (int): Maximum number of tasks to be rolled back in one
          iteration (0 means unlimited parallelism). Default: 0
        delay (int): Amount of time between rollbacks, in nanoseconds.
        failure_action (string): Action to take if a rolled back task fails to
          run, or stops running during the rollback. Acceptable values are
          ``continue``, ``pause`` or ``rollback``.
          Default: ``continue``
        monitor (int): Amount of time to monitor each rolled back task for
          failures, in nanoseconds.
        max_failure_ratio (float): The fraction of tasks that may fail during
          a rollback before the failure action is invoked, specified as a
          floating point number between 0 and 1. Default: 0
        order (string): Specifies the order of operations when rolling out a
          rolled back task. Either ``start-first`` or ``stop-first`` are
          accepted.
    """

class RestartConditionTypesEnum:
    NONE: Final = "none"
    ON_FAILURE: Final = "on-failure"
    ANY: Final = "any"

class RestartPolicy(dict[str, Incomplete]):
    """
    Used when creating a :py:class:`~docker.types.ContainerSpec`,
    dictates whether a container should restart after stopping or failing.

    Args:

        condition (string): Condition for restart (``none``, ``on-failure``,
          or ``any``). Default: `none`.
        delay (int): Delay between restart attempts. Default: 0
        max_attempts (int): Maximum attempts to restart a given container
          before giving up. Default value is 0, which is ignored.
        window (int): Time window used to evaluate the restart policy. Default
          value is 0, which is unbounded.
    """

    condition_types: type[RestartConditionTypesEnum]
    def __init__(
        self, condition: Literal["none", "on-failure", "any"] = "none", delay: int = 0, max_attempts: int = 0, window: int = 0
    ) -> None: ...

class DriverConfig(dict[str, Incomplete]):
    """
    Indicates which driver to use, as well as its configuration. Can be used
    as ``log_driver`` in a :py:class:`~docker.types.ContainerSpec`,
    for the `driver_config` in a volume :py:class:`~docker.types.Mount`, or
    as the driver object in
    :py:meth:`create_secret`.

    Args:

        name (string): Name of the driver to use.
        options (dict): Driver-specific options. Default: ``None``.
    """

    def __init__(self, name: str, options: dict[Incomplete, Incomplete] | None = None) -> None: ...

class EndpointSpec(dict[str, Incomplete]):
    """
    Describes properties to access and load-balance a service.

    Args:

        mode (string): The mode of resolution to use for internal load
          balancing between tasks (``'vip'`` or ``'dnsrr'``). Defaults to
          ``'vip'`` if not provided.
        ports (dict): Exposed ports that this service is accessible on from the
          outside, in the form of ``{ published_port: target_port }`` or
          ``{ published_port: <port_config_tuple> }``. Port config tuple format
          is ``(target_port [, protocol [, publish_mode]])``.
          Ports can only be provided if the ``vip`` resolution mode is used.
    """

    def __init__(
        self, mode: str | None = None, ports: Mapping[str, str | tuple[str | None, ...]] | list[dict[str, str]] | None = None
    ) -> None: ...

@overload
def convert_service_ports(ports: list[_T]) -> list[_T]: ...
@overload
def convert_service_ports(ports: Mapping[str, str | tuple[str | None, ...]]) -> list[dict[str, str]]: ...

class ServiceMode(dict[str, Incomplete]):
    """
    Indicate whether a service or a job should be deployed as a replicated
    or global service, and associated parameters

    Args:
        mode (string): Can be either ``replicated``, ``global``,
          ``replicated-job`` or ``global-job``
        replicas (int): Number of replicas. For replicated services only.
        concurrency (int): Number of concurrent jobs. For replicated job
          services only.
    """

    mode: Literal["replicated", "global", "ReplicatedJob", "GlobalJob"]
    def __init__(
        self,
        mode: Literal["replicated", "global", "replicated-job", "global-job"],
        replicas: int | None = None,
        concurrency: int | None = None,
    ) -> None: ...
    @property
    def replicas(self) -> int | None: ...

class SecretReference(dict[str, Incomplete]):
    """
    Secret reference to be used as part of a :py:class:`ContainerSpec`.
    Describes how a secret is made accessible inside the service's
    containers.

    Args:
        secret_id (string): Secret's ID
        secret_name (string): Secret's name as defined at its creation.
        filename (string): Name of the file containing the secret. Defaults
            to the secret's name if not specified.
        uid (string): UID of the secret file's owner. Default: 0
        gid (string): GID of the secret file's group. Default: 0
        mode (int): File access mode inside the container. Default: 0o444
    """

    def __init__(
        self,
        secret_id: str,
        secret_name: str,
        filename: str | None = None,
        uid: str | None = None,
        gid: str | None = None,
        mode: int = 292,
    ) -> None: ...

class ConfigReference(dict[str, Incomplete]):
    """
    Config reference to be used as part of a :py:class:`ContainerSpec`.
    Describes how a config is made accessible inside the service's
    containers.

    Args:
        config_id (string): Config's ID
        config_name (string): Config's name as defined at its creation.
        filename (string): Name of the file containing the config. Defaults
            to the config's name if not specified.
        uid (string): UID of the config file's owner. Default: 0
        gid (string): GID of the config file's group. Default: 0
        mode (int): File access mode inside the container. Default: 0o444
    """

    def __init__(
        self,
        config_id: str,
        config_name: str,
        filename: str | None = None,
        uid: str | None = None,
        gid: str | None = None,
        mode: int = 292,
    ) -> None: ...

class Placement(dict[str, Incomplete]):
    """
    Placement constraints to be used as part of a :py:class:`TaskTemplate`

    Args:
        constraints (:py:class:`list` of str): A list of constraints
        preferences (:py:class:`list` of tuple): Preferences provide a way
            to make the scheduler aware of factors such as topology. They
            are provided in order from highest to lowest precedence and
            are expressed as ``(strategy, descriptor)`` tuples. See
            :py:class:`PlacementPreference` for details.
        maxreplicas (int): Maximum number of replicas per node
        platforms (:py:class:`list` of tuple): A list of platforms
            expressed as ``(arch, os)`` tuples
    """

    def __init__(
        self,
        constraints: list[str] | None = None,
        preferences: Iterable[tuple[str, str] | PlacementPreference] | None = None,
        platforms: Iterable[tuple[str, str]] | None = None,
        maxreplicas: int | None = None,
    ) -> None: ...

class PlacementPreference(dict[str, Incomplete]):
    """
    Placement preference to be used as an element in the list of
    preferences for :py:class:`Placement` objects.

    Args:
        strategy (string): The placement strategy to implement. Currently,
            the only supported strategy is ``spread``.
        descriptor (string): A label descriptor. For the spread strategy,
            the scheduler will try to spread tasks evenly over groups of
            nodes identified by this label.
    """

    def __init__(self, strategy: Literal["spread"], descriptor: str) -> None: ...

class DNSConfig(dict[str, Incomplete]):
    """
    Specification for DNS related configurations in resolver configuration
    file (``resolv.conf``). Part of a :py:class:`ContainerSpec` definition.

    Args:
        nameservers (:py:class:`list`): The IP addresses of the name
            servers.
        search (:py:class:`list`): A search list for host-name lookup.
        options (:py:class:`list`): A list of internal resolver variables
            to be modified (e.g., ``debug``, ``ndots:3``, etc.).
    """

    def __init__(
        self, nameservers: list[str] | None = None, search: list[str] | None = None, options: list[str] | None = None
    ) -> None: ...

class Privileges(dict[str, Incomplete]):
    """
    Security options for a service's containers.
    Part of a :py:class:`ContainerSpec` definition.

    Args:
        credentialspec_file (str): Load credential spec from this file.
            The file is read by the daemon, and must be present in the
            CredentialSpecs subdirectory in the docker data directory,
            which defaults to ``C:\\ProgramData\\Docker\\`` on Windows.
            Can not be combined with credentialspec_registry.

        credentialspec_registry (str): Load credential spec from this value
            in the Windows registry. The specified registry value must be
            located in: ``HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion
            \\Virtualization\\Containers\\CredentialSpecs``.
            Can not be combined with credentialspec_file.

        selinux_disable (boolean): Disable SELinux
        selinux_user (string): SELinux user label
        selinux_role (string): SELinux role label
        selinux_type (string): SELinux type label
        selinux_level (string): SELinux level label
    """

    def __init__(
        self,
        credentialspec_file: str | None = None,
        credentialspec_registry: str | None = None,
        selinux_disable: bool | None = None,
        selinux_user: str | None = None,
        selinux_role: str | None = None,
        selinux_type: str | None = None,
        selinux_level: str | None = None,
    ) -> None: ...

class NetworkAttachmentConfig(dict[str, Incomplete]):
    """
    Network attachment options for a service.

    Args:
        target (str): The target network for attachment.
            Can be a network name or ID.
        aliases (:py:class:`list`): A list of discoverable alternate names
            for the service.
        options (:py:class:`dict`): Driver attachment options for the
            network target.
    """

    def __init__(self, target: str, aliases: list[str] | None = None, options: dict[str, Incomplete] | None = None) -> None: ...
