from _typeshed import Incomplete

from aws_xray_sdk.core.context import Context

from .sampling_rule import SamplingRule

class ServiceConnector:
    """
    Connector class that translates Centralized Sampling poller functions to
    actual X-Ray back-end APIs and communicates with X-Ray daemon as the
    signing proxy.
    """

    def __init__(self) -> None: ...
    def fetch_sampling_rules(self) -> list[SamplingRule]: ...
    def fetch_sampling_target(self, rules) -> tuple[Incomplete, int]: ...
    def setup_xray_client(self, ip: str, port: str | int, client) -> None:
        """
        Setup the xray client based on ip and port.
        If a preset client is specified, ip and port
        will be ignored.
        """

    @property
    def context(self) -> Context: ...
    @context.setter
    def context(self, v: Context) -> None: ...
