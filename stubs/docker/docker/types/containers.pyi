from _typeshed import Incomplete
from collections.abc import Iterable, Mapping
from typing import Any, Final, Literal

from docker._types import ContainerWeightDevice

from .. import errors
from .base import DictType
from .healthcheck import Healthcheck
from .networks import NetworkingConfig
from .services import Mount

class LogConfigTypesEnum:
    JSON: Final = "json-file"
    SYSLOG: Final = "syslog"
    JOURNALD: Final = "journald"
    GELF: Final = "gelf"
    FLUENTD: Final = "fluentd"
    NONE: Final = "none"

class LogConfig(DictType):
    """
    Configure logging for a container, when provided as an argument to
    :py:meth:`~docker.api.container.ContainerApiMixin.create_host_config`.
    You may refer to the
    `official logging driver documentation <https://docs.docker.com/config/containers/logging/configure/>`_
    for more information.

    Args:
        type (str): Indicate which log driver to use. A set of valid drivers
            is provided as part of the :py:attr:`LogConfig.types`
            enum. Other values may be accepted depending on the engine version
            and available logging plugins.
        config (dict): A driver-dependent configuration dictionary. Please
            refer to the driver's documentation for a list of valid config
            keys.

    Example:

        >>> from docker.types import LogConfig
        >>> lc = LogConfig(type=LogConfig.types.JSON, config={
        ...   'max-size': '1g',
        ...   'labels': 'production_status,geo'
        ... })
        >>> hc = client.create_host_config(log_config=lc)
        >>> container = client.create_container('busybox', 'true',
        ...    host_config=hc)
        >>> client.inspect_container(container)['HostConfig']['LogConfig']
        {
            'Type': 'json-file',
            'Config': {'labels': 'production_status,geo', 'max-size': '1g'}
        }
    """

    types: type[LogConfigTypesEnum]
    def __init__(self, **kwargs) -> None: ...
    @property
    def type(self): ...
    @type.setter
    def type(self, value) -> None: ...
    @property
    def config(self): ...
    def set_config_value(self, key, value) -> None:
        """Set a the value for ``key`` to ``value`` inside the ``config``
        dict.
        """

    def unset_config(self, key) -> None:
        """Remove the ``key`` property from the ``config`` dict."""

class Ulimit(DictType):
    """
    Create a ulimit declaration to be used with
    :py:meth:`~docker.api.container.ContainerApiMixin.create_host_config`.

    Args:

        name (str): Which ulimit will this apply to. The valid names can be
            found in '/etc/security/limits.conf' on a gnu/linux system.
        soft (int): The soft limit for this ulimit. Optional.
        hard (int): The hard limit for this ulimit. Optional.

    Example:

        >>> nproc_limit = docker.types.Ulimit(name='nproc', soft=1024)
        >>> hc = client.create_host_config(ulimits=[nproc_limit])
        >>> container = client.create_container(
                'busybox', 'true', host_config=hc
            )
        >>> client.inspect_container(container)['HostConfig']['Ulimits']
        [{'Name': 'nproc', 'Hard': 0, 'Soft': 1024}]

    """

    def __init__(self, **kwargs) -> None: ...
    @property
    def name(self): ...
    @name.setter
    def name(self, value) -> None: ...
    @property
    def soft(self): ...
    @soft.setter
    def soft(self, value) -> None: ...
    @property
    def hard(self): ...
    @hard.setter
    def hard(self, value) -> None: ...

class DeviceRequest(DictType):
    """
    Create a device request to be used with
    :py:meth:`~docker.api.container.ContainerApiMixin.create_host_config`.

    Args:

        driver (str): Which driver to use for this device. Optional.
        count (int): Number or devices to request. Optional.
            Set to -1 to request all available devices.
        device_ids (list): List of strings for device IDs. Optional.
            Set either ``count`` or ``device_ids``.
        capabilities (list): List of lists of strings to request
            capabilities. Optional. The global list acts like an OR,
            and the sub-lists are AND. The driver will try to satisfy
            one of the sub-lists.
            Available capabilities for the ``nvidia`` driver can be found
            `here <https://github.com/NVIDIA/nvidia-container-runtime>`_.
        options (dict): Driver-specific options. Optional.
    """

    def __init__(self, **kwargs) -> None: ...
    @property
    def driver(self): ...
    @driver.setter
    def driver(self, value) -> None: ...
    @property
    def count(self): ...
    @count.setter
    def count(self, value) -> None: ...
    @property
    def device_ids(self): ...
    @device_ids.setter
    def device_ids(self, value) -> None: ...
    @property
    def capabilities(self): ...
    @capabilities.setter
    def capabilities(self, value) -> None: ...
    @property
    def options(self): ...
    @options.setter
    def options(self, value) -> None: ...

class HostConfig(dict[str, Incomplete]):
    def __init__(
        self,
        version: str,
        binds: dict[str, Mapping[str, str]] | list[str] | None = None,
        port_bindings: Mapping[int | str, Incomplete] | None = None,
        lxc_conf: dict[str, Incomplete] | list[dict[str, Incomplete]] | None = None,
        publish_all_ports: bool = False,
        links: dict[str, str] | dict[str, None] | dict[str, str | None] | Iterable[tuple[str, str | None]] | None = None,
        privileged: bool = False,
        dns: list[str] | None = None,
        dns_search: list[str] | None = None,
        volumes_from: list[str] | None = None,
        network_mode: str | None = None,
        restart_policy: Mapping[str, str | int] | None = None,
        cap_add: list[str] | None = None,
        cap_drop: list[str] | None = None,
        devices: list[str] | None = None,
        extra_hosts: dict[str, Incomplete] | list[Incomplete] | None = None,
        read_only: bool | None = None,
        pid_mode: str | None = None,
        ipc_mode: str | None = None,
        security_opt: list[str] | None = None,
        ulimits: list[Ulimit] | None = None,
        log_config: LogConfig | None = None,
        mem_limit: str | int | None = None,
        memswap_limit: str | int | None = None,
        mem_reservation: str | int | None = None,
        kernel_memory: str | int | None = None,
        mem_swappiness: int | None = None,
        cgroup_parent: str | None = None,
        group_add: Iterable[str | int] | None = None,
        cpu_quota: int | None = None,
        cpu_period: int | None = None,
        blkio_weight: int | None = None,
        blkio_weight_device: list[ContainerWeightDevice] | None = None,
        device_read_bps: list[Mapping[str, str | int]] | None = None,
        device_write_bps: list[Mapping[str, str | int]] | None = None,
        device_read_iops: list[Mapping[str, str | int]] | None = None,
        device_write_iops: list[Mapping[str, str | int]] | None = None,
        oom_kill_disable: bool = False,
        shm_size: str | int | None = None,
        sysctls: dict[str, str] | None = None,
        tmpfs: dict[str, str] | None = None,
        oom_score_adj: int | None = None,
        dns_opt: list[Incomplete] | None = None,
        cpu_shares: int | None = None,
        cpuset_cpus: str | None = None,
        userns_mode: str | None = None,
        uts_mode: str | None = None,
        pids_limit: int | None = None,
        isolation: str | None = None,
        auto_remove: bool = False,
        storage_opt: dict[Incomplete, Incomplete] | None = None,
        init: bool | None = None,
        init_path: str | None = None,
        volume_driver: str | None = None,
        cpu_count: int | None = None,
        cpu_percent: int | None = None,
        nano_cpus: int | None = None,
        cpuset_mems: str | None = None,
        runtime: str | None = None,
        mounts: list[Mount] | None = None,
        cpu_rt_period: int | None = None,
        cpu_rt_runtime: int | None = None,
        device_cgroup_rules: list[Incomplete] | None = None,
        device_requests: list[DeviceRequest] | None = None,
        cgroupns: Literal["private", "host"] | None = None,
    ) -> None: ...

def host_config_type_error(param: str, param_value: object, expected: str) -> TypeError: ...
def host_config_version_error(param: str, version: str, less_than: bool = True) -> errors.InvalidVersion: ...
def host_config_value_error(param: str, param_value: object) -> ValueError: ...
def host_config_incompatible_error(param: str, param_value: str, incompatible_param: str) -> errors.InvalidArgument: ...

class ContainerConfig(dict[str, Incomplete]):
    def __init__(
        self,
        version: str,
        image: str,
        command: str | list[str],
        hostname: str | None = None,
        user: str | int | None = None,
        detach: bool = False,
        stdin_open: bool = False,
        tty: bool = False,
        # list is invariant, enumerating all possible union combination would be too complex for:
        # list[str | int | tuple[int | str, str] | tuple[int | str, ...]]
        ports: dict[str, dict[Incomplete, Incomplete]] | list[Any] | None = None,
        environment: dict[str, str] | list[str] | None = None,
        volumes: str | list[str] | None = None,
        network_disabled: bool = False,
        entrypoint: str | list[str] | None = None,
        working_dir: str | None = None,
        domainname: str | None = None,
        host_config: HostConfig | None = None,
        mac_address: str | None = None,
        labels: dict[str, str] | list[str] | None = None,
        stop_signal: str | None = None,
        networking_config: NetworkingConfig | None = None,
        healthcheck: Healthcheck | None = None,
        stop_timeout: int | None = None,
        runtime: str | None = None,
    ) -> None: ...
