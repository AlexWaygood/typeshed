from logging import Logger

log: Logger

class DefaultSampler:
    """Making sampling decisions based on centralized sampling rules defined
    by X-Ray control plane APIs. It will fall back to local sampler if
    centralized sampling rules are not available.
    """

    def __init__(self) -> None: ...
    def start(self) -> None:
        """
        Start rule poller and target poller once X-Ray daemon address
        and context manager is in place.
        """

    def should_trace(self, sampling_req=None):
        """
        Return the matched sampling rule name if the sampler finds one
        and decide to sample. If no sampling rule matched, it falls back
        to the local sampler's ``should_trace`` implementation.
        All optional arguments are extracted from incoming requests by
        X-Ray middleware to perform path based sampling.
        """

    def load_local_rules(self, rules) -> None:
        """
        Load specified local rules to local fallback sampler.
        """

    def load_settings(self, daemon_config, context, origin=None) -> None:
        """
        The pollers have dependency on the context manager
        of the X-Ray recorder. They will respect the customer
        specified xray client to poll sampling rules/targets.
        Otherwise they falls back to use the same X-Ray daemon
        as the emitter.
        """

    @property
    def xray_client(self): ...
    @xray_client.setter
    def xray_client(self, v) -> None: ...
