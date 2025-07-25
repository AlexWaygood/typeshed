from _typeshed import Incomplete
from typing import Any

from .services import DriverConfig

class SwarmSpec(dict[str, Any]):
    """
    Describe a Swarm's configuration and options. Use
    :py:meth:`~docker.api.swarm.SwarmApiMixin.create_swarm_spec`
    to instantiate.
    """

    def __init__(
        self,
        version: str,
        task_history_retention_limit: int | None = None,
        snapshot_interval: int | None = None,
        keep_old_snapshots: int | None = None,
        log_entries_for_slow_followers: int | None = None,
        heartbeat_tick: int | None = None,
        election_tick: int | None = None,
        dispatcher_heartbeat_period: int | None = None,
        node_cert_expiry: int | None = None,
        external_cas: list[SwarmExternalCA] | None = None,
        name: str | None = None,
        labels: dict[str, Incomplete] | None = None,
        signing_ca_cert: str | None = None,
        signing_ca_key: str | None = None,
        ca_force_rotate: int | None = None,
        autolock_managers: bool | None = None,
        log_driver: DriverConfig | None = None,
    ) -> None: ...

class SwarmExternalCA(dict[str, Any]):
    """
    Configuration for forwarding signing requests to an external
    certificate authority.

    Args:
        url (string): URL where certificate signing requests should be
            sent.
        protocol (string): Protocol for communication with the external CA.
        options (dict): An object with key/value pairs that are interpreted
            as protocol-specific options for the external CA driver.
        ca_cert (string): The root CA certificate (in PEM format) this
            external CA uses to issue TLS certificates (assumed to be to
            the current swarm root CA certificate if not provided).



    """

    def __init__(
        self,
        url: str,
        protocol: str | None = None,
        options: dict[Incomplete, Incomplete] | None = None,
        ca_cert: str | None = None,
    ) -> None: ...
