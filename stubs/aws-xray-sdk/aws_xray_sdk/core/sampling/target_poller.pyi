from logging import Logger

log: Logger

class TargetPoller:
    """
    The poller to report the current statistics of all
    centralized sampling rules and retrieve the new allocated
    sampling quota and TTL from X-Ray service.
    """

    def __init__(self, cache, rule_poller, connector) -> None: ...
    def start(self) -> None: ...
